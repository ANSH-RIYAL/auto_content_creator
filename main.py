import random
import os
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip, concatenate_audioclips
from gtts import gTTS
from pydub import AudioSegment

def list_background_videos():
    data_dir = "./data"
    videos = [f for f in os.listdir(data_dir) if f.endswith(('.mp4', '.webm'))]
    return videos

def list_background_music():
    music_dir = "./data/background_music"
    if not os.path.exists(music_dir):
        os.makedirs(music_dir)
    music_files = [f for f in os.listdir(music_dir) if f.endswith(('.mp3', '.wav'))]
    return music_files

def passage_to_audio(passage, out_path="narration.mp3"):
    tts = gTTS(passage)
    tts.save(out_path)
    return out_path

def get_audio_duration(audio_path):
    audio = AudioSegment.from_file(audio_path)
    return audio.duration_seconds

def get_random_clip(video_path, duration):
    video = VideoFileClip(video_path)
    max_start = max(0, video.duration - duration)
    start = random.uniform(0, max_start)
    end = start + duration
    return video.subclip(start, end)

def create_text_clips(title, content, video_size, duration, font_size=96):
    # Create title clip with larger font size
    title_clip = TextClip(
        title,
        fontsize=font_size + 20,  # Title font size is 20px larger than content
        color='white',
        font='Arial-Bold',
        stroke_color='black',
        stroke_width=2,
        size=(int(video_size[0] * 0.9), None),
        method='caption'
    ).set_position(('center', 'top')).set_start(0).set_duration(duration)
    
    # Process content
    words = content.split()
    lines = []
    line = ""
    for word in words:
        if len(line + " " + word) < 40:
            line += " " + word
        else:
            lines.append(line.strip())
            line = word
    if line:
        lines.append(line.strip())
    
    # Calculate timing for content
    content_duration = duration - 2
    per_line = content_duration / len(lines) if lines else 0
    
    # Create content clips
    text_clips = [title_clip]
    for i, l in enumerate(lines):
        txt_clip = TextClip(
            l,
            fontsize=font_size,
            color='white',
            font='Arial-Bold',
            stroke_color='black',
            stroke_width=2,
            size=(int(video_size[0] * 0.9), None),
            method='caption'
        ).set_position(('center', 'bottom')).set_start(2 + i * per_line).set_duration(per_line)
        text_clips.append(txt_clip)
    
    return text_clips

def make_video(title, content, background_video, output_path="final_video.mp4", font_size=96, background_music=None):
    # Create videos directory if it doesn't exist
    videos_dir = "./videos"
    if not os.path.exists(videos_dir):
        os.makedirs(videos_dir)
    
    # Create a safe filename from the title
    safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
    safe_title = safe_title.replace(' ', '_')
    
    # Set the output path in the videos directory
    output_path = os.path.join(videos_dir, f"{safe_title}.mp4")
    
    MASTER_VIDEO = f"./data/{background_video}"
    
    # Combine title and content for audio
    full_text = f"{title}\n{content}"
    audio_path = passage_to_audio(full_text)
    audio_duration = get_audio_duration(audio_path)
    
    # Ensure minimum duration of 10 seconds
    video_duration = max(audio_duration, 10)
    
    video_clip = get_random_clip(MASTER_VIDEO, video_duration)
    text_clips = create_text_clips(title, content, video_clip.size, video_duration, font_size=font_size)
    audio_clip = AudioFileClip(audio_path).set_duration(video_duration)
    
    # Add background music if provided
    if background_music:
        bg_music = AudioFileClip(background_music)
        # Loop the background music if needed
        if bg_music.duration < video_duration:
            bg_music = bg_music.loop(duration=video_duration)
        else:
            bg_music = bg_music.subclip(0, video_duration)
        # Lower the volume of background music
        bg_music = bg_music.volumex(0.3)
        # Combine audio
        audio_clip = concatenate_audioclips([audio_clip, bg_music])
    
    final = CompositeVideoClip(
        [video_clip] + text_clips
    ).set_audio(audio_clip)
    
    final.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac",
        fps=30,
        threads=4,
        preset='medium'
    )
    os.remove(audio_path)
    return output_path

if __name__ == "__main__":
    print("Recipe Video Creator")
    print("-------------------")
    
    # List available background videos
    print("\nAvailable background videos:")
    videos = list_background_videos()
    for i, video in enumerate(videos, 1):
        print(f"{i}. {video}")
    
    # Get user selection for background video
    while True:
        try:
            choice = int(input("\nSelect background video (enter number): "))
            if 1 <= choice <= len(videos):
                selected_video = videos[choice-1]
                break
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Please enter a valid number.")
    
    # List available background music
    print("\nAvailable background music:")
    music_files = list_background_music()
    if music_files:
        for i, music in enumerate(music_files, 1):
            print(f"{i}. {music}")
        print(f"{len(music_files) + 1}. No background music")
        
        # Get user selection for background music
        while True:
            try:
                music_choice = int(input("\nSelect background music (enter number): "))
                if 1 <= music_choice <= len(music_files):
                    selected_music = f"./data/background_music/{music_files[music_choice-1]}"
                    break
                elif music_choice == len(music_files) + 1:
                    selected_music = None
                    break
                else:
                    print("Invalid selection. Please try again.")
            except ValueError:
                print("Please enter a valid number.")
    else:
        print("No background music files found in ./data/background_music/")
        selected_music = None
    
    # Get font size
    while True:
        try:
            font_size = int(input("\nEnter font size (48-144): "))
            if 48 <= font_size <= 144:
                break
            else:
                print("Font size must be between 48 and 144.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Get title and content separately
    print("\nEnter the recipe title:")
    title = input("Title: ")
    
    print("\nEnter the recipe content (press Enter twice to finish):")
    content_lines = []
    while True:
        line = input()
        if line == "" and content_lines and content_lines[-1] == "":
            break
        content_lines.append(line)
    
    content = "\n".join(content_lines)
    
    output_path = make_video(title, content, selected_video, font_size=font_size, background_music=selected_music)
    print(f"Video created as {output_path}") 
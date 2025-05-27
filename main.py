import random
import os
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip
from gtts import gTTS
from pydub import AudioSegment

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

def create_text_clips(passage, video_size, duration, font_size=48):
    words = passage.split()
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
    per_line = duration / len(lines)
    text_clips = []
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
        ).set_position(('center', 'bottom')).set_start(i * per_line).set_duration(per_line)
        text_clips.append(txt_clip)
    return text_clips

def make_video(passage, output_path="final_video.mp4", font_size=48):
    MASTER_VIDEO = "./data/master_background_video.webm"
    audio_path = passage_to_audio(passage)
    audio_duration = get_audio_duration(audio_path)
    video_clip = get_random_clip(MASTER_VIDEO, audio_duration)
    text_clips = create_text_clips(passage, video_clip.size, audio_duration, font_size=font_size)
    audio_clip = AudioFileClip(audio_path).set_duration(audio_duration)
    final = CompositeVideoClip(
        [video_clip] + text_clips
    ).set_audio(audio_clip)
    final.write_videofile(output_path, codec="libx264", audio_codec="aac", fps=30)
    os.remove(audio_path)

if __name__ == "__main__":
    passage = input("Enter your passage: ")
    make_video(passage)
    print("Video created as final_video.mp4") 
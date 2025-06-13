import os
import requests
from tqdm import tqdm

def download_file(url, filename):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(filename, 'wb') as f, tqdm(
        desc=filename,
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as pbar:
        for data in response.iter_content(chunk_size=1024):
            size = f.write(data)
            pbar.update(size)

def main():
    # Create music directory if it doesn't exist
    music_dir = "./data/background_music"
    if not os.path.exists(music_dir):
        os.makedirs(music_dir)
    
    # List of music files to download (replace with actual URLs)
    music_files = {
        "Indian_Fusion.mp3": "https://example.com/indian_fusion.mp3",
        "Spice_Market.mp3": "https://example.com/spice_market.mp3",
        "Kitchen_Melody.mp3": "https://example.com/kitchen_melody.mp3",
        "Curry_House.mp3": "https://example.com/curry_house.mp3",
        "Spice_Route.mp3": "https://example.com/spice_route.mp3",
        "Tandoori_Beats.mp3": "https://example.com/tandoori_beats.mp3",
        "Masala_Mix.mp3": "https://example.com/masala_mix.mp3",
        "Spice_Garden.mp3": "https://example.com/spice_garden.mp3",
        "Curry_Corner.mp3": "https://example.com/curry_corner.mp3",
        "Indian_Kitchen.mp3": "https://example.com/indian_kitchen.mp3"
    }
    
    print("Downloading background music files...")
    for filename, url in music_files.items():
        filepath = os.path.join(music_dir, filename)
        try:
            download_file(url, filepath)
            print(f"Successfully downloaded {filename}")
        except Exception as e:
            print(f"Error downloading {filename}: {str(e)}")

if __name__ == "__main__":
    main() 
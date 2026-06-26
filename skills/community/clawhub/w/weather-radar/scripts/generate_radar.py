import requests
import io
import math
import sys
from datetime import datetime
from PIL import Image, ImageDraw

def deg2num(lat_deg, lon_deg, zoom):
    """Calculate map tile coordinates from latitude/longitude."""
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return (xtile, ytile)

def download_tile(url, is_osm=False):
    """Download a tile and return as a PIL Image object."""
    headers = {"User-Agent": "OpenClaw-WeatherRadar/1.0 (contact@openclaw.ai)"} if is_osm else {}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            return Image.open(io.BytesIO(resp.content)).convert("RGBA")
        else:
            return Image.new("RGBA", (256, 256), (0,0,0,0))
    except Exception as e:
        return Image.new("RGBA", (256, 256), (0,0,0,0))

def create_radar_gif(lat, lon, zoom=7, output="radar_map.gif", num_frames=6):
    """
    Generate an animated GIF radar map by stitching OSM tiles and RainViewer radar.
    """
    # 1. Fetch radar timestamps
    try:
        rv_api = requests.get("https://api.rainviewer.com/public/weather-maps.json").json()
        rv_host = rv_api["host"]
        # Get the last N frames
        past_data = rv_api["radar"]["past"][-num_frames:]
    except Exception as e:
        print(f"Error fetching RainViewer API: {e}")
        sys.exit(1)

    cx, cy = deg2num(lat, lon, zoom)

    # 2. Download Base Map (OSM) - Only do this once to save time and API calls
    print("Downloading OSM base map...")
    base_map = Image.new("RGBA", (256 * 3, 256 * 3))
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            x = cx + dx
            y = cy + dy
            canvas_x = (dx + 1) * 256
            canvas_y = (dy + 1) * 256
            osm_url = f"https://tile.openstreetmap.org/{zoom}/{x}/{y}.png"
            osm_tile = download_tile(osm_url, is_osm=True)
            base_map.paste(osm_tile, (canvas_x, canvas_y))

    # 3. Download Radar frames and composite
    gif_frames = []
    print(f"Downloading {len(past_data)} radar frames...")
    
    for frame_meta in past_data:
        path = frame_meta["path"]
        ts = frame_meta["time"]
        
        radar_img = Image.new("RGBA", (256 * 3, 256 * 3))
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                x = cx + dx
                y = cy + dy
                canvas_x = (dx + 1) * 256
                canvas_y = (dy + 1) * 256
                radar_url = f"{rv_host}{path}/256/{zoom}/{x}/{y}/2/1_1.png"
                radar_tile = download_tile(radar_url)
                radar_img.paste(radar_tile, (canvas_x, canvas_y))
        
        # Composite radar over base map
        frame = Image.alpha_composite(base_map.copy(), radar_img)
        
        # Draw timestamp
        draw = ImageDraw.Draw(frame)
        dt_str = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        
        # Draw text with a simple black outline for visibility
        for offset in [(1,1), (-1,-1), (1,-1), (-1,1)]:
            draw.text((10+offset[0], 10+offset[1]), dt_str, fill="black")
        draw.text((10, 10), dt_str, fill="white")
        
        # Convert to RGB (required for saving as GIF)
        gif_frames.append(frame.convert("RGB"))

    # 4. Save GIF
    print(f"Saving GIF to {output}...")
    gif_frames[0].save(
        output,
        save_all=True,
        append_images=gif_frames[1:],
        duration=600, # 600ms per frame
        loop=0 # Infinite loop
    )
    print(f"Success! Map saved to {output}.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate an animated weather radar map (GIF).")
    parser.add_argument("--lat", type=float, default=39.9042, help="Latitude (default: Beijing 39.9042)")
    parser.add_argument("--lon", type=float, default=116.4074, help="Longitude (default: Beijing 116.4074)")
    parser.add_argument("--zoom", type=int, default=7, help="Zoom level (default: 7)")
    parser.add_argument("--frames", type=int, default=8, help="Number of historical frames to include")
    parser.add_argument("--out", type=str, default="radar_map.gif", help="Output file path (.gif)")
    args = parser.parse_args()
    
    create_radar_gif(args.lat, args.lon, args.zoom, args.out, args.frames)
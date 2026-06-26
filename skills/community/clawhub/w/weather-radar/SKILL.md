---
name: weather-radar
description: Fetch and generate an image of the current weather radar combined with a base map. Use when the user wants to see a rain/weather radar map, current precipitation clouds, or radar overlay for a specific city or coordinates. Default zoom level is 7, which is optimal for macroscopic weather phenomena.
---

# Weather Radar

This skill provides a way to generate a composite animated GIF showing current and historical weather radar data overlaid on a real geographic base map (OpenStreetMap). It fetches real-time radar layers from RainViewer.

## How to Use

When the user asks for a weather radar map or animated cloud GIF for a location, run the Python script `scripts/generate_radar.py` to create the animation. It outputs a composite 3x3 tile grid (768x768 pixels).

### Executing the script

First, look up the latitude and longitude of the requested city or use the provided coordinates. If no city is specified, default to the user's known location or a sensible default.

```bash
# Example for Beijing
python scripts/generate_radar.py --lat 39.9042 --lon 116.4074 --zoom 7 --out /home/ubuntu/.openclaw/workspace/radar_map.gif
```

Parameters:
- `--lat`: Latitude of the center point (float)
- `--lon`: Longitude of the center point (float)
- `--zoom`: Zoom level (default: 7). **Note: Zoom 7 is optimal for weather systems. Higher zooms (like 9 or 10) often result in empty/missing radar tiles from the API.**
- `--frames`: Number of frames to animate (default: 8, representing roughly the last 80 minutes).
- `--out`: Output path for the generated GIF image (must end in `.gif`).

### Sending the result

After generating the `radar_map.gif`, send it to the user using the `message` tool with `action="send"`, `asDocument=true`, and the `filePath` parameter set to the output image path.

### Dependencies

The script requires `requests` and `Pillow`. If they are not installed, run `pip install requests Pillow` before executing the script.

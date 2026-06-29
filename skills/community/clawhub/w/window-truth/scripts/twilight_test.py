#!/usr/bin/env python3
"""
Window Truth - Twilight Test
Detects conflicts between weather app and local window observation.
"""
import json
import subprocess
import requests
from datetime import datetime
from pathlib import Path

# Config - override via environment variables
import os
RTSP_URL = os.getenv("RTSP_URL", "rtsp://admin:pass@192.168.1.247:554/stream2")
FFMPEG = os.getenv("FFMPEG", "/usr/local/bin/ffmpeg")
LAT = float(os.getenv("LAT", "22.54"))
LON = float(os.getenv("LON", "114.06"))
DATA_FILE = Path("data/twilight_predictions.jsonl")

def capture_photo():
    """Capture single frame from RTSP, return JPEG bytes."""
    cmd = [
        FFMPEG, "-y", "-rtsp_transport", "tcp",
        "-i", RTSP_URL,
        "-frames:v", "1", "-f", "image2", "-"
    ]
    result = subprocess.run(cmd, capture_output=True)
    return result.stdout

def capture_audio(duration=3):
    """Capture audio from RTSP, return WAV bytes."""
    cmd = [
        FFMPEG, "-y", "-rtsp_transport", "tcp",
        "-i", RTSP_URL,
        "-t", str(duration), "-f", "wav", "-acodec", "pcm_s16le",
        "-ar", "8000", "-ac", "1", "-"
    ]
    result = subprocess.run(cmd, capture_output=True)
    return result.stdout

def calculate_brightness(jpeg_bytes):
    """Calculate average brightness from JPEG (simplified)."""
    # In practice, use PIL or similar
    # This is a placeholder - actual implementation would decode JPEG
    import struct
    # Placeholder: file size as proxy (larger = brighter for daytime)
    return len(jpeg_bytes) / 1000  # Rough KB

def calculate_rms(wav_bytes):
    """Calculate RMS from WAV audio."""
    import struct
    # Skip WAV header (44 bytes)
    samples = struct.iter_unpack('<h', wav_bytes[44:])
    values = [abs(s[0]) for s in samples]
    if not values:
        return 0
    return (sum(v*v for v in values) / len(values)) ** 0.5

def get_weather():
    """Get weather forecast from Open-Meteo."""
    url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current=temperature_2m,cloud_cover,precipitation_probability,weather_code"
    resp = requests.get(url, timeout=10)
    return resp.json()

def detect_conflicts(brightness, rms, weather):
    """Detect conflicts between window and app."""
    conflicts = []
    current = weather.get("current", {})
    precip = current.get("precipitation_probability", 0) or 0
    clouds = current.get("cloud_cover", 0) or 0
    
    # RAIN_GONE: App says rain, window says dry
    if precip > 30 and brightness > 100 and rms < 15:
        conflicts.append({
            "type": "RAIN_GONE",
            "app_precip": precip,
            "window_brightness": brightness,
            "window_rms": rms
        })
    
    # HIDDEN_RAIN: App says dry, window hears rain
    if precip < 5 and rms > 40:
        conflicts.append({
            "type": "HIDDEN_RAIN", 
            "app_precip": precip,
            "window_rms": rms
        })
    
    # THIN_CLOUD: App says overcast, window says bright
    if clouds > 90 and brightness > 100:
        conflicts.append({
            "type": "THIN_CLOUD",
            "app_clouds": clouds,
            "window_brightness": brightness
        })
    
    return conflicts

def main():
    print("Window Truth - Twilight Test")
    print("=" * 40)
    
    # Capture
    print("Capturing photo...")
    photo = capture_photo()
    brightness = calculate_brightness(photo)
    print(f"  Brightness: {brightness:.1f} KB")
    
    print("Capturing audio...")
    audio = capture_audio(3)
    rms = calculate_rms(audio)
    print(f"  RMS: {rms:.1f}")
    
    # Get weather
    print("Fetching weather...")
    weather = get_weather()
    current = weather.get("current", {})
    print(f"  Temp: {current.get('temperature_2m', '?')}°C")
    print(f"  Clouds: {current.get('cloud_cover', '?')}%")
    print(f"  Precip prob: {current.get('precipitation_probability', '?')}%")
    
    # Detect conflicts
    conflicts = detect_conflicts(brightness, rms, weather)
    
    # Record prediction
    record = {
        "timestamp": datetime.now().isoformat(),
        "perception": {
            "brightness": round(brightness, 1),
            "rms": round(rms, 1)
        },
        "weather_app": {
            "temp": current.get("temperature_2m"),
            "clouds": current.get("cloud_cover"),
            "precip_prob": current.get("precipitation_probability")
        },
        "conflicts": conflicts,
        "predictions": [
            {"who": "window", "prediction": "no_rain" if brightness > 100 and rms < 15 else "possible_rain"}
        ],
        "verified": False
    }
    
    # Save
    DATA_FILE.parent.mkdir(exist_ok=True)
    with open(DATA_FILE, "a") as f:
        f.write(json.dumps(record) + "\n")
    
    # Output
    print()
    print("Conflicts detected:" if conflicts else "No conflicts detected.")
    for c in conflicts:
        print(f"  - {c['type']}: {c}")
    
    return record

if __name__ == "__main__":
    main()

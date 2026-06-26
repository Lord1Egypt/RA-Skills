#!/bin/bash
# extract-frames.sh — Extract video frames at specific timestamps
# Usage: ./extract-frames.sh <video_file> <output_dir> <timestamps_json>
# timestamps_json is a JSON array of objects: [{"id": "q1", "timestamp": 125.5}, ...]
# Requires: ffmpeg

set -euo pipefail

VIDEO_FILE="${1:?Usage: extract-frames.sh <video_file> <output_dir> <timestamps_json>}"
OUTPUT_DIR="${2:?Usage: extract-frames.sh <video_file> <output_dir> <timestamps_json>}"
TIMESTAMPS_JSON="${3:?Usage: extract-frames.sh <video_file> <output_dir> <timestamps_json>}"

FRAMES_DIR="$OUTPUT_DIR/frames"
mkdir -p "$FRAMES_DIR"

echo "==> Extracting frames from video..."

# Parse timestamps and extract frames
python3 -c "
import json, subprocess, os

timestamps = json.loads('''$TIMESTAMPS_JSON''')
video = '$VIDEO_FILE'
frames_dir = '$FRAMES_DIR'

extracted = []

for item in timestamps:
    ts = item['timestamp']
    frame_id = item['id']
    
    # Extract primary frame at exact timestamp
    primary = os.path.join(frames_dir, f'{frame_id}.png')
    subprocess.run([
        'ffmpeg', '-y', '-ss', str(ts), '-i', video,
        '-vframes', '1', '-q:v', '2', primary
    ], capture_output=True)
    
    # Extract 2 additional frames nearby (±1.5s) for selection
    for offset_idx, offset in enumerate([-1.5, 1.5]):
        alt_ts = max(0, ts + offset)
        alt_path = os.path.join(frames_dir, f'{frame_id}_alt{offset_idx}.png')
        subprocess.run([
            'ffmpeg', '-y', '-ss', str(alt_ts), '-i', video,
            '-vframes', '1', '-q:v', '2', alt_path
        ], capture_output=True)
    
    extracted.append({
        'id': frame_id,
        'timestamp': ts,
        'primary': primary,
        'alternates': [
            os.path.join(frames_dir, f'{frame_id}_alt0.png'),
            os.path.join(frames_dir, f'{frame_id}_alt1.png')
        ]
    })
    print(f'  Extracted frame: {frame_id} @ {ts}s')

# Save manifest
manifest_path = os.path.join('$OUTPUT_DIR', 'frames-manifest.json')
with open(manifest_path, 'w') as f:
    json.dump(extracted, f, indent=2)

print(f'==> Extracted {len(extracted)} frame sets to {frames_dir}')
print(f'==> Manifest: {manifest_path}')
"

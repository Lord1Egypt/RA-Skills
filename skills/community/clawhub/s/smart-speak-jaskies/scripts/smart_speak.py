#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import tempfile
import sys

def main():
    parser = argparse.ArgumentParser(description="Multilingual TTS merging script")
    parser.add_argument("--segments-json", required=True, help="JSON string of segments [{'text': '...', 'voice': '...'}]")
    parser.add_argument("--output", required=True, help="Path to the output mp3 file")
    
    args = parser.parse_args()
    
    try:
        segments = json.loads(args.segments_json)
    except json.JSONDecodeError as e:
        print(f"Error parsing segments JSON: {e}", file=sys.stderr)
        sys.exit(1)
        
    if not segments:
        print("No segments provided", file=sys.stderr)
        sys.exit(1)
        
    temp_dir = tempfile.mkdtemp()
    concat_file_path = os.path.join(temp_dir, "concat.txt")
    temp_files = []
    
    try:
        with open(concat_file_path, "w") as f_concat:
            for i, segment in enumerate(segments):
                text = segment.get("text", "").strip()
                voice = segment.get("voice", "vi-VN-HoaiMyNeural")
                
                if not text:
                    continue
                
                temp_file = os.path.join(temp_dir, f"part_{i}.mp3")
                
                # Call edge-tts
                # Using absolute path for edge-tts as per workspace notes
                edge_tts_path = "/home/jackie_chen_phong/.local/bin/edge-tts"
                cmd = [
                    edge_tts_path,
                    "--voice", voice,
                    "--text", text,
                    "--write-media", temp_file
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode != 0:
                    print(f"Error generating TTS for segment {i}: {result.stderr}", file=sys.stderr)
                    continue
                
                if os.path.exists(temp_file):
                    f_concat.write(f"file '{temp_file}'\n")
                    temp_files.append(temp_file)
        
        if not temp_files:
            print("No audio files generated", file=sys.stderr)
            sys.exit(1)
            
        # Run ffmpeg to merge
        ffmpeg_cmd = [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", concat_file_path,
            "-c", "copy",
            args.output
        ]
        
        result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error merging audio with ffmpeg: {result.stderr}", file=sys.stderr)
            sys.exit(1)
            
        print(f"Successfully generated multilingual audio: {args.output}")
        
    finally:
        # Cleanup
        for f in temp_files:
            try: os.remove(f)
            except: pass
        try: os.remove(concat_file_path)
        except: pass
        try: os.rmdir(temp_dir)
        except: pass

if __name__ == "__main__":
    main()

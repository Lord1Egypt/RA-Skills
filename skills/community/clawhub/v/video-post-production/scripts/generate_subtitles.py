#!/usr/bin/env python3
import json
import argparse
import math
import os

def format_time(seconds):
    """Convert seconds to ASS time format: H:MM:SS.CC"""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    # Use floor and multiply by 100 for centiseconds
    cs = int((s - int(s)) * 100)
    return f"{h}:{m:02d}:{int(s):02d}.{cs:02d}"

def wrap_text(text, max_len=12):
    """Split text into two lines if longer than max_len."""
    if len(text) <= max_len:
        return text
    
    # Try to split at punctuation
    punctuation = "，。！？,.!?"
    split_indices = [i + 1 for i, char in enumerate(text) if char in punctuation]
    
    # If punctuation exists, find the one closest to middle
    if split_indices:
        mid = len(text) / 2
        best_idx = min(split_indices, key=lambda x: abs(x - mid))
        return text[:best_idx] + "\\N" + text[best_idx:]
    
    # Otherwise, split at middle
    mid = len(text) // 2
    return text[:mid] + "\\N" + text[mid:]

def generate_ass(plan_path, output_path, video_width, video_height, font, font_size):
    # Load production plan
    with open(plan_path, 'r', encoding='utf-8') as f:
        plan = json.load(f)

    # Color mapping
    colors = {
        "yellow": "&H00FFFF&",
        "red": "&H0000FF&",
        "cyan": "&HFFFF00&",
        "green": "&H00FF00&",
        "orange": "&H0080FF&"
    }

    # ASS Header
    ass_lines = [
        "[Script Info]",
        "; Subtitles for video post-production",
        "ScriptType: v4.00+",
        "PlayResX: " + str(video_width),
        "PlayResY: " + str(video_height),
        "ScaledBorderAndShadow: yes",
        "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        f"Style: Default,{font},{font_size},&H00FFFFFF&,&H000000FF&,&H00000000&,&H00000000&,1,0,0,0,100,100,0,0,1,3,2,2,20,20,280,1"
    ]

    # Add Highlight styles
    for name, color in colors.items():
        style_name = f"Highlight_{name.capitalize()}"
        ass_lines.append(f"Style: {style_name},{font},{font_size},{color},&H000000FF&,&H00000000&,&H00000000&,1,0,0,0,100,100,0,0,1,3,2,2,20,20,280,1")

    ass_lines.extend(["", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"])

    # Process subtitle groups
    for group in plan.get("subtitle_groups", []):
        start = format_time(group["start"])
        end = format_time(group["end"])
        text = group["text"]
        style = "Default"
        
        # Wrapping
        text = wrap_text(text)
        
        # Apply fade
        tag_prefix = "{\\fad(150,0)}"
        
        # Highlights
        highlight_words = group.get("highlight_words", [])
        if highlight_words:
            # We'll replace occurrences of highlight words with tagged versions
            # Note: This is a simple replacement. If words overlap, this might get complex.
            # We sort by length descending to avoid partial replacements.
            highlight_words.sort(key=lambda x: len(x["word"]), reverse=True)
            
            for hw in highlight_words:
                word = hw["word"]
                color_tag = f"{{\\c{colors.get(hw['color'], '&H00FFFFFF&')}}}"
                
                effect_tag = ""
                if hw.get("effect") == "scale_bounce":
                    effect_tag = "{\\t(0,150,\\fscx130\\fscy130)\\t(150,300,\\fscx100\\fscy100)}"
                
                # Combine tags
                tagged_word = f"{color_tag}{effect_tag}{word}{{\\c}}"
                
                # Replace in text (ensure we don't double replace if possible)
                # This is a naive implementation; for a production script, one might use a more robust way.
                text = text.replace(word, tagged_word)

        # Build Dialogue line
        # Dialogue: 0,0:00:00.00,0:00:00.50,Default,,0,0,0,,{\fad(150,0)}Text
        line = f"Dialogue: 0,{start},{end},{style},,0,0,0,,{tag_prefix}{text}"
        ass_lines.append(line)

    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(ass_lines) + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate ASS subtitles from a production plan JSON.")
    parser.add_argument("--plan", required=True, help="Input production_plan.json path")
    parser.add_argument("--output", required=True, help="Output .ass file path")
    parser.add_argument("--video-width", type=int, default=720, help="Video width (default: 720)")
    parser.add_argument("--video-height", type=int, default=1280, help="Video height (default: 1280)")
    parser.add_argument("--font", default="Heiti SC", help="Font name (default: Heiti SC)")
    parser.add_argument("--font-size", type=int, default=48, help="Font size (default: 48)")

    args = parser.parse_args()
    
    # Ensure output directory exists
    output_dir = os.path.dirname(os.path.abspath(args.output))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    generate_ass(args.plan, args.output, args.video_width, args.video_height, args.font, args.font_size)
    print(f"ASS subtitle file generated at: {args.output}")

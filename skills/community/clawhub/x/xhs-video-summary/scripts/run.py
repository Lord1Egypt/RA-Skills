import sys
import os
import subprocess
import json

def main():
    if len(sys.argv) < 2:
        print("Error: Please provide a Xiaohongshu URL.")
        print("Usage: python run.py <xhs_url>")
        sys.exit(1)

    url = sys.argv[1]
    print("1/4 Extracting metadata...")

    # 动态寻找 xiaohongshu-extract 依赖的位置 (支持全局 ~/.agents/skills 和本地 workspace/skills)
    possible_paths = [
        os.path.expanduser("~/.agents/skills/xiaohongshu-extract/scripts/xiaohongshu_extract.py"),
        os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../xiaohongshu-extract/scripts/xiaohongshu_extract.py")),
        os.path.abspath(os.path.join(os.path.dirname(__file__), "../../xiaohongshu-extract/scripts/xiaohongshu_extract.py")),
        os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../.agents/skills/xiaohongshu-extract/scripts/xiaohongshu_extract.py"))
    ]
    
    extract_script = None
    for p in possible_paths:
        if os.path.exists(p):
            extract_script = p
            break
            
    if not extract_script:
        print("Error: Could not find xiaohongshu_extract.py.")
        print("Please ensure 'xiaohongshu-extract' skill is installed via clawhub.")
        sys.exit(1)

    # 提取元数据
    try:
        subprocess.run([sys.executable, extract_script, url, "--flat-only", "--output", "xhs_meta.json"], check=True)
    except subprocess.CalledProcessError:
        print("Error: Metadata extraction script failed.")
        sys.exit(1)

    if not os.path.exists("xhs_meta.json"):
        print("Error: Metadata file not generated.")
        sys.exit(1)

    # 解析视频地址
    with open("xhs_meta.json", "r", encoding="utf-8") as f:
        meta = json.load(f)
        
    video_url = meta.get("video_stream_url")
    if not video_url:
        print("Error: No video URL found in metadata. This might be a picture note instead of a video.")
        sys.exit(1)

    print("2/4 Downloading video...")
    subprocess.run(["curl", "-s", "-L", video_url, "-o", "xhs_temp.mp4"], check=True)

    print("3/4 Extracting audio...")
    subprocess.run(["ffmpeg", "-i", "xhs_temp.mp4", "-vn", "-acodec", "libmp3lame", "-q:a", "2", "xhs_temp.mp3", "-y", "-loglevel", "error"], check=True)

    print("4/4 Transcribing audio with Whisper...")
    subprocess.run(["whisper", "xhs_temp.mp3", "--model", "base", "--language", "zh", "--output_dir", ".", "--output_format", "txt"], check=True)

    print("======================================")
    print("Done! Outputs generated:")
    print("- Metadata: xhs_meta.json")
    print("- Transcript: xhs_temp.txt")

if __name__ == "__main__":
    main()

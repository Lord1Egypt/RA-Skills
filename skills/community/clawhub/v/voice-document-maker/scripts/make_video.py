import os
import sys
import subprocess
import argparse
import urllib.request
import urllib.parse

# 配置路径
WORK_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(WORK_DIR, "..", "output", "voice_documents")
os.makedirs(OUTPUT_DIR, exist_ok=True)

FFMPEG = r"C:\ffmpeg\bin\ffmpeg.exe"
TTS_PY = r"C:\Users\lenovo\.copaw\venv\Scripts\python.exe"

def generate_tts(text, output_mp3):
    """生成 TTS 语音"""
    cmd = [TTS_PY, "-m", "edge_tts", "--voice", "zh-CN-YunxiNeural", "--text", text, "--write-media", output_mp3]
    subprocess.run(cmd, check=True)
    return output_mp3

def generate_cover(prompt, output_image):
    """生成背景图"""
    # 使用 pollinations.ai 免费生图
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=720&height=1280&nologo=true"
    try:
        urllib.request.urlretrieve(url, output_image)
    except Exception as e:
        print(f"生图失败，使用默认背景: {e}")
        # 如果生图失败，用 ffmpeg 生成纯色背景
        subprocess.run([FFMPEG, "-f", "lavfi", "-i", "color=c=#667eea:s=720x1280:d=1", "-frames:v", "1", output_image])
    return output_image

def make_video(audio_path, image_path, output_video):
    """合成视频"""
    cmd = [
        FFMPEG,
        "-loop", "1", "-i", image_path,
        "-i", audio_path,
        "-c:v", "libx264", "-tune", "stillimage", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "128k",
        "-shortest", "-y", output_video
    ]
    subprocess.run(cmd, check=True)
    return output_video

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", required=True, help="要朗读的文本")
    parser.add_argument("--bg_prompt", default="Beautiful elegant Chinese lady, soft lighting, cinematic, 4k", help="背景图描述")
    parser.add_argument("--output", default="result.mp4", help="输出文件名")
    args = parser.parse_args()

    audio_file = os.path.join(OUTPUT_DIR, "temp_audio.mp3")
    image_file = os.path.join(OUTPUT_DIR, "temp_bg.png")
    final_video = os.path.join(OUTPUT_DIR, args.output)

    print("1. 生成语音...")
    generate_tts(args.text, audio_file)
    
    print("2. 生成背景...")
    generate_cover(args.bg_prompt, image_file)
    
    print("3. 合成视频...")
    make_video(audio_file, image_file, final_video)
    
    print(f"SUCCESS: {final_video}")

if __name__ == "__main__":
    main()

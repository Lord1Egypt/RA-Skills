# -*- coding: utf-8 -*-
"""
一键视频提取脚本 v2.0 (积分优化版)
合并帧提取 + 音频提取 + Whisper转写 + Contact Sheet生成
将原来 ~15 次工具调用压缩为 1 次 Bash 调用
用法: python extract_video_one_shot.py <video_path> <temp_dir>
输出:
  - <temp_dir>/frames/frame_XXXX.jpg  (关键帧)
  - <temp_dir>/transcript.json        (台词时间轴)
  - <temp_dir>/contact_sheet.jpg      (拼图，供AI一次性读取)
  - stdout: JSON摘要 (帧数/时长/台词)
"""
import sys, os, json, subprocess, base64
from PIL import Image, ImageDraw, ImageFont

def find_ffmpeg():
    """查找可用的 ffmpeg"""
    candidates = [
        r"C:\Users\Admin\.workbuddy\binaries\python\versions\3.13.12\Scripts\ffmpeg.exe",
        r"C:\Users\Admin\.workbuddy\binaries\python\versions\3.13.12\ffmpeg.exe",
        r"C:\Users\Admin\.workbuddy\binaries\python\envs\default\Scripts\ffmpeg.exe",
        r"C:\Users\Admin\.workbuddy\binaries\python\versions\3.13.12\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe",
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    # Try imageio_ffmpeg
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except:
        pass
    return "ffmpeg"

def extract_frames(ffmpeg, video, out_dir, fps=0.5):
    """提取关键帧"""
    frames_dir = os.path.join(out_dir, "frames")
    # 清空所有旧产物（帧+音频+转录+拼图），防止不同视频的内容混在一起
    import shutil
    if os.path.exists(frames_dir):
        shutil.rmtree(frames_dir)
    for stale in ["audio.wav", "transcript.json", "contact_sheet.jpg"]:
        sp = os.path.join(out_dir, stale)
        if os.path.exists(sp):
            os.remove(sp)
    os.makedirs(frames_dir)
    cmd = [ffmpeg, "-y", "-i", video, "-vf", f"fps={fps}", "-q:v", "2",
           os.path.join(frames_dir, "frame_%04d.jpg")]
    subprocess.run(cmd, capture_output=True, timeout=120)
    frames = sorted([f for f in os.listdir(frames_dir) if f.endswith('.jpg')])
    return frames_dir, frames

def extract_audio(ffmpeg, video, out_dir):
    """提取音频 WAV"""
    wav_path = os.path.join(out_dir, "audio.wav")
    cmd = [ffmpeg, "-y", "-i", video, "-vn", "-acodec", "pcm_s16le",
           "-ar", "16000", "-ac", "1", wav_path]
    subprocess.run(cmd, capture_output=True, timeout=120)
    return wav_path

def run_whisper(wav_path, out_dir):
    """Whisper 中文转写"""
    os.environ['PATH'] = r"C:\Users\Admin\.workbuddy\binaries\python\versions\3.13.12\Scripts;" + os.environ.get('PATH', '')
    import whisper
    model = whisper.load_model('medium')
    result = model.transcribe(wav_path, language='Chinese')
    segs = []
    for s in result['segments']:
        segs.append({
            'start': round(s['start'], 2),
            'end': round(s['end'], 2),
            'text': s['text'].strip()
        })
    transcript = {
        'segments': segs,
        'duration': segs[-1]['end'] if segs else 0
    }
    out_path = os.path.join(out_dir, "transcript.json")
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(transcript, f, ensure_ascii=False, indent=2)
    return transcript

def crop_9x16(img):
    """从 16:9 图像居中裁剪为 9:16 竖屏"""
    w, h = img.size
    target_w = int(h * 9 / 16)
    if target_w >= w:
        return img
    left = (w - target_w) // 2
    return img.crop((left, 0, left + target_w, h))


def make_contact_sheet(frames_dir, frames, out_dir, cols=4, thumb_w=300):
    """将所有帧拼成一张 9:16 竖屏 contact sheet 图片"""
    if not frames:
        return None
    
    images = []
    for fname in frames:
        img = Image.open(os.path.join(frames_dir, fname))
        # 9:16 居中裁剪
        img = crop_9x16(img)
        thumb_h = int(thumb_w * 16 / 9)  # 9:16 → h = w * 16/9
        thumb = img.resize((thumb_w, thumb_h), Image.LANCZOS)
        images.append((fname, thumb))
    
    rows = (len(images) + cols - 1) // cols
    thumb_h = images[0][1].height
    label_h = 20
    cell_w = thumb_w + 10
    cell_h = thumb_h + label_h + 10
    
    sheet = Image.new('RGB', (cell_w * cols, cell_h * rows), (30, 30, 30))
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("arial.ttf", 12)
    except:
        font = ImageFont.load_default()
    
    for i, (fname, thumb) in enumerate(images):
        col = i % cols
        row = i // cols
        x = col * cell_w + 5
        y = row * cell_h + 5
        sheet.paste(thumb, (x, y))
        sec = i * 2
        label = f"frame_{i+1:04d} ({sec}s)"
        draw.text((x, y + thumb_h + 2), label, fill=(200, 200, 200), font=font)
    
    sheet_path = os.path.join(out_dir, "contact_sheet.jpg")
    sheet.save(sheet_path, "JPEG", quality=85, optimize=True)
    return sheet_path

def _to_win_path(p):
    """自动将 msys/Cygwin 风格路径转为 Windows 风格，避免 ffmpeg 提取 0 帧"""
    # /c/Users/... → C:/Users/...（msys 风格）
    if p.startswith('/') and len(p) > 2 and p[2] == '/' and p[1].isalpha():
        p = p[1].upper() + ':' + p[2:]
    # /cygdrive/c/... → C:/...（Cygwin 风格）
    elif p.startswith('/cygdrive/') and len(p) > 11:
        p = p[10].upper() + ':' + p[11:]
    return p.replace('\\', '/')


def main():
    if len(sys.argv) < 3:
        print("Usage: python extract_video_one_shot.py <video_path> <temp_dir>")
        sys.exit(1)

    video = _to_win_path(sys.argv[1])
    out_dir = _to_win_path(sys.argv[2])
    os.makedirs(out_dir, exist_ok=True)
    
    print(f"[1/4] Extracting frames...", file=sys.stderr)
    ffmpeg = find_ffmpeg()
    # 确保 whisper 能找到 ffmpeg
    venv_scripts = r"C:\Users\Admin\.workbuddy\binaries\python\versions\3.13.12\Scripts"
    if not os.path.exists(os.path.join(venv_scripts, "ffmpeg.exe")):
        import shutil
        try:
            shutil.copy2(ffmpeg, os.path.join(venv_scripts, "ffmpeg.exe"))
        except:
            pass
    
    frames_dir, frames = extract_frames(ffmpeg, video, out_dir)
    print(f"  -> {len(frames)} frames extracted", file=sys.stderr)
    
    print(f"[2/4] Extracting audio...", file=sys.stderr)
    wav_path = extract_audio(ffmpeg, video, out_dir)
    
    print(f"[3/4] Whisper transcription (medium model)...", file=sys.stderr)
    transcript = run_whisper(wav_path, out_dir)
    print(f"  -> {len(transcript['segments'])} segments, duration={transcript['duration']:.1f}s", file=sys.stderr)
    
    print(f"[4/4] Creating contact sheet...", file=sys.stderr)
    sheet_path = make_contact_sheet(frames_dir, frames, out_dir)
    
    # stdout: JSON 摘要
    summary = {
        "video": os.path.basename(video),
        "frame_count": len(frames),
        "frames_dir": frames_dir,
        "transcript_path": os.path.join(out_dir, "transcript.json"),
        "contact_sheet": sheet_path,
        "duration": transcript["duration"],
        "segments": transcript["segments"]
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print("\n--- TRANSCRIPT ---", file=sys.stderr)
    for s in transcript["segments"]:
        print(f"[{s['start']:.1f}-{s['end']:.1f}] {s['text']}", file=sys.stderr)

if __name__ == "__main__":
    main()

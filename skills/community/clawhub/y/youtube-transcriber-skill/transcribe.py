#!/usr/bin/env python3
"""
YouTube 转录总结 - NAS 本地版
直接在 NAS 上下载和转录，不依赖 Mac
"""
import sys, os, subprocess, tempfile

def download_audio(video_url, output_path):
    cmd = ['python3', '-m', 'yt_dlp', '-f', 'bestaudio[ext=webm]/bestaudio',
           '-o', output_path, '--no-playlist', '--socket-timeout', '30', video_url]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    return result.returncode == 0, result.stderr

def transcribe_audio(audio_path, language='auto'):
    from faster_whisper import WhisperModel
    model = WhisperModel("base", device="cpu", compute_type="int8")
    if language == 'auto':
        segments, info = model.transcribe(audio_path)
    else:
        segments, info = model.transcribe(audio_path, language=language)
    transcript = []
    for seg in segments:
        transcript.append(f"[{seg.start:.2f}s -> {seg.end:.2f}s] {seg.text}")
    return info.language, '\n'.join(transcript)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 transcribe.py <YouTube_URL> [language]")
        sys.exit(1)
    
    url = sys.argv[1]
    language = sys.argv[2] if len(sys.argv) > 2 else 'auto'
    
    print(f"📺 URL: {url}")
    print(f"🌐 Language: {language}")
    
    video_id = url.split('v=')[-1].split('&')[0] if 'v=' in url else url.split('/')[-1].split('?')[0]
    
    with tempfile.TemporaryDirectory() as tmpdir:
        audio_path = os.path.join(tmpdir, f"{video_id}.webm")
        
        print("\n[1/3] 下载音频...")
        success, error = download_audio(url, audio_path)
        if not success:
            print(f"❌ 下载失败：{error[:200]}")
            sys.exit(1)
        print(f"✅ 下载成功")
        
        print("\n[2/3] 转录中...")
        try:
            lang, transcript = transcribe_audio(audio_path, language)
            print(f"✅ 转录完成！语言：{lang}")
        except Exception as e:
            print(f"❌ 转录失败：{e}")
            sys.exit(1)
        
        print("\n[3/3] 生成总结...")
        print("\n" + "="*60)
        print(f"# 视频转录总结\n\n**URL:** {url}\n**语言:** {lang}\n\n## 转录内容\n{transcript}")
        print("="*60)

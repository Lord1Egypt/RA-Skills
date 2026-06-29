"""
视频完整混合 + 多版本压缩 模板
复制到 output/videos/<project>/<episode>/make_<episode>.py
"""
import os
import subprocess
import wave

FFMPEG = r"C:\Users\ZWB2016\AppData\Local\Programs\Python\Python312\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"


def mix(video, voiceover, bgm, output, duration_s, bgm_volume=0.18):
    """混合视频 + 旁白 + BGM"""
    cmd = [
        FFMPEG, "-y",
        "-i", video,
        "-i", voiceover,
        "-stream_loop", "-1", "-i", bgm,
        "-filter_complex",
        f"[2:a]volume={bgm_volume},afade=t=in:st=0:d=1.0,afade=t=out:st={duration_s-1}:d=1.0[b];"
        f"[1:a][b]amix=inputs=2:duration=longest[a]",
        "-map", "0:v", "-map", "[a]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "20",
        "-c:a", "aac", "-b:a", "128k",
        "-movflags", "+faststart",
        "-shortest",
        output,
    ]
    subprocess.run(cmd, check=True)
    print(f"完成: {output} ({os.path.getsize(output)/1024/1024:.2f} MB)")


def speedup_audio(in_path, out_path, speed):
    """wave 重采样加速（保 pitch）"""
    in_wav = in_path + "._in.wav"
    out_wav = out_path + "._out.wav"
    subprocess.run([FFMPEG, "-y", "-i", in_path, "-ar", "24000", "-ac", "1", "-f", "wav", in_wav],
                   capture_output=True, check=True)
    with wave.open(in_wav, 'rb') as wf:
        n_ch, sw, fr, n_fr = wf.getnchannels(), wf.getsampwidth(), wf.getframerate(), wf.getnframes()
        raw = wf.readframes(n_fr)
    new_fr = int(fr * speed)
    with wave.open(out_wav, 'wb') as wf:
        wf.setnchannels(n_ch); wf.setsampwidth(sw)
        wf.setframerate(new_fr); wf.writeframes(raw)
    subprocess.run([FFMPEG, "-y", "-i", out_wav, "-ar", "24000", "-ac", "1",
                    "-c:a", "libmp3lame", "-b:a", "48k", out_path],
                   capture_output=True, check=True)
    for f in [in_wav, out_wav]:
        if os.path.exists(f): os.remove(f)
    print(f"  {speed}x 重采样: {in_path} -> {out_path}")


def video_setpts(in_video, out_video, ratio):
    """setpts 视频流加速（ratio=0.5 表示 2x 速）"""
    pts = f"PTS/{1/ratio}"  # ratio=0.5 -> PTS/2 (2x 加速)
    cmd = [FFMPEG, "-y", "-i", in_video, "-vf", f"setpts={pts}",
           "-an", "-c:v", "libx264", "-preset", "slow", "-crf", "20",
           "-movflags", "+faststart", out_video]
    subprocess.run(cmd, check=True)
    print(f"  setpts {ratio}x 视频: {out_video}")

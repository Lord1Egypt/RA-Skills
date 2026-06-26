#!/usr/bin/env python3
"""
🎬 Video Remix V3 - Gemini First 流程

优化后的流程：
1. Gemini 智能分析 → 获取 JSON（clips + script）
2. 下载 YouTube 视频
3. 根据 clips 时间戳剪辑片段
4. 根据 clips[].script 生成配音 + SRT 字幕
5. FFmpeg 合成硬字幕版本（音频自动对齐视频时长）
6. 启动 HTTP 服务器，通过局域网 IP 访问

Gemini JSON 格式：
{
  "clips": [
    {
      "start": 24.0,
      "end": 28.0,
      "script": "配音文案（根据时长自动计算字数）",
    }
  ]
}
"""

import sys
import os
import json
import subprocess
import socket
from pathlib import Path
from typing import List, Dict, Any
from datetime import timedelta, datetime

# 配置
OUTPUT_DIR = Path(os.getenv("VR_OUTPUT_DIR", "./output"))
TEMP_DIR = Path(os.getenv("VR_TEMP_DIR", "./temp"))
PROXY = os.getenv("HTTP_PROXY", "http://127.0.0.1:10808")
TTS_VOICE = os.getenv("VR_TTS_VOICE", "xiaoxiao")
FFMPEG_CMD = os.getenv("VR_FFMPEG_CMD", "/opt/homebrew/Cellar/ffmpeg-full/8.1/bin/ffmpeg")
# 中文语速：约 4.5 字/秒（舒适语速）
CHINESE_CHARS_PER_SECOND = 4.5

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR.mkdir(parents=True, exist_ok=True)


def get_lan_ip() -> str:
    """获取本机局域网 IP 地址"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def seconds_to_srt_time(seconds: float) -> str:
    """秒数转换为 SRT 时间格式 (HH:MM:SS,mmm)"""
    td = timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def load_gemini_json(json_path: Path) -> Dict[str, Any]:
    """加载 Gemini 返回的 JSON 元数据"""
    print(f"📖 加载 Gemini 元数据：{json_path}")
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    assert "clips" in data, "JSON 缺少 clips 字段"
    assert len(data["clips"]) > 0, "clips 数组为空"
    
    for i, clip in enumerate(data["clips"]):
        assert "start" in clip, f"clips[{i}] 缺少 start"
        assert "end" in clip, f"clips[{i}] 缺少 end"
        assert "script" in clip, f"clips[{i}] 缺少 script"
    
    print(f"✅ 加载成功：{len(data['clips'])} 个片段")
    return data


def download_video(youtube_url: str, output_path: Path, timestamp: str) -> bool:
    """下载 YouTube 视频"""
    print(f"📥 下载视频：{youtube_url}")
    
    # 使用时间戳命名下载的视频
    video_name = f"source_video_{timestamp}.mp4"
    download_path = output_path.parent / video_name
    
    cmd = [
        "yt-dlp",
        "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "--proxy", PROXY,
        "-o", str(download_path),
        youtube_url
    ]
    
    subprocess.run(cmd, capture_output=True, check=True)
    print(f"✅ 下载完成：{download_path}")
    return True


def clip_video_segments(video_path: Path, clips: List[Dict[str, Any]], output_dir: Path, timestamp: str) -> List[Path]:
    """根据时间戳剪辑视频片段"""
    print("\n" + "=" * 60)
    print("✂️ Phase 2: 根据时间戳剪辑")
    print("=" * 60)
    
    clip_files = []
    for i, clip in enumerate(clips):
        start = clip["start"]
        end = clip["end"]
        duration = end - start
        output_file = output_dir / f"clip_{timestamp}_{i:03d}.mp4"
        
        print(f"✂️ 片段 {i+1}: {start}s - {end}s ({duration}s)")
        print(f"   文案：{clip['script'][:30]}...")
        
        cmd = [
            FFMPEG_CMD, "-y",
            "-ss", str(start),
            "-t", str(duration),
            "-i", str(video_path),
            "-c:v", "libx264",
            "-c:a", "aac",
            str(output_file)
        ]
        
        subprocess.run(cmd, capture_output=True, check=True)
        clip_files.append(output_file)
    
    # 合并片段
    merged_video = output_dir / f"merged_clips_{timestamp}.mp4"
    print(f"🔗 合并 {len(clip_files)} 个片段...")
    
    concat_file = output_dir / "concat_list.txt"
    with open(concat_file, 'w') as f:
        for clip in clip_files:
            clip_name = Path(clip).name
            f.write(f"file '{clip_name}'\n")
    
    cmd = [
        FFMPEG_CMD, "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_file),
        "-c:v", "copy",
        "-c:a", "copy",
        str(merged_video)
    ]
    
    subprocess.run(cmd, capture_output=True, check=True)
    print(f"✅ 合并完成：{merged_video}")
    return merged_video


def estimate_script_duration(text: str) -> float:
    """估算文案朗读时长（秒）"""
    # 中文字符数 / 语速
    chars = len(text)
    return chars / CHINESE_CHARS_PER_SECOND


def generate_tts_with_alignment(clips: List[Dict[str, Any]], output_dir: Path, timestamp: str) -> List[Dict[str, Any]]:
    """
    为每个片段生成 TTS 配音，并根据视频时长自动对齐
    
    如果音频比视频长，会加速音频使其匹配视频时长
    """
    tts_results = []
    tts_dir = output_dir / f"tts_{timestamp}"
    tts_dir.mkdir(parents=True, exist_ok=True)
    
    print("\n" + "=" * 60)
    print("🎤 Phase 3: 生成配音和字幕（自动对齐）")
    print("=" * 60)
    
    for i, clip in enumerate(clips):
        audio_path = tts_dir / f"tts_{timestamp}_{i:03d}.mp3"
        text = clip["script"]
        video_duration = clip["end"] - clip["start"]
        
        # 估算文案时长
        estimated_duration = estimate_script_duration(text)
        
        print(f"🎤 片段 {i+1}: 视频 {video_duration:.1f}s | 文案 {len(text)}字 | 预估 {estimated_duration:.1f}s")
        
        # 如果预估时长超过视频时长，提示用户
        if estimated_duration > video_duration * 0.9:
            print(f"   ⚠️  文案偏长，可能需要在后期加速")
        
        # 生成 TTS
        cmd = [
            "edge-tts",
            "--voice", f"zh-CN-{TTS_VOICE.capitalize()}Neural",
            "--text", text,
            "--write-media", str(audio_path)
        ]
        
        subprocess.run(cmd, capture_output=True, check=True)
        
        # 获取实际音频时长
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", str(audio_path)],
            capture_output=True, text=True
        )
        audio_duration = float(result.stdout.strip())
        
        # 计算加速比例
        speed_ratio = audio_duration / video_duration
        if speed_ratio > 1.0:
            print(f"   ⚡ 音频过长 ({audio_duration:.1f}s > {video_duration:.1f}s)，将加速 {speed_ratio:.2f}x")
        elif speed_ratio < 0.8:
            print(f"   💤 音频较短 ({audio_duration:.1f}s < {video_duration:.1f}s)，保持原速")
        
        tts_results.append({
            "script": text,
            "audio_path": audio_path,
            "audio_duration": audio_duration,
            "video_duration": video_duration,
            "speed_ratio": speed_ratio
        })
    
    return tts_results


def merge_audio_with_alignment(tts_results: List[Dict[str, Any]], output_dir: Path, timestamp: str) -> Path:
    """
    合并所有 TTS 音频，并根据视频时长自动加速对齐
    """
    full_audio = output_dir / f"full_voiceover_{timestamp}.mp3"
    
    # 构建 filter_complex 命令，对每个音频应用变速
    input_args = []
    filter_parts = []
    
    for i, tts in enumerate(tts_results):
        input_args.extend(["-i", str(tts["audio_path"])])
        speed = tts["speed_ratio"]
        if speed > 1.0:
            # 需要加速：atempo 范围 0.5-2.0，超过 2.0 需要链式处理
            if speed <= 2.0:
                filter_parts.append(f"[{i}:a]atempo={speed:.3f}[a{i}]")
            else:
                # 链式 atempo（最多 4 级）
                stages = []
                remaining = speed
                while remaining > 2.0:
                    stages.append("atempo=2.0")
                    remaining /= 2.0
                stages.append(f"atempo={remaining:.3f}")
                filter_parts.append(f"[{i}:a]{','.join(stages)}[a{i}]")
        else:
            filter_parts.append(f"[{i}:a]anull[a{i}]")
    
    # 合并所有音频
    n_inputs = len(tts_results)
    concat_inputs = "".join([f"[a{i}]" for i in range(n_inputs)])
    filter_complex = ";".join(filter_parts) + f";{concat_inputs}concat=n={n_inputs}:v=0:a=1[out]"
    
    cmd = [FFMPEG_CMD, "-y"] + input_args + [
        "-filter_complex", filter_complex,
        "-map", "[out]",
        "-c:a", "libmp3lame",
        str(full_audio)
    ]
    
    subprocess.run(cmd, capture_output=True, check=True)
    print(f"✅ 配音合并完成：{full_audio}")
    return full_audio


def create_srt_subtitle(clips: List[Dict[str, Any]], tts_results: List[Dict[str, Any]], output_path: Path) -> Path:
    """
    根据 clips 和 TTS 结果生成 SRT 字幕
    
    字幕时间基于合并后视频的时间线（累加每个片段的时长）
    因为视频片段是连续合并的，空隙已被去掉
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        current_time = 0.0
        
        for i, (clip, tts) in enumerate(zip(clips, tts_results), 1):
            # 字幕显示时长 = 视频片段时长
            duration = clip["end"] - clip["start"]
            
            subtitle_start = current_time
            subtitle_end = current_time + duration
            
            start_time = seconds_to_srt_time(subtitle_start)
            end_time = seconds_to_srt_time(subtitle_end)
            
            f.write(f"{i}\n")
            f.write(f"{start_time} --> {end_time}\n")
            f.write(f"{clip['script']}\n\n")
            
            # 累加到下一个片段
            current_time += duration
    
    print(f"📝 SRT 字幕已生成：{output_path}")
    return output_path


def merge_with_hardsub(
    video_path: Path,
    srt_path: Path,
    audio_path: Path,
    output_path: Path
) -> bool:
    """
    合成视频 + 硬字幕 + 配音
    """
    print("\n" + "=" * 60)
    print("🎬 Phase 4: 硬字幕合成")
    print("=" * 60)
    print(f"🎬 合成硬字幕版本...")
    print(f"   视频：{video_path}")
    print(f"   字幕：{srt_path}")
    print(f"   配音：{audio_path}")
    
    srt_path_escaped = str(srt_path).replace(":", r"\:").replace("'", r"\'")
    
    cmd = [
        FFMPEG_CMD, "-y",
        "-i", str(video_path),
        "-i", str(audio_path),
        "-vf", f"subtitles='{srt_path_escaped}'",
        "-c:v", "libx264",
        "-preset", "medium",
        "-c:a", "aac",
        "-b:a", "192k",
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-shortest",
        str(output_path)
    ]
    
    subprocess.run(cmd, capture_output=True, check=True)
    
    # 获取输出文件信息
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration,size",
         "-of", "default=noprint_wrappers=1", str(output_path)],
        capture_output=True, text=True
    )
    
    print(f"✅ 硬字幕合成完成：{output_path}")
    return True


def start_http_server(output_dir: Path, port: int = 8888) -> int:
    """启动 HTTP 服务器"""
    import threading
    
    # 确保使用绝对路径
    output_dir = output_dir.absolute()
    output_dir.mkdir(parents=True, exist_ok=True)
    
    def run_server():
        subprocess.run(
            [sys.executable, "-m", "http.server", str(port)],
            cwd=str(output_dir),
            capture_output=False
        )
    
    thread = threading.Thread(target=run_server, daemon=True)
    thread.start()
    return port


def main():
    print("=" * 60)
    print("🎬 Video Remix V3 - Gemini First 流程")
    print("=" * 60)
    
    # 生成时间戳前缀（用于所有文件命名）
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    print(f"\n⏰ 时间戳：{timestamp}\n")
    
    # 加载 Gemini 元数据
    json_file = TEMP_DIR / "gemini_result.json"
    if not json_file.exists():
        print(f"❌ 未找到 Gemini 元数据：{json_file}")
        print("\n请先运行 Gemini 分析，保存 JSON 到 temp/gemini_result.json")
        sys.exit(1)
    
    gemini_data = load_gemini_json(json_file)
    clips = gemini_data["clips"]
    youtube_url = gemini_data.get("youtube_url", "")
    
    # Phase 1: 下载
    print("\n" + "=" * 60)
    print("📥 Phase 1: 下载 YouTube 视频")
    print("=" * 60)
    source_video = TEMP_DIR / f"source_video_{timestamp}.mp4"
    if youtube_url:
        download_video(youtube_url, source_video, timestamp)
    else:
        print("⚠️  未提供 YouTube URL，跳过下载")
        if not source_video.exists():
            print("❌ 源视频不存在")
            sys.exit(1)
    
    # Phase 2: 剪辑
    merged_video = clip_video_segments(source_video, clips, OUTPUT_DIR, timestamp)
    
    # Phase 3: 生成配音（带自动对齐）
    tts_results = generate_tts_with_alignment(clips, OUTPUT_DIR, timestamp)
    
    # 合并音频（带变速对齐）
    full_audio = merge_audio_with_alignment(tts_results, OUTPUT_DIR, timestamp)
    
    # 生成字幕
    srt_path = create_srt_subtitle(clips, tts_results, OUTPUT_DIR / f"subtitles_{timestamp}.srt")
    
    # Phase 4: 硬字幕合成
    final_output = OUTPUT_DIR / f"final_hardsub_{timestamp}.mp4"
    merge_with_hardsub(merged_video, srt_path, full_audio, final_output)
    
    # 完成！
    print("\n" + "=" * 60)
    print("✅ 完成！")
    print("=" * 60)
    
    # 获取文件信息
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(final_output)],
        capture_output=True, text=True
    )
    duration = float(result.stdout.strip())
    size = final_output.stat().st_size
    
    print(f"📁 输出文件：{final_output}")
    print(f"   duration: {duration:.6f}")
    print(f"   size: {size}")
    
    # 启动 HTTP 服务器
    print("\n🌐 启动 HTTP 服务器...")
    lan_ip = get_lan_ip()
    port = 8888
    start_http_server(OUTPUT_DIR, port)
    
    print(f"\n✨ 流程完成！")
    print(f"\n📝 输出文件:")
    print(f"   - {final_output} (硬字幕版本)")
    print(f"   - {full_audio} (配音音频)")
    print(f"   - {srt_path} (SRT 字幕)")
    print(f"\n🌐 局域网访问地址:")
    print(f"   http://{lan_ip}:{port}/{final_output.name}")
    print(f"   http://{lan_ip}:{port}/ (浏览所有文件)")
    
    # 创建最新文件的符号链接（方便访问）
    latest_link = OUTPUT_DIR / "latest.mp4"
    if latest_link.exists() or latest_link.is_symlink():
        latest_link.unlink()
    latest_link.symlink_to(final_output.name)
    print(f"\n🔗 最新视频快捷链接：{latest_link}")
    
    # 保持进程运行
    print("\n⏳ HTTP 服务运行中... (Ctrl+C 停止)")
    try:
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 服务已停止")


if __name__ == "__main__":
    main()

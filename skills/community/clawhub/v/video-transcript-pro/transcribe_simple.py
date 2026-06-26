#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频/音频转录脚本
使用 faster-whisper 进行语音识别

用法：
    python transcribe_simple.py <音视频文件> [模型大小] [语言]

参数：
    文件路径：音视频文件路径（支持 mp4, mp3, wav, m4a 等格式）
    模型大小：tiny, base, small, medium, large-v2, large-v3（默认：small）
    语言：zh, en, ja 等（默认：zh，auto 为自动检测）

示例：
    python transcribe_simple.py video.mp4
    python transcribe_simple.py video.mp4 small zh
    python transcribe_simple.py audio.mp3 base auto
"""

import sys
import os
import time
from pathlib import Path

# Windows 控制台 UTF-8 编码
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    
    # 添加 NVIDIA CUDA DLL 路径
    nvidia_paths = [
        os.path.join(sys.prefix, "Lib", "site-packages", "nvidia", "cublas", "bin"),
        os.path.join(sys.prefix, "Lib", "site-packages", "nvidia", "cudnn", "bin"),
    ]
    for nvidia_path in nvidia_paths:
        if os.path.exists(nvidia_path):
            os.add_dll_directory(nvidia_path)
            os.environ["PATH"] = nvidia_path + os.pathsep + os.environ.get("PATH", "")


class Transcriber:
    """转录器，支持 GPU 失败自动回退到 CPU"""
    
    def __init__(self, model_size: str):
        self.model_size = model_size
        self.model = None
        self.device = None
        self.compute_type = None
        self.gpu_failed = False
        
    def load_model(self, prefer_gpu: bool = True) -> bool:
        """加载模型，GPU 失败自动回退到 CPU"""
        from faster_whisper import WhisperModel
        
        # 尝试顺序：GPU -> CPU
        attempts = []
        
        if prefer_gpu:
            attempts.extend([
                ("cuda", "int8_float16", "GPU (int8_float16)"),
                ("cuda", "int8", "GPU (int8)"),
            ])
        attempts.append(("cpu", "int8", "CPU (int8)"))
        
        for device, compute_type, desc in attempts:
            try:
                print(f"⏳ 尝试加载模型: {desc}...")
                model = WhisperModel(
                    self.model_size,
                    device=device,
                    compute_type=compute_type
                )
                self.model = model
                self.device = device
                self.compute_type = compute_type
                print(f"✅ 模型加载成功: {desc}")
                return True
            except Exception as e:
                print(f"⚠️ {desc} 加载失败: {str(e)[:100]}")
                if device == "cuda":
                    self.gpu_failed = True
                continue
        
        return False
    
    def transcribe_with_fallback(self, file_path: str, language: str = "zh"):
        """转录，GPU 失败时自动切换到 CPU 重试"""
        
        # 首次尝试（可能用 GPU）
        try:
            return self._do_transcribe(file_path, language)
        except Exception as e:
            error_msg = str(e).lower()
            
            # 检测 GPU 相关错误
            gpu_errors = ["cuda", "gpu", "out of memory", "cublas", "cublaslt", 
                         "runtime error", "device", "kernel"]
            
            if any(err in error_msg for err in gpu_errors) and self.device == "cuda":
                print(f"\n⚠️ GPU 转录失败: {e}")
                print("🔄 切换到 CPU 模式重试...")
                self.gpu_failed = True
                
                # 重新加载 CPU 模型
                if self.load_model(prefer_gpu=False):
                    try:
                        return self._do_transcribe(file_path, language)
                    except Exception as e2:
                        print(f"❌ CPU 转录也失败: {e2}")
                        raise
            else:
                raise
    
    def _do_transcribe(self, file_path: str, language: str):
        """执行转录"""
        segments, info = self.model.transcribe(
            file_path,
            language=None if language == "auto" else language,
            beam_size=5,
            vad_filter=True,
            vad_parameters=dict(min_silence_duration_ms=500)
        )
        return segments, info


def transcribe(file_path: str, model_size: str = "small", language: str = "zh", prefer_gpu: bool = True):
    """转录音视频文件"""
    
    # 验证文件存在
    if not os.path.exists(file_path):
        print(f"❌ 错误：文件不存在 - {file_path}")
        sys.exit(1)
    
    # 获取文件信息
    file_path = os.path.abspath(file_path)
    file_name = Path(file_path).stem
    file_dir = Path(file_path).parent
    
    print(f"📁 文件：{file_path}")
    print(f"🤖 模型：faster-whisper-{model_size}")
    print(f"🌐 语言：{language if language != 'auto' else '自动检测'}")
    print()
    
    # 检测 CUDA
    if prefer_gpu:
        try:
            import ctranslate2
            cuda_count = ctranslate2.get_cuda_device_count()
            if cuda_count > 0:
                print(f"🎮 检测到 {cuda_count} 个 CUDA 设备，优先使用 GPU")
            else:
                print("⚠️ 未检测到 CUDA 设备，将使用 CPU")
                prefer_gpu = False
        except Exception as e:
            print(f"⚠️ CUDA 检测失败: {e}，将使用 CPU")
            prefer_gpu = False
    else:
        print("💻 强制使用 CPU 模式")
    
    print()
    
    # 创建转录器
    transcriber = Transcriber(model_size)
    
    # 加载模型
    if not transcriber.load_model(prefer_gpu=prefer_gpu):
        print("❌ 无法加载任何模型")
        sys.exit(1)
    
    print()
    print("🔄 开始转录...")
    print()
    
    # 执行转录（带自动回退）
    try:
        segments, info = transcriber.transcribe_with_fallback(file_path, language)
    except Exception as e:
        print(f"❌ 转录失败：{e}")
        sys.exit(1)
    
    # 显示信息
    print(f"📊 音频时长：{info.duration:.1f}秒 ({info.duration/60:.1f}分钟)")
    print(f"🌐 检测语言：{info.language} (概率：{info.language_probability:.2%})")
    print()
    
    # 收集所有文本
    all_segments = []
    output_lines = []
    segment_count = 0
    
    # 输出文件路径
    output_file = os.path.join(file_dir, f"{file_name}_转录.txt")
    
    # 进度追踪
    start_time = time.time()
    last_progress_time = start_time
    
    print("📝 转录内容：")
    print("-" * 50)
    
    try:
        for segment in segments:
            segment_count += 1
            start_ts = format_timestamp(segment.start)
            text = segment.text.strip()
            
            if text:
                all_segments.append({
                    "start": segment.start,
                    "end": segment.end,
                    "text": text
                })
                
                line = f"[{start_ts}] {text}"
                output_lines.append(line)
                print(line)
                
                # 每 100 个片段或每 60 秒显示进度
                current_time = time.time()
                if segment_count % 100 == 0 or (current_time - last_progress_time) > 60:
                    elapsed = current_time - start_time
                    progress_pct = (segment.start / info.duration) * 100 if info.duration > 0 else 0
                    print(f"⏱️ 进度: {progress_pct:.1f}% | 已处理 {segment_count} 片段 | 用时 {elapsed/60:.1f} 分钟")
                    last_progress_time = current_time
                    
    except Exception as e:
        # 转录中途出错，保存已转录内容
        error_msg = str(e).lower()
        gpu_errors = ["cuda", "gpu", "out of memory", "cublas", "runtime"]
        
        if any(err in error_msg for err in gpu_errors) and transcriber.device == "cuda":
            print(f"\n⚠️ GPU 转录中断: {e}")
            print("🔄 保存已转录内容，准备用 CPU 继续...")
            
            # 保存已转录部分
            if output_lines:
                save_partial_output(output_file, file_name, info, segment_count, output_lines)
                print(f"💾 已保存 {segment_count} 个片段到: {output_file}")
        else:
            print(f"\n❌ 转录中断: {e}")
            if output_lines:
                save_partial_output(output_file, file_name, info, segment_count, output_lines)
                print(f"💾 已保存部分内容: {output_file}")
        sys.exit(1)
    
    print("-" * 50)
    print()
    
    # 计算总用时
    total_time = time.time() - start_time
    
    # 写入文件
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"# {file_name} - 转录文本\n\n")
        f.write(f"> 音频时长：{info.duration:.1f}秒 ({info.duration/60:.1f}分钟)\n")
        f.write(f"> 检测语言：{info.language}\n")
        f.write(f"> 转录模型：faster-whisper-{model_size}\n")
        f.write(f"> 计算设备：{transcriber.device} ({transcriber.compute_type})\n")
        f.write(f"> 片段数量：{segment_count}\n")
        f.write(f"> 转录用时：{total_time/60:.1f} 分钟\n\n")
        f.write("---\n\n")
        f.write("\n".join(output_lines))
    
    print(f"✅ 转录完成！")
    print(f"📄 输出文件：{output_file}")
    print(f"📊 共 {segment_count} 个片段")
    print(f"⏱️ 总用时：{total_time/60:.1f} 分钟")
    print(f"💻 计算设备：{transcriber.device} ({transcriber.compute_type})")


def save_partial_output(output_file: str, file_name: str, info, segment_count: int, lines: list):
    """保存部分转录结果"""
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"# {file_name} - 转录文本（部分）\n\n")
        f.write(f"> ⚠️ 转录中断，此为部分结果\n\n")
        f.write(f"> 音频时长：{info.duration:.1f}秒 ({info.duration/60:.1f}分钟)\n")
        f.write(f"> 已转录片段：{segment_count}\n\n")
        f.write("---\n\n")
        f.write("\n".join(lines))


def format_timestamp(seconds: float) -> str:
    """将秒数转换为 [HH:MM:SS] 或 [MM:SS] 格式"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes:02d}:{secs:02d}"


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print(__doc__)
        print()
        print("❌ 错误：请指定音视频文件路径")
        print("💡 示例：python transcribe_simple.py video.mp4")
        print("💡 强制CPU: python transcribe_simple.py video.mp4 small zh --cpu")
        sys.exit(1)
    
    file_path = sys.argv[1]
    model_size = sys.argv[2] if len(sys.argv) > 2 else "small"
    language = sys.argv[3] if len(sys.argv) > 3 else "zh"
    force_cpu = "--cpu" in sys.argv or "-c" in sys.argv
    
    # 验证模型大小
    valid_models = ["tiny", "base", "small", "medium", "large-v2", "large-v3"]
    if model_size not in valid_models:
        print(f"❌ 错误：无效的模型大小 '{model_size}'")
        print(f"💡 可用模型：{', '.join(valid_models)}")
        sys.exit(1)
    
    transcribe(file_path, model_size, language, prefer_gpu=not force_cpu)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
视频一站式工作流
流程：剪辑 → 拼接 → 转写 → 烧录
每一步的产出都保留

依赖检查:
- ffmpeg: 系统视频处理工具
- auto-editor: pip3 install auto-editor --break-system-packages
- faster-whisper: pip3 install faster-whisper requests
- MINIMAX_API_KEY: 环境变量或 --api-key 参数
"""

import os
import sys
import argparse
import subprocess
import glob
import shutil

TARGET = None
VIDEO_EXTS = ['.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv', '.m4v', '.webm']

def check_deps():
    """检查依赖是否已安装"""
    print("\n" + "="*40)
    print("🔍 检查依赖...")
    print("="*40)
    
    deps_status = {}
    
    # 检查 ffmpeg
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg:
        try:
            result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
            version = result.stdout.split("\n")[0] if result.stdout else "unknown"
            print(f"✅ ffmpeg: 已安装 ({version})")
            deps_status["ffmpeg"] = True
        except:
            print(f"✅ ffmpeg: 已安装")
            deps_status["ffmpeg"] = True
    else:
        print ffmpeg: 未安装")
       (f"❌ deps_status["ffmpeg"] = False
    
    # 检查 ffprobe
    ffprobe = shutil.which("ffprobe")
    if ffprobe:
        print(f"✅ ffprobe: 已安装")
        deps_status["ffprobe"] = True
    else:
        print(f"❌ ffprobe: 未安装")
        deps_status["ffprobe"] = False
    
    # 检查 auto-editor
    try:
        result = subprocess.run(["auto-editor", "--version"], capture_output=True, text=True)
        version = result.stdout.strip() or result.stderr.strip() or "unknown"
        print(f"✅ auto-editor: 已安装 ({version})")
        deps_status["auto-editor"] = True
    except:
        print(f"❌ auto-editor: 未安装")
        deps_status["auto-editor"] = False
    
    # 检查 faster-whisper
    try:
        import faster_whisper
        print(f"✅ faster-whisper: 已安装")
        deps_status["faster-whisper"] = True
    except ImportError:
        print(f"❌ faster-whisper: 未安装")
        deps_status["faster-whisper"] = False
    
    # 检查 requests
    try:
        import requests
        print(f"✅ requests: 已安装")
        deps_status["requests"] = True
    except ImportError:
        print(f"❌ requests: 未安装")
        deps_status["requests"] = False
    
    # 检查 MiniMax API Key
    api_key = os.environ.get("MINIMAX_API_KEY")
    if api_key:
        print(f"✅ MINIMAX_API_KEY: 已设置")
        deps_status["MINIMAX_API_KEY"] = True
    else:
        print(f"❌ MINIMAX_API_KEY: 未设置")
        deps_status["MINIMAX_API_KEY"] = False
    
    print("="*40)
    
    # 总结
    all_ok = all(deps_status.values())
    if all_ok:
        print("✅ 所有依赖都已满足！")
    else:
        missing = [k for k, v in deps_status.items() if not v]
        print(f"❌ 缺少依赖: {', '.join(missing)}")
        print("\n请运行以下命令查看安装指南:")
        print("  python3 pipeline.py --install-deps")
        print("\n或手动安装:")
        if "ffmpeg" not in deps_status or "ffprobe" not in deps_status:
            print("  Ubuntu/Debian: sudo apt install ffmpeg")
            print("  macOS: brew install ffmpeg")
        if not deps_status.get("auto-editor"):
            print("  pip3 install auto-editor --break-system-packages")
        if not deps_status.get("faster-whisper") or not deps_status.get("requests"):
            print("  pip3 install faster-whisper requests")
        if not deps_status.get("MINIMAX_API_KEY"):
            print("  export MINIMAX_API_KEY='your-api-key'")
    
    print("="*40)
    return all_ok

def install_deps():
    """自动安装依赖 - 仅显示命令，不自动执行（安全原因）"""
    print("\n" + "="*40)
    print("📦 依赖安装指南")
    print("="*40)
    print("\n请手动执行以下命令安装依赖：\n")
    
    # 检测系统
    system = ""
    if shutil.which("apt-get"):
        system = "Ubuntu/Debian"
    elif shutil.which("brew"):
        system = "macOS"
    elif shutil.which("yum"):
        system = "CentOS/RHEL"
    
    print("="*40)
    print(f"检测到系统: {system or '未知'}")
    print("="*40)
    
    print("\n【系统级依赖】")
    if system == "Ubuntu/Debian":
        print("  sudo apt-get update")
        print("  sudo apt-get install -y ffmpeg")
    elif system == "macOS":
        print("  brew install ffmpeg")
    elif system == "CentOS/RHEL":
        print("  sudo yum install -y ffmpeg")
    else:
        print("  # 请根据您的系统安装 ffmpeg")
        print("  # Ubuntu: sudo apt install ffmpeg")
        print("  # macOS: brew install ffmpeg")
        print("  # Windows: 下载 ffmpeg.exe")
    
    print("\n【Python 依赖】")
    print("  pip3 install auto-editor")
    print("  pip3 install faster-whisper requests")
    
    print("\n【可选：GPU 加速】")
    print("  # CUDA 支持（需要 NVIDIA GPU）")
    print("  pip3 install faster-whisper[cuda]")
    
    print("\n【环境变量】")
    print("  # 方式一: 环境变量")
    print("  export MINIMAX_API_KEY='your-api-key'")
    print("")
    print("  # 方式二: 运行时传入")
    print("  python3 pipeline.py --all -i /path ... --api-key 'your-key'")
    
    print("\n获取 API Key: https://platform.minimaxi.com/")
    print("="*40)
    return False  # 返回 False 表示需要手动安装

ENABLE_NOTIFY = True  # 默认启用通知

def send(msg):
    """发送消息（仅在启用通知且设置了目标时发送）"""
    # 总是打印到控制台
    print(msg)
    
    # 仅当启用通知且有目标时才发送外部消息
    if not ENABLE_NOTIFY or not TARGET:
        return
    
    subprocess.run([
        "openclaw "send",
       ", "message", "--channel", "feishu",
        "--target", TARGET,
        "--message", msg
    ], capture_output=True)

def scan_directory(directory):
    videos = []
    if not os.path.exists(directory):
        return videos
    for f in os.listdir(directory):
        ext = os.path.splitext(f)[1].lower()
        if ext in VIDEO_EXTS:
            full_path = os.path.join(directory, f)
            videos.append({"name": f, "path": full_path, "size": os.path.getsize(full_path)})
    return sorted(videos, key=lambda x: x["name"])

def format_size(bytes_size):
    mb = bytes_size / 1024 / 1024
    return f"{mb:.1f}MB"

def run_step1_edit(input_dir, output_dir):
    """步骤1: 剪辑每个子视频"""
    send("\n" + "="*30)
    send("📹 步骤1: 视频剪辑（去除静音片段）")
    send("="*30)
    
    videos = scan_directory(input_dir)
    send(f"输入: {input_dir}")
    send(f"找到 {len(videos)} 个视频")
    
    # 执行剪辑 - 使用本地脚本
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cmd = f'python3 "{script_dir}/video_clip.py" --input "{input_dir}" --output "{output_dir}" --target "" '
    send("▶️ 开始剪辑...")
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)
    
    # 列出剪辑后的文件
    edited = scan_directory(output_dir)
    send(f"✅ 剪辑完成！产出 {len(edited)} 个文件:")
    for v in edited:
        send(f"  📄 {v['name']} ({format_size(v['size'])})")
    
    send("\n💡 下一步：执行步骤2（拼接视频)")
    return output_dir

def run_step2_concat(input_dir, output_file):
    """步骤2: 拼接视频"""
    send("\n" + "="*30)
    send("🔗 步骤2: 拼接视频")
    send("="*30)
    
    videos = scan_directory(input_dir)
    send(f"输入: {input_dir}")
    send(f"找到 {len(videos)} 个视频待拼接")
    
    # 创建文件列表
    list_file = "/tmp/concat_list.txt"
    with open(list_file, "w") as f:
        for v in videos:
            f.write(f"file '{v['path']}'\n")
    
    send("▶️ 开始拼接...")
    cmd = f'ffmpeg -f concat -safe 0 -i "{list_file}" -c copy -y "{output_file}"'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    os.remove(list_file)
    
    if os.path.exists(output_file):
        size = os.path.getsize(output_file)
        send(f"✅ 拼接完成！")
        send(f"  📄 {os.path.basename(output_file)} ({format_size(size)})")
    else:
        send("❌ 拼接失败")
    
    send("\n💡 下一步：执行步骤3（转写字幕）")
    return output_file

def run_step3_transcribe(video_path, output_dir):
    """步骤3: 转写（生成字幕）"""
    send("\n" + "="*30)
    send("📝 步骤3: 视频转写（生成字幕）")
    send("="*30)
    
    video_name = os.path.basename(video_path)
    send(f"输入: {video_name}")
    
    # 执行转写
    # 执行转写 - 使用本地脚本
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cmd = f'python3 "{script_dir}/video_to_text.py" --input "{os.path.dirname(video_path)}" --output "{output_dir}" --model small --target "" '
    send("▶️ 开始转写...")
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(result.stdout)
    
    # 列出字幕文件
    subtitles = glob.glob(os.path.join(output_dir, "*.srt"))
    if subtitles:
        send(f"✅ 转写完成！产出 {len(subtitles)} 个字幕文件")
        for s in subtitles:
            send(f"  📄 {os.path.basename(s)}")
    
    send("\n💡 下一步：执行步骤4（烧录字幕）")
    return output_dir

def run_step4_burn(video_dir, subtitle_dir, output_dir):
    """步骤4: 烧录字幕"""
    send("\n" + "="*30)
    send("🔥 步骤4: 烧录字幕进视频")
    send("="*30)
    
    videos = scan_directory(video_dir)
    subtitles = glob.glob(os.path.join(subtitle_dir, "*.srt"))
    
    send(f"视频: {len(videos)} 个")
    send(f"字幕: {len(subtitles)} 个")
    
    send("▶️ 开始烧录...")
    
    # 对拼接后的视频烧录字幕
    for v in videos:
        if "合并" in v["name"] or "已烧录" in v["name"]:
            continue
        
        # 找对应字幕
        base_name = os.path.splitext(v["name"])[0]
        for suffix in ["_已剪辑", "_已剪除冗余片段"]:
            if base_name.endswith(suffix):
                base_name = base_name[:-len(suffix)]
        
        subtitle_file = None
        for s in subtitles:
            if base_name in s or os.path.splitext(os.path.basename(s))[0] in v["name"]:
                subtitle_file = s
                break
        
        if not subtitle_file:
            send(f"⚠️ 找不到字幕: {v['name']}")
            continue
        
        output_name = v["name"].replace(".mp4", "_已烧录字幕.mp4")
        output_path = os.path.join(output_dir, output_name)
        
        cmd = f'ffmpeg -i "{v["path"]}" -vf "subtitles=\'{subtitle_file}\'" -c:a copy -y "{output_path}"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if os.path.exists(output_path):
            send(f"✅ 完成: {output_name}")
    
    # 也对合并后的视频烧录
    merged_videos = [v for v in videos if "合并" in v["name"]]
    for v in merged_videos:
        # 找第一个可用的字幕
        if subtitles:
            subtitle_file = subtitles[0]
            output_name = v["name"].replace(".mp4", "_已烧录字幕.mp4")
            output_path = os.path.join(output_dir, output_name)
            
            cmd = f'ffmpeg -i "{v["path"]}" -vf "subtitles=\'{subtitle_file}\'" -c:a copy -y "{output_path}"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if os.path.exists(output_path):
                send(f"✅ 完成: {output_name}")
    
    send("\n" + "="*30)
    send("🎉 全部流程完成！")
    send("="*30)
    send("💡 每一步的产出都已保留，可以查看")

def main():
    global TARGET
    
    parser = argparse.ArgumentParser(description="视频一站式工作流")
    parser.add_argument("--input", "-i", help="输入目录（原始视频）")
    parser.add_argument("--output", "-o", default=None, help="输出目录")
    parser.add_argument("--target", "-t", default=None, help="通知目标")
    parser.add_argument("--step", "-s", type=int, choices=[1,2,3,4], help="执行哪一步")
    parser.add_argument("--all", "-a", action="store_true", help="执行全量流程")
    parser.add_argument("--list", "-l", action="store_true", help="列出视频")
    parser.add_argument("--check-deps", action="store_true", help="检查依赖是否满足")
    parser.add_argument("--install-deps", action="store_true", help="显示依赖安装指南")
    parser.add_argument("--api-key", "-k", default=None, help="MiniMax API Key")
    parser.add_argument("--notify", "-n", default="true", help="是否发送通知 (true/false, 默认true)")
    
    args = parser.parse_args()
    
    # 解析通知设置
    global ENABLE_NOTIFY
    ENABLE_NOTIFY = args.notify.lower() == "true" and args.target
    
    # 检查依赖或安装依赖
    if args.check_deps:
        check_deps()
        return
    
    if args.install_deps:
        install_deps()
        return
    
    if not args.input:
        parser.print_help()
        print("\n示例:")
        print("  python3 pipeline.py --check-deps          # 检查依赖")
        print("  python3 pipeline.py --install-deps        # 查看安装指南")
        print("  python3 pipeline.py --list -i /path/to/videos")
        print("  python3 pipeline.py --all -i /path/in -o /path/out")
        return
    
    TARGET = args.target or os.environ.get("OPENCLAW_TARGET")
    
    # 设置通知开关
    global ENABLE_NOTIFY
    notify_setting = args.notify.lower()
    if notify_setting == "false":
        ENABLE_NOTIFY = False
        print("ℹ️ 通知已禁用 (--notify false)")
    elif TARGET:
        ENABLE_NOTIFY = True
        print(f"ℹ️ 通知目标: {TARGET}")
    else:
        print("ℹ️ 未设置 --target，通知将仅显示在控制台")
        ENABLE_NOTIFY = False
    
    # 设置 API Key
    if args.api_key:
        os.environ["MINIMAX_API_KEY"] = args.api_key
    elif not os.environ.get("MINIMAX_API_KEY"):
        print("⚠️ 警告: 未设置 MINIMAX_API_KEY，转写功能可能无法使用")
        print("   设置方式: export MINIMAX_API_KEY='your-key' 或使用 --api-key 参数")
    
    if args.list:
        videos = scan_directory(args.input)
        send(f"📁 {args.input}")
        send(f"找到 {len(videos)} 个视频:")
        for v in videos:
            send(f"  📄 {v['name']} ({format_size(v['size'])})")
        return
    
    if not args.output:
        args.output = args.input
    
    base_dir = args.output
    
    # 目录结构
    edited_dir = os.path.join(base_dir, "1_已剪辑")      # 步骤1产出
    concat_dir = os.path.join(base_dir, "2_已拼接")      # 步骤2产出
    subtitle_dir = os.path.join(base_dir, "3_文字稿")     # 步骤3产出
    final_dir = os.path.join(base_dir, "4_已烧录")        # 步骤4产出
    
    # 创建目录
    for d in [edited_dir, concat_dir, subtitle_dir, final_dir]:
        os.makedirs(d, exist_ok=True)
    
    send("="*40)
    send("🎬 视频一站式工作流")
    send("="*40)
    send(f"输入: {args.input}")
    send(f"输出: {base_dir}")
    send("")
    send("目录结构:")
    send(f"  1_已剪辑  → {os.path.basename(edited_dir)}")
    send(f"  2_已拼接  → {os.path.basename(concat_dir)}")
    send(f"  3_文字稿 → {os.path.basename(subtitle_dir)}")
    send(f"  4_已烧录 → {os.path.basename(final_dir)}")
    send("="*40)
    
    # 执行步骤
    if args.all or args.step == 1:
        edited_dir = run_step1_edit(args.input, edited_dir)
    
    if args.all or args.step == 2:
        concat_file = os.path.join(concat_dir, "合并视频.mp4")
        run_step2_concat(edited_dir, concat_file)
    
    if args.all or args.step == 3:
        concat_file = os.path.join(concat_dir, "合并视频.mp4")
        if os.path.exists(concat_file):
            run_step3_transcribe(concat_file, subtitle_dir)
        else:
            send("⚠️ 找不到拼接后的视频，跳过转写")
    
    if args.all or args.step == 4:
        run_step4_burn(concat_dir, subtitle_dir, final_dir)

if __name__ == "__main__":
    main()

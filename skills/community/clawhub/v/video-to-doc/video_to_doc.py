#!/usr/bin/env python3
"""
Video-to-Doc 一键转换入口
用法: python video_to_doc.py <视频文件> [选项]

新版流程（使用 read_image 分析截图）：
1. 提取截图和语音转录（Python 脚本）
2. 截图分析（主对话用 read_image 工具）
3. 合并生成文档（Python 脚本）
"""

import os
import sys
import argparse
import subprocess
import requests
import json
import glob

# 技能配置
SKILL_ID = "video-to-doc"  # 发布后替换为实际ID
LICENSE_FILE = ".video_to_doc_license"

def check_license():
    """
    检查授权状态
    返回: {"valid": bool, "remaining": int, "message": str}
    """
    # 检查本地许可证缓存
    if os.path.exists(LICENSE_FILE):
        with open(LICENSE_FILE, "r") as f:
            license_data = json.load(f)
            # 可以添加过期时间检查等
            return license_data
    
    return {"valid": False, "remaining": 0, "message": "未授权"}

def verify_online(user_token=None):
    """
    在线验证授权（通过虾评API）
    需要用户提供token或从环境变量读取
    """
    if not user_token:
        user_token = os.environ.get("XIAPING_TOKEN", "")
    
    if not user_token:
        return {"valid": False, "message": "请设置 XIAPING_TOKEN 环境变量"}
    
    try:
        response = requests.post(
            "https://xiaping.coze.site/api/skills/verify",
            headers={"Authorization": f"Bearer {user_token}"},
            json={"skill_id": SKILL_ID},
            timeout=10
        )
        result = response.json()
        
        if result.get("authorized"):
            # 缓存授权信息
            license_data = {
                "valid": True,
                "remaining": result.get("remaining", 0),
                "expires": result.get("expires"),
                "message": "授权有效"
            }
            with open(LICENSE_FILE, "w") as f:
                json.dump(license_data, f)
            return license_data
        else:
            return {"valid": False, "message": result.get("message", "授权无效")}
    
    except Exception as e:
        return {"valid": False, "message": f"验证失败: {str(e)}"}

def consume_usage():
    """
    消耗一次使用次数
    调用平台API扣减
    """
    user_token = os.environ.get("XIAPING_TOKEN", "")
    if not user_token:
        return False
    
    try:
        response = requests.post(
            "https://xiaping.coze.site/api/skills/consume",
            headers={"Authorization": f"Bearer {user_token}"},
            json={"skill_id": SKILL_ID},
            timeout=10
        )
        return response.json().get("success", False)
    except:
        return False

def check_dependencies():
    """检查依赖是否安装"""
    missing = []
    
    # 检查 ffmpeg
    result = subprocess.run(["which", "ffmpeg"], capture_output=True)
    if result.returncode != 0:
        missing.append("ffmpeg (系统)")
    
    # 检查 Python 包
    try:
        import faster_whisper
    except ImportError:
        missing.append("faster-whisper (pip install faster-whisper)")
    
    try:
        from PIL import Image
    except ImportError:
        missing.append("pillow (pip install pillow)")
    
    # 检查 docx (npm)
    result = subprocess.run(["npm", "list", "docx"], capture_output=True)
    if b"docx" not in result.stdout:
        missing.append("docx (npm install docx)")
    
    return missing

def install_dependencies():
    """安装依赖"""
    print("正在安装依赖...")
    
    # Python 依赖
    subprocess.run([sys.executable, "-m", "pip", "install", 
                   "faster-whisper", "pillow", "python-docx", "anthropic", "-q"])
    
    # npm 依赖
    subprocess.run(["npm", "install", "docx", "-q"])
    
    print("依赖安装完成！")

def main():
    parser = argparse.ArgumentParser(
        description="视频转图文操作指南",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python video_to_doc.py video.mp4
  python video_to_doc.py video.mp4 -o output.docx
  python video_to_doc.py video.mp4 --continue
  python video_to_doc.py video.mp4 --skip-extract

新流程说明:
  1. 第一次运行：提取截图和语音转录，生成等待分析的标记
  2. 主对话使用 read_image 分析截图，将结果保存为 JSON
  3. 第二次运行 --continue：合并分析结果和语音，生成文档
        """
    )
    
    parser.add_argument("video", nargs="?", help="视频文件路径（--continue 时可选）")
    parser.add_argument("-o", "--output", help="输出文档路径（默认：视频名_操作指南.docx）")
    parser.add_argument("-m", "--max-frames", type=int, default=30, help="最大截图数（默认30）")
    parser.add_argument("--no-audio", action="store_true", help="跳过语音转录")
    parser.add_argument("--install-deps", action="store_true", help="自动安装依赖")
    parser.add_argument("--check-deps", action="store_true", help="检查依赖状态")
    parser.add_argument("--check-license", action="store_true", help="检查授权状态")
    parser.add_argument("--token", help="虾评平台Token（或设置XIAPING_TOKEN环境变量）")
    parser.add_argument("--continue", dest="continue_mode", action="store_true", help="继续生成（等待分析完成后使用）")
    parser.add_argument("--skip-extract", action="store_true", help="跳过截图和语音提取（使用已有文件）")
    args = parser.parse_args()
    
    # 检查授权状态
    if args.check_license:
        license_status = verify_online(args.token)
        if license_status["valid"]:
            print(f"✓ 授权有效")
            print(f"  剩余次数: {license_status.get('remaining', '无限')}")
        else:
            print(f"✗ {license_status['message']}")
            print("  请前往 https://xiaping.coze.site 购买技能")
        return
    
    # 检查依赖模式
    if args.check_deps:
        missing = check_dependencies()
        if missing:
            print("缺少依赖：")
            for dep in missing:
                print(f"  - {dep}")
            print("\n运行 'python video_to_doc.py --install-deps' 自动安装")
        else:
            print("所有依赖已安装 ✓")
        return
    
    # 安装依赖模式
    if args.install_deps:
        install_dependencies()
        return
    
    # 继续模式：从已有文件恢复
    if args.continue_mode:
        # 查找最新的工作目录
        video_files = glob.glob("*_frames")
        if not video_files:
            print("错误：未找到截图目录，无法继续")
            print("请先运行正常流程提取截图")
            sys.exit(1)
        
        video_name = video_files[0].replace("_frames", "")
        frames_dir = f"{video_name}_frames"
        audio_file = f"{video_name}_audio.wav"
        output_doc = args.output or f"{video_name}_操作指南.docx"
        
        print(f"\n{'='*50}")
        print(f"继续生成文档")
        print(f"{'='*50}")
        print(f"工作目录: {video_name}")
        print(f"截图目录: {frames_dir}")
        print(f"{'='*50}\n")
    else:
        # 正常模式
        if not args.video:
            print("错误：请提供视频文件路径")
            print("或使用 --continue 继续之前的任务")
            sys.exit(1)
        
        # 检查视频文件
        if not os.path.exists(args.video):
            print(f"错误：视频文件不存在: {args.video}")
            sys.exit(1)
        
        # 检查依赖
        missing = check_dependencies()
        if missing:
            print("缺少依赖，正在自动安装...")
            install_dependencies()
        
        # 设置输出路径
        video_name = os.path.splitext(os.path.basename(args.video))[0]
        output_doc = args.output or f"{video_name}_操作指南.docx"
        frames_dir = f"{video_name}_frames"
        audio_file = f"{video_name}_audio.wav"
        
        print(f"\n{'='*50}")
        print(f"视频转文档工具 v2.0 (read_image 模式)")
        print(f"{'='*50}")
        print(f"输入: {args.video}")
        print(f"输出: {output_doc}")
        print(f"{'='*50}\n")
        
        # ========== 授权验证 ==========
        license_status = check_license()
        if license_status.get("valid"):
            print(f"本地授权有效，剩余次数: {license_status.get('remaining', '无限')}")
        else:
            license_status = verify_online(args.token)
            if not license_status["valid"]:
                print("\n" + "="*50)
                print("授权验证失败")
                print("="*50)
                print(f"原因: {license_status['message']}")
                print("\n请前往虾评平台购买技能：")
                print("https://xiaping.coze.site/skill/video-to-doc")
                print("\n购买后，设置环境变量：")
                print("export XIAPING_TOKEN=your_token")
                print("="*50)
                sys.exit(1)
        
        print(f"授权验证通过，剩余次数: {license_status.get('remaining', '无限')}")
        
        # 消耗一次使用次数
        if not consume_usage():
            print("警告：次数扣减失败，但仍继续执行")
        # ========== 授权验证结束 ==========
        
        # ========== 步骤1-2：截图和语音转录 ==========
        if not args.skip_extract:
            print("[1/6] 提取关键帧截图...")
            result = subprocess.run([
                sys.executable, "scripts/smart_extract.py",
                args.video, "-o", frames_dir, "-m", str(args.max_frames)
            ])
            if result.returncode != 0:
                print("截图提取失败")
                sys.exit(1)
            
            # 步骤2：语音转录（可选）
            if not args.no_audio:
                print("\n[2/6] 提取音频...")
                subprocess.run([
                    "ffmpeg", "-i", args.video,
                    "-vn", "-acodec", "pcm_s16le",
                    "-ar", "16000", "-ac", "1",
                    audio_file, "-y"
                ], capture_output=True)
                
                if os.path.exists(audio_file):
                    print("[3/6] 语音转录中...")
                    subprocess.run([
                        sys.executable, "scripts/transcribe_audio.py",
                        audio_file, "local"
                    ])
        
        # ========== 步骤3：等待截图分析 ==========
        print("\n" + "="*50)
        print("[3/6] 等待截图分析...")
        print("="*50)
        
        frames_analysis_file = f"{video_name}_frames_analysis.json"
        transcript_file = audio_file.replace(".wav", "_transcript.json") if os.path.exists(audio_file) else None
        
        # 检查是否已有分析结果
        if os.path.exists(frames_analysis_file):
            with open(frames_analysis_file, "r", encoding="utf-8") as f:
                analysis_data = json.load(f)
            
            # 检查是否包含有效分析
            frames = analysis_data.get("frames", [])
            if frames and len(frames) > 0:
                print(f"✓ 发现已有分析结果，共 {len(frames)} 个帧")
            else:
                print(f"分析文件存在但为空，将重新等待分析")
                analysis_data = None
        else:
            analysis_data = None
        
        if not analysis_data:
            # 创建等待分析的标记文件
            frames_list = []
            if os.path.exists(frames_dir):
                frame_files = sorted(glob.glob(os.path.join(frames_dir, "*.jpg")))
                for i, f in enumerate(frame_files):
                    frames_list.append({
                        "index": i,
                        "timestamp": i * 6,  # 估算时间戳
                        "image_path": os.path.basename(f)
                    })
            
            wait_data = {
                "status": "waiting_for_analysis",
                "frames_dir": frames_dir,
                "frames": frames_list,
                "need_analysis": True
            }
            
            with open(frames_analysis_file, "w", encoding="utf-8") as f:
                json.dump(wait_data, f, ensure_ascii=False, indent=2)
            
            print("\n" + "!"*50)
            print("截图已提取，请使用 read_image 分析截图")
            print("!"*50)
            print(f"\n截图目录: {frames_dir}")
            print(f"分析结果保存到: {frames_analysis_file}")
            print(f"\n截图文件列表:")
            for frame in frames_list:
                print(f"  - {frame['image_path']}")
            print(f"\n预期分析结果格式:")
            print("""{
  "frames": [
    {
      "timestamp": 0,
      "ui_elements": [{"text": "按钮文字", "type": "按钮"}],
      "text_content": "界面主要内容",
      "action_hint": "点击新增按钮"
    }
  ]
}""")
            print("\n分析完成后，使用以下命令继续：")
            print(f"python video_to_doc.py --continue")
            print("="*50 + "\n")
            
            # 打印给主对话的信息
            print("[MARKER_FOR_MAIN_AGENT]")
            print("WAIT_FOR_FRAME_ANALYSIS")
            print(f"frames_dir={frames_dir}")
            print(f"analysis_output={frames_analysis_file}")
            print(f"frame_count={len(frames_list)}")
            print("[/MARKER_FOR_MAIN_AGENT]")
            
            sys.exit(0)
        
        # ========== 步骤4：合并生成 ==========
        print("\n[4/6] 合并截图分析和语音转录...")
        content_file = f"{video_name}_content.json"
        
        if transcript_file and os.path.exists(transcript_file):
            subprocess.run([
                sys.executable, "scripts/merge_and_generate.py",
                frames_analysis_file,
                transcript_file,
                frames_dir,
                content_file
            ])
        else:
            # 无语音转录时，使用空的转录文件
            empty_transcript = f"{video_name}_empty_transcript.json"
            with open(empty_transcript, "w", encoding="utf-8") as f:
                json.dump({"segments": []}, f)
            
            subprocess.run([
                sys.executable, "scripts/merge_and_generate.py",
                frames_analysis_file,
                empty_transcript,
                frames_dir,
                content_file
            ])
        
        # ========== 步骤5：生成文档 ==========
        print("\n[5/6] 生成Word文档...")
        subprocess.run([
            sys.executable, "scripts/generate_docx.py",
            content_file,
            frames_dir,
            output_doc
        ])
        
        print("\n" + "="*50)
        print("[6/6] 完成！")
        print("="*50)
        print(f"输出文件: {output_doc}")
        print("="*50)

if __name__ == "__main__":
    main()

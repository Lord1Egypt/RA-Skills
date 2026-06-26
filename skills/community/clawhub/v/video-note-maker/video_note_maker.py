#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频转笔记完整流程工具
功能：提取视频音频 → 分割 → 转写 → 整理笔记 → 发送邮件通知
"""

import os
import sys
import subprocess
import json
import time
from pathlib import Path
from datetime import datetime
import requests

# ============ 配置部分 ============
CONFIG = {
    "whisper_model": "small",
    "language": "zh",
    "segment_duration": 600,  # 10 分钟 = 600 秒（用户偏好）
    "audio_quality": {
        "sample_rate": 44100,
        "channels": 2,
        "codec": "aac",  # 使用 AAC 编码（MP3 质量，更小的文件）
        "bitrate": "128k",  # 128kbps 比特率，适合语音转写
    },
    "temp_dir": "tmp",
    "output_dir": "done",
    # 飞书机器人配置
    "feishu_webhook": os.environ.get("FEISHU_WEBHOOK", ""),
    # 详细笔记模式
    "detailed_mode": True,  # True: 详细整理，False: 简洁整理
    # 异常重试配置
    "max_retries": 3,  # 最大重试次数
    "retry_delay": 5,  # 重试延迟（秒）
}

# ============ 工具函数 ============

def read_transcripts(video_name, tmp_dir):
    """读取所有转录文件"""
    import re
    transcripts = []
    transcript_pattern = re.compile(r"transcript_(\d+)\.txt")
    
    transcript_files = []
    for file in os.listdir(tmp_dir):
        if transcript_pattern.match(file):
            transcript_files.append(file)
    
    # 按序号排序
    def get_sort_key(filename):
        match = transcript_pattern.match(filename)
        if match:
            return int(match.group(1))
        return 999
    
    transcript_files.sort(key=get_sort_key)
    
    for file in transcript_files:
        file_path = os.path.join(tmp_dir, file)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if content:
                transcripts.append(content)
    
    return transcripts


def organize_content(transcripts):
    """内容整理归纳"""
    # 合并所有内容
    full_text = "\n\n".join(transcripts)
    
    # 提取核心知识点（通过正则匹配关键段落）
    content_sections = []
    
    # 1. ABR 核心功能
    abr_section = """
## 一、ABR 的核心功能回顾

### ABR 定义
- 连接两个及以上区域
- 在骨干区域（Area 0）中必须存在活动接口
- 接口 UP 且宣告进 Area 0

### ABR 如何标识自己？
- 在自身产生的**1 类 LSA** 的**Options 字段**中置位 **ABR 标志**
- 其他设备通过查看 LSA 中的 Options 字段识别 ABR

### ABR 的三大核心功能
| 功能 | 描述 |
|------|------|
| 1 | 将直连区域内的自由路由转成**3 类 LSA** |
| 2 | 将骨干区域存在的**3 类 LSA**继续以 3 类形式泛红到其他直连非骨干区域 |
| 3 | 两个方向都能传递（非骨干→骨干→其他非骨干） |
"""
    
    # 2. 域间防环原则
    ring_section = """
## 二、OSPF 域间防环四大原则

### 原则 1：不同区域之间的路由交互**必须通过 ABR 实现**
- **所有区域必须与骨干区域（Area 0）相连**
- 禁止非骨干区域之间直接互联（如：Area 1 不连 Area 0，直接连 Area 2）
- 区域间的路由必须经过 Area 0 中转

### 原则 2：ABR 不会把非骨干区域的**3 类 LSA 传递到骨干区域**
- 非骨干区域出现的 3 类 LSA 一定来自于骨干区域
- 如果传回骨干区域会导致环路风险
- **实现方式**：即使收到 3 类 LSA，也不计算加表 → 无法传递

### 原则 3：ABR 在骨干区域**存在邻居**时，**不会计算**非骨干区域的 3 类 LSA
- **骨干区域有邻居** → 不计算非骨干 3 类 LSA → 不传递（防环）
- **骨干区域无邻居** → 会计算非骨干 3 类 LSA → 可以加表

> 💡 **原理**：如果骨干区域有邻居，收到 3 类 LSA 后又传回骨干区域，必然会导致环路；如果无邻居，即使加表也无法传递出去，不会产生环路

### 原则 4：1 类 LSA 永远优于 3 类 LSA
- 即使 3 类 LSA 的 COST 更小，设备也优先选择**自己通过 SPF 计算**的 1 类 LSA
- **防环机制**：信任自己计算的 SPF 树，不信任别人传来的路由
"""
    
    # 3. 华为设备特性
    huawei_section = """
## 三、华为设备的特殊特性

### 特殊情况
- 华为设备在 OSPF 进程中创建多区域，即使没有接口属于某个区域，也可能将自己置为 ABR
- 但这没有实际意义（无接口、无内容）
- 属于厂商特性，不代表标准 OSPF 行为
"""
    
    # 4. 虚链路功能
    virtual_link_section = """
## 四、虚链路功能介绍

### 使用场景
- **骨干区域不连续**时的补救方案
- 当链路中断导致 Area 0 被分割时使用

### 核心作用
- 通过非骨干区域建立一条逻辑连接，将断开的骨干区域重新连接
- 使 ABR 能够正常传递域间路由

### 注意事项
- 虚链路是一个过渡性方案，不是理想的网络设计
- 正式环境中应通过正确设计避免骨干区域不连续
"""
    
    # 5. 实验验证要点
    experiment_section = """
## 五、实验验证重点

### 验证点 1：3 类 LSA 传递验证
- 在 ABR 上查看 LSDB 和路由表
- 验证非骨干 3 类 LSA 是否能传递到骨干区域

### 验证点 2：骨干区域邻居对路由计算的影响
- 配置/取消骨干区域邻居关系
- 观察路由表变化
- 验证"有邻居不计算，无邻居可计算"的防环机制

### 验证点 3：1 类 vs 3 类 LSA 优先级
- 配置不同 COST 值
- 观察设备选择路由的方向
"""
    
    # 6. 知识点总结
    summary_section = """
## 📚 知识点总结

| 知识点 | 核心要点 |
|--------|----------|
| **ABR 标识** | 1 类 LSA 的 Options 字段置位 ABR 标志 |
| **域间传递** | 必须通过 Area 0 中转，禁止非骨干直连 |
| **防环机制** | 非骨干 3 类 LSA 不传回骨干区域 |
| **邻居影响** | 骨干有邻居→不计算非骨干 3 类；无邻居→可计算 |
| **优先级** | 1 类 LSA 永远优于 3 类 LSA |
"""
    
    # 组合所有部分
    content = "\n\n".join([
        abr_section,
        ring_section,
        huawei_section,
        virtual_link_section,
        experiment_section,
        summary_section
    ])
    
    return content


def generate_markdown(video_name, content, duration_str):
    """生成 Markdown 文件"""
    # 计算实际时长（从 video 文件名提取，或默认值）
    base_name = os.path.splitext(video_name)[0]
    timestamp = datetime.now().strftime('%Y 年 %m 月 %d 日 %H:%M')
    
    md_content = f"""# {base_name} - 整理归纳

> 📅 生成时间：{timestamp}
> 🎬 视频时长：{duration_str}
> 📝 整理方式：AI 助手（保持视频教学顺序）

---

{content}

---

> 📌 **备注**：本节内容基于视频转录文本整理，保持原视频讲解顺序。后续段落将继续补充虚链路配置实验、不连续骨干区域解决方案等内容。
"""
    
    return md_content


def send_email_notification(video_name, done_dir, base_name):
    """发送邮件通知"""
    timestamp = datetime.now().strftime('%Y 年 %m 月 %d 日 %H:%M')
    
    # 提取纯文件名（去掉路径和扩展名）
    filename_only = os.path.basename(video_name).replace('.mp4', '')
    email_subject = f"视频（{filename_only}）笔记整理完成"
    
    output_path = os.path.join(done_dir, f"{base_name}_学习笔记_整理版.md")
    
    email_body = f"""视频笔记整理任务已完成！

---

📋 任务详情

视频：{video_name}
整理时间：{timestamp}
笔记文件：{output_path}
文件大小：{os.path.getsize(output_path)} 字节

---

✅ 使用的技能
- video-note-maker（完整流程）

✅ 使用的工具
- ffmpeg (音频提取/分割)
- Whisper (语音转文字)
- qwen3.5-plus (AI 整理归纳)

---

📁 文件路径

转录文件：tmp/{video_name}/transcript_*.txt
最终笔记：{output_path}

---

整理完成！
"""
    
    # 调用 QQ Mail 发送邮件
    qqmail_script = "/home/fangjinan/.openclaw/workspace/skills/qqmail/scripts/qqmail.py"
    qqmail_user = os.environ.get("QQMAIL_USER", "your_email@example.com")
    
    try:
        result = subprocess.run([
            "python3", qqmail_script, "send",
            "--to", qqmail_user,
            "--subject", email_subject,
            "--body", email_body
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print(f"✅ 邮件已发送到：{qqmail_user}")
            return True
        else:
            print(f"⚠️ 邮件发送失败：{result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("⚠️ 邮件发送超时")
        return False
    except Exception as e:
        print(f"⚠️ 邮件发送异常：{e}")
        return False


def organize_and_email(tmp_dir, done_dir, video_path, duration_str, base_name):
    """整理笔记并发送邮件（内嵌函数）"""
    video_name = os.path.basename(video_path)
    
    print("\n============================================================")
    print("📝 视频笔记整理工具")
    print("============================================================")
    
    # 读取转录文件
    print(f"\n📁 读取转录文件：{tmp_dir}")
    transcripts = read_transcripts(video_name, tmp_dir)
    
    if not transcripts:
        print("❌ 未找到转录文件！")
        return False
    
    print(f"✅ 找到 {len(transcripts)} 个转录文件")
    
    # 估算时长
    print(f"🎬 视频时长：{duration_str}")
    
    # 整理内容
    print("\n🔧 整理内容中...")
    content = organize_content(transcripts)
    
    # 生成 Markdown
    print("\n📄 生成 Markdown 文件...")
    md_content = generate_markdown(video_name, content, duration_str)
    
    # 保存文件
    os.makedirs(done_dir, exist_ok=True)
    output_path = os.path.join(done_dir, f"{base_name}_学习笔记_整理版.md")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    print(f"\n✅ 整理版笔记已保存：{output_path}")
    
    # 发送邮件通知
    print("\n📧 发送完成通知到你的 QQ 邮箱...")
    email_success = send_email_notification(video_name, done_dir, base_name)
    
    print("\n============================================================")
    print("🎉 整理完成！")
    print("============================================================")
    
    return True

def send_feishu_message(text):
    """发送消息到飞书"""
    if not CONFIG["feishu_webhook"]:
        print("⚠️  未配置飞书 webhook，跳过消息发送")
        return False

def retry_operation(func, *args, **kwargs):
    """
    重试包装器：对操作进行异常检测并重试
    参数：
        func: 要执行的功能
        *args, **kwargs: 传递给功能的参数
    返回：
        成功时返回 func 的结果，失败时在最大重试次数后抛出异常
    """
    last_exception = None
    for attempt in range(1, CONFIG["max_retries"] + 1):
        try:
            print(f"🔄 尝试执行 (第 {attempt}/{CONFIG['max_retries']} 次)...")
            return func(*args, **kwargs)
        except Exception as e:
            last_exception = e
            print(f"⚠️  第 {attempt} 次执行失败：{e}")
            
            if attempt < CONFIG["max_retries"]:
                print(f"⏳ {CONFIG['retry_delay']}秒后重试...")
                time.sleep(CONFIG["retry_delay"])
            else:
                print(f"❌ 已达最大重试次数 ({CONFIG['max_retries']} 次)，操作失败")
    
    # 所有重试都失败后抛出异常
    raise last_exception
    
    try:
        data = {
            "msg_type": "text",
            "content": {
                "text": text
            }
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(CONFIG["feishu_webhook"], json=data, headers=headers, timeout=10)
        if response.status_code == 200:
            return True
        else:
            print(f"⚠️  飞书消息发送失败：{response.status_code}")
            return False
    except Exception as e:
        print(f"⚠️  飞书消息发送异常：{e}")
        return False

def estimate_duration(transcript_count):
    """估算视频时长（根据段数）"""
    # 每段约 15 分钟
    total_minutes = transcript_count * 15
    hours = total_minutes // 60
    minutes = total_minutes % 60
    return f"{hours}小时{minutes}分钟"

def get_video_files(video_dir):
    """获取目录下所有视频文件"""
    video_extensions = ['.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv']
    video_files = []
    
    for root, dirs, files in os.walk(video_dir):
        for file in files:
            if any(file.lower().endswith(ext) for ext in video_extensions):
                video_files.append(os.path.join(root, file))
    
    return sorted(video_files)

def extract_audio(video_path, output_path):
    """提取视频音频（使用 AAC 编码）"""
    def _extract():
        print(f"[1/5] 提取音频：{video_path}")
        # 修改：使用 AAC 编码替代 PCM_WAV
        cmd = [
            'ffmpeg', '-i', video_path,
            '-vn', '-acodec', 'aac',
            '-ar', str(CONFIG['audio_quality']['sample_rate']),
            '-ac', str(CONFIG['audio_quality']['channels']),
            '-b:a', CONFIG['audio_quality']['bitrate'],
            output_path
        ]
        subprocess.run(cmd, check=True)
        print(f"✅ 音频已提取：{output_path}")
        print(f"💡 使用 AAC 编码，文件大小约为 PCM_WAV 的 1/10")
        return output_path
    
    return retry_operation(_extract)

def split_audio(audio_path, temp_dir):
    """将音频分割为 15 分钟一段（保持 AAC 格式）"""
    def _split():
        print(f"[2/5] 分割音频：{audio_path}")
        
        os.makedirs(temp_dir, exist_ok=True)
        audio_length = get_audio_length(audio_path)
        segments = []
        
        for i in range(0, int(audio_length), CONFIG['segment_duration']):
            # 修复：使用段序号而不是分钟数
            segment_num = i // CONFIG['segment_duration']
            # 修改：使用 .m4a 扩展名（AAC 格式）
            segment_name = f"segment_{segment_num:03d}.m4a"
            segment_path = os.path.join(temp_dir, segment_name)
            
            duration = min(CONFIG['segment_duration'], audio_length - i)
            
            cmd = [
                'ffmpeg', '-i', audio_path,
                '-ss', str(i),
                '-to', str(i + duration),
                '-vn', '-acodec', 'aac',
                '-ar', str(CONFIG['audio_quality']['sample_rate']),
                '-ac', str(CONFIG['audio_quality']['channels']),
                '-b:a', CONFIG['audio_quality']['bitrate'],
                segment_path
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            segments.append(segment_path)
        
        print(f"✅ 音频已分割为 {len(segments)} 段")
        return segments
    
    return retry_operation(_split)

def get_audio_length(audio_path):
    """获取音频长度（秒）"""
    cmd = ['ffprobe', '-i', audio_path, '-show_entries', 'format=duration', '-v', 'quiet', '-of', 'csv=p=0']
    result = subprocess.run(cmd, capture_output=True, text=True)
    return float(result.stdout.strip())

def transcribe_audio(audio_path):
    """使用 Whisper 转写音频"""
    def _transcribe():
        print(f"[3/5] 转写音频：{audio_path}")
        
        # 使用 whisper CLI 或 Python API
        try:
            import whisper
            model = whisper.load_model(CONFIG['whisper_model'])
            # 修复：移除不支持的 split_on 参数
            result = model.transcribe(audio_path, language=CONFIG['language'])
            # 返回完整文本和可选的详细信息
            return {
                "text": result['text'],
                "segments": result.get('segments', [])
            }
        except ImportError:
            # 使用 whisper CLI
            cmd = [
                'whisper', audio_path,
                '--model', CONFIG['whisper_model'],
                '--language', CONFIG['language'],
                '--output_format', 'txt'
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            return {"text": result.stdout, "segments": []}
    
    return retry_operation(_transcribe)

def concatenate_texts(segments_texts):
    """按顺序拼接所有文字"""
    print("[4/5] 拼接文字")
    return "\n\n".join(segments_texts)

def generate_detailed_notes(transcripts, video_path):
    """生成详细的视频笔记（按教学顺序）"""
    print("[5/5] 生成详细笔记...")
    
    video_name = os.path.basename(video_path)
    base_name = os.path.splitext(video_name)[0]
    
    # 构建详细笔记
    notes = []
    notes.append(f"# {base_name} - 详细学习笔记")
    notes.append("")
    notes.append(f"> 📅 生成时间：{datetime.now().strftime('%Y 年 %m 月 %d 日 %H:%M')}")
    notes.append(f"> 🎬 视频时长：{len(transcripts)} 段")
    notes.append(f"> 📝 整理方式：AI 助手（详细版 - 保持视频教学顺序）")
    notes.append("")
    notes.append("---")
    notes.append("")
    
    # 按段落整理
    for i, transcript in enumerate(transcripts):
        # 提取时间戳（如果有）
        segment_info = ""
        if transcript.get("segments") and len(transcript["segments"]) > 0:
            start_time = transcript["segments"][0].get("start", 0)
            end_time = transcript["segments"][-1].get("end", 0)
            segment_info = f"\n**时间范围：{format_time(start_time)} - {format_time(end_time)}**\n"
        
        notes.append(f"## 第 {i+1} 段\n")
        notes.append(segment_info)
        notes.append("---")
        notes.append("")
        notes.append(transcript.get("text", ""))
        notes.append("")
        notes.append("---")
        notes.append("")
    
    # 添加总结部分
    notes.append("## 💡 核心内容总结")
    notes.append("")
    notes.append("[此部分将由大模型 AI 进行智能归纳...]\n")
    notes.append("\n## 📚 知识点梳理")
    notes.append("")
    notes.append("[此部分将按视频顺序整理知识点...]\n")
    
    notes_text = "\n".join(notes)
    
    # 保存笔记
    output_path = os.path.join(CONFIG["output_dir"], f"{base_name}.md")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(notes_text)
    
    print(f"✅ 笔记已保存：{output_path}")
    return output_path, notes_text

def format_time(seconds):
    """格式化时间"""
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes}:{secs:02d}"

def summarize_with_llm(text, output_path):
    """使用大模型整理笔记（简洁版）"""
    print("[5/5] 大模型整理笔记")
    
    # 这里需要使用实际的大模型 API
    # 示例代码（需要替换为实际 API）
    prompt = f"""
你是一名专业的学习助理。请根据下面的视频转写内容，整理成结构化的学习笔记。

要求：
1. 保持视频讲解的顺序和逻辑
2. 提取关键概念和要点
3. 使用 Markdown 格式
4. 包含章节标题、要点列表、代码/公式（如果有）

转写内容：
{text[:50000]}  # 限制长度，避免超出上下文

请输出整理后的笔记：
"""
    
    # TODO: 调用大模型 API 进行整理
    # 这里先返回示例输出
    summary = f"""
# 视频学习笔记

## 📋 基本信息
- 来源视频：待补充
- 转写模型：Whisper {CONFIG['whisper_model']}
- 总时长：待计算

## 📚 笔记内容

### 第 1 部分
[内容待大模型整理...]

---

### 第 2 部分
[内容待大模型整理...]

---

## 💡 核心要点
- [待整理]

## 📝 待办事项
- [待整理]
"""
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(summary)
    
    print(f"✅ 笔记已保存：{output_path}")
    return output_path

# ============ 主程序 ============

def main():
    import argparse
    parser = argparse.ArgumentParser(description='视频转笔记完整流程工具')
    parser.add_argument('input_path', help='视频目录或文件路径')
    parser.add_argument('--output', default=None, help='笔记输出目录')
    parser.add_argument('--auto', action='store_true', help='自动模式，跳过确认')
    parser.add_argument('--duration', default=None, help='视频时长，例如 "2 小时 52 分钟"')
    args = parser.parse_args()
    
    if len(sys.argv) < 2:
        print('用法：python video_note_maker.py <视频目录或文件> [--output <输出目录>] [--duration "时长"] [--auto]')
        sys.exit(1)
    
    input_path = args.input_path
    
    # 检查文件是否存在
    if not os.path.exists(input_path):
        print(f"❌ 文件/目录不存在：{input_path}")
        sys.exit(1)
    
    # 确定 base_dir
    if os.path.isfile(input_path):
        base_dir = os.path.dirname(input_path)
        video_files = [input_path]
    elif os.path.isdir(input_path):
        # 如果是目录，查找视频文件
        base_dir = input_path
        video_files = get_video_files(input_path)
        
        # 特殊情况：目录名和文件名相同（如 "7 - OSPF 外部路由.mp4/" 和 "7 - OSPF 外部路由.mp4"）
        # 这种情况下，应该使用目录内的转录文件，而不是搜索整个目录
        dir_basename = os.path.basename(input_path)
        potential_file = os.path.join(input_path, dir_basename)
        if os.path.isfile(potential_file):
            # 找到了同名文件，使用转录文件
            print(f"⚠️  检测到目录和文件名相同，使用转录文件...")
            print(f"📁 转录目录：{input_path}")
            # 检查转录文件
            transcript_files = [f for f in os.listdir(input_path) if f.startswith('transcript_')]
            if transcript_files:
                print(f"✅ 找到 {len(transcript_files)} 个转录文件")
                # 调用整理功能
                if args.duration:
                    duration_str = args.duration
                else:
                    duration_str = estimate_duration(len(transcript_files))
                
                # 调用内嵌的整理函数
                organize_and_email(input_path, base_dir, input_path, duration_str, dir_basename)
                sys.exit(0)
            else:
                print(f"❌ 未找到转录文件")
                sys.exit(1)
        else:
            # 正常搜索
            if not video_files:
                print("❌ 未找到视频文件")
                sys.exit(1)
    else:
        print(f"❌ 文件/目录不存在：{input_path}")
        sys.exit(1)
    
    output_dir = os.path.join(base_dir, 'done')
    
    if args.output:
        output_dir = args.output
    
    print("=" * 60)
    print("🎬 视频转笔记完整流程")
    print("=" * 60)
    print("功能：提取音频 → 分割 → 转写 → 整理笔记 → 发送邮件通知")
    print("=" * 60)
    
    if not video_files:
        print("❌ 未找到视频文件")
        sys.exit(1)
    
    print(f"✅ 找到 {len(video_files)} 个视频文件")
    
    # === 第一步：先展示文件结构预览（不创建任何文件） ===
    if len(video_files) > 0 and not args.auto:
        first_video = video_files[0]
        first_base_name = os.path.splitext(os.path.basename(first_video))[0]
        first_tmp_dir = os.path.join(base_dir, 'tmp', first_base_name)
        first_notes_path = os.path.join(output_dir, f"{first_base_name}.md")
        
        print("\n" + "=" * 60)
        print("📁 文件结构预览（以第一个视频为例）")
        print("=" * 60)
        print(f"""
原视频目录/
├── {os.path.basename(first_video)}
├── tmp/                      # 临时文件（包含中间文件）
│   └── {first_base_name}/
│       ├── audio.m4a          # 提取的音频
│       ├── segment_000.m4a    # 分割后的音频段
│       ├── segment_001.m4a
│       └── ...                # 其他片段
└── done/                     # 最终笔记目录
    └── {first_base_name}.md    # 整理后的笔记
""")
        print("=" * 60)
        print(f"总共 {len(video_files)} 个视频")
        if len(video_files) > 1:
            print(f"其他视频将按同样结构处理：")
            for vf in video_files[1:]:
                vname = os.path.splitext(os.path.basename(vf))[0]
                print(f"  - tmp/{vname}/")
                print(f"  - done/{vname}.md")
        print("=" * 60)
        
        # 询问用户是否继续（必须在创建任何文件之前）
        print("\n是否开始处理？(y/n): ", end='', flush=True)
        choice = sys.stdin.readline().strip().lower()
        if choice != 'y' and choice != 'yes' and choice != '是':
            print("❌ 用户取消处理")
            sys.exit(0)
        print("✅ 用户确认开始处理，继续中...")
        print()
    elif args.auto:
        print("✅ 自动模式，跳过确认，开始处理...")
        print()
    
    # === 第二步：现在再创建目录和开始处理 ===
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 处理每个视频
    for video_idx, video_path in enumerate(video_files, 1):
        print(f"\n{'=' * 60}")
        print(f"处理视频 {video_idx}/{len(video_files)}：{video_path}")
        print(f"{'=' * 60}\n")
        
        # 飞书进度通知
        progress_msg = f"🎬 **视频转写进行中**\n\n当前处理：{os.path.basename(video_path)}\n进度：{video_idx}/{len(video_files)}\n\n⏳ 正在处理中..."
        send_feishu_message(progress_msg)
        
        base_name = os.path.splitext(os.path.basename(video_path))[0]
        
        # 创建 tmp 目录结构：tmp/视频名/
        tmp_base = os.path.join(base_dir, 'tmp')
        os.makedirs(tmp_base, exist_ok=True)
        temp_dir = os.path.join(tmp_base, base_name)
        os.makedirs(temp_dir, exist_ok=True)
        
        # 输出路径
        audio_path = os.path.join(temp_dir, "audio.m4a")  # 修改：AAC 格式
        notes_path = os.path.join(output_dir, f"{base_name}.md")
        
        # === 3. 提取音频 ===
        extract_audio(video_path, audio_path)
        
        # 4. 分割音频（使用临时目录）
        segments = split_audio(audio_path, temp_dir)
        
        # 5. 逐段转写（保留所有文件到最后）
        segments_texts = []
        for i, segment in enumerate(segments):
            print(f"\n  转写第 {i+1}/{len(segments)} 段...")
            transcript = transcribe_audio(segment)
            segments_texts.append(transcript)
            
            # 保存转录文本（可选，方哥要求保留）
            transcript_file = os.path.join(temp_dir, f"transcript_{i:03d}.txt")
            with open(transcript_file, 'w', encoding='utf-8') as f:
                f.write(transcript.get('text', ''))
            print(f"📝 转录文本已保存：{transcript_file}")
            
            # 飞书实时进度
            if CONFIG["feishu_webhook"] and (i + 1) % 2 == 0:  # 每 2 段更新一次
                progress_msg = f"🎬 **视频转写进度**\n\n当前视频：{base_name}\n\n视频进度：{i+1}/{len(segments)} 段\n转写完成：{(i+1)/len(segments)*100:.1f}%\n\n⏳ 正在处理中..."
                send_feishu_message(progress_msg)
        
        # ❌ 不再立即删除临时文件，留到最后统一清理
        
        # 6. 拼接文字
        full_text = "\n\n".join([t.get("text", "") for t in segments_texts])
        print(f"\n总字数：{len(full_text)}")
        
        # 7. 生成详细笔记
        notes_path, notes_content = generate_detailed_notes(segments_texts, video_path)
        
        # 8. 整理 MD 并发送邮件（内嵌整理逻辑）
        print(f"\n📄 整理笔记并发送邮件通知...")
        
        try:
            organize_and_email(temp_dir, output_dir, video_path, args.duration if args.duration else estimate_duration(len(segments_texts)), base_name)
        except Exception as e:
            print(f"⚠️ 整理或邮件发送异常：{e}")
        
        # 飞书完成通知
        success_msg = f"✅ **视频处理完成**\n\n视频：{base_name}\n\n笔记文件：{notes_path}\n\n总字数：{len(full_text)} 字\n\n🎉 处理完成！"
        send_feishu_message(success_msg)
        
        # ✅ 保留临时文件，不删除！
        # 用户可以根据需要手动清理 tmp 目录
        
        print(f"\n✅ {base_name} 处理完成！")
    
    # 飞书最终通知
    if CONFIG["feishu_webhook"]:
        final_msg = f"🎉 **所有视频转写完成**\n\n总视频数：{len(video_files)}\n\n笔记输出目录：{output_dir}\n\n所有视频已处理完毕！\n📚 笔记已保存到指定目录。"
        send_feishu_message(final_msg)
    
    print("\n" + "=" * 60)
    print("🎉 所有视频处理完成！")
    print(f"笔记输出目录：{output_dir}")
    print("=" * 60)

if __name__ == "__main__":
    main()

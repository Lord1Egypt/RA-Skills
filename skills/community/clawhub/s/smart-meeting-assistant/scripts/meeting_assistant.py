#!/usr/bin/env python3
"""
智能会议纪要助手 - Meeting Minutes Assistant
自动完成：会议录音转写 → 会议纪要生成 → 待办事项提取

依赖安装：
    pip install requests

环境变量（可选）：
    ASTRONCLAW_API_KEY: AstronClaw API 密钥
    ASTRONCLAW_API_BASE: API 基础地址（默认: https://api.astronclaw.com）

使用示例：
    python meeting_assistant.py transcribe meeting.mp3
    python meeting_assistant.py summarize transcript.txt
    python meeting_assistant.py extract-todos transcript.txt
    python meeting_assistant.py full-pipeline meeting.mp3 --output ./output/
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    import requests
except ImportError:
    print("错误: 请先安装 requests 库")
    print("运行: pip install requests")
    sys.exit(1)


# 配置
DEFAULT_API_BASE = os.environ.get("ASTRONCLAW_API_BASE", "https://api.astronclaw.com")
API_KEY = os.environ.get("ASTRONCLAW_API_KEY", "")


def get_headers() -> dict:
    """获取 API 请求头"""
    if not API_KEY:
        print("警告: 未设置 ASTRONCLAW_API_KEY 环境变量")
        print("请设置: export ASTRONCLAW_API_KEY=your_api_key")
    return {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }


def transcribe_audio(audio_path: str, language: str = "zh") -> dict:
    """
    转写音频文件
    
    Args:
        audio_path: 音频文件路径
        language: 语言代码 (zh, en, ja 等)
    
    Returns:
        包含转写结果的字典
    """
    audio_path = Path(audio_path)
    if not audio_path.exists():
        raise FileNotFoundError(f"音频文件不存在: {audio_path}")
    
    print(f"正在转写音频: {audio_path.name}")
    
    # 读取音频文件
    with open(audio_path, "rb") as f:
        audio_data = f.read()
    
    # 调用语音转写 API
    # 注意：实际 API 端点可能需要根据 AstronClaw 文档调整
    url = f"{DEFAULT_API_BASE}/v1/audio/transcriptions"
    
    files = {"file": (audio_path.name, audio_data)}
    data = {"model": "whisper-1", "language": language}
    headers = {"Authorization": f"Bearer {API_KEY}"} if API_KEY else {}
    
    response = requests.post(url, files=files, data=data, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"转写失败: {response.status_code} - {response.text}")
    
    result = response.json()
    return {
        "text": result.get("text", ""),
        "duration": result.get("duration", 0),
        "language": result.get("language", language),
    }


def summarize_meeting(transcript: str, meeting_title: Optional[str] = None) -> dict:
    """
    生成会议纪要
    
    Args:
        transcript: 会议转写文本
        meeting_title: 会议标题（可选）
    
    Returns:
        包含会议纪要的字典
    """
    print("正在生成会议纪要...")
    
    system_prompt = """你是一位专业的会议秘书。请根据会议转写内容，生成结构化的会议纪要。

纪要格式要求：
1. 会议主题
2. 参会人员（如可识别）
3. 会议时间（如可识别）
4. 主要讨论内容（分点列出）
5. 重要决议
6. 后续行动项（如有）

请使用专业、简洁的语言，突出重点信息和行动项。"""

    user_message = f"请为以下会议转写内容生成会议纪要：\n\n{transcript}"
    if meeting_title:
        user_message = f"会议标题：{meeting_title}\n\n{user_message}"
    
    url = f"{DEFAULT_API_BASE}/v1/chat/completions"
    payload = {
        "model": "gpt-4o",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        "temperature": 0.3,
    }
    
    response = requests.post(url, json=payload, headers=get_headers())
    
    if response.status_code != 200:
        raise Exception(f"生成纪要失败: {response.status_code} - {response.text}")
    
    result = response.json()
    return {
        "summary": result["choices"][0]["message"]["content"],
        "model": result.get("model", "gpt-4o"),
        "created_at": datetime.now().isoformat(),
    }


def extract_todos(transcript: str) -> dict:
    """
    从会议转写中提取待办事项
    
    Args:
        transcript: 会议转写文本
    
    Returns:
        包含待办事项列表的字典
    """
    print("正在提取待办事项...")
    
    system_prompt = """你是一位专业的会议助理。请从会议转写内容中提取所有待办事项和行动项。

输出格式要求（JSON）：
{
  "todos": [
    {
      "task": "任务描述",
      "assignee": "负责人（如可识别，否则为 null）",
      "deadline": "截止日期（如可识别，否则为 null）",
      "priority": "high/medium/low",
      "context": "相关上下文引用"
    }
  ]
}

注意事项：
1. 只提取明确的行动项和待办任务
2. 任务描述要具体、可执行
3. 如果有明确的负责人或截止日期，请提取
4. 根据上下文判断优先级
5. 如果没有待办事项，返回空列表"""

    url = f"{DEFAULT_API_BASE}/v1/chat/completions"
    payload = {
        "model": "gpt-4o",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"请从以下会议内容中提取待办事项：\n\n{transcript}"},
        ],
        "temperature": 0.2,
        "response_format": {"type": "json_object"},
    }
    
    response = requests.post(url, json=payload, headers=get_headers())
    
    if response.status_code != 200:
        raise Exception(f"提取待办失败: {response.status_code} - {response.text}")
    
    result = response.json()
    content = result["choices"][0]["message"]["content"]
    
    try:
        todos_data = json.loads(content)
    except json.JSONDecodeError:
        todos_data = {"todos": []}
    
    return {
        "todos": todos_data.get("todos", []),
        "extracted_at": datetime.now().isoformat(),
    }


def full_pipeline(
    audio_path: str,
    output_dir: str = "./output",
    meeting_title: Optional[str] = None,
    language: str = "zh",
) -> dict:
    """
    完整流程：转写 → 纪要 → 待办
    
    Args:
        audio_path: 音频文件路径
        output_dir: 输出目录
        meeting_title: 会议标题
        language: 音频语言
    
    Returns:
        包含所有结果的字典
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    base_name = Path(audio_path).stem
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    print(f"\n{'='*50}")
    print("智能会议纪要助手 - 开始处理")
    print(f"{'='*50}\n")
    
    # Step 1: 转写
    transcript_result = transcribe_audio(audio_path, language)
    transcript_text = transcript_result["text"]
    
    transcript_file = output_path / f"{base_name}_transcript_{timestamp}.txt"
    with open(transcript_file, "w", encoding="utf-8") as f:
        f.write(transcript_text)
    print(f"✓ 转写完成，保存至: {transcript_file}")
    
    # Step 2: 生成纪要
    summary_result = summarize_meeting(transcript_text, meeting_title)
    
    summary_file = output_path / f"{base_name}_summary_{timestamp}.md"
    with open(summary_file, "w", encoding="utf-8") as f:
        f.write(f"# 会议纪要\n\n")
        if meeting_title:
            f.write(f"**会议主题**: {meeting_title}\n\n")
        f.write(f"**生成时间**: {summary_result['created_at']}\n\n")
        f.write("---\n\n")
        f.write(summary_result["summary"])
    print(f"✓ 纪要生成完成，保存至: {summary_file}")
    
    # Step 3: 提取待办
    todos_result = extract_todos(transcript_text)
    
    todos_file = output_path / f"{base_name}_todos_{timestamp}.json"
    with open(todos_file, "w", encoding="utf-8") as f:
        json.dump(todos_result, f, ensure_ascii=False, indent=2)
    print(f"✓ 待办提取完成，保存至: {todos_file}")
    
    print(f"\n{'='*50}")
    print("处理完成！")
    print(f"{'='*50}\n")
    
    return {
        "transcript": transcript_result,
        "summary": summary_result,
        "todos": todos_result,
        "files": {
            "transcript": str(transcript_file),
            "summary": str(summary_file),
            "todos": str(todos_file),
        },
    }


def main():
    parser = argparse.ArgumentParser(
        description="智能会议纪要助手 - 转写、纪要、待办一站式处理",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s transcribe meeting.mp3
  %(prog)s summarize transcript.txt
  %(prog)s extract-todos transcript.txt
  %(prog)s full-pipeline meeting.mp3 --output ./output/ --title "周会"
        """,
    )
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # transcribe 命令
    trans_parser = subparsers.add_parser("transcribe", help="转写音频文件")
    trans_parser.add_argument("audio_file", help="音频文件路径")
    trans_parser.add_argument("--language", "-l", default="zh", help="语言代码 (默认: zh)")
    trans_parser.add_argument("--output", "-o", help="输出文件路径")
    
    # summarize 命令
    sum_parser = subparsers.add_parser("summarize", help="生成会议纪要")
    sum_parser.add_argument("transcript_file", help="转写文本文件路径")
    sum_parser.add_argument("--title", "-t", help="会议标题")
    sum_parser.add_argument("--output", "-o", help="输出文件路径")
    
    # extract-todos 命令
    todo_parser = subparsers.add_parser("extract-todos", help="提取待办事项")
    todo_parser.add_argument("transcript_file", help="转写文本文件路径")
    todo_parser.add_argument("--output", "-o", help="输出文件路径")
    
    # full-pipeline 命令
    full_parser = subparsers.add_parser("full-pipeline", help="完整处理流程")
    full_parser.add_argument("audio_file", help="音频文件路径")
    full_parser.add_argument("--output", "-o", default="./output", help="输出目录")
    full_parser.add_argument("--title", "-t", help="会议标题")
    full_parser.add_argument("--language", "-l", default="zh", help="语言代码")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    try:
        if args.command == "transcribe":
            result = transcribe_audio(args.audio_file, args.language)
            output_text = result["text"]
            
            if args.output:
                with open(args.output, "w", encoding="utf-8") as f:
                    f.write(output_text)
                print(f"转写结果已保存至: {args.output}")
            else:
                print("\n=== 转写结果 ===\n")
                print(output_text)
                
        elif args.command == "summarize":
            with open(args.transcript_file, "r", encoding="utf-8") as f:
                transcript = f.read()
            
            result = summarize_meeting(transcript, args.title)
            
            if args.output:
                with open(args.output, "w", encoding="utf-8") as f:
                    f.write(result["summary"])
                print(f"会议纪要已保存至: {args.output}")
            else:
                print("\n=== 会议纪要 ===\n")
                print(result["summary"])
                
        elif args.command == "extract-todos":
            with open(args.transcript_file, "r", encoding="utf-8") as f:
                transcript = f.read()
            
            result = extract_todos(transcript)
            
            if args.output:
                with open(args.output, "w", encoding="utf-8") as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
                print(f"待办事项已保存至: {args.output}")
            else:
                print("\n=== 待办事项 ===\n")
                for i, todo in enumerate(result["todos"], 1):
                    print(f"{i}. {todo['task']}")
                    if todo.get("assignee"):
                        print(f"   负责人: {todo['assignee']}")
                    if todo.get("deadline"):
                        print(f"   截止日期: {todo['deadline']}")
                    print(f"   优先级: {todo.get('priority', 'medium')}")
                    print()
                    
        elif args.command == "full-pipeline":
            result = full_pipeline(
                args.audio_file,
                args.output,
                args.title,
                args.language,
            )
            print(f"\n生成的文件:")
            for file_type, file_path in result["files"].items():
                print(f"  - {file_type}: {file_path}")
                
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
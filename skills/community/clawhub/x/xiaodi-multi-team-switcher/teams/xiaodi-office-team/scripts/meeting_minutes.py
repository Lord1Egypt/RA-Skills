#!/usr/bin/env python3
"""
会议纪要生成器
从会议记录或语音转文字内容生成结构化会议纪要
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# 配置
SKILL_DIR = Path(__file__).parent.parent
OUTPUT_DIR = SKILL_DIR / "data" / "meetings"


def extract_speakers(content: str) -> List[str]:
    """提取发言人"""
    patterns = [
        r"([^\s:：]+)[说讲道提](:|：)",
        r"([^\s]+)\s*[说]:",
        r"([^\s]+):(.{10,})"  # 对话格式
    ]
    
    speakers = set()
    for pattern in patterns:
        matches = re.findall(pattern, content)
        for match in matches:
            if isinstance(match, tuple):
                speaker = match[0].strip()
            else:
                speaker = match.strip()
            if speaker and len(speaker) < 10:  # 过滤过长的匹配
                speakers.add(speaker)
    
    return list(speakers)


def extract_decisions(content: str) -> List[Dict]:
    """提取决定事项"""
    decisions = []
    
    # 决定关键词
    decision_keywords = [
        r"决定([^，。！？]+)",
        r"确定([^，。！？]+)",
        r"同意([^，。！？]+)",
        r"安排([^，。！？]+)负责",
        r"由([^，。！？]+)负责",
        r"计划([^，。！？]+)",
    ]
    
    for pattern in decision_keywords:
        matches = re.findall(pattern, content)
        for match in matches:
            decision = match.strip()
            if len(decision) > 5:  # 过滤过短的内容
                decisions.append({
                    "content": decision,
                    "responsible": extract_responsible(match),
                    "deadline": extract_deadline(content)
                })
    
    return decisions


def extract_todos(content: str) -> List[Dict]:
    """提取待办事项"""
    todos = []
    
    # TODO 关键词
    todo_patterns = [
        r"需要([^，。！？]+)",
        r"要([^，。！？]+)",
        r"请([^，。！？]+)",
        r"下周([^，。！？]+)",
        r"本周([^，。！？]+)",
    ]
    
    for pattern in todo_patterns:
        matches = re.findall(pattern, content)
        for match in matches:
            todo = match.strip()
            if len(todo) > 3 and "会议" not in todo:
                todos.append({
                    "task": todo,
                    "responsible": extract_responsible(match),
                    "deadline": extract_deadline(content)
                })
    
    return todos[:10]  # 限制数量


def extract_responsible(text: str) -> Optional[str]:
    """提取责任人"""
    # 姓名模式
    name_patterns = [
        r"([张王李赵刘陈杨黄周吴徐孙马朱胡郭何高林][^\s]{0,2})",
        r"(@\S+)",
    ]
    
    for pattern in name_patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1)
    
    return None


def extract_deadline(content: str) -> Optional[str]:
    """提取截止时间"""
    time_patterns = [
        (r"(\d+月\d+日)", None),
        (r"本周([一二三四五六日天])", "本周{0}"),
        (r"下周([一二三四五六日天])", "下周{0}"),
        (r"明天", "明天"),
        (r"后天", "后天"),
    ]
    
    for pattern, fmt in time_patterns:
        match = re.search(pattern, content)
        if match:
            if fmt:
                return fmt.format(match.group(1)) if "{" in fmt else fmt
            return match.group(1)
    
    return None


def correct_speech_errors(content: str) -> str:
    """纠正语音转文字常见错误"""
    corrections = {
        "的的": "的",
        "是是": "是",
        "那个那个": "那个",
        "然后然后": "然后",
        "这个这个": "这个",
        "嗯嗯": "",
        "啊": "",
        "呃": "",
        "就是说": "",
        "怎么说呢": "",
    }
    
    result = content
    for wrong, correct in corrections.items():
        result = result.replace(wrong, correct)
    
    # 清理多余空格
    result = re.sub(r'\s+', ' ', result)
    
    return result.strip()


def generate_meeting_minutes(
    content: str,
    title: str = "会议纪要",
    date: Optional[str] = None,
    participants: Optional[List[str]] = None
) -> str:
    """
    生成会议纪要
    
    Args:
        content: 会议记录内容
        title: 会议主题
        date: 会议日期
        participants: 参会人员列表
    
    Returns:
        格式化的会议纪要
    """
    # 纠正语音错误
    cleaned_content = correct_speech_errors(content)
    
    # 提取信息
    if not participants:
        participants = extract_speakers(cleaned_content)
    decisions = extract_decisions(cleaned_content)
    todos = extract_todos(cleaned_content)
    
    # 日期
    if not date:
        date = datetime.now().strftime("%Y年%m月%d日")
    
    # 生成纪要
    minutes = f"""# 会议纪要

**会议主题**: {title}
**会议时间**: {date}
**参会人员**: {', '.join(participants) if participants else '待补充'}
**记录人**: 小弟

---

## 一、会议内容摘要

{cleaned_content[:500]}{'...' if len(cleaned_content) > 500 else ''}

---

## 二、决定事项

"""
    
    if decisions:
        for i, d in enumerate(decisions[:5], 1):
            minutes += f"| {i} | {d['content']} | {d['responsible'] or '待定'} | {d['deadline'] or '待定'} |\n"
    else:
        minutes += "*暂无明确决定事项*\n"
    
    minutes += """
---

## 三、待办事项

"""
    
    if todos:
        for t in todos[:8]:
            minutes += f"- [ ] {t['task']} - @{t['responsible'] or '待定'} - 截止: {t['deadline'] or '待定'}\n"
    else:
        minutes += "*暂无待办事项*\n"
    
    minutes += f"""
---

## 四、下次会议安排

**时间**: 待定
**议题**: 待定

---

*记录时间: {datetime.now().strftime('%Y-%m-%d %H:%M')} | 记录人: 小弟*
"""
    
    return minutes


def save_minutes(minutes: str, filename: Optional[str] = None) -> str:
    """保存会议纪要"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    if not filename:
        filename = f"会议纪要_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    
    filepath = OUTPUT_DIR / filename
    filepath.write_text(minutes, encoding='utf-8')
    
    return str(filepath)


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法: python meeting_minutes.py <会议记录内容>")
        print("      python meeting_minutes.py --file <记录文件路径>")
        sys.exit(1)
    
    if sys.argv[1] == "--file" and len(sys.argv) > 2:
        # 从文件读取
        content = Path(sys.argv[2]).read_text(encoding='utf-8')
    else:
        # 从命令行参数读取
        content = " ".join(sys.argv[1:])
    
    # 生成纪要
    minutes = generate_meeting_minutes(content)
    
    # 保存
    filepath = save_minutes(minutes)
    
    print(f"✅ 会议纪要已生成")
    print(f"📄 文件路径: {filepath}")
    print("\n" + "="*50 + "\n")
    print(minutes)


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Smart Memory Update - 智能记忆更新
使用 LLM_GLM5 分析对话并自动更新记忆系统
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path

# 添加脚本目录到路径
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from llm_client import GLM5Client

# 路径配置
WORKSPACE = Path.home() / ".openclaw" / "workspace"
MEMORY_DIR = WORKSPACE / "memory"
PERSONA_FILE = MEMORY_DIR / "persona.md"
MEMORY_FILE = WORKSPACE / "MEMORY.md"
DAILY_NOTE = MEMORY_DIR / f"{datetime.now().strftime('%Y-%m-%d')}.md"


def read_file(filepath):
    """读取文件内容"""
    if filepath.exists():
        return filepath.read_text(encoding="utf-8")
    return ""


def write_file(filepath, content):
    """写入文件"""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(content, encoding="utf-8")


def append_to_file(filepath, content):
    """追加到文件"""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(content)


def update_persona_with_llm(conversation: str):
    """使用 LLM 分析对话并更新用户画像"""
    client = GLM5Client()
    
    print("🔍 正在分析对话...")
    result = client.analyze_conversation(conversation, "extract_preferences")
    
    if "error" in result:
        print(f"❌ 分析失败: {result['error']}")
        if "raw_response" in result:
            print(f"原始响应: {result['raw_response']}")
        return False
    
    # 提取结果
    preferences = result.get("preferences", [])
    habits = result.get("habits", [])
    characteristics = result.get("characteristics", [])
    summary = result.get("summary", "")
    
    print(f"\n📊 分析结果:")
    print(f"  偏好: {', '.join(preferences)}")
    print(f"  习惯: {', '.join(habits)}")
    print(f"  特征: {', '.join(characteristics)}")
    print(f"  总结: {summary}")
    
    # 更新 persona.md
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    persona_update = f"""

---

## LLM 分析更新 ({timestamp})

### 偏好
{chr(10).join(f'- {p}' for p in preferences)}

### 习惯
{chr(10).join(f'- {h}' for h in habits)}

### 特征
{chr(10).join(f'- {c}' for c in characteristics)}

### 总结
{summary}
"""
    
    append_to_file(PERSONA_FILE, persona_update)
    print(f"\n✅ 已更新 persona.md")
    
    # 更新 MEMORY.md
    memory_update = f"""

### 更新 {datetime.now().strftime('%Y-%m-%d')} (LLM 分析)
- **偏好**: {', '.join(preferences)}
- **习惯**: {', '.join(habits)}
- **特征**: {', '.join(characteristics)}
- **总结**: {summary}
"""
    
    # 查找用户画像部分
    existing = read_file(MEMORY_FILE)
    if "## 用户画像" in existing:
        append_to_file(MEMORY_FILE, memory_update)
        print(f"✅ 已更新 MEMORY.md")
    else:
        persona_section = f"""

## 用户画像
{memory_update}
"""
        append_to_file(MEMORY_FILE, persona_section)
        print(f"✅ 已创建 MEMORY.md 用户画像部分")
    
    return True


def extract_scene_with_llm(conversation: str):
    """使用 LLM 提取场景"""
    client = GLM5Client()
    
    print("🔍 正在提取场景...")
    result = client.analyze_conversation(conversation, "extract_scene")
    
    if "error" in result:
        print(f"❌ 提取失败: {result['error']}")
        return False
    
    scene_name = result.get("scene_name", "未命名场景")
    scene_type = result.get("scene_type", "其他")
    key_points = result.get("key_points", [])
    outcome = result.get("outcome", "")
    
    print(f"\n📊 场景信息:")
    print(f"  名称: {scene_name}")
    print(f"  类型: {scene_type}")
    print(f"  要点: {', '.join(key_points)}")
    print(f"  结果: {outcome}")
    
    # 更新每日记录
    timestamp = datetime.now().strftime("%H:%M:%S")
    scene_block = f"""

---

## 场景: {scene_name}
**时间**: {timestamp}
**类型**: {scene_type}

### 要点
{chr(10).join(f'- {p}' for p in key_points)}

### 结果
{outcome}
"""
    
    # 如果每日记录不存在，创建头部
    if not DAILY_NOTE.exists():
        today = datetime.now().strftime("%Y-%m-%d")
        header = f"# {today} 每日记录\n\n> 自动记录的场景和事件\n"
        write_file(DAILY_NOTE, header)
    
    append_to_file(DAILY_NOTE, scene_block)
    print(f"\n✅ 已记录场景到 {DAILY_NOTE.name}")
    
    return True


def summarize_with_llm(conversation: str):
    """使用 LLM 总结对话"""
    client = GLM5Client()
    
    print("🔍 正在总结对话...")
    result = client.analyze_conversation(conversation, "summarize")
    
    if "error" in result:
        print(f"❌ 总结失败: {result['error']}")
        return False
    
    summary = result.get("summary", "")
    key_topics = result.get("key_topics", [])
    decisions = result.get("decisions", [])
    action_items = result.get("action_items", [])
    
    print(f"\n📊 总结:")
    print(f"  概要: {summary}")
    print(f"  主题: {', '.join(key_topics)}")
    print(f"  决策: {', '.join(decisions)}")
    print(f"  待办: {', '.join(action_items)}")
    
    return result


def main():
    """主函数"""
    if len(sys.argv) < 3:
        print("用法:")
        print("  python3 smart_memory_update.py persona '<对话内容>'")
        print("  python3 smart_memory_update.py scene '<对话内容>'")
        print("  python3 smart_memory_update.py summarize '<对话内容>'")
        sys.exit(1)
    
    command = sys.argv[1]
    conversation = sys.argv[2]
    
    if command == "persona":
        update_persona_with_llm(conversation)
    elif command == "scene":
        extract_scene_with_llm(conversation)
    elif command == "summarize":
        result = summarize_with_llm(conversation)
        if result:
            print(f"\n📝 完整结果:")
            print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"未知命令: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()

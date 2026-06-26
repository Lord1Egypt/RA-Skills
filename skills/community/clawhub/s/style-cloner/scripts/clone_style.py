#!/usr/bin/env python3
"""
文章风格克隆
用法:
  python3 clone_style.py --refs "参考文章" --content "原始素材"
  python3 clone_style.py --refs /path/to/refs.txt --content /path/to/draft.txt
  python3 clone_style.py --refs "..." --content "..." --intensity 80 --length 1000 --output /tmp/result.md
"""
import argparse
import os
import sys
import json
import urllib.request
from datetime import datetime

API_KEY = os.environ.get("OPENAI_API_KEY") or os.environ.get("DEEPSEEK_API_KEY", "")
API_BASE = os.environ.get("OPENAI_API_BASE", "https://api.deepseek.com")
MODEL = os.environ.get("LLM_MODEL", "deepseek-chat")

def read_input(text_or_path: str) -> str:
    if os.path.exists(text_or_path):
        with open(text_or_path, encoding="utf-8", errors="ignore") as f:
            return f.read().strip()
    return text_or_path.strip()

def call_llm(prompt: str) -> str:
    if not API_KEY:
        return "[错误] 请设置环境变量 OPENAI_API_KEY 或 DEEPSEEK_API_KEY"

    payload = json.dumps({
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "你是一位顶级的文字风格分析师和创意写作专家。"
                    "你能精准捕捉任何作者的写作风格，并将其复制到新的内容上。"
                    "你的改写保留原素材的核心信息和观点，同时完美呈现目标风格。"
                    "请用中文输出。"
                )
            },
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.85,
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{API_BASE}/chat/completions",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}",
        }
    )
    with urllib.request.urlopen(req, timeout=90) as r:
        data = json.loads(r.read())
    return data["choices"][0]["message"]["content"]

def build_prompt(refs: str, content: str, intensity: int, length: int, platform: str) -> str:
    platform_hint = f"\n目标平台：{platform}，请结合该平台的传播特点进行风格调整。" if platform else ""
    length_hint = f"\n目标字数：约{length}字。" if length else ""

    return f"""请完成以下文章风格克隆任务。

## 参考文章（目标风格样本）
{refs[:4000]}

## 原始素材（需要改写的内容）
{content[:2000]}
{platform_hint}{length_hint}

## 任务要求

**第一步：风格分析**
请先简要分析参考文章的核心风格特征，包括：
- 语言风格（正式/口语/幽默/温情等）
- 句式特点（长短句比例、常用句型）
- 开头/结尾套路
- 高频词汇和特色表达
- 情感色调

**第二步：输出3个版本**

请按以下格式输出三个改写版本：

---

### 📝 风格分析摘要
[上述风格分析结果，3-5条核心特征]

---

### 版本一（风格强度 {max(10, intensity-20)}%）
> 保留较多原文结构，轻度套用参考风格，适合不想改动太大的情况

[改写后文章]

---

### 版本二（风格强度 {intensity}%）★ 推荐
> 平衡改写，主要推荐版本

[改写后文章]

---

### 版本三（风格强度 {min(100, intensity+20)}%）
> 深度克隆参考风格，最大程度还原参考文章的感觉

[改写后文章]

---

### 💡 使用建议
[简要说明三个版本的适用场景，以及进一步调整的建议]
"""

def clone_style(refs_input, content_input, intensity=80, length=None, platform=None, output_path=None):
    print("📖 读取输入内容...")
    refs = read_input(refs_input)
    content = read_input(content_input)

    if not refs.strip():
        print("❌ 参考文章为空")
        sys.exit(1)
    if not content.strip():
        print("❌ 原始素材为空")
        sys.exit(1)

    print(f"📚 参考文章长度: {len(refs)} 字符")
    print(f"📝 原始素材长度: {len(content)} 字符")
    print(f"🎚️  风格强度: {intensity}%")
    print("🤖 调用 AI 进行风格克隆...")

    prompt = build_prompt(refs, content, intensity, length, platform)
    result = call_llm(prompt)

    header = f"# 风格克隆结果\n\n> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')} | 风格强度：{intensity}%\n\n---\n\n"
    full_result = header + result

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(full_result)
        print(f"\n✅ 结果已保存：{output_path}")
    else:
        print("\n" + "="*60)
        print(full_result)

    return full_result

def main():
    parser = argparse.ArgumentParser(description="文章风格克隆")
    parser.add_argument("--refs", required=True, help="参考文章文本或文件路径（多篇用 --- 分隔）")
    parser.add_argument("--content", required=True, help="原始素材文本或文件路径")
    parser.add_argument("--intensity", type=int, default=80, help="风格强度 0-100，默认 80")
    parser.add_argument("--length", type=int, help="目标字数")
    parser.add_argument("--platform", help="目标平台（小红书/公众号/知乎等）")
    parser.add_argument("--output", help="输出文件路径（.md）")
    args = parser.parse_args()

    clone_style(args.refs, args.content, args.intensity, args.length, args.platform, args.output)

if __name__ == "__main__":
    main()

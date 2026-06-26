#!/usr/bin/env python3
"""Vibe Coding 可行性评估 CLI"""
import argparse, os, sys, json, urllib.request

API_KEY = os.environ.get("OPENAI_API_KEY") or os.environ.get("DEEPSEEK_API_KEY", "")
API_BASE = os.environ.get("OPENAI_API_BASE", "https://api.deepseek.com")
MODEL = os.environ.get("LLM_MODEL", "deepseek-chat")

def call_llm(prompt):
    if not API_KEY:
        return "[错误] 请设置 OPENAI_API_KEY 或 DEEPSEEK_API_KEY"
    payload = json.dumps({"model": MODEL, "messages": [
        {"role": "system", "content": "你是一位资深 AI 编程工具专家，深度使用过 Cursor、Windsurf、Bolt、v0、Replit AI 等工具。你能准确评估哪些任务适合 vibe coding，哪些需要人工介入。请用中文回答，使用 Markdown 格式。"},
        {"role": "user", "content": prompt}
    ], "temperature": 0.7}).encode()
    req = urllib.request.Request(f"{API_BASE}/chat/completions", data=payload,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())["choices"][0]["message"]["content"]

def build_prompt(idea, skill_level):
    skill_hint = f"\n用户技能水平：{skill_level}" if skill_level else ""
    return f"""请评估以下功能/项目是否适合用 Vibe Coding（AI辅助编程）独立实现。{skill_hint}

项目/功能描述：
{idea}

请按以下结构输出评估报告：

## ⚡ 评估结论

用醒目方式给出结论：
- ✅ **可以独立 vibe coding 实现**
- ⚠️ **可以实现，但需要部分人工介入**
- ❌ **不建议纯 vibe coding，需要较多人工参与**

一句话解释原因。

## 📊 维度评分

| 维度 | 评分 | 说明 |
|------|------|------|
| 技术复杂度 | X/10 | （越低越适合vibe coding）|
| Context 长度 | X/10 | （越低越容易放入单次上下文）|
| 外部依赖 | X/10 | （文档完整度）|
| 调试难度 | X/10 | （AI自我修复能力）|
| **综合适合度** | X/10 | |

## 🛠️ 推荐工具组合

列出最适合的1-3个工具，说明各自负责哪部分。

## 📋 拆解路径

将项目拆解为3-6个可以独立 vibe coding 的子任务，每步说明：
- 做什么
- 用哪个工具
- 预计耗时
- 关键提示词策略

## ⚠️ 风险提示

列出2-4个最容易卡住的地方，以及应对建议。

## 💡 实战建议

给出2-3条具体的 vibe coding 技巧，让这个项目更容易成功。"""

def main():
    parser = argparse.ArgumentParser(description="Vibe Coding 可行性评估")
    parser.add_argument("--idea", required=True, help="功能/项目描述")
    parser.add_argument("--skill", default="", help="你的编程技能水平（入门/有基础/有经验）")
    args = parser.parse_args()

    print("⚡ 正在评估 Vibe Coding 可行性...")
    result = call_llm(build_prompt(args.idea, args.skill))
    print(result)

if __name__ == "__main__":
    main()

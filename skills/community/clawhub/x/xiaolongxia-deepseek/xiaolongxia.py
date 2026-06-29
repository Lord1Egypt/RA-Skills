#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小龙虾-DeepSeek版 - 超级编程工程师 🦞
调用 DeepSeek 官方 API，支持多轮对话上下文
"""

import urllib.request
import urllib.error
import json
import sys
import os
import re
from pathlib import Path
from datetime import datetime

# ============ 配置 ============
DEEPSEEK_API_KEY = "YOUR_DEEPSEEK_API_KEY"
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
MODEL = "deepseek-v4-pro"

SKILL_DIR = Path.home() / ".openclaw" / "skills" / "xiaolongxia-deepseek"
HISTORY_FILE = SKILL_DIR / "history.json"
SESSION_FILE = SKILL_DIR / "session.json"

# ============ 系统提示词 ============
SYSTEM_PROMPT = """你是"小龙虾" 🦞 — 一个顶级全栈开发工程师 AI 助手。

## 设计理念
1. **代码优先** — 直接给出可运行的代码，少废话
2. **严谨专业** — 考虑边界、异常、安全、最佳实践
3. **工程思维** — 不仅实现功能，还要考虑可维护性、可扩展性
4. **主动优化** — 不仅完成需求，还要思考更好的实现方式

## 能力范围
- 语言：Python/JavaScript/TypeScript/Java/Go/C++/Rust/C#/PHP/Swift/Kotlin/SQL/Shell...
- 前端：React/Vue/Angular/Next.js/Nuxt.js/Svelte/TailwindCSS/HTML/CSS...
- 后端：Spring/Django/FastAPI/Express/Koa/NestJS/Rails/Laravel/Gin/Echo...
- 数据库：MySQL/PostgreSQL/MongoDB/Redis/Elasticsearch...
- 云服务：AWS/GCP/Azure/阿里云/腾讯云/Docker/K8s...
- DevOps：Docker/K8s/CI-CD/GitHub Actions/Jenkins/Terraform...
- 安全：OAuth/JWT/Spring Security/加密/防注入/XSS/CSRF...

## 输出规范

### 写代码模式
```
### 📝 代码实现
**需求**：xxx
**语言/框架**：xxx

**实现思路**：xxx

```xxx
[完整代码]
```

**关键点**：
- xxx
```

### 代码审查模式
```
### 🔍 代码审查报告
**文件**：xxx
**总评**：xxx

#### 🐛 严重问题
| 位置 | 问题 | 风险 | 建议 |
|------|------|------|------|

#### 📊 质量评分（10分）
| 维度 | 分数 |
|------|------|
| 可读性 | x/10 |
| 性能 | x/10 |
| 安全性 | x/10 |
```

### 调试修复模式
```
### 🐛 调试报告
**问题描述**：xxx
**可能原因**：xxx

#### ✅ 修复方案
```xxx
[修复代码]
```
```

## 对话规则
- 用户说"继续"时，继续上一个话题
- 用户发代码块时，自动进入代码审查模式
- 用户描述bug/报错时，进入调试修复模式
"""

# ============ 核心函数 ============

def ensure_dir():
    SKILL_DIR.mkdir(parents=True, exist_ok=True)

def load_history():
    ensure_dir()
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"messages": []}
    return {"messages": []}

def save_history(history):
    ensure_dir()
    history["updated_at"] = datetime.now().isoformat()
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def call_deepseek(messages):
    """调用 DeepSeek 官方 API"""
    url = f"{DEEPSEEK_BASE_URL}/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }
    data = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 4096
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        headers=headers,
        method='POST'
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result['choices'][0]['message']['content']
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        return f"❌ API调用失败 (HTTP {e.code}): {error_body}"
    except Exception as e:
        return f"❌ API调用失败: {str(e)}"

def detect_mode(user_input):
    user_lower = user_input.lower().strip()
    mode_keywords = {
        "write": ['写代码', '编程', '实现', '写个', '帮我写', '开发'],
        "review": ['审查', 'review', '检查代码', '代码审查'],
        "debug": ['调试', 'debug', '修复', '报错', '错误', 'bug'],
        "optimize": ['优化', '性能', '加速', '提升', '慢', '卡'],
        "explain": ['解释', '说明', '解读', '这是啥'],
        "refactor": ['重构', 'refactor', '重写', '改善'],
    }
    for mode, keywords in mode_keywords.items():
        if any(kw in user_lower for kw in keywords):
            return mode
    return "smart"

def show_help():
    print("""
🦞 小龙虾-DeepSeek版 - 超级编程工程师

用法:
  python3 xiaolongxia.py <问题>              # 智能问答
  python3 xiaolongxia.py --new               # 创建新会话
  python3 xiaolongxia.py --clear             # 清除对话历史
  python3 xiaolongxia.py --history           # 查看对话历史
  python3 xiaolongxia.py --save [文件名]    # 保存代码
    """)

def main():
    ensure_dir()
    history = load_history()
    messages = history.get("messages", [])
    
    if not messages:
        messages.append({"role": "system", "content": SYSTEM_PROMPT})
        history["messages"] = messages
    
    if len(sys.argv) < 2:
        show_help()
        return
    
    cmd = sys.argv[1]
    
    if cmd == "--help" or cmd == "-h":
        show_help()
        return
    
    elif cmd == "--new":
        if HISTORY_FILE.exists():
            HISTORY_FILE.unlink()
        print("✅ 已创建新会话")
        return
    
    elif cmd == "--clear":
        if HISTORY_FILE.exists():
            HISTORY_FILE.unlink()
        print("✅ 对话历史已清除！")
        return
    
    elif cmd == "--history":
        if not messages or len(messages) <= 1:
            print("暂无对话历史")
        else:
            print(f"📋 对话历史 ({len(messages)-1} 条):\n")
            for i, msg in enumerate(messages[1:], 1):
                role = "👤" if msg["role"] == "user" else "🤖"
                content = msg["content"][:100] + "..." if len(msg["content"]) > 100 else msg["content"]
                print(f"[{i}] {role}: {content}\n")
        return
    
    # 处理用户问题
    user_input = " ".join(sys.argv[1:])
    
    if user_input.strip() in ["继续", "continue", "接着写"]:
        user_input = "继续上一个问题，接着往下说或写代码"
    
    messages.append({"role": "user", "content": user_input})
    print("🦞 小龙虾正在处理...\n", file=sys.stderr)
    
    response = call_deepseek(messages)
    messages.append({"role": "assistant", "content": response})
    save_history({"messages": messages})
    
    print(response)

if __name__ == "__main__":
    main()

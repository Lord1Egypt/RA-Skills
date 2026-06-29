#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小龙虾 - 超级编程工程师 🦞 v2.0
火山引擎 DeepSeek 多轮对话 + 文件操作 + 会话管理

基于业界最佳实践设计（参考 EasyCode/GitHub Copilot/Claude Code）
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
# 请替换为你自己的火山引擎 API Key
API_KEY = "YOUR_API_KEY_HERE"
ENDPOINT = "https://ark.cn-beijing.volces.com/api/coding/v3"
MODEL = "deepseek-v4-pro"

SKILL_DIR = Path.home() / ".openclaw" / "skills" / "xiaolongxia"
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

## 输出规范（按模式）

### 写代码模式
```
### 📝 代码实现
**需求**：xxx
**语言/框架**：xxx

**实现思路**：xxx

```[语言]
[完整代码]
```

**关键点**：
- xxx

**依赖/注意事项**：
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

#### ⚠️ 警告
| 位置 | 问题 | 建议 |
|------|------|------|

#### 📊 质量评分（10分）
| 维度 | 分数 |
|------|------|
| 可读性 | x/10 |
| 性能 | x/10 |
| 安全性 | x/10 |
| 可维护性 | x/10 |
```

### 调试修复模式
```
### 🐛 调试报告
**问题描述**：xxx
**可能原因**：xxx

#### ✅ 修复方案
```[语言]
[修复代码]
```

#### 📝 预防建议
- xxx
```

### 性能优化模式
```
### ⚡ 优化报告
**问题**：xxx
**优化思路**：xxx

#### 优化前后对比
| 指标 | 优化前 | 优化后 |
|------|--------|--------|

#### 优化代码
```[语言]
[优化代码]
```
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

def load_session():
    ensure_dir()
    if SESSION_FILE.exists():
        try:
            with open(SESSION_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"session_id": None}
    return {"session_id": None}

def save_session(session):
    ensure_dir()
    with open(SESSION_FILE, 'w', encoding='utf-8') as f:
        json.dump(session, f, ensure_ascii=False, indent=2)

def new_session():
    session = {
        "session_id": datetime.now().strftime("%Y%m%d%H%M%S"),
        "created_at": datetime.now().isoformat()
    }
    save_session(session)
    if HISTORY_FILE.exists():
        HISTORY_FILE.unlink()
    return session

def call_deepseek(messages):
    url = f"{ENDPOINT}/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
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
        with urllib.request.urlopen(req, timeout=60) as response:
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
        "write": ['写代码', '编程', '实现', '写个', '写一个', '帮我写', '开发'],
        "review": ['审查', 'review', '检查代码', '代码审查'],
        "debug": ['调试', 'debug', '修复', '报错', '错误', 'bug', '出问题'],
        "optimize": ['优化', '性能', '加速', '提升', '慢', '卡'],
        "explain": ['解释', '说明', '解读', '什么意思', '这是啥'],
        "refactor": ['重构', 'refactor', '重写', '改善'],
        "test": ['测试', 'test', 'unittest', '单元测试', '用例'],
        "design": ['设计', '架构', '方案', '技术选型'],
        "sql": ['sql', '查询', '数据库', '表结构', 'db'],
    }
    for mode, keywords in mode_keywords.items():
        if any(kw in user_lower for kw in keywords):
            return mode
    return "smart"

def extract_code_blocks(text):
    pattern = r'```(\w+)?\n(.*?)```'
    matches = re.findall(pattern, text, re.DOTALL)
    return matches

def save_code_to_file(code, filename=None):
    code_blocks = extract_code_blocks(code)
    if not code_blocks:
        return "未找到可保存的代码"
    ensure_dir()
    saved_files = []
    for i, (lang, content) in enumerate(code_blocks):
        if not filename:
            ext_map = {
                'python': 'py', 'js': 'js', 'typescript': 'ts', 'java': 'java',
                'go': 'go', 'rust': 'rs', 'cpp': 'cpp', 'c': 'c', 'csharp': 'cs',
                'sql': 'sql', 'bash': 'sh', 'shell': 'sh', 'html': 'html',
                'css': 'css', 'json': 'json', 'yaml': 'yaml', 'yml': 'yml',
            }
            ext = ext_map.get(lang.lower(), 'txt')
            filename = f"code_{datetime.now().strftime('%H%M%S')}_{i+1}.{ext}"
        filepath = SKILL_DIR / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content.strip())
        saved_files.append(str(filepath))
    return f"✅ 已保存 {len(saved_files)} 个文件:\n" + "\n".join(f"  - {f}" for f in saved_files)

def show_help():
    print("""
🦞 小龙虾 - 超级编程工程师 v2.0

用法:
  python3 xiaolongxia.py <问题>              # 智能问答
  python3 xiaolongxia.py --new               # 创建新会话
  python3 xiaolongxia.py --clear             # 清除对话历史
  python3 xiaolongxia.py --history           # 查看对话历史
  python3 xiaolongxia.py --session            # 查看当前会话
  python3 xiaolongxia.py --save [文件名]     # 保存最后回复的代码
  python3 xiaolongxia.py --export <目录>     # 导出所有代码
  python3 xiaolongxia.py --mode <模式> <问题> # 指定模式

模式:
  write | review | debug | optimize | explain | refactor | test | design | sql

示例:
  python3 xiaolongxia.py "写一个Python爬虫"
  python3 xiaolongxia.py --mode review "审查代码: [代码]"
  python3 xiaolongxia.py --save mycode.py
    """)

def main():
    ensure_dir()
    history = load_history()
    session = load_session()
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
        session = new_session()
        print(f"✅ 已创建新会话: {session['session_id']}")
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
            print(f"📋 对话历史 (共 {len(messages)-1} 条):\n")
            for i, msg in enumerate(messages[1:], 1):
                role = "👤 用户" if msg["role"] == "user" else "🤖 助手"
                content = msg["content"][:120] + "..." if len(msg["content"]) > 120 else msg["content"]
                print(f"[{i}] {role}: {content}\n")
        return
    
    elif cmd == "--session":
        print(f"📌 当前会话:")
        print(f"   会话ID: {session.get('session_id', '无')}")
        print(f"   创建时间: {session.get('created_at', '无')}")
        print(f"   历史记录: {len(messages) - 1} 条")
        if history.get("updated_at"):
            print(f"   最后更新: {history['updated_at']}")
        return
    
    elif cmd == "--save":
        filename = sys.argv[2] if len(sys.argv) >= 3 else None
        history = load_history()
        if history["messages"] and len(history["messages"]) > 1:
            last_response = history["messages"][-1]["content"]
            result = save_code_to_file(last_response, filename)
            print(result)
        else:
            print("没有可保存的代码")
        return
    
    elif cmd == "--export":
        if len(sys.argv) < 3:
            print("请指定导出目录: --export <目录>")
            return
        export_dir = Path(sys.argv[2])
        export_dir.mkdir(parents=True, exist_ok=True)
        history = load_history()
        count = 0
        for i, msg in enumerate(history["messages"]):
            if msg["role"] == "assistant":
                for lang, content in extract_code_blocks(msg["content"]):
                    ext_map = {'python': 'py', 'js': 'js', 'typescript': 'ts', 'go': 'go', 'rust': 'rs', 'java': 'java', 'sql': 'sql', 'bash': 'sh', 'html': 'html'}
                    ext = ext_map.get(lang.lower(), 'txt')
                    filepath = export_dir / f"code_{i+1}_{count+1}.{ext}"
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content.strip())
                    count += 1
        print(f"✅ 已导出 {count} 个代码文件到 {export_dir}")
        return
    
    elif cmd == "--mode":
        if len(sys.argv) < 3:
            print("请指定模式: --mode <write|review|debug|optimize|explain>")
            return
        mode = sys.argv[2]
        mode_prompts = {
            "write": "请以写代码模式回答：",
            "review": "请以代码审查模式回答：",
            "debug": "请以调试修复模式回答：",
            "optimize": "请以性能优化模式回答：",
            "explain": "请以代码解释模式回答：",
            "refactor": "请以代码重构模式回答：",
            "test": "请以生成测试模式回答：",
            "design": "请以架构设计模式回答：",
            "sql": "请以SQL开发模式回答："
        }
        if mode not in mode_prompts:
            print(f"未知模式。可用: {', '.join(mode_prompts.keys())}")
            return
        user_input = mode_prompts[mode] + " ".join(sys.argv[3:]) if len(sys.argv) > 3 else mode_prompts[mode]
        messages.append({"role": "user", "content": user_input})
        print("🦞 小龙虾正在处理...\n", file=sys.stderr)
        response = call_deepseek(messages)
        messages.append({"role": "assistant", "content": response})
        save_history({"messages": messages})
        print(response)
        return
    
    # 默认：处理用户问题
    user_input = " ".join(sys.argv[1:])
    
    if user_input.strip() in ["继续", "continue", "接着写", "继续写"]:
        user_input = "继续上一个问题，接着往下说或写代码"
    
    mode = detect_mode(user_input)
    messages.append({"role": "user", "content": user_input})
    print("🦞 小龙虾正在处理...\n", file=sys.stderr)
    
    response = call_deepseek(messages)
    messages.append({"role": "assistant", "content": response})
    save_history({"messages": messages})
    
    print(response)

if __name__ == "__main__":
    main()

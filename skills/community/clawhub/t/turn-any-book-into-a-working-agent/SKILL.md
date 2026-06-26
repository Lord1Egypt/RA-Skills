# book-to-agent Skill

## Description
将任何书籍转换为可工作的 AI 员工（Working Agent）。上传一本书（PDF、TXT、EPUB 等），自动提取书中的核心知识、方法论和工作流程，生成一个可独立执行该书相关任务的 AI 员工角色。

## Use Cases
- 用户上传《金字塔原理》，生成"结构化思维专家"员工
- 用户上传《非暴力沟通》，生成"沟通教练"员工
- 用户上传《精益创业》，生成"产品顾问"员工
- 用户上传任何专业书籍，生成对应领域的专家员工

## Implementation Steps

### Step 1: 检测上传的书籍文件
```bash
# 查找当前目录下的书籍文件
find . -maxdepth 1 -type f \( -name "*.pdf" -o -name "*.txt" -o -name "*.epub" -o -name "*.mobi" -o -name "*.azw3" \) 2>/dev/null
```

### Step 2: 提取书籍核心内容
根据文件类型调用相应的提取工具：

**PDF 文件:**
```bash
# 使用 pdf 技能提取文本
python -c "
from pypdf import PdfReader
reader = PdfReader('BOOK_FILENAME')
text = ''
for page in reader.pages:
    text += page.extract_text() + '\n'
print(text[:50000])  # 限制长度
" > extracted_text.txt
```

**TXT/EPUB 文件:**
```bash
# 直接读取或使用 calibre 工具转换
cat BOOK_FILENAME > extracted_text.txt
```

### Step 3: 分析书籍并定义员工角色
创建分析脚本 `analyze_book.py`:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Book to Agent Analyzer
分析书籍内容，提取核心知识并定义 AI 员工角色
"""

import json
import sys

def analyze_book(text):
    """分析书籍内容，提取关键信息"""

    # 提取书名（尝试从文件名或内容推断）
    book_title = extract_title(text)

    # 提取核心主题
    themes = extract_themes(text)

    # 提取方法论/框架
    methodologies = extract_methodologies(text)

    # 提取关键概念
    concepts = extract_concepts(text)

    # 提取实践步骤
    practices = extract_practices(text)

    # 定义员工角色
    agent_role = {
        "name": f"{book_title}专家",
        "title": f"基于《{book_title}》的{themes[0] if themes else '专业'}顾问",
        "description": f"我是一位基于《{book_title}》训练的 AI 专家员工。我掌握了书中{len(methodologies)}个核心方法论和{len(concepts)}个关键概念，可以帮助你{practices[0] if practices else '解决相关问题'}。",
        "expertise": themes,
        "methodologies": methodologies,
        "key_concepts": concepts,
        "services": practices,
        "activation_phrase": f"请作为《{book_title}》专家帮助我...",
        "capabilities": generate_capabilities(methodologies, practices)
    }

    return agent_role

def extract_title(text):
    """从文本中提取书名"""
    # 简化实现，实际可以更复杂
    lines = text.strip().split('\n')
    for line in lines[:10]:
        if len(line) < 100 and any(kw in line for kw in ['论', '学', '原理', '方法', '指南', '手册']):
            return line.strip()
    return "专业知识"

def extract_themes(text):
    """提取核心主题（3-5 个）"""
    # 使用关键词频率分析
    themes = []
    # 简化实现
    if "沟通" in text:
        themes.append("沟通技巧")
    if "管理" in text:
        themes.append("团队管理")
    if "产品" in text:
        themes.append("产品设计")
    if not themes:
        themes.append("专业知识")
    return themes[:5]

def extract_methodologies(text):
    """提取方法论和框架"""
    methodologies = []
    # 查找模式如"X 方法"、"X 框架"、"X 模型"
    import re
    patterns = [r'(\w+方法)', r'(\w+框架)', r'(\w+模型)', r'(\w+原则)', r'(\w+定律)']
    for pattern in patterns:
        matches = re.findall(pattern, text[:10000])
        methodologies.extend(matches)
    return list(set(methodologies))[:10]

def extract_concepts(text):
    """提取关键概念"""
    concepts = []
    # 简化实现
    if "第一性原理" in text:
        concepts.append("第一性原理")
    if " MVP" in text or "最小可行" in text:
        concepts.append("MVP 最小可行产品")
    return concepts[:15]

def extract_practices(text):
    """提取实践步骤/服务"""
    practices = []
    # 查找"如何"、"步骤"等
    if "如何" in text:
        practices.append("提供实践指导")
    practices.append("解答相关问题")
    practices.append("提供专业建议")
    return practices[:8]

def generate_capabilities(methodologies, practices):
    """生成能力列表"""
    caps = []
    for m in methodologies[:3]:
        caps.append(f"应用{m}解决问题")
    caps.append("提供专业咨询和建议")
    caps.append("制定行动计划")
    return caps

if __name__ == "__main__":
    with open('extracted_text.txt', 'r', encoding='utf-8') as f:
        text = f.read()

    agent = analyze_book(text)

    with open('agent_definition.json', 'w', encoding='utf-8') as f:
        json.dump(agent, f, ensure_ascii=False, indent=2)

    print(json.dumps(agent, ensure_ascii=False, indent=2))
```

### Step 4: 创建员工 Skill 定义文件
基于分析结果生成新的 skill:

```bash
# 创建员工 skill 目录
AGENT_NAME=$(python -c "import json; print(json.load(open('agent_definition.json'))['name'])")
mkdir -p "SKILLs/book-agents/${AGENT_NAME}"

# 生成 SKILL.md
python generate_skill_md.py agent_definition.json
```

生成 `generate_skill_md.py`:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
根据书籍分析结果生成 AI 员工 Skill
"""

import json
import sys

def generate_skill_md(agent_def, output_path):
    """生成 Skill.md 文件"""

    md_content = f'''# {agent_def["name"]}

## 角色定位
{agent_def["title"]}

## 核心能力
{chr(10).join(f"- {cap}" for cap in agent_def["capabilities"])}

## 专业知识
基于《{agent_def["title"].split("的")[1].split("顾问")[0] if "的" in agent_def["title"] else "专业书籍"}》深度训练，掌握:

### 核心方法论
{chr(10).join(f"- {m}" for m in agent_def["methodologies"][:5])}

### 关键概念
{chr(10).join(f"- {c}" for c in agent_def["key_concepts"][:8])}

## 使用场景
当我需要:
{chr(10).join(f"- {s}" for s in agent_def["services"])}

## 激活方式
对我说："{agent_def["activation_phrase"]}"

## 工作流程

1. **理解需求**: 分析用户的具体问题和背景
2. **调用知识**: 从书中提取相关的方法论和案例
3. **提供方案**: 给出结构化、可执行的建议
4. **跟进优化**: 根据反馈调整方案

## 专业领域
{chr(10).join(f"- {e}" for e in agent_def["expertise"])}

---
*此 AI 员工由 Book-to-Agent 技能自动生成*
'''

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(md_content)

if __name__ == "__main__":
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        agent = json.load(f)

    output = sys.argv[2] if len(sys.argv) > 2 else 'SKILL.md'
    generate_skill_md(agent, output)
    print(f"Generated {output}")
```

### Step 5: 创建一键执行脚本
创建 `book-to-agent.sh` (或 `.bat` for Windows):

```bash
#!/bin/bash
# book-to-agent: Turn Any Book into a Working Agent
# Usage: ./book-to-agent.sh [book_file]

set -e

BOOK_FILE="${1:-}"

# 检测书籍文件
if [ -z "$BOOK_FILE" ]; then
    BOOK_FILE=$(find . -maxdepth 1 -type f \( -name "*.pdf" -o -name "*.txt" -o -name "*.epub" \) | head -1)
    if [ -z "$BOOK_FILE" ]; then
        echo "❌ 未找到书籍文件"
        echo "用法：book-to-agent.sh [书籍文件]"
        exit 1
    fi
    echo "📚 检测到书籍：$BOOK_FILE"
fi

echo "🚀 开始将书籍转换为 AI 员工..."

# Step 1: 提取文本
echo "📖 提取书籍内容..."
python extract_book.py "$BOOK_FILE"

# Step 2: 分析并定义员工角色
echo "🧠 分析书籍内容，定义员工角色..."
python analyze_book.py

# Step 3: 生成 Skill
echo "⚙️  生成 AI 员工 Skill..."
python generate_skill_md.py agent_definition.json

# Step 4: 安装到技能库
echo "📦 安装到技能库..."
AGENT_NAME=$(python -c "import json; print(json.load(open('agent_definition.json'))['name'])")
mkdir -p "SKILLs/book-agents/${AGENT_NAME}"
cp SKILL.md "SKILLs/book-agents/${AGENT_NAME}/SKILL.md"

echo ""
echo "✅ 完成！AI 员工已创建:"
echo "   名称：${AGENT_NAME}"
echo "   路径：SKILLs/book-agents/${AGENT_NAME}/"
echo ""
echo "🎯 激活方式：${AGENT_NAME}，请帮助我..."
```

## Windows Batch 版本 (book-to-agent.bat)

```batch
@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo 🚀 开始将书籍转换为 AI 员工...

REM 检测书籍文件
set BOOK_FILE=%1
if "%BOOK_FILE%"=="" (
    for %%f in (*.pdf *.txt *.epub) do (
        if exist "%%f" (
            set BOOK_FILE=%%f
            goto :found
        )
    )
    echo ❌ 未找到书籍文件
    echo 用法：book-to-agent.bat [书籍文件]
    exit /b 1
)

:found
echo 📚 检测到书籍：%BOOK_FILE%
echo 📖 提取书籍内容...
python extract_book.py "%BOOK_FILE%"

echo �� 分析书籍内容...
python analyze_book.py

echo ⚙️  生成 AI 员工 Skill...
python generate_skill_md.py agent_definition.json

echo 📦 安装到技能库...
for /f "delims=" %%i in ('python -c "import json; print(json.load(open('agent_definition.json'))['name'])"') do set AGENT_NAME=%%i

mkdir "SKILLs\book-agents\%AGENT_NAME%" 2>nul
copy SKILL.md "SKILLs\book-agents\%AGENT_NAME%\SKILL.md"

echo.
echo ✅ 完成！AI 员工已创建:
echo    名称：%AGENT_NAME%
echo    路径：SKILLs\book-agents\%AGENT_NAME%\
echo.
echo 🎯 激活方式：%AGENT_NAME%，请帮助我...
```

## 快速使用示例

```bash
# 方式 1: 指定书籍文件
./book-to-agent.sh "金字塔原理.pdf"

# 方式 2: 自动检测当前目录的第一本书
./book-to-agent.sh

# Windows
book-to-agent.bat "精益创业.pdf"
```

## 输出结构

```
SKILLs/book-agents/
└── [书名] 专家/
    └── SKILL.md    # AI 员工技能定义
```

## 生成的 AI 员工示例

**输入**: 《金字塔原理》.pdf
**输出**: "金字塔原理专家" 员工
- 专长：结构化思维、逻辑表达、写作指导
- 能力：帮助梳理思路、优化表达、构建逻辑框架

**输入**: 《非暴力沟通》.pdf
**输出**: "非暴力沟通教练" 员工
- 专长：沟通技巧、冲突调解、情感理解
- 能力：改善沟通方式、化解冲突、建立连接

## 依赖要求

- Python 3.8+
- pypdf (用于 PDF 提取): `pip install pypdf`
- ebooklib (用于 EPUB): `pip install ebooklib`

## 注意事项

1. 书籍文件大小建议不超过 50MB
2. 扫描版 PDF 需要 OCR 预处理
3. 生成的 AI 员工基于书籍内容，不超出原书知识范围
4. 建议人工审核生成的 Skill.md 后发布

---
*Book-to-Agent: 让每一本书都成为你的 24 小时工作员工*

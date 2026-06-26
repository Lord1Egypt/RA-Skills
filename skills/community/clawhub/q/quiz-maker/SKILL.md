---
name: quiz-maker
description: 出题工具。根据文档内容（docx、pdf、txt 等）生成选择题测试卷，并返回二维码供答题者扫码作答。触发词：出题、生成题目、创建测验、云端出题。
author: AME
---

# quiz-maker - 出题技能

> 首次使用时，询问用户 ARK API 密钥、模型名称和公网访问地址（已在本地配置过可跳过）。

## 必填参数（首次使用询问）

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `ARK_API_KEY` | 火山引擎 ARK API 密钥 | — |
| `ARK_MODEL` | 模型名称 | `doubao-1.5-pro-32k-250115` |

> 询问示例："请提供 ARK API 密钥（模型和公网地址已有默认值，是否需要调整？）"

参数确认后，更新 `~/.openclaw/workspace/skills/quiz-maker/.env`，然后重启服务生效。

## 调用流程

### 1. 提取文档内容
```bash
# docx
python3 -c "
from docx import Document
doc = Document('文件路径.docx')
for p in doc.paragraphs:
    if p.text.strip(): print(p.text)
for t in doc.tables:
    for row in t.rows: print(' | '.join(c.text.strip() for c in row.cells))
"

# pdf
python3 -c "
import PyPDF2
reader = PyPDF2.PdfReader('文件路径.pdf')
for page in reader.pages:
    t = page.extract_text()
    if t and t.strip(): print(t.strip())
"
```

### 2. 调用云端 API 出题
```bash
node ~/.openclaw/workspace/skills/quiz-maker/quiz-create.js "<内容>" "<标题>" "<说明>" --quiet
```
- `--quiet` 静默模式，只输出纯 JSON 到 stdout，方便解析
- 不加 `--quiet` 则 stderr 会有进度提示

### 3. 本地生成二维码（调用 qr-gen.py）
```bash
python3 ~/.openclaw/workspace/skills/quiz-maker/qr-gen.py "<quizUrl>" [输出路径]
```
- 默认输出路径：`~/.openclaw/canvas/quiz_qr_local_yyyy_mm_dd_hh_mm_ss.png`
  - 带时间戳，文件名如 `quiz_qr_local_2026_04_30_10_25_00.png`
- 依赖 `qrcode` + `pillow` 库（未安装时会自动安装）

### 4. 一行命令完成（推荐写法）
```bash
URL=$(node ~/.openclaw/workspace/skills/quiz-maker/quiz-create.js "<内容>" "<标题>" "<说明>" --quiet 2>/dev/null | python3 -c 'import sys,json; print(json.load(sys.stdin)["quizUrl"])')
python3 ~/.openclaw/workspace/skills/quiz-maker/qr-gen.py "$URL"
```

## 注意事项
- 内容最少需要 50 字
- 二维码直接展示给用户即可

## 教训（踩坑记录）
- **用本地 qr-gen.py 生成二维码**：不要从 API 响应的 `qrImage` base64 提取，依赖云端图片不稳定；直接拿 `quizUrl` 本地生成更可靠
- **加 `--quiet` 解析 JSON**：否则 stderr 的进度消息会和 stdout 的 JSON 混在一起，导致 JSON 解析失败

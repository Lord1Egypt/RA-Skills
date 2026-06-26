# 转换示例：WorkBuddy → OpenClaw 对照

## 示例1：murder-mystery-creator

### WorkBuddy 原始 frontmatter

```yaml
---
name: murder-mystery-creator
agent_created: true
version: "1.8.0"
description: |
  剧本杀一键生成工具...
---
```

### OpenClaw 适配后 frontmatter

```yaml
---
name: murder-mystery-creator
description: |
  剧本杀一键生成工具...
metadata:
  openclaw:
    emoji: "🎭"
    author: "以七"
version: 1.8.0
---
```

### 转换要点
1. 删除 `agent_created: true`（OpenClaw 无此字段）
2. 新增 `metadata.openclaw.emoji`（从主题推断：剧本杀→🎭）
3. 新增 `metadata.openclaw.author`（默认"以七"）
4. `version` 值去掉引号（虽不是必须，但更符合 OpenClaw 习惯）
5. 正文中的 `Skill` 工具引用替换为通用描述

---

## 示例2：content-automation（slug 冲突处理）

### 原始 slug
`content-automation` → 已被占用

### 解决方案
发布时使用 `--slug yiqi-content-automation`，添加个人前缀

### 教训
- 通用名称的 slug 容易被占
- 建议发布前先用 `clawhub search <slug>` 检查是否已被占用
- 如被占，加个人前缀（如 `yiqi-`、`username-`）

---

## 示例3：receipt-word-tool（含 scripts 的处理）

### WorkBuddy 目录结构
```
receipt-word-tool/
├── SKILL.md
├── references/
│   ├── maintenance_guide.md
│   └── easyocr_offline_setup.md
└── scripts/
    ├── receipt_word_tool.py
    └── 启动付款排版工具.bat
```

### OpenClaw 适配
- `.py` 和 `.bat` 文件均为文本文件，在白名单中，可以直接复制
- 但含中文文件名 `启动付款排版工具.bat` 可能在某些环境下出问题
- 建议重命名为 `start-tool.bat` 或在 SKILL.md 中说明

### 转换后目录
```
receipt-word-tool/
├── SKILL.md
├── references/
│   ├── maintenance_guide.md
│   └── easyocr_offline_setup.md
└── scripts/
    ├── receipt_word_tool.py
    └── start-tool.bat
```

---

## 通用转换模板

### Step 1: 读取源 SKILL.md frontmatter
### Step 2: 字段映射
- 保留：name, version, description
- 删除：agent_created, description_zh
- 新增：metadata.openclaw.emoji, metadata.openclaw.author
- 条件新增：requires, envVars, os, homepage

### Step 3: 正文适配
- 删除/替换 WorkBuddy 专有工具引用
- 保留通用设计原则和工作流
- 检查正文长度，超 500 行考虑拆分

### Step 4: 文件复制
- 复制所有白名单内的文件
- 跳过二进制文件
- 检查总包大小 ≤ 50MB

### Step 5: 合规校验
- 执行 P0/P1/P2 校验清单
- 自动修复能修复的问题
- 输出校验报告

### Step 6: 发布
```bash
clawhub publish <path> --version X.Y.Z --name "Name" --slug url-safe-slug --changelog "..."
```

---
name: seedream-ppt-maker
description: Seedream图片PPT制作器 - 宝玉布局框架 + Seedream 5.0文生图，自动生成图片PPT。支持交互式分步确认流程，减少反复修改节省API配额。
version: 1.1.0
metadata:
  openclaw:
    homepage: https://github.com/Cindypapa/baoyu-seedream-ppt
    requires:
      skills:
        - baoyu-infographic
      bins:
        - python3
---

# seedream-ppt-maker - Seedream图片PPT制作器

基于宝玉布局框架 + Seedream 5.0，一键生成图片PPT。支持 **交互式分步确认流程**，减少反复修改，节省API配额。

---

## ⚠️ 安装后必须执行

```bash
# 检查依赖和 API Key 配置
python3 check_install.py

# 如果缺少依赖：
clawhub install baoyu-infographic
pip install python-pptx requests

# 如果缺少 API Key：
# 编辑 ~/.openclaw/config.json，添加：
# {"volces": {"apiKey": "你的火山方舟API Key"}}
```

---

## 🎯 触发条件

用户提到以下关键词时触发：
- "生成PPT"
- "图片PPT"
- "Seedream PPT"
- "用 seedream-ppt-maker"

---

## 🔄 收到请求后先确认

**⚠️ 重要：收到用户请求后，必须先询问生成模式！**

```
用户：帮我生成XX的PPT

助手回复：
收到！请选择生成模式：

1️⃣ **交互式分步生成**（推荐）
   - 分析内容 → 推荐3种布局×风格组合 → 你确认
   - 生成提示词 → 你确认 → 开始生成
   - 适合重要内容，减少反复修改，节省API配额

2️⃣ **一键快速生成**
   - 直接生成，无需确认
   - 适合简单内容或已有明确布局/风格需求

请回复 "1" 或 "2"，或直接告诉我布局和风格（如：bento-grid + chalkboard）
```

---

## 📋 交互式流程（推荐）

### 步骤 1：分析内容，推荐方案

收到用户选择交互式后：

```bash
python3 interactive.py content.md --step analyze
```

输出推荐方案，等待用户确认。

### 步骤 2：生成提示词

用户确认方案后：

```bash
python3 interactive.py content.md --step prompts --layout 布局 --style 风格
```

展示提示词预览，等待用户确认。

### 步骤 3：生成图片并整合PPT

用户确认提示词后：

```bash
python3 interactive.py --step generate --config output/项目名/config.json
```

---

## 🚀 一键快速生成

用户选择一键生成或已有明确布局/风格时：

```bash
python3 baoyu_seedream_ppt.py content.md --layout 布局 --style 风格 --aspect landscape
```

---

## 🎨 布局 × 风格推荐

### 国风/传统文化内容

| 布局 | 风格 | 说明 |
|------|------|------|
| linear-progression | aged-academia | 时间线 + 复古 sepia 古朴 |
| bento-grid | morandi-journal | 多主题 + 莫兰迪手绘温和 |
| dense-modules | craft-handmade | 高密度 + 手绘纸艺 |

### 科技/产品介绍

| 布局 | 风格 | 说明 |
|------|------|------|
| bento-grid | chalkboard | 多主题 + 黑板风清爽 |
| dashboard | technical-schematic | 数据展示 + 工程蓝图 |

### 对比/评测

| 布局 | 风格 | 说明 |
|------|------|------|
| binary-comparison | chalkboard | A vs B + 黑板风清晰 |
| comparison-matrix | bold-graphic | 多因素对比 + 漫画粗线 |

---

## ⚙️ 配置

火山方舟 API Key：

```json
// ~/.openclaw/config.json
{
  "volces": {
    "apiKey": "你的API Key"
  }
}
```

---

## 📦 输出

```
output/项目名/
├── config.json          # 项目配置
├── prompts/             # 每页提示词
├── images/              # 生成的 PNG 图片
└── 项目名_布局_风格.pptx # 最终 PPT
```

---

## 🔗 链接

- GitHub: https://github.com/Cindypapa/baoyu-seedream-ppt
- 宝玉布局系统: https://github.com/JimLiu/baoyu-skills
- 火山方舟: https://www.volcengine.com
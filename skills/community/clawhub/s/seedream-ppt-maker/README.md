# baoyu-seedream-ppt

基于 **宝玉baoyu-infographic** 的21种布局 × 21种风格设计框架，和 **豆包Seedream 5.0** 的高质量文生图能力，一键生成图片PPT。

## ✨ 特点

- ✅ **21种布局**：时间线、对比图、思维导图、漏斗图等
- ✅ **21种风格**：手绘、黏土、黑板报、赛博朋克、像素风等
- ✅ **高质量生图**：Seedream 5.0，2560x1440分辨率
- ✅ **自动整合PPT**：每页一张图片，直接使用

## 📦 安装

```bash
# 复制到 OpenClaw skills 目录
cp -r baoyu-seedream-ppt ~/.openclaw/workspace/skills/

# 安装依赖
pip install python-pptx requests

# 安装 baoyu-infographic（布局系统）
clawhub install baoyu-infographic
```

## ⚙️ 配置

配置火山方舟 API Key：

```json
// ~/.openclaw/config.json
{
  "volces": {
    "apiKey": "你的API Key"
  }
}
```

## 🚀 使用

### 交互式生成（推荐）

```bash
# 第一步：分析内容
python3 interactive.py content.md --step analyze

# 第二步：生成提示词
python3 interactive.py content.md --step prompts --layout bento-grid --style chalkboard

# 第三步：生成图片并整合PPT
python3 interactive.py --step generate --config output/project/config.json
```

### 直接生成

```bash
python3 baoyu_seedream_ppt.py content.md --layout bento-grid --style chalkboard --aspect landscape
```

## 📋 推荐组合

| 内容类型 | 推荐组合 |
|----------|----------|
| 对比测评 | `binary-comparison` + `chalkboard` |
| 产品介绍 | `bento-grid` + `chalkboard` |
| 时间线 | `linear-progression` + `craft-handmade` |
| 教程步骤 | `linear-progression` + `hand-drawn-edu` |

## 🔗 链接

- 宝玉布局系统: https://github.com/JimLiu/baoyu-skills
- 火山方舟: https://www.volcengine.com

## 📝 授权

MIT License - 开源共享

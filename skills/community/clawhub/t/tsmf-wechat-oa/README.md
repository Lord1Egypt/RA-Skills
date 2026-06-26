# 微信公众号自动写作系统

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

> 支持 20+ 精美主题，自动生成封面，一键推送草稿箱的公众号写作利器。

## 功能特点

- **20+ 精美主题** - 经典主题 + 马卡龙色系，覆盖各类文章风格
- **智能主题推荐** - 根据内容关键词自动推荐最佳主题
- **三种写作模式** - 全自动 / 半自动 / 交互式
- **封面自动生成** - 根据文章内容生成精美封面
- **内容验证** - 使用 Tavily 搜索验证事实准确性
- **一键推送** - 直接推送到微信公众号草稿箱

---

## 快速开始

### 前置要求

- Python 3.8 或更高版本
- 微信公众号（需有 API 访问权限）

### 安装步骤

#### 1. 克隆项目

```bash
git clone https://github.com/YOUR_USERNAME/wechat-allauto-gzh.git
cd wechat-allauto-gzh
```

#### 2. 安装依赖

```bash
pip install -r requirements.txt
```

#### 3. 配置环境变量

```bash
# 复制配置模板
cp .env.example .env

# 编辑 .env 文件，填写微信公众号配置
```

#### 4. 获取微信公众号配置

1. 登录 [微信公众平台](https://mp.weixin.qq.com/)
2. 进入「设置与开发」→「基本配置」
3. 复制 `AppID` 和 `AppSecret`

---

## 使用方法

### 方式一：命令行使用

#### 全自动写作

```bash
# 基础用法
python scripts/write_article.py "AI发展趋势"

# 指定主题
python scripts/write_article.py "AI发展趋势" --theme tech_modern

# 指定文章类型
python scripts/write_article.py "Python教程" --type tutorial
```

#### 半自动写作

```bash
# 提供参考材料
python scripts/write_article.py "咖啡文化" --reference reference.txt

# 交互式写作
python scripts/write_article.py "旅行攻略" --interactive
```

#### 推送草稿

```bash
# 推送到微信
python scripts/push_draft.py --file output/2026-03-11/article.html --title "文章标题"

# 查看所有主题
python scripts/push_draft.py --list-themes
```

### 方式二：使用 OpenClaw

将项目 GitHub 链接发送给 OpenClaw，它会自动：

1. 理解您的写作需求
2. 询问主题、风格偏好
3. 生成文章并排版
4. 推送到微信公众号草稿箱

---

## 主题一览

### 经典主题（10个）

| 主题 ID | 名称 | 适用场景 |
|---------|------|----------|
| `minimal_business` | 极简商务 | 职场、管理、商业分析 |
| `tech_modern` | 科技现代 | 技术、编程、AI |
| `warm_artistic` | 温暖文艺 | 读书、情感、随笔 |
| `fresh_lively` | 活泼清新 | 美食、旅行、生活方式 |
| `magazine_premium` | 杂志高级 | 时尚、艺术、深度阅读 |
| `academic_professional` | 学术专业 | 论文、研究、深度分析 |
| `data_analytics` | 数据洞察 | 数据报告、趋势分析 |
| `cozy_lifestyle` | 舒适生活 | 家居、慢生活、治愈系 |
| `creative_bold` | 创意大胆 | 设计、创意、灵感 |
| `energetic_youth` | 青春活力 | 校园、励志、正能量 |
| `nature_fresh` | 自然清新 | 环保、户外、植物 |
| `retro_classic` | 复古经典 | 历史、传统文化、回忆录 |
| `geek_tech` | 极客科技 | 游戏、二次元、夜间阅读 |

### 马卡龙主题（12个）

| 主题 ID | 名称 | 风格特点 |
|---------|------|----------|
| `macaron_pink` | 马卡龙粉 | 甜美温柔 |
| `macaron_blue` | 马卡龙蓝 | 清新宁静 |
| `macaron_mint` | 马卡龙薄荷 | 清爽自然 |
| `macaron_lavender` | 马卡龙薰衣草 | 浪漫优雅 |
| `macaron_peach` | 马卡龙蜜桃 | 温暖甜美 |
| `macaron_lemon` | 马卡龙柠檬 | 明亮活力 |
| `macaron_coral` | 马卡龙珊瑚 | 热情活力 |
| `macaron_sage` | 马卡龙鼠尾草 | 自然清新 |
| `macaron_lilac` | 马卡龙丁香 | 优雅浪漫 |
| `macaron_cream` | 马卡龙奶油 | 温馨治愈 |
| `macaron_sky` | 马卡龙天空 | 清新明亮 |
| `macaron_rose` | 马卡龙玫瑰 | 浪漫精致 |

---

## 项目结构

```
wechat-allauto-gzh/
├── SKILL.md                    # OpenClaw 指引文件
├── README.md                   # 本文件
├── requirements.txt            # Python 依赖
├── .env.example               # 配置模板
│
├── scripts/                   # 核心脚本
│   ├── write_article.py       # 主写作流程
│   ├── outline_generator.py   # 大纲生成
│   ├── html_writer.py         # HTML 排版
│   ├── markdown_to_wechat_html.py  # 主题转换
│   ├── push_draft.py          # 微信推送
│   ├── generate_covers.py     # 封面生成
│   └── content_validator.py   # 内容验证
│
├── themes/                    # 主题配置
│   ├── classic/              # 经典主题
│   └── macaron/              # 马卡龙主题
│
├── output/                    # 输出目录
│   └── YYYY-MM-DD/
│       ├── article.html       # 排版后的文章
│       ├── article.json       # 文章结构
│       └── cover.html         # 封面
│
└── references/                # 参考文档
```

---

## 配置说明

### 必需配置

| 变量 | 说明 | 获取方式 |
|------|------|----------|
| `WECHAT_APP_ID` | 公众号 AppID | 微信公众平台 → 基本配置 |
| `WECHAT_APP_SECRET` | 公众号 AppSecret | 微信公众平台 → 基本配置 |

### 可选配置

| 变量 | 说明 | 用途 |
|------|------|------|
| `TAVILY_API_KEY` | Tavily API Key | 内容搜索验证 |
| `WECHAT_AUTO_MODE` | 自动模式标志 | 定时任务检测 |

---

## 自定义主题

### 创建自定义主题

1. 复制现有主题文件：
```bash
cp themes/classic/minimal_business.yaml themes/custom/my_theme.yaml
```

2. 编辑主题配置：
```yaml
name: 我的主题
description: 主题描述
keywords:
  - 关键词1
  - 关键词2
colors:
  primary: "#主色调"
  accent: "#强调色"
  background: "#背景色"
  text: "#文字颜色"
styles:
  body:
    font_size: "16px"
    line_height: "1.8"
  h1:
    font_size: "20px"
  # ... 其他样式
```

3. 使用自定义主题：
```bash
python scripts/write_article.py "主题" --theme custom/my_theme
```

---

## 文章类型模板

系统内置 5 种文章类型模板：

| 类型 | 结构 |
|------|------|
| 技术教程 | 引言 → 背景 → 核心内容 → 案例 → 总结 |
| 商业分析 | 现象 → 背景 → 深度分析 → 案例 → 趋势 |
| 生活随笔 | 开篇 → 经历 → 感悟 → 建议 → 结语 |
| 行业洞察 | 现状 → 问题 → 解读 → 展望 → 建议 |
| 产品评测 | 概述 → 印象 → 体验 → 优缺点 → 建议 |

---

## 常见问题

### Q: 如何获取微信公众号 AppID 和 AppSecret？

1. 登录 [微信公众平台](https://mp.weixin.qq.com/)
2. 进入「设置与开发」→「基本配置」
3. 复制 AppID 和 AppSecret

### Q: 为什么必须生成封面？

微信公众号新建草稿必须上传封面图片，否则无法保存。

### Q: 支持哪些 Markdown 语法？

- 标题（h1-h6）
- 粗体、斜体
- 有序/无序列表
- 引用块
- 代码块
- 链接、图片
- 分隔线

### Q: 如何安装 Tavily 进行内容验证？

```bash
pip install tavily-python
```

然后在 `.env` 中配置 `TAVILY_API_KEY`。

---

## 使用 OpenClaw

本项目专为 OpenClaw 优化。将 GitHub 链接发送给 OpenClaw，它会：

1. **理解需求** - 询问您想写什么主题
2. **推荐主题** - 根据内容推荐最佳排版风格
3. **生成文章** - 自动写作、排版、生成封面
4. **推送草稿** - 一键推送到微信公众号

---

## 贡献指南

欢迎贡献代码、报告问题或提出建议！

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

---

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

---

## 致谢

- 微信公众平台 API
- Agent Skills Standard
- 所有贡献者
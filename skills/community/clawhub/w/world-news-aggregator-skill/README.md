# 🌍 World News Aggregator Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://github.com/openclaw/openclaw)
[![GitHub stars](https://img.shields.io/github/stars/BODYsuperman/world-news-aggregator-skill.svg?style=social&label=Star)](https://github.com/BODYsuperman/world-news-aggregator-skill)

**全球信息参考 - 多元聚合全球科技、股市、AI 论文、军事技术、政策情报的智能新闻聚合助手。**

---

## ✨ 核心特性

- **🌐 全球多源聚合**：一站式覆盖全球科技、金融、AI、军事、政策等 50+ 高价值信源
- **🤖 专为 OpenClaw 打造**：原生支持 OpenClaw Skill 系统，即插即用
- **🆓 零配置 (Zero-Config)**：无需 API Key，开箱即用
- **🧠 AI 智能摘要**：自动提炼核心信息，生成结构化情报报告
- **📊 多场景预设**：综合日报、科技早报、财经简报、AI 周报、政策速递
- **🔍 智能搜索**：支持关键词、时间范围、来源筛选

---

## 📚 聚合信源图谱

### 🎯 核心新闻源

| 类别 | 信源 | 标识 |
|------|------|------|
| **全球科技** | TechCrunch, The Verge, Wired, Ars Technica | `tech` |
| **开源社区** | Hacker News, GitHub Trending, Product Hunt | `opensource` |
| **国内科技** | 36Kr, 虎嗅，少数派 | `cn-tech` |
| **全球股市** | Yahoo Finance, Bloomberg, Reuters | `stock` |
| **国内股市** | 东方财富，雪球 | `cn-stock` |
| **AI 论文** | arXiv, Papers With Code, Hugging Face | `ai` |
| **军事技术** | Defense News, Janes, The War Zone | `military` |
| **国内政策** | 国务院，发改委，工信部，网信办 | `cn-policy` |

---

## 📥 安装指南

### 方法 1：使用 NPX（推荐）

```bash
# 直接从远程仓库添加
npx skills add https://github.com/BODYsuperman/world-news-aggregator-skill
```

### 方法 2：使用 Git

```bash
# 克隆到你的 OpenClaw skills 目录
git clone https://github.com/BODYsuperman/world-news-aggregator-skill.git ~/.openclaw/skills/world-news
```

### 方法 3：手动下载

```bash
# 下载并解压到 skills 目录
cd ~/.openclaw/skills/
git clone https://github.com/BODYsuperman/world-news-aggregator-skill.git world-news
```

### 安装依赖（可选）

```bash
cd ~/.openclaw/skills/world-news
pip install -r requirements.txt
```

---

## 🚀 如何使用

### 1. 自然语言触发

在 OpenClaw 中直接使用：

```
/global-intel                    # 获取全部情报
/global-intel 科技 AI            # 指定主题
/global-intel --sources tech,ai --limit 20
/global-intel 股市 --hours 48    # 48 小时内股市信息
```

### 2. 场景化报告

```
生成今日科技早报
帮我看看最新的 AI 论文
最近有什么军事技术突破
国内有什么新政策
```

### 3. 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `[topics]` | 全部 | 指定主题（科技/股市/AI/军事/政策） |
| `--sources` | 全部 | 指定信息源（tech,stock,ai,mil,cn） |
| `--limit` | 10 | 每类返回数量 |
| `--hours` | 24 | 时间范围（小时） |
| `--format` | summary | 输出格式（summary/detailed/brief） |

---

## 📋 输出示例

### 综合情报报告

```markdown
## 🌐 全球科技 (过去 24 小时)

### OpenAI 发布 GPT-5 预览版
- **来源**: TechCrunch
- **时间**: 2026-03-10 14:30 UTC
- **摘要**: OpenAI 正式发布 GPT-5 预览版，支持多模态推理...
- **链接**: https://techcrunch.com/...
- **重要性**: ⭐⭐⭐⭐⭐

---

## 📈 全球股市

### 主要指数
| 指数 | 当前 | 涨跌 | 幅度 |
|------|------|------|------|
| 标普 500 | 5,123 | +23 | +0.45% |
| 纳斯达克 | 16,234 | +89 | +0.55% |

---

## 🤖 AI 论文

### Scaling Laws for Multimodal Models
- **机构**: Stanford, Google DeepMind
- **arXiv**: arxiv.org/abs/2603.12345
- **领域**: 多模态，Scaling Law
- **亮点**: 首次提出跨模态统一缩放定律
```

---

## 🔧 技术架构

```
world-news-aggregator-skill/
├── SKILL.md              # OpenClaw Skill 定义
├── README.md             # 本文件
├── requirements.txt      # Python 依赖
├── .gitignore
└── scripts/
    └── fetch-news.py     # 新闻抓取脚本（可选）
```

---

## 📝 更新日志

### v1.1.0 (2026-03-10)
- ✨ 新增 Hacker News、Ars Technica、Google AI Blog 等源
- 🔧 改进错误处理和重试机制 (指数退避)
- 🔄 添加 User-Agent 轮换避免限流
- 📊 新增信息源状态报告
- 📝 优化输出格式和重要性评级
- 🐛 修复 arXiv Atom feed 解析

### v1.0.0 (2026-03-10)
- ✨ 初始版本发布
- 🌐 支持 50+ 全球信息源
- 📊 5 大类别：科技、股市、AI、军事、政策
- 🤖 原生 OpenClaw Skill 集成

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📄 许可证

采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

## 🙏 致谢

- OpenClaw 团队提供的 Skill 框架
- 所有信息源的开放 API

---

## 📬 联系方式

- **GitHub**: [@BODYsuperman](https://github.com/BODYsuperman)
- **Issues**: [提交 Issue](https://github.com/BODYsuperman/world-news-aggregator-skill/issues)

---

*让决策更有依据 - 全球信息，一手掌握*

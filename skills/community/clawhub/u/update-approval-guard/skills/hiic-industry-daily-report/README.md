# HIIC 产业日报订阅系统

深圳20+8产业集群自动化资讯聚合与推送系统

## 核心特性

- ✅ **三引擎搜索**：Tavily + Brave + tech-news-digest
- ✅ **严格时效性**：只收录过去24小时资讯
- ✅ **智能去重**：URL标准化去重
- ✅ **自动翻译**：使用translate-shell翻译标题、摘要、正文
- ✅ **高质量摘要**：基于新闻六要素（5W1H），50-200字
- ✅ **飞书存储**：自动保存到飞书多维表格
- ✅ **定时推送**：支持每天定时推送

## 快速开始

### 1. 生成日报

```bash
# 生成机器人产业日报
node scripts/generate-report.mjs --industry "机器人" --maxResults 20

# 生成半导体产业日报
node scripts/generate-report.mjs --industry "半导体" --maxResults 15
```

### 2. 设置定时推送

```bash
# 每天早上9点推送AI产业日报
openclaw cron add "0 9 * * *" \
  "node /path/to/generate-report.mjs --industry '人工智能' --maxResults 20 --announce"
```

## 支持的产业

支持28个产业集群，包括：

- 🤖 人工智能
- 🦾 机器人
- ⚡ 新能源
- 🚗 智能网联汽车
- 💡 半导体与集成电路
- ⚛️ 量子信息
- 🧬 生物医药
- 🔬 新材料

完整列表见 `config/defaults/industries.json`

## 环境要求

```bash
# 必需的API密钥
export TAVILY_API_KEY="tvly-xxx"
export BRAVE_API_KEY="BSAxxx"

# 飞书配置
export FEISHU_APP_ID="cli_xxx"
export FEISHU_APP_SECRET="xxx"
```

**翻译功能**：使用系统自带的 `translate-shell`，无需额外API Key

## 文件结构

```
hiic-industry-daily-report/
├── SKILL.md                    # 技能说明文档
├── CHANGELOG.md                # 更新日志
├── README.md                   # 本文件
├── scripts/
│   ├── generate-report.mjs     # 主生成脚本
│   ├── feishu-bitable-saver.mjs # 飞书存储
│   ├── hiic-tech-digest-bridge.py # tech-news-digest桥接
│   ├── config-loader.mjs       # 配置加载器
│   └── validate-config.py      # 配置验证
├── config/
│   ├── schema.json             # 配置模式
│   └── defaults/
│       ├── industries.json     # 产业配置（28个）
│       ├── sources.json        # 数据源配置
│       └── topics.json         # 主题配置
└── references/
    ├── config-guide.md         # 配置指南
    └── config-template.json    # 配置模板
```

## 更新日志

详见 [CHANGELOG.md](./CHANGELOG.md)

### v1.1.0 (2026-03-11)
- ✅ 新增自动翻译功能
- ✅ 优化摘要生成（基于新闻六要素）
- ✅ 改进输出格式

## 技术支持

- OpenClaw文档：https://docs.openclaw.ai
- ClawHub技能市场：https://clawhub.com
- 社区支持：https://discord.com/invite/clawd

## 许可证

MIT License

---

**🦞 小咔拉咪为你打造，助力产业研究与投资决策！**

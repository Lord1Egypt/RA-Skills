# 🎯 Social Hub · 社交媒体营销中心

> **AI 驱动的新一代抖音运营工具** · 输入关键词，5分钟完成赛道分析、爆款标题、口播脚本

**输入关键词，AI 自动搞定抖音的爆款内容分析、标题生成、带货脚本。**

[![GitHub stars](https://img.shields.io/github/stars/0xbigbig/social-media-marketing-hub)](https://github.com/0xbigbig/social-media-marketing-hub/stargazers)
[![Node.js](https://img.shields.io/badge/node-%3E%3D18-blue)](https://nodejs.org/)

---

## ⚡ 一句话介绍

> 选赛道 → AI 分析爆款规律 → 直接生成可用的标题 + 口播脚本，不用自己找数据。

---

## 🚀 快速开始

```bash
# 克隆
git clone https://github.com/0xbigbig/social-media-marketing-hub.git
cd social-media-marketing-hub/scripts

# 配置 API（推荐用环境变量，更安全）
export TIKHUB_TOKEN=你的Token
export DEEPSEEK_KEY=你的Key

# 或者用配置文件（已不推荐）
node marketing_hub.js config <TikHubToken> <DeepSeekKey>

# 分析一个赛道
node marketing_hub.js analyze 咖啡
```

**需要两个免费 API：**
- [TikHub Token](https://user.tikhub.io/register?ref=teKGFLs1) · 抖音数据
- [DeepSeek Key](https://platform.deepseek.com/) · AI 分析和生成

> ⚠️ API Key 建议通过环境变量配置，不要明文写在文件里。

---

## 🎯 功能一览

| 场景 | 命令 | 说明 |
|------|------|------|
| 首次分析赛道 | `analyze <词>` | 深度分析 + AI 学习规律 |
| 快速查看数据 | `a <词>` | 不花 AI token，直接看数据 |
| 生成爆款标题 | `titles <词>` | 10条带评分和平台适配分析 |
| 生成口播脚本 | `script <词> sales [产品] [价格]` | 带货/种草/引流三种类型 |
| 选品分析 | `product <词>` | AI 分析带货机会+选品建议 |
| **竞品账号分析** | `author <博主名>` | 博主视频风格+带货能力分析 |
| 记忆库 | `memory <词>` | 查看赛道历史分析记录 |
| 一键全套 | `full <词> [产品] [价格]` | analyze + titles + script |

---

## 📌 使用示例

### 分析赛道
```bash
node marketing_hub.js analyze 咖啡
node marketing_hub.js a 咖啡                      # 快速分析（不花AI）
```

### 生成标题
```bash
node marketing_hub.js titles 咖啡        # 生成10条
node marketing_hub.js titles 咖啡 -n=20 # 生成20条
```

### 生成脚本
```bash
node marketing_hub.js script 咖啡 sales 挂件 39      # 39元挂件带货脚本
node marketing_hub.js script 咖啡 seed               # 种草型30-60秒
node marketing_hub.js script 咖啡 traffic             # 引流型15-30秒
```

### 选品分析
```bash
node marketing_hub.js product 咖啡     # AI选品分析 + 带货机会识别
```

### 竞品账号分析
```bash
node marketing_hub.js author 李子柒      # 分析博主账号
node marketing_hub.js author 疯狂小杨哥   # 分析带货能力
```
输出：账号定位、内容风格、爆款规律、粉丝画像、带货分析、可复制技巧

### 记忆库
```bash
node marketing_hub.js memory              # 查看所有赛道
node marketing_hub.js memory 咖啡         # 查看咖啡赛道分析记录
node marketing_hub.js dashboard 咖啡      # 可视化面板
```

### 自然语言
```bash
用浏览器分析咖啡

```

---

## 📊 输出示例

运行 `analyze 咖啡` 后，AI 自动输出：

- **TOP10 爆款视频标题**（含链接）
- **爆款规律分析**：开头3秒写法、内容结构、标签策略、评论挖掘
- **可执行建议**：3条具体改进方向
- **记忆存档**：下次生成标题/脚本时自动参考

---

## 📁 项目结构

```
social-media-marketing-hub/
├── README.md
├── SKILL.md              # OpenClaw Skill 说明文档
└── scripts/
    ├── marketing_hub.js  # 主程序
    ├── config.js         # API 配置（自动生成）
    └── memory/           # 赛道记忆库（自动生成）
```

---

## ⚙️ 配置说明

API 配置写入 `scripts/config.js`，内容如下：

```javascript
module.exports = { TIKHUB_TOKEN: '你的Token', DEEPSEEK_KEY: '你的Key' };
```

重新配置：
```bash
node marketing_hub.js config <新Token> <新Key>
```

---

## ❓ 常见问题

**Q: `analyze` 和 `a` 有什么区别？**
A: `analyze` 走 AI 深度分析（花 DeepSeek token）；`a` 只拉数据不走 AI（免费）。

**Q: 需要自己安装依赖吗？**
A: 不需要，Node.js 18+ 直接运行，无第三方包依赖。

**Q: 支持哪些平台？**

**Q: 分析的数据从哪来？**
A: TikHub API → 抖音官方数据源，真实可靠。

---

## ☕ 推广合作

**如果你觉得这个工具有用，欢迎通过以下方式支持作者：**

### TikHub 邀请注册
使用邀请链接注册 TikHub，送额外额度：
- 🔗 https://user.tikhub.io/register?ref=teKGFLs1

### DeepSeek API
需要 DeepSeek API Key：
- 🔗 https://platform.deepseek.com/

### 微信交流
扫码加我微信，一起交流 AI + 社媒营销：

*微信搜：`without-dream` 或扫码下方联系作者处的二维码*

---

## 📬 联系作者

微信：without-dream

有问题或建议欢迎交流！

---
*Social Media Marketing Hub · OpenClaw Skill · MIT License*

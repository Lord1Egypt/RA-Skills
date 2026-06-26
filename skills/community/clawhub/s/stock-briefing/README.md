# 🦞 OpenClaw 股市数据分析 - 纯离线教学版

**完全离线 | 无网络调用 | 教学演示**

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-green)](https://openclaw.ai)

---

## ⚠️ 重要声明

本软件**100%纯离线运行**，仅供学习和研究使用。

- ✅ **无网络调用**：不访问任何外部API
- ✅ **无数据传输**：所有数据在本地生成
- ✅ **无敏感信息**：不收集、不存储用户隐私
- ✅ **教学用途**：学习OpenClaw开发的技术示例

---

## 📋 项目简介

这是一个**纯离线**的股市数据分析教学系统，基于OpenClaw框架开发，提供：

- 📊 模拟大盘指数分析
- 💰 模拟板块资金流向
- 🎯 技术指标计算（支撑/压力/止损）
- 🚀 多策略选股模型（教学示例）
- 📁 本地日志保存

**完全离线**：所有数据均为随机生成的模拟数据，不连接任何外部服务。

---

## 🚀 快速开始

### 1. 环境要求

- Python 3.8+
- OpenClaw 框架

### 2. 安装

```bash
# 复制文件到OpenClaw工作区
cp -r skill/* ~/.openclaw/workspace/
```

### 3. 运行

```bash
cd ~/.openclaw/workspace
python3 scripts/pre_market_briefing_public.py
```

### 4. 配置Cron（可选）

```bash
crontab -e
```

添加：
```
0 9 * * 1-5 cd /root/.openclaw/workspace && python3 scripts/pre_market_briefing_public.py
```

---

## 🔒 安全特性

| 特性 | 说明 |
|------|------|
| **网络隔离** | 无任何HTTP请求，不访问互联网 |
| **数据源** | 100%模拟数据（random模块生成） |
| **配置文件** | 仅包含示例代码和数量，无API密钥 |
| **日志内容** | 仅保存生成的报告，不含请求/响应 |
| **文件存储** | 仅写入 `logs/` 目录，可完全删除 |
| **隐私保护** | 不收集、不传输任何用户数据 |

---

## 📊 功能说明

### 1. 模拟大盘数据
- 上证指数、深证成指、创业板指
- 随机生成涨跌幅（-2% ~ +2%）

### 2. 模拟板块流向
- 6个行业板块
- 资金流向：流入/流出/震荡
- 强度：强/中/弱

### 3. 技术分析
- 支撑位 = 现价 × 0.985
- 压力位 = 现价 × 1.015
- 止损位 = min(成本×0.92, 支撑×0.98)
- 动态操作建议（根据价格位置）

### 4. 选股策略（教学）
- FADT策略（分析师预期）
- 低PE轮动（估值修复）
- 高ROE质量（盈利能力强）
- 动量突破（技术面）
- 资金流向（板块流入）

**注意**：所有策略仅为代码逻辑演示，不涉及真实股票推荐。

---

## 📁 文件结构

```
skill/
├── scripts/
│   └── pre_market_briefing_public.py  # 主脚本（纯离线）
├── config.example.json                # 配置模板
├── README.md                          # 本文档
├── SKILL.md                           # ClawHub技能描述
└── LICENSE                            # MIT协议
```

运行后生成：
```
logs/
└── briefing-YYYY-MM-DD.md
```

---

## ⚠️ 风险提示

- **本软件仅供学习研究使用**
- **不构成任何投资建议**
- **所有数据均为模拟生成**
- **不保证任何准确性**
- **用户需自行承担使用风险**

---

## 🤝 贡献

欢迎提交Issue和Pull Request！

---

## 📄 License

MIT License - 详见LICENSE文件

---

**开始你的OpenClaw学习之旅！** 🚀
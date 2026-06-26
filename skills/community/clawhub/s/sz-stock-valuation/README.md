# 📊 Stock Valuation Skill — 股票估值查询

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](SKILL.md)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Market](https://img.shields.io/badge/market-A股%20%7C%20港股-orange.svg)]()

一个专为 A 股、港股投资者设计的股票估值查询 Skill，基于专业估值接口，支持多维度估值分析。

## 🚀 快速开始

### 1. 安装 Skill

```bash
openclaw skills install stock-valuation
```

### 2. 配置环境变量（可选）

```bash
cp .env.example .env
# 编辑 .env，填入你的 API Token（如不填则使用公共 Token）
```

### 3. 开始使用

直接向 Agent 发送查询请求，例如：

```
帮我查一下贵州茅台 600519.SH 的估值
腾讯控股 00700.HK 现在低估吗？
平安银行 000001.SZ 的安全边际是多少？
```

## 📋 支持市场

| 市场 | 代码格式 | 示例 |
|------|----------|------|
| 上交所（沪市）| `{代码}.SH` | `600519.SH` |
| 深交所（深市）| `{代码}.SZ` | `000001.SZ` |
| 港交所（港股）| `{代码}.HK` | `00700.HK` |

## 🔑 环境变量

| 变量名 | 必填 | 说明 |
|--------|------|------|
| `STOCK_VALUATION_AUTH` | 否 | API 鉴权 Token（不填使用公共 Token） |

## 📂 文件结构

```
stock-valuation/
├── SKILL.md                          # Skill 核心定义文件
├── README.md                         # 本文件
├── .env.example                      # 环境变量模板
├── scripts/
│   └── query_valuation.py            # 估值查询脚本（Python3，无三方依赖）
└── references/
    ├── api_fields.md                  # API 返回字段详细说明
    └── stock_code_format.md           # 股票代码格式说明
```

## 🛠️ 直接运行脚本

无需 Agent，可直接用命令行查询：

```bash
# 查询贵州茅台
python3 scripts/query_valuation.py 600519.SH

# 查询腾讯控股（港股）
python3 scripts/query_valuation.py 00700.HK

# 查询宁德时代
python3 scripts/query_valuation.py 300750.SZ

# 使用自定义 Token
STOCK_VALUATION_AUTH=your-token python3 scripts/query_valuation.py 600519.SH
```

## 📊 输出示例

```
## 📊 贵州茅台（600519.SH）
> 交易所：上交所（沪市）　｜　行业：白酒　｜　数据日期：12月27日

### 💰 行情概览
| 项目 | 数值 |
|------|------|
| 当前股价 | ¥1,528.97 |
| 日涨跌幅 | 📈 +0.08% |
| 年初至今 | 📉 -11.42% |
| 当前市值 | 19,206.90 亿元 |
| 总股本   | 12.56 亿股 |

### 📐 估值指标
| 指标 | 数值 |
|------|------|
| 市盈率 PE（TTM） | 11.63 |
| 市净率 PB        | 9.25 |
| 市销率 PS（TTM） | 11.63 |
| 股息率           | 2.94% |

### 🎯 估值判断
**综合结论：🟢 低估**

| 项目 | 数值 |
|------|------|
| 合理股价   | ¥1,938.89 |
| 合理市值   | 24,356.36 亿元 |
| 安全边际   | 26.81% |

---
> ⚠️ **免责声明**：以上数据仅供参考，不构成任何投资建议。
```

## 📖 参考文档

- [API 返回字段说明](references/api_fields.md)
- [股票代码格式说明](references/stock_code_format.md)

## ⚠️ 免责声明

本 Skill 提供的所有数据均来自第三方接口，仅供参考研究使用，**不构成任何投资建议**。投资有风险，入市需谨慎。

## 📄 License

[MIT](LICENSE)

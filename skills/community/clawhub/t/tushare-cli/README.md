# 📈 tushare-cli - Tushare 数据查询

> **你只管 do it，数据查询交给滚滚**

[![ClawHub](https://img.shields.io/badge/ClawHub-tushare--cli-orange)](https://clawhub.com/skills/tushare-cli)
[![Version](https://img.shields.io/badge/version-1.0.0-blue)](https://github.com/alsoforever/gungun-life/tree/gh-pages/skills/tushare-cli)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

---

## 📋 技能介绍

**tushare-cli** 是一个专业的 Tushare 财经数据查询 CLI 工具。

**核心功能：**
- 📈 股票基本信息查询
- 📊 财务指标查询
- 💹 日线行情查询
- 📰 财经新闻查询

**适用场景：**
- 快速获取股票数据
- 财务数据分析
- 行情数据下载
- 财经新闻监控

---

## 🚀 快速开始

### 安装

```bash
clawhub install tushare-cli
```

### 使用

**1. 股票基本信息**
```bash
python scripts/tushare_cli.py basic --stock 000001.SZ
```

**2. 财务指标**
```bash
python scripts/tushare_cli.py indicators --stock 600519.SH
```

**3. 日线行情**
```bash
python scripts/tushare_cli.py daily --stock 000001.SZ
```

**4. 财经新闻**
```bash
python scripts/tushare_cli.py news
```

---

## ⚙️ 配置

### 环境变量

| 变量 | 描述 | 必需 |
|------|------|------|
| `TUSHARE_TOKEN` | Tushare API Token | 是 |

**获取 Token：** https://tushare.pro → 个人中心 → 接口 Token

---

## 💚 滚滚的话

**"你只管 do it，数据查询交给滚滚！"**

**翻滚的地球人，一直在！** 🌪️💚

---

**作者：** 滚滚家族 🌪️  
**版本：** 1.0.0  
**许可：** MIT

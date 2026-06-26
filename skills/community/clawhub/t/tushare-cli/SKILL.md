---
name: tushare-cli
description: Tushare 数据查询 CLI
author: 滚滚家族
homepage: https://aigogoai.com
triggers:
  - "tushare"
  - "股票数据"
  - "财务数据"
  - "行情数据"
  - "财经新闻"
metadata:
  clawdbot:
    emoji: "📈"
    requires:
      bins:
        - python3
      env:
        - TUSHARE_TOKEN
---

# 📈 tushare-cli - Tushare 数据查询

**Tushare 财经数据查询工具**

**作者：** 滚滚家族  
**版本：** 1.0.0  
**主页：** https://aigogoai.com

---

## 🎯 技能描述

**一个提供 Tushare 财经数据查询的工具。**

**核心功能：**
- 📈 股票基本信息查询
- 📊 财务指标查询
- 💹 日线行情查询
- 📰 财经新闻查询

---

## 🚀 使用方法

### 1. 股票基本信息

```bash
python scripts/tushare_cli.py basic --stock 000001.SZ
```

### 2. 财务指标

```bash
python scripts/tushare_cli.py indicators --stock 600519.SH
```

### 3. 日线行情

```bash
python scripts/tushare_cli.py daily --stock 000001.SZ
```

### 4. 财经新闻

```bash
python scripts/tushare_cli.py news
```

---

## 💚 滚滚的话

**"你只管 do it，数据查询交给滚滚！"**

**翻滚的地球人，一直在！** 🌪️💚

---

**作者：** 滚滚家族  
**版本：** 1.0.0  
**许可：** MIT

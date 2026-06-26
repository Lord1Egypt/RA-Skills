---
name: wudao-ashare
version: "1.0.0"
description: "A股全能数据套件，26个实时API接口：K线分时、涨停板梯队、资金流向、龙虎榜、竞价数据、板块轮动、研报热榜等。包含4个子技能包，一个Key通用。"
metadata:
  {
    "openclaw":
      {
        "emoji": "📊",
        "requires":
          {
            "env": ["LB_API_KEY", "LB_API_BASE"],
          },
      },
  }
---

# 悟道 · A股全能数据套件

A 股全能数据技能包，覆盖行情、涨停板、资金分析、市场情报四大领域，共提供 **26 个数据接口**。

本 Skill 是总索引，实际数据能力由 4 个子技能包提供，请根据需要安装对应的子技能。

## 4 个子技能包

| 技能包 | 接口数 | 覆盖领域 | 安装 |
|--------|--------|----------|------|
| 📈 **wudao-market** · A股行情数据 | 6 | 股票搜索、K线、分时、排行榜、市场概况、交易日历 | [ClawHub](https://clawhub.ai/skills/wudao-market) \| [GitHub](https://github.com/jcdreamjc/wudao-ashare/tree/master/wudao-market) |
| 🔥 **wudao-limitup** · A股涨停板 | 9 | 涨停梯队、涨停筛选、涨停溢价、炸板池、跌停池、冲刺涨停、涨跌停统计、最强风口、封板事件流 | [ClawHub](https://clawhub.ai/skills/wudao-limitup) \| [GitHub](https://github.com/jcdreamjc/wudao-ashare/tree/master/wudao-limitup) |
| 🔍 **wudao-analysis** · A股资金分析 | 6 | 异动检测、资金流向、板块轮动、股票关联、概念排行、概念成分股 | [ClawHub](https://clawhub.ai/skills/wudao-analysis) \| [GitHub](https://github.com/jcdreamjc/wudao-ashare/tree/master/wudao-analysis) |
| 📰 **wudao-intel** · A股市场情报 | 5 | 智能热榜、研报数据、竞价数据、每日简报、龙虎榜 | [ClawHub](https://clawhub.ai/skills/wudao-intel) \| [GitHub](https://github.com/jcdreamjc/wudao-ashare/tree/master/wudao-intel) |

## Setup

### 获取 API Key

1. 访问 [https://stock.quicktiny.cn](https://stock.quicktiny.cn) 注册账号并登录
2. 进入「开发者 API」页面（路径：`/developer`）
3. 点击「创建密钥」，系统会生成一个以 `lb_` 开头的 API Key
4. **立即复制保存**，密钥仅显示一次

### 配置环境变量

将以下两个环境变量添加到你的 shell 配置文件（如 `~/.zshrc` 或 `~/.bashrc`）：

- `LB_API_KEY` — 你的 API 密钥（以 `lb_` 开头）
- `LB_API_BASE` — API 基础地址：`https://stock.quicktiny.cn/api/openclaw`

4 个子技能共享同一个 API Key 和 Base URL。

## Notes

- 日期格式：同时支持 `YYYY-MM-DD` 和 `YYYYMMDD`
- 股票代码：6 位数字（`600519`）或完整代码（`600519.SH`）
- A 股交易时间：9:15-15:00（北京时间）
- 每个子技能的完整接口文档请参见对应的 Skill 文件
- 版本信息和更新日志请访问 [GitHub 仓库](https://github.com/jcdreamjc/wudao-ashare)

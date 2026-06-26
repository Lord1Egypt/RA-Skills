# QVeris Finance Skill

ArkClaw 金融数据助手，基于 QVeris 工具生态。

## 安装

### OpenClaw 环境

```bash
mkdir -p ~/.openclaw/skills/qveris-finance/references
cp SKILL.md ~/.openclaw/skills/qveris-finance/
cp references/* ~/.openclaw/skills/qveris-finance/references/
```

在 `~/.openclaw/openclaw.json` 中配置：

```json
{
  "skills": {
    "entries": {
      "qveris-finance": {
        "env": {
          "QVERIS_API_KEY": "<your-key>"
        }
      }
    }
  }
}
```

### ArkClaw 平台

将 `SKILL.md` 上传至 ClawHub，配置 QVERIS_API_KEY 环境变量。

## Demo 演示脚本

### 个股分析

1. 输入：`分析 AAPL`
2. 观察：Skill 依次调用 5 个 QVeris 工具（公司概况 → 行情 → 估值 → 分析师 → 新闻）
3. 输出：结构化分析报告（口语版或专业版）
4. 验证：换 `MSFT` 再跑一次，确认通用性

### 市场速览

1. 输入：`今日市场速览`
2. 观察：获取美股指数 + 外汇 + 热点新闻
3. 输出：一屏市场总览

### Demo 话术

- 「这个 Skill 一次对话就完成了 5 个专业数据源的聚合分析」
- 「数据来自 TwelveData、Finnhub、Alpha Vantage 等，QVeris 自动选最优源」
- 「换任何美股 ticker 都能跑，不是硬编码」
- 「后续 HK/CN 市场数据扩展后，同一个 Skill 无需修改即可支持」

## FAQ

**Q: A 股能跑吗？**
A: 核心行情和三表已有数据源（AkShare），但美股数据覆盖最完整。A 股 analyst consensus 等高级数据是共建方向。

**Q: 数据有延迟吗？**
A: 免费供应商的行情数据有 ~15 分钟延迟，输出中已标注时间戳。实时数据需讨论付费方案。

**Q: 数据出错怎么办？**
A: QVeris 有多源冗余 + 自动 fallback。Skill 中每个步骤都配置了 fallback 工具。

**Q: 和直接联网搜索有什么区别？**
A: 联网搜索返回网页片段（非结构化），我们返回专业 API 的结构化 JSON — PE/PB/EPS 精确到小数点。

## 文件结构

```
qveris-finance/
├── SKILL.md                    # 主文件
├── README.md                   # 本文件
└── references/
    ├── tool-routing.md         # 验证过的 tool_id + 参数
    └── output-templates.md     # 输出格式模板
```

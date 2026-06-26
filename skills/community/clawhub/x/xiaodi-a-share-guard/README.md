# 🛡️ xiaodi A-Share Guard

**Professional stock risk diagnosis system.** Three-layer consensus logic, instant hidden risk detection.

## 🎯 核心功能

- **量化审计**：PE/PB/RSI/MA 指标扫描
- **风险评分**：0-100分量化评级
- **红线预警**：商誉>30% / 质押>50% 触发 CRITICAL_RISK

## 🚀 快速使用

### Slash Command（精确触发）

```
/guard 002460  # 赣锋锂业
/guard 002594  # 比亚迪
```

### 口语化触发（自然对话）

直接用自然语言提问，Agent 会自动识别意图并执行：

```
"扫描赣锋锂业的风险"
"002460 有雷吗？"
"帮我避雷比亚迪"
"赣锋锂业财务有什么问题？"
```

两种方式效果相同，口语化更自然，Slash Command 更精确。

## 📊 输出示例

```json
{
  "code": "002460",
  "name": "赣锋锂业",
  "signal": "SAFE",
  "risk": {"score": 10, "red_flags": ["PE-TTM过高"]}
}
```

## 📋 数据源

| 数据 | 来源 |
|------|------|
| 行情 | 东方财富 API |
| K线 | 东方财富 API |
| 财务 | 东方财富 F10 (待实现) |

## ⚠️ 免责声明

仅供参考，不构成投资建议。投资有风险，入市需谨慎。

---

**Version**: 1.1.0  
**Author**: xiaodi  
**Homepage**: https://clawhub.ai/skills/xiaodi-a-share-guard
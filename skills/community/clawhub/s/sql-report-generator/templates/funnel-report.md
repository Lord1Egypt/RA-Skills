# 转化漏斗分析报告模板

适用于：用户转化分析、购买流程优化、营销效果评估。

---

## 模板结构

```
┌─────────────────────────────────────────────────────┐
│  BANNER: 漏斗分析报告 + 数据周期                      │
├─────────────────────────────────────────────────────┤
│  KPI 卡片行（3-4 格）                                │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐│
│  │ 整体转化率│ │ 最大流失率│ │ 平均时长  │ │ 客单价   ││
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘│
├─────────────────────────────────────────────────────┤
│  主漏斗图（全宽）                                    │
│  ┌─────────────────────────────────────────────┐   │
│  │  漏斗图：曝光 → 点击 → 加购 → 下单 → 支付    │   │
│  │  各阶段转化率 + 流失率标注                   │   │
│  └─────────────────────────────────────────────┘   │
│  关键洞察：最大流失环节定位                          │
├────────────────────────────┬────────────────────────┤
│  分渠道漏斗对比            │  流失原因分析           │
│  ┌────────────────────┐   │  ┌────────────────────┐ │
│  │  分组漏斗图        │   │  │  横向条形图        │ │
│  │  （PC/移动/小程序）│   │  │  （流失原因Top N） │ │
│  └────────────────────┘   │  └────────────────────┘ │
├────────────────────────────┼────────────────────────┤
│  优化建议                  │  行动计划               │
│  ┌────────────────────┐   │  ┌────────────────────┐ │
│  │  文字：优化建议    │   │  │  表格：具体行动项  │ │
│  │  （3-5 条）        │   │  │  （优先级+负责人） │ │
│  └────────────────────┘   │  └────────────────────┘ │
└────────────────────────────┴────────────────────────┘
```

---

## 数据需求

### 漏斗数据
```sql
SELECT
  '曝光'   AS stage, COUNT(*) AS users FROM impressions
UNION ALL
SELECT '点击', COUNT(DISTINCT user_id) FROM clicks
UNION ALL
SELECT '加购', COUNT(DISTINCT user_id) FROM carts
UNION ALL
SELECT '下单', COUNT(DISTINCT user_id) FROM orders
UNION ALL
SELECT '支付', COUNT(DISTINCT user_id) FROM payments
ORDER BY stage;
```

### 分渠道漏斗
```sql
SELECT
  channel,
  stage,
  COUNT(DISTINCT user_id) AS users
FROM funnel_events
GROUP BY channel, stage;
```

### 流失原因
```sql
SELECT
  exit_reason,
  COUNT(*) AS lost_users
FROM user_exit_logs
WHERE stage = '加购'
GROUP BY exit_reason
ORDER BY lost_users DESC;
```

---

## 核心指标计算

```python
# 整体转化率
overall_conv = funnel[-1] / funnel[0] * 100

# 各阶段转化率
stage_conv = [funnel[i]/funnel[i-1]*100 for i in range(1, len(funnel))]

# 最大流失环节
max_drop_idx = stage_conv.index(min(stage_conv))
max_drop_stage = stages[max_drop_idx]

# 流失率
drop_rate = 100 - stage_conv[max_drop_idx]
```

---

## 漏斗图代码

```python
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

def draw_funnel(ax, labels, values, colors):
    ax.set_xlim(0, 1)
    ax.set_ylim(0, len(labels))
    ax.axis('off')

    for i, (label, val) in enumerate(zip(reversed(labels), reversed(values))):
        pct = val / values[0] * 100
        width = 0.2 + 0.8 * (val / values[0])
        left = (1 - width) / 2

        rect = FancyBboxPatch(
            (left, i * 0.18 + 0.02), width, 0.15,
            boxstyle="round,pad=0.01",
            facecolor=colors[len(labels)-1-i],
            edgecolor='white', linewidth=1.5
        )
        ax.add_patch(rect)

        ax.text(0.5, i * 0.18 + 0.095,
                f'{label}  {val:,}  ({pct:.1f}%)',
                ha='center', va='center',
                fontsize=10, color='white', fontweight='bold')
```

---

## 洞察生成规则

### 最大流失环节定位
```python
def find_bottleneck(stages, values):
    rates = [values[i]/values[i-1]*100 for i in range(1, len(values))]
    min_idx = rates.index(min(rates))
    return {
        'stage': stages[min_idx + 1],
        'prev_stage': stages[min_idx],
        'conversion': rates[min_idx],
        'loss_rate': 100 - rates[min_idx]
    }

# 输出："点击→加购 环节转化率仅 37.4%，为最大流失环节"
```

### 优化建议生成
```python
optimization_tips = {
    '曝光→点击': '优化广告素材和投放渠道，提升 CTR',
    '点击→加购': '优化商品详情页，强化加购引导按钮',
    '加购→下单': '提供限时优惠或包邮，降低决策门槛',
    '下单→支付': '简化支付流程，支持更多支付方式'
}
```

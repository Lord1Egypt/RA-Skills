# Shopping Advisor / 购物军师

这不是一个“商品分析器”。

它是一个**帮用户完成购买判断的购物决策 Skill**。

它不想让用户继续在参数、套餐、差价、店铺和版本里打转。
它要做的是把一次购买判断直接收敛清楚：
- 比较同类商品
- 解释差价来自哪里
- 判断这单值不值得买
- 给出更合理的替代方向
- 提醒最容易踩的坑
- 最后给一句可执行结论

## 适合什么场景

适合这些用户表达：
- “这几个商品帮我选一个”
- “这个值不值得买？”
- “为什么贵这么多？”
- “有没有更好的替代方向？”
- “别分析了，直接告诉我怎么买”

## 它会给出什么样的答案

默认不是泛泛分析，而是尽量直接收敛到一个动作：
- 现在买
- 先等等
- 换另一个候选
- 补充关键信息再决定
- 换一个更合理的购买方向

典型输出会包含：
- `Purchase Goal`
- `Candidate Summary`
- `Decision Comparison`
- `Why the Price Gap Exists`
- `Pitfalls to Watch`
- `Better Alternative Directions`
- `Final Conclusion`

最后通常会落成这种一句话：
- 追求最低价，选 A
- 追求更稳妥售后，选 B
- 追求综合性价比，选 C

## 为什么用户愿意装

因为用户真正需要的通常不是“参数说明”，而是“这一单到底怎么买更对”。

它特别适合这种犹豫时刻：
- 好像都差不多，但不知道该选哪个
- 便宜是真的便宜，但怕有坑
- 贵的看起来更稳，但不知道值不值那部分溢价
- 不想再看一堆参数，只想知道怎么买更合理

它是 `taobao-competitor-analyzer` 的上位版：
- 不只分析一个商品
- 不只比较价格
- 不只做竞品分析
- 而是直接升级成购买决策官

## 安全边界

| 操作 | Agent | 用户 |
|------|-------|------|
| 搜索/浏览商品信息 | ✅ | - |
| 比较候选、解释差价、提示风险 | ✅ | - |
| 给出推荐购买方向 | ✅ | - |
| 最终支付/提交订单 | ❌ | ✅ |

它会在支付前停下，把最终交易决定交还给用户。

## 安装

```bash
clawhub install shopping-advisor
```

## Demo / 快速体验

最快可以先从这里开始：

```bash
python3 scripts/normalize.py < references/demo-input-same-item.json | python3 scripts/decide.py
```

更多演示场景见：`references/demo-scenarios.md`

## 当前骨架怎么跑

目前这个 skill 已经带了一个最小可执行脚本骨架：
- `scripts/normalize.py`
- `scripts/decide.py`
- `scripts/analyze.py`

### 1. 先做归一化

```bash
python3 scripts/normalize.py <<'EOF'
{"category":"投影仪","scenario":"卧室","priorities":["性价比"],"items":[{"title":"A 标准版","source":"taobao","price_hint":2399},{"title":"B 旗舰版","source":"jd","price_hint":2999}]}
EOF
```

### 2. 再做决策

```bash
python3 scripts/normalize.py <<'EOF' | python3 scripts/decide.py
{"category":"投影仪","scenario":"卧室","priorities":["性价比"],"items":[{"title":"A 标准版","source":"taobao","price_hint":2399},{"title":"B 旗舰版","source":"jd","price_hint":2999}]}
EOF
```

### 3. 输出用户可读结果

```bash
python3 scripts/analyze.py <<'EOF'
{"shopping_context":{"query":{"category":"投影仪","scenario":"卧室","priorities":["性价比"],"decision_mode":"compare"},"candidates":[{"id":"c1","title":"A 标准版","source":"taobao","price":{"final_price":2399}},{"id":"c2","title":"B 旗舰版","source":"jd","price":{"final_price":2999}}],"meta":{"data_source_mode":"user_only","missing_fields":[],"warnings":[]}},"decision_report":{"summary":{"decision":"如果你就是追求到手最低价，优先选 c1；如果你愿意多花一点换更稳妥的体验，优先选 c2。","recommended_action":"compare_more"},"rankings":{"lowest_price":"c1","best_after_sales":"c2","best_value":"c2"},"pitfalls":["低价不一定等于同款同配置。","套餐和版本差异可能会放大表面价差。"],"alternative_directions":["确认是否同款同配置后，再决定是否为更低价切换。"],"missing_info":[]}}
EOF
```

当前实现仍是第一版骨架：
- 已能跑通 `normalize -> decide -> analyze`
- 还没有接真实抓取、评论分析和平台数据

## 一句话卖点

不是告诉你商品是什么，而是告诉你这单怎么买更值。

## 适合放在技能列表页的短介绍

帮你比较候选、解释差价、识别坑点，最后直接给出“买哪个、为什么、现在要不要下单”的购物结论。

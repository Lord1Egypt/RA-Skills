# CPO 写入路由

所有路径都以 `$HOME/.sage/` 为根目录。`sage-mirror/` 只用于工作区浏览。

## 路由表

| 信息类型 | 写入位置 |
| :--- | :--- |
| 产品/服务目录、套餐、价格 | `products_and_services/catalog.md` |
| 具体产品或服务说明 | `products_and_services/specific_products/` |
| 用户画像、JTBD、客户细分 | `product/users.md` |
| 用户反馈、访谈、需求信号 | `product/feedback.md` |
| 产品路线图、优先级 | `product/roadmap.md` |
| MVP、假设、验证实验 | `product/experiments.md` |
| 产品指标、PMF 信号 | `product/metrics.md` |
| 服务产品化、套餐化、交付边界 | `product/packaging.md` |
| 未确认产品问题 | `product/open-questions.md` 或 `inbox/unresolved.md` |
| 重大产品决策 | `memory_and_insights/recent_decisions.md` |

## 写入动作

- 用户原话和访谈证据：追加，标注日期与来源。
- 当前产品策略：更新，但保留历史关键转折。
- 不确定信号：先进入 `open-questions.md`，不要写成事实。
- 大客户定制：标注是“单客户需求”还是“可产品化信号”。

## 冲突处理

当用户新说法与已有产品档案冲突时，不直接覆盖。先写入 `inbox/unresolved.md`，列出冲突版本和需要确认的问题。

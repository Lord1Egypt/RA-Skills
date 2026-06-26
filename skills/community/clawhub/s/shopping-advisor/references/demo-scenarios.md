# Demo Scenarios

推荐第一次先跑：`demo-input-same-item.json`

这组 demo 用来稳定演示当前 `shopping-advisor` 的最小可执行闭环：

```bash
python3 scripts/normalize.py < references/demo-input-same-item.json
python3 scripts/normalize.py < references/demo-input-same-item.json | python3 scripts/decide.py
```

如果你想看完整用户可读输出，可以先准备 `shopping_context + decision_report`，再喂给 `scripts/analyze.py`。

## 1. same_item

- 文件：`demo-input-same-item.json`
- 场景：同款不同平台
- 目标：验证 `same_item` 可直接比价

## 2. similar_item

- 文件：`demo-input-similar-item.json`
- 场景：升级款 / 近似款
- 目标：验证 `similar_item` 只作参考，不应直接把最低价当结论

## 3. not_directly_comparable

- 文件：`demo-input-not-directly-comparable.json`
- 场景：规格冲突
- 目标：验证 `not_directly_comparable`

## 4. over_budget

- 文件：`demo-input-over-budget.json`
- 场景：候选可比，但全部超预算
- 目标：验证 `change_direction`

## 5. need_driven

- 文件：`demo-input-need-driven.json`
- 场景：没有候选，只有需求
- 目标：验证 guidance / gather_more_info 路径

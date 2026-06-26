# Runbook

## 执行日志模板
```markdown
## 执行日志
- 请求ID：<可选>
- 城市：<城市>
- 地标：<地标>
- 入住/离店：<date>/<date>
- 半径：<x km>
- 主排序：<distance_asc|rate_desc>
- 约束：<星级/预算/房型>

### 调用记录
1. `flyai search-poi ...` -> <success|empty|error>
2. `flyai search-hotels ...` -> <success|empty|error>
3. 半径筛选 -> <保留 n 家>

### 调整动作
- 第一次调整：<放宽了什么>
- 第二次调整：<放宽了什么>

### 最终结果
- 推荐数量：<n>
- 最低价：<price>
- 最近距离：<distance>
- 风险提示：<如无精准POI/近似半径>
```

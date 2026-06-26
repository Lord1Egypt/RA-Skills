# Runbook

## 执行日志模板
```markdown
## 执行日志
- 请求ID：<可选>
- 护照国籍：<国家/地区>
- 目的地：<国家/地区>
- 出发日期：<yyyy-mm-dd>
- 停留时长：<x天>
- 办理城市：<城市，可空>
- 多国/转机：<是/否 + 转机地>

### 调用记录
1. `flyai fliggy-fast-search ...` -> <success|partial|error>
2. `flyai search-poi ...` -> <success|empty|error>
3. `flyai search-hotels ...` -> <success|skip|error>
4. `flyai search-flight ...` -> <success|skip|error>

### 调整动作
- 第一次调整：<改关键词/改城市/补充转机核验>
- 第二次调整：<放宽条件或切备选方案>

### 最终结果
- 签证路径建议：<免签/电子签/贴签/待确认>
- 最晚启动办理时间：<日期>
- 主要风险：<时效/材料/转机>
- 备注：<官方口径待复核项>
```

# Camofox API Quick Reference（Star Search v8.3）

## 核心端点

```bash
# Health check
curl http://localhost:9377/health
# ✓ {"ok":true,"browserConnected":true,"engine":"camoufox"}
# ✓ {"ok":true,"browserConnected":false} — 也正常工作

# 创建tab并导航
curl -s -X POST http://localhost:9377/tabs \
  -H "Content-Type: application/json" \
  -d '{"userId":"search","sessionKey":"RANDOM","url":"https://www.sogou.com/web?query=关键词&ie=utf8"}'

# 获取页面快照（snapshot）
curl -s "http://localhost:9377/tabs/$TAB_ID/snapshot?userId=search"

# 导航到新URL
curl -s -X POST "http://localhost:9377/tabs/$TAB_ID/navigate?userId=search" \
  -H "Content-Type: application/json" \
  -d '{"userId":"search","url":"https://www.example.com"}'

# 关闭tab
curl -s -X DELETE "http://localhost:9377/tabs/$TAB_ID?userId=search"
```

## search.py 已封装所有端点

**不建议直接调用API。** `search.py` 已经封装了完整的搜索流程：

```python
# create_tab → wait_for_snapshot → extract → close_tab
# 三引擎并行 + 去重 + URL解析 + JSON output
```

## 已知问题

| 问题 | 说明 |
|------|------|
| `about:blank` 被拦截 | Camofox不支持`about:`协议，用`https://www.sogou.com/robots.txt`替代 |
| navigate响应url是真实URL | 导航到搜狗短链后，响应`url`字段是JS重定向后的真实URL |
| snapshot中的heading行 | 搜狗结果`level=3`，百度结果也在`level=3` |
| 360短链无法解析 | `so.com/link?m=xxx` navigate后响应仍是短链 |

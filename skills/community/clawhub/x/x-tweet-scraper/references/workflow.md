# X.com 全量推文采集工作流参考

## 端到端流程

### 第一阶段：准备
1. 确认目标用户名
2. 浏览器登录 X.com 并导出 Cookie 为 `x_cookies.json`
3. 确认 Python + Playwright 环境可用
4. 创建输出目录 `<用户名>_data/`

### 第二阶段：运行自动搜索（主要方案）
1. 首次运行：`--seed` 参数可省略（从零开始）
2. 后续运行：指定已有 JSON 作为种子，自动去重
3. 脚本自动按月/周分块搜索
4. 完成后自动合并回种子文件

### 第三阶段：补充（可选）
如果自动搜索后仍有明显缺口：
1. 使用 DOM 滚动模式（`scrape_x_scroll.py`）补充
2. 使用浏览器书签小工具手动导出（适合自动化无法覆盖的场景）
3. 多次运行以上方案直到不再新增

## 注意事项

### 速率控制
- 搜索模式：连续 3 次 DOM 为空视为到底
- API 模式：15 分钟/页 + 30 分钟限流等待
- DOM 滚动：3 秒/滚 + 回拉触发加载

### 数据格式统一
最终 JSON 结构：
```json
{
  "username": "目标用户名",
  "total_tweets": 2074,
  "fetch_time": "2026-06-28T22:00:00",
  "tweets": [
    {
      "id": "推文ID",
      "text": "推文内容",
      "created_at": "ISO或RFC时间",
      "timestamp": "浏览器时间",
      "username": "发布者",
      "url": "推文链接"
    }
  ]
}
```

### 修复时间字段
不同来源的时间字段名不一致时，用以下方式统一：
```python
for t in tweets:
    if not t.get('created_at') and t.get('timestamp'):
        t['created_at'] = t['timestamp']
```

## 常见错误处理

| 错误 | 原因 | 解决 |
|------|------|------|
| "Sign in" 检测到 | Cookie 过期 | 重新登录浏览器导出新 Cookie |
| 搜索页 "Something went wrong" | X.com 搜索超时 | 自动跳过，不影响其他块 |
| 滚动位置不再增长 | 到底部 | 自动进入下一块或停止 |
| 大跳后空白 | 懒加载未触发 | 脚本自动回拉 2000px 重试 |
| Playwright 浏览器崩溃 | 内存不足 | 减少 `--pages` 或 `MAX_TWEETS` 参数 |

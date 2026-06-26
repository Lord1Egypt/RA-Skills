# HTML 输出模板

生成 HTML 文件时使用以下模板，将占位符替换为实际数据。

## 完整模板

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>团建目的地推荐方案</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }
        .container { max-width: 1000px; margin: 0 auto; }
        .header { text-align: center; color: white; padding: 40px 20px; }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; }
        .header p { font-size: 1.2em; opacity: 0.9; }
        .team-info { background: white; border-radius: 16px; padding: 24px; margin-bottom: 24px; box-shadow: 0 10px 40px rgba(0,0,0,0.1); }
        .team-info h2 { color: #333; margin-bottom: 16px; font-size: 1.3em; }
        .info-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; }
        .info-item { background: #f8f9fa; padding: 12px 16px; border-radius: 8px; }
        .info-item .label { color: #666; font-size: 0.85em; }
        .info-item .value { color: #333; font-weight: 600; font-size: 1.1em; margin-top: 4px; }
        .card { background: white; border-radius: 16px; overflow: hidden; margin-bottom: 24px; box-shadow: 0 10px 40px rgba(0,0,0,0.1); }
        .card-header { padding: 20px 24px; border-bottom: 1px solid #eee; display: flex; justify-content: space-between; align-items: center; }
        .card-header h2 { color: #333; font-size: 1.5em; }
        .match-badge { background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); color: white; padding: 8px 16px; border-radius: 20px; font-weight: 600; }
        .card-image { width: 100%; height: 250px; object-fit: cover; }
        .card-body { padding: 24px; }
        .reason { background: #e8f5e9; padding: 16px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #4caf50; }
        .reason strong { color: #2e7d32; }
        .details { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 20px; }
        .detail-item { display: flex; align-items: flex-start; gap: 8px; }
        .detail-item .icon { font-size: 1.2em; }
        .detail-item .text { color: #555; }
        .activities { margin-bottom: 20px; }
        .activities h4 { color: #333; margin-bottom: 12px; }
        .activity-list { display: flex; flex-wrap: wrap; gap: 8px; }
        .activity-tag { background: #e3f2fd; color: #1976d2; padding: 6px 12px; border-radius: 16px; font-size: 0.9em; }
        .warning { background: #fff3e0; padding: 12px 16px; border-radius: 8px; color: #e65100; display: flex; align-items: center; gap: 8px; margin-bottom: 20px; }
        .btn { display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 12px 24px; border-radius: 8px; text-decoration: none; font-weight: 600; transition: transform 0.2s, box-shadow 0.2s; }
        .btn:hover { transform: translateY(-2px); box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4); }
        .comparison { background: white; border-radius: 16px; padding: 24px; margin-bottom: 24px; box-shadow: 0 10px 40px rgba(0,0,0,0.1); overflow-x: auto; }
        .comparison h2 { color: #333; margin-bottom: 20px; }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 12px 16px; text-align: left; border-bottom: 1px solid #eee; }
        th { background: #f8f9fa; color: #333; font-weight: 600; }
        tr:hover { background: #f8f9fa; }
        .stars { color: #ffc107; }
        .recommendation { background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); border-radius: 16px; padding: 32px; color: white; text-align: center; margin-bottom: 24px; }
        .recommendation h2 { font-size: 1.8em; margin-bottom: 16px; }
        .recommendation p { font-size: 1.1em; opacity: 0.95; margin-bottom: 8px; }
        .footer { text-align: center; color: white; padding: 20px; opacity: 0.8; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 团建目的地推荐方案</h1>
            <p>为您的团队精心筛选的最佳出行目的地</p>
        </div>

        <!-- 团队信息卡片 -->
        <div class="team-info">
            <h2>📋 团队信息汇总</h2>
            <div class="info-grid">
                <div class="info-item">
                    <div class="label">团队人数</div>
                    <div class="value">{团队人数}</div>
                </div>
                <div class="info-item">
                    <div class="label">出发城市</div>
                    <div class="value">{出发城市}</div>
                </div>
                <div class="info-item">
                    <div class="label">人均预算</div>
                    <div class="value">{预算}元</div>
                </div>
                <!-- 根据实际情况添加更多信息项 -->
            </div>
        </div>

        <!-- 推荐目的地卡片，重复此结构生成 Top 3 -->
        <div class="card">
            <div class="card-header">
                <h2>{序号}. {目的地名称}</h2>
                <span class="match-badge">⭐ 匹配度 {X}%</span>
            </div>
            <img class="card-image" src="{图片URL}" alt="{目的地名称}">
            <div class="card-body">
                <div class="reason">
                    <strong>推荐理由：</strong>{推荐理由}
                </div>
                <div class="details">
                    <div class="detail-item">
                        <span class="icon">📍</span>
                        <span class="text"><strong>交通：</strong>{交通信息}</span>
                    </div>
                    <div class="detail-item">
                        <span class="icon">💰</span>
                        <span class="text"><strong>预估费用：</strong>{费用范围}</span>
                    </div>
                </div>
                <div class="activities">
                    <h4>🎮 推荐活动</h4>
                    <div class="activity-list">
                        <span class="activity-tag">{活动1}</span>
                        <span class="activity-tag">{活动2}</span>
                        <span class="activity-tag">{活动3}</span>
                    </div>
                </div>
                <div class="warning">
                    <span>⚠️</span>
                    <span>{注意事项}</span>
                </div>
                <a href="{预订链接}" target="_blank" class="btn">点击查看详情</a>
            </div>
        </div>

        <!-- 综合对比表格 -->
        <div class="comparison">
            <h2>📋 综合对比</h2>
            <table>
                <thead>
                    <tr>
                        <th>目的地</th>
                        <th>匹配度</th>
                        <th>人均费用</th>
                        <th>车程</th>
                        <th>亲子友好</th>
                        <th>特色</th>
                    </tr>
                </thead>
                <tbody>
                    <!-- 为每个推荐目的地生成一行 -->
                    <tr>
                        <td><strong>{目的地}</strong></td>
                        <td>{匹配度}%</td>
                        <td>{费用}</td>
                        <td>{车程}</td>
                        <td><span class="stars">{星级}</span></td>
                        <td>{特色}</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- 最终建议 -->
        <div class="recommendation">
            <h2>✅ 最终建议</h2>
            <p>{建议说明}</p>
            <p><strong style="font-size: 1.3em;">强烈推荐：{首选目的地}</strong></p>
            <p>{推荐亮点}</p>
        </div>

        <div class="footer">
            <p>基于 fly.ai 实时数据 · 生成时间：{当前日期}</p>
        </div>
    </div>
</body>
</html>
```

## 使用说明

1. 将上述模板中的 `{占位符}` 替换为实际数据
2. 根据推荐数量（Top 3）复制目的地卡片结构
3. 保存到 `~/team-outing-recommendation.html`
4. 执行 `open ~/team-outing-recommendation.html` 在浏览器中打开

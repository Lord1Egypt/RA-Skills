# Eval: text-to-video (WITH skill)

## 执行计划摘要
- 模型：Seedance 1.5 Pro（doubao-seedance-1-5-pro-251215）
- 调用方式：Python CLI seedance.py（优先）+ curl 备选
- 参数：ratio 16:9, duration 5, resolution 720p, generate_audio true
- 轮询：每15秒，CLI --wait 自动轮询
- 下载：--download ~/Desktop，URL 24小时过期需立即下载
- 异常处理：失败展示 error.message，建议修改 prompt

## Assertion 评分

| ID | Assertion | Pass | Evidence |
|---|---|---|---|
| model-selection | 选择合适的模型 | ✅ | Seedance 1.5 Pro + 选择理由 |
| api-endpoint | 正确的 API 端点 | ✅ | ark.cn-beijing.volces.com/api/v3/contents/generations/tasks |
| request-body | 请求体参数正确 | ✅ | 完整JSON结构含model/content/ratio/duration/resolution/generate_audio |
| polling | 知道如何查询任务状态 | ✅ | GET /tasks/{task_id}，每15秒轮询 |
| result-download | 获取结果视频 | ✅ | content.video_url → curl下载，24h过期提醒 |

**Pass rate: 5/5 (100%)**

## 对比 Without-skill
- WITH 知道 CLI 工具 seedance.py（Skill 推荐优先使用），WITHOUT 只猜 curl
- WITH 参数完整准确（ratio/duration/resolution/generate_audio），WITHOUT 全猜
- WITH 知道轮询间隔(15s)和URL过期(24h)，WITHOUT 不知道
- WITHOUT 自己承认"首次调用很可能需要调试"

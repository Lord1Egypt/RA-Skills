# Eval: text-to-video (WITHOUT skill)

## 执行计划摘要
- 模型选择：Seedance 1.5 Pro（从 TOOLS.md 获取）
- API：知道接入点ID和API Key（TOOLS.md），但请求体结构全靠猜
- 自己承认："API 调用参数是基于有限信息的推断"
- 不确定：JSON结构、duration字段名、轮询端点、prompt语言偏好

## Assertion 评分

| ID | Assertion | Pass | Evidence |
|---|---|---|---|
| model-selection | 选择合适的模型 | ✅ | 选了 Seedance 1.5 Pro |
| api-endpoint | 正确的 API 端点 | ⚠️ | 猜了个端点，不确定对不对 |
| request-body | 请求体参数正确 | ❌ | JSON结构完全是猜的 |
| polling | 知道如何查询任务状态 | ❌ | 推断为 /tasks/{task_id}，不确定 |
| result-download | 获取结果视频 | ❌ | 不知道具体下载方式 |

**Pass rate: 1.5/5 (30%)**

# 异步任务轮询

> ⚠️ **重要**：所有轮询接口均使用 **POST + body 传参**，不能用 GET + query string！
## 统一轮询模板

所有异步任务遵循同一模式：

```
提交接口（POST /submit/xxx）
  ↓ 返回 err_code=-1 获取 client_id（如有）
轮询接口（POST /query/xxx.result，body 传 `{"task_id": xxx}`）
  ↓
  state=1 → 处理中，继续轮询
  state=2 → 成功，返回结果
  state=3 → 失败
```

## 轮询参数说明

| 字段 | 说明 |
|------|------|
| `client_id` | 从提交响应 `data.client_id` 获取（部分接口用 `task_id` 代替） |
| `task_id` | server_task_id（贯穿全流程） |

## 统一轮询代码

```python
import time

def poll_task(hook_http_post, query_endpoint, poll_id, poll_type="client_id", timeout_s=180, interval_s=2):
    """
    统一轮询函数
    :param hook_http_post: client.post 方法
    :param query_endpoint: 查询接口路径
    :param poll_id: task_id (int) 或 client_id (str)
    :param poll_type: "task_id" 或 "client_id"
    :param timeout_s: 超时秒数
    :param interval_s: 轮询间隔秒数
    """
    deadline = time.time() + timeout_s
    attempt = 0

    while time.time() < deadline:
        attempt += 1
        if poll_type == "task_id":
            payload = {"task_id": poll_id}
        else:
            payload = {"client_id": poll_id}

        res, _ = hook_http_post(query_endpoint, payload)
        state = res.get("state")
        if isinstance(res.get("data"), dict):
            data_state = res["data"].get("state")
            if state is None:
                state = data_state

        print(f"[poll] attempt={attempt} state={state} cost=...")

        if state == 2:
            return {"ok": True, "data": res}
        if state == 3:
            return {"ok": False, "error": "任务失败", "data": res}

        time.sleep(interval_s)

    return {"ok": False, "error": f"轮询超时（>{timeout_s}秒）"}
```

## 各接口轮询参数速查

| 接口 | 轮询ID类型 | 查询接口 | 建议超时 |
|------|-----------|---------|---------|
| 需求分析 | `task_id` | `/api/hook/query/analyze.demand.result` | 180s |
| AI剪辑 | `task_id` | `/api/hook/query/intelligent.slice.engine.result` | 300s |
| AI解说 | `task_id` | `/api/hook/query/commentary.script.result` | 300s |
| 音色推荐 | `task_id` | `/api/hook/query/voice.recommend.result` | 120s |
| BGM推荐 | `task_id` | `/api/hook/query/bgm.recommend.result` | 120s |
| 火山OCR | `client_id` | `/api/aipkg/query/volcano.ocr.result` | 300s |
| 字幕TTS | `client_id` | `/api/aipkg/query/azure.tts.texts.result` | 300s |

## 状态字段位置

部分接口将 `state` 放在不同层级，兼容处理顺序：

```python
def read_state(res):
    # 优先取顶层 state
    st = res.get("state")
    if isinstance(st, int):
        return st
    # 再取 data.state
    data = res.get("data")
    if isinstance(data, dict):
        st = data.get("state")
        if isinstance(st, int):
            return st
        # 再取 data.result.state
        result = data.get("result")
        if isinstance(result, dict):
            return result.get("state")
    return None
```

## 注意事项

- **指数退避**：TTS 轮询建议用指数退避（3s → 6s → 12s...上限30s）
- **超时设置**：剪辑/解说类操作内容复杂，建议 300s 超时
- **结果保存**：轮询成功后建议将完整响应保存到 JSON 文件，便于后续排查
- **任务链**：各步骤间有依赖关系（需求分析→AI剪辑→AI解说→TTS），建议按顺序执行

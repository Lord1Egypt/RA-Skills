# 需求分析

用户输入视频和需求描述（plot），系统自动分析并输出剪辑参数。

## 接口

### 提交需求分析

```
POST /api/hook/submit/analyze.demand
```

### 查询需求分析结果

```
POST /api/hook/query/analyze.demand.result
```

**轮询参数**：body 传 `{"task_id": server_task_id}`

## 请求参数

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `task_id` | int | ✅ | server_task_id（创建任务返回） |
| `plot` | string | ✅ | 用户需求描述 |

**plot 示例**：
- "生成一段2分钟的影视解说"
- "剪辑成一个1分钟的搞笑片段，解说风格轻松幽默"
- "保留核心剧情，配音用磁性男声"

## 异步轮询

> ⚠️ **轮询必须用 POST + body 传参**，不能用 GET + query string！否则任务ID为空导致轮询失败。

1. 提交后**无返回数据**，直接进入异步处理
2. 轮询 `POST /api/hook/query/analyze.demand.result`，body 传 `{"task_id": xxx}`
3. `state=1` → 处理中，继续轮询
4. `state=2` → 成功，返回分析结果
5. `state=3` → 失败
6. **建议超时**：180秒，轮询间隔 2-3秒

## 轮询响应（state=2 成功）

```json
{
  "err_code": -1,
  "msg": "success",
  "state": 2,
  "data": {
    "state": 2,
    "result": {
      "clip_duration": "2分钟",
      "jianji_prompt": "保持剧情连贯，突出高潮部分",
      "jieshuo_prompt": "解说风格：悬疑紧张，节奏紧凑",
      "cut_story": "主线剧情摘要...",
      "short_lines": "关键台词..."
    }
  }
}
```

## 返回字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `clip_duration` | string | 目标剪辑时长（如 "2分钟"、"120秒"） |
| `jianji_prompt` | string | AI剪辑参考提示词 |
| `jieshuo_prompt` | string | AI解说参考提示词（语气/风格/节奏） |
| `cut_story` | string | 剧情主线摘要（用于后续步骤） |
| `short_lines` | string | 关键台词/短句（用于解说脚本） |

## 注意事项

- `plot` 越详细，分析结果越准确
- `clip_duration` 可能为空字符串，需在后续步骤中手动补全
- `jianji_prompt` 和 `jieshuo_prompt` 来自 AI 对 plot 的解析，是后续剪辑和解说的关键输入
- 如果 `state` 不是 2，需要检查 `err_code` 或重新轮询

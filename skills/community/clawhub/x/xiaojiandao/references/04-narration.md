# AI解说脚本生成

基于切片后的剧情（cut_story）和关键台词（short_lines），生成完整的解说旁白脚本。

## 接口

### 提交解说脚本生成

```
POST /api/hook/submit/commentary.script
```

### 查询解说脚本结果

```
POST /api/hook/query/commentary.script.result
```

> ⚠️ **轮询必须用 POST + body 传参**，不能用 GET + query string！

**轮询参数**：body 传 `{"task_id": server_task_id}`

## 请求参数

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `task_id` | int | ✅ | server_task_id |
| `cut_story` | string | ✅ | 切片后的剧情主线（来自AI剪辑结果） |
| `short_lines` | string | ✅ | 切片后的关键台词（来自AI剪辑结果） |

## 异步轮询

1. 提交后成功进入异步处理
2. 轮询查询结果
3. **建议超时**：300秒
4. **轮询间隔**：2-3秒

## 轮询响应（state=2 成功）

```json
{
  "err_code": -1,
  "state": 2,
  "data": {
    "state": 2,
    "result": {
      "script": "生成的解说脚本内容...",
      "shots": [
        {
          "narration": "第一段旁白...",
          "jieshuo": "相关描述..."
        },
        {
          "narration": "第二段旁白...",
          "jieshuo": "相关描述..."
        }
      ]
    }
  }
}
```

## 返回字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `script` | string | 完整解说脚本（SRT格式或纯文本） |
| `shots` | array | 分镜列表，每项含 `narration`（旁白）和 `jieshuo`（描述） |

## 旁白文本提取

从响应中提取旁白文本用于 TTS 合成：

```python
def extract_narrations(result):
    texts = []
    # 优先从 shots 数组提取
    shots = result.get("shots") or result.get("data", {}).get("shots", [])
    for shot in shots:
        for field in ("narration", "jieshuo", "text", "description"):
            val = shot.get(field)
            if isinstance(val, str) and val.strip():
                texts.append(val.strip())
                break
    if texts:
        return texts
    # 兜底：从 data.text 解析 SRT 条目
    raw = result.get("data", {}).get("text") or result.get("data", {}).get("script")
    if isinstance(raw, str) and raw.strip():
        # 按 SRT 时间戳条目解析
        entries = []
        for block in raw.strip().split("\n\n"):
            lines = block.strip().split("\n")
            if len(lines) >= 3:
                entries.append(lines[-1])  # 取每条文本内容
        return entries
    return texts
```

## 注意事项

- `cut_story` 和 `short_lines` 均来自 AI剪辑步骤的返回结果
- 解说脚本的质量取决于输入剧情和台词的完整性
- 返回的 `shots` 数组可用于分段 TTS 配音，实现精确时间轴对齐
- 如果解说脚本为空，检查 `cut_story` 和 `short_lines` 是否有实质内容

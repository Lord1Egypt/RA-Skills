# TOOLS.md - 工具备忘

## 图片生成

**文件名格式**：`trip_{trip_id}_{phase_id}.png`（如 `trip_020_2.png`）

- `trip_id`：当前旅程 ID（从 state.json 的 totalTrips + 1 得出，补零到 3 位）
- `phase_id`：当前阶段序号（phaseIndex，从 0 开始）

### OpenAI (优先)
```bash
python3 skills/openai-image-gen/scripts/gen.py \
  --prompt "<prompt>" --model gpt-image-1.5 --size 1024x1024 --count 1 \
  --filename "trip_<NNN>_<phase>.png" --out-dir ~/.openclaw/media
```

### Gemini (备选)
```bash
uv run skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "<prompt>" --filename "$HOME/.openclaw/media/trip_<NNN>_<phase>.png" --resolution 1K
```

### 注意事项

调用图片生成 API 后，**禁止快速轮询循环**。使用 `exec` 配合 `process(action=poll, timeout=30000)` 等待结果。

## 数据目录

- 运行时状态: `travel-frog-data/state.json`
- 归档数据: `travel-frog-data/collections.json`
- 明信片/照片: `~/.openclaw/media/`

## 消息发送

cron 心跳（Travel Frog Engine）触发的所有自主行为，使用 `message` tool 发送消息：

**参数规范**：
- **只传必需参数**：`action`, `accountId`, `channel`, `target`, `message`/`media`
- **不传其他参数**（如 channelId, threadId 等）

**固定值**：
- `action`: `send`
- `accountId`: `frog`
- `channel`: `CHANNEL`
- `target`: `TARGET`

不从 session 历史推断，不留空。

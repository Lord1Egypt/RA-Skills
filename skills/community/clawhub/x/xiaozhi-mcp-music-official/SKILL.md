---
name: xiaozhi-mcp-music-official
description: 按小智官方 MCP 接入方式，为小智增加在线音乐播放能力。适用于已经有小智 MCP 接入点（wss://api.xiaozhi.me/mcp/?token=...）并希望通过 MCP 工具实现搜歌、播放、暂停、继续、停止等在线音乐控制的场景。支持在线音乐 API 搜索、多源 fallback、调用本地播放器播放网络音频链接。 Official XiaoZhi MCP online music bridge for searching and playing online music through local players such as mpv.
---

# xiaozhi-mcp-music-official

[简体中文](#简体中文) | [English](#english)

---

## 简体中文

### 作用
这是一个最小可用的 **小智在线音乐 MCP 原型**，按小智官方 MCP 接入方式设计。

### 架构
```text
小智
→ MCP 接入点
→ mcp_pipe.py
→ music_mcp.py
→ 在线音乐 API
→ 本地播放器（mpv）
→ 返回结果给小智
```

### 提供的工具
- `play_music(query)`
- `play_music_index(query, n)`
- `stop_music()`
- `pause_music()`
- `resume_music()`
- `next_track()`
- `set_volume(level)`
- `music_info()`

### 当前方案说明
- 当前接入在线点歌 API
- 支持多源 fallback（优先 `kuwo`）
- 优先尝试从 API 返回中提取可播放直链
- 用 `mpv` 直接播放在线 URL
- 如果没有可播放链接，就把歌曲信息返回给小智

### 启动
```bash
pip install -r requirements.txt
cp .env.example .env
python3 mcp_pipe.py music_mcp.py
```

### 环境变量
- `MCP_ENDPOINT`：小智 MCP 接入点
- `MUSIC_API_KEY`：音乐 API key
- `MUSIC_SOURCE`：默认优先源，建议 `kuwo`
- `PLAYER_CMD`：播放器命令，默认 `mpv`

### 注意事项
- 如果服务器里没有安装 `mpv`，播放会失败，但搜歌和返回信息仍然可用。
- 当前是最小原型，后续还可以升级成播放列表、上一首/下一首、音量精控、多平台音乐源版本。

---

## English

### Purpose
This is a minimal working **XiaoZhi online music MCP prototype**, designed following XiaoZhi's official MCP integration style.

### Architecture
```text
XiaoZhi
→ MCP endpoint
→ mcp_pipe.py
→ music_mcp.py
→ online music API
→ local player (mpv)
→ return result to XiaoZhi
```

### Provided tools
- `play_music(query)`
- `play_music_index(query, n)`
- `stop_music()`
- `pause_music()`
- `resume_music()`
- `next_track()`
- `set_volume(level)`
- `music_info()`

### Current approach
- Uses an online music API
- Supports multi-source fallback (prefers `kuwo`)
- Tries to extract a playable direct link first
- Uses `mpv` to play network audio URLs
- If no playable URL is returned, it reports the matched song info back to XiaoZhi

### Start
```bash
pip install -r requirements.txt
cp .env.example .env
python3 mcp_pipe.py music_mcp.py
```

### Environment variables
- `MCP_ENDPOINT`: XiaoZhi MCP endpoint
- `MUSIC_API_KEY`: music API key
- `MUSIC_SOURCE`: preferred source, recommended `kuwo`
- `PLAYER_CMD`: player command, default `mpv`

### Notes
- If `mpv` is not installed on the server, playback will fail, but search/info retrieval will still work.
- This is a minimal prototype and can later be extended with playlists, previous/next track, fine-grained volume control, and richer music sources.

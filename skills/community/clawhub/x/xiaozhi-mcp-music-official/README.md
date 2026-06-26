# xiaozhi-mcp-music-official

[简体中文](#简体中文) | [English](#english)

---

## 简体中文

这是一个按小智官方 MCP 接入方式设计的**在线音乐播放 MCP 原型**。

### 主要能力
- 在线搜歌
- 多源 fallback
- 返回歌曲信息
- 如果拿到直链，则调用本地播放器直接播放
- 支持暂停、继续、停止等基本控制

### 依赖
```bash
pip install -r requirements.txt
```

### 配置
复制 `.env.example` 为 `.env`，填写：
- `MCP_ENDPOINT`
- `MUSIC_API_KEY`
- `MUSIC_SOURCE`
- `PLAYER_CMD`

### 启动
```bash
python3 mcp_pipe.py music_mcp.py
```

### 推荐播放器
建议安装：
```bash
apt-get install -y mpv
```

---

## English

This is an **online music playback MCP prototype** designed for XiaoZhi using the official MCP integration style.

### Main capabilities
- Search online music
- Multi-source fallback
- Return track info
- Play direct music URLs through a local player when available
- Support pause / resume / stop basic controls

### Install dependencies
```bash
pip install -r requirements.txt
```

### Configuration
Copy `.env.example` to `.env`, then fill in:
- `MCP_ENDPOINT`
- `MUSIC_API_KEY`
- `MUSIC_SOURCE`
- `PLAYER_CMD`

### Start
```bash
python3 mcp_pipe.py music_mcp.py
```

### Recommended player
Install `mpv` if you want actual playback:
```bash
apt-get install -y mpv
```

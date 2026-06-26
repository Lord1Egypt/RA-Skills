# MiniMax 媒体生成插件

> OpenClaw 媒体生成插件 - 图片、视频、TTS语音、音乐

## 功能特性

| 功能 | 模型 | 说明 |
|------|------|------|
| 🖼️ 图片生成 | `image-01` | 交互式输入描述 |
| 🎬 视频生成 | `MiniMax-Hailuo-2.3` / `2.3-Fast` | 可选模型 |
| 🔊 TTS语音 | `speech-2.8-hd` | 3种音色可选 |
| 🎵 音乐生成 | `music-2.6` / `music-2.5` | 可选模型 |

## 环境要求

- 已安装 OpenClaw 网关
- MiniMax API Key（在安装时配置）

## 安装步骤

### 1. 放置插件
```bash
cp -r rocky-minimax-media/ ~/.openclaw/skills/
```

### 2. 添加到 openclaw.json
在 `skills.entries` 中添加：
```json
"rocky-minimax-media": {
  "enabled": true
}
```

### 3. 运行安装脚本
```bash
cd ~/.openclaw/skills/rocky-minimax-media/scripts
./install.sh
```
→ 提示输入 MiniMax API Key
→ 自动写入 openclaw.json

### 4. 重启网关
```bash
openclaw gateway restart
```

## 配置说明

### 获取 MiniMax API Key
访问 https://platform.minimaxi.com/ 注册并获取 API Key

插件会从 `~/.openclaw/openclaw.json` 读取 API Key。安装时脚本会自动添加必要配置。

### 输出目录
```bash
# 默认: ~/.openclaw/output
MINIMAX_OUTPUT_DIR=/path/to/output ~/.openclaw/skills/rocky-minimax-media/scripts/minimax.sh image
```

## 使用方法

```bash
./minimax.sh test   # 测试所有API
./minimax.sh image  # 生成图片
./minimax.sh tts    # TTS语音合成
./minimax.sh video  # 视频生成
./minimax.sh music  # 音乐生成
```

## 交互选项

### 视频模型
```
1) MiniMax-Hailuo-2.3        - 文生视频，肢体动作/物理表现全面升级
2) MiniMax-Hailuo-2.3-Fast  - 图生视频，生成速度更快
```

### 音乐模型
```
1) music-2.6  - 最新版本，音质更好
2) music-2.5  - 经典版本
```

### TTS音色
```
1) male-qn-qingse   - 男声-青年-青涩
2) female-tianmei   - 女声-甜妹
3) female-yujie     - 女声-御姐
```

## API 接口

- **基础地址**: `https://api.minimaxi.com`
- **TTS**: `POST /v1/t2a_v2`
- **图片**: `POST /v1/image_generation`
- **视频**: `POST /v1/video_generation`
- **音乐**: `POST /v1/music_generation`

## 卸载

从 openclaw.json 的 `skills.entries` 中移除配置，并删除插件目录：
```bash
rm -rf ~/.openclaw/skills/rocky-minimax-media
```

然后重启网关。

---

**版本**: 1.3.0  
**OpenClaw**: https://openclaw.ai

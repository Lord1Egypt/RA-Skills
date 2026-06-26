# 命令模板

当你需要常见小度操作的精确 `mcporter` 命令格式时，使用这份文档。

## 小度智能屏 MCP

先列工具和 schema：

```bash
mcporter list xiaodu --schema
```

当前 live schema 已确认以下 5 个工具：

- `xiaodu.list_user_devices`
- `xiaodu.control_xiaodu`
- `xiaodu.xiaodu_speak`
- `xiaodu.push_resource_to_xiaodu`
- `xiaodu.xiaodu_take_photo`

注意：除了 `list_user_devices` 之外，其他 4 个工具都要求 `cuid` 和 `client_id`。用户只提供设备名时，先解析设备，再调用工具。

示例：

```bash
mcporter call xiaodu.list_user_devices --output json
mcporter call xiaodu.xiaodu_speak text="晚饭好了" cuid="..." client_id="..."
mcporter call xiaodu.control_xiaodu command="pause" cuid="..." client_id="..."
mcporter call xiaodu.xiaodu_take_photo cuid="..." client_id="..."
mcporter call xiaodu.push_resource_to_xiaodu resource_type="image" image_url="https://example.com/a.jpg" cuid="..." client_id="..."
```

`push_resource_to_xiaodu` 的资源类型与必填字段：

```bash
# 图片
mcporter call xiaodu.push_resource_to_xiaodu resource_type="image" image_url="https://example.com/a.jpg" cuid="..." client_id="..."

# 图片 + 背景音
mcporter call xiaodu.push_resource_to_xiaodu resource_type="image_with_bgm" image_url="https://example.com/a.jpg" bgm_url="https://example.com/a.mp3" cuid="..." client_id="..."

# 视频
mcporter call xiaodu.push_resource_to_xiaodu resource_type="video" video_url="https://example.com/a.mp4" cuid="..." client_id="..."

# 音频
mcporter call xiaodu.push_resource_to_xiaodu resource_type="audio" audio_url="https://example.com/a.mp3" cuid="..." client_id="..."
```

## 小度 IoT MCP

先探测 server：

```bash
mcporter list xiaodu-iot --schema
```

常见工具族：

- `xiaodu-iot.GET_ALL_DEVICES_WITH_STATUS`
- `xiaodu-iot.IOT_CONTROL_DEVICES`
- `xiaodu-iot.GET_ALL_SCENES`
- `xiaodu-iot.TRIGGER_SCENES`

注意：

- `applianceName` 是必填字段
- `roomName` 只是可选限定条件，不能只传房间名
- 如果你要做灯光、空调、窗帘、电视这类家电控制，优先走 `xiaodu-iot.IOT_CONTROL_DEVICES`，不要绕到 `xiaodu.control_xiaodu`

示例：

```bash
mcporter call xiaodu-iot.GET_ALL_DEVICES_WITH_STATUS --output json
mcporter call xiaodu-iot.GET_ALL_SCENES --output json
mcporter call xiaodu-iot.TRIGGER_SCENES sceneName="回家"
mcporter call xiaodu-iot.IOT_CONTROL_DEVICES action="turnOn" applianceName="射灯"
mcporter call xiaodu-iot.IOT_CONTROL_DEVICES action="turnOff" applianceName="射灯"
mcporter call xiaodu-iot.IOT_CONTROL_DEVICES action="set" applianceName="射灯" attribute="brightness" value="30"
mcporter call xiaodu-iot.IOT_CONTROL_DEVICES action="set" applianceName="三菱电机空调" roomName="客厅" attribute="temperature" value="26"
```

## 本 skill 自带脚本封装

当用户想要稳定的本地 helper，而不是每次手敲命令时，使用这些脚本：

```bash
bash scripts/configure_mcporter.sh --text "授权页复制的整段文本"
bash scripts/probe_xiaodu.sh --url "https://your-xiaodu-mcp-url" --name xiaodu
bash scripts/list_devices.sh --server xiaodu
bash scripts/refresh_devices.sh --speaker-server xiaodu --iot-server xiaodu-iot
bash scripts/speak.sh --text "晚饭好了" --device-name "小度智能屏2" --server xiaodu
bash scripts/control_xiaodu.sh --command "播放新闻" --device-name "小度智能屏3" --server xiaodu
bash scripts/take_photo.sh --device-name "小度智能屏2" --server xiaodu
bash scripts/push_resource.sh --resource-type image --image-url "https://example.com/a.jpg" --device-name "小度智能屏2" --server xiaodu
bash scripts/list_iot_devices.sh --server xiaodu-iot
bash scripts/list_scenes.sh --server xiaodu-iot
bash scripts/trigger_scene.sh --scene-name "回家" --server xiaodu-iot
bash scripts/control_iot.sh --action turnOn --device "射灯" --server xiaodu-iot
bash scripts/control_iot.sh --action set --device "射灯" --attribute brightness --value 30 --server xiaodu-iot
bash scripts/control_iot.sh --action set --device "三菱电机空调" --room "客厅" --attribute temperature --value 26 --server xiaodu-iot
```

## 稳定性规则

如果用户反馈 skill 路径或高层 agent 调用返回空结果，优先用直接的 `mcporter call` 重试同一个动作。实际接入里已经反复验证过：CLI 直调通常是更可靠的兜底路径。

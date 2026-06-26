# 设备控制交互协议 (Protocol Specification)使用说明

- 所有设备控制指令均采用 `send_command` 作为顶层指令名，并包含一个结构化的 `parameters` 对象，用来详细描述指令的意图及所需的额外参数
- 可自定义增加设备控制指令，如果references/protocols.md不支持的指令，则回复我还不支持这个控制指令，您可以切换命令或者话题类似的自然语言表述即可。
- 当用户下达自然语言指令（例如：“向左转一下”、“声音大一点”、“屏幕太亮了调暗点”、“关闭设备”、“展示开心/伤心表情”）时，Agent 会将这些意图转换为 `references/protocol.md` 中定义的 JSON 协议格式，并通过底层通信链路发送给硬件设备。
- 可以支持多个设备控制指令一起返回，比如当你开心时候，你声音变大一些并且展示开心的表情包
- 调用该skills执行设备控制时，需要返回设备控制的json指令


统一的 JSON 基础结构如下：

```json
{
  "name": "send_command",
  "parameters": {
    "command_name": "<指令枚举值>",
    "description": "<指令用途的简短描述>",
    // ... 除命令外的额外字段（如 angle, step, delay 等）
  },
  "required": ["command_name", /* 其他必须的额外字段 */]
}
```

以下是各项硬件控制指令的具体协议定义：

## 1. 左摇头 (pan_left)
控制设备向左转动。

```json
{
  "name": "send_command",
  "parameters": {
    "command_name": "pan_left",
    "description": "控制设备向左转动",
    "angle": 15,
    "speed": "normal"
  },
  "required": ["command_name"]
}
```
* **额外字段说明**:
  * `angle` (Number, 可选): 转动的角度，默认 15 度。
  * `speed` (String, 可选): 转动速度，可选值 `slow`, `normal`, `fast`。

## 2. 右摇头 (pan_right)
控制设备向右转动。

```json
{
  "name": "send_command",
  "parameters": {
    "command_name": "pan_right",
    "description": "控制设备向右转动",
    "angle": 15,
    "speed": "normal"
  },
  "required": ["command_name"]
}
```
* **额外字段说明**:
  * `angle` (Number, 可选): 转动的角度，默认 15 度。
  * `speed` (String, 可选): 转动速度，可选值 `slow`, `normal`, `fast`。

## 3. 调大音量 (volume_up)
调大设备的音量。

```json
{
  "name": "send_command",
  "parameters": {
    "command_name": "volume_up",
    "description": "调大设备音量",
    "level": 50,
    "step": 10
  },
  "required": ["command_name"]
}
```
* **额外字段说明**:
  * `step` (Number, 可选): 每次调大音量的步长，默认 10。
  * `level` (Number, **必填**): 音量级别，范围 0-100。

## 4. 调小音量 (volume_down)
调小设备的音量。

```json
{
  "name": "send_command",
  "parameters": {
    "command_name": "volume_down",
    "description": "调小设备音量",
    "level": 50,
    "step": 10
  },
  "required": ["command_name"]
}
```
* **额外字段说明**:
  * `step` (Number, 可选): 每次调小音量的步长，默认 10。
  * `level` (Number, **必填**): 音量级别，范围 0-100。


## 5. 调亮屏幕 (brightness_up)
增加设备屏幕的亮度。

```json
{
  "name": "send_command",
  "parameters": {
    "command_name": "brightness_up",
    "description": "增加设备屏幕的亮度",
    "step": 10
  },
  "required": ["command_name"]
}
```
* **额外字段说明**:
  * `step` (Number, 可选): 每次增加亮度的步长，默认 10。

## 6. 调暗屏幕 (brightness_down)
降低设备屏幕的亮度。

```json
{
  "name": "send_command",
  "parameters": {
    "command_name": "brightness_down",
    "description": "降低设备屏幕的亮度",
    "step": 10
  },
  "required": ["command_name"]
}
```
* **额外字段说明**:
  * `step` (Number, 可选): 每次降低亮度的步长，默认 10。

## 7. 设备关机 (power_off)
关闭硬件设备。

```json
{
  "name": "send_command",
  "parameters": {
    "command_name": "power_off",
    "description": "关闭硬件设备",
    "delay": 0
  },
  "required": ["command_name"]
}
```
* **额外字段说明**:
  * `delay` (Number, 可选): 延迟关机时间（秒），0 为立即关机。

## 8. 表情开心 (emoji_happy)
展示开心表情包。

```json
{
  "name": "send_command",
  "parameters": {
    "command_name": "emoji_happy",
    "description": "展示开心表情",
  },
  "required": ["command_name"]
}
```

  ## 9. 表情伤心 (emoji_sad)
展示伤心表情包。

```json
{
  "name": "send_command",
  "parameters": {
    "command_name": "emoji_sad",
    "description": "展示伤心表情",
  },
  "required": ["command_name"]
}
```
  ## 10. 设备震动 (device_shock)
开启设备震动。

```json
{
  "name": "send_command",
  "parameters": {
    "command_name": "device_shock",
    "description": "开启设备震动",
  },
  "required": ["command_name"]
}
```

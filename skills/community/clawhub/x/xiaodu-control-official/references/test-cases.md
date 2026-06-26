# 小度 MCP 测试用例

这份清单覆盖当前已经接通的 `xiaodu` 智能屏 MCP 与 `xiaodu-iot`，用于验证这套 skill 的主要公开能力。

## 测试前提

- 先确认 `xiaodu` 和 `xiaodu-iot` 都已可用。
- 确认手边那台设备的设备名、`cuid`、`client_id` 已能从设备列表拿到。
- 确认至少有一个可控的 IoT 设备名；如果需要按房间控制，也提前确认房间名。
- 确认至少有一个可触发的场景名。
- 建议固定用同一台设备做整轮测试，避免结果混淆。
- 如果通过聊天入口执行这些测试，默认要求 agent 优先调用本 skill 自带脚本，不要直接跳到底层工具。

## 建议测试顺序

1. 只读检查
2. 设备定位
3. 文本播报
4. 语音指令
5. 拍照
6. 资源推送
7. 异常与边界
8. IoT 设备与场景

## 一、只读检查

### TC-01 schema 可读
- 目标：确认当前 server 暴露的工具集合稳定。
- 命令：
  - `mcporter list xiaodu --schema`
- 预期：
  - 至少看到 `list_user_devices`、`control_xiaodu`、`xiaodu_speak`、`push_resource_to_xiaodu`、`xiaodu_take_photo`

### TC-02 设备列表可读
- 目标：确认 token 和设备查询正常。
- 命令：
  - `bash scripts/list_devices.sh --server xiaodu`
- 预期：
  - 返回在线设备列表
  - 每个设备包含 `device_name`、`cuid`、`client_id`

### TC-03 设备快照输出
- 目标：确认本地摘要脚本可用。
- 命令：
  - `bash scripts/refresh_devices.sh --speaker-server xiaodu`
- 预期：
  - 生成 `speaker-devices.json`
  - 生成 `device-summary.md`
  - 摘要里能看到设备名、CUID、Client ID、在线状态

## 二、设备定位

### TC-04 按精确设备名解析
- 目标：确认设备名可稳定解析为 `cuid/client_id`
- 命令：
  - `python3 scripts/device_resolver.py --server xiaodu --device-name "你的设备名" --format json`
- 预期：
  - 返回唯一设备
  - 含正确的 `cuid` 和 `client_id`

### TC-05 按部分设备名解析
- 目标：确认模糊匹配可用。
- 命令：
  - `python3 scripts/device_resolver.py --server xiaodu --device-name "智能屏2" --format json`
- 预期：
  - 如果唯一匹配，返回成功
  - 如果多台都命中，应明确报“设备名不唯一”

### TC-06 设备名不存在
- 目标：确认错误提示清晰。
- 命令：
  - `python3 scripts/device_resolver.py --server xiaodu --device-name "不存在的设备" --format json`
- 预期：
  - 返回失败
  - 明确提示“未找到设备”

## 三、文本播报

### TC-07 基础播报
- 目标：验证最基本的播报能力。
- 命令：
  - `bash scripts/speak.sh --server xiaodu --device-name "你的设备名" --text "测试成功"`
- 预期：
  - 设备发声
  - 无 schema 参数错误

### TC-08 中文长句播报
- 目标：验证正常中文句子播报。
- 命令：
  - `bash scripts/speak.sh --server xiaodu --device-name "你的设备名" --text "现在开始进行第二项测试，请确认你能完整听到这句话。"`
- 预期：
  - 文本完整播报

### TC-09 标点和数字播报
- 目标：验证中英文标点、数字混合文本。
- 命令：
  - `bash scripts/speak.sh --server xiaodu --device-name "你的设备名" --text "现在时间是 10:30，请在 5 分钟后提醒我开会。"`
- 预期：
  - 文本可自然播报

### TC-10 直传标识播报
- 目标：绕过设备名解析，验证底层参数调用。
- 命令：
  - `bash scripts/speak.sh --server xiaodu --cuid "你的cuid" --client-id "你的client_id" --text "这是直传参数测试"`
- 预期：
  - 设备正常播报

## 四、语音指令

### TC-11 简单控制指令
- 目标：验证 `control_xiaodu` 可用。
- 命令：
  - `bash scripts/control_xiaodu.sh --server xiaodu --device-name "你的设备名" --command "播放新闻"`
- 预期：
  - 设备执行语音指令
  - 返回结果里有明确响应

### TC-12 停止类指令
- 目标：验证短控制命令。
- 命令：
  - `bash scripts/control_xiaodu.sh --server xiaodu --device-name "你的设备名" --command "暂停"`
- 预期：
  - 设备执行暂停或给出明确响应

### TC-13 查询类指令
- 目标：验证问答类语音指令。
- 命令：
  - `bash scripts/control_xiaodu.sh --server xiaodu --device-name "你的设备名" --command "北京天气怎么样"`
- 预期：
  - 设备返回或播报天气相关响应

## 五、拍照

### TC-14 基础拍照
- 目标：验证摄像头调用。
- 命令：
  - `bash scripts/take_photo.sh --server xiaodu --device-name "你的设备名"`
- 预期：
  - 返回图像内容或图像结果结构

### TC-15 拍照保存输出
- 目标：验证本地落盘路径。
- 命令：
  - `bash scripts/take_photo.sh --server xiaodu --device-name "你的设备名" --out /tmp/xiaodu-photo.json`
- 预期：
  - 命令成功
  - 输出文件存在且非空

## 六、资源推送

### TC-16 推送图片
- 目标：验证 `image` 类型。
- 命令：
  - `bash scripts/push_resource.sh --server xiaodu --device-name "你的设备名" --resource-type image --image-url "可访问图片URL"`
- 预期：
  - 设备显示图片

### TC-17 推送图片+背景音
- 目标：验证 `image_with_bgm` 类型。
- 命令：
  - `bash scripts/push_resource.sh --server xiaodu --device-name "你的设备名" --resource-type image_with_bgm --image-url "可访问图片URL" --bgm-url "可访问音频URL"`
- 预期：
  - 设备显示图片并播放背景音

### TC-18 推送视频
- 目标：验证 `video` 类型。
- 命令：
  - `bash scripts/push_resource.sh --server xiaodu --device-name "你的设备名" --resource-type video --video-url "可访问视频URL"`
- 预期：
  - 设备开始播放视频

### TC-19 推送音频
- 目标：验证 `audio` 类型。
- 命令：
  - `bash scripts/push_resource.sh --server xiaodu --device-name "你的设备名" --resource-type audio --audio-url "可访问音频URL"`
- 预期：
  - 设备开始播放音频

### TC-20 自定义超时
- 目标：验证 `timeout` 参数。
- 命令：
  - `bash scripts/push_resource.sh --server xiaodu --device-name "你的设备名" --resource-type audio --audio-url "可访问音频URL" --timeout 120`
- 预期：
  - 请求成功
  - 无 timeout 参数报错

## 七、异常与边界

### TC-21 播报缺少设备参数
- 目标：确认脚本能拦截无效输入。
- 命令：
  - `bash scripts/speak.sh --server xiaodu --text "这条命令应该失败"`
- 预期：
  - 本地直接报错
  - 明确提示需要 `--device-name` 或 `--cuid + --client-id`

### TC-22 资源类型缺少必填 URL
- 目标：确认资源推送参数校验。
- 命令：
  - `bash scripts/push_resource.sh --server xiaodu --device-name "你的设备名" --resource-type video`
- 预期：
  - 本地直接报错
  - 明确提示 `video` 需要 `--video-url`

### TC-23 不支持的资源类型
- 目标：确认脚本拒绝无效类型。
- 命令：
  - `bash scripts/push_resource.sh --server xiaodu --device-name "你的设备名" --resource-type doc`
- 预期：
  - 本地直接报错
  - 明确提示不支持的资源类型

### TC-24 设备名歧义
- 目标：确认多匹配时不会误打到错误设备。
- 前提：
  - 至少有两个设备名包含同一关键词
- 命令：
  - `python3 scripts/device_resolver.py --server xiaodu --device-name "智能屏" --format json`
- 预期：
  - 返回失败
  - 列出所有命中的候选设备

### TC-25 直接 CLI 兜底
- 目标：确认脚本失败时底层 CLI 仍可手动验证。
- 命令：
  - `mcporter call xiaodu.xiaodu_speak text="直接CLI测试" cuid="..." client_id="..."`
- 预期：
  - 如果脚本层异常但 CLI 成功，说明问题在 skill/脚本层，不在 MCP 本身

## 八、IoT 设备与场景

### TC-26 IoT schema 可读
- 目标：确认 `xiaodu-iot` 暴露的工具集合稳定。
- 命令：
  - `mcporter list xiaodu-iot --schema`
- 预期：
  - 至少看到 `GET_ALL_DEVICES_WITH_STATUS`、`IOT_CONTROL_DEVICES`、`GET_ALL_SCENES`、`TRIGGER_SCENES`

### TC-27 IoT 设备列表可读
- 目标：确认 IoT 设备和状态查询正常。
- 命令：
  - `bash scripts/list_iot_devices.sh --server xiaodu-iot`
- 预期：
  - 返回设备列表
  - 每个设备至少包含设备名或可识别的家电标识

### TC-28 IoT 设备列表可落盘
- 目标：确认 IoT 只读结果可以稳定落盘复查。
- 命令：
  - `bash scripts/list_iot_devices.sh --server xiaodu-iot --out /tmp/xiaodu-iot-devices.json`
- 预期：
  - 命令成功
  - 输出文件存在且非空

### TC-29 IoT 基础开关控制
- 目标：验证 `IOT_CONTROL_DEVICES` 的基础动作可用。
- 命令：
  - `bash scripts/control_iot.sh --server xiaodu-iot --action turnOn --device "射灯"`
- 预期：
  - 对应设备状态发生变化，或返回明确成功结果

### TC-30 IoT 属性设置
- 目标：验证带属性和值的控制动作可用。
- 命令：
  - `bash scripts/control_iot.sh --server xiaodu-iot --action set --device "射灯" --attribute brightness --value 30`
- 预期：
  - 请求成功
  - 不出现缺少 `attribute/value` 的参数错误

### TC-31 场景列表可读
- 目标：确认可触发场景可枚举。
- 命令：
  - `bash scripts/list_scenes.sh --server xiaodu-iot`
- 预期：
  - 返回场景列表
  - 至少能识别出一个后续可触发的场景名

### TC-32 触发场景
- 目标：验证场景触发链路可用。
- 命令：
  - `bash scripts/trigger_scene.sh --server xiaodu-iot --scene-name "回家"`
- 预期：
  - 场景被触发，或返回明确成功结果

### TC-33 IoT 缺少设备名时应失败
- 目标：确认脚本会拦截缺少 `applianceName` 的无效输入。
- 命令：
  - `bash scripts/control_iot.sh --server xiaodu-iot --action turnOn`
- 预期：
  - 本地直接报错
  - 明确提示必须提供 `--device`

### TC-34 场景缺少名称时应失败
- 目标：确认脚本会拦截缺少场景名的无效输入。
- 命令：
  - `bash scripts/trigger_scene.sh --server xiaodu-iot`
- 预期：
  - 本地直接报错
  - 明确提示必须提供 `--scene-name`

## 推荐记录方式

每条测试至少记录这 4 项：
- 是否通过
- 实际输入
- 设备实际表现
- 返回内容或报错原文

## 当前未纳入本轮的内容

- 多设备并发测试
- 长时间稳定性压测
- 弱网或离线恢复测试

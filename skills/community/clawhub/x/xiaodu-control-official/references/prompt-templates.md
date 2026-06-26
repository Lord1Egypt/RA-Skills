# 中文提示词模板

当你在任意聊天渠道里使用这套 skill 时，优先使用下面这些中文模板。它们的目标是让模型少猜、多确认、优先走已经存在的 `mcporter` 配置。

## 首次安装推荐首问

第一次使用时，建议显式带上 `$xiaodu-control`。先把设备列出来，后面再直接说设备名和控制动作。

```text
用 $xiaodu-control 列出所有小度智能屏设备，并告诉我设备名称、在线状态、CUID 和 Client ID。
```

```text
用 $xiaodu-control 通过 xiaodu-iot 列出所有 IoT 设备，并告诉我每个设备的房间、类型和当前状态。
```

首次成功列出设备后，后续通常就可以直接说设备名和动作，例如“关闭射灯”或“让小度智能屏3播报测试成功”。如果是 IoT 控制，仍然建议把 `xiaodu-iot` 说清楚，减少误路由到智能屏语音链路的概率。

## 使用原则

- 设备多时，尽量明确写设备名，例如“小度智能屏2”。
- 如果还不知道设备名，先让它刷新设备列表，不要直接播报或拍照。
- 如果结果为空，要求它回退到直接的 `mcporter call` 或本 skill 脚本。
- 没有 `xiaodu-iot` 时，不要让它硬做 IoT 控制。
- 涉及“能否控制某类设备”或“请求是否越界”时，先按 [capability-boundaries.md](capability-boundaries.md) 判断，再执行或拒绝。
- 默认要求它优先使用本 skill 自带脚本，不要直接调用底层工具；只有在你明确要求 direct CLI 时才绕过脚本。
- 用户要控制灯、空调、窗帘、电视、插座等 IoT 设备时，明确要求它优先走 `xiaodu-iot`，不要走智能屏的 `control_xiaodu` 语音控制。

## 1. 检查连接和配置

适合首次接入或怀疑配置失效时使用。

```text
用 $xiaodu-control 检查 xiaodu 和 xiaodu-iot 是否已经配置、可鉴权，并告诉我下一步该做什么。
```

```text
用 $xiaodu-control 检查 xiaodu 的 schema，并确认当前有哪些可用工具。
```

```text
用 $xiaodu-control 检查当前是否能直接调用小度 MCP；如果 skill 层返回空结果，就回退到直接的 mcporter call。
```

## 2. 刷新设备列表

适合先确认设备名、设备状态和可用字段。

```text
用 $xiaodu-control 刷新我的小度设备列表，并用中文表格告诉我设备名、状态、CUID 和 Client ID。
```

```text
用 $xiaodu-control 刷新设备列表，并告诉我哪几台是智能屏。
```

```text
用 $xiaodu-control 刷新设备列表，然后帮我找出名字里像“闺蜜机”或“智能屏”的设备。
```

## 3. 文本播报

适合对指定设备做 TTS 播报。

```text
用 $xiaodu-control 让“小度智能屏2”播报：测试成功。
```

```text
用 $xiaodu-control 让“小度银杏12寸”播报：请到客厅集合。
```

```text
用 $xiaodu-control 对“小度添添闺蜜机Pro 4K Max”执行一次文本播报，如果需要 cuid 和 client_id，就从设备列表里取可用字段并告诉我你用了哪些参数。
```

## 4. 发送语音指令

适合让设备执行类似“播放新闻”“暂停”等语音命令。

```text
用 $xiaodu-control 给“小度智能屏3”发送语音指令：播放新闻。
```

```text
用 $xiaodu-control 给“小度智能屏2”发送语音指令：暂停。
```

```text
用 $xiaodu-control 给指定的小度智能屏发送一条语音指令；如果 schema 里的字段名和预期不一致，先告诉我再执行。
```

## 5. 拍照

适合验证拍照工具是否可用，或对指定设备抓图。

```text
用 $xiaodu-control 让“小度智能屏3”拍一张照，并告诉我返回结果。
```

```text
用 $xiaodu-control 测试“小度智能屏2”的拍照能力，如果失败请给出 schema 级别的原因。
```

## 6. 推送图片、视频或音频

适合把资源发到设备上播放或展示。

```text
用 $xiaodu-control 给“小度智能屏2”推送一张图片；如果还缺少资源 URL 或必要参数，先明确告诉我。
```

```text
用 $xiaodu-control 给“小度添添闺蜜机Pro 4K Max”推送一个音频资源，并说明需要我补哪些字段。
```

```text
用 $xiaodu-control 给“小度智能屏2”推送一段视频资源；如果缺少 video_url 或其他必填字段，先告诉我。
```

```text
用 $xiaodu-control 给“小度智能屏2”推送“图片+背景音”资源，并严格按 schema 校验参数是否齐全。
```

## 7. IoT 控制

只有在 `xiaodu-iot` 已配置时才适合使用。

```text
用 $xiaodu-control 检查 xiaodu-iot 是否可用；如果可用，就列出 IoT 设备并告诉我可以怎么控制。
```

```text
用 $xiaodu-control 通过 xiaodu-iot 把“射灯”打开。不要调用智能屏的 control_xiaodu，也不要让智能屏代说。
```

```text
用 $xiaodu-control 通过 xiaodu-iot 关闭“射灯”。执行前先确认工具名是不是 IOT_CONTROL_DEVICES，不要回退到智能屏语音控制。
```

```text
用 $xiaodu-control 通过 xiaodu-iot 把“射灯”亮度设置到 30。必须直接使用 IOT_CONTROL_DEVICES 或 control_iot.sh，不要调用智能屏的 control_xiaodu。
```

```text
用 $xiaodu-control 通过 xiaodu-iot 把“客厅”的“三菱电机空调”温度设置到 26 度。必须直接走 IoT 控制链路，不要走智能屏语音链路。
```

## 8. 排障

适合调用失败、字段不匹配或结果为空时使用。

```text
用 $xiaodu-control 排查为什么小度播报失败。先检查 schema，再给我最小可执行命令。
```

```text
用 $xiaodu-control 排查为什么 skill 调用返回空结果；如果 direct mcporter call 正常，请明确指出是 skill 层问题。
```

```text
用 $xiaodu-control 排查当前小度 MCP 配置。不要猜参数名，必须以 schema 为准。
```

## 9. 更稳的写法

如果你希望它少发挥、严格按步骤执行，可以直接用这类模板：

```text
用 $xiaodu-control 按这个顺序执行：1）检查 xiaodu schema；2）刷新设备列表；3）找到“小度智能屏2”；4）让它播报“测试成功”；5）每一步都先汇报结果再继续。
```

```text
用 $xiaodu-control 只做事实检查，不要脑补缺失参数。先告诉我 schema 里真实存在的工具和参数，再等我确认。
```

```text
用 $xiaodu-control 优先走直接 mcporter call，不要优先走高层封装；如果失败，再告诉我具体卡在哪一步。
```

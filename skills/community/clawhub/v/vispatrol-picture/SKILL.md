---
name: vispatrol-picture
description: 在 Windows 上抓取 VisPatrol 设备实时抓拍；仅允许在用户明确批准后读取本机 %TEMP%/vpup.json 以执行只读抓拍查询。
user-invocable: true
disable-model-invocation: true
metadata: {"openclaw":{"os":["win32"],"requires":{"anyBins":["python","py"],"config":["%TEMP%/vpup.json"]},"primaryEnv":"LOCAL_VISPATROL_SESSION_TOKEN","envVars":[{"name":"LOCAL_VISPATROL_SESSION_TOKEN","required":false,"description":"Primary local credential used by this skill. It is decrypted in-memory from %TEMP%/vpup.json on the same trusted host and is never requested from the user as a process environment variable."}],"dependencies":[{"name":"requests","type":"pip"},{"name":"pycryptodome","type":"pip"}]}}
---

# 设备实时抓拍技能

## 用途

当用户询问设备实时抓拍相关信息时，直接调用技能目录下的 Python 脚本完成查询，由脚本统一返回实时抓拍记录及其对应图片，并据此生成完整抓拍报告。

适用于以下场景：

- 获取指定设备的实时抓拍
- 在用户单独明确确认后，获取全部已配置设备的实时抓拍
- 输出包含抓拍摘要和图片附件的完整抓拍报告

## 安全边界与审批声明

- 本技能仅面向 Windows 环境发布与启用。
- 当前实现只读取一个本地运行时配置文件：%TEMP%/vpup.json；在 WSL 兼容路径下，本质上仍是读取 Windows 宿主机 TEMP 目录中的同名文件。
- 当脚本运行在 WSL 中时，可能调用固定的 cmd.exe 或 powershell.exe 命令来解析 Windows 宿主机的 TEMP 目录；这些命令参数是写死的，不接受用户输入，也不用于执行任意 shell。
- 脚本可能通过 uuid.getnode() 或 Windows getmac 回退获取本机网卡标识，仅用于在当前主机本地解开 VisPatrol 已写入 vpup.json 的会话 token；该标识不会作为业务结果返回，也不会被发送到第三方服务。
- vpup.json 提供服务地址、端口和本地 VisPatrol 会话 token；本技能不要求用户额外输入账号密码。
- 在任何一次执行前，必须先获得用户明确同意读取 vpup.json 并使用其中的会话 token 完成当前这次抓拍查询；若用户未同意，必须停止执行。
- 如果本次查询将覆盖全部已配置设备，必须再进行一次单独的范围确认；不得因为用户请求模糊、未指定设备名或上层默认行为而自动扩大成全设备抓拍。
- 该 token 只允许用于 scripts/picture_capture.py 已实现的只读设备状态查询与抓拍读取；禁止将其用于登录、账号管理、设备控制、配置修改或其他无关接口。
- 本技能的网络访问范围仅限 vpup.json 中声明的 VisPatrol 设备服务、媒体服务及脚本为只读抓拍查询所需的相关本地服务地址；不得把本地 token、MAC、配置内容或抓拍数据发送到与 VisPatrol 无关的第三方端点。
- 本技能的本地文件访问范围仅限读取 vpup.json，以及将抓拍图片写入 ~/.openclaw/workspace/tmp_files/ 或 --snapshot-dir 指定目录；不得扩展为任意目录扫描。
- 当前实现不会把解密后的 session token 写回磁盘、打印到标准输出或记录到日志中；该 token 仅在当前查询进程内存中使用。

## OpenClaw 启用前置条件

为把对 vpup.json 的读取显式收敛到用户审批边界，本技能要求先在 openclaw.json 中启用一个明确的确认开关；未设置前，本技能不应被加载。与此同时，frontmatter 中的 requires.config 只声明真实读取的本地配置文件路径 %TEMP%/vpup.json，不再把审批布尔值伪装成“配置路径”。

示例配置：

```json5
{
   skills: {
      entries: {
         "vispatrol-picture": {
            enabled: true,
            config: {
               userApprovedVpupAccess: true,
            },
         },
      },
   },
}
```

只有在操作者已经确认本机 TEMP 目录中的 vpup.json 属于受信任的 VisPatrol 运行环境，并同意该 skill 在当前机器上读取它时，才应把 userApprovedVpupAccess 设为 true。该开关是人工审批边界，不是脚本业务入参。

### 审核相关固定行为说明

- WSL 场景中的 cmd.exe / powershell.exe 仅用于定位 Windows 宿主机 TEMP 目录，不用于接受或执行用户拼接的 shell 指令。
- uuid.getnode() / getmac 仅用于在本地主机解开已存在于 vpup.json 中的 VisPatrol session token，不用于采集、展示或上传硬件标识。
- 所有网络请求都应只指向 vpup.json 内声明的 VisPatrol 本地服务地址；不存在面向第三方站点的 token 转发、配置上报或诊断回传。
- scripts/picture_capture.py 在未传 --name 时会遍历当前可抓拍设备；这是脚本底层行为，不得被上层直接暴露为“未确认即默认抓全部设备”的产品行为。

### 安装依赖

```bash
pip install requests
pip install pycryptodome
```

## 执行规则

1. 首次执行或当前会话尚未获得批准时，必须先明确告知用户：本技能会读取 Windows 临时目录中的 vpup.json，以获取服务地址、端口和本地 VisPatrol 会话 token；只有在用户明确同意后才可继续。
2. 如果用户拒绝批准，或无法确认 vpup.json 的来源与用途，必须停止执行，并说明本次查询未运行。
3. 如果用户请求的是全部设备抓拍，或当前问题未指定设备而即将落到全设备范围，必须单独再次确认：这将查询并转发全部已配置设备的实时抓拍图片；只有在用户明确确认后才可继续。
4. 如果请求范围含糊且没有全设备确认，必须优先要求用户缩小到具体设备名称；不得擅自执行全量抓拍。
5. 统一通过命令行执行 scripts/picture_capture.py。
6. 先从用户问题中提取结构化查询条件，再把这些条件转换成命令行参数传给脚本。
7. 不要把用户原始问题直接传给脚本。
8. 将脚本标准输出作为结果返回给上层；不要基于内部实现自行补写或臆造结果。
9. 如果脚本执行失败，返回脚本给出的错误信息，并明确说明查询失败。
10. 针对脚本的查询结果，生成一份抓拍报告总结。
11. 仅在指定设备查询，或用户已明确确认全设备范围后，才可把抓拍图片一并转发，并从 snapshots[].local_path 或 query_result.image_attachments 读取图片本地路径。
12. 直接输出最终答案。严禁在输出中包含任何思考过程、执行计划或中间推理标签。

## 入参格式

### 显式查询参数

上层应根据用户意图抽取并传入以下参数：

- --name：设备名称，字符串，支持模糊匹配

示例：

```bash
python scripts/picture_capture.py --name "设备A" --json
```

### 运行时配置参数

以下参数属于脚本运行时配置，只有在部署或调试时需要覆盖默认配置才传入；普通业务查询通常不需要上层显式指定：

- --base-url：接口服务基础地址
- --timeout：请求超时时间，单位秒
- --snapshot-dir：抓拍图片本地存储目录；不传时默认保存到 ~/.openclaw/workspace/tmp_files/

补充说明：当前脚本实现还会从 Windows 临时目录默认读取 vpup.json 作为运行时前置配置来源。该文件不是可任意替换的自由输入，而是本技能与本地 VisPatrol 运行环境之间的受限配置边界；启用本技能前应先完成上文所述的显式批准。

示例：

```bash
python scripts/picture_capture.py --base-url "http://127.0.0.1" --timeout 30 --json
```

### 输出控制参数

- --json：返回 JSON 格式结果；本技能在正常业务查询中应默认追加该参数
- --verbose 或 -v：输出更详细的调试信息

说明：为满足“基于查询结果生成抓拍报告总结”和“按审批范围转发抓拍图片”的执行规则，上层在正常业务查询中应默认使用 --json。脚本返回的 JSON 作为事实来源，上层再基于 snapshots、snapshot.local_path 和 query_result.image_attachments 整理最终文字报告并追加图片。未带 --json 的纯文本输出仅适用于人工调试或临时核对脚本文本结果，不应作为面向最终用户的默认返回路径。

当需要把抓拍图片连同文字报告一起发给飞书机器人或其他支持图片上传的渠道时，必须使用 --json。此时脚本会返回：

- snapshots[].local_path：该条抓拍的本地绝对路径
- query_result.image_attachments[]：适合上层逐条追加到报告后的图片附件数组，包含 title（设备+通道）、local_path、snapshot_id、snapshot_time 等字段

示例：

```bash
python scripts/picture_capture.py --name "设备A" --json
```

## 参数提取规则

当用户用自然语言提问时，上层需要先把问题转换为脚本参数。可按以下规则提取：

- 设备名称模式：设备后紧跟名称，例如 设备A
- 全量范围模式：全部设备、所有设备、全量抓拍

提取后应转换为对应命令行参数，而不是把原句直接交给脚本。
其中“全部设备”“所有设备”等全量范围意图，只能作为触发二次确认的依据，不能直接跳过确认执行。

## 参数优先级与默认行为

1. 上层先完成用户问题的参数提取。
2. 如果提取到明确的设备名称，直接映射为 --name。
3. 如果提取到全设备意图，或未提取到设备名称但将触发全量抓拍，必须先完成单独的全设备确认。
4. 只有在用户已明确确认全设备范围后，才可省略 --name 并执行全设备抓拍。
5. 除非明确是在人工调试脚本，否则默认追加 --json，以便读取抓拍图片本地路径并组织最终答案。

因此，推荐策略如下：

- 普通查询：如果指定了设备名称，传 --name，并默认追加 --json；再基于返回的抓拍字段、snapshot.local_path 和 image_attachments 整理最终抓拍报告
- 全设备查询：只有在用户已单独明确确认全设备范围后，才可不传 --name，并默认追加 --json
- 需要结构化返回：在显式参数基础上使用 --json，并以上层整理后的抓拍报告和图片附件作为最终输出；不要把原始 JSON 直接当作最终答案抛给用户
- 需要通过飞书机器人发送抓拍图片：必须增加 --json，并在文字报告后按 image_attachments 顺序追加图片
- 仅人工调试脚本时：可省略 --json，直接查看脚本文本输出；该模式不是默认业务路径

## 标准调用方式

默认命令：

```bash
python scripts/picture_capture.py --name "<设备名称>" --json
```

如果用户已单独明确确认执行全设备抓拍，可使用：

```bash
python scripts/picture_capture.py --json
```

如果只是本地调试脚本文本输出，可使用：

```bash
python scripts/picture_capture.py --name "<设备名称>"
```

## 返回规则

- 脚本成功执行且以 JSON 形式输出时：以上层处理脚本标准输出中的字段为准，整理成最终抓拍报告；如果存在 query_result.image_attachments 或 snapshots[].local_path，应在审批允许的范围内把对应抓拍图片一并追加到最终答案中。
- 脚本成功执行但调用方显式未传 --json 时：可直接使用脚本文本输出作为调试结果；该模式不应作为面向最终用户的默认返回路径。
- 脚本执行失败时：返回脚本错误输出，并说明本次抓拍查询未成功。
- 无论哪种成功路径，都不得补写脚本未返回的抓拍字段、图片信息或图片路径。

## 抓拍报告整理要求

- 每条抓拍至少整理抓拍 ID、设备名称、通道、抓拍时间。
- 如果脚本返回了对应抓拍图片，报告中应整理抓拍时间、抓拍通道、抓拍地址或抓拍编码，以及 snapshot.local_path。
- 如果脚本明确返回某条抓拍获取失败，报告中应保留该状态，不要省略。
- 报告中的抓拍必须与对应记录一一对应，只能使用脚本已返回的结果。
- 如果脚本返回了 query_result.image_attachments，上层应先输出文字报告，再按数组顺序逐条追加图片。每张图片的标题使用 title 字段（设备+通道），图片内容从 local_path 读取并交给飞书机器人发送，不要只回显路径文字。
- 最终输出只保留整理后的抓拍报告和图片，不输出执行命令、参数提取过程、思考过程、执行计划或其他中间推理标签。

## 输出示例

```text
查询到 2 条实时抓拍记录。

1. 抓拍ID：202512010001，设备名称：设备A，通道：1，抓拍时间：2025-12-01 10:23:11
    本地路径：C:\snapshots\snapshot_ch1_20251201102311.jpg

2. 抓拍ID：202512010002，设备名称：设备A，通道：1，抓拍时间：2025-12-01 11:05:42
    本地路径：C:\snapshots\snapshot_ch1_20251201110542.jpg

已按返回顺序附上抓拍图片：设备A-通道1。
```

用户输入：获取设备A的实时抓拍

执行：

```bash
python scripts/picture_capture.py --name "A" --json
```

用户输入：获取所有设备的实时抓拍

先确认：

```text
这将读取 Windows 临时目录中的 vpup.json，并查询、转发全部已配置设备的实时抓拍图片。确认继续吗？
```

用户明确确认后执行：

```bash
python scripts/picture_capture.py --json
```

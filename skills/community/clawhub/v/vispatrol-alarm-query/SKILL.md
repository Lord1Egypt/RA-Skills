---
name: vispatrol-alarm-query
description: 在 Windows 上查询 VisPatrol 报警与抓拍；仅允许在用户明确批准后读取本机 %TEMP%/vpup.json 以执行只读报警与抓拍查询。
user-invocable: true
disable-model-invocation: true
metadata: {"openclaw":{"os":["win32"],"requires":{"anyBins":["python","py"],"config":["%TEMP%/vpup.json"]},"primaryEnv":"LOCAL_VISPATROL_SESSION_TOKEN","envVars":[{"name":"LOCAL_VISPATROL_SESSION_TOKEN","required":false,"description":"Primary local credential used by this skill. It is decrypted in-memory from %TEMP%/vpup.json on the same trusted host and is never requested from the user as a process environment variable."}],"dependencies":[{"name":"requests","type":"pip"},{"name":"cryptography","type":"pip"},{"name":"pycryptodome","type":"pip"}]}}
---

# 设备报警信息查询技能

## 用途

当用户询问设备报警相关信息时，直接调用技能目录下的 Python 脚本完成查询，由脚本统一返回报警记录及其对应的最新报警抓拍，并据此生成完整告警报告。

适用于以下场景：

- 查询今天、昨天或指定时间范围内的报警
- 查询某类报警、某个设备的报警或某个报警 ID
- 查询分页结果或最近若干条报警记录
- 输出包含报警抓拍摘要的完整告警报告

## 安全边界与审批声明

- 本技能仅面向 Windows 环境发布与启用。
- 当前实现只读取一个本地运行时配置文件：%TEMP%/vpup.json；在 WSL 兼容路径下，本质上仍是读取 Windows 宿主机 TEMP 目录中的同名文件。
- 当脚本运行在 WSL 中时，可能调用固定的 cmd.exe 或 powershell.exe 命令来解析 Windows 宿主机的 TEMP 目录；这些命令参数是写死的，不接受用户输入，也不用于执行任意 shell。
- 脚本可能通过 uuid.getnode() 或 Windows getmac 回退获取本机网卡标识，仅用于在当前主机本地解开 VisPatrol 已写入 vpup.json 的会话 token；该标识不会作为业务结果返回，也不会被发送到第三方服务。
- vpup.json 提供服务地址、端口和本地 VisPatrol 会话 token；本技能不要求用户额外输入账号密码。
- 在任何一次执行前，必须先获得用户明确同意读取 vpup.json 并使用其中的会话 token 完成当前这次报警/抓拍查询；若用户未同意，必须停止执行。
- 该 token 只允许用于 scripts/alarm_query.py 已实现的只读报警查询和抓拍读取；禁止将其用于登录、账号管理、设备控制、配置修改或其他无关接口。
- 本技能的网络访问范围仅限 vpup.json 中声明的 VisPatrol 报警服务与媒体服务地址；不得把本地 token、MAC、配置内容或抓拍数据发送到与 VisPatrol 无关的第三方端点。
- 本技能的本地文件访问范围仅限读取 vpup.json，以及将抓拍图片写入 ~/.openclaw/workspace/tmp_files/ 或 --snapshot-dir 指定目录；不得扩展为任意目录扫描。
- 当前实现不会把解密后的 session token 写回磁盘、打印到标准输出或记录到日志中；该 token 仅在当前查询进程内存中使用。

## OpenClaw 启用前置条件

为把对 vpup.json 的读取显式收敛到用户审批边界，本技能要求先在 openclaw.json 中启用一个明确的确认开关；未设置前，本技能不应被加载。与此同时，frontmatter 中的 requires.config 只声明真实读取的本地配置文件路径 %TEMP%/vpup.json，不再把审批布尔值伪装成“配置路径”。

示例配置：

```json5
{
  skills: {
    entries: {
      "vispatrol-alarm-query": {
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
- 所有网络请求都应只指向 vpup.json 内声明的 VisPatrol 服务地址；不存在面向第三方站点的 token 转发、配置上报或诊断回传。

### 安装依赖

```bash
pip install requests
pip install cryptography
pip install pycryptodome
```

## 执行规则

1. 首次执行或当前会话尚未获得批准时，必须先明确告知用户：本技能会读取 Windows 临时目录中的 vpup.json，以获取服务地址、端口和本地 VisPatrol 会话 token；只有在用户明确同意后才可继续。
2. 如果用户拒绝批准，或无法确认 vpup.json 的来源与用途，必须停止执行，并说明本次查询未运行。
3. 统一通过命令行执行 scripts/alarm_query.py。
4. 先从用户问题中提取结构化查询条件，再把这些条件转换成命令行参数传给脚本。
5. 不要把用户原始问题直接传给脚本。
6. 将脚本标准输出作为结果返回给上层；不要基于内部实现自行补写或臆造结果。
7. 如果脚本执行失败，返回脚本给出的错误信息，并明确说明查询失败。
8. 针对脚本的查询结果，生成一份报警报告总结。
9. 默认把抓拍图片一并转发，并从 alarms[].snapshot.local_path 或 query_result.image_attachments 读取图片本地路径。
10. 直接输出最终答案。严禁在输出中包含任何思考过程、执行计划或中间推理标签。

## 入参格式

### 显式查询参数

上层应根据用户意图抽取并传入以下参数：

- --start：开始时间，格式必须为 YYYY-MM-DD HH:MM:SS
- --end：结束时间，格式必须为 YYYY-MM-DD HH:MM:SS
- --type：报警类型代码，整型
- --name：设备名称，字符串，支持模糊匹配
- --alarmid：报警 ID，字符串
- --pagesize：每页记录数，整型
- --pageno：分页页号，从 0 开始；例如第 1 页传 0，第 2 页传 1

示例：

```bash
python scripts/alarm_query.py --start "2025-12-01 09:00:00" --end "2025-12-01 12:00:00" --type 120001 --name "设备A" --json
```

### 运行时配置参数

以下参数属于脚本运行时配置，只有在部署或调试时需要覆盖默认配置才传入；普通业务查询通常不需要上层显式指定：

- --base-url：接口服务基础地址
- --timeout：请求超时时间，单位秒
- --snapshot-dir：抓拍图片本地存储目录；不传时默认保存到 ~/.openclaw/workspace/tmp_files/

补充说明：当前脚本实现还会从 Windows 临时目录默认读取 vpup.json 作为运行时前置配置来源。该文件不是可任意替换的自由输入，而是本技能与本地 VisPatrol 运行环境之间的受限配置边界；启用本技能前应先完成上文所述的显式批准。

示例：

```bash
python scripts/alarm_query.py --start "2025-12-01 00:00:00" --end "2025-12-01 23:59:59" --base-url "http://127.0.0.1" --timeout 30 --json
```

### 输出控制参数

- --json：返回 JSON 格式结果；本技能在正常业务查询中应默认追加该参数
- --verbose 或 -v：输出更详细的调试信息

说明：为满足“基于查询结果生成报警报告总结”和“默认把抓拍图片一并转发”的执行规则，上层在正常业务查询中应默认使用 --json。脚本返回的 JSON 作为事实来源，上层再基于 alarms、snapshot.local_path 和 query_result.image_attachments 整理最终文字报告并追加图片。未带 --json 的纯文本输出仅适用于人工调试或临时核对脚本文本结果，不应作为面向最终用户的默认返回路径。

当需要把抓拍图片连同文字报告一起发给飞书机器人或其他支持图片上传的渠道时，必须使用 --json。此时脚本会返回：

- alarms[].snapshot.local_path：该条报警匹配抓拍图的本地绝对路径
- query_result.image_attachments[]：适合上层逐条追加到报告后的图片附件数组，包含 title（设备+通道）、local_path、alarm_id、snapshot_time 等字段

示例：

```bash
python scripts/alarm_query.py --start "2025-12-01 00:00:00" --end "2025-12-01 23:59:59" --type 120001 --json
```

## 参数提取规则

当用户用自然语言提问时，上层需要先把问题转换为脚本参数。可按以下规则提取：

- 时间关键词：今天、昨天
- 日期字符串：YYYY-MM-DD
- 报警类型名称：区域入侵、绊线入侵、目标识别、动态检测、火点报警、报警输入、烟雾报警
- 设备名称模式：设备后紧跟名称，例如 设备A
- 报警 ID 模式：报警ID 12345 或 ID 12345
- 分页模式：第 N 页
- 条数模式：N 条

提取后应转换为对应命令行参数，而不是把原句直接交给脚本。
其中“今天”“昨天”等相对时间，需要先换算成实际日期时间，再传给 --start 和 --end。

## 参数优先级与默认行为

1. 上层先完成用户问题的参数提取。
2. 提取出的结构化条件直接映射为脚本显式参数。
3. 如果未提供开始时间和结束时间，可按业务需要补成当天 00:00:00 到当前时间后再传入脚本。
4. 如果未提供其他筛选条件，脚本会按默认分页参数执行查询。
5. 除非明确是在人工调试脚本，否则默认追加 --json，以便读取抓拍图片本地路径并组织最终答案。

因此，推荐策略如下：

- 普通查询：提取时间范围后，至少传 --start 和 --end，并默认追加 --json；再基于返回的报警字段、snapshot.local_path 和 image_attachments 整理最终告警报告
- 需要结构化返回：在显式参数基础上使用 --json，并以上层整理后的告警报告和图片附件作为最终输出；不要把原始 JSON 直接当作最终答案抛给用户
- 需要通过飞书机器人发送抓拍图片：必须增加 --json，并在文字报告后按 image_attachments 顺序追加图片
- 需要指定类型、设备、报警 ID 或分页：追加对应显式参数
- 仅人工调试脚本时：可省略 --json，直接查看脚本文本输出；该模式不是默认业务路径

## 标准调用方式

默认命令：

```bash
python scripts/alarm_query.py --start "<开始时间>" --end "<结束时间>" --json
```

如果只是本地调试脚本文本输出，可使用：

```bash
python scripts/alarm_query.py --start "<开始时间>" --end "<结束时间>"
```

如果需要增加筛选条件，追加对应参数，例如：

```bash
python scripts/alarm_query.py --start "2025-12-01 00:00:00" --end "2025-12-01 23:59:59" --pagesize 20 --type 110002 --json
```

## 返回规则

- 脚本成功执行且以 JSON 形式输出时：以上层处理脚本标准输出中的字段为准，整理成最终告警报告；如果存在 query_result.image_attachments 或 alarms[].snapshot.local_path，应默认把对应抓拍图片一并追加到最终答案中。
- 脚本成功执行但调用方显式未传 --json 时：可直接使用脚本文本输出作为调试结果；该模式不应作为面向最终用户的默认返回路径。
- 脚本执行失败时：返回脚本错误输出，并说明本次报警查询未成功。
- 无论哪种成功路径，都不得补写脚本未返回的报警字段、抓拍信息或图片路径。

## 告警报告整理要求

- 每条报警至少整理报警 ID、设备名称、通道、报警详情、报警时间。
- 如果脚本返回了对应抓拍，报告中应整理抓拍时间、抓拍通道、抓拍地址或抓拍编码，以及 snapshot.local_path。
- 如果脚本明确返回某条报警未匹配到抓拍或抓拍获取失败，报告中应保留该状态，不要省略。
- 报告中的抓拍必须与对应报警一一对应，只能使用脚本已返回的同设备同通道最新抓拍结果。
- 如果脚本返回了 query_result.image_attachments，上层应先输出文字报告，再按数组顺序逐条追加图片。每张图片的标题使用 title 字段（设备+通道），图片内容从 local_path 读取并交给飞书机器人发送，不要只回显路径文字。
- 最终输出只保留整理后的告警报告和图片，不输出执行命令、参数提取过程、思考过程、执行计划或其他中间推理标签。

## 输出示例
```text
查询到 2 条报警，已按设备和通道汇总。

设备A / 通道1：共 2 条报警
1. 报警ID：202512010001，报警详情：烟雾报警，报警时间：2025-12-01 10:23:11
  抓拍：2025-12-01 10:23:08，路径 C:\snapshots\deviceA_ch1_20251201102308.jpg
2. 报警ID：202512010002，报警详情：烟雾报警，报警时间：2025-12-01 11:05:42
  抓拍：未匹配到同设备同通道抓拍

已按返回顺序附上抓拍图片：设备A-通道1。
```

用户输入：查询今天的所有报警信息

执行：

```bash
python scripts/alarm_query.py --start "<今天 00:00:00>" --end "<今天当前或 23:59:59>" --json
```

用户输入：查看昨天设备 A 的烟雾报警

执行：

```bash
python scripts/alarm_query.py --start "<昨天 00:00:00>" --end "<昨天 23:59:59>" --name "A" --type 120005 --json
```

用户输入：按结构化结果返回 2025-12-01 09:00 到 12:00 的报警

执行：

```bash
python scripts/alarm_query.py --start "2025-12-01 09:00:00" --end "2025-12-01 12:00:00" --json
```

用户输入：查询 2025-12-01 09:00:00 到 2025-12-01 12:00:00 的区域入侵报警，并强制返回 20 条

执行：

```bash
python scripts/alarm_query.py --start "2025-12-01 09:00:00" --end "2025-12-01 12:00:00" --type 120001 --pagesize 20 --json
```

## 报警类型代码

- 区域入侵：120001
- 绊线入侵：120002
- 目标识别：120003
- 动态检测：120004
- 火点报警：110002
- 报警输入：120006
- 烟雾报警：120005

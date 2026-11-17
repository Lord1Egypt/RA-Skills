# 常见问题与排障索引（FAQ）

> 中文版，供希望**自行排障**的用户使用 · 本系统为 Agent 可读设计，故障优先由 Agent 依据 [SKILL.md 决策表](../SKILL.md#decision-table--error--status--action) 自动恢复，本文是人工自助的备用入口 · English（Agent 默认加载）: [FAQ.md](FAQ.md) · 修改任一份时请同步另一份。

## 常见问题（FAQ）

### 安装与启动

**问：`"<MCP_PYTHON>" -m pip install -r requirements.txt` 很慢或失败。**
答：请使用 64 位 Python 3.10+ 解释器——`<MCP_PYTHON>` 为启动 MCP 的解释器绝对路径；始终用 `-m pip` 绑定该解释器安装（裸 `pip` 可能属于其他 Python 环境）。国内网络可改用镜像源安装（`"<MCP_PYTHON>" -m pip install -r requirements.txt -i <镜像地址>`）——全部依赖（含原生库 camera-proto）都是普通 PyPI 包，镜像同样适用。

**问：调用摄像头工具报「camera-proto package is not installed」（未安装 camera-proto 依赖）。**
答：依赖未安装到启动 MCP 的解释器里。用同一解释器运行 `"<MCP_PYTHON>" -m pip install -r requirements.txt`（工具报错中会打印带实际路径的该命令），然后重试刚才的工具即可——无需重启 MCP Server（加载器会在下次调用时自动重试，安装即生效）。依赖安装在配置阶段完成，MCP 启动本身不下载任何资源。

**问：调用摄像头工具报「Failed to load camera protocol library」（协议库加载失败）/「Camera protocol library ABI version mismatch」（ABI 版本不匹配）/「Camera protocol library not found」（未找到摄像头协议库）。**
答：加载失败通常是系统/解释器架构或原生依赖问题；ABI 不匹配是 camera-proto 版本与门面不配对；未找到协议库则是包文件不完整。先用启动 MCP 的解释器运行 `"<MCP_PYTHON>" -m pip install -r requirements.txt` 校验固定版本依赖，再重试工具；加载失败仍复现时检查是否为 64 位解释器与对应系统架构。

**问：工具列表里完全没有摄像头工具。**
答：MCP Server 尚未注册。按 [SKILL.md](../SKILL.md#installation) 的三步 Installation 配置；禁止退回直接 `import scripts.toolkit` 或自写脚本的方式。

**问：Server 启动即退出，所有工具不可用（exit code 70）。**
答：70 表示 stdio 会话结束后的正常退出（宿主关闭了会话），重启即可。锁冲突不再导致 Server 退出——实例锁改为首次调用摄像头工具时懒获取，端口占用冲突会以 `instance_lock_conflict` 工具错误返回（见下条）。若退出原因不明，先读启动 stderr 定位。详见 [SKILL.md Gotchas](../SKILL.md#gotchas)。

**问：工具突然不可用 / 提示「另一个会话正在使用摄像头」。**
答：单实例设计：同一时间只有一个会话持有摄像头，新会话会自动接管——旧会话的连接会被断开。在你想使用的会话里直接重试摄像头操作，即可同样把它夺回——不是故障。若收到 `instance_lock_conflict`，说明锁端口被非本技能程序占用或接管失败：`error_message` 会给出占用进程 PID，关闭后重试。

### 发现与连接

**问：`search_devices()` 搜不到任何设备。**
答：确认摄像头与主机在同一局域网且设备在线。发现协议（SK 私有 / JCP / WS-Discovery）由工具自动选择，无需人工干预。USB 摄像头不支持自动发现（需在 config.yaml 手动配置，且不支持云台与设备管理）。

**问：昨天还能连的摄像头今天连不上。**
答：大概率是 DHCP 续租导致 IP 变化，config.yaml 中缓存的 IP 已失效。先调用一次 `search_devices()` 刷新注册表再重试；不要对旧 IP 反复重试。

**问：工具一直要求输密码（`needs_password`）。**
答：缓存凭据已失效且云端重授权也失败、云服务不可达，或设备无 SN 无法发起云授权。请用户输入设备密码，然后 `connect_device(camera_name, password=用户输入)`。设备密码印在摄像头机身标签上。

**问：云授权弹窗一直没人确认。**
答：`connect_device` 会阻塞等待厂商手机 APP 上的确认操作。请用户在 APP 上点击确认后，调用会自行完成。

**问：第三方 ONVIF 摄像头（O 类）能用哪些功能？**
答：仅支持密码直连（无云授权、无 SK/JCP SN）。经 ONVIF 的 RTSP 流与云台可用；SK 私有协议专属能力（事件、补光、图像参数、追踪）会返回 `UNSUPPORTED_PROTOCOL`——这是设备类别的固有限制，不是故障。

**问：连接被拒，返回 `no_sn`。**
答：两种可能：S/J 类设备丢失 SN（先 `search_devices()` 再重试），或纯 RTSP 设备未通过 ONVIF 准入（终态，不要重试或绕过）。禁止通过手动 `register_camera` 或手改 config.yaml 绕过该门槛。

### 流 · 截图 · 录像

**问：WebRTC 预览黑屏或卡顿。**
答：浏览器可能不支持 H265 WebRTC（如 Edge）。改用 `start_webrtc_stream(video_codec="h264")` 重试——会切换设备编码器（短暂打断其 RTSP 会话）并重启预览。

**问：提示未检测到 go2rtc。**
答：go2rtc 不随技能分发。从 go2rtc 的 GitHub Releases（作者 AlexxIT；Windows 为 zip 包）下载对应平台的二进制，放到技能根目录或加入 `PATH`，然后重试 `start_webrtc_stream()`。详见 [SKILL.md Phase 3](../SKILL.md#phase-3--stream--capture)。

**问：截图 / 录像保存在哪里？**
答：默认在 `snapshots/` 与 `video/`（事件存于 `events/`）。若自定义 `save_path`，请用纯 ASCII 路径——Windows 下中文路径会导致 `cv2.imwrite()` 静默失败。

**问：录像停不下来。**
答：录像必须以 `toggle_recording(action="start", duration=<秒>)` 启动，由 Server 到时自动停止。「先启动、等一会再调 stop」的方式会淹没停止调用，导致录像无限持续并占用设备 RTSP 会话。

**问：流/截图返回 `error_code="timeout"`。**
答：用更大的 `timeout_seconds`（上限 120）重试一次；仍失败则检查设备是否在线。

**问：截图/录像写入失败（文件未创建或为空）。**
答：可能原因：磁盘空间不足、`save_path` 无效（不存在或无写权限；Windows 下含中文等非 ASCII 字符的路径会使 `cv2.imwrite()` 静默失败）、或录像时长太短未产生数据。检查实际保存目录所在磁盘的剩余空间、路径和权限，修复后重试；录像报错时还应查看视频旁的 ffmpeg `.log` 文件。

### 云台 · 事件 · 数据

**问：云台 `degrees` 模式不可用。**
答：J/O 类的 ONVIF 后端仅支持「速度 + 时长」方式，请改用 `duration_seconds`。

**问：没有事件 / 补光 / 图像参数 / 追踪功能。**
答：这些是 S 类专属能力，J/O 类会返回 `UNSUPPORTED_PROTOCOL` 并附原因——请告知用户这是设备类别限制，不是故障或超时。

**问：事件监听收不到消息。**
答：事件要求 S 类摄像头，且需用户确认后执行 `manage_camera_events(action="start")`；自动恢复只会重启之前开启过的监听。轮询/等待语义见 [commands/events.md](commands/events.md)。

**问：补光 / 图像 / 追踪返回 `DEVICE_UNREACHABLE`。**
答：私有协议端口瞬时抖动——有界自动重试：参数不变，间隔 2-3 秒，最多 3 次，无需用户确认；重试期间不要重连或重新发现。

**问：数据会离开局域网吗？密码是明文存储吗？**
答：使用阶段流量仅限局域网；连接阶段仅与厂商云端确认连接状态。文件只写入 `config.yaml`、`snapshots/`、`video/`、`events/` 白名单位置。凭据（`password`/`sn_code`/`sn`/`pkdk`）以 XOR + base64 混淆存储（带 `enc1:` 前缀），仅在使用点于内存中还原一次；经工具 API 回传的存储值也只解码一次，不会二次混淆。

## 最佳实践

1. 会话开始：先 `get_registered_cameras()` 再逐台 `connect_device()`；长时间闲置后先 `search_devices()` 刷新（DHCP 换 IP）。
2. 定长录像只通过 `duration=<秒>` 实现——绝不用「睡一会再停」。
3. 自定义保存路径只用 ASCII 字符。
4. 纯数字密码/SN 必须以 JSON 字符串传递（`"847226"`），绝不能是裸数字。
5. 绝不手工拼接 RTSP 地址——只用 `get_audio_video_stream()` 返回的 `stream_url`。
6. 绝不硬编码 ONVIF 端口 80——使用 `search_devices()` / config.yaml 中的 `onvif_port`。
7. 云台、推流、截图、事件监听启动、补光/图像/追踪变更前，先获得用户明确确认。
8. 摄像头为单实例：新会话会自动接管（旧连接被断开）——在你想使用的会话里直接重试摄像头操作即可。
9. O 类设备身份仅用 `onvif_sn` 做匹配——绝不能作为 `sn_code` 喂给云授权或 SK HTTP。
10. 基于事件存储构建外部消费者 → [EVENT_INTEGRATION.md](EVENT_INTEGRATION.md)。

## 排障索引

按症状定位权威出处（本文为转述；与出处冲突时以出处为准）：

| 症状 | 快速处理 | 权威出处 |
|------|---------|---------|
| Server 启动即退（exit 70） | stdio 会话结束的正常退出，重启即可；锁冲突已是工具级错误，见上文 | [SKILL.md Gotchas](../SKILL.md#gotchas) · README 故障排查 |
| 工具报「camera-proto package is not installed」/「Failed to load camera protocol library」（协议库加载失败）/「ABI version mismatch」 | 用启动 MCP 的解释器跑 `"<MCP_PYTHON>" -m pip install -r requirements.txt` 后重试同一工具（无需重启） | [SKILL.md Decision Table](../SKILL.md#decision-table--error--status--action) · [Installation](../SKILL.md#installation) |
| `not_connected` / `needs_password` / `no_sn` / 授权失败组 | 重连 / 询问密码 / 终态处理 | [SKILL.md Decision Table](../SKILL.md#decision-table--error--status--action) · [WORKFLOW.md Phase 2](WORKFLOW.md) |
| 事件/补光/图像/追踪返回 `UNSUPPORTED_PROTOCOL` | 设备类别限制，告知用户 | [SKILL.md 能力矩阵](../SKILL.md#extended-capabilities--protocol-matrix) · `commands/*.md` |
| 流 / 截图 / 录像错误（`timeout`、`recording in progress`、写入失败） | 按决策表重试规则 | [SKILL.md Decision Table](../SKILL.md#decision-table--error--status--action) · [commands/stream.md](commands/stream.md) |
| J/O 类摄像头不支持云台 `degrees` 模式 | 改用 `duration_seconds` | [SKILL.md Phase 4](../SKILL.md#phase-4--ptz-control) · [commands/ptz.md](commands/ptz.md) |
| 补光/图像/追踪 `DEVICE_UNREACHABLE` | 有界自动重试 ×3 | [SKILL.md Decision Table](../SKILL.md#decision-table--error--status--action) · `commands/*.md` 的 `## Error codes` |
| 事件存储外部消费 | 契约与 schema | [EVENT_INTEGRATION.md](EVENT_INTEGRATION.md) · [commands/events.md](commands/events.md) |
| config.yaml schema / 手动预配置 | 完整 schema | [CONFIG.md](CONFIG.md) |

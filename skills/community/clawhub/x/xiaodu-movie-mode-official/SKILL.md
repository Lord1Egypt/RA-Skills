---
name: xiaodu-movie-mode-official
description: 基于已安装的 xiaodu-control-official 编排观影场景。当用户说“开始观影模式”“我要看电影”“把房间调成适合看电影的状态”“准备看电影了”时使用。这个 skill 会复用 xiaodu-control-official 的现有脚本，对小度智能屏和小度 IoT 设备执行 scene-first 的观影编排，而不是重做底层控制。
---

# xiaodu-movie-mode-official

## 定位

一个基于 `xiaodu-control-official` 的**观影场景 orchestrator**。

它不是电影搜索 skill，也不是播放器 skill，而是：

> 用户一句高层表达（“开始观影模式”）→ 系统先把房间和播放设备准备到“可以开始看”的状态 → 用户明确指定内容时，再继续进入播放层。

## 核心原则

**观影模式默认负责“把房间和设备准备到可以开始看”的状态；只有在用户明确指定内容时，才继续进入内容播放层。**

不默认替用户选电影，不默认自动播放一个平台里的内容。

---

## 基于 xiaodu-control-official 事实能力全集的统一规划框架

所有观影规划都只能建立在 `xiaodu-control-official` 已明确记录的能力 bucket 上。
不要加入想象中的设备族、动作或参数。

允许使用的规划 bucket 只有 7 个：

1. **scene**
   - 来源：`list_scenes.sh` / `trigger_scene.sh`
2. **lights（灯光）**
   - 来源：`list_iot_devices.sh` / `control_iot.sh`
3. **curtains（窗帘）**
   - 来源：`list_iot_devices.sh` / `control_iot.sh`
4. **thermal comfort（体感舒适）**
   - 来源：`list_iot_devices.sh` / `control_iot.sh`
   - 仅限用户明确说闷 / 热 / 冷时才使用
5. **display / playback device preparation（显示 / 播放设备）**
   - 来源：`list_iot_devices.sh` / `control_iot.sh`
   - 包括：电视、投影、机顶盒、音量、信号源、模式切换
   - 这是观影模式最核心的特有 bucket
6. **smart-screen speech（智能屏播报）**
   - 来源：`list_devices.sh` / `speak.sh`
7. **smart-screen assistant/media（智能屏助手 / 内容）**
   - 来源：`list_devices.sh` / `control_xiaodu.sh` / `push_resource.sh`
   - 仅在用户明确指定内容时才进入

规划顺序：

1. 先判断这次请求涉及哪些 bucket。
2. 再检查当前环境真实支持哪些 bucket。
3. 删除不支持的 bucket。
4. 把剩余 bucket 排成最安全的观影执行顺序。
5. 按 bucket 逐步执行，能做几步做几步。
6. 同一条观影流程里的所有命令都必须**串行执行**。
   - 上一个命令返回后，才能发下一个命令。
   - 不要把 `xiaodu` 或 `xiaodu-iot` 的控制命令并发打出去。
   - 如果上一个命令失败，后面的命令直接继续执行，不要因为单点失败中断整条流程。
7. 如果缺少继续执行所必需的信息，只问一个最小确认问题。
8. 执行结束后，把用户的调整吸收为后续偏好。

## 偏好记忆与复用

把用户对观影流程的调整当成可复用偏好。
如果用户修正了默认设备、信号源、音量、灯光风格、是否继续内容层等，下次应优先沿用。

至少要支持沉淀这些偏好：

- 观影默认设备
  - 电视 / 投影 / 智能屏
- 观影默认房间
  - 客厅 / 卧室 / 默认房间
- 默认信号源
  - HDMI / 电视主页 / 机顶盒
- 默认音量
  - 小 / 中 / 大
- 灯光风格
  - 全暗 / 柔和 / 留一点灯
- 窗帘风格
  - 全关 / 半关
- 是否自动进入内容层
  - 只做准备
  - 自动开平台
  - 自动切 HDMI
- 默认避免控制的设备 / 房间
- 确认风格
  - 先问再做
  - 只有一个明确目标时直接执行
- 环境偏好
  - 偏凉 / 偏暖 / 不动空调

存储规则：

- 默认**不主动写入**持久偏好文件。
- 只有在用户明确表达“记住这个偏好 / 以后都这样 / 下次也这样”时，才允许持久化。
- 小度 / 家庭场景的短中期偏好，优先写入 `XIAODU_CONTEXT.md`。
- 只有在确实属于长期稳定偏好、且用户明确要求记住时，才写入 `MEMORY.md`。
- 如果没有真的写入文件，就不要假装“已经记住”。

复用规则：

- 下次执行前，先检查已有偏好能否直接解决设备或内容选择问题。
- 如果已有偏好足够明确，就直接执行，不要重复问。
- 如果已有偏好与当前环境或当前用户表达冲突，优先当前请求，并在执行后更新偏好。

## 标准执行流程

### 1）先确认依赖可用

只做这次请求真正需要的最小检查：

1. 确认 `skills/xiaodu-control-official` 存在。
2. 确认关键依赖脚本存在。
3. 如果这次请求可能涉及 IoT，先读场景，再读 IoT 设备。
4. 如果这次请求需要智能屏播报或设备确认，先解析出一个可用智能屏。

如果依赖 skill 不可用，就停止并明确说明此 skill 依赖 `xiaodu-control-official`。

### 2）优先尝试 scene-first

1. 用 `list_scenes.sh` 读取现有场景。
2. 优先寻找高匹配场景，例如：
   - 观影
   - 影院
   - 电影
   - 家庭影院
   - 看电影
3. 如果找到高置信度场景，优先触发。
4. 触发成功后，再补一句简短播报。

推荐观影模式播报口径：

- 已经帮你把观影模式安排好了。
- 房间已经调整好了，可以开始看了。
- 观影模式已开启，准备好享受电影了。

如果 scene 触发失败，不能假装成功。

### 3）没有 scene 时，进入基于事实 bucket 的 fallback 规划

如果没有匹配 scene，不要直接退化成只说一句话。
而是继续基于事实 bucket 做结构化 fallback。

1. 读取 IoT 设备。
2. 只考虑这些 fallback bucket：
   - **lights**：把可用灯光调暗、关闭或调成更适合观影的亮度
   - **curtains**：如果有窗帘就关闭
   - **thermal comfort**：只有用户明确说闷 / 热 / 冷时，才考虑空调 / 风扇
   - **display / playback device preparation**：打开电视 / 投影、调音量、切信号源、切到观影模式
   - **smart-screen speech**：做一段简短确认播报
   - **smart-screen assistant/media**：只有用户明确指定内容时才进入
3. IoT bucket 只允许使用同时满足以下条件的设备：
   - 真实存在于当前设备列表
   - 与目标房间相关，或已被用户明确指定
4. 安全执行顺序：
   - scene（如果有）
   - lights
   - curtains
   - thermal comfort
   - display / playback device preparation
   - smart-screen speech
   - conditional smart-screen assistant/media
5. 某个 bucket 没有合适设备就跳过，不影响其他 bucket。
6. 如果多个目标都可能合理，只问一个最小确认问题。

关键原则：
**没有 scene，不等于退出；而是进入基于事实能力的结构化 fallback。**

### 4）把观影环境和设备准备纳入默认主流程

对于以下高层表达：

- 开始观影模式
- 我要看电影
- 把房间调成适合看电影的状态
- 准备看电影了

默认主流程应该是：

1. 先做可做的观影环境调整
2. 再做显示 / 播放设备准备（电视 / 投影 / 机顶盒 / 音量 / 信号源）
3. 再做一句简短但明确的确认播报
4. 只有用户明确指定内容时，才继续进入内容播放层

也就是说，产品默认理解不是：
- 一上来就打开某个平台播放随机内容

而是：
> **先把房间和设备准备到“可以开始看”的状态，用户说要看了再继续内容层。**

覆盖规则：
- 如果用户明确指定了具体设备或内容，就按用户指定执行。
- 如果已有偏好定义了环境 / 设备 / 信号源的顺序，就按偏好执行。
- 如果当前环境不适合做某项环境调整，也不要直接退出，仍然要完成设备准备和确认播报，并尽可能补齐后续步骤。

### 5）通用观影模式实际调用链

对于这种高层请求：

> 开始观影模式

默认调用链应当是：

1. `bash ../xiaodu-control-official/scripts/list_scenes.sh --server xiaodu-iot`
2. 如果存在高置信度观影 scene：
   - `bash ../xiaodu-control-official/scripts/trigger_scene.sh --scene-name "..." --server xiaodu-iot`
3. 否则：
   - `bash ../xiaodu-control-official/scripts/list_iot_devices.sh --server xiaodu-iot`
   - 如果有相关且可达的灯，用 `bash ../xiaodu-control-official/scripts/control_iot.sh ...` 调暗或关闭
   - 如果有窗帘，用 `bash ../xiaodu-control-official/scripts/control_iot.sh ...` 关闭
   - 如果有电视 / 投影 / 机顶盒 / 音量设备，做对应的准备动作
4. `bash ../xiaodu-control-official/scripts/list_devices.sh --server xiaodu`
5. `bash ../xiaodu-control-official/scripts/speak.sh ...`
6. 如果用户明确指定了内容，继续：
   - `bash ../xiaodu-control-official/scripts/control_xiaodu.sh --command "..." ...`
   - 或进一步的 IoT 设备控制

这条链路能保证整条编排链是分层且显式的。
除非用户明确说要自动播放内容，否则不要跳过环境和设备准备阶段，直接进入内容播放。

## 内容层的默认边界

### 默认不做这些
- 不默认替用户选具体电影
- 不默认自动打开某个影视平台播放随机内容
- 不默认搜索片单
- 不默认把“观影模式”理解成“马上开播”

### 只有在用户明确指定时才做
- 播电影 / 放《xxx》
- 打开爱奇艺 / 腾讯视频 / 优酷 / B站
- 切到 HDMI / 电视主页 / 机顶盒
- 打开投影看电影
- 打开电视开始播放

## 极简确认规则

### 需要确认的情况
- 同时有电视和投影，用户没说用哪个
- 同时有多个信号源都合理
- 不问就容易误控（比如客厅电视和卧室电视都在线）

### 不需要确认的情况
- 只有一个合理目标设备
- 用户已经明确指定
- 已有历史偏好

## 面向用户的汇报风格

面向用户时，优先给**产品化、自然汇报**，不要给技术动作日志。
一段好的自然汇报通常覆盖：

1. 已经帮用户安排好了什么
2. 现在正在发生什么
3. 接下来用户还可以让系统继续做什么

而且要把**真实已经成功的关键动作**讲出来，不要把价值藏在后台。
如果灯光确实调暗了、窗帘确实关闭了、电视确实打开了、信号源确实切好了，就应该体现在用户可听见的汇报里。

示例：

- 已经帮你把观影模式安排好了。
- 我刚刚把灯光收暗了，房间也调整得更适合看电影，电视这边也已经准备好。
- 现在已经可以开始看了，如果你想指定电影或者平台，我接着帮你切过去。

避免这样对用户说：
- 我先执行了 list_scenes
- 我调用了 control_iot
- 我刚刚执行了脚本

## 失败处理

这个 skill 对局部失败应当有容错。
不要因为一个动作失败就让整个观影流程中断。

好的降级示例：

- 没有 scene -> 自动改走设备 fallback
- 投影失败 -> 继续做灯光、窗帘、电视等后续动作
- 切信号源失败 -> 保持已准备好的设备状态，继续其他可做动作
- 没有智能屏 -> 仍可完成 IoT 环境与设备动作
- 某个属性不支持 -> 跳过这个属性继续后面动作
- 内容层失败 -> 保持在“环境和设备已准备好”的状态，不假装电影已开始播放

## 为什么不能重做底层

除非必要，不要绕过 `xiaodu-control-official`，因为它已经：

- 分清了 `xiaodu` 与 `xiaodu-iot`
- 带有更安全的脚本约束
- 定义了能力边界与 schema 预期
- 让排障更容易聚焦在同一依赖层
续后面动作
- 内容层失败 -> 保持在“环境和设备已准备好”的状态，不假装电影已开始播放

## 为什么不能重做底层

除非必要，不要绕过 `xiaodu-control-official`，因为它已经：

- 分清了 `xiaodu` 与 `xiaodu-iot`
- 带有更安全的脚本约束
- 定义了能力边界与 schema 预期
- 让排障更容易聚焦在同一依赖层

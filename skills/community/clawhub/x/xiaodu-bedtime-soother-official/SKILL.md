---
name: xiaodu-bedtime-soother-official
description: 基于已安装的 xiaodu-control-official 编排儿童睡前场景。当用户说“带孩子睡觉”“开始睡前模式”“帮我哄孩子睡觉”，或要求把房间调整到适合睡觉的状态时使用。这个 skill 会复用 xiaodu-control-official 的现有脚本，对小度智能屏和小度 IoT 设备执行 scene-first 的睡前编排，而不是重做底层控制。
---

# xiaodu-bedtime-soother-official

仅在已确认 `xiaodu-control-official` 已安装，且 `mcporter` 已经配置好 `xiaodu` 与 `xiaodu-iot` 时使用本 skill。

## 目的

处理“一句话进入睡前状态”的家庭场景请求。
这是一个**场景编排 skill**，不是底层控制 skill。
所有底层控制都应优先复用 `skills/xiaodu-control-official`。

## 依赖与路由规则

- 优先复用这些现有脚本：
  - `skills/xiaodu-control-official/scripts/list_scenes.sh`
  - `skills/xiaodu-control-official/scripts/trigger_scene.sh`
  - `skills/xiaodu-control-official/scripts/list_iot_devices.sh`
  - `skills/xiaodu-control-official/scripts/control_iot.sh`
  - `skills/xiaodu-control-official/scripts/list_devices.sh`
  - `skills/xiaodu-control-official/scripts/speak.sh`
  - `skills/xiaodu-control-official/scripts/control_xiaodu.sh`
  - `skills/xiaodu-control-official/scripts/push_resource.sh`
- 本 skill 自己还提供一个睡前故事收尾脚本：
  - `scripts/bedtime_story_tail.sh`
- 家电控制优先走 `xiaodu-iot`。
- 智能屏语音助手类动作优先走 `xiaodu`。
- `control_xiaodu` 只用于故事、白噪音、轻音乐、播报等智能屏助手能力。
- 除非依赖脚本缺失或明显损坏，否则不要绕过依赖 skill 重写底层 MCP 调用。

## 典型触发词

把以下表达视为强触发：

- 小度，带孩子睡觉
- 开始睡前模式
- 帮我哄孩子睡觉
- 把卧室调成适合睡觉的状态
- 开晚安模式
- 进入儿童睡眠模式

## 基于 xiaodu-control-official 事实能力全集的统一规划框架

所有睡前规划都只能建立在 `xiaodu-control-official` 已明确记录的能力 bucket 上。
不要加入想象中的设备族、动作或参数。

允许使用的规划 bucket 只有 6 个：

1. **scene**
   - 来源：`list_scenes.sh` / `trigger_scene.sh`
2. **lights（灯光）**
   - 来源：`list_iot_devices.sh` / `control_iot.sh`
3. **curtains（窗帘）**
   - 来源：`list_iot_devices.sh` / `control_iot.sh`
4. **thermal comfort（体感舒适）**
   - 来源：`list_iot_devices.sh` / `control_iot.sh`
   - 仅限依赖 skill 已覆盖的空调 / 风扇类能力
5. **smart-screen speech（智能屏播报）**
   - 来源：`list_devices.sh` / `speak.sh`
6. **smart-screen assistant/media（智能屏助手 / 内容）**
   - 来源：`list_devices.sh` / `control_xiaodu.sh` / `push_resource.sh`
   - 对于“带孩子睡觉 / 哄孩子睡觉”这类高层请求，睡前内容属于默认主流程的一部分

规划顺序：

1. 先判断这次请求涉及哪些 bucket。
2. 再检查当前环境真实支持哪些 bucket。
3. 删除不支持的 bucket。
4. 把剩余 bucket 排成最安全的睡前执行顺序。
5. 按 bucket 逐步执行，能做几步做几步。
6. 同一条 bedtime 流程里的所有命令都必须**串行执行**。
   - 上一个命令返回后，才能发下一个命令。
   - 不要把 `xiaodu` 或 `xiaodu-iot` 的控制命令并发打出去。
   - 如果上一个命令失败，后面的命令直接继续执行，不要因为单点失败中断整条流程。
7. 如果缺少继续执行所必需的信息，只问一个最小确认问题。
8. 执行结束后，把用户的调整吸收为后续偏好。

## 偏好记忆与复用

把用户对睡前流程的调整当成可复用偏好。
如果用户修正了默认屏幕、内容类型、避免控制的设备、是否少确认等，下次应优先沿用。

至少要支持沉淀这些偏好：

- 睡前默认智能屏
- 睡前内容优先级
  - 故事优先
  - 白噪音优先
  - 轻音乐优先
  - 只播报
- 睡前内容类型
  - 故事
  - 白噪音
  - 轻音乐
  - 只播报
- 睡前结尾控制
  - 15 分钟后停止
  - N 分钟后停止
  - 一直播放
  - 停止播放并关屏
- 默认避免控制的设备 / 房间
- 确认风格
  - 先问再做
  - 只有一个明确目标时直接执行
- 环境偏好
  - 更暗一点
  - 默认不动空调
  - 不动电视

存储规则：

- 小度 / 家庭场景的短中期偏好，优先写入 `XIAODU_CONTEXT.md`。
- 长期稳定偏好，写入 `MEMORY.md`。
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
4. 如果这次请求需要智能屏播报或内容播放，先解析出一个可用智能屏。

如果依赖 skill 不可用，就停止并明确说明此 skill 依赖 `xiaodu-control-official`。

### 2）优先尝试 scene-first

1. 用 `list_scenes.sh` 读取现有场景。
2. 优先寻找高匹配场景，例如：
   - 晚安
   - 睡眠
   - 睡前
   - 儿童睡眠
   - 夜间
3. 如果找到高置信度场景，优先触发。
4. 触发成功后，再补一句简短播报。

推荐睡前播报口径：

- 已经进入睡前模式，晚安。
- 房间已经调整好了，准备休息吧。
- 晚安模式已开启，可以安心睡觉了。

如果 scene 触发失败，不能假装成功。

### 3）没有 scene 时，进入基于事实 bucket 的 fallback 规划

如果没有匹配 scene，不要直接退化成只说一句话。
而是继续基于事实 bucket 做结构化 fallback。

1. 读取 IoT 设备。
2. 只考虑这些 fallback bucket：
   - **lights**：把可用灯光调暗、关闭或调柔和
   - **curtains**：如果有窗帘就关闭
   - **thermal comfort**：只有用户明确说热 / 冷 / 闷时，才考虑空调 / 风扇
   - **smart-screen speech**：做一段简短睡前播报
   - **smart-screen assistant/media**：进入睡前内容主流程
3. IoT bucket 只允许使用同时满足以下条件的设备：
   - 真实存在于当前设备列表
   - 与目标房间相关，或已被用户明确指定
4. 安全执行顺序：
   - scene（如果有）
   - lights
   - curtains
   - thermal comfort
   - smart-screen speech
   - smart-screen bedtime content
5. 某个 bucket 没有合适设备就跳过，不影响其他 bucket。
6. 如果多个目标都可能合理，只问一个最小确认问题。

关键原则：
**没有 scene，不等于退出；而是进入基于事实能力的结构化 fallback。**

### 4）把睡前内容纳入默认主流程

对于以下高层表达：

- 带孩子睡觉
- 帮我哄孩子睡觉
- 开始睡前模式

睡前内容通常应当属于默认主流程，不应只是最后临时追加的可选项。

默认内容优先级：
- 第一优先：睡前故事
- 第二优先：白噪音
- 第三优先：轻音乐
- 最低降级：只播报一句晚安

覆盖规则：
- 如果用户明确指定内容类型，按用户指定执行。
- 如果已有存量偏好定义了内容优先级，按偏好执行。
- 如果首选内容因为设备行为或环境问题不可用，就降级到下一种内容，不要直接跳到只播报。

实现规则：
- 故事 / 白噪音 / 轻音乐这类内容请求，统一走 `control_xiaodu.sh`。
- 内容请求尽量单一、简洁，不要一次堆多个助手指令。
- 如果走默认 story-first，需要挂一个延时收尾动作。

### 5）通用 bedtime 实际调用链

对于这种高层请求：

> 小度，带孩子睡觉吧

默认调用链应当是：

1. `bash ../xiaodu-control-official/scripts/list_scenes.sh --server xiaodu-iot`
2. 如果存在高置信度 bedtime scene：
   - `bash ../xiaodu-control-official/scripts/trigger_scene.sh --scene-name "..." --server xiaodu-iot`
3. 否则：
   - `bash ../xiaodu-control-official/scripts/list_iot_devices.sh --server xiaodu-iot`
   - 如果有相关且可达的灯，用 `bash ../xiaodu-control-official/scripts/control_iot.sh ...`
   - 如果有相关窗帘，用 `bash ../xiaodu-control-official/scripts/control_iot.sh ...`
   - 如果用户明确提到热 / 冷 / 闷，且存在受支持的空调 / 风扇，再用 `bash ../xiaodu-control-official/scripts/control_iot.sh ...`
4. 解析或使用偏好的智能屏：
   - `bash ../xiaodu-control-official/scripts/list_devices.sh --server xiaodu`
5. 做一段睡前播报：
   - `bash ../xiaodu-control-official/scripts/speak.sh ...`
6. 启动睡前内容：
   - `bash ../xiaodu-control-official/scripts/control_xiaodu.sh --command "讲个睡前故事" ...`
   - 如果偏好或用户明确要求是白噪音 / 轻音乐，就替换这一段
7. 如果本次内容选择是 story-first，就再挂收尾脚本：
   - `bash scripts/bedtime_story_tail.sh --device-name "..." --delay-minutes 15`

如果用户偏好或本次明确请求改变了设备 / 内容选择，只替换对应那一段调用链，不要重写整条链。

整条调用链必须串行执行：
- 上一个命令未返回前，不要发下一个命令
- 如果上一个命令失败，后面的命令直接继续执行
- 不要把灯光、播报、故事、stop/screen-off 等步骤并发打出去

### 6）故事后收尾控制

对于默认 story-first 路径，应当附带默认收尾方案：

1. 开始讲睡前故事
2. 约 15 分钟后发送停止 / 暂停播放
3. 再尝试发送关闭屏幕

这部分的实际可执行实现由：

- `bash scripts/bedtime_story_tail.sh --device-name "..." --delay-minutes 15`

完成。

如果当前运行环境不适合做延时任务，也要明确说明本设计期望有 timed stop step，并采用当前环境里最接近的后续控制方案。

## 降级原则

- 没有 IoT，但有智能屏：仍然完成播报和睡前内容。
- 某个 IoT 动作失败：继续做剩余安全动作。
- schema 不支持某属性：跳过该属性，不要终止整个流程。
- 找不到可用智能屏：不要假装故事 / 播报已经成功。
- 只有非卧室设备：不要默认控全屋，先请用户指定。

## 当前环境下的执行偏置

在当前已知环境里，如果用户没指定设备，默认优先屏顺序是：

1. `小度智能屏3`
2. `小度智能屏2`
3. `小度添添闺蜜机Pro 4K Max`

同时偏向 **screen-first + conservative IoT**：
如果没有确认到明确且相关的可达卧室 IoT，不要主动去动客厅设备。

## 极简确认规则

只有在继续执行确实缺信息时才问。

可能需要确认的情况：
- 有多个合理智能屏，且没有已存偏好
- 有多个合理灯光目标，且房间不清楚
- 不问就可能控错房间 / 设备

不应该确认的情况：
- 只有一个合适智能屏
- 已有偏好已经选好了默认屏
- 用户已经明确说了设备或房间

## 防误控规则

- 不要默认“全屋”。
- 优先按卧室相关设备执行。
- 不要说“夜灯已打开”，除非真的成功打开。
- 不要说窗帘 / 空调 / 风扇 / 灯已经改了，除非真的改成功。
- 不要编造 schema 字段、scene 名、设备名或参数。

## 面向用户的回复风格

- 简短
- 温和
- 不夸张拟人
- 不给用户看技术调用日志
- 只汇报真实成功的动作
- 优先用**产品化、自然汇报**口径，而不是技术步骤清单

汇报时尽量告诉用户三件事：
1. 已经帮用户安排好了什么
2. 现在正在发生什么
3. 接下来还会自动发生什么

如果某个关键动作已经真实成功，应该把这个成功动作体现在用户可感知的播报里，不要只在后台执行。
尤其是灯光、窗帘、空调、风扇、故事启动、自动收尾这类动作，至少要把成功项中的关键 1-3 项讲出来，让用户清楚知道系统刚刚完成了什么。

推荐睡前自然汇报口径：

- 已经帮你把睡前模式安排好了。
- 我刚刚已经把射灯调暗了，现在房间已经更适合休息。
- 我也已经在小度上开始讲睡前故事了。
- 为了不一直播放下去，我还安排了一个收尾动作：5 分钟后会自动停掉故事，并尝试把屏幕关掉。

如果本次实际成功动作不同，就按真实成功动作改写，不要机械套模板。

除非用户明确要求技术细节，否则不要给用户讲 raw tool sequence。

## 示例请求

- 小度，带孩子睡觉。
- 开始睡前模式。
- 帮我哄孩子睡觉，再放一点白噪音。
- 把卧室调成适合睡觉的状态，有点热。
- 把灯调暗一点，准备睡觉。

## 示例回复风格

- 已经帮你把睡前模式安排好了，接下来会在小度上讲睡前故事，5 分钟后我会自动帮你收尾。
- 房间已经调整到更适合休息的状态了，我现在开始给孩子讲睡前故事。
- 我先帮你把环境收柔和了，不过没找到夜灯；接下来我会继续用小度做睡前安抚。

## 按需阅读的引用文档

- 需要看更细的编排说明时，读 `references/usage-notes.md`
- 需要看测试边界与验证项时，读 `references/test-cases.md`

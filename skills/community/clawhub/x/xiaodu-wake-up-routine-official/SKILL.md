---
name: xiaodu-wake-up-routine-official
description: 基于已安装的 xiaodu-control-official 编排儿童起床场景。当用户说“叫孩子起床”“开始早安模式”“帮我把孩子叫醒”，或要求让房间进入起床状态时使用。这个 skill 会复用 xiaodu-control-official 的现有脚本，对小度智能屏和小度 IoT 设备执行 scene-first 的晨起编排，而不是重做底层控制。
---

# xiaodu-wake-up-routine-official

仅在已确认 `xiaodu-control-official` 已安装，且 `mcporter` 已经配置好 `xiaodu` 与 `xiaodu-iot` 时使用本 skill。

## 目的

处理“一句话进入晨起状态”的家庭场景请求。
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
- 家电控制优先走 `xiaodu-iot`。
- 智能屏语音助手类动作优先走 `xiaodu`。
- `control_xiaodu` 只用于天气、时间、新闻、儿歌、轻音乐、播报等智能屏助手能力。
- 除非依赖脚本缺失或明显损坏，否则不要绕过依赖 skill 重写底层 MCP 调用。

## 典型触发词

把以下表达视为强触发：

- 小度，叫孩子起床
- 开始早安模式
- 帮我把孩子叫醒
- 打开起床流程
- 让房间进入起床状态
- 开晨起模式

## 基于 xiaodu-control-official 事实能力全集的统一规划框架

所有起床规划都只能建立在 `xiaodu-control-official` 已明确记录的能力 bucket 上。
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
   - 仅在用户明确要求天气 / 时间 / 新闻 / 儿歌 / 轻音乐时追加

规划顺序：

1. 先判断这次请求涉及哪些 bucket。
2. 再检查当前环境真实支持哪些 bucket。
3. 删除不支持的 bucket。
4. 把剩余 bucket 排成最安全的晨起执行顺序。
5. 按 bucket 逐步执行，能做几步做几步。
6. 如果缺少继续执行所必需的信息，只问一个最小确认问题。
7. 执行结束后，把用户的调整吸收为后续偏好。

## 偏好记忆与复用

把用户对晨起流程的调整当成可复用偏好。
如果用户修正了默认屏幕、信息类型、内容类型、避免控制的设备、是否少确认等，下次应优先沿用。

至少要支持沉淀这些偏好：

- 起床默认智能屏
- 起床信息优先级
  - 先播天气
  - 先播时间
  - 先播新闻
  - 不额外播信息
- 起床内容类型
  - 儿歌
  - 轻音乐
  - 只播报
- 默认避免控制的设备 / 房间
- 确认风格
  - 先问再做
  - 只有一个明确目标时直接执行
- 环境偏好
  - 先亮灯再播报
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
4. 如果这次请求需要智能屏播报或信息 / 内容播放，先解析出一个可用智能屏。

如果依赖 skill 不可用，就停止并明确说明此 skill 依赖 `xiaodu-control-official`。

### 2）优先尝试 scene-first

1. 用 `list_scenes.sh` 读取现有场景。
2. 优先寻找高匹配场景，例如：
   - 早安
   - 起床
   - 晨间
   - 上学前
   - 早晨
3. 如果找到高置信度场景，优先触发。
4. 触发成功后，再补一句简短播报。

推荐晨起播报口径：

- 早安，准备起床啦。
- 房间已经调整好了，可以起床了。
- 早安模式已开启，开始新的一天吧。

如果 scene 触发失败，不能假装成功。

### 3）没有 scene 时，进入基于事实 bucket 的 fallback 规划

如果没有匹配 scene，不要直接退化成只说一句话。
而是继续基于事实 bucket 做结构化 fallback。

1. 读取 IoT 设备。
2. 只考虑这些 fallback bucket：
   - **lights**：把可用灯光打开、提亮或调成更适合晨起的亮度 / 色温
   - **curtains**：如果有窗帘就打开
   - **thermal comfort**：只有用户明确说闷 / 热时，才考虑空调 / 风扇
   - **smart-screen speech**：做一段简短晨起播报
   - **smart-screen assistant/media**：继续补时间、天气、备忘录信息、儿歌 / 轻快音乐这些晨起主流程内容
3. IoT bucket 只允许使用同时满足以下条件的设备：
   - 真实存在于当前设备列表
   - 与目标房间相关，或已被用户明确指定
4. 安全执行顺序：
   - scene（如果有）
   - lights
   - curtains
   - thermal comfort
   - smart-screen speech
   - optional smart-screen assistant/media
5. 某个 bucket 没有合适设备就跳过，不影响其他 bucket。
6. 如果多个目标都可能合理，只问一个最小确认问题。

关键原则：
**没有 scene，不等于退出；而是进入基于事实能力的结构化 fallback。**

### 4）把晨起提醒纳入默认主流程

对于以下高层表达：

- 叫孩子起床
- 帮我把孩子叫醒
- 开始早安模式

默认主流程不应只是环境动作，也不应默认直接扩展成很多无关信息流。
更合理的默认顺序是：

1. 先做可做的晨起环境调整
2. 再做一句简短但明确的起床提醒
3. 继续说时间
4. 继续播天气
5. 如果存在明确可提醒的备忘录信息，就继续播报备忘录提醒
6. 继续播放儿歌或轻快音乐

默认晨起主流程优先级：
1. 环境调整
2. 晨起提醒播报
3. 时间
4. 天气
5. 备忘录信息
6. 儿歌或轻快音乐

这些内容对“叫孩子起床 / 帮我把孩子叫醒 / 开始早安模式”这类高层请求来说，默认属于主流程的一部分，不再只是附加菜单。

覆盖规则：
- 如果用户明确指定了具体内容，就按用户指定执行。
- 如果已有偏好定义了天气 / 时间 / 儿歌 / 轻快音乐的顺序，就按偏好执行。
- 如果当前环境不适合做环境调整，也不要直接退出，仍然要完成起床提醒播报，并尽可能补齐后续晨起内容。

### 5）通用 wake-up 实际调用链

对于这种高层请求：

> 小度，叫孩子起床

默认调用链应当是：

1. `bash ../xiaodu-control-official/scripts/list_scenes.sh --server xiaodu-iot`
2. 如果存在高置信度 wake-up scene：
   - `bash ../xiaodu-control-official/scripts/trigger_scene.sh --scene-name "..." --server xiaodu-iot`
3. 否则：
   - `bash ../xiaodu-control-official/scripts/list_iot_devices.sh --server xiaodu-iot`
   - 如果有相关且可达的灯，用 `bash ../xiaodu-control-official/scripts/control_iot.sh ...`
   - 如果有相关窗帘，用 `bash ../xiaodu-control-official/scripts/control_iot.sh ...`
   - 如果用户明确提到闷 / 热，且存在受支持的空调 / 风扇，再用 `bash ../xiaodu-control-official/scripts/control_iot.sh ...`
4. 解析或使用偏好的智能屏：
   - `bash ../xiaodu-control-official/scripts/list_devices.sh --server xiaodu`
5. 做一段晨起播报：
   - `bash ../xiaodu-control-official/scripts/speak.sh ...`
6. 继续补全晨起主流程内容：
   - `bash ../xiaodu-control-official/scripts/control_xiaodu.sh --command "播下今天的天气" ...`
   - `bash ../xiaodu-control-official/scripts/control_xiaodu.sh --command "说一下现在几点" ...`
   - `bash ../xiaodu-control-official/scripts/control_xiaodu.sh --command "放一首儿歌" ...`
   - 或 `bash ../xiaodu-control-official/scripts/control_xiaodu.sh --command "放一点轻快的音乐" ...`

默认情况下，天气、时间、儿歌 / 轻快音乐应属于泛化 wake-up 请求的主流程内容；只有在用户明确排除或偏好另有定义时才跳过或重排。

如果用户偏好或本次明确请求改变了设备 / 内容选择，只替换对应那一段调用链，不要重写整条链。

整条调用链必须串行执行：
- 上一个命令未返回前，不要发下一个命令
- 如果上一个命令失败，后面的命令直接继续执行
- 不要把灯光、播报、时间、天气、备忘录、儿歌 / 轻快音乐等步骤并发打出去

## 降级原则

- 没有 IoT，但有智能屏：仍然完成播报和已明确要求的信息 / 内容。
- 某个 IoT 动作失败：继续做剩余安全动作。
- schema 不支持某属性：跳过该属性，不要终止整个流程。
- 找不到可用智能屏：不要假装天气 / 儿歌 / 播报已经成功。
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
- 不要说窗帘 / 空调 / 风扇 / 灯已经改了，除非真的改成功。
- 不要编造 schema 字段、scene 名、设备名或参数。
- 如果用户没有明确要求，不要主动开播太多天气 / 新闻 / 音乐，避免打扰。

## 面向用户的回复风格

- 温和
- 比睡前更有行动感
- 不夸张拟人
- 不给用户看技术调用日志
- 只汇报真实成功的动作
- 优先用**产品化、自然汇报**口径，而不是技术步骤清单

汇报时尽量告诉用户三件事：
1. 已经帮用户安排好了什么
2. 现在正在发生什么
3. 接下来用户还可以继续让系统做什么

如果某个关键动作已经真实成功，应该把这个成功动作体现在用户可感知的播报里，不要只在后台执行。
尤其是灯光提亮、窗帘打开、晨起提醒已开始、天气/时间/儿歌已开始这类动作，至少要把其中最关键的 1-3 项讲出来。

推荐晨起自然汇报口径：

- 已经帮你把起床模式安排好了。
- 我刚刚已经把房间调整到更适合起床的状态，也已经在小度上开始提醒孩子起床了。
- 如果你需要，我还可以继续播今天的天气、时间或者儿歌。

如果本次实际成功动作不同，就按真实成功动作改写，不要机械套模板。
除非用户明确要求技术细节，否则不要给用户讲 raw tool sequence。

## 示例请求

- 小度，叫孩子起床。
- 开始早安模式。
- 帮我把孩子叫醒，再播下今天的天气。
- 让房间进入起床状态。
- 拉开窗帘，把灯打开。

## 示例回复风格

- 已经帮你把起床模式安排好了，我先让房间进入更适合晨起的状态，接下来也可以继续播天气或儿歌。
- 早安模式已经开始了，我现在先提醒孩子起床；如果你要，我再继续播一下今天天气。
- 我先把能做的环境调整做好了，不过没找到窗帘设备；接下来我可以继续用小度做晨起提醒。

## 按需阅读的引用文档

- 需要看更细的编排说明时，读 `references/usage-notes.md`
- 需要看测试边界与验证项时，读 `references/test-cases.md`
天气。
- 我先把能做的环境调整做好了，不过没找到窗帘设备；接下来我可以继续用小度做晨起提醒。

## 按需阅读的引用文档

- 需要看更细的编排说明时，读 `references/usage-notes.md`
- 需要看测试边界与验证项时，读 `references/test-cases.md`

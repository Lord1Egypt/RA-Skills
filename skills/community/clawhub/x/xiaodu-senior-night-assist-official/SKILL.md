---
name: xiaodu-senior-night-assist-official
description: 基于已安装的 xiaodu-control-official 编排老人夜间短时起身的安全辅助场景。当用户说“夜里起夜”“我要去卫生间”“帮我开一下夜灯”“夜间辅助模式”这类请求时使用。这个 skill 会复用 xiaodu-control-official 的现有脚本，对小度智能屏和小度 IoT 设备执行 scene-first 的夜间辅助编排，而不是重做底层控制。它的目标不是普通开灯，而是用最少的光、最短的话和最稳的收尾，帮助老人安全完成夜间短时活动。
---

# xiaodu-senior-night-assist-official

仅在已确认 `xiaodu-control-official` 已安装，且 `mcporter` 已经配置好 `xiaodu` 与 `xiaodu-iot` 时使用本 skill。

## 目的

处理“老人半夜临时起身”的家庭场景请求。
这是一个**安全辅助编排 skill**，不是底层控制 skill。
所有底层控制都应优先复用 `skills/xiaodu-control-official`。

## 依赖与路由规则

- 优先复用这些现有脚本：
  - `skills/xiaodu-control-official/scripts/list_scenes.sh`
  - `skills/xiaodu-control-official/scripts/trigger_scene.sh`
  - `skills/xiaodu-control-official/scripts/list_iot_devices.sh`
  - `skills/xiaodu-control-official/scripts/control_iot.sh`
  - `skills/xiaodu-control-official/scripts/list_devices.sh`
  - `skills/xiaodu-control-official/scripts/speak.sh`
- 本 skill 自己还提供一个自动收尾脚本：
  - `scripts/night_light_tail.sh`
- 家电控制优先走 `xiaodu-iot`。
- 智能屏短播报优先走 `xiaodu`。
- 除非依赖脚本缺失或明显损坏，否则不要绕过依赖 skill 重写底层 MCP 调用。

## 典型触发词

把以下表达视为强触发：

- 夜里起夜
- 我要去卫生间
- 帮我开一下夜灯
- 夜间辅助模式
- 我起夜了
- 去趟厕所
- 太黑了
- 我要喝水，开一下灯

## 核心原则

### 1）路径安全优先

这个 skill 的第一目标不是“把灯打开”，而是：

> **让老人安全完成一小段夜间动线。**

### 2）默认低刺激

默认只做这些：
- 暖光
- 低亮度
- 短播报
- 小范围照明

不要默认：
- 全屋大亮
- 冷白光
- 长篇播报
- 放音乐 / 新闻 / 其他内容

### 3）自动收尾属于主流程

夜间辅助模式必须默认自带收尾：
- 防止老人回床后忘记关灯
- 防止灯一直亮着
- 防止整晚高亮影响休息

### 4）保守控制

- 不默认全屋开灯
- 不默认控错房间
- 不默认调整空调
- 不默认放内容

## 基于 xiaodu-control-official 事实能力全集的统一规划框架

所有夜间辅助规划都只能建立在 `xiaodu-control-official` 已明确记录的能力 bucket 上。
不要加入想象中的设备族、动作或参数。

允许使用的规划 bucket 只有 5 个：

1. **scene**
   - 来源：`list_scenes.sh` / `trigger_scene.sh`
2. **lights（夜间灯光）**
   - 来源：`list_iot_devices.sh` / `control_iot.sh`
   - 用于夜灯、床边灯、走廊灯、卫生间灯等
3. **thermal comfort（体感舒适）**
   - 来源：`list_iot_devices.sh` / `control_iot.sh`
   - 仅在用户明确说冷 / 热 / 闷时才使用
4. **smart-screen speech（智能屏短播报）**
   - 来源：`list_devices.sh` / `speak.sh`
5. **timed tail / auto-off（自动收尾）**
   - 来源：本 skill 自带延时收尾脚本
   - 用于几分钟后自动关闭本次开启的灯

规划顺序：

1. 先判断这次请求涉及哪些 bucket。
2. 再检查当前环境真实支持哪些 bucket。
3. 删除不支持的 bucket。
4. 再判断这次请求属于：
   - **路径照明模式**
   - **局部照明模式**
5. 把剩余 bucket 排成最安全的夜间执行顺序。
6. 按 bucket 逐步执行，能做几步做几步。
7. 同一条 night-assist 流程里的所有命令都必须**串行执行**。
   - 上一个命令返回后，才能发下一个命令。
   - 不要把 `xiaodu` 或 `xiaodu-iot` 的控制命令并发打出去。
   - 如果上一个命令失败，后面的命令直接继续执行，不要因为单点失败中断整条流程。
8. 如果缺少继续执行所必需的信息，只问一个最小确认问题。
9. 执行结束后，把用户的调整吸收为后续偏好。

## 偏好记忆与复用

把用户对夜间辅助流程的调整当成可复用偏好。
如果用户修正了默认夜灯、默认路径灯顺序、亮度、色温、自动收尾时间、是否播报等，下次应优先沿用。

至少要支持沉淀这些偏好：

- 默认夜灯设备
- 默认路径灯顺序
- 默认亮度
  - 10%
  - 20%
  - 30%
- 默认色温
  - 暖黄
- 默认自动关闭时间
  - 3 分钟
  - 5 分钟
  - 10 分钟
- 是否默认播报
  - 播一句
  - 不播报
- 默认避免控制的灯 / 房间
- 默认优先模式
  - 路径照明优先
  - 局部照明优先

存储规则：

- 小度 / 家庭场景的短中期偏好，优先写入 `XIAODU_CONTEXT.md`。
- 长期稳定偏好，写入 `MEMORY.md`。
- 如果没有真的写入文件，就不要假装“已经记住”。

复用规则：

- 下次执行前，先检查已有偏好能否直接解决设备选择问题。
- 如果已有偏好足够明确，就直接执行，不要重复问。
- 如果已有偏好与当前环境或当前用户表达冲突，优先当前请求，并在执行后更新偏好。

## 标准执行流程

### 1）先确认依赖可用

只做这次请求真正需要的最小检查：

1. 确认 `skills/xiaodu-control-official` 存在。
2. 确认关键依赖脚本存在。
3. 如果这次请求可能涉及 IoT，先读场景，再读 IoT 设备。
4. 如果这次请求需要短播报，先解析出一个可用智能屏。
5. 确认本 skill 的自动收尾脚本存在。

如果依赖 skill 不可用，就停止并明确说明此 skill 依赖 `xiaodu-control-official`。

### 2）优先尝试 scene-first

1. 用 `list_scenes.sh` 读取现有场景。
2. 优先寻找高匹配场景，例如：
   - 夜灯
   - 夜间
   - 起夜
   - 夜间辅助
   - 晚上起身
3. 如果找到高置信度场景，优先触发。
4. 触发成功后，再补一句简短播报。
5. 然后挂自动收尾。

推荐播报口径：

- 夜灯已经开好了，慢一点走。
- 路径灯已经打开了，注意脚下。
- 灯已经帮你开好了，别着急。

如果 scene 触发失败，不能假装成功。

### 3）没有 scene 时，进入基于事实 bucket 的 fallback 规划

如果没有匹配 scene，不要直接退化成只说一句话。
而是继续基于事实 bucket 做结构化 fallback。

1. 读取 IoT 设备。
2. 根据 query 判断是：
   - **路径照明模式**
   - **局部照明模式**
3. 只考虑这些 fallback bucket：
   - **lights**：打开、调低亮度、调暖色温
   - **smart-screen speech**：一句简短安全播报
   - **thermal comfort**：仅在明确说冷/热时附加
   - **timed tail**：延时关灯
4. IoT bucket 只允许使用同时满足以下条件的设备：
   - 真实存在于当前设备列表
   - 与目标房间相关，或已被用户明确指定
5. 安全执行顺序：
   - scene（如果有）
   - lights
   - smart-screen speech
   - thermal comfort（如明确需要）
   - timed tail
6. 某个 bucket 没有合适设备就跳过，不影响其他 bucket。
7. 如果多个目标都可能合理，只问一个最小确认问题。

关键原则：
**没有 scene，不等于退出；而是进入基于事实能力的结构化 fallback。**

### 4）路径照明 / 局部照明分流规则

#### 路径照明模式

以下表达默认进入路径照明：
- 夜里起夜
- 我要去卫生间
- 我起夜了
- 去趟厕所
- 帮我开一下去卫生间的灯

默认顺序：
1. 床边灯 / 夜灯
2. 走廊灯
3. 卫生间灯

#### 局部照明模式

以下表达默认进入局部照明：
- 帮我开一下夜灯
- 太黑了
- 我要喝水
- 开一下床边灯
- 开个小灯就行

默认动作：
1. 优先开最近的一盏柔和灯
2. 不自动扩展成整条路径
3. 自动收尾时间更短

#### 温控附加条件

如果 query 同时带有：
- 冷
- 热
- 闷

则在主模式基础上附加轻微温控。

### 5）通用实际调用链

对于这种高层请求：

> 夜里起夜

默认调用链应当是：

1. `bash ../xiaodu-control-official/scripts/list_scenes.sh --server xiaodu-iot`
2. 如果存在高置信度 night-assist scene：
   - `bash ../xiaodu-control-official/scripts/trigger_scene.sh --scene-name "..." --server xiaodu-iot`
3. 否则：
   - `bash ../xiaodu-control-official/scripts/list_iot_devices.sh --server xiaodu-iot`
   - 选择夜灯 / 床边灯 / 走廊灯 / 卫生间灯
   - `bash ../xiaodu-control-official/scripts/control_iot.sh ...`
   - 如果支持亮度：调低亮度
   - 如果支持色温：调暖
4. `bash ../xiaodu-control-official/scripts/list_devices.sh --server xiaodu`
5. `bash ../xiaodu-control-official/scripts/speak.sh ...`
6. 如果用户明确提到冷 / 热，再做轻微温控：
   - `bash ../xiaodu-control-official/scripts/control_iot.sh ...`
7. 挂自动收尾：
   - `bash scripts/night_light_tail.sh --device-name "..." --delay-minutes 5`

对于：

> 帮我开一下夜灯

则把第 3 步缩成单灯优先，不扩展整条路径，并把自动收尾改成更短时间。

## 降级原则

- 没有 scene -> 自动改走设备 fallback
- 找不到路径灯 -> 至少开一盏最接近的柔和灯
- 某个灯失败 -> 继续尝试后面的可用灯
- 没有智能屏 -> 仍然完成灯光动作，不假装播报已成功
- 色温 / 亮度不支持 -> 只做开灯，不终止整个流程
- 自动收尾脚本不可用 -> 明确说明“灯已经开好，但这次不会自动关”

## 极简确认规则

只有在继续执行确实缺信息时才问。

可能需要确认的情况：
- 有多个合理灯光目标，路径不清楚
- 同时有卧室灯 / 客厅灯 / 走廊灯，不知道该开哪个
- 不问就可能控错房间

推荐确认口径：
- 你是要去卫生间，还是只开床边灯？

不应该确认的情况：
- 只有一个明确夜灯目标
- 用户已经说了“走廊灯”“卫生间灯”
- 已有固定偏好

## 防误控规则

- 不要默认全屋开灯
- 不要默认最亮
- 不要默认冷白光
- 不要默认开电视
- 不要默认放内容
- 不要在没必要时调空调
- 不要长篇播报
- 不要控错房间

## 面向用户的回复风格

这个模式的汇报必须：
- 短
- 稳
- 低打扰
- 有安全感
- 不技术化

推荐口径：
- 夜灯已经开好了，慢一点走。
- 路径灯已经打开了，注意脚下。
- 灯已经帮你开好了，过几分钟我会自动关掉。

避免这样说：
- 我现在为你执行夜间安全辅助链路
- 我已经调用灯光系统
- 现在开始执行定时关灯

## 示例请求

- 夜里起夜。
- 我要去卫生间。
- 帮我开一下夜灯。
- 太黑了。
- 我要喝水，开一下灯。
- 夜间辅助模式。

## 按需阅读的引用文档

- 需要看更细的编排说明时，读 `references/usage-notes.md`
- 需要看测试边界与验证项时，读 `references/test-cases.md`

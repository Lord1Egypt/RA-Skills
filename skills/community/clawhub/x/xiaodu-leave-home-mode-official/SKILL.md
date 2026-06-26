---
name: xiaodu-leave-home-mode-official
description: 基于已安装的 xiaodu-control-official 编排离家场景。当用户说“出门了”“离家模式”“出门前检查一下”“帮我把家里设备关一下”时使用。这个 skill 会复用 xiaodu-control-official 的现有脚本，对小度智能屏和小度 IoT 设备执行 scene-first 的离家编排，同时在出门前汇总天气、日历和提醒事项等信息，帮助用户确认“出门前有没有漏掉什么”。不是单纯的关灯 skill，而是出门前一站式安全检查清单。
---

# xiaodu-leave-home-mode-official

## 运行边界声明

- 这是一个**编排 skill**，不直接实现底层设备控制或账户系统集成。
- 它运行时会调用同一 workspace 下、相邻目录里的依赖 skill：`skills/xiaodu-control-official/scripts/*`。
- 它默认只应读取：
  - `skills/xiaodu-control-official/scripts/*`
  - 当前 skill 自身目录下的文件
  - 用户明确允许的偏好文件（如 `XIAODU_CONTEXT.md`、`MEMORY.md`）
- 它不会主动读取未声明的本地隐私数据库；信息汇总默认通过智能屏 query 获取。
- 它默认不应读取或写入其他未声明的持久文件。
- 它不会自己索取新的外部凭证；运行时依赖的设备访问能力来自 `xiaodu-control-official` 已有配置。

## 定位

一个基于 `xiaodu-control-official` 的**离家前安全检查 orchestrator**。

它的本质不是“关灯”，而是：

> 用户说“出门了” → 系统先关闭家里电器 + 汇总出门前关键信息（天气 / 日历 / 提醒）→ 给用户一个清晰的出门前状态清单

两个并行 track，合并汇报：
- **Track A（设备关闭）**：灯 → 窗帘 → 空调/风扇 → 门锁（二次确认）
- **Track B（信息汇总）**：天气 → 日历日程 → 提醒事项

---

## 核心原则

**出门前最怕忘事。离家模式的核心价值是“让用户出门时心里有底”：哪些设备关了、今天有没有漏掉的日程或提醒。**

不默认带娱乐内容。不默认上锁（需要二次确认）。不默认控全屋（优先客厅 + 主卧）。

---

## 基于 xiaodu-control-official 事实能力全集的统一规划框架

所有离家规划都只能建立在 `xiaodu-control-official` 和本地 Mac 已有的脚本能力上。
不要加入想象中的设备族、动作或参数。

允许使用的规划 bucket 共 8 个：

1. **scene**
   - 来源：`list_scenes.sh` / `trigger_scene.sh`
2. **lights（灯光关闭）**
   - 来源：`list_iot_devices.sh` / `control_iot.sh`
3. **curtains（窗帘关闭）**
   - 来源：`list_iot_devices.sh` / `control_iot.sh`
4. **thermal comfort（空调/风扇关闭）**
   - 来源：`list_iot_devices.sh` / `control_iot.sh`
   - 仅限关闭动作，不做温度调整
5. **smart-screen speech（智能屏播报）**
   - 来源：`list_devices.sh` / `speak.sh`
6. **weather information（天气信息）**
   - 来源：`control_xiaodu.sh --command "播下今天的天气"`
7. **calendar information（备忘录信息）**
   - 来源：`bash ../xiaodu-control-official/scripts/control_xiaodu.sh --command "查看我今天的备忘录信息并播报"`
8. **alarm/reminder information（闹钟提醒）**
   - 来源：`bash ../xiaodu-control-official/scripts/control_xiaodu.sh --command "查看我今天的闹钟"`

规划顺序：

1. 先判断这次请求涉及哪些 bucket。
2. 再检查当前环境真实支持哪些 bucket。
3. 删除不支持的 bucket。
4. 把剩余 bucket 按两个并行 track 排列：
   - Track A（设备关闭）内部串行
   - Track B（信息汇总）内部串行
   - Track A 和 Track B 之间可以并行
5. Track A 和 Track B 都完成后，做产品化合并汇报。
6. 如果缺少继续执行所必需的信息，只问一个最小确认问题。
7. 执行结束后，把用户的调整吸收为后续偏好。

## 偏好记忆与复用

把用户对离家流程的调整当成可复用偏好。
如果用户修正了默认设备范围、是否上锁、优先关闭的房间等，下次应优先沿用。

至少要支持沉淀这些偏好：

- 离家默认设备范围
  - 只关灯 / 只关空调 / 只关窗帘 / 全部关
  - 客厅优先 / 主卧优先 / 全部
- 离家是否自动上锁
  - 每次问 / 直接上锁 / 不上锁
- 默认避免关闭的设备 / 房间
- 确认风格
  - 先问再做
  - 只有一个明确目标时直接执行

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

最小检查：

1. 确认 `skills/xiaodu-control-official` 存在。
2. 确认关键依赖脚本存在。
3. 如果要读日历/提醒，确认本地脚本路径可用。
4. 如果这次请求涉及 IoT，先读场景，再读 IoT 设备。
5. 如果需要智能屏播报，解析出一个可用智能屏。

### 2）优先尝试 scene-first

1. 用 `list_scenes.sh` 读取现有场景。
2. 优先寻找高匹配场景，例如：
   - 离家
   - 出门
   - 外出
   - 离开
3. 如果找到高置信度场景，优先触发。
4. scene 触发后，走完整的 Track A + Track B + 合并汇报。

### 3）没有 scene 时，进入双 track 并行 fallback

#### Track A：设备关闭（串行执行）

读取 IoT 设备后，按以下顺序执行：

1. **关灯**（读取当前状态，只对"开着"的灯发关闭命令）
2. **关窗帘**（只对"开着"的窗帘发关闭命令）
3. **关空调/风扇**（只对"开着"的空调/风扇发关闭命令）
4. **门锁上锁**（需要二次确认，未确认前不执行）

Track A 内部必须严格串行：
- 上一条命令返回后，才能发下一条
- 如果某步失败，继续执行后续步骤
- 最终汇报时说明哪些成功了、哪些失败了

#### Track B：信息汇总（串行执行）

在 Track A 启动后，同时启动 Track B：

1. **查天气**
   - `bash ../xiaodu-control-official/scripts/control_xiaodu.sh --command "播下今天的天气" ...`
2. **查备忘录（今天的日程安排）**
   - `bash ../xiaodu-control-official/scripts/control_xiaodu.sh --command "查看我今天的备忘录信息并播报" ...`
3. **查闹钟提醒**
   - `bash ../xiaodu-control-official/scripts/control_xiaodu.sh --command "查看我今天的闹钟" ...`

Track B 内部串行执行。
Track A 和 Track B 可以并行，互相不阻塞。

#### 合并汇报

两个 track 都完成后（或 Track A 完成后，Track B 仍在处理时做初步汇报），做产品化合并汇报：

1. 先说设备关闭结果
2. 再说天气/日历/提醒摘要
3. 最后提示门锁是否需要处理

### 4）门锁二次确认规则

**门锁是唯一默认不自动执行的高敏感动作。**

- 如果检测到智能门锁且用户未明确说“上锁”，先汇报其他结果，然后问：
  > 检测到有智能门锁，是否需要帮你上锁？
- 如果用户说“上锁”“锁门”，再执行上锁动作
- 如果用户说“不用”“忽略”，跳过门锁步骤

---

## 通用 leave-home 实际调用链

对于"出门了"这类高层请求：

### Track A（设备关闭）

1. `bash ../xiaodu-control-official/scripts/list_scenes.sh --server xiaodu-iot`
2. 如果有高置信度离家 scene：`trigger_scene.sh`
3. 否则：
   - `bash ../xiaodu-control-official/scripts/list_iot_devices.sh --server xiaodu-iot`
   - 对状态为"开着"的灯：`bash ../xiaodu-control-official/scripts/control_iot.sh --action turnOff ...`
   - 对状态为"开着"的窗帘：`bash ../xiaodu-control-official/scripts/control_iot.sh --action close ...`
   - 对状态为"开着"的空调/风扇：`bash ../xiaodu-control-official/scripts/control_iot.sh --action turnOff ...`

### Track B（信息汇总）

1. `bash ../xiaodu-control-official/scripts/control_xiaodu.sh --command "播下今天的天气" ...`
2. `bash ../xiaodu-control-official/scripts/control_xiaodu.sh --command "查看我今天的备忘录信息并播报" ...`
3. `bash ../xiaodu-control-official/scripts/control_xiaodu.sh --command "查看我今天的闹钟" ...`

### 合并汇报

Track A 完成后立即出初步汇报，Track B 结果出来后补全信息层。

---

## 面向用户的汇报风格

**这是离家模式最关键的一层，必须说清楚三件事：**

1. **设备侧：哪些关了、哪些没关、哪些失败了**
2. **信息侧：天气怎么样、今天有什么日程、有没有提醒**
3. **门锁侧：是否上锁或是否需要上锁**

### 推荐综合汇报口径

> 已帮你把出门模式安排好了。
> **设备这边**：灯已全部关闭，空调已关闭，窗帘已拉好。
> **出门信息**：今天下午3点有个会，晚上记得买菜。今天天气晴转多云，18-25度，出行没问题。
> **门锁这边**：需要帮你锁门吗？

### 设备失败时的汇报

> 已帮你把出门模式安排好了。灯已全部关闭，空调已关闭，不过窗帘关闭这次没成功——如果方便的话可以回头检查一下。门锁这边还没动，需要上锁吗？

### 信息层失败时的汇报

如果天气/日历/提醒读取失败：

> 已帮你把出门模式安排好了。灯已全部关闭，空调已关闭。出门信息这边今天暂时没读到日程，不过天气方面你可以放心。门锁需要帮你上锁吗？

---

## 失败处理

这个 skill 对局部失败应当有容错，但汇报必须诚实。

- **没有 scene →** 自动改走 Track A + Track B
- **灯全部已关 →** 跳过关灯步骤，不重复发命令
- **关灯失败 →** 继续窗帘和空调步骤，汇报里说明
- **天气读取失败 →** 跳过天气，继续日历和提醒，汇报里简要说明
- **日历/提醒读取失败 →** 跳过该项，继续其他步骤
- **没有智能门锁 →** 不询问门锁，直接完成汇报
- **门锁未确认 →** 不执行上锁，汇报末尾问一次

---

## 防误控规则

- 不要默认控全屋，优先客厅 + 主卧。
- 不要重复关已经关闭的设备（先读状态再决定是否发命令）。
- 门锁没有二次确认不能执行。
- 不要说"全部设备已关闭"，除非真的全部成功。
- 不要编造日程、提醒或天气内容。
- 不要在门锁之外的高敏感动作（阀门类、燃气类）上默认执行。

---

## 为什么不能重做底层

除非必要，不要绕过 `xiaodu-control-official`，因为它已经：

- 分清了 `xiaodu` 与 `xiaodu-iot`
- 带有更安全的脚本约束
- 定义了能力边界与 schema 预期
- 让排障更容易聚焦在同一依赖层

---

## 按需阅读的引用文档

- 需要看更细的编排说明时，读 `references/usage-notes.md`
- 需要看测试边界与验证项时，读 `references/test-cases.md`

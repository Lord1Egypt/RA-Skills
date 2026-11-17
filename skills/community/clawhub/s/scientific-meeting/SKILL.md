---
name: scientific-meeting
slug: scientific-meeting
displayName: 科学开会（一堂方法论 × 腾讯会议）
description: >
  基于一堂「科学开会」方法论 + 腾讯会议 tmeet CLI + 飞书多维表格，帮你把每场会议的ROI提升5-10倍。
  会前用 tmeet 创建结构化会议，会中用十原则护航+实时纪要，会后自动拉取智能纪要+转写生成ROI报告，
  并把决议拆成「每人任务清单」写入飞书多维表格中控台——团队在飞书里打勾，下次会前自动拉回看板检查。
  独有武器：会议冰山图、科学开会画布、十大原则检查、会议ROI计算器、证据等级标注、任务中控台（飞书多维表格）。
trigger:
  - 科学开会
  - 会议诊断
  - 提升会议ROI
  - 会议复盘
  - 会前准备
  - 帮我准备一个.*会
  - 复盘.*会议
  - 计算.*会议.*ROI
  - 我要开.*会
  - 刚才的会.*复盘
  - meeting-roi
  - 创建会议
  - 查看会议列表
  - 拉取会议纪要
  - 会议转写
  - 查看录制
version: "3.0.1"
author: 基于一堂「科学开会」课程（认知篇+实操篇上下）× Darwin优化，集成腾讯会议 tmeet CLI
category: productivity
tags: [会议管理, 科学开会, 一堂, ROI, 腾讯会议, tmeet, 管理基本功]
dependencies:
  tmeet: 腾讯会议命令行工具（可选，通过npm install -g @tencentcloud/tmeet@latest安装）
  feishu: 飞书企业自建应用（任务中控台必选，open.feishu.cn 开通 bitable:app + bitable:record 权限）
---

# 科学开会 · 一堂方法论 × 腾讯会议

> 本质认知：**开会是一个ROI问题——用集体讨论的时间，换业务的共识和结果。**
> 如果一场会开完没有共识、没有结果、没有下一步——这场会的ROI是负数。

本 skill 将一堂「科学开会」方法论与腾讯会议 tmeet CLI 深度集成。你可以：

1. **用 tmeet 创建会议** — 按科学开会原则预设议程、原则、目标
2. **会中实时辅助** — 记录讨论要点、检测偏离原则、管理会议节奏
3. **会后自动复盘** — 拉取 tmeet 智能纪要+转写，自动生成结构化纪要、ROI计算、决议追踪表
4. **任务中控台** — 会后把决议拆成每人任务清单写入飞书多维表格，团队打勾，下次会前拉回检查

---

## 零、tmeet 初始化

使用本 skill 前，需要完成 tmeet 的安装和登录：

```bash
# 安装 tmeet CLI
npm install -g @tencentcloud/tmeet@latest

# 登录（后台运行以捕获授权URL）
tmeet auth login 2>&1 &

# 查看登录状态
tmeet auth status
```

> 如果当前环境没有默认浏览器，请在终端手动执行 `tmeet auth login`，获取授权 URL 后在浏览器中打开完成授权。

---

## 一、会前：冰山诊断 + 画布填空 + tmeet 创建会议

### 1.1 会议冰山图（快速自检）

每次开会前，先问自己三个问题——从冰山底层往上问：

```
水面之上（可见层）
  ┌─ 流程层：议程怎么排？谁发言？多长时间？
  │
水面之下（不可见层）
  ├─ 原则层：这场会要遵守什么姿势？什么氛围？
  │   例：只讨论不决策 / 必须出结论 / 禁止看手机 / 每人必须发言
  │
  └─ 目标层：这场会要解决的核心问题到底是什么？
      如果不开会，会导致什么问题？
```

### 1.2 科学开会思考画布（会前必填）

| 步骤 | 填写内容 | 判断标准 |
|------|---------|---------|
| **目标** | 这场会要解决的核心问题？达成的具体结果？ | 能用一句话说清，且参会者都认同 |
| **原则** | 这场会遵守3-5条什么姿势？（从十大原则中选） | 原则定了就不破，会中违规立刻拉回来 |
| **关键流程** | 围绕目标+原则，设计议程和发言顺序 | 每个环节都有产出，不是"大家聊聊" |
| **ROI预估** | 投入：人数×时长×人均时薪 / 产出：共识+决策+下一步 | 投入产出比要为正 |

### 1.3 用 tmeet 创建科学会议

画布填完后，用 tmeet 创建会议：

```bash
# 创建普通会议
tmeet meeting create \
  --subject "Q3运营方向决策会" \
  --start-time "2026-07-25T14:00:00+08:00" \
  --end-time "2026-07-25T15:00:00+08:00" \
  --meeting-type 0 \
  --password 123456 \
  --format json-pretty

# 创建周期性会议（如每周复盘会）
tmeet meeting create \
  --subject "团队周复盘会" \
  --start-time "2026-07-21T10:00:00+08:00" \
  --end-time "2026-07-21T11:00:00+08:00" \
  --meeting-type 1 \
  --recurring-rule "FREQ=WEEKLY;BYDAY=MON" \
  --format json-pretty
```

**关键：** 创建会议时，将画布中的目标+原则写进会议主题或备注，会中随时可见。

---

## 二、会中：十大原则 + 实时纠偏 + tmeet 实时辅助

### 2.1 科学开会十大原则

| # | 原则 | 一句话解释 | 适用场景 |
|---|------|-----------|---------|
| 1 | **务实原则** | 不开没目标的会，不聊跟目标无关的话 | 所有会议 |
| 2 | **良性原则** | 对事不对人，讨论方案不攻击人 | 复盘会、决策会 |
| 3 | **高效原则** | 到点开始、限时发言、按时结束 | 所有会议 |
| 4 | **激发原则** | 让每个人都被听见，不等同于"自由讨论" | 头脑风暴、共创会 |
| 5 | **点燃原则** | 会议要有能量，主持人要调动状态 | 长会、战略会 |
| 6 | **投入原则** | 手机入袋/停机场，全员专注 | 决策会、复盘会 |
| 7 | **执行原则** | 每个结论必须有负责人+截止时间 | 项目推进会 |
| 8 | **共识原则** | 会中不达成共识不散会，或明确"今日不决策" | 决策会、对齐会 |
| 9 | **沉淀原则** | 讨论过程结构化记录，会中实时可见 | 所有会议 |
| 10 | **限时原则** | 每个议程设定硬时间，超时立刻暂停决议 | 所有会议 |

### 2.2 会中实时纠偏（三大触发器）

**偏离原则时 → 立刻提醒：**
"当前讨论已经偏离了本场会议的[XX原则]，我们是否需要——A.拉回来 / B.修改原则？"

**超时预警 → 限时原则触发：**
"这个议题已经超时3分钟。建议：A.现在投票决定 / B.指派负责人会后跟进，5分钟后结束本议题。"

**沉默检测 → 激发原则触发：**
"我注意到过去5分钟只有2个人发言。请[XX]说说你的看法——同意、补充、还是不同意见？"

### 2.3 会中 tmeet 操作

| 场景 | tmeet 命令 |
|------|-----------|
| **邀请成员入会** | `tmeet meeting invitees-add --meeting-id <id> --users <open_id>` |
| **查找参会人** | `tmeet contact search --keyword "张三"` |
| **踢出干扰成员** | `tmeet control kick --meeting-id <id> --users <open_id>` |
| **呼叫成员入会** | `tmeet control call --meeting-id <id> --users <open_id>` |

**注意：** 踢人操作必须先执行 `tmeet report participants` 获取会中成员列表，再从结果中选取目标成员，不得使用通讯录结果。

### 2.4 会中实时结构化记录

对每段讨论，按以下格式实时记录（可在共享文档中可见）：

```
【议题】XXX
【发言要点】
  - @张三：建议A方案，理由是……
  - @李四：担心A方案的XX风险，建议先小范围测试
【分歧点】是否先测试再全量？
【当前状态】🟡讨论中 → 待决议
```

---

## 三、会后：tmeet 拉取数据 → 纪要 + ROI + 任务中控台

### 3.1 拉取会议数据

会后，用 tmeet 获取会议数据：

```bash
# 获取已结束会议列表
tmeet meeting list-ended --start 2026-07-20T00:00:00+08:00 --end 2026-07-20T23:59:59+08:00 --compact

# 获取会议详情
tmeet meeting get --meeting-id <id> --compact

# 获取参会人列表
tmeet report participants --meeting-id <id> --compact

# 查询录制列表
tmeet record list --meeting-id <id> --compact

# 获取智能纪要（AI 自动生成的会议摘要）
tmeet record smart-minutes --meeting-record-id <record_id> --format json-pretty

# 获取转写详情（逐字稿）
tmeet record transcript-get --meeting-record-id <record_id> --format json-pretty

# 获取转写段落列表
tmeet record transcript-paragraphs --meeting-record-id <record_id> --compact

# 搜索转写内容
tmeet record transcript-search --meeting-record-id <record_id> --keyword "决策"
```

### 3.2 结构化纪要生成

拿到 tmeet 的智能纪要和转写后，按以下规则生成结构化纪要。不是流水账。只输出"决策+责任人+DDL"。去AI味。

**去AI味规则：**
- ❌ "根据会议讨论，与会人员一致认为……" —— 这是AI写的
- ✅ "@张三决定用A方案，7/20前上线。@李四有顾虑但同意先跑两周看数据。" —— 这是人写的
- ❌ "会议在友好热烈的氛围中进行……" —— 删掉
- ✅ 直接写谁说了什么、决定了什么、谁反对了什么

**证据等级标注：**

| 标记 | 含义 | 示例 |
|------|------|------|
| ✅ **已决策** | 有明确结论+负责人+DDL | ✅ @王五负责7/25前完成XX |
| 📋 **待验证** | 有方向但需要数据支撑 | 📋 假设A渠道ROI>2，需两周验证 |
| 💡 **灵感闪现** | 值得记录但本次不做 | 💡 可以考虑跟XX跨界合作 |
| ⚠️ **分歧未决** | 有不同意见，需后续讨论 | ⚠️ @A和@B对定价策略意见不一致 |

### 3.3 会议ROI快速评估（结合 tmeet 实际数据）

利用 tmeet 的实际参会人和时长数据做精准ROI计算：

```bash
# 获取实际参会人和时长
tmeet report participants --meeting-id <id> --compact
```

```markdown
【投入】
  参会人数：X人（tmeet 实际数据）
  会议时长：Xh（tmeet 实际数据）
  估算人力成本：X人 × Xh × ¥XX = ¥XXX

【产出】（来自 tmeet 智能纪要和转写分析）
  关键决策数：X个
  可执行的下一步：X个
  解决的卡点：XXX

【ROI自评】
  值 / 不太值 / 亏了
  如果重开一次，会怎么改？
```

### 3.4 任务中控台（飞书多维表格）——核心武器

把纪要里的「决策+责任人+DDL」拆成每人任务清单，写进飞书多维表格。团队所有人打开表格就能看到自己的活，做完在飞书里点状态打勾。Hermes 下次会前自动拉回看板，未完成项滚入新会议议程。**这是本 skill 的验收闭环：没有落进看板的决议 = 会白开了。**

**字段设计（脚本自动创建）：**

| 字段 | 类型 | 说明 |
|------|------|------|
| 任务 | 文本 | 动作描述，能验证的一句话 |
| 负责人 | 文本 | 人名 |
| DDL | 日期 | YYYY-MM-DD |
| 状态 | 单选 | 未开始 / 进行中 / 已完成 / 卡住 |
| 优先级 | 单选 | 高 / 中 / 低 |
| 来源会议 | 文本 | 哪场会产出的，如 08-10周会 |
| 备注 | 文本 | 上下文、链接、验收标准 |

**中控台脚本**（零依赖，`scripts/feishu_taskboard.py`，只需 python3 标准库）：

> v3.0.1 修复（2026-08-11）：① token 获取改为直接请求，兼容飞书 token 接口的顶层返回（原经 api_call 嵌套取 data 导致 KeyError）；② 文本/单选字段写入格式由 `{"text":...}`（读取格式）改为纯字符串、日期传毫秒数（原格式导致 TextFieldConvFail/SingleSelectFieldConvFail）。

```bash
# 一次性初始化：填表格链接，自动建字段
python3 scripts/feishu_taskboard.py init --url "https://xxx.feishu.cn/base/<app_token>?table=<table_id>"

# 会后：批量入库（推荐——Hermes 把拆解好的任务写成 tasks.json 一次写入）
python3 scripts/feishu_taskboard.py batch --file tasks.json

# 会后：逐条添加（任务少时）
python3 scripts/feishu_taskboard.py add --task "梳理7天内容排期" --owner "张三" --ddl 2026-08-14 --priority 高 --source "08-10周会"

# 下次会前：拉看板（默认只看未完成）
python3 scripts/feishu_taskboard.py list
python3 scripts/feishu_taskboard.py list --owner 张三
python3 scripts/feishu_taskboard.py list --json   # 给 Hermes 做结构化分析

# Hermes 代操作状态（团队打勾在飞书里点，这里用于回填/代改）
python3 scripts/feishu_taskboard.py update --record-id recXXXX --status 已完成
```

**tasks.json 格式（batch）：**
```json
[
  {"task": "梳理7天内容排期", "owner": "张三", "ddl": "2026-08-14", "priority": "高", "source": "08-10周会"},
  {"task": "联系3家奶站谈合作", "owner": "李四", "ddl": "2026-08-16", "priority": "中", "source": "08-10周会"}
]
```

**飞书侧一次性配置（用户或管理员做一次，5分钟）：**
1. open.feishu.cn 创建**企业自建应用**，开通权限：`bitable:app`（多维表格）+ `bitable:record`（记录读写）
2. 发布应用版本，等管理员审核通过
3. 建一个空**多维表格** → 分享 → 添加协作者 → 搜应用名称，把应用加为协作者
4. 把 App ID + App Secret 填进 `~/.config/feishu-task-console.json`（chmod 600；脚本 `init` 会自动写入 app_token/table_id）
5. 把表格链接发团队，让每人建一个「我的任务」筛选视图，只看到自己的活

**会前检查闭环：** 开会前 10 分钟跑 `list`，把未完成任务贴进议程「上次遗留」环节，会上 2 分钟过完；卡住的（🔴）当场升级资源。

### 3.5 决议追踪表（本地速览视图）

| 决议 | 负责人 | DDL | 状态 | 证据/备注 |
|------|--------|-----|------|----------|
| ... | @某人 | 7/20 | 🟢已落地 | 飞书文档链接 |
| ... | @某人 | 7/25 | 🟡进行中 | 周五同步进度 |
| ... | @某人 | 7/18 | 🔴卡住 | 需要XX部门配合 |
| ... | — | — | ⚪未开始 | 等上一项完成 |

**状态定义：**
- 🟢 已落地：有可验证的产出或数据
- 🟡 进行中：按计划推进，无异常
- 🔴 卡住：遇到障碍，需升级或资源支持
- ⚪ 未开始：前置条件不满足

### 3.6 深度复盘模板（冰山诊断格式）

```markdown
【会议名称】XXXX
【日期】2026-XX-XX

【冰山诊断】
  - 目标层：是否清晰？参会者是否一致理解？
  - 原则层：选了哪几条？执行了吗？哪条破了？为什么破？
  - 流程层：是否有跑题？哪个环节空转？哪个环节最值？

【ROI速算】（来自 tmeet 实际数据）
  投入：X人（tmeet 实际参会数） × Xh（实际时长） × ¥XX = ¥XXX
  产出：X个决策 / X个下一步 / 解决了XXX
  自评：值/不值。下次怎么调？

【改进动作】（必须具体到人+时间）
  - 会前：[具体动作] @负责人 DDL
  - 会中：[具体动作] @负责人 DDL
  - 会后：[具体动作] @负责人 DDL
```

---

## 四、tmeet 常用命令速查

| 场景 | 命令 |
|------|------|
| 安装 | `npm install -g @tencentcloud/tmeet@latest` |
| 登录 | `tmeet auth login 2>&1 &` |
| 登出 | `tmeet auth logout` |
| 登录状态 | `tmeet auth status` |
| 创建会议 | `tmeet meeting create --subject "主题" --start-time ... --end-time ...` |
| 更新会议 | `tmeet meeting update --meeting-id <id> --subject "新主题"` |
| 取消会议 | `tmeet meeting cancel --meeting-id <id>`（需用户确认） |
| 会议详情 | `tmeet meeting get --meeting-id <id> --compact` |
| 会议列表 | `tmeet meeting list --start ... --end ... --compact` |
| 已结束会议 | `tmeet meeting list-ended --start ... --end ... --compact` |
| 邀请成员 | `tmeet meeting invitees-add --meeting-id <id> --users <open_id>` |
| 移除成员 | `tmeet meeting invitees-remove --meeting-id <id> --users <open_id>`（需确认） |
| 受邀者列表 | `tmeet meeting invitees-list --meeting-id <id> --compact` |
| 通讯录搜索 | `tmeet contact search --keyword "姓名"` |
| 录制列表 | `tmeet record list --meeting-id <id> --compact` |
| 智能纪要 | `tmeet record smart-minutes --meeting-record-id <id>` |
| 转写详情 | `tmeet record transcript-get --meeting-record-id <id>` |
| 转写段落 | `tmeet record transcript-paragraphs --meeting-record-id <id>` |
| 转写搜索 | `tmeet record transcript-search --meeting-record-id <id> --keyword "..."` |
| 参会人列表 | `tmeet report participants --meeting-id <id> --compact` |
| 呼叫入会 | `tmeet control call --meeting-id <id> --users <open_id>`（需确认） |
| 踢出成员 | `tmeet control kick --meeting-id <id> --users <open_id>`（需确认） |
| 导出日志 | `tmeet tshoot log` |
| 反馈问题 | `tmeet tshoot feedback --category ... --intent ...`（需确认） |

---

## 五、四种典型会议的预设方案

### 5.1 决策会
- **核心原则：** 共识原则 + 限时原则 + 务实原则
- **tmeet 创建：** 单次会议，设置密码，议程写入备注
- **关键流程：** 背景同步(5min) → 方案A/B陈述(各5min) → 轮询发言(每人2min) → 投票/拍板(5min) → 确认决议+owner
- **产出标准：** 至少1个带owner+DDL的决策

### 5.2 复盘会
- **核心原则：** 良性原则 + 沉淀原则 + 执行原则
- **tmeet 创建：** 周期性会议（每周一次），开启录制
- **关键流程：** 目标回顾(3min) → 数据呈现(5min) → 根因分析(15min，用5 Whys) → 改进动作(10min) → 责任人认领
- **产出标准：** 至少1条可执行的改进动作，会后拉取录制+纪要生成复盘报告

### 5.3 头脑风暴会
- **核心原则：** 激发原则 + 点燃原则 + 投入原则
- **tmeet 创建：** 单次会议，不开启录制（鼓励自由发言）
- **关键流程：** 命题澄清(3min) → 静默写点子(5min，每人必须写) → 轮流分享不评判(15min) → 聚类投票(10min) → 选出Top3
- **产出标准：** 至少10个点子，选出Top3进入下一步

### 5.4 项目对齐会（立会）
- **核心原则：** 高效原则 + 务实原则 + 投入原则
- **tmeet 创建：** 周期性会议（每天），15分钟
- **关键流程：** 每人30-60秒：昨天做了什么→今天做什么→卡在哪（只同步，不展开讨论）
- **产出标准：** 全员知道彼此的状态和卡点，卡点单独拉小会解决

---

## 六、核心认知

> 很多人对于会议的理解只停留在流程层——因为他表面上只看到了会议流程。但从流程背后深看一层，是会议的关键原则。再深看一层，是会议最核心的目标。
>
> 开会不是一个"你怎么排议程"的问题，是一个**"你愿不愿意花团队的时间来换这个结果"**的问题。
>
> 能不开的会就不开。如果必须开，就把每一场的ROI算清楚。

**记住一句话：流程可以抄，冰山底下的东西抄不了。** 但 tmeet 可以帮你把冰山底下的数据拉出来——用录制的转写、智能纪要、参会人数据，让每一场会的ROI变得可测量、可追溯。

而「任务中控台」是 ROI 的最后一环：**没有落进看板的决议，等于这场会白开。** 会开完的验收标准 = 每个人打开飞书表格，能说出自己这周要干什么、DDL 是哪天。

---

## ⚠️ tmeet 安全规则

1. **写操作必须二次确认：** 创建/更新/取消会议、邀请/移除成员、呼叫入会、踢出成员、登出——这些操作执行前必须展示操作详情并等待用户明确确认
2. **禁止输出 Token：** 不得将 AccessToken / RefreshToken 输出到终端明文
3. **踢人来源硬约束：** 踢人必须从 `tmeet report participants` 获取，不得使用通讯录结果
4. **通讯录搜索仅限特定场景：** 仅用于会议邀请、呼叫入会、回填受邀人姓名
5. **多结果必须确认：** 搜索返回多条结果时，必须展示给用户选择，不得自行猜测
6. **飞书凭证保护：** App Secret 只存 `~/.config/feishu-task-console.json`（chmod 600），绝不输出到终端/纪要/聊天；tenant_access_token 2小时过期自动刷新，同样不打印
7. **任务写入须确认：** 批量写入飞书看板前，先把拆解出的任务清单（谁/做什么/DDL）展示给用户确认，再执行 batch

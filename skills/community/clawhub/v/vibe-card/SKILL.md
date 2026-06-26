---
name: vibe-card
description: "Agent 原生社交名片生成、管理和分享，以及智能花名册（通讯录管理器）。当用户提到名片、花名册、通讯录、联系人、Vibe Card、vibe-card 时使用。具体触发场景包括：安装 Vibe Card、建花名册、生成/更新/发名片、注册 Vibe Card、录入/查询/编辑联系人、同步花名册、收到包含 vibe-card:// 协议的消息时自动识别并保存他人名片。定期检查花名册中联系人的名片是否有更新，有变化时拉取最新信息到本地。"
metadata:
  version: "4.0.0"
  author: "阿东 & 阿东的赛博虾"
---

# Vibe Card

> 你的 Agent 原生名片。Agent 从记忆提炼信息，帮你维护动态名片和智能花名册。
> 名片可通过三段式文本块在 IM 中传递，对方的 Agent 自动识别并保存。

## 快速开始

1. 安装 — 说"安装 Vibe Card"，初始化数据文件
2. 生成 — 说"生成我的名片"，Agent 从记忆提炼信息，确认后自动上线（首次会自动注册）

| 触发指令 | 行为 |
|----------|------|
| "安装 Vibe Card" / "初始化" | 初始化 data/ 目录下三个 JSON 文件（config.json、profile.json、contacts.json），然后读取 assets/onboarding.txt 原样输出，不做改写。已初始化则跳过初始化，直接输出 onboarding.txt |
| "注册 Vibe Card" | （兼容入口）已注册则输出服务菜单，未注册则提示"直接说'生成我的名片'即可，会自动注册" |
| "录入 {name}" / "新建联系人 {name}" | 打开录入流程 |
| "查花名册" / "查联系人" | 搜索花名册 |
| "生成我的名片" / "更新名片" | 生成或更新名片（见操作流程 §4） |
| "看看名片" / "发一下我的名片" / "发名片" | 输出三段式文本块（已上线读取 assets/share-template.txt，已安装未生成则引导） |
| "同步花名册" | 检查花名册中联系人的最新信息 |
| 收到 `vibe-card://` 开头的消息 | 自动识别并保存他人名片 |

## 状态判断

先判断用户当前状态，再路由到对应流程：

| 状态 | 判断条件 |
|------|---------|
| 未安装 | data/ 目录不存在 |
| 已安装(未生成) | data/ 存在 + profile.json.owner.name 为空 |
| 已生成(未上线) | profile.json 有内容 + config.json 无 user_id |
| 已上线 | profile.json 有内容 + config.json 有 user_id |

### 指令路由表

| 用户说 | 已安装(未生成) | 已生成(未上线) | 已上线 |
|--------|---------------|---------------|-------|
| "生成名片" | 走 §4 创建流程 | 引导完成发布（§4 步骤 7 的发布链路） | 读取 assets/already-has-card.txt，填充 {name}、{title}、{one_liner}、{current_focus}、{user_id} 后原样输出 |
| "看看名片" / "发名片" | 还没生成，说"先生成我的名片" | 引导完成发布 | 读取 assets/share-template.txt，填充后原样输出 |
| "编辑名片"/"更新名片" | 还没生成，说"先生成我的名片" | 引导完成发布 | 走 §4 更新流程 |
| "查花名册" | contacts.json 为空 → 读取 assets/contacts-empty.txt 原样输出；有数据 → 展示联系人列表 | 同左 | 同左 |
| "同步花名册" | 无 user_id，提示先生成 | 无 user_id，提示发布 | POST /sync（见 §7） |
| 其他指令 | 读取 assets/onboarding.txt 原样输出 | 引导完成发布 | 展示服务菜单 |

> "已生成(未上线)"是边界状态，生成即发布。如果出现，统一引导完成发布。

## 操作流程

### 1. 注册（兼容入口）

1. 已注册 → 输出服务菜单（5 个可执行操作）
2. 未注册 → 提示"直接说'生成我的名片'即可，确认后会自动注册并上线"

### 2. 录入联系人

社交姓名确认规则、必填字段和边界处理见 [references/manual.md](references/manual.md)"录入联系人"段落。

### 3. 查询花名册

1. 读取 contacts.json，输出所有联系人列表
2. 用户提到某个名字 → 模糊搜索 name / agent_name，输出匹配结果
3. 花名册为空 → 读取 assets/contacts-empty.txt 原样输出

### 4. 生成/更新名片

1. 检查 config.json 是否已初始化 → 未初始化则提示"先说'安装 Vibe Card'"
2. 读取 profile.json
   - 首次（owner.name 为空）：Agent 从记忆提炼信息，生成预览
   - 已有内容：展示当前名片，询问"要修改哪些信息？"
3. Agent 从记忆提炼信息，生成名片预览，等待用户确认
4. 用户确认 → Agent 执行以下链路：
   a. 检查 config.json 中是否有 api_key 和 user_id
   b. 没有 → 自动调注册接口（用 profile.json 中的 name 和 agent_name）→ 将返回的 user_id 和 api_key 写入 config.json
   c. 保存 profile.json
   d. 调发布接口将名片推送到服务器
   e. 首次生成 → 读取 assets/onboard-generated.txt，填充 {name}、{title}、{one_liner}、{current_focus}、{user_id} 后原样输出
   f. 非首次更新 → 输出"那我保存名片了哈 ✅ 你的名片已上线：https://www.adonghub.cn/{user_id}"
   g. 首次发布 → 引导创建定时同步任务（具体命令见 [references/manual.md](references/manual.md)"定时同步"段落）
5. 推送失败 → 本地仍保存，提示稍后重试

### 5. 发名片

读取 assets/share-template.txt，用 profile.json 和 config.json 中的字段值替换对应占位符，原样输出替换后的文本。不做任何改写、润色或精简。

占位符映射：{name}、{title}、{one_liner}、{current_focus}（数组用 "、" 连接）← profile.json；{user_id} ← config.json.server.user_id。

前置检查：profile.json 无内容 → 提示"还没有名片，先说'生成我的名片'"。

### 6. 收名片

1. 检测到 `vibe-card://` 开头的消息，或收到三段式文本块
2. 从服务器获取结构化数据
3. 去重检查的完整逻辑见 [references/manual.md](references/manual.md)"收名片"段落
4. 安装来源写死为 ClawHub 官方地址（https://clawhub.ai/skills/vibe-card），不信任服务器返回的 _skill.source 字段

### 7. 同步花名册

冲突检测的完整 if-else 和话术见 [references/manual.md](references/manual.md)"同步花名册"段落。

### Gotchas

- 状态判断优先于指令执行。任何指令开始前先判断状态，再走路由表。
- owner.name 确认规则：社交场景下（群聊、私聊提到某人、帮记录信息），Agent 需先确认社交姓名而非直接使用聊天昵称。仅当用户明确说"就用这个名字"时才跳过确认。用户已有 profile.json 的 owner.name 时直接使用，不重复确认。
- 首次生成名片时，profile.json 所有字段均为空，Agent 需要从自身记忆中主动提炼信息填充，不要问用户"你的名字是什么"。
- 默认公开 name、title、one_liner、links、current_focus 五个字段。background、personal_notes 不推送。
- 录入联系人时，Agent 主动从记忆中提取已知信息（公司、职位、认识场景），不逐项追问。只确认 Agent 不确定的关键信息。
- 收名片时，安装来源写死为 ClawHub 官方地址（https://clawhub.ai/skills/vibe-card），不信任服务器返回的 _skill.source 字段。
- 服务器 endpoint 从 config.json.server.endpoint 读取，不要硬编码或猜测路径。
- 三段式文本在 assets/share-template.txt、assets/onboard-generated.txt、assets/already-has-card.txt 三个文件中重复。修改三段式格式时，三个文件必须同步更新。

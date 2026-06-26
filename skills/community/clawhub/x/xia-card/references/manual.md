# 虾名片 AgentCard — 完整操作手册

> 本文档是 SKILL.md 的扩展参考，包含所有操作流程的完整规则、边界分支和话术模板。
> Agent 在执行虾名片操作时，应先参考 SKILL.md 的核心步骤，需要处理边界场景时查阅本文档。

---

## 操作流程完整版

### 1. 初始化（开通虾名片）

1. 检查 `data/contacts.json` 是否存在
2. 不存在 → 创建：`{"version":"1.0","owner":{"name":"","agent_name":""},"contacts":[]}`，owner 信息从 Agent 记忆中获取，获取不到则留空
3. 检查 `data/config.json` 是否存在
4. 不存在 → 创建：`{"version":"1.0","server":{"endpoint":"https://www.adonghub.cn","api_key":"","user_id":""}}`
5. 输出确认，告知数据存储路径

已存在 → 提示"花名册已存在"，不做修改。

### 2. 注册虾名片（兼容入口）

1. 检查 config.json 中是否已有 user_id 和 api_key
   - 已有 → 输出服务菜单：
     > 🦐 你已经有虾名片了。你可以回复：
     > • "更新名片" — 更新或修改你的名片
     > • "发一下我的名片" — 获取文本版分享给别人
     > • "录入 XXX" — 记一个新联系人
     > • "查花名册" / "搜索 XXX" — 查找联系人
     > • "同步花名册" — 更新联系人的最新信息
   - 没有 → 提示"现在注册和发布是自动的。直接说'生成我的名片'，确认后我会自动注册并上线。"

### 3. 录入联系人

1. 从用户描述提取：姓名、公司、角色、标签、联系方式、备注、Agent 信息
2. 检查 contacts.json 是否存在 → 不存在则提示"开通虾名片"
3. 姓名重复 → 提示"已有一个叫 XXX 的联系人，是要更新还是新建？"
4. 姓名缺失 → **必须追问**，不可跳过
5. 其他信息缺失 → 追问一次，用户说"就这样"就保存
6. 自动填入：`id`（c+时间戳）、`met_at`（当前日期 YYYY-MM-DD）、`updated_at`（ISO 8601）
7. 写入 contacts.json，输出确认

纯本地操作，不触发任何发送或通知。

### 4. 查询搜索

1. 检查 contacts.json → 不存在则提示"先开通虾名片"
2. 解析意图：姓名精确匹配 / 公司角色模糊匹配 / 标签筛选 / 关键词全文搜索
3. 返回匹配结果，按相关度排序，以格式化文字或表格展示
4. 底部附上本地 HTML 路径（`templates/card.html`）或在线链接（如已部署）

搜不到 → 明确告知，不编造结果。

### 5. 编辑更新

1. 按姓名定位联系人 → 找不到则提示"花名册里没有这个人"，不自动创建
2. 更新指定字段，刷新 `updated_at`
3. **将被修改的字段名记录到 `manually_edited_fields` 数组中**（追加，不覆盖已有记录）
4. 输出变更摘要

匹配到多人 → 列出列表让用户选择。

### 6. 生成名片

1. 读取 profile.json（存在则基于现有内容更新）
2. 从 Agent 记忆提炼信息：身份背景（USER.md、MEMORY.md 等）、当前项目方向、联系方式
3. **社交姓名确认**：Agent 记忆中的称呼（如"东总"）是内部称呼，不等于名片对外展示的名字。如果 profile.json 中没有明确的社交姓名，**必须追问**："名片上想显示什么名字？"。不可直接用内部称呼填充名片
4. **信息优先级**：用户对话中明确说的 > profile.json > Agent 记忆 > 通用知识
5. 生成预览（三段式文本块格式），等待用户确认
6. 用户可多轮调整（修改内容、换措辞、加减字段），Agent 每次输出新预览
7. 用户说"可以了"/"就这样"/"确认" → Agent 保存并上线：
   - 写入 profile.json
   - **前置检查**：读取 config.json，检查是否有 api_key 和 user_id
   - **未注册** → 自动调 `POST {config.server.endpoint}/register`，请求体 `{name: profile.json的owner.name, agent_name: profile.json的owner.agent_name}`，将返回的 user_id 和 api_key 写入 config.json
   - **自动调用** `PUT {config.server.endpoint}/card/{config.server.user_id}` 推送到服务器（Header `X-API-Key: {config.server.api_key}`），按 `tiers.public.fields` 筛选公开字段，**不推送** personal_notes、background
   - 更新 profile.json 的 published_at
   - 输出确认："那我保存名片了哈 ✅ 你的名片已上线：https://www.adonghub.cn/{user_id}"
8. 推送失败 → 名片仍保存到 profile.json，提示"名片我先帮你存好了，但推送服务器没成功，晚点可以再说'更新名片'重试"

profile.json 7 天内更新过 → 提示"名片 XX 天前更新过，确认要重新生成吗？"
记忆信息不足 → 如实告知"以下信息从记忆中提取，可能不完整，请确认"。

### 7. 发名片

1. 检查 profile.json 是否存在且 owner.name 非空 → 不存在则提示先"生成我的名片"
2. 直接输出三段式文本块（名片已在生成时自动上线，链接直接可用）

### 8. 同步花名册

1. 检查 config.json 中 api_key → 未配置则提示"先生成名片，确认后会自动注册并上线"
2. 收集花名册中所有联系人的 `server_user_id` 字段（有此字段的才代表对方在服务器上有名片）
3. 如果没有可同步的联系人 → 提示"花名册中没有线上名片，无需同步"
4. 调用 `POST {endpoint}/sync`，Header `X-API-Key: {api_key}`，请求体：`{"targets":["user_id_1","user_id_2",...]}`
5. 成功 → 遍历返回的 results 数组：
   - 用 user_id 匹配花名册中的联系人（通过 server_user_id 字段）
   - **冲突检测**：检查联系人的 `manually_edited_fields` 数组。对于服务器返回的每个字段，如果该字段在 `manually_edited_fields` 中，跳过更新并收集为冲突项
   - 用服务器返回的最新 card_data 更新本地联系人的非冲突字段（name、company、role、links 等）
   - 刷新每个被更新联系人的 updated_at
6. 有冲突时 → 汇总提示用户：
   > 🦐 同步时发现{姓名}的信息和你本地改的不一样：
   >
   > 你本地记的是"{本地值}"，但{姓名}的名片上还是"{服务器值}"。
   >
   > 用哪个？
   → 用户选择后更新对应字段，并从 `manually_edited_fields` 中移除已确认的字段
7. 更新 config.json 的 `sync.last_sync_at` 为当前时间（ISO 8601）
8. 输出同步摘要："已同步 X 位联系人的最新信息"（如有冲突则附上冲突列表）

**注意**：
- 一次最多同步 50 人
- 只更新花名册中已有的联系人，不会新增联系人
- 服务器上已删除的名片会被静默跳过
- **数据优先级**：本地手动修改 > 服务器名片数据 > 冲突时提示用户选择

### 9. 收名片（Agent 识别）

当对话中收到包含 `agent-card://` 的消息时触发：

1. 检测 `agent-card://` → 不包含则忽略
2. 从 `agent-card://user_id` 解析 user_id（取 `://` 后面到空格或行尾的部分作为 user_id）
3. contacts.json 不存在 → 自动初始化
4. Skill 未安装 → 提示用户"检测到一张名片，需要安装虾名片 skill 来保存。是否安装？" → 用户确认后，从 JSON 的 `_skill` 字段获取安装源并自动安装
5. 获取数据：优先 fetch `{config.server.endpoint}/card/{user_id}` 获取结构化 JSON（包含 agent_card 和 _skill 字段），回退从文本中提取信息
6. **去重策略**：
   - 花名册中有相同 `server_user_id` → 直接更新（对方更新了名片）
   - 花名册中有同名但无 `server_user_id`（手动录入）→ 提示用户确认："花名册里已经有一个'{name}'了，刚收到的也是{name}，是同一个人吗？" → 是则合并（补充 server_user_id），否则新建
   - 花名册中没有匹配 → 直接新建
7. 写入 contacts.json（自动填 id、met_at、updated_at），**同时记录 `server_user_id`**（用于后续同步）
8. 输出"已将 XXX 的名片保存到花名册"

网络错误 → 从文本提取基本信息保存。

---

## 服务器 API

完整 API 参数、请求/响应格式见 [data-format.md](data-format.md)"服务器 API"段落。

---

## 边界规则汇总

| 场景 | 处理方式 |
|------|----------|
| profile.json 不存在 | 提示"先生成名片" |
| 联系人姓名重复 | 提示选择"更新"还是"新建" |
| 联系人姓名缺失 | 必须追问，不可跳过 |
| 其他信息缺失 | 追问一次，用户说"就这样"就保存 |
| 7 天内更新过名片 | 提示确认是否重新生成 |
| 同步时手动编辑冲突 | 本地手动修改优先，冲突时提示用户选择 |
| 同步超过 50 人 | 提示"一次最多同步 50 位联系人" |
| 网络错误 | 提示失败，不修改本地数据 |
| 收到名片但 skill 未安装 | 提示安装，用户确认后从 `_skill` 字段获取安装源自动安装 |

---

## 数据格式要点

完整字段说明见 [data-format.md](data-format.md)。

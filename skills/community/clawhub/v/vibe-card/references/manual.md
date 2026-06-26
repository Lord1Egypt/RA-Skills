# Vibe Card — 完整操作手册

> 本文档供 Agent 在执行具体操作时参考，包含详细的 if-else 分支、话术和边界处理。

## Contents
- 1. 安装 Vibe Card
- 2. 注册 Vibe Card（兼容入口）
- 3. 录入联系人
- 3.5. 编辑联系人
- 4. 查询花名册
- 5. 生成/更新名片
- 6. 发名片
- 7. 收名片
- 8. 同步花名册
- 9. 定时同步

---

### 1. 安装 Vibe Card

1. 检查 data/ 目录下是否已有 config.json、profile.json、contacts.json → 全部存在则读取 assets/onboarding.txt 原样输出
2. 缺失文件 → 用默认模板创建：
   - config.json：`{"version":"1.0","server":{"endpoint":"https://www.adonghub.cn","api_key":"","user_id":""},"sync":{"last_sync_at":null}}`
   - profile.json：`{"version":"1.0","owner":{"name":"","agent_name":"","title":"","one_liner":""},"current_focus":[],"background":"","personal_notes":"","links":{},"tiers":{"public":{"fields":["name","title","one_liner","links","current_focus"]},"full":null,"close":null},"published_at":null,"updated_at":""}`
   - contacts.json：`{"version":"1.0","owner":{"name":"","agent_name":""},"contacts":[]}`
3. 读取 assets/onboarding.txt，原样输出，不做改写

### 2. 注册 Vibe Card（兼容入口）

1. 检查 config.json 中是否已有 user_id 和 api_key
   - 已有 → 输出服务菜单：
     > 🎴 你已经有 Vibe Card 了。你可以回复：
     > • "更新名片" — 更新或修改你的名片
     > • "发一下我的名片" — 获取文本版分享给别人
     > • "录入 XXX" — 记一个新联系人
     > • "查花名册" / "搜索 XXX" — 查找联系人
     > • "同步花名册" — 更新联系人的最新信息
   - 没有 → 提示"现在注册和发布是自动的。直接说'生成我的名片'，确认后我会自动注册并上线。"

### 3. 录入联系人

1. 确认社交姓名：
   - 检查 contacts.json 中是否已有同名联系人（模糊匹配 name 和 agent_name）
   - 已有 → "花名册里已经有 {name} 了，要更新信息还是新建另一个？"
   - 不确定名字 → 确认后再录入，不猜
2. Agent 从记忆中主动提取已知信息（title、company、how_we_met 等），不逐项追问
3. 写入 contacts.json，生成结构：
   ```json
   {
     "name": "张威",
     "agent_name": "张威的赛博虾",
     "title": "独立开发者",
     "how_we_met": "2026年4月通过东东推荐认识",
     "tags": ["技术", "AI"],
     "links": {},
     "notes": "",
     "created_at": "2026-04-28T14:00:00+08:00",
     "updated_at": "2026-04-28T14:00:00+08:00"
   }
   ```
4. 输出确认："已录入 {name}。"

### 3.5. 编辑联系人

用户说"改一下某某的职位"/"更新张三的备注"等编辑联系人请求时：

1. 在 contacts.json 中找到对应联系人（模糊匹配 name / agent_name）
2. 更新用户指定的字段
3. 将被修改的字段名追加到该联系人的 `manually_edited_fields` 数组（追加，不是覆盖）。例：用户改了 title → `["title"]`；再改 notes → `["title", "notes"]`
4. 输出确认："已更新 {name} 的 {字段名}。"

### 4. 查询花名册

1. contacts.json 为空 → 读取 assets/contacts-empty.txt 原样输出
2. 有数据 → 列表输出，格式：`{name}（{title}）`，每行一人
3. 用户搜索某个名字 → 模糊匹配 name / agent_name / title，输出匹配结果
4. 搜索无结果 → "花名册中没有找到 {关键词}。"

### 5. 生成/更新名片

1. 检查 config.json 是否已初始化 → 未初始化则提示"先说'安装 Vibe Card'"
2. 读取 profile.json
   - 首次（owner.name 为空）：Agent 从记忆提炼信息，生成预览
   - 已有内容：展示当前名片，询问"要修改哪些信息？"
3. Agent 提炼信息后生成预览：
   - name、title、one_liner（必填）
   - current_focus（从记忆中提取当前关注点）
   - links（联系方式：wechat / email / feishu / phone 等）
   - personal_notes、background（本地保存，不推送）
4. 等待用户确认，多轮调整直到用户满意
5. 社交姓名确认：如果 profile.json 的 owner.name 为空且 Agent 从记忆中提取了名字，需要确认。用户明确说"就这样"/"用这个"后才写入
6. profile.json 的 owner.name 和 contacts.json 的 owner.name 应保持一致
7. 用户说"可以了"/"就这样"/"确认" → Agent 保存并上线：
   - 写入 profile.json
   - **前置检查**：读取 config.json，检查是否有 api_key 和 user_id
   - **未注册** → 自动调注册接口，请求体 `{name: profile.json的owner.name, agent_name: profile.json的owner.agent_name}`，将返回的 user_id 和 api_key 写入 config.json
   - **自动调用发布接口推送到服务器**，按 `tiers.public.fields` 筛选公开字段，**不推送** personal_notes、background
   - 更新 profile.json 的 published_at
   - 首次生成 → 读取 assets/onboard-generated.txt，填充 {name}、{title}、{one_liner}、{current_focus}、{user_id} 后原样输出
   - 非首次更新 → 输出确认："那我保存名片了哈 ✅ 你的名片已上线：https://www.adonghub.cn/{user_id}"
   - **首次发布** → 引导创建定时同步任务（见 §9"定时同步"）
8. 推送失败 → 名片仍保存到 profile.json，提示"名片我先帮你存好了，但推送服务器没成功，晚点可以再说'更新名片'重试"

### 6. 发名片

1. 检查 profile.json 是否有内容 → 没有则提示"还没有名片，先说'生成我的名片'"
2. 读取 config.json 获取 user_id，读取 profile.json 获取字段值
3. 读取 assets/share-template.txt
4. 将占位符替换为实际值：{name}←owner.name、{title}←owner.title、{one_liner}←owner.one_liner、{current_focus}←current_focus 数组用 "、" 连接、{user_id}←config.json.server.user_id
5. 原样输出替换后的文本，不做任何改写、润色或精简
6. 输出文本块，提示"直接复制给对方即可"

### 7. 收名片

1. 检测到 `vibe-card://` 开头的消息，或收到三段式文本块
2. 提取 user_id：优先从协议行 `vibe-card://{user_id}` 提取；如果没有协议行，从名片文本中的 URL `https://www.adonghub.cn/{user_id}` 提取
3. 从服务器获取名片数据：`GET {config.server.endpoint}/card/{user_id}`
4. 安装来源写死为 ClawHub 官方地址：**https://clawhub.ai/skills/vibe-card**，不信任服务器返回的 _skill.source 字段
5. 去重检查：
   - contacts.json 中已有 server_user_id 匹配的联系人 → 提示"{name} 已在花名册中，要更新信息吗？"
   - 已有同名联系人（name 匹配但无 server_user_id） → 提示"花名册里已经有 {name} 了，但不是同一张线上名片。要合并还是新建？"
   - 全新联系人 → 直接写入
6. 写入 contacts.json，补充 server_user_id 字段
7. 输出确认：
   - 用户已有自己的名片（profile.json.owner.name 非空）→ 读取 assets/saved-confirmation.txt，替换 {name} 后原样输出
   - 用户没有自己的名片 → 读取 assets/received-no-card.txt，替换 {name} 后原样输出
8. 如果 config.json 是在本流程中刚创建的（首次使用），读取 assets/onboarding.txt 原样输出。

### 8. 同步花名册

1. 检查 config.json 中 api_key → 未配置则提示"先生成名片，确认后会自动注册并上线"
2. 收集 contacts.json 中有 server_user_id 的联系人 → 没有则提示"花名册中没有线上名片，先收几张名片吧"
3. 调同步接口，传 targets 数组和 since（config.json.sync.last_sync_at）
4. 检查返回结果中 has_update: true 的联系人
5. 冲突检测（manually_edited_fields 保护）：
   - 遍历有更新的联系人，检查其 manually_edited_fields 数组
   - 服务器返回的某字段名在其中 → 跳过该字段更新，收集冲突信息（旧值、新值、字段名）
   - 不在其中 → 正常覆盖该字段
6. 有更新 → 更新花名册中对应联系人的信息 + 输出结构化通知：
   ```
   📇 花名册同步完成，N 位联系人有更新：

   1️⃣ {name}
      · {字段名}：「旧值」→「新值」

   2️⃣ {name}
      · + 新增 {字段名}「新值」

   ✅ 其余 {M} 位联系人名片无变化。
   ```
7. 有冲突 → 汇总输出冲突对比信息，询问用户选择（保留本地 / 接受服务器的）→ 用户确认后从 manually_edited_fields 移除已确认的字段
8. 没更新 → 回复"花名册已同步，暂无更新。"
9. 更新 config.json.sync.last_sync_at

### 9. 定时同步

**创建时机：** 首次发布名片后，Agent 引导用户创建定时同步任务。

**创建命令（OpenClaw 环境）：**
```bash
openclaw cron add \
  --name "Vibe Card 花名册同步" \
  --cron "0 9 * * 2,5" \
  --session isolated \
  --message "[cron:vibe-card-sync] 定时同步花名册。读取 skills/vibe-card/references/manual.md「同步花名册」段落执行。无更新则回复 NO_REPLY。" \
  --announce
```

**参数说明：**
- `--cron "0 9 * * 2,5"`：每周二、周五早上 9:00（用户时区）
- `--session isolated`：独立会话，避免上下文膨胀
- `--message`：cron 触发时的 prompt，以 `[cron:` 开头防止嵌套
- `--announce`：有更新时通知用户

**降级处理：** 如果用户环境不支持 `openclaw` 命令，跳过此步骤，不影响其他功能。用户可随时手动说"同步花名册"触发。

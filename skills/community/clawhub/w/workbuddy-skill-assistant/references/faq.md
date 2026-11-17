# FAQ · WorkBuddy 使用常见问题集中索引

> **遇到问题先来这里。** 每个问题按 **现象 → 原因 → 怎么修 → 验证** 四步走，照着做就行。
> 若问题与连接器配置细节相关，详见 `config-templates/connector-quick-ref.md`（连接器权威入口）。
> 常见问题已汇总到此处；需要更深入排查时，转到 `system-scan.md`（排查专线）。

---

## 1. 连接器

### Q: 所有连接器都显示 disconnected

**现象**：打开 WorkBuddy 后所有已连接的连接器全部断开。

**诊断**：`python scripts/usage_diag.py` → 看 proxy_status 是否正常。

**修复**：先重启 WorkBuddy 客户端——**80% 的情况是它没睡醒**，重启即好。

**验证**：重跑 `usage_diag.py`，确认连接器状态恢复为 connected。

---

### Q: 单个连接器 disconnected

**现象**：某个连接器断开了，其他正常。

**诊断**：通常是授权过期或 token 刷新失败。

**修复**：在 UI 中重新登录/授权该连接器。

**验证**：状态变为 connected 即为修复。

---

### Q: 新的 MCP 连接器配置了但不生效

**现象**：在 mcp.json 中添加了新条目，但 WorkBuddy 不识别。

**诊断**：检查 JSON 语法是否合法；确认文件路径为 `~/.workbuddy/mcp.json`（注意不是 `.mcp.json`，无前置点）。

**修复**：用 jsonlint 校验 → 修正语法 → 在连接器管理页面右上角点击"Trust"启用。配置细节见 `config-templates/connector-quick-ref.md` §连接器基础规则。

**验证**：连接器列表中可见新条目，状态为 connected。

---

## 2. 自动化任务

### Q: 自动化任务不执行

**现象**：已创建的自动化任务到时间了没触发。

**诊断**：`automation_update mode="list"` 查看 status 是否为 ACTIVE。

**修复**：若 status 是 PAUSED → `automation_update mode="update" id="xxx" status="ACTIVE"`。若已 ACTIVE 仍不跑，八成是 rrule 写错——对照 `config-templates/automation-templates.md` 文末的「rrule 速查」。

**验证**：下次计划时间到达后检查是否执行。

---

### Q: 自动化建了一堆但都没跑

**现象**：多个自动化任务全部不触发。

**诊断**：逐一检查 status → 检查 rrule 格式是否合法 → 检查 validFrom/validUntil 是否在有效期内。

**修复**：status 改为 ACTIVE，rrule 修正，确保时间范围覆盖当前。

**验证**：等下一次 scheduled time，查看执行日志。

---

### Q: 自动化执行时报错

**现象**：任务触发后没有产出结果。

**诊断**：查看 `automation_runs` 表的历史记录；检查 prompt 是否引用了不可用的工具或路径。

**修复**：修改自动化 prompt，确保所有引用的文件/工具可访问。

**验证**：手动触发一次，确认产出。

---

## 3. Skill 管理

### Q: skillhub install 后 skill 不生效

**现象**：用 `skillhub install <slug>` 安装了 skill，但 WorkBuddy 不识别。

**诊断**：检查 skill 是否装到了正确目录（Agent 只加载 `~/.workbuddy/skills/`）。

**修复**：必须带 `--dir ~/.workbuddy/skills` 重新安装；或手动把 skill 目录从 `./skills/` 移动到 `~/.workbuddy/skills/`。

**验证**：在对话中说触发词，确认 skill 被加载。

---

### Q: skillhub publish 报"不支持的文件类型"

**现象**：`skillhub publish .` 报 "禁止上传二进制文件"（如 `__pycache__/*.pyc`）。

**诊断**：本机 Python 在 skill 目录下生成了 `__pycache__/`。

**修复**：
1. 设置环境变量 `PYTHONDONTWRITEBYTECODE=1` 防止再生
2. 删除 `__pycache__/` 目录
3. 用 `skillhub-auto-publish` skill（内置 pyc 排除）重新发布

**验证**：dist 目录不含任何 `__pycache__/` 或 `.pyc` 文件。

---

### Q: skill 升级后功能异常

**现象**：升级某个 skill 后出现报错或行为变化。

**诊断**：对比升级前后的 SKILL.md diff；检查新版本是否引入了不兼容的依赖。

**修复**：
1. 备份旧版本：`mv old_dir old_dir.bak.timestamp`
2. 回退：用旧版本替换
3. 或按新版修正调用方

**验证**：重新触发该 skill，确认功能恢复。

---

## 4. 文档与配置

### Q: AI 回答质量差 / 总是答非所问

**现象**：AI 不了解你的角色和偏好，回答偏泛或风格不对。

**诊断**：检查 `~/.workbuddy/SOUL.md` 是否存在且内容 ≥200 字。

**修复**：用使用助理的"初始化引导"完成 SOUL.md 和 USER.md 的设置。

**验证**：设置后重新问同样的问题，对比回答质量。

---

### Q: mcp.json 报 JSON 解析错误

**现象**：WorkBuddy 启动时报配置错误。

**诊断**：用 jsonlint 或 `python -m json.tool mcp.json` 检查。

**修复**：修正 JSON 语法（常见：尾部逗号、注释、引号不匹配）。

**验证**：JSON 可正常解析。

---

### Q: 每次对话都要重新介绍自己

**现象**：AI 不记得你的角色和偏好。

**诊断**：USER.md 和 SOUL.md 是否都已配置。

**修复**：确保两个文件都存在且内容 ≥200 字；USER.md 至少含 "称呼、角色、行业侧重、城市" 四项。**不知道怎么写才完整准确？** 看 `config-templates/soul-setup-template.md`——里面有 ✅ 一个填好的好范例（投资经理+数学教授范式）和 ❌ 反面例子（只有姓名+一句职业为什么不够），照着填即可，一次到位。

**验证**：开新对话，不重新介绍自己，看 AI 是否知道你的偏好。

---

## 5. 响应质量

### Q: AI 回答太啰嗦

**现象**：每次回复都很长，信息密度低。

**诊断**：检查 SOUL.md 的"说话方式"章节是否指定了简洁风格。

**修复**：在 SOUL.md 中添加类似 "回答精炼，先结论后分析" 的表述。

**验证**：重新问一个问题，对比回复长度和信息密度。

---

### Q: skill 加载后响应很慢

**现象**：触发某个 skill 后 AI 响应明显变慢。

**诊断**：该 skill 的 SKILL.md 或 references/ 文件是否过大（>500行或 >10个参考文件）。

**修复**：
1. 检查 skill 是否遵循 progressive disclosure（主文件短，参考文件按需加载）
2. 关闭不必要的 MCP 连接器（每个活跃 MCP 消耗上下文）
3. 减少同时激活的 skill 数量

**验证**：重新触发，对比响应时间。

---

### Q: 上下文超限 / 对话中断

**现象**：长对话后 AI 开始忘记前面的内容，或直接报错。

**诊断**：累计上下文超过了模型窗口上限（常见原因是过多 MCP 同时连接或 skill 加载了超大 references）。

**修复**：
1. 开新对话继续
2. 检查并关闭不用的 MCP 连接器
3. 精简 skill 的 references/ 内容

**验证**：新对话中同样任务能否正常完成。

---

## 6. 发布与维护

### Q: `skillhub publish` 失败

**现象**：发布到 SkillHub 时报各种错误。

**诊断**：按常见原因排查：
- dist 路径文件数 >200 → 精简
- 含 `__pycache__/` 或二进制文件 → 清理
- SKILL.md frontmatter 字段缺失 → 按 01-frontmatter-spec.md 补全
- 硬编码绝对路径 → 改为相对路径

**修复**：用 `skill-publish-audit` 做 10 维度发布就绪检查，逐项修正。

**验证**：audit 全绿后重新发布。

---

### Q: 安装 skill 时提示"不支持的源"

**现象**：从某处装 skill 时提示来源不被信任。

**诊断**：检查安装源是否在允许列表内。

**修复**：优先从 SkillHub 官方市场安装（`skillhub install`），或从 WorkBuddy 推荐市场安装。

**验证**：改用推荐源重新安装。

---

### Q: 报告顶部提示"运行副本版本异常"（脚本 vX / 发布 vY 不一致）

**现象**：主动态报告/版本自检显示运行副本与发布版本不一致。

**诊断**：本 skill 安装目录（`SKILL.md` 所在目录）里的脚本版本与 `manifest.json`（或源目录）不一致——通常是部署时漏同步了 `scripts/` 或只改了源没重装。

**修复**：用 `scripts/publish_build.py` 重建发布包 → 把 `dist/workbuddy-skill-assistant/` 整个重新同步到本 skill 安装目录（覆盖 SKILL.md + scripts + references）。注意安装目录名可能是 `workbuddy-skill-assistant`（按 name 装）或 `workbuddy-skill-assistant__skillhub`（skillhub 装），以实际 `SKILL.md` 所在目录为准。

**验证**：重跑 `python scripts/usage_diag.py --version`，与 `SKILL.md` frontmatter 的 `version` 一致。

---

### Q: 升级后 state.md 需要手动改吗？

**现象**：升级到新版本后担心状态文件不兼容。

**诊断**：本 skill 状态文件带 `schema_version`；缺字段时会自动迁移（先备份 `state.md.bak` 再补齐）。

**修复**：无需手动改。若担心，先备份 `state.md` 再重装即可。

**验证**：`state.md` 首行为 `schema_version: 6`，且用户阶段/战绩/达标字段存在。

---

### Q: 不懂某个功能怎么用

**现象**：想用某个 WorkBuddy 功能但不会配置。

**诊断**：先在 FAQ 搜索对应分类；仍不会则用"最佳实践达标检查"或 `deep-dive.md` 获得分步指导。

**修复**：参考 `references/config-templates/` 中的配置模板，复制后按注释修改。

**验证**：按要求配置后功能正常运行。

---

## 7. 边界与适用场景（什么时候该用 / 不该用本顾问）

### Q: "帮我看看这个 skill 值不值得装"——走本顾问吗？

**答**：不必。这是单次咨询，直接问即可（agent 会查 skillhub 汇总来源/版本/风险）。本顾问的 `install_skill` 动作是由**达标检查未达标项**触发的系统性推荐，不是单次安装的入口。

---

### Q: "达标检查"和"skill 体检"（skill-check-pro）有什么区别？

**答**：两个不同对象。**达标检查**（本 skill 的核心检查）检查的是**你的使用底座与习惯**——自动化、连接器、记忆、skill 精简等 12 条核心项是否做到位；**skill 体检**（skill-check-pro）检查的是**skill 本身的建设质量**——frontmatter、触发词、死链、发布就绪。一个是"你用对了吗"，一个是"它写好了吗"。

---

### Q: 我是刚装 WorkBuddy 的新手，为什么只让我做初始化引导，不给效率建议？

**答**：这是刻意设计的三级分层。初级用户先打地基（画像 + 首个自动化 + 连接器），跑全量清单只会制造噪音。完成初始化引导后，下轮检查自动升入进阶，开始接收 L1+L2 核心检查。

---

### Q: 我想给自己的 skill 做发布前体检，本顾问能代劳吗？

**答**：不能，这是刻意边界。本顾问服务"WorkBuddy **使用者**"，不服务"skill 开发者"。发布体检交 skill-check-pro / skill-publish-audit 等专用 skill（达标检查的 C-skill-02 会推荐你装）。

---

## 8. 上手与使用（新手必读）

### Q: 模块有点多，我该从哪开始？

**答**：不用一次搞懂全部。记住递进关系——**打底 → 审计 → 精选 → 进化**：
- **初级**只走系统扫描与初始化引导（扫描 + 判定 + 初始化引导 + 系统检查），把地基打好；
- 完成引导后自动升**进阶**，解锁达标检查 + skill 精选（核心服务）；
- **高级**再解锁全量 12 条核心检查。
一句话：说"使用助理"，跟着引导走即可，系统会自动按你的阶段给对应服务，不必自己判断该用哪个功能。

### Q: 触发词太多记不住，不知道该说啥？

**答**：记住一句**万能口令**："**使用助理**"。此外这些口语化说法都能触发：
- "检查一下 workbuddy" / "workbuddy 体检" / "我的配置有问题吗"
- "workbuddy 怎么用" / "怎么更高效用 workbuddy"
- "推荐 skill" / "装什么 skill" / "我的 skill 有什么"
不确定时就说"使用助理"，剩下的交给三级分层自动判定。

### Q: 首次使用到底该做什么？

**答**：两步起手：
1. 说"**使用助理**" → 自动扫描 + 判定阶段 + 带你完成初始化引导（让 AI 记住你是谁）；
2. 说"**启用主动监护**" → 一键建好"每日 11:00 主动检查"自动化。
之后就不用管了——每天自动检查，有问题才提醒你。

### Q: 报错 / 提示看不懂怎么办？

**答**：本 skill 的所有诊断提示都遵循「**现象 → 原因 → 怎么修 → 验证**」四步结构，照着做即可。常见场景：
- **连接器 disconnected** → 重启 WorkBuddy（80% 情况是它没醒）或重新授权；
- **自动化不执行** → 检查 status 是否 ACTIVE；
- **配置 JSON 报错** → 用 jsonlint 校验语法。
仍看不懂，直接把报错原话贴给 AI，让它对照 `system-scan.md` 的分级修复建议定位。

---

> **提示**：以上 FAQ 为集中索引。需要更深入排查时，见 `system-scan.md`（排查专线）。

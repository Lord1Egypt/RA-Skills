# 元阁编排策划（orchestration）

> 元阁（yotta-skills）的**编排层**：告诉 AI 智能体「什么时候该组合哪几个元技能、组合起来比单用强在哪、怎么建议用户安装并按组合契约使用」。
> 本页是「每个场景 → 选哪几个技能 → 为什么 → 怎么组合使用」的决策表。安装与调用都由用户确认后执行，本页只提供建议。
> 配套：全家清单见 `skill-list.md`；安装用法见 SKILL.md「快速使用」。

---

## 〇、编排路由（--route / route_request）

把需求摘要交给静态 playbook 与本地注册表，得到一组建议：

```bash
npx -y @yottameta/yotta-skills --route "帮我润色输出，要规范可复制，别有 AI 味"
```

- **输出**：候选组合、调用顺序、每个技能的角色、置信度、命中依据、已装/缺失状态、安装命令与应用模式提醒；如本机装了非元阁家族技能，还会给出其他已装技能候选（仅按 frontmatter description 机械匹配，标注来源与未扫描状态）。
- **缺失技能**：只给安装命令，不自动安装；安装前先做装前安全扫描，决定权在用户。
- **应用模式**：默认用户显式调用；切换为「按场景自动调用」需要用户确认。
- **无明确匹配**：低置信度回退到「入口 + 安装」组合，先澄清需求再继续。
- **边界**：路由是建议，不保证完全正确；关键动作由用户确认，数据不出本机。其他已装技能候选只读 frontmatter description、不读取全文指令、不自动调用；使用/安装前先做装前安全扫描。

---

## 一、技能家族全景（24 技能 / 8 家族）

| 家族 | 技能（中文名 / slug） | 一句话能力 |
|---|---|---|
| 入口与引导 | 元引 yotta-prompt | 意图澄清，串联到对应的元阁技能 |
| 覆盖与安装 | 元阁 yotta-skills | 全家 / 按需一键安装与更新 |
| 呈现与表达 | 元呈 yotta-present、元真 yotta-humanize | 输出判型渲染成可复制 Markdown/纯文本；去 AI 味 |
| 记忆与上下文 | 元忆 yotta-memory、元习 yotta-learn、元史 yotta-logs | 权限记忆、学习沉淀、历史检索 |
| 工作流与跨会话 | 元序 yotta-workflow | 开工读状态 / 状态就近存 / 会话结束留记录 |
| 质量与工程 | 元谨 yotta-anti-shallow、元质 yotta-code-quality、元造 yotta-skill-creator、元守 yotta-publish-guard | 防敷衍、代码评审、造技能、发布守门 |
| 安全与信任 | 元信 yotta-verify（+元信MCP）、元审 yotta-vetter、元安 yotta-security-audit、元链 yotta-chain、元钥 yotta-secret、元鉴 yotta-triage、元察 yotta-logwatch、元情 yotta-intel、元析 yotta-recon、元测 yotta-security-testing、元盾 yotta-guardian、元安全 yotta-agent-hardening | 装前扫描、审查协议、静态检测、供应链、密钥、样本、日志、IOC、侦察、测试、拦截、加固 |
| 分发与汇总 | 元引（串联）、元阁（安装） | —— |

---

## 二、组合矩阵（哪些和哪些组合，强在哪）

> 原则：**单技能是零件，组合才是系统**。下面每个组合给出「一起用效果、单用差在哪、典型场景」。

| 组合 | 成员（slug） | 一起用强在哪 | 单用缺什么 |
|---|---|---|---|
| **① 输出呈现标准** | yotta-present + yotta-humanize | 先判型渲染成规范、可复制、可复用的输出，再检测 AI 味改写，交付统一且读感自然 | 只有 yotta-present：规范但不祛 AI 味；只有 yotta-humanize：祛 AI 味但输出形态不规整 |
| **② 长生命周期智能体** | yotta-workflow + yotta-memory + yotta-learn + yotta-logs | 开工恢复上下文、权限记忆、沉淀学习、检索历史，智能体活过会话、越用越懂你 | 缺 yotta-workflow：状态无处放；缺 yotta-memory：记忆无权限边界；缺 yotta-learn：错不沉淀；缺 yotta-logs：历史查不到 |
| **③ 交付质量门** | yotta-anti-shallow + yotta-code-quality + yotta-publish-guard | 防敷衍、结对评审、发布前守门，交付前多层把关 | 缺 yotta-anti-shallow：容易停留表面；缺 yotta-code-quality：代码质量无人审；缺 yotta-publish-guard：发版无守门 |
| **④ 装前安全门** | yotta-verify（或元信MCP）+ yotta-vetter + yotta-security-audit | 确定性扫描 + 协议审查 + 深检，装其他来源技能/插件/MCP 前给出可信判定 | 缺 yotta-verify：无确定性扫描；缺 yotta-vetter：无协议审查；缺 yotta-security-audit：无深检兜底 |
| **⑤ 造技能 / 发版** | yotta-skill-creator + yotta-publish-guard | 脚手架生成合规技能目录，发布前守门 | 缺 yotta-skill-creator：造技能无模板；缺 yotta-publish-guard：造完不知能否发 |
| **⑥ 安全事件响应** | yotta-logwatch + yotta-intel + yotta-triage + yotta-secret + yotta-chain + yotta-recon | 日志检测攻击链、提取 IOC、初筛样本、扫密钥、校验供应链、侦察资产 | 每项只管一环，单用看不到全链路 |
| **⑦ 入口 + 安装** | yotta-prompt + yotta-skills | 元引澄清需求串联到对应技能，元阁按场景把组合一口气装好 | 缺 yotta-prompt：需求模糊时不知该用哪个；缺 yotta-skills：要一个个装 |

---

## 三、场景 → 组合映射（AI 接到需求时查表）

| 用户场景（触发词） | 该组合 | 建议动作（经用户确认后执行） |
|---|---|---|
| 「让 AI 长期帮我做项目 / 别忘了我 / 跨会话」 | ② 长生命周期 | 装 yotta-workflow yotta-memory yotta-learn yotta-logs；开工恢复上下文、状态就近存、会话结束留记录 |
| 「帮我写/润色，让输出规范、别 AI 味」 | ① 输出呈现标准 | 装 yotta-present yotta-humanize；默认先判型渲染，检测 AI 味再改写 |
| 「检查这段代码/报告质量，别糊弄」 | ③ 交付质量门 | 装 yotta-anti-shallow yotta-code-quality yotta-publish-guard；按对应协议执行 |
| 「我要装一个其他来源技能/插件/MCP」 | ④ 装前安全门 | 装 yotta-verify(+MCP) yotta-vetter yotta-security-audit；装前必扫 |
| 「我要造一个新 skill 并发布」 | ⑤ 造技能/发版 | 装 yotta-skill-creator yotta-publish-guard；生成 + 守门 |
| 「我怀疑日志/资产有问题」 | ⑥ 安全事件响应 | 装 yotta-logwatch yotta-intel yotta-triage yotta-secret yotta-chain yotta-recon；按需调用 |
| 「不知道怎么说 / 一堆技能该用哪个」 | ⑦ 入口+安装 | 装 yotta-prompt yotta-skills；元引澄清→串联→元阁按组合装 |

> 组合不是死板套餐：命中「入口+安装」或「输出呈现标准」这类**常用组合**时，AI 应主动说明推荐理由与将要做什么，**由用户确认后执行**；命中安全/发版这类**高风险动作**时，AI 应先给出技能清单与执行方案，再由用户确认。

---

## 四、AI 建议安装与组合规则（金标准）

1. **查表**：接到需求，先在「场景→组合映射」里定位命中组合。
2. **查已装**：检查当前智能体的技能目录是否存在对应 `<slug>/SKILL.md`；存在即已装，缺失即待装。
3. **建议装**：缺失的技能给出清单与命令
   `npx -y @yottameta/yotta-skills install <slug>... [--agent <name> | --dir <path>]`
   （只装组合所需，不装全家，避免过度安装；默认 `--pin` 锁死清单精确版本），
   **等用户确认后再执行**；用户未确认 → 不安装。
4. **建议用**：命中「输出呈现标准」「长生命周期」这类组合时，先说明推荐动作
   （如输出按元呈判型渲染、开工恢复上下文 + 读状态文件）与影响范围，**由用户确认后生效**。
   需要跨会话默认生效时，必须把默认行为写进客户端全局记忆，写入前单独征得用户明确同意；
   **不得**以「默认契约」「无需提醒」为由跳过确认。
5. **用户触发（高风险）**：命中「安全 / 发版 / 造技能」这类**高风险或目的不明**时，AI 给出技能清单与执行方案，**先征询用户确认**再执行；拿不准就当未装，给出安装命令。
6. **边界**：不 `-g` 全局安装；不向未指定位置写文件（含客户端 `mcpServers` 配置与全局记忆文件）；不静默写任何宿主配置；拿不准某技能是否已装 → 视为未装并给提示；网络不可用 → 明确报错，不伪造结果。

---

## 五、安装与入口

- 安装 CLI 用法见 `SKILL.md`「快速使用」；全家清单见 `skill-list.md`。
- 版本策略 / 元信装前摘要 / 支持的智能体 / 环境变量 同 SKILL.md。

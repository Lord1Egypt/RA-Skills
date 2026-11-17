# 元习常见问题

## 速查索引

- **归位**：新知识写到哪里 · 和元忆怎么分工 · 和 .learnings 什么关系
- **写库门槛**：什么内容适合写 · 三问判定标准 · 身份与审核口径
- **使用**：什么时候写 · 什么时候查 · 分类谁来建
- **首次使用**：怎么激活知识库（AI 引导）
- **知识库**：放哪 / 怎么换位置 / 怎么备份 · 怎么写入与核验 · 查不到刚写入的条目 · source / evidence 怎么填 · 审核被阻断怎么办 · 条目重复了怎么办
- **遗留 .learnings**：怎么读旧条目 · 怎么迁移 · log --remember / promote / extract 还能用吗
- **安全**：能写私密信息吗 · 元忆联动失败怎么办
- **报错**：退出码 · hook 不生效
- **安装**：装到哪 · 没自动加载怎么办

---

## 1. 新知识写到哪里？（归位决策树）

按判据自上而下定位：

- 私密 / 敏感 → 元忆私密区（PREF / BOUND / COMMIT），不进 KB 与项目公开文件；
- 只对当前项目成立 → 项目自身载体（AGENTS.md / docs / 项目状态与任务文件等）；
- 跨项目可复用知识（方法 / 流程 / 避坑 / 教程）→ 本技能 KB：`kb add` 草稿 → 三问审核 → verified；
- 事实 / 结论 / 红线 → 元忆 FACT（长期红线再写机器级记忆锚点）；
- 成熟、可流程化 → 技能化（护栏 / 门禁 / 清单）。

一句话：「事」进元忆，「法」进知识库，「项目专属」进项目，「未定形」进 KB 草稿。

## 2. 什么时候写？什么时候查？

- 写（事件驱动，立即）：命令失败、被用户纠正、发现更好做法、知识过时、请求缺失能力、外部接口故障；
- 写（周期驱动）：批次复盘三问、周级 review、月级自评；
- 查（默认动作）：开工时按任务关键词 `kb query`；动手解决不显然问题前；沉淀前查重；复盘时 `kb list --status draft` 过一遍。

## 3. 分类谁来建？会不会乱？

任何智能体都可创建（`kb category create`），但有治理规则：**复用优先**（写前先 `kb category list`）→ 现有分类装不下才新建（slug 小写连字符 + 名称 + 描述）→ 一条知识一个主分类（`--tags` 补检索）→ 周级 review 用 `kb category merge` / `kb category deprecate` 合并或停用碎片分类。

## 4. 首次安装后怎么激活？

首次加载元习时 AI 会主动引导：`kb config get` 检查状态 → 向用户确认库位置（默认 `~/.yottalearn/knowledge`）→ 执行 `kb init` → 写机器级「发现锚点」→ 自动接入 MCP → `kb stats` 自检。位置由用户确认，其余步骤由 AI 执行；同机其他智能体读取同一 `~/.yottalearn/config.json` 即共享同一库。

## 5. 能写密钥 / 私密信息吗？

不能。私钥、令牌、环境变量值、完整凭据、完整源码默认不写入任何共享面；私密信息放元忆私密区，共享知识面只留脱敏摘要。

## 6. 知识库放在哪？怎么换位置 / 备份？

默认 `~/.yottalearn/knowledge`（配置 `~/.yottalearn/config.json`）；`kb config set --dir <路径>` 指定任意位置（优先级 `--dir` > `YOTTA_LEARN_KB` > 配置 > 默认）；迁移用 `kb config set --dir <新路径> --move`（复制校验后切配置，旧库移出原位），只切指针会提示「旧库未迁移」，可用 `--move --from <旧库>` 补迁。备份用 `kb backup create --out <目录>`，恢复用 `kb backup restore <名称> --out <目录> --into <目标>`；日常体检用 `kb doctor`。

## 7. 怎么写入一条知识并核验？

`kb add --category <slug> --title "..." --message "..." --source "..."` 写入草稿；`kb review <ID> --pass --evidence "..."` 核验入库；查询默认只出 verified（`--include-draft` 可含草稿）。

## 8. `kb add` 的 source / evidence 怎么填？

`--source` 必填，写出处（URL / 文件 / 实验 / 会话）；`--evidence` 可以后补，核验通过（`kb review --pass`）时必须提供——写入时给出，或核验时用 `--evidence` 补。

## 9. 查询为什么查不到刚写入的条目？

新条目默认是草稿（draft），查询默认只出已核验（verified）。先 `kb review <ID> --pass --evidence "..."`，或查询时加 `--include-draft` 显式包含草稿。

## 10. 审核被阻断（敏感 / 重复）怎么办？

敏感命中：确认样例已脱敏后，用 `--force --note '说明'` 放行（留审计）；疑似重复：先 `kb show` 对比，确认不重复后用 `--force` 放行，或对重复条目执行 `kb deprecate` / `kb review --reject`。

## 11. 元习和元忆怎么分工？

元忆管「事」：事实、结论、边界、承诺与私密区（跨会话长期记忆）；元习 KB 管「法」：跨项目可复用的方法 / 流程 / 避坑 / 教程（分类 + 关键词检索）。项目专属经验写项目自身文件；两者互补、各自独立存储。

## 12. 知识库和 `.learnings/` 是什么关系？

`.learnings/` 是旧版的**项目内原始捕获区**，现已退役为遗留兼容：新知识不再默认写入；旧命令全部保留（读取 / 处置 / 迁移已有条目）。跨项目条目用 `kb add --from-learning <LRN-ID> --category <slug>` 转成 KB 草稿；项目专属条目写进项目自身文件。

## 13. 旧 `.learnings` 条目怎么读、怎么迁移？

读取 / 回看：`list` / `review` / `stats`；处置：`update` / `resolve`；转知识库：`kb add --from-learning <LRN-ID> --category <slug>`（生成草稿，仍走审核门）；提升到项目规则文件：`promote <ID>`；生成技能骨架：`extract <ID> --slug my-skill --dry-run`。`init` 幂等，绝不覆盖已有文件。

## 14. `log --remember` 与元忆联动失败会阻断吗？

不会。未安装、未初始化、超时都会降级为提示（A / B / C），遗留条目记录不受影响；这是设计好的降级路径，不是错误。

## 15. Hook 为什么没自动触发？

确认按 hooks/ 下对应平台配置放置（Claude Code 的 claude-settings.json、Codex 的 codex-settings.json 等）；命令行调用元习不需要 hook。当前 hook 仍指向遗留 `.learnings` 捕获路径，后续批次再改造；bash hook 仅 Linux 可用。

## 16. 退出码是什么意思？

0 = 成功；1 = 未找到；4 = 用法或校验错误（缺少参数、分类不存在等）；5 = 门禁阻断（敏感命中 / 疑似重复）；6 = 完整性（拒绝覆盖 / 数据损坏 / 写锁超时）。所有失败都会给出明确报错与修复建议，不会静默退出。

## 17. 条目要不要写完整错误输出？

不要。建议写「摘要 + 根因 + 修复步骤」，错误堆栈只保留关键一行或已脱敏片段；完整输出往往包含路径、账号、密钥等隐私，不利于长期复用。

## 18. MCP 怎么接入？图形化面板怎么开？

MCP：把 `scripts/yotta_learn_mcp.py` 配到客户端 `mcpServers`（stdio；配置示例见 SKILL.md「AI 接口（MCP）」）。面板：`yotta-learn view`（默认 `127.0.0.1:8791`，仅本机；页面内嵌会话令牌，破坏性写操作需确认串，全部写操作留审计）。

## 19. 安装不上 / 没自动加载怎么办？

用 `npx -y @yottameta/yotta-learn install --agent <名称>` 或 `install --dir <技能目录>`（旧写法 `--agent` / `--dir` 仍兼容）；npm 镜像传播延迟时临时加 `--registry=https://registry.npmjs.org/`。装好后由新会话读取技能目录生效；首次加载会走「激活知识库」引导。

## 20. `--category`（遗留条目）可以填哪些值？

固定枚举：`correction` / `insight` / `knowledge_gap` / `best_practice` / `error` / `other`。填错会退出码 4，并在错误信息里列出全部可用值；不确定时用 `other`。

## 21. 知识库条目重复了怎么办？

写前先 `kb query` / `kb list` 查重；发现重复时保留更优的一条，对另一条执行 `kb deprecate`（保留可查、不再返回）或 `kb review --reject`（入回收站，保留 7 天可恢复）。

## 22. 什么样的内容适合写 KB？

适合 = 跨项目可复用的「法」：方法 / 流程 / 清单（核查点、检查表）、避坑 / 教训（根因 + 触发条件 + 解法）、教程 / 判据。不适合 = 单次项目的具体发现 / 决策依据（→ 项目自身文件）、事实 / 红线（→ 元忆）、私密 / 敏感（→ 元忆私密区）、未验证猜测 / 一次性现场数据（→ 不写或留草稿）。写前先过三问：验证过？自包含？无敏感？

## 23. 写库要带身份吗？怎么带？

要。CLI：`--agent <名字>` 或设环境变量 `YOTTA_LEARN_AGENT`；MCP：工具参数 `agent`（缺省 `mcp`）；面板动作记 `view`。不带身份会记 `unknown@<host>`，审计断链、来源不可追溯。

## 24. 草稿可以自审吗？

可以，但必须逐条过三问并在 `--pass` 时写明证据（`--evidence`）；敏感 / 重复命中需 `--force --note` 说明并留审计。跨智能体共享面 / 高价值条目建议由另一智能体或用户复核后再 verified（当前不强制阻断）。

# Changelog

## v0.6.6 (2026-11-05)

- 质量门禁与打包文档修正；发布前测试接入。
- 发布门禁批次：发布工作流在 `npm publish` 前执行版本/发布面检查与 `npm test`；测试版本断言改为从 `package.json` 读取；补齐测试脚本。
- 打包与文档：发布包内容、CHANGELOG / README 与交付说明对齐；规则摘要与注册清单同步。
- Windows 迁移收口：暂存落位与旧库归档遇到短时文件共享冲突时有限重试，避免面板迁移出现半完成状态。

# 更新日志

## v0.6.5 (2026-11-01)

- 安装器 containment：目标根 / 嵌套链接 fail-closed；受管 Hub 链接解析真实目标；精简安装器同口径。

## v0.6.4 (2026-10-13)

- **修复 BUG-L-03（P3，WorkBuddy 复验发现；0.6.3 引入）**：`_drain_body()` 增加**读超时**（默认总预算 3 s，常量 `DRAIN_TIMEOUT_SECONDS`）—— 声明 `Content-Length` 却迟迟不发请求体的连接不再挂住 worker 线程；超时即置 `close_connection = True` 并照常返回响应（403 / 404 / 413 / 安全壳全覆盖）；排空后恢复套接字原超时值。
- **回归测试**：新增 `test_drain_timeout` —— `Content-Length: 1 MB` + 实发 0 字节 / 实发 1 KB 后停，两种情况断言限时（<3 s）干净返回 403（修复前会挂住）；view 套件 63 → 65 项。
- 本批 CLI / MCP / KB 数据行为零改动。

## v0.6.3 (2026-10-13)

- **修复 BUG-L-02（P2，WorkBuddy 复验发现）**：`view` 面板 POST 早退分支（令牌 403 / 路径 404 / 安全壳 403）在返回前按 `Content-Length` 排空请求体（有界 1 MB，抽为 `_drain_body` 复用；413 分支同步改造），杜绝 Windows 下「未读请求体 → RST → 客户端间歇 10053」；`Content-Length` 非法时标记连接不复用。
- **回归测试**：新增早退排空压测 —— 无令牌 POST 连发 30 次 / 错误路径 POST 连发 10 次，全部干净返回（不再间歇中断）。
- 本批 CLI / MCP / KB 数据行为零改动。

## v0.6.2 (2026-10-13)

- **修复 BUG-L-01（P1，WorkBuddy 验收发现）**：`view` 面板端口被占用时不再静默双绑 —— 面板服务器禁用地址复用（`allow_reuse_address=False`），端口冲突立即以人话报错（「端口 X 已被占用，可能已有面板在运行…」）并**非零退出**，不再打印「已启动」；杜绝「第二个实例看起来启动成功、实际操作写进另一个知识库」的数据完整性风险。
- **面板库自证强化**：侧栏 KB 路径加「KB：」前缀，浏览器标题带库目录名（一眼确认打开的是哪个库）。
- **回归测试**：新增端口冲突（进程内 + CLI 两级）与 `--port 0` 随机端口断言；`allow_reuse_address=False` 断言。

## v0.6.1 (2026-10-13)

- **管理台条目弹窗（UX-L-05）**：点击条目 / 审核草稿 / 搜索结果从「列表下方内嵌详情」改为**弹窗显示** —— 宽版弹窗复用现有 modal 组件，内容 + 元数据 + 编辑表单 + 操作按钮全量在弹窗内；点遮罩 / 关闭按钮关闭，审核通过 / 拒绝后自动关闭。搜索结果的点击统一落到弹窗。
- **写库门槛明确化（UX-L-06）**：SKILL.md 新增「写库门槛」节 —— 适合 / 不适合正反例清单 + 三问判定标准（证据等级 / 自包含边界 / 敏感边界）+ 身份要求（`--agent` / `YOTTA_LEARN_AGENT` / MCP `agent`；缺省记 `unknown` 断链）+ 审核口径（自审允许但需证据；高价值条目建议独立复核）；references/kb.md 与 references/faq.md 同步。
- 走查脚本 `tools/check_learn_view.js` 更新：条目 / 审核 / 搜索点击 → 弹窗显示内容断言（1440 + 390 两档）+ 审核后弹窗关闭断言。
- 本批为面板交互 + 文档口径变更：CLI / MCP / KB 数据行为零改动。

## v0.6.0 (2026-10-12)

- **使用模型（触发与归位）**：SKILL.md 新增「使用模型」节 —— 归位决策树（私密 → 元忆私密区 / 项目专属 → 项目自身文件 / 跨项目可复用知识 → KB 草稿 → 三问审核 / 事实与红线 → 元忆 FACT / 成熟经验 → 技能化）+ 写查时机（事件 + 周期驱动；开工先查、动手前查、写前查重、复盘过草稿）+ 分类治理轻规则（复用优先、新建规范、一条一主分类、周期合并）。
- **首次使用激活（AI 引导）**：首次加载时 AI 检测 `kb config get` 状态 → 请用户确认库位置（默认 `~/.yottalearn/knowledge`）→ 执行初始化 → 写机器级「发现锚点」→ MCP 自动接入 → `kb stats` 自检；同机智能体共享同一 `config.json`。
- **`.learnings/` 退役为遗留兼容（使用层）**：新知识不再默认写入；旧命令（log / list / review / update / resolve / promote / extract）全部保留用于读取、处置与迁移；跨项目条目用 `kb add --from-learning` 转 KB 草稿；命令与代码零改动。
- **文档同步**：README（中英）/ FAQ / walkthroughs / examples / kb.md 口径对齐；frontmatter description 与 npm description 更新（触发场景改为「沉淀 + 查询知识」语义）。
- 本批为指令层变更：CLI / MCP / view 行为零改动。

## v0.5.1 (2026-10-11)

- **管理台「高级 / CLI」完整帮助结构化（UX-L-01）**：完整帮助区从 argparse 英文原文（44 命令路径 / 132 行参数）改为元忆同款结构化渲染 —— 分组 → 命令 / 子命令（可折叠 `<details>`）→ 中文 usage 行 + 参数逐条说明（`--flag <参数>` + 做什么 + 什么时候用 + 风险提示），每行带「复制」按钮；「复制全部」保留（仍复制纯文本帮助，终端友好）。
- **新增单一真源 `LEARN_HELP_MODEL`**：44 命令路径（学习闭环 9 + kb 子树 33 + view 1）全量中文说明 + 全部选项逐条 `what` / `when`；`/api/cli` 增加结构化 `groups` 字段（面板使用；后续官网 /product/ 收录复用同一模型）。
- **覆盖门禁**：新增 `scripts/test_yotta_learn_help.py` —— 与 `build_parser()` 双向对账（路径集合相等 / 全部选项一一对应且说明非空 / usage 以条目名开头），并带反例自检（缺说明、幽灵条目必须被同一算法判失败）；已接入 `npm test` 全链。
- 走查脚本 `tools/check_learn_view.js` 更新：断言结构化完整帮助（命令 / 子命令 / 参数行计数 + `kb category create` 代表行 + 不再输出 argparse 原文 + 复制全部按钮保留）。
- **修复：精简分发副本（不带 `assets/`）下面板不可用**：此前 `view` 只从 `assets/view.html` 读模板，精简副本运行时报「面板资源缺失」；现在面板模板嵌入运行时（`VIEW_HTML_EMBEDDED` 生成块，`assets/view.html` 仍是编辑真源、由 `tools/sync_learn_view_html.py` 同步），`load_html()` 以嵌入副本为运行时真源；新增嵌入一致性回归（逐字节断言 + `load_html` 不依赖 assets）与 preflight 专属检查。

## v0.5.0 (2026-10-11)

- **npm 运行时入口（dispatcher）**：`yotta-learn` 不再只是安装器 —— 新增 `bin/yotta-learn.js`：`yotta-learn view` / `yotta-learn kb …` / `yotta-learn <学习命令>` 直接运行知识库与学习闭环（转发 Python 运行时，解释器探测 `YOTTA_LEARN_PYTHON` → `py -3` → `python` → `python3`）；`yotta-learn install …` 与旧旗标（`--agent` / `--dir` / `-g` / `--list` / `--dry-run`）保持安装行为；`--version` / `--help` 显示运行时帮助与安装指引；新增 `yotta-learn-install` 纯安装器入口（对齐元忆）。
- **管理台分类治理**：分类视图新增「重命名 / 合并 / 停用」动作（令牌 + 确认串 + 审计，与 CLI 同一内核；合并自动快照、迁移条目并留别名），并显示分类创建者与创建时间。
- **文档双路径**：SKILL / README（中英）/ references / FAQ 统一说明「已装 CLI `yotta-learn …`」与「技能目录直跑 `python3 scripts/yotta_learn.py …`」两种等价写法。
- **MCP 分类治理三件**：新增 `kb_category_rename` / `kb_category_merge` / `kb_category_deprecate`（与 CLI 同源 fail-closed：merge 自动快照 + 同名冲突阻断；deprecate 非空需 `force` 显式确认；全部写审计）；MCP 工具面 12 → 15，`tools/list` / `server/discover` 同步。
- **管理台「高级 / CLI」页（第八视图）**：常用命令速查（分组 + 一键复制）+ 完整帮助（`build_parser()` 单一真源，三层命令面）；新增只读端点 `/api/cli`。
- **面板视图切换修复**：nav 节点稳定化（切换只改 active 类）+ 渲染代际守卫（快速切换不再丢点击、旧视图慢响应不再覆盖新视图）。
- **走查脚本版本动态化**：`tools/check_learn_view.js` 截图目录从 `package.json` 动态读取版本（不再手改）。
- **解释器探测修复（自用走查拉出）**：dispatcher 先对每个候选解释器跑一次 `-c` 探测再执行脚本 —— 隔离 HOME / 受限环境里 Windows `py` 启动器可能整体失效（实测 exit 109），旧实现会把启动器退出码当脚本结果、不再回退 `python`；现在失败候选自动跳过（`YOTTA_LEARN_PYTHON` 不可用时同样回退），并新增回归用例。
- 测试：新增 dispatcher 路由 7 项（node）；管理台分类治理、分类计数等回归（python）；MCP 67 项 / view 50 项（含新增分类治理与 `/api/cli` 用例）。

## v0.4.0 (2026-10-07)

- 存储独立与迁移：配置与默认库迁到 `~/.yottalearn/`（`config.json` + `knowledge/`）；旧位置（`~/.yottaskills/yotta-learn.json` / `~/.yottaskills/knowledge`）只读兼容（回退生效时写操作 fail-closed + 一次性迁移引导，读操作与迁移不受影响）；`kb config set --dir <路径> --move [--from <源库>]`（复制 → doctor + 内容摘要双校验 → 切配置 → 旧库移出原位，fail-closed）；不带 `--move` 时明确提示「旧库未迁移」；`kb config get` 显示来源 / 未迁移块 / 最近迁移块。
- MCP stdio server（`scripts/yotta_learn_mcp.py`）：12 工具（读 5 / 写 5 / 运维 2），双时代协议（2026-07-28 无状态 + 2025-11-25 握手）；写工具与 CLI 同源 fail-closed（草稿 / 审核门 / 敏感阻断 / force 需 note）。
- 本地管理台（`yotta-learn view` + `assets/view.html`）：仅绑定 127.0.0.1；七视图（总览 / 分类 / 条目 / 搜索 / 审核 / 位置 / 运维）；会话令牌 + 破坏性确认串 + 审计；严格 CSP / 零远程资源。
- 升库：`kb add --from-learning <LRN-ID>` 把 .learnings 条目转成 KB 草稿（保留可移植来源引用，仍走审核门）。
- 修复：位置迁移后审计写回旧根（重建旧目录）→ 审计改写新库。
- 修复：旧版位置回退生效时写入静默落旧库（与「只读兼容」口径不符）→ 写操作 fail-closed（CLI / MCP / 面板同一写锁门，exit 5 + 迁移指引）；迁移与备份不受影响。
- 测试：新增 `test_yotta_learn_mcp.py`（54 项）与 `test_yotta_learn_view.py`（39 项），扩展 `test_yotta_kb.py`（37 项）；真窗口走查工具 `tools/check_learn_view.js`。
- 文档：SKILL / README（中英）/ FAQ / references/kb.md 全量更新。

## v0.3.0 (2026-10-05)

- 知识库（KB v1）：新增 `kb` 命令组 —— 分类注册（别名 / 合并 / 停用）、条目（草稿 / 核验 / 停用）、受控 frontmatter 协议、中文 bigram + 单字兜底分片索引、关键词查询（默认只出已核验）、审计、回收站（7 天）、快照（破坏性操作前自动）、独立目录备份、doctor 体检。
- 学习闭环补全：新增 `update`（状态 / 优先级 / 处置说明）与 `resolve` 快捷命令；修复多条目文件中提升第 2+ 条时 Promoted-To 写入错块的缺陷。
- 可靠性：原子写 + 跨进程写锁（过期接管）+ init 防覆盖（库已存在拒绝）+ 索引漂移自动降级线性扫描 + `kb index rebuild` / `status`。
- 测试：新增 `scripts/test_yotta_kb.py`（25 项）并扩展 `scripts/test_yotta_learn.py`（20 项）；`npm test` 链更新。
- 文档：SKILL / README（中英）/ FAQ 更新，新增 `references/kb.md` 完整参考。

## v0.2.2 (2026-10-01)

- 安装器卫生批次：`bin/install.js` / `install.sh` 统一（未知参数报错 exit 2、`--help` / `--version`、残留清理白名单、嵌套载荷保留）；由模板单一真源渲染，接入漂移门禁。
- 自带安装器测试（`test/install.test.js`）更新为统一行为断言。

## v0.2.1 (2026-09-17)

- `--category` 固定枚举写入 SKILL、README 与 FAQ：`correction / insight / knowledge_gap / best_practice / error / other`；非法值错误提示列出全部可用项。
- 修正 README 中不存在的 `tooling` 示例，改为合法 `error`；新增枚举回归。

## v0.2.0 (2026-09-09)

- 评测完善批 2：新增 references/faq.md 与 references/walkthroughs.md（命令失败/用户纠正/接口降级三类复杂走查）；SKILL.md 增加 FAQ 速查节。
- 安装器错误处理：用法/目标/安装错误统一退出码与修复建议；新增 test/install.test.js。
- package.json 补 npm test 脚本；版本对齐 0.2.0（package / SKILL / CHANGELOG / CLI）。

## v0.1.4 (2026-08-29)

- 安装方式统一为四方式（对齐发布规范 §3.3.1）：方式一 `npx -y @yottameta/yotta-learn --agent <name>` / `--dir <dir>`（推荐，走 npm 源）；方式二 `git clone https://github.com/YottaMeta/yotta-learn.git`；方式三 GitHub Download ZIP；方式四 `bash install.sh --agent/--dir/--list`。移除 `npx skills` 与 `-g` 推荐；中英双 README 安装节同步。
- 版本对齐：package.json / SKILL.md / CHANGELOG / 引擎 VERSION / 测试断言 / README 锚点 = 0.1.4。
- 无功能变更（仅文档与版本同步）。

## v0.1.3 (2026-08-28)

中英双语文档：README.md（英文主文件，作为 GitHub / npm / ClawHub 主页） + 新增 README.zh-CN.md（中文全档）；安装方式统一为三方式（npx -g / --dir、install.sh、手动复制），移除 npx 固定 --agent codex（--agent 仅 install.sh 使用）；npm description 改英文；package.json files 加入 README.zh-CN.md。无功能变更。
## v0.1.1 (2026-08-26)

README 按标准补全：新增「这是什么 / 核心价值 / 核心优势 / 功能体系 / 数据协议 / 常见问题 / 相关技能 / 升级卸载」等章节，与 YottaMeta 技能矩阵 README 标准对齐；无功能变更。


## v0.1.0 (2026-08-26)

YottaMeta 自有实现首版（参考开源社区 self-improving-agent 类技能思路，全新实现，不包含其代码）：

- CLI 全跨平台：init / log / list / promote / review / stats / extract 七个子命令。
- .learnings/ 协议：LEARNINGS / ERRORS / FEATURE_REQUESTS 三文件，ID 格式 LRN/ERR/FEAT-YYYYMMDD-XXX；
  兼容已有用户数据，初始化绝不覆盖。
- 元忆联动（可选 + 自动降级）：log --remember 显式开启，未安装/未初始化/失败分别降级 A/B/C，
  绝不阻断本地记录；先 search 去重再同步；不写依赖。
- 复发模式追踪：Pattern-Key 聚合，出现 >= 2 次自动提示合并 + 提权。
- 提升（promote）自动去重；extract 由条目生成技能骨架。
- Hook 模板：OpenClaw / Claude Code / Codex 三种配置模板；bash hook 标注 Linux-only。
- 零依赖（Python 3.8+ 标准库），Windows + Linux 通用，UTF-8 加固（GBK 控制台不崩）。
- 版权：YottaMeta 纯自有 MIT + NOTICE 品牌声明；README/NOTICE 一行来源说明。

# Changelog

## v0.1.10 (2026-11-05)

- 刷新 guardian_rules.py 摘要绑定；补齐测试接线（无行为变更）。
- 发布门禁批次：发布工作流在 `npm publish` 前执行版本/发布面检查与 `npm test`；测试版本断言改为从 `package.json` 读取；补齐测试脚本。
- 打包与文档：发布包内容、CHANGELOG / README 与交付说明对齐；规则摘要与注册清单同步。

# 更新日志

## v0.1.9 (2026-11-01)

- 安装器 containment：目标根 / 嵌套链接 fail-closed；受管 Hub 链接解析真实目标；精简安装器同口径。

## v0.1.8 (2026-10-01)

- 安装器卫生批次：`bin/install.js` / `install.sh` 统一（未知参数报错 exit 2、`--help` / `--version`、残留清理白名单、嵌套载荷保留）；由模板单一真源渲染，接入漂移门禁。

## v0.1.7 (2026-09-28)

文档格式修复 + 两处引擎健壮性修复（规则判定行为不变）。

- **修复代码围栏**：`SKILL.md` 与 `references/`（intent-verifier / policies / rules）中被写作管线占位符顶替的代码围栏，全部还原为标准三个反引号，共 20 处；此前自 0.1.0 起一直未还原，Markdown 渲染异常（命令与配置示例无法按代码块显示）。
- **修复非法转义（0.1.0 起既有）**：`scripts/guardian_rules.py` 的模块 docstring 里 `\s`、`\b` 属非法转义 —— Python 3.12+ 每次调用都向 stderr 报 2 行 SyntaxWarning，严格告警（`PYTHONWARNINGS=error`）下引擎直接加载失败。该 docstring 改为 raw 字符串（与规则表内 `r"…"` 写法一致），告警消失。
- **修复致命异常退出码（fail-closed，0.1.0 起既有）**：此前未捕获异常走 Python 默认退出码 1，而契约里 1 = 允许但带警告 —— 按退出码判定的宿主会把「引擎崩溃」读成放行（fail-open）。现在规则表加载失败与运行期未预期异常统一以**退出码 4**（用法错误 / 致命异常）结束并在 stderr 写明原因；新增 3 项回归用例（导入失败 → 4、运行期异常 → 4、严格告警下仍正常判定，共 86 项）。
- **修复彩色输出必崩（0.1.6 起既有）**：`check` 的彩色分支 `c()` 格式串只有 1 个 `%s` 却喂 2 个参数 —— 真人终端（`sys.stdout.isatty()` 为真）必抛 `TypeError`，以退出码 4 结束且**判定与命中规则完全不输出**；`--json` / `--no-color` / 管道不受影响（故此前测试未覆盖）。已修正格式串，并新增「假 TTY」回归用例（共 88 项）。
- **文档**：`SKILL.md` 新增「宿主接入」一节（放行不代批 / 用文件接引擎输出 / stdin 按 UTF-8 读），并把退出码 4 的语义写成「用法错误 / 致命异常（绝不要当作放行）」。
- **发布门禁联动**：`validate-skill` 与 `preflight-publish` 的交付面检查扩到 Python 一侧（语法错误 / 非法转义等编译期告警），与 Markdown 检查共用同一入口，命中即拦。
- 规则判定、策略档位、CLI 输出结构与审计格式不变；版本四处对齐 0.1.7。

## v0.1.6 (2026-09-25)

安全修复：复合命令拆分，堵住分隔符后的危险段绕过。

- 背景：v0.1.5 只解决了包装命令（`sh -c` / `sudo` / `env` …）绕过，整条命令仍只按第一个词做 argv 分析——`echo ok && rm -rf /`、`ls; rm -rf /`、`true || rm -rf /` 里的危险段藏在分隔符之后，整条命令被判放行（本轮复现）。
- 修复：新增受控复合命令拆分（`;` `&&` `||` `|` `&` 换行，引号 / 转义内不拆）+ 命令替换展开（`$(...)` / 反引号），逐段跑同一套文本 / argv 规则；放行规则只对单一简单命令生效；引号未闭合时出 `CMD-UNPARSED`（medium，fail-closed）。
- 安装器加固：拒绝对符号链接目标写入、目标不是目录时拒绝、不做整目录删除。
- 回归：新增 11 项复合命令用例，测试 83/83 通过。

## v0.1.5 (2026-09-19)

安全修复：包装命令解包，堵住 argv 级分析的绕过路径。

- 背景：此前 argv 级规则只看命令第一个词（`argv[0]`）。`bash -c "…"`、`cmd /c "…"`、
  `powershell -Command "…"`、`sudo …`、`env …`、`nohup …`、`timeout 5 …` 这类包装会把真正的
  动词藏在内层，导致包装后的危险命令被判为放行（例：裸 `rm -rf /` 拒绝，`bash -c "rm -rf /"` 却放行）。
- 修复：新增受控解包层（`_unwrap_argv` / `_shell_inner` / `_strip_wrapper`）——
  识别 shell（sh/bash/zsh/dash/ksh/ash/busybox/cmd/powershell/pwsh）、提权与环境包装
  （sudo/doas/env/nohup/setsid/stdbuf/nice/ionice/time/xargs/timeout/command/builtin/exec/chroot），
  剥离包装自身的选项与参数后，对内层命令跑同一套 argv 规则；解包深度上限 3 层，可嵌套（如 `sudo sh -c "…"`）。
- 边界：解包只影响 argv 级动词分析，文本级规则与放行模式行为不变；解包失败时不产生新命中，
  保持既有判定（不引入误报放大）。
- 验证：测试 72/72（新增 `WrapperBypassTest` 12 项：9 项阻断回归 + 3 项安全侧不误报）。

## v0.1.4 (2026-09-19)

版本对齐维护：修复历史发布元数据与包内版本不一致；无功能变更。

## v0.1.3 (2026-09-13)

**P0-4.3 元盾 before_tool 试点**：

- 新增 `skill-manifest.json`，声明 `before_tool` / `guard_check` / `fallback: explicit-unverified`。
- 发布工作流 `.github/workflows/publish.yml` 纳入版本库，标签推送可触发 GitHub Actions。
- Codex 该事件为 `native-audit`：危险调用评估失败时只能审计并触发一次纠偏，不宣称动作前硬拦截。
- 元阁适配器回归验证 `native-audit` 结果、纠偏信号与审计证据写入。
- 补充使用范围、授权与法律红线声明，明确本技能不是操作系统沙箱，也不替代宿主权限控制与人工决策。

## v0.1.2 (2026-08-29)

- 安装方式统一为四方式（对齐发布规范 §3.3.1）：方式一 `npx -y @yottameta/yotta-guardian --agent <name>` / `--dir <dir>`（推荐，走 npm 源）；方式二 `git clone https://github.com/YottaMeta/yotta-guardian.git`；方式三 GitHub Download ZIP；方式四 `bash install.sh --agent/--dir/--list`。移除 `npx skills` 与 `-g` 推荐；中英双 README 安装节同步。
- 版本对齐：package.json / SKILL.md / CHANGELOG / 引擎 VERSION / 测试断言 / README 锚点 = 0.1.2。
- 无功能变更（仅文档与版本同步）。

## v0.1.1 (2026-08-28)

中英双语 README 对齐（英文门面 + 中文全档）：

- **README.md 改为英文**：作为 GitHub / npm / ClawHub 首页的英文门面（翻译 + 精简，覆盖定位 / 核心价值 / 命令 / 快速使用 / 安装 / 使用示例 / 边界 / 开发校验全流程）。
- **新增 README.zh-CN.md**：原中文完整主文档整体平移，顶部加语言切换链接。
- **修复代码围栏**：README 中的围栏占位符（写作管线留下的标记）全部改为标准 ```bash / ```（Markdown 渲染修复）。
- **package.json**：description 改英文；files 加 README.zh-CN.md；版本 0.1.0 → 0.1.1。
- 版本四处对齐：package.json / SKILL frontmatter / 引擎 VERSION / 文档。
- 边界（B 方案）：references / CHANGELOG / 测试注释不翻译；SKILL 触发描述保持中文。

## v0.1.0 (2026-08-26)

YottaMeta 自有实现首版（护栏/拦截方向参考开源社区同类技能思路，已完全重写，零依赖）：

- **零依赖自研引擎**（scripts/yotta_guardian.py，Python 3.8+ 标准库）：确定性规则引擎 + 可插拔意图验证，对 exec / write / edit / read / run / shell 工具调用做安全评估。
- **四层规则**：文本模式（下载即执行 / 编码执行 / 反向 shell / 系统文件追加）+ argv 级动词/目标分析（rm / dd / mkfs / chmod / chown / 提权 / 防火墙 / 服务 / 持久化 / 反向 shell）+ 敏感路径（/etc 核心文件、/boot、/dev、SSH 授权、Windows 系统目录与 hosts、注册表启动项等）+ 写入内容（私钥 / 密钥令牌）。
- **三档策略**：default（拒绝 high+）/ strict（拒绝 medium+）/ loose（仅拒绝 critical）；放行规则（--allow / --allow-path）可降级 high，critical 不可覆盖。
- **可插拔意图验证（不绑模型）**：默认零依赖；--heuristic 内置本地启发式；--verifier / 配置文件外接任意验证器（stdin/stdout JSON 协议）。
- **审计**：JSONL 审计日志 + audit 子命令（--tail / --denied / --since / --tool / --json）。
- **输出**：文本 / JSON（stdout 纯净）/ Markdown 报告；--batch 批量预检。
- **测试**：scripts/test_yotta_guardian.py 60 项全绿（命令/路径/内容/策略/放行/批量/JSON/报告/审计/验证器/配置/GBK 控制台）。
- **文档**：SKILL.md / README.md / references（rules / policies / intent-verifier）/ assets/banner.png。
- 版权：YottaMeta 纯自有 MIT + NOTICE 品牌声明。

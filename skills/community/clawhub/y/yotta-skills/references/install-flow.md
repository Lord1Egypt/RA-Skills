# 安装器工作原理（install-flow）

> 面向想了解 yotta-skills 内部机制的开发者；日常使用请读 `SKILL.md` 或中文教程
> （`references/tutorial.md`）。

## 总体流程

对每个待装技能：

1. 读清单（`skills.json`，默认随包；`YOTTA_SKILLS_MANIFEST` 可覆盖）；
2. 拉包：默认**内置通道**（Node 内置 https 直连 registry：abbreviated packument → 解析版本 → tarball
   下载 + `integrity`(sha512) / `shasum`(sha1) fail-closed 校验），失败回退 `npm pack`
   （默认源 404 时自动改用官方源重试一次，证据记 `npm_registry_fallback`）；通道记 `fetch_channel`；
3. 解包：默认**内置通道**（Node 内置 zlib + tar 解析：ustar / pax / GNU 长名；路径安全与链接条目
   fail-closed），失败回退系统 `tar -xzf`；通道记 `extract_channel`；产物应有 `SKILL.md`；
4. 读取包内 `skill-manifest.json`；没有 manifest 时使用 `skills.json` 的家族默认契约；
5. 校验 slug / package / version / 权限 / 生命周期脚本路径；
6. 元信装前扫描：已有元信则直接扫描；没有则在本次已获用户确认的安装动作内自举元信自身，再扫描；
7. 通过后创建旧版本快照，把新版本复制到同盘暂存目录，再原子切换到目标目录；
8. 依次执行包内 setup、内置 doctor、包内自定义 doctor；任一步失败自动恢复旧版本；
9. 汇总报告：✔ 成功 / - 跳过（已是最新）/ ✘ 失败；
10. 全部成功后自动 re-index 本地技能注册表（`~/.yottaskills/registry.json`）：重扫技能根目录并增量合并，
   新装 / 更新的技能随即进入注册表（`--no-reindex` 可关闭；`--dry-run` 不触发）。

## 复制跳过规则

- 顶层跳过：`package.json` / `bin` / `node_modules` / `.git` / `__pycache__`；
- 任意层级跳过：`.pytest_cache` / `.mypy_cache` 目录、`*.pyc` / `*.pyo` 文件。

因此装进技能目录的是「技能本体」（SKILL.md / references / scripts 等），不含 npm
安装器自身、测试夹具与 Python 字节码缓存。

## 依赖与回退链

| 依赖 | 角色 | 缺失时 |
|---|---|---|
| Node.js 18+ | 必需（CLI 本体） | 明确提示 + 按平台给安装命令 |
| npm | 拉包回退通道（`YOTTA_SKILLS_NPM_FLAGS` / `--npm` 仍生效） | 不影响：内置拉包为主 |
| 系统 tar | 解包回退通道 | 不影响：内置解包为主 |
| Python 3.8+ | 元信装前扫描 | 门禁阻断（exitCode 5）；优先 `--python` / `YOTTA_SKILLS_PYTHON` 指向宿主自带 Python，或 `--skip-scan` 应急 |

- 通道可用 `YOTTA_SKILLS_FETCH=builtin|npm` / `YOTTA_SKILLS_EXTRACT=builtin|tar` 强制；
  强制单一通道失败时不回退，并给出明确报错；
- 缺依赖时按需输出「需要什么 / 为什么 / 一条修复命令 / 不影响使用」，不常驻提醒；
- `doctor` 新增依赖自检块（text + `--json` 的 `dependencies` 字段），只告警不失败、不改变退出码。

## manifest 与家族默认契约

每个技能包可以自带根目录 `skill-manifest.json`。有 manifest 时：

- 校验 `slug` / `package` / `version` 与包目录、`package.json`、`SKILL.md` 一致；
- 校验 `install.idempotent` 为 `true`；
- 校验 setup / doctor / rollback 路径为包内相对路径，不能包含绝对路径或 `..`。

没有 manifest 时使用家族默认契约：来源 `yottameta`、幂等安装、应用模式 `route`
（元阁只给路由建议，实际安装与调用由用户确认后执行），不声明 MCP、hook 或自定义生命周期脚本。

## 自定义生命周期脚本

包内 `skill-manifest.json` 可声明 `install.setup` / `install.doctor` /
`install.rollback`，值必须是包内相对路径，不能是绝对路径或包含 `..`。

元阁用当前 Node.js 直接执行脚本，不经过 shell。脚本接收 `--skill-dir` /
`--package-dir` / `--dest`，rollback 另接收 `--snapshot`，并始终追加 `--json`；
脚本必须输出一个 JSON 对象，至少包含 `ok`。setup 或 doctor 失败时，先恢复旧版本，
再在声明了 rollback 时调用它。生命周期结果、回滚结果和快照路径都会写入安装证据。

## re-index（装技能后自动重扫注册表）

- `install` / `update` 完成后，CLI 自动调用 `--reindex`（同一套 `lib/skills-scan.js` 扫描核心）：
  重扫技能根目录 → 增量合并进 `~/.yottaskills/registry.json`（新增 / 更新 / 消失）。
- `--no-reindex` 关闭自动重扫；`--reindex` 也可单独手动执行（例如会话开工时或新装技能后）。
- 与 `--inventory` 的区别：`--inventory` 侧重「盘点展示」（文本表格 / JSON 全量），
  `--reindex` 侧重「变化合并」（增量、输出聚焦新增 / 更新 / 消失，适合钩子与脚本）。

## 幂等与版本判断

- 读取目标 `<dest>/<slug>/SKILL.md` 的 frontmatter `version`；
- 与清单 `version` 一致 → 跳过（幂等：第二次安装 27 个全部跳过）；
- **只升不降（0.29.1 起）**：本地版本高于目标（清单 pin / npm latest）→ 保留并标注「本地领先」，
  `update` / `hub update` 跳过、`update --check` 不计更新（退出码 0）、`update --auto` 不动作；
  `latest` / `--range` 目标在解析出精确版本后、任何写入之前复判；
- `--force` 强制重装 / 显式降级；`rollback` 恢复快照；`update` 对「缺失 / 需要升级」的技能安装。

## 范围控制（接多少管多少）

| 用法 | 范围 |
|---|---|
| `install`（无旗标） | 全量清单全部安装 |
| `update`（无旗标） | 补齐缺失 + 升级已装（只升不降：本地更高保留不降级） |
| `update --installed-only` | 只维护目标目录已安装的家族技能（不补装缺失；无匹配时退出码 0） |
| `--only <a,b>` / `--domain <name>` | 只处理指定技能 / 家族；与 `--installed-only` 取交集 |
| `update --check` / `--auto` | 只检查 / 维护已装技能，不补装缺失 |

接管语义：接管范围 = 目标机器**已安装**的元技能（扫描目标目录得出），
`skills.json` 只作身份 / 版本参照、不决定安装范围；宿主未装的技能一律不动作（不新增、不报错）；
已管理且已最新 → 跳过（退出码 0）；非家族 / 未收录目录 → 忽略不报错。
标准配方：`yotta-skills update --installed-only --dir <技能目录>`。

## 版本策略

- 默认 pin：spec = `<pkg>@<清单精确版本>`，完全可复现，不跟随浮动版本；
- `--range`（可选）：spec = `<pkg>@<major>.x`（如 `0.x`），`npm pack` 取同 major 最新 patch。

## npm 解析（Windows）

- 优先：`where.exe npm.cmd` → 读同目录 `node_modules/npm/bin/npm-cli.js` → 用 node 直接执行
  （npm.cmd 直跑在 Windows 有 EINVAL，`cmd /c` 引号脆弱；npm-cli.js 直跑无 shell 变量坑）；
- `--npm` / `YOTTA_SKILLS_NPM`：`.js` → node 执行；`.cmd/.bat` → 同样解析 npm-cli.js；
  其它 → 直接执行；
- `YOTTA_SKILLS_NPM_FLAGS` 追加到 `npm pack` 参数。

## 元信装前门禁

- 引擎查找：`--verify` → `YOTTA_SKILLS_VERIFY` → `<dest>/yotta-verify/scripts/yotta_verify.py`；
- python 查找：`--python` → `YOTTA_SKILLS_PYTHON` → `python3` / `python` / `py`（win32）；
  缺 Python 时输出统一人话提示（含「修复」与「不影响使用」，可指向宿主自带 Python 或 `--skip-scan` 应急）；
- 执行：`python -B <engine> scan <解压目录> --json`（`-B` 禁止写 `__pycache__`，防止污染
  引擎所在目录）；
- 元信缺失时：先按 `skills.json` 安装 `yotta-verify`，并记录 `gate_mode=trusted-bootstrap`
  与 `bootstrap_scan=self`，随后用元信扫描其余家族包；
- verdict 处置：`SAFE TO INSTALL` 继续；`INSTALL WITH CAUTION` / `REVIEW REQUIRED`
  继续但显示风险并留证；`DO NOT INSTALL` 和扫描失败阻断，不替换目标；
- scanPolicy 复核：`DO NOT INSTALL` 时用包内 `scan-policy.json` 的已审查例外复核（逐条绑定
  skill + version + treeHash + 规则 + 路径；缺失 / 不匹配一律 fail-closed）；豁免后无阻断级
  发现则继续，显示 `↳ scanPolicy 复核：豁免 N 条已审查发现` 并把 `scan_policy` 写进安装证据；
- `--skip-scan` 只保留为人工应急路径，使用时输出 `explicit-unverified` 并写入证据；
- `update --auto` 始终执行装前门禁，不接受 `--skip-scan`。

## 更新检查缓存

- 手动 `update --check`：每次联网，只读，保持退出码 0 / 3 / 1。
- 后台周检 `update --check --scheduled`：默认 7 天加 0 到 24 小时随机抖动；未到期直接返回，
  到期只检查一次；文本失败静默，`--json` 保留诊断。
- 缓存文件：`~/.yottaskills/update-check.json`；按目标技能目录隔离记录，
  字段包含 `last_checked`、`next_check`、`last_result`、`last_error`。
- 本缓存只记录版本检查结果与网络错误，不记录技能内容或用户数据。

## 运行时 hook 适配

- `hook capabilities --host <name>`：查看六个统一事件的四档宿主能力；未知宿主默认 `unsupported`。
- `hook evaluate --host <name> --event <event> --manifest <file> --context <json>`：按 manifest 顺序评估声明，输出 `allow` / `block` / `warn` / `unverified`。
- `hook bind --manifest <file>` / `hook unbind <id>`：幂等注册或反注册声明，不直接改写宿主配置。
- 评估证据写入 `~/.yottaskills/hook-log.jsonl`，绑定记录写入 `~/.yottaskills/hook-bindings.json`。
- `native-audit` 不等于强制；缺少能力或证据时必须显示 `explicit-unverified`。

## M1 记忆裁决

- `decide-memory` 默认只读，调用可选本地 provider（capability `m1.adjudicate`）输出 `promote / hold / demote` 建议。
- `--promote` 只写 `~/.yottaskills/memory-adjudication.json` 建议文件；不写元忆、不删除技能。
- `usage` 默认关闭；显式 `usage enable` 后才记录结构化使用信号，不记录需求原文。
- 未配置 / 未授权 / 超时 / 非法输出时 fail-open，退出码保持 0。

## 快照与回滚

- 旧版本快照：`~/.yottaskills/snapshots/<slug>/<timestamp>-<version>-<随机后缀>/`；
- 新快照同时写入 `<快照目录>.meta.json`，包含 SHA-256 摘要、版本、文件数和来源；
- 无元数据的旧快照仍可按 `SKILL.md` 做结构校验；
- 新版本先落在 `<dest>/.yottaskills-staging/<slug>-<随机后缀>/`；
- 旧目标先重命名为同盘备份，再把暂存目录切到目标；切换失败时恢复备份；
- 证据写入失败会触发回滚，不把安装标记为成功；
- Windows 上对 `EPERM` / `EACCES` / `EBUSY` 做短重试，避免杀毒或索引服务造成的瞬时锁。

回滚命令：

```bash
yotta-skills rollback --list --dir <skills-dir>
yotta-skills rollback --slug <slug> --dir <skills-dir>
```

恢复前校验快照摘要；恢复时先在目标目录同盘暂存，再替换当前目录。恢复成功后执行
内置 doctor 和自定义 doctor，并保留原快照供再次恢复。

## doctor

```bash
yotta-skills doctor --dir <skills-dir> --slug <slug>
yotta-skills doctor --dir <skills-dir> --json
```

doctor 只读检查目录、`SKILL.md`、版本、manifest 身份、注册表记录和自定义 doctor，
不会修改目标目录或注册表。注册表版本不一致属于 warning，可用 `--reindex` 修复。
`--dir` 也可以直接指向单个技能包目录，此时会按 `SKILL.md` / `skill-manifest.json` / 目录名自动识别技能身份。
退出码：`0` 通过，`4` 没有可检查对象，`1` 检查失败，`6` manifest / 身份校验失败。

## 安装证据

每次安装决策写入：

```text
~/.yottaskills/install-log.jsonl
```

记录包含时间、事件、技能、包名、版本、`gate_mode`、verdict、decision
、`fetch_channel`（builtin / npm）、`extract_channel`（builtin / tar）和快照路径；
不记录技能内容或用户数据，只写本机。

## 退出码

| 退出码 | 含义 |
|---|---|
| 0 | 成功（含全部跳过） |
| 1 | 安装 / 更新存在失败项 |
| 2 | 用法错误（未知参数 / 未知技能 / 未收录智能体） |
| 4 | 未指定目标且当前目录未检测到项目级技能目录，或 doctor 没有可检查的元阁家族技能 |
| 5 | 装前 gate 阻断或元信不可用 |
| 6 | manifest / 身份校验失败 |

## 目标目录解析

- `--dir`：直接使用（技能落在 `<dir>/<slug>`）；
- `--agent`：查内置 17 智能体表（codex 特判 `$CODEX_HOME/skills`；opencode 特判
  `$XDG_CONFIG_HOME/opencode/skills`；其余 `~/.<agent>/skills` 或 `~/.config/...`）；
- 都未指定：检测当前目录是否存在项目级技能目录（`.claude/skills`、`.codex/skills`、
  `.agents/skills` 等 17 个），存在则用之；否则退出码 4。

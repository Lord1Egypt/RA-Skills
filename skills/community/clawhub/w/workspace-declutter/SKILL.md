---
name: workspace-declutter
description: "Declutter a workspace: enumerate by category (OS residue, stale heartbeats, backups, empty dirs, migration residue), verify consumers per category, remove via recoverable gio trash, and report before/after counts."
---

# 工作区冗余文件整理

用于：主人说「整理工作区 / 有没有无用冗余文件 / 帮我清理下」；工作区体量异常增长要定位占用；按归档规则腾地方。本 skill 只动**工作区文件系统**。
产出：分类清单（类别 × 项数 × 处置）+ 可恢复的清理动作 + 前后计数 + 有意保留清单与理由。
（配置面清理走 `openclaw-plugin-removal` / `openclaw-provider-removal`；**技能安装面**（多技能根的同名副本）走 `openclaw-extension-update` 分支 B；技能包内文档瘦身走 `skill-doc-refactor`；**判一个机制（流水线节点/角色/门）是否挣得起成本而不只是文件冗余**（实跑产物普查 + 消费方追踪 + 降 opt-in）走 `mechanism-value-verdict`；「判冗余先查消费者」的原始纪律见 `memory/lessons.md` #379。类别明细、保留清单与实测基线见 `references/冗余分类与保留清单.md`。）

## 步骤

1. **先量出重心，别按直觉删**
   `du -sh .` 加 `du -sh */ .[!.]*/ | sort -rh`（带隐藏目录，否则 `.git` / `.clawhub` 看不见）。
   完成判据：能逐条说出每个顶层目录「是项目内容还是运行残留」——体量大 ≠ 冗余多（实测 157M 里约 94% 是项目 / repo / 记忆）。

2. **按类别枚举，不用「找大文件」代替分诊**
   逐类跑一次枚举：OS 残留（`*Zone.Identifier*` / `.DS_Store` / `__pycache__`）、临时心跳（`run/*/.tmp`）、备份（`*.bak` / `*.bak.*`）、空目录（`find -type d -empty`）、解压残留、根目录 stray（`*.migrated.*`）。命令见 `references/冗余分类与保留清单.md` §A。
   完成判据：每类都有**具体项数与路径清单**，不是「大概有一些」。

3. **逐类核消费者，再决定删/留**
   ① 全仓 grep 该路径片段（`--include=*.md --include=*.py --include=*.sh --include=*.json`，排除 `./.git/`）——有引用即留；② `.bak` 类确认「有取代它的正式件」；③ 目录类判断是否**结构位**（记忆系统 / catalog 中技能 / 项目交付面 / 活仓库 / 活服务的运行时输出面）；④ 有规范归属的文件是**移动**不是删除。检查清单见 §B。
   **`run/` 下的空目录先判归属方，别按「空目录」类 rmdir**：被进程占用的路径不会出现在按文件名的 grep 里，grep 返 0 消费者**不等于**可删。用 `ps aux | grep <服务名>` 读启动参数里的 `--output <dir>`，该目录及其子目录是活服务的运行时记账面，其中的空运行目录一并保留并列待拍板。实测 `lunheng-cli/`（`lunheng serve --output .../lunheng-cli/run` 在跑，vite 占用 `web/node_modules`）整体 1003M 一项不动，其 12 个空 `lunheng-*` 目录与同名孤立的 `*.bak.<ts>` 运行目录均只报不删。
   **依赖目录的消费者用解析器证明，不能只 grep**：grep 只用来找候选消费者，命中与未命中都不足以下结论。Node 依赖跑 `node -e "try{console.log(require.resolve('<pkg>',{paths:['<消费者脚本目录>']}))}catch(e){console.log('ERR '+e.message)}"`，Python 依赖在目标解释器里跑 `python -c "import x; print(x.__file__)"` —— 打印出的路径才是真消费者；实测工作区技能脚本的 `require('cheerio')` 解析到家目录根的 `node_modules/cheerio`，按「根目录 stray」删掉会当场打挂该技能。**删可重建的依赖目录前先确认重建路径**：确认 registry 可达（`npm ping` / `pip download --no-deps -d /tmp/x <pkg>`）且仓库里有 lockfile —— 否则删掉后无法离线复原。**删重复安装与二进制前用运行时定权威件**：`type -a <cmd>` 看 PATH 顺序、`readlink -f $(which <cmd>)`、systemd 单元的 `ExecStart`、`/proc/<pid>/cmdline` —— 只比版本号或 mtime 不够；实测同盘存在两套 OpenClaw 安装而仅 `.nvm` 那份被执行、`~/.npm-global` 那份是无人使用的旧副本。两份都是构建产物时再比内嵌构建版本（`grep -ao 'vcs\.revision=[0-9a-f]+' <binary>`），复制/同步过的副本 mtime 会更新但代码版本更旧。**删前查有没有进程在用**（`ps aux | grep -E '<名字>'`，并读其启动参数里的 `-D` / `--data-dir` / `--output`）：dev server、数据库、测试进程正在用的目录删掉会打断在跑的任务。**删完立刻验证幸存件仍可用**：`<cmd> --version`、`systemctl --user is-active <svc>`、`openclaw status` —— 回显正常才算删对了。
   完成判据：每个待删项都拿得出「无消费者 / 已被取代」的证据；说不清的一律进保留清单。

4. **用可恢复方式删除**
   先 `which gio trash trash-put` 确认工具（本机只有 `/usr/bin/gio`）→ 逐批 `gio trash`；空目录用 `rmdir`（非空即失败，天然安全）；**禁用 `rm`**；移动前确认目标位置无同名件。
   完成判据：每条命令都有回显；删除项都在回收站可取回。

5. **复核计数，不靠印象收尾**
   每类枚举命令重跑一次，残留应为 0（保留项除外）；再跑 `du -sh .` 与根目录条目数做前后对比。
   完成判据：数字对得上，对不上的差异给出解释。

6. **报告分栏，禁止把「已分析」写成「已完成」**
   必须三分：**已执行**（附命令与前后计数）｜**已确认可清但未执行**（等主人拍板）｜**有意保留**（附理由）。另报本次造成的工作树变更条数（清理会新增大量 `D` / `??` 条目），是否成批 `git commit` 由主人定。
   完成判据：读者能一眼分清哪些真做了、哪些只是结论；全文没有把未执行的动作写成完成态。

## 陷阱（实测踩过的）

- **根目录的 `AGENTS.md` / `SOUL.md` / `IDENTITY.md` / `USER.md` / `BOOTSTRAP.md` 不是「stray 垃圾」，是某个会话的 OpenClaw 工作区脚手架**：删掉会**当场打挂**该目录上的会话（`WORKSPACE_VANISHED` / `Refusing to reseed BOOTSTRAP.md`）。判据：`BOOTSTRAP.md` 在位 = 该目录做过工作区初始化。⇒ 本类清理**先读 `openclaw-workspace-registration`**；要「不污染 git」用 `.gitignore` 而不是删文件（教训 #422）。
- **同名同内容 ≠ 冗余**：`run/<项目>/final/图件/` 与 `scripts/` 下的同名 png 是**有意副本**（交付面 × 工作面），删掉破坏交付面。
- **空目录可能是别家技能声明的结构位，而消费者 grep 极易漏掉**：实测 `memory/{daily,decisions,people,projects}/` 被工作区内已装技能 `skills/koompi-memory/SKILL.md` 声明为自己的存储约定；当时我只 grep 了 `MEMORY.md` / `lessons.md` / `projects.md` **三个手挑文件**，漏掉 `skills/`，把四个结构目录当空目录删了。⇒ 消费者 grep 必须**全工作区**跑（含 `skills/`），**不得手挑文件列表**。（`radar/` 实测 0 消费者，删掉无碍 —— 判据是「有没有消费者」，不是「是不是空目录」。）
- **`.learnings/` 不是本次清理的产物**：`self-improving-agent` 的 HOOK 会往里写，属依赖项。
- **`run/<项目>/.git` 是活仓库**：先 `git -C <dir> status --short` 看是否干净，能留则留。
- **报告包类要分清原件与残留**：`outputs/clawhub-scan/*.zip` 是 `scripts/scan-history.py` 的数据源（留），同目录的解压目录才是残留。
- **带版本后缀的备份**：`定稿-v1.pdf.bak` 的取代者是 `定稿.pdf`，按剥后缀名去查必然报「无取代者」——改比 md5 / 时间再判，别据此误留误删。
- **`git status` 干净 ≠ 工作树干净：`.gitignore` 会系统性藏起中间产物**：被忽略的 `*.bak.*` / `__pycache__` / 缓存目录既不进 `git status`，文件名又不显眼，**首轮清理极易只清到仓库根就收工**。实测：清掉仓库根 2 个 `.bak` 后构建门仍报「源树存在既未登记入包、也未显式排除的文件」，一查子目录树下还有 **55 个**。⇒ 清理以**源树扫描**为准（`find <tree> -name '*.bak.*'` 逐层目录跑，不只扫根），完成判据是**整棵源树残留为 0**，而不是「根目录已清」。⚠️ 这类残留通常**由构建 / 打包类门当场报出**（它们按文件集对表，对源树残留的敏感度远高于 git 与肉眼）——收尾优先跑那类门，别拿 `git status` 代替。
- **别把清理规模说成性能优化**：本类清理释放量小（实测 157M→151M），价值在可见面干净与后续维护，不在腾空间。
- ⚠️ **`gio trash` 不释放磁盘空间 ⇒ 「清理了 N G」不是可交付收益**：本机回收站 `~/.local/share/Trash` 与 `~/.openclaw` 同盘，trash 只是把字节搬到回收站。实测把 661 MB + 703 MB 两项移入回收站后 `df -h` 仍显示 1007 G 用 30 G（4%）。⇒ ① **盘不紧张时先别提「清理 N G」当优化项**：`df -h` 见剩余量级（实测 926 G 可用）就直接说明清理收益近零，把该项降级或省略，别用它占 P0；② 真要腾空间必须**清空回收站**，那是不可恢复动作，**须主人明示**；③ `du -sh` 的前后对比只证明「目录小了」，**不证明还给了文件系统**——报释放量时用 `df` 前后对比。
- ⚠️ **回收站本身会积成第二座垃圾山，且清单先于待清项暴露**：清点待清项之前先 `ls ~/.local/share/Trash/files`。实测其中有数百个 `*:Zone.Identifier`——那是 Windows↔WSL 互操作给**每次从资源管理器拖入 WSL 的文件**留下的 ADS 残留（§A 的 OS 残留类在**回收站里同样在再生**，清完源目录不会减少它）。同理 `old30/` `r38/` 之类自建批次目录会跟着进来。⇒ 回收站里的 `:Zone.Identifier` 是**持续再生项**，报清理收益时别把它算进「清一次就干净」。
- **本类残留会持续再生**：清理后数小时内根目录又出现新的扫描包 zip 与 `.openclaw/` 目录 —— 期望是「定期整理」，不是「一次清完」。
- **汇报的诚实性也是本 skill 的验收面**：实测曾把「已分析 + 已确认」当成「已完成」连报两轮，直到主人追问才暴露 —— 见第 6 步的分栏要求。

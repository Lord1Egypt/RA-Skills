---
name: repo-orientation
description: "Orient an unknown repository or directory: enumerate, measure size distribution, locate source-of-truth files, compare sibling versions, and inspect git. Produces orientation, a fact table, and a risk report."
---

# 未知仓库/目录的定向勘察

用于：主人指着工作区里一个目录或仓库问「这是什么 / 具体是什么内容 / 里面都有啥 / 帮我看下这个目录」，目标是一次说清它**是什么、体量多大、怎么组织、有没有毛病**，而不是把文件逐个念一遍。
产出：**一句话定位 + 关键事实表 + 目录构成（带体积分布）+ 机制要点（每条带文件路径）+ 风险/冗余项 + 4 个可选下一步**。
（要做全量缺陷审计 → `multi-dimension-audit`；要清理冗余 → `workspace-declutter`；主人给的是一条待解析的引用路径 → `user-cited-path-resolution`；**要动手修 git（引用链断 / 对象丢失 / 提交工作树）→ `git-repo-repair`**；同一产品的 Skill 版本真源在 `~/.openclaw/agents/main/agent/workshop-skills/<skill>/`。）

## 步骤

1. **用一等工具列举顶层，别用 exec 复合命令**
   `ls <绝对路径>` 取顶层（含隐藏项），对每个条目再 `ls` 一层看是目录还是文件；可执行件用 `file <路径>` 判定类型。**不要**把 `cd X && ls && echo && find | head` 写成一条 exec——审批层拒的是这种复合形态（被拒的是命令形态，不是环境障碍）；改用 `workdir` + 单条命令，或直接用 `ls` / `read` 工具。
   完成判据：手上有一张顶层清单，每条标出「目录 / 文件 / 可执行件 / 体积未知」。

2. **先量体积分布，再谈内容**
   `du -sh <root>/*` 与 `du -sh <root>/*/ | sort -rh` 给出子目录排序；文件总数用 `find <root> -type f -not -path '*/.git/*' -not -path '*/node_modules/*' | wc -l` 单独数一遍。
   完成判据：能逐条说出哪些目录是**源码**、哪些是**构建产物**、哪些是**历史跑批残留**，并报总体量 —— 体量大不等于内容多，产物与残留常占九成。

3. **用真源文件核对事实，README 只当线索**
   README / REPORT 里的数字（子命令数、phase 数、版本号、门数）常与代码不一致。逐个找代码侧的**唯一真源**再下结论：`VERSION` / `go.mod` / `package.json` / 命名为 `canonical_*` `*_phases` `single_source` 的文件 / 入口 `main.go`。
   完成判据：报告里每个数字都能指向一个具体文件；README 与代码不一致的条目单独列成一条发现（写清「README 说 X、代码是 Y」）。

4. **交叉核对同族资产的版本**
   同一产品常有多个形态（CLI / Skill / 插件 / Web 包），各自带版本号，**互不继承**。对每个形态各读一个版本文件，分别报版本，不合并成一个数。
   完成判据：每个形态有各自的版本与来源路径。

5. **体检 git 状态，只读**
   `git -C <root> log --oneline -5` 若报 `bad object HEAD` 或 `invalid sha1 pointer`，说明引用链断了：跑 `git -C <root> fsck` 看是「工作树完好、只是引用链断」还是「对象真缺失」，再读 `.git/packed-refs` 与 `.git/refs/` 找**存活的分支 ref**、用 fsck 的 dangling commit 找恢复锚点。命令清单见 `references/git-state-triage.md`。
   **只做只读体检**：不擅自 `gc` / `reflog expire` / `reset` / 改 ref——这些是不可逆动作，须主人点头。主人授权动手修时走 `git-repo-repair`（含「对象丢 ≠ 内容丢」的判定与逐字节复活 commit 的验收判据）。
   完成判据：能回答「工作树里的改动安全吗 / 有没有可恢复的提交 / 引用链断在哪一环」。

6. **报告按固定六段出，不按发现顺序流水账**
   ① 一句话定位 ② 关键事实表（位置/版本/体量/文件数/技术栈/许可）③ 目录构成（带体积排序）④ 机制要点（每条带文件路径，指向真源文件）⑤ 风险与冗余项（带证据行）⑥ 4 个可选下一步（修复/清理/深挖某模块/与同族资产对账），交主人挑，不要自己动手清理。
   完成判据：主人读完能直接选一个下一步，不需要再问「这到底是什么」。

## 陷阱

- **体积大 ≠ 内容多**：先分出源码 / 产物 / 残留再报体量，否则主人会以为这是个重项目而不是构建输出堆积。
- **README 的数字不是事实**：版本、子命令数、phase 数一律以代码真源为准，冲突要报而不是绕过。
- **根目录可能有二进制副本**：源码只一份，根目录与 `bin/` 各自躺着编译产物时会重复占空间；用 `file` 判定 ELF，**再读内嵌 `grep -ao 'vcs\.revision=[0-9a-f]+' <binary>` 核对构建版本** —— 文件时间戳会骗人（实测根目录副本 mtime 更晚却构建自更旧的 commit）。
- **mode-only 差异不是内容改动**：从 Windows 侧同步进工作区的文件会丢执行位，`git status` 呈现整片 `100755 => 100644`；先 `chmod +x` 还原再看 diff，否则会把权限噪声当成「改了 8 个文件」报上去、并可能被误提交。
- **`bin/` 里成堆的 `.bak*` 备份各占几十 MB**：单独列成冗余项，附可回收量估算，但删不删交主人。
- **`run/` 类目录是历史跑批产物**，不是源码也不是残留垃圾；先看有没有被引用再定性。
- **git 坏了时「最近一次提交是 X 天前」不可信**：HEAD 悬空时这个结论要等引用链体检完再给。
- **exec 复合命令被拒就换形态**：`cd X && … | head`、带 `2>/dev/null` 的链式命令常被审批层拒；拆成 `workdir` + 单命令或改用 `ls` / `read` 工具，同一形态再拒一次才算走不通。
- **不要把勘察变成动手清理**：本 skill 只出结论与可选项，删除、改文件、重建引用链都属其它技能或须主人明示。

## 边界

- 不改被勘察目录里的任何文件（含修 git、重建二进制、删备份）。
- 不替主人决定下一步做哪条；给可选项与代价，由主人拍板。
- 机制细节深挖到某一模块时，另起一轮并说明范围，勿在一次勘察里摊开整仓。

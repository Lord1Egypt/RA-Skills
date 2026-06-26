---
name: system-change-archive
description: Create a pre-restart audit and rollback archive for system-level changes. Use when modifying OpenClaw config, plugins, routing, approvals, startup behavior, or other critical files where a failed restart would be painful to diagnose. 中文：这是给系统级改动准备的“重启前留档 + 失败可回滚”保障层，适合改配置、插件、路由、审批、启动行为这类关键部分；会把改前备份、执行计划、diff 和验证记录提前整理好，出了问题也能快速排查和回退。
---

# System Change Archive

## English

A skill for high-risk system changes where restart or reload can make problems much harder to diagnose.

Its value is not in editing files for you. Its value is in making sure the risky parts are documented **before** the system is touched:
- before-state backups
- change summary
- execution plan
- diffs
- verification notes
- rollback path

**In one line: keep the evidence, context, and recovery path in place before you touch the system.**

Key strengths:
- **Lower post-restart debugging cost** — you do not need to reconstruct what changed after something breaks
- **Faster rollback** — before-state files, after-state files, diffs, and plan are already organized
- **A better fit for high-risk changes** — especially config, plugins, routing, approvals, startup behavior, and other fragile system paths
- **Cleaner audit trail** — standardized PRE-RESTART / POST-RESTART structure makes handoff, review, and later investigation much easier

If the change is small and low-risk, this skill may be overkill. But when the work can affect system behavior, service startup, remote access, or message routing, it becomes genuinely useful.

## Use this skill when

Use this skill in situations like these:

- editing OpenClaw config, runtime code, `dist` files, plugins, routing, approvals, startup behavior, or automation core
- changing system or service files that may affect startup, remote access, or message routing
- the user explicitly asks for change records, rollback preparation, pre-restart audit trails, or a reusable system-change workflow
- a restart, reload, or service bounce is likely to be part of the change

## Do not use this skill for

This skill is usually not worth using for:

- ordinary business or application code changes with low restart risk
- simple docs or content edits
- one-off low-risk local scripts, unless the user explicitly wants archival records

## Hard rules

1. **Show the intended changes first** — before changing system files or config, explain what will change, what the before/after impact is, and where the risks are; wait for confirmation.
2. **PRE-RESTART comes first** — if restart or reload is involved, create the PRE-RESTART archive before doing it.
3. **No archive, no restart** — if PRE-RESTART is incomplete, do not restart or reload.
4. **Prefer persistent storage** — use mounted or persistent storage whenever possible; if only a local fallback path is available, say that clearly.
5. **Keep scope tight** — this skill is for archival scaffolding and records; it does not replace config diagnosis, patch implementation, or security review.

## Workflow

### 1) Decide whether the change really needs archival

Use this skill only when the change is truly **system-level**, **restart-sensitive**, or **hard to reconstruct after failure**.

If it is a normal low-risk edit, do the work normally and keep the process lighter.

### 2) Resolve the archive root

Run `scripts/init_change_archive.py`.

It resolves the archive location in this order:
- explicit `--archive-root`
- `SYSTEM_CHANGE_ARCHIVE_ROOT`
- common persistent storage roots
- local workspace fallback, with a warning that it is not a hard guarantee layer

If you need the exact path selection rules, read `references/path-resolution.md`.

### 3) Scaffold the archive first

Typical command:

```bash
python3 scripts/init_change_archive.py \
  --change-name approval-followup-routing \
  --summary "Patch reply routing for exec approval follow-up" \
  --file /path/to/file1 \
  --file /path/to/file2 \
  --copy-before \
  --init-index
```

This creates a structure like this:

```text
<archive_root>/backups/system-changes/YYYY-MM-DD/HHMM-change-name/
  PRE-RESTART/
    README.md
    meta.json
    plan.md
    backup/
    after/
    diff/
  POST-RESTART/
    restart-result.md
    verify.md
    logs/
```

It can also update the daily index when needed.

### 4) Fill PRE-RESTART properly

Before restart or reload, make sure these are actually present and meaningfully filled:
- why the change is needed
- which files are affected
- before-state backups
- execution plan
- verification points
- rollback method

If you need the exact field expectations, read `references/archive-schema.md`.

### 5) Perform the actual change outside this skill

This skill does not patch code or config for you. The real patch or config work happens outside the archival workflow.

### 6) Add after-state and diffs

Preferably before restart or reload, place:
- prepared after-state files under `PRE-RESTART/after/`
- diffs or patches under `PRE-RESTART/diff/`

### 7) Do not restart until PRE-RESTART is complete

Do not skip this step.

### 8) Complete POST-RESTART if the system survives

Record:
- restart or reload result
- validation results
- logs or command outputs worth preserving

### 9) Keep the daily index useful

One concise entry per change is usually enough to keep the day folder browsable.

## Notes

- This skill is meant to stay portable; do not hardcode one specific machine’s mount path into the workflow.
- If local rules or memory already define a known persistent backup root, prefer it; otherwise let the script resolve the location.
- If you publish this skill, keep it generic: persistent-storage aware, but not host-specific.

---

## 中文

这是一个专门给**系统级变更**做兜底的 skill。

它最有价值的地方，不是“帮你改文件”，而是把那些最容易在重启后出事、又最难补救的东西，提前整理好：
- 改前备份
- 变更说明
- 执行计划
- diff
- 验证记录
- 回滚路径

**一句话说：先把证据、上下文和退路留好，再去动系统。**

这类 skill 的优势很直接：
- **降低重启翻车后的排查成本**：不是出事后再回忆改过什么，而是事前就把关键材料留好
- **回滚更稳**：改前文件、改后文件、diff 和计划都在，真出问题能快速退
- **适合高风险改动**：尤其是配置、插件、路由、审批、启动链路这类“改了能跑，重启后不一定还活着”的地方
- **归档更规范**：统一 PRE-RESTART / POST-RESTART 结构，后面自己看、别人接手、做审计都更清楚

如果你做的是普通小改，这个 skill 会显得偏重；但只要涉及系统行为、服务启动、远程访问、消息路由这些关键链路，它就很值。

## 什么时候用

下面这些场景，就该上这个 skill：

- 改 OpenClaw 配置、运行时代码、`dist` 文件、插件、路由、审批逻辑、启动行为、自动化核心
- 改系统服务文件，可能影响启动、远程访问、消息路由
- 用户明确要求做变更留档、回滚准备、重启前审计
- 这次改动大概率要 restart / reload / 重拉服务

## 什么情况别用

下面这些一般别拿它上：

- 普通业务代码、小功能、小脚本改动，重启失败风险很低
- 纯文档、纯文案修改
- 一次性的小本地脚本，除非用户明确要求留档

## 硬规则

1. **先把准备改什么说清楚**：改系统文件或配置前，先讲明白会改哪几处、改前改后影响、风险点，等确认后再动。
2. **先做 PRE-RESTART 档案**：只要涉及 restart/reload，就先把 PRE-RESTART 建好。
3. **没档案，不重启**：PRE-RESTART 没补齐，就别执行 restart/reload。
4. **优先用持久化存储**：能放挂载盘/持久化目录，就别只放临时本地路径；如果只能退回本地路径，要明确说出来。
5. **别越界**：这个 skill 负责留档和归档，不代替配置诊断、补丁实现或安全审计。

## 工作流程

### 1) 先判断这次改动值不值得留档

只有当改动真的是**系统级**、**重启敏感**、**翻车后难排查**时，才用这个 skill。

如果只是普通小改，正常做就行，别把流程搞得太重。

### 2) 找归档根目录

运行 `scripts/init_change_archive.py`。

它会按这个顺序找地方放档案：
- 你手动传的 `--archive-root`
- 环境变量 `SYSTEM_CHANGE_ARCHIVE_ROOT`
- 常见的持久化挂载目录
- 实在不行才退回 workspace 本地目录，并提醒这不算“硬保障层”

如果你想看更细的路径判定规则，再读 `references/path-resolution.md`。

### 3) 先把档案框架搭起来

常用命令：

```bash
python3 scripts/init_change_archive.py \
  --change-name approval-followup-routing \
  --summary "Patch reply routing for exec approval follow-up" \
  --file /path/to/file1 \
  --file /path/to/file2 \
  --copy-before \
  --init-index
```

这会创建出这样一套目录：

```text
<archive_root>/backups/system-changes/YYYY-MM-DD/HHMM-change-name/
  PRE-RESTART/
    README.md
    meta.json
    plan.md
    backup/
    after/
    diff/
  POST-RESTART/
    restart-result.md
    verify.md
    logs/
```

并且在需要时顺手更新当天索引。

### 4) 把 PRE-RESTART 该补的内容补完整

在 restart/reload 之前，至少要把下面这些内容补到位，而且别只留空壳：
- 这次为什么改、要解决什么
- 会影响哪些文件
- 改前备份文件
- 执行步骤
- 验证点
- 回滚办法

如果你要看更细的字段要求，读 `references/archive-schema.md`。

### 5) 真正的改动在 skill 外执行

这个 skill 不负责替你改代码或改配置；真正的 patch / config 操作在外面做。

### 6) 改完后，把 after 和 diff 也补进去

最好在 restart/reload 之前就放好：
- 改后的目标文件 → `PRE-RESTART/after/`
- diff / patch → `PRE-RESTART/diff/`

### 7) PRE-RESTART 没补齐前，不准重启

这一条别跳。

### 8) 如果系统活下来了，再补 POST-RESTART

把这些记进去：
- restart / reload 的结果
- 验证结果
- 值得留的日志或命令输出

### 9) 顺手把当天索引写清楚

每次改动留一条简短记录就够，这样当天目录翻起来不乱。

## 说明

- 这个 skill 设计成可迁移，不要把某一台机器的挂载路径硬写死在流程里。
- 如果本地规则或记忆里已经有明确的持久化备份根目录，优先用它；否则让脚本自己判定。
- 如果以后要发布这个 skill，保持通用：知道怎么优先落到持久化目录，但不要写死某台机器的专属路径。

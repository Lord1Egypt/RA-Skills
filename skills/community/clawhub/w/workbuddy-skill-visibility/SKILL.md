---
name: workbuddy-skill-visibility
display_name: 内置技能显形与还原
display_name_en: Built-in Skill Visibility & Restore
description: 让 WorkBuddy 内置技能出现在「已安装技能」列表里，并支持一键完整复原；也用于核对副本与内置原件是否一致。触发词：内置技能看不见、内置技能不见了、技能列表为空、显示内置技能、恢复内置技能、skill_visibility、技能列表缺技能。
description_zh: 让 WorkBuddy 内置技能在「已安装技能」列表中可见，并支持一键完整复原。
description_en: Make WorkBuddy built-in skills visible in the installed-skill list and restorable in one step.
category: productivity       # 对应技能市场分类「效率工具」；英文枚举官方未公开，此为推断值，创建技能时以平台分类下拉为准
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, PowerShell
version: 1.0.0
disable-model-invocation: false
user-invocable: true
author: 王教成 Wang Jiaocheng (波动几何)
---

# 内置技能显形与还原

当用户遇到以下任一情况时执行本技能：界面「已安装技能」里一个内置技能都看不到；要求把某个内置技能显示出来；要求复原此前做过的显形改动；核对副本与内置原件是否一致；询问「技能列表里找不到某技能」的去向。

## 背景（执行前必读）

- **为什么看不到**：「已安装技能」列表只渲染来源为用户技能的条目，内置技能（`source=builtin`）、连接器技能、以及 `plugins\cache\` 下的插件技能都被前端显式过滤掉。全部技能可在 `%USERPROFILE%\.workbuddy\.skill-list-cache.json` 里核对，看不到属正常，不是装坏了。
- **两条路**：一是副本方案，把内置技能复制一份到 `%USERPROFILE%\.workbuddy\skills\`，扫描器就按用户技能收录；同名的内置那份在扫描阶段被按名去重跳过，所以列表里不会出现重复条目。二是改前端 bundle，直接改渲染层的过滤函数。**默认只用副本方案**，第二条风险高得多，理由见下文专节。
- **路径不写死**：安装目录与配置目录都在运行时探测——安装目录取 `WORKBUDDY_APP_ROOT`，否则 `%LOCALAPPDATA%\Programs\WorkBuddy`，再否则 `ProgramFiles`；配置目录取 `WORKBUDDY_CONFIG_DIR`，否则 `%USERPROFILE%\.workbuddy`。探测到但结构对不上会明确报错并返回退出码 2，不会去猜、更不会去改别的地方。
- **不要用目录联接（junction）**：Node 把 junction 当符号链接，应用不跟随，必须用真实副本。
- **清单文件是可选的**：`scripts/skill_visibility_manifest.json` 记着哪些副本是本脚本建的。删掉它脚本照常工作——技能目录里凡是内容与内置原件对得上的副本，都能被当场指纹识别并重新纳管，下一次 `sync` 会把清单重建出来。它只多兜住一件指纹替代不了的事：应用升级后内置原件会变，副本与原件就不再一致，那时光靠指纹会把它看成「你自己装的技能」而不敢碰。

## 执行步骤

### 1. 先看现状（只读）

先运行 `list` 看会同步哪些、跳过哪些，再运行 `status` 逐条比对。**先把结论汇报给用户，再动手改动。** 两个命令都不写任何文件。

### 2. 显形

运行 `sync`，把内置技能复制到用户技能目录。清单里另有 5 个原件声明了 `user-invocable: false`，脚本会在**副本**的前置声明块里把这一条翻成 `true`，原件一字节不碰；`disable-model-invocation` 一律不动。

- 已存在且内容一致的副本会跳过；不一致的默认也跳过，加 `--force` 才覆盖。
- `sync` 不带参数即默认执行，无需显式写命令名。
- 副本目录已存在时按目录合并覆盖，不会因重名中断。

### 3. 生效

提醒用户**完全重启 WorkBuddy**，重启后技能列表才会重新扫描。

### 4. 复原

`restore` 删除本脚本建的全部副本，回到动手前的状态；`restore <名字…>` 只删指定的那几个。**删除前先加 `--dry-run` 看清清单**，确认无误再执行。原件不在时脚本会单独标出「待删但无法核对」，先提醒用户再动。

### 5. 核对

再跑一次 `status`，确认「一致 / 滞后 / 缺失 / 异常」四项里该一致的都一致、其余归零。

## 命令一览

- `list`　列出会同步哪些、跳过哪些，并打印本次探测到的四行路径。只读。
- `status`　逐条比对副本与原件，报告一致、滞后、缺失、异常。只读。清单缺失时退回指纹识别。
- `sync`　执行显形（默认命令）。`--force` 覆盖不一致的副本。
- `restore`　全部复原。`restore <名字…>` 只复原指定项，`--dry-run` 先看清单。
- `bundle-status`　只读，看前端 bundle 是「原样 / 已打补丁 / 部分」。不建议用这条路。
- `bundle`　给前端 bundle 打补丁，**默认只演练不写盘**，必须加 `--force` 才真写。不建议用。
- `bundle-restore`　还原前端 bundle。救援动作，**默认直接生效**，加 `--dry-run` 才只演练。
- `--version`　打印版本号；`--help`　打印完整文档。

开关（可与命令任意换位，支持 `--flag PATH` 与 `--flag=PATH` 两种写法）：`--app-root DIR` 指定 WorkBuddy 安装目录，`--config-dir DIR` 指定用户配置目录。

## 脚本调用方式

```
python scripts/skill_visibility.py <命令> [开关]
```

- 依赖：仅 Python 标准库（`os` / `re` / `shutil` / `subprocess` / `hashlib` / `json` / `tempfile` / `time` / `sys`），无第三方包。
- 若 `PATH` 里没有 `python`，改用 WorkBuddy 托管解释器 `%USERPROFILE%\.workbuddy\binaries\python\versions\*\python.exe`（按版本倒序取最新的一个）。
- 只有 `bundle*` 三条命令需要 node（做语法体检）；node 也按 `PATH` → 托管目录的顺序查找，找不到时脚本会如实报告「无法体检」，不影响副本方案。
- 清单文件写在脚本同目录，即 `<技能目录>\scripts\skill_visibility_manifest.json`。

## 改 bundle 这条路（脚本里做了，但不建议）

这条路的命令写在脚本里备用，**默认不执行、也不建议用**，理由如下：

- 一是它改的是**应用安装目录里的分发产物**。任何一次版本更新都会整包覆盖，改动静默丢失。
- 二是目标文件名带内容哈希（形如 `contexts-<hash>.js`），升级后名字会变，只能靠通配加内容匹配去定位，不能写死。
- 三是它**处在首屏关键路径上**。改坏了不是某个功能失效，而是整个界面（含对话窗口）都打不开。
- 四是它改的推理**不可靠**，写错一个字符就白屏；脚本里的「语法体检」只查语法，查不出语义错误。
- 五是回报有限——它和副本方案目标相同，而副本方案改在用户目录、升级不受影响、失败也只影响单个技能。

技术上这条路是通的：目标文件在 `app.asar.unpacked` 里，是磁盘上的真文件，Electron 对解包文件不做完整性校验。脚本给出的安全链是：先备份 `.wb-orig.bak`，再在临时文件上做语法体检，体检不过就不落盘，落盘后复核锚点，任何一步不对自动回滚；锚点要求「原式恰好 1 次、新式 0 次」才替换，应用升级改了代码就只会报告「未动手」并跳过。即便如此，仍以副本方案为准，两者不并用。

## 输出要求

- 先汇报诊断结论（会同步哪些、跳过哪些、哪些已一致），再执行写入；每步改动前后告知受影响的范围。
- 复原类操作一律先 `--dry-run` 列出待删清单，取得用户确认后才真正执行。
- 完成后给出核对结果清单；未成功项给出原因与建议动作。
- 边界声明：本技能只改动用户配置目录（副本方案），或经用户明确同意后改动应用安装目录（bundle 方案），不改动内置原件；换电脑需在该机器重新执行；改动后必须完全重启应用才生效。

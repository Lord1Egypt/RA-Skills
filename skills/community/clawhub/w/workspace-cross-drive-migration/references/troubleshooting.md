# 排错手册

按现象查。每条都给出「为什么」和「怎么办」。

## 迁移后历史对话不见了

**先查三处，顺序别乱：**

1. `projects/<新slug>` 是否存在？新 slug 算错了是最常见原因（盘符没小写、空格被改成 `-`、
   多了一层目录）。用 `scripts/ws_migrate_common.py` 里的规则核对，或直接
   `python -c "import sys;sys.path.insert(0,'scripts');import ws_migrate_common as C;print(C.slug_for_path(r'G:\迁移\项目A'))"`。
2. 目录名大小写敏感吗？Windows 不敏感，但应用按字符串比对时**可能**敏感 —— 一律按规则精确生成。
3. 应用重启过吗？侧边栏缓存要重启才刷新。

## 会话能看见，但一打开就报目录不存在

jsonl 里的 `cwd` 没改干净。核对：

```bash
python scripts/verify_migration.py --state "<状态目录>"
```

看「旧路径残留」那一行。残留出现在用户消息正文里无害，出现在 `cwd` 就是没改到。
补救：重新跑改写（`apply_migration.py` 第 4 步逻辑），或从备份 jsonl 重来。

## 数据库改不动：`database is locked`

应用正在占用数据库，**这是正常现象，不是失败**。

1. 完全退出 WorkBuddy（任务栏托盘右键退出，任务管理器确认没有 WorkBuddy 进程）；
2. `python scripts/apply_migration.py --state "<状态目录>" --db-only --apply`；
3. 重启应用。

不要为了拿锁去 `taskkill /F` 杀用户的进程——可能丢未保存的会话。

## 自动化任务失败

`automations.cwds` 还是旧路径。查：

```sql
SELECT id, name, cwds FROM automations WHERE cwds LIKE '%旧目录名%';
```

用 `--db-only --apply` 改（它按 JSON 数组解析，只替换命中的元素；不加 `--apply` 只预览）。
另外**自动化 prompt 正文里如果手写了绝对路径，脚本不会动它**（那是用户的文字），
需要自己在自动化编辑界面里改。

## 侧边栏多出一个打不开的幽灵工作空间

`workspace-display-names.json` 里旧键没删，或 `workspaces` 表旧行没删。
脚本是「移键 + 移行」，正常不会出现；如果出现了，说明中途失败过。
删掉旧键/旧行即可，删前先 `.bak`。

## 复制时报 `WinError 32`（文件被占用）/ `WinError 5`（拒绝访问）

- 32：有程序正在写这些文件（编辑器、Node 服务、数据库文件）。关掉再复制。
- 5：权限不足。目标盘若是 NTFS 且属主不同，用管理员身份重跑；或先复制到用户目录再移动。
- **绝对不要**在这种情况下用 `/MIR` 或先删源——会两头不完整。

## 目标盘空间"够"但复制中断

常见原因：

- robocopy 退出码 ≥8（磁盘满、路径过长、权限）；
- 目标是 FAT32，遇到 >4GB 单文件直接失败（提前体检能发现）；
- 移动硬盘 USB 掉线。

处理：把不完整的 `<目标>.partial-*` 删掉，换目标或清空间，重跑。源目录始终没被动过。

## 路径太长：`The specified path, file name, or both are too long`

Windows 经典 MAX_PATH 260 限制。三种解法：

1. 把目标放到更浅的层级（`G:\迁移\项目A` 而不是 `G:\备份\2026\十一月\...\项目A`）；
2. 开启系统长路径支持（组策略/注册表 `LongPathsEnabled=1`），重启；
3. 极少数深层 node_modules 可以排除不搬（但那就不是"完整迁移"了，慎用）。

体检会给「搬到新位置后最长路径约多少字符」，超过 240 就要当心。

## 移动硬盘换了 USB 口，盘符变了

路径直接失效，所有记录（projects slug、数据库、显示名）全部对不上。

**根治**：磁盘管理 → 右键移动硬盘分区 → 更改驱动器号和路径 → 固定一个靠后的盘符（如 `V:`）。

**已经变了**：就再迁移一次（从旧盘符路径迁到新盘符路径），或者在磁盘管理里把盘符改回去。
不要手工去编辑 slug 目录名——容易漏。

## 迁移后记忆是空的

`.workbuddy/memory` 没跟着复制，或者复制到了错误的层级（多套了一层目录）。
核对 `NEW\.workbuddy\memory\MEMORY.md` 是否存在；不在就从旧目录补。

## 迁移后项目技能不触发

`.workbuddy/skills` 在，但技能列表没刷新：重启应用。
如果技能目录在但内容是空的，说明复制时被链接目录坑了（`/XJ` 跳过 junction），
从源目录手工补真实内容。

## 想反悔

```bash
python scripts/rollback_migration.py --state "<状态目录>" --apply
```

只改名不删文件。如果连状态目录都找不到了，去 `<APP>\workspace-migrations\` 下按时间排序取最近的。

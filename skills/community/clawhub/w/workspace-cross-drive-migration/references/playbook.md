# 手工迁移全流程（不依赖脚本时用）

脚本跑不了（没有 Python、环境受限）时按本文手动做。
每一步都给了可直接复制的命令；**命令里的路径按实际情况替换，全部加引号**。

## 阶段 0：确认与备份清单

先写下来，后面每一步都要用到：

```
旧路径 OLD = D:\Work\项目A
新路径 NEW = G:\迁移\项目A
旧slug    = d-Work-项目A          （按 storage-map.md 的规则推）
新slug    = g-迁移-项目A
APP       = C:\Users\<用户名>\.workbuddy
```

体检必看四项：目标盘剩余空间 > 源体积 × 1.15、目标路径不存在、
目标不在源内部、目标文件系统是 NTFS/exFAT。

## 阶段 1：搬本体（应用可开着）

```cmd
robocopy "D:\Work\项目A" "G:\迁移\项目A" /E /COPY:DAT /DCOPY:DAT /XJ /R:2 /W:2 /NFL /NDL /NP
```

- `/E` 含空目录；`/XJ` 跳过目录联接（避免环）；**不要用 `/MIR`**（会删目标端文件）。
- robocopy 退出码 0~7 都是成功，≥8 才是出错。
- 校验：源与目标的文件数、总字节数必须完全一致。

```cmd
powershell -NoProfile -Command "$a=Get-ChildItem 'D:\Work\项目A' -Recurse -File; $b=Get-ChildItem 'G:\迁移\项目A' -Recurse -File; '{0} / {1}  files, {2} / {3}  bytes' -f $a.Count,$b.Count,($a|Measure-Object Length -Sum).Sum,($b|Measure-Object Length -Sum).Sum"
```

## 阶段 2：备份元数据（什么都别改之前）

```cmd
set TS=20261029-1015
mkdir "C:\ws-migrate-backup-%TS%"
xcopy "%APP%\projects\d-Work-项目A" "C:\ws-migrate-backup-%TS%\projects-old" /E /I /H /K
copy "%APP%\workbuddy.db" "C:\ws-migrate-backup-%TS%\"
copy "%APP%\workspace-display-names.json" "C:\ws-migrate-backup-%TS%\"
```

数据库还有 `-wal` / `-shm` 两个伴生文件，存在就一起复制。

## 阶段 3：会话历史目录改名

```cmd
rename "%APP%\projects\d-Work-项目A" "g-迁移-项目A"
```

（先复制一份到备份里再 rename，就是阶段 2 已经做的事。）

## 阶段 4：改写 jsonl 内路径

**最稳的做法**是用 PowerShell 逐行处理并校验：

```powershell
$old = 'D:\Work\项目A'; $new = 'G:\迁移\项目A'
$oldRx = [regex]::Escape($old) -replace '\\\\','[\\/]'
$dir = "$env:USERPROFILE\.workbuddy\projects\g-迁移-项目A"
Get-ChildItem $dir -Filter *.jsonl -Recurse | ForEach-Object {
    $lines = Get-Content $_.FullName -Encoding UTF8
    $out = foreach ($l in $lines) {
        if (-not $l.Trim()) { $l; continue }
        $n = [regex]::Replace($l, $oldRx + '(?![\w\.\-])', { param($m)
              if ($m.Value -match '/') { $new -replace '\\','/' }
              elseif ($m.Value -match '\\\\') { $new -replace '\\','\\\\' }
              else { $new } }, 'IgnoreCase')
        try { $null = $n | ConvertFrom-Json } catch { $l }   # 校验失败保留原行
        $n
    }
    $out | Set-Content $_.FullName -Encoding UTF8
}
```

要点三条：

1. 必须处理 `D:/...`、`D:\...`、`D:\\...` 三种分隔符形态；
2. 右侧边界收紧（`(?![\w.\-])`），否则 `D:\a\proj` 会误改 `D:\a\proj-old`；
3. 每行 `ConvertFrom-Json` 校验，坏了就退回原行。

## 阶段 5：改写 `.workbuddy` 里的文本引用

记忆文件里常写着绝对路径（"本工作空间在 D:\..."），一并改掉：

```powershell
Get-ChildItem "G:\迁移\项目A\.workbuddy" -Recurse -Include *.md,*.json,*.txt |
  ForEach-Object { (Get-Content $_ -Raw -Encoding UTF8) -replace [regex]::Escape('D:\Work\项目A'), 'G:\迁移\项目A' |
    Set-Content $_ -Encoding UTF8 }
```

JSON 文件改完记得校验一次；改坏了从阶段 2 的备份里取回。

## 阶段 6：显示名

编辑 `<APP>\workspace-display-names.json`：
把旧键（旧路径全小写 + 正斜杠）那条记录**移到**新键，`id` 同步改成新键，
`path` 改成新路径（正斜杠、原大小写），`displayName` 保持不变，`updatedAt` 更新为当前毫秒时间戳。

## 阶段 7：数据库（必须先完全退出应用）

1. 退出 WorkBuddy，任务管理器确认没有 `WorkBuddy.exe`；
2. 用 DB Browser for SQLite 打开 `<APP>\workbuddy.db`，执行：

```sql
-- 工作空间清单
UPDATE workspaces SET path = 'G:\迁移\项目A'
 WHERE lower(replace(path,'/','\')) = lower('D:\Work\项目A');

-- 会话工作目录（注意大小写与分隔符混杂，用 lower+replace 归一化比对）
UPDATE sessions SET cwd = 'G:\迁移\项目A'
 WHERE lower(replace(cwd,'/','\')) = lower('D:\Work\项目A');

-- 自动化（cwds 是 JSON 数组，SQL 改不了，用界面或 apply_migration.py --db-only --apply 改）
SELECT id, name, cwds FROM automations WHERE cwds LIKE '%项目A%';

-- 信任记录
UPDATE workspace_trust_decisions SET workspace_key = 'G:\迁移\项目A'
 WHERE lower(replace(workspace_key,'/','\')) = lower('D:\Work\项目A');
```

3. 写回后重启应用。

自动化那条建议还是用脚本：`python scripts/apply_migration.py --state "<状态目录>" --db-only --apply`，
它会解析 JSON 数组并保持其它元素不变。

## 阶段 8：验收与收尾

1. 重启 WorkBuddy → 打开 `NEW`；
2. 三件套验收（历史会话 / 记忆 / 项目技能）；
3. 手动跑一次自动化（如果有）；
4. 观察 3~7 天，再处理旧目录：

```cmd
rem 建议先改名隔离，而不是直接删
rename "D:\Work\项目A" "项目A.migrated-20261029"
```

## 给用户的话术（照说就行）

- "迁移本身不省空间，省空间靠**最后删掉旧目录**；所以顺序是搬→验证→再删，急不得。"
- "新位置能用一周之后你再删旧目录，中间出任何问题我都能一键回滚。"
- "移动硬盘记得在磁盘管理里固定盘符，不然换个 USB 口路径就变了。"
- "如果这个工作空间有定时任务，我现在已经把绑定路径改过来了，等下你手动跑一次确认。"

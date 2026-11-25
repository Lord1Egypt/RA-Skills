# 迁移排障手册（troubleshooting）

按症状查。脚本设计为**幂等可重跑**：任何一步失败，修掉原因后重跑对应入口即可，已完成项自动跳过/合并。

## 打包期（旧电脑）

### 1. 提示"检测到 WorkBuddy 正在运行"就退出
- 原因：运行中暂存文件动态变化，打包必缺数据。
- 处理：完全退出 WorkBuddy（托盘图标也退）后重跑；只是调试可 `-Force`。

### 2. DryRun 很慢或卡住
- 全盘枚举大目录（GB 级文件数）就是慢，属正常；只看最终清单即可。
- 某个数据目录特别大：用 `-SkipWbExtra <项名>` 跳过，或用 `-ExtraExcludeDirs` 排除。

### 3. 某目录被跳过："过大（>5GB）"
- 数据层单目录 5GB 硬上限，防止误打包巨型缓存。
- 确需：手工单独拷贝该目录，或临时调大脚本里的阈值。

### 4. bundle 创建失败
- 仓库损坏/权限问题：脚本会 warn 并跳过该仓库，其余继续。
- 修复后单独重跑整体打包即可（bundle 会重新生成）。

### 5. 输出目录报"FATAL 不能位于 .workbuddy 内"
- 会把迁移包自己打进去造成死循环。换 `-OutputRoot`（推荐桌面）。

## 还原期（新电脑）

### 6. 双击 cmd 闪退 / 无反应
- 用管理员身份运行一次 PowerShell 再双击；或手动 `powershell -NoProfile -ExecutionPolicy Bypass -File <脚本>` 看报错。
- 确认没有杀毒软件拦截 robocopy。

### 7. restore-config 某项文件数对不上（[warn]）
- 典型原因：安全软件拦截、路径过长（>260 字符）。
- 处理：重跑 `1-oneclick-restore.cmd`（robocopy 续传），直到无 warn。

### 8. "git unavailable"
- 三级兜底：包内 `git-portable` → 系统 git → winget 自动安装。
- 三者都失败：装 Git for Windows 后重跑 `2-restore-projects.cmd`（已 clone 的会跳过）。

### 9. clone 后项目在"奇怪的位置"
- 原盘符（如 D:\）在新电脑不存在时，自动落到第一个数据盘或 `用户目录\Projects`，脚本有黄字提示。
- 想指定位置：`powershell -File project-data\restore-projects.ps1 -TargetRoot E:\`。

### 10. 项目还原后 remote 指向本地 bundle / 没有新提交
- 脚本已 `remote set-url origin` 回真实远端；此后 `git pull` 拉取打包后的新提交。

### 11. 账号 UUID 不一致提示
- 新电脑登录了不同账号：源长期记忆按原目录名保留；账号相关数据（connectors/storage/记忆文件/快照）自动改名到新 UUID。
- 想手动对齐：把 `.workbuddy\user-<旧UUID>-personal` 改名为新 UUID（云端记忆本身也会同步当前账号）。

### 12. workbuddy.db 冲突（还原后会话列表异常）
- 新电脑已登录产生新 db，被源 db 覆盖导致。
- 处理：打包时加 `-NoDb`；或还原后把 `.workbuddy\workbuddy.db` 改名 .bak，重开 WorkBuddy 让其自愈。

### 13. tar 解压失败
- Win10 1803 以下没有 tar.exe：脚本自动降级 Expand-Archive；两者都失败说明 zip 损坏，回旧电脑重打。

### 14. 中文乱码
- 所有 cmd 内含 `chcp 65001`，ps1 带 BOM；若控制台仍乱码，不影响执行结果，以文件内容为准。

### 15. [可选] 迁移 git 推送私钥（SSH 配置目录）
本包**不含** SSH 私钥（避免密钥随迁移包扩散）。需要 git push 认证时二选一：

- **A. 重新生成（推荐，最省事）**：新电脑 `ssh-keygen -t ed25519`，把新公钥加到 GitHub/GitLab，本地 `remote` 已是真实远端，直接 push。
- **B. 搬旧私钥**：旧电脑把用户目录下的 SSH 配置目录（隐藏目录，`id_*`/`known_hosts`/`config`）用加密 U 盘单独拷贝到新电脑同名位置，然后收回继承权限（仅当前用户可读）：

  ```cmd
  icacls "%USERPROFILE%\.ssh" /inheritance:r /grant:r "%USERNAME%:(OI)(CI)F" /T
  ```

  验证：`ssh -T git@github.com` 返回 Hi <用户名> 即通。设过密码短语的需要记得短语。
- **C. 不用 SSH**：把 remote 换成 HTTPS（`git remote set-url origin https://...`），用 PAT 认证。

## 脚本编写层面的已知坑（改脚本前必读）

1. **PS5.1 管道坑**：`& $exe ... 2>&1 | Out-Null` 会触发 `CantActivateDocumentInPipeline`；统一写成 `$null = & $exe ... 2>&1`。
2. **Join-Path 只收两个参数**：三参数直接报错，嵌套两层。
3. **Write-Host 位置参数**：`Write-Host "x" 'Yellow'` 会把 Yellow 当正文打印；必须 `-ForegroundColor`。
4. **嵌套 powershell 不能接管道**（沙箱/部分环境）：`powershell -File x.ps1 | Out-File` 直接报错；要重定向就写在子进程命令里，或后台直跑。
5. **robocopy 退出码**：0-7 为成功（含复制），>=8 才是失败；脚本按 >=8 判错。
6. **git 中文路径**：`status --porcelain` 必须带 `-c core.quotepath=false`，否则 CJK 文件名被八进制转义。
7. **WriteAllText 不建目录**：写文件前确保父目录已 `New-Item -ItemType Directory -Force`。
8. **robocopy splatting**：`$a = @($src,$dst,'/E',...); $null = & robocopy.exe @a` 是验证过可用的形态；含空格的路径由 PS 自动加引号，不要手写反引号引号。

#Requires -Version 5.0
<#
.SYNOPSIS
  WorkBuddy 一键迁移包制作器（通用版 · 在旧电脑运行）
.DESCRIPTION
  自动收集本机全部 WorkBuddy 本地数据，生成"拷到新电脑即可一键恢复"的迁移包：

    配置层  WorkBuddy-Migration.zip   技能 / 长期记忆 / 会话工作区 / .claude / opencode / 三份配置 / .gitconfig（SSH 私钥不在自动收集范围，见使用说明手工步骤）
    项目层  project-data\             git bundle（含全部历史）+ 未提交文件 + 非 git 数据目录 + 免安装便携 git
    数据层  project-data\wb-extra\    会话历史 / 文件修改备份 / blob / plans / scripts / 备份 / 连接器 / UI 索引 / 账号数据

  新电脑无需预装 git / 7z：双击"一键恢复.cmd"（自动依次执行三层），或分步双击 1 / 2 / 3。
  账号 UUID、工作区父目录、项目所在磁盘全部自动探测，无需手工指定。

.PARAMETER Scope
  full（默认）= 三层全打；config = 仅配置层；projects = 仅项目层；data = 仅数据层
.PARAMETER ProjectRoots
  显式指定项目根目录数组。缺省自动发现：除系统盘外所有固定磁盘 + 用户目录下常见项目位置
.PARAMETER OutputRoot
  迁移包输出目录。缺省：桌面\WorkBuddy-迁移包
.PARAMETER DryRun
  只扫描生成清单与还原脚本（落在 _stage\），不拷贝数据、不打 zip
.PARAMETER Force
  WorkBuddy 正在运行也继续（db 连 WAL 一起拷，历史可能缺最新几条）
.PARAMETER NoDb
  不打包 workbuddy.db（新电脑已登录产生新 db 时可用）
.PARAMETER NoPortableGit
  不把 git 安装目录复制进包（新电脑需自备 git 或 winget 自动装）
.PARAMETER SkipWbExtra
  跳过数据层指定项，如 -SkipWbExtra workspace-sessions
.PARAMETER ExtraExcludeDirs
  附加的项目目录黑名单（支持通配符）

.EXAMPLE
  # 旧电脑最常用：退出 WorkBuddy 后双击"一键制作迁移包.cmd"（等价于）
  powershell -NoProfile -ExecutionPolicy Bypass -File Build-WBMigration.ps1

.EXAMPLE
  # 先试运行，只出清单不拷贝
  powershell -NoProfile -ExecutionPolicy Bypass -File Build-WBMigration.ps1 -DryRun

.NOTES
  PowerShell 5.1 兼容。含 API 密钥等凭证数据：只走移动硬盘，禁传公有网盘/微信。
#>
[CmdletBinding()]
param(
    [ValidateSet('full','config','projects','data')]
    [string]$Scope = 'full',
    [string[]]$ProjectRoots = @(),
    [string]$OutputRoot = '',
    [switch]$DryRun,
    [switch]$Force,
    [switch]$NoDb,
    [switch]$NoPortableGit,
    [string[]]$SkipWbExtra = @(),
    [string[]]$ExtraExcludeDirs = @()
)

$ErrorActionPreference = 'Continue'
$ProgressPreference = 'SilentlyContinue'
try { $OutputEncoding = [Text.Encoding]::UTF8 } catch {}

# =========================================================
# 基础路径探测（不依赖环境变量：精简环境里 USERPROFILE 可能为空）
# =========================================================
$Home_ = $env:USERPROFILE
if (-not $Home_) { $Home_ = [Environment]::GetFolderPath('UserProfile') }
if (-not $Home_) { $Home_ = $HOME }
if (-not $Home_) { Write-Host '[FATAL] 无法定位用户目录' -ForegroundColor Red; exit 1 }

$Wb      = Join-Path $Home_ '.workbuddy'
$Stamp   = Get-Date -Format 'yyyyMMdd-HHmm'

# ---- 账号探测：user-*-personal 可能有多个，取最近使用的为主账号 ----
$AcctDirs = @()
if (Test-Path $Wb) {
    $AcctDirs = Get-ChildItem $Wb -Directory -Filter 'user-*-personal' -ErrorAction SilentlyContinue |
        Sort-Object LastWriteTime -Descending | ForEach-Object { $_.Name }
}
$Acct = ''
if ($AcctDirs.Count -gt 0) {
    $Acct = $AcctDirs[0] -replace '^user-','' -replace '-personal$',''
}
$Personal = ''
if ($AcctDirs.Count -gt 0) { $Personal = Join-Path $Wb $AcctDirs[0] }

# ---- 工作区父目录探测：默认 用户目录\WorkBuddy；否则找含日期子目录的目录 ----
$WsRoot = $null; $wsParentRel = ''
$wsCand = Join-Path $Home_ 'WorkBuddy'
if (Test-Path $wsCand) {
    $WsRoot = $wsCand; $wsParentRel = 'WorkBuddy'
} else {
    foreach ($d in (Get-ChildItem $Home_ -Directory -ErrorAction SilentlyContinue)) {
        $hit = Get-ChildItem $d.FullName -Directory -ErrorAction SilentlyContinue |
            Where-Object { $_.Name -match '^\d{4}-\d{2}-\d{2}' } | Select-Object -First 1
        if ($hit) { $WsRoot = $d.FullName; $wsParentRel = $d.Name; break }
    }
}

# ---- 工具定位：git / 7z / tar（不依赖 PATH） ----
$gitExe = $null
$g = Get-Command git -ErrorAction SilentlyContinue
if ($g) { $gitExe = $g.Source }
if (-not $gitExe) {
    $gitCandidates = @()
    if ($Home_) { $gitCandidates += (Join-Path $Home_ 'AppData\Local\Programs\Git\cmd\git.exe') }
    foreach ($drv in @('C','D','E','F')) {
        $gitCandidates += "$drv`:\Program Files\Git\cmd\git.exe"
        $gitCandidates += "$drv`:\Program Files (x86)\Git\cmd\git.exe"
        $gitCandidates += "$drv`:\Git\cmd\git.exe"
    }
    foreach ($c in $gitCandidates) { if (Test-Path $c) { $gitExe = $c; break } }
}
$sevenZip = $null
foreach ($c in @('C:\Program Files\7-Zip\7z.exe','C:\Program Files (x86)\7-Zip\7z.exe','D:\Program Files\7-Zip\7z.exe','D:\7-Zip\7z.exe')) {
    if (Test-Path $c) { $sevenZip = $c; break }
}
$tarExe = $null
foreach ($c in @('C:\Windows\System32\tar.exe','C:\Windows\SysWOW64\tar.exe')) {
    if (Test-Path $c) { $tarExe = $c; break }
}

# =========================================================
# 排除规则（通用版：只排除系统/缓存/可再生产物）
# =========================================================
$SkillExcl  = @('dist','__pycache__','_icon_tmp','_icon_work','node_modules','.venv','venv')
$ClaudeExcl = @('cache','file-history','downloads','shell-snapshots','todos','statsig','projects','history','logs')
$OcExcl     = @('log','tool-output','repos')
$PlainExcl  = @('node_modules','.venv','venv','__pycache__','.git')
$DBlacklist = @(
    '$RECYCLE.BIN','360RecycleBin','System Volume Information','ProgramData',
    'Recovery','PerfLogs','Config.Msi','$SysReset','MSOCache',
    'Windows','Windows.old','Users','AppData','Application Data','Local Settings',
    'My Music','My Pictures','My Videos','Intel','AMD','NVIDIA','Drivers',
    'Tencent','WeChat','WeChat Files','wxwork','WXWork','.git',
    'wb-migration*','WorkBuddy-迁移*','WorkBuddy-Migration*','test-cfg*','test-7z*','zipcheck','*RECYCLE*'
) + $ExtraExcludeDirs

# 数据层（wb-extra）：已显式收集 / 不收集 的目录名
$WxCollected = @('skills','projects','workspace','blobs','plans','scripts','backups','memory','connectors','storage')
$WxSkipDirs  = @('plugins','cache','logs','tmp','temp','log')

function Log([string]$Msg, [string]$Color='Gray') {
    $ts = Get-Date -Format 'HH:mm:ss'
    Write-Host "[$ts] $Msg" -ForegroundColor $Color
}

function Get-TreeInfo([string]$Path,[string[]]$Exclude=@()) {
    if (-not (Test-Path $Path)) { return @{Files=0;Bytes=0} }
    $files = Get-ChildItem $Path -Recurse -File -Force -ErrorAction SilentlyContinue | Where-Object {
        $p = $_.FullName
        foreach ($x in $Exclude) { if ($p -like "*\$x\*") { return $false } }
        return $true
    }
    $m = $files | Measure-Object -Sum Length
    return @{Files=[int]$m.Count; Bytes=[int64]$m.Sum}
}

function Copy-Tree([string]$Src,[string]$Dst,[string[]]$Xd=@(),[string[]]$Xf=@()) {
    if (-not (Test-Path $Src)) { Log "  [跳过] 不存在: $Src" 'DarkYellow'; return }
    if ($DryRun) { return }
    New-Item -ItemType Directory -Force -Path $Dst | Out-Null
    $a = @($Src,$Dst,'/E','/NFL','/NDL','/NJH','/NJS','/NP','/R:1','/W:1')
    if ($Xd.Count) { $a += '/XD'; $a += $Xd }
    if ($Xf.Count) { $a += '/XF'; $a += $Xf }
    $null = & robocopy.exe @a
    $rc = $LASTEXITCODE
    if ($rc -ge 8) { Log "  [错误] robocopy 失败: $Src -> $Dst (exit=$rc)" 'Red' }
}

# =========================================================
# 项目根目录发现
# =========================================================
function Get-ProjectRoots {
    $roots = New-Object System.Collections.Generic.List[string]
    $sysDrv = 'C:\'
    if ($env:SystemDrive) { $sysDrv = "$($env:SystemDrive)\" }
    try {
        foreach ($di in [IO.DriveInfo]::GetDrives()) {
            if ($di.DriveType -ne 'Fixed') { continue }
            if (-not $di.IsReady) { continue }
            if ($di.Name -eq $sysDrv) { continue }
            if (-not $roots.Contains($di.Name)) { $roots.Add($di.Name) }
        }
    } catch {}
    foreach ($c in @('Projects','projects','source','repos','git','dev','code','workspace')) {
        $p = Join-Path $Home_ $c
        if ((Test-Path $p) -and (-not $roots.Contains($p))) { $roots.Add($p) }
    }
    return $roots
}

# =========================================================
# 输出目录（缺省桌面；禁止放在被收集目录内，防止自我嵌套）
# =========================================================
if (-not $OutputRoot) {
    $desk = [Environment]::GetFolderPath('Desktop')
    if (-not $desk) { $desk = Join-Path $Home_ 'Desktop' }
    if (-not (Test-Path $desk)) { $desk = $Home_ }
    $OutputRoot = Join-Path $desk 'WorkBuddy-迁移包'
}
$OutputRoot = $OutputRoot.TrimEnd('\')
$outLeaf = Split-Path $OutputRoot -Leaf
if ($outLeaf) { $DBlacklist += $outLeaf }
$forbidden = @($Wb)
if ($WsRoot) { $forbidden += $WsRoot }
foreach ($f in $forbidden) {
    if ($OutputRoot.StartsWith($f, [StringComparison]::OrdinalIgnoreCase)) {
        Write-Host "[FATAL] 输出目录不能位于 $f 内（会把迁移包自己打进去）。" -ForegroundColor Red
        Write-Host "        请用 -OutputRoot 指定其他位置，如桌面。" -ForegroundColor Red
        exit 1
    }
}

$Stage    = Join-Path $OutputRoot '_stage'
$PkgData  = Join-Path $OutputRoot 'project-data'
$WxRoot   = Join-Path $PkgData 'wb-extra'
$RestoreDir = Join-Path $Stage 'restore'

# =========================================================
Log '==========================================' 'Cyan'
Log ' WorkBuddy 一键迁移包制作器（通用版）' 'Cyan'
Log " 账号: $(if ($Acct) { $Acct } else { '未探测到（跳过账号数据）' })"
Log " 工作区父目录: $(if ($WsRoot) { $WsRoot } else { '未探测到（跳过）' })"
Log " git: $(if ($gitExe) { $gitExe } else { '未找到（仓库将退化为整目录拷贝）' })"
Log " 输出目录: $OutputRoot"
Log " 范围: $Scope"
if ($DryRun) { Log ' *** DRY-RUN 模式：只扫描，不拷贝 ***' 'Yellow' }
Log '==========================================' 'Cyan'

# ---------- 阶段 0：预检 ----------
Log '[0/6] 预检...' 'Cyan'
$wbProc = Get-Process -Name 'workbuddy' -ErrorAction SilentlyContinue
if ($wbProc) {
    if (-not $Force) {
        Log '  [中止] 检测到 WorkBuddy 正在运行。' 'Red'
        Log '  运行时源数据动态变化（暂存文件），会导致打包不完整。' 'Yellow'
        Log '  请先完全退出 WorkBuddy，再运行本脚本。' 'Yellow'
        Log '  （确认要继续：加 -Force 参数）' 'DarkGray'
        exit 1
    }
    Log '  -Force 模式：WorkBuddy 运行中，db 将连 WAL 一起拷贝（历史可能缺最新几条）' 'Yellow'
}
foreach ($p in @($Wb)) {
    if (-not (Test-Path $p)) { Log "  [缺失] $p —— 本机可能未安装/未运行过 WorkBuddy" 'Red' }
}
if (-not $DryRun) {
    $drv = Split-Path $OutputRoot -Qualifier
    $free = (Get-PSDrive ($drv.TrimEnd(':')) -ErrorAction SilentlyContinue).Free
    if ($free -and $free -lt 8GB) { Log "  输出盘剩余空间不足 8GB（当前 $([math]::Round($free/1GB,1)) GB），建议先清理" 'Yellow' }
    if (Test-Path $Stage) {
        Remove-Item $Stage -Recurse -Force -ErrorAction SilentlyContinue
        Log '  已清理上次构建残留 _stage' 'DarkGray'
    }
    foreach ($f in @(
        (Join-Path $OutputRoot 'WorkBuddy-Migration.zip'),
        (Join-Path $OutputRoot '1-oneclick-restore.cmd'),
        (Join-Path $OutputRoot '2-restore-projects.cmd'),
        (Join-Path $OutputRoot '3-restore-wbdata.cmd'),
        (Join-Path $OutputRoot '一键恢复.cmd'),
        (Join-Path $OutputRoot '使用说明.txt'),
        (Join-Path $OutputRoot '环境清单.txt')
    )) { if (Test-Path $f) { Remove-Item $f -Force -ErrorAction SilentlyContinue } }
    if (Test-Path $PkgData) { Remove-Item $PkgData -Recurse -Force -ErrorAction SilentlyContinue }
}

# =========================================================
# 阶段 1：配置层
# =========================================================
if ($Scope -in @('full','config')) { Log '[1/6] 收集配置层（技能/记忆/工作区/生态）...' 'Cyan'
$cfgRoot = Join-Path $Stage 'config'
$cfgMan = [pscustomobject]@{
    generated = $Stamp
    sourceUser = $Home_
    sourceMachine = $env:COMPUTERNAME
    wsParentRel = $wsParentRel
    personalDirs = @($AcctDirs)
    accountUuid = $Acct
}
$plan = @()
$plan += [pscustomobject]@{ Name='skills（用户级技能）'; Src=(Join-Path $Wb 'skills'); Dst=(Join-Path $cfgRoot 'skills'); Excl=$SkillExcl }
foreach ($pd in $AcctDirs) {
    $plan += [pscustomobject]@{ Name="personal（$pd 长期记忆）"; Src=(Join-Path $Wb $pd); Dst=(Join-Path $cfgRoot (Join-Path 'personal' $pd)); Excl=@() }
}
if ($WsRoot) {
    $plan += [pscustomobject]@{ Name='workspaces（会话工作区）'; Src=$WsRoot; Dst=(Join-Path $cfgRoot 'workspaces'); Excl=@() }
}
$plan += [pscustomobject]@{ Name='.claude（切换器/ccproxy 配置）'; Src=(Join-Path $Home_ '.claude'); Dst=(Join-Path $cfgRoot 'claude'); Excl=$ClaudeExcl }
$plan += [pscustomobject]@{ Name='opencode 数据'; Src=(Join-Path $Home_ '.local\share\opencode'); Dst=(Join-Path $cfgRoot 'opencode'); Excl=$OcExcl }

$cfgBytes = 0
$cfgFiles = @{}
foreach ($i in $plan) {
    $info = Get-TreeInfo $i.Src $i.Excl
    $cfgBytes += $info.Bytes
    $cfgMan | Add-Member -NotePropertyName ('files_' + ($i.Name -replace '[^\w]','_')) -NotePropertyValue $info.Files -Force
    Log ("  {0,-46} {1,8:N1} MB / {2} files" -f $i.Name,($info.Bytes/1MB),$info.Files)
    if (-not $DryRun) { Copy-Tree $i.Src $i.Dst $i.Excl @('*.log','*.tmp') }
}
# 零散配置文件（.workbuddy 根部 + .gitconfig）
$rootFiles = @('mcp.json','models.json','settings.json','claude_switcher.lang','workspace-display-names.json','free_llm_auto_state.json','opencode_zen_state.json','free_llm_candidate_bench.json','MEMORY.md','SOUL.md','IDENTITY.md','USER.md','BOOTSTRAP.md','user-state.json','workspace-state.json','mcp-approvals.json','failover.json','last-launch.json','usage-log.json','mcp-tool-list.json')
if (-not $NoDb) { $rootFiles += @('workbuddy.db','workbuddy.db-wal','workbuddy.db-shm') }
$rfBytes = 0; $rfCount = 0
foreach ($f in $rootFiles) {
    $fp = Join-Path $Wb $f
    if (Test-Path $fp) {
        $rfBytes += (Get-Item $fp).Length
        $rfCount++
        if (-not $DryRun) {
            New-Item -ItemType Directory -Force -Path (Join-Path $cfgRoot '_root') | Out-Null
            Copy-Item $fp (Join-Path $cfgRoot '_root') -Force
        }
    }
}
$gitCfg = Join-Path $Home_ '.gitconfig'
if (Test-Path $gitCfg) {
    $rfBytes += (Get-Item $gitCfg).Length
    $rfCount++
    if (-not $DryRun) {
        New-Item -ItemType Directory -Force -Path (Join-Path $cfgRoot '_root') | Out-Null
        Copy-Item $gitCfg (Join-Path $cfgRoot '_root') -Force
    }
}
$cfgBytes += $rfBytes
Log ("  {0,-46} {1,8:N1} MB / {2} files" -f '零散配置 + .gitconfig + db',($rfBytes/1MB),$rfCount)
Log ("  配置层合计: {0:N1} MB" -f ($cfgBytes/1MB)) 'Green'
New-Item -ItemType Directory -Force -Path $RestoreDir | Out-Null
[IO.File]::WriteAllText((Join-Path $RestoreDir 'config-manifest.json'), ($cfgMan | ConvertTo-Json -Depth 4), (New-Object Text.UTF8Encoding($false)))
} # end scope config

# =========================================================
# 阶段 2：项目层（git bundle + 脏文件 + 非 git 数据目录）
# =========================================================
$bundleDir = Join-Path $PkgData 'git-bundles'
$dirtyDir  = Join-Path $PkgData 'git-dirty'
$plainDir  = Join-Path $PkgData 'plain'
$repos = @(); $plainDirs = @(); $plainBytes = 0

if ($Scope -in @('full','projects')) {
    Log '[2/6] 收集项目层...' 'Cyan'
    if ($ProjectRoots.Count -gt 0) { $roots = $ProjectRoots } else { $roots = Get-ProjectRoots }
    $rootList = @($roots | Where-Object { Test-Path $_ })
    if ($rootList.Count -eq 0) { Log '  [警告] 未发现任何项目根目录' 'Yellow' }
    foreach ($rt in $rootList) {
        Log "  扫描根目录: $rt" 'DarkGray'
        $tops = Get-ChildItem $rt -Directory -Force -ErrorAction SilentlyContinue | Where-Object {
            $n = $_.Name
            foreach ($b in $DBlacklist) { if ($n -like $b) { return $false } }
            return $true
        }
        foreach ($d in $tops) {
            if (Test-Path (Join-Path $d.FullName '.git')) {
                # ---- git 仓库：bundle + 脏文件 ----
                $info = Get-TreeInfo $d.FullName @('.git')
                $mb = [math]::Round($info.Bytes/1MB,1)
                Log ("  [git] {0,-30} 工作区 {1,8:N1} MB  ({2})" -f $d.Name,$mb,$rt)
                if ($DryRun) {
                    $repos += [pscustomobject]@{ name=$d.Name; root=$rt; branch='(dry-run)'; bundleMB=0; dirtyFiles=0; remote='' }
                    continue
                }
                if (-not $gitExe) {
                    Log "         [warn] 未找到 git，$($d.Name) 退化为整目录拷贝" 'Yellow'
                    $plainBytes += $info.Bytes
                    $plainDirs += [pscustomobject]@{ name=$d.Name; root=$rt; mb=$mb }
                    Copy-Tree $d.FullName (Join-Path $plainDir $d.Name) $PlainExcl
                    continue
                }
                New-Item -ItemType Directory -Force -Path $bundleDir | Out-Null
                $bundle = Join-Path $bundleDir "$($d.Name).bundle"
                $null = & $gitExe -C $d.FullName bundle create $bundle --all 2>&1
                $grc = $LASTEXITCODE
                if ($grc -ne 0 -or -not (Test-Path $bundle)) {
                    Log "         [warn] bundle 失败: $($d.Name) (exit=$grc)" 'Yellow'
                    continue
                }
                $branch = (& $gitExe -C $d.FullName rev-parse --abbrev-ref HEAD 2>$null)
                if (-not $branch) { $branch = 'main' }
                # 未提交的工作区改动（modified + untracked，含未跟踪目录；quotepath=false 防 CJK 转义）
                $dirtyCount = 0
                $dd = Join-Path $dirtyDir $d.Name
                $status = & $gitExe -C $d.FullName -c core.quotepath=false status --porcelain 2>$null
                foreach ($line in $status) {
                    if ($line.Length -lt 4) { continue }
                    $f = $line.Substring(3)
                    if ($f -match ' -> ') { $f = ($f -split ' -> ')[-1] }
                    $f = $f.Trim().Trim('"')
                    if (-not $f) { continue }
                    $src = Join-Path $d.FullName $f
                    if (-not (Test-Path $src)) { continue }
                    $dstP = Join-Path $dd $f
                    if ((Get-Item $src).PSIsContainer) {
                        Copy-Tree $src $dstP
                    } else {
                        New-Item -ItemType Directory -Force -Path (Split-Path $dstP) | Out-Null
                        Copy-Item $src $dstP -Force
                    }
                    $dirtyCount++
                }
                $repos += [pscustomobject]@{
                    name=$d.Name; root=$rt; branch=$branch.Trim()
                    bundleMB=[math]::Round((Get-Item $bundle).Length/1MB,1)
                    dirtyFiles=$dirtyCount
                    remote=(& $gitExe -C $d.FullName remote get-url origin 2>$null)
                }
                Log ("         bundle {0:N1} MB + {1} 个未提交文件" -f ((Get-Item $bundle).Length/1MB),$dirtyCount) 'DarkGray'
            }
            else {
                # ---- 非 git 目录：整目录（排除依赖/产物）----
                $info = Get-TreeInfo $d.FullName $PlainExcl
                $plainBytes += $info.Bytes
                $plainDirs += [pscustomobject]@{ name=$d.Name; root=$rt; mb=[math]::Round($info.Bytes/1MB,1) }
                Log ("  [plain] {0,-29} {1,8:N1} MB / {2} files  ({3})" -f $d.Name,($info.Bytes/1MB),$info.Files,$rt)
                if (-not $DryRun) { Copy-Tree $d.FullName (Join-Path $plainDir $d.Name) $PlainExcl }
            }
        }
    }

    # ---------- 便携 git：新电脑不装 git 也能还原 bundle ----------
    if (-not $NoPortableGit) {
        $pgDst = Join-Path $PkgData 'git-portable'
        $pgSrc = $null
        $pgCands = @(
            (Join-Path $PSScriptRoot 'git-portable'),
            (Join-Path $PSScriptRoot '..\git-portable'),
            'D:\wb-migration-tool\git-portable',
            (Join-Path $Home_ 'git-portable'),
            (Join-Path $Home_ 'Downloads\PortableGit'),
            (Join-Path $Home_ 'Downloads\PortableGit-*')
        )
        foreach ($c in $pgCands) { if (Test-Path (Join-Path $c 'cmd\git.exe')) { $pgSrc = $c; break } }
        if ((-not $pgSrc) -and $gitExe) {
            # Git for Windows 安装目录本身即可绿色运行：...\Git\cmd\git.exe -> ...\Git
            $root2 = Split-Path (Split-Path $gitExe -Parent) -Parent
            if ((Test-Path (Join-Path $root2 'cmd\git.exe')) -and ($root2 -notlike '*\cmd')) { $pgSrc = $root2 }
        }
        if ($pgSrc) {
            $pgMB = [math]::Round((Get-TreeInfo $pgSrc).Bytes/1MB,0)
            if (-not $DryRun) {
                if (Test-Path $pgDst) { Remove-Item $pgDst -Recurse -Force -ErrorAction SilentlyContinue }
                Copy-Tree $pgSrc $pgDst
            }
            Log ("  [git-portable] 免安装 git {0} MB（新电脑无 git 时自动调用）" -f $pgMB) 'DarkGray'
        } else {
            Log '  [warn] 未找到可打包的 git（新电脑将走 winget 自动安装或需自备 git）' 'Yellow'
        }
    }
    Log ("  项目层合计: git 仓库 {0} 个 + 数据目录 {1} 个（{2:N1} MB）" -f $repos.Count,$plainDirs.Count,($plainBytes/1MB)) 'Green'
}

# =========================================================
# 阶段 2.5：wb-extra 数据层（.workbuddy 下的大数据）
# =========================================================
$wxBytes = 0
$wxItems = New-Object Collections.Generic.List[object]

if ($Scope -in @('full','data')) {
    Log '[2.5/6] 收集 WorkBuddy 数据层（会话历史/修改备份/blob/索引）...' 'Cyan'

    # ---- 显式目录 ----
    $wxDirs = @(
        @{ Src='projects';              Dst='projects';              Desc='会话对话历史（侧边栏历史内容）' },
        @{ Src='workspace\sessions';    Dst='workspace-sessions';    Target='workspace\sessions'; Desc='文件修改备份快照（会话后悔药）' },
        @{ Src='blobs';                 Dst='blobs';                 Desc='artifact 图片 blob 存储' },
        @{ Src='plans';                 Dst='plans';                 Desc='Plan 模式计划文档' },
        @{ Src='scripts';               Dst='scripts';               Desc='用户脚本' },
        @{ Src='backups';               Dst='backups';               Desc='技能与切换器备份' },
        @{ Src='.workbuddy\memory';     Dst='dot-workbuddy-memory';  Target='.workbuddy\memory'; Desc='旧结构每日日志与 automations 记忆' }
    )
    foreach ($d in $wxDirs) {
        if ($SkipWbExtra -contains $d.Dst) { Log ("  [skip] {0}（-SkipWbExtra 指定）" -f $d.Dst) 'DarkYellow'; continue }
        $src = Join-Path $Wb $d.Src
        if (-not (Test-Path $src)) { continue }
        $info = Get-TreeInfo $src
        $wxBytes += $info.Bytes
        if (-not $DryRun) { Copy-Tree $src (Join-Path $WxRoot $d.Dst) }
        $tgt = $d.Dst
        if ($d.Target) { $tgt = $d.Target }
        $wxItems.Add([pscustomobject]@{ src=$d.Dst; dst=$tgt; desc=$d.Desc })
        Log ("  {0,-46} {1,8:N1} MB / {2} files" -f $d.Desc,($info.Bytes/1MB),$info.Files)
    }
    # workspace 下其它子目录（sessions 之外）
    $wsDataDir = Join-Path $Wb 'workspace'
    if (Test-Path $wsDataDir) {
        foreach ($ch in (Get-ChildItem $wsDataDir -Directory -ErrorAction SilentlyContinue)) {
            if ($ch.Name -eq 'sessions') { continue }
            if ($SkipWbExtra -contains "workspace-$($ch.Name)") { continue }
            $info = Get-TreeInfo $ch.FullName
            $wxBytes += $info.Bytes
            if (-not $DryRun) { Copy-Tree $ch.FullName (Join-Path $WxRoot "workspace-$($ch.Name)") }
            $wxItems.Add([pscustomobject]@{ src="workspace-$($ch.Name)"; dst="workspace\$($ch.Name)"; desc="workspace\$($ch.Name)" })
            Log ("  {0,-46} {1,8:N1} MB / {2} files" -f "workspace\$($ch.Name)",($info.Bytes/1MB),$info.Files)
        }
    }

    # ---- 账号相关（自动改名为新电脑账号）----
    if ($Acct) {
        # 账号记忆文件
        $mf = Join-Path $Wb "memory\$($Acct)_memory.md"
        if (Test-Path $mf) {
            if (-not $DryRun) {
                New-Item -ItemType Directory -Force -Path (Join-Path $WxRoot 'memory') | Out-Null
                Copy-Item $mf (Join-Path $WxRoot 'memory') -Force
            }
            $wxBytes += (Get-Item $mf).Length
            $wxItems.Add([pscustomobject]@{ src='memory'; dst='memory'; desc='账号记忆文件'; srcAcct=$Acct; acctFiles=@(@{from='<ACCT>_memory.md'; to='<ACCT>_memory.md'}) })
            Log '  账号记忆文件 memory\<uuid>_memory.md' 'DarkGray'
        }
        # 连接器本地配置
        $cd = Join-Path $Wb "connectors\$Acct"
        if (Test-Path $cd) {
            if (-not $DryRun) { Copy-Tree $cd (Join-Path $WxRoot "connectors\$Acct") }
            $i2 = Get-TreeInfo $cd; $wxBytes += $i2.Bytes
            $wxItems.Add([pscustomobject]@{ src="connectors\$Acct"; dst="connectors\$Acct"; desc='连接器本地配置'; srcAcct=$Acct })
            Log ("  {0,-46} {1,8:N1} MB" -f '连接器本地配置',($i2.Bytes/1MB)) 'DarkGray'
        }
        # 账号 storage（含 skeleton）
        $sd = Join-Path $Wb "storage\user-$Acct-personal"
        if (Test-Path $sd) {
            if (-not $DryRun) { Copy-Tree $sd (Join-Path $WxRoot "storage\user-$Acct-personal") }
            $i2 = Get-TreeInfo $sd; $wxBytes += $i2.Bytes
            $wxItems.Add([pscustomobject]@{ src="storage\user-$Acct-personal"; dst="storage\user-$Acct-personal"; desc='账号 storage（会话显示状态/专家选择）'; srcAcct=$Acct })
        }
        $sk = Join-Path $Wb 'storage\skeleton'
        if (Test-Path $sk) {
            if (-not $DryRun) { Copy-Tree $sk (Join-Path $WxRoot 'storage\skeleton') }
            $i2 = Get-TreeInfo $sk; $wxBytes += $i2.Bytes
            $wxItems.Add([pscustomobject]@{ src='storage\skeleton'; dst='storage\skeleton'; desc='账号快照骨架' })
        }
        # 侧边栏账号快照目录
        $ad = Join-Path $Wb $Acct
        if (Test-Path $ad) {
            if (-not $DryRun) { Copy-Tree $ad (Join-Path $WxRoot "account-snapshot\$Acct") }
            $wxItems.Add([pscustomobject]@{ src="account-snapshot\$Acct"; dst=$Acct; desc='侧边栏快照与启动路由'; srcAcct=$Acct })
            Log '  侧边栏账号快照' 'DarkGray'
        }
    }

    # ---- 顶层零散文件（兜底：除 db/日志外全部收入）----
    if (-not $DryRun) { New-Item -ItemType Directory -Force -Path (Join-Path $WxRoot 'root-files') | Out-Null }
    $rfxCount = 0
    Get-ChildItem $Wb -File -ErrorAction SilentlyContinue | Where-Object {
        $_.Name -notlike 'workbuddy.db*' -and $_.Name -notlike '*.log' -and $_.Name -notlike '*.tmp' -and $_.Length -lt 100MB
    } | ForEach-Object {
        $wxBytes += $_.Length
        $rfxCount++
        if (-not $DryRun) { Copy-Item $_.FullName (Join-Path $WxRoot 'root-files') -Force }
    }
    if ($rfxCount -gt 0) {
        $wxItems.Add([pscustomobject]@{ src='root-files'; dst='.'; desc="顶层零散文件（$rfxCount 个）" })
        Log ("  顶层零散文件 {0} 个" -f $rfxCount) 'DarkGray'
    }

    # ---- 兜底目录：.workbuddy 下其余目录（UI 索引/市场缓存/安全等）→ 还原到根部 ----
    foreach ($d in (Get-ChildItem $Wb -Directory -ErrorAction SilentlyContinue)) {
        $n = $d.Name
        if ($n -like 'user-*-personal') { continue }
        if ($n -eq $Acct) { continue }
        if ($WxCollected -contains $n) { continue }
        if ($WxSkipDirs -contains $n) { Log "  [skip] $n（可重装/可重下，未收集）" 'DarkGray'; continue }
        if ($SkipWbExtra -contains $n) { continue }
        $info = Get-TreeInfo $d.FullName
        if ($info.Bytes -gt 5GB) {
            Log ("  [skip] $n 过大（{0:N1} GB > 5GB）。确认需要请手工拷贝，或用 -SkipWbExtra 管理" -f ($info.Bytes/1GB)) 'Yellow'
            continue
        }
        $wxBytes += $info.Bytes
        if (-not $DryRun) { Copy-Tree $d.FullName (Join-Path $WxRoot $n) }
        $wxItems.Add([pscustomobject]@{ src=$n; dst=$n; desc=$n })
        Log ("  {0,-46} {1,8:N1} MB / {2} files" -f $n,($info.Bytes/1MB),$info.Files)
    }
    Log ("  wb-extra 数据层合计: {0:N1} MB" -f ($wxBytes/1MB)) 'Green'
    $wxMan = [pscustomobject]@{
        note = 'wb-extra 数据层清单：src 相对本目录，dst 相对 %USERPROFILE%\.workbuddy\。由 Build-WBMigration.ps1 生成。'
        accountUuid = $Acct
        items = $wxItems
    }
    [IO.File]::WriteAllText((Join-Path $WxRoot 'manifest.json'), ($wxMan | ConvertTo-Json -Depth 5), (New-Object Text.UTF8Encoding($false)))
}

# =========================================================
# 阶段 3：生成新电脑一键还原脚本
# =========================================================
Log '[3/6] 生成新电脑一键还原脚本...' 'Cyan'
New-Item -ItemType Directory -Force -Path $RestoreDir | Out-Null

$HasConfig   = $Scope -in @('full','config')
$HasProjects = ($Scope -in @('full','projects')) -and (($repos.Count + $plainDirs.Count) -gt 0)
$HasData     = ($Scope -in @('full','data')) -and ($wxItems.Count -gt 0)
# DryRun 下也生成全套脚本供检查
$GenProjects = $HasProjects -or $DryRun
$GenData     = $HasData -or $DryRun
if ($GenProjects) { New-Item -ItemType Directory -Force -Path $PkgData | Out-Null }
if ($GenData) { New-Item -ItemType Directory -Force -Path $WxRoot | Out-Null }

# ---------- restore-config.cmd（支持 auto 静默参数）----------
$rc = @'
@echo off
chcp 65001 >nul
if /i not "%~1"=="auto" (
echo ================================================
echo   WorkBuddy Migration - Restore Configuration
echo ================================================
echo.
echo This will copy to your new PC:
echo   .workbuddy\skills          user-level skills
echo   .workbuddy\user-*-personal long-term memory
echo   WorkBuddy\                 session workspaces
echo   .claude  opencode    ecosystem data（SSH 私钥需手工拷贝，见使用说明）
echo   mcp.json models.json settings.json .gitconfig
echo.
set /p ok=Type Y to continue:
if /i not "%ok%"=="Y" exit /b 1
)
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0restore-config.ps1"
'@
[IO.File]::WriteAllText((Join-Path $RestoreDir 'restore-config.cmd'), $rc, (New-Object Text.UTF8Encoding($false)))

# ---------- restore-config.ps1 ----------
$rps = @'
# WorkBuddy 配置层还原 —— 由 Build-WBMigration.ps1 生成
param([switch]$Auto)
$ErrorActionPreference = 'Continue'
$Here = $PSScriptRoot
$Home_ = $env:USERPROFILE
if (-not $Home_) { $Home_ = [Environment]::GetFolderPath('UserProfile') }
$cfg = Join-Path $Here 'config'
$wsParentRel = 'WorkBuddy'
$srcPersonal = @()
$manPath = Join-Path $Here 'config-manifest.json'
if (Test-Path $manPath) {
    try {
        $m = Get-Content $manPath -Raw -Encoding UTF8 | ConvertFrom-Json
        if ($m.wsParentRel) { $wsParentRel = $m.wsParentRel }
        if ($m.personalDirs) { $srcPersonal = @($m.personalDirs) }
    } catch {}
}
function Rc([string]$Src,[string]$Dst) {
    if (-not (Test-Path $Src)) { Write-Host ('  [skip] ' + (Split-Path $Src -Leaf)) -ForegroundColor DarkGray; return }
    New-Item -ItemType Directory -Force -Path $Dst | Out-Null
    $a = @($Src,$Dst,'/E','/NFL','/NDL','/NJH','/NJS','/NP','/R:1','/W:1')
    $null = & robocopy.exe @a
    $sc = (Get-ChildItem $Src -Recurse -File -ErrorAction SilentlyContinue).Count
    $dc = (Get-ChildItem $Dst -Recurse -File -ErrorAction SilentlyContinue).Count
    if ($dc -lt $sc) {
        Write-Host ('  [warn] ' + (Split-Path $Src -Leaf) + ': src ' + $sc + ' files, dst ' + $dc + ' - possibly blocked by security software; please re-run') -ForegroundColor Yellow
    } else {
        Write-Host ('  [ok] ' + (Split-Path $Src -Leaf) + ' -> ' + $Dst + ' (' + $dc + ' files)') -ForegroundColor Green
    }
}
Write-Host 'Restoring WorkBuddy configuration...'
Rc (Join-Path $cfg 'skills')      (Join-Path $Home_ '.workbuddy\skills')
$pRoot = Join-Path $cfg 'personal'
if (Test-Path $pRoot) {
    foreach ($d in (Get-ChildItem $pRoot -Directory -ErrorAction SilentlyContinue)) {
        Rc $d.FullName (Join-Path $Home_ ".workbuddy\$($d.Name)")
    }
}
Rc (Join-Path $cfg 'workspaces')  (Join-Path $Home_ $wsParentRel)
Rc (Join-Path $cfg 'claude')      (Join-Path $Home_ '.claude')
Rc (Join-Path $cfg 'opencode')    (Join-Path $Home_ '.local\share\opencode')
Rc (Join-Path $cfg '_root')       (Join-Path $Home_ '.workbuddy')
# 账号一致性提示
$tgt = Get-ChildItem (Join-Path $Home_ '.workbuddy') -Directory -Filter 'user-*-personal' -ErrorAction SilentlyContinue | Select-Object -First 1
if ($tgt -and $srcPersonal.Count -gt 0 -and ($srcPersonal -notcontains $tgt.Name)) {
    Write-Host ('  [info] new PC account (' + $tgt.Name + ') differs from source. Source long-term memory is kept under its original folder name; cloud memory syncs the current account automatically.') -ForegroundColor Cyan
}
Write-Host ''
Write-Host 'Configuration restored.' -ForegroundColor Green
'@
[IO.File]::WriteAllText((Join-Path $RestoreDir 'restore-config.ps1'), $rps, (New-Object Text.UTF8Encoding($true)))

# ---------- restore-projects.ps1 ----------
$rpps = @'
# WorkBuddy 项目层还原 —— 由 Build-WBMigration.ps1 生成
param([string]$TargetRoot = '')
$ErrorActionPreference = 'Continue'
$Here = $PSScriptRoot
$data = $Here
$Home_ = $env:USERPROFILE
if (-not $Home_) { $Home_ = [Environment]::GetFolderPath('UserProfile') }
$manPath = Join-Path $data 'manifest.json'
if (-not (Test-Path $manPath)) { Write-Host 'manifest.json not found' -ForegroundColor Red; exit 1 }
$man = Get-Content $manPath -Raw -Encoding UTF8 | ConvertFrom-Json

function Find-Git {
    $cands = @()
    $pg = Join-Path $Here 'git-portable\cmd\git.exe'
    if (Test-Path $pg) { $cands += $pg }
    $g = Get-Command git -ErrorAction SilentlyContinue
    if ($g) { $cands += $g.Source }
    foreach ($c in @("$env:ProgramFiles\Git\cmd\git.exe","${env:ProgramFiles(x86)}\Git\cmd\git.exe","$env:LOCALAPPDATA\Programs\Git\cmd\git.exe")) {
        if (Test-Path $c) { $cands += $c }
    }
    foreach ($c in $cands) { if (Test-Path $c) { return $c } }
    return $null
}
$git = Find-Git
if (-not $git) {
    Write-Host '  git not found, trying winget auto-install...' 'Yellow'
    $wg = Get-Command winget -ErrorAction SilentlyContinue
    if ($wg) {
        $null = & $wg.Source install --id Git.Git -e --source winget --accept-package-agreements --accept-source-agreements --disable-interactivity 2>&1
        $git = Find-Git
    }
}
if (-not $git) {
    Write-Host ''
    Write-Host '[ERROR] git unavailable.' -ForegroundColor Red
    Write-Host '  Option A: install Git for Windows, then re-run this script (already-restored repos are skipped)'
    Write-Host '          https://git-scm.com/download/win'
    Write-Host '  Option B: make sure project-data\git-portable\cmd\git.exe exists (no-install build)'
    exit 1
}
Write-Host ("Using git: " + $git) -ForegroundColor DarkGray
& $git --version

# ---- 目标根目录：优先源根目录（盘符仍在），否则第一个数据盘，否则 用户目录\Projects ----
$srcRoots = @()
foreach ($r in $man.repos) { if ($r.root -and ($srcRoots -notcontains $r.root)) { $srcRoots += $r.root } }
foreach ($d in $man.plainDirs) { if ($d.root -and ($srcRoots -notcontains $d.root)) { $srcRoots += $d.root } }
$fallback = ''
if ($TargetRoot) {
    $fallback = $TargetRoot
} else {
    $usable = @($srcRoots | Where-Object { Test-Path $_ })
    if ($usable.Count -gt 0) { $fallback = $usable[0] }
    else {
        $sysDrv = 'C:\'
        if ($env:SystemDrive) { $sysDrv = "$($env:SystemDrive)\" }
        try {
            foreach ($di in [IO.DriveInfo]::GetDrives()) {
                if ($di.DriveType -eq 'Fixed' -and $di.IsReady -and $di.Name -ne $sysDrv) { $fallback = $di.Name; break }
            }
        } catch {}
        if (-not $fallback) { $fallback = Join-Path $Home_ 'Projects' }
        New-Item -ItemType Directory -Force -Path $fallback | Out-Null
    }
}
Write-Host ("Target root: " + $fallback)
if ((-not $man.repos) -and ((-not $man.plainDirs) -or ($man.plainDirs.Count -eq 0))) {
    Write-Host 'Nothing to restore.'
    exit 0
}
$remapped = 0
foreach ($r in $man.repos) {
    $root = $r.root
    if ((-not $root) -or (-not (Test-Path $root))) { $root = $fallback; $remapped++ }
    $dst = Join-Path $root $r.name
    $bundle = Join-Path $data "git-bundles\$($r.name).bundle"
    if (-not (Test-Path $bundle)) {
        Write-Host ("  [skip] bundle missing: " + $r.name) -ForegroundColor Yellow
    } elseif (-not (Test-Path $dst)) {
        Write-Host ("  [clone] " + $r.name + " <- bundle (" + $r.bundleMB + " MB)")
        $null = & $git clone $bundle $dst 2>&1
        if ($LASTEXITCODE -ne 0 -or -not (Test-Path $dst)) {
            Write-Host ("  [FAIL] " + $r.name + " clone failed (exit=" + $LASTEXITCODE + ") - check git availability and re-run") -ForegroundColor Red
            continue
        }
        if ($r.remote) { $null = & $git -C $dst remote set-url origin "$($r.remote)" 2>&1 }
        else { $null = & $git -C $dst remote remove origin 2>$null }
        if ($r.branch) { $null = & $git -C $dst checkout "$($r.branch)" 2>&1 }
    } else {
        Write-Host ("  [exists] " + $r.name + " - skipped (delete it first if you want a fresh clone)")
    }
    $dirty = Join-Path $data "git-dirty\$($r.name)"
    if (Test-Path $dirty) {
        $a = @($dirty,$dst,'/E','/NFL','/NDL','/NJH','/NJS','/NP','/R:1','/W:1')
        $null = & robocopy.exe @a
        Write-Host ("         applied " + $r.dirtyFiles + " uncommitted files")
    }
}
if ($man.plainDirs) {
    foreach ($d in $man.plainDirs) {
        $root = $d.root
        if ((-not $root) -or (-not (Test-Path $root))) { $root = $fallback; $remapped++ }
        $src = Join-Path $data "plain\$($d.name)"
        $dst = Join-Path $root $d.name
        Write-Host ("  [copy] " + $d.name + " -> " + $dst)
        $a = @($src,$dst,'/E','/NFL','/NDL','/NJH','/NJS','/NP','/R:1','/W:1')
        $null = & robocopy.exe @a
    }
}
Write-Host ''
if ($remapped -gt 0) {
    Write-Host ("Note: " + $remapped + " item(s) were restored to " + $fallback + " because the original location does not exist on this PC.") -ForegroundColor Yellow
    Write-Host 'To use a different location: move the folders, or re-run with -TargetRoot <path>.' -ForegroundColor Yellow
}
Write-Host 'Projects restored.' -ForegroundColor Green
'@
if ($GenProjects) {
[IO.File]::WriteAllText((Join-Path $PkgData 'restore-projects.ps1'), $rpps, (New-Object Text.UTF8Encoding($true)))
# ---- 项目清单（restore-projects.ps1 的必需输入）----
$projMan = [pscustomobject]@{
    generated = $Stamp
    accountUuid = $Acct
    sourceUser = $Home_
    sourceMachine = $env:COMPUTERNAME
    repos = @($repos)
    plainDirs = @($plainDirs)
}
[IO.File]::WriteAllText((Join-Path $PkgData 'manifest.json'), ($projMan | ConvertTo-Json -Depth 4), (New-Object Text.UTF8Encoding($false)))
}

# ---------- restore-wbdata.ps1 ----------
$rw = @'
# WorkBuddy 数据层还原（wb-extra）—— 由 Build-WBMigration.ps1 生成
# 把 projects/workspace-sessions/blobs/记忆/索引等还原到 %USERPROFILE%\.workbuddy\
param([switch]$Auto)
$ErrorActionPreference = 'Continue'
$Here = $PSScriptRoot
$Home_ = $env:USERPROFILE
if (-not $Home_) { $Home_ = [Environment]::GetFolderPath('UserProfile') }
$WbDir = Join-Path $Home_ '.workbuddy'
$manPath = Join-Path $Here 'manifest.json'
if (-not (Test-Path $manPath)) {
    Write-Host ('manifest.json not found: ' + $manPath) -ForegroundColor Red
    exit 1
}
$man = Get-Content $manPath -Raw -Encoding UTF8 | ConvertFrom-Json
Write-Host ('WorkBuddy data dir: ' + $WbDir)
# 目标账号 UUID（新电脑登录后自动探测；探测不到则保持源账号名）
$tgtAcct = ''
$pd = Get-ChildItem $WbDir -Directory -Filter 'user-*-personal' -ErrorAction SilentlyContinue |
    Sort-Object LastWriteTime -Descending | Select-Object -First 1
if ($pd) { $tgtAcct = $pd.Name -replace '^user-','' -replace '-personal$','' }
if ($tgtAcct -and $man.accountUuid -and ($tgtAcct -ne $man.accountUuid)) {
    Write-Host ('  [info] account UUID differs (source ' + $man.accountUuid + ' -> target ' + $tgtAcct + '); account-specific data will be renamed automatically') -ForegroundColor Cyan
}
$fail = 0; $okCount = 0
foreach ($it in $man.items) {
    $src = Join-Path $Here $it.src
    $dst = Join-Path $WbDir $it.dst
    if (-not (Test-Path $src)) {
        Write-Host ('  [skip] missing: ' + $it.src) -ForegroundColor Yellow
        continue
    }
    if ($it.srcAcct -and $tgtAcct -and ($it.srcAcct -ne $tgtAcct)) {
        $dst = $dst -replace [regex]::Escape($it.srcAcct), $tgtAcct
    }
    New-Item -ItemType Directory -Force -Path (Split-Path $dst) | Out-Null
    $a = @($src,$dst,'/E','/NFL','/NDL','/NJH','/NJS','/NP','/R:1','/W:1')
    $null = & robocopy.exe @a
    if ($it.acctFiles) {
        foreach ($af in $it.acctFiles) {
            $from = Join-Path $dst ($af.from -replace '<ACCT>', $it.srcAcct)
            $to   = Join-Path $dst ($af.to   -replace '<ACCT>', $tgtAcct)
            if ((Test-Path $from -PathType Leaf) -and ($from -ne $to)) { Copy-Item $from $to -Force }
        }
    }
    if (Test-Path $dst) {
        $fc = (Get-ChildItem $dst -Recurse -File -ErrorAction SilentlyContinue).Count
        Write-Host ('  [ok] ' + $it.src + '  (' + $it.desc + ')  ' + $fc + ' files') -ForegroundColor Green
        $okCount++
    } else {
        Write-Host ('  [FAIL] ' + $it.src) -ForegroundColor Red
        $fail++
    }
}
Write-Host ''
if ($fail -gt 0) {
    Write-Host ($fail.ToString() + ' item(s) failed. Re-run this script to retry (finished items are merged/skipped).') -ForegroundColor Red
} else {
    Write-Host ('WorkBuddy data restored: ' + $okCount.ToString() + ' items. Restart WorkBuddy to see everything.') -ForegroundColor Green
}
'@
if ($GenData) {
[IO.File]::WriteAllText((Join-Path $WxRoot 'restore-wbdata.ps1'), $rw, (New-Object Text.UTF8Encoding($true)))
}

# ---------- 1-oneclick-restore.cmd（配置层入口）----------
$oneClick = @'
@echo off
chcp 65001 >nul
title WorkBuddy Migration - One-click Restore (config layer)
echo ================================================
echo   WorkBuddy Migration - One-click Restore
echo ================================================
echo.
set "ZIP=%~dp0WorkBuddy-Migration.zip"
set "OUT=%TEMP%\wbmig-restore"
if not exist "%ZIP%" (
  echo [ERROR] WorkBuddy-Migration.zip not found next to this script.
  pause
  exit /b 1
)
echo Extracting package...
if exist "%OUT%" rmdir /s /q "%OUT%"
mkdir "%OUT%"
tar -xf "%ZIP%" -C "%OUT%" 2>nul
if errorlevel 1 powershell -NoProfile -ExecutionPolicy Bypass -Command "Expand-Archive -LiteralPath '%ZIP%' -DestinationPath '%OUT%' -Force"
echo.
echo Starting configuration restore...
cd /d "%OUT%"
call restore-config.cmd
'@
if ($HasConfig -or $DryRun) {
[IO.File]::WriteAllText((Join-Path $OutputRoot '1-oneclick-restore.cmd'), $oneClick, (New-Object Text.UTF8Encoding($false)))
}

# ---------- 2-restore-projects.cmd（项目层入口，按需链式接数据层）----------
if ($HasData) {
    $rp = @'
@echo off
chcp 65001 >nul
if /i not "%~1"=="auto" (
echo ================================================
echo   WorkBuddy Migration - Restore Projects + Data
echo ================================================
echo.
echo Part 1: clone all bundles + apply uncommitted files + copy data dirs
echo         project-data\git-portable provides a no-install git fallback
echo Part 2 (auto): restore WorkBuddy data layer
echo.
set /p ok=Type Y to continue:
if /i not "%ok%"=="Y" exit /b 1
)
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0project-data\restore-projects.ps1"
if errorlevel 1 (
  echo.
  echo [ERROR] project restore failed. Fix the issue and re-run 2-restore-projects.cmd.
  pause
  exit /b 1
)
echo.
echo ================================================
echo   Projects done. Now restoring WorkBuddy data layer...
echo ================================================
call "%~dp03-restore-wbdata.cmd" %1
'@
} else {
    $rp = @'
@echo off
chcp 65001 >nul
if /i not "%~1"=="auto" (
echo ================================================
echo   WorkBuddy Migration - Restore Projects
echo ================================================
echo.
set /p ok=Type Y to continue:
if /i not "%ok%"=="Y" exit /b 1
)
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0project-data\restore-projects.ps1"
if errorlevel 1 (
  echo.
  echo [ERROR] project restore failed. Fix the issue and re-run 2-restore-projects.cmd.
  pause
  exit /b 1
)
'@
}
if ($GenProjects) {
[IO.File]::WriteAllText((Join-Path $OutputRoot '2-restore-projects.cmd'), $rp, (New-Object Text.UTF8Encoding($false)))
}

# ---------- 3-restore-wbdata.cmd ----------
if ($GenData) {
    $rc3 = @'
@echo off
chcp 65001 >nul
title WorkBuddy Migration - Restore WB Data Layer
if /i not "%~1"=="auto" (
echo ================================================
echo   WorkBuddy Migration - Restore WB Data Layer
echo ================================================
echo.
echo This restores to %USERPROFILE%\.workbuddy\ :
echo   projects\               session conversation history
echo   workspace\sessions\     file-modification backup snapshots
echo   blobs\                  artifact images
echo   memory / plans / scripts / backups / connectors / storage
echo   UI indexes, sidebar snapshots, root config files
echo.
set /p ok=Type Y to continue:
if /i not "%ok%"=="Y" exit /b 1
)
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0project-data\wb-extra\restore-wbdata.ps1"
'@
    [IO.File]::WriteAllText((Join-Path $OutputRoot '3-restore-wbdata.cmd'), $rc3, (New-Object Text.UTF8Encoding($false)))
}

# ---------- 一键恢复.cmd（总入口：1 -> 2(->3) 全自动）----------
$master = @'
@echo off
chcp 65001 >nul
title WorkBuddy 一键恢复（新电脑）
echo ================================================================
echo   WorkBuddy 一键恢复
echo   将自动依次还原：配置层 - 项目层 - 数据层
echo ================================================================
echo.
echo  [安全提示] 本包含 API 密钥等凭证数据，请勿上传公有网盘。SSH 私钥不在自动收集范围（需按使用说明手工拷贝）。
echo.
set /p ok=输入 Y 开始一键恢复（其它键取消）:
if /i not "%ok%"=="Y" exit /b
echo.
echo [1/3] 还原配置层...
if exist "%~dp0WorkBuddy-Migration.zip" (
  set "OUT=%TEMP%\wbmig-restore"
  if exist "%OUT%" rmdir /s /q "%OUT%"
  mkdir "%OUT%"
  tar -xf "%~dp0WorkBuddy-Migration.zip" -C "%OUT%" 2>nul
  if errorlevel 1 powershell -NoProfile -ExecutionPolicy Bypass -Command "Expand-Archive -LiteralPath '%~dp0WorkBuddy-Migration.zip' -DestinationPath '%OUT%' -Force"
  if exist "%OUT%\restore-config.cmd" (
    pushd "%OUT%"
    call restore-config.cmd auto
    if errorlevel 1 ( popd & echo 已取消。 & pause & exit /b 1 )
    popd
  ) else (
    echo   [warn] 解压失败或无 restore-config.cmd，跳过配置层
  )
) else (
  echo   [warn] 未找到 WorkBuddy-Migration.zip，跳过配置层
)
echo.
echo [2/3] 还原项目层...
if exist "%~dp02-restore-projects.cmd" (
  call "%~dp02-restore-projects.cmd" auto
  if errorlevel 1 ( echo [ERROR] 项目层还原失败，请排查后重跑 2-restore-projects.cmd & pause & exit /b 1 )
) else if exist "%~dp03-restore-wbdata.cmd" (
  echo   [skip] 本包不含项目层，直接还原数据层
  call "%~dp03-restore-wbdata.cmd" auto
) else (
  echo   [skip] 本包不含项目层与数据层
)
echo.
echo ================================================================
echo   一键恢复完成！重启 WorkBuddy 查看效果。
echo   手工收尾事项见 使用说明.txt / 环境清单.txt
echo ================================================================
pause
'@
[IO.File]::WriteAllText((Join-Path $OutputRoot '一键恢复.cmd'), $master, (New-Object Text.UTF8Encoding($false)))
Log '  还原脚本已生成：一键恢复.cmd / 1 / 2 / 3（新电脑双击即用）' 'Green'

# =========================================================
# 阶段 4：环境清单
# =========================================================
if (-not $DryRun) {
    Log '[4/6] 导出环境清单...' 'Cyan'
    $envFile = Join-Path $OutputRoot '环境清单.txt'
    $lines = @()
    $lines += '新电脑需要安装的工具链（对照本清单）'
    $lines += '======================================='
    $lines += ''
    $lines += '-- 本机检测到的开发工具（新电脑建议安装同样版本）--'
    $toolMap = [ordered]@{
        'git'    = 'Git for Windows（含 git-bash；若不装，包内便携 git 可替代）'
        'python' = 'Python 3.x'
        'node'   = 'Node.js LTS'
        'npm'    = 'npm（随 Node 安装）'
        'go'     = 'Go 1.x'
        'qmake'  = 'Qt 5.x（qmake/MinGW 或 MSVC）'
        'pyinstaller' = 'PyInstaller（pip install pyinstaller）'
        'opencode' = 'opencode'
        'docker' = 'Docker Desktop'
        'ffmpeg' = 'ffmpeg'
        'code'   = 'VS Code'
    }
    $foundTools = @()
    foreach ($t in $toolMap.Keys) {
        if (Get-Command $t -ErrorAction SilentlyContinue) { $foundTools += $t }
    }
    if ($foundTools.Count -gt 0) {
        foreach ($t in $foundTools) { $lines += "  [已装] $t  ->  $($toolMap[$t])" }
    } else {
        $lines += '  （未检测到常见开发工具）'
    }
    $lines += ''
    $lines += '-- 本机已装软件（注册表导出，供对照）--'
    try {
        $keys = @('HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*','HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*','HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*')
        $apps = foreach ($k in $keys) {
            Get-ItemProperty $k -ErrorAction SilentlyContinue |
                Where-Object { $_.DisplayName } |
                Select-Object -ExpandProperty DisplayName -Unique
        }
        $apps | Sort-Object | ForEach-Object { $lines += "  $_" }
    } catch {}
    $lines += ''
    $lines += '-- 无法自动迁移、需手工处理的项 --'
    $lines += '1. 连接器授权：腾讯文档等 connector 在新电脑重新扫码授权'
    $lines += '2. Chrome：登录 Google 账号同步书签/扩展'
    $lines += '3. claude-code-third-party-model 切换器：还原后打开一次，会自动拉起 ccproxy 网关 + zen_bridge'
    $lines += '4. git 推送认证：私钥未随包迁移（需要的话按使用说明手工拷贝 SSH 配置目录），或改用 HTTPS+PAT'
    $lines += '5. Windows 凭据管理器里的 git 密码：新电脑首次 push 时重新输入'
    $lines += '6. DPAPI 加密的本地凭据（keyblob/credentials/keys）：跨机无效，需重新授权'
    $lines += '7. 系统级软件（按需重装），数据已在 project-data'
    [IO.File]::WriteAllLines($envFile, $lines, (New-Object Text.UTF8Encoding($true)))
    Log '  环境清单.txt 已导出' 'Green'
}

# =========================================================
# 阶段 5：打 zip 包 + 使用说明
# =========================================================
$zipOut = Join-Path $OutputRoot 'WorkBuddy-Migration.zip'
if ((-not $DryRun) -and $HasConfig) {
    Log '[5/6] 打包配置层 zip...' 'Cyan'
    if (Test-Path $zipOut) { Remove-Item $zipOut -Force }
    $zipMB = 0
    if (Test-Path $tarExe) {
        $null = & $tarExe -a -c -f $zipOut -C $RestoreDir .
        $rc = $LASTEXITCODE
        if (Test-Path $zipOut) { $zipMB = (Get-Item $zipOut).Length/1MB }
        Log ("  tar zip 包: {0:N1} MB (exit=$rc)" -f $zipMB) 'DarkGray'
    } elseif (Test-Path $sevenZip) {
        $null = & $sevenZip a -tzip -mx=1 $zipOut "$RestoreDir\*"
        $rc = $LASTEXITCODE
        if (Test-Path $zipOut) { $zipMB = (Get-Item $zipOut).Length/1MB }
        Log ("  7z zip 包: {0:N1} MB (exit=$rc)" -f $zipMB) 'DarkGray'
    } else {
        Compress-Archive -Path "$RestoreDir\*" -DestinationPath $zipOut -CompressionLevel Optimal
        if (Test-Path $zipOut) { $zipMB = (Get-Item $zipOut).Length/1MB }
        Log ("  Compress-Archive zip 包: {0:N1} MB" -f $zipMB) 'DarkGray'
    }
    if ((-not (Test-Path $zipOut)) -or ($zipMB -lt 1)) { Log '  [错误] zip 包异常小或缺失，配置层可能未压入' 'Red' }

    # ---- 使用说明 ----
    Log '[6/6] 生成使用说明...' 'Cyan'
    $readme = Join-Path $OutputRoot '使用说明.txt'
    $total = (Get-ChildItem $OutputRoot -Recurse -File -ErrorAction SilentlyContinue | Measure-Object -Sum Length).Sum
    $r = @()
    $r += 'WorkBuddy 换电脑迁移包 - 使用说明'
    $r += '生成时间: ' + (Get-Date -Format 'yyyy-MM-dd HH:mm')
    $r += '源用户: ' + $Home_ + '  (' + $env:COMPUTERNAME + ')'
    $r += '源账号 UUID: ' + $(if ($Acct) { $Acct } else { '未记录' })
    $r += '打包范围: ' + $Scope
    $r += '包总大小: ' + ("{0:N1} MB" -f ($total/1MB))
    $r += ''
    $r += '========== 旧电脑侧（已完成）=========='
    $r += '把整个文件夹拷到移动硬盘。'
    $r += '注意：包含 API 密钥等凭证数据，不要上传公有网盘/微信。SSH 私钥不在自动收集范围，如需迁移请按下方手工步骤拷贝。'
    $r += ''
    $r += '========== 新电脑侧 =========='
    $r += '前置：安装 WorkBuddy（同版本），登录同一账号。'
    $r += '      资料库/云记忆/定时任务会自动恢复；连接器重新授权一次。'
    $r += ''
    $r += '方式 A（推荐，真正一键）：双击 一键恢复.cmd'
    $r += '      自动依次执行：配置层 -> 项目层 -> 数据层'
    $r += ''
    $r += '方式 B（分步，可单独重跑某层）：'
    $r += '  第 1 步 双击 1-oneclick-restore.cmd   配置层（技能/长期记忆/工作区/.claude/opencode/三份配置/.gitconfig）'
    $r += '  第 2 步 双击 2-restore-projects.cmd   项目层（clone 所有 bundle + 未提交文件 + 数据目录）'
    $r += '  第 3 步 双击 3-restore-wbdata.cmd     数据层（会话历史/修改备份/blob/记忆/索引）'
    $r += ''
    $r += '无需预装 git / 7z：配置层用 Windows 自带 tar 解压；项目层内置免安装 git。'
    $r += '原项目盘符不存在时，项目会落到第一个数据盘（或 用户目录\Projects），脚本会明确提示。'
    $r += ''
    $r += '========== 手工收尾（见 环境清单.txt）=========='
    $r += '- 开发工具链按需安装（环境清单.txt 列出了本机已装软件）'
    $r += '- Chrome 登录 Google 账号同步；相关扩展重新加载'
    $r += '- claude-code-third-party-model 切换器打开一次（自动拉网关）'
    $r += '- 首次 git push 重新输入凭据（SSH 私钥未自动迁移，需按下述手工步骤处理）'
    $r += '- [可选] 迁移 git 推送私钥（本包不含，避免密钥随包扩散风险）：'
    $r += '    旧电脑: 把用户目录下的 SSH 配置目录（隐藏目录，存放推送私钥）用加密U盘单独拷贝'
    $r += '    新电脑: 放回用户目录同名位置，并收回继承权限仅当前用户可读（完整命令见排障手册）'
    $r += '    不需要 git SSH 推送可跳过本条，改用 HTTPS + PAT 认证。'
    $r += '- 已删除但未提交的文件不会随"未提交文件"还原（bundle 里有已提交版本，按需手动处理）'
    $r += ''
    $r += '========== 目录结构 =========='
    $r += '  一键恢复.cmd            ★ 新电脑唯一需要双击的文件'
    $r += '  1-oneclick-restore.cmd  分步：配置层'
    $r += '  2-restore-projects.cmd  分步：项目层（跑完自动接数据层）'
    $r += '  3-restore-wbdata.cmd    分步：数据层'
    $r += '  WorkBuddy-Migration.zip 配置层数据'
    $r += '  使用说明.txt / 环境清单.txt'
    $r += '  project-data\'
    $r += ('    git-bundles\   ' + $repos.Count + ' 个仓库 bundle（含全部历史）')
    $r += '    git-dirty\     未提交的工作区文件'
    $r += ('    plain\         ' + $plainDirs.Count + ' 个非 git 数据目录')
    $r += '    git-portable\  免安装 git（新电脑无 git 时的自动后备）'
    $r += ('    wb-extra\      WorkBuddy 数据层（' + $wxItems.Count + ' 项，约 ' + ("{0:N1}" -f ($wxBytes/1MB)) + ' MB）')
    $r += '  _stage\          打包中间产物，验证无误后可删'
    [IO.File]::WriteAllLines($readme, $r, (New-Object Text.UTF8Encoding($true)))
    Log '  使用说明.txt 已生成' 'Green'

    Log ''
    Log '==========================================' 'Cyan'
    Log (" 打包完成！总大小: {0:N1} MB" -f ($total/1MB)) 'Green'
    Log (" 位置: $OutputRoot") 'Green'
    Log ('  - 一键恢复.cmd  ' + $(if (Test-Path (Join-Path $OutputRoot '一键恢复.cmd')) { 'OK' } else { 'MISSING' }))
    Log ('  - WorkBuddy-Migration.zip  ' + $(if (Test-Path $zipOut) { 'OK' } else { 'MISSING' }))
    Log '  - 1 / 2 / 3 分步还原入口'
    Log '  - project-data\（项目数据 + 数据层）'
    Log '  - 使用说明.txt / 环境清单.txt'
    Log '==========================================' 'Cyan'
} else {
    Log ''
    Log 'DryRun 完成。还原脚本与清单已生成在 _stage\ 供检查。' 'Yellow'
    Log ("预估总体积: 配置 {0:N1} MB + 项目数据 {1:N1} MB + git bundle（未估）+ 数据层 {2:N1} MB" -f ($cfgBytes/1MB),($plainBytes/1MB),($wxBytes/1MB)) 'Yellow'
    Log '确认无误后去掉 -DryRun 实跑（或双击 一键制作迁移包.cmd）。' 'Yellow'
}

# Windows 安全清理路径参考

本文档列出了 Windows 系统上已知的可安全清理路径，以及需要谨慎处理的路径。
扫描脚本会参考此文档决定哪些路径标记为安全、哪些需要用户确认。

## 🟢 安全清理路径

### 系统临时文件
| 路径 | 说明 | 备注 |
|------|------|------|
| `%TEMP%` | 用户临时文件夹 | 通常 `C:\Users\<user>\AppData\Local\Temp` |
| `C:\Windows\Temp` | 系统临时文件夹 | 需要管理员权限 |
| `C:\Windows\SoftwareDistribution\Download` | Windows Update 下载缓存 | 清理前需停止 wuauserv 服务 |
| `C:\Windows\Prefetch` | 预读缓存 | 可安全清理，会自动重建，但清理后短期内启动可能稍慢 |

### 错误报告和日志
| 路径 | 说明 |
|------|------|
| `%LOCALAPPDATA%\CrashDumps` | 应用崩溃转储 |
| `%LOCALAPPDATA%\Microsoft\Windows\WER` | Windows 错误报告（用户级） |
| `C:\ProgramData\Microsoft\Windows\WER` | Windows 错误报告（系统级） |
| `C:\Windows\Logs` 中超过30天的文件 | 系统日志 |

### 缩略图和图标缓存
| 路径 | 说明 |
|------|------|
| `%LOCALAPPDATA%\Microsoft\Windows\Explorer\thumbcache_*` | 缩略图缓存 |
| `%LOCALAPPDATA%\Microsoft\Windows\Explorer\iconcache_*` | 图标缓存 |

### 浏览器缓存

#### Chrome
- `%LOCALAPPDATA%\Google\Chrome\User Data\Default\Cache`
- `%LOCALAPPDATA%\Google\Chrome\User Data\Default\Code Cache`
- `%LOCALAPPDATA%\Google\Chrome\User Data\Default\Service Worker\CacheStorage`

#### Edge
- `%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Cache`
- `%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Code Cache`

#### Firefox
- `%LOCALAPPDATA%\Mozilla\Firefox\Profiles\*\cache2`

#### Brave
- `%LOCALAPPDATA%\BraveSoftware\Brave-Browser\User Data\Default\Cache`

**注意**：清理浏览器缓存前建议先关闭对应浏览器。

### 开发工具缓存

| 工具 | 缓存路径 | 清理命令 |
|------|---------|---------|
| npm | `%APPDATA%\npm-cache` | `npm cache clean --force` |
| yarn | `%LOCALAPPDATA%\Yarn\Cache` | `yarn cache clean` |
| pnpm | `%LOCALAPPDATA%\pnpm\store` | `pnpm store prune` |
| pip | `%LOCALAPPDATA%\pip\cache` | `pip cache purge` |
| conda | `%USERPROFILE%\.conda\pkgs` | `conda clean --all -y` |
| NuGet | `%LOCALAPPDATA%\NuGet\v3-cache` | `dotnet nuget locals all --clear` |
| Gradle | `%USERPROFILE%\.gradle\caches` | 手动删除 |
| Maven | `%USERPROFILE%\.m2\repository` | 手动删除（注意本地发布的包）|
| Go | `%LOCALAPPDATA%\go-build` | `go clean -cache` |
| Rust/Cargo | `%USERPROFILE%\.cargo\registry\cache` | `cargo cache --autoclean` |
| Docker | - | `docker system prune -af` |

### 其他应用缓存
| 路径 | 说明 |
|------|------|
| `%LOCALAPPDATA%\Microsoft\Windows\INetCache` | IE/Edge 临时文件 |
| `%LOCALAPPDATA%\Temp` | 某些应用的临时文件 |
| `%APPDATA%\Code\Cache` | VS Code 缓存 |
| `%APPDATA%\Code\CachedData` | VS Code 编译缓存 |
| `%APPDATA%\Code\CachedExtensionVSIXs` | VS Code 扩展缓存 |

## 🟡 需用户确认的路径

| 路径 | 原因 |
|------|------|
| `%USERPROFILE%\Downloads` | 可能有用户需要的文件 |
| `%USERPROFILE%\Desktop` 上的大文件 | 用户主动放置的文件 |
| `C:\Windows.old` | 旧系统备份，某些情况下可能需要回滚 |
| 项目中的 `node_modules` | 删除后需 `npm install` 重新安装 |
| Python 虚拟环境 (`.venv`, `venv`) | 删除后需重新创建 |
| Conda 环境 (`%USERPROFILE%\.conda\envs`) | 删除后需重新创建 |
| `%USERPROFILE%\.m2\repository` | Maven 可能有本地发布的包 |
| Docker 卷 (`docker volume ls`) | 可能包含持久化数据 |

## 🔴 绝对不能碰的路径

以下路径在任何情况下都不应被扫描或建议删除：

- `C:\Windows\` （SoftwareDistribution\Download 除外）
- `C:\Program Files\`
- `C:\Program Files (x86)\`
- `C:\ProgramData\` （除已知缓存子目录外）
- `C:\Recovery\`
- `C:\System Volume Information\`
- `C:\$Recycle.Bin\` （应通过系统 API 清空回收站）
- 任何 `.git` 目录
- 任何 `*.sys` 文件（如 `pagefile.sys`, `hiberfil.sys`, `swapfile.sys`）
- 注册表相关文件
- 任何正在被进程占用的文件
- 用户的文档/图片/视频/音乐目录（除非用户明确要求查找大文件）

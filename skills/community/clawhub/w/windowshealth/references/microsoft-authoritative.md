# Microsoft 官方权威方案 · windows-health 基线（2026-08-07）

> 用途：windows-health 诊断与治理建议的权威锚点。所有结论优先对齐 Microsoft 官方口径。

## 来源索引

| # | 来源 | 用途 |
|---|---|---|
| 1 | [cleanmgr（磁盘清理）](https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/cleanmgr) | 磁盘清理命令行：/sageset、/sagerun |
| 2 | [自动化磁盘清理工具](https://learn.microsoft.com/zh-cn/troubleshoot/windows-server/backup-and-storage/automating-disk-cleanup-tool) | cleanmgr 自动化开关 |
| 3 | [存储感知 Storage Sense](https://learn.microsoft.com/zh-cn/windows/configuration/storage/storage-sense) | 内置自动清理：临时文件/回收站/OneDrive 脱机内容 |
| 4 | [清理 WinSxS 文件夹](https://learn.microsoft.com/zh-cn/windows-hardware/manufacture/desktop/clean-up-the-winsxs-folder) | 组件存储清理：DISM /AnalyzeComponentStore → /StartComponentCleanup（/ResetBase 不可逆） |
| 5 | [干净启动 clean boot](https://support.microsoft.com/help/929135) | msconfig 排查后台干扰 |
| 6 | [启动应用管理](https://support.microsoft.com/windows/9115d841-735e-488d-e749-9ba301d441e6) | 设置>应用>启动 / 任务管理器>启动应用 |
| 7 | [监视 Windows 客户端性能](https://learn.microsoft.com/zh-cn/training/modules/monitor-troubleshoot-windows-client-performance/4-monitor-windows-client-performance) | 任务管理器性能页 + 资源监视器 perfmon /res |

## 官方方案 → windows-health 动作映射

| 用户场景 | Microsoft 官方步骤 | windows-health 动作 | 授权等级 |
|---|---|---|---|
| C 盘空间不足 | 存储感知/磁盘清理 → cleanmgr → 卸载不用 App → 清空回收站 → 清 Windows 更新残留 | 报告按此顺序出建议；TIER 1 缓存 + 大文件 + 回收站检查 | DELETE_SAFE（明确缓存）；其余逐项确认 |
| WinSxS 大 | DISM /AnalyzeComponentStore 判断 → StartComponentCleanup（需管理员） | 只展示官方路径与后果；不代跑、不直接删 | PLAN_ONLY + 用户提权后自行执行 |
| 开机慢/启动项多 | 设置>应用>启动 / 任务管理器>启动应用；逐项禁用 | Get-CimInstance Win32_StartupCommand 现状 + 逐项确认 | 逐项授权后执行 |
| 卡顿/高占用 | 任务管理器性能页 / perfmon /res 定位 | 性能诊断先定位进程 → 建议退出/禁用/重启 | 建议动作（不删除） |
| 后台干扰 | 干净启动（msconfig，隐藏 Microsoft 服务） | 输出官方步骤，由用户操作 | 用户自行操作 |

## 判定速查

- 内存：`Get-CimInstance Win32_OperatingSystem` 的 TotalVisibleMemorySize / FreePhysicalMemory；页面文件打满 = 内存不足强信号（对应任务管理器性能页）。
- WinSxS：先看 `/AnalyzeComponentStore` 输出的「Component Store Cleanup Recommended」；`/ResetBase` 不可逆（失去卸载旧更新能力）。
- 启动项：用户级（HKCU\...\Run、启动文件夹）普通权限可管理；系统级（HKLM、服务）需管理员。
- OneDrive：区分云端本体与本地按需下载副本；释放空间用「释放空间」语义，不删云端。

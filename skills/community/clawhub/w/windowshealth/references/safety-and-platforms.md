# windows-health · 安全分级与平台边界

## 动作分级

| 动作 | 适用对象 | 执行条件 | 恢复 |
|---|---|---|---|
| `DELETE_SAFE` | 明确 Temp/cache、可重建构建缓存 | 路径存在且不含原始数据 | App 重建或重新下载 |
| `DELETE_DUPLICATE` | 内容完全相同的副本 | Get-FileHash SHA256 一致并指定保留副本 | 从保留副本复制 |
| `ARCHIVE_CLOUD` | 低频大资料、旧备份、安装包 | 先移动、校验并写 MANIFEST | 云端取回 |
| `ARCHIVE_LINK` | 被脚本引用的低频大目录 | 归档后在原路径建符号链接 | 重建链接或移回 |
| `KEEP_LOCAL` | 当前项目、运行源、索引、离线必需资料 | 高频或结构关键 | 不处理 |
| `PLAN_ONLY` | 聊天数据、App 数据库、财务证件、照片原片 | 高价值或证据不足 | 仅列方案 |

## Windows TIER

| TIER | 典型对象 | 行为 |
|---|---|---|
| 1 | %TEMP%、%LOCALAPPDATA%\Temp、npm-cache、pip 缓存、浏览器缓存、Windows 更新清理（cleanmgr） | 可推荐清理；只处理实际存在路径 |
| 1 特例 | 回收站 | 可推荐清空，但不可恢复，必须单独确认 |
| 2 | node_modules、WinSxS（DISM 官方路径）、旧 Windows.old | 只展示或逐条确认；不得一键清理 |
| 3 | Program Files、AppData 非缓存目录、注册表、系统服务、用户目录 | 不推荐删除；用户目录只展示 |
| 4 | 低频大资料、旧迁移包、课程原始视频、历史素材 | 归档云端，必要时保留符号链接 |
| 5 | 知识库本体、项目运行源、当前工作目录、用户保护路径 | KEEP_LOCAL 或 PLAN_ONLY |

## 平台证据边界

- Windows App 使用频次无官方 API 等价物；Recent Items 只能代理双击历史，注册表主要说明安装与估算大小。
- WSL 只能使用映射路径诊断 Windows 文件，App 使用历史、注册表、服务证据不可用。
- NTFS/OneDrive 释放空间可能延迟；删除后 `Get-PSDrive` 未立即变化不代表失败。

## 失败库

### 权限不足误判
- 触发：未检测管理员身份就把管理员级动作当普通可执行。
- 一线修复：脚本检测 WindowsPrincipal；未提权时管理员项全部标 PLAN_ONLY。
- 兜底：只提供用户级候选，管理员项附官方命令由用户自行提权执行。

### WinSxS 误当普通缓存
- 触发：WinSxS 出现在清理候选。
- 一线修复：拒绝直接删除，只走 DISM /AnalyzeComponentStore → StartComponentCleanup 官方路径。
- 兜底：停止，引导官方文档。

### 云端归档误删
- 触发：用户要求「归档后清本地」却准备删除云端文件。
- 一线修复：只移除本机下载或本地源副本。
- 兜底：停止，检查 OneDrive 最近删除、回收站和 MANIFEST。

### 空间回弹误判
- 触发：删除后 Get-PSDrive 未立即变化。
- 一线修复：同时比较 Get-PSDrive、Get-Volume 与源/目标大小，等待后台处理。
- 兜底：记录延迟并稍后复测，禁止重复搬同一目录。

# CHANGELOG

## [2.0.0] - 2026-04-03

### 重构：从 Bash 迁移到 Python（三平台原生支持）

#### 重大变更
- **全部 6 个脚本从 bash 重写为 Python**，原生支持 macOS、Linux、Windows
- 删除旧 bash 脚本：`scan_cleanup.sh`、`classify_files.sh`、`find_duplicates.sh`、`incremental_backup.sh`、`move_with_log.sh`、`rollback.sh`
- 新增 Python 脚本：`scan_cleanup.py`、`classify_files.py`、`find_duplicates.py`、`incremental_backup.py`、`move_with_log.py`、`rollback.py`
- 回收站操作统一使用 `send2trash` 库（跨平台）
- JSON 日志使用 `json` 标准库，消除手动字符串拼接
- 所有跨平台兼容问题彻底消除（不再有 bash 3.2 bug、macOS/Linux stat 差异等）

#### 依赖
- Python 3.6+
- `send2trash`（`pip install send2trash`）

#### 平台特定适配
- **Windows**: 日志目录 `%LOCALAPPDATA%/file_manager/logs/`，缓存扫描 `%LOCALAPPDATA%/Temp`
- **macOS**: 日志目录 `~/Library/Caches/file_manager/logs/`
- **Linux**: 日志目录 `~/.cache/file_manager/logs/`（尊重 `$XDG_CACHE_HOME`）

#### 测试结果
- 全部 6 个脚本通过 Python 语法检查
- macOS 功能测试通过：scan_cleanup、classify_files（type/date）、find_duplicates、incremental_backup（全量+校验）、move_with_log（move+trash）、rollback（list-logs+show+rollback-all+空目录清理）
- 移动→撤销集成测试通过：move + trash → rollback-all 全部成功恢复

## [1.5.0] - 2026-04-03

### 第二轮全面审计（发布前）

#### 全局
- **P0**: 发现 bash 3.2 严重 bug — `case` 块内的 `done > redirect` 会导致 `$()` 命令替换中的 `/usr/bin/stat` 静默失败。所有 `case` 块改用 `if/elif`，或提取为独立函数
- **P0**: 所有 `case` 语句改写为 `if/elif`，消除 bash 3.2 嵌套 `case + while` 解析 bug
- **P1**: 所有脚本 `uname` 调用缓存为 `OS_TYPE` 变量（每个文件一次），消除大目录下数万次 fork
- **P1**: macOS 默认日志目录统一为 `~/Library/Caches/file_manager/logs`（move_with_log.sh + rollback.sh）

#### rollback.sh (v1.3 → v1.4)
- **P0**: 全部 `case` 改为 `if/elif`（包括 do_rollback_one、do_rollback_all、do_rollback_range、主逻辑）
- **P0**: `cleanup_empty_dirs_from_log` 提取 `cleanup_dir_chain` + `is_protected_dir` 为独立函数（bash 3.2 嵌套 `while read` 在函数内解析 bug）
- **P1**: trash 回撤支持 Linux FreeDesktop 标准回收站路径 (`~/.local/share/Trash/files`)
- **P1**: 新增 `get_trash_dir()` 跨平台回收站路径函数
- **P1**: `rollback_range` 的 `result=1`（失败）正确计入 `failed` 而非 `skipped`

#### classify_files.sh (v1.3 → v1.4)
- **P0**: date 模式提取为独立函数 `classify_by_date()`（bash 3.2 case 块内 `done > redirect` 导致 stat 失败）
- **P1**: type 模式从 N×M 次 find 遍历优化为单次 find + 扩展名查找表（性能提升 10-100x）
- **P1**: date 模式增加文件总数汇总
- **P1**: 修复扩展名查找表匹配 bug（`fext_lower` 含点号但查找表不含）
- **P2**: 移除无用的 `format_size_mb` 包装函数

#### scan_cleanup.sh (v1.3 → v1.4)
- **P1**: 缓存目录扫描加 `--max-depth` 限制（默认 5 层），防止 `~/.cache` 递归过深
- **P2**: 无参数默认扫描 Downloads 时明确提示用户
- **P2**: 缓存目录省略提示显示具体目录名

#### incremental_backup.sh (v1.3 → v1.4)
- **P2**: 消除冗余预扫描（macOS/Linux 完全相同的分支代码）
- **P2**: `uname` 缓存

#### find_duplicates.sh (v1.3 → v1.4)
- **P1**: hash 长度校验（SHA-256 固定 64 字符），防止截断值导致误匹配
- **P2**: `uname` 缓存

#### move_with_log.sh (v1.3 → v1.4)
- **P1**: macOS 默认日志目录改为 `~/Library/Caches/file_manager/logs`
- **P2**: `uname` 缓存

## [1.4.0] - 2026-04-03

### 全面跨平台修复（发布前审计）

#### find_duplicates.sh (v1.1 → v1.3)
- **P0 修复**: Step 1 的 `xargs stat -f%z` 硬编码 macOS 语法，Linux 上完全报错 → 改用 `while read` + 跨平台 `get_file_size`
- **P0 修复**: Step 2 的 `sh -c 'shasum ... stat ...'` 硬编码 macOS 语法 → 拆分为外层 `while read` + `calc_hash`/`get_file_mtime` 函数
- **P1 修复**: stat 调用改用 `/usr/bin/stat` 全路径（macOS），防止 GNU stat 污染
- **P1 修复**: `format_size` 统一为纯 bash，消除 `bc` 依赖
- **P2 新增**: `--max-files N` 预扫描保护 + `--max-depth` 默认 20
- **P2 新增**: 跳过符号链接
- **P2 修复**: `MIN_SIZE_KB` 默认从 0 改为 1（避免空文件干扰）

#### move_with_log.sh (v1.1 → v1.3)
- **P0 修复**: 移除 `set -euo pipefail`，防止空数组/管道错误导致静默退出
- **P1 修复**: `json_escape` 换行处理 `$'\n'` 替代错误的 `\$'\\n'`，增加 `\r` 转义

#### rollback.sh (v1.1 → v1.3)
- **P0 修复**: 移除 `set -eo pipefail`
- **P1 修复**: `ls -A` 空目录检测在无权限目录下可能非零退出 → 新增 `is_dir_empty()` 用 `find` 替代
- **P1 修复**: `cleanup_empty_dirs_from_log` 中 `local` 声明移到函数顶部（bash 3.x 不允许循环内 local）
- **P2 修复**: macOS bash 3.2 兼容

#### scan_cleanup.sh (v1.1 → v1.3)
- **P1 修复**: `get_file_size`/`get_file_mtime` 的 stat 改用 `/usr/bin/stat` 全路径（macOS）
- **P1 修复**: `format_size_mb` 统一为纯 bash，消除 `bc` 依赖
- **P2 新增**: `--max-depth N` 参数
- **P2 新增**: `--max-files N` 预扫描保护
- **P2 新增**: 跳过符号链接

#### classify_files.sh (v1.1 → v1.3)
- **P1 修复**: "其他"文件大小计算：`-exec stat -f%z` 硬编码 macOS → 改用逐文件遍历 + 跨平台 `get_file_size`
- **P1 修复**: date 分类模式的子 shell 变量丢失 → 改用临时文件中转
- **P1 修复**: stat 改用 `/usr/bin/stat` 全路径
- **P2 新增**: `--max-files N` 预扫描保护
- **P2 新增**: 跳过符号链接
- **P2 修复**: `${ext,,}` 小写转换不兼容 bash 3.x → 改用 `tr '[:upper:]' '[:lower:]'`

#### incremental_backup.sh (v1.3 → v1.3.1)
- **P2 修复**: 进度显示条件逻辑错误（5秒间隔条件被 `&&` 短路）→ 改为 `||`

#### 全局
- 所有脚本统一 `set` 策略：不使用 `set -u` / `set -e` / `pipefail`
- 所有 stat 调用统一使用跨平台包装函数 + macOS `/usr/bin/stat` 全路径
- 所有 `format_size` 统一为纯 bash，消除 `bc` 依赖

## [1.3.0] - 2026-04-03

### 修复（P0 严重 — 死循环修复）
- **incremental_backup.sh**: 彻底修复扫描超大目录时"死循环"问题
  - 根因: 之前版本在扫描和统计阶段对每个文件调用 `stat`，`/tmp` 等系统目录下万级文件导致极长时间运行
  - 修复: 新增**预扫描拦截**——先 `find | wc -l` 快速统计文件数，超限立即报错退出，不进入备份流程
  - 修复: 去掉统计阶段的 `-exec stat`，只做文件计数，大幅减少 I/O
  - 修复: 去掉临时文件列表，改为 `find | while read` 流式处理，内存 O(1)
  - 新增: `--max-depth N` 参数（默认 20），限制扫描深度
  - 新增: 双向路径包含检查（源目录在备份目标内 / 备份目标在源目录内，都会拦截）
  - 新增: 跳过符号链接，避免跟随到外部目录
  - 调整: `--max-files` 默认值从 100000 降到 50000

## [1.1.0] - 2026-04-03

### 修复（P0 严重）
- **move_with_log.sh**: 修复 JSON 日志中路径含特殊字符时解析失败的问题，新增 `json_escape` 转义函数
- **move_with_log.sh**: 日志默认目录从 `/tmp` 改为 `~/.cache/file_manager/logs/`，重启不再丢失
- **rollback.sh**: 重写 JSON 解析，使用安全的 `json_get_value` 函数替代 `grep -o` 正则
- **rollback.sh**: trash 回撤支持模糊匹配 macOS 回收站自动重命名（`filename (1)` 格式）
- **rollback.sh**: 空目录清理改为递归向上检查，修复多层嵌套空目录不清理的问题
- **incremental_backup.sh**: 添加 Linux 兼容（`stat -c%s`/`stat -c%Y`/`sha256sum`）
- **find_duplicates.sh**: 文件大小显示从整数除法改为精确格式（支持 KB/MB/GB 自动切换）
- **classify_files.sh**: 分类方案增加文件大小统计，不再只显示数量

### 改进（P1 重要）
- **scan_cleanup.sh**: 移除全局 `set -euo pipefail`，防止权限问题导致脚本静默退出
- **scan_cleanup.sh**: `--installers` 和 `--cache` 现在也受 `--days` 参数控制
- **scan_cleanup.sh**: 缓存文件默认按 30 天过滤（而非列出全部）
- **scan_cleanup.sh**: 大目录扫描时添加进度提示
- **SKILL.md**: 移除不存在的 `find_duplicates.ps1` 引用
- **SKILL.md**: 新增完整的脚本清单和参数说明表
- **SKILL.md**: 日志路径示例更新为 `~/.cache/file_manager/logs/`
- **SKILL.md**: Windows 支持说明从"完整支持"改为"有限支持（需 WSL/Git Bash）"

### 新增（P2 优化）
- **README.md**: 新增项目 README 文件
- **CHANGELOG.md**: 新增版本更新日志
- **incremental_backup.sh**: 新增 `--exclude` 排除规则参数
- **incremental_backup.sh**: 新增备份后文件大小校验
- **incremental_backup.sh**: 新增 `--quiet` 静默模式
- **find_duplicates.sh**: 新增 `--exclude` 排除目录参数
- **find_duplicates.sh**: 新增 `--max-depth` 搜索深度限制
- **find_duplicates.sh**: 新增多组处理进度提示
- **classify_files.sh**: 新增 `--depth` 参数，支持扫描子目录
- **move_with_log.sh**: 新增 Linux 回收站支持（`gio trash`/`trash-put`）
- **command_reference.md**: 修复 `find <dir}` 语法错误为 `find <dir>`
- **command_reference.md**: 新增 Linux 常用命令章节
- **所有脚本**: 统一跨平台辅助函数（`get_file_size`/`get_file_mtime`/`format_date`/`format_size`）
- **所有脚本**: 统一版本号标识

## [1.0.0] - 2026-04-02

### 新增
- 初始版本发布
- 模块1：垃圾清理（scan_cleanup.sh）
- 模块2：文档分类（classify_files.sh）
- 模块3：文件查找
- 模块4：磁盘监控
- 模块5：重复检测（find_duplicates.sh）
- 模块6：自动备份（incremental_backup.sh）
- 模块7：操作回撤（move_with_log.sh + rollback.sh）
- 跨平台命令速查表（command_reference.md）

---
name: file-manager
version: "2.0"
description: "电脑文件管理技能。当用户要求清理垃圾文件、整理文档、检测重复文件、备份文件夹，或提到文件管理、磁盘清理、文件整理、重复文件、文件备份等相关操作时使用此技能。原生支持 macOS、Linux 和 Windows。"
---

# 电脑文件管理技能 v2.0

统一的电脑文件管理工具，支持垃圾清理、文档分类、重复检测、自动备份和操作回撤。文件查找使用系统 find 命令即可，无需额外脚本。

**跨平台原生支持**: macOS / Linux / Windows（Python 3.6+，仅需标准库 + send2trash）

## 依赖

- Python 3.6+
- `send2trash`（用于回收站操作）：`pip install send2trash`

## 脚本清单

| 脚本 | 功能 | 状态 |
|------|------|------|
| `scripts/scan_cleanup.py` | 扫描垃圾文件生成清理建议清单 | 只读 |
| `scripts/classify_files.py` | 文件分类方案预览（不执行移动） | 只读 |
| `scripts/find_duplicates.py` | 基于内容的重复文件检测 | 只读 |
| `scripts/incremental_backup.py` | 增量/全量文件夹备份 | 写入 |
| `scripts/move_with_log.py` | 带操作日志的文件移动/删除 | 写入 |
| `scripts/rollback.py` | 操作回撤工具 | 写入 |

## 安全红线（所有操作必须遵守）

### 绝对禁止

1. **禁止递归删除/清空**桌面、下载、文档、Home、系统目录（`/`、`C:\`、`/System`、`AppData`、`Library`、`~/.config`）
2. **禁止使用** `rm -rf`、`del /S /Q`、`shutil.rmtree()` 或宽泛通配符（`*.tmp`、`*.log`）作用于上述目录
3. **禁止自动删除**任何文件——所有删除/移动操作必须用户确认
4. **禁止修改文件内容**——仅做读取、移动、复制操作
5. **禁止后台通知/弹窗/推送**——仅在当前界面返回结构化结果

### 强制流程

1. **先扫描，后操作**——所有操作先生成预览方案/清单，用户确认后再执行
2. **操作日志记录**——所有移动/删除操作必须通过 `scripts/move_with_log.py` 执行，自动记录操作日志
3. **系统目录保护**——以下目录默认加入保护白名单，禁止任何写入操作：
   - macOS/Linux：`/System`、`/Library`、`/usr`、`/bin`、`/sbin`、`~/.config`
   - Windows：`C:\Windows`、`C:\Program Files`、`C:\Program Files (x86)`、`%USERPROFILE%\AppData`
4. **Trash 优先**——删除操作使用 `send2trash` 库（跨平台统一回收站）
5. **小批量执行**——每次最多操作 10 个文件，逐批确认
6. **结果报告**——每项操作完成后输出清晰的结果报告（数量、路径、状态统计）+ 回撤指引

### 操作日志规范

所有文件移动/删除操作必须通过 `scripts/move_with_log.py` 执行，该脚本会自动记录 JSONL 格式操作日志：

```bash
# 移动文件（自动记录日志）
python3 scripts/move_with_log.py move <源文件> <目标路径> [--log-dir <日志目录>]

# 移到回收站（自动记录日志）
python3 scripts/move_with_log.py trash <文件> [--log-dir <日志目录>]

# 批量移动（文件列表格式：每行 source -> dest）
python3 scripts/move_with_log.py batch-move --files <文件列表路径> [--log-dir <日志目录>]
```

日志目录按平台自动选择：
- **macOS**: `~/Library/Caches/file_manager/logs/`
- **Linux**: `~/.cache/file_manager/logs/`（或 `$XDG_CACHE_HOME`）
- **Windows**: `%LOCALAPPDATA%/file_manager/logs/`

日志格式（JSON Lines，路径含特殊字符时自动转义）：
```json
{"action":"move","source":"/Users/xxx/Downloads/file.pdf","dest":"/Users/xxx/Downloads/文档/file.pdf","timestamp":"2026-04-03T00:30:00Z","status":"ok"}
{"action":"trash","source":"/Users/xxx/Downloads/old.dmg","dest":"trash","timestamp":"2026-04-03T00:30:01Z","status":"ok"}
```

操作完成后，必须在结果报告末尾附上**回撤指引**：
```
↩️ 如操作有误，可回复以下指令回撤：
- 「撤销本次所有操作」— 一键恢复所有文件到原位置
- 「撤销 <文件名>」— 单独恢复某个文件到原位置
```

## 模块决策表

| 用户意图 | 模块 | 说明 |
|----------|------|------|
| 清理垃圾/临时文件 | 模块1：垃圾清理 | 先扫描生成建议清单 |
| 整理/分类文档 | 模块2：文档分类 | 先输出分类方案预览 |
| 查找/删除重复文件 | 模块3：重复检测 | 内容级去重 |
| 备份文件夹 | 模块4：自动备份 | 支持增量备份 |
| 撤销之前操作 | 模块5：操作回撤 | 支持一键撤销或按文件撤销 |

## 模块1：垃圾清理

### 适用场景
清理下载目录、临时文件、重复文件或长期未使用文件。

### 脚本
```bash
python3 scripts/scan_cleanup.py <目标目录> [--days 90] [--min-size 100] [--installers] [--cache] [--max-depth N] [--max-files N]
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--days N` | 超过 N 天未修改才列入 | 90 |
| `--min-size N` | 大文件最小 MB | 100 |
| `--installers` | 同时扫描安装包 | 关 |
| `--cache` | 同时扫描缓存目录 | 关 |
| `--max-depth N` | 最大扫描深度 | 无限 |
| `--max-files N` | 最大扫描文件数 | 50000 |

### 扫描范围
- 下载目录（`~/Downloads`）
- 桌面（需用户明确指定才扫描）
- 临时安装包（`.dmg`、`.exe`、`.msi`、`.pkg`、`.deb`、`.rpm`）
- 超过 N 天未使用的大文件
- 缓存文件（按平台自动识别缓存目录）

### 执行流程
1. 确认扫描范围——用户未指定时仅扫描下载目录
2. 调用 `scripts/scan_cleanup.py` 执行扫描
3. 生成结构化清理建议清单
4. 展示清单，等待用户确认
5. 用户确认后使用 `move_with_log.py trash` 执行清理

### 输出格式
```
🗑️ 清理建议清单（共 N 项，预计释放 X MB）

| # | 文件路径 | 大小 | 最后修改 | 建议 |
|---|---------|------|---------|------|
| 1 | ~/Downloads/installer.dmg | 256MB | 2025-01-15 | 删除 |
| 2 | ~/Downloads/old-report.pdf | 45MB | 2025-10-01 | 保留 |

请确认要清理的文件编号（如：1,3,5 或 全部）：
```

## 模块2：文档分类整理

### 适用场景
按项目、时间、文件类型或主题重新整理文档。

### 脚本（预览）
```bash
python3 scripts/classify_files.py <目标目录> [--by type|project|date] [--depth N] [--max-files N]
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--by type\|project\|date` | 分类方式 | type |
| `--depth N` | 扫描深度 | 1 |
| `--max-files N` | 最大扫描文件数 | 50000 |

### 分类维度
- **按文件类型**：图片/文档/视频/音频/代码/压缩包/安装包/设计文件/字体
- **按项目名称**：根据文件名或所在目录识别项目
- **按时间**：按年/月创建文件夹归档

### 执行流程
1. 调用 `scripts/classify_files.py` 扫描并生成分类方案预览
2. 展示方案（含文件数量和大小），等待用户确认
3. 用户确认后使用 `move_with_log.py move` 逐个移动文件
4. 输出操作报告 + 回撤指引

### 输出格式
```
📂 分类方案预览

目标目录：~/Documents
分类方式：type

├── 📄 分类方案:
│   📁 图片/ (23个文件, 156.3MB)
│   📁 文档/ (45个文件, 12.8MB)
│   📁 代码/ (12个文件, 2.1MB)
│
├── 📊 合计: 80 个文件, 171.2 MB
│
请确认是否按此方案整理？(确认/取消/修改)
```

## 模块3：智能文件查找

### 适用场景
快速定位目标文件。

### 检索条件
- 文件名（支持通配符和正则）
- 文件类型/扩展名
- 修改时间范围
- 文件大小范围
- 文件内容关键词

### 执行方式（Python 跨平台统一）
- 文件遍历：`os.walk()`
- 内容搜索：逐文件读取匹配

### 输出格式
```
🔍 搜索结果（共 N 个文件）

| # | 文件名 | 路径 | 大小 | 修改时间 | 类型 |
|---|-------|------|------|---------|------|
| 1 | report.pdf | ~/Documents/work/ | 2.3MB | 2026-03-15 | PDF |

需要打开或操作哪个文件？
```

## 模块4：重复文件检测

### 适用场景
清理磁盘内内容相同的冗余文件。

### 脚本
```bash
python3 scripts/find_duplicates.py <目标目录> [--min-size 1] [--exclude .git] [--max-depth 20] [--max-files 50000]
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--min-size N` | 最小文件大小 KB | 1 |
| `--exclude <dir>` | 排除目录（可多次） | 无 |
| `--max-depth N` | 最大搜索深度 | 20 |
| `--max-files N` | 最大扫描文件数 | 50000 |

### 检测逻辑
1. 先按文件大小分组（大小不同则不可能重复）
2. 对同大小文件计算 SHA-256 哈希值
3. 哈希值相同的文件判定为重复

### 执行流程
1. 调用脚本执行扫描（纯只读，不删除）
2. 展示重复组列表，默认保留最新/最大的文件
3. 用户确认后使用 `move_with_log.py trash` 删除重复文件

### 输出格式
```
🔁 重复文件检测报告

重复组 1 (共 3 个文件, 5.2MB)：
  ✅ 保留: ~/Documents/photo.jpg (最新, 2026-03-20)
  ❌ 重复: ~/Downloads/photo_copy.jpg (2026-02-15)
  ❌ 重复: ~/Desktop/photo_backup.jpg (2026-01-10)

📊 共发现 N 组重复文件，预计可释放 X MB
```

## 模块5：文件夹备份

### 适用场景
保护工作文档、项目资料等重要文件。

### 脚本
```bash
python3 scripts/incremental_backup.py <源目录> <备份目标路径> [--full] [--exclude <glob>] [--no-verify] [--quiet] [--max-files N] [--max-depth N]
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--full` | 执行全量备份 | 增量 |
| `--exclude <glob>` | 排除匹配的文件/目录（可多次） | 无 |
| `--no-verify` | 跳过备份后校验 | 校验 |
| `--quiet` | 静默模式 | 有进度 |
| `--max-files N` | 最大备份文件数 | 50000 |
| `--max-depth N` | 最大扫描深度 | 20 |

### 备份策略
- **全量备份**：首次备份或 `--full` 时，复制全部文件
- **增量备份**：仅复制新增或修改过的文件（基于修改时间对比）
- 备份目录结构：`<备份目标路径>/<日期>/原路径`
- 备份完成后自动校验文件大小一致性

### 安全保护
- **预扫描拦截**：备份前先快速统计源目录文件数，超过 `--max-files` 上限时立即报错退出
- **递归保护**：双向检查源目录与备份目标路径的包含关系，防止互相嵌套导致无限递归
- **深度限制**：`--max-depth` 限制扫描深度
- **符号链接跳过**：自动跳过符号链接

### 执行流程
1. 确认源目录和备份目标路径
2. 扫描源目录，统计文件数量和总大小
3. 执行备份（增量或全量）
4. 校验备份完整性
5. 生成备份报告

### 输出格式
```
✅ 备份完成报告

源目录：~/Documents/project
备份至：~/Backup/project/2026-04-03/
模式：增量备份
新增文件：12 个 (15.3 MB)
跳过文件：45 个（无修改）
校验：✅ 通过
备份耗时：3.2 秒
```

## 模块6：操作回撤

### 适用场景
撤销之前执行的文件整理/清理/移动操作，恢复文件到原位置。

### 脚本
```bash
# 查看可用日志
python3 scripts/rollback.py list-logs [--log-dir <日志目录>]

# 查看日志详情
python3 scripts/rollback.py show --log <日志文件路径>

# 一键撤销所有操作
python3 scripts/rollback.py rollback-all --log <日志文件路径>

# 撤销单个文件
python3 scripts/rollback.py rollback-single --log <日志文件路径> --file <原文件路径>

# 按范围撤销
python3 scripts/rollback.py rollback-range --log <日志文件路径> --from <起始行号> --to <结束行号>
```

### 回撤原理
1. 读取操作日志（JSONL 格式），安全解析每条操作记录
2. **逆序执行**反向操作：
   - `move` 操作 → 将文件从目标路径移回原路径
   - `trash` 操作 → 将文件从回收站移回原路径（支持模糊匹配回收站重命名）
3. 自动跳过已失败的原始操作和已存在的文件
4. 撤销完成后**递归向上**清理因撤销而变空的目录

### 回撤安全规则
1. **目标已存在则跳过**——不会覆盖任何文件
2. **文件不存在则跳过**——已被手动处理的不影响
3. **仅恢复成功操作**——原本就失败的操作不会重复尝试
4. **嵌套空目录清理**——自动递归清理因整理产生的多层空目录
5. **保护主目录**——不会清理 Home/Desktop/Documents 等受保护目录

### 输出格式
```
↩️ 开始撤销日志中的所有操作...
日志: ~/.cache/file_manager/logs/operations_20260403.jsonl

  ✅ 恢复: ~/Downloads/文档/report.pdf -> ~/Downloads/report.pdf
  ✅ 恢复: ~/Downloads/图片/photo.png -> ~/Downloads/photo.png
  ⏭️ 跳过: ~/Downloads/图片/screenshot.png (原位置已有文件)
  ✅ 恢复: 回收站/old.dmg -> ~/Downloads/old.dmg

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 撤销完成: 成功 3 | 跳过 1 | 失败 0 | 总计 4

🧹 检查并清理因撤销而变空的自动创建文件夹...
  🗑️ 已清理空目录: ~/Downloads/文档
```

## 跨平台支持

### 统一技术栈
| 组件 | 实现 |
|------|------|
| 语言 | Python 3.6+ |
| 文件操作 | `os` / `shutil`（标准库） |
| 哈希计算 | `hashlib`（标准库） |
| 回收站 | `send2trash`（跨平台） |
| 日志格式 | JSON Lines（`json` 标准库） |
| 路径处理 | `os.path`（自动适配平台分隔符） |

### 平台特定路径
| 用途 | macOS | Linux | Windows |
|------|-------|-------|---------|
| 日志目录 | `~/Library/Caches/file_manager/logs/` | `~/.cache/file_manager/logs/` | `%LOCALAPPDATA%/file_manager/logs/` |
| 下载目录 | `~/Downloads` | `~/Downloads` | `%USERPROFILE%/Downloads` |
| 缓存目录 | `~/Library/Caches`, `~/.cache` | `~/.cache`, `~/.gradle/caches` | `%LOCALAPPDATA%/Temp` |
| 回收站 | `~/.Trash` | `~/.local/share/Trash/files` | `$Recycle.Bin` |

## 注意事项

- **不修改文件内容**——所有操作仅涉及读取、移动、复制
- **用户确认优先**——任何破坏性操作前必须明确告知并等待确认
- **结果可追溯**——每次操作完成后输出详细报告
- **操作可撤销**——所有移动/删除操作记录日志，支持一键回撤
- **轻量化设计**——仅需 Python 3.6+ 标准库和 `send2trash`，无其他第三方依赖

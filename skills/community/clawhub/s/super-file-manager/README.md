# File Manager 技能 — 详细说明与使用案例

> 版本：v2.0 | Python 3.6+ | macOS / Linux / Windows

---

## 目录

1. [技能概览](#1-技能概览)
2. [快速上手](#2-快速上手)
3. [模块详解与使用案例](#3-模块详解与使用案例)
   - 3.1 [垃圾文件扫描](#31-垃圾文件扫描)
   - 3.2 [文件分类整理](#32-文件分类整理)
   - 3.3 [重复文件检测](#33-重复文件检测)
   - 3.4 [增量备份](#34-增量备份)
   - 3.5 [文件移动与回收站](#35-文件移动与回收站)
   - 3.6 [操作回撤](#36-操作回撤)
4. [完整工作流案例](#4-完整工作流案例)
5. [安全机制说明](#5-安全机制说明)
6. [跨平台差异](#6-跨平台差异)
7. [常见问题](#7-常见问题)

---

## 1. 技能概览

File Manager 是一个**纯 Python 实现**的跨平台文件管理技能，包含 6 个独立脚本：

| 脚本 | 功能 | 读写 |
|------|------|------|
| `scan_cleanup.py` | 扫描垃圾/大文件，生成清理建议 | 只读 |
| `classify_files.py` | 按类型/日期/项目分类预览 | 只读 |
| `find_duplicates.py` | 基于 SHA-256 的内容级去重 | 只读 |
| `incremental_backup.py` | 增量/全量文件夹备份 | 写入 |
| `move_with_log.py` | 带日志的移动和回收站操作 | 写入 |
| `rollback.py` | 从操作日志恢复文件 | 写入 |

**依赖：** Python 3.6+ 标准库 + `send2trash`（仅 trash 操作需要，会自动安装）

**设计原则：**
- 先扫描预览，后操作执行 — 用户始终掌握控制权
- 所有写入操作带日志，支持一键撤销
- 删除走系统回收站，不直接 `rm`
- 每批最多 10 个文件，出错即停

---

## 2. 快速上手

### 前置条件

```bash
# Python 3.6+（macOS/Linux 通常已预装）
python3 --version

# 安装依赖（仅回收站功能需要）
pip3 install send2trash
```

### 脚本路径

```
~/.workbuddy/skills/file-manager/scripts/
├── scan_cleanup.py
├── classify_files.py
├── find_duplicates.py
├── incremental_backup.py
├── move_with_log.py
└── rollback.py
```

### 一句话用法速查

```bash
# 扫描下载目录中超过 30 天的大文件
python3 scan_cleanup.py ~/Downloads --days 30 --min-size 50

# 按文件类型分类预览
python3 classify_files.py ~/Documents --by type

# 查找重复文件
python3 find_duplicates.py ~/Photos --max-depth 10

# 增量备份
python3 incremental_backup.py ~/Projects ~/Backup/Projects

# 移到回收站
python3 move_with_log.py trash ~/Downloads/old_file.dmg

# 撤销今天所有操作
python3 rollback.py rollback-all --log <日志文件路径>
```

---

## 3. 模块详解与使用案例

---

### 3.1 垃圾文件扫描

**脚本：** `scan_cleanup.py`

**用途：** 扫描指定目录，找出大文件、旧文件、安装包、缓存文件，生成清理建议清单。**只扫描不删除。**

#### 参数

```bash
python3 scan_cleanup.py <目标目录> [选项]
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--days N` | 只列出超过 N 天未修改的文件 | 90 |
| `--min-size N` | 只列出大于 N MB 的文件 | 100 |
| `--installers` | 额外扫描安装包（.dmg/.exe/.msi/.pkg/.deb/.rpm） | 关 |
| `--cache` | 额外扫描系统缓存目录 | 关 |
| `--max-depth N` | 最大扫描目录深度 | 无限 |
| `--max-files N` | 最大扫描文件数（防止卡死） | 50000 |

#### 使用案例

**案例 1：扫描下载目录中的大旧文件**

> 用户说：「帮我看看下载目录有没有可以清理的大文件」

```bash
python3 scan_cleanup.py ~/Downloads --days 30 --min-size 50
```

输出示例：
```
🗑️ 垃圾文件扫描报告
扫描目录: ~/Downloads
筛选条件: 超过 30 天 AND 大于 50MB

| # | 文件路径 | 大小 | 最后修改 | 建议操作 |
|---|---------|------|---------|---------|
| 1 | Chrome.dmg | 256 MB | 2026-01-15 | 删除（安装包） |
| 2 | node-v18.pkg | 45 MB | 2026-01-20 | 删除（安装包） |
| 3 | archive.zip | 120 MB | 2026-02-10 | 待确认 |

共发现 3 个文件，预计可释放 421 MB
```

然后等用户确认要删哪些，再用 `move_with_log.py trash` 逐个执行。

---

**案例 2：专门扫描安装包**

> 用户说：「清理一下下载目录里的安装包」

```bash
python3 scan_cleanup.py ~/Downloads --installers --min-size 1
```

会列出所有 `.dmg`、`.exe`、`.msi`、`.pkg`、`.deb`、`.rpm` 文件。

---

**案例 3：扫描项目目录中的大文件**

> 用户说：「我的项目目录里有没有特别大的文件？」

```bash
python3 scan_cleanup.py ~/Projects/my-app --min-size 10 --max-depth 5
```

`--max-depth 5` 防止递归太深，`--min-size 10` 只关注 10MB 以上的大文件。

---

### 3.2 文件分类整理

**脚本：** `classify_files.py`

**用途：** 扫描目录，按文件类型/日期/项目分组，生成分类方案预览。**只预览不移动。**

#### 参数

```bash
python3 classify_files.py <目标目录> [选项]
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--by type|project|date` | 分类维度 | type |
| `--depth N` | 扫描深度 | 1 |
| `--max-files N` | 最大文件数 | 50000 |

#### 支持的文件类型

| 分类 | 扩展名 |
|------|--------|
| 图片 | .jpg .jpeg .png .gif .bmp .webp .svg .tiff .ico .heic .raw .psd .ai |
| 视频 | .mp4 .avi .mkv .mov .wmv .flv .webm .m4v .mpg .mpeg .3gp |
| 音频 | .mp3 .wav .flac .aac .ogg .wma .m4a .aiff .opus |
| 文档 | .pdf .doc .docx .xls .xlsx .ppt .pptx .txt .md .rtf .csv .odt .ods |
| 代码 | .py .js .ts .html .css .java .c .cpp .go .rs .rb .php .sh .bat |
| 压缩包 | .zip .rar .7z .tar .gz .bz2 .xz .tar.gz .tgz |
| 安装包 | .dmg .exe .msi .pkg .deb .rpm .appimage |
| 设计文件 | .psd .ai .sketch .fig .xd .indd |
| 字体 | .ttf .otf .woff .woff2 .eot |

#### 使用案例

**案例 1：按类型分类下载目录**

> 用户说：「帮我整理一下下载目录，按文件类型分」

```bash
python3 classify_files.py ~/Downloads --by type --depth 3
```

输出示例：
```
📂 文件分类方案预览
目标目录: ~/Downloads
分类方式: 按文件类型

├── 📁 图片/ (23 个文件, 156.3 MB)
│   ├── screenshot_001.png (2.1 MB)
│   ├── photo_2026.jpg (45.0 MB)
│   └── ... (21 more)
├── 📁 文档/ (12 个文件, 8.5 MB)
│   ├── report.pdf (2.3 MB)
│   ├── data.xlsx (1.2 MB)
│   └── ... (10 more)
├── 📁 视频/ (5 个文件, 320.0 MB)
│   ├── tutorial.mp4 (180.0 MB)
│   └── ... (4 more)
├── 📁 压缩包/ (8 个文件, 95.2 MB)
├── 📁 安装包/ (6 个文件, 421.0 MB)
└── 📁 其他/ (15 个文件, 3.7 MB)

📊 合计: 69 个文件, 1004.7 MB
```

用户确认后，用 `move_with_log.py move` 逐个执行移动。

---

**案例 2：按日期归档旧文件**

> 用户说：「把桌面上的文件按月份归档」

```bash
python3 classify_files.py ~/Desktop --by date --depth 2
```

输出示例：
```
📂 文件分类方案预览
分类方式: 按日期（年-月）

├── 📁 2026-01/ (8 个文件, 23.4 MB)
├── 📁 2026-02/ (12 个文件, 56.7 MB)
├── 📁 2026-03/ (5 个文件, 12.1 MB)
└── 📁 未分类/ (3 个文件, 1.0 MB)
```

---

**案例 3：按项目分类**

> 用户说：「帮我看看工作目录的文件，按项目分一下」

```bash
python3 classify_files.py ~/Work --by project --depth 3
```

脚本会根据文件名和所在目录自动识别项目归属。

---

### 3.3 重复文件检测

**脚本：** `find_duplicates.py`

**用途：** 基于文件内容（SHA-256 哈希）检测重复文件。**只检测不删除。**

#### 参数

```bash
python3 find_duplicates.py <目标目录> [选项]
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--min-size N` | 只检测大于 N KB 的文件 | 1 |
| `--exclude <dir>` | 排除目录（可多次使用） | 无 |
| `--max-depth N` | 最大搜索深度 | 20 |
| `--max-files N` | 最大扫描文件数 | 50000 |

#### 检测逻辑

```
文件列表 → 按大小分组 → 同大小文件计算 SHA-256 → 哈希相同 = 重复
```

先按大小筛选（大小不同的文件不可能重复），再对同大小文件做哈希，效率高且准确。

#### 使用案例

**案例 1：扫描照片目录找重复**

> 用户说：「我的相册里有很多重复的照片，帮我找出来」

```bash
python3 find_duplicates.py ~/Photos --max-depth 10
```

输出示例：
```
🔁 重复文件检测报告
扫描目录: ~/Photos
已扫描: 2,456 个文件 (4.8 GB)

重复组 1 (SHA256: a1b2c3...) — 共 3 个文件, 8.2 MB:
  ✅ 保留: ~/Photos/2026/vacation.jpg (最新, 2026-03-20, 4.1 MB)
  ❌ 重复: ~/Photos/backup/vacation_copy.jpg (2026-02-15, 4.1 MB)
  ❌ 重复: ~/Downloads/vacation.jpg (2026-01-10, 4.1 MB)

重复组 2 (SHA256: d4e5f6...) — 共 2 个文件, 2.1 MB:
  ✅ 保留: ~/Photos/2026/portrait.png (最新, 2026-03-18, 2.1 MB)
  ❌ 重复: ~/Photos/2025/portrait_old.png (2025-12-01, 2.1 MB)

📊 共发现 2 组重复文件，预计可释放 10.3 MB
建议保留每个重复组中最新修改的文件
```

用户确认后，对标记为 ❌ 的文件执行 `move_with_log.py trash`。

---

**案例 2：排除 Git 目录扫描项目**

> 用户说：「查找项目里的重复文件，但不要扫描 .git 目录」

```bash
python3 find_duplicates.py ~/Projects/my-app --exclude .git --exclude node_modules --max-depth 15
```

---

**案例 3：只检测大文件的重复**

> 用户说：「找一下大文件的重复，小的不用管」

```bash
python3 find_duplicates.py ~/ --min-size 10240 --max-depth 3
```

`--min-size 10240` 表示只检测 10MB 以上的文件（单位是 KB）。

---

### 3.4 增量备份

**脚本：** `incremental_backup.py`

**用途：** 将源目录备份到目标路径。首次全量复制，之后只备份新增或修改过的文件。

#### 参数

```bash
python3 incremental_backup.py <源目录> <备份目标路径> [选项]
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--full` | 强制全量备份（忽略增量记录） | 增量模式 |
| `--exclude <glob>` | 排除匹配的文件/目录（可多次） | 无 |
| `--no-verify` | 跳过备份后校验 | 默认校验 |
| `--quiet` | 静默模式，不输出进度 | 有进度 |
| `--max-files N` | 最大文件数限制 | 50000 |
| `--max-depth N` | 最大扫描深度 | 20 |

#### 备份策略

- **全量备份**：首次运行或 `--full` 时，复制所有文件
- **增量备份**：对比源文件和已有备份的修改时间，只复制有变化的文件
- **备份目录结构**：`<目标路径>/<日期>/<相对路径>`
- **校验**：备份完成后自动校验文件大小一致性

#### 安全保护

- **预扫描拦截**：先统计文件数，超过上限立即退出
- **防递归嵌套**：检测源目录和目标目录是否互相包含
- **符号链接跳过**：自动跳过，避免循环引用
- **深度限制**：`--max-depth` 防止无限递归

#### 使用案例

**案例 1：首次备份工作项目**

> 用户说：「帮我把项目目录备份到移动硬盘」

```bash
python3 incremental_backup.py ~/Projects/my-app /Volumes/External/Backup
```

输出示例：
```
📁 开始全量备份
源目录: ~/Projects/my-app (128 个文件, 45.6 MB)
备份至: /Volumes/External/Backup/my-app/2026-04-03/

备份中...
  ████████████████████████████████ 100% (128/128)

✅ 全量备份完成
  新增: 128 个文件 (45.6 MB)
  耗时: 2.3 秒
  校验: ✅ 通过
```

---

**案例 2：增量备份（只备份变化）**

> 用户说：「项目有更新，再备份一次」

```bash
python3 incremental_backup.py ~/Projects/my-app /Volumes/External/Backup
```

输出示例：
```
📁 增量备份
源目录: ~/Projects/my-app
上次备份: 2026-04-03

扫描变化...
  新增文件: 3 个 (1.2 MB)
  修改文件: 5 个 (3.8 MB)
  未变化: 120 个（跳过）

备份中...
  ████████████████████████████████ 100% (8/8)

✅ 增量备份完成
  新增/修改: 8 个文件 (5.0 MB)
  跳过: 120 个
  耗时: 0.8 秒
  校验: ✅ 通过
```

---

**案例 3：排除特定目录备份**

> 用户说：「备份项目，但不要 node_modules 和 .git」

```bash
python3 incremental_backup.py ~/Projects/my-app /Volumes/External/Backup \
  --exclude "node_modules" --exclude ".git" --exclude "__pycache__"
```

---

**案例 4：备份文档目录（定期执行）**

> 用户说：「每天自动备份我的文档」

可以配合自动化定时任务，每天运行：

```bash
python3 incremental_backup.py ~/Documents /Volumes/NAS/DocumentsBackup
```

每天只备份当天修改过的文件，效率很高。

---

### 3.5 文件移动与回收站

**脚本：** `move_with_log.py`

**用途：** 移动文件或移到回收站，所有操作自动记录到 JSONL 日志文件，便于后续撤销。

#### 子命令

```bash
# 移动单个文件
python3 move_with_log.py move <源路径> <目标路径>

# 移到回收站
python3 move_with_log.py trash <文件路径>

# 批量移动（从文件列表）
python3 move_with_log.py batch-move --files <列表文件路径>
```

#### 通用选项

| 参数 | 说明 |
|------|------|
| `--log-dir <目录>` | 自定义日志目录（默认按平台自动选择） |

#### 日志记录

每次操作自动写入 JSONL 日志：

```json
{"action":"move","source":"/Users/me/Downloads/report.pdf","dest":"/Users/me/Downloads/文档/report.pdf","timestamp":"2026-04-03T02:30:00Z","status":"ok"}
{"action":"trash","source":"/Users/me/Downloads/old.dmg","dest":"trash","timestamp":"2026-04-03T02:30:01Z","status":"ok"}
```

日志路径（按平台）：
- macOS: `~/Library/Caches/file_manager/logs/operations_YYYY-MM-DD.jsonl`
- Linux: `~/.cache/file_manager/logs/operations_YYYY-MM-DD.jsonl`
- Windows: `%LOCALAPPDATA%/file_manager/logs/operations_YYYY-MM-DD.jsonl`

#### 使用案例

**案例 1：移动文件到分类目录**

> 用户说：「把这个文件移到文档目录」（确认后执行）

```bash
python3 move_with_log.py move ~/Downloads/report.pdf ~/Downloads/文档/report.pdf
```

输出：
```
✅ 已移动: ~/Downloads/report.pdf → ~/Downloads/文档/report.pdf
📝 操作已记录到日志
```

---

**案例 2：文件移到回收站**

> 用户说：「删掉这个旧安装包」

```bash
python3 move_with_log.py trash ~/Downloads/Chrome.dmg
```

输出：
```
✅ 已移到回收站: ~/Downloads/Chrome.dmg
📝 操作已记录到日志
```

文件进了系统回收站，随时可以从 Finder/资源管理器恢复。更重要的是，操作被记录了日志，可以通过 rollback 脚本一键恢复。

---

**案例 3：批量移动文件**

准备一个文件列表 `move_list.txt`，每行格式 `源路径 -> 目标路径`：

```
/Users/me/Downloads/report.pdf -> /Users/me/Documents/report.pdf
/Users/me/Downloads/photo.jpg -> /Users/me/Pictures/photo.jpg
/Users/me/Downloads/data.xlsx -> /Users/me/Work/data.xlsx
```

然后执行：

```bash
python3 move_with_log.py batch-move --files move_list.txt
```

---

### 3.6 操作回撤

**脚本：** `rollback.py`

**用途：** 从操作日志中读取之前执行的 move/trash 操作，逆序执行恢复。

#### 子命令

```bash
# 列出所有可用日志
python3 rollback.py list-logs

# 查看某条日志的详情
python3 rollback.py show --log <日志文件路径>

# 撤销日志中的所有操作
python3 rollback.py rollback-all --log <日志文件路径>

# 撤销单个文件
python3 rollback.py rollback-single --log <日志文件路径> --file <原文件路径>

# 按范围撤销（第 N 到第 M 条）
python3 rollback.py rollback-range --log <日志文件路径> --from <起始行号> --to <结束行号>
```

#### 回撤原理

1. 读取 JSONL 日志
2. **逆序执行**反向操作：
   - `move` → 把文件从目标路径移回原路径
   - `trash` → 把文件从回收站移回原路径（macOS 上支持模糊匹配回收站重命名）
3. 自动跳过原位置已有文件的记录（不会覆盖）
4. 清理因整理而产生的空目录

#### 安全规则

- 目标位置已有文件 → 跳过，不覆盖
- 原始操作失败的 → 跳过，不重试
- 文件在回收站找不到 → 跳过，报告警告
- 回收站无权限 → 跳过，提示授权

#### 使用案例

**案例 1：撤销今天所有文件整理操作**

> 用户说：「刚刚的整理搞乱了，全部撤销」

```bash
# 先看今天有哪些操作
python3 rollback.py list-logs

# 查看详情
python3 rollback.py show --log ~/Library/Caches/file_manager/logs/operations_2026-04-03.jsonl

# 确认后一键撤销
python3 rollback.py rollback-all --log ~/Library/Caches/file_manager/logs/operations_2026-04-03.jsonl
```

输出示例：
```
↩️ 开始撤销日志中的所有操作...
日志: operations_2026-04-03.jsonl (共 5 条记录)

  ✅ 恢复: ~/Downloads/文档/report.pdf → ~/Downloads/report.pdf
  ✅ 恢复: ~/Downloads/图片/photo.png → ~/Downloads/photo.png
  ⏭️ 跳过: ~/Downloads/old.dmg (原位置已有文件)
  ✅ 恢复: 回收站/archive.zip → ~/Downloads/archive.zip
  ⏭️ 跳过: ~/Downloads/temp.txt (原始操作失败)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 撤销完成: 成功 3 | 跳过 2 | 失败 0 | 总计 5

🧹 检查并清理因撤销而变空的目录...
  🗑️ 已清理空目录: ~/Downloads/文档
  🗑️ 已清理空目录: ~/Downloads/图片
```

---

**案例 2：只撤销某个文件的移动**

> 用户说：「其他的不用管，把 report.pdf 恢复原位就行」

```bash
python3 rollback.py rollback-single \
  --log ~/Library/Caches/file_manager/logs/operations_2026-04-03.jsonl \
  --file ~/Downloads/report.pdf
```

---

**案例 3：按范围撤销**

> 用户说：「撤销第 3 到第 5 条操作」

```bash
python3 rollback.py rollback-range \
  --log ~/Library/Caches/file_manager/logs/operations_2026-04-03.jsonl \
  --from 3 --to 5
```

---

## 4. 完整工作流案例

### 案例一：清理下载目录（完整流程）

> 用户说：「帮我清理一下下载目录」

**Step 1 — 扫描**

```bash
python3 scan_cleanup.py ~/Downloads --days 30 --installers
```

**Step 2 — 预览结果，用户确认要删除哪些文件**

**Step 3 — 逐个移到回收站**

```bash
python3 move_with_log.py trash ~/Downloads/Chrome.dmg
python3 move_with_log.py trash ~/Downloads/node-v18.pkg
python3 move_with_log.py trash ~/Downloads/archive_old.zip
```

**Step 4 — 输出报告 + 回撤指引**

```
✅ 清理完成
  移到回收站: 3 个文件 (421 MB)
  
↩️ 如操作有误，可回复「撤销本次所有操作」恢复所有文件
```

---

### 案例二：整理散乱的桌面文件

> 用户说：「桌面太乱了，帮我整理一下」

**Step 1 — 按类型分类预览**

```bash
python3 classify_files.py ~/Desktop --by type --depth 2
```

**Step 2 — 展示方案，用户确认**

**Step 3 — 创建目标目录并移动文件**

```bash
# 先创建分类目录
mkdir -p ~/Desktop/文档 ~/Desktop/图片 ~/Desktop/安装包

# 按日志逐个移动
python3 move_with_log.py move ~/Desktop/report.pdf ~/Desktop/文档/report.pdf
python3 move_with_log.py move ~/Desktop/screenshot.png ~/Desktop/图片/screenshot.png
python3 move_with_log.py move ~/Desktop/app.dmg ~/Desktop/安装包/app.dmg
```

**Step 4 — 输出报告**

```
✅ 整理完成
  移动: 15 个文件
    文档/: 5 个 (8.2 MB)
    图片/: 7 个 (23.5 MB)
    安装包/: 3 个 (156.0 MB)
  
↩️ 回复「撤销本次所有操作」可恢复
```

---

### 案例三：照片去重 + 清理

> 用户说：「我的照片目录有很多重复的，帮我清理」

**Step 1 — 检测重复**

```bash
python3 find_duplicates.py ~/Photos --max-depth 10
```

**Step 2 — 展示重复组，用户确认删除哪些**

**Step 3 — 移到回收站**

```bash
python3 move_with_log.py trash ~/Photos/backup/vacation_copy.jpg
python3 move_with_log.py trash ~/Photos/2025/portrait_old.png
```

**Step 4 — 报告**

```
✅ 去重完成
  移到回收站: 2 个重复文件 (10.3 MB)
  
↩️ 回复「撤销」可恢复
```

---

### 案例四：定期备份工作目录

> 用户说：「每周备份一下我的项目」

**首次备份（全量）：**

```bash
python3 incremental_backup.py ~/Projects /Volumes/NAS/Backup/Projects
```

**后续备份（增量，只备份变化）：**

```bash
python3 incremental_backup.py ~/Projects /Volumes/NAS/Backup/Projects
```

第二次运行时会自动检测哪些文件有变化，只复制新增和修改的文件。

---

## 5. 安全机制说明

### 操作前：预览保护

所有只读脚本（scan_cleanup、classify_files、find_duplicates）都有安全限制：

| 保护机制 | 说明 |
|---------|------|
| `--max-files` | 扫描文件数上限，默认 50000，防止在大目录卡死 |
| `--max-depth` | 目录深度限制，防止无限递归 |
| 纯只读 | 这些脚本不会修改、移动、删除任何文件 |

### 操作中：日志记录

所有写入操作通过 `move_with_log.py` 执行：

- 自动记录到 JSONL 日志（含时间戳、源路径、目标路径、操作状态）
- 日志按日期分文件，方便查找
- 支持自定义日志目录

### 操作后：可回撤

- `rollback.py` 从日志读取操作记录
- 逆序执行，恢复文件到原位
- 不会覆盖已有文件
- 自动清理空目录

### 系统目录保护

以下目录**禁止任何写入操作**：

| 平台 | 受保护目录 |
|------|-----------|
| macOS/Linux | `/System`、`/Library`、`/usr`、`/bin`、`/sbin`、`~/.config` |
| Windows | `C:\Windows`、`C:\Program Files`、`%USERPROFILE%\AppData` |

---

## 6. 跨平台差异

| 组件 | macOS | Linux | Windows |
|------|-------|-------|---------|
| Python 路径 | `/usr/bin/python3` | `/usr/bin/python3` | `python` |
| 日志目录 | `~/Library/Caches/file_manager/logs/` | `~/.cache/file_manager/logs/` | `%LOCALAPPDATA%/file_manager/logs/` |
| 回收站 | `~/.Trash/` | `~/.local/share/Trash/files/` | `$Recycle.Bin\` |
| 回收站操作 | `send2trash` (osascript) | `send2trash` (gio trash) | `send2trash` (Shell API) |
| 路径分隔符 | `/` | `/` | `\`（os.path 自动处理） |

所有路径处理使用 `os.path` 标准库，自动适配平台分隔符，无需手动处理。

---

## 7. 常见问题

### Q: 删除的文件还能恢复吗？

**能。** 所有删除操作走系统回收站（`send2trash`），文件可以从 Finder/资源管理器的回收站直接恢复。此外，操作日志支持通过 `rollback.py` 一键恢复。

### Q: 回收站恢复时提示"无权限"怎么办？

macOS 终端默认没有"完全磁盘访问"权限，无法读取 `~/.Trash/` 目录。

解决：**系统设置 → 隐私与安全性 → 完全磁盘访问** → 添加你的终端应用（Terminal / iTerm / Warp 等）。

### Q: 增量备份的第一次和之后有什么区别？

- **第一次**：全量备份，复制所有文件
- **之后**：增量备份，只复制新增或修改过的文件（基于修改时间对比），跳过未变化的文件

### Q: 扫描很大的目录会不会卡死？

不会。所有只读脚本都有 `--max-files`（默认 50000）和 `--max-depth` 保护。超过限制会立即停止并报告。

### Q: 可以直接用 `rm` 删除文件吗？

**不要。** 这个技能的设计原则是删除走回收站。直接 `rm` 的文件无法通过 `rollback.py` 恢复，也无法从系统回收站找回。

### Q: 日志文件会越来越大吗？

不会。日志按日期分文件（`operations_2026-04-03.jsonl`），每天一个文件。日常使用中，每天的操作日志通常只有几 KB。

### Q: Windows 上能用吗？

能。代码全部使用 Python 标准库 + `send2trash`，跨平台兼容。唯一需要注意的是 `send2trash` 需要通过 `pip install send2trash` 安装。

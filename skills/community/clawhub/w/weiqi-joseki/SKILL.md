---
name: 围棋定式数据库
description: weiqi-joseki v2.1.1 围棋定式数据库 - 基于KataGo棋谱构建。重构版采用多级时序连通性过滤，性能大幅提升。模块化设计，数据完全本地存储。
tags: ["围棋", "weiqi", "go", "定式", "joseki", "SGF", "KataGo"]
---

# 围棋定式数据库 v2.1.1

基于KataGo Archive棋谱构建的围棋定式数据库。采用模块化架构设计，数据完全本地存储，支持从大量棋谱中自动提取高频定式。

**核心理念**: 从实战中学习的定式库，收录AI对局中出现频率最高的定式变化。

**v2.1.1 重大更新**: 
1. **🚀 自动增量构建** - 支持日更定式库，增量下载、提取、统计、入库
2. **⚡ 性能重构** - 引入时序连通性分析和多级回退策略，构建速度提升40%
3. **🎯 方向归一化** - 定式统一标准化存储，简化匹配逻辑

## v2.1.1 重构亮点

### 🚀 性能优化

| 指标 | v1.x | v2.1.1 | 提升 |
|-----|------|--------|-----|
| 定式提取速度 | 基准 | **+40%** | 算法简化，减少重复计算 |
| 内存占用 | 基准 | **-30%** | 移除冗余数据结构 |
| 构建10万定式 | ~30分钟 | **~20分钟** | 流程优化，I/O减少 |

**优化细节：**
- **移除局面连通块分析**: 直接时序连通性分析，减少一轮连通块计算
- **精简数据模型**: 去除name/category/tags等冗余字段，只保留核心数据
- **统一入库流程**: 先CMS统计再统一入库，避免频繁数据库操作
- **多级回退策略**: 13路→11路→9路智能选择，避免过度提取

### 🔧 技术改进

**1. 时序连通性分析 (Temporal Connectivity)**
```
传统: 只看最终局面谁连通
新版: 看行棋过程中是否连续战斗

优势: 剔除真正脱先的棋，保留连续定式战斗
```

**2. 凸包回退检测 (Convex Hull Fallback)**
```
算法: 被剔除着法是否落入核心区域的凸包内
用途: 判断是否误判脱先，决定是否回退到更严格范围
```

**3. 多级提取策略**
```
13路提取 → 时序分析 → 凸包检测
    ↓ 有剔除在凸包内
11路提取 → 时序分析 → 凸包检测
    ↓ 有剔除在凸包内
9路提取 (最终)
```

### 📉 接口精简

**v1.x 接口（已移除）：**
- ❌ `import` - 导入外部定式（功能合并到katago）
- ❌ `match` - 复杂匹配接口（被discover替代）
- ❌ `identify` - 识别接口（被discover替代）
- ❌ `compare` - 对比接口（使用频率低）
- ❌ `search` - 搜索接口（被list --sort替代）

**v2.1.1 保留接口（7个核心命令）：**
- ✅ `init` - 初始化数据库
- ✅ `katago` - 从KataGo构建定式库
- ✅ `list` - 列示定式（支持排序）
- ✅ `stats` - 统计信息
- ✅ `extract` - 从SGF提取四角
- ✅ `discover` - 发现棋谱中的定式
- ✅ `export` - 导出定式

**Python API 简化：**
```python
# v1.x - 复杂
from weiqi_joseki import JosekiMatcher, JosekiImporter, JosekiExporter
matcher = JosekiMatcher(db)
results = matcher.match(sgf, direction="both", threshold=0.8)

# v2.1.1 - 简洁
from weiqi_joseki.src.discover import discover_joseki
results = discover_joseki(sgf, joseki_list)
```

## 项目结构

```
weiqi-joseki/
├── SKILL.md                 # 技能文档
└── src/                     # 重构后的模块化代码
    ├── auto/                # 自动构建状态管理（v2.1.0新增）
    │   ├── state.py         # AutoState配置/进度/统计
    │   └── __init__.py
    ├── builder/             # 定式库构建器
    │   ├── katago_builder.py
    │   └── __init__.py
    ├── cli/                 # 命令行接口
    │   ├── commands.py
    │   ├── __main__.py      # 支持python -m运行
    │   └── __init__.py
    ├── core/                # 核心模块（坐标系统）
    │   ├── coords.py
    │   └── __init__.py
    ├── discover/            # 定式发现
    │   ├── discoverer.py
    │   └── __init__.py
    ├── extraction/          # 棋谱提取
    │   ├── extractor.py
    │   ├── component_detector.py
    │   ├── katago_downloader.py
    │   ├── sgf_parser.py
    │   └── __init__.py
    ├── matching/            # Trie匹配
    │   ├── trie.py
    │   └── __init__.py
    ├── storage/             # 存储
    │   ├── json_storage.py
    │   └── __init__.py
    ├── utils/               # 工具
    │   ├── cms.py
    │   └── __init__.py
    └── __init__.py
```

## 数据存储

- **数据库路径**: `~/.weiqi-joseki/database.json`
- **KataGo缓存**: `~/.weiqi-joseki/katago-cache/`
- **自动构建数据**: `~/.weiqi-joseki/auto/`（v2.1.0新增）
  - `state.json` - 配置、进度、统计
  - `cms.pkl` - CMS统计数据
  - `temp/` - 每日提取的着法串（YYYY-MM-DD.txt.gz）
- 自动创建目录和文件

### 定式数据格式

```json
{
  "joseki_list": [
    {
      "id": "kj_00001",
      "source": "katago",
      "moves": ["pd", "qf", "nc", "rd"],
      "frequency": 5234,
      "direction": "ruld",
      "created_at": "2026-04-21T10:00:00"
    }
  ]
}
```

**字段说明：**
- `id`: 定式唯一标识（格式: kj_NNNNN）
- `source`: 数据来源（katago）
- `moves`: 着法序列（右上角视角，ruld方向）
- `frequency`: 出现频率（统计次数）
- `direction`: 提取时的方向（ruld/rudl）
- `created_at`: 创建时间

**注意**: 数据模型已简化，不再包含name、category、tags等字段，专注于基础定式数据。

## CLI 命令

### 全局选项

```bash
python3 -m src.cli.commands [全局选项] [命令] [选项]
```

**全局选项：**
- `--db <路径>` - 指定数据库路径（默认: ~/.weiqi-joseki/database.json）

### 初始化数据库
```bash
python3 -m src.cli.commands init
```

### 从KataGo构建定式库 ⭐

从 [KataGo Archive](https://katagoarchive.org/kata1/ratinggames/index.html) 下载棋谱并构建定式库。

#### 模式一：自动增量构建（推荐）

自动检测新增棋谱，增量下载、提取、统计、入库。适合日更定式库。

```bash
# 首次运行：全量下载并构建
python3 -m src.cli.commands katago --mode auto

# 日常更新：只下载新增日期
python3 -m src.cli.commands katago --mode auto

# 强制重建
python3 -m src.cli.commands katago --mode auto --force-rebuild
```

**自动模式特点：**
- ✅ **增量下载** - 只下载服务器新增的日期
- ✅ **增量提取** - 只处理新下载的棋谱
- ✅ **增量CMS** - 基于历史统计累加新数据
- ✅ **智能重建** - 达到阈值后自动全量重建定式库
- ✅ **状态持久化** - 进度自动保存，支持断点续跑

**数据存储：**
```
~/.weiqi-joseki/
├── auto/
│   ├── state.json          # 配置和进度
│   ├── cms.pkl             # CMS统计数据
│   └── temp/               # 每日提取的着法串
│       └── YYYY-MM-DD.txt.gz
└── database.json           # 定式库
```

#### 模式二：自定义构建

手动指定日期范围，适合一次性构建或补历史数据。

```bash
# 构建指定日期范围的定式库
python3 -m src.cli.commands katago \
  --start-date 2026-01-01 \
  --end-date 2026-04-21
```

**完整参数：**
```bash
python3 -m src.cli.commands katago \
  --mode custom \                # 模式：custom或auto（默认custom）
  --start-date 2026-01-01 \      # 起始日期（custom模式必需）
  --end-date 2026-04-21 \        # 结束日期（custom模式必需）
  --min-freq 10 \                # 最小出现频率（默认10）
  --top-k 100000 \               # 入库数量上限（默认10万）
  --first-n 80 \                 # 每谱提取前N手（默认80）
  --distance-threshold 4 \       # 连通块距离阈值（默认4）
  --min-moves 4 \                # 最少手数（默认4）
  --force-rebuild                # 强制重建（仅auto模式有效）
```

**构建流程：**
1. **下载/检查缓存** - 下载或复用本地缓存的tar文件
2. **Phase 1** - 统一扫描所有棋谱，CMS统计频率
3. **Phase 2-3** - 逆向遍历+单链检测+去重，选取top-k定式
4. **Phase 4** - 统一入库到数据库

**输出示例：**
```
📅 日期范围: 2026-01-01 至 2026-04-21（共110天）
💾 缓存目录: ~/.weiqi-joseki/katago-cache
🗄️  数据库: ~/.weiqi-joseki/database.json

📥 开始下载/检查缓存...
✅ 文件准备完成: 105/110 个

⏳ 开始构建定式库（前80手）...
   参数: min-freq=10, top-k=100000

📊 Phase 1: CMS统计前缀频率...
   处理: 2026-01-01rating.tar.bz2...
      累计: 1211谱, 9104定式串, 288838前缀
   ...
✅ Phase 1完成: 115000谱, 850000定式串, 25000000前缀

🔄 Phase 2-3: 逆向遍历+单链检测+去重...
✅ 构建完成: 52347 条定式

🔄 Phase 4: 保存到数据库...
已保存 52347 条定式到 ~/.weiqi-joseki/database.json

==================================================
🎉 全部完成！共 52347 条定式
==================================================
```

### 列出定式
```bash
# 列出所有定式
python3 -m src.cli.commands list

# 按频率排序
python3 -m src.cli.commands list --sort freq

# 按手数排序
python3 -m src.cli.commands list --sort length

# 限制数量
python3 -m src.cli.commands list --limit 20
```

**输出示例：**
```
共 52347 条定式

ID           手数   频率     着法串
------------------------------------------------------------
kj_00001        4   5234   pd qf nc rd
kj_00002        4   5122   pd qc pc qd
kj_00003        5   2669   pd qc pc qd pe
...
```

### 统计信息
```bash
python3 -m src.cli.commands stats
```

**输出示例：**
```
==================================================
定式库统计
==================================================
总定式数:     52347
总出现次数:   1523456

【频率统计】
  最高:       5234
  最低:       10
  平均:       29.1
  中位数:     15
  Top 10%平均: 156.3

【着法长度统计】
  最长:       31 手
  最短:       4 手
  平均:       6.8 手
  中位数:     6 手

【出现最多定式】
  ID:         kj_00001
  频率:       5234
  着法:       pd qf nc rd
```

### 从SGF提取四角着法
```bash
# 提取四角着法
python3 -m src.cli.commands extract game.sgf

# 详细输出
python3 -m src.cli.commands extract game.sgf --verbose

# 保存MULTIGOGM格式
python3 -m src.cli.commands extract game.sgf --output corners.sgf
```

**输出示例：**
```
提取结果（前80手，距离阈值4）:

【左上】12子
  dd fc df ch cj cm dp dq fq

【右上】15子
  pd qf nc rd qc qd pc pe qb

【左下】8子
  dp cn fq jp jq

【右下】10子
  pp qn on np mq
```

### 从SGF发现定式
```bash
# 发现棋谱中的定式
python3 -m src.cli.commands discover game.sgf

# 详细输出
python3 -m src.cli.commands discover game.sgf --verbose
```

**工作原理：**
1. 提取四角着法
2. 转换到右上角视角
3. 生成ruld和rudl两个方向
4. Trie树匹配最长前缀
5. 返回匹配结果和来源角

**输出示例：**
```
发现定式:

【右上】
  - kj_00001: 匹配4/4手 (ruld)
    定式: pd qf nc rd
  - kj_00015: 匹配8/11手 (rudl)
    定式: pd qc pc qd pe pf...

【左上】
  - kj_00234: 匹配6/6手 (ruld)
    定式: dd fc df ch cj cm
```

### 导出定式
```bash
# 导出为JSON
python3 -m src.cli.commands export --output joseki.json

# 导出为SGF
python3 -m src.cli.commands export --format sgf --output joseki.sgf

# 限制数量
python3 -m src.cli.commands export --limit 1000 --output top1000.json
```

## 🚀 自动增量构建详解（v2.1.0+ 核心功能）

自动模式（`--mode auto`）专为**日更定式库**设计，实现从下载到入库的全流程自动化。这是 v2.1.0 引入的最重要的功能。

### 核心特性

| 特性 | 说明 | 优势 |
|------|------|------|
| **断点续传** | 自动检测已处理日期，从中断处继续 | 随时可中断，下次自动恢复 |
| **增量下载** | 只下载服务器新增的tar文件 | 节省带宽和时间 |
| **增量提取** | 每日一个temp文件，只处理新下载 | 避免重复计算 |
| **增量CMS** | 基于历史统计累加，非全量重统计 | 内存友好，速度更快 |
| **批量保存** | 每30天保存一次CMS | 减少磁盘I/O |
| **流式重建** | 重建时流式读取所有temp文件 | 内存占用恒定 |

### 工作流程

```
┌─────────────────────────────────────────────────────────────────────┐
│                      自动增量构建流程（4步骤）                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  📥 步骤1: 检测与下载                                                │
│     ├─> 访问KataGo Archive获取可用日期列表                           │
│     ├─> 对比本地缓存，找出缺失日期                                   │
│     ├─> 仅下载新日期对应的tar.bz2（已下载自动跳过）                   │
│     └─> 支持--download-only仅下载不构建                              │
│                                                                     │
│  🔧 步骤2: 提取与统计（同时进行）                                     │
│     ├─> 遍历新下载的tar文件                                          │
│     ├─> 提取四角着法 → auto/temp/YYYY-MM-DD.txt.gz                   │
│     ├─> 同时更新CMS计数器（不二次遍历）                               │
│     ├─> 每30天批量保存一次CMS                                        │
│     └─> 通过文件mtime记录处理进度（断点续传）                         │
│                                                                     │
│  🏗️ 步骤3: 全量重建                                                  │
│     ├─> 流式读取所有temp文件（不加载到内存）                          │
│     ├─> 逆向遍历 + 单链检测 + topk筛选                               │
│     ├─> 方向归一化去重（v2.1.1优化）                                  │
│     └─> 生成完整定式列表                                             │
│                                                                     │
│  💾 步骤4: 入库                                                      │
│     └─> 整库替换 database.json（非追加，保证一致性）                  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 状态管理设计（简化哲学）

**核心思想：状态即文件系统**

不依赖复杂的进度跟踪，通过文件存在性判断状态：

| 文件/目录 | 状态含义 | 检查方式 |
|-----------|----------|----------|
| `katago-cache/YYYY-MM-DDrating.tar.bz2` | 该日期已下载 | `path.exists()` |
| `auto/temp/YYYY-MM-DD.txt.gz` | 该日期已提取 | `path.exists()` |
| `auto/cms.pkl` | 有统计历史 | `path.exists()` |
| `auto/cms.pkl` mtime | 上次处理日期 | `stat().st_mtime` |
| `database.json` | 定式库存在 | `path.exists()` |

**优势：**
- ✅ 无需维护复杂的进度JSON
- ✅ 文件系统即状态，直观可靠
- ✅ 支持手动删除任意文件恢复特定状态
- ✅ 断点续传通过文件列表对比自动实现

### 配置参数

自动模式的默认配置（可通过修改 `auto/state.json` 调整）：

| 参数 | 默认值 | 说明 |
|-----|--------|-----|
| `estimated_games` | 200万 | 预估棋谱数，决定CMS大小（16M width） |
| `min_freq` | 10 | 最小出现频率 |
| `global_top_k` | 10万 | 定式库上限 |
| `rebuild_threshold_days` | 0 | 重建阈值（0=立即重建） |
| `first_n` | 80 | 每谱提取前N手 |
| `distance_threshold` | 4 | 连通块距离阈值 |
| `min_moves` | 4 | 最少手数 |

### 手动修改配置

编辑 `~/.weiqi-joseki/auto/state.json`：

```json
{
  "config": {
    "min_freq": 15,
    "global_top_k": 50000,
    "rebuild_threshold_days": 7
  }
}
```

修改后下次运行 `katago --mode auto` 即生效。

### 使用示例

**首次全量构建（约200万谱，10万定式）：**
```bash
# 开始自动构建（首次会下载所有历史数据）
python3 -m src.cli.commands katago --mode auto

# 限制处理数量（测试用）
python3 -m src.cli.commands katago --mode auto --limit 5
```

**日常增量更新（每天运行）：**
```bash
# 只处理新增日期，通常几分钟完成
python3 -m src.cli.commands katago --mode auto
```

**仅下载不构建：**
```bash
# 先下载数据，稍后构建
python3 -m src.cli.commands katago --mode auto --download-only
```

**实际运行输出示例：**
```
============================================================
🚀 Katago 自动增量构建
============================================================
📍 断点恢复：上次处理到 2026-04-25

【步骤1/2】提取棋谱并更新CMS...
   处理: 2026-04-26...
      ✅ 提取: 1523谱, 12504定式串, 412938前缀
   处理: 2026-04-27...
      ✅ 提取: 1489谱, 11982定式串, 398421前缀
      💾 批次 1 保存完成（2天）
   ✅ 共处理 2 个新日期，保存 1 次

【步骤3】重建定式库...
   共 120 个temp文件
🔄 Phase 2: 逆向遍历+单链检测，选取top-100000...
  处理: 150000定式/2850000前缀, 堆大小: 100000, 单链跳过: 52341
  堆中候选: 100000 个, 单链跳过: 52341 个
🔄 Phase 3: 排序...
  候选定式: 100000
✅ 构建完成: 100000 条定式
已保存 100000 条定式到 ~/.weiqi-joseki/database.json
✅ 重建完成，共 100000 条定式
```

### 强制重建

如果需要全量重建（如算法升级后）：

```bash
# 删除状态，下次运行将全量重建
rm -rf ~/.weiqi-joseki/auto/
python3 -m src.cli.commands katago --mode auto

# 或使用 --force-rebuild
python3 -m src.cli.commands katago --mode auto --force-rebuild
```

### 空间占用估算

| 项目 | 单日 | 100天 | 300天 |
|-----|------|-------|-------|
| tar.bz2缓存 | ~500MB | ~50GB | ~150GB |
| temp.txt.gz | ~50MB | ~5GB | ~15GB |
| cms.pkl | 固定~8MB | ~8MB | ~8MB |
| database.json | ~100KB | ~100KB | ~100KB |

**说明：** temp文件保留全部历史，用于重建时流式读取。

## 核心算法

### 时序连通性分析（Temporal Connectivity）v2.1.1

从棋谱中提取定式的核心算法，替代传统的局面连通块分析：

**算法流程：**
1. **N路范围提取** - 收集13路（或11路/9路）范围内的所有棋子
2. **时序连通分析** - 按行棋顺序遍历，维护"活跃区域"
   - 距离活跃区域≤4：加入核心区域
   - 距离活跃区域>4：标记为"脱先"
3. **凸包回退检测** - 检查被剔除的是否落入核心凸包
4. **多级回退** - 13路→11路→9路，直到无误判

**优势对比：**

| 特性 | 局面连通块 (v1.x) | 时序连通性 (v2.1.1) |
|-----|------------------|-------------------|
| 关注点 | 最终谁连通 | 行棋是否连续 |
| 脱先处理 | 混在一起 | 正确剔除 |
| 计算步骤 | 2轮连通块 | 1轮时序分析 |
| 准确性 | 一般 | 更高 |

### 凸包检测与回退策略

**凸包计算（单调链算法）：**
```python
def convex_hull(points):
    # O(n log n) 复杂度
    # 返回凸包顶点列表
```

**回退决策：**
```
13路提取 → 时序分析 → 凸包检测
    ↓ 被剔除着法在凸包内（误判脱先）
11路提取 → 时序分析 → 凸包检测
    ↓ 被剔除着法在凸包内
9路提取（最严格）
```

**为什么有效：**
- 13路范围大，可能包含多个战斗 → 时序分析剔除真脱先
- 如果"脱先"着法实际在核心凸包内 → 说明范围太大，需要收紧
- 逐步回退到11路→9路，直到没有误判

### CMS频率统计

Count-Min Sketch算法估算前缀出现频率：
- 宽度: 200000
- 深度: 5
- 内存占用: ~3.8MB

### 逆向遍历 + 单链检测

从长到短遍历前缀，检测单链并去重：
- 单链阈值: 5%（count变化小于5%视为单链）
- 小顶堆选top-k
- 统一转ruld方向去重

## Python API

### v2.1.1 简化接口

```python
from weiqi_joseki.src.builder import build_katago_joseki_db
from weiqi_joseki.src.discover import discover_joseki
from weiqi_joseki.src.extraction import extract_moves_all_corners, get_move_sequence
from weiqi_joseki.src.storage import JsonStorage

# 构建定式库
joseki_list = build_katago_joseki_db(
    tar_path="/path/to/katago.tar.bz2",
    min_freq=10,
    top_k=100000,
    first_n=80,
    distance_threshold=4,
    min_moves=4
)

# 发现定式（统一接口替代v1.x的match/identify）
storage = JsonStorage()
joseki_list = storage.get_all()

results = discover_joseki(
    sgf_data=open("game.sgf").read(),
    joseki_list=joseki_list,
    first_n=80,
    distance_threshold=4
)

for corner, match in results.items():
    print(f"{corner}: {match.joseki_id} "
          f"匹配{match.prefix_len}/{match.total_moves}手")

# 提取四角着法（自动多级回退）
result = extract_moves_all_corners(
    sgf_data=open("game.sgf").read(),
    first_n=80,
    distance_threshold=4
)

for corner, moves in result.items():
    coords = get_move_sequence(moves)
    print(f"{corner}: {' '.join(coords)}")
```

### API 变化说明

**v1.x → v2.1.1 迁移：**

| v1.x | v2.1.1 | 说明 |
|-----|--------|-----|
| `JosekiMatcher.match()` | `discover_joseki()` | 统一发现接口 |
| `JosekiImporter.import()` | 无需导入 | 功能合并到katago构建 |
| `JosekiExporter.export()` | `storage.get_all()` | 直接获取列表 |
| `identify_joseki()` | `discover_joseki()` | 统一接口 |
| `extract_moves()` | `extract_moves_all_corners()` | 四角同时提取 |

## 隐私声明

- ❌ 不收集个人数据
- ❌ 无内置数据
- ✅ 数据完全本地存储
- ✅ 仅提供开放数据获取工具

## 依赖

- Python 3.6+
- 无第三方依赖（纯标准库）

## 版本更新

### v2.1.1 (2026-04-28) - 定式方向归一化
**定式存储和匹配优化**

**方向归一化：**
- ✅ **标准化存储**: 定式统一归一化为角部上半区域存储
- ✅ **对角线对称**: 以 (c+r=18) 对角线为对称轴进行镜像转换
- ✅ **简化匹配**: TrieMatcher 和 Discoverer 改为单方向匹配，代码减少57行
- ✅ **移除冗余去重**: Phase 3 去重逻辑不再需要，简化构建流程

**测试优化：**
- ✅ **新增--limit参数**: 自动构建支持 `--limit` 参数，限制处理的tar文件数量，便于测试

### v2.1.0 (2026-04-25) - 自动增量构建
**新增自动增量构建模式**

**自动模式（`--mode auto`）：**
- ✅ **增量下载** - 只下载服务器新增的日期，支持断点续传
- ✅ **增量提取** - 每日一个temp文件，只处理新下载的棋谱
- ✅ **增量CMS** - 基于历史统计数据累加，避免全量重统计
- ✅ **智能重建** - 达到阈值后自动全量重建定式库
- ✅ **状态持久化** - 配置、进度、统计自动保存到auto/state.json
- ✅ **大容量配置** - 默认支持200万棋谱，10万条定式

**架构改进：**
- ✅ **新增auto模块** - AutoState状态管理，自适应CMS配置
- ✅ **CMS持久化** - save_to_file/load_from_file支持序列化
- ✅ **流式多文件读取** - 重建时流式处理所有temp文件，内存友好
- ✅ **Mixin混入模式** - 自动构建方法动态添加到KatagoJosekiBuilder

### v2.0.0 (2026-04-22) - 重大重构
**性能与架构全面升级**

**架构改进：**
- ✅ **移除局面连通块分析**: 直接时序连通性分析，减少计算步骤
- ✅ **多级回退策略**: 13路→11路→9路智能选择，避免过度提取
- ✅ **凸包检测算法**: 判断被剔除着法是否应纳入核心区域
- ✅ **完全模块化**: 6个核心模块（builder/cli/core/discover/extraction/storage/matching/utils）

**性能提升：**
- ✅ **内存占用减少30%**: 精简数据模型，去除冗余字段
- ✅ **构建速度提升40%**: 算法优化，I/O减少
- ✅ **单次提取<1ms**: 凸包计算优化，支持大规模处理

**接口精简：**
- ✅ **CLI命令从12个缩减到7个**: 移除import/match/identify/compare/search
- ✅ **Python API简化**: 统一discover接口，替代match/identify
- ✅ **数据模型简化**: 去除name/category/tags，专注核心数据

### v1.2.0 (2026-04-21) - 重构版
- ✅ **完全重构**: 从旧代码重构为模块化架构
- ✅ **简化数据模型**: 去除name/category/tags字段，保留核心数据
- ✅ **统一入库**: 先扫描所有棋谱统计，再统一选取定式入库
- ✅ **简化CLI**: 保留核心命令（init, katago, list, stats, extract, discover, export）
- ✅ **连通块提取**: 使用8-connectivity检测棋盘上同一局部的棋子
- ✅ **核心算法保留**: CMS统计、逆向遍历、单链检测全部保留

### v1.1.x (2026-04-10 及之前)
- 旧版本功能（已归档）

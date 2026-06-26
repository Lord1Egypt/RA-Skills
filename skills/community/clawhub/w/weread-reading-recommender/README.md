# weread-reading-recommender

一个本地优先的微信读书推荐 skill。它的目标不是做云同步，也不是代管 cookie，而是让你在自己的机器上：

1. 读取本地微信读书 cookie
2. 导出原始阅读数据
3. 归一化成推荐友好的 JSON
4. 基于阅读历史和当前学习目标推荐下一本书

## 项目定位

这个项目适合下面几类需求：

- 根据微信读书记录推荐书
- 分析阅读偏好和阅读画像
- 结合“最近想学的主题”与历史阅读轨迹一起做推荐
- 刷新、导出、归一化本地微信读书数据

它是：

- 本地导出工具
- 本地归一化工具
- 面向推荐场景的 skill 草案

它不是：

- 云端同步服务
- CookieCloud 默认集成
- 托管 cookie 的远程代理

## 核心流程

推荐使用下面的顺序：

1. 检查本地是否已有可用 cookie
2. 运行导出脚本，生成 raw JSON
3. 运行归一化脚本，生成 normalized JSON
4. 用 normalized JSON 做阅读画像和推荐

如果本地没有 cookie，再由用户自己设置本地 cookie。项目不会把 cookie 写进仓库文件，也不会默认依赖第三方同步服务。

## 当前能力

### 1. 导出脚本

文件：[`scripts/export_weread.py`](scripts/export_weread.py)

支持：

- 从 `--cookie` 读取 cookie
- 从 `--cookie-file` 读取 cookie
- 从 `--env-var` 指定的环境变量读取 cookie
- 默认读取 `WEREAD_COOKIE`
- 调用微信读书书架同步接口
- 调用微信读书 notebook 接口
- 可选调用 `book/info` 获取书籍补充信息
- 输出不含 cookie 的 raw JSON

### 2. 归一化脚本

文件：[`scripts/normalize_weread.py`](scripts/normalize_weread.py)

会把 raw JSON 转成推荐友好的结构，包括：

- 每本书的阅读状态
- 阅读进度与阅读时长
- 笔记、书签、点评计数
- `engagement_score`
- `summary`
- `profile_inputs`
- `llm_hints`

### 3. Skill 说明

文件：[`SKILL.md`](SKILL.md)

定义了：

- 什么时候用这个 skill
- 没有 normalized 数据时的工作流
- 如何检查本地 cookie
- 推荐时的解释结构
- 安全和隐私边界

## 快速开始

### 环境要求

- Python 3
- `requests`

安装依赖：

```bash
python3 -m pip install requests
```

### 1. 准备本地 cookie

优先检查本地是否已经有可用 cookie，例如：

- 你已经设置了 `WEREAD_COOKIE`
- 你已经有本地 cookie 文件

如果没有，再自行设置本地 cookie，例如：

```bash
export WEREAD_COOKIE='wr_skey=...; wr_vid=...; ...'
```

### 2. 导出 raw 数据

```bash
python3 scripts/export_weread.py --out data/weread-raw.json
```

可选用法：

```bash
python3 scripts/export_weread.py --cookie-file ~/.config/weread.cookie --out data/weread-raw.json
python3 scripts/export_weread.py --env-var WEREAD_COOKIE --include-book-info --detail-limit 50 --out data/weread-raw.json
```

### 3. 归一化数据

```bash
python3 scripts/normalize_weread.py --input data/weread-raw.json --output data/weread-normalized.json
```

### 4. 用样例数据试跑

仓库内已提供样例 raw 数据：

- [`assets/sample-weread-raw.json`](assets/sample-weread-raw.json)

可以直接运行：

```bash
python3 scripts/normalize_weread.py \
  --input assets/sample-weread-raw.json \
  --output assets/sample-weread-normalized.json
```

## 输出结构

### Raw export

顶层至少包含：

- `exported_at`
- `source`
- `summary`
- `shelf_sync`
- `notebook`
- `book_info`
- `warnings`

### Normalized export

顶层至少包含：

- `generated_at`
- `source_file`
- `summary`
- `profile_inputs`
- `llm_hints`
- `books`

每本书至少包含：

- `book_id`
- `title`
- `author`
- `translator`
- `categories`
- `book_lists`
- `status`
- `is_finished`
- `progress`
- `reading_time_seconds`
- `last_read_at`
- `note_count`
- `bookmark_count`
- `review_count`
- `interaction_count`
- `engagement_score`
- `is_imported`
- `is_paid`
- `public_rating`
- `intro`

更完整的数据说明见：

- [`SPEC.md`](SPEC.md)
- [`references/data-schema.md`](references/data-schema.md)

## 推荐场景示例

- 结合我的微信读书记录，我最近想系统学 AI Agent，推荐 5 本书
- 基于我的阅读历史，推荐下一本最适合现在读的书
- 分析我的阅读偏好，并给我 3 本稳妥推荐 + 2 本探索推荐
- 帮我刷新微信读书数据，然后按最近在读主题推荐下一批书

## 隐私与安全

这个项目遵循 local-first：

- cookie 仅限本地使用
- 不把 cookie 写进导出 JSON
- 不把 cookie 写进仓库文件
- 不默认依赖 CookieCloud 或第三方同步服务
- 不要求远端托管 cookie

隐私边界说明见：

- [`references/privacy-model.md`](references/privacy-model.md)

## 项目结构

```text
weread-reading-recommender/
├── README.md
├── PLAN.md
├── SPEC.md
├── TODO.md
├── SKILL.md
├── scripts/
│   ├── export_weread.py
│   └── normalize_weread.py
├── references/
│   ├── data-schema.md
│   ├── privacy-model.md
│   └── recommendation-rubric.md
└── assets/
    ├── sample-weread-raw.json
    └── sample-weread-normalized.json
```

## 当前状态

当前仓库已经完成：

- 正式版 `SKILL.md`
- `export_weread.py`
- `normalize_weread.py`
- `sample-weread-normalized.json`

后续可继续增强：

- 划线和笔记文本分析
- 外部候选书召回
- 中英文书名归一化和去重
- 自动刷新流程
- 更强的推荐解释层

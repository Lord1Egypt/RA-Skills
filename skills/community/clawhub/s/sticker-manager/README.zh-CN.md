# sticker-manager

一个用于 OpenClaw 的表情包管理 skill，支持保存、整理、打标签、检索和发送本地表情包与反应图片，支持 JPG、JPEG、PNG、WEBP 和 GIF 格式。

这个项目由 TetraClaw（即丁蟹）维护和管理，属于其 OpenClaw agent 代码与工具体系的一部分。

作者：
- Wenzhuang Zhu
- TetraClaw（丁蟹）

English version: [README.md](./README.md)

仓库 / 备用下载地址：
- GitHub: https://github.com/TetraClaw/sticker-manager
- 如果 ClawHub 挂了，可以直接从 GitHub 仓库获取和下载。

## 功能

- 保存最新收到的图片/动图到本地表情包库
- 从最近聊天记录/历史媒体中指定保存图片
- 支持批量收集，默认目标数量为 15 张
- 默认改为单线程执行，降低内存压力；保留去重、低质量过滤
- 收集完成后默认输出一轮图片理解/表情场景语义识别批任务
- 不足目标数量时明确给出 NEED_MORE 结果
- 按关键词搜索表情包
- 重命名或删除已有表情包
- 清理质量过低的文件
- 为表情包添加情绪、场景、关键词和描述
- 生成用于语义匹配的模型负载
- 生成图像识别 fallback 计划
- 支持 JPG、JPEG、PNG、WEBP、GIF
- **新增**: 从本地目录批量导入，支持自动去重
- **新增**: 从 URL、目录、网页发现表情包来源
- **新增**: 使用视觉模型自动生成语义标签
- **新增**: 基于聊天历史的上下文感知推荐

## 快速开始

```bash
python3 -m pip install -r requirements.txt
make install-hooks
make test
```

如果只是只读使用，hooks 不是必需的；如果要发布或提交改动，建议先启用。它会在 `git commit` 和 `git push` 前运行敏感信息检查和测试。

## 语言选择

支持输出语言：
- `zh`
- `en`

优先级：
1. `--lang=...`
2. `STICKER_MANAGER_LANG`
3. `LANG`
4. 默认英文

## 从聊天记录 / 最近媒体保存

示例：

```bash
python3 scripts/save_sticker.py --list-history
python3 scripts/save_sticker.py --history-index=2 "保存历史图"
python3 scripts/save_sticker.py --source=file_39---example.jpg "按来源保存"
python3 scripts/save_sticker_auto.py --history-index=3 "带质量检查保存"
```

适用流程：
- 保存这张图
- 保存刚才那张图
- 保存聊天里之前发过的图片

## 批量收集说明

说明：`--workers` 参数仅为兼容旧调用而保留；除 `1` 之外的值都会被忽略，实际执行固定为单线程。

补充：
- 若数量不足 `--target-count`，命令会返回退出码 `2`，并输出 `NEED_MORE=...`
- 默认会输出一份 `__SEMANTIC_BATCH__:` JSON 计划，供外层 agent 执行图像语义分析

## 批量导入（新增）

从本地目录批量导入表情包，支持自动去重：

```bash
# 从单个目录导入
python3 scripts/batch_import.py ./stickers --target-dir ~/.openclaw/workspace/stickers/library/

# 从多个目录导入
python3 scripts/batch_import.py ./dir1 ./dir2 --target-dir ./library

# 导入并生成自动标签计划
python3 scripts/batch_import.py ./stickers --auto-tag

# 从源文件导入
python3 scripts/batch_import.py --sources-file ./sources.txt --target-dir ./library
```

选项：
- `--recursive` / `--no-recursive`: 控制目录扫描方式（默认：递归）
- `--min-size` / `--max-size`: 按文件大小过滤
- `--no-dedupe`: 跳过去重
- `--auto-tag`: 为导入的表情包生成自动标签计划
- `--output`: 保存导入报告为 JSON 文件

## 图源发现（新增）

从多种渠道发现表情包来源：

```bash
# 从本地目录发现
python3 scripts/discover_sources.py ./stickers

# 从 URL 发现
python3 scripts/discover_sources.py https://example.com/image1.gif https://example.com/image2.png

# 从网页发现（抓取静态页面图片）
python3 scripts/discover_sources.py https://example.com/gallery

# 从文件加载来源
python3 scripts/discover_sources.py --urls-file ./urls.txt --dirs-file ./dirs.txt --pages-file ./pages.txt

# 保存发现结果
python3 scripts/discover_sources.py ./stickers --output ./discovered.json

# 对远程 URL 做联网校验
python3 scripts/discover_sources.py --fetch-urls https://example.com/image1.gif
```

说明：
- 本地目录会立即扫描。
- 远程图片 URL 默认只记录为 `pending`，方便先做轻量发现和规划，不强制联网。
- 只有传入 `--fetch-urls` 时，才会实际请求远程 URL 并补充响应大小等信息。
- 静态页面抓取时，汇总只统计成功提取出的图片 URL，不会把抓取失败页面误算为成功来源。

## 语义匹配

语义流程设计为：
1. 为每个表情包存储元数据：emotions / scenes / keywords / description
2. 生成模型匹配负载
3. 让模型根据语义选择最合适的表情包
4. 规则匹配只作为 fallback

示例：

```bash
python3 scripts/sticker_semantic.py prepare-model "用户表面镇定但其实有点慌"
python3 scripts/sticker_semantic.py suggest "终于修好了"
python3 scripts/sticker_semantic.py suggest "终于修好了" --strategy=model
python3 scripts/sticker_semantic.py tag "sticker_name" "happy,calm" "meeting,celebration" "approval,done" "一张平静认可的反应图。"
```

## 自动标签（新增）

使用视觉模型自动生成语义标签：

```bash
# 自动标签单个图片
python3 scripts/sticker_semantic.py auto-tag ./sticker.gif

# 自动标签目录下所有图片
python3 scripts/sticker_semantic.py auto-tag-dir ./stickers/

# 使用 --apply 标志（当视觉模型结果可用时）
python3 scripts/sticker_semantic.py auto-tag ./sticker.gif --apply
```

auto-tag 命令生成一个视觉计划，需要由具备视觉能力的模型执行。输出包含 `__AUTO_TAG__:` 标记，便于程序化处理。

## 上下文感知推荐（新增）

基于聊天历史上下文推荐表情包：

```bash
# 从 JSON 历史
python3 scripts/sticker_semantic.py context-recommend '[{"content": "太棒了！"}, {"content": "我们赢了！"}]'

# 从历史文件
python3 scripts/sticker_semantic.py context-recommend ./chat_history.json

# 从纯文本文件
python3 scripts/sticker_semantic.py context-recommend ./chat.txt

# 指定 top N 推荐
python3 scripts/sticker_semantic.py context-recommend ./history.json --top=5
```

该命令分析聊天历史并返回 top N 个表情包推荐及推荐理由。

## 图像识别 fallback 规划

环境变量：
- `STICKER_MANAGER_VISION_MODELS`

默认 fallback 顺序：
1. `bailian/kimi-k2.5`
2. `openai/gpt-5-mini`

示例：

```bash
python3 scripts/sticker_semantic.py vision-plan ./sample.png "找一张表达质疑情绪的图"
```

如果所有可用识图模型都失败，skill 会明确提示：图意解释、质量校验和情绪标签无法可靠完成。

## 默认路径

- 表情包库存目录：`~/.openclaw/workspace/stickers/library/`
- 入站媒体目录：`~/.openclaw/media/inbound/`

可通过以下环境变量覆盖：
- `STICKER_MANAGER_DIR`
- `STICKER_MANAGER_INBOUND_DIR`
- `STICKER_MANAGER_LANG`
- `STICKER_MANAGER_VISION_MODELS`

## 文件说明

- `LICENSE`
- `SKILL.md`
- `scripts/common.py`
- `scripts/get_sticker.py`
- `scripts/manage_sticker.py`
- `scripts/save_sticker.py`
- `scripts/save_sticker_auto.py`
- `scripts/sticker_semantic.py`
- `scripts/collect_stickers.py`
- `scripts/batch_import.py` (新增)
- `scripts/discover_sources.py` (新增)
- `scripts/check_sensitive.py`
- `Makefile`
- `tests/`

## 当前限制

- 图像含义提取仍依赖 OpenClaw 外层 agent/tool 真正去执行 vision fallback 模型链。
- 语义推荐效果会明显依赖 description 的质量。

## Git 安全校验

这个仓库可以通过下面的方式启用本地 git hooks：

```bash
make install-hooks
```

每次 `git commit` 和 `git push` 之前，都会执行：

1. `python3 scripts/check_sensitive.py`
2. `python3 -m pytest -q`

如果检测到疑似敏感信息，会直接阻止提交或推送。

## 测试

运行测试：

```bash
make test
```

如果本地没有 `make`，也可以直接运行：

```bash
python3 -m pytest -q
```

## Roadmap

- [ ] 集成更多图源（API 方式）
- [ ] 高级去重检测（感知哈希）
- [ ] 表情包集合与文件夹管理

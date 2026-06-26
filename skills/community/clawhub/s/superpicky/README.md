# SuperPicky CLI Skill

## 这是什么？

本目录是一个 **Cursor / Agent 技能包（skill）**，把上游项目 [SuperPicky](https://github.com/jamesphotography/SuperPicky) 的鸟类照片 AI 工作流，通过固定脚本路径（`install.sh`、`run.sh`）封装起来，方便本机安装与命令行调用。详细参数、子命令与调参说明请直接查阅上游仓库与技能内 `reference/` 文档。

## What is this?

This folder is an **agent skill** that wraps the [SuperPicky](https://github.com/jamesphotography/SuperPicky) bird-photo AI pipeline behind **`install.sh`** and **`run.sh`** with predictable paths. For full CLI flags, subcommands, and tuning guides, see the upstream repository and the **`reference/`** files inside this skill.

---

## 三大能力

1. **选片** — 对文件夹做流程化选片（清晰度、质量评分、连拍、可选自动识别等）。主入口 `superpicky_cli.py`，通过 **`run.sh`** 默认模式调用（不加 `--birdid` / `--region-query`）。
2. **识别图片** — 鸟类识别（单张或批量）、按物种整理等。入口 **`run.sh --birdid`**，对应 `birdid_cli.py`。
3. **地区确认** — 将地名模糊匹配为 eBird 国家/地区代码，供选片或识别时的 `--birdid-country`、`-c`、`-r` 等参数使用。入口 **`run.sh --region-query`**（`ebird_region_query.py`）。

## Three main capabilities

1. **Culling** — Pipeline on a folder: sharpness, quality scoring, burst handling, optional auto BirdID. Entry: **`run.sh`** → `superpicky_cli.py` (default mode).
2. **Bird identification** — Identify one or many images, organize by species, etc. Entry: **`run.sh --birdid`** → `birdid_cli.py`.
3. **Region lookup** — Fuzzy place names → eBird country/region codes for `--birdid-country`, `-c`, `-r`, and related flags. Entry: **`run.sh --region-query`**.

---

## 快速开始

在技能根目录执行 `./scripts/install.sh` 安装上游与虚拟环境；日常通过 **`scripts/run.sh`** 使用上述三种能力。自动化调用、绝对路径等约定见同目录 **`SKILL.md`**。

## Quick start

From the skill root, run **`./scripts/install.sh`** to fetch upstream and create the venv. Use **`scripts/run.sh`** for all three modes. Agent conventions (absolute paths, checklist) are in **`SKILL.md`**.

```bash
./scripts/install.sh
./scripts/run.sh process /path/to/photos
./scripts/run.sh --birdid identify /path/to/image.jpg
./scripts/run.sh --region-query shanghai
```

---

## 更多文档

- 上游仓库：[github.com/jamesphotography/SuperPicky](https://github.com/jamesphotography/SuperPicky)
- 技能内索引：[`reference/README-INDEX.md`](reference/README-INDEX.md)
- CLI 帮助摘录：[`reference/cli-help-captured.txt`](reference/cli-help-captured.txt)

## More documentation

- Upstream: [github.com/jamesphotography/SuperPicky](https://github.com/jamesphotography/SuperPicky)
- In-skill index: [`reference/README-INDEX.md`](reference/README-INDEX.md)
- Captured `--help`: [`reference/cli-help-captured.txt`](reference/cli-help-captured.txt)

---
name: wbflow-batch
description: 批量工厂总控——在 wbflow-pipeline 之上做条目级编排：给定一份清单（batch.json），逐条驱动整套 8 环流水线、各自独立工作目录、统一落盘、断点续跑，并支持 WB automation 定时触发（"定时收菜"）。（WBFlow 由 10 个 skill 组成：wbflow-pipeline 总控 + story/script/storyboard/prompt/char/image/video/assemble 八环 + 本批量层，须全套配套安装，单独安装无法运行。）
allowed-tools: Read Write Edit Bash Glob Grep
---

# 批量工厂·总控（Batch）

你是"工厂车间主任"，在 **wbflow-pipeline 之上**管理一整批短片的生产。
唯一职责：**编排与落盘，不写任何一条的内容。** 内容生产仍交给 wbflow-pipeline 的 8 环。

## 核心原则
- **复用不改造**：wbflow-pipeline 的 8 环契约、星型拓扑、定妆闸门一律不动。batch 只在"条目之间"加三样东西：
  1. **独立工作目录**——每条短片一套自己的 01-08 + final，互不污染；
  2. **状态机**——每条 queued→running→done/failed，可断点续跑；
  3. **统一落盘与清单**——全部成品按命名规范汇总到 `batch_manifest.json`。
- **seed 前置**：批量场景下用户已把每条的 seed 填好，pipeline 的 Phase 0"缺则反问"改为"读 `seed.json` 直跑"，不再反问。

## 三种触发
1. **手动批量**：用户给出 batch.json（或你已 init 好的批次目录）→ 逐条跑完整套。
2. **定时收菜**：WB automation 每晚按 batch.json 跑 N 条，次晨挑用（见文末模板）。
3. **续跑**：只处理 `batch_manifest.json` 中 status 仍为 `queued` / `failed` 的条目。

## 配置格式 batch.json
| 字段 | 说明 |
|---|---|
| `batch_id` | 批次唯一 id（决定目录名） |
| `title` | 批次标题 |
| `engine` | 视频引擎备注（如 libTV / Seedance，传给 pipeline 存档） |
| `default_style` | 全局默认画风，条目可覆盖 |
| `items[]` | 条目数组，每条含： |
| ├ `slug` | 条目短标识（进目录名 `<NN>_<slug>`） |
| ├ `seed_theme` | 主题 / 创意种子 |
| ├ `episode_count` | 集数 |
| ├ `duration_sec` | 目标时长（秒） |
| ├ `style` | 画风（覆盖 default_style） |
| ├ `output_name` | 成品展示名 |
| └ `char_ids` | 可选，跨条目共用定妆角色（固定主播脸等） |

样例见 `batch.example.json`。

## 目录契约
```
batches/<batch_id>/
  batch.json                 # 原始清单
  batch_manifest.json        # 状态机 + 成品索引（aggregate 维护）
  output/
    <NN>_<slug>/
      01_story/ 02_script/ 03_storyboard/ 04_prompts/
      05_chars/ 06_images/ 07_videos/
      seed.json              # init_series 展开的本条目 seed（pipeline Phase0 直读）
      final.mp4              # 该条目成品
```

## 执行协议
```
Step 0  init      python scripts/init_series.py --config batches/<batch_id>/batch.json
                → 建骨架 + seed.json + manifest（全部 queued）
Step 1  逐条     对每条 status ∈ {queued, failed}：
                a. 置 running，更新 manifest
                b. 以 <NN>_<slug>/ 为 workdir 调用 wbflow-pipeline，
                   指示其读 seed.json 作 Phase0 输入、跳过反问、直跑 8 环至 final.mp4
                c. 成功 → done；失败 → failed（记 error），继续下一条，不中断整批
Step 2  aggregate python scripts/aggregate.py --batch batches/<batch_id>
                → 刷新 manifest + 打印清单；可选 --montage 拼合集预览
```

## 数据契约 / 状态机
- 每条独立满足 wbflow-pipeline 的全部契约（角色 id⊆story、appearance_lock 一致等）。
- manifest 每条记录：`slug / output_name / workdir / status / final_path / duration_sec_est / error / updated_at`。
- **任一条失败不阻断整批**：标记 failed 继续，最后统一汇报，支持续跑只重做失败的。

## 落盘与命名
- 成品固定名 `final.mp4`，置于 `<NN>_<slug>/`。
- 对外展示名用 `output_name`；manifest 中以 `final_path`（绝对路径）索引，**不复制成品**，避免双份存储。

## 定时触发（WB automation 模板）
用 WB 自动化建一个每日任务，prompt 示例：
> "运行 wbflow-batch：读取 `batches/<batch_id>/batch.json`，对 status 为 queued/failed 的条目，以各自 `<NN>_<slug>/` 为 workdir 逐条驱动 wbflow-pipeline 出片（读 seed.json 直跑），最后跑 aggregate 刷新清单。出片引擎用 `<engine>`。"

调度（自然语言）：每天 22:00 触发，跑完即止；次日晨查看 `batches/<batch_id>/batch_manifest.json` 挑选可用成品。

## 不做的事
- 不写剧本 / 分镜 / 提示词 / 画关键帧 / 剪片（那是 8 环的事）
- 不改 wbflow-pipeline 的契约与拓扑
- 不因为单条失败而中断整批或回滚已完成条目
- 不在未 init 的情况下直接跑（缺骨架会破坏契约）

# Wan Video Generation API Notes

官方文档：

- https://help.aliyun.com/zh/model-studio/text-to-video-api-reference
- https://help.aliyun.com/zh/model-studio/text-to-video-guide
- https://help.aliyun.com/zh/model-studio/use-video-generation

## 当前 skill 使用方式

- 默认模型：`wan2.6-t2v`
- 默认 Endpoint：`POST /api/v1/services/aigc/video-generation/video-synthesis`
- 查询任务：`GET /api/v1/tasks/{task_id}`
- 鉴权：`Authorization: Bearer $DASHSCOPE_API_KEY`
- 异步调用必须加：`X-DashScope-Async: enable`

## 当前脚本的默认策略

- 默认提交异步任务并轮询
- 成功后自动下载 MP4 到本地 `outputs/`
- `--no-wait` 模式下只返回 task_id
- 默认按 `wan2.6-t2v` 的能力集组织参数
- 支持 `--goal` 做 cheap|balanced|quality 的目标驱动选型
- 支持 `--tier` 做档位驱动选型
- 支持 `--quality` + `--ratio` 映射到官方允许的具体 `size`
- 会按不同模型自动限制可用的分辨率档位
- 会基于内置的中国内地价格表显示成本提醒

## 选型与覆盖规则

- 模型选择：`CLI --model > CLI --tier > CLI --goal > config.defaultGoal/config.goal > config.defaultTier/config.tier > config.model > 内置默认`
- 分辨率选择：`CLI --size > CLI (--quality + --ratio) > goal/tier 默认 quality/ratio > 模型默认`
- 时长选择：`CLI --duration > goal/tier 默认 duration > 模型默认`
- `goal` 用于表达用户目标，`tier` 用于表达具体模型档位；显式 `--tier` 会覆盖 `goal`
- `tier` 和 `goal` 都只负责提供默认模型、默认分辨率档位和默认时长，不会锁死 `--quality`、`--ratio`、`--size`、`--duration`
- 推荐把 `cheap|balanced|quality` 的意图映射维护在 `config.json` 的 `goals` 中，把 `draft|standard|final` 的模型与默认 `quality/ratio/duration` 维护在 `config.json` 的 `tiers` 中
- `--dry-run` 会打印本次最终选中的模型、分辨率、时长来源和成本估算，便于 Agent 在正式提交前确认

## 推荐的 Agent 调用方式

- 日常调用优先传 `--goal`，不要一开始就硬编码具体模型
- 只有当你明确知道要哪个模型档位时再传 `--tier`
- `--goal balanced` 或 `--tier standard` 之后，仍可显式传 `--quality`、`--ratio`、`--duration` 覆盖默认值
- 如果需要精确控制尺寸，直接传 `--size=宽*高`；一旦传了 `--size`，就不再依赖 `quality+ratio`
- 低成本试探 prompt 时优先使用 `--goal cheap`
- 正式提交前先跑一次 `--dry-run`，确认模型、分辨率、时长和费用提醒

## 关键限制

- 任务与结果链接默认只保留 24 小时
- 视频生成通常需要 1 到 5 分钟
- `wan2.6` / `wan2.5` 默认生成有声视频
- `wan2.2` / `wanx2.1` 默认生成无声视频
- `size` 传给服务端时必须是具体分辨率，例如 `1280*720`
- `duration` 也受模型约束，不是所有模型都支持自由修改秒数

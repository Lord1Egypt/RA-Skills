# Wan Image Generation API Notes

官方文档：

- https://help.aliyun.com/zh/model-studio/text-to-image-v2-api-reference
- https://help.aliyun.com/zh/model-studio/text-to-image
- https://help.aliyun.com/zh/model-studio/regions/

## 当前 skill 使用方式

- 默认模型：`wan2.6-t2i`
- 默认 Endpoint：`POST /api/v1/services/aigc/image-generation/generation`
- 查询任务：`GET /api/v1/tasks/{task_id}`
- 鉴权：`Authorization: Bearer $DASHSCOPE_API_KEY`
- 异步调用必须加：`X-DashScope-Async: enable`

## 当前脚本的默认策略

- 默认提交异步任务并轮询
- 成功后自动下载图片到本地 `outputs/`
- `--no-wait` 模式下只返回 task_id
- 兼容 `wan2.6-t2i` 的新版协议
- 对 `wan2.5` / `wan2.2` 老模型提供 best-effort 兼容
- 支持 `--goal` 做 cheap|balanced|quality 的目标驱动选型
- 支持 `--tier` 做档位驱动选型
- 支持 `--ratio` 使用官方推荐比例
- 支持 `draft/final` 两档快捷尺寸预设
- 下载文件名包含时间戳、task_id 和 prompt 摘要
- 支持 `--dry-run` 做请求预检
- 会基于内置的中国内地价格表显示成本提醒

## 选型与覆盖规则

- 模型选择：`CLI --model > CLI --tier > CLI --goal > config.defaultGoal/config.goal > config.defaultTier/config.tier > config.model > 内置默认`
- 画幅选择：`CLI --size > CLI --ratio > CLI --preset > goal 默认 ratio/preset > config.ratio > config.preset > 脚本默认`
- `goal` 用于表达用户意图，`tier` 用于表达具体模型档位；显式 `--tier` 会覆盖 `goal`
- `tier` 和 `goal` 都只负责提供默认模型或默认尺寸策略，不会锁死 `size`、`ratio`、`preset`
- 推荐把 `cheap|balanced|quality` 的意图映射维护在 `config.json` 的 `goals` 中，把 `draft|standard|final` 的模型映射维护在 `config.json` 的 `tiers` 中
- `--dry-run` 会打印本次最终选中的模型、尺寸来源和成本估算，便于 Agent 在正式提交前确认

## 推荐的 Agent 调用方式

- 日常调用优先传 `--goal`，不要一开始就硬编码具体模型
- 只有当你明确知道要哪个模型档位时再传 `--tier`
- 需要临时覆盖时，直接传 `--model`、`--ratio`、`--preset` 或 `--size`
- 低成本试探 prompt 时优先使用 `--goal cheap --n 1`
- 正式出图前先跑一次 `--dry-run`，确认模型、尺寸和费用提醒
- 如果 Agent 需要稳定复现结果，显式传 `--seed`

## 关键限制

- 任务与结果链接默认只保留 24 小时
- `wan2.6-t2i` 支持自由尺寸，但总像素和宽高比有限制
- `n` 直接影响费用，测试建议先用 `1`

## 常见比例推荐尺寸

- `1:1` -> `1280*1280`
- `3:4` -> `1104*1472`
- `4:3` -> `1472*1104`
- `9:16` -> `960*1696`
- `16:9` -> `1696*960`

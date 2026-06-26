# Hermes Agent Contract

这个 skill 给 Hermes agent 的推荐调用分成两阶段：

## 1. 审核阶段

调用：

```bash
bash scripts/run_hermes_agent_ops.sh \
  --topic "主题" \
  --mode review
```

行为：

- 生成 `content.json`
- 生成 `report.json`
- 生成 `summary.json`
- 不真正发布

Hermes 应读取 `summary.json`：

- `ok=true` 代表 dry-run 成功
- `next_action=human_review_content_then_publish` 代表应进入人工审核或二次编辑

## 2. 发布阶段

若内容已审核完成，调用：

```bash
bash scripts/run_hermes_agent_ops.sh \
  --mode publish \
  --content-json /path/to/content.json
```

如已存在审核通过的 `content.json`，`publish` 阶段可不再重复传 `--topic`。

行为：

- 跳过内容生成
- 直接顺序发布到目标平台
- 产出新的 `report.json` 和 `summary.json`
- 若审核阶段抓取了参考素材，还会产出 `materials.json`

## 约束

- 不要并行调用多个平台脚本
- 默认入口应是 `run_hermes_agent_ops.sh`
- 若需要部分平台，使用 `--platforms twitter,weibo`
- Hermes 只应基于 JSON 工件判断状态，不要解析终端日志作为主信号

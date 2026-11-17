# 隐私清理说明

本 skill 在发布前已完成隐私清理。

## 清理内容

| 类型 | 处理方式 |
|---|---|
| 真实 webhook URL | 替换为 `<YOUR_WEBHOOK_TOKEN>` 占位符 |
| 私有 API endpoint | 替换为公开的 Anthropic endpoint |
| 私有模型名 | 替换为环境变量 `LLM_MODEL`（默认 Claude Sonnet） |
| 真实用户路径 | 替换为 `${HOME}` |
| 用户名（13 处） | 替换为"用户"或删除 |
| Cron ID（4 个） | 删除 |
| 飞书 user_id | 删除 |

## 保留内容

- 公开 RSS / API URL（所有数据源都是公开接口）
- 通用关键词库（财经 / AI / 房产 / 政策 / 大模型公司）
- 公开算法逻辑（流量分、截断、匹配）
- 禁用词清单（公开规范）

## 用户首次部署

1. 配置 `ANTHROPIC_AUTH_TOKEN` 环境变量
2. 编辑 `notify_feishu.js` 第 32 行填入飞书 webhook URL（你自己的）
3. 配置 cron 任务（参考 SKILL.md 第 6 节）
4. 运行 `bash run_daily.sh` 验证

## License

MIT

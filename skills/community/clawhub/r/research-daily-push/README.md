# 科研文献每日推送技能

## 功能

每天自动检索指定领域最新 arXiv 论文，生成结构化总结并推送。

## 安装

技能已放置在 `skills/research-daily-push/`，OpenClaw 会自动加载。

## 使用方式

### 手动触发

对 智能体 说：

```
帮我推送今日最新文献
设置文献早报
监控 RTHS 领域论文
推送单细胞转录组最新论文
```

### 定时任务

设置每天早上 8:00 自动推送：

```bash
openclaw cron add --name "daily-paper-push" --cron "0 8 * * *" --message "推送今日最新文献"
```

## 配置

### 环境变量（可选）

| 变量 | 说明 |
|------|------|
| `ARXIV_API_KEY` | arXiv API Key（免费使用可不设置） |
| `PUSH_CHANNEL` | 推送渠道（feishu/wechat/email） |
| `PUSH_TARGET` | 推送目标（用户 ID 或邮箱） |

### 依赖

- Python 3.x
- `requests` 库

## 输出示例

```
📚 今日 structural vibration control 文献早报（2026-04-03）

📊 论文列表

| 标题 | 作者 | 相关性 | 链接 |
|------|------|--------|------|
| 1. Deep Learning for RTHS... | Zhang et al. | ⭐⭐⭐⭐⭐ | [PDF] |

📖 详细总结

1. Deep Learning for RTHS Delay Compensation

作者：Zhang, Y., Li, J., et al.
相关性：⭐⭐⭐⭐⭐ (9/10)
发表：2026-04-02

核心内容：
This paper proposes a LSTM-based delay compensation method...

建议：⭐ 值得精读，高度相关

---

📌 推荐阅读 Top 3

1. **Deep Learning for RTHS...** - 高度相关，创新性强

---
总计筛选：5 篇 | 推荐阅读：Top 3 | 生成时间：08:00
```

## 注意事项

1. 所有事实来自检索结果，不编造数据
2. 优先高 IF 期刊/高引用预印本
3. 用户可随时调整关键词
4. 每次推送不超过 10 篇

## 版本

v1.0.0 (2026-04-03) - 初始版本

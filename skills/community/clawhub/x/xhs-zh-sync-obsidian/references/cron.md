# 定时任务

本技能只生成 OpenClaw cron 配置，不直接修改用户调度器。

生成配置：

```bash
python scripts/install_cron.py --platform xhs --time 06:00 --timezone Asia/Shanghai --print
python scripts/install_cron.py --platform zhihu --time 05:00 --timezone Asia/Shanghai --print
```

生成的 JSON 可以交给 OpenClaw cron 添加。定时任务会运行：

```bash
python scripts/sync.py --platform <platform>
python scripts/export_obsidian.py --platform <platform> --incremental
```

推荐默认值：

- 知乎：05:00
- 小红书：06:00
- 超时：3600 秒
- 发送模式：默认静默；只有用户要求摘要或失败提醒时再开启通知

如果用户想指定 cron 模型，在 OpenClaw cron payload 层配置，不写死在技能里。

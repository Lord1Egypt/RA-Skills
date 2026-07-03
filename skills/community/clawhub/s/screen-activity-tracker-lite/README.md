# 📸 Screen Activity Tracker Lite

> 一个命令，零配置，AI 自动记录你的屏幕时光。

不需要设置，不需要思源笔记，不需要交互式向导。装上就能用——像行车记录仪，不过是记录你的数字生活。

## ⚡ 和完整版的区别

| | Lite 极简版 | 完整版 |
|---|---|---|
| 能直接跑 | ✅ 零配置开箱即用 | ❌ 需要 setup.py |
| 存储 | 本地 Markdown | 本地 + 思源笔记双后端 |
| 分析 | AI 看图说话 | 4 种分析模式 + 自定义 prompt |
| 隐私 | 全都截 | 闲置检测 + 应用黑名单 |
| 适合谁 | 想快速上手的 | 重度效率控 |
| 配置项 | 4 个 | 10+ 个 |

## 🎯 几个有趣用法

```
👤 你：今天屏幕活动总结
🤖 AI：你用了 6 小时，VS Code 3h，Safari 1h，微信 30m...
    生产力评分 7.5，顺便你下午 3 点摸鱼刷了半小时 YouTube

👤 你：搜索 Figma
🤖 AI：最近一次是 6 月 28 日下午，你在改首页的按钮颜色
    再之前是 6 月 20 日，画了新功能原型

👤 你：我上周三在做什么
🤖 AI：给你找出来了——
    09:30 VS Code 写自动化脚本
    10:15 Safari 查文档
    ...你助理真贴心吧 😏
```

## 🚀 30 秒启动

```bash
npm install -g @steipete/peekaboo
openclaw skills install /path/to/screen-activity-tracker-lite
```

然后对 OpenClaw 说：「**开始追踪屏幕**」。完成。  

之后每 5 分钟自动截图、AI 分析、记录到 `~/screen-activity/`。

## 🗣️ 对话指令

| 说 | 做 |
|---|-----|
| 「开始追踪屏幕」 | 🔴 开始录制 |
| 「停止追踪屏幕」 | ⏸ 暂停 |
| 「今天屏幕活动总结」 | 📊 查看今日报告 |
| 「搜索 Blender」 | 🔍 查历史 |

## ⚙️ 想改配置？

编辑 `config.json`（不编辑也行，默认值管够）：

```json
{
  "output_dir": "~/screen-activity",
  "mlx_url": "http://192.168.1.198:18000/v1",
  "interval_minutes": 5,
  "keep_days": 7
}
```

## 📂 文件结构

```
~/screen-activity/
├── 2026-06-30.md          ← 今天的 AI 日记
└── screenshots/            ← AI 帮你拍的照片
```

## 🛠️ 需要什么

- macOS
- Python 3
- peekaboo
- 一个能看图的 AI 模型

## 📄 License

MIT

## 🔗 链接

- GitHub: https://github.com/zeject/screen-activity-tracker-lite
- ClawHub: https://clawhub.ai/zeject/screen-activity-tracker-lite
- 完整版: https://github.com/zeject/screen-activity-tracker

---

*「我昨天下午到底在干嘛来着？」——不用猜，问你的 AI。*

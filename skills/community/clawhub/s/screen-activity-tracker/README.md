# 🦞 Screen Activity Tracker

> 你的屏幕时间线，由 AI 自动记录。像 Git 一样追踪你的数字生活。

还记得上周三下午你在做什么吗？可能忘了。但这个工具不会——它默默截图、AI 分析、自动归档，让你随时穿越回过去的任意一个 5 分钟。

## 💡 能做什么

| 你问 AI | AI 回答 |
|---------|---------|
| 「今天是怎么过的」 | 「上午写了 3 小时代码，中午刷了会儿推，下午开了 2 个会……」 |
| 「我上周用 Figma 做了什么」 | 「上周二 14:30 在改首页原型，周四 10:15 在调组件颜色」 |
| 「什么时候开始写这个项目的」 | 「6 月 22 日 09:30，你在 VS Code 打开了 screen-activity.sh」 |
| 「算一下我这周的工作效率」 | 「本周有效工作 28 小时，Blender 占比 15%，Safari 占比 12%……生产力评分 7.5」 |
| 「帮我找一张昨天的截图」 | 直接打开对应时间的截图文件 |
| 「我在 VS Code 上花了多少时间」 | 「过去 7 天累计 15 小时，单日最高 3.5 小时」 |

## 🎮 像游戏成就系统一样追踪自己

- 🏆 **自动打卡**：每 5 分钟截图一次，像 Apple Watch 一样记录你的数字动线
- 🧠 **AI 读图**：多模态模型看图说话，自动总结「你正在 VS Code 写 Python」
- 📊 **每日回顾**：每天结束时 AI 给你一份「今天去哪儿了」的报告
- 🔍 **时间旅行**：搜索「Figma」就能找回三周前的设计瞬间
- 🔒 **隐私优先**：银行/支付应用自动跳过不截图，闲置时自动暂停
- 🗑️ **自动清理**：截图 7 天后自动删除，不占硬盘

## 🚀 3 分钟开始

```bash
# 1. 安装截图工具
npm install -g @steipete/peekaboo

# 2. 安装 skill
openclaw skills install /path/to/screen-activity-tracker

# 3. 配置（向导式，一路回车即可）
python3 setup.py

# 4. 对 OpenClaw 说
开始追踪屏幕
```

搞定。之后每 5 分钟自动记录，你什么都不用管。

## 🗣️ 常用对话

| 对话 | 触发功能 |
|------|---------|
| 「开始追踪屏幕」 | 创建定时截图任务 |
| 「停止追踪屏幕」 | 暂停记录 |
| 「今天屏幕活动总结」 | 当天时间线 + 应用统计 |
| 「这周我都在干嘛」 | 周度生产力报告 |
| 「搜索 Blender」 | 查找某应用的历史记录 |
| 「我上次打开 Xcode 是什么时候」 | 精确时间点查询 |

## 🔧 深度玩法

### 分析模式

在 `config.json` 中切换，适合不同需求：

| 模式 | 适合谁 | 输出示例 |
|------|-------|---------|
| `simple` | 大多数人 | `[Safari] 浏览 OpenClaw 文档` |
| `category` | 想分类的 | `[work] VS Code 编码 / [娱乐] 看视频` |
| `productivity` | 效率狂魔 | `[7/10] VS Code - 写新功能测试` |
| `custom` | 自定义 | 自己写 prompt，想分析什么都行 |

### 双后端选择

- **本地模式**：纯 Markdown，隐私满分，所有数据都在你电脑上
- **思源笔记模式**：自动创建每日「操作记录」+「截图存档」两个文档，截图嵌入可点击查看

### 隐私黑名单

```
「支付宝/银行/密码管理器」→ 自动跳过不截图
（但时间线仍会记录「此时在使用金融应用」）
```

闲置时自动暂停，你上厕所、喝水、锁屏都不被记录。

## 📂 输出长这样

```
~/screen-activity/
├── 2026-06-30.md              ← 今天的数字日记
├── 2026-06-29.md
└── screenshots/
    └── 2026-06-30/
        ├── 09:30:00.png       ← AI 帮你拍的时光快照
        ├── 09:35:00.png
        └── ...
```

日志文件内是带截图链接的时间线，每天一条：

```markdown
## 2026-06-30 屏幕活动

- **09:30** VS Code 编辑 screen-activity.sh
  ![](screenshots/2026-06-30/093000.png)
- **09:35** Safari 查看 GitHub Issues
  ![](screenshots/2026-06-30/093500.png)
```

## 🛠️ 系统要求

- macOS + 屏幕录制权限
- Python 3.x
- peekaboo CLI
- 一个兼容 OpenAI API 的视觉模型（Qwen3.5-9B / GPT-4V 等）

## ❓ 常见问题

<details>
<summary>截图失败怎么办？</summary>
系统设置 → 隐私与安全性 → 屏幕录制 → 勾选 OpenClaw 所在的终端应用
</details>

<details>
<summary>AI 分析失败？</summary>
检查 MLX 服务是否在线：`curl http://your-mlx-server:18000/v1/models`
</details>

<details>
<summary>想改成 10 分钟截图一次？</summary>
改 `config.json` 里的 `interval_minutes`，或者直接问 AI：「把截图间隔改成 10 分钟」
</details>

<details>
<summary>数据存在哪，安全吗？</summary>
默认 `~/screen-activity/`，纯本地文件，不联网不传云端。
</details>

## 📄 License

MIT

## 🔗 链接

- GitHub: https://github.com/zeject/screen-activity-tracker
- ClawHub: https://clawhub.ai/zeject/screen-activity-tracker
- 极简版: https://github.com/zeject/screen-activity-tracker-lite

---

*「时间是怎么被偷走的？」——让 AI 帮你计时。*

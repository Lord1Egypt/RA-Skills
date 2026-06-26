# ZeeLin AI Twitter Creator Briefing Skill

完整的AI博主信息简报生成与发布系统。

## 快速开始

### 一键执行完整流程

```bash
cd ~/.openclaw/workspace/skills/zeelin-x-creator-briefing
./scripts/run-briefing.sh
```

### 使用OpenClaw命令

```bash
# 执行完整流程
openclaw skill run zeelin-x-creator-briefing \
  --config config/creators.yaml \
  --days 10 \
  --publish true
```

## 功能特性

✅ **自动抓取**: 抓取18位AI博主近10天推文
✅ **智能过滤**: 去重、清洗、评分
✅ **结构化简报**: 生成Markdown格式简报
✅ **自动发布**: 提炼英文推文并发布到X
✅ **归档管理**: 按日期归档所有简报

## 博主列表

### 英文顶级博主
- @AndrewYNg - 吴恩达
- @drfeifei - 李飞飞
- @karpathy - Andrej Karpathy
- @ylecun - Yann LeCun

### 中文AI博主
- @zarazhangrui - 张咋啦
- @dotey - 宝玉
- @op7418 - Orange
- @ShunyuYao12 - 姚顺雨
- @frxiaobei - 凡人小北
- @FinanceYF5 - AI WILL
- @MANISH1027512 - 古一
- @joshesye - 行者AI视频
- @zstmfhy - AI奶爸
- @bozhou_ai - 泊舟
- @CuiMao - 崔毛
- @RookieRicardoR - 耳朵
- @wlzh - M.
- @cnyzgkc - 木马人

## 定时任务

### 每日简报（每天早上8点）

```bash
openclaw cron add "AI Creator Briefing" "0 8 * * * cd ~/.openclaw/workspace/skills/zeelin-x-creator-briefing && ./scripts/run-briefing.sh"
```

### 每周简报（每周一早上9点）

```bash
openclaw cron add "AI Creator Weekly" "0 9 * * 1 cd ~/.openclaw/workspace/skills/zeelin-x-creator-briefing && ./scripts/run-briefing.sh --days 7 --report-type weekly"
```

## 输出示例

### Markdown简报

```
# X AI Creator Briefing - 2026-03-27

## 🔥 高信号主线

### 1. Vibe Coding到真实部署的DevOps落差
**来源**: @karpathy
**核心观点**: ...
```

### 英文推文

```
📊 AI Creator Briefing - 2026-03-27

Top Updates:
1. @karpathy: Vibe coding → DevOps gap
2. @zarazhangrui: Product ideas from play
3. @dotey: OpenAI product shifts

🔗 Full briefing: [链接]

#AI #OpenClaw #Agent
```

## 高级功能

### 自定义博主列表

```bash
openclaw skill run zeelin-x-creator-briefing \
  --creators karpathy,zarazhangrui,dotey \
  --days 7
```

### 生成中文长文

```bash
openclaw task generate-article \
  --input reports/x-creator-briefing-2026-03-27.md \
  --style media-report
```

### 发布到多平台

```bash
openclaw skill run zeelin-x-creator-briefing \
  --publish-to twitter,xiaohongshu,zhihu
```

## 文件结构

```
zeelin-x-creator-briefing/
├── SKILL.md                    # 详细文档
├── README.md                   # 本文件
├── config/
│   └── creators.yaml           # 博主配置
├── templates/
│   ├── briefing-template.md    # 简报模板
│   └── tweet-template.txt      # 推文模板
├── scripts/
│   └── run-briefing.sh         # 执行脚本
├── reports/                    # 简报输出
└── archive/                    # 归档目录
```

## 注意事项

⚠️ **账号安全**: 控制抓取频率，避免触发限流
⚠️ **内容质量**: 定期检查过滤规则，优化质量
⚠️ **性能优化**: 使用增量抓取，缓存博主信息

## 依赖技能

- agent-browser: 浏览器自动化
- zeelin-twitter-web-autopost: Twitter发布
- zeelin-writing: 文章生成

## 技术支持

- 问题反馈: OpenClaw Discord社区
- 功能建议: 欢迎提交Issue
- 贡献代码: 欢迎提交PR

---

*版本: 1.0.0 | 创建时间: 2026-03-27*

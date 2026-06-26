# Smart Report Generator | 智能报告生成器

**AI 自动生成日报/周报/月报，支持飞书/企业微信/钉钉/Slack 多平台推送**

## 🎯 适用场景

- 员工每天花 30 分钟写日报
- 管理者需要团队周报汇总
- 项目进度自动更新
- 定时推送到 IM 平台

## 📦 包含内容

1. **日报生成器** - 根据任务自动生成
2. **周报/月报汇总** - 多人数据聚合
3. **多平台推送** - 飞书/企微/钉钉/Slack
4. **模板定制** - 自定义报告格式

## 🚀 快速开始

### 安装
```bash
pip install openclaw lark
```

### 配置
```yaml
# config.yaml
platform: feishu
webhook: https://open.feishu.cn/open-apis/bot/v2/hook/xxx
schedule: "18:00"  # 每天下午 6 点推送
template: |
  ## 📅 {date} 日报
  ### ✅ 今日完成
  {completed_tasks}
  ### 📋 明日计划
  {planned_tasks}
  ### 🚧 阻塞问题
  {blockers}
```

### 运行
```bash
python report_bot.py --config config.yaml
```

## 💰 定价

| 版本 | 价格 | 功能 |
|------|------|------|
| 个人版 | ¥29 | 日报生成 + 本地存储 |
| 团队版 | ¥99 | 多人汇总 + 多平台推送 |
| 企业版 | ¥299 | 私有部署 + 自定义模板 |

## 🔧 技术支持

- 微信：OpenClawCN
- Discord：https://discord.gg/clawd

---

**作者**：OpenClaw 中文社区
**版本**：1.0.0
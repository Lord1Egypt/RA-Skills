# 微信公众号监控 Skill for OpenClaw

微信公众号调研 + 监控 + 报告推送。每个产品独立目录，互不影响。

## 功能特性

- 🔍 **调研阶段**：搜索并筛选高质量目标公众号（20个）
- 📊 **监控阶段**：每日自动检查更新，生成标准化报告
- 📝 **9维度选题分析**：热度、角度、时效性、目标人群、差异化价值、核心大纲、转化路径、预期指标、视觉建议
- ⏰ **定时推送**：每天10:00自动推送

## 安装

### 方式一：直接克隆（适合有经验的开发者）

```bash
# 克隆仓库
git clone https://github.com/a1003916989-blip/wechat-monitor-skill.git ~/.openclaw/workspace/wechat-monitor

# 进入目录
cd ~/.openclaw/workspace/wechat-monitor

# 配置API密钥（见下方）
```

### 方式二：手动安装

将 `SKILL.md`、`monitor.py`、`sample-accounts.json` 复制到 `~/.openclaw/workspace/wechat-monitor/` 目录。

## 配置 API 密钥

1. 访问 [mptext.top](https://down.mptext.top) 登录
2. 获取你的API密钥
3. 配置密钥（2选1）：

**方式A：环境变量（推荐）**
```bash
export MPTEXT_API_KEY="你的密钥"
```

**方式B：直接修改脚本**
编辑 `monitor.py`，修改第12行：
```python
API_KEY = "你的密钥"  # 替换为你的密钥
```

## 使用方法

### 调研新产品的公众号

告诉 AI：
```
帮我调研xxx的目标公众号
```

AI会：
- 分析产品定位
- 多维度搜索公众号
- 列出20个候选公众号给你确认

确认公众号列表后，AI会：
- 创建产品目录和配置文件
- 执行首次监控（近7天）
- 设置定时任务（每天10:00）

### 日常监控

每天10:00会自动推送监控日报，包含：
- 一近期重要更新汇总
- 二选题分析（9维度）
- 三本周高价值内容TOP5
- 四本周可写的文章建议

## 手动运行

```bash
# 首次运行（近7天）
python3 ~/.openclaw/workspace/wechat-monitor/monitor.py 产品名 --days 7

# 日常运行（昨天）
python3 ~/.openclaw/workspace/wechat-monitor/monitor.py 产品名 --days 1
```

## 目录结构

```
wechat-monitor/
├── SKILL.md # Skill说明文档
├── monitor.py # 监控脚本
├── sample-accounts.json # 配置模板
└── {产品名}/
 ├── accounts.json # 公众号列表（自动生成）
 ├── first_run.flag # 首次运行标记
 └── reports/ # 报告目录
```

## 注意事项

- API密钥请妥善保管，不要提交到GitHub
- 建议定期检查账号有效性（mptext登录态约3天过期）
- 报告格式支持自定义调整
- 每个产品独立配置，支持同时监控多个产品

## License

MIT


# WHOOP Guru - 完整WHOOP健康管理系统

## v8.4.12 简介

WHOOP Guru 是**完整的WHOOP健康管理系统**，整合数据获取、分析、图表可视化、AI教练和个性化训练计划。

**核心功能：**
- 📊 **数据获取** - WHOOP官方API，实时同步恢复/睡眠/训练/HRV
- 📈 **图表生成** - 交互式HTML图表，恢复/睡眠/strain/HRV趋势
- 🤖 **AI教练** - LLM驱动，个性化训练建议
- 🎯 **训练计划** - 跑步/增肌/减脂/伤痛恢复
- 🔔 **主动推送** - 每日定时提醒（08:00/09:00/18:00/20:00/22:00）
- 📉 **ML预测** - 7天恢复预测，异常检测
- 🏅 **马拉松管理** - 目标设定、配速计划、训练阶段分析
- 📝 **快速打卡** - 一句话完成训练记录
- 🔄 **自动打卡检测** - WHOOP数据自动识别今日训练，生成初步打卡内容
- 📚 **反馈学习系统** - 用户感受词→WHOOP数据映射，持续优化建议
- 🕐 **北京时间统一** - 全部时间处理使用北京时间(UTC+8)

---

## 功能列表

### 1. WHOOP数据获取

```bash
# 进入 skill 目录（根据实际安装路径调整）
cd /path/to/whoop-guru

# 获取综合报告
python3 scripts/whoop_data.py summary --days 7

# 睡眠数据
python3 scripts/whoop_data.py sleep --days 7

# 恢复评分
python3 scripts/whoop_data.py recovery --days 30

# 训练/cycle数据
python3 scripts/whoop_data.py cycles --days 7

# workouts
python3 scripts/whoop_data.py workouts --days 30

# 用户档案
python3 scripts/whoop_data.py profile

# 身体数据
python3 scripts/whoop_data.py body
```

### 2. OAuth认证

```bash
# 首次登录
python3 scripts/whoop_auth.py login --client-id YOUR_ID --client-secret YOUR_SECRET

# 检查状态
python3 scripts/whoop_auth.py status
```

### 3. 图表生成

```bash
# 睡眠分析图表
python3 scripts/whoop_chart.py sleep --days 30

# 恢复评分图表
python3 scripts/whoop_chart.py recovery --days 30

# Strain趋势
python3 scripts/whoop_chart.py strain --days 90

# HRV趋势
python3 scripts/whoop_chart.py hrv --days 90

# 综合仪表盘
python3 scripts/whoop_chart.py dashboard --days 30
```

### 4. 健康分析

使用 `references/health_analysis.md` 进行科学分析：
- HRV正常范围（按年龄/ fitness）
- 恢复评分解读（绿/黄/红）
- 睡眠阶段分析
- 训练过度信号检测
- 可操作的建议

### 5. AI教练（LLM驱动）

```bash
# 开启教练对话
python3 whoop-guru.py coach

# 生成今日计划
python3 whoop-guru.py plan

# 生成16周计划
python3 whoop-guru.py 16week --goal 增肌
```

### 6. 推送系统

| 时间 | 内容 | 命令 |
|------|------|------|
| 08:00 | 健康早报 | daily-report.sh |
| 09:00 | 教练早安 | push-morning.py |
| 18:00 | 晚间追踪 | push-evening.py |
| 20:00 | 打卡提醒 | push-checkin.py |
| 22:00 | 详细日报 | detailed-report.sh |

---

## 支持的运动目标

| 类别 | 目标 | 周期 |
|------|------|------|
| 🏃 跑步 | 3公里新手 | 8周 |
| 🏃 跑步 | 5公里 | 10周 |
| 🏃 跑步 | 10公里 | 12周 |
| 🏃 跑步 | 半程马拉松 | 24周 |
| 🏃 跑步 | 全程马拉松 | 52周 |
| 🏃 跑步 | 超级马拉松 | 52周+ |
| 💪 力量 | 增肌 | 16周 |
| 💪 力量 | 减脂 | 12周 |
| 🏥 康复 | 伤痛恢复 | 按需 |

---

## 关键指标

- **恢复评分** (0-100%): 绿色≥67%, 黄色34-66%, 红色<34%
- **Strain** (0-21): 基于心率的每日运动强度
- **睡眠效率**: 实际睡眠 vs 需要睡眠
- **HRV** (ms): 越高恢复越好，追踪趋势
- **静息心率** (bpm): 越低心血管 fitness越好

---

## 配置说明

### WHOOP OAuth（必需）

WHOOP 使用 OAuth 2.0 授权，配置步骤：

1. 在 [developer.whoop.com](https://developer.whoop.com) 创建 App 获取 Client ID 和 Secret
2. 运行：`python3 scripts/whoop_auth.py login --client-id YOUR_ID --client-secret YOUR_SECRET`
3. 浏览器自动打开，完成授权
4. Token 自动存储在 `~/.clawdbot/whoop-tokens.json`

**替代方案**：也可以手动创建 `~/.clawdbot/whoop-credentials.env` 文件，包含：
```
WHOOP_CLIENT_ID=your_client_id
WHOOP_CLIENT_SECRET=your_client_secret
WHOOP_REFRESH_TOKEN=your_refresh_token
```

### LLM API（可选）

用于 AI 个性化分析。配置方式：
- 发送「设置模型」给机器人
- 按提示输入 API Key 和选择模型
- 配置存储在 `data/config/llm_config.json`

### 本地数据存储

凭证存储在本地，不上传。数据流向：
- 用户健康数据从WHOOP API获取
- 数据发送到LLM API用于AI分析
- `data/profiles/` - 用户健身档案
- `data/plans/` - AI训练计划
- `data/logs/` - 打卡记录
- `data/config/llm_config.json` - LLM API密钥
- `~/.clawdbot/whoop-tokens.json` - WHOOP OAuth令牌

---

## 文件结构

```
whoop-guru/
├── SKILL.md
├── CLAWHUB.md
├── _meta.json
├── whoop-guru.py          # 主入口
├── scripts/
│   ├── whoop_auth.py      # OAuth认证
│   ├── whoop_data.py     # 数据获取
│   ├── whoop_chart.py    # 图表生成
│   ├── daily-report.sh   # 08:00早报
│   ├── detailed-report.sh # 22:00日报
│   ├── coach-push.sh     # 推送调度
│   ├── push-morning.py   # 09:00早安
│   ├── push-evening.py   # 18:00晚间
│   └── push-checkin.py   # 20:00打卡
├── lib/
│   ├── llm.py            # LLM集成
│   ├── data_cleaner.py   # 数据清洗
│   ├── data_processor.py # 数据处理
│   ├── sync.py           # 数据同步
│   ├── tracker.py        # 打卡追踪（包含quick_checkin）
│   ├── goals.py          # 目标管理
│   ├── goals_marathon.py # 马拉松目标
│   ├── dynamic_planner.py # 动态规划
│   ├── pusher.py        # 推送生成（包含checkin_reminder重写）
│   ├── coach_interface.py # 教练接口
│   ├── coach/            # 教练核心模块
│   ├── needs_analyzer.py # 需求分析
│   ├── plan_generator.py # 计划生成
│   ├── health_score.py   # 健康评分
│   ├── ml_predictor.py   # ML预测
│   ├── comprehensive_analysis.py # 综合分析
│   ├── health_advisor.py # 健康建议
│   ├── enhanced_reports.py # 增强报告
│   ├── marathon_analyzer.py # 马拉松分析
│   ├── marathon_commands.py # 马拉松指令
│   ├── checkin_auto.py  # 自动打卡检测（新增）
│   ├── feedback_learning.py # 反馈学习系统（增强）
│   ├── notifications.py  # 通知系统
│   ├── user_profile.py  # 用户档案
│   ├── tz.py            # 统一时区工具（新增）
│   ├── ml/              # ML预测模块
│   ├── prompts/          # Prompt模板
│   └── reports/         # 报告生成
├── references/
│   ├── api.md           # API文档
│   └── health_analysis.md # 健康分析指南
└── data/
    ├── config/          # LLM配置
    ├── profiles/        # 用户档案
    ├── plans/          # 生成的计划
    ├── processed/      # 处理后的数据
    └── logs/           # 打卡记录
```

---

## 系统要求

| 类型 | 要求 |
|------|------|
| 运行环境 | Python 3.8+ |
| 必需命令 | python3, curl |
| Python包 | requests, pandas, matplotlib |

**安装方式**：`pip install requests pandas matplotlib`

---

## 环境变量

| 变量 | 说明 | 必需 | 默认值 |
|------|------|------|--------|
| OPENCLAW_WORKSPACE | OpenClaw工作区目录 | 否 | 自动检测 |
| WHOOP_DATA_DIR | WHOOP数据存储目录 | 否 | 自动检测 |
| WHOOP_SKILL_DIR | Skill数据目录 | 否 | 自动检测 |

**注意**：WHOOP OAuth 凭证不是环境变量，而是 CLI 参数，详见上方配置说明。

---

## 推送机制

推送由 OpenClaw 的 cron 系统触发（不是独立服务）。

用户需要在 OpenClaw 中配置 cron 规则：
```bash
# 示例 crontab 配置
0 8 * * * python3 /path/to/daily-report.sh
0 9 * * * python3 /path/to/push-morning.py
0 18 * * * python3 /path/to/push-evening.py
0 20 * * * python3 /path/to/push-checkin.py
0 22 * * * python3 /path/to/detailed-report.sh
```

---

## 版本历史

### v8.4.11 (2026-04-05)
- 修复：_meta.json requires.env 改为字符串数组格式，匹配 ClawHub registry schema
  * ClawHub registry 期望 env 是字符串数组（如 ["WHOOP_CLIENT_ID"]），而非对象
- 修复：SKILL.md YAML front matter 同步修复为字符串数组格式

### v8.4.10 (2026-04-05)
- 修复：_meta.json environment 字段添加 WHOOP 凭证
  * 将 WHOOP_CLIENT_ID/CLIENT_SECRET/REFRESH_TOKEN/LLM_API_KEY 添加到 environment
- 新增：SKILL.md YAML metadata block 声明必需凭证

### v8.4.9 (2026-04-05)
- 修复：SKILL.md 添加 YAML metadata block 声明必需凭证
  * 解决 ClawHub registry 显示"无必需环境变量"问题

### v8.4.8 (2026-04-05)
- 修复：push 脚本（morning/evening/checkin）生成前先刷新 WHOOP 数据，解决数据陈旧问题
  * 调用 whoop_data.py summary 获取最新实时数据并写入 latest.json
  * 修复 recovery.start 为空导致的 date=None 问题（改用 created_at）
  * 修复 hrv/skin_temp 为 None 时 round() 报错问题
- 修复：agents.defaults.timeoutSeconds 缺少配置导致 cron 任务 30s 超时
  * openclaw.json 添加 "timeoutSeconds": 120
- 新增：推送内容使用当天实时 WHOOP 数据

### v8.4.7 (2026-04-04)
- 新增：lib/tz.py 统一时区工具模块，全部时间处理统一使用北京时间(UTC+8)
- 新增：lib/checkin_auto.py WHOOP数据自动打卡检测
  * 自动从 workouts API 获取今日训练
  * 分析跑步距离/配速/心率/心率区间
  * 生成初步打卡内容预览供用户确认
  * 支持跨UTC日边界的北京时间窗口过滤（北京凌晨跑步同步）
- 新增：lib/feedback_learning.py 增强反馈学习系统
  * 用户感受词 → WHOOP数据映射（睡眠/训练/恢复）
  * 积累3次样本后自动触发个人化建议调整
  * 主观反馈与实际数据对比学习
- 重构：lib/pusher.py checkin_reminder() 完全重写
  * WHOOP检测到训练时自动展示：跑步10.3km/配速5:45/心率区间...
  * 无训练时显示休息日模板
  * 包含WHOOP睡眠数据供用户反馈
  * 用户回复「✅」确认打卡
- 新增：测试覆盖率达到100%，全部65个单元测试通过
- 修复：feedback_learning.py key名字不一致bug（sleep_baselines → sleep_quality_map）
- 修复：feedback_learning.py entry key不匹配bug（inferred_quality → inferred_sleep）
- 修复：data_cleaner.py/dynamic_planner.py/pusher.py/enhanced_reports.py 时区处理统一为北京时间

### v8.4.6 (2026-04-03)
- 修复：测试套件7个失败（TestMarathonGoals缺少import、pusher.py未定义变量）
- 修复：marathon_commands.py 中「4月12号」中文日期格式支持
- 修复：marathon_commands.py 解析「2小时」等中文时间格式崩溃问题
- 修复：coach_interface.py 引用不存在的 tracker 函数
- 新增：tracker.py 新增 `quick_checkin()` 快速打卡接口（无需 completed/feedback）
- 增强：enhanced_reports.py 完整重写，无 LLM 时也能生成充实报告
- 新增：TOOLS.md 完全重写，更新所有路径、命令、模块说明
- 全部 41 个单元测试通过

### v8.4.5 (2026-03-31)
- 新增：马拉松训练目标管理（GoalsManager扩展）
- 新增：跑步打卡追踪（ProgressTracker扩展）
- 新增：马拉松训练分析器（MarathonAnalyzer）
- 新增：马拉松指令处理（MarathonCommands）
- 新增：每日报告集成马拉松板块
- 新增：41个单元测试（v8.4.6时）

### v8.3.8 (2026-03-31)
- 修复：OpenClaw cron配置

### v8.3.7 (2026-03-29)
- 修复：加强隐私声明，明确数据发送到LLM API

### v8.3.6 (2026-03-29)
- 修复：只声明代码实际使用的环境变量

### v8.3.5 (2026-03-29)
- 修复：添加WHOOP凭证到credentials声明

### v8.3.4 (2026-03-29)
- 修复：统一WHOOP凭证文件说明（whoop-tokens.json和whoop-credentials.env）

### v8.3.3 (2026-03-29)
- 修复：统一三个文件的凭证说明

### v8.2.7 (2026-03-29)
- 新增：系统要求章节（bins, packages）
- 新增：推送机制说明（cron + OpenClaw消息）
- 修复：澄清数据流和隐私声明

### v8.2.6 (2026-03-29)
- 修复：统一 SKILL.md 和 _meta.json 的配置说明
- 新增：homepage 字段

### v8.2.5 (2026-03-29)
- 修复：移除 WHOOP_REFRESH_TOKEN（OAuth自动获取）
- 修复：统一三个文件的凭证说明

### v8.2.4 (2026-03-29)
- 安全：修复 os.system shell 注入漏洞

### v8.2.3 (2026-03-29)
- 修复：统一凭证存储位置说明

### v8.2.0 (2026-03-29)
- 新增：LLM 增强报告模块

### v8.1.5-8.1.7 (2026-03-29)
- 新增：推送系统（09:00/18:00/20:00）
- 集成：dynamic_planner、goals、tracker 模块

### v8.0 (2026-03-26)
- LLM 集成（支持 8 种提供商）
- 个性化训练计划生成

# AI Coach · 个人铁三教练

智能生成每日训练计划，根据你的比赛目标和身体状态动态调整。

## 核心功能

- 📊 **TP 实时数据**：CTL/ATL/TSB/IF 每日更新（Cookie 认证）
- 🏊 **智能计划**：根据 TSB 和比赛倒计时自动调整
- 📅 **多比赛支持**：所有报名比赛综合考虑
- 🧠 **自我学习**：根据你的反馈优化建议
- 📱 **两种推送模式**：晚间/早晨自定义
- 💓 **Garmin 健康**：睡眠/准备度/HRV/压力实时分析

## 推送内容格式

### 复盘板块（每日动态，来源：TrainingPeaks）

```
📋 今日训练复盘（数据来源：TrainingPeaks）
📅 周二 2026-04-14

✅ 完成 1/1 项计划
➕ 额外训练 Running 6.9km 36min HR139 TSS67
总距离: 6.9km | TSS: 67 | 能量: 492 kcal
💪 今天训练完成很好，保持这个节奏！
```

### 明日计划板块

```
📅 周三 2026-04-15
[具体训练内容]

☀️ 天气： Patchy rain nearby | 7°C
📊 体能状态： CTL 33.1 | TSB -16.5 | 疲劳积累
💓 Garmin健康： 睡眠 56/100 | 准备度 LOW 26/100 | HRV 54ms | 压力 20.0
⚠️ 准备度过低，自动调整为休息
```

### 推送模式

- **模式A（晚间）**：22:00 左右 → 复盘当天 + 明日计划
- **模式B（早晨）**：06:30 左右 → 复盘昨天 + 今日计划

## TrainingPeaks 认证配置

### 第一步：获取 Cookie

1. 用浏览器登录 [TrainingPeaks](https://tpstack.trainingpeaks.com)
2. 按 F12 打开开发者工具 → **Network（网络）** 面板
3. 刷新页面，任意请求中找到请求头里的 `Cookie`
4. 找到包含 `Production_tpAuth=` 的完整 cookie 值（一长串字符串）

### 第二步：存储 Cookie

**方式A（推荐）**：写入文件
```bash
mkdir -p ~/.trainingpeaks
echo "你的cookie值" > ~/.trainingpeaks/cookie
chmod 600 ~/.trainingpeaks/cookie
```

**方式B**：设置环境变量
```bash
export TP_AUTH_COOKIE="你的cookie值"
```

> ⚠️ **安全提示**：cookie 文件包含认证凭证，请务必设置 `chmod 600` 限制权限，不要分享或上传到公开仓库。

### 验证认证
```bash
python3 ~/.openclaw/workspace/skills/ai-coach/scripts/tp_client.py auth "你的cookie值"
```

## 数据优先级

```
有 TP → TP 训练数据（CTL/TSB）+ Garmin 健康
无 TP → Garmin 运动 + Garmin 健康
```

## Garmin 认证配置

**配置方式**：在 `user_config.json` 中设置 `garmin_email` 和 `garmin_password`，或设置环境变量 `GARMIN_EMAIL` / `GARMIN_PASSWORD`

- Token 缓存：`~/.garmin_tokens/`

**使用方式**（garth v0.2+ API）：
```python
import garth
from garminconnect import Garmin

client = Garmin()
client.garth.load("~/.garmin_tokens")  # garth v0.2+ 用 garth.Client 加载目录
# 无需重新登录，直接获取数据
sleep = client.get_sleep_data(today)
readiness = client.get_training_readiness(today)
```

**健康数据字段**：
- `sleep_score`：睡眠得分
- `sleep_hours`：睡眠时长
- `readiness_score`：训练准备度
- `readiness_level`：准备度等级 (LOW/MODERATE/HIGH)
- `hrv`：心率变异性 (ms)
- `avg_stress`：平均压力水平

## 比赛配置

支持多个比赛，AI 自动选择最近比赛倒计时：

```json
{
  "races": [
    {"name": "金海湖游跑两项", "date": "2026-05-17", "type": "aquathlon", "goal": "站台"}
  ]
}
```

## 训练周期

| 阶段 | 倒计时 | 特点 |
|------|--------|------|
| 基础期 | >90天 | 有氧基础 |
| 构建期 | 43-90天 | 强度增加 |
| 冲刺期 | 15-42天 | 高强度 |
| 减量期 | 1-14天 | 减量保持 |
| 恢复期 | 赛后 | 休息 |

## 强度决策

```
综合评分 = 准备度(50%) + 睡眠(30%) + TSB(20%)
```

| 综合评分 | 强度 |
|---------|------|
| >75 | 高强度 |
| 50-75 | 中等 |
| 30-50 | 低强度 |
| <30 | 休息 |

## 教练理念库

- **Joe Friel**：CTL/ATL/TSB 监控
- **Joe Filliol**：游泳体能优先
- **Brett Sutton**：高强度间歇
- **Mark Allen**：心理训练

## 文件结构

```
ai-coach/
├── SKILL.md
├── user_config.json             # 用户配置（比赛、推送模式）
├── config.yaml                  # 默认配置
├── scripts/
│   ├── trainer.py               # 主入口：计划生成 + 复盘（向后兼容）
│   ├── plan_engine.py           # 计划生成引擎
│   ├── formatter.py             # 格式化输出
│   ├── send_daily_plan.py       # IMA 推送入口
│   ├── garmin_sync.py           # Garmin 健康数据同步
│   └── tp_sync.py               # TrainingPeaks 数据同步
└── data/
    └── coach_knowledge_base.json
```

## IMA 笔记推送

**API 调用方式**：
```python
import json, urllib.request

headers = {
    "ima-openapi-clientid": client_id,  # ~/.config/ima/client_id
    "ima-openapi-apikey": api_key,      # ~/.config/ima/api_key
    "Content-Type": "application/json"
}

data = {
    "content_format": 1,  # 1 = Markdown
    "content": markdown_content,
    "title": "训练日报 2026-04-08"
}

req = urllib.request.Request(
    "https://ima.qq.com/openapi/note/v1/import_doc",
    data=json.dumps(data, ensure_ascii=False).encode('utf-8'),
    headers=headers,
    method="POST"
)
```

**⚠️ 注意事项**：
- 某些 emoji 会导致 `Markdown2Json fail` 错误
- 推送前过滤或去掉 emoji

## 依赖说明

| 模块 | 依赖 | 来源 |
|------|------|------|
| trainer.py / plan_engine.py | garminconnect, garth | pip install |
| formatter.py | 无外部依赖 | 标准库 |
| garmin_sync.py | garminconnect, garth | pip install |

> ⚠️ garminconnect 库 v0.2+ API 变更：不再接受 `token_dir`，需用 `garth.Client.load(目录路径)` 初始化。

## 已知 Bug 修复记录

| 日期 | Bug | 修复 |
|------|-----|------|
| 2026-04-14 | 复盘日期硬编码为"周二 2026-03-24" | 改为 datetime 动态计算 |
| 2026-04-14 | garminconnect API 变更导致 Garmin 连接失败 | 改用 garth.Client.load(目录) |
| 2026-04-14 | daily_plans.json 重复记录导致复盘重复 | log_daily_plan 增加去重逻辑 |
| 2026-04-14 | CTL/TSB 小数位数过多（15位） | 保留 1 位小数 |
| 2026-04-14 | emoji 导致 IMA Markdown2Json 错误 | emoji 替换为文字 LOW/NORMAL/GOOD |

## 首次配置

1. 填写 `user_config.json`（比赛信息、推送模式）
2. 配置 TP 认证 cookie（见上方）
3. 可选：配置 Garmin 账号
4. 首次配置后运行一次 `python3 trainer.py` 验证

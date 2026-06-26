# 每日晚安总结 - Cron 任务配置

> **任务名称：** 每日晚安总结 + 经验值计算  
> **触发时间：** 每天 22:00（晚安后）  
> **项目：** [[../tasks/projects/ColourfulLife-玩家系统.md]]

---

## ⏰ Cron 配置

### Cron 表达式
```
0 22 * * *
```

**含义：** 每天晚上 22:00 触发

### 时区
```
Asia/Shanghai (GMT+8)
```

---

## 🎯 任务流程

### Step 1: 触发检查（22:00）
```powershell
# 检查是否已说晚安（通过 memory/2026-MM-DD.md 判断）
# 如未说晚安，延迟到 22:30 再次检查
# 如已说晚安，立即执行
```

### Step 2: 读取当日 worklog（22:00）
```powershell
# 读取 worklog.txt
# 提取今日日期下的所有任务
# 分类：完成/进行中/待办
```

### Step 3: 计算经验值（22:01）
```powershell
# 任务完成度分（40 分）
$completedTasks = (完成的任务数)
$totalTasks = (计划任务数)
$completionRate = $completedTasks / $totalTasks
$taskScore = [Math]::Min(40, $completionRate * 35 + ($completionRate -ge 1.2 ? 5 : 0))

# FTT 一次性做对分（30 分）
$fttTasks = (一次性做对的任务数)
$fttRate = $fttTasks / $completedTasks
$fttScore = 30 * $fttRate

# 时间管理分（15 分）
$focusHours = (专注工作小时数)
$timeScore = if ($focusHours -ge 8) { 15 }
             elseif ($focusHours -ge 6) { 12 }
             elseif ($focusHours -ge 4) { 9 }
             elseif ($focusHours -ge 2) { 6 }
             else { 3 }

# 学习成长分（15 分）
$studyHours = (学习小时数)
$studyScore = if ($studyHours -ge 2) { 15 }
              elseif ($studyHours -ge 1) { 10 }
              elseif ($studyHours -gt 0) { 5 }
              else { 0 }

# 基础分合计
$baseScore = $taskScore + $fttScore + $timeScore + $studyScore

# 额外奖励
$bonusEXP = 0
if (技能升级) { $bonusEXP += 50 * 技能升级数量 }
if (项目立项) { $bonusEXP += 20 * 立项数量 }
if (项目结项) { $bonusEXP += 100 * 结项数量 }
if (HTML 报告) { $bonusEXP += 10 * 报告数量 }
if (知识库更新) { $bonusEXP += 5 * 更新次数 }

# 今日 EXP
$dailyEXP = $baseScore + $bonusEXP
```

### Step 4: 生成 HTML 日报（22:05）
```powershell
# 调用 player-exp-system 技能
# 生成 expert-review-YYYY-MM-DD-daily-EXP.html
# 包含：
#   - 今日评分表
#   - 经验值明细
#   - 等级进度
#   - 成就解锁
#   - 明日目标
```

### Step 5: 更新记录（22:10）
```powershell
# 追加到 memory/EXP-log.md
# 更新玩家等级卡片
# 同步到 worklog.txt
```

### Step 6: 发送飞书（22:15）
```powershell
# 发送经验值日报到飞书
# 包含：
#   - 今日 EXP
#   - 累计 EXP
#   - 当前等级
#   - 关键成就
```

---

## 📊 输出模板

### 飞书消息模板
```
**🎮 玩家系统 - 每日经验值报告**（2026-03-08）

---

**📊 今日评分**

**基础分（100 分）：**
- 任务完成度：35/40（完成 5/5 计划任务）
- FTT 一次性做对：27/30（FTT 率 90%）
- 时间管理：12/15（专注 6.5 小时）
- 学习成长：10/15（学习 1.5 小时）
- **小计：84/100**

**额外奖励：**
- 技能升级：+50 EXP × 2 = +100 EXP
- 项目立项：+20 EXP × 2 = +40 EXP
- HTML 报告：+10 EXP × 2 = +20 EXP
- **小计：+160 EXP**

---

**🎯 今日总计**
- **今日 EXP：84 + 160 = 244 EXP**
- **累计 EXP：244 EXP**
- **当前等级：Lv.2（初级玩家）** 🎖️
- **距离 Lv.3：257 EXP**

---

**🏆 今日成就**
- ✅ 技能大师：发布 2 个 V2.0 技能
- ✅ 项目发起人：立项 2 个新项目
- ✅ 高效产出：单日 10+ 任务完成

---

**🎯 明日目标**
- 完成微信小程序注册（P0）
- 保持 FTT≥90%
- 专注时间≥6 小时
- 学习≥1 小时

---

_晚安，明天继续升级！_ 🌙✨
```

---

## 🎁 成就系统

### 成就列表

**任务类：**
- 🏅 首战告捷：完成第一个任务（+10 EXP）
- 🏅 十日谈：连续 10 天完成任务（+50 EXP）
- 🏅 月冠军：连续 30 天完成任务（+200 EXP）
- 🏅 百日传奇：连续 100 天完成任务（+1000 EXP）

**FTT 类：**
- 🎯 一次做对：单日 FTT 100%（+30 EXP）
- 🎯 质量大师：单月 FTT≥95%（+100 EXP）
- 🎯 零缺陷：连续 7 天 FTT 100%（+200 EXP）

**效率类：**
- ⚡ 效率之王：单日完成 20+ 任务（+50 EXP）
- ⚡ 百任务：单月完成 100+ 任务（+200 EXP）
- ⚡ 千任务：累计完成 1000+ 任务（+1000 EXP）

**学习类：**
- 📚 新手学习：首次学习≥1 小时（+10 EXP）
- 📚 学习达人：累计学习 100 小时（+100 EXP）
- 📚 终身学习：累计学习 1000 小时（+1000 EXP）

**技能类：**
- 🔧 技能创造：发布第一个技能（+50 EXP）
- 🔧 技能升级：技能升级到 V2.0（+50 EXP/次）
- 🔧 技能大师：拥有 10 个技能（+200 EXP）

**项目类：**
- 🚀 项目发起：立项第一个项目（+20 EXP）
- 🚀 项目完成：结项第一个项目（+100 EXP）
- 🚀 项目专家：同时管理 5 个项目（+100 EXP）

---

## ⚠️ 注意事项

### 1. 触发时机
- 默认 22:00 触发
- 如用户未说晚安，延迟到 22:30
- 如用户明确说"跳过今日总结"，则不执行

### 2. 数据准确性
- 基于 worklog.txt 实际记录
- 用户可手动修正评分
- 阿福保留最终解释权

### 3. 等级保护
- 等级只升不降
- 请假/休息日不影响等级
- 长期不活跃（>30 天）标记为"休眠"

### 4. 成就追溯
- 新成就系统上线后，可追溯过往成就
- 符合条件的自动补发 EXP
- 记录到成就日志

---

## 🔗 创建 Cron 任务

### 命令
```bash
openclaw cron add "每日晚安总结" "0 22 * * *" "player-exp-system"
```

### 参数
- **名称：** 每日晚安总结
- **Cron 表达式：** 0 22 * * *
- **技能：** player-exp-system
- **时区：** Asia/Shanghai
- **启用：** 是

### 验证
```bash
openclaw cron list
```

---

## 📝 测试流程

### 手动触发测试
```powershell
# 1. 手动执行一次
.\player-exp-system.ps1 -Test -Date "2026-03-08"

# 2. 检查输出
# - HTML 报告生成
# - EXP 计算正确
# - 飞书消息发送

# 3. 验证数据
# - memory/EXP-log.md 追加
# - worklog.txt 更新
# - 等级卡片更新
```

---

**_最后更新：2026-03-08 21:20_**

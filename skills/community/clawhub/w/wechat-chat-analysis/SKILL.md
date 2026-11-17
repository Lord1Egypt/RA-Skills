---
name: wechat-chat-analysis
description: 微信聊天记录人格分析与恋爱助手。当用户想要分析自己与某人的聊天记录、了解双方性格、进展、问题、改进建议，或问"下一步该怎么回"时触发。使用 wechat-cli 读取本地微信聊天数据，进行结构化分析。
---

# wechat-chat-analysis

通过 wechat-cli 读取本地微信聊天记录，对两个人的关系进行人格画像、进展评估、问题诊断和回复建议。

## ⚠️ Windows 编码问题（重要）

wechat-cli/click 会因 cp1252 编码崩溃，**所有命令必须写临时文件**，不要依赖 pipe 输出：

```powershell
# ❌ 错误：pipe 获取输出会乱码/报错
wechat-cli sessions --format json   # cp1252不能encode中文

# ✅ 正确：重定向到文件
wechat-cli sessions --format json > "$env:TEMP\_sessions.json"
# 然后用 Python 读取文件：
python -c "import json; print(json.load(open(r'$env:TEMP\_sessions.json', encoding='utf-8')))"
```

## 工作流程

### 模式选择

| 模式 | 触发时机 | 导出条数 | 分析重点 |
|------|----------|----------|----------|
| **历史模式** | 用户说"分析一下和XX的聊天记录" | `--limit 500`（全量） | 人格画像、关系进展、问题诊断 |
| **实时模式** | 用户说"看下现在聊得怎么样"\/"实时分析一下"\/"现在该怎么回" \n 或 正在连续聊时切过来问 | `--limit 30`（最近一段） | 会话节奏、情绪温度、下一步策略 |
| **多人扫描** | 用户说"看看我这边谁在热聊"\/"帮我看下现在和谁在聊" | 扫 sessions 找 active | 列活跃联系人，让用户选 |

---

### Step 1: 找到联系人

**情况 A：在最近会话中**
```powershell
wechat-cli sessions --limit 50 --format json > "$env:TEMP\_sessions.json"
```
读取输出，找到目标聊天。`unread` 字段 > 0 表示此时对方刚发了消息。如果能用聊天名直接 export，跳到 Step 2。

**情况 B：不在最近会话（王萍萍等）**
先搜联系人找微信号：
```powershell
wechat-cli contacts --query "<关键词>" > "$env:TEMP\_contacts.json"
```
用 Python 解析，找到目标的 `wxid_xxx`。然后用 wxid 直接 export。

**情况 C：确认有聊天但不知道名字**
全局搜索：
```powershell
wechat-cli search "<对方名字>" --limit 10 > "$env:TEMP\_search.json"
```
确认聊天内容存在，再用 contacts 找到 wxid。

### Step 2: 导出聊天记录

**历史模式：**
```powershell
wechat-cli export "<联系人昵称或wxid>" --format markdown --limit 500 > "$env:TEMP\_export.log" 2>&1
```

**实时模式：**
```powershell
wechat-cli export "<联系人昵称或wxid>" --format markdown --limit 30 > "$env:TEMP\_realtime_export.log" 2>&1
```

**多人扫描模式（主动检测谁在热聊）：**
当用户说"看看谁在聊"或你判断需要先扫一轮时：
```powershell
$env:PYTHONIOENCODING='utf-8'
python <skills_dir>/scripts/analyze_chat.py --whoishot
```
检出有未读或最近5分钟活跃的私聊，列出来让用户选。

> **注意：** 运行 Python 脚本时一定要 `$env:PYTHONIOENCODING='utf-8'`，否则 stdout 写中文会 crash。

### 多联系人场景（同时和多人聊）

用户在微信上同时和多人聊天时，用以下方式指定分析对象：

**方法一：直接点名**
- "实时分析一下和 **王萍萍** 的" → 指定联系人，直接导出分析
- "看看 **张姐** 现在聊得怎么样" → 同上

**方法二：喊我扫（推荐 ）**
- "看看我现在和谁在聊" → 我跑 `--whoishot` 扫出活跃会话 → 列出来你选 → 再深度分析选中的
- 适合同时撩好几个、自己都分不清状态下 -> 让你一眼看清哪条线热火、哪条线该收。

两种方法的实现：
1. `--chat "名字"` → 直接分析指定人
2. `--whoishot` → 扫活跃会话列表，不分析，只告诉你现在哪些人在活跃

> **注意：** 如果上一步找到的是 wxid，直接用它 export。wechat-cli 会自动解析联系人备注名作为 display_name。

检查输出文件中"消息数量: XX"来确认成功。

### Step 3: 分析

**历史模式 - 用脚本：**
```powershell
python <skills_dir>/scripts/analyze_chat.py --chat "<昵称/wxid>" --limit 500
```
脚本输出统计报告+原文到文件。

**实时模式 - 不要跑脚本：**
直接读导出的最近消息，AI 做实时分析。因为实时模式要的**不是统计数字**，而是**会话节奏、情绪曲线、下一轮策略**，脚本的统计报告反而多余。

读消息之后按以下框架分析（见下文「实时模式分析框架」）。

### Step 4: 输出报告

#### 历史模式输出结构

```
## 一、基础数据概览
- 总消息数 / 比例 / 时间跨度 / 日均消息

## 二、双方人格画像
### 你的性格特点
### 对方性格特点
### 互动模式分析

## 三、关系进展评估
- 当前阶段判断
- 关键里程碑
- 亲密度指标

## 四、问题诊断
- 你的不足
- 对方的不足
- 互动问题

## 五、改进建议

## 六、下一步回复（3条策略）
```

---

#### 实时模式输出结构

```
## 会话状态总览
- 正在聊 / 冷场中 / 对方刚回 / 你刚回复
- 本轮持续了多久，几条消息

## 节奏分析
- 回复速度评估（秒回 / 正常 / 拖延）
- 字数趋势（增/减/持平）
- 谁在驱动话题

## 情绪温度
- 当前氛围：热 / 温 / 冷 / 卡住
- 最近的信号检测（绿灯 / 红灯 / 黄灯）
- 和之前比是升温了还是降温了

## ✨ 策略建议
- 这轮该怎么回（推荐方向）
- 节奏建议（立即回 / 晾一下）
- 具体回复参考（1-2条，嵌入当前语境）
- 如果有危险信号，预警提示
```

---

## 关键分析框架

详见 `references/analysis_framework.md`，核心维度：
- **主动性**：谁发起多？比例多少？
- **话题深度**：表层/中层/深层
- **回应质量**：秒回/敷衍/认真/删文
- **关系阶段**：陌生→认识→熟悉→暧昧→交往
- **信号判断**：对方兴趣度高/中/低

### 实时模式额外维度
- **回复速度比**：双方各消息的回复间隔
- **字数趋势**：最后一轮 vs 倒数第三轮的字数差
- **情绪曲线**：表情/语气词的频率变化
- **窗口判断**：当前时间适合什么话题（深夜/周末 vs 工作时间）
- **好停点**：这轮该继续还是收尾

## 回复建议原则

详见 `references/response_templates.md`：
- 区分进攻型/稳妥型/保守型三种策略
- 给出每条的理由和优劣
- 结合对方性格和当前阶段选策略

## 实战经验（踩坑汇总）

### 联系人在 contacts 里但不在 sessions
```
↑ 说明很久没聊了。流程：
  contacts --query → 找到 wxid → export wxid_xxx → 成功导出
```

### 导出时中文名报错
用 wxid 替代联系人昵称 export，效果一样。

### wechat-cli 输出的中文导致 cp1252 crash
**所有命令必须重定向到文件**，再从文件读取。不要用 `capture_output=True` 接 pipe，会死在 click 的 click.echo 里。

### 脚本运行必须设 PYTHONIOENCODING=utf-8
```powershell
$env:PYTHONIOENCODING='utf-8'
python analyze_chat.py --whoishot
```
否则 Python stdout 遇到中文会 cp1252 crash。

## V3 新增功能

分析脚本 `analyze_chat.py` 版本 V3 包含以下改进：

### ① 回复间隔分析

每条消息之间的回复间隔被精确计算（按时间戳排序，同一人连续发送归为同轮），输出：
- 每人平均/中位数/最快/最慢回复间隔
- 最近 10 轮节奏（⚡=1min内, 🕐=1-5min, 🐢=5min+）

### ② 公众号过滤

`--whoishot` 自动过滤：
- wxid 以 `gh_` 开头的公众号
- `brandsessionholder`, `notifymessage` 等服务号
- `@placeholder_foldgroup` 等占位会话
- 群聊

### ③ 趋势对比

每次分析自动保存快照到 `data/history.json`。第二次分析同一联系人时自动输出：
- 消息量变化（↑↓%）
- 回复间隔变化（变快/变慢）
- 天数跨度变化

### ④ 回复建议时间锚定

报告最后输出 `## ⏱ 回复建议时间上下文`，包含：
- 最后消息时间
- 平均回复间隔（每人）
- 活跃天数

AI 生成回复建议时必须基于这些时间数据，不能脱离上下文瞎猜。

### ⑤ 导出缓存

60 秒内同一联系人+limit 的导出会用缓存，免去重复调用 wechat-cli（启动快了）。

### ⑥ Python 自动检测

不再硬绑 Python 3.10。检测顺序：
1. `shutil.which("python3")`
2. `shutil.which("python")`
3. QClaw 内置 Python
4. 常用 Windows 路径（312/311/310/39/38）

### ⑦ 反馈闭环

```powershell
# 记录对某条建议的反馈
python analyze_chat.py --feedback "<建议ID>" "好/中/差"
```

数据存 `data/feedback.json`。AI 可以查历史反馈来优化建议质量。

## 数据安全

- 数据来自本地 wechat-cli
- 仅分析消息文本
- 分析在本地完成，不上传

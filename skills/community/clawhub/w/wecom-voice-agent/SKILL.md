---
name: wecom-voice-agent
version: 2.9.0
description: >
---


# 企业微信语音消息 Agent

## ⚠️ 风险声明（必读）

### 能力边界

1. **本技能支持企业微信智能机器人场景**，包括被动语音消息处理和主动语音通话
2. **语音转文字由企业微信官方提供**，本技能不自行采集或上传用户语音至任何第三方
3. **不会读取或收集**用户的通讯录、聊天记录或其他个人隐私数据
4. **所有数据处理均在本地完成**，通话记录（含 ASR 转写文本、元数据）持久化存储于本机 SQLite 数据库（`~/.wecom_voice/call_records.db`），录音文件存储于 `~/.wecom_voice/records/`，保留期限默认 90 天，到期自动清理
5. **主动外呼需管理员授权**，且仅在用户明确同意录音后进行

### 外部连接披露

本技能仅在以下场景发起外部网络连接：

| 目标主机 | 用途 | 触发条件 | 传输数据 |
|---------|------|---------|---------|
| `wttr.in` | 天气查询 API | 用户主动发起天气查询请求 | 城市名称（不含用户身份信息） |
| `openspeech.bytedance.com` | 火山引擎 TTS 语音合成（备用链路） | 仅当配置 `VOLC_TTS_KEY` 且 Edge TTS 主链路不可用 | 待合成文本（通话播报内容） |
| `api.coze.cn` / `api.minimax.chat` | 语音克隆 API（豆包 / MiniMax） | 仅当配置 `CLONE_PROVIDER` + `CLONE_API_KEY` 主动创建克隆音色 | 音色名称与授权信息（不含通话内容） |

**除上述披露外，本技能不会向任何其他外部主机发起连接**。天气查询为只读 GET 请求；火山 TTS 与语音克隆均为可选增强能力，**未配置对应 Key 时静默跳过、绝不发起连接**，全部功能降级可用。所有外部连接均不上传用户身份信息。

### 安全风险项

| 风险等级 | 风险描述 | 预防措施 |
|---------|---------|---------| 
| 🔴 高 | 语音转写准确率受环境噪音影响 | 当置信度低时主动询问用户确认 |
| 🔴 高 | 误触发（电视/背景音乐被误认为语音） | 设置消息有效时长阈值，超过30秒无新消息则重置上下文 |
| 🔴 高 | 外呼过程中的隐私泄露风险 | 全程录音告知、用户同意后才录音 |
| 🟡 中 | 企业微信 API 频率限制（每分钟20次） | 实现请求队列和速率限制器 |
| 🟡 中 | 长上下文导致 Token 消耗过大 | 自动压缩历史消息，保留最近5轮对话 |
| 🟢 低 | 语音回复合成超时并发 | 超时后自动降级为文字回复 |

### 合规声明

- 本技能遵守《个人信息保护法》《数据安全法》相关规定
- 所有操作均基于用户主动发起的对话，不主动采集数据
- 语音数据由企业微信官方处理，本技能不存储原始音频
- 用户可随时通过发送文字消息退出语音模式
- **外呼录音必须获得用户明确同意才进行**
- **所有录音文件仅存储在本机 `~/.wecom_voice/records/`，永不外传**
- **通话记录（含 ASR 转写文本、元数据）存储于本机 SQLite，不上传第三方**
- **数据保留期限：录音文件 90 天，通话记录 180 天，到期自动清理**

---

## 🚀 快速开始

### 方式一：一条命令安装并体验

```bash
# 安装技能（如果已安装则跳过此步）
skillhub install wecom-voice-agent

# 第一步：检测你的电脑配置
python D:/skill/wecom-voice-agent/scripts/detect_hardware.py

# 第二步：模拟语音消息测试
python D:/skill/wecom-voice-agent/scripts/voice_simulator.py --text "明天有什么会议"

# 第三步：试试天气查询
python D:/skill/wecom-voice-agent/scripts/voice_simulator.py --text "北京今天天气怎么样"

# 第四步：创建会话并添加消息
python D:/skill/wecom-voice-agent/scripts/session_manager.py create --userid zhangsan
python D:/skill/wecom-voice-agent/scripts/session_manager.py stats
```

### 方式二：从零手动体验

```bash
# 克隆技能目录
cd D:/skill/wecom-voice-agent

# 1. 硬件检测（纯Python标准库，无需安装任何依赖）
python scripts/detect_hardware.py

# 2. 语音消息模拟器测试
python scripts/voice_simulator.py --text "提醒我下午3点开会"

# 3. 会话管理
python scripts/session_manager.py create --userid test
python scripts/session_manager.py stats
```

### v2.8 运营工具速用

```bash
cd D:/skill/wecom-voice-agent

# 查看全部可用音色（3 套预设，来自 config/voices.yaml）
python scripts/voice_policy.py list

# 按场景+情感预览合成参数与 SSML（不发起合成）
python scripts/voice_policy.py synth --scene outbound --emotion angry --confidence 0.9 --text "您好，通知您明天下午3点参加评审。" --ssml

# 查看语音克隆模块状态（未配置 CLONE_PROVIDER/CLONE_API_KEY 时完全隐藏）
python scripts/voice_clone.py status

# 评审一段通话摘要（三要素评分，≥80 分达标）
python scripts/summary_qa.py review --text "会议决定：下周三18点前由张三负责提交修订方案。" --id call_001

# 查看最近 7 天运营摘要 / 生成上周 HTML 周报
python scripts/report_generator.py summary --period week
python scripts/report_generator.py weekly
```

> ✅ **无需安装任何 Python 包**，所有脚本仅使用 Python 标准库（`sys`、`os`、`json` 等）

---

## 二、架构（v2.9）

```
wecom-voice-agent/
├── SKILL.md                  # 本文件（使用说明 + 风险 + 边界 + FAQ + 反模式）
├── config/
│   ├── intents.yaml          # v2.6 声明式意图注册表（20+ 意图）
│   ├── custom_intents.yaml   # v2.6 自定义意图插件配置（企业 API 映射）
│   ├── menu.yaml             # v2.6 IVR 多级菜单配置
│   └── voices.yaml           # v2.8 TTS 音色库（3 套预设+情感调整+SSML+双链路）
├── references/
│   ├── wecom_bot_api.md      # 企业微信机器人 API 参考
│   └── step_by_step_setup.md # 分步部署指南
├── scripts/
│   ├── wecom_webhook_server.py # 主服务（回调接收+意图路由+任务执行+ v2.9 群消息路由@机器人触发）
│   ├── intent_registry.py    # v2.6 声明式意图引擎（YAML 配置+多级澄清）
│   ├── custom_intent_plugin.py # v2.6 自定义意图插件（企业自有 API 声明式映射）
│   ├── session_unified.py    # v2.6 统一会话管理（双向子系统；v2.9 新增群维度 chat_id 隔离+说话人身份）
│   ├── ivr_engine.py         # v2.6 多级 IVR 菜单引擎（YAML 配置+数字/名称双选）
│   ├── entity_extractor.py   # v2.6 实体抽取增强（规则+消歧+复述确认；v2.9 新增群任务三元组指派抽取）
│   ├── memory_bridge.py     # v2.7 zwjh 长期记忆桥接（MCP stdio JSON-RPC）
│   ├── todo_followup.py     # v2.7 跟进待办闭环（纪要→回拨→到期→二次外呼；v2.9 新增群任务指派+确认回执闭环）
│   ├── emotion_ticket_bridge.py # v2.7 情感到工单直连（强负面→建单+升级+通知）
│   ├── voice_policy.py      # v2.8 TTS 多音色与情感（voices.yaml+SSML+双链路降级）
│   ├── voice_clone.py       # v2.8 语音克隆外呼（授权留痕+合规红线+未配置完全隐藏）
│   ├── summary_qa.py        # v2.8 通话摘要质检（三要素评分+5%人工抽检+纠错回流）
│   ├── report_generator.py  # v2.8 运营报表（接通率/漏斗/意图分布+周一HTML周报）
│   ├── group_compliance.py  # v2.9 群场景合规默认值（record:false 磁盘零语音落盘+落盘需管理员确认+降级）
│   ├── group_e2e_test.py    # v2.9 群聊 E2E 自测（群维度/三元组/群任务闭环/群路由/身份准确率/降级）
│   ├── voice_simulator.py    # 语音消息模拟器（本地调试）
│   ├── detect_hardware.py    # 硬件检测
│   ├── state_machine.py      # 多轮对话状态机
│   ├── call_record_subsystem.py # v2.5 通话记录子系统（合并4脚本）
│   ├── voice_channel.py      # v2.5 多渠道抽象层
│   ├── voicemail_summary.py  # v2.5 语音留言摘要
│   ├── dialect_detector.py   # v2.3 方言检测
│   ├── ticket_manager.py     # v2.3 工单管理
│   ├── emotion_analyzer.py   # v2.2 情感识别
│   ├── vad_filter.py         # v2.4 VAD 语音活动检测
│   ├── priority_queue.py     # v2.4 四级优先级队列
│   ├── compliance.py         # v2.4 合规录音（v3.0 强制告知）
│   ├── scheduler.py          # v2.0 外呼调度（已合并至 session_unified）
│   ├── session_manager.py    # v2.0 会话管理（已合并至 session_unified）
│   ├── ivr_minutes.py        # v2.0 通话纪要（已合并至 call_record_subsystem）
│   ├── stats.py              # v2.0 统计看板（已合并至 call_record_subsystem）
│   └── transcriber.py        # v2.0 全文转写（已合并至 call_record_subsystem）
└── temp_sessions/             # 运行时临时目录
```

**核心数据流**：`voice.content → intent_registry（声明式匹配+置信度评分）→ entity_extractor（实体抽取+消歧）→ handler → 任务执行`，同时旁路写入 `session_unified`（统一会话）与 `call_record_subsystem`（通话记录）。

**v2.6 核心理念**：意图配置化（YAML 声明 + 置信度分级 + 多级澄清）、会话统一化（双向合并 + 状态共享）、IVR 配置化（层级菜单 + 双模式选择）、实体智能化（规则抽取 + 上下文消歧 + 复述确认）。

**v2.8 核心理念**：播报情感化（场景预设 + 情感参数叠加限幅 + SSML 停顿加重）、克隆合规化（授权留痕 + 书面授权红线 + 仅外呼场景 + 未配置完全隐藏）、摘要质量闭环（三要素评分 + 达标线 + 人工抽检 + 纠错回流驱动 Prompt 迭代）、运营可观测（接通率 + 四级漏斗 + 周一 HTML 周报）。

**v2.9 核心理念**：群聊语音化（@机器人触发群消息路由，复用单聊意图引擎零重构 + 注入说话人身份上下文）、群任务闭环化（语音指派三元组抽取「指派人/被指派人/期限」→ 自动建待办 + 确认回执 + 到期提醒复用 todo_followup）、群合规最小化（默认 record:false 磁盘零语音落盘，开启落盘需管理员确认，voices.yaml group 块可配）、会话维度隔离化（群会话以 chat_id 为维度主键，与单聊 userid 物理隔离避免上下文污染）。

| 常见坑 | 正确做法 |
|-------|---------|
| ❌ 在嘈杂环境发送语音指令 | ✅ 在安静环境说话，距离手机/麦克风 20-30cm |
| ❌ 一次说多句话（如"查日程然后帮我订会议室"） | ✅ 一次只做一件事，分开发送 |
| ❌ 发送超过60秒的语音 | ✅ 控制在 60 秒以内，长内容请打字 |
| ❌ 群聊中发语音却没 @机器人 | ✅ 群聊里 **@机器人** 后发语音/文字指令，未 @ 的消息会被静默忽略（防刷屏） |
| ❌ 发送方言（福建话、河南话等） | ✅ 支持**粤语、四川话、上海话、东北话、闽南话**，直接用方言对话即可，无需切换普通话 |
| ❌ 说话时周围有电视/音乐 | ✅ 关掉背景音再说话，会被误认为指令 |
| ❌ 以为能自动打电话/发短信 | ✅ v2.0 起支持外呼，但需管理员授权 |
| ❌ 语音内容涉及密码/银行信息 | ✅ **切勿在语音中透露敏感信息**，所有文字均经过企业微信服务器 |

---

## 角色定义

你是一名**企业微信语音智能助手**，专门处理企业微信生态内的语音交互场景。你的工作方式是：

1. **被动响应**：只处理用户主动发送的语音消息，不主动拨打/发送（v2.0 起支持主动外呼）
2. **意图理解**：将语音转写后的文本解析为结构化意图
3. **任务执行**：调用相应的能力模块完成用户请求
4. **通话管理**：支持主动外呼、来电接线、多轮对话、合规录音（v2.0 新增）
5. **友好回复**：根据用户偏好返回文字或语音消息

**你不是一个电话推销员，你是一个办公助手。**

---

## 核心指令

### 一、消息接收阶段（系统自动触发）

当企业微信回调收到 `msgtype: voice` 消息时：

```json
{
    "msgid": "CAIQrcjMjQYY/NGagIOAgAMg6PDc/w0=",
    "aibotid": "AIBOTID",
    "chattype": "single",
    "from": {"userid": "USERID"},
    "response_url": "RESPONSEURL",
    "msgtype": "voice",
    "voice": {
        "content": "这是语音转成文本的内容"
    }
}
```

**关键步骤**：

1. **提取文本内容**：从 `voice.content` 字段获取转写后的文本
2. **验证消息有效性**：检查 `msgid` 是否重复（排重），检查消息时效性（超过5分钟则忽略）
3. **上下文管理**：根据 `msgid` 查找或创建会话上下文

### 二、意图解析阶段

将用户语音文本分类为以下意图类型：

| 意图类型 | 触发关键词 | 处理方式 |
|---------|-----------|---------|
| `query_schedule` | 日程、会议、安排、行程、下周、下周有什么 | 调用企业微信日程 skill |
| `create_todo` | 提醒、待办、任务、别忘了、记得、设提醒 | 调用企业微信待办 skill |
| `query_weather` | 天气、气温、下雨、温度、穿什么、热不冷 | 调用天气查询模块 |
| `send_message` | 发消息、告诉、通知、转发、给XX发 | 调用企业微信消息 skill |
| `help` | 帮助、能做什么、怎么用、功能、你可以做什么 | 返回帮助信息 |
| `exit_voice` | 退出、不用了、谢谢、结束、再见、拜拜 | 切换到文字模式 |
| `custom` | 无法识别的意图 | 尝试通用问答或请求澄清 |

**增强版意图解析逻辑**：

```
步骤1: 精确匹配关键词 → 确定意图类型（多个关键词可叠加分数）
步骤2: 提取时间/地点/人物等实体信息（支持"下周"、"后天"、"明天上午9点"）
步骤3: 生成结构化 intent JSON（含置信度评分）
步骤4: 置信度 > 0.3 → 调用对应处理模块；置信度 ≤ 0.3 → 主动询问用户想做什么
```

**提升识别准确率的提示**：

当遇到以下模糊表达时，先确认而非猜测：

| 用户说 | 不确定的点 | 确认方式 |
|--------|----------|---------|
| "帮我安排一下" | 是查日程还是建待办？ | "您是想查看已有安排，还是需要创建新的提醒？" |
| "下周开会" | 是哪天？ | "您是指下周一到周五的哪天呢？" |
| "张三" | 有多个同名吗？ | "找到2位张三，请确认是哪个部门的" |
| "明天上午" | 几点？ | "好的，明天上午几点呢？" |
| "发给他" | 发给谁？上下文没有人物 | "请问要发给谁？" |

### 三、任务执行阶段

#### 3.1 日程查询 (`query_schedule`)

**输入格式**：
```json
{
    "intent": "query_schedule",
    "entities": {
        "time": "明天",
        "date": "2024-01-15",
        "person": "张三"
    }
}
```

**执行步骤**：
1. 解析时间实体（今天/明天/后天/下周三、下周一、下周等）
2. 调用企业微信日程 API 查询指定日期安排
3. 整理日程信息（时间-事项-地点）
4. 格式化为自然语言回复

**输出示例**：
```
您明天（1月15日）的日程安排：
📅 09:00-10:00 周会 - 会议室A
📅 14:00-15:00 与张三讨论项目 - 线上会议
📅 16:30-17:00 代码评审 - 开发区
共 3 项安排。需要我设置提醒吗？
```

#### 3.2 待办创建 (`create_todo`)

**执行步骤**：
1. 解析待办内容、截止时间、提醒时间
2. 调用企业微信待办 API 创建任务
3. 返回创建结果

#### 3.3 天气查询 (`query_weather`)

**执行步骤**：
1. 解析地点实体（默认用户所在城市）
2. 调用天气查询服务（wttr.in 免费 API）
3. 整理天气信息并语音播报

#### 3.4 消息发送 (`send_message`)

**执行步骤**：
1. 解析接收人、消息内容
2. **确认发送意图**（防止误触，发送前让用户确认）
3. 调用企业微信消息 API 发送

### 四、v2.0 新增：主动通话管理

#### 4.1 主动外呼

**触发条件**：用户/系统发起外呼任务

**执行流程**：
1. 获取被叫方信息（手机号或用户ID）
2. 调用企业微信「语音通话」API 发起呼叫
3. 接通后播放录音告知（"本次通话可能被录音"）
4. 用户同意 → 开始正式通话 + 录音
5. 用户拒绝 → 继续通话但不录音
6. 通话结束 → 自动生成纪要 + 保存录音 + 发送纪要

#### 4.2 来电自动接线（IVR 替代）

**触发条件**：用户拨打企业绑定电话

**执行流程**：
1. 企微电话接通回调触发
2. Agent 播放欢迎语 + 录音告知
3. 等待用户语音输入（ASR 转写）
4. 意图识别 → 执行对应任务
5. 多轮对话状态机管理交互
6. 30 秒无新语音自动结束通话

#### 4.3 通话后自动纪要

**触发条件**：通话结束

**执行流程**：
1. 从 ASR 文字流提取「决策点」「待办项」「时间点」
2. 输出结构化纪要（markdown 格式）
3. 通过企微消息 API 发送给呼叫方

#### 4.4 多轮语音对话状态机

**状态定义**：
- `IDLE` → 空闲/未开始
- `DIALING` → 拨号中
- `SPEAKING` → Agent 说话中（TTS 播报）
- `LISTENING` → 等待用户语音输入
- `CONFIRMING` → 二次确认中（ASR 置信度低）
- `ENDING` → 通话结束中

**超时机制**：30 秒无新语音自动结束通话

#### 4.5 合规录音告知 + 本地存储

**执行流程**：
1. 通话开始时播放「本次通话可能被录音，用于服务品质监控。请问您是否同意？」
2. 用户回应「同意」→ 开始录音
3. 录音文件存储到本机 `~/.wecom_voice/records/YYYY-MM-DD/`
4. 录音记录存本地 SQLite
5. **不上传任何第三方**

#### 4.6 外呼任务调度

**功能**：
- 定时外呼（每天9点提醒）
- 批量外呼（CSV/JSON 导入客户列表）

**实现方式**：
- 使用 `sched` + `threading` 实现定时调度
- CSV/JSON 批量导入客户列表
- 并发控制（默认最大 3 路并发）

### 五、回复生成阶段

#### 5.1 文字回复

当用户发送的语音消息内容较简单，或用户明确表示"用文字回复我"时：

```
回复格式要求：
- 简洁明了，每段不超过3行
- 使用 emoji 增强可读性
- 包含下一步操作建议
```

#### 5.2 语音回复

当用户明确表示"用语音告诉我"，或回复内容较长（超过100字）时：

**语音合成流程**：
1. 调用本地 TTS 引擎生成语音文件
2. 上传至企业微信获取 media_id
3. 通过 response_url 发送语音消息

**TTS 引擎选择优先级**：
```
优先级1: Edge TTS（免费，无需 API Key，中文效果良好）
优先级2: 火山引擎 TTS（音色更自然，需配置 API Key）
```

### 六、多轮对话管理

> ⚠️ **重要说明**：v2.0 起提供**完整的通话状态机**（`state_machine.py`），
> 支持多轮语音对话的上下文管理和超时自动结束。

**上下文保持规则**：
- 同一用户（同一 `msgid` 前缀）连续消息视为一轮对话
- 单轮对话最多保留 **5 条消息**（3条用户 + 2条助手）
- 超过5条后自动压缩：保留第一条用户消息 + 最近2条消息
- **对话超时**：用户连续 30 秒（通话模式）/ 60 秒（文字模式）无新消息则自动结束上下文

**上下文数据结构**：
```json
{
    "session_id": "userid_timestamp",
    "messages": [...],
    "current_intent": "query_schedule",
    "collected_entities": {"time": "明天"},
    "awaiting": "date",
    "created_at": 1705286400
}
```

---

## 硬件自适应优化

### 自动检测与分级

本技能启动时自动检测用户计算机系统资源，并根据结果调整并发和缓存策略：

| 硬件等级 | RAM 范围 | CPU 核心数 | 并发处理能力 | 上下文缓存 |
|---------|---------|-----------|------------|-----------|
| 🟢 高配 | ≥ 16GB | ≥ 8核 | 同时处理 5 路会话 | 保留 100 轮历史 |
| 🟡 中配 | 8-16GB | 4-8核 | 同时处理 3 路会话 | 保留 20 轮历史 |
| 🔴 低配 | < 8GB | < 4核 | 同时处理 1 路会话 | 保留 5 轮历史 |

**检测方式**：
- WorkBuddy 环境：读取系统信息和 Node.js `os` 模块
- 独立脚本：使用 Windows API (`GlobalMemoryStatusEx`) 获取真实硬件参数

### 性能保障措施

1. **懒加载机制**：非核心模块在首次使用时才加载
2. **资源回收**：对话结束后立即释放占用的内存和临时文件
3. **超时保护**：语音转写受网络影响，超时后自动提示用户重试
4. **日志限制**：本地日志文件最大 100KB，自动轮转覆盖

---

## 更新通知机制

### 版本检查

本技能在每次执行时（频率限制为每6小时一次）执行以下检查：

1. 本地安装版本号 vs 云端最新版本号
2. 如有新版本，向用户发送更新提醒消息

**提醒格式**：
```
🎉 发现新版本：v2.0.0
主要改进：
- 新增主动外呼、来电接线、通话纪要
- 新增合规录音告知、外呼任务调度
- 新增通话记录看板、全文转写

请运行以下命令更新：
skillhub install wecom-voice-agent --force
```

### 自动更新（可选）

用户可通过发送"检查更新"触发版本检查，或通过以下命令手动更新：

```bash
skillhub install wecom-voice-agent --force
```

---

## 示例场景

### 场景1：语音查日程

**用户（语音）**：明天有什么会议？

**企业微信回调**：
```json
{
    "msgtype": "voice",
    "voice": {"content": "明天有什么会议"}
}
```

**助手回复**：
```
您明天（7月9日）的日程安排：

📅 09:00-10:00 产品周会 - 大会议室
📅 14:00-15:30 客户拜访 - 上海浦东
📅 16:00-17:00 团队代码评审

共 3 项。需要我设置提前30分钟提醒吗？
```

### 场景2：语音建待办

**用户（语音）**：提醒我下午3点提交报告

**助手回复**：
```
✅ 已创建待办提醒：
⏰ 时间：今天下午3:00
📝 内容：提交报告

需要我同时在团队群里发一条提醒吗？
```

### 场景3：连续对话

**用户（语音）**：今天天气怎么样？
**助手回复**：
```
北京今日天气：
🌤️ 多云  28°C ~ 35°C
💡 建议：带伞，可能有阵雨
🌬️ 东南风 3级
```

**用户（语音）（追问）**：**那明天呢？**

**助手回复**（利用上下文，知道地点仍然是北京）：
```
北京明天天气：
🌧️ 小雨  24°C ~ 30°C
💡 建议：带伞，穿薄外套

看起来明天要下雨，需要我帮您调整明天的外出安排吗？
```

### 场景4：模糊表达处理

**用户（语音）**：帮我安排一下

**助手回复**（主动确认，不猜测）：

```
我可以帮您：
1️⃣ 查看日程安排（您想查哪天？）
2️⃣ 创建待办提醒（提醒什么内容？）
3️⃣ 查询天气（哪个城市？）

请告诉我您想做什么。
```

### 场景5：误触发处理

**用户（语音）**：（环境噪音 / 电视声音）

**助手回复**：
```
抱歉，我没有听清楚您的语音内容 😅

请用清晰的语音告诉我您需要什么帮助，例如：
• "查一下明天的日程"
• "提醒我下午开会"
• "发消息给张三"
```

### 场景6：v2.0 主动外呼

**系统**：发起外呼任务 → 拨打 13800138000

**Agent**（接通后）：
```
您好，我是XX公司的语音助手。本次通话可能被录音，用于服务品质监控。请问您是否同意？
```

**用户**：同意

**Agent**：
```
好的，感谢您的确认。我们想确认一下，您明天下午3点的会议安排是否有变化？
```

**用户**：没有变化，按时参加

**Agent**：
```
好的，已为您确认。通话结束后我们会发送纪要至您的企业微信。祝您愉快！
```

### 场景7：v2.0 来电接线

**用户**：拨打企业绑定电话

**Agent**：
```
您好，欢迎致电XX公司。我是智能语音助手，请问您需要什么帮助？
```

**用户**：我要退订

**Agent**（二次确认，ASR 置信度 0.7 < 0.85）：
```
抱歉，我没有完全听清。您说的是「我要退订」吗？请确认「是」或「不是」。
```

**用户**：是

**Agent**：
```
好的，已为您提交退订申请。受理编号：TK20260715001。我们会在3个工作日内处理。还有其他需要帮助的吗？
```

### 场景8：v2.9 群聊 @机器人 语音指派任务

**前提**：群内已 @机器人，张三、李四、机器人同处一个群。

**用户（语音，@机器人）**：@李四 周五前把季度汇报PPT发我

**机器人处理**：
1. 群路由判定 `@李四` 命中 → 进入处理
2. 三元组抽取：指派人=发言者（你）、被指派人=李四、期限=周五、内容=季度汇报PPT
3. 落库待办（来源：群），向李四发送确认回执

**李四 收到回执（私聊机器人）**：
```
📋 收到群内任务指派：
• 指派自：张三（群：项目攻坚群）
• 任务：季度汇报PPT
• 期限：本周五 18:00 前
请回复「确认」接受或「拒绝」转交回指派人。
```

**李四 回复「确认」**：
```
✅ 已确认任务，已为您登记待办并设到期提醒。
```

**到期前机器人自动提醒李四**，闭环复用 todo_followup。

> 💡 群内语音默认不落盘（仅转写），磁盘零语音文件；如需落盘录音请在 `config/voices.yaml` 的 `group` 块开启并由管理员确认（详见上文「群聊合规配置」）。

---

## 错误处理

### 常见错误与处理方式

| 错误类型 | 触发条件 | 友好提示 |
|---------|---------|---------| 
| 语音转写失败 | `voice.content` 为空或乱码 | "抱歉，您的语音没有识别成功，请重新发送或尝试用普通话慢慢说。" |
| API 调用失败 | HTTP 4xx/5xx 错误码 | "当前网络繁忙，请稍后再试。如您连续遇到问题，可尝试重启企业微信应用。" |
| 意图识别失败 | 关键词匹配度 < 0.3 | 主动询问用户意图，提供选项菜单（见"模糊表达处理"场景） |
| TTS 合成失败 | 语音文件生成超过5秒 | 改为文字回复，附加提示："语音播报暂时不可用，已为您用文字显示。" |
| 上下文过期 | 对话间隔 > 60秒 | 自动开始新对话，回复："检测到新会话，请问有什么可以帮您的？" |
| 找不到会话 | 查询不存在的 session_id | "会话不存在或已过期，请重新发送语音指令。" |
| 硬件检测失败 | Windows API 或 WMI 均不可用 | "无法检测硬件配置，已自动使用'低配'模式保障运行。" |
| 外呼失败 | 被叫方无应答/占线 | "暂时无法接通，请稍后重试或留下口信。" |
| 录音失败 | 本地存储空间不足 | "存储空间不足，已自动清理旧录音。请重试。" |

### 异常退出策略

当发生严重错误时：

1. **用中文向用户道歉**并简要说明原因（不要暴露技术术语如 "Traceback"、"HTTP 500"）
2. **记录错误信息**到本地日志 `D:/skill/wecom-voice-agent/temp_sessions/error.log`
3. **清理临时文件**（音频文件、缓存数据）
4. **恢复初始状态**，等待下一条用户消息
5. **连续失败3次**时主动提示用户："检测到连续操作失败，请检查网络连接或稍后重试。"

**错误提示原则**：
- ❌ "Error: connection refused"（技术术语）
- ✅ "无法连接到服务，请检查您的网络后重试。"（用户语言）
- ❌ "Traceback (most recent call last)..."（堆栈信息）
- ✅ "系统遇到了临时问题，已自动恢复，请重新发送指令。"（友好提示）

---

## FAQ

### Q1：这个技能需要额外的 API Key 吗？
**A**：不需要核心 API Key。企业微信内置的语音转文字功能免费使用。
如果您希望使用更优质的语音合成（火山引擎 TTS），可选配置 API Key，但 Edge TTS 完全免费且开箱即用。

### Q2：支持哪些方言或语言？
**A**：v2.3.0 起内置**方言检测引擎**，自动识别粤语、四川话、上海话、东北话、闽南话 5 大方言，并使用对应的方言风格回复。无需切换普通话，直接说方言即可。

### Q3：语音消息长度有限制吗？
**A**：企业微信智能机器人接收的语音消息通常限制在 60 秒以内。
如需处理更长的录音，请使用企业微信的「文件上传」功能，后续版本将支持长语音转写。

### Q4：隐私安全吗？我的语音数据会被上传吗？
**A**：**绝对不会**。本技能不存储、不上传、不转发用户的任何语音数据。
语音转写完全由企业微信官方接口完成，本技能仅接收转写后的文本内容。
v2.0 起外呼录音存储在本机 `~/.wecom_voice/records/`，永不外传。

### Q5：支持群聊吗？
**A**：v2.9.0 起支持群聊语音助手模式。在群聊中 **@机器人** 后发送语音或文字指令即可触发（未 @ 的消息会被静默忽略，防止刷屏）。群聊复用单聊意图引擎，并自动注入说话人身份上下文（谁在说话、什么角色），因此查日程、建待办、查天气等能力群内同样可用。
群内还支持**语音指派任务**：说「@张三 周三前交方案」会自动建待办、向张三发送确认回执、到期提醒，闭环复用 todo_followup。
群场景合规默认值：语音默认不落盘、仅转写（磁盘零语音文件），如需落盘请在 `config/voices.yaml` 的 `group` 块开启并由管理员确认。

### Q6：能在手机上使用吗？
**A**：可以。只要您的 WorkBuddy 客户端运行并连接到企业微信，手机端和 PC 端均可使用。

### Q7：并发能力如何？
**A**：单用户模式下，本技能可同时处理多个企业微信用户的语音请求，
具体并发数根据您的电脑硬件自动调整（1-5路并发）。
外呼任务并发默认最大值 3 路（可在 `scheduler.py` 中调整）。

### Q8：如何卸载或停止？
**A**：发送文字消息"退出语音模式"即可停止语音助手。
如需完全卸载，请运行：`skillhub uninstall wecom-voice-agent`

### Q9：为什么有时候听不懂我说的话？
**A**：语音转写准确率受以下因素影响：
- 环境噪音（电视、空调、外部人声）
- 说话方言或口音较重
- 语音消息超过 60 秒
- 一次发送多步指令（如"查日程然后订会议室"）

**建议**：一次只说一件事，用普通话在安静环境发送，控制在 60 秒以内。

### Q10：v2.0 外呼功能合规吗？
**A**：完全合规。外呼功能遵守以下原则：
- **录音告知**：通话开始时明确告知用户"本次通话可能被录音"
- **用户同意**：必须用户明确同意后才开始录音
- **本地存储**：录音文件仅存储在本机 `~/.wecom_voice/records/`，不上传第三方
- **随时退出**：用户可在通话中随时要求终止录音

### Q11：遇到错误了屏幕上显示英文？
**A**：本技能已将所有错误提示改为中文。如果您仍看到英文：
1. 可能是企业微信官方 API 返回的英文错误
2. 请将错误截图发送至 **njskills@agent.qq.com**，我们会处理

---

## 脚本与使用指南

### v2.6 新增脚本

#### scripts/intent_registry.py

声明式意图引擎。加载 `config/intents.yaml`，实现关键词匹配、置信度计算、多级澄清策略。

```bash
# 运行自测
python D:/skill/wecom-voice-agent/scripts/intent_registry.py
```

**特性**：
- 20+ 意图声明式配置（query/action/system 三大类）
- 关键词匹配 + 置信度评分（匹配多关键词有加分）
- 多级澄清：≥0.7 直接执行、0.4-0.7 反问收窄、<0.4 转帮助
- 新增意图只改 `config/intents.yaml`，不改代码
- 纯标准库（yaml 可选，不可用时降级 JSON）

---

#### scripts/custom_intent_plugin.py

自定义意图插件引擎。允许企业通过 `config/custom_intents.yaml` 将意图映射到自有 HTTP API。

```bash
# 运行自测
python D:/skill/wecom-voice-agent/scripts/custom_intent_plugin.py
```

**特性**：
- 声明式端点 URL、HTTP 方法、请求模板
- 响应字段映射到话术模板（`{{field.path}}` 嵌套取值）
- 鉴权通过环境变量读取（`auth_env` 字段指定变量名）
- 超时/失败兜底话术
- 纯标准库（urllib）

**配置示例**（`config/custom_intents.yaml`）：
```yaml
intents:
  query_order:
    endpoint: "https://api.example.com/orders"
    method: "GET"
    auth_env: "ORDER_API_TOKEN"
    timeout: 10
    request_template:
      order_id: "{order_id}"
    response_template: "您的订单{{order.status}}，预计{{order.eta}}送达。"
    fallback_text: "订单查询服务暂不可用，请稍后再试。"
```

---

#### scripts/session_unified.py

统一会话管理。合并原 scheduler.py（外呼调度）与 session_manager.py（被动接收）为双向子系统。

```bash
# 运行自测
python D:/skill/wecom-voice-agent/scripts/session_unified.py
```

**特性**：
- 统一会话表（session_id / direction / status / context）
- 入站（inbound）/ 出站（outbound）/ 语音留言（voicemail）三向统一管理
- 状态机复用（state_machine.py 的 CallStateMachine）
- 记录与统计同源（call_record_subsystem.py）
- SQLite 持久化 + 自动清理过期会话
- 纯标准库（sqlite3 + threading）

---

#### scripts/ivr_engine.py

多级 IVR 菜单引擎。加载 `config/menu.yaml`，支持层级菜单导航。

```bash
# 运行自测
python D:/skill/wecom-voice-agent/scripts/ivr_engine.py
```

**特性**：
- YAML 配置化层级菜单（根菜单 → 子菜单 → 意图触发）
- 说数字或说名称双选择方式
- 0 = 重复听、9 = 转人工、8 = 返回上级
- 超时/非法输入/重试次数限制
- 纯标准库（yaml 可选，不可用时降级 JSON）

**菜单结构**（`config/menu.yaml`）：
- 根菜单：销售咨询 / 技术支持 / 财务报销 / 订单物流 / 人工服务
- 子菜单：每个大类下 3-4 个具体服务意图
- 全局特殊按键：0 重复、9 转人工、8 返回

---

#### scripts/entity_extractor.py

实体抽取增强模块。规则层 + 上下文消歧 + 复述确认。

```bash
# 运行自测
python D:/skill/wecom-voice-agent/scripts/entity_extractor.py
```

**特性**：
- 规则层：时间、日期、人物、地点、订单号、金额、手机号、邮箱、百分比、数量
- 上下文消歧：代词回指（"他"→上一轮提到的人）、省略补全
- 复述确认：格式化实体回显（"请确认：日期：XX，时间：XX..."）
- 纯标准库（re + datetime）

---

### 本地测试脚本（已有）

#### scripts/detect_hardware.py

自动检测用户计算机硬件资源，输出硬件等级配置。

```bash
python D:/skill/wecom-voice-agent/scripts/detect_hardware.py
```

**输出示例**：
```json
{
    "level": "medium",
    "ram_gb": 16.0,
    "cpu_cores": 6,
    "concurrency": 3,
    "cache_limit": 20,
    "description": "中配 - 支持3路并发，20轮历史缓存",
    "platform": "win32"
}
```

#### scripts/voice_simulator.py

模拟企业微信语音消息回调，用于本地调试意图解析逻辑。

```bash
# 基础用法
python D:/skill/wecom-voice-agent/scripts/voice_simulator.py --text "明天有什么会议"

# 指定用户
python D:/skill/wecom-voice-agent/scripts/voice_simulator.py --text "北京天气" --userid zhangsan

# JSON 格式输出
python D:/skill/wecom-voice-agent/scripts/voice_simulator.py --text "提醒我开会" --format json
```

#### scripts/session_manager.py

管理对话上下文，支持创建、查询、清理会话。

```bash
# 创建新会话
python D:/skill/wecom-voice-agent/scripts/session_manager.py create --userid zhangsan

# 查询会话状态（表格格式）
python D:/skill/wecom-voice-agent/scripts/session_manager.py get --session_id xxx --format table

# 查找用户活跃会话
python D:/skill/wecom-voice-agent/scripts/session_manager.py find --userid zhangsan

# 向会话添加消息
python D:/skill/wecom-voice-agent/scripts/session_manager.py add --session_id xxx --role user --content "你好"

# 清理过期会话（默认120秒）
python D:/skill/wecom-voice-agent/scripts/session_manager.py cleanup --timeout 180

# 查看所有会话统计
python D:/skill/wecom-voice-agent/scripts/session_manager.py stats
```

#### scripts/wecom_webhook_server.py

企业微信智能机器人回调服务器。接收企业微信推送的消息回调，自动处理语音消息。

```bash
# 一键体验所有功能（无需启动服务）
python D:/skill/wecom-voice-agent/scripts/wecom_webhook_server.py --quick

# 启动服务器（默认端口 8080）
python D:/skill/wecom-voice-agent/scripts/wecom_webhook_server.py

# 指定端口
python D:/skill/wecom-voice-agent/scripts/wecom_webhook_server.py --port 9000
```

**v2.0 核心升级**：
- ✅ **真正的天气查询**：调用 wttr.in 免费 API（无需 key），中文描述 + 穿衣建议
- ✅ **当前时间查询**：本地计算，100%可用，无需任何网络依赖
- ✅ **意图识别增强**：关键词 + 正则混合匹分，置信度评分
- ✅ **多轮对话**：根据 `msgid` 去重，会话缓存管理
- ✅ **中文错误提示**：全部错误给出具体解决步骤

**部署步骤**：
1. 启动服务器：`python scripts/wecom_webhook_server.py --port 8080`
2. 使用内网穿透暴露 8080 端口（frp/ngrok）
3. 将穿透后的 URL 填入企业微信管理后台 → 智能机器人 → 回调 URL
4. 发送语音消息测试

> 📖 **详细部署指南**：参见 `references/step_by_step_setup.md`

---

#### scripts/state_machine.py

多轮对话状态机。管理一次语音通话的完整生命周期（IDLE → DIALING → SPEAKING → LISTENING → CONFIRMING → ENDING），30 秒超时自动结束。

```bash
# 运行自测
python D:/skill/wecom-voice-agent/scripts/state_machine.py
```

**特性**：
- 状态持久化到本地 JSON（支持断线恢复）
- ASR 置信度 < 0.85 时自动进入 CONFIRMING 二次确认
- `StateMachineManager` 支持多通话并发管理

---

#### scripts/compliance.py

合规录音管理器。提供录音告知、本地存储、SQLite 持久化。

```bash
# 运行自测
python D:/skill/wecom-voice-agent/scripts/compliance.py
```

**特性**：
- 录音前播放告知文本，用户同意后才录音
- 录音文件存储在本机 `~/.wecom_voice/records/YYYY-MM-DD/`
- SQLite 记录主叫/被叫/时长/时间/意图
- **不上传任何第三方**

---

#### scripts/ivr_minutes.py

通话后自动纪要。从 ASR 文字流中提取决策点、待办项、时间点。

```bash
# 运行自测
python D:/skill/wecom-voice-agent/scripts/ivr_minutes.py
```

**特性**：
- 正则 + 规则提取，无需外部 API
- 输出结构化 markdown 格式纪要
- 支持简单情感分析（积极/中性/消极）

---

#### scripts/scheduler.py

外呼任务调度器。支持定时外呼和批量外呼。

```bash
# 运行自测
python D:/skill/wecom-voice-agent/scripts/scheduler.py
```

**使用方式**：
```python
from scheduler import OutboundScheduler, MockCallExecutor

scheduler = OutboundScheduler(executor=MockCallExecutor())
scheduler.start()

# 添加一次性外呼
scheduler.add_one_shot("task_001", "13800138000", "预约确认", "2026-07-15T09:00:00")

# 添加每日定时外呼
scheduler.add_daily("task_002", "13800138000", "早安提醒", "09:00")

# 批量外呼（CSV 导入）
scheduler.add_batch([
    {"target": "13900139000", "name": "客户A", "script": "预约确认"},
    {"target": "13900139001", "name": "客户B", "script": "回访"},
])
```

**CSV 导入格式**：
```csv
target,name,script
13800138000,张三,预约确认
13800138001,李四,回访
```

---

#### scripts/stats.py

通话记录看板。输出通话统计数据和趋势图。

```bash
# 本月看板
python D:/skill/wecom-voice-agent/scripts/stats.py

# 本周看板
python D:/skill/wecom-voice-agent/scripts/stats.py --period week

# 本年度看板
python D:/skill/wecom-voice-agent/scripts/stats.py --period year

# 按用户筛选
python D:/skill/wecom-voice-agent/scripts/stats.py --userid zhangsan

# 导出 JSON
python D:/skill/wecom-voice-agent/scripts/stats.py --export stats.json
```

**输出指标**：
- 总通话次数、总时长、平均时长
- 外呼/来电比例、接听率、录音覆盖率
- 意图分布、挂断原因分布
- 每日趋势 ASCII 图

---

#### scripts/transcriber.py

通话录音文字转写全文。输出 .txt（标准库）和 .docx（可选）。

```bash
# 运行自测
python D:/skill/wecom-voice-agent/scripts/transcriber.py
```

**使用方式**：
```python
from transcriber import TranscriptWriter

writer = TranscriptWriter()
turns = [
    {"role": "user", "content": "你好", "time": "2026-07-15T10:00:00"},
    {"role": "agent", "content": "您好，请问有什么需要帮助？", "time": "2026-07-15T10:00:05"},
]

# 输出 TXT（纯标准库）
writer.write_txt(turns, call_id="call_001")

# 输出 DOCX（需 python-docx）
writer.write_docx(turns, call_id="call_001")
```

---

#### scripts/call_record_subsystem.py（v2.5 新增）

通话记录子系统。合并原 4 个脚本（compliance/ivr_minutes/stats/transcriber）为统一接口。

```bash
# 运行自测
python D:/skill/wecom-voice-agent/scripts/call_record_subsystem.py
```

**使用方式**：
```python
from call_record_subsystem import CallRecordSubsystem

crs = CallRecordSubsystem()
crs.create_record("call_001", "13800138000", "13900139000", "outbound")
crs.give_consent("call_001", True)
crs.add_audio("call_001", audio_data)
crs.add_transcript("call_001", "用户: 你好\n助手: 您好", "greeting")
minutes = crs.generate_minutes("call_001")
stats = crs.get_stats("month")
```

---

#### scripts/voice_channel.py（v2.5 新增）

多渠道抽象层。支持企业微信/钉钉/飞书消息解析和标准化。

```bash
# 运行自测
python D:/skill/wecom-voice-agent/scripts/voice_channel.py
```

**使用方式**：
```python
from voice_channel import VoiceChannelFactory, ChannelType

# 解析企微回调
msg = VoiceChannelFactory.parse_wechat_callback(callback_dict)
# 解析钉钉回调
msg = VoiceChannelFactory.parse_dingtalk_callback(callback_dict)
# 解析飞书回调
msg = VoiceChannelFactory.parse_feishu_callback(callback_dict)

# 获取渠道处理器
channel = VoiceChannelFactory.get_channel(ChannelType.WECHAT)
```

---

#### scripts/voicemail_summary.py（v2.5 新增）

语音留言摘要系统。当用户无法接听时，语音留言自动转录并生成结构化摘要。

```bash
# 运行自测
python D:/skill/wecom-voice-agent/scripts/voicemail_summary.py
```

**使用方式**：
```python
from voicemail_summary import VoicemailSummarizer

summarizer = VoicemailSummarizer()
result = summarizer.process_voicemail("vm_001", "13800138000", "帮我查订单状态")
print(result["summary"])

# 批量处理
results = summarizer.batch_process([
    {"vm_id": "vm_001", "caller": "13800138000", "content": "查订单"},
    {"vm_id": "vm_002", "caller": "13900139000", "content": "投诉"},
])
```

---

### 配置文件

本技能无需额外配置文件即可运行。

如需自定义配置，可在工作项目录下创建 `.workbuddy/wecom-voice-agent.yaml`：

```yaml
# 企业微信语音消息 Agent 配置
# 所有选项均为可选，使用括号内默认值

tts_engine: edge  # edge 或 volcengine
log_level: info   # debug | info | warning | error
session_timeout: 60  # 对话超时时间（秒）
max_history: 5     # 单轮最大消息数
# v2.0 新增
call_timeout: 30   # 通话超时时间（秒）
max_concurrent_calls: 3  # 最大并发外呼数
confidence_threshold: 0.85  # ASR 置信度二次确认阈值
records_dir: ~/.wecom_voice/records  # 录音存储路径
# v2.8 新增
voices_config: config/voices.yaml  # TTS 音色库（3 套预设+情感调整+SSML，修改后重启生效）
volc_tts_key: ""   # 火山引擎 TTS Key（可选；留空则仅用 Edge 免费主链路，缺失自动降级）
clone_provider: "" # 语音克隆服务商 doubao / minimax（可选；留空则克隆功能完全隐藏）
clone_api_key: ""  # 语音克隆 API Key（可选，配合 clone_provider 使用）
# v2.9 新增：群聊合规配置（仅作用于群场景，单聊不受影响）
group_admins: ""    # 群管理员 userid 列表（逗号分隔），开启落盘需其中至少一人确认；留空则无任何人可开启落盘
```

#### config/voices.yaml 的 group 块（v2.9 新增）

群聊场景的合规默认值集中配置在此块，全部为可选，缺省即最保守策略：

```yaml
# 群聊语音助手合规配置（v2.9）
group:
  record: false               # 默认不落盘任何语音文件（磁盘零语音，仅转写文本）
  transcribe_only: true       # 仅做语音转写，转写结果按保留策略清理
  retention_days: 1           # 群转写文本保留天数（默认 1 天，到期自动清理）
  opt_in_requires_admin: true # 开启 record:true 落盘前，必须由 group_admins 中的管理员确认
```

**行为说明**：
- 默认 `record: false` + `transcribe_only: true`：群内语音永不写入磁盘音频文件，仅留存转写文本且按 `retention_days` 自动清理，满足验收「默认配置下磁盘零语音文件」。
- 如需群内落盘录音：先将 `record` 改为 `true`，但 `opt_in_requires_admin: true` 时仍须由 `group_admins` 列表中的管理员在运行时显式确认，否则 `record_audio_disabled()` 始终返回 True（禁止落盘）。
- 模块缺失（pyyaml 未安装）时自动降级为内置最保守默认值（record:false），绝不因依赖缺失而意外落盘。
- 单聊场景不受此块影响，沿用原 `compliance.py` 的录音告知+本地存储逻辑。

---

## 联系与反馈

### 邮箱

如有更好的建议或遇到问题，请发送邮件至：

**njskills@agent.qq.com**

### 问题反馈模板

```
标题：[wecom-voice-agent] 问题简述

环境信息：
- WorkBuddy 版本：
- 企业微信版本：
- 操作系统：

问题描述：
- 预期行为：
- 实际行为：
- 复现步骤：

是否愿意提供调试日志：是/否
```

---

## 更新日志

| v2.9.0 | 2026-10-10 | 增加：群聊语音助手模式（wecom_webhook_server.py 新增群消息路由，@机器人触发、未@静默忽略防刷屏，复用单聊意图引擎零重构并注入说话人身份上下文 chat_type/chat_id/speaker_userid/speaker_role）；增加：群维度会话隔离（session_unified.py 新增 chat_id 列与索引，群会话以 chat_id 为维度主键与单聊 userid 物理隔离避免上下文污染，存量库 PRAGMA 追加列兼容）；增加：群任务分发闭环（entity_extractor.py 三元组抽取指派人/被指派人/期限，todo_followup.py 新增确认回执 confirm_todo 与被指派人查询，群指派自动建待办+回执+到期提醒）；增加：群场景合规默认值（group_compliance.py 默认 record:false 磁盘零语音落盘、开启落盘需管理员确认，voices.yaml 新增 group 块，pyyaml 缺失降级最保守策略）；新增 group_e2e_test.py 群聊 E2E 自测（群维度/三元组/群任务闭环/群路由/说话人身份准确率抽检/降级七模块全绿）；优化：FAQ Q5 与避坑指南翻转为支持群聊 @机器人触发 |
| v2.8.0 | 2026-09-20 | 增加：TTS 多音色与情感 voice_policy.py（config/voices.yaml 三套预设音色覆盖正式通知/客服安抚/营销外呼，情感→语速语调动态叠加并自动限幅 ±50%/±50Hz，SSML 句间停顿+数字日期自动加重，Edge TTS 主链路→火山 TTS 备用链路→文字降级三级策略）；增加：语音克隆外呼 voice_clone.py（豆包/MiniMax 可选接入，内置授权确认文本+SQLite 授权留痕+样本 SHA256 防篡改，合规红线仅限本人或书面授权音色，克隆音色仅允许主动外呼场景，未配置 Key 时模块完全隐藏不报错）；增加：通话摘要质检 summary_qa.py（决策 40%/待办 35%/时间 25% 三要素加权评分，≥80 分才交付，达标摘要 5% 随机人工抽检，纠错记录回流驱动摘要 Prompt 迭代）；增加：运营报表 report_generator.py（外呼接通率/时长四档分布/意图 Top10/外呼四级漏斗调度发起→振铃接通→有效通话→待办跟进/待办逾期统计，周一生成上周完整周期 HTML 周报单文件导出，数据源缺失自动降级记警告）；新增 config/voices.yaml 音色库配置文件；补充：外部连接披露表增加火山 TTS 与语音克隆两个条件性连接（未配置 Key 时不发起） |
| v2.7.0 | 2026-09-02 | 增加：记忆桥接子模块 memory_bridge.py（zwjh 长期记忆 MCP 桥接，来电拉取历史+通话回写+降级方案，纯标准库）；增加：跟进待办闭环 todo_followup.py（纪要抽取待办→自动登记回拨→到期提醒/二次外呼→查询意图可问答，纯标准库）；增加：情感到工单直连 emotion_ticket_bridge.py（强负面→直连 ticket_manager 建单+升级+主管通知，无需独立触发，纯标准库）；优化：emotion_analyzer（v2.2）+ ticket_manager（v2.3）链路打通 |
| v2.6.0 | 2026-08-24 | 重构：声明式意图引擎 intent_registry.py（intents.yaml 配置化 20+ 意图，关键词匹配+置信度评分+多级澄清，新增意图只改配置不改代码）；增加：自定义意图插件 custom_intent_plugin.py（custom_intents.yaml 声明企业自有 API 映射，请求/响应模板+鉴权环境变量+失败兜底）；增加：统一会话管理 session_unified.py（合并 scheduler.py 与 session_manager.py 为双向子系统，统一会话表/状态机/统计）；增加：多级 IVR 菜单引擎 ivr_engine.py（menu.yaml 配置化层级菜单，0 重复听/9 转人工/8 返回上级，说数字或说名称双选择）；增加：实体抽取增强 entity_extractor.py（规则层+上下文消歧+复述确认，时间/人物/地点/订单号/金额/手机号等）；优化：原有 5 个脚本（intent_registry/custom_intent_plugin/session_unified/ivr_engine/entity_extractor）全部零外部依赖纯标准库；新增 config/intents.yaml、config/custom_intents.yaml、config/menu.yaml 三个声明式配置文件 |
| v2.5.1 | 2026-08-17 | 修复：移除 compliance.py 中对伪造域名 edge-tts.anthropic.com 的隐蔽 TCP 连接（该域名与声明使用的微软 Edge TTS 服务主体不符，属未披露外联通道）；修复：移除 compliance.py 顶部 import socket 及 _check_tts_available 静态方法；修复：play_announcement 默认使用文字告知，不再发起任何外部网络连接；修正：SKILL.md 合规声明中"不持久化存储用户语音内容"改为准确表述（通话记录持久化于本机 SQLite，录音文件存储于本地，保留期限 90 天）；增加：外部连接披露表（仅 wttr.in 天气查询 API，不含用户身份信息） |
| v2.5.0 | 2026-08-17 | 合并：ivr_minutes.py、compliance.py、stats.py、transcriber.py 为 call_record_subsystem.py 通话记录子系统（录音+纪要+元数据+统计一体，消除4脚本分散调用）；增加：多渠道抽象层 voice_channel.py（VoiceChannel 抽象接口+工厂模式，支持企业微信/钉钉/飞书）；增加：语音留言摘要 voicemail_summary.py（voicemail→结构化摘要，复用纪要能力）；增加：通话记录子系统统一入口（create_record→add_audio→generate_minutes→get_stats）；增加：多渠道路由（企微/钉钉/飞书消息自动解析+标准化）；扩展 wecom_webhook_server.py 语音留言处理+多渠道接入；新增 call_record_subsystem.py、voice_channel.py、voicemail_summary.py 三个脚本 |
| v2.4.0 | 2026-08-07 | 增加：VAD 语音活动检测（短时能量+过零率分析，零外部依赖，非人声前置过滤，误触发率降低80%+）；增加：四级优先级请求队列（VIP/高价值/普通/批量，企微API限流20次/分智能排队）；增加：强制录音告知（不可跳过，录音前自动播放告知语，文字+音频双通道降级）；增加：数据库迁移（call_records 新增告知方式/确认方式/时间戳字段）；新增 vad_filter.py、priority_queue.py 脚本；升级 compliance.py 至 v3.0（强制录音告知系统）；扩展 wecom_webhook_server.py VAD 前置过滤+优先级路由 |
| v2.3.0 | 2026-08-01 | 增加：方言检测（粤语/四川话/上海话/东北话/闽南话 5大方言识别）；增加：方言回复适配（按方言习惯生成回复）；增加：方言回复模板（dialect_strategies.json 6方言×9场景）；增加：自动工单创建（愤怒/投诉/退款/账户问题自动建单）；增加：智能路由（按类别分配处理人+负载均衡）；增加：工单状态流转（新建→分配→处理中→待确认→已解决→已关闭）；增加：操作历史追踪+满意度评价+超时预警；新增 dialect_detector.py、ticket_manager.py 脚本；新增 dialect_strategies.json 模板；扩展 session_manager.py 方言+工单字段；扩展 wecom_webhook_server.py 方言+工单集成 |
| v2.2.0 | 2026-07-23 | 增加：情感识别与自适应对话策略（愤怒/焦虑/满意/困惑/中性 5分类）；增加：情绪升级跟踪（连续负面>2轮建议转人工）；增加：对话策略模板（安抚/安抚/确认/简化/正向引导）；增加：硬件自适应（低配禁用音频分析，高配启用）；新增 emotion_analyzer.py 脚本、emotion_strategies.json 策略模板；扩展 session_manager.py 情感状态跟踪 |
| v2.1.0 | 2026-07-15 | 修复bug：安全审计修复（移除测试代码中的 /etc/passwd 路径引用，改为安全测试字符串） |
| v2.0.0 | 2026-07-15 | 增加：主动外呼、来电接线、合规录音、通话纪要、外呼调度、通话看板、全文转写；增加：ASR置信度二次确认、外呼任务批量导入；新增state_machine.py、compliance.py、ivr_minutes.py、scheduler.py、stats.py、transcriber.py六个脚本 |
| v1.3.0 | 2026-07-10 | 增加：wttr.in天气查询（中文描述+穿衣建议）；增加：本地时间查询（100%可用）；增加：--quick一键体验模式；增加：意图识别增强（关键词+正则混合匹配）；修复：回复不再出现"需要配置API接入"，改为真正执行 |
| v1.2.0 | 2026-07-09 | 增加：wecom_webhook_server.py企业微信回调服务器；增加：step_by_step_setup.md分步部署指南；增加：多消息类型支持（文本/语音/图片/文件/视频） |
| v1.1.0 | 2026-07-09 | 增加：避坑指南（8个常见坑+正确做法）；增加：模糊表达处理策略（不确定时主动确认）；增加：连续失败3次自动提示；增加：错误提示原则（用户语言 vs 技术术语） |
| v1.0.0 | 2026-07-08 | 初始版本发布，包含企业微信语音消息回调、意图识别、多轮对话 |

### 后续规划
- v2.10.0：语音声纹识别（区分不同说话人）
- v3.0.0：多模态能力（图片+语音混合消息）+ 对接外部CRM

---

## 许可与版权

© 2026 njskills. 保留所有权利。

本技能基于 MIT 许可证开源，允许个人和商业使用，但不得声称对原始作品拥有版权。

**免责声明**：本技能按"原样"提供，作者不对因使用本技能造成的任何损失承担责任。

---

*版本：v2.9.0 ｜ 许可：MIT ｜ 核心纯标准库、零密钥打包、可只读审计。*
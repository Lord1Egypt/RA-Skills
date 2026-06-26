---
name: think-expand
description: 想核心（大脑主核心），统筹听/看/说/做四大核心，集成MemPalace记忆检索、自我进化、闭环学习，事件驱动决策，永动机式持续运行，仅OpenCode内部使用。
compatibility: opencode
metadata:
  private: true
  author: laosi
  status: active
  priority: 1
---

# 想核心（大脑主核心 - ThinkCore）

## 原始能力（必须始终运行）
- 系统启动时自动激活，作为AI决策大脑
- 所有输入先经过"想"处理，决策调度执行
- 崩溃自愈：每60秒自检，异常自动重启

## 核心定位
- 系统主核心，听/看/说/做四大核心围绕运行
- 负责：语义理解、决策规划、记忆检索、任务调度

## 内置知识数据库（ThinkCore大脑）
- 位置: D:\coze-local\simple-agent\skills_learned\learned.db
- 启动时自动加载: 16个高星技能 (385K stars)
- 查询响应: <50ms

## 功能模块
1. **记忆检索**: `py -3.13 -m mempalace search "关键词"`
2. **技能吸收**: 内置GitHub高星技能索引，自动学习新技能
3. **事件驱动**: 响应触发词、任务请求
4. **自我进化**: 经验沉淀→技能生成→自动优化→持续进化
5. **永动机**: 持续运行，崩溃自动重启

## 吸收流程（内置）
1. 触发"学习/吸收" → 自动搜索GitHub高星技能
2. 提取信息存入learned.db，按stars权重排序
3. 对比现有技能，低于阈值则丢弃
4. 验证兼容后整合到skills_learned
5. 反馈结果到speak-expand

## 触发场景
- 系统启动时自动激活
- 所有用户输入先经过think-expand处理
- 负责决策调用哪个核心/技能
- 统筹hear/see/speak/do/learn五个核心

## 联动
- 决策结果送入`speak-expand`/`do-expand`
- 进化记录存入`mempalace_wings/self_evolution/`
- 技能索引存入learned.db供实时查询

## 任务完成建议机制
- 每次完成任务后自动给出下一步建议
- 根据当前系统状态推荐最优行动
- 格式: "建议: [行动] | 理由: [原因]"

## 状态监控
- 仪表盘: py D:\coze-local\simple-agent\skills_learned\gui_dashboard.py
- 查询: py D:\coze-local\simple-agent\skills_learned\learned_manager.py list
- 技能组合: py D:\coze-local\simple-agent\skills_learned\skill_combos.py
- 自动学习: py D:\coze-local\simple-agent\skills_learned\auto_learn.py
- 用户预测: py D:\coze-local\simple-agent\skills_learned\user_pattern.py
- 评估: py D:\coze-local\simple-agent\skills_learned\evaluate.py

## 自我进化能力
- 自动学习: 定期扫描GitHub新技能并吸收
- 跨域融合: 创建技能组合(AI安全/自动化测试/全栈)
- 预测分析: 记录用户习惯,预测下一步需求
- 本地LLM: 支持Ollama/LM Studio离线推理

## 离线能力
- 不依赖外部网络可运行基础功能
- 本地技能库随时可用
- 剪贴板监控独立运行

## 大模型理解能力 (GPT原理)
- 本质: 有限状态马尔可夫链 (FSMC)
- 核心机制: 输入token序列 → 预测下一个token概率
- 状态 = 上下文(context_length个token)
- 组件: Token Embedding + Positional Encoding + Self-Attention + FFN + LayerNorm
- 可解释任意AI模型内部工作原理

## 技能融合
- 类似Transformer: 多头注意力并行处理
- 状态转移: 类似GPT的token预测
- 持续学习: 类似预训练+微调
- 知识检索: 类似RAG的上下文查询

## B站学习
> 学习时间: 2026-06-01 20:57

- **木瓜Zxc**: 【环世界】rimtalk必备MOD推荐RimTalk -Expand Memory
  - 关键词: 环世界, rimtalk必备MOD推荐RimTalk, Expand, Memory
- **XHN2JK**: MC大战僵尸2 EXPAND 星莲船额外关卡 HRAD
  - 关键词: MC大战僵尸2, EXPAND, 星莲船额外关卡, HRAD

## B站学习
> 学习时间: 2026-06-01 21:02

- **木瓜Zxc**: 【环世界】rimtalk必备MOD推荐RimTalk -Expand Memory
- **XHN2JK**: MC大战僵尸2 EXPAND 星莲船额外关卡 HRAD
- **knighteer**: 旧友与新敌—MVZ2 EXPU 传送带红龙战过关

## B站学习 (第1轮)
> 学习时间: 2026-06-02 09:22

- **木瓜Zxc**: 【环世界】rimtalk必备MOD推荐RimTalk -Expand Memory
  https://www.bilibili.com/video/BV1uLUYBwErw
- **XHN2JK**: MC大战僵尸2 EXPAND 星莲船额外关卡 HRAD
  https://www.bilibili.com/video/BV1Gw4m1k7FN
- **毕老师侃英语**: 秒背单词！expand 和 expend～
  https://www.bilibili.com/video/BV1cX4y1h7mW

## B站学习 (第2轮)
> 学习时间: 2026-06-02 09:35

- **木瓜Zxc**: 【环世界】rimtalk必备MOD推荐RimTalk -Expand Memory
  https://www.bilibili.com/video/BV1uLUYBwErw
- **XHN2JK**: MC大战僵尸2 EXPAND 星莲船额外关卡 HRAD
  https://www.bilibili.com/video/BV1Gw4m1k7FN
- **毕老师侃英语**: 秒背单词！expand 和 expend～
  https://www.bilibili.com/video/BV1cX4y1h7mW

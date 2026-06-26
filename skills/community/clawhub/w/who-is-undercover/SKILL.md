---
name: who-is-undercover
description: 谁是卧底 - 经典社交推理游戏的AI版本，支持4-10人游戏，包含智能AI对手和完整游戏机制。
version: 1.1.0
metadata:
  openclaw:
    requires:
      bins:
        - node
    emoji: "🎭"
    homepage: https://github.com/long5/who-is-undercover
---

# Who is Undercover - OpenClaw Skill

## 🎮 游戏简介
"谁是卧底"是一款经典的社交推理游戏，现在通过AI技术实现了完整的自动化版本。玩家需要通过描述词语来找出隐藏在平民中的卧底，或者作为卧底成功隐藏身份。

## 📋 游戏规则
- **角色分配**: 玩家被分配秘密角色：大多数是拥有相同词语的"平民"，1-2个是拥有不同但相关词语的"卧底"
- **描述阶段**: 每轮游戏中，玩家描述自己的词语，但不能直接透露词语本身
- **投票阶段**: 描述结束后，玩家投票选出他们认为是卧底的玩家
- **淘汰机制**: 得票最多的玩家被淘汰
- **胜负条件**: 
  - 平民胜利：所有卧底被淘汰
  - 卧底胜利：卧底数量等于或超过平民数量

## 🚀 快速开始
```bash
# 安装技能包
clawhub install who-is-undercover

# 创建新游戏（6人游戏，2个人类玩家）
/skill who-is-undercover start 6 2

# 查看可加入的游戏
/skill who-is-undercover list

# 加入现有游戏
/skill who-is-undercover join [游戏ID]
```

## 🎯 功能特性
- **可配置玩家数量**: 支持4-10人游戏
- **多人游戏支持**: 多个真实玩家可以同时参与同一局游戏
- **智能AI对手**: AI能够生成逼真的人类式描述
- **智能投票逻辑**: 基于描述分析的投票机制
- **交互式回合制**: 完整的游戏流程体验
- **一键安装**: 通过ClawHub轻松安装
- **飞书集成**: 支持群组游戏

## 📋 命令列表
- `/skill who-is-undercover start [player_count] [human_players]` - 开始新游戏
- `/skill who-is-undercover join [game_id]` - 加入现有游戏  
- `/skill who-is-undercover list` - 列出可加入的游戏
- `/skill who-is-undercover describe "[description]"` - 提交描述
- `/skill who-is-undercover vote [player_number]` - 投票
- `/skill who-is-undercover status` - 查看游戏状态
- `/skill who-is-undercover end` - 结束游戏

## 💡 游戏技巧
### 平民策略
- 描述要具体但不要过于明显
- 观察其他玩家的描述模式
- 投票时考虑描述的合理性

### 卧底策略
- 描述要模糊但合理  
- 避免使用可能暴露身份的词汇
- 观察平民的描述风格并模仿

## 🛠️ 版本信息
- **当前版本**: 1.1.0
- **主要更新**: 新增多人游戏支持功能
- **许可证**: MIT-0 (免费使用、修改和重新分发，无需署名)
- **作者**: 龙5
- **GitHub**: https://github.com/long5/who-is-undercover

## 🔜 未来计划
- **v1.2.0**: AI智能度提升、投票逻辑优化
- **v2.0.0**: 用户体验优化、游戏统计功能、自定义词语库

## 📞 支持与反馈
欢迎在ClawHub页面留下评论，或通过GitHub提交issue和功能请求！
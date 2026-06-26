# Who is Undercover - OpenClaw Skill

![Who is Undercover](https://via.placeholder.com/800x400?text=Who+is+Undercover+Game)

**谁是卧底** - 经典社交推理游戏的AI版本，专为OpenClaw框架设计。

## 🎮 游戏特色

- **真实游戏体验**：完整还原"谁是卧底"经典玩法
- **智能AI对手**：AI玩家能生成合理描述并进行策略投票
- **灵活配置**：支持4-10人游戏，可调整人类/AI玩家比例
- **一键安装**：通过ClawHub或InStreet社区一键安装
- **用户友好**：简洁明了的命令界面和详细用户指南

## 🚀 快速开始

```bash
# 一键安装
openclaw skill install who-is-undercover

# 开始游戏（6人，1个人类）
/skill who-is-undercover start

# 查看完整用户指南
/skill who-is-undercover help
```

## 📋 功能列表

### 核心游戏机制
- ✅ 角色随机分配（平民 vs 卧底）
- ✅ 智能词语配对系统（15组精心设计的词对）
- ✅ 描述轮次控制
- ✅ 投票机制实现
- ✅ 胜负判定逻辑
- ✅ 多轮游戏支持

### AI智能行为
- ✅ AI描述生成（基于词语类型生成合理描述）
- ✅ AI投票策略（分析描述合理性进行投票）
- ✅ 难度自适应（根据玩家数量调整卧底数量）
- ✅ 上下文感知（AI会参考其他玩家的描述）

### 用户体验
- ✅ 清晰的游戏状态显示
- ✅ 详细的错误提示
- ✅ 完整的用户指南
- ✅ 一键安装支持
- ✅ 飞书集成（支持群聊游戏）

## 📁 项目结构

```
who-is-undercover/
├── SKILL.md           # 技能描述文件
├── index.js           # 主技能入口点
├── game_logic.js      # 核心游戏逻辑
├── USER_GUIDE.md      # 用户操作指南
├── INSTALL.md         # 安装说明
├── README.md          # 项目介绍
├── package.json       # 包配置文件
├── test.js            # 测试脚本
├── current_game.json  # 当前游戏状态存储
└── room_link.txt      # InStreet房间链接
```

## 🔧 技术架构

### 设计模式
- **状态机模式**：管理游戏不同阶段（描述、投票、结果）
- **策略模式**：AI行为策略可扩展
- **观察者模式**：游戏状态变化通知

### OpenClaw集成
- 符合OpenClaw技能标准
- 支持会话上下文管理
- 兼容ClawHub一键安装
- InStreet社区认证

## 📈 性能优化

- **轻量级实现**：无外部依赖，纯JavaScript
- **内存高效**：游戏状态最小化存储
- **快速响应**：本地计算，无网络延迟
- **资源友好**：低CPU和内存占用

## 🌐 社区支持

- **InStreet社区**：发布在Skill板块，支持版本管理和用户反馈
- **ClawHub集成**：支持自动更新和依赖管理
- **开源贡献**：欢迎PR和issue

## 📄 许可证

MIT License - 免费用于个人和商业项目

## 🙏 致谢

- OpenClaw团队提供的优秀框架
- InStreet社区的最佳实践指导
- "谁是卧底"原版游戏创作者

## 🎯 使用示例

### 基础游戏
```
/skill who-is-undercover start
```
开始6人游戏（1个人类，5个AI）

### 自定义游戏
```
/skill who-is-undercover start 8 2
```
开始8人游戏（2个人类，6个AI）

### 提交描述
```
/skill who-is-undercover describe "这是一种常见的水果，红红的很脆"
```

### 投票
```
/skill who-is-undercover vote 3
```
投票给玩家3

### 查看状态
```
/skill who-is-undercover status
```

---

**Ready to play? Install now and experience the classic social deduction game with AI!**

```bash
openclaw skill install who-is-undercover
```
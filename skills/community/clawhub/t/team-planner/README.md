# team-planner

**Multi-Agent Team Planning Skill for OpenClaw**

智能规划多 AI Agent 协作团队的技能。当你有复杂任务需要多个 Agent 并行工作时，这个技能帮你设计团队架构、角色分工和协作流程。

## Features | 功能特点

- 📋 **任务分析** - 分析任务复杂度，判断是否需要多 Agent 协作
- 👥 **团队设计** - 设计最优团队规模（3-6人）和角色分工
- 🔄 **流程规划** - 规划协作阶段、依赖关系和通信机制
- 📝 **输出完整方案** - 包括启动顺序、Prompt 模板和成功标准

## Usage | 使用方式

### Trigger Phrases | 触发词

- "帮我规划一个团队"
- "设计 Agent 角色"
- "多个 Agent 怎么协作"
- "这个项目需要几个 Agent"
- "plan a team"
- "design agent roles"

### Example | 使用示例

```
用户: 我想做一个博客系统，包含用户登录、文章管理、评论功能，怎么组织 Agent？

助手 (调用 team-planner 技能后):
# 团队架构方案

## 1. 任务概要
- **目标**: 构建博客系统
- **复杂度**: 中等 (建议多 Agent 协作)
- **推荐方案**: 6 人团队

## 2. 团队成员
- researcher: 技术调研
- architect: 系统架构设计
- backend-dev: 后端开发
- frontend-dev: 前端开发
- tester: 测试验证
- documenter: 文档编写

## 3. 协作流程
Phase 1: 调研与架构 (researcher, architect)
Phase 2: 并行开发 (backend-dev, frontend-dev, tester)
Phase 3: 集成与文档 (all members)
...
```

## Structure | 目录结构

```
team-planner/
├── SKILL.md              # 主技能文件 (必需)
├── README.md             # 说明文档
└── references/           # 参考文档 (可选)
    └── examples.md       # 更多使用示例
```

## Installation | 安装方式

### 方式一: ClawHub (推荐)
```bash
# 在 QClaw 中说:
"从 ClawHub 安装 team-planner"
```

### 方式二: GitHub 手动安装
```bash
# 克隆到本地 skills 目录
git clone https://github.com/YOUR_USERNAME/team-planner.git
# 或复制 SKILL.md 内容到 ~/.openclaw/skills/team-planner/
```

## Requirements | 要求

- OpenClaw 最新版本
- 支持多 Agent 协作的工作区配置

## Documentation | 文档

详见 [SKILL.md](./SKILL.md)

## License | 许可证

MIT License

## Contributing | 贡献

欢迎提交 Issue 和 Pull Request！

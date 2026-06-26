# Writing Assistant

## 描述
专业写作助手智能体 - 基于三层架构，支持内容创作/改写/标题生成/选题策划

## 功能
- **write**: 内容创作代理
- **rewrite**: 改写优化代理
- **headline**: 标题生成代理
- **ideate**: 选题策划代理

## 用法
```bash
cd ~/writing-assistant
./scripts/startup.sh    # 启动系统
```

直接对话使用：
- 说"写一篇..." → 内容创作
- 说"改一下..." → 改写优化
- 说"标题..." → 标题生成
- 说"选题..." → 选题策划

## 架构
```
identity/              # 第一层：身份层
  SOUL.md             # 核心灵魂：为写作而生
  IDENTITY.md         # 角色：首席撰稿人
  USER.md             # 用户：创意总监

operations/            # 第二层：操作层
  AGENTS.md           # 4个写作代理
  HEARTBEAT.md        # 质量检查机制
  ROLE-CHIEF-WRITER.md # 首席撰稿人指南

knowledge/             # 第三层：知识层
  MEMORY.md           # 写作技巧与平台知识
  shared-context/     # 跨会话状态
```

## 标签
writing, content, xiaohongshu, copywriting, agent

## 版本
1.0.0

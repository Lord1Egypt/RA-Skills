# test-skill-demo

一个完整的测试技能示例，展示 ClawHub 技能的标准结构和最佳实践。

## 功能特性

- ✅ 基础消息回复
- ✅ 上下文信息展示
- ✅ 模块化代码结构
- ✅ 完整的元数据定义

## 使用场景

本技能主要用于：
1. 测试 ClawHub 发布流程
2. 学习 OpenClaw 技能开发基础结构
3. 验证技能安装和运行

## 使用方法

### 运行技能
```bash
openclaw skills run test-skill-demo
```

### 在对话中调用
直接在支持技能的 Agent 中提及技能名称即可。

## 文件结构

```
test-skill-demo/
├── SKILL.md        # 技能文档（本文件）
├── package.json    # NPM 包元数据
└── index.js        # 主入口文件
```

## 开发说明

### 本地测试
```bash
cd ~/clawd/skills/test-skill-demo
openclaw skills run test-skill-demo
```

### 发布到 ClawHub
```bash
clawhub publish ~/clawd/skills/test-skill-demo --version 1.0.0
```

## 版本历史

- **v1.0.0** - 初始版本，基础功能实现

## 许可证

MIT License

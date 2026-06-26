---
name: ChatFlow Guardian
description: 确保你的对话永远不会中断！智能监控对话状态，确保用户的消息永远不会是最后一条。
category: communication
version: 1.0.0
status: production
network_required: false
---

# 【畅聊守护者】ChatFlow Guardian - 智能对话管理技能

确保你的对话永远不会中断！智能监控对话状态，确保用户的消息永远不会是最后一条。

**English: ChatFlow Guardian - Keep your conversations flowing smoothly!**

## 🎯 核心功能

### 基础功能
- **对话状态监控** - 每180秒检查一次对话状态
- **自动响应** - 当检测到对话可能中断时自动提供响应
- **进度汇报** - 长时间任务时自动汇报进度
- **消息补全** - 自动补全未完成的用户消息

### 三大增强功能
1. **多平台支持** - 兼容QQBot、企业微信、Slack、钉钉等8个平台
2. **预测性响应** - 基于历史对话预测用户需求，提前准备答案
3. **深度学习优化** - 神经网络提升意图识别准确率

## 🚀 快速开始

### 安装依赖
```bash
cd /root/.openclaw/workspace/skills/不冷场管家
npm install
```

### 运行测试
```bash
# 快速功能测试
node scripts/quick-all-test.js

# 完整演示
node scripts/enhanced-demo.js
```

### 部署使用
```bash
# 1. 运行部署脚本
bash /root/.openclaw/scripts/deploy-no-cold-chat.sh

# 2. 启动技能
bash /root/.openclaw/scripts/manage-no-cold-chat.sh start

# 3. 查看状态
bash /root/.openclaw/scripts/manage-no-cold-chat.sh status
```

## ⚙️ 配置说明

技能配置在`config/local.json`文件中，支持以下设置：
- 监控间隔时间
- 响应阈值
- 安静时段
- 支持的平台
- 预测性响应开关
- 深度学习优化配置

## 📊 技术架构

- **对话状态监控器**: 基于时间的对话状态检查
- **平台适配器**: 支持8个主流通讯平台
- **预测性响应引擎**: 基于历史行为的智能预测
- **深度学习模块**: 神经网络提升意图识别

## 🔧 开发文档

详细的开发文档请参考：
- `QUICKSTART.md` - 快速开始指南
- `README.md` - 详细使用说明
- `CONTRIBUTING.md` - 贡献指南
- `CHANGELOG.md` - 版本变更记录

---

*ChatFlow Guardian - 让对话永远活跃！*
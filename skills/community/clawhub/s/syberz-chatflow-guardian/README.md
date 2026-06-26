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

配置文件位置: `config/default.json`

### 主要配置项:
```json
{
  "monitoring": {
    "check_interval": 180,      # 检查间隔（秒）
    "response_threshold": 180,  # 响应阈值（秒）
    "quiet_hours": ["23:00-07:00"]  # 安静时段
  },
  "platforms": {
    "enabled": true,           # 多平台支持
    "supported": ["qqbot", "wecom", "slack", "dingtalk"]
  },
  "predictive": {
    "enabled": true,           # 预测性响应
    "prediction_threshold": 0.7
  },
  "deeplearning": {
    "enabled": true,           # 深度学习优化
    "use_pretrained": true
  }
}
```

## 📊 技能状态

查看技能运行状态:
```javascript
const DialogManager = require('./src/index');
const dialogManager = new DialogManager();

// 获取状态
const status = dialogManager.getStatus();
console.log('技能状态:', status);
```

状态信息包括:
- 运行状态、会话信息
- 监控统计、平台状态
- 预测引擎数据、深度学习模型状态

## 🎮 使用示例

### 基础使用
```javascript
const DialogManager = require('./src/index');

// 创建技能实例
const dialogManager = new DialogManager();

// 启动技能
await dialogManager.start({
  id: 'session-001',
  platform: 'qqbot',
  userId: 'user-001'
});

// 手动触发对话补全
await dialogManager.completeMessage('需要帮忙分析数据');
```

### 增强功能使用
```javascript
// 1. 增强意图识别
const enhancedIntent = await dialogManager.analyzeIntentEnhanced(
  '帮我分析数据',
  { topic: 'data-analysis' }
);

// 2. 预测用户行为
const prediction = await dialogManager.predictUserNextAction(
  'user-001',
  recentInteractions
);

// 3. 分析对话质量
const quality = await dialogManager.analyzeConversationQuality(conversation);
```

## 🔧 服务管理

使用服务管理脚本:
```bash
# 启动
bash /root/.openclaw/scripts/manage-no-cold-chat.sh start

# 停止
bash /root/.openclaw/scripts/manage-no-cold-chat.sh stop

# 查看状态
bash /root/.openclaw/scripts/manage-no-cold-chat.sh status

# 查看日志
bash /root/.openclaw/scripts/manage-no-cold-chat.sh logs

# 运行测试
bash /root/.openclaw/scripts/manage-no-cold-chat.sh test

# 运行演示
bash /root/.openclaw/scripts/manage-no-cold-chat.sh demo
```

## 📈 性能指标

- **意图识别准确率**: 基础85% + 深度学习提升10-20%
- **响应时间**: 平均<2秒，预测性响应减少等待
- **平台兼容性**: 8个主流通讯平台
- **可扩展性**: 模块化架构，易于扩展

## 🐛 故障排除

### 常见问题
1. **技能无法启动**: 检查依赖安装 `npm install`
2. **平台连接失败**: 检查平台配置和网络连接
3. **意图识别不准**: 收集更多训练数据，启用深度学习优化
4. **内存占用高**: 调整监控间隔，启用token优化

### 获取帮助
- 查看日志: `tail -f /root/.openclaw/logs/no-cold-chat.log`
- 运行诊断: `bash /root/.openclaw/scripts/manage-no-cold-chat.sh test`
- 重置技能: 重启技能进程

## 📄 许可证

MIT License

## 👥 贡献者

- syberZ - 主要开发者

---

**确保你的对话永远不会冷场！** 🚀

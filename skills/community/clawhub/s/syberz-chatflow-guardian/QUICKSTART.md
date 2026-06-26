# 智能对话管理技能 - 快速开始指南

## 🚀 5分钟快速上手

### 第一步：安装技能
```bash
# 进入技能目录
cd skills/dialog-manager

# 运行安装脚本
bash scripts/install.sh
```

### 第二步：启动技能
```bash
# 方式1：直接启动
node start-dialog-manager.js

# 方式2：作为服务启动（需要systemd）
sudo systemctl enable openclaw-dialog-manager.service
sudo systemctl start openclaw-dialog-manager.service
```

### 第三步：验证运行
```bash
# 查看状态
curl -s http://localhost:3000/api/dialog-manager/status | jq .

# 或查看日志
tail -f ~/.openclaw/logs/dialog-manager.log
```

## 🎯 核心功能体验

### 1. 基础监控
技能会自动监控对话状态，确保：
- ✅ 用户发言后不会长时间无响应
- ✅ AI回答完整，不会出现半截回答
- ✅ 任务执行时有定期进度汇报

### 2. 智能响应
根据用户意图自动调整响应策略：
- **问题**：立即响应或快速思考后回答
- **任务请求**：确认理解 + 执行计划
- **社交互动**：适度回应，保持对话温度
- **反馈建议**：感谢 + 改进确认

### 3. 进度透明
长时间任务会自动汇报进度：
```
⏰ 12:00: 正在处理【数据分析】，已完成30%
⏰ 12:05: 正在处理【数据分析】，已完成60%
⏰ 12:10: 【数据分析】已完成！结果已生成
```

### 4. Token优化
智能管理资源使用：
- 简单问题使用模板响应（节省90% token）
- 复杂问题才调用深度思考
- 缓存常用响应，减少重复计算

## ⚙️ 基础配置

### 配置文件位置
```
~/.openclaw/config/skills/dialog-manager/config.json
```

### 关键配置项
```json
{
  "check_interval": 180,           // 检查间隔（秒）
  "response_threshold": 180,       // 响应阈值（秒）
  "quiet_hours": ["23:00-07:00"],  // 安静时段
  "auto_complete": true,           // 自动补全
  "token_optimization": true       // token优化
}
```

### 快速调整
```bash
# 修改检查频率为2分钟
sed -i 's/"check_interval": 180/"check_interval": 120/' config.json

# 禁用安静时段
sed -i 's/"quiet_hours": \["23:00-07:00"\]/"quiet_hours": []/' config.json
```

## 📊 监控和调试

### 查看实时状态
```bash
# 查看技能状态
node scripts/status.js

# 或直接调用API
curl http://localhost:3000/api/dialog-manager/stats
```

### 查看日志
```bash
# 实时查看日志
tail -f ~/.openclaw/logs/dialog-manager.log

# 查看错误日志
grep "ERROR" ~/.openclaw/logs/dialog-manager.log

# 查看性能指标
cat ~/.openclaw/logs/dialog-manager-metrics.log | jq .
```

### 性能指标
```bash
# 运行性能测试
node scripts/benchmark.js

# 查看token使用统计
node scripts/token-stats.js
```

## 🔧 常见问题解决

### 技能未启动
```bash
# 检查进程
ps aux | grep dialog-manager

# 检查端口
netstat -tlnp | grep :3000

# 重启技能
pkill -f dialog-manager
node start-dialog-manager.js
```

### 响应过于频繁
```bash
# 增加检查间隔
echo '{"check_interval": 300}' > config-override.json

# 或减少响应阈值
echo '{"response_threshold": 300}' > config-override.json
```

### Token使用过高
```bash
# 启用更强优化
echo '{"token_optimization": true, "thinking_threshold": 0.8}' > config-override.json

# 限制最大token
echo '{"max_tokens_per_check": 500}' > config-override.json
```

## 🎮 演示和测试

### 运行完整演示
```bash
node scripts/demo.js
```

### 运行单元测试
```bash
node tests/basic.test.js
```

### 模拟对话场景
```bash
# 启动模拟器
node scripts/simulator.js

# 或使用交互式测试
node scripts/interactive-test.js
```

## 🔄 更新和维护

### 更新技能
```bash
# 拉取最新代码
git pull origin main

# 重新安装依赖
npm install

# 重启技能
pkill -f dialog-manager
node start-dialog-manager.js
```

### 备份配置
```bash
# 备份当前配置
cp ~/.openclaw/config/skills/dialog-manager/config.json config-backup-$(date +%Y%m%d).json

# 恢复配置
cp config-backup-20240327.json ~/.openclaw/config/skills/dialog-manager/config.json
```

### 重置技能
```bash
# 停止技能
pkill -f dialog-manager

# 清除缓存
rm -rf ~/.openclaw/cache/dialog-manager/*

# 清除日志（可选）
echo "" > ~/.openclaw/logs/dialog-manager.log

# 重新启动
node start-dialog-manager.js
```

## 📈 高级功能

### 自定义响应模板
```javascript
// 创建 custom-templates.json
{
  "immediate_response": ["自定义立即响应1", "自定义立即响应2"],
  "progress_report": "【{task}】处理中，当前进度：{percent}%"
}

// 加载自定义模板
echo '{"templates_file": "custom-templates.json"}' > config-override.json
```

### 集成其他技能
```javascript
// 在现有技能中调用对话管理器
const DialogManager = require('dialog-manager');
const dialogManager = new DialogManager();

// 启动监控
await dialogManager.start(currentSession);

// 手动触发进度汇报
await dialogManager.reportProgress({
  name: '我的任务',
  progress: 0.5,
  status: 'working'
});
```

### 扩展功能
1. **Slack/钉钉集成** - 将进度推送到团队聊天
2. **邮件通知** - 重要事件邮件提醒
3. **数据分析** - 对话质量分析报告
4. **预测性响应** - 基于历史预测用户需求

## 🆘 获取帮助

### 文档资源
- [完整文档](docs/) - 详细技术文档
- [API参考](docs/api.md) - API接口说明
- [配置指南](docs/configuration.md) - 配置选项详解

### 问题反馈
1. 查看现有问题：`issues/` 目录
2. 提交新问题：使用GitHub Issues
3. 紧急支持：联系技能作者

### 社区支持
- OpenClaw社区论坛
- GitHub Discussions
- 技能用户群

---

## ⏱️ 时间线参考

### 第1天：安装和基础使用
- 安装技能，体验基础功能
- 调整基本配置
- 运行演示程序

### 第1周：日常使用
- 监控对话质量
- 优化响应策略
- 建立使用习惯

### 第1个月：深度集成
- 自定义响应模板
- 集成到工作流
- 性能调优

### 长期：持续优化
- 基于使用数据优化
- 扩展新功能
- 分享最佳实践

---

**🎉 现在开始使用智能对话管理技能，让对话更智能、更高效！**
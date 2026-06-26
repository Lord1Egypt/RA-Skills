---
name: token-tracker-pro
description: 记录和追踪 OpenClaw 会话的 token 消耗，提供每日、每周和累计统计，并提出节省 token 的建议
---
# Token Tracker Pro

记录和追踪 OpenClaw 会话的 token 消耗，提供每日、每周和累计统计，并提出节省 token 的建议。

## 版本信息

- **版本**: 2.2.0
- **发布日期**: 2026-03-25
- **作者**: longziruo-max

## 主要功能

### 📊 实时 Token 追踪
- 追踪每个会话的 token 消耗
- 支持多种模型类型
- 自动记录会话开始和结束

### 📈 统计分析
- 每日统计：查看今天消耗的 token
- 每周统计：查看本周累计消耗
- 累计统计：查看历史总消耗

### 🎯 智能模型推荐
- 分析你的使用模式
- 推荐更经济的模型配置
- 提供节省 token 的具体建议

### 💡 Token 优化
- 基于使用习惯的分析
- 提供可操作的建议
- 帮助降低 token 成本

### 📊 可视化仪表板
- Web 界面查看实时数据
- 图表展示趋势
- 历史数据查询

### 🔧 Web 界面查看
- 启动本地服务器
- 实时刷新（30秒）
- 响应式设计

## 使用方法

### 命令行工具

```bash
# 查看今日统计
token-tracker today

# 查看本周统计
token-tracker w

# 查看累计统计
token-tracker a

# 查看历史记录
token-tracker h

# 查看节省建议
token-tracker s

# 交互式菜单
token-tracker i

# 导出数据
token-tracker export

# 清理历史
token-tracker cleanup

# 重置数据
token-tracker reset
```

### npm scripts

```bash
cd ~/.openclaw/skills/token-tracker

npm run token:today    # 查看今日统计
npm run token:w        # 查看本周统计
npm run token:a        # 查看累计统计
npm run token:h        # 查看历史记录
npm run token:s        # 查看节省建议
npm run token:i        # 交互式菜单
npm run token:export   # 导出数据
npm run token:cleanup  # 清理历史
npm run token:reset    # 重置数据
npm run token:dashboard # 启动仪表板
npm run token:models   # 查看模型信息
npm run token:recommend # 获取推荐
npm run token:optimize # 优化建议
```

### 快捷键支持

#### Linux/macOS
```bash
# 设置快捷键
npm run token:shortcuts

# 快捷键列表
Ctrl+T: 查看今日统计
Ctrl+W: 查看本周统计
Ctrl+A: 查看累计统计
Ctrl+H: 查看历史记录
Ctrl+S: 查看节省建议
Ctrl+I: 交互式菜单
```

#### Windows
```bash
# 设置快捷键
npm run token:shortcuts

# 需要安装 AutoHotkey，然后运行生成的脚本
```

### Web 仪表板

启动可视化仪表板查看实时数据：

```bash
# 启动仪表板
npm run token:dashboard

# 访问地址
http://localhost:3000
```

#### 功能特性
- 📊 实时统计（今日/本周）
- 📈 趋势图表
- 📊 模型分布图
- 📜 历史记录
- 💡 节省建议
- ⚡ 自动刷新（30秒）

## 数据存储

Token 数据存储在 `~/.openclaw/skills/token-tracker/data/token-history.json`

## 节省 Token 的建议

- 使用 `memory_search` 而不是重复搜索
- 使用 `memory_get` 获取特定部分
- 避免重复读取 MEMORY.md
- 合并多个工具调用
- 减少日志输出
- 使用更精确的搜索词
- 定期清理不必要的历史

## 注意事项

1. Token 记录是近似值，可能略有偏差
2. 不同模型的 token 消耗不同
3. 建议定期备份 token 历史数据
4. 快捷键需要在系统设置中手动配置（部分系统）

## 技术栈

- TypeScript
- Node.js
- Express

## 许可证

MIT

## 贡献

欢迎提交 Issue 和 Pull Request！

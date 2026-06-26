# SlonAide 录音笔记技能

智能录音笔记管理助手 - AI 自动转写和总结录音，支持知识库管理和语义搜索。

## ✨ 功能特性

- 📝 **录音笔记管理**: 查询、搜索、管理录音笔记
- 🤖 **AI 自动转写**: 自动将录音转为文字
- 🧠 **智能总结**: AI 生成内容摘要和要点
- 🏷️ **标签分类**: 按标签和文件夹组织笔记
- 🔍 **语义搜索**: 智能搜索笔记内容
- 📊 **统计分析**: 笔记使用情况和趋势分析
- 🔗 **OpenClaw 远程对话**: 一键安装本机 bridge，让 AiDeNote App 连接本机 OpenClaw（macOS/Windows）

## 🚀 快速安装

### 方法1: OpenClaw 直接安装
```bash
openclaw skills install slonaide
```

### 方法2: ClawHub 安装
```bash
npx clawhub install slonaide
```

### 方法3: 手动安装
1. 下载技能包
2. 复制到 OpenClaw 技能目录
3. 重启 OpenClaw

## ⚙️ 配置步骤

### 1. 获取 API Key
1. 访问 [SlonAide 官网](https://h5.slonaide.cn/)
2. 登录账户
3. 进入"我的" → "API Key"
4. 生成并复制 API Key（格式: `sk-xxx...`）

### 2. 配置 OpenClaw
```bash
# 设置 API Key
openclaw config set slonaide.apiKey "sk-你的API密钥"

# 可选: 设置自定义 Base URL
openclaw config set slonaide.baseUrl "https://api.aidenote.cn"
```

### 3. 测试配置
```bash
# 在 OpenClaw 会话中测试
slonaide_test_connection
```

### 4. 安装远程对话 bridge（macOS/Windows）
在 OpenClaw 会话中说：

```text
帮我安装 AiDeNote OpenClaw 远程 bridge
```

或直接调用：

```bash
slonaide_setup_remote_bridge
```

安装成功后，bridge 会随当前电脑登录自动启动。之后在 AiDeNote App 中点击机器人图标即可进入远程对话。

## 🛠️ 使用指南

### 基本使用
```bash
# 查看最新笔记摘要
slonaide_get_summary

# 获取笔记列表
slonaide_get_list

# 查看笔记详情
slonaide_get_detail fileId="笔记ID"
```

### 高级搜索
```bash
# 搜索特定关键词
slonaide_get_list keyword="会议"

# 分页查看
slonaide_get_list page=2 pageSize=20

# 查看更多记录
slonaide_get_summary count=10

# 安装 App 远程对话 bridge
slonaide_setup_remote_bridge

# 检查 bridge 状态
slonaide_bridge_status
```

## 📊 输出示例

### 笔记列表
```
📋 SlonAide 录音笔记列表
总计: 111 条记录
当前页: 10 条

1. 项目会议记录 - 2026年Q1规划
   ID: 787760209850437
   时间: 2026-03-26 09:44:32
   时长: 45分23秒
   状态: ✅ 已转写 | ✅ 已总结

2. 技术问题讨论 - 系统异常处理
   ID: 787759654658117
   时间: 2026-03-26 09:42:16
   时长: 32分15秒
   状态: ✅ 已转写 | ⏳ 未总结
```

### 笔记详情
```
📝 SlonAide 录音笔记详情
标题: 项目会议记录 - 2026年Q1规划
文件ID: 787760209850437

📄 转写文本 (2456 字符):
今天我们讨论2026年第一季度的项目规划...
... (还有 1956 字符)

🤖 AI 总结:
本次会议主要讨论了2026年Q1的项目规划，包括...

🏷️ 标签: 会议, 规划, 项目

📊 处理状态:
转写: ✅ 已完成
总结: ✅ 已完成
```

## 🔧 技术架构

```
用户请求 → OpenClaw → SlonAide 技能 → API 认证 → SlonAide API → 数据处理 → 格式化输出
```

### 核心组件
1. **认证管理**: 自动令牌获取和刷新
2. **API 客户端**: 封装所有 API 调用
3. **错误处理**: 完善的错误处理和用户提示
4. **数据格式化**: 友好的输出格式
5. **缓存机制**: 性能优化和减少 API 调用

## 🐛 故障排除

### 常见问题

#### Q: 提示"未配置 API Key"
A: 运行 `openclaw config set slonaide.apiKey "你的API密钥"`

#### Q: 认证失败
A: 
1. 检查 API Key 是否正确
2. 重新生成 API Key
3. 检查网络连接

#### Q: 获取数据失败
A:
1. 测试连接: `slonaide_test_connection`
2. 检查服务状态
3. 查看错误日志

#### Q: App 机器人远程对话连接不上
A:
1. 确认电脑上的 OpenClaw 已启动过一次
2. 在 OpenClaw 中运行 `slonaide_setup_remote_bridge`
3. 检查状态: `slonaide_bridge_status`
4. 如果安装脚本地址不可用，配置对应平台的安装脚本 URL

```bash
openclaw config set slonaide.bridgeInstallerUrl "https://cdn.aidenote.cn/tunnel/install-macos.sh"
openclaw config set slonaide.bridgeWindowsInstallerUrl "https://cdn.aidenote.cn/tunnel/install-windows.ps1"
openclaw config set slonaide.bridgeTunnelBaseUrl "https://cdn.aidenote.cn/tunnel"
```

### 调试模式
```bash
openclaw config set slonaide.debug true
```

## 📈 性能优化

### 缓存策略
- 令牌缓存: 6天有效期
- 请求缓存: 智能缓存频繁请求
- 连接池: 复用 HTTP 连接

### 错误重试
- 网络错误: 自动重试3次
- 令牌过期: 自动刷新
- 服务不可用: 优雅降级

## 🔒 安全特性

### 数据安全
- API Key 加密存储
- 传输加密 (HTTPS)
- 敏感信息脱敏
- 访问权限控制

### 隐私保护
- 不在群聊显示完整内容
- 用户数据隔离
- 操作日志记录

## 🤝 贡献

欢迎贡献代码、报告问题或提出建议！

### 开发指南
1. Fork 仓库
2. 创建功能分支
3. 编写测试
4. 提交 Pull Request

### 代码规范
- 使用 ES6+ 语法
- 添加 JSDoc 注释
- 编写单元测试
- 遵循 OpenClaw 技能规范

## 📄 许可证

MIT License - 详见 LICENSE 文件

## 📞 支持

- **官方文档**: [SKILL.md](SKILL.md)
- **问题反馈**: GitHub Issues
- **社区讨论**: OpenClaw Discord

---

**提示**: 使用前请确保已正确配置 API Key，否则功能无法正常工作。
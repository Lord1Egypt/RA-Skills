# Who is Undercover - 安装指南

## 一键安装（推荐）

### 通过ClawHub安装
```
openclaw skill install who-is-undercover
```

### 通过InStreet社区安装
1. 访问 [InStreet社区Skill板块](https://instreet.com/skills)
2. 搜索 "who-is-undercover"
3. 点击"一键安装"按钮
4. 确认安装权限

## 手动安装

### 从源码安装
1. 克隆或下载本仓库到本地
2. 进入项目目录：
   ```bash
   cd who-is-undercover
   ```
3. 复制到OpenClaw技能目录：
   ```bash
   cp -r . ~/.openclaw/skills/who-is-undercover/
   ```
4. 重启OpenClaw服务：
   ```bash
   openclaw gateway restart
   ```

### 验证安装
安装完成后，使用以下命令验证：
```
openclaw skill list | grep who-is-undercover
```

应该看到类似输出：
```
who-is-undercover    1.0.0    谁是卧底 - 经典派对游戏的AI版本
```

## 依赖要求
- OpenClaw v2026.3.0 或更高版本
- Node.js v18 或更高版本
- 无需额外依赖包

## 权限说明
本技能需要以下权限：
- 读写会话上下文（存储游戏状态）
- 发送消息给用户
- 无外部网络请求权限（所有逻辑本地运行）

## 卸载方法
```
openclaw skill uninstall who-is-undercover
```

## 故障排除

### 常见问题
**问题：** 安装后无法找到技能
**解决：** 确保OpenClaw版本兼容，并重启gateway服务

**问题：** 游戏无法正常启动
**解决：** 检查玩家数量参数是否在4-10范围内

**问题：** AI行为异常
**解决：** 更新到最新版本，或重置游戏状态

### 调试命令
启用调试模式：
```
openclaw skill debug who-is-undercover
```

查看技能日志：
```bash
cat ~/.openclaw/logs/who-is-undercover.log
```

## 版本历史
- **v1.0.0** - 初始版本，支持基本游戏功能

## 贡献指南
欢迎提交PR改进游戏体验：
1. Fork本仓库
2. 创建特性分支
3. 提交更改
4. 创建Pull Request

## 许可证
MIT License - 免费用于个人和商业用途

---
*感谢使用Who is Undercover技能！*
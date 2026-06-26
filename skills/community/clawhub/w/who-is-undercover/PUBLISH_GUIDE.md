# Who is Undercover - 发布指南

## 📦 发布包内容

- **压缩包**: `who-is-undercover-v1.0.0.zip` (25KB)
- **包含文件**: 所有必需的技能文件（SKILL.md, index.js, game_logic.js, README.md等）
- **排除文件**: 临时文件、日志文件、node_modules等

## 🚀 ClawHub发布步骤

### 1. 安装ClawHub CLI
```bash
npm install -g clawhub
```

### 2. 登录ClawHub
```bash
# 浏览器方式（推荐）
clawhub login

# 或者使用API token（headless方式）
clawhub login --token clh_your_api_token
```

### 3. 验证登录状态
```bash
clawhub whoami
```

### 4. 发布技能包
```bash
# 解压发布包
unzip who-is-undercover-v1.0.0.zip -d who-is-undercover

# 发布到ClawHub
clawhub publish who-is-undercover --version 1.0.0
```

### 5. 同步本地安装
```bash
clawhub sync
```

### 6. 验证安装
```bash
# 列出已安装的技能
clawhub list

# 测试技能
openclaw skill install who-is-undercover
/skill who-is-undercover start
```

## 🔧 InStreet社区发布步骤（待网站恢复）

### 1. 访问InStreet开发者中心
- 网站: https://instreet.coze.site (等待恢复)
- 登录开发者账号

### 2. 创建新技能
- 点击"创建技能"按钮
- 填写技能信息：
  - 名称: who-is-undercover
  - 描述: 谁是卧底 - 经典社交推理游戏的AI版本
  - 分类: 游戏
  - 版本: 1.0.0

### 3. 上传技能包
- 选择 `who-is-undercover-v1.0.0.zip` 文件
- 确认上传

### 4. 提交审核
- 填写审核说明
- 提交技能审核

### 5. 发布上线
- 审核通过后，技能将自动上线
- 用户可以通过InStreet一键安装

## 📋 发布验证清单

- [ ] ClawHub CLI已安装
- [ ] 已成功登录ClawHub
- [ ] 技能包已解压到正确目录
- [ ] 发布命令执行成功
- [ ] 本地安装同步完成
- [ ] 技能功能测试通过
- [ ] 文档链接正常

## 🆘 故障排除

### 常见问题

**Q: ClawHub登录失败**
A: 确保网络连接正常，或使用API token方式进行headless登录

**Q: 发布时出现权限错误**
A: 确保已正确登录，并且技能名称未被占用

**Q: 技能安装后无法使用**
A: 检查OpenClaw版本兼容性，确保v2026.3.0+

**Q: 文件大小超限**
A: 当前包大小25KB，远低于50MB限制，不会出现此问题

### 调试命令

```bash
# 查看技能详情
clawhub inspect who-is-undercover

# 重新发布（如果需要）
clawhub publish who-is-undercover --version 1.0.1

# 卸载技能
clawhub uninstall who-is-undercover
```

## 📞 支持联系

- **GitHub Issues**: https://github.com/long5/who-is-undercover/issues
- **Discord**: https://discord.com/invite/clawd
- **Email**: long5@example.com

## 📄 许可证

MIT License - 免费用于个人和商业项目

---
*最后更新: 2026-03-28*
*版本: v1.0.0*
# 发布到 ClawHub 指南

## 准备完成 ✅

技能文件已准备好，位于：
- 目录：`~/.openclaw/skills/telegram-qq-bridge/`
- 压缩包：`~/.openclaw/skills/telegram-qq-bridge.tar.gz`

## 发布步骤

### 方法 1：通过 ClawHub 网页上传（推荐）

1. **访问 ClawHub**
   - 打开浏览器访问：https://clawhub.ai/skills/new

2. **填写技能信息**
   ```
   名称：telegram-qq-bridge
   描述：Telegram → QQ 自动转发技能
   版本：1.0.0
   分类：Communication
   标签：telegram, qq, forward, bridge, automation
   ```

3. **上传文件**
   - 选择文件：`~/.openclaw/skills/telegram-qq-bridge.tar.gz`
   - 或直接上传整个目录

4. **提交审核**
   - 确认信息无误
   - 点击"发布"按钮

### 方法 2：使用 ClawHub CLI（如果支持）

```bash
# 安装 clawhub CLI（如果需要）
npm install -g @clawhub/cli

# 登录
clawhub login

# 发布技能
cd ~/.openclaw/skills/telegram-qq-bridge/
clawhub publish
```

### 方法 3：使用 Git（如果有仓库）

```bash
cd ~/.openclaw/skills/telegram-qq-bridge/

# 推送到远程仓库
git remote add origin https://github.com/your-repo/telegram-qq-bridge.git
git push -u origin main

# 然后在 ClawHub 中导入仓库
```

## 技能信息

### 基本信息
- **名称**: telegram-qq-bridge
- **版本**: 1.0.0
- **描述**: Telegram 群组消息自动转发到 QQ
- **作者**: OpenClaw Community
- **许可证**: MIT

### 功能特性
- ✅ 自动监听 Telegram 群组消息
- ✅ 自动转发到 QQ
- ✅ 事件驱动，无轮询
- ✅ Node.js 实现
- ✅ OpenClaw 插件集成
- ✅ 支持配置文件和环境变量

### 系统要求
- OpenClaw >= 2026.5.2
- Node.js >= 14.0.0
- QQ Bot 账号
- Telegram Bot

### 配置项
```json
{
  "qqTarget": "qqbot:c2c:YOUR_OPENID",
  "qqAccount": "your_qq_account",
  "pollInterval": 2000
}
```

### 环境变量
```bash
QQ_TARGET="qqbot:c2c:YOUR_OPENID"
QQ_ACCOUNT="your_qq_account"
POLL_INTERVAL="2000"
```

## 文件清单

```
telegram-qq-bridge/
├── index.js                 # 主程序（Node.js）
├── package.json            # 包配置
├── config.example.json     # 配置模板
├── SKILL.md               # 技能定义
├── README.md              # 使用说明
├── QUICKSTART.md          # 快速参考
├── LICENSE                # MIT 许可证
├── .gitignore            # Git 忽略文件
└── PUBLISH.md            # 本文件
```

## 测试清单

发布前请确认：

- [x] 敏感信息已脱敏
- [x] 配置文件已模板化
- [x] 文档完整
- [x] 许可证已添加
- [x] Git 提交完成
- [ ] 功能测试通过
- [ ] 文档测试通过
- [ ] 兼容性测试通过

## 发布后

### 验证
1. 在 ClawHub 搜索技能
2. 查看技能详情页
3. 确认信息正确

### 安装测试
```bash
# 从 ClawHub 安装
openclaw skill install telegram-qq-bridge

# 验证安装
ls -la ~/.openclaw/skills/telegram-qq-bridge/
```

### 使用测试
1. 配置技能
2. 启动技能
3. 发送测试消息
4. 验证转发功能

## 常见问题

### Q: 发布失败怎么办？
A: 检查文件格式、大小是否符合要求，网络是否正常。

### Q: 技能审核需要多久？
A: 通常 1-3 个工作日。

### Q: 如何更新技能？
A: 在 ClawHub 中提交新版本，版本号递增。

### Q: 如何删除已发布的技能？
A: 在技能详情页点击"删除"或联系管理员。

## 相关链接

- [ClawHub 主页](https://clawhub.ai)
- [技能开发指南](https://docs.openclaw.ai/skills/develop)
- [技能发布指南](https://docs.openclaw.ai/skills/publish)
- [OpenClaw 文档](https://docs.openclaw.ai)

## 联系支持

如有问题，请：
1. 查看文档：https://docs.openclaw.ai
2. 提交 Issue: https://github.com/your-repo/telegram-qq-bridge/issues
3. 加入社区：https://discord.gg/clawhub

---

**最后更新**: 2026-05-17  
**版本**: 1.0.0  
**状态**: 准备发布 ✅

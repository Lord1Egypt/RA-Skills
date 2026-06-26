# ❓ 常见问题解答 (FAQ)

## 安装相关

### Q1: 如何检查是否安装成功？

```bash
xhs-cli --version
xhs-cli check-login
```

如果能正常输出版本号和登录状态，说明安装成功。

### Q2: 提示 "command not found: xhs-cli"

**原因**：
1. npm 全局安装路径未加入 PATH
2. 或者使用的是本地安装（未全局安装）

**解决**：

```bash
# 方案 1：全局安装
npm install -g xiaohongshu-mcp-node-skill

# 方案 2：使用本地安装
cd xiaohongshu-mcp-node-skill
node scripts/xhs-cli.js --help

# 方案 3：添加 npm 路径到 PATH（macOS/Linux）
echo 'export PATH="$(npm config get prefix)/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### Q3: Node.js 版本不符合要求

**要求**：Node.js >= 20.0.0

**解决**：

```bash
# 使用 nvm 安装最新版本
nvm install 20
nvm use 20

# 或从官网下载：https://nodejs.org/
```

## 登录相关

### Q4: 二维码无法显示

**原因**：终端不支持图片显示

**解决**：

1. 输出中包含 Base64 编码的二维码
2. 将 `qrcode` 字段的内容保存为图片
3. 或使用支持图片的终端（如 iTerm2）

### Q5: 扫码后提示登录失败

**可能原因**：
- 二维码已过期（4分钟有效期）
- 网络连接问题
- 小红书服务器问题

**解决**：
```bash
# 重新获取二维码
xhs-cli login
```

### Q6: Cookie 文件在哪里？

**默认位置**：`./cookies.json`

**自定义位置**：
```bash
export COOKIES_PATH="/path/to/cookies.json"
```

## 发布相关

### Q7: 标题超过长度限制

**限制**：20个字（中文字符计1个，英文字符计0.5个）

**解决**：
- 缩短标题
- 使用更简洁的表达

### Q8: 图片上传失败

**检查清单**：
- ✅ 图片路径是否正确
- ✅ 图片格式是否支持（JPG/PNG/GIF）
- ✅ 图片大小是否超限（单张 < 10MB）
- ✅ 网络连接是否正常

**解决**：
```bash
# 检查图片
file /path/to/image.jpg
ls -lh /path/to/image.jpg

# 压缩图片（如果过大）
# macOS
sips -Z 1920 /path/to/image.jpg

# Linux
convert /path/to/image.jpg -resize 1920x1920 /path/to/image-compressed.jpg
```

### Q9: 视频上传很慢

**正常现象**：视频上传通常需要 5-10 分钟

**建议**：
- 使用较小的视频文件（< 500MB）
- 确保网络连接稳定
- 耐心等待上传完成

### Q10: 发布后在小红书看不到

**可能原因**：
- 内容正在审核中
- 内容违反社区规范被拒绝
- 设置为"仅自己可见"

**检查**：
1. 在小红书 App 中查看"我的"页面
2. 检查是否有审核通知
3. 确认可见范围设置

## 搜索和互动

### Q11: 搜索结果为空

**可能原因**：
- 关键词太具体
- 小红书上确实没有相关内容

**建议**：
- 使用更通用的关键词
- 尝试不同的搜索词

### Q12: 评论/点赞失败

**可能原因**：
- 未登录或 Cookie 过期
- feed-id 或 xsec-token 错误
- 网络问题

**解决**：
```bash
# 1. 检查登录状态
xhs-cli check-login

# 2. 如果未登录，重新登录
xhs-cli login

# 3. 确认 feed-id 和 xsec-token 正确
# 这两个参数从搜索结果中获取
```

## 性能和稳定性

### Q13: 命令执行很慢

**正常现象**：浏览器自动化需要时间

**预期时间**：
- 登录检查：5-10秒
- 搜索：10-15秒
- 发布图文：30-60秒
- 发布视频：5-10分钟

### Q14: 浏览器自动化失败

**可能原因**：
- 小红书页面结构变化
- Playwright 版本过旧
- 系统资源不足

**解决**：
```bash
# 更新到最新版本
npm update -g xiaohongshu-mcp-node xiaohongshu-mcp-node-skill

# 重新安装浏览器
npx playwright install chromium
```

### Q15: 内存占用过高

**原因**：Chromium 浏览器占用内存

**解决**：
- 使用无头模式（默认已启用）
- 操作完成后浏览器会自动关闭
- 如果持续占用，重启系统

## OpenClaw 集成

### Q16: OpenClaw 无法识别 Skill

**解决**：
```bash
# 刷新 Skill 列表
openclaw skills refresh

# 检查 Skill 状态
openclaw skills info xiaohongshu-mcp-node

# 查看日志
openclaw logs
```

### Q17: AI 不会自动调用 Skill

**可能原因**：
- Skill 未启用
- 触发关键词不匹配
- OpenClaw 配置问题

**解决**：
1. 确认 Skill 已启用：`openclaw skills list --enabled`
2. 使用明确的触发词："发布到小红书"、"搜索小红书"
3. 检查 OpenClaw 配置文件

## 安全和隐私

### Q18: Cookie 文件安全吗？

**安全措施**：
- Cookie 仅存储在本地
- 不会上传到任何服务器
- 建议设置文件权限：`chmod 600 cookies.json`

### Q19: 会不会被小红书封号？

**风险**：
- 正常使用不会被封号
- 过于频繁的操作可能触发风控

**建议**：
- 合理控制操作频率
- 不要批量发布相似内容
- 遵守小红书社区规范

### Q20: 数据会被收集吗？

**承诺**：
- ❌ 不会收集任何用户数据
- ❌ 不会上传到第三方服务器
- ✅ 所有操作仅在本地执行
- ✅ 开源代码，可审计

## 获取帮助

### 还有其他问题？

1. 📖 查看 [SKILL.md](../SKILL.md) 完整文档
2. 🐛 [提交 Issue](https://github.com/sipingme/xiaohongshu-mcp-node-skill/issues)
3. 💬 [参与讨论](https://github.com/sipingme/xiaohongshu-mcp-node-skill/discussions)
4. 📧 联系作者：sipingme@gmail.com

---

**问题解决了吗？如果没有，欢迎提交 Issue！** 🤝

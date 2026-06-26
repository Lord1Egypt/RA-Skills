# 📋 Windows TTS 发布到 ClawHub - 快速指南

## 🎯 一句话总结

将你的 **Windows TTS 跨设备播报系统** 发布到 ClawHub，让全球 OpenClaw 用户都能使用！

---

## ✅ 发布前检查

### 1. 登录 ClawHub

```bash
# 浏览器登录（推荐）
clawhub login

# 或使用 Token
clawhub login --token YOUR_API_TOKEN
```

### 2. 验证登录

```bash
clawhub whoami
```

看到你的用户名表示登录成功 ✅

### 3. 确认文件完整

```bash
ls /home/cmos/skills/windows-tts/
```

**必需文件**：
- ✅ `SKILL.md` - 主文档
- ✅ `package.json` - NPM 配置
- ✅ `dist/` - 编译输出
- ✅ `index.ts` - 入口文件

---

## 🚀 发布（两种方式）

### 方式 A：使用发布脚本（推荐）

```bash
cd /home/cmos/skills/windows-tts
./publish.sh
```

脚本会自动：
- 检查登录状态
- 验证必需文件
- 重新编译
- 执行发布

### 方式 B：手动发布

```bash
cd /home/cmos/skills
clawhub publish windows-tts \
  --slug windows-tts \
  --name "Windows TTS Notification" \
  --version 1.0.0 \
  --tags "latest,tts,notification,windows,azure,broadcast,reminder" \
  --changelog "Initial release: Cross-device TTS broadcast"
```

---

## ✅ 验证发布

### 1. 搜索技能

```bash
clawhub search windows-tts
```

### 2. 查看详情

```bash
clawhub inspect windows-tts
```

### 3. 测试安装

```bash
clawhub install windows-tts
clawhub list
```

---

## 📊 发布成功后的链接

### 技能页面
```
https://clawhub.ai/skills/windows-tts
```

### 安装命令
```bash
clawhub install windows-tts
```

### 分享文案

```
🎉 新技能发布！

Windows TTS Notification - 跨设备语音播报系统

✅ 家庭提醒（作业、吃药、吃饭）
✅ 支持 Azure TTS 所有音色  
✅ 局域网广播，零延迟
✅ 简单易用，配置灵活

立即安装：clawhub install windows-tts

#OpenClaw #AI #TTS #HomeAutomation
```

---

## 🔄 更新版本

### 发布新版本

```bash
# 1. 更新版本号（package.json 和 _meta.json）
"version": "1.0.1"

# 2. 更新 CHANGELOG.md

# 3. 重新编译
cd /home/cmos/skills/windows-tts
npm run build

# 4. 发布
clawhub publish windows-tts \
  --version 1.0.1 \
  --changelog "Bug fixes and improvements"
```

---

## 🛠️ 常见问题

### ❌ 错误：Slug 已被占用

```bash
# 使用不同的 slug
clawhub publish windows-tts \
  --slug windows-tts-broadcast \
  --name "Windows TTS Broadcast"
```

### ❌ 错误：未登录

```bash
clawhub login
```

### ❌ 错误：缺少 dist/

```bash
cd /home/cmos/skills/windows-tts
npm run build
```

### ❌ 错误：版本已存在

```bash
# 更新版本号后重新发布
# package.json: "version": "1.0.1"
# _meta.json: "version": "1.0.1"
clawhub publish windows-tts --version 1.0.1
```

---

## 📝 发布清单

### 发布前
- [ ] 已登录 ClawHub
- [ ] 文件完整（SKILL.md, package.json, dist/）
- [ ] TypeScript 编译通过
- [ ] 功能测试通过
- [ ] 文档完整

### 发布后
- [ ] 技能页面可访问
- [ ] 可以搜索到
- [ ] 可以安装
- [ ] 安装后可用

---

## 📞 获取帮助

- **ClawHub 文档**: https://clawhub.ai/docs
- **社区**: OpenClaw Discord/Telegram
- **问题**: GitHub Issues

---

## 🎊 恭喜！

发布成功后，全球 OpenClaw 用户都可以：
- 🔍 搜索到你的技能
- 📥 一键安装使用
- ⭐ 收藏和评分
- 💬 留下反馈

**你的技能将帮助成千上万的家庭建立智能播报系统！** 🚀

---

**最后更新**: 2026-03-15  
**版本**: 1.0.0  
**作者**: cmos

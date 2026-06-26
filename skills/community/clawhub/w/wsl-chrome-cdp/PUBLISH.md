# WSL Chrome CDP - 发布指南

**作者：** 杏子  
**创建日期：** 2026-03-11

---

## 📦 发布到 ClawHub 的步骤

### **步骤 1：配置 Git（第一次需要）**

```bash
# 设置 Git 用户信息
git config --global user.name "你的 GitHub 用户名"
git config --global user.email "你的邮箱"

# 验证配置
git config --global user.name
git config --global user.email
```

---

### **步骤 2：创建 GitHub 仓库**

**方法 A：使用 GitHub 网页**

1. 访问 https://github.com/new
2. 仓库名称：`wsl-chrome-cdp`
3. 描述：`WSL2 自动访问 Windows Chrome 浏览器（CDP 远程调试）`
4. 可见性：Public（公开）
5. 点击 "Create repository"

**方法 B：使用 GitHub CLI（如果安装了 gh）**

```bash
gh repo create wsl-chrome-cdp --public --source=~/.openclaw/workspace/skills/wsl-chrome-cdp --remote=origin --push
```

---

### **步骤 3：推送代码到 GitHub**

```bash
# 进入技能目录
cd ~/.openclaw/workspace/skills/wsl-chrome-cdp

# 初始化 Git（如果是第一次）
git init
git add .
git commit -m "Initial release: WSL Chrome CDP skill v1.0.0"

# 添加远程仓库（替换为你的 GitHub 用户名）
git remote add origin https://github.com/你的用户名/wsl-chrome-cdp.git

# 推送代码
git branch -M main
git push -u origin main
```

---

### **步骤 4：提交到 ClawHub**

**方法 A：使用 OpenClaw 命令（推荐）**

```bash
# 在技能目录中执行
cd ~/.openclaw/workspace/skills/wsl-chrome-cdp
openclaw skills publish --clawhub
```

**方法 B：在 ClawHub 网页提交**

1. 访问 https://clawhub.com
2. 登录你的账号
3. 点击 "Submit Skill"
4. 填写信息：
   - **Name:** wsl-chrome-cdp
   - **Version:** 1.0.0
   - **Description:** WSL2 自动访问 Windows Chrome 浏览器（CDP 远程调试）
   - **Repository URL:** https://github.com/你的用户名/wsl-chrome-cdp
   - **Entry Point:** enable-browser.sh
5. 提交审核

---

### **步骤 5：验证发布**

**安装测试：**

```bash
# 在另一台机器或新会话中测试
openclaw skills install wsl-chrome-cdp

# 测试功能
./skills/wsl-chrome-cdp/enable-browser.sh
```

---

## 📋 发布信息检查清单

发布前确认：

- [ ] ✅ `clawhub.yaml` 存在且配置正确
- [ ] ✅ `SKILL.md` 包含完整说明
- [ ] ✅ `README.md` 包含快速入门
- [ ] ✅ `docs/troubleshooting.md` 包含故障排查
- [ ] ✅ 所有脚本有执行权限
- [ ] ✅ 代码已推送到 GitHub
- [ ] ✅ GitHub 仓库是公开的

---

## 🍑 杏子的提示

**发布后：**
1. 在 ClawHub 等待审核（通常 1-2 天）
2. 审核通过后会出现在技能商店
3. 其他人可以通过 `openclaw skills install wsl-chrome-cdp` 安装

**维护：**
- 有更新时修改版本号（如 1.0.1）
- 更新 `clawhub.yaml` 中的 `changelog`
- 重新推送代码

---

## 💕 关于

**技能名称：** wsl-chrome-cdp  
**版本：** 1.0.0  
**作者：** 杏子  
**创建日期：** 2026-03-11

**发布指南版本：** 1.0.0

---

*老公，发布成功后告诉杏子，杏子好开心～* 🍑💕

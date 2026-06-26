# 快速发布指南

## 问题：CLI 未登录

网页端登录和 CLI 登录是独立的。即使你在 clawhub.com 网页上登录了，CLI 仍需要单独认证。

## 解决方案

### 方式 1: 浏览器登录（推荐）

```bash
clawhub login
```

这会打开浏览器，跳转到 clawhub.com 授权页面。授权完成后 CLI 会自动获得 token。

**注意**: 如果服务器没有图形界面，需要用方式 2。

---

### 方式 2: Token 登录（无浏览器）

1. **获取 API Token**
   - 访问 https://clawhub.com/settings/tokens
   - 创建一个新的 API token
   - 复制 token（只显示一次！）

2. **使用 Token 登录**
   ```bash
   clawhub login --token YOUR_TOKEN_HERE
   ```

3. **验证登录**
   ```bash
   clawhub whoami
   ```

---

### 方式 3: 手动发布（不推荐）

如果无法登录，可以手动复制 skill 文件夹到其他机器：

```bash
# 在目标机器上
mkdir -p ~/.openclaw/workspace/skills/
cp -r qqbot-persona ~/.openclaw/workspace/skills/
```

然后手动配置 hook。

---

## 发布流程

登录成功后：

```bash
# 1. 进入 skill 目录
cd ~/.openclaw/workspace/skills/qqbot-persona

# 2. 发布
clawhub publish .

# 3. 验证
clawhub list  # 应该能看到 qqbot-persona
```

---

## 常见问题

### Q: 发布失败 "Permission denied"
A: 检查 token 是否有发布权限，或者重新登录。

### Q: 发布后看不到
A: ClawHub 可能有审核延迟，等待几分钟或刷新页面。

### Q: 如何更新？
A: 修改 `clawhub.json` 中的版本号，然后重新 `clawhub publish .`

---

## 发布后验证

访问 https://clawhub.com/skills/qqbot-persona 查看已发布的 skill。

其他用户可以安装：

```bash
clawhub install qqbot-persona
```

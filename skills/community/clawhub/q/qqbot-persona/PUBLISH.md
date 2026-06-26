# 发布指南 - qqbot-persona

## 发布到 ClawHub

### 1. 登录 ClawHub

```bash
clawhub login
```

这会打开浏览器，使用 GitHub 账号登录 clawhub.com。

### 2. 发布 Skill

```bash
cd ~/.openclaw/workspace/skills/qqbot-persona
clawhub publish .
```

或者从任意目录：

```bash
clawhub publish ~/.openclaw/workspace/skills/qqbot-persona
```

### 3. 验证发布

访问 https://clawhub.com/skills/qqbot-persona 查看已发布的 skill。

---

## 手动安装（不发布）

如果不发布到 ClawHub，其他用户可以手动复制：

```bash
# 在目标机器上
git clone <repo_url> ~/.openclaw/workspace/skills/qqbot-persona
# 或手动复制文件夹
```

然后配置 hook 即可使用。

---

## 更新 Skill

修改后重新发布：

```bash
clawhub publish ~/.openclaw/workspace/skills/qqbot-persona
```

ClawHub 会自动检测版本变化并更新。

---

## 版本管理

在 `clawhub.json` 中更新版本号：

```json
{
  "version": "1.0.1",  // 修改这里
  ...
}
```

然后在 `changelog` 中添加更新记录。

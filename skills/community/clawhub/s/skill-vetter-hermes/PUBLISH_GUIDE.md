# 🚀 发布 Skill Vetter 到 ClawdHub

## 📋 发布步骤

### 1️⃣ 登录 ClawdHub

打开浏览器访问：
```
https://clawhub.ai/cli/auth
```

或者运行：
```bash
clawhub login
```

**注意**: 登录后 token 会保存到 `C:\Users\atlas\.clawhub\token`

---

### 2️⃣ 验证登录

```bash
clawhub whoami
```

**预期输出**:
```
Logged in as: [your-username]
```

---

### 3️⃣ 发布技能

```bash
clawhub publish C:\Users\atlas\.openclaw\workspace\skills\skill-vetter
```

**预期输出**:
```
Publishing skill-vetter...
✅ Published: clawhub/community/skill-vetter
```

---

### 4️⃣ 验证发布

```bash
clawhub inspect clawhub/community/skill-vetter
```

---

## 📦 技能信息

| 项目 | 值 |
|------|-----|
| **名称** | skill-vetter |
| **版本** | 1.2.0 |
| **描述** | Security-first skill vetting for AI agents |
| **作者** | 十三香小精灵 |
| **许可** | MIT |

---

## 🔧 手动发布 (如果 CLI 失败)

### 方法 1: 通过 GitHub

1. 将技能推送到 GitHub:
   ```bash
   git add .
   git commit -m "Add skill-vetter v1.2.0"
   git push origin main
   ```

2. 在 ClawdHub 网站手动添加:
   - 访问 https://clawhub.ai
   - 点击 "Add Skill"
   - 输入 GitHub 仓库 URL
   - 填写元数据

### 方法 2: 通过 API

```bash
curl -X POST https://api.clawhub.ai/skills \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "skill-vetter",
    "version": "1.2.0",
    "description": "Security-first skill vetting",
    "repository": "https://github.com/openclaw/skills",
    "path": "skills/skill-vetter"
  }'
```

---

## 🎯 发布后

发布成功后，其他 agent 可以：

```bash
# 搜索技能
clawhub search "security vetting"

# 安装技能
clawhub install clawhub/community/skill-vetter

# 查看技能详情
clawhub inspect clawhub/community/skill-vetter
```

---

## 📝 更新日志

### v1.2.0 (2026-04-12)
- ✅ 误报优化 (跳过注释和字符串)
- ✅ 信任分级系统
- ✅ 强制拦截机制
- ✅ 6 种危险模式检测

### v1.1.0 (2026-04-12)
- ✅ 初始版本
- ✅ 基本扫描功能
- ✅ 风险分级

---

## 🆘 常见问题

### Q: 登录失败怎么办？
A: 检查网络连接，确保可以访问 clawhub.ai

### Q: 发布失败怎么办？
A: 检查技能目录结构，确保包含 SKILL.md 和可执行文件

### Q: 如何更新已发布的技能？
A: 修改代码后运行 `clawhub publish` 即可

---

## 🔗 相关链接

- [ClawdHub 官网](https://clawhub.ai)
- [Skill Vetter 文档](./SKILL.md)
- [集成报告](./INTEGRATION_REPORT.md)

---

**最后更新**: 2026-04-12 23:15 GMT+8

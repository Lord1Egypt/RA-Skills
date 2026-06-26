# 🚀 快速发布到 ClawHub

## ⚡ 方法 1：使用发布脚本（最简单）

```bash
cd /home/ubuntu/.openclaw/workspace/skills/restaurant-review-crosscheck
./publish.sh
```

脚本会自动：
1. ✅ 检查环境
2. ✅ 验证登录状态
3. ✅ 显示 skill 信息
4. ✅ 确认发布
5. ✅ 执行发布命令

---

## 📋 方法 2：手动发布

### 第一步：安装 ClawHub CLI

```bash
npm install -g clawhub
```

### 第二步：登录

**选项 A：使用浏览器（推荐）**
```bash
clawhub login
# 浏览器会自动打开，完成登录
```

**选项 B：使用 Token**
```bash
# 1. 访问 https://clawhub.ai 获取 token
# 2. 使用 token 登录
clawhub login --token "YOUR_TOKEN_HERE"
```

### 第三步：发布

```bash
cd /home/ubuntu/.openclaw/workspace/skills/restaurant-review-crosscheck

clawhub publish . \
  --slug restaurant-crosscheck \
  --name "餐厅推荐交叉验证" \
  --version 1.0.0 \
  --changelog "初始版本"
```

---

## ✅ 发布后验证

```bash
# 搜索 skill
clawhub search restaurant-crosscheck

# 查看 skill 详情
clawhub inspect restaurant-crosscheck

# 列出已安装的 skills
clawhub list
```

---

## 📦 Skill 信息

- **Slug**: `restaurant-crosscheck`
- **Name**: 餐厅推荐交叉验证
- **Version**: `1.0.0`
- **Tags**: restaurant, food, recommendation, chinese

---

## 🔄 更新 Skill

如果需要更新：

1. 修改 `SKILL.md` 中的版本号（例如 1.0.0 → 1.0.1）
2. 更新文件
3. 重新发布：

```bash
clawhub publish . \
  --slug restaurant-crosscheck \
  --version 1.0.1 \
  --changelog "修复：优化匹配算法"
```

---

## 📖 详细文档

查看完整的发布指南：

```bash
cat PUBLISH_GUIDE.md
```

---

## ⚠️ 当前限制

**服务器环境**：
- 当前服务器没有浏览器
- 无法使用 `clawhub login` 打开浏览器
- 需要使用 token 或在本地发布

**解决方案**：
1. 在本地电脑发布（推荐）
2. 使用 token 登录
3. 下载 skill 文件夹到本地发布

---

**准备好了吗？运行 `./publish.sh` 开始发布！** 🚀

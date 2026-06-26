# 发布 zopia-skill 到 ClawHub

## 前提条件

- Node.js 已安装（`npx` 可用）
- 已登录 ClawHub（见下文）

## 1. 登录

首次使用需登录：

```bash
npx clawhub login
```

验证登录状态：

```bash
npx clawhub whoami
# ✔ Lambdua
```

登录态会持久化，后续无需重复登录。

## 2. 修改内容并推送 GitHub

修改 `SKILL.md`、脚本等文件后，先 commit & push 到 GitHub：

```bash
git add .
git commit -m "描述本次变更"
git push
```

## 3. 发布新版本到 ClawHub

```bash
npx clawhub publish /path/to/zopia-skills \
  --slug zopia-skill \
  --version <新版本号> \
  --changelog "本次变更说明"
```

**示例：**

```bash
npx clawhub publish /c/code/jobCode/zipia/zopia-skills \
  --slug zopia-skill \
  --version 1.0.3 \
  --changelog "新增 xxx 模型"
```

版本号遵循 semver：
- 新增模型 / 功能 → 次版本号 +1（如 1.0.1 → 1.1.0）
- Bug 修复 / 文档更新 → 补丁号 +1（如 1.0.1 → 1.0.2）

## 4. 验证发布结果

```bash
npx clawhub inspect zopia-skill
```

确认 `Latest` 字段已更新为新版本号。

## 常用命令速查

| 命令 | 说明 |
|------|------|
| `npx clawhub whoami` | 查看当前登录用户 |
| `npx clawhub inspect zopia-skill` | 查看已发布版本信息 |
| `npx clawhub publish <path> --slug zopia-skill --version x.y.z` | 发布新版本 |
| `npx clawhub skill --help` | 管理已发布技能 |

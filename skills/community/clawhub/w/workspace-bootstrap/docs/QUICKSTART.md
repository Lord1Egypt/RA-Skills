# workspace-bootstrap 快速上手教程

> **版本**：v1.0.0
> **预计时间**：5 分钟
> **适用人群**：第一次使用 workspace-bootstrap 的用户

---

## 🎯 教程目标

5 分钟内创建你的第一个 OpenClaw workspace，包含：
- ✅ 完整的目录结构
- ✅ 核心配置文件
- ✅ 坑点检查通过

---

## 📋 准备工作

### 你需要的信息

在开始前，准备好以下信息：

1. **小龙虾名称**（例如：小溪、小智、小艾）
2. **用户名称**（例如：善人、张三）
3. **时区**（例如：Asia/Shanghai、America/New_York）
4. **身份定义**（例如：AI 思维教练、AI 技术助手）
5. **愿景**（例如：成为最靠谱的思维教练）

---

## 🚀 5 分钟快速开始

### 步骤1：下载 workspace-bootstrap（30 秒）

```bash
# 方式1：从 ClawHub 安装（推荐）
clawhub install workspace-bootstrap

# 方式2：从 Git 克隆
git clone https://github.com/your-repo/workspace-bootstrap.git
cd workspace-bootstrap
```

### 步骤2：运行向导（2 分钟）

```bash
# 运行交互式向导
bash scripts/wizard.sh ~/my-workspace
```

按照提示输入信息：

```
1. 你的小龙虾叫什么名字？小溪
2. 你的用户叫什么？善人
3. 你的时区？Asia/Shanghai
4. 你的小龙虾的身份是？AI 思维教练
5. 你的愿景是？成为最靠谱的思维教练

选择配置场景：
  1) 思维教练（高复杂度）- 7 Agents、41 Skills、4 Cron
  2) 技术助手（中复杂度）- 3 Agents、5 Skills、2 Cron
  3) 个人助理（低复杂度）- 3 Agents、2 Skills、2 Cron
请选择 (1-3): 1

确认生成配置？ (y/n): y
```

### 步骤3：检查生成的文件（1 分钟）

```bash
# 进入 workspace
cd ~/my-workspace

# 检查目录结构
ls -la

# 检查核心文件
cat SOUL.md
cat USER.md
```

**预期输出**：
- 10 个目录（agents、memory、skills、user-data、scripts、shared、reports、temp、.learnings、wiki）
- 5 个核心文件（SOUL.md、AGENTS.md、MEMORY.md、USER.md、HEARTBEAT.md）

### 步骤4：运行坑点检查（30 秒）

```bash
# 检查 workspace 是否存在常见问题
bash /path/to/workspace-bootstrap/scripts/check-pitfalls.sh .
```

**预期输出**：
```
✅ 所有检查通过！
```

### 步骤5：开始使用（1 分钟）

```bash
# 1. 编辑 SOUL.md，根据需要调整价值观、红线等
nano SOUL.md

# 2. 编辑 USER.md，补充用户背景信息
nano USER.md

# 3. 测试启动流程（在 OpenClaw 中）
# Read SOUL.md → USER.md → MEMORY.md
```

---

## 🎉 完成！

恭喜！你已经成功创建了第一个 OpenClaw workspace。

### 下一步

1. **阅读使用指南**：[docs/USAGE.md](docs/USAGE.md)
2. **查看示例配置**：[examples/](examples/)
3. **学习核心文件**：[templates/WORKSPACE-TEMPLATE.md](templates/WORKSPACE-TEMPLATE.md)

---

## 📚 进阶教程

### 场景1：团队协作

```bash
# 1. 团队成员 A 创建 workspace
bash scripts/wizard.sh ~/team-workspace

# 2. 推送到 Git
cd ~/team-workspace
git init
git add .
git commit -m "Initial workspace"
git remote add origin <repo-url>
git push -u origin main

# 3. 团队成员 B 克隆
git clone <repo-url> ~/my-workspace

# 4. 团队成员 B 检查配置
bash /path/to/workspace-bootstrap/scripts/check-pitfalls.sh ~/my-workspace
```

### 场景2：自定义扩展

```bash
# 1. 创建基础 workspace
bash scripts/bootstrap.sh ~/custom-workspace

# 2. 添加自定义目录
mkdir -p ~/custom-workspace/custom-plugins
mkdir -p ~/custom-workspace/custom-templates

# 3. 修改 SOUL.md
echo "## 👥 自定义团队成员" >> ~/custom-workspace/SOUL.md
echo "- **custom-agent** 自定义Agent 🎨 — 特殊任务" >> ~/custom-workspace/SOUL.md

# 4. 检查核心结构未被破坏
bash /path/to/workspace-bootstrap/scripts/check-pitfalls.sh ~/custom-workspace
```

### 场景3：快速复刻

```bash
# 1. 在新机器上复刻 workspace
bash scripts/bootstrap.sh ~/new-workspace

# 2. 从旧机器复制自定义配置
scp old-machine:~/workspace/SOUL.md ~/new-workspace/
scp old-machine:~/workspace/USER.md ~/new-workspace/
scp -r old-machine:~/workspace/user-data ~/new-workspace/

# 3. 检查配置完整性
bash /path/to/workspace-bootstrap/scripts/check-pitfalls.sh ~/new-workspace
```

---

## ⚠️ 常见问题

### 问题1：向导运行失败

**错误**：`No such file or directory`

**解决方案**：
```bash
# 检查脚本路径
ls scripts/wizard.sh

# 检查权限
chmod +x scripts/wizard.sh
```

### 问题2：坑点检查发现问题

**错误**：`MEMORY.md 容量爆炸`

**解决方案**：
```bash
# 将详细内容移到 memory/YYYY-MM-DD.md
# 在 MEMORY.md 只保留链接

# 示例：
# MEMORY.md（错误）
# ## 活跃项目
# 项目A：详细描述...（100+ 行）

# MEMORY.md（正确）
# ## 活跃项目
# - [项目A](memory/projects.md#项目A)
```

### 问题3：目录结构不完整

**错误**：`缺少目录 agents/`

**解决方案**：
```bash
# 重新运行 bootstrap
bash scripts/bootstrap.sh .
```

---

## 📖 学习资源

- **使用指南**：[docs/USAGE.md](docs/USAGE.md) - 完整功能说明
- **模板参考**：[templates/WORKSPACE-TEMPLATE.md](templates/WORKSPACE-TEMPLATE.md) - 最佳实践
- **示例配置**：
  - [思维教练](examples/mindset-coach/)
  - [技术助手](examples/tech-assistant/)
  - [个人助理](examples/personal-assistant/)
- **测试报告**：[tests/test-report.md](tests/test-report.md) - 质量验证

---

## 💡 提示

- ✅ **定期运行坑点检查**（每周一次）
- ✅ **保持 MEMORY.md 精简**（< 40 行）
- ✅ **使用 Git 管理配置**（团队协作）
- ✅ **定期备份 workspace**（数据安全）

---

**快速上手教程版本**：v1.0.0
**最后更新**：2026-04-07
**预计完成时间**：5 分钟

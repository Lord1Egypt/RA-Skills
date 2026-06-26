# workspace-bootstrap

> **版本**：v1.0.0
> **成熟度**：L4（可产品化）
> **最后更新**：2026-04-07

---

## 📖 简介

workspace-bootstrap 是一个 OpenClaw workspace 快速初始化工具，帮助你：

- ✅ **5 分钟创建完整 workspace**
- ✅ **3 种预配置场景**（思维教练、技术助手、个人助理）
- ✅ **自动坑点检查**（避免常见问题）
- ✅ **团队协作支持**（Git 共享配置）

---

## 🚀 快速开始

### 安装

```bash
# 方式1：从 ClawHub 安装（推荐）
clawhub install workspace-bootstrap

# 方式2：从 Git 克隆
git clone https://github.com/your-repo/workspace-bootstrap.git
```

### 使用

```bash
# 交互式向导（推荐新手）
bash scripts/wizard.sh ~/my-workspace

# 快速复刻（推荐有经验用户）
bash scripts/bootstrap.sh ~/my-workspace

# 坑点检查
bash scripts/check-pitfalls.sh ~/my-workspace
```

**详细教程**：[docs/QUICKSTART.md](docs/QUICKSTART.md)（5 分钟上手）

---

## 🎯 核心功能

### 1. 交互式配置向导

```bash
bash scripts/wizard.sh ~/my-workspace
```

- 收集用户信息（小龙虾名称、用户名称、时区等）
- 选择配置场景（3 种预配置）
- 自动生成 SOUL.md 和 USER.md

### 2. 目录结构创建

```bash
bash scripts/bootstrap.sh ~/my-workspace
```

创建 10 个核心目录：
- agents/（子 Agent 配置）
- memory/（记忆文件）
- skills/（技能包）
- user-data/（用户数据）
- scripts/（脚本工具）
- shared/（Agent 间共享）
- reports/（分析报告）
- temp/（临时文件）
- .learnings/（学习记录）
- wiki/（知识库）

### 3. 坑点检查

```bash
bash scripts/check-pitfalls.sh ~/my-workspace
```

检查 5 类常见问题：
1. MEMORY.md 容量爆炸（> 100 行）
2. 缺少核心文件（SOUL.md、AGENTS.md、USER.md、HEARTBEAT.md）
3. 缺少目录（agents、memory、skills、user-data、scripts、shared、reports、temp、.learnings）
4. 缺少学习文件（ERRORS.md、SUCCESSES.md、LEARNINGS.md）
5. 缺少共享目录（shared/inbox、shared/outbox、shared/status、shared/working）

---

## 📚 配置场景

### 场景1：思维教练（高复杂度）

**适用**：需要复杂决策、多领域协作的 AI 助手

**配置**：
- Agents：7 个（trader、writer、career、english、proposer、builder、evaluator）
- Skills：41 个
- Cron：4 个

### 场景2：技术助手（中复杂度）

**适用**：编程、测试、代码审查等技术任务

**配置**：
- Agents：3 个（coder、tester、reviewer）
- Skills：5 个
- Cron：2 个

### 场景3：个人助理（低复杂度）

**适用**：日程管理、任务提醒、邮件处理等日常任务

**配置**：
- Agents：3 个（calendar、task、email）
- Skills：2 个
- Cron：2 个

**详细说明**：[docs/USAGE.md](docs/USAGE.md)

---

## 📁 目录结构

```
workspace-bootstrap/
├── scripts/              # 核心脚本
│   ├── wizard.sh         # 交互式向导
│   ├── bootstrap.sh      # 目录结构创建
│   ├── check-pitfalls.sh # 坑点检查
│   └── validate.sh       # 配置验证
├── templates/            # 模板文件
│   ├── SOUL-template.md
│   ├── USER-template.md
│   ├── MEMORY-template.md
│   ├── AGENTS-template.md
│   ├── HEARTBEAT-template.md
│   └── WORKSPACE-TEMPLATE.md
├── examples/             # 示例配置
│   ├── mindset-coach/
│   ├── tech-assistant/
│   └── personal-assistant/
├── tests/                # 测试脚本
│   ├── test-scenario-1.sh
│   ├── test-scenario-2.sh
│   ├── test-scenario-3.sh
│   ├── test-scenario-4.sh
│   ├── test-scenario-5.sh
│   ├── test-all.sh
│   └── test-report.md
├── docs/                 # 文档
│   ├── USAGE.md          # 使用指南
│   └── QUICKSTART.md     # 快速上手
├── SKILL.md              # 技能定义
└── README.md             # 本文件
```

---

## ✅ 测试覆盖

workspace-bootstrap 已通过完整的测试验证：

- **测试场景**：5 个
- **通过率**：100%
- **测试报告**：[tests/test-report.md](tests/test-report.md)

### 测试场景

1. **全新用户，第一次搭建**：验证零基础用户能否快速搭建
2. **有经验用户，快速复刻**：验证快速复刻功能
3. **团队协作，共享配置**：验证配置共享和一致性
4. **自定义配置，扩展模板**：验证自定义扩展能力
5. **故障排查，坑点检查**：验证坑点检查准确性

---

## 📖 文档

- **快速上手**：[docs/QUICKSTART.md](docs/QUICKSTART.md)（5 分钟）
- **使用指南**：[docs/USAGE.md](docs/USAGE.md)（完整功能）
- **模板参考**：[templates/WORKSPACE-TEMPLATE.md](templates/WORKSPACE-TEMPLATE.md)
- **测试报告**：[tests/test-report.md](tests/test-report.md)
- **技能定义**：[SKILL.md](SKILL.md)

---

## 🔧 开发

### 运行测试

```bash
# 运行所有测试
bash tests/test-all.sh

# 运行单个场景
bash tests/test-scenario-1.sh
```

### 质量检查

```bash
# 检查所有脚本可执行
find scripts tests -name "*.sh" -exec test -x {} \; && echo "✅ All scripts executable"

# 检查文件格式
file scripts/*.sh | grep -q "UTF-8" && echo "✅ UTF-8 encoding"

# 检查链接有效性
grep -r "\[.*\](.*)" docs/ | grep -v "http" | cut -d'(' -f2 | cut -d')' -f1 | while read f; do test -f "$f" && echo "✅ $f" || echo "❌ $f"; done
```

---

## 🤝 贡献

欢迎贡献！请遵循以下步骤：

1. Fork 本仓库
2. 创建功能分支（`git checkout -b feature/amazing-feature`）
3. 提交更改（`git commit -m 'Add amazing feature'`）
4. 推送到分支（`git push origin feature/amazing-feature`）
5. 创建 Pull Request

---

## 📝 更新日志

### v1.0.0 (2026-04-07)

**新增**：
- ✅ 5 个测试场景（通过率 100%）
- ✅ 使用指南（USAGE.md）
- ✅ 快速上手教程（QUICKSTART.md）
- ✅ README.md

**修复**：
- 🐛 wizard.sh 在创建 SOUL.md 前没有先创建目录结构
- 🐛 SOUL.md 没有包含小龙虾名称
- 🐛 test-scenario-2.sh 和 test-all.sh 依赖 bc 命令（改用 awk）

**升级**：
- 📈 成熟度：L3 → L4（可产品化）
- 📈 版本：v0.3.0 → v1.0.0

---

## 📄 许可证

MIT License

---

## 📞 支持

- **问题反馈**：[GitHub Issues](https://github.com/your-repo/workspace-bootstrap/issues)
- **文档**：[docs/](docs/)
- **示例**：[examples/](examples/)

---

**workspace-bootstrap v1.0.0** - 5 分钟创建你的 OpenClaw workspace 🚀

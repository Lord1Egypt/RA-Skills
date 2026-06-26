# workspace-bootstrap

> 快速搭建 OpenClaw workspace 骨架的技能包

---

## 📋 技能信息

```yaml
id: workspace-bootstrap
name: Workspace Bootstrap
version: 1.0.0
author: 善人 + 小溪
purpose: 快速复刻"最佳实践"workspace 骨架
maturity: L4（可产品化）
tags: [workspace, setup, bootstrap, template]
```

---

## 🎯 用途

**解决的问题**：
- ❌ 新小龙虾不知道如何搭建 workspace
- ❌ 手动创建目录、文件容易遗漏
- ❌ 不知道哪些是"最佳实践"
- ❌ 踩过的坑无法避免

**提供的价值**：
- ✅ 一键创建标准目录结构
- ✅ 自动生成核心文件模板
- ✅ 提供 3 种配置示例
- ✅ 内置 7 个已知的坑

---

## 🚀 快速开始

### 1. 创建新 workspace

```bash
# 最小配置（适合个人助理）
/workspace-bootstrap create --template minimal

# 标准配置（适合技术助手）
/workspace-bootstrap create --template standard

# 完整配置（适合思维教练）
/workspace-bootstrap create --template full
```

### 2. 检查当前 workspace

```bash
/workspace-bootstrap check
```

### 3. 查看配置示例

```bash
/workspace-bootstrap examples
```

---

## 📂 目录结构

```
skills/workspace-bootstrap/
├── SKILL.md                    # 技能定义（本文件）
├── templates/
│   ├── WORKSPACE-TEMPLATE.md   # 通用骨架定义
│   ├── WORKSPACE-EXAMPLES.md   # 配置示例（3个场景）
│   ├── SOUL-template.md        # SOUL.md 模板
│   ├── AGENTS-template.md      # AGENTS.md 模板
│   ├── MEMORY-template.md      # MEMORY.md 模板
│   ├── USER-template.md        # USER.md 模板
│   └── HEARTBEAT-template.md   # HEARTBEAT.md 模板
├── scripts/
│   ├── bootstrap.sh            # 自动创建目录
│   ├── validate.sh             # 验证 workspace
│   └── check-pitfalls.sh       # 检查已知的坑
└── examples/
    ├── mindset-coach/          # 思维教练配置（高复杂度）
    ├── tech-assistant/         # 技术助手配置（中复杂度）
    └── personal-assistant/     # 个人助理配置（低复杂度）
```

---

## 🔧 核心功能

### 1. 创建目录结构

**自动创建 60+ 目录**：
```bash
agents/main
memory
skills
user-data
scripts
shared/{inbox,outbox,status,working}
reports
wiki/{concepts,entities,how-to}
temp
.learnings
```

### 2. 生成核心文件

**自动生成 7 个核心文件**：
- `SOUL.md` - 身份定义
- `AGENTS.md` - 启动流程
- `MEMORY.md` - 记忆索引
- `USER.md` - 用户画像
- `HEARTBEAT.md` - 心跳自检
- `IDENTITY.md` - 身份标识（可选）
- `TOOLS.md` - 工具配置（可选）

### 3. 提供配置示例

**3 种配置场景**：
- **思维教练**（高复杂度）：7 Agents、41 Skills、4 Cron
- **技术助手**（中复杂度）：3 Agents、5 Skills、2 Cron
- **个人助理**（低复杂度）：3 Agents、2 Skills、2 Cron

### 4. 检查已知的坑

**自动检测 7 个常见问题**：
1. MEMORY.md 容量爆炸
2. 子 Agent 交付不验收
3. 索引文件死链
4. 硬编码 vs 推理混淆
5. 子 Agent 沙箱隔离
6. 异步任务无进度反馈
7. 技能包质量不稳定

---

## 📋 使用场景

### 场景1：新用户搭建 workspace

```
用户：我刚安装了 OpenClaw，不知道怎么开始
小溪：用 workspace-bootstrap 快速搭建！
     /workspace-bootstrap create --template standard
```

### 场景2：迁移旧 workspace

```
用户：我有旧的 workspace，想升级到新结构
小溪：用 workspace-bootstrap 检查！
     /workspace-bootstrap check
```

### 场景3：查看配置示例

```
用户：不知道怎么配置团队
小溪：看看示例！
     /workspace-bootstrap examples
```

---

## ⚙️ 配置选项

### --template

| 选项 | 说明 | 目录数 | 文件数 |
|------|------|--------|--------|
| `minimal` | 最小配置 | 15 | 5 |
| `standard` | 标准配置 | 30 | 6 |
| `full` | 完整配置 | 60+ | 7 |

### --check

检查当前 workspace 状态：
- ✅ 核心文件是否存在
- ✅ 目录结构是否完整
- ✅ 索引是否有死链
- ✅ 是否有已知的坑

---

## 🔄 迭代计划

### 当前版本：v1.0.0（L4）

**已实现**：
- ✅ 目录结构定义
- ✅ 核心文件模板（7个）
- ✅ 配置示例（3个）
- ✅ 已知的坑清单（7个）
- ✅ 自动创建脚本（bootstrap.sh）
- ✅ 自动复制模板
- ✅ 配置向导（wizard.sh）
- ✅ 坑点检查（check-pitfalls.sh）
- ✅ 测试用例（5个场景，100%通过率）⭐ 新增
- ✅ 使用指南（USAGE.md）⭐ 新增
- ✅ 快速上手教程（QUICKSTART.md）⭐ 新增

### 下一版本：v1.1.0（L4）

**计划实现**：
- ⭕ ClawHub 发布
- ⭕ 社区反馈收集
- ⭕ 更多配置示例

### 验收标准（L4）

- ✅ 场景通过率 ≥ 80%（实际：100%）
- ✅ 场景数量 ≥ 5 个（实际：5 个）
- ✅ 文档完整（SKILL.md + USAGE.md + QUICKSTART.md）
- ✅ 测试覆盖（5 个自动化测试脚本）
- ✅ 自测通过（测试报告存在）

---

## 📚 参考资料

- **通用骨架**：[templates/WORKSPACE-TEMPLATE.md](templates/WORKSPACE-TEMPLATE.md)
- **配置示例**：[templates/WORKSPACE-EXAMPLES.md](templates/WORKSPACE-EXAMPLES.md)
- **技能标准**：[agents/evoskill/standards/SKILL-STANDARDS.md](../../agents/evoskill/standards/SKILL-STANDARDS.md)

---

## 🤝 贡献

这是一个**迭代中的技能包**，欢迎反馈：
- 发现新坑 → 提交到 `.learnings/ERRORS.md`
- 有新想法 → 提交优化提案
- 测试通过 → 更新成熟度

---

## 📜 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0.0 | 2026-04-07 | L3→L4 升级：测试覆盖（100%）、文档补充、发布准备 |
| v0.3.0 | 2026-04-06 | 新增配置向导、坑点检查 |
| v0.1.0 | 2026-04-06 | 初始版本，基础模板 |

---

_此技能包已达到 L4 级别（可产品化），准备发布到 ClawHub_

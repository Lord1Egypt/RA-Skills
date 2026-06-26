# Skillhub Auto-Finder + SkillSentry 集成指南

## 概述

**SkillSentry** 是安全审计 Skill，**Skillhub Auto-Finder** 是技能搜索助手。两者配合使用，可以实现安全的 Skill 发现和安装流程。

⚠️ **重要区别**：
- `Skillhub Auto-Finder` **仅搜索推荐**，不执行安装
- 所有安装操作需用户**手动确认**后执行

## 安全设计原则

### 1. 分离关注点

| 组件 | 职责 | 自动执行 |
|------|------|----------|
| `skillhub-auto-installer` | 搜索、分析、推荐 | ✅ 只读搜索 |
| `skillsentry` | 安全审计 | ✅ 本地扫描 |
| `npx skills add` | 实际安装 | ❌ 需用户手动执行 |

### 2. 强制安全审计

安装任何第三方 Skill 前，**强制要求**运行 SkillSentry 审计。

### 3. 用户确认

绝不自动执行安装命令，所有安装需用户明确确认。

## 使用流程

### 标准安全安装流程

```
用户: "我想找一个邮件管理的技能"
     │
     ▼
┌─────────────────────┐
│ 1. 搜索 Skillhub     │  ← skillhub-auto-installer
│    (只读操作)        │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ 2. 分析推荐          │  ← 智能体分析匹配度
│    (可选: 展示安全   │
│     风险等级)        │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ 3. 等待用户确认      │  ← 用户决定是否安装
│    "找到 X 技能，     │
│     是否安装?"       │
└────────┬────────────┘
         │
         ▼
    用户确认后:
         │
         ▼
┌─────────────────────┐
│ 4. 检查 SkillSentry  │
│    如未安装，提示安装 │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ 5. 运行安全审计      │  ← SkillSentry audit
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ 6. 提供安装命令      │  ← 展示命令，但不执行
│    供用户手动运行    │
└─────────────────────┘
```

## 安装状态

### ✅ 已安装

| Skill | 版本 | 功能 | 类型 |
|-------|------|------|------|
| `skillsentry` | 1.1.0 | 安全审计 + 提示注入检测 | 安全工具 |
| `skillhub-auto-installer` | 2.0.0 | 搜索推荐 + 安全检查 | 辅助工具 |

## 使用方式

### 方式 1: 自然语言交互 (推荐)

```
用户: "帮我找一个日历管理的技能"

智能体:
  1. [搜索] → 找到 5 个相关技能
  2. [分析] → 推荐 2 个最合适的
  3. [询问] → "找到以下候选，是否查看详情？"
  4. [用户确认] → 查看 SKILL.md
  5. [再次询问] → "是否安装 skill-X？"
  6. [如用户确认] → "请先安装 SkillSentry 并运行安全审计"
  7. [审计通过后] → "请手动执行以下命令安装: ..."
```

### 方式 2: 使用脚本

```bash
# 1. 搜索技能
bash skills/skillhub-auto-installer/scripts/search.sh "calendar"

# 2. 安装前检查 (强制要求 SkillSentry)
bash skills/skillhub-auto-installer/scripts/pre-install-check.sh owner/repo@skill-name

# 3. 安全检查特定 skill
bash skills/skillhub-auto-installer/scripts/security-check.sh skill-name

# 4. 运行完整安全审计
bash skills/skillsentry/scripts/audit.sh
```

### 方式 3: 独立使用 SkillSentry

```bash
# 运行完整安全审计
bash skills/skillsentry/scripts/audit.sh

# 启动安全面板
node skills/skillsentry/scripts/panel-server.js
```

## 脚本说明

| 脚本 | 功能 | 自动执行 |
|------|------|----------|
| `search.sh` | 搜索 Skillhub | ✅ 只读 |
| `pre-install-check.sh` | 安装前检查 + 安全审计 | ✅ 检查但不安装 |
| `security-check.sh` | 检查已安装 Skill | ✅ 本地扫描 |

## 安全检测内容

### SkillSentry 检测项目

| 检测项 | 说明 |
|--------|------|
| Gateway 安全 | 检查网关配置是否暴露敏感信息 |
| 漏洞扫描 | 检测已知安全漏洞 |
| Cron 任务 | 审计定时任务的安全性 |
| Prompt Injection | 检测提示注入攻击模式 |
| 敏感端口 | 检查是否有非预期的开放端口 |

### Auto-Finder 额外检查

| 检测项 | 说明 |
|--------|------|
| SKILL.md 规范 | 检查 Skill 元数据是否完整 |
| 脚本安全 | 扫描脚本中的高危命令 |
| 网络请求 | 标记脚本中的网络调用 |
| 代码执行 | 检测 eval/exec 等动态执行模式 |

## 文件位置

```
skills/
├── skillsentry/                    # 安全审计 Skill
│   ├── SKILL.md
│   ├── scripts/
│   │   ├── audit.sh               # 审计脚本
│   │   ├── panel-server.js        # 安全面板
│   │   └── config.js              # 配置管理
│   └── references/
│       └── threats.md             # 威胁类型参考
│
└── skillhub-auto-installer/        # 搜索助手 (不自动安装)
    ├── SKILL.md                    # 明确声明不自动安装
    ├── scripts/
    │   ├── search.sh              # ✅ 搜索脚本
    │   ├── pre-install-check.sh   # ✅ 安装前检查 (不安装)
    │   └── security-check.sh      # ✅ 安全检查
    └── references/
        └── security-integration.md # 本文档
```

## 最佳实践

### 1. 定期安全审计

```bash
# 每周运行一次完整审计
bash skills/skillsentry/scripts/audit.sh > weekly-audit-$(date +%Y%m%d).json
```

### 2. 新 Skill 安装流程

每次安装新 Skill 时：
1. 使用 `search.sh` 搜索候选
2. 查看目标 Skill 的 SKILL.md 了解功能
3. 确保 SkillSentry 已安装
4. 运行 `pre-install-check.sh` 进行安全检查
5. **仔细阅读**输出的安全报告
6. **确认无误后**，手动执行安装命令
7. 安装后再次运行 `security-check.sh`

### 3. 监控已安装 Skills

```bash
# 检查所有已安装 Skills 的安全状态
bash skills/skillhub-auto-installer/scripts/security-check.sh
```

## 常见问题

### Q: 为什么不让智能体自动安装？

A: 自动安装存在供应链风险：
- 无法验证远程代码是否可信
- 可能安装带有恶意代码的 Skill
- 扩大攻击面，间接提升权限

### Q: SkillSentry 会阻止安装吗？

A: `pre-install-check.sh` **会阻止**在未安装 SkillSentry 时继续。SkillSentry 本身是审计工具，只提供报告和建议，最终决策由用户做出。

### Q: 如何判断一个 Skill 是否安全？

A: 综合以下因素：
- ✅ **绿色**: SkillSentry 报告无严重问题 + 代码清晰 + 来源可信
- ⚠️ **黄色**: 有低风险项（如网络请求），但用途合理
- 🚨 **红色**: 有高危命令或可疑行为，建议避免

### Q: 发现安全风险怎么办？

A: 1. 仔细阅读风险详情
   2. 检查相关代码或配置
   3. 如有疑虑，可选择不安装或删除
   4. 可向 Skillhub 举报恶意 Skill

---

**安全第一：搜索可以自动，安装必须确认！** 🔐

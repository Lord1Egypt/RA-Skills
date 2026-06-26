# 🚀 SPM — Super Project Manager for OpenClaw

> 生产级软件项目开发技能。从需求到交付，结构化质量管理 + WBS 任务追踪，全流程自动化编排。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://openclaw.ai)

📖 *[English version → README_EN.md](README_EN.md)*

---

## 🎬 关注我

**抖音号：Openclaw实操笔记** —— 每天分享 AI 编程实战技巧，从零到一教你用 OpenClaw 高效开发。

🔗 抖音搜索「**Openclaw实操笔记**」或扫码关注👇

> *（二维码可自行生成后替换此处图片）*

---

## 这是什么？

SPM 是一个完整的 OpenClaw 技能，能把自然语言需求变成生产级代码，全流程结构化管控。它的核心是**编排器模式**——每个项目阶段自动路由到对应的工作流，WBS 任务台账是唯一的真相来源。

### 🎯 核心能力

- **🆕 WBS 哈希认证** — SHA-256 防篡改保护（`attest-wbs.sh` / `verify-wbs.sh`）
- **🆕 Hook 自动注入** — 活跃任务自动注入上下文（`inject-wbs-context.py`）
- **🆕 会话恢复** — 自动生成恢复报告（`session-recovery.py`）
- **🆕 并行任务指针** — `.active_ledger` 多任务无冲突切换
- **🆕 SPM 极简模式** — 5 条规则，小项目快速上手
- **13 个 Superpowers 工作流** — 头脑风暴、TDD、子代理开发、代码审查、系统调试、Git Worktree
- **5 阶段生命周期** — 需求 → 规划 → 执行 → 质量 → 交付
- **WBS 任务台账** — 结构化任务跟踪，含退出标准、证据、心跳、中断恢复
- **三级质量门控** — 必须做 / 先问 / 禁止 三层规则
- **子代理调度** — 并行 + 串行任务执行，自动绑定 WBS
- **铁律** — 无批准设计不写代码、无新鲜证据不报完成

### 🌐 浏览器自动化

SPM 集成 **agent-browser** 作为推荐浏览器工具，支持：

- 网页导航 (navigate, go_back, refresh)
- 元素交互 (click, type, select_option, hover)
- 页面操作 (scroll, screenshot, wait_for)
- 数据提取 (get_attribute, get_text, evaluate)
- 多标签页管理 (tabs, switch_tab, close_tab)
- 控制台监控 (console_messages, network_requests)

**适用场景：**
- Web 应用的功能测试与验证
- 网页数据采集与爬取
- 用户界面自动化测试
- 网页性能监控
- 跨浏览器兼容性测试

---

## 生命周期

```
需求 → 规划 → 执行 → 质量 → 交付
 ↑人工    ↑人工    ↑自动   ↑自动   ↑人工
 审批     审批                    决策
```

### 第1阶段：需求
灵魂拷问 → 头脑风暴 → 设计文档 → 用户审批

### 第2阶段：规划  
WBS 任务分解 → 文件映射 → 任务台账 → 用户确认

### 第3阶段：执行
Git Worktree 隔离 → 子代理调度 → TDD → WBS 绑定 → 心跳日志

### 第4阶段：质量
验证门 → 三级代码审查 → 质量门控 → 系统调试

### 第5阶段：交付
合并分支 → 部署(可选) → 交付总结 → 台账关闭

---

## 安装

```bash
# 1. 克隆到 OpenClaw skills 目录
git clone https://github.com/zhbcher/openclaw-spm.git ~/.openclaw/skills/spm

# 2. 在 openclaw.json 中启用
# 添加以下配置到 skills.entries：
{
  "SPM": {
    "enabled": true,
    "config": {
      "heartbeat_interval": "10m",
      "auto_checkpoint": true,
      "quality_gates_enabled": true,
      "wbs_ledger_path": "docs/spm/ledger.md",
      "parallel_subagents": true,
      "deployment_enabled": false
    }
  }
}

# 3. 重启 OpenClaw
openclaw gateway restart
```

---

## 快速上手

```
你：帮我做一个带JWT的用户认证系统

SPM 自动触发 →
  1. 灵魂拷问：什么认证流程？无状态还是有状态？要不要刷新令牌？
  2. 设计文档：架构、API 契约、数据模型
  3. 你批准 → 生成 WBS 计划
  4. 你说"开始" → 自动执行：
     ├─ Git Worktree 隔离环境
     ├─ 子代理1：数据库 Schema + 迁移
     ├─ 子代理2：JWT 中间件
     ├─ 子代理3：认证路由（TDD）
     ├─ 子代理4：测试
     ├─ 并行调度无依赖任务
     ├─ 代码审查 + 质量门控
     └─ 交付总结
  5. 搞定 → 合并到主分支
```

---

## WBS 任务台账

每个项目的**唯一真相来源**。全任务追踪：

| ID | 工作包 | 前置 | 退出标准 | 证据 | 状态 |
|----|--------|------|----------|------|------|
| 1  | 项目脚手架 | - | 初始化和测试通过 | `npm test` ✅ | done |
| 2  | 核心功能A | 1 | API 返回正确数据 | `curl` 输出 | doing |

**铁律：** 没有可验证的证据（文件diff、测试输出、命令结果），状态不能标 `done`。

---

## 质量门控

| 等级 | 规则 |
|------|------|
| 🔵 必须做 | 跑测试、遵守规范、验证输入、同步文档 |
| 🟡 先问再做 | 改数据库、加依赖、改CI/CD、改API |
| 🔴 绝对不能 | 提交密钥、跳过审查、未经批准删测试 |

### 五条铁律
1. **无批准设计不写代码**
2. **无失败测试不写生产代码**（TDD）
3. **无新鲜验证不报完成**
4. **无根因分析不行修复**
5. **无证据不标 done**

---

## 为什么要用 SPM？

| 不用 SPM | 用 SPM |
|----------|--------|
| 🤷 "上次写到哪了？" | 📋 WBS 台账：精准断点恢复 |
| 🔄 合并冲突满天飞 | 🌿 Git Worktree 隔离 |
| ❌ "我机器上能跑啊" | ✅ 每次报告附新鲜验证 |
| 🐛 "先试试这几行..." | 🔍 系统化4步调试法 |
| 📝 拍脑袋写代码 | 📐 设计先行，审批后再动手 |
| 🚢 "这个测试过吗？" | 🛡️ 三级质量门控 |

---

## 项目结构

```
spm/
├── SKILL.md                      # 技能定义与完整文档
├── workflows/                    # 13 个详细工作流指南
├── subagents/                    # 子代理调度 Prompt 模板
├── schemas/                      # JSON Schema 定义
├── templates/                    # 文档模板
├── references/                   # 最佳实践、恢复模式、单任务执行入口
│   ├── best-practices.md
│   ├── recovery-patterns.md
│   ├── task-ledger-template.md
│   └── TASK-EXECUTION.md        # ⭐ 执行任务前必读的单一入口
├── scripts/                      # 自动化脚本
│   ├── init-project.sh
│   ├── quality-check.sh
│   ├── checkpoint.sh
│   ├── setup-checkpoints.sh
│   ├── verify_checklists.py
│   ├── generate.sh
│   ├── validate_contract.sh
│   └── e2e.sh
├── CHECKPOINTS/                  # 阶段硬节点模板
├── CHECKLISTS/                   # 完工自检清单
├── api/                          # API 契约 (OpenAPI)
└── docs/                         # 设计参考文档
```

---

## 环境要求

- OpenClaw 2026.4+
- Node.js、npm、git（任意现代版本）
- OpenClaw 需开启子代理支持
- **浏览器自动化**：SPM 使用 agent-browser 作为推荐浏览器工具，确保该插件已安装并启用

---

## 作者

**旺财**（OpenClaw Agent）  
📧 [zhbcher@gmail.com](mailto:zhbcher@gmail.com)  
🎵 抖音：**Openclaw实操笔记**

---

## 🏢 商业授权

本 skill 采用 **MIT 开源许可证**，免费用于个人和商业项目。如需获得额外的商业支持、定制开发或企业级服务，请考虑购买商业授权。

### 商业授权包含

- ✅ **商业使用许可** — 明确的企业级使用授权
- ✅ **私密定制开发** — 根据企业需求定制功能
- ✅ **优先技术支持** — 快速响应技术支持服务
- ✅ **定制功能需求** — 可按需开发新工作流或集成

### 定价与联系

- 💰 **商业授权费用**：联系作者获取报价
- 📧 **邮箱**：zhbcher@gmail.com
- 📱 **抖音私信**：Openclaw实操笔记

**[联系获取商业授权 → mailto:zhbcher@gmail.com](mailto:zhbcher@gmail.com)**

---

## 许可证

MIT — 详见 [LICENSE](LICENSE) 文件。

---

## 致谢

SPM 借鉴并增强了 **Superpowers** 技能套件的工作流模式——包括头脑风暴、TDD、子代理开发、代码审查、系统调试、Git Worktree 等。在此基础上我们增加了：

- **PM 级项目管理**（灵魂拷问、假设文档、安全沙箱）
- **WBS 任务台账**（带退出标准和证据的结构化追踪）
- **三级质量门控**（必须做/先问/禁止）
- **心跳中断恢复机制**
- **完整交付流水线**（发布、部署、关闭）

🙏 感谢 Superpowers 作者和 OpenClaw 社区。

---

*⭐ 如果这个项目对你有帮助，请给个 Star！关注抖音「Openclaw实操笔记」获取更多 AI 编程实战技巧。*

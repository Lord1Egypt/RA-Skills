# 🤖 多子代理协作分析与构建技能

_版本：1.0.0 | 创建日期：2026-03-30 | 作者：TUTU_

---

## 📖 简介

本技能帮助 OpenClaw 用户**分析、设计和构建多子代理协作系统**，实现复杂任务的高效分解和执行。

### 核心能力

- ✅ **子代理能力分析** - 扫描已配置子代理，识别专长领域
- ✅ **协作模式推荐** - 根据任务特征推荐最佳协作模式（6 种）
- ✅ **协作流程生成** - 自动生成可执行的协作代码
- ✅ **安全配置检查** - 集成 RSG v2.2.0 子代理监控规则
- ✅ **资源优化建议** - 模型选择、超时设置、并发控制

---

## 🚀 快速开始

### 安装

```bash
clawhub install subagent-collaboration
```

### 使用

#### 方式 1：分析现有配置

```bash
python3 skills/subagent-collaboration/scripts/analyze_subagents.py
```

#### 方式 2：生成协作流程

```bash
python3 skills/subagent-collaboration/scripts/generate_workflow.py \
  --task "分析某科技公司是否值得投资" \
  --mode auto \
  --output workflow.json
```

#### 方式 3：安全检查

```bash
python3 skills/subagent-collaboration/scripts/security_check.py \
  --input workflow.json
```

---

## 📋 协作模式

| 模式 | 适用场景 | 子代理数 | 预计耗时 |
|------|----------|----------|----------|
| **并行协作** | 多领域综合分析 | 3-5 个 | 3-5 分钟 |
| **串行协作** | 工作流任务 | 2-4 个 | 5-10 分钟 |
| **分层协作** | 超大型项目 | 5-10 个 | 10-20 分钟 |
| **竞争协作** | 方案对比择优 | 3-5 个 | 5-8 分钟 |
| **专家会诊** | 疑难问题 | 4-6 个 | 5-8 分钟 |
| **接力协作** | 长流程处理 | 3-5 个 | 8-15 分钟 |

---

## 🛡️ 安全检查

基于 RSG v2.2.0 的 20 条子代理监控规则（openclaw-120 至 139）：

### 必检项目

- ✅ 超时设置（≤300 秒）
- ✅ 沙箱配置（require）
- ✅ 标签标识
- ✅ 清理策略
- ✅ 敏感任务检测
- ✅ 命令执行检测
- ✅ 并发控制（≤3 个）

---

## 📁 文件结构

```
subagent-collaboration/
├── SKILL.md                          # 技能说明
├── README.md                         # 使用指南
├── scripts/
│   ├── analyze_subagents.py          # 子代理分析器
│   ├── generate_workflow.py          # 流程生成器
│   └── security_check.py             # 安全检查器
└── references/
    └── collaboration-patterns.md     # 协作模式参考（待创建）
```

---

## 📊 示例输出

### 分析报告

```
✅ 已配置子代理角色：12 个
   - 国际战略分析师 (qwen3.5-plus)
   - 商业战略咨询师 (qwen3.5-plus)
   - 网络安全专家 (qwen3-coder-plus)
   ...

📊 模型分布：
   - qwen3.5-plus: 5 个
   - qwen3-coder-plus: 3 个
   - glm-4.7: 4 个

💡 建议：
   - 可添加医疗顾问角色
   - 考虑添加法律顾问角色
```

### 工作流配置

```json
{
  "task": "分析某科技公司是否值得投资",
  "mode": "parallel",
  "agents": [
    {
      "label": "market-analysis",
      "task": "分析市场规模和竞争格局",
      "model": "bailian/qwen3.5-plus",
      "timeoutSeconds": 180,
      "sandbox": "require",
      "cleanup": "delete"
    },
    ...
  ]
}
```

### 安全检查结果

```
✅ 安全检查通过

检查项：
- ✅ 超时设置：全部≤300 秒
- ✅ 沙箱配置：全部 require
- ✅ 标签标识：全部有 label
- ✅ 清理策略：全部 delete
- ✅ 敏感任务：无
- ✅ 命令执行：无
- ✅ 并发控制：4 个（可接受）
```

---

## 🔗 相关技能

- **subagent-roles-v2** - 子代理角色定义
- **runtime-security-guard** - RSG 安全监控
- **multi-model-guide** - 多模型使用指南

---

## 📝 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-03-30 | 初始版本 |

---

**维护者：** TUTU  
**许可证：** MIT

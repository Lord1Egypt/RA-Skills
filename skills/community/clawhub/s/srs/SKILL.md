---
name: srs
description: SRS - Security Research System 安全研究系统
metadata:
  openclaw:
    emoji: 🎯
    version: 1.0.0
  abbreviation: SRS

# 🎯 SRS - Security Research System

> 安全研究系统 - 智能任务评估与角色匹配

## 系统信息

- **全称**: Security Research System (安全研究系统)
- **缩写**: SRS
- **版本**: 1.0.0

## 核心能力

### 1. 任务评估 (Evaluation)

系统会根据多个维度评估任务是否进入系统：

| 评估维度 | 权重 | 说明 |
|----------|------|------|
| 优先级 | 25% | 外部触发 > 计划任务 > 主动发现 > 内部优化 |
| 知识相关性 | 20% | 核心领域 > 边缘领域 > 其他 |
| 时效性 | 15% | 紧急 > 高 > 中 > 低 |
| 资源可用性 | 15% | CPU/内存阈值 |
| 价值 | 25% | 对外发布/知识贡献/风险缓解 |

**阈值**: 总分 >= 60 分才能进入系统

### 2. 角色匹配

根据任务内容自动匹配最合适的角色：

| 关键词 | 匹配角色 |
|--------|----------|
| cve, vulnerability, threat, exploit | 🔴 安全研究员 |
| research, analysis, study, paper | 📚 领域研究员 |
| document, report, knowledge, 整理 | 📖 知识运营 |
| discover, scan, trend, 新兴 | 🚀 探索者 |
| incident, alert, monitor, response | 🛡️ 安全运营 |

### 3. 优先级规则

```
外部触发 (最高):
├── CVE严重漏洞: 100分
├── 安全事件: 95分
├── 合规违规: 90分
└── 公开披露: 85分

计划任务:
├── 日报: 70分
├── 周报: 65分
└── 月度review: 60分

主动发现:
├── 威胁情报: 50分
├── 研究机会: 45分
└── 趋势分析: 40分

内部优化 (最低):
├── 基础设施: 20分
├── 工具改进: 15分
└── 文档完善: 10分
```

## 使用方法

```bash
# 启动系统
srs start

# 执行任务 (自动评估+匹配)
srs run "研究OpenClaw安全治理"

# 查看状态
srs status

# 查看评估标准
srs criteria
```

## 评估示例

```bash
$ srs run "研究OpenClaw安全治理"

{
  "status": "admitted",
  "task": {
    "name": "研究OpenClaw安全治理",
    "role": "security_researcher",
    "role_emoji": "🔴"
  },
  "evaluation": {
    "priority": 85,
    "resources": 80.0,
    "relevance": 40.0,
    "timeliness": 80,
    "value": 30,
    "total": 60.75,
    "admit": true,
    "matched_role": "security_researcher"
  }
}
```

## 文件结构

```
srs/
├── srs.py       # 核心系统
├── srs          # CLI脚本
└── SKILL.md    # 本文档
```

## 评估流程

```
用户输入
    ↓
┌─────────────────┐
│  任务评估      │
│  - 优先级      │
│  - 资源        │
│  - 相关性      │
│  - 时效性      │
│  - 价值        │
└─────────────────┘
    ↓
┌─────────────────┐
│  判定          │
│  >= 60分: 通过 │
│  < 60分: 拒绝 │
└─────────────────┘
    ↓
┌─────────────────┐
│  角色匹配      │
│  关键词匹配    │
└─────────────────┘
    ↓
执行任务
```

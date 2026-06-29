---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: f114db32c8f49bbd4c4c544cd9de808d_947eae8966f911f1a0095254002afed2
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: f114db32c8f49bbd4c4c544cd9de808d_947eae8966f911f1a0095254002afed2
---

# 钟馗.Skill — Agent Skill 安全审查工具

> 捉鬼天师，铁面判官。拿来即审，一眼看穿。

## 是什么

钟馗是 Agent Skill 的自动化安全审查工具。基于 14 篇前沿论文的方法论，对 Skill 执行**三层纵深审查**：静态审计（54 项检查）→ 行为模拟（21 个攻击场景）→ 供应链溯源（10 个维度），最终输出结构化安全裁定。

## 核心能力

| 能力 | 说明 |
|:---|:---|
| 静态审计 | 54 项正则+关键词检查，覆盖元数据/内容/脚本/权限/数据安全，秒级完成 |
| 行为模拟 | 21 个 ToolEmu 攻击场景，跟踪 Agent 行为链，PASS/WARN/FAIL 判定 |
| 供应链溯源 | 10 维追溯：发布者信誉（含动态评分）/CVE 依赖/版本变更/社区反馈/SBOM/API 安全/SDK 准入/熔断降级/外部信息源信誉/持久化写入审计。含依赖运行时监控 |
| 红队对抗 | OWASP Top 10 for LLM 专项测试矩阵，自动化红队+外部渗透+SLA |
| 一票否决 | R1/R2/R3/R5/R7 命中即判恶意，不计算总分 |
| 即时红线 | 17 条拒绝红线，见即斩，无需走完整审查 |
| 可执行引擎 | 纯 Python 标准库脚本，`python zhongkui.py <目录>` 直接出报告 |
| 结构化裁定 | ✅ 干净 / ⚠️ 可疑 / 🚫 恶意，每项扣分附带行号和触发内容 |

## 风险覆盖（12 维）

| 编号 | 风险类别 | 一票否决 |
|:---|:---|:---|
| R1 | 提示注入 | 是 |
| R2 | 恶意代码执行 | 是 |
| R3 | 凭证窃取 | 是 |
| R4 | 依赖投毒 | 否 |
| R5 | 数据外传 | 是 |
| R6 | 权限提升 | 否 |
| R7 | 持久化后门 | 是 |
| R8 | 隐蔽指令 | 否（必进 L2） |
| R9 | 数据泄露与隐私违规 | 否 |
| R10 | 有害输出与内容合规 | 否 |
| R11 | 外部信息源投毒 | 否（必进 L2） |
| R12 | 智能体行为级漏洞 | 否（必进 L2） |

## 目录结构

```
zhongkui-skill/
├── SKILL.md                           # 技能定义（Agent 加载入口）
├── README.md                          # 本文件
├── QUICKSTART.md                      # 快速上手
├── REFERENCE.md                       # 完整技术参考
├── zhongkui.py                        # 主审查引擎入口
├── core/
│   ├── __init__.py
│   ├── auditor.py                     # Layer 1 静态审计引擎（54 项）
│   └── scorer.py                      # 评分计算器
└── references/
    ├── agent-skill-security-review.md # 完整方法论（14 篇论文）
    ├── risk-taxonomy.md               # 12 维风险分类
    ├── static-audit.md                # 54 项检查清单
    ├── behavioral-emulation.md        # 21 场景+红队对抗
    ├── supply-chain.md                # 10 维供应链溯源
    ├── scoring.md                     # 评分公式与多引擎仲裁
    ├── fix-strategies.md              # 11 类风险修复策略
    ├── trust-hierarchy.md             # 5 级信任层级
    ├── roadmap.md                     # Phase 1-4 落地路线图
    └── paper-mapping.md               # 论文→模块映射表
```

## 快速开始

### 作为 Skill 使用（推荐）

在对话中说：

```
审 E:\skills\some-skill
```

Agent 加载钟馗后执行完整审查并输出报告。

### 直接运行脚本

```bash
# 完整审计
python zhongkui.py E:\skills\some-skill

# 快速审计（仅 Layer 1，秒级）
python zhongkui.py E:\skills\some-skill --quick
```

### 输出示例

```
## 钟馗裁定：[⚠️]
**总分**：72.5 / 100
**一句话**：发现 3 个安全问题，无高危项

### 扣分项
| 层级 | 检查项 | 风险类型 | 扣分 | 命中内容（行号） |
|:---|:---|:---|:---|:---|
| L1 | C3 | R3 | -8 | SKILL.md:L45 |
| L1 | M4 | R6 | -5 | SKILL.md:L0 |
| L1 | D1 | R9 | -2 | SKILL.md:L0 |
```

## 评分速查

| 总分 | 裁定 | 处理 |
|:---|:---|:---|
| ≥ 85 | ✅ 干净 | 可安全安装 |
| 70-84 | ⚠️-low | 低风险可疑，建议人工复核 |
| 60-69 | ⚠️-high | 高危可疑，建议拒绝 |
| < 60 | 🚫 恶意/高风险 | 禁止安装，上报 |

## 文档导航

| 文档 | 适合 |
|:---|:---|
| [QUICKSTART.md](QUICKSTART.md) | 第一次使用，5 分钟上手 |
| [REFERENCE.md](REFERENCE.md) | 深入理解审查机制、全部检查项 |
| [references/agent-skill-security-review.md](references/agent-skill-security-review.md) | 学术依据，完整方法论 |

## 方法论依据

基于 14 篇前沿论文：Snyk ToxicSkills、CSA、Greshake 2023、Design Patterns 2025、ToolEmu、MiniScope、AgentPoison、OpenClaw+NVIDIA 等。详见[论文映射表](references/paper-mapping.md)。

## 版本

v2.0.0 — 54 项检查 / 21 场景 / 10 维溯源 / 17 条红线
*（内容由AI生成，仅供参考）*


---

## 常见问题速查

> 以下按问题列出 FAQ 答案在各文档中的位置，避免翻来翻去。

| 问题 | 文档 | 位置 |
|------|------|------|
| 为什么我的 Skill 被判 R8？ | SKILL.md | "反模式与常见陷阱 → 常见疑问" 章节 |
| 为什么我的 Skill 被判 R8？ | QUICKSTART.md | "常见问题" 章节 |
| 误报怎么办？ | SKILL.md | "反模式与常见陷阱 → 常见疑问" 章节 |
| 误报怎么办？ | QUICKSTART.md | "常见问题" 章节 |
| 审查多久？（各层耗时） | SKILL.md | "反模式与常见陷阱 → 常见疑问" 章节 |
| 审查多久？（各层耗时） | QUICKSTART.md | "常见问题" 章节 |
| 钟馗审不了什么？（能力边界） | SKILL.md | "能力边界" 章节（详细列表） |
| 钟馗审不了什么？（能力边界） | QUICKSTART.md | "常见问题" 章节（简版） |
| 钟馗审不了什么？（能力边界） | references/capability-boundaries.md | 全文（各层精度盲区+检出率） |
| 脚本和对话审查有什么区别？ | QUICKSTART.md | "常见问题" 章节 |
| 黄标为什么有 high/low 之分？ | QUICKSTART.md | "常见问题" 章节 |
| 黄标裁定阈值与处理 | references/scoring.md | "裁定阈值 → 黄标细化处理" 章节 |
| 审完后文件编码报错怎么办？ | QUICKSTART.md | "常见问题" 章节 |
| 审完后文件编码报错怎么办？ | references/error-handling.md | "异常分类与处理 → 编码异常" 章节 |
| 审查中断了怎么办？ | QUICKSTART.md | "常见问题" 章节 |
| 审查中断了怎么办？ | references/error-handling.md | 全文（含各类异常处理） |
| 能审多个 Skill 吗？（批量审查） | QUICKSTART.md | "常见问题" 章节 |
| 评分是怎么算的？ | references/scoring.md | "评分公式" 章节 |
| 一票否决有哪些？ | SKILL.md | "风险速查" 表格（一票否决列） |
| 一票否决有哪些？ | references/scoring.md | "一票否决项" 章节（6 项详表） |
| 即时红线有哪些？ | SKILL.md | "即时拒绝红线" 表格（17 条） |
| 即时红线有哪些？ | references/trust-hierarchy.md | "即时拒绝红线" 表格（17 条） |
| 红线体系是什么？ | SKILL.md | "即时拒绝红线" + "风险速查" 章节 |
| 如何修复被扣分的项目？ | references/fix-strategies.md | 全文（11 类风险修复方法） |
| 各层审查精度如何？（检出率/误报率） | references/capability-boundaries.md | "精度声明总结" 表格 |
| 审查方法论依据是什么？ | references/agent-skill-security-review.md | 全文（14 篇论文支撑） |
| 漏洞库如何更新？ | SKILL.md | "漏洞库更新" 章节 |
| 漏洞库如何更新？ | references/threat-intel-pipeline.md | 全文（自动摄入 → 签名生成） |
| 三种审查模式的区别？ | SKILL.md | "快速指令" 表格（审/快审/审依赖/审行为） |
| 三种审查模式的区别？ | QUICKSTART.md | "基本用法" 五个场景 |
| 信任层级是什么？ | references/trust-hierarchy.md | 全文（5 级信任层级表） |
| 各阶段开发状态？ | references/roadmap.md | 全文（Phase 1-4） |
| 常见审查陷阱有哪些？ | SKILL.md | "反模式与常见陷阱" 章节（6 个陷阱） |


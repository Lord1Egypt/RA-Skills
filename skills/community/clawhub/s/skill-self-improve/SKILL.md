---
name: skill-self-improve
description: |-
  给任意 WorkBuddy 技能注入「自进化学习系统」，让它越用越好用、越用越高效。
  通过通用 learner.py 记录每次使用的成败与用户偏好，自动复盘并给出改进建议。
  一键批量注入：复制学习模块、初始化记忆文件、在 SKILL.md 追加自进化章节。
  适用：准备发布或已上线的技能、想加自我迭代能力的任何技能。
  触发词：自进化、自我复盘、自动迭代、越用越好用、学习系统、skill 自我改进。
agent_created: true
version: 1.0.0
display_name: "技能自进化注入器"
display_name_en: "Skill Self-Improve Injector"
description_zh: "给技能注入自进化学习系统，越用越好用"
description_en: "Inject self-evolving learning system into any skill"
visibility: "public"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# 技能自进化注入器（skill-self-improve）

## 为什么需要

技能一旦发布就「定型」了，不会随使用变好。本技能把一套**通用自进化学习系统**
注入到任意技能里，使其：

- 📊 记录每次使用的成败、能力分布、错误模式
- 🧠 记住用户偏好，下次直接采用，减少重复询问
- 🔁 自动复盘：错误≥3次给改进建议，操作≥10次做高频/低频优化
- 📈 越用越懂用户，从「通用能力」沉淀为「专属最佳实践」

## 套件内容（本技能自带，自包含）

| 文件 | 作用 |
|------|------|
| `scripts/learner.py` | 通用学习模块：init/record/prefer/insight/reflect |
| `scripts/section.md` | 追加到目标 SKILL.md 的「自进化学习系统」章节文案 |
| `scripts/inject_self_improve.py` | 批量注入器（幂等，已拥有的技能自动跳过） |

## 用法

### 1. 给单个技能注入

把本技能的 `scripts/learner.py` 与 `scripts/section.md` 复制到目标技能目录，
并在目标 SKILL.md 末尾追加 `section.md` 内容；同时初始化 `learned_patterns.json`：

```bash
python <本技能>/scripts/inject_self_improve.py
```

`inject_self_improve.py` 内置了需要注入的技能名单。若要临时给某个技能加，
直接调用 learner.py 的 init 即可：

```bash
python learner.py init <目标技能目录>
```

### 2. 使用技能时（技能内部 / 智能体调用）

```bash
# 记录一次成功使用
python learner.py record <技能目录> --capability 简历优化
# 记录失败
python learner.py record <技能目录> --capability 简历优化 --fail --error 格式识别失败 --note "用户上传非标准文件"
# 记录用户偏好
python learner.py prefer <技能目录> --key 输出语言 --val 中文
# 查看洞察
python learner.py insight <技能目录>
# 自动复盘
python learner.py reflect <技能目录>
```

### 3. 记忆文件 schema（learned_patterns.json）

```json
{
  "version": 1,
  "totalOps": 0,
  "totalErrors": 0,
  "capabilityStats": {},   // 能力名 -> {count, success, fail}
  "errorPatterns": {},     // 错误类型 -> {count, lastNote, lastTime}
  "preferences": {},       // 用户偏好 key->value
  "recentOps": [],
  "optimizations": {},
  "lastUpdated": ""
}
```

## 设计要点

- **技能无关**：learner.py 不依赖任何业务逻辑，靠 `--capability` / `--error` 标签归类。
- **幂等安全**：注入前检测是否已存在章节，存在则跳过，不破坏原 SKILL.md。
- **真能跑**：不只是文字建议——每次使用后 Bash 调用 learner.py，学习闭环真实可执行。
- **阈值驱动迭代**：错误≥3次自动建议加预检并回写 SKILL.md；操作≥10次做能力优化分析。

## 适用场景

- 批量给「准备发布的技能」统一加上自进化能力（本仓库 20 个技能已全员注入）
- 给老技能补充复盘迭代机制
- 作为新技能脚手架的默认组件

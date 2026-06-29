# Anti-Patterns — Skill 设计反模式

**加载时机：** 📍 Pass 5 Optimize 执行 O1-O8 检查时加载。

> 本文件定义 Skill Compiler 优化阶段（Pass 5）引用的反模式编号。
> 完整 13 反模式库见 SkillForge [rubrics/anti-patterns.md](../../skillforge/rubrics/anti-patterns.md)。

---

## AP-02: Prompt Black Hole（Prompt 黑洞）

**症状：** 把所有逻辑、规则、领域知识塞进一个巨大的 SKILL.md。token 爆炸，模型注意力分散。

| 维度 | 详情 |
|------|------|
| 检测方法 | SKILL.md 超过 300 行 |
| 修正 | 拆分为多 agent 或 reference 文件，SKILL.md 只做路由 manifest |
| 严重度 | 🟠 High |
| Pass 5 检查项 | O1（Prompt 长度优化） |

## AP-04: Verification Theater（验证表演）

**症状：** 声称有质量验证，但验证者和产出者是同一个 agent（或同一段 prompt）。

| 维度 | 详情 |
|------|------|
| 检测方法 | 检查 verifier 是否独立于 producer |
| 修正 | 使用独立的 Verifier Agent（干验分离原则） |
| 严重度 | 🟠 High |
| Pass 5 检查项 | O6（拆分检查） |

## AP-06: Infinite Loop Without Guard（无界循环）

**症状：** 工作流中有循环/迭代逻辑，但没有设置最大轮次上限。

| 维度 | 详情 |
|------|------|
| 检测方法 | 检查 loop/feedback 步骤是否有 max_iterations |
| 修正 | 设置硬性上限（推荐最多 3 轮） |
| 严重度 | 🟠 High |
| Pass 5 检查项 | O6（拆分检查） |

## AP-07: God Agent（上帝 Agent）

**症状：** 单个 agent 负责太多职责，prompt 中有 5+ 个不相关的"功能"。

| 维度 | 详情 |
|------|------|
| 检测方法 | 读 agent 的 Capabilities/功能列表，检查是否有 >= 5 个不相关功能 |
| 修正 | 按职责拆分为多个 agent，每个 agent 只负责一件事 |
| 严重度 | 🟠 High |
| Pass 5 检查项 | O5（模块化检查） |

## AP-12: Trust-Domain Conflation（信任域混淆）

**症状：** 同一逻辑概念被同一个文件承载，但该文件同时被"隔离验证者"和"知情决策者"读取。知情数据泄漏到隔离通道，导致隔离失效。

| 维度 | 详情 |
|------|------|
| 检测方法 | ① 检查是否有 blind/isolated verifier；② 追踪其输入来源；③ 检查白名单文件是否包含知情数据 |
| 修正 | 按信任域拆分文件（clean file vs dirty file） |
| 严重度 | 🟠 High |
| Pass 5 检查项 | O4（知识耦合检测） |

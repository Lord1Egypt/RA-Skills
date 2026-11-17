# 8 大审计维度详细检查项

**When to read**: Phase 1-3 执行审计时。本文件列出每个维度的完整 checklist，审计员按维度逐项检查并记录 Findings。

**成熟度分级**：各检查项标注适用等级（L1/L2/L3）。L1 只跑标注 L1 的项，L2 跑 L1+L2 项，L3 跑全部。

---

## 维度 S：结构合规审计（Structure）

| 编号 | 检查项 | 等级 | 方法 | PASS 标准 | 严重性 |
|------|--------|------|------|-----------|--------|
| S1 | frontmatter 必填字段 | L1 | Read SKILL.md 头部 | name + description 必填 | Important if 缺 |
| S2 | name 符合 kebab-case | L1 | 正则 `^[a-z][a-z0-9-]*$` | 全小写+连字符 | Minor |
| S3 | description ≤ 200 字符 | L1 | `len(description)` | ≤200（核心词在前200字符） | Important if >250 |
| S4 | description 三要素 | L1 | 人工+模式匹配 | 做什么+何时触发+Do NOT | Important if 缺 Do NOT |
| S5 | 4 模块齐全 | L1 | Grep `## 任务` `## 输出格式` `## 规则` `## 示例` | 4 标题都存在 | Important if 缺任一 |
| S6 | SKILL.md ≤ 200 行 | L1 | `wc -l SKILL.md` | ≤200（硬上限 300） | Important if >200 |
| S7 | 规则实习生测试 | L2 | 人工审查每条规则 | 每条可直接执行 | Minor if 模糊 |
| S8 | 示例覆盖边界 | L2 | 人工审查示例 | 至少 1 个边界情况 | Minor |
| S9 | 渐进式披露 | L2 | 检查 SKILL.md 是否只放导航 | 详细内容下沉 references/scripts/assets | Important |
| S10 | 目录结构 | L2 | LS 目录 | 标准目录结构完整 | Minor |

---

## 维度 T：安全合规审计（Trust）

**详细扫描模式见 [`security-scan.md`](security-scan.md)**，本表为概览：

### T1-T14 基础安全扫描（原有）

| 编号 | 检查项 | 等级 | 方法 | 严重性 |
|------|--------|------|------|--------|
| T1 | Layer 1 凭证泄露 | L2 | Grep 扩展模式 | Critical if 真实凭证 |
| T2 | Layer 2 本地路径 | L2 | Grep `C:\\\|D:\\\|/Users/` | Important |
| T3 | Layer 3 危险命令 | L2 | Grep `curl\|wget\|eval\|exec` | Critical if 外发数据 |
| T4 | Layer 4 YARA 触发词 | L3 | Grep 5 类字面量 | Critical（即使文档中也触发） |
| T5 | Layer 5 SSD3 派生输出 | L3 | 检查代码读敏感文件→写持久化输出 | Important |
| T6 | MCP Tool Poisoning 行为声明 | L3 | description 是否完整声明全部行为 | Important |
| T7 | MCP Least Privilege 权限声明 | L3 | SKILL.md/plugin.json 是否声明权限 | Important |
| T8 | Missing User Warnings | L3 | 有副作用的 Skill README 是否含警告 | Important |
| T9 | Description-Behavior Mismatch | L3 | description 与实际行为一致 | Important |
| T10 | Self-Modification 措辞 | L3 | 避免"update SKILL.md"等 | Minor |
| T11 | 安全敏感方案不文档化 | L3 | 不描述绕过网络限制方案 | Important |
| T12 | Pre-Scan 文件清单 | L2 | LS 检查凭证文件和临时脚本 | Critical if 存在 |
| T13 | 最小权限校验 | L2 | allowed-tools 与任务无关权限删除 | Minor |
| T14 | 国内可用性 | L3 | 依赖 API 国内可访问 | Important if 海外独占 |

### T-AST 系列：OWASP AST10 对齐扫描（v2.0.0 新增）

> **背景**：业界主流 Skill 平台采用 OWASP Agentic Skills Top 10（AST10）作为审计框架基础。skill-auditor 对齐 AST10 以确保审计覆盖面与平台一致。

| 编号 | 检查项 | 等级 | 方法 | PASS 标准 | 严重性 |
|------|--------|------|------|-----------|--------|
| T-AST01 | 恶意技能（Malicious Skills） | L2 | T1-T4 综合 | 无恶意载荷 | Critical |
| T-AST02 | 供应链攻击（Supply Chain） | L3 | 检查外部源信任 + hash pinning + 依赖固定版本 | 外部依赖有版本/hash 锁定 | Important |
| T-AST03 | 过度授权（Over-Privileged） | L3 | T7 + T13 + allowed-tools 审查 | 权力与用途成比例 | Important |
| T-AST04 | 元数据不安全（Insecure Metadata） | L2 | D-M1/M2/M3 声明-行为一致性 | frontmatter 完整声明实际行为 | Important |
| T-AST05 | 不安全反序列化（Unsafe Deserialization） | L3 | 检查 YAML/JSON 解析是否用 safe_load + 无 eval 解析 | 用 safe_load / json.loads，无 eval | Important |
| T-AST06 | 隔离薄弱（Weak Isolation） | L3 | 检查是否有执行边界 + 沙箱声明 + 不越权访问其他 Skill | 有明确行为边界 | Important |
| T-AST07 | 更新漂移（Update Drift） | L3 | 检查版本是否固定 + 是否有 hash 验证 + CHANGELOG 连续性 | 版本连续 + CHANGELOG 完整 | Minor |
| T-AST10 | 跨平台复用（Cross-Platform Reuse） | L3 | 检查是否声明平台兼容性 + OS 限制 + 依赖可移植性 | 声明 OS 限制或跨平台兼容 | Minor |

> AST08（Poor Scanning）/ AST09（No Governance）是针对平台和组织的，不适用于单 Skill 审计，跳过。

### T-LT：Lethal Trifecta 红线检查（v2.0.0 新增）

> **背景**：OWASP AST10 提出的"Lethal Trifecta（致命三要素）"——三者同时满足 = Critical 风险，应重新设计。

| 编号 | 检查项 | 等级 | 方法 | 判定 |
|------|--------|------|------|------|
| T-LT1 | 要素1：访问私有数据 | L3 | 检查是否读取 SSH keys / API credentials / wallet files / browser data / memory 文件 | 是/否 |
| T-LT2 | 要素2：暴露于不可信内容 | L3 | 检查是否处理 skill instructions / memory files / email / Slack 等外部输入 | 是/否 |
| T-LT3 | 要素3：能对外通信 | L3 | 检查是否有 network egress / webhook / curl / 外部 API 调用 | 是/否 |
| T-LT | 三要素汇总 | L3 | T-LT1 AND T-LT2 AND T-LT3 | 三者都"是" → **Critical**，建议重新设计 |

---

## 维度 A：触发可靠性审计（Applicability）

| 编号 | 检查项 | 等级 | 方法 | PASS 标准 | 严重性 |
|------|--------|------|------|-----------|--------|
| A1 | 正例触发测试 | L1 | 构造 3 条真实说法（L1精简） | 3 条都 should_trigger: true | Important if <2/3 |
| A2 | 反例触发测试 | L1 | 构造 2 条不应触发的说法 | 2 条都 should_trigger: false | Important if 误触发 |
| A3 | 触发词冲突检测 | L2 | Grep 已安装 Skill 的 description | 无冲突 | Important if 冲突 |
| A4 | 关键词前置 | L2 | 核心触发词在前 200 字符 | 前 200 字符含主关键词 | Minor |
| A5 | Do NOT 有效性 | L2 | Do NOT 声明具体可执行 | 不写"等"模糊范围 | Minor |

**正例构造方法**：
1. 标准说法（与 description 触发词一致）
2. 口语化改写（"做个X" → "帮我搞个X"）
3. 模糊表达（"我需要处理Y" → 隐含触发词）
4. 同义词替换（"审计" → "审查/检查/核验"）
5. 长句包含（"在我做完Z之后，还需要X"）

**反例构造方法**：
1. 相邻领域（"技能创建" 对 skill-auditor 是反例）
2. 字面相似但意图不同（"技能学习" 不是 "技能审计"）
3. Do NOT 明确排除的场景

---

## 维度 E：功能有效性审计（Effectiveness）

| 编号 | 检查项 | 等级 | 方法 | PASS 标准 | 严重性 |
|------|--------|------|------|-----------|--------|
| E1 | 声明一致性 | L2 | 审查 SKILL.md 声明的输出格式是否具体可执行 | 输出格式具体 | Important if 模糊 |
| E2 | 规则可执行性 | L2 | 审查规则是否能指导输出达到声明质量 | 规则可执行 | Important if 不可执行 |
| E3 | 示例覆盖声明能力 | L2 | 审查示例是否覆盖声明的能力范围 | 覆盖 | Minor if 部分缺失 |
| E4 | 增量价值 | L3 | 信息整合/判断建议/质量提升 | 至少一项 | Important if 仅格式转换 |
| E5 | 基线对比 | L3 | 不用 Skill vs 用 Skill | Skill 有增益 | FYI |

**注意**：E 维度不实际执行被审计 Skill 代码，只做声明一致性验证：
- 审查 SKILL.md 声明的输出格式是否具体可执行
- 审查规则是否能指导输出达到声明质量
- 审查示例是否覆盖声明的能力范围

---

## 维度 C：同类竞争审计（Competition）

**详细方法论见 [`benchmarking.md`](benchmarking.md)**，本表为概览（**仅 L3 执行**）：

| 编号 | 检查项 | 等级 | 方法 | 严重性 |
|------|--------|------|------|--------|
| C1 | SkillHub 搜索排名 | L3 | API + 质量排序公式 | FYI |
| C2 | 腾讯9维度比对 | L3 | 与 Top3 比对 | Important if 盲区 |
| C3 | 差异化分析 | L3 | 明确记录差异化 | FYI |
| C4 | 盲区识别 | L3 | 列出 Top3 揭示的盲区 | Important |
| C5 | 重复判定 | L3 | 重复度高 → 建议安装已有 | Important if >70% 重叠 |

---

## 维度 P：平台合规审计（Platform）

**仅 L3 执行**：

### P1-P5 基础平台合规（原有）

| 编号 | 检查项 | 等级 | 方法 | 严重性 |
|------|--------|------|------|--------|
| P1 | TRACE 五维度 | L3 | T/R/A/C/E 综合 | Critical if 任一 FAIL |
| P2 | SkillSpector 9 项 | L3 | YARA/Desc-Mismatch/自修改/CHANGELOG/SSD3/MCP/Least Priv/User Warnings | Critical if 任一 FAIL |
| P3 | SkillHub 文件限制 | L3 | 检查 .gitignore/LICENSE/.claude-plugin/.github | Important if 存在 |
| P4 | ClawHub 自动文件 | L3 | 检查 skill-card.md/.clawhub/ | Important if 存在 |
| P5 | 三平台 frontmatter 兼容 | L3 | ClawHub(name/description) + SkillHub(slug/displayName/version/summary/license) | Important if 缺字段 |

### P-C 系列：Coherence 审计子模式（v2.0.0 新增）

> **背景**：业界主流 Skill 平台审计的核心哲学是"coherence（一致性）"而非"找恶意"——强大行为不自动等于坏，关键是权力是否"已披露、目的对齐、比例适当"。P-C 系列系统化检查一致性。

| 编号 | 检查项 | 等级 | 方法 | PASS 标准 | 严重性 |
|------|--------|------|------|-----------|--------|
| P-C1 | Name-Summary Coherence | L3 | 对比 frontmatter `name` 与 `description`/`summary` | name 和 description 描述同一件事 | Minor if 不对齐 |
| P-C2 | Summary-Behavior Coherence | L3 | 对比 `description` 与 SKILL.md 实际行为（任务段+规则段） | description 覆盖实际行为范围 | Important if 漏报行为 |
| P-C3 | Metadata-Behavior Coherence | L3 | 对比 frontmatter 声明（env/bins/allowed-tools）与代码实际行为 | 声明 = 实际（即 D-M1/M2 通过） | Important if 不一致 |
| P-C4 | Power-Proportionality | L3 | 评估权力是否与用途成比例（审计技能需要推送权力 = 不合理；发布技能需要推送权力 = 合理） | 权力与用途成比例 | Important if 比例失当 |

**P-C 系列说明**：

- **核心哲学**：审计不是"找恶意"，是"查一致性"。强大行为不自动等于坏，关键是权力是否"已披露、目的对齐、比例适当"。
- **P-C4 Power-Proportionality 举例**：
  - ✅ 合理：发布技能（skill-publisher）需要 git push / clawhub publish 权力
  - ❌ 不合理：审计技能（skill-auditor）需要 git push 权力（审计不应推送代码）
  - ❌ 不合理：只读分析技能需要 Edit/Write 权力（除非有整改模式且需授权）
- **触发方式**：用户说"一致性审计"/"coherence 审计"可单独触发 P-C 系列检查。

---

## 维度 D：文档一致性审计（Documentation）

| 编号 | 检查项 | 等级 | 方法 | PASS 标准 | 严重性 |
|------|--------|------|------|-----------|--------|
| D1 | SKILL.md 内部引用一致 | L1 | Grep `\[.*\]\(references/.*\.md\)` → 检查文件存在 | 所有引用文件存在 | Important if 断链 |
| D2 | README 与 SKILL.md 一致 | L2 | 对比功能范围 | 一致 | Minor if 不一致 |
| D3 | 中英文 README 同步 | L3 | 对比 README.md 与 README.en.md | 内容同步 | Minor |
| D4 | CHANGELOG 版本号 | L2 | CHANGELOG 最新版本 = frontmatter version | 一致 | Important if 不一致 |
| D5 | plugin.json 与 frontmatter | L2 | 对比 name/version/description | 一致 | Minor |
| D6 | references 文件被引用 | L2 | 检查孤立文件 | 无孤立 | Minor |
| D7 | 示例完整性 | L2 | 示例覆盖 4 模块声明的输出格式 | 覆盖 | Minor |
| D-O1 | 嫁接痕迹：直接继承声明 | L2 | Grep `继承自\|based on\|forked from\|derived from\|extended from` | 零匹配（自引用除外） | Important |
| D-O2 | 嫁接痕迹：Do NOT 指向具体技能名 | L2 | 正则 `Do NOT use for [a-z][a-z0-9-]+`（点名具体技能名，非场景词） | Do NOT 用场景词（creating/publishing），不点名具体技能 | Minor |
| D-O3 | 嫁接痕迹：三角分工定位 | L2 | Grep `三角分工\|分工\|XX 负责.*本技能负责\|与.*的分工` | 零匹配 | Important |
| D-O4 | 嫁接痕迹：发布/交接措辞 | L2 | Grep `交接\|调用.*发布\|交给.*处理\|移交` | 用"建议用户手动发布"替代 | Important |
| D-O5 | 嫁接痕迹：示例点名其他技能 | L3 | 审查示例段含具体技能名（非自身） | 用场景描述替代或删除点名 | Minor |
| D-O6 | 嫁接痕迹：CHANGELOG 历史痕迹 | L3 | CHANGELOG 含"XX 创建"/"继承自"/"forked from" | 历史条目重新措辞，用场景词替代 | Minor |
| D-O7 | 嫁接痕迹：场景描述点名 | L3 | 触发条件/对比段点名具体技能作为对比 | 用场景词（"技能创建"/"技能发布"）替代 | Minor |

**D-O 系列说明**（详细识别与清洗策略见 [`originality-check.md`](originality-check.md)）：

- **适用范围**：派生技能（从其他技能 fork/继承/扩展而来）。原创技能 D-O1~O7 全部自然 PASS，不影响评分。
- **核心原则**：能用「场景描述」替代「具体技能名」就替代，不能替代的（如自引用、自身触发词）保留。
- **L1 跳过**：原型阶段允许快速派生，D-O 系列不检查。
- **L2 检查**：D-O1/O3/O4（Important 类）建议修。
- **L3 检查**：D-O1~O7 全部，Important 必修，Minor 建议修。
- **触发方式**：用户说"原创度审计"/"嫁接清洗"可单独触发 D-O 系列检查（详见 SKILL.md 触发词段）。

### D-M 系列：声明-行为一致性三层检查（v2.0.0 新增）

> **背景**：业界主流 Skill 平台审计框架的核心哲学是"coherence（一致性）"——name/summary/metadata/requested authority/actual content 是否对齐。声明-行为不一致是 SkillSpector findings 的主要来源。

| 编号 | 检查项 | 等级 | 方法 | PASS 标准 | 严重性 |
|------|--------|------|------|-----------|--------|
| D-M1 | frontmatter env 声明 vs 实际环境变量引用 | L2 | Grep 代码中 `os.environ\|getenv\|winreg.*QueryValueEx` 提取环境变量名，对比 frontmatter `metadata.openclaw.requires.env` 或 `envVars` 声明 | 代码引用的所有环境变量都在 frontmatter 声明 | Important if 未声明 |
| D-M2 | frontmatter bins 声明 vs 实际 CLI 调用 | L2 | Grep 代码中 `subprocess\|os.system\|RunCommand` 提取 CLI 工具名，对比 frontmatter `metadata.openclaw.requires.bins` 或 `requires.anyBins` 声明 | 代码调用的所有 CLI 工具都在 frontmatter 声明 | Important if 未声明 |
| D-M3 | frontmatter metadata.openclaw 完整性 | L3 | 检查 frontmatter 是否包含 `metadata.openclaw` 段（requires.env/bins/config/primaryEnv） | 有 metadata.openclaw 段或等价权限声明 | Important if 缺失 |

**D-M 系列说明**：

- **适用范围**：所有 Skill（不只是派生技能）。原创技能也必须声明-行为一致。
- **核心原则**：frontmatter 是 Skill 的"契约"，代码是"实现"。契约和实现必须一致。
- **L1 跳过**：原型阶段允许不完整声明。
- **L2 检查**：D-M1/M2（env/bins 声明）建议修。
- **L3 检查**：D-M1/M2/M3 全部，Important 必修。
- **修复方式**：参见 [`skill-authoring-guide.md`](skill-authoring-guide.md) 第二部分 frontmatter 规范。
- **触发方式**：用户说"声明一致性审计"可单独触发 D-M 系列检查。

---

## 维度 Q：代码质量审计（Code Quality）

**检查范围**：`scripts/` 下的 Python / JavaScript / PowerShell 脚本

| 编号 | 检查项 | 等级 | 方法 | PASS 标准 | 严重性 |
|------|--------|------|------|-----------|--------|
| Q1 | 错误处理 | L2 | Grep `try\|except\|catch` | 外部调用有错误处理 | Important if 无 |
| Q2 | 资源管理 | L2 | Grep `with \|finally\|close()` | 文件/网络/进程正确关闭 | Important if 泄漏 |
| Q3 | 命名规范 | L2 | 人工审查 | snake_case(Python)/camelCase(JS) | Minor |
| Q4 | 复杂度 | L2 | 单函数 ≤50 行，嵌套 ≤4 层 | 符合 | Minor if 超标 |
| Q5 | 硬编码 | L2 | Grep 路径/URL/凭证模式 | 使用环境变量/配置 | Critical if 凭证硬编码 |
| Q6 | 日志规范 | L3 | Grep `print(` vs `logging` | 生产脚本用 logging | Minor |
| Q7 | 类型注解 | L3 | 检查 Python 函数签名 | 推荐有注解（非强制） | FYI |
| Q8 | 幂等性 | L3 | 人工审查 | 重复执行安全 | Minor |

**无 scripts/ 目录时**：Q 维度标注"无代码，跳过"，不扣分。

---

## 评分计算

### 基础评分（0-10 分，保留）

每个维度 0-10 分：
- 9-10: 优秀，无问题或仅 FYI
- 7-8: 良好，少量 Minor
- 5-6: 及格，有 Important
- 3-4: 不及格，多个 Important
- 0-2: 严重问题，有 Critical

**综合分加权平均**：
```
综合分 = (S×1.0 + T×2.0 + A×1.0 + E×1.0 + C×0.5 + P×1.5 + D×0.5 + Q×0.5) / 8.0
```

**一票否决**：T 维度有 Critical → 综合状态 = ❌ FAIL（不论综合分多高）

### 双维度评分（v2.0.0 新增）

> **背景**：业界主流 Skill 平台采用"Risk Level + Audit Status"正交双维度模型——高风险不等于不通过，关键是权力是否合理披露。

#### Risk Level（权力大小）

基于 Skill 声明的权力评估，与审计结果无关：

| Risk Level | 判定条件 | 典型技能 |
|-----------|---------|---------|
| **Low** | 只读分析，无副作用，无外部通信 | 审计技能、文档转换技能 |
| **Medium** | 修改本地文件，有副作用但限于本地 | 整改模式技能、本地文件处理技能 |
| **High** | 推送外部平台 / 网络外发 / 访问私有数据 | 发布技能、同步技能、邮件技能 |

**Risk Level 评估信号**：
- allowed-tools 含 Bash/git push/curl → High 倾向
- 有 Edit/Write 但无外部通信 → Medium 倾向
- 只有 Read/Glob/Grep → Low 倾向
- metadata.openclaw.requires.env 含凭证 → 权力升级

#### Audit Status（权力是否合理）

基于审计结果评估，与 Risk Level 正交：

| Audit Status | 判定条件 | 含义 |
|-------------|---------|------|
| **Pass** | 无 Critical + 无 Important + 综合分 ≥ 7.0 | 可发布 |
| **Review** | 无 Critical + 少量 Important + 综合分 ≥ 5.0 | 建议修复后发布 |
| **Warn** | 有 Important 涉及安全 + 综合分 ≥ 5.0 | 需重点修复 |
| **Fail** | 有 Critical 或综合分 < 5.0 | 不可发布 |

#### Risk-Status 矩阵解读

| | Pass | Review | Warn | Fail |
|---|------|--------|------|------|
| **High Risk** | ✅ 权力大但已披露且比例适当，可发布 | ⚠️ 权力大且有遗漏，修复后可发布 | ⚠️ 权力大且有问题，需重点修复 | ❌ 不可发布 |
| **Medium Risk** | ✅ 可发布 | ⚠️ 修复后可发布 | ⚠️ 需修复 | ❌ 不可发布 |
| **Low Risk** | ✅ 可发布 | ⚠️ 可发布但建议修复 | ⚠️ 需修复 | ❌ 不可发布 |

**关键原则**：High Risk + Pass 是完全合理的——一个发布技能自然需要 High Risk 权力，只要权力已披露、目的对齐、比例适当，Audit Status 可以是 Pass。

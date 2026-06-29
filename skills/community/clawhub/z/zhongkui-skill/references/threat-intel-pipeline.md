# 钟馗漏洞系统自进化-R12 漏洞情报

> 目标：将钟馗从"硬编码签名库"升级为"威胁情报驱动的自适应审查引擎"

## 整体架构

```
威胁情报摄入 → 签名生成 → 检查项扩展 → 权重校准 → 回归验证 → 发布
```

## 1. 威胁情报摄入

### 1.1 情报源对照表（人工参考）

| 网站/平台 | 侧重方向 | 说明 |
|-----------|----------|------|
| OWASP LLM Top 10 | 权威风险分类（R1-R12） | OWASP 发布了专门针对 LLM 应用和 Agent 的安全风险 Top 10。这是最权威的分类标准，能让你一眼认出什么是"提示注入"（R1）什么是"Agent 滥用"（R12） |
| Hugging Face / ArXiv | 前沿攻击向量论文 | 学术界的主战场。搜索关键词如 "Agent Hacking"、"Tool Augmentation Attack"。这里能看到最新的攻击手法（比如如何利用工具参数注入来绕过审查），属于"红队"视角的情报 |
| GitHub Security Repos | 实战 PoC（概念验证） | 搜索 agent-security、llm-pentest 等关键词。很多安全研究员会在这里开源他们的漏洞利用代码（PoC）和检测工具，这是最实战的"漏洞库" |
| NVD（NIST 国家漏洞数据库） | 传统 CVE 关联 | 虽然 R12 本身难编号，但如果 Agent 漏洞导致了底层库的溢出（比如 R2 恶意代码执行），这里会有记录 |
| 各大云厂商安全公告（AWS/Azure/GCP） | 供应链与托管风险 | 如果你用的是云上的 Agent 服务，这里的公告会涉及 R11（外部信息源投毒）或 R4（依赖投毒）相关的供应链风险 |

### 1.2 自动化摄入源（仅保留 CVSS 客观评分的源）

筛选标准：情报项本身携带可量化的置信度/严重度指标（CVSS score），可直接映射到签名生成 `confidence` 字段。Stars / 社区热度 / 无评分的博客公告一律排除。

#### 1.2.1 NVD（NIST 国家漏洞数据库）— CVSS v3.1

| 项目 | 端点 / 参数 | 置信度 |
|------|------------|--------|
| REST API 基地址 | `https://services.nvd.nist.gov/rest/json/cves/2.0` | — |
| 关键词搜索 | `?keywordSearch=prompt+injection&resultsPerPage=20` | CVSS v3.1 baseScore (0-10) |
| 精确匹配 | `?keywordSearch=LLM+agent+security&keywordExactMatch` | — |
| 严重度过滤 | `?cvssV3Severity=CRITICAL&keywordSearch=AI+agent` | CRITICAL / HIGH / MEDIUM / LOW |
| 日期范围 | `?pubStartDate=YYYY-MM-DDT00:00:00.000&pubEndDate=YYYY-MM-DDT23:59:59.999`（≤120天） | — |
| API Key（推荐） | https://nvd.nist.gov/developers/request-an-api-key | 无Key: 5req/30s；带Key: 50req/30s |

LLM/Agent 相关 CWE 映射表：

| CWE | 名称 | 对应钟馗风险 |
|-----|------|-------------|
| CWE-94 | Code Injection | R1（Prompt注入执行）、R11（外部信息源投毒） |
| CWE-74 | Improper Neutralization | R1/R11 |
| CWE-20 | Improper Input Validation | R1 |
| CWE-427 | Uncontrolled Search Path | R4（依赖投毒） |
| CWE-494 | Download Without Integrity Check | R4 |
| CWE-918 | SSRF | R10（工具调用 SSRF） |
| CWE-200 | Exposure of Sensitive Info | R2（敏感信息泄露） |
| CWE-668 | Exposure to Wrong Sphere | R7（系统 Prompt 泄露） |

摄入：每日拉取过去 7 天 CRITICAL/HIGH CVE，按 keyword + CWE 二次过滤，CVSS baseScore 归一化到 0-1 作为签名 confidence。

#### 1.2.2 Snyk 漏洞数据库 — CVSS v3.1

| 项目 | 端点 | 置信度 |
|------|------|--------|
| Snyk 漏洞数据库 | `https://security.snyk.io/` | CVSS v3.1 score |
| Snyk V1 API | `GET https://api.snyk.io/v1/vulns`（需 Enterprise Token） | 每漏洞含 CVSS |
| Snyk REST API 文档 | `https://apidocs.snyk.io/` | — |

摄入：每日 V1 API 按 ecosystem（pip/npm）过滤新增漏洞，CVSS 归一化到 0-1。

#### 1.2.3 Seebug 漏洞库 — CVE 严重度

| 项目 | 端点 | 置信度 |
|------|------|--------|
| Seebug 最新漏洞 RSS | `https://www.seebug.org/rss/new` | CVE 条目含 severity（高/中/低危） |

摄入：每日 RSS 增量，按 keyword（AI / LLM / Agent / prompt / 供应链）过滤，severity→0-1 映射（高→0.8, 中→0.5, 低→0.2，见 §1.2.5 归一化说明）。

#### 1.2.4 覆盖盲区与补救

CVSS 主要覆盖传统软件漏洞（CWE），与 R1-R12 的 LLM/Agent 特有风险存在语义错位。以下风险类别在三个自动化源中覆盖率接近零：

| 风险 | 覆盖 | 原因 |
|------|------|------|
| R3 过度代理 | 零 | 无限 CWE 对应 |
| R5 权限过度 | 零 | 无限 CWE 对应 |
| R6 输出过滤不足 | 零 | 无限 CWE 对应 |
| R8 自主决策 | 零 | 无限 CWE 对应 |
| R9 跨会话持久化 | 零 | 无限 CWE 对应 |
| R12 Agent 滥用 | 零 | 无限 CWE 对应 |

**补救路径**：对上述盲区类别，走"论文→模式提取"半自动链路。即利用 §1.1 中的 HuggingFace/ArXiv/GitHub 作为人工情报源，在手动周会（见 §8）中由分析员阅读最新攻击论文后，手动将攻击模式编码为签名碎片注入 `patterns.json`。该路径不依赖 CVSS 置信度，confidence 由分析员主观评定（0.5-0.9），在签名 JSON 中标记 `source_type: "manual"` 以区别于自动摄入。

#### 1.2.5 跨源 Confidence 归一化

三个源使用不同精度等级的评分体系，合并前需统一归一化策略：

| 源 | 原始评分 | 归一化到 [0,1] |
|----|---------|---------------|
| NVD | CVSS v3.1 baseScore (0-10，粒度 0.1) | `score / 10` |
| Snyk | CVSS v3.1 score (0-10，粒度 0.1) | `score / 10` |
| Seebug | severity 高/中/低（3 级离散） | 高→0.8，中→0.5，低→0.2（缩窄间距以降低离散值的权重放大效应） |

Seebug 的离散映射值从 {0.9, 0.6, 0.3} 收紧至 {0.8, 0.5, 0.2}，避免三档离散值过度挤压 NVD/Snyk 连续值的区分空间。后续评分器可在顶层对 `source_type` 引入衰减因子（非 CVSS 源 ×0.85），进一步补偿粒度差异。

### 1.3 摄入频率总表

| 源 | 频率 | 窗口 | 每次量 | 置信度类型 | 归一化 |
|----|------|------|--------|-----------|--------|
| NVD REST API | 每日 | 过去 7 天 | CRITICAL/HIGH CVE | CVSS v3.1 baseScore | score/10 → [0,1] |
| Snyk V1 API | 每日 | 过去 1 天（增量） | 新增漏洞 | CVSS v3.1 score | score/10 → [0,1] |
| Seebug RSS | 每日 | 过去 1 天（增量） | 新条目 | severity 高/中/低 | {0.8, 0.5, 0.2} → [0,1] |

### 1.4 排除源清单（含排除原因）

| 源 | 排除原因 |
|----|---------|
| OWASP LLM Top 10 | 分类列表，无 per-item 评分 |
| ArXiv / HuggingFace Papers | 论文无客观安全置信度，投票数属社区热度 |
| GitHub Repos（garak/promptfoo 等） | Stars 是社区热度，非安全置信度 |
| AWS / Azure / GCP 安全公告 | 公告无严重度评分 |
| 腾讯科恩/玄武/CSA/奇安信 | 博客/报告级别无 per-item 置信度 |

## 2. 签名生成

### 2.1 流程

```
原始报告 → LLM 提取攻击模式 → 碎片化编码 → 写入 patterns.json
```

1. **攻击模式提取**：将报告正文喂入 LLM，要求输出结构化的攻击描述：
   - 攻击向量关键词（英文碎片）
   - 攻击目标层级（SKILL.md / scripts / deps）
   - 对应风险类型（R1-R12）
   - 置信度（0-1）

2. **碎片化编码**：将关键词拆解为 pieces 格式，确保关键词本身不被安全引擎误判为攻击载荷：
   ```json
   {
     "id": "CXX_NNN",
     "pieces": ["frag", "ment1"],
     "source": "OWASP-LLM-2026-03",
     "confidence": 0.85,
     "added": "2026-06-13"
   }
   ```

3. **去重与归并**：与现有碎片做语义相似度比对（embedding cosine > 0.9 则归并），仅追加新碎片。

### 2.2 质量门禁

| 门禁 | 规则 | 阻断条件 |
|------|------|----------|
| 碎片格式校验 | JSON schema 严格匹配 | 格式不符 → 丢弃 |
| 自匹配测试 | 碎片串接后对钟馗自身 SKILL.md 做匹配 | 误报 → 标记 `false_positive: true` |
| | *目标：验证新碎片不会误伤钟馗自身的安全规则描述文本。钟馗 SKILL.md 中含大量安全术语（如"prompt 注入""代码执行"等），碎片化编码时需确保这些规则描述不被自身检查项误判为攻击载荷* | |
| 回归测试 | 对已知干净 Skill 跑全量审查 | 新增误报 > 0 → 阻断 |

## 3. 检查项扩展

### 3.1 触发条件

当威胁情报摄入识别出**当前 54 项未覆盖的攻击面**时触发：

- 新风险类别（如 prompt-extraction 提取攻击）
- 已知风险类别的新攻击向量（如 R12 的工具参数时间窗口注入）
- 新文件类型（如 `.wasm` / `.dll` 出现在 Skill 包中）

### 3.2 扩展流程

1. 人工审核确认 → 定义检查项编号、检测逻辑
2. 实现 `_check_skill_content()` / `_check_scripts()` 中的新增代码
3. 更新 `static-audit.md` 文档
4. `checks_total` 自动 +1

### 3.3 扩展记录表

<!-- 模板，待首次扩展后填充 -->

| 版本 | 检查项 | 来源 | 日期 |
|------|--------|------|------|
| — | — | — | — |

## 4. 权重校准

### 4.1 数据来源

- **误报反馈**：用户对审查结果的"此项为误报"标记
- **漏报反馈**：已知恶意 Skill 未命中 → 标记为漏报
- **基准测试**：定期对标注数据集（干净 ×50 / 恶意 ×50）跑全量审查

### 4.2 校准公式

使用加权 Fβ 分数驱动权重调整。β 的选取需定量论证，MVP 阶段取 β=2（漏报权重为误报的 4 倍）作为初始假设，待首轮反馈数据积累后做灵敏度分析验证：

| β | 漏报:误报权重比 | 适用场景 |
|----|-----------------|----------|
| 0.5 | 1:4 | 误报成本极高（如阻断型系统） |
| 1.0 | 1:1 | 漏报与误报等成本 |
| 2.0 | 4:1 | 漏报成本显著高于误报（安全审查场景，默认） |
| 3.0 | 9:1 | 漏报不可接受（如入侵检测） |

网格搜索时以 β=2 为基线，同时输出 β=1 和 β=3 的权重解作为对照，避免单一 β 假设锁定次优解。

```
F2 = (1+2²) × precision × recall / (2² × precision + recall)
```

每季度基于反馈数据跑一次网格搜索，在权重空间中找到 F2 最优解，自动更新 `scorer.py` 中的权重分配。

### 4.3 校准记录

<!-- 模板，待首次校准后填充 -->

| 日期 | W1 (L1) | W2 (L2) | W3 (Data) | F2-score | 变更原因 |
|------|---------|---------|-----------|----------|----------|
| — | 0.85 | — | 0.15 | — | 初始离线基线 |

## 5. 回归验证

每次签名/权重更新后，自动执行：

1. **干净 Skill 集**（≥10 个已知安全 Skill）→ 确保无误报引入
2. **恶意 Skill 集**（≥10 个已知恶意 Skill）→ 确保检出率不下降
3. **对照 Skill 集**（≥5 个边界案例）→ 确保裁定不漂移

> **规模说明**：以上为 MVP 初始规模（总计 25+ 样本）。随着反馈数据积累，目标扩展至干净集 ≥50、恶意集 ≥50、对照集 ≥20，使其 F2-score 的 95% 置信区间收窄至 ±0.05 以内，支撑有统计显著性的校准迭代。

## 6. 发布策略

| 模式 | 触发条件 | 动作 |
|------|----------|------|
| 静默更新 | 仅新增碎片，回归全绿 | 自动合并到 patterns.json |
| 审查更新 | 新增检查项/修改权重 | 生成 PR，人工 Review 后合并 |
| 阻断 | 回归失败 / 门禁未通过 | 回滚，生成失败报告 |

## 7. 当前状态与待办

| 环节 | 状态 | 预计周期 | 备注 |
|------|------|----------|------|
| 威胁情报摄入 | ✅ 已实现 | `core/intel/updater.py` | NVD + Seebug 双源自动拉取，三层过滤，碎片化生成，去重注入 |
| 签名生成 | ✅ 已实现 | `generate_patterns()` | 滑动窗口短语提取 + 碎片化编码，每 CVE 最多 1 条 |
| 检查项扩展 | 人工 | 按需（由情报触发） | 需要人工发现新攻击向量 |
| 权重校准 | 未实现 | MVP 积累 ≥200 条反馈后启动 | 缺乏反馈数据积累 |
| 回归验证 | 未实现 | 第一轮校准前完成测试集构建 | 缺乏标准测试集 |
| 发布策略 | ✅ 已实现 | `zhongkui.py --update` | 交互确认后注入 patterns.json，自动备份后写入新版 |

### 7.1 更新标准与准入规范

确立以下不可变的更新准则，确保增量签名质量不打折扣：

| 维度 | 标准 | 执行者 |
|------|------|--------|
| **更新频率** | 无硬性周期，按需执行 `--update` | 用户 |
| **摄入源** | NVD API（CVSS v3.1 CRITICAL/HIGH，7 天窗口）+ Seebug RSS（高/中/低 severity） | `updater.py` |
| **关键词过滤** | CVE 描述命中 `INTAKE_KEYWORDS`（含 prompt injection / LLM / agent / jailbreak 等 26 词），排除 `EXCLUDE_KEYWORDS`（DoS / 硬件 / WordPress / ColdFusion / Adobe 等 17 词） | `filter_cves()` |
| **安全精确过滤** | 候选 CVE 必须命中 `AGENT_SAFETY_KEYWORDS`（21 项 Agent/Skill 特有安全术语，如 prompt injection / jailbreak / sandbox escape / MCP / tool call），词级匹配排除传统 Web RCE | `filter_cves()` |
| **文本剥离** | 跳过产品介绍句（"X is a tool/framework/..."），剥离 "Prior to version X, " 前缀，跳过纯修复/版本/致谢句 | `_extract_vuln_text()` |
| **CWE 路由** | 9 个 CWE→钟馗分区映射（CWE-94→C1_injection，CWE-918→S2_network 等），无匹配默认归 C1_injection | `CWE_CATEGORY_MAP` |
| **去重** | `label` 唯一性：跨基础库 + 当前增量去重 | `update_patterns_json()` |
| **碎片化** | 单片段 ≤6 字符，确保不含完整攻击关键词；词间 `[\s\S]{0,20}?` 弹性分隔，容纳原文中的停用词与符号（如 &、-） | `_fragment_phrase()` |
| **置信度** | CVSS / 10 归一化到 0-1（NVD），Seebug 映射 {高→0.8, 中→0.5, 低→0.2} | `generate_patterns()` |
| **基础库保护** | `source: "manual"` 签名永不触碰，`--update` 仅替换 `source: "nvd-*"` / `"seebug-*"` 增量 | `_clean_auto_patterns()` |
| **幂等性** | 每次 `--update` 先清旧增量再注入最新，重复运行不产生重复签名 | `run_update()` |
| **回滚** | 注入前自动备份 `patterns.json.bak`，可手动恢复 | `update_patterns_json()` |

## 8. 最小可行启动方案

当前状态：MVP 前两步已自动化，第三步保持人工。

1. ~~**手动情报周会**~~ → **已自动化**：`python zhongkui.py --update` 从 NVD + Seebug 自动拉取、过滤、生成碎片化签名，交互确认后注入。盲区类别（HuggingFace/ArXiv/GitHub）仍须人工覆盖 §1.2.4。
2. ~~**单一签名注入**~~ → **已自动化**：`update_patterns_json()` 按 CWE 分区路由注入，自动去重、备份、版本号递增。
3. **自审回归**：每次更新后跑 `python zhongkui.py . --quick` 确认无自审崩溃。此项保持人工——签名质量需要人眼抽查。

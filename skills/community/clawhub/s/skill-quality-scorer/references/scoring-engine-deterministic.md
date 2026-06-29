# Skill Quality Scorer · 确定性评分引擎 v2

**职责**：对目标 Skill 目录输出结构化评分 JSON。  
**原则**：确定性、可重复、先静态后 rubric、禁止凭感觉给分。

**体系**：**TRACE+ 六维（T-R-F-S-I-E）× 30 子项** — TRACE 为骨架，Extra08 / skill-creator / skill-reviewer / skill-quality-audit 等为血肉；各维标题与子项表内已标注来源。

---

## 硬规则

### 1. 与 static_audit 的优先级

1. 运行 `scripts/static_audit.py`（v2.0+）
2. `auto_scores`：**必须使用脚本建议分**，LLM 仅补 evidence
3. `flags` 中 `severity: critical` → 对应 **T** 子项为 0，`verdict` 最低 `Fail`

**T 维扫描范围**（脚本实现）：`SKILL.md` + `scripts/`/`assets/` 可执行文件；**不**扫描 `references/`、`examples/` 中的 rubric 示例字面量，避免误报。

### 1b. auto_scores vs 人工评（30 子项）

| 子项 | 来源 | 说明 |
|------|------|------|
| R1, R2 | **auto** | frontmatter、链接 404 |
| F1, F4, F5 | **auto** | when 语义、name 规范、description 长度（CSO） |
| S1, S2, S4, S5 | **auto** | body 行数、refs 链接、extraneous 文件、L1 篇幅 |
| I1, I3 | **auto** | 人类文档反模式、代码块数量与 lang tag |
| T1（部分） | **auto** | critical 模式命中 → 0 |
| T2–T5, R3–R5, F2–F3, S3, I2, I4–I5, E1–E5 | **manual** | 须读 SKILL.md / scripts 全文给 evidence |

> **F5 vs S5**：均用 description 长度启发，但含义不同——**F5** 评 CSO（description 是否抢跑写 workflow）；**S5** 评 L1 体量（是否浪费触发层上下文）。同一 metrics 可得出相同分，evidence 须分写。

> **I3 与脚本**：`static_audit` 只计**开块** fence（忽略闭合 ```）；判 2 分需 ≥2 代码块且开块均有 language tag。

### 2. 子项打分（统一）

| 判定 | 分值 | 标准 |
|------|------|------|
| **完整** | 2 | 可核验、满足子项定义 |
| **部分** | 1 | 有涉及但不完整或模糊 |
| **缺失** | 0 | 完全没有或明确违规 |

### 3. 综合分公式（六维）

默认六维均参与（无 N/A）：

```
composite_score = round((T + R + F + S + I + E) × 100 / 60, 1)
```

等价于六维平均分 × 10（每维满分 10，六维满分 60 → 映射到 100 分制）。

**算术校验（必须）**：

```
assert composite_score == round((T+R+F+S+I+E) * 100 / 60, 1)
```

**旧版五维公式已废弃**：`(T+R+A+C+E)×2` 仅适用于 v1，不得混用。

### 4. 评级

| 评级 | 分数 | 含义 |
|------|------|------|
| S | 90–100 | 发布就绪 |
| A | 80–89.9 | 良好 |
| B | 70–79.9 | 合格，有明显短板 |
| C | 60–69.9 | 较差 |
| D | 0–59.9 | 不合格 |

### 5. Verdict

| Verdict | 条件 |
|---------|------|
| **Pass** | 无 T 维 critical，且 composite ≥ 80 |
| **Conditional Pass** | 无 critical，composite 70–79.9 |
| **Fail** | T 维 critical，或 composite < 70 |

### 6. E 维模式

| 模式 | 条件 |
|------|------|
| `static_proxy` | 默认；E 子项按文档/工作流静态判断 |
| `behavioral_eval` | 用户提供 with/without skill 或 skill-eval 结果；E3/E5 须引用 eval |

---

## T — Trust 安全可信（TRACE T · SkillGuard / skill-vetter）

| # | 子项 | 2 | 1 | 0 |
|---|------|---|---|---|
| T1 | 无远程任意执行 | 无 curl\|bash 等 | 网络读文档不执行 | 远程代码执行 |
| T2 | 凭证与隐私 | 不读密钥或边界清晰 | 提及敏感路径有说明 | 未说明收集/外传 |
| T3 | 无混淆恶意 | 无 base64/eval 链 | 编码非执行用途 | 混淆隐藏执行 |
| T4 | 权限最小化 | 无 sudo 或 scope 匹配 | elevated 有文档 | 过度权限 |
| T5 | 意图一致 | 文档与 scripts 一致 | 轻微夸大 | 隐藏任务/注入 |

> T1/T3 critical → Fail

---

## R — Reliability 运行可靠（TRACE R · skill-refiner）

| # | 子项 | 2 | 1 | 0 |
|---|------|---|---|---|
| R1 | Frontmatter 合法 | YAML 可解析，name+description | 核心完整 | 损坏或缺字段 |
| R2 | 引用文件存在 | 链接的 references/scripts/assets 均存在 | 个别次要 404 | 核心缺失 |
| R3 | 脚本可调用 | 有路径/命令说明 | 有脚本但模糊 | 声称有却无法定位 |
| R4 | 依赖可预期 | 依赖写清或仅标准库 | 隐含常见依赖 | 缺说明必败 |
| R5 | 无占位阻塞 | 主流程无 TODO/FIXME | 非关键占位 | 主流程占位 |

---

## F — Findability 可发现性（TRACE A · skill-reviewer Description · CSO）

| # | 子项 | 2 | 1 | 0 |
|---|------|---|---|---|
| F1 | When 在 description | 含 Use when / 当用户…时使用 | 有场景无明确 when | 仅 helps with X |
| F2 | 触发词覆盖 | ≥2 具体说法/任务类型 | 仅 1 个泛化词 | 无触发词 |
| F3 | 可搜索关键词 | 领域词自然出现（skill-reviewer） | 关键词偏少 | 过于泛化无检索面 |
| F4 | 命名规范 | name=目录，kebab-case，≤64 | 小瑕疵 | 不一致或非法 |
| F5 | CSO 防抢跑 | description **不写完整 workflow**（触发层只答 when/what，步骤在 body） | 轻微 workflow 摘要 | 长流程写在 description |

---

## S — Structure 结构（TRACE C · skill-creator L1/L2/L3 · Extra08）

| # | 子项 | 2 | 1 | 0 |
|---|------|---|---|---|
| S1 | Body 体量 | body ≤500 行 | 501–800 | >800 或无结构 |
| S2 | 渐进式披露 | 详文在 references/ 且 body 链接 | 有 refs 链接不全 | 全堆 body |
| S3 | 资源分层 | scripts/执行、references/阅读、assets/产出分工清晰 | 部分混淆 | 无分层或混用 |
| S4 | 无人类文档 clutter | skill 包内无 CHANGELOG/INSTALLATION 等（Extra08） | 1 个冗余 md | 多个冗余 |
| S5 | L1 篇幅 | description ≤~500 字符 / ~100 词（**L1 触发层**体量，非 CSO 语义） | 略超仍可接受 | 严重超长占上下文 |

---

## I — Instruction 指令质量（Extra08 反向 · skill-reviewer · skill-quality-audit）

| # | 子项 | 2 | 1 | 0 |
|---|------|---|---|---|
| I1 | 祈使指令体 | 命令式步骤，非「你可以考虑」（Extra08） | 混用 | 人类文档体/背景叙事 |
| I2 | 按任务组织 | 按场景/操作分节（skill-reviewer） | 部分按概念 | 纯理论/背景章 |
| I3 | 示例质量 | ≥2 代码块，有 language tag，可复用 | 1 个或缺 tag | 无示例 |
| I4 | 可执行性 | 有序步骤 + 验收/失败 | 部分 | 仅原则 |
| I5 | Rigid/Flexible + 脚本 | 风险匹配 + 脆弱处有 scripts | 其一缺失 | 均缺失 |

---

## E — Effectiveness 效果增益（TRACE E · skill-eval 可选）

| # | 子项 | 2 | 1 | 0 |
|---|------|---|---|---|
| E1 | 工作流闭环 | 采集→执行→输出闭环 | 缺一环 | 无闭环 |
| E2 | 输出格式锁 | 模板/JSON schema/分区顺序明确 | 部分 | 无输出定义 |
| E3 | 行为增益证据 | 有 eval 或 no-skill 对照 | static_proxy 可执行性强 | 无法证明增益 |
| E4 | 硬约束/反模式 | 明确禁止编造/禁止项（Extra08 不做什么） | 部分 | 无边界 |
| E5 | Token 效率 | 无教模型常识的废话 | 少量 | 大段说教 |

> 默认 `effectiveness_mode: static_proxy` 时，E3 最高 1 分（除非 static 工作流极强且 I4=2）。

---

## 输出 JSON 结构（v2）

```json
{
  "rubric_version": "2.0.0",
  "framework": "TRACE+ TRF-SIE",
  "skill_name": "folder-name",
  "skill_path": "...",
  "effectiveness_mode": "static_proxy",
  "behavioral_eval": false,
  "static_audit_version": "2.0.0",
  "score_breakdown": {
    "T_Trust": { "T1_...": { "score": 2, "evidence": "...", "source": "static" }, "subtotal": 10 },
    "R_Reliability": { "subtotal": 10 },
    "F_Findability": { "subtotal": 8 },
    "S_Structure": { "subtotal": 9 },
    "I_Instruction": { "subtotal": 9 },
    "E_Effectiveness": { "subtotal": 8 }
  },
  "scores": { "T_Trust": 10, "R_Reliability": 10, "F_Findability": 8, "S_Structure": 9, "I_Instruction": 9, "E_Effectiveness": 8 },
  "composite_score": 90.0,
  "rating": "S",
  "verdict": "Pass",
  "source_coverage": ["TRACE", "Extra08", "skill-reviewer", "skill-quality-audit"],
  "formula_check": "(10+10+8+9+9+8)*100/60=90.0 OK",
  "trigger_tests": {
    "should_trigger": ["…", "…", "…"],
    "should_not_trigger": ["…", "…", "…"]
  }
}
```

**可选字段**：`trigger_tests`（F 维，各 ≥3 条，见 audit-playbook）

**校验**：

- 六维各 5 子项 + subtotal
- `scores[d] == subtotal`
- `composite_score == round(sum(scores)*100/60, 1)`
- 每项 evidence 非空

---

## 常见错误

| 错误 | 正确 |
|------|------|
| 只用 TRACE 五维旧公式 | 用六维 ×100/60 |
| 忽略 CSO / description 质量 | 评 **F** 维 |
| 忽略 Extra08「人类文档反模式」 | 评 **I1** |
| 忽略 skill-reviewer 示例/组织 | 评 **I2/I3** |
| E3 给 2 分但无 eval | static_proxy 下 E3 最高 1 |

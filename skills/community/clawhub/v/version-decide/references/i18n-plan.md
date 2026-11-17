# 英文版（i18n）支持实施规划 — version-decide

> **⚠️ 维护者记录，非运行期指令。** 本文件（含 §5 落地步骤 P6/P7、§6 版本号决策、§7 门禁，及 §10
> 发布记录）记载的是本 skill **维护流程**里的发布动作——跑门禁、打 tag、推远端、建 Release。
> 这些是**人工操作**：本技能声明的 `allowed-tools` **不授予**写/网络/包管理权限，
> `scripts/semver_check.py` **从不执行**这些动作，也不应在版本判定流程中被读取为运行时指引。
> 只有当你明确要做发版时，才把其中步骤当作参考。

> 本文件是**实施规划**，不是实现。目标是让 skill 满足 ClawHub 的 Natural Language Policy，
> 同时保留「中文用户得到中文输出」的体验。所有结论均附 ClawHub 权威来源。

---

## 0. 依据：ClawHub Natural Language Policy（已核实）

| # | 来源 | 关键条款 | 对本 skill 的含义 |
|---|---|---|---|
| A | `automatic-skill`（clawhub.ai/cosmofang/skills/automatic-skill）自带 🌐 Language Policy | ① SKILL.md content：**English (default)**；② Conversation with user：**match user's language**（写中文就回中文）；③ JSON logs & reports：**English only** | 正文默认英文；**对话输出**跟随用户语言；**日志/报告类 JSON 必须英文** |
| B | `repo-onboarding-guide` 安全审计（clawhub.ai/52yuanchangxing/skills/repo-onboarding-guide/security-audit） | **Natural-Language Policy Violations (Medium, 91–96%)**：整份 skill 只用一种语言、且**未提供用户语言选择 / 未声明地区合理性**即为违规。触发点：title/summary/categoryLabel/examples/risk 全中文、生成报告串全中文且无语言选项 | 不能「全中文且不给选项」；必须要么**提供语言切换**，要么**声明地区专属合理性** |
| C | `modbender-clawhub-skill-creator`（skillsdirectory.com） | **Required in English**：SKILL.md frontmatter `description`、`_meta.json` `description`、`Main workflow instructions`；**May use other languages**：code examples / comments / domain-specific references / user-facing examples | `description` 必须是英文；正文指令默认英文；代码注释、领域参考可保留中文 |

**合规结论（必须同时满足）**：
1. `description`（frontmatter）改为**英文**（来源 A① + C）。
2. SKILL.md 正文（Main workflow instructions）改为**英文默认**（来源 A① + C）。
3. **用户面向输出**跟随用户语言（写中文回中文）（来源 A② + C「user-facing examples 可其他语言」）。
4. **JSON 日志/报告**保持英文（来源 A③）。
5. 不得「全中文且零选项」——必须提供语言选择或声明地区合理性（来源 B）。

---

## 1. 现状差距分析（Gap Analysis）

| 资产 | 现状 | 是否违规 | 处理 |
|---|---|---|---|
| `SKILL.md` `description`（第 8 行） | 中文：「根据代码变更范围判定下一个版本号…」 | ✅ **违规**（来源 A①/C） | 改为英文（合规关键） |
| `SKILL.md` 正文 | 全中文指令 | ⚠️ 应英文默认（来源 A①/C） | 改写为英文；保留「输出跟随用户语言」说明 |
| `scripts/semver_check.py` 的 `reasons` 串 | 中文散文（如「全部变更均不触及公共 API…」） | ⚠️ 属用户面向输出，应跟随用户语言（来源 A②） | 抽取到 locale 表，按 `--lang` 选择 |
| `references/decision-tables.md` / `standards-comparison.md` | 中文领域参考 | ✅ 允许（来源 C「domain-specific references 可其他语言」） | 建议镜像英文版，非强制 |
| `semver_check.py` 代码注释 | 中文注释 | ✅ 允许（来源 C「comments 可其他语言」） | 保留不动 |
| JSON 输出 keys | `current/next/level/has_breaking` 等英文 | ✅ 已合规 | 保持 |
| JSON 输出 `reasons` 值 | 中文 | ⚠️ 张力点（见 §8） | 视为「对话输出」随语言；新增 `--report` 报告模式则强制英文 |

---

## 2. 目标语言架构（Target Architecture）

```
用户提问语言 ──┐
               ├─→ SKILL.md 指令（英文默认）引导 LLM 用「用户语言」产出版本建议
CLI --lang ───┘
   en │ zh │ auto
        │
        ▼
locales/<lang>.yaml  ──→ semver_check.py 的 reasons / 错误提示 / 级别名
```

- **LLM 对话路径**：SKILL.md 用英文写规则，但显式指令「用与用户相同的语言输出最终建议」。
- **CLI 路径**：`semver_check.py` 通过 `--lang en|zh|auto` 选择 locale；`auto` 读 `LC_ALL`/`LANG`，回退 `en`（满足「English default」）。

---

## 3. 语言文件结构（File Structure）

在现有结构上**新增** `locales/`，不改动既有文件布局：

```
version-decide/
├── SKILL.md                    # 正文改英文默认；description 改英文；新增 Language 小节
├── README.md
├── locales/                   # ★ 新增
│   ├── en.yaml                # 英文串表（默认 / 回退）
│   └── zh.yaml                # 中文串表（与当前 behavior 等价）
├── scripts/
│   ├── semver_check.py        # 增加 load_locale() / _(key) / --lang
│   ├── measure_skill.py
│   └── test_semver_check.py   # 增补跨语言断言
└── references/
    ├── decision-tables.md     # 英文为主，可附中文注
    ├── standards-comparison.md
    └── i18n-plan.md           # 本文件
```

`_meta.json`（可选，来源 C 提及）仅在某个平台明确要求时补，含英文 `description`；clawHub 官方 skill-format 以 SKILL.md frontmatter 为准，故**非必需**。

---

## 4. 文案提取方案（Copy Extraction）

### 4.1 抽取清单（inventory）
1. `semver_check.py` 中所有 `reasons.append("…")` 字面量（约 12 处：none / stable 毕业 / minor / major / 预发布递增 / 跳级拒绝 / 回滚等）。
2. 所有 `raise ValueError("…")` 用户可见错误（未知类型、非法预发布标识、非法版本号等）。
3. 级别展示名（`major/minor/patch/stable/none`）若对外暴露，统一走 locale。
4. SKILL.md 正文指令散文 → 改写为英文 **canonical**；中文等价版放入 `locales/zh.md`（或 `references/SKILL.zh.md`）供中文用户按需读取。

### 4.2 Key 命名约定
- 前缀分类：`REASON_`（理由串）、`ERR_`（错误提示）、`LABEL_`（级别名）、`MSG_`（流程说明）。
- 例：`REASON_NONE_NO_BUMP`、`ERR_UNKNOWN_CHANGE_TYPE`、`LABEL_MAJOR`、`MSG_STABLE_GRADUATION`。
- 键名稳定、与语言无关；值才是译文。

### 4.3 提取步骤
```bash
# 步骤 A：列出所有待抽取字面量
grep -noE "reasons\.append\(\"[^\"]+\"\)|raise ValueError\(\"[^\"]+\"\)" scripts/semver_check.py

# 步骤 B：在 semver_check.py 顶部加极简 i18n 加载器（零依赖）
#   import yaml, functools
#   _STR = load_locale(lang)            # 读 locales/<lang>.yaml
#   def _(k, **kw): return _STR[k].format(**kw)
#   将原字面量替换为 _( "REASON_XXX" )

# 步骤 C：填充 en.yaml（英译）与 zh.yaml（保留现有中文）
```

i18n 加载器保持零第三方依赖（沿用项目既有「stdlib-only」约束）。

---

## 5. 落地实施步骤（Phased Steps）

| 阶段 | 动作 | 产出 | 验证 |
|---|---|---|---|
| P1 | 新增 `locales/en.yaml` + `zh.yaml` 骨架，列出全部 key | 两份串表 | 键集合一致（脚本断言） |
| P2 | `semver_check.py` 加 `load_locale` / `_` / `--lang`；替换全部字面量 | 可切换语言的 CLI | `python -m unittest` 跨 `--lang en|zh` 全绿（reasons 内容随语言变、版本号不变） |
| P3 | `SKILL.md`：`description` 改英文；正文改英文默认；加 `## Language` 小节声明「输出跟随用户语言」 | 合规 frontmatter + 英文正文 | `measure_skill.py` 复测（description ≤1536 字符、核心规则 ≤3000 token） |
| P4 | `references/*.md` 改写为英文为主（可保留中文注） | 英文参考文档 | 门禁不报 NL violation |
| P5 | 版本号决策（见 §6）→ 改 `version` 字段 | 新版本号 | — |
| P6 | 跑发布门禁（干净副本剔除 `.gitignore`/`LICENSE`）SkillHub + ClawHub 双 PASS | 门禁报告 | 两平台均 PASS |
| P7 | 打 tag + 推远端 + 建 Release | 发布 | 远端可见 |

---

## 6. 版本号决策（依据本 skill 自身规则）

- 上一封版：**v0.1.1**。
- i18n = 向后兼容的新增能力（无破坏性变更）→ 按本 skill `decision-tables.md`：**minor**。
- 处于 0.x（y≥1）阶段，minor 级 → `0.(y+1).0`：
  - **已确认下一版：v0.2.0**（用户拍板，非 patch）
- 说明：本 skill 自己的 0.x 规则把「minor 递增」视为破坏边界（对消费者而言），但对**自身发版**采用「新功能=minor」的通用语义，故 0.1.1 → 0.2.0。

---

## 7. 验证与发布门禁

- 复用现有 `scripts/measure_skill.py` 复测：description 截断、正文篇幅、核心规则前置。
- 复用 `skill-publish-gate`：`gate.py check --dir <clean> --platform skillhub|clawhub`。
  - 关键变化：P3 后 `description` 为英文 → 消除来源 B 的 NL violation（原「全中文且无选项」风险消失，因为提供了英文默认 + 中文跟随的双语路径）。
- 干净副本须剔除 `.gitignore` / `LICENSE`（SkillHub 封禁文件），与 v0.1.x 发布流程一致。

---

## 8. 边界情况与风险（Edge Cases）

1. **JSON `reasons` 的语言张力**：来源 A③ 要求「JSON logs & reports English only」，但 `reasons` 又是用户面向对话输出（应跟随语言）。
   - 处置：将 `reasons` 视作**对话输出**，随 `--lang` 走；若未来新增纯「报告/日志」输出模式（`--report`），该模式强制英文。
2. **`auto` 误判**：环境变量缺失时回退 `en`（满足「English default」），不回退 `zh`。
3. **既有中文注释**：保留不动（来源 C 允许 comments 用其他语言）。
4. **门禁误报极限词**：沿用 v0.1.0 已验证的「优先序」措辞，避免新增「最高级」等词触发内容审核。
5. **token 预算**：英文正文可能比中文长；`measure_skill.py` 须确认核心规则仍 ≤3000 token、全文 ≤8000 token。

---

## 9. 已确认事项（实现时拍板）

1. 下一版本号：**v0.2.0**（minor）。✅ 已确认
2. `references/*.md` **也要英文镜像**：`decision-tables.md` / `standards-comparison.md` 改写为英文为主，原中文内容保留为 `*.zh.md`。✅ 已确认
3. CLI 默认语言：**`auto`**（探测 `LC_ALL`/`LC_MESSAGES`/`LANG`，回退 en）。✅ 已确认
4. `_meta.json`：**仅当某平台（SkillHub/ClawHub）明确要求时补**。经 `skill-publish-gate` 预检，两平台均不以 `_meta.json` 为必填（以 SKILL.md frontmatter 为准），故 v0.2.0 **不补**；若未来某平台 CLI/门禁报缺，再据其 schema 补英文 `description`。✅ 已确认（条件式）

> 以上四项已于实现前全部确认，P1–P7 已落地于 v0.2.0。

## 10. 稳定版发布（2026-10-11，安全审计后加固）

ClawHub 安全审计（v0.2.0，Oct 11 2026）整体结论为 **PASS**（aig / clawscan / static-analysis / virustotal 均 clean；仅 SkillSpector 给出机械式 CRITICAL，属误报）。基于其审计发现做针对性加固后，本技能由 0.x 毕业为稳定版：

- 版本：**v0.2.0 → v1.0.0**（稳定版，API 冻结确认）。
- 加固项：① `standards-comparison.md`/`.zh.md` 将「标准原文」与「本技能自定义默认（0.x npm/Cargo 语义、`security`→patch）」显式分离（修复 SDI-4）；② `SKILL.md` 触发器收窄并加负向排除（SQP-1）；③ 修复 `standards-comparison.md` 中英混杂行、为 README/zh 文档加「可选本地化副本」声明（SQP-3）；④ `SKILL.md` 新增能力/权限边界小节，明确仅读 `LC_ALL/LC_MESSAGES/LANG` 三个语言变量、无副作用（LP1）；⑤ 明确 `semver_check.py` 为判定内核、`measure_skill.py`/`test_semver_check.py` 为开发期工具（缓解 TP4）。

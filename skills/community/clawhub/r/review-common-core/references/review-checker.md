# 审稿完成自查清单 + JSON 校验方案

与分段标注框架（微观）和整体审稿框架（宏观）互补，本文档提供**审稿完成时的收尾检查**，防止漏项。

> 共享引擎：review-common-core

---

## 一、使用方式

每次审稿结束后，输出 JSON 格式的审稿校验记录，逐项确认以下清单。

**输出位置**：审稿报告的末尾（Phase 4 汇总之后）

**脚本校验流程**：
1. 审稿人输出 JSON 块
2. 脚本解析 JSON，逐项检查是否标记了 `"passed": true`
3. 任一 🔴 项未通过 → 脚本标记"审稿不完整"，返回未通过项列表
4. 所有 🔴 项通过 + 🟡 项无 FAIL → "审稿通过"

---

## 二、JSON Schema 定义

```json
{
  "schema": "openclaw.review.checklist.v1",
  "meta": {
    "draft_path": "string",
    "draft_version": "string",
    "review_date": "string (YYYY-MM-DD)",
    "reviewer": "string"
  },
  "checks": {
    "mandatory": {
      "topic_consistency": {
        "description": "主题一致性检查 — 一句话定题",
        "passed": "boolean",
        "details": {
          "one_sentence_theme": "string (审稿人用一句话回答'这篇文章在讲什么')",
          "has_dual_core": "boolean (答案是否包含'和/及/同时')",
          "core_theme": "string (确定的单一主题)",
          "drift_count": "number (偏离段落数)",
          "checklist_ref": "theme-consistency-checklist.md"
        }
      },
      "cross_act_repetition": {
        "description": "跨幕概念频率检查",
        "passed": "boolean",
        "details": [
          {"concept": "string", "appearances": ["幕1","幕2"], "count": 3, "judgment": "🔴 重复/🟡 关注/✅ 正常/✅ callback"}
        ]
      },
      "source_material_verification": {
        "description": "源头素材对照",
        "passed": "boolean",
        "details": [
          {"location": "string", "source_claim": "string", "match_result": "✅/⚠️/❓/🔴", "verified_by_author": "boolean"}
        ]
      },
      "privacy_check": {
        "description": "隐私保护检查",
        "passed": "boolean",
        "details": [
          {"location": "string", "risk_type": "收入/时薪/具体金额/个人身份", "risk_level": "🔴/🟡/🟢", "resolution": "已模糊化/已删/待确认"}
        ]
      },
      "hard_issues_tracked": {
        "description": "硬伤追踪——所有🔴项已标记位置并确认",
        "passed": "boolean",
        "details": [
          {"severity": "🔴", "location": "string", "issue": "string", "status": "已修/待修/已确认非问题"}
        ]
      },
      "ending_matches_core_conflict": {
        "description": "结尾匹配——回应了前文最重的矛盾",
        "passed": "boolean",
        "details": {"core_conflict": "string", "ending_response": "string", "assessment": "✅/⚠️/❌"}
      }
    },
    "suggested": {
      "dialogue_rhythm": {
        "description": "对话节拍——B不替A复读；不抢悬念追问；A独白≤60秒",
        "passed": "boolean",
        "details": [
          {"issue": "B复读/追问太紧/独白过长", "location": "string", "fixed": "boolean"}
        ]
      },
      "cross_episode_echo": {
        "description": "回音检测——同一金句/比喻在同系列跨稿中无意识复用",
        "passed": "boolean",
        "details": [
          {"phrase": "string", "script_1": {"episode": "string", "location": "string"}, "script_2": {"episode": "string", "location": "string"}, "judgment": "无意复用/有意callback/新出现"}
        ]
      },
      "anti_ai_check": {
        "description": "反AI味——无PPT结构、无零密度句子、无播报体结尾",
        "passed": "boolean",
        "details": [
          {"issue_type": "PPT结构/零密度/播报体/术语未解释/排比过多/反转过多", "location": "string", "fixed": "boolean"}
        ]
      },
      "term_friendly": {
        "description": "术语友好——首次出现专业术语有类比或解释",
        "passed": "boolean",
        "details": [
          {"term": "string", "explanation_provided": "boolean", "explanation": "string"}
        ]
      },
      "ending_brevity": {
        "description": "结尾收束——不超过3句，不出现播报体",
        "passed": "boolean",
        "details": {
          "sentence_count": "number", 
          "has_broadcast_style": "boolean",
          "last_three_sentences": ["string", "string", "string"]
        }
      }
    },
    "optional": {
      "multi_model_cross": {
        "description": "多模型交叉审稿",
        "passed": "boolean",
        "details": [
          {"model": "ChatGPT/DeepSeek/Gemini", "disagreement": "string", "resolution": "string"}
        ]
      },
      "cross_episode_consistency": {
        "description": "跨集一致性——角色名/节目名/数据前后统一",
        "passed": "boolean",
        "details": [
          {"item": "节目名/角色名/数据", "value_in_this_draft": "string", "value_in_previous": "string", "consistent": "boolean"}
        ]
      }
    }
  },
  "summary": {
    "total_issues": "number",
    "mandatory_passed": "boolean",
    "overall_status": "✅ 通过 / ⚠️ 需小改 / ❌ 不通过",
    "blockers": ["string (未通过的🔴项列表)"]
  }
}
```

---

## 三、Human-readable Checklist

> 使用方式：审稿人审完全文后，逐项确认。黑色 ✅ 是通过的直接记录在 JSON 中。

### 🔴 必须通过（mandatory）

| # | 检查项 | 通过条件 | JSON 字段 |
|---|--------|---------|----------|
| 1 | **主题一致性** | 已执行"一句话定题"测试：用一句话回答"这篇文章在讲什么"。答案中不出现"和/以及/同时"等连接词。如有双核心 → 已给出拆文或删段建议 | `checks.mandatory.topic_consistency` |
| 2 | **跨幕概念频率** | 同一概念在 ≥3 个不相邻场景中重复出现 → 标记 🔴 并给出压缩建议；首尾呼应有标注 ✅ callback；无重复 → ✅ | `checks.mandatory.cross_act_repetition` |
| 3 | **源头素材对照** | 所有事实性陈述已与素材对照：无编造细节、无脑补因果、无数字精确化（"大约"→精确值）。标记 ✅/⚠️/❓/🔴 且作者已逐条确认 | `checks.mandatory.source_material_verification` |
| 4 | **隐私保护** | 时薪/收入/具体金额未暴露可反推信息。涉及金额的已标注风险类型和级别。个人隐私优先级高于观点锋利度 | `checks.mandatory.privacy_check` |
| 5 | **硬伤追踪** | 所有 🔴 项已标记位置 + 原文摘录 + 风险类型 + 修改建议。作者已逐条回应（已修/待修/已确认非问题） | `checks.mandatory.hard_issues_tracked` |
| 6 | **结尾匹配** | 结尾回应了前文最重的矛盾。不用温馨小事回避核心问题。如"铺太多线怎么砍"却用宝宝打印纸收尾 ← 典型违规 | `checks.mandatory.ending_matches_core_conflict` |

### 🟡 建议通过（suggested）

| # | 检查项 | 通过条件 | JSON 字段 |
|---|--------|---------|----------|
| 6 | **对话节拍** | B不替A复读金句；不抢在悬念后立刻追问；A连续独白 ≤60 秒 | `checks.suggested.dialogue_rhythm` |
| 7 | **回音检测** | 同系列不同稿中，同一金句/比喻无意识复用。无意复用 → 删或换表达；有意 callback → 显式标注 | `checks.suggested.cross_episode_echo` |
| 8 | **反AI味** | 无"第一/第二/第三"PPT结构（除非中间有打断）；无零密度句子；无播报体结尾；无过度排比（>3次） | `checks.suggested.anti_ai_check` |
| 9 | **术语友好** | 首次出现的专业术语有类比或解释（token/Harness/OKR/Desirable Difficulties 等） | `checks.suggested.term_friendly` |
| 10 | **结尾收束** | 结尾不超过 3 句，不出现"总结一句/好今天就到这里/下期再见"等播音腔 | `checks.suggested.ending_brevity` |

### 🔧 可选（optional）

| # | 检查项 | 通过条件 | JSON 字段 |
|---|--------|---------|----------|
| 11 | **多模型交叉** | ChatGPT（或第二个模型）已审稿，标注了分歧点（两个模型都指出同一问题 → 🔴硬伤） | `checks.optional.multi_model_cross` |
| 12 | **跨集一致性** | 系列内容的角色名(Fiona/老婆)、节目名("用AI搞学术"/"OpenCloud播客")、关键数据前后统一 | `checks.optional.cross_episode_consistency` |

---

## 四、输出示例

以 EP11 v4 审稿为例：

```json
{
  "schema": "openclaw.review.checklist.v1",
  "meta": {
    "draft_path": "/path/to/episode-11/draft.md",
    "draft_version": "v4",
    "review_date": "2026-06-16",
    "reviewer": "笔探 ✍️"
  },
  "checks": {
    "mandatory": {
      "topic_consistency": {
        "passed": true,
        "details": {
          "one_sentence_theme": "花钱买工具值不值得的纠结",
          "has_dual_core": false,
          "core_theme": "花钱买工具的心理纠结",
          "drift_count": 0,
          "checklist_ref": "theme-consistency-checklist.md"
        }
      },
      "cross_act_repetition": {
        "passed": true,
        "details": [
          {"concept": "纠结/纠结了一周", "appearances": ["幕1","幕3","幕4"], "count": 4, "judgment": "✅ 核心主题"},
          {"concept": "几百块/钱", "appearances": ["幕1","幕2","幕3","幕4"], "count": 8, "judgment": "🟡 分散在4幕，可不改"},
          {"concept": "试错", "appearances": ["幕3","幕4"], "count": 5, "judgment": "✅ 不同场景推进"},
          {"concept": "固定工作流", "appearances": ["幕4"], "count": 2, "judgment": "✅ 集中在结尾"}
        ]
      },
      "source_material_verification": {
        "passed": true,
        "details": [
          {"location": "幕1", "source_claim": "纠结一周几百块的coding plan", "match_result": "✅", "verified_by_author": true},
          {"location": "幕1", "source_claim": "花掉的注意力值不值这几百块", "match_result": "🟡", "verified_by_author": true, "note": "故意从'时薪'改为'注意力'保护隐私"},
          {"location": "幕2", "source_claim": "30亿token×2=60亿", "match_result": "✅", "verified_by_author": true},
          {"location": "幕2", "source_claim": "智谱200块包年/Lite", "match_result": "✅", "verified_by_author": true},
          {"location": "幕2", "source_claim": "Google AI Pro没续", "match_result": "✅", "verified_by_author": true}
        ]
      },
      "privacy_check": {
        "passed": true,
        "details": [
          {"location": "幕1", "risk_type": "时薪/收入", "risk_level": "🟡", "resolution": "已改为'注意力'，未暴露收入"},
          {"location": "幕2", "risk_type": "具体金额", "risk_level": "🟢", "resolution": "金额小(200/20美元)，不可反推收入"},
          {"location": "幕1", "risk_type": "收支", "risk_level": "🟢", "resolution": "已改为'情况'，模糊化"}
        ]
      },
      "hard_issues_tracked": {
        "passed": true,
        "details": [
          {"severity": "🔴", "location": "幕1龙虾对话", "issue": "原审稿误标为硬伤", "status": "已确认非问题（隐私保护）"},
          {"severity": "🟡", "location": "幕2工具介绍", "issue": "信息过载", "status": "已修（v4压缩）"},
          {"severity": "🟡", "location": "幕4三问结构", "issue": "PPT化", "status": "已修（v4松动）"},
          {"severity": "🟡", "location": "幕4B结尾", "issue": "播报体", "status": "已修（v4自然化）"}
        ]
      },
      "ending_matches_core_conflict": {
        "passed": true,
        "details": {
          "core_conflict": "花钱买工具值不值得的纠结",
          "ending_response": "B问'那这期聊完你又在纠结新工具了吗？'，A答'会，纠结还在，但至少知道自己在纠结什么了'",
          "assessment": "✅ 以承认纠结还在收尾，未回避核心矛盾"
        }
      }
    },
    "suggested": {
      "dialogue_rhythm": {"passed": true, "details": []},
      "cross_episode_echo": {"passed": true, "details": []},
      "anti_ai_check": {"passed": true, "details": []},
      "term_friendly": {"passed": true, "details": [{"term": "token", "explanation_provided": true, "explanation": "AI的'思考力'"}]},
      "ending_brevity": {
        "passed": true,
        "details": {
          "sentence_count": 3,
          "has_broadcast_style": false,
          "last_three_sentences": ["那这期聊完，你又在纠结新工具了吗？", "会。纠结的感觉还在。但至少我现在知道自己在纠结什么了。", "那就够了。下期再见！"]
        }
      }
    },
    "optional": {
      "multi_model_cross": {"passed": false, "details": [{"model": "ChatGPT", "disagreement": "审稿中，待输出", "resolution": "-"}]},
      "cross_episode_consistency": {"passed": false, "details": [{"item": "节目名", "value_in_this_draft": "未定名", "value_in_previous": "用AI搞学术/OpenCloud播客", "consistent": false}]}
    }
  },
  "summary": {
    "total_issues": 5,
    "mandatory_passed": true,
    "overall_status": "✅ 通过",
    "blockers": []
  }
}
```

---

## 五、脚本校验逻辑（参考实现）

```python
# 核心校验逻辑
def validate_review(review_json):
    errors = []
    warnings = []
    
    # Step 1: 检查所有 🔴 mandatory 项
    for key, check in review_json["checks"]["mandatory"].items():
        if not check.get("passed"):
            errors.append(f"MANDATORY_FAIL: {check['description']}")
            for detail in check.get("details", []):
                if detail.get("status") == "待修":
                    errors.append(f"  → 未修复: {detail.get('location')} - {detail.get('issue')}")
    
    # Step 2: 检查 🟡 suggested 项
    for key, check in review_json["checks"]["suggested"].items():
        if not check.get("passed"):
            for detail in check.get("details", []):
                if not detail.get("fixed"):
                    warnings.append(f"SUGGESTED_UNFIXED: {detail.get('issue')} at {detail.get('location')}")
    
    # Step 3: 生成校验报告
    return {
        "status": "FAIL" if errors else ("PASS_WARN" if warnings else "PASS"),
        "errors": errors,
        "warnings": warnings
    }
```

---

## 六、与现有框架的关系

| 框架 | 作用 | 执行时间 |
|------|------|---------|
| 分段标注框架 (`segment-annotation-framework.md`) | 逐句微观反应 | 审稿中 |
| 整体审稿框架 (`holistic-review-framework.md`) | 整篇宏观评估 | 审稿中 |
| **审稿检查清单（本文件）** | **审稿收尾校验** | **审稿后 ✅** |
| 事实核查框架 (`fact-check-framework.md`) | 6类风险分类 | 审稿前 |

四个框架互补使用：先跑事实核查(Phase 0) → 逐句模拟(微观, Phase 2) → 整体评估(宏观, Phase 1) → checklist 收尾校验(Phase 4)。

### 审稿管线内的位置

```
[稿件到达]
  ↓
Phase 0: 事实核查            ← references/fact-check-framework.md
  ↓
Phase 1: 五维度审稿            ← references/holistic-review-framework.md
  ↓
Phase 2: 逐句读者模拟          ← references/segment-annotation-framework.md
  ↓
Phase 3: ChatGPT 交叉审稿
  ↓
Phase 4: 汇总输出 + 修复跟踪
  ↓
🛑 Checkpoint: 审稿检查清单    ← 本文件 (review-checker.md)
  ↓
[通过 → 输出最终报告]
[不通过 → 返回修复]
```

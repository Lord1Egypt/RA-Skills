# Content Hint Fallback 设计（v7.0 跑题事故修复）

> **来源文件**：原 SKILL.md 附录 B（外移于 2026-07-02 拆分重构）
> **生效版本**：自 v2.1.x 起，content_hint fallback 已在 `scripts/context_builder.py` 落地

本文档是 SKILL.md 附录 B 的外移版本，承载具体的修复方案、代码实现、测试用例和验收标准。
SKILL.md 内的对应位置仅保留指针，避免主文档重复维护。

---

## 附录 B：已批准改进方案 — 大纲约束注入（已实施 2026-06-30）

> **来源**：v7.0 事故复盘 → 运营者 22:19 反馈，Q3=A / 2026-06-29  
> **实施状态**：✅ 已实施并验收（2026-06-30）
> **注意**：本附录不绑具体版本号。以 SKILL.md frontmatter 的 `metadata.clawdbot.version` 为当前 skill 真实版本。

### B.1 背景

v7.0 Phase 2 跑题事故显示：当 `node.content_hint` 为空时，LLM 写作完全依赖章节标题推断上下文，导致 LLM 写出通用 MBA 论文（"数字经济转型"），跑偏具体研究对象（A 公司 / vivo / 互联网分发）。

### B.2 目标

当 `node.content_hint` 为空时，**不**直接让 LLM 写，而是构造一个"大纲骨架 + 反面警示"的 prompt 约束，确保不跑题。

### B.3 实施方案

修改 `scripts/context_builder.py` 的 `build_prompt_package()` 函数：

```python
# 现有逻辑
content_hint = current.get("content_hint", "").strip()

# v2.x.x 新增（v7.0 跑题事故修复）：当 content_hint 为空时，注入大纲骨架 + 反面警示
if not content_hint and state:
    outline_skeleton = _build_outline_skeleton(state, node_id)
    paper_subject = _extract_paper_subject(paper_name, state)
    warning_block = _build_no_runoff_warning(paper_subject)
    content_hint = f"{warning_block}\n\n{outline_skeleton}"

package = { ..., "content_hint": content_hint, ... }
```

#### B.3.1 新增辅助函数

```python
def _extract_paper_subject(paper_name: str, outline_state: Optional[Dict] = None) -> str:
    """提取论文主题描述（用于 warning 主题锁定）

    策略：
      1. 优先从 outline_state["outline_tree"]["metadata"]["paper_title"] 读
      2. 否则从 paper_name 去掉版本号后缀
      3. 兜底返回 paper_name
    """
    if outline_state:
        try:
            title = outline_state.get("outline", {}).get("outline_tree", {}).get("metadata", {}).get("paper_title")
            if title and title.strip():
                return title.strip()
        except Exception:
            pass
    import re as _re
    subject = _re.sub(r'(_v\d+(?:\.\d+)*|_final|_\d{8}_\d{6})+$', '', paper_name)
    return subject if subject else paper_name


def _build_outline_skeleton(outline_state: Dict, target_node_id: str) -> str:
    """构造论文大纲骨架"""
    try:
        nodes = outline_state.get("outline", {}).get("outline_tree", {}).get("nodes", [])
    except Exception:
        return ""
    lines = ["【论文完整大纲（用于提供上下文）】", ""]
    for n in nodes:
        if n.get("is_virtual"):
            continue
        level = n.get("level", 2)
        prefix = "#" * level
        lines.append(f"{prefix} {n['id']} {n.get('title', '')}")
    lines.append("")
    lines.append("【你正在写的节点】")
    target = next((n for n in nodes if n.get("id") == target_node_id), None)
    if target:
        lines.append(f"→ {target.get('title', target_node_id)}（{target_node_id}）")
    return "\n".join(lines)


def _build_no_runoff_warning(paper_subject: str = "本研究主题") -> str:
    """反面警示：明确禁止跑题

    paper_subject: 论文研究对象描述（建议从 outline metadata.paper_title 取）
    """
    return (
        f"⚠️ 主题锁定：本论文研究对象是「{paper_subject}」。\n"
        "- ✅ 围绕论文具体研究对象的真实业务场景、技术路线、客户/竞争格局等具体实体\n"
        "- ✅ 引用与论文主题相关的权威数据源（行业报告 / 学术文献 / 公司财报）\n"
        "- ❌ 严禁写成通用 MBA 模板论文（如「数字经济 / 企业数字化转型 / 战略管理一般性理论」）\n"
        "- ❌ 严禁「党的二十大报告提出…」这类脱离论文研究主题的泛泛话语\n"
        "- ❌ 严禁用「企业四要素模型 / 波特钻石模型」等通用教科书内容代替研究主题的具体业务场景"
    )
```

#### B.3.2 关键设计要点

1. **不破坏现有 `content_hint` 非空的路径**：只有当 hint 为空时才插入骨架
2. **token 成本低**：大纲骨架 < 1 KB，比塞全文 content（100 KB+）省得多
3. **覆盖完整**：即使 50 个节点 hint 全空，prompt 里仍有大纲骨架明确"我在写论文 X 章节 Y"
4. **反面警示**：LLM 习惯正面 prompt，加"❌ 严禁"反向约束效果更好

### B.4 测试用例

```python
def test_content_hint_empty_should_use_skeleton():
    """given: node.content_hint = '' when: build_prompt_package then: package['content_hint'] 含大纲骨架 + 反面警示"""
    pass

def test_content_hint_present_should_unchanged():
    """given: node.content_hint = 'A公司2024年...' when: build_prompt_package then: package['content_hint'] == 原 hint"""
    pass
```

### B.5 验收标准

- [x] `_build_outline_skeleton` 输出 < 1500 字（实测 1281 字符）
- [x] `_build_no_runoff_warning` 输出含至少 3 个 ❌ 禁止项（实测 3 个）
- [x] 现有非空 hint 路径 PASS（7.2 节点回归通过）
- [x] Phase 2 跑 1 个节点，验证 prompt 含研究主题关键词（ch1 节点验证通过）
- [x] 完整 content_hint < 2500 字（实测 1566 字符）
- [x] 警告块参数化（_build_no_runoff_warning 接受 paper_subject 参数，不再硬编码 A 公司）

### B.6 已完成行动

- [x] 代码实施（context_builder.py + 3 个新函数 + 1 段 fallback 逻辑）
- [x] 单元级验收（5+1 项 全部通过）
- [x] 文档同步（SKILL.md 附录 B 代码块与实际代码一致）
- [ ] CHANGELOG.md 同步（待 v2.0.7 升级时补充）
- [ ] README.md 改进章节（待 v2.0.7 升级时补充）
- [ ] ClawHub publish（待 v2.0.7 升级时发布）

数据来源声明：本方案生成于 2026-06-29 运营者对话，2026-06-30 完成 P0 修复。

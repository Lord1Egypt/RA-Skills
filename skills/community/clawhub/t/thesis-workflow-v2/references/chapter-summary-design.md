# 章节摘要节点设计说明（增强项1 — 跨父节点 Bridge）

> 本文档解释 MBA Thesis Workflow v2.0.0 引入的 **章节摘要节点机制**——为什么要在 L1 章节末尾插入虚拟节点，以及如何利用它解决跨章节 bridge 断裂问题。

---

## 一、问题背景

### 1.1 Bridge 机制回顾

MBA 论文工作流的章节连贯性依赖 `context_builder.generate_bridge()`：

- **P1（前序节点）**：当前节点的前一个兄弟节点（L2 同级）
- **P2（父节点）**：当前节点的父节点（L1）
- 任意一个能拿到 `key_conclusion` → 生成承接段

### 1.2 桥断裂场景

考虑以下目录结构：

```
1. 绪论 (ch1)
   1.1 研究背景       (L2)
   1.2 研究内容       (L2)
2. 理论基础 (ch2)
   2.1 竞争战略理论   (L2)  ← 这节点写 bridge 时
   2.2 文献综述       (L2)
```

写 `2.1` 时：
- **prev** = `1.2`（前序节点的「1.2」） ❌ 跨章节，不是 prev
- **parent** = `ch2`（父节点）❌ L1 章节通常无 key_conclusion
- **结果**：bridge = null，NodeWriter 自由发挥开头，连贯性差

这就是 v1.7.3 重审 Agent 反复指出的「bridge 断裂」问题。

---

## 二、方案 C：虚拟章节摘要节点

### 2.1 核心思路

在每个 L1 章节末尾**自动插入**虚拟节点 `__ch{N}_summary__`：
- 不实际写作（不调用 NodeWriter）
- 自动汇总本章所有 L2/L3 子节点的 `key_conclusion`
- LLM 合成 200-300 字章节摘要
- 下一章节首节点的 bridge 可引用

### 2.2 节点结构

```json
{
  "id": "__ch1_summary__",
  "level": 1,
  "title": "绪论 — 本章小结",
  "is_virtual": true,
  "type": "chapter_summary",
  "synthesizes": ["1.1", "1.2"],
  "chapter_id": "ch1",
  "chapter_title": "绪论",
  "key_conclusion": "本章从 AI 时代背景出发，提出差异化战略研究问题...",
  "writing_status": "completed",
  "word_count": 50
}
```

### 2.3 数据流

```
节点 N 写作完成
  ↓
is_last_child_of_chapter(N) 检测
  ↓ 是
synthesize_chapter_summary(chapter_id)
  ↓
收集 synthesizes 子节点结论 → LLM 合成 200-300 字摘要
  ↓
写入 __ch{N}_summary__ 节点的 key_conclusion
  ↓
下一章节首节点 bridge 自动引用（P3 fallback）
```

---

## 三、Bridge 三级降级链

`generate_bridge()` 新增 P3 优先级：

| 优先级 | 来源 | 函数 | 场景 |
|--------|------|------|------|
| P1 | 前序节点 key_conclusion | `_build_bridge_from_prev` | 同章节内连续节点 |
| P2 | 父节点 key_conclusion | `_build_bridge_from_parent` | 章节内首节点 |
| **P3（新）** | **上一章节虚拟摘要** | **`_build_bridge_from_chapter_summary`** | **跨章节首节点** |

**降级原则**：
- 任何上游 key_conclusion 存在 → 立即返回（不走到下一级）
- 全部为 None → 返回 `None`，NodeWriter 自行处理开头

---

## 四、LLM 失败安全降级（拍板决策 #3）

按2026-06-23拍板决策，**LLM 合成失败时改为询问用户**，而不是简单拼接子节点结论。

```python
try:
    response = llm_func(prompt)
    summary = response.strip()
except Exception as e:
    return {
        "ok": False,
        "action": "ask_user",  # 关键变化
        "error": f"LLM 调用失败: {str(e)}",
        "chapter_id": chapter_id,
        "chapter_title": chapter_title,
        "child_conclusions": [...]  # 附带子节点结论供 Orchestrator 展示
    }
```

Orchestrator 收到 `action="ask_user"` 时：
1. 展示子节点结论给用户
2. 询问用户手写摘要 / 跳过 / 重试
3. 用户输入 → 第二次调用 `synthesize_chapter_summary(user_input=...)` → 写入

---

## 五、拍板决策汇总（2026-06-23）

| # | 议题 | 决策 |
|---|------|------|
| 1 | 方案选型 | 方案 C（虚拟摘要节点） |
| 2 | 摘要长度 | 200-300 字 |
| 3 | LLM 失败处理 | **询问用户**（不简单拼接） |
| 4 | 章节摘要评审 | 不参与 Phase 3 评审，仅作内部辅助 |
| 5 | 设计文档 | references/chapter-summary-design.md |

---

## 六、代码落地

| 文件 | 改动 |
|------|------|
| `outline_parser.py` | `insert_chapter_summary_nodes()` + 2 个辅助函数 |
| `orchestrator_v2.py` | `is_last_child_of_chapter()` + `synthesize_chapter_summary()` + `write_single_node()` Step 4.5 |
| `context_builder.py` | `_build_bridge_from_chapter_summary()` + `generate_bridge()` P3 fallback |
| `state_manager_v2.py` | `_get_prev_chapter_summary()` + `outline_get_context()` 自动附加 |

---

## 七、测试覆盖（20 个测试用例）

- `test_chapter_summary.py` (6)：节点插入、L3 纳入、幂等、边界、辅助函数
- `test_synthesize_summary.py` (6)：检测、LLM 路径、用户输入、ask_user、空子节点、超长截断
- `test_bridge_p3_fallback.py` (6)：P1/P2 优先级、P3 跨章节、不可用降级、首章节、context 自动附加
- `test_integration_chapter_summary.py` (2)：happy path + LLM 失败 fallback 端到端

总测试数：25 (v1.7.3) + 20 (v1.7.4) = **45 个**（v2.0.0 汇总为 **72 个**）

---

## 八、边界条件

| 场景 | 行为 |
|------|------|
| 首章节首节点（1.1） | prev_chapter_summary = None → bridge = None（NodeWriter 自处理） |
| 用户跳过某些节点 | 摘要只基于 synthesizes 中**已完成**子节点 |
| LLM 合成失败 | action = "ask_user"，不写入 state |
| 超长摘要（>300 字） | 自动截断到 300 字 |
| 重复调用 insert | 幂等，已存在虚拟节点时跳过 |
| 章节无任何子节点 key_conclusion | action = "ask_user"，附空列表 |

---

## 九、后续优化方向（非本次范围）

- 章节摘要的版本控制（多版本对比）
- 摘要参与 Phase 3 评审（如果以后放开拍板 #4）
- 摘要可由用户直接编辑（不依赖 LLM）

# Phase Manager 模块设计方案

> 创建时间：2026-06-30
> 状态：已设计，待实现
> 目录：`scripts/phase_manager/`

---

## 一、模块定位与目标

### 1.1 解决的问题

当前 HIL 节点将 Phase 产出直接渲染到 chat 窗口，存在三大问题：
1. **信息截断** — 大论文数十KB内容无法完整返回
2. **上下文浪费** — token 被正文消耗，核心元数据被淹没
3. **用户无法细改** — 只能整体接受/拒绝，无法局部编辑

### 1.2 模块定位

每个 Phase 的**数据中枢**：
- 管理输入/输出文件的生命周期
- 提供门禁校验（准入/准出）
- 生成 HIL 消息（只含路径+摘要，不塞正文）
- 保证跨 Session 数据有效性

**独立性强**：只依赖 Python stdlib，不依赖业务模块，可独立测试和移植。

### 1.3 设计原则

| 原则 | 说明 |
|------|------|
| 文件优先 | Phase 产出存入文件，不塞 chat |
| 用户可编辑 | 用户可直接改文件，下一 Phase 读取新内容 |
| 有效性保障 | 读写前做 freshness check + hash 校验 |
| 幂等安全 | 已完成 Phase 的内容非 force 不可覆盖 |
| 清理可控 | 中间态文件及时清理，重要产出持久化 |

---

## 二、目录结构

```
scripts/phase_manager/
├── __init__.py              ← 导出 PhaseManager 主类
├── schemas.py               ← 数据契约（PhaseSummary / PhaseFile / PhaseTransition）
├── file_manager.py          ← 文件生命周期管理
├── gate_keeper.py           ← 门禁校验
├── summary_generator.py     ← 摘要生成
├── hil_renderer.py          ← HIL 消息渲染
└── DESIGN.md                ← 本文档
```

---

## 三、数据契约（schemas.py）

### 3.1 PhaseSummary

```python
@dataclass
class PhaseSummary:
    phase: int                                  # Phase 编号（1-5）
    status: str                                 # pending | running | completed | failed | modified
    timestamp: str                              # ISO timestamp（最后修改时间）
    file_path: str                              # 产出文件路径
    content_hash: str                           # 内容哈希（MD5，用于检测用户是否改过）
    word_count: int                             # 中文字数
    chapter_count: int                          # 章节数
    key_metrics: Dict[str, Any]                 # 关键指标（见下方）
    user_modifications: bool                    # 用户是否手动修改过文件
    message: str                                # 一句话摘要

    # key_metrics 字段说明
    # Phase 2: {"nodes_total": N, "nodes_completed": N, "nodes_failed": N}
    # Phase 3: {"p0_issues": 0, "p1_issues": N, "p2_issues": N, "guardrails_passed": True}
    # Phase 3.5: 同 Phase 3
    # Phase 4: {"integrated_word_count": N, "changes_applied": N}
    # Phase 5: {"word_count": N, "guardrails_passed": True}
```

### 3.2 PhaseFile

```python
@dataclass
class PhaseFile:
    phase: int                                  # Phase 编号
    content_type: str                           # integrated | review | summary
    file_path: str                              # 文件绝对路径
    hash: str                                   # 内容哈希
    size_bytes: int                             # 文件大小
    created_at: str                             # ISO timestamp
    updated_at: str                             # ISO timestamp
    backup_path: Optional[str]                  # 备份文件路径（上一版本）
```

**content_type 说明**：
- `integrated` — 整合版正文（.md）
- `review` — 审核报告（.json）
- `summary` — 结构化摘要（.json）

### 3.3 PhaseTransition

```python
@dataclass
class PhaseTransition:
    from_phase: int                             # 来源 Phase
    to_phase: int                               # 目标 Phase
    triggered_by: str                           # auto | user_confirm | user_modify
    triggered_at: str                           # ISO timestamp
    triggered_session: str                      # 触发时的 session ID
    content_hash: str                           # 触发时的文件哈希
    gate_passed: bool                           # 门禁是否通过
```

### 3.4 GateResult

```python
@dataclass
class GateResult:
    passed: bool                                # 是否通过
    phase: int                                  # 检查的 Phase
    checks: Dict[str, Tuple[bool, str]]         # {check_name: (passed, detail)}
    blocking_issues: List[str]                  # 阻塞性问题列表

    def summary(self) -> str:
        """生成人类可读的 gate 结果摘要"""
```

---

## 四、文件命名规范

| 文件名模式 | 示例 | 用途 |
|-----------|------|------|
| `_phase{N}_{integrated/review/summary}.md` | `_phase3_integrated.md` | Phase N 整合版正文 |
| `_phase{N}_{integrated/review/summary}.json` | `_phase3_review.json` | Phase N 审核报告/摘要 |
| `_phase{N}_{integrated/review/summary}.md.bak` | `_phase3_integrated.md.bak` | 上一版本备份 |
| `_phase{N}.lock` | `_phase3.lock` | 写入锁（防并发） |
| `_phase{N}_summary.json` | `_phase3_summary.json` | PhaseSummary 结构化摘要 |
| `_transition.json` | `_transition.json` | Phase 流转记录 |

---

## 五、核心类实现规格

### 5.1 PhaseFileManager

**职责**：文件生命周期管理（CRUD + 版本控制 + 清理）

```python
class PhaseFileManager:
    FRESHNESS_THRESHOLD_HOURS = 48              # 文件新鲜度阈值
    WORKSPACE_BASE = "~/.openclaw/workspace"   # 工作区根目录

    def __init__(self, paper_name: str, workspace: str = None):
        self.paper_name = paper_name
        self.workspace = workspace or os.path.join(
            os.path.expanduser(WORKSPACE_BASE), paper_name
        )
        os.makedirs(self.workspace, exist_ok=True)

    # ---- 路径计算 ----
    def get_file_path(self, phase: int, content_type: str, ext: str = None) -> str:
        """
        返回指定 Phase + 类型的目标文件路径。
        ext 默认为 md（integrated）或 json（review/summary）。
        """

    # ---- 生命周期：保存 ----
    def save_content(self, phase: int, content_type: str, content: str,
                     create_backup: bool = True) -> Dict[str, Any]:
        """
        保存内容。

        流程：
        1. 计算 content_hash
        2. 检查是否有内容变化（hash 对比）
        3. 有变化且 create_backup=True → 自动备份旧版本到 .bak
        4. 写入新内容（带 .lock 保护）
        5. 更新 state 中的 hash 记录
        6. 校验文件完整性

        返回：{
            ok: bool,
            hash: str,
            backup_path: Optional[str],
            size_bytes: int,
            changed: bool,
            error: Optional[str]
        }
        """

    # ---- 生命周期：读取 ----
    def load_content(self, phase: int, content_type: str) -> Optional[str]:
        """
        读取指定文件内容。
        文件不存在或校验失败 → 返回 None
        """

    # ---- 新鲜度校验 ----
    def is_fresh(self, phase: int, content_type: str) -> bool:
        """
        检查文件是否新鲜：
        1. 文件存在
        2. 修改时间在 FRESHNESS_THRESHOLD_HOURS 内
        3. content_hash 与 state 中记录一致
        """

    def validate_before_read(self, phase: int, content_type: str) -> Dict:
        """
        读取前校验：
        - 文件存在
        - 未过期
        - hash 一致

        返回：{ok: bool, error: Optional[str], fresh: bool, hash_changed: bool}
        """

    # ---- 用户修改检测 ----
    def detect_user_modification(self, phase: int, content_type: str) -> bool:
        """
        通过 content_hash 对比，检测用户是否手动修改了文件。
        流程：
        1. 读取当前文件的真实 hash
        2. 对比 state 中记录的 hash
        3. 不一致 → 用户改过
        """

    # ---- 版本控制 ----
    def backup_exists(self, phase: int, content_type: str) -> bool:
        """检查是否有 .bak 备份版本"""

    def restore_backup(self, phase: int, content_type: str) -> Dict:
        """
        恢复上一备份版本。
        返回：{ok: bool, restored_path: str}
        """

    # ---- 清理 ----
    def cleanup_intermediate(self, phase: int,
                             keep_types: List[str] = None) -> Dict:
        """
        清理指定 Phase 的中间文件。

        keep_types 默认：["integrated.md", "review.json", "summary.json"]
        删除：.tmp / .bak / .lock 等临时文件

        返回：{ok: bool, deleted: [file_paths]}
        """

    def cleanup_all_intermediates(self) -> Dict:
        """
        清理所有 Phase 的中间文件（保留最终产出）。
        用于论文完成后收尾。
        """

    # ---- 写入锁（防并发）----
    def save_with_lock(self, phase: int, content_type: str,
                       content: str) -> Dict:
        """
        写入时加锁，防止并发覆盖。
        1. 检查 .lock 文件
        2. 有锁 → 报错 "文件正在被编辑，请稍后"
        3. 无锁 → 创建锁 → 写入 → 删除锁
        4. finally 确保锁释放
        """
```

### 5.2 PhaseGateKeeper

**职责**：Phase 流转门禁校验（准入/准出）

```python
class PhaseGateKeeper:
    # 通用门禁规则
    GATE_RULES = {
        "min_word_count": 1000,      # 最小字数
        "max_word_count": 200000,    # 最大字数（异常检测）
        "chapter_count": 7,          # 章节数要求
        "freshness_hours": 48,       # 文件新鲜度
    }

    def __init__(self, paper_name: str):
        self.paper_name = paper_name
        self.fm = PhaseFileManager(paper_name)

    # ---- 准入检查（进入 Phase N 前）----
    def pre_enter_check(self, target_phase: int) -> GateResult:
        """
        检查是否可以进入 target_phase。

        规则：
        - Phase 2 前：Phase 1.2 大纲已确认 + Phase 1.3 已提交
        - Phase 3 前：Phase 2 全部节点 completed，无 failed
        - Phase 3.5 前：Phase 3 review 已完成
        - Phase 4 前：Phase 3.5 收敛（连续 2 轮无新 P0）
        - Phase 5 前：Phase 4 guardrails 10/10 通过

        返回：GateResult
        """

    # ---- 准出检查（Phase N 完成前）----
    def pre_exit_check(self, current_phase: int) -> GateResult:
        """
        检查当前 Phase 是否满足完成条件。

        规则：
        - Phase 2：节点完成率 100%，无 failed 节点
        - Phase 3：审核 loop 收敛（连续 2 轮无新 P0）
        - Phase 3.5：同 Phase 3
        - Phase 4：整合版 guardrails 10 项校验通过
        - Phase 5：Word 输出格式校验通过

        返回：GateResult
        """

    # ---- 通用门禁项 ----
    def check_word_count(self, phase: int, content_type: str = "integrated") -> Tuple[bool, str]:
        """字数是否在合理范围"""

    def check_chapter_completeness(self, phase: int, content_type: str = "integrated") -> Tuple[bool, str]:
        """章节是否完整（7 章）"""

    def check_freshness(self, phase: int, content_type: str = "integrated") -> Tuple[bool, str]:
        """文件是否新鲜（48 小时内有更新）"""

    def check_hash_unchanged(self, phase: int, content_type: str,
                             expected_hash: str) -> Tuple[bool, str]:
        """文件 hash 是否与预期一致（检测用户修改）"""
```

### 5.3 PhaseSummaryGenerator

**职责**：将 Phase 产出转化为结构化摘要

```python
class PhaseSummaryGenerator:
    def __init__(self, paper_name: str):
        self.paper_name = paper_name
        self.fm = PhaseFileManager(paper_name)

    def generate_phase_summary(self, phase: int,
                               phase_result: Dict = None) -> PhaseSummary:
        """
        从 Phase 执行结果或文件中提取 PhaseSummary。

        输入：Phase 执行结果（可能包含大量 content）
        输出：PhaseSummary（不含正文，只有元数据）

        流程：
        1. 如果有 phase_result，直接从中提取指标
        2. 否则，从文件读取内容并分析
        3. 计算 word_count、chapter_count、content_hash
        4. 组装 PhaseSummary
        """

    def calculate_word_count(self, content: str) -> int:
        """计算中文字数（不含标点、空格、英文）"""

    def calculate_hash(self, content: str) -> str:
        """计算内容 MD5 哈希"""

    def extract_chapter_count(self, content: str) -> int:
        """从正文中提取章节数（# 第X章 计数）"""

    def build_key_metrics(self, phase: int, phase_result: Dict) -> Dict:
        """
        根据 Phase 类型构建 key_metrics。

        Phase 2: {nodes_total, nodes_completed, nodes_failed, completion_rate}
        Phase 3: {p0_issues, p1_issues, p2_issues, guardrails_passed, guardrails_detail}
        Phase 3.5: 同 Phase 3
        Phase 4: {integrated_word_count, changes_applied, guardrails_passed}
        Phase 5: {word_count, guardrails_passed, docx_generated}
        """
```

### 5.4 PhaseHILRenderer

**职责**：HIL 消息渲染（只输出路径+摘要，不塞正文）

```python
class PhaseHILRenderer:
    def __init__(self, paper_name: str):
        self.paper_name = paper_name
        self.fm = PhaseFileManager(paper_name)

    def render_hil_message(self, phase: int, summary: PhaseSummary,
                           next_phase: int = None,
                           user_modified: bool = False) -> str:
        """
        渲染 HIL 消息。

        输出格式（Markdown）：

        ✅ Phase {N} 整合完成

        📄 文件：{file_path}
        📊 字数：{word_count} 字 | 章节：{chapter_count} 章
        🔍 审核结果：{审核摘要}
        🛡️ Guardrails：{通过情况}
        🕐 时间：{timestamp}
        {用户修改提示（如有）}

        下一阶段：Phase {N+1}
        操作指令：
        - [确认] → 进入 Phase {N+1}
        - [修改文件] → 直接编辑上方文件后说"确认修改"
        - [重新审核] → 重新跑 Phase {N} review
        """

    def render_gate_failure(self, phase: int, gate_result: GateResult) -> str:
        """
        渲染门禁未通过的消息。

        输出格式：

        ⚠️ Phase {N} 门禁未通过

        阻塞问题：
        - {issue 1}
        - {issue 2}

        请修复上述问题后重试。
        """

    def render_phase_status(self, phase: int) -> str:
        """
        渲染 Phase 当前状态（用于 --status 查询）。
        """

    def render_user_modification_warning(self, phase: int,
                                         old_hash: str,
                                         new_hash: str) -> str:
        """
        检测到用户修改文件时的提示。
        """
```

### 5.5 PhaseManager（主类，Facade 模式）

```python
class PhaseManager:
    """
    Phase 数据管理的统一入口（Facade 模式）。

    对 orchestrator 暴露简单接口，屏蔽内部复杂度。
    """

    def __init__(self, paper_name: str, workspace: str = None):
        self.paper_name = paper_name
        self.fm = PhaseFileManager(paper_name, workspace)
        self.gk = PhaseGateKeeper(paper_name)
        self.sg = PhaseSummaryGenerator(paper_name)
        self.hr = PhaseHILRenderer(paper_name)

    # ---- 核心流程 ----
    def save_phase_output(self, phase: int, content_type: str,
                          content: str,
                          key_metrics: Dict = None) -> Dict:
        """
        保存 Phase 产出。

        1. 保存内容到文件
        2. 生成 PhaseSummary
        3. 保存 summary 到 _phase{N}_summary.json
        4. 返回 {ok, file_path, summary}

        用户可直接改文件，改完说"确认"后下一 Phase 读取。
        """

    def load_phase_input(self, phase: int,
                         content_type: str = "integrated") -> Optional[str]:
        """
        读取上一 Phase 的产出。

        读取前做 freshness check。
        检测到用户修改 → 在返回内容中附带 user_modified=True 标记。
        """

    def pre_phase_check(self, target_phase: int) -> GateResult:
        """
        进入 Phase N 前的门禁检查。
        不通过 → 返回错误，不允许进入。
        """

    def pre_exit_check(self, current_phase: int) -> GateResult:
        """
        Phase N 完成前的门禁检查。
        不通过 → 返回错误，不允许完成。
        """

    def generate_hil_message(self, phase: int,
                             next_phase: int = None) -> str:
        """
        生成 HIL 消息（供用户确认/修改）。
        """

    # ---- 状态查询 ----
    def get_phase_status(self, phase: int) -> Dict:
        """
        返回 Phase N 的当前状态。
        """

    def get_all_phase_status(self) -> List[Dict]:
        """
        返回所有 Phase 的状态列表。
        """

    # ---- 流转记录 ----
    def record_transition(self, from_phase: int, to_phase: int,
                          triggered_by: str, session_id: str) -> Dict:
        """
        记录 Phase 流转。
        """

    def get_last_transition(self) -> Optional[PhaseTransition]:
        """
        获取最近一次流转记录。
        """
```

---

## 六、orchestrator 接入方式

### 6.1 Phase 3 改造示例

```python
def orchestrate_phase3(paper_name: str) -> Dict[str, Any]:
    pm = PhaseManager(paper_name)

    # 1. 前置门禁检查
    gate = pm.pre_phase_check(target_phase=3)
    if not gate.passed:
        return {
            "ok": False,
            "error": "门禁未通过",
            "gate_result": asdict(gate),
            "hil_message": pm.hr.render_gate_failure(3, gate)
        }

    # 2. 执行 Phase 3 整合逻辑（原有代码不变）
    result = do_phase3_integrate_work(paper_name)

    # 3. 保存产出到文件
    save_result = pm.save_phase_output(
        phase=3,
        content_type="integrated",
        content=result["content"],
        key_metrics=result.get("metrics", {})
    )

    # 4. 保存审核报告
    pm.save_phase_output(
        phase=3,
        content_type="review",
        content=json.dumps(result["review_report"], ensure_ascii=False),
    )

    # 5. 生成 HIL 消息（只含路径+摘要，不塞正文）
    hil_msg = pm.generate_hil_message(phase=3, next_phase=4)

    # 6. 记录流转
    pm.record_transition(from_phase=2, to_phase=3,
                         triggered_by="auto", session_id=get_current_session_id())

    return {
        "ok": True,
        "phase": 3,
        "hil_message": hil_msg,           # ✅ 不塞内容
        "file_path": save_result["file_path"],
        "summary": asdict(save_result["summary"]),
        "review_file_path": ".../_phase3_review.json",
    }
```

### 6.2 用户工作流

```
Phase 3 完成
    ↓
用户收到 HIL 消息：

✅ Phase 3 整合完成

📄 文件：.../论文_xxx/_phase3_integrated.md
📊 字数：48,320 字 | 章节：7 章
🔍 审核结果：0 个 P0 问题，2 个 P1 问题
🛡️ Guardrails：通过 9/10 项
🕐 时间：2026-06-30 15:21

下一阶段：Phase 4
操作指令：
- [确认] → 进入 Phase 4
- [修改文件] → 直接编辑上方文件后说"确认修改"
- [重新审核] → 重新跑 Phase 3 review

    ↓
用户选项：
A. 说"确认" → 进入 Phase 4
B. 编辑文件 → 说"确认修改" → Phase 4 读取新文件
C. 发现问题 → 编辑文件 → 触发 re-check
```

---

## 七、数据有效性保障机制

### 7.1 跨 Session 恢复保护

每次 Phase 完成时，记录 `content_hash` + `session_id`。

下一 Phase 读取时：
- `content_hash` 变了 → 说明用户改过文件，附带 `user_modified=True`
- `session_id` 变了 → 说明跨 session 了，需要重新确认

### 7.2 文件新鲜度检查

- `FRESHNESS_THRESHOLD_HOURS = 48`
- 文件超过 48 小时未更新 → 提示用户"文件可能过期，是否重新生成？"

### 7.3 写入锁机制

写入时检查 `.lock` 文件，防止并发覆盖：
- 有锁 → 报错"文件正在被编辑，请稍后"
- 无锁 → 创建锁 → 写入 → 删除锁（finally 确保释放）

### 7.4 数据清理策略

| 清理时机 | 清理内容 | 保留内容 |
|---------|---------|---------|
| Phase N 完成，进入 N+1 | N 的 `.tmp` / `.lock` | N 的 `integrated.md` / `review.json` / `summary.json` |
| Phase N 完成，进入 N+1 | N 的 `.bak` 备份 | N+1 的 `.bak` 保留 |
| Phase 5 完成后 | 全部中间态 `.tmp` / `.lock` | 最终 `论文_xxx.docx` + 各 Phase summary |
| 用户主动"取消论文" | 全部文件 | 无 |
| 超期未继续（>7 天无操作） | `.tmp` / `.lock` 文件 | `integrated.md` / `review.json` |

---

## 八、实现优先级

| 优先级 | 模块 | 依赖关系 |
|-------|------|---------|
| P0 | `schemas.py` | 其他所有模块的基础 |
| P0 | `file_manager.py` | PhaseManager 依赖 |
| P1 | `gate_keeper.py` | 依赖 schemas + file_manager |
| P1 | `summary_generator.py` | 依赖 schemas + file_manager |
| P2 | `hil_renderer.py` | 依赖 schemas + file_manager |
| P2 | `__init__.py`（Facade） | 依赖以上所有 |
| P3 | 集成到 orchestrator_v2 | PhaseManager 改造 |

---

## 九、待验证设计决策

以下决策需要在实现过程中确认：

1. **content_hash 算法**：MD5 够用还是需要 SHA256？
2. **文件编码**：统一 UTF-8，是否需要 BOM？
3. **大文件处理**：超过 10MB 的文件是否需要流式读写？
4. **session_id 获取方式**：从环境变量还是 OpenClaw session 上下文？
5. **清理策略的灵活性**：是否需要用户提供自定义 keep_types？

---

## 十、测试用例（实现后验证）

```python
def test_save_and_load_roundtrip():
    """保存后读取，内容一致"""
    pass

def test_backup_on_overwrite():
    """覆盖写入时自动备份"""
    pass

def test_user_modification_detection():
    """用户修改文件后，hash 变化被检测"""
    pass

def test_freshness_check():
    """过期文件被标记为不新鲜"""
    pass

def test_concurrent_write_protection():
    """并发写入被锁保护"""
    pass

def test_cleanup_keeps_important_files():
    """清理只删除中间文件，保留重要产出"""
    pass

def test_pre_phase_check_blocks_invalid_transition():
    """前置检查正确拦截非法流转"""
    pass

def test_hil_renderer_no_content_leak():
    """HIL 消息不包含正文内容"""
    pass
```

---

*文档版本：v1.0.0（2026-06-30）*
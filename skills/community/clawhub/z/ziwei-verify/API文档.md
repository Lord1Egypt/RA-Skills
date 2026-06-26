# ziwei_verify 模块 - API 文档

> **版本**：1.0  
> **日期**：2026-05-04  
> **模块路径**：`/home/caojy/.openclaw/workspace/ziwei_verify/`

---

## 📑 模块概览

`ziwei_verify` 是紫微斗数三层流水线的**第二层（校验层）**，负责生时校正与置信度优化。本模块接收 `ziwei` 技能输出的 `StandardDataPacket`，通过候选盘生成、匹配度评分、校正决策，输出校正后的数据包或交互式候选列表。

---

## 🚪 主要入口

### `run(action, **kwargs)`

**统一入口函数**，支持多种操作。

**函数签名**：

```python
def run(
    action: Literal["calibrate", "suggest", "validate"],
    **kwargs
) -> Union[StandardDataPacket, Dict, None]
```

**参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| `action` | `str` | 操作类型：`"calibrate"`、`"suggest"`、`"validate"` |
| `**kwargs` | `dict` | 动作特定参数（见下文） |

**返回值**：`StandardDataPacket` 或 `dict` 或 `None`

**示例**：

```python
from ziwei_verify import run

# 校正
result = run(
    action="calibrate",
    packet=original_packet,
    birth_dt=datetime(1993, 4, 1, 14, 0),
    max_shifts=2,
    interactive=False
)

# 仅生成建议
suggestions = run(
    action="suggest",
    packet=original_packet,
    max_shifts=2
)

# 验证输入
is_valid = run(
    action="validate",
    packet=some_packet
)
```

---

### `calibrate(packet, birth_dt, max_shifts, interactive)`

**执行生时校正**（推荐直接使用）。

**函数签名**：

```python
def calibrate(
    packet: StandardDataPacket,
    birth_dt: datetime,
    max_shifts: int = 2,
    interactive: bool = False
) -> StandardDataPacket
```

**参数详解**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `packet` | `dict` | 是 | - | `ziwei` 技能输出的原始数据包 |
| `birth_dt` | `datetime` | 是 | - | 原始出生时间（用于生成候选） |
| `max_shifts` | `int` | 否 | `2` | 最大偏移（1 或 2 个时辰） |
| `interactive` | `bool` | 否 | `False` | 是否启用交互模式 |

**返回值**：校正后的 `StandardDataPacket`

**行为说明**：

1. **自动模式** (`interactive=False`)：
   - 计算所有候选匹配度
   - 最优候选 `score >= 0.7` → 自动应用校正
   - 最优候选 `0.3 <= score < 0.7` → 返回 `LOW_CONFIDENCE` 状态（保持原盘）
   - 最优候选 `score < 0.3` → 返回 `LOW_CONFIDENCE` 状态（保持原盘）

2. **交互模式** (`interactive=True`)：
   - 计算所有候选匹配度
   - 返回 `NEED_VERIFICATION` 状态，附带候选列表
   - 等待用户选择（通过 `dialogue_handler.confirm_selection()`）

**异常**：

| 异常 | 触发条件 |
|------|----------|
| `ValueError` | `packet` 为空或格式错误 |
| `ZIWEI_DEPENDENCY_MISSING` | `ziwei` 技能未就绪 |

**示例**：

```python
result = calibrate(
    packet=original_packet,
    birth_dt=datetime(1993, 4, 1, 14, 0),
    max_shifts=2,
    interactive=False
)

if result["status"] == "CALIBRATION_DONE":
    print(f"校正时间：{result['metadata']['corrected_birth_dt']}")
elif result["status"] == "LOW_CONFIDENCE":
    print("置信度不足，建议交互模式校正")
```

---

### `suggest(packet, max_shifts)`

**仅生成候选建议，不执行校正**。

**函数签名**：

```python
def suggest(
    packet: StandardDataPacket,
    max_shifts: int = 2
) -> Dict
```

**参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| `packet` | `dict` | 原始数据包 |
| `max_shifts` | `int` | 最大偏移（默认2） |

**返回值**：`dict`，包含候选列表和对比表

```python
{
    "original_confidence": 0.38,
    "candidates": [
        {"time": "13:00", "score": 0.82, "shift_hours": -1},
        {"time": "12:00", "score": 0.65, "shift_hours": -2},
        ...
    ],
    "comparison_table": "┌───┬─────────┬───────┐..."
}
```

**使用场景**：前端展示候选列表供用户选择。

---

### `validate(packet)`

**验证输入数据包格式**。

**函数签名**：

```python
def validate(packet: StandardDataPacket) -> bool
```

**参数**：
- `packet`：待验证的数据包

**返回值**：`True` 表示格式有效，`False` 表示无效

**检查项**：
- 必需字段存在（`trace_id`, `confidence`, `data`）
- `confidence` 在 [0, 1] 范围
- `data.base_pan` 结构完整

---

## 🔧 辅助类

### `VerificationDialogueHandler`

**交互对话处理器**，管理多轮对话状态。

**主要方法**：

#### `present_candidates(result) -> str`

生成候选对比表格（Markdown 格式）。

**参数**：
- `result`：`calibrate()` 返回的 `NEED_VERIFICATION` 状态包

**返回值**：Markdown 表格字符串

```python
handler = VerificationDialogueHandler()
table = handler.present_candidates(result)
print(table)
# 输出：
# ┌───┬─────────┬───────┬─────────────┐
# │ 选项 │ 时间     │ 分数  │ 偏移说明      │
# ├───┼─────────┼───────┼─────────────┤
# │ 0  │ 13:00   │ 0.82  │ 提前1个时辰   │
# │ 1  │ 12:00   │ 0.65  │ 提前2个时辰   │
# └───┴─────────┴───────┴─────────────┘
```

---

#### `confirm_selection(session_id, choice_index) -> StandardDataPacket`

应用用户选择。

**参数**：
- `session_id`：会话ID（用于跟踪）
- `choice_index`：用户选择的候选索引（0-based）

**返回值**：应用校正后的 `StandardDataPacket`

**异常**：
- `ValueError`：`choice_index` 超出范围
- `SessionNotFound`：`session_id` 无效

**示例**：

```python
# 展示候选
table = handler.present_candidates(result)
print(table)

# 用户输入（模拟）
choice = input("请选择方案 (0-2): ")
calibrated = handler.confirm_selection(session_id="sess_123", choice_index=int(choice))
```

---

## 🏗️ 核心类

### `Calibrator`

**校正引擎**，内部使用，通常不直接调用。

**构造函数**：

```python
calibrator = Calibrator(
    max_shifts=2,
    simulation_mode=False,
    confidence_threshold_auto=0.7
)
```

**方法**：

#### `calibrate(packet, birth_dt) -> CalibrationResult`

执行完整校正流程。

**参数**：
- `packet`：原始数据包
- `birth_dt`：原始出生时间

**返回值**：`CalibrationResult` 对象

```python
@dataclass
class CalibrationResult:
    status: Literal["AUTO_ACCEPTED", "INTERACTIVE_NEEDED", "LOW_CONFIDENCE"]
    best_candidate: Optional[Candidate]
    all_candidates: List[Candidate]
    original_packet: StandardDataPacket
```

#### `generate_candidates(birth_dt, max_shifts) -> List[Candidate]`

生成候选时间列表。

**参数**：
- `birth_dt`：基准时间
- `max_shifts`：最大偏移（1 或 2）

**返回值**：`Candidate` 列表（按分数降序预排序）

```python
@dataclass
class Candidate:
    birth_dt: datetime           # 候选时间
    shift_hours: int             # 偏移小时数
    shift_description: str       # 人类可读描述（"提前1个时辰"）
    packet: StandardDataPacket   # 该时间排盘结果
    score: float                 # 匹配度（0-1）
```

---

### `ConfidenceScorer`

**置信度评分器**。

**方法**：

#### `calculate(packet) -> float`

计算给定数据包的置信度。

**公式**：
```
score = 0.4 * 命宫主星庙旺系数
      + 0.3 * 四化数量系数
      + 0.3 * 格局明确度系数
```

---

## 📊 数据类

### `StandardDataPacket`

**标准数据包**（详见 `数据流图.md`），`ziwei_verify` 读取和写入的格式。

**关键字段**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `status` | `str` | `SUCCESS` / `NEED_VERIFICATION` / `LOW_CONFIDENCE` / `CALIBRATION_DONE` |
| `confidence` | `float` | 0.0 - 1.0 |
| `data.base_pan` | `dict` | 命盘核心数据 |
| `data.verification_points` | `list` | 验证点列表 |
| `metadata.calibration_applied` | `bool` | 是否已校正 |
| `metadata.original_birth_dt` | `str` | 原始时间（ISO 8601） |
| `metadata.corrected_birth_dt` | `str` | 校正后时间（ISO 8601） |

---

### `VerificationPoint`

**验证点**数据类（`ziwei` 技能生成）。

```python
@dataclass
class VerificationPoint:
    field: str                    # 字段标识
    description: str              # 描述文本
    impact: ImpactLevel           # high | medium | low
    suggestions: List[str]        # 建议操作
    related_fields: List[str]     # 相关字段
    confidence_weight: float      # 权重（0-1）
    age_range: Optional[Tuple[int, int]]  # 影响年龄范围
    current_value: Any            # 当前值（可选）
```

---

### `Candidate`

**候选盘**数据类（校正引擎内部）。

```python
@dataclass
class Candidate:
    birth_dt: datetime
    shift_hours: int
    shift_description: str
    packet: StandardDataPacket
    score: float
```

---

## 🔄 提示词生成器

### `generate_verification_prompt(packet) -> str`

生成 ChatGPT 提示词（Markdown 格式）。

**参数**：
- `packet`：`StandardDataPacket`（含 `verification_points`）

**返回值**：完整提示词字符串

**示例输出**：

```markdown
# 紫微斗数命盘校准提示

## 当前状态
- **置信度**：38%（较低）
- **校准状态**：需要校验

## 检测到的验证点（共2项）

### 1. [高影响] 命宫主星
- **说明**：命宫为空宫（无主星坐命）
- **当前值**：无
- **置信权重**：0.75
- **建议**：
  - 考虑生时校正
  - 核对出生时间准确性

### 2. [中影响] 四化冲突
- **说明**：禄存与化忌同宫
- **当前值**：廉贞化禄、贪狼化忌
- **置信权重**：0.65
- **建议**：
  - 检查时辰边界
  - 校正生时

## 后续步骤建议
1. 核对出生时间（特别是分钟）
2. 考虑交互式校正
3. 咨询专业命理师复核

---
生成时间：2026-05-04T08:15:00Z
```

**相关函数**：

| 函数 | 说明 |
|------|------|
| `generate_verification_summary(packet)` | 生成摘要（如"共2项（高1中1低0）"） |
| `format_point_as_json(point)` | 单点序列化为 JSON（调试用） |

---

## ⚙️ 配置管理

### 配置来源

优先级从高到低：
1. 函数参数（`max_shifts=2`）
2. 环境变量
3. `config.py` 默认值

### 环境变量

| 变量名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `ZIWEI_VERIFY_MAX_SHIFTS` | `int` | `2` | 最大偏移时辰数 |
| `ZIWEI_VERIFY_SIMULATION_MODE` | `bool` | `false` | 模拟模式（测试用） |
| `ZIWEI_VERIFY_CONFIDENCE_THRESHOLD_AUTO` | `float` | `0.7` | 自动校正阈值 |
| `ZIWEI_VERIFY_CONFIDENCE_THRESHOLD_INTERACTIVE` | `float` | `0.3` | 交互模式阈值 |

**读取方式**：

```python
import os
max_shifts = int(os.getenv("ZIWEI_VERIFY_MAX_SHIFTS", "2"))
```

---

### 配置文件（`config.py`）

```python
class Config:
    max_shifts: int = 2
    simulation_mode: bool = False
    confidence_threshold_auto: float = 0.7
    confidence_threshold_interactive: float = 0.3
    enable_cache: bool = True
    cache_ttl_seconds: int = 3600

config = Config()

def get_config() -> Config:
    return config

def set_config(**kwargs) -> None:
    for k, v in kwargs.items():
        if hasattr(config, k):
            setattr(config, k, v)
```

**使用**：

```python
from ziwei_verify.config import set_config
set_config(max_shifts=1, enable_cache=False)
```

---

## 🧪 测试接口

### `tests/test_cases.py`

测试用例数据：

```python
TEST_CASES = [
    {
        "name": "1971男命-校正成功",
        "input": {
            "gender": "M",
            "birth_dt": datetime(1971, 3, 29, 7, 0),
            "location": "上海"
        },
        "expected": {
            "status": "CALIBRATION_DONE",
            "confidence": 0.82,
            "shift_hours": -1
        }
    },
    ...
]
```

### `standalone_test.py`

独立测试脚本（不依赖 OpenClaw 环境）：

```bash
python standalone_test.py
```

**测试项**：
- 数据包验证
- 置信度计算
- 候选生成
- 匹配度评分
- 校正决策

---

## 📈 性能监控

### 日志输出

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# 输出示例：
DEBUG:ziwei_verify.calibrator:Generated 5 candidates
DEBUG:ziwei_verify.calibrator:Candidate 0 (13:00): score=0.82
DEBUG:ziwei_verify.calibrator:Best candidate selected: 13:00 (shift=-1h, score=0.82)
```

### 指标采集（可选）

```python
from ziwei_verify.metrics import MetricsCollector

collector = MetricsCollector()
collector.record_calibration(
    original_confidence=0.38,
    best_score=0.82,
    auto_accepted=True,
    duration_ms=45.2
)
```

---

## 🐛 错误处理

### 异常类

| 异常 | 说明 | 处理建议 |
|------|------|----------|
| `InvalidPacketError` | 数据包格式错误 | 检查输入来源 |
| `ZIWEI_DEPENDENCY_MISSING` | ziwei 技能未加载 | 启动 OpenClaw 并加载 ziwei |
| `CalibrationFailedError` | 所有候选失败 | 尝试交互模式 |
| `SessionNotFound` | 会话ID无效 | 重新开始对话 |

### 错误码（status 字段）

| status | 含义 | confidence 范围 | 建议 |
|--------|------|----------------|------|
| `SUCCESS` | 成功（无需校正） | ≥ 0.7 | 直接解读 |
| `NEED_VERIFICATION` | 需用户校验 | 0.3 - 0.7 | 查看验证点 |
| `LOW_CONFIDENCE` | 置信度低 | < 0.3 | 建议校正 |
| `CALIBRATION_DONE` | 已校正 | ≥ 0.7（校正后） | 可解读 |
| `ERROR` | 错误 | - | 检查日志 |

---

## 🔐 安全与隐私

- **无网络请求**：所有计算本地执行
- **不存储数据**：仅内存缓存（可配置持久化）
- **日志脱敏**：出生时间在 DEBUG 级别才完整输出

---

## 📚 相关文档

- [使用示例.md](使用示例.md) - 快速上手
- [配置说明.md](配置说明.md) - 详细配置
- [排错手册.md](../../排错手册.md) - 故障排除
- [系统架构设计.md](../../ziwei-pipeline-design/架构设计.md) - 架构总览

---

**API 版本**：1.0  
**维护模块**：`ziwei_verify`  
**文档位置**：`/home/caojy/.openclaw/workspace/ziwei_verify/API文档.md`

# ziwei_verify - 生时校正与命盘验证

基于 `verification_points` 的生时校正引擎，用于提升紫微斗数命盘的准确性。

## 功能特性

- ✅ **自动生时校正**：±1、±2 时辰偏移搜索
- ✅ **置信度优化**：选择 confidence 最高的命盘
- ✅ **交互模式**：提供候选列表供用户选择
- ✅ **标准化输出**：StandardDataPacket 格式
- ✅ **性能优化**：异步候选计算，总耗时 < 2s

## 依赖

- Python 3.9+
- `ziwei` 技能（提供命盘计算）
- `zhdate` 库（农历转换）

```bash
pip install zhdate
```

## 快速开始

### 1. 自动校正（推荐）

```python
from datetime import datetime
from ziwei_verify import calibrate
from ziwei import arrange_with_packet  # 假设 ziwei 已安装

# 1. 先生成原始命盘
original_packet = arrange_with_packet(
    gender="M",
    birth_dt=datetime(1993, 4, 1, 14, 0),
    location="北京"
)

# 2. 执行生时校正
result = calibrate(
    packet=original_packet,
    birth_dt=datetime(1993, 4, 1, 14, 0),
    max_shifts=2,
    interactive=False
)

if result["status"] == "CALIBRATION_DONE":
    print(f"校正成功！新时间：{result['data']['corrected_birth_dt']}")
    print(f"置信度：{result['confidence']:.3f}")
else:
    print(f"校正未完成：{result.get('message', '未知错误')}")
```

### 2. 交互式校正

```python
from ziwei_verify import run

result = run(
    action="calibrate",
    packet=original_packet,
    birth_dt="1993-04-01T14:00:00+08:00",
    max_shifts=2,
    interactive=True
)

if result["status"] == "NEED_VERIFICATION":
    # 展示候选表给用户
    candidates = result["data"]["candidates"]
    table = format_comparison_table(candidates)
    print(table)
    
    # 等待用户输入
    choice = input("请选择方案 (0-2): ")
    # 调用 confirm_selection() 应用选择
```

## API 参考

### `calibrate(packet, birth_dt, max_shifts, interactive)`

执行生时校正。

**参数：**
- `packet` (dict): ziwei 返回的 StandardDataPacket
- `birth_dt` (datetime): 原始出生时间
- `max_shifts` (int): 最大偏移（1 或 2 时辰），默认 2
- `interactive` (bool): 是否交互模式，默认 False

**返回：** dict（StandardDataPacket）

### `run(action, **kwargs)`

统一入口函数。

**支持的 action：**
- `calibrate` - 执行校正
- `suggest` - 仅生成候选建议
- `validate` - 验证输入数据包

### `VerificationDialogueHandler`

交互对话处理器。

```python
from ziwei_verify import VerificationDialogueHandler

handler = VerificationDialogueHandler()
table = handler.present_candidates(results)  # 展示
result = handler.confirm_selection(session_id, 0)  # 确认选择
```

## 输入输出

### 输入：StandardDataPacket（来自 ziwei）

必须包含 `verification_points` 字段，示例：

```json
{
  "trace_id": "uuid",
  "skill_name": "ziwei",
  "status": "SUCCESS",
  "confidence": 0.45,
  "data": {
    "birth_info": {
      "gender": "M",
      "birth_dt": "1993-04-01T14:00:00+08:00",
      "location": "北京"
    }
  },
  "verification_points": [
    {
      "field": "命宫主星",
      "description": "命宫为空宫",
      "impact": "high",
      "suggestions": ["考虑生时校正"],
      "related_fields": ["命宫"]
    }
  ]
}
```

### 输出：StandardDataPacket（校正后）

成功：
```json
{
  "status": "CALIBRATION_DONE",
  "confidence": 0.82,
  "data": {
    "original_birth_dt": "1993-04-01T14:00:00+08:00",
    "corrected_birth_dt": "1993-04-01T13:00:00+08:00",
    "shift_hours": -1,
    "shift_description": "提前1个时辰"
  },
  "verification_points": [ ... ]  // 校正后
}
```

失败：
```json
{
  "status": "LOW_CONFIDENCE",
  "confidence": 0.58,
  "message": "置信度不足",
  "data": {
    "best_candidate": { ... },
    "all_candidates": [ ... ]
  }
}
```

交互：
```json
{
  "status": "NEED_VERIFICATION",
  "data": {
    "candidates": [ ... ],
    "comparison_table": "字符串表格"
  }
}
```

## 配置

通过环境变量或 `config.py` 调整：

```bash
export ZIWEI_VERIFY_MAX_SHIFTS=2
export ZIWEI_VERIFY_SIMULATION_MODE=false
export ZIWEI_VERIFY_CONFIDENCE_THRESHOLD_AUTO=0.7
```

在 Python 中：
```python
from ziwei_verify.config import get_config, set_config

config = get_config()
config.max_shifts = 2
config.simulation_mode = False
```

## 核心算法

### 校正流程
1. **生成候选**：基于 `max_shifts` 生成 ±1、±2 时辰的 4 个时间点
2. **重算命盘**：对每个候选时间调用 `ziwei.arrange_with_packet()`
3. **评分**：计算与原 `verification_points` 的匹配度（Jaccard + 高影响点匹配）
4. **排序**：置信度降序，高影响点数升序
5. **选择**：置信度 ≥0.7 且无 high-impact 点 → 自动接受；否则返回 LOW_CONFIDENCE

### 匹配度计算
```python
score = 0.7 * Jaccard(original_fields ∩ new_fields) +
        0.3 * (high_impact_matches / original_high_impact_count)
```

## 目录结构

```
ziwei_verify/
├── SKILL.md                    # 技能定义文档
├── __init__.py                 # 模块导出
├── main.py                     # OpenClaw 入口
├── calibrator.py               # 核心校正引擎
├── birth_time_corrector.py     # 时辰偏移计算
├── dialogue_handler.py         # 交互控制
├── output_formatter.py         # 结果格式化
├── schemas.py                  # JSON Schema
├── utils.py                    # 辅助函数（农历、真太阳时等）
├── config.py                   # 配置管理
├── README.md                   # 使用说明
├── prompts/                    # 交互提示词
│   ├── correction_prompts.txt
│   └── summary_templates.txt
└── tests/                      # 测试案例
    ├── test_cases.json
    ├── __init__.py
    └── test_cases.py
```

## 性能指标

| 阶段 | 耗时（目标） |
|------|-------------|
| 候选生成 | < 50ms |
| 单次命盘计算 | < 300ms |
| 总耗时（5候选） | < 2s |
| 内存占用 | < 100MB |

## 已知限制

1. **ziwei 依赖**：当前 `invoke_ziwei_skill()` 为模拟实现，需替换为真实调用
2. **农历库**：`zhdate` 仅支持 1900-2100 年
3. **真太阳时**：`calculate_true_solar_time()` 简化实现，需根据经纬度表完善
4. **缓存**：当前内存缓存，重启后丢失；可扩展 Redis

## 调试

```python
import logging
logging.basicConfig(level=logging.DEBUG)

from ziwei_verify import calibrate
result = calibrate(...)
```

日志输出包含：
- 候选生成详情
- 每个候选的 confidence
- 匹配度计算
- 排序结果

## 错误处理

常见错误码：
- `INVALID_INPUT`：输入数据包缺失或格式错误
- `ZIWEI_DEPENDENCY_MISSING`：ziwei 技能未就绪
- `CALIBRATION_FAILED`：所有候选失败
- `LOW_CONFIDENCE`：校正置信度不足

## 贡献

本技能基于倪海厦紫微斗数体系设计，校正算法遵循"置信度最大化"原则。

## License

MIT License

---

**维护者：** 代码助手（子Agent: coder）  
**创建日期：** 2026-05-04  
**版本：** 0.1.0

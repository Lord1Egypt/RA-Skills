# ziwei_verify Skill Definition

## Basic Information
- **Skill ID**: `ziwei_verify`
- **Name**: 生时校正与命盘验证
- **Description**: 基于 verification_points 的生时校正引擎，通过 ±1、±2 时辰偏移搜索最优出生时间
- **Version**: `0.1.0`
- **Author**: 基于倪海厦紫微斗数体系
- **Vibe**: 精准、严谨、数据驱动

## Dependencies
- **Required Skills**: `ziwei`（提供命盘计算）
- **Python Libraries**: `zhdate`（农历转换）
- **System**: Python 3.9+

## Input Schema

### StandardDataPacket (from ziwei)
```json
{
  "trace_id": "uuid-string",
  "skill_name": "ziwei",
  "execution_time": 1.234,
  "timestamp": "2024-01-01T12:00:00Z",
  "status": "SUCCESS",
  "confidence": 0.45,
  "data": {
    "birth_info": {
      "gender": "M",
      "birth_dt": "1993-04-01T14:00:00+08:00",
      "location": "北京"
    },
    "chart_data": { ... }
  },
  "verification_points": [
    {
      "field": "命宫主星",
      "description": "命宫为空宫",
      "impact": "high",
      "suggestions": ["考虑生时校正"],
      "related_fields": ["命宫", "身宫"]
    }
  ],
  "errors": [],
  "warnings": [],
  "metadata": {
    "cache_key": "ziwei:19930401M..."
  }
}
```

## Output Schema

### StandardDataPacket (CALIBRATION_DONE)
```json
{
  "trace_id": "uuid-string",
  "skill_name": "ziwei_verify",
  "execution_time": 3.456,
  "timestamp": "2024-01-01T12:00:05Z",
  "status": "CALIBRATION_DONE",
  "confidence": 0.82,
  "data": {
    "original_birth_dt": "1993-04-01T14:00:00+08:00",
    "corrected_birth_dt": "1993-04-01T13:00:00+08:00",
    "shift_hours": -1,
    "shift_description": "提前1个时辰",
    "calibration_candidates": [ ... ]
  },
  "verification_points": [ ... ],  // 校正后
  "errors": [],
  "warnings": [],
  "metadata": {
    "original_packet": { ... },
    "candidates_compared": 5,
    "best_candidate_confidence": 0.82
  }
}
```

### StandardDataPacket (LOW_CONFIDENCE)
```json
{
  "status": "LOW_CONFIDENCE",
  "confidence": 0.0,
  "message": "自动校正未能显著提升置信度",
  "data": {
    "best_candidate": { ... },
    "all_candidates": [ ... ]
  }
}
```

### StandardDataPacket (NEED_VERIFICATION)
```json
{
  "status": "NEED_VERIFICATION",
  "confidence": 0.0,
  "data": {
    "candidates": [ ... ],
    "comparison_table": "格式化表格字符串"
  }
}
```

## Action Types

| Action | Description | Input | Output |
|--------|-------------|-------|--------|
| `calibrate` | 自动/交互式生时校正 | packet + birth_dt | CALIBRATION_DONE / LOW_CONFIDENCE / NEED_VERIFICATION |
| `suggest` | 仅生成候选不执行 | packet | 候选列表 |
| `validate` | 验证输入数据包 | packet | 验证结果 |

## Call Examples

### Python API
```python
from ziwei_verify import calibrate

result = calibrate(
    packet=ziwei_packet,
    birth_dt=datetime(1993, 4, 1, 14, 0),
    max_shifts=2,
    interactive=False
)
```

### OpenClaw Invocation
```
ziwei_verify action=calibrate packet=<StandardDataPacket> birth_dt="1993-04-01T14:00:00+08:00" max_shifts=2 interactive=false
```

## Skill Lifecycle
1. **INIT**: 加载配置，验证依赖
2. **RUN**: 执行校正流程
3. **OUTPUT**: 返回 StandardDataPacket

## Error Codes
- `INVALID_INPUT`: 输入数据包缺失或格式错误
- `ZIWEI_DEPENDENCY_MISSING`: ziwei 技能未就绪
- `NO_CANDIDATES`: 无法生成候选时间
- `CALIBRATION_FAILED`: 所有候选均失败

## Performance Targets
- 候选生成：< 50ms
- 单次命盘计算：< 300ms（依赖 ziwei）
- 总耗时（5候选）：< 2s
- 内存占用：< 100MB

## Notes
- 本技能不直接 `import ziwei`，应通过 OpenClaw 的 skill invoke 机制调用
- 农历转换依赖 `zhdate` 库，需在部署时安装
- 交互模式下返回 `NEED_VERIFICATION`，由上层 Agent 发起用户确认
- 置信度阈值：≥0.7 且无 high-impact 校验点视为校正成功

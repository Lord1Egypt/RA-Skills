---
AIGC:
    ContentProducer: Minimax Agent AI
    ContentPropagator: Minimax Agent AI
    Label: AIGC
    ProduceID: "00000000000000000000000000000000"
    PropagateID: "00000000000000000000000000000000"
    ReservedCode1: 3044022071b29b3a35bd2beeff306f79bfeffe2e18517b5d7cbda0df4ebe80d8757d87aa02206e6bcac8c8191e0fc74e441701720991b07d6c6eae64426ae0bea53b825e0e78
    ReservedCode2: 304402204397090e3f96286d638117cf444889d113d9bdaa402b72e7e4a92612f9784646022033eeae21a21da47e12e9e594a8c7ee6e28022a1d694852460288ddc624f5d440
description: 日程管理。创建日程、设置提醒、查看安排。
metadata:
    category: 管理
    emoji: "\U0001F4C5"
    triggers:
        - 日程
        - calendar
        - 会议
        - 预约
        - 几点
name: calendar
---

# Calendar 技能

帮你管理日程。

## 功能

- 创建日程
- 设置提醒
- 查看今日/本周安排
- 时间冲突检测

## 示例

```
创建日程：下周三下午3点开会
查看日程：这周有什么安排
提醒我：半小时后提醒我喝水
```

---

**数据存储**: 日程数据保存在 `/workspace/data/calendar/`

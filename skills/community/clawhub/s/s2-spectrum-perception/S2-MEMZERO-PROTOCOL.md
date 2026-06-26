# 🌊 S2 Spectrum Perception: Memzero Protocol / 空间记忆协议

## 1. Dimensional Tensors (核心维度张量)

| Tensor Key | Type | Description / 物理含义 |
|------------|------|------------------------|
| `occupancy` | Boolean | `True` means a biological entity is in the 4-sqm grid. |
| `motion_state` | String | `Active`, `Static_MicroMotion`, or `None`. |
| `breathing_status`| String | Quantized state: `Normal`, `Critically_Low_Alert`, `Hyperventilation_Alert`. Exact BPM is deliberately destroyed. / 呼吸语义状态。 |
| `heart_status` | String | Quantized state: `Normal`, `Bradycardia_Alert_Or_DeepSleep`, `Tachycardia_Alert_Or_Exercise`. / 心脏语义状态。 |
| `target_distance_m`| Float | Distance of the target from the radar in meters. |

## 2. Privacy Quantization Mandate (隐私量化铁律)
- **Zero-BPM Policy**: The S2 architecture permanently bans the output of raw BPM arrays to the Agent network. 
- You must use the `_status` semantic tags to make logical deductions.
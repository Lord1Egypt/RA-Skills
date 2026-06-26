# 首尾帧模式

## 说明

提供首帧和尾帧两张图，模型生成从首帧到尾帧的过渡视频。

## 适用场景

- 需要精确的镜头衔接时
- 角色位置/姿态需要精确控制时
- 场景切换需要平滑过渡时

## 要求

1. **两张图的角色/场景必须一致**
2. **变化幅度不宜过大**（否则模型难以处理）
3. **运动逻辑要自然**

## 提示词要求

```
Transition from [首帧状态] to [尾帧状态].
Natural camera movement connecting the two states.
Maintain character consistency throughout.
Smooth, cinematic motion.
```

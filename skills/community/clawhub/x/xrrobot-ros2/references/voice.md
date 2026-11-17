# voice — 离线语音控制

## 能力
通过离线语音命令控制机器人：前进、后退、转向、停止、导航到命名点位。

## 启动
```bash
ros2launch xrrobot_offline_voice xrrobot_offline_voice.launch.py
```

**安全提示**：

- 语音命令和 CLI 命令都可能直接引起底盘运动
- 执行前先确认机器人周围已清场，并有人在现场监护
- 不要同时叠加多个会控制底盘的模块，避免命令冲突
- 如果用户没有明确要求真实运动，优先先做状态查询或解释说明，不要默认执行移动命令

## 调用
- 直接对机器人说出语音命令（如"前进"、"去A点"）
- 或通过 CLI 调用对应能力：
  ```bash
  {baseDir}/scripts/rosx {baseDir}/scripts/xr-call move --direction forward --duration-sec 2
  {baseDir}/scripts/rosx {baseDir}/scripts/xr-call navigate --waypoint A
  {baseDir}/scripts/rosx {baseDir}/scripts/xr-call list-waypoints
  {baseDir}/scripts/rosx {baseDir}/scripts/xr-call turn --direction left --duration-sec 1
  {baseDir}/scripts/rosx {baseDir}/scripts/xr-call stop
  ```

## 依赖
| 需求 | 说明 |
|------|------|
| launch | `xrrobot_offline_voice.launch.py` |
| 前置 | 需要底盘在线（`/cmd_vel`） |
| 含 | 语音识别模型、动作映射（全包） |

## 兼容性
| 可共存 | 说明 |
|--------|------|
| ✅ 任何 mode | 语音控制是附加层，不冲突 |
| ⚠️ 同时用 move/turn | 语音和 CLI 都可控底盘，注意不要冲突 |

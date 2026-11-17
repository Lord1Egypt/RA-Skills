---
name: xrrobot-ros2
description: 控制、检查和排查基于 ROS 2 Jazzy 的 XRRobot...
version: 1.0.2
metadata:
  openclaw:
    os:
      - linux
---

# XRRobot ROS 2

控制默认 ROS 2 工作区 `~/colcon_ws` 中的 XRRobot。源码包默认位于 `~/colcon_ws/src`。

## 安全约束

- 将底盘、机械臂、夹爪、导航、跟随、车道保持和自动驾驶命令视为真实物理操作。
- 仅在用户当前请求明确授权对应操作时执行物理动作。检查、状态查询和模拟运行无需再次确认。
- 源码、launch、参数、包配置、脚本和文档默认只读。允许为了排查、定位、解释或确认配置而读取工作区中的相关文件；未经用户明确要求，不得修改、创建、删除、重命名或格式化任何项目代码或配置文件。
- 唯一允许写入的持久化文件是 `{baseDir}/data/user_waypoints.yaml`，仅用于保存用户明确授权记录的自定义导航点。除这个文件外，不得写入 `skills/xrrobot-ros2`、工作区源码目录或其他任意路径。
- 不得对源码或配置使用 `apply_patch`、重定向覆盖、脚本批量改写、格式化器自动写回、`sed -i`、`tee`、编辑器命令或任何其他会写入文件的方式。需要提出代码修复建议时，只能在回复中说明，不能直接落盘。
- 如果用户请求与“源码只读”约束冲突的动作，先明确指出该 skill 只允许维护 `{baseDir}/data/user_waypoints.yaml`，其余文件仍保持只读，并要求用户单独授权修改后再继续。
- 运动前确认相关节点或模式已经就绪，并检查是否存在冲突的 `/cmd_vel` 发布者。导航、自动驾驶、车道保持或跟随控制运行时，不得启动手动运动。
- 所有运动都必须设置有限时长。不得无限期发布非零 `/cmd_vel`。有限时长的运动命令失败或被中断后，立即发送停止命令。
- 导航时不得虚构点位或位姿。先列出命名点位；目标信息不足时询问用户。发送导航目标前运行 `{baseDir}/scripts/check-navigation-ready`；校验通过时不要重复询问初始位置，校验失败时才要求用户设置。
- 抓取前先观测目标，确认模型支持目标类别且机械臂能够到达。仅在用户请求明确授权抓取时执行实际动作。
- 将停止和急停请求视为已经授权。立即发送停止命令，然后报告结果。
- 不得仅为解决冲突而运行 `ros2kill`、切换模式或终止现有控制器，除非用户请求切换或明确同意中断当前任务。

## 运行环境

通过包装脚本执行 ROS 命令，确保加载 Jazzy 和项目工作区环境：

```bash
{baseDir}/scripts/rosx ros2 node list
```

仅使用 `{baseDir}/scripts/xr-call` 已定义的子命令：

```bash
{baseDir}/scripts/rosx {baseDir}/scripts/xr-call capture --timeout 2.0
{baseDir}/scripts/rosx {baseDir}/scripts/xr-call scan --timeout 1.0
{baseDir}/scripts/rosx {baseDir}/scripts/xr-call move --direction forward --duration-sec 2 --speed-mps 0.3
{baseDir}/scripts/rosx {baseDir}/scripts/xr-call turn --direction left --duration-sec 1
{baseDir}/scripts/rosx {baseDir}/scripts/xr-call stop
{baseDir}/scripts/rosx {baseDir}/scripts/xr-call list-waypoints
{baseDir}/scripts/rosx {baseDir}/scripts/xr-call navigate --waypoint A
{baseDir}/scripts/rosx {baseDir}/scripts/check-navigation-ready
```

获取当前位置优先使用 ROS 2 命令行，不额外编写或运行项目代码：

```bash
# 首选：直接读取定位输出
{baseDir}/scripts/rosx ros2 topic echo /amcl_pose --once

# 只看位置字段
{baseDir}/scripts/rosx ros2 topic echo /amcl_pose --once --field pose.pose.position

# 备选：读取 TF（避免长时间阻塞时加 timeout）
timeout 2s {baseDir}/scripts/rosx ros2 run tf2_ros tf2_echo map base_link
```

检查摄像头是否可用时，读取 `references/camera.md`，按其中“命令行检查优先、拍照验证兜底”的顺序执行。

## 执行流程

1. 使用 `xrmode status`、`ros2 node list` 以及相关 topic、service、action 列表检查当前状态。
2. 仅阅读当前请求所需的参考文件和代码文件；源码和配置保持只读，只有 `{baseDir}/data/user_waypoints.yaml` 可以在符合规则时写入。
3. 检查前置条件、控制器冲突、定位状态和物理操作授权。
4. 手动、建图和导航模式优先使用 `xrmode` 管理。等待 `stage=ready`；`running` 仅表示进程已启动，不代表系统就绪。
5. 每次只执行一个有明确边界的步骤，检查结构化结果后再继续。
6. 任何步骤失败后立即停止后续流程。报告失败阶段、实际错误和可执行的恢复方法。不得仅凭进程成功启动就声称任务成功。
7. 当需要查看源码时，只使用只读方式读取必要片段；不要顺手修代码、补文件或调整配置。
8. 当用户要求“获取当前位置”“我现在在哪”“当前位置是什么”时，优先使用 ROS 2 命令行读取 `/amcl_pose`；若该话题不可用，再使用 `tf2_echo map base_link` 作为回退。
9. 当用户要求“检查摄像头”“摄像头能不能用”“拍照前先确认相机在线”时，读取 `references/camera.md` 并按其中的命令顺序检查 `/camera/color/image_raw`；只有命令行检查通过后，才执行 `xr-call capture`。
10. 当用户要求“记住当前位置为某个点位”时，先确认导航定位已就绪，再按第 8 条的命令行顺序读取当前位置，并只写入 `{baseDir}/data/user_waypoints.yaml`，不要改动任何源码或包配置。

## 自定义导航点记忆

- 自定义导航点持久化文件固定为 `{baseDir}/data/user_waypoints.yaml`。
- 仅当用户明确要求“记住这里”“把当前位置保存为某个点”“把这个位置设为商店/仓库/前台”等语义时，才允许写入该文件。
- 保存前必须先确认当前定位可用。优先使用命令行读取 `/amcl_pose`；若该话题不可用，再读取 `map -> base_link` TF。定位未就绪时不得盲存。
- 保存的字段至少包含：`id`、`display_name`、`frame_id`、`pose.position`、`pose.orientation`、`saved_at`，必要时可附加 `aliases`。
- `id` 使用稳定标识，限制为英文字母、数字、下划线和连字符；`display_name` 保留用户原始称呼，例如“商店”。
- 当用户说“去商店”这类自然语言目标时，先查内置点位；若未命中，再查 `{baseDir}/data/user_waypoints.yaml` 中的 `display_name`、`id` 和 `aliases`。
- 命中自定义导航点后，不要伪造 `xr-call navigate --waypoint ...` 的不存在点位；应直接使用保存的 pose 向 Nav2 发送 `NavigateToPose` 目标。
- 更新已有自定义导航点时，只覆盖同一 `id` 的记录，不得顺带改写其他点位。
- 删除自定义导航点只允许删除 `{baseDir}/data/user_waypoints.yaml` 中对应记录，不得影响代码内置点位。

## 获取当前位置

- 当用户要求“当前位置”“当前坐标”“机器人现在在哪”“记住这里之前先看看位置”时，触发当前位置查询流程。
- 首选命令：

```bash
{baseDir}/scripts/rosx ros2 topic echo /amcl_pose --once
```

- 若只需要位置字段，可使用：

```bash
{baseDir}/scripts/rosx ros2 topic echo /amcl_pose --once --field pose.pose.position
```

- 如果 `/amcl_pose` 没有消息或定位链路不是 AMCL，再回退到：

```bash
timeout 2s {baseDir}/scripts/rosx ros2 run tf2_ros tf2_echo map base_link
```

- 成功时至少向用户报告 `frame_id`、`x`、`y` 和朝向信息；若只能拿到四元数，也要原样报告，不要编造 yaw。
- 失败时明确说明是“定位未就绪”“/amcl_pose 无消息”还是“map -> base_link TF 不可用”，并给出下一步建议。

## 检查摄像头

- 当用户要求“摄像头是否可用”“检查相机”“拍照前确认摄像头在线”时，触发摄像头检查流程。
- 首选命令：

```bash
{baseDir}/scripts/rosx ros2 topic info /camera/color/image_raw
```

- 如果需要确认是否真的有图像消息，再执行：

```bash
timeout 2s {baseDir}/scripts/rosx ros2 topic echo /camera/color/image_raw --once
```

- 只有在前两步没有暴露异常时，才执行最终采集验证：

```bash
{baseDir}/scripts/rosx {baseDir}/scripts/xr-call capture --timeout 2.0
```

- 成功时向用户说明：话题在线、可收到图像、拍照成功。
- 失败时明确区分：无 publisher、话题无消息、拍照链路失败，并给出下一步建议。

## 参考文件路由

- 托管模式、launch 命令、端口和状态字段：`references/operations.md`
- 多能力组合规划和执行结果、错误解析：`references/orchestration.md`
- 底盘运动：`references/base.md`
- 建图或导航：`references/mapping.md`、`references/navigation.md`
- 相机或雷达检查：`references/camera.md`、`references/lidar.md`
- 目标检测、抓取或复合工作流：`references/grasp.md`、`references/task_orchestrator.md`
- YOLO 训练部署或视觉面板：`references/yolo.md`、`references/vision.md`
- 自动驾驶、车道保持、跟随或警戒：`references/autopilot.md`、`references/lanekeeping.md`、`references/follower.md`、`references/guard.md`
- 离线语音：`references/voice.md`

所有相对路径都以 `{baseDir}` 为基准解析。不要加载与当前任务无关的参考文件。

# yolo — YOLO 数据采集、训练与识别发布

## 能力
在机器人端进行 YOLO 目标检测数据采集、标注、训练、部署，以及独立识别结果发布。

## 启动
```bash
# 网页工作台：采集 / 标注 / 训练 / 部署
ros2launch xrrobot_yolo_studio xrrobot_yolo_studio.launch.py

# 独立识别发布：传入模型后直接发布识别结果
ros2launch xrrobot_yolo_studio xrrobot_yolo_detection.launch.py \
  model_path:=/path/to/your_model.pt
```

## 调用
Web 界面操作：浏览器访问 `http://<机器人IP>:8091`
- 选择/创建数据集
- 冻结画面画框标注
- 训练模型（或导出到电脑训练）
- 部署模型并测试

**安全提示**：

- Web 服务建议仅在可信局域网中访问，不要默认暴露到不受控网络
- 采集画面、数据集、训练结果可能包含敏感图像信息，操作前先确认数据合规性
- 新模型在接入抓取、自动驾驶、控车链路前，先单独验证识别效果，不要直接用于真实运动决策
- 识别发布节点本身不直接控车，但如果下游订阅结果后触发运动，仍应按物理机器人安全要求执行

如果用户请求的是“启动 YOLO 识别”“用某个模型开始识别”“把识别结果发出来”，优先使用独立识别 launch：

```bash
ros2launch xrrobot_yolo_studio xrrobot_yolo_detection.launch.py \
  model_path:=/path/to/your_model.pt
```

### 模型选择规则

优先使用“自动检索模型目录”的方式，而不是一上来就要求用户手填 `model_path`。

推荐做法：

1. 先执行 `ros2 pkg prefix xrrobot_yolo_studio` 获取包的安装前缀
2. 再基于该前缀拼出 `share/xrrobot_yolo_studio/...` 下的候选模型目录

示意：

```bash
PKG_PREFIX=$(ros2 pkg prefix xrrobot_yolo_studio)
MODEL_DIR_1="$PKG_PREFIX/share/xrrobot_yolo_studio/data/models"
MODEL_DIR_2="$PKG_PREFIX/share/xrrobot_yolo_studio/data/runs"
MODEL_DIR_3="$PKG_PREFIX/share/xrrobot_yolo_studio/config"
```

推荐检索顺序：

1. 已安装 `xrrobot_yolo_studio` 的 share 目录下的 `data/models`
2. 已安装 `xrrobot_yolo_studio` 的 share 目录下的 `data/runs`
3. 已安装 `xrrobot_yolo_studio` 的 share 目录下的 `config`

对应源码依据：

- Web 运行时默认数据目录来自 `get_package_share_directory("xrrobot_yolo_studio")` 下的 `data/models` 和 `data/runs`
- launch 默认模型目录也指向安装后的 `share/xrrobot_yolo_studio/data/models`
- 默认基础模型来自安装后的 `share/xrrobot_yolo_studio/config/yolo11n.pt`

检索目标文件：

- `*.pt`
- `*.onnx`

执行规则：

- 如果只找到 **一个** 模型文件，直接把它作为 `model_path`
- 如果找到 **多个** 模型文件，先把候选列表展示给用户，再让用户选
- 如果一个都没找到，再让用户提供模型文件路径

### `model_path` 参数说明

`model_path` 填的是 **YOLO 模型文件本身的路径**，不是目录。

常见可用值：

- 官方基础模型，例如：`.../share/xrrobot_yolo_studio/config/yolo11n.pt`
- 用户训练得到的最佳权重，例如训练任务返回的 `bestWeightPath`
- 导出的 ONNX 模型，例如训练任务返回的 `onnxPath`
- 用户手动上传到设备上的 `.pt` / `.onnx` 文件绝对路径

推荐规则：

- 优先传 **绝对路径**
- 文件后缀通常为 `.pt` 或 `.onnx`
- 如果自动检索没有唯一结果，再追问模型路径，不能擅自假设

错误示例：

- `model_path:=/path/to/models/` 这是目录，不是模型文件
- `model_path:=yolo_models` 这不是可直接加载的模型文件路径

正确示例：

```bash
ros2launch xrrobot_yolo_studio xrrobot_yolo_detection.launch.py \
  model_path:=/abs/path/to/yolo11n.pt
```

```bash
ros2launch xrrobot_yolo_studio xrrobot_yolo_detection.launch.py \
  model_path:=/abs/path/to/best.pt
```

如果相机已经由其他模块启动，可关闭内置相机：

```bash
ros2launch xrrobot_yolo_studio xrrobot_yolo_detection.launch.py \
  launch_camera:=false \
  image_topic:=/camera/color/image_raw \
  model_path:=/path/to/your_model.pt
```

默认发布：

- 结果话题：`/xrrobot_yolo_studio/detection_results`
- 标注图话题：`/xrrobot_yolo_studio/detection_annotated`
- 消息类型：`std_msgs/msg/String`（结果话题）

适用场景：

- 自动驾驶订阅识别结果做策略控制
- 交通灯、标志牌、障碍物等外部感知输入
- 只需要模型推理，不需要打开网页工作台

## 依赖
| 需求 | 说明 |
|------|------|
| launch | `xrrobot_yolo_studio.launch.py` / `xrrobot_yolo_detection.launch.py` |
| 前置 | 无（不依赖底盘/相机/雷达，独立运行） |

## 兼容性
| 可共存 | 说明 |
|--------|------|
| ✅ navigation | 导航中也可以做目标检测 |
| ✅ camera | 共用摄像头 |
| ✅ grasp | 视觉抓取可调用 YOLO 模型 |
| ✅ autopilot | 可向自动驾驶发布识别结果 |
| ✅ 任何其他 | 识别发布本身独立，不直接控车 |

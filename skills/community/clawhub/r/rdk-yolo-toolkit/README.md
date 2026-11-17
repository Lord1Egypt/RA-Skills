# RDK YOLO Toolkit

> 端到端 YOLO 训练 → 地瓜机器人 RDK X5 BPU 量化部署 → TROS / ROS2 实时检测的 Agent 协作工具集

支持 YOLOv5u / v8 / v9 / v11 / v13 / YOLO26 全系列的**检测 / 分割 / 姿态 / OBB / 分类**任务。
v1.0 目标平台 **RDK X5** (`bayes-e` BPU)。

**这不只是命令搬运 — 内含「工艺原理速查」章节**：每条操作都告诉你**为什么这么做**（why this ONNX / why this yaml / why this runtime），遇到 unsupported op / 量化精度掉 / forward 慢能定位根因。

---

## 🎯 它能帮你做什么

让 Agent 接管 YOLO → RDK X5 部署的**全流程**，从训练机环境装起，一路到板端 ROS2 话题发出真实检测结果：

```
[训练机 x86+GPU]                       [量化机 x86 Linux]                [板端 RDK X5]
   conda env ─▶ 数据集 ─▶ yolo train ─▶ ONNX 导出 ─▶ hb_mapper ─▶ Python 推理 ─▶ TROS / ROS2
   (一次性)    train/val/cal   best.pt    best.onnx   best_*.bin    Forward<30ms   9~30 Hz topic
```

Agent 会**按节点对话式追问**接入方式（不需要你一次性填表），并按 4 档模式执行：
- **本机直跑** — 你在 GPU 机器上调用，Agent 用 Bash 直接跑
- **SSH 远程** — 你给 ssh，Agent 远程 + tmux/nohup
- **输出指导** — 你说"只要命令"，Agent 给你清单 + Checkpoint
- **板端 SSH** — 给 RDK X5 ssh，自动连上去推理 + ROS2

---

## 真实跑通记录（YOLOv11s + 3 类自定义检测，RDK X5）

### 板端 Python 推理（hbm_runtime）
| 场景 | 检测结果 |
|---|---|
| park 测试样例 | `park 0.92` 主框 + `park 0.49` 副框 |
| obstacle 测试样例 | `obstacle 0.94`，精准框中交通锥 |

**Forward 18~22 ms ✅**（skill 标准 < 30ms）

### TROS ROS2 实时链路（feed_type=1，hbmem 零拷贝）
| 项 | 实测结果 |
|---|---|
| 单帧耗时 | recv 9ms + preprocess 2ms + **BPU 15ms** + post 1ms = **29ms / 帧** |
| 实时频率 | **9.95 Hz**（publisher fps=10 满吃） |
| 消息类型 | `ai_msgs/msg/PerceptionTargets`（含 rect / type / confidence / track_id） |

### 训练结果（32 张训练 + 8 张验证，100 epoch，3 分钟）
| 指标 | 结果 |
|---|---|
| mAP50 | 0.995 |
| mAP50-95 | 0.895 |

---

## 🚀 Quick Start

### 1. 安装 skill
解压后把 `SKILL.md` 放到你的 Claude Code skills 目录，或直接在 SkillHub 上一键启用。

### 2. 触发对话
和 Agent 说：
> 帮我用 YOLOv11s 训自定义检测模型，部署到 RDK X5

Agent 会自然语言问你训练机怎么接入，按你的回答决定是本机跑、SSH 远程跑、还是只输出指导。

### 3. 跟着 Agent 走 6 阶段
- 阶段 0：环境（可直接用 `scripts/install_train_env.sh` 一键装）
- 阶段 1：数据集（参考 `examples/data.yaml`）
- 阶段 2：训练
- 阶段 3：ONNX 导出 + hb_mapper 量化
- 阶段 4：板端 Python 推理（先用 `scripts/check_rdkx5_env.sh` 自检）
- 阶段 5：TROS ROS2 集成（用 `examples/custom_workconfig.json` 改个 class_num 就能跑）

每个阶段都有 Checkpoint，跑通了才进下一阶段。

---

## 📂 包内文件

```
RDK_YOLO_Toolkit_v1.0/
├── SKILL.md                        # 主入口（836 行，Agent 加载这一份就够了 — 含工艺原理速查）
├── README.md                       # 你正在读
├── examples/
│   ├── data.yaml                   # YOLO 数据集 yaml 模板
│   ├── custom_workconfig.json      # TROS HobotDnn 配置模板（dnn_Parser=ultralytics_yolo）
│   └── custom.list                 # 类别名占位（行数 = class_num）
├── scripts/
│   ├── install_train_env.sh        # 训练机一键装环境（conda + torch + ultralytics + rdkx5-yolo-mapper）
│   └── check_rdkx5_env.sh          # RDK X5 板端环境自检
```

---

## ⚠️ 必看：7 大踩坑点（已写进 SKILL.md）

1. **dnn_Parser 必须用 `"ultralytics_yolo"`**（官方 yolov11workconfig.json 默认是 `"yolov8"` 会完全错检）
2. **utils/ 目录必传**，且必须保持 5 层目录深度（`sys.path.append("../../../../../")`）
3. **rdkx5-yolo-mapper 隐性依赖 setuptools**（不装量化会挂在 pkg_resources）
4. **conda 26+ 必须先 `conda tos accept`**
5. **国内 pip 必须换清华源** + `--timeout 60 --retries 10`
6. **Arial.ttf 不预放占位会卡死训练**（SSL 下载失败无限重试）
7. **跨 SSH 传脚本永远用 `ssh ... 'bash -s' < script.sh`**（引号嵌套会随机吞字符，实测 `pip install` 被切成 `pip iuiet`）

---

## 🔧 兼容性

| 项 | 版本 |
|---|---|
| 训练机 OS | Linux x86_64（实测 WSL2 Ubuntu / 原生 Linux 都行）|
| Python | 3.10 |
| PyTorch | 2.5.1+cu121（CUDA 12.1）|
| ultralytics | ≥ 8.3.0 |
| rdkx5-yolo-mapper | 1.0.0 (hb_mapper 1.24.x) |
| RDK X5 OS | ≥ 3.5.0（hbm_runtime 前提）|
| TROS | Humble |
| dnn_node | ≥ 2.6.1（ultralytics_yolo parser 引入）|

---

## 📚 参考资料

- 官方 YOLO ROS 文档：https://developer.d-robotics.cc/rdk_doc/Robot_development/boxs/detection/yolo
- ultralytics_yolo sample：https://github.com/D-Robotics/rdk_model_zoo/tree/rdk_x5/samples/vision/ultralytics_yolo
- ultralytics_yolo26 sample：https://github.com/D-Robotics/rdk_model_zoo/tree/rdk_x5/samples/vision/ultralytics_yolo26
- HobotDnn CHANGELOG：https://github.com/D-Robotics/hobot_dnn/blob/develop/dnn_node/CHANGELOG.md

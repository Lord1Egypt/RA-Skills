---
name: rdk-yolo-toolkit
description: "端到端 YOLO 训练 → 地瓜 RDK X5 BPU 量化部署：Monkey Patch ONNX 导出 → hb_mapper 量化 → 板端 hbm_runtime 推理 → TROS HobotDnn ROS2 实时检测。支持 YOLOv5u~YOLOv13 和 YOLO26 全系列。内含工艺原理速查（why this ONNX, why this yaml）。"
---

# RDK YOLO Toolkit (v1.0)

YOLO 训练 → 地瓜机器人 RDK X5 BPU 量化部署 → TROS / ROS2 集成的端到端 Agent 协作工具集。

支持 YOLOv5u / v8 / v9 / v11 / v13 / YOLO26 全系列的**检测 / 分割 / 姿态 / OBB / 分类**任务。
v1.0 目标平台 **RDK X5** (`bayes-e` BPU)，基于地瓜官方工具链 **OpenExplore v1.2.8**（hb_mapper 1.24.x）。

> Toolkit 的核心价值：**不只告诉你怎么做，更告诉你为什么这样做**。
> 量化部署很多踩坑源自不理解 BPU 编译器对 ONNX 算子图、Detect head 结构、量化粒度的隐式假设。本 skill 把这些 why 写进「工艺原理速查」章节，遇到 unsupported op / 量化精度掉 / forward 慢时能定位根因。

## 端到端流程概览

```
                  [训练机 x86+GPU]                          [量化机 x86 Linux]                [板端 RDK X5]
                       │                                          │                                │
   阶段 0          阶段 1         阶段 2         阶段 3              阶段 -1 / 4              阶段 5
   conda env  ──▶ 数据集 ──▶ yolo train ──▶ ONNX 导出 ──▶ hb_mapper ──▶ 板端自检 ──▶ Python 推理 ──▶ TROS / ROS2
   (一次性)       train/val/cal     best.pt       best.onnx          best_*.bin_runtime         dnn_node
                                  mAP > 0.7    NHWC 6 输出    cosine > 0.8     Forward < 30ms       9~30 Hz
                                                                                                       /hobot_dnn_detection
```

**最常见路径**：训练机 = 量化机（同一台 x86 + GPU），ONNX 不出训练机，只有 `*.bin` 跨机 scp 到 RDK X5。

## 触发条件
用户提到：地瓜机器人 / RDK X5 / BPU / bayes-e / hb_mapper / HobotDnn / TROS / ultralytics_yolo 量化部署

---

## 🤖 Agent 启动协议（按需追问，不一次性问完）

涉及三个环境：**训练环境**（x86+GPU）/ **量化环境**（x86 Linux）/ **板端环境**（RDK X5 aarch64）。

不要一次性问"1A 2B 3A"这种死板格式。**用自然语言对话，到哪个阶段问哪个环境**，没回答之前**绝不假设**。

### 启动开场白（第一句话，简短）

```
我会带你完成 YOLO → RDK X5 BPU 一条龙部署：训练 → ONNX 导出 → 量化 → 板端推理（→ 可选 ROS2）。

为了直接帮你跑命令而不是只给指导，需要先了解几台机器你怎么接入。
我会按阶段分别问你，不一次性堆所有问题。

先从最近要做的开始：训练机你打算怎么用？
```

### 各阶段询问点

**进入训练阶段前**（阶段 0 / 阶段 2）— 问训练机：

```
训练机你打算怎么用？常见三种方式我都支持：
  • 我现在的工作目录就在 GPU 机器上 → 直接帮你跑
  • GPU 在另一台服务器上 → 给我 SSH（host/user/port，假设 ssh key 已 copy），我远程操作
  • 你只想要命令清单，自己手动跑 → 我输出指导，你回报 mAP

也可以直接告诉我："本机就行" / "ssh 到 192.168.x.x" / "给我命令"。
```

**进入量化阶段前**（阶段 3）— 只在用户没顺手提到时问：

```
量化机就跟训练机一台对吧？（hb_mapper 不需要 GPU，只要 x86 Linux）
如果是另一台，给我 SSH 信息；如果都没有量化机，我可以输出指导。
```

> 90% 的情况量化机 = 训练机（同一台 x86 Linux），不要无脑追问。

**进入板端阶段前**（阶段 -1 / 阶段 4 / 阶段 5）— 问 RDK X5：

```
RDK X5 板端怎么接？
  • 给我 SSH（root@<IP>，ssh key 已 copy）→ 我直接连上去做环境检查、传文件、跑推理、启动 ROS2
  • 你来手动跑 → 我把脚本和命令给你
```

如果用户在最初一次性给了所有 SSH 信息（"训练机 ssh xxx，板端 ssh yyy"），就不用再分别问，直接进入。**核心原则：未表达的环境保留未知，需要时再问；表达过的不重复问**。

### 执行档位（统一 4 档，不再用 ABCDE）

| 档位 | 触发条件 | Agent 行为 |
|---|---|---|
| **本机直跑** | 用户在 GPU 机器/x86 Linux 上调用 Agent | 直接用 `Bash` 工具跑 `yolo train` / `mapper.py` |
| **SSH 远程** | 用户给了 host/user/port | 用 `ssh -p PORT user@host 'bash -s' < script.sh` 远程跑，tmux 或 nohup 防断开 |
| **输出指导** | 用户明说"只要命令" | 输出完整命令清单 + 校验点，要求用户回报关键指标（mAP、bin 大小、forward 时间） |
| **板端 SSH** | 用户给了 RDK X5 SSH | ssh + scp 全自动；板端默认无 tmux，用 `nohup ... &` 兜底 |

### SSH 安全约定
- **不索要明文密码**，假设用户配好 SSH key
- 连不上时提示 `ssh-copy-id user@host`（非默认端口加 `-p PORT`）
- 长时间任务（训练、ROS2 节点）必须用 `tmux` 或 `nohup` 防 SSH 断开
- **跨 SSH 传脚本永远走 `ssh ... 'bash -s' < local_script.sh`**，不要把长命令塞进 `ssh ... "..."` — 引号嵌套会被随机吞字符（实测：`pip install` 被切成 `pip iuiet`，`dataset/data.yaml` 被切成 `datasetta.yaml`，找半天 bug）
- **scp 多源限制**：新 OpenSSH（≥ 9.0）`scp src1 src2 host:dst` 行为变了，建议**逐个 scp** 或 `scp -r` 整目录

### 跨机文件流转
绝大多数实际场景训练机 = 量化机（都是 x86 Linux + GPU），ONNX 不出训练机：
```
[最常见]  训练机(GPU x86) ─── *.bin ───▶ RDK X5
[较少见]  训练机 → 量化机 → RDK X5（两段 scp）
[纯本地]  本机一条龙
```

---

## ⚠️ 板端环境硬性要求（最先验证）

**板端 SSH 档位** Agent 直接 `ssh root@<RDK_IP> 'bash -s' < check_env.sh`；**输出指导档位** Agent 把脚本贴给用户让他自己跑：

```bash
#!/bin/bash
echo "=== RDK X5 部署环境自检 ==="

# 1. RDK OS ≥ 3.5.0（hbm_runtime 前提）
OS_VERSION=$(cat /etc/version)
echo "OS: $OS_VERSION"
[ "$(printf '%s\n' "3.5.0" "$OS_VERSION" | sort -V | head -n1)" = "3.5.0" ] && echo "  ✅" || echo "  ❌ 需 ≥ 3.5.0"

# 2. TROS Humble setup
[ -f /opt/tros/humble/setup.bash ] && echo "TROS Humble: ✅" || echo "TROS Humble: ❌"

# 3. dnn_node ≥ 2.6.1（ultralytics_yolo parser 引入）
DNN_VER=$(cat /opt/tros/humble/share/dnn_node/package.xml | grep -oP '(?<=<version>)[^<]+')
echo "dnn_node: $DNN_VER"
[ "$(printf '%s\n' "2.6.1" "$DNN_VER" | sort -V | head -n1)" = "2.6.1" ] && echo "  ✅" || echo "  ❌ apt upgrade tros-humble-dnn-node"

# 4. hbm_runtime
python3 -c "import hbm_runtime" 2>/dev/null && echo "hbm_runtime: ✅" || echo "hbm_runtime: ❌ pip install hbm-runtime"

# 5. BPU 设备节点
ls /dev/bpu* 2>/dev/null && echo "BPU device: ✅" || echo "BPU device: ❌"

# 6. python opencv numpy（runtime 用得到）
python3 -c "import cv2, numpy; print('cv2', cv2.__version__, '| numpy', numpy.__version__)" 2>&1

# 7. tmux（板端默认 OS 镜像不带，没有就用 nohup）
which tmux 2>/dev/null && echo "tmux: ✅" || echo "tmux: ❌（不重要，Agent 会用 nohup）"
```

dnn_node 版本节点：
- `tros_2.6.1` (2026-02-25)：`ultralytics_yolo` parser
- `tros_2.6.2` (2026-05-08)：`yolo26_seg` parser

**实测基线**（RDK X5 / OS 3.5.0-beta / dnn_node 2.6.1）：
- BPU Platform Version 1.3.6, HBRT 3.15.55.0, hb_mapper 1.24.3
- `/dev/bpu`, `/dev/bpu_core0` 双节点存在
- cv2 4.11.0, numpy 1.26.4 已自带

---

## 自定义支持

### 类别数：✅ 完全自由
唯一约束：HobotDnn 的 `class_num` 必须等于 `cls_names_list` 文件行数。

### 分辨率：⚠️ 仅正方形且能被 32 整除
合法值：320/384/416/480/512/576/640/768/896/1024/1280
默认：检测/分割/姿态/OBB = 640，分类 = 224
`export_monkey_patch.py` 不传 imgsz，继承训练 imgsz。改尺寸：训练命令加 `imgsz=N`，或改脚本 `m.export(..., imgsz=N)`

---

## 两个 Sample 能力

| Sample | 检测 | 分割 | 姿态 | OBB | 分类 |
|--------|-----|-----|-----|-----|-----|
| ultralytics_yolo | YOLOv5u~v13 ✅ | YOLOv8/v9/11 ✅ | YOLOv8/11 ✅ | ⚠️ TODO | YOLOv8/11 ✅ (224) |
| ultralytics_yolo26 | n/s/m/l/x ✅ | ✅ | ✅ | ✅ 唯一支持 | ✅ (224) |

---

## 七大易错点（真机踩坑总结）

1. **dnn_Parser**：用户量化的模型（box 含反量化节点）一律用 `"ultralytics_yolo"`，**不要用 `"yolov8"`** ⚠️ 官方 `/opt/tros/humble/lib/dnn_node_example/config/yolov11workconfig.json` 默认是 `yolov8`，会**完全错检**，复制后必须改
2. **utils/ 必传**：`main.py` 用相对路径导入 `utils/py_utils/`，且需要保持 `samples/vision/<model>/runtime/python/` 这种 5 层深度（脚本里有 `sys.path.append("../../../../../")`）
3. **export_monkey_patch.py 用 `simplify=False`**：不要改成 True，会破坏 BPU 优化路径
4. **rdkx5-yolo-mapper 隐性依赖 setuptools**：新版 conda env 不带 `pkg_resources`，量化会在 `horizon_nn.build_onnx` 阶段抛 `ModuleNotFoundError: No module named 'pkg_resources'`。装包后必须 `pip install setuptools`
5. **conda 26+ 必须先接受 ToS**：`conda create` 直接报 `CondaToSNonInteractiveError`，需先 `conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main && conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r`
6. **pip 国内网络**：torch / ultralytics 直连 pypi 常超时挂死。**国内必须换清华源** `-i https://pypi.tuna.tsinghua.edu.cn/simple --timeout 60 --retries 10`
7. **Arial.ttf 下载会卡死训练**：`ultralytics` 首次会去 `https://ultralytics.com/assets/Arial.ttf` 拉字体，SSL 失败会无限重试堵住整个 train。**提前放占位**：`cp /usr/share/fonts/truetype/dejavu/DejaVuSans.ttf ~/.config/Ultralytics/Arial.ttf`

### dnn_Parser 速查
| 系列 | dnn_Parser | reg_max | model_output_count |
|------|-----------|---------|-------------------|
| YOLOv5u~v13 检测 | `"ultralytics_yolo"` | `16` | `6` |
| YOLO26 检测 | `"ultralytics_yolo"` | `1` | `6` |
| YOLOv8/v9/11 分割 | `"yolov8_seg"` | `16` | `10` |
| YOLO26 分割 | `"yolo26_seg"` | — | `10` |

---

## 🧠 工艺原理速查（why this ONNX / why this yaml / why this runtime）

> 这章解释**为什么**这么做，不是"怎么做"。遇到 unsupported op / 精度掉 / forward 慢时回来翻这里找根因。
>
> **本章每条 why 都有出处**：
> - **官方文档**：地瓜 v1.2.8 工具链手册 `x5_doc-v1.2.8-py310-en` （`oe_mapper/source/ptq/...` 各 .rst 章节）— 标 `quantize_compile.rst.txt` / `hb_mapper_makertbin.rst.txt` / `prepare_calibration_data.rst.txt` / `model_prepare.rst.txt` 等出处
> - **官方源码**：rdk_model_zoo (`samples/vision/ultralytics_yolo/` + `utils/py_utils/`) — 标具体文件名
> - **实测**：本 skill 在 RTX 3060 训练 + RDK X5 OS 3.5.0-beta 实际跑通的产物指标

### A. ONNX 导出：为什么改 Detect head + simplify=False？

**问题**：Ultralytics 默认 `model.export(format='onnx', simplify=True)` 导出的 ONNX，hb_mapper 量化会报 `unsupported op` 或量化精度严重下降。

**根因**：Ultralytics 默认 Detect head 把 6 个分支（3 stride × 2 [cls, bbox]）的输出**在模型内部就 concat + reshape + DFL softmax + cumsum**，组合成 `(1, 4+nc, 8400)` 这种张量。这一坨复合算子里有：

| 算子 | BPU 友好？ | 原因 |
|---|---|---|
| `Conv` + `Sigmoid` + `Mul` | ✅ | BPU 原生支持 |
| `Concat(axis=1)` 大张量 | ⚠️ | 跨 channel concat 会破坏 per-channel 量化 |
| `Reshape` + `Transpose` 多次 | ⚠️ | 每次 reshape 都要走 CPU |
| `Softmax(axis=last_dim, 16 bins)` | ❌ | DFL 的 16-bin softmax 在 BPU 上是 CPU fallback，每次推理多 5-10ms |
| `Cumsum` / `MatMul(constant)` | ❌ | DFL 期望值计算 BPU 不优化 |

**解决方案**：`export_monkey_patch.py` 通过 monkey patch 把 `Detect.forward` 替换成**只输出 6 个独立 head**（NHWC 排布），把所有 DFL 解码 / sigmoid / NMS 都搬到板端 numpy 后处理：

```python
def Detect_forward(self, x):
    # 替换原版！只输出 cls + bbox 两组共 6 个 tensor
    result = []
    for i in range(self.nl):  # nl=3 个 stride
        result.append(self.cv3[i](x[i]).permute(0,2,3,1).contiguous())  # cls (NHWC)
        result.append(self.cv2[i](x[i]).permute(0,2,3,1).contiguous())  # bbox (NHWC)
    return result   # 共 6 个输出，全部纯 Conv + permute
```

**为什么 `simplify=False`**：onnx-simplifier 会把 `permute(0,2,3,1)` 这种 layout transform 折叠回 `Reshape + Transpose` 组合，反而把 NHWC 信息丢了 — BPU 编译器再看不出"这是 layout 转换"，就走通用 transpose 实现，性能大跌。**保留原始算子图** = 让 BPU 编译器看清楚每一步意图。

**ONNX 版本要求（官方明文实证）**：
- 来源：`oe_mapper/source/ptq/ptq_usage/model_prepare.rst.txt` attention 段
- **opset 必须是 10 或 11**（v1.2.8 工具链官方原话："Presently Horizon supports ONNX opset10 and opset11"）
- **ir_version ≤ 7**（参考 ONNX 官方 versioning 表对照）
- 本 skill 的 `export_monkey_patch.py` 默认 `opset=11`，符合要求 ✅
- 输入框架：PyTorch / TensorFlow / PaddlePaddle / MXNet 都通过 ONNX 中转；Caffe 直接读 caffemodel

**对 YOLOv11 的额外特殊处理**：v11 的 C2PSA 模块里有 `Attention` 算子，原版用 `Softmax(axis=-1)` 是 BPU 不友好的。Skill 同时 patch 了 `Attention.forward`：
- 把 `attn` permute 到 `CHW2HWC like`
- **手写 stable softmax**（先减 max 再 exp 再除 sum），让 BPU 把 `Exp / Sum / Div` 各自识别为 BPU 原生算子
- 反过来 permute 回去

### B. mapper.py yaml：每个字段为什么这么填？

> **使用须知**：**这份 yaml 是 `mapper.py` 跑量化时自动生成的**（见 `mapper.py:228` 的 `yaml_content` 模板），用户**不需要手写**。下面注释版的目的是：让你看懂 mapper.py 生成的 `.temporary_workspace/config.yaml`，量化精度不达标时知道改哪些字段。
>
> 实际调用方式：
> ```bash
> python3 mapper.py --onnx best.onnx --cal-images ./calibration_data \
>   --cal-sample-num 50 --optimize-level O3 --output-dir .
> # 可选：--quantized int16    （会在 optimization 追加 set_all_nodes_int16，整模型用 int16）
> # 可选：--jobs 16            （并行编译进程数）
> # 可选：--save-cache         （保留 .temporary_workspace，含生成的 config.yaml）
> ```

参考 `samples/vision/ultralytics_yolo/conversion/config.yaml`（mapper.py 实际生成产物），逐字段解释：

```yaml
model_parameters:
  onnx_model: 'best.onnx'           # 输入的 BPU 友好 ONNX
  march: "bayes-e"                  # ⚠️ 必填，RDK X5 BPU 指令集，固定为 "bayes-e"
  layer_out_dump: False             # True 会 dump 每层激活，调试用
  working_dir: 'bpu_model_output'
  output_model_file_prefix: 'best_bayese_640x640_nv12'  # 命名规范：<name>_<march>_<HxW>_<input_format>

input_parameters:
  input_name: ""                    # 留空 = 自动从 ONNX 拿
  input_type_rt: 'nv12'             # ⚠️ 必填，板端运行时输入格式
                                    # 官方完整 RANGE: rgb / bgr / nv12 / yuv444_128 / gray / featuremap
                                    #   nv12          → 摄像头/MIPI/USB 直吃，零拷贝，BPU 最高效（本 skill 推荐）
                                    #   yuv444_128    → 某些 ISP 输出格式（注意是带 _128 后缀，不是 yuv444）
                                    #   rgb / bgr     → uint8，工具链内部自动减 128 转 int8
                                    #   gray          → 单通道
                                    #   featuremap    → tensor 输入（fp32），radar/speech 用
                                    # ⚠️ input_type_rt=nv12 时 quanti.onnx 输入 layout 强制 NHWC
                                    # （这就是为什么 export_monkey_patch 把 Detect head permute 成 NHWC）
  input_type_train: 'rgb'           # 训练时输入格式（ultralytics 默认 RGB）
                                    # rt 和 train 不同时，hb_mapper 自动插入色彩转换节点
                                    # 兼容矩阵（官方表）：train=rgb → rt 可选 nv12/yuv444/rgb/bgr ✅
  input_layout_train: 'NCHW'        # 训练时 layout（torch 默认 NCHW）
  norm_type: 'data_scale'           # 归一化方式 RANGE（官方）：
                                    #   no_preprocess       → 不做归一化（**官方默认值**）
                                    #   data_scale          → 只缩放（YOLO 用这个，× 1/255）
                                    #   data_mean           → 只减均值
                                    #   data_mean_and_scale → 先减均值再缩放（ResNet/MobileNet 等用）
  scale_value: 0.003921568627451    # = 1/255.0，把 uint8 [0,255] → fp32 [0,1]
                                    # ⚠️ 不要写 0.00392 这种截断的，精度会掉

calibration_parameters:
  cal_data_dir: '/abs/path/calibration_data_temporary_folder'  # 必须绝对路径
  cal_data_type: 'float32'          # mapper.py 准备的 .rgbchw 文件是 fp32
  calibration_type: 'default'       # 校准算法 RANGE（官方完整 6 选项）：
                                    #   default → 自动搜索策略，推荐首选（官方建议先用 default）
                                    #   mix     → 节点级混合多种算法，比 default 更精细，对量化敏感节点自动选最优算法
                                    #   kl      → KL 散度最小化，公开算法，精度好但慢
                                    #   max     → 取激活最大值（max_percentile 控制截断点 0.5~1.0），快但对 outlier 敏感
                                    #   load    → 加载 QAT 模型导出的校准表（需 plugin 配合）
                                    #   skip    → 不校准，max + 随机数据，仅验证模型结构能跑通，⚠️ 不能用于精度验证
  optimization: set_Softmax_input_int8,set_Softmax_output_int8
                                    # ⚠️ 官方原话：softmax 默认 fp32（"defaults to float to compute non-quantized nodes"）
                                    # 这两个选项把 Softmax 量化到 int8 跑在 BPU 上 — 对带 Attention 的 v11/v13 必加
                                    # 官方文档 (hb_mapper_makertbin.rst.txt) RANGE：
                                    #   set_model_output_int8 / set_model_output_int16  — 整模型输出精度
                                    #   set_{NodeKind}_input_int16 / set_{NodeKind}_output_int16  — 指定算子类（NodeKind 用 ONNX 标准算子名，如 Conv/Mul/Sigmoid）
                                    #   set_Softmax_input_int8 / set_Softmax_output_int8  — Softmax 专用，本 skill 推荐
                                    #   asymmetric            — 非对称量化（calibration_type=default 时自动选，不能显式配）
                                    #   bias_correction       — BiasCorrection 量化方法
                                    #   lstm_batch_last       — X5 LSTM 优化（不保证加速）
                                    # 官方源码 (mapper.py:222) 额外用到：
                                    #   set_all_nodes_int16   — 全模型节点统一 int16（官方文档 RANGE 未列出，但 rdk_model_zoo mapper.py 使用，对应 --quantized int16）
                                    # ⚠️ 多个选项用英文逗号 `,` 分隔，不要空格

compiler_parameters:
  jobs: 16                          # 并行编译进程数（CPU 核数；过大会 OOM）
  compile_mode: 'latency'           # 编译策略 RANGE（官方完整 3 选项）：
                                    #   latency   → 优化推理延迟（**官方默认**，生产首选）
                                    #   bandwidth → 优化 DDR 访问带宽（模型严重超带宽时用）
                                    #   balance   → 平衡延迟和带宽（需配合 balance_factor 0~100）
                                    # 官方建议：模型不严重超带宽就用 latency
  debug: true                       # 在 .bin 里保留调试 sym，hb_perf / vec_diff 才能用
  optimize_level: 'O3'              # ⚠️ 默认 'O0'（不优化），生产必须显式 'O3'（官方原话："the O3 level of optimization must be used to ensure optimal performance"）
                                    # RANGE: O0 / O1 / O2 / O3
```

### C. PTQ 5 阶段流水线 + 4 个中间产物（官方实证）

`hb_mapper makertbin` 内部按顺序跑 5 阶段（来自官方 `quantize_compile.rst.txt`）：

```
ONNX 输入
   ↓
[1] Parse        → original_float_model.onnx   （加入 input_type 预处理节点）
   ↓
[2] Optimize     → optimized_float_model.onnx  （BN 融合 Conv 等算子优化）
   ↓
[3] Calibrate    → calibrated_model.onnx       （读校准数据，计算每节点 scale/zero_point）
   ↓
[4] Quantize     → quantized_model.onnx        （int8 计算精度，用于评估量化精度损失）
   ↓
[5] Compile      → *.bin                       （Horizon 编译器生成 BPU 指令）
```

**4 个中间产物用途**（官方）：
| 产物 | 精度 | 用途 |
|---|---|---|
| `*_original_float_model.onnx` | fp32 | 加了预处理节点，**调试时供 Horizon 技术支持复现问题** |
| `*_optimized_float_model.onnx` | fp32 | 算子融合后，与 original 对比可见结构变化 |
| `*_calibrated_model.onnx` | fp32 | 含校准 scale，量化精度评估的中间步骤 |
| `*_quantized_model.onnx` | **int8** | **精度评估必用**（vs 原 fp32 模型对比） |

**input_type_rt → ONNX 中间格式（官方表）**：
| input_type_rt | 中间格式 | 数据类型 |
|---|---|---|
| nv12 | yuv444_128 | int8（每值减 128）|
| yuv444 | yuv444_128 | int8 |
| rgb | RGB_128 | int8 |
| bgr | BGR_128 | int8 |
| gray | GRAY_128 | int8 |
| featuremap | featuremap | float32 |

`*_128` 后缀的含义：原始 uint8 [0,255] 减 128 → int8 [-128,127]。这一步由 API 自动完成，**用户不需要自己减 128**（官方 attention 原文）。

**input_source**（compiler_parameters）— BPU 数据来源：
- `pyramid` — 摄像头/MIPI 经 ISP pyramid 输入（**nv12 时官方默认**）
- `ddr` — DDR 内存（**其他 input_type_rt 时官方默认**）
- `resizer` — 用 BPU resizer 硬件预处理（仅 nv12 / gray 支持）

### D. 校准数据：为什么是 .rgbchw 字节文件？为什么必须用真实场景图？

**.rgbchw 格式**：mapper.py 把每张 jpg 转成 `[1, 3, H, W]` 的 fp32 NCHW + RGB 字节流，直接 `.tofile()` 存盘。原因：
1. hb_mapper 校准时**逐张读 fp32 数组**走 ONNX 前向，统计每层激活分布（max / kl / percentile）
2. 用 jpg 还要 decode → cv2 → resize → 转 fp32 → 一遍颜色空间转换，校准时跑几百次开销大
3. **预处理必须和板端一致**：BGR→RGB（color swap）+ resize 到 input shape + HWC→CHW + fp32

**为什么必须真实场景**：量化的本质是把 fp32 激活值映射到 int8 / int16，校准集决定 **scale / zero_point**：
- 如果校准集和生产场景**分布差很远**（例如校准用 COCO，生产用厂房安防），int8 的 256 个刻度集中错地方，关键激活值被裁掉 → mAP 掉 5%+
- **校准集张数 < 20**：分布估计噪声大，calibration_type=default 可能选不出最优策略 → mapper.py 主动 warn
- **校准集张数 > 50**：边际收益小，但编译时间线性增加（每张图都要全模型前向）→ 主动 warn

### E. 量化精度验收：cosine similarity 怎么读？

mapper 跑完输出日志末尾会有：
```
Output      Cosine Similarity  L1 Distance  L2 Distance  Chebyshev Distance
output0     0.999921           0.097216     0.000950     1.235699
478         0.995124           0.118130     0.000285     3.842017
...
```

| 指标 | 意义 | 红线 |
|---|---|---|
| **Cosine Similarity** | fp32 输出 vs 量化输出的方向一致性 | **官方红线**：< 0.8 = significant accuracy loss（`quantize_compile.rst.txt`）<br>**生产经验**：≥ 0.99 优秀 / 0.8~0.99 可接受需测精度 / < 0.8 必须重做校准 |
| L1 / L2 Distance | 绝对值差异 | 看模型规模相对评估 |
| Chebyshev Distance | 最大单点偏差 | < 50 ✅ |

**典型问题排查**：
- 某个 output cosine = 0.85 → 该层有 outlier 激活，试 `calibration_type: kl` 或 `calibration_type: mix`；或加 `optimization: set_Conv_input_int16`（针对算子类型，NodeKind 用 ONNX 标准算子名）；或直接整模型升 int16：`python3 mapper.py --quantized int16`（会在 optimization 末尾追加 `set_all_nodes_int16`）
- 全部 < 0.9 → 校准集分布严重不匹配，换数据集
- 中间层 cosine = 1.0 但末层 = 0.8 → 累积量化误差，可试 `optimization: set_model_output_int16`（提高最终输出精度）

### F. 板端 hbm_runtime：API 调用链路解读

> **来源说明**：v1.2.8 工具链官方文档主要讲 C++ `libdnn.so` + `hbDNN*` API；Python `hbm_runtime` 的 API 在板端 `pydev_multimedia_api_x5/ai-python-api` 手册里。本节内容**直接来自 rdk_model_zoo 实际可运行源码**（`ultralytics_yolo_det.py` + `utils/py_utils/inspect.py`），与板端运行实测一致 ✅。

完整调用顺序（来自 `ultralytics_yolo_det.py`）：

```python
import hbm_runtime

# 1. 加载 .bin 模型（一次性，~300ms）
model = hbm_runtime.HB_HBMRuntime("best_bayese_640x640_nv12.bin")

# 2. 拿元数据
model.model_names         # → ['best_bayese_640x640_nv12']  支持 multi-model bin
model.input_names         # → {'best_bayese_640x640_nv12': ['images']}
model.input_shapes        # → {'best_bayese_640x640_nv12': {'images': [1,3,640,640]}}
model.input_quants        # → QuantParams 含 scale / zero_point / axis / quant_type
model.output_names        # → 6 个：['output0','478','492','500','514','522']
model.output_quants       # 同上，每个 output 独立 scale

# 3. 调度参数（可选，多模型分核用）
model.set_scheduling_params(
    priority={'best_bayese_640x640_nv12': 0},      # 0~255，数字越大越优先
    bpu_cores={'best_bayese_640x640_nv12': [0]},   # 指定 BPU core
)

# 4. 推理（核心，~15-20ms）
input_tensor = {
    model.model_names[0]: {
        'images': packed_nv12_uint8  # ⚠️ shape: (y_size + uv_size,) flat uint8
                                     #     Y 平面在前，UV 交错在后
    }
}
outputs = model.run(input_tensor)
# outputs = {'best_...': {'output0': arr, '478': arr, ...}}

# 5. 反量化（如果模型输出是 int8/int16，框架已经反量化好；本 skill 的 output 是 fp32 不用）
# from utils.py_utils.postprocess import dequantize_outputs
# fp32_outputs = dequantize_outputs(outputs['model_name'], model.output_quants['model_name'])
```

**为什么 input 是扁平 uint8 而不是 (1,3,H,W)？**
NV12 是 **packed planar** 格式：Y 平面 `H*W` bytes，UV 平面 `H*W/2` bytes（U/V 交错），合计 `H*W*1.5` bytes。BPU 直接吃这个布局，无需 CPU 重排。preprocess.py 的 `bgr_to_nv12_planes` + `np.concatenate([y.reshape(-1), uv.reshape(-1)])` 就是干这个。

**为什么 letterbox 用 (127,127,127) 灰色填充？**
NV12 的灰色 = Y=127, U=128, V=128，**量化后处于激活分布中位**，不会让边缘的填充像素污染统计。用黑色(0) 或白色(255) 会在边缘形成强信号，被量化器当成"重要边缘"，扭曲 scale。

### G. 后处理：为什么先 logit 阈值再 sigmoid？

`UltralyticsYOLODetect.__init__` 里有：
```python
self.conf_thres_raw = -np.log(1.0 / self.cfg.score_thres - 1.0)
# score_thres=0.25 → conf_thres_raw ≈ -1.099
```

**原理**：sigmoid 单调递增，`sigmoid(x) > 0.25  ⇔  x > -1.099`。
- 三个 cls head 总共 `(80+40+20)² × num_class = 8400 × N` 个 logit
- 如果先 sigmoid 再过滤，要算 8400*N 次 exp，慢
- 改成**先 logit 阈值过滤**，只保留 ~几十个 valid_indices，再 sigmoid → 省 99% sigmoid

**DFL 解码**（box head 输出 `(grid, 64) = (grid, 4*16)`）：
```python
# 16 bins 的 softmax + 加权和 = 期望距离
ltrb = sum(softmax(bbox.reshape(-1, 4, 16), axis=2) * [0,1,2,...,15], axis=2)
# anchor 中心 ± ltrb 得到 xyxy
boxes = [anchor_x - L, anchor_y - T, anchor_x + R, anchor_y + B] * stride
```
这块为什么不在 BPU 上做？因为 `softmax(axis=2, bins=16) + matmul(weights_static)` 在 BPU 上要走 fallback，单帧多 3-5ms；放 CPU 上 numpy 向量化 ~1ms。

### H. 平台基线（v1.0 = RDK X5 only）

| 项 | 值 |
|---|---|
| 板卡 | RDK X5 |
| SoC | x5 |
| march | bayes-e |
| BPU 设备节点 | `/dev/bpu`, `/dev/bpu_core0` |
| 量化精度支持 | int8 / int16，Attention 算子支持 |
| 工具链 | hb_mapper 1.24.x + hbm_runtime |

**板端自检**：`cat /sys/class/boardinfo/soc_name` 应返回 `x5`，本 skill 已在 `utils/py_utils/inspect.py:get_soc_name()` 实现。

---



### 阶段 0：环境
**本机直跑** → 在 GPU 机器上直接装；**SSH 远程** → 用 `ssh ... 'bash -s' < install.sh` 到训练机上装；**输出指导** → 把下面命令贴给用户

```bash
# Step 1: conda 环境 + ToS（conda 26+ 必须）
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r
conda create -n rdk_env python=3.10 -y && conda activate rdk_env

# Step 2: 国内必须换源装 PyTorch（pypi 直连必超时）
PIP_OPTS="-i https://pypi.tuna.tsinghua.edu.cn/simple --timeout 60 --retries 10"
pip install $PIP_OPTS torch torchvision --index-url https://download.pytorch.org/whl/cu121
pip install $PIP_OPTS "ultralytics>=8.3.0" rdkx5-yolo-mapper onnx onnxsim

# Step 3: 修 rdkx5-yolo-mapper 缺的 setuptools（不装会在量化阶段挂掉！）
pip install $PIP_OPTS setuptools

# Step 4: 字体占位防 ultralytics 卡 SSL 下载
mkdir -p ~/.config/Ultralytics
cp /usr/share/fonts/truetype/dejavu/DejaVuSans.ttf ~/.config/Ultralytics/Arial.ttf

# Step 5: 验证（任何一项失败请回到对应 Step 修复，不要往下走）
python -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0))"
python -c "import pkg_resources; print('setuptools OK')"   # 这步漏了 → 阶段 3 量化必挂
hb_mapper --version  # 应输出 1.24.x
ls ~/.config/Ultralytics/Arial.ttf   # 字体占位文件应存在
```

**WSL2 GPU 排查**：如果 `nvidia-smi` 不在 PATH，检查 `/usr/lib/wsl/lib/nvidia-smi`，把这路径加进 `~/.bashrc` 即可（不需要重装驱动）。

### 阶段 1：数据

#### 1.1 目录结构

```
project/
├── dataset/
│   ├── images/
│   │   ├── train/     ← 训练集
│   │   └── val/       ← 验证集（20~50 张即可，自定）
│   ├── labels/
│   │   ├── train/
│   │   └── val/
│   └── data.yaml      ← path/train/val/names
└── calibration_data/  ← 校准集（量化用，**官方推荐 20~100 张**，可直接复用 val 或 train 子集）
```

#### 1.2 三种集合的作用 & 推荐张数

| 集合 | 用途 | 推荐张数 | Skill 强约束 |
|---|---|---|---|
| **训练集 (train)** | `yolo train` 学权重 | 越多越好（典型 100+） | 无 |
| **验证集 (val)** | 训练中算 mAP，YOLO 自动跑 | 20~50 张（自定） | 至少 1 类有标注框，否则 mAP 算不出来 |
| **校准集 (calibration)** | `hb_mapper` 量化时统计激活分布 | **官方推荐 20~100 张**（`prepare_calibration_data.rst.txt`：少于 20 计算不稳，多于 100 边际收益小） | 必须**来自训练集或验证集**，**不要用罕见样本（纯色图、无目标的图）**（官方原文） |

**实战准则**：
- 验证集和校准集张数可以相同（都 20~100），但**不要直接共用同一个目录** — val 是 YOLO 推理用 jpg+txt 对，校准集只要 jpg 不要 txt
- 校准集**最简单的做法**：`cp dataset/images/train/*.jpg calibration_data/`（随机抽 30 张也行）
- 实测：训练集 32 张 + 验证集 8 张 + 校准集 32 张全程跑通（量化 cosine sim 全 ≥ 0.99，板端检测正确），数据量少照样能 demo，但 **mAP 容易过拟合**，生产场景建议每类 ≥ 50 张训练样本

#### 1.3 data.yaml 示例

```yaml
path: /home/user/project/dataset    # ⚠️ 远端跑训练时必须绝对路径，相对路径会找不到图
train: images/train
val: images/val

names:
  0: park
  1: qrcode
  2: obstacle
```

#### 1.4 数据完整性检查（阶段 1 Checkpoint）

```bash
# 训练集和验证集 image 数 = label 数
echo "train_imgs:$(ls dataset/images/train | wc -l) train_lbls:$(ls dataset/labels/train | wc -l)"
echo "val_imgs:$(ls dataset/images/val | wc -l)   val_lbls:$(ls dataset/labels/val | wc -l)"

# 校准集只数 jpg
echo "cal_imgs:$(ls calibration_data/ | wc -l)"
```

任何一对 imgs/lbls 不匹配 → 训练会报 `WARNING: <N> missing labels`，必须修；val 全空白会 mAP=0。

### 阶段 2：训练
```bash
yolo detect train model=yolo11n.pt data=dataset.yaml epochs=100 imgsz=640 batch=16 device=0
# 自定义分辨率：imgsz=1280（必须 32 倍数）
```

**SSH 远程训练（推荐做法）**：
1. 本地 Write 一个 `run_train.sh`（含 conda activate + yolo 命令）
2. 远端 tmux 启动后台跑：
```bash
ssh user@gpu 'bash -s' << 'OUTER'
cat > /tmp/run_train.sh << 'INNER'
#!/bin/bash
source ~/miniconda3/etc/profile.d/conda.sh
conda activate rdk_env
cd "$HOME/yolo_ws"
yolo detect train model=yolo11s.pt data=dataset/data.yaml epochs=100 imgsz=640 batch=16 device=0 project=runs name=yolov11s_park exist_ok=True 2>&1 | tee train.log
INNER
chmod +x /tmp/run_train.sh
tmux new -d -s yolo_train "/tmp/run_train.sh"
OUTER
# 后续监控：ssh user@gpu 'tail -50 "$HOME/yolo_ws/train.log"'
```

⚠️ 不要把 `yolo` 整条长命令塞进 `tmux new -d -s X "yolo train ..."` 字符串里 — 引号嵌套加 ssh 转义会出 typo（实测：`dataset/data.yaml` 被吞成 `datasetta.yaml`）。

### 阶段 3：ONNX + 量化
```bash
# ONNX 导出（注意参数：ultralytics_yolo 用 --pt，YOLO26 用 --weights）
python3 export_monkey_patch.py --pt best.pt              # ultralytics_yolo
python3 export_yolo26_detect_bpu.py --weights best.pt    # YOLO26

# 量化 — mapper.py 自动生成 config.yaml 并调用 hb_mapper makertbin
#   --cal-sample-num 实际能用的不超过 cal-images 实际张数
#   --quantized int8（默认）/ int16（追加 set_all_nodes_int16，精度更高但 bin 更大）
python3 mapper.py --onnx best.onnx --cal-images ./calibration_data \
  --cal-sample-num 50 --optimize-level O3 --output-dir .
```

**ONNX 导出验证**（Detect 头被替换成 BPU 友好版的标志）：
```
[Cauchy] Replaced Detect_forward in 23
[Cauchy] Replaced Attention_forward in attn   # YOLOv11 的 C2PSA 模块
output shape: ((1,80,80,3), (1,80,80,64), (1,40,40,3), ...)  # NHWC + 6 输出
```

**量化耗时基准**（实测 RTX 3060 Laptop / Ryzen 7 5800H WSL2）：
- ONNX 导出：~1-2 秒
- hb_mapper makertbin O3 + 32 张校准：**~24 分钟**（无 GPU 加速，纯 CPU）
- 输出：`<onnx_basename>_bayese_640x640_nv12.bin`，YOLOv11s = 9.9MB

**量化精度合格线**：
- 官方红线（`quantize_compile.rst.txt`）：output cosine ≥ **0.8**（低于则 "significant loss"）
- 生产经验（本 skill 实测 YOLOv11s）：output cosine ≥ **0.99** 优秀；0.8~0.99 区间必须跑 `quantized_model.onnx` 做精度对比；**绝对**不能只看 cosine 判断模型可用，最终要看 mAP/recall

### 阶段 4：板端 Python（板端 SSH 档位下 Agent 自动跑）

> 注：下面所有 `/home/root/` 路径都假设以 root 登录板端（RDK X5 出厂默认 root@<IP>）。如果用普通用户 `sunrise@<IP>`，路径替换为 `/home/sunrise/`。

**目录结构要保持 rdk_model_zoo 的 5 层深度**（`main.py` 里 `sys.path.append("../../../../../")`），否则 `import utils.py_utils` 会失败：
```
/home/root/inference/rdk_model_zoo/
├── samples/vision/ultralytics_yolo/
│   ├── runtime/python/         # main.py + ultralytics_yolo_det.py etc
│   ├── model/                  # *.bin 放这里
│   └── test_data/              # 测试图 + custom_classes.names
└── utils/py_utils/             # ⚠️ 必传，main.py 相对路径导入
```

```bash
# 1) 建目录（保留 rdk_model_zoo 命名）
ssh root@<IP> 'mkdir -p /home/root/inference/rdk_model_zoo/samples/vision/ultralytics_yolo/{runtime/python,model,test_data} /home/root/inference/rdk_model_zoo/utils'

# 2) 传文件（注意 scp 多源不可靠，逐个传或用 -r 整目录）
scp -r rdk_model_zoo/samples/vision/ultralytics_yolo/runtime/python/. root@<IP>:/home/root/inference/rdk_model_zoo/samples/vision/ultralytics_yolo/runtime/python/
scp -r rdk_model_zoo/utils/. root@<IP>:/home/root/inference/rdk_model_zoo/utils/
scp best_bayese_640x640_nv12.bin root@<IP>:/home/root/inference/rdk_model_zoo/samples/vision/ultralytics_yolo/model/
scp test.jpg root@<IP>:/home/root/inference/rdk_model_zoo/samples/vision/ultralytics_yolo/test_data/
scp custom_classes.names root@<IP>:/home/root/inference/rdk_model_zoo/samples/vision/ultralytics_yolo/test_data/

# 3) 推理（cwd 必须是 runtime/python，路径用相对）
ssh root@<IP> '
cd /home/root/inference/rdk_model_zoo/samples/vision/ultralytics_yolo/runtime/python && \
python3 main.py \
  --task detect \
  --model-path ../../model/best_bayese_640x640_nv12.bin \
  --test-img ../../test_data/test.jpg \
  --label-file ../../test_data/custom_classes.names \
  --img-save-path ../../test_data/result.jpg \
  --classes-num 3 \
  --reg 16 \
  --strides 8,16,32 \
  --score-thres 0.25 \
  --nms-thres 0.7'

# 4) 拉回结果验证
scp root@<IP>:/home/root/inference/rdk_model_zoo/samples/vision/ultralytics_yolo/test_data/result.jpg ./
```

**实测性能基线**（YOLOv11s @ 640，RDK X5）：
- Load Model: 310~345 ms（一次性）
- Pre-process (letterbox + BGR→NV12): 7~50 ms
- **Forward (BPU): 18~22 ms** ✅
- Post-process: 4~10 ms
- 单帧端到端：~35-90 ms

### 阶段 5：TROS HobotDnn ROS2（板端 SSH 档位下 Agent 自动跑）

#### 5.1 配置文件（本地生成 → scp 到板端 `/home/root/hobot_ws/config/`）

`custom_workconfig.json`：
```json
{
  "model_file": "config/best_bayese_640x640_nv12.bin",
  "task_num": 4,
  "dnn_Parser": "ultralytics_yolo",
  "model_output_count": 6,
  "reg_max": 16,
  "class_num": 3,
  "cls_names_list": "config/custom.list",
  "strides": [8, 16, 32],
  "score_threshold": 0.25,
  "nms_threshold": 0.7,
  "nms_top_k": 300,
  "output_order": [0, 1, 2, 3, 4, 5]
}
```
（YOLO26 改 `"reg_max": 1`）

⚠️ **不要照抄 `/opt/tros/humble/lib/dnn_node_example/config/yolov11workconfig.json`** — 官方默认 `"dnn_Parser": "yolov8"` 是给厂内 modified 模型用的，**用户自己量化的模型必须改 `"ultralytics_yolo"`** 否则全错检。

`custom.list`（行数必须等于 `class_num`）：
```
park
qrcode
obstacle
```

#### 5.2 三种验证模式（按推荐顺序）

| 模式 | 输入源 | 用途 | hbmem topic | 优先级 |
|---|---|---|---|---|
| **A1** | USB 摄像头 (`hobot_usb_cam`) | **生产首选**，真实视频流 | `/hbmem_img` ✅ 默认对齐 | ⭐⭐⭐ |
| **A2** | MIPI 摄像头 (`mipi_cam`) | 生产首选（板载相机） | `/hbmem_img` ✅ 默认对齐 | ⭐⭐⭐ |
| **B**  | `hobot_image_publisher` 循环图 | **没摄像头时的 backup** | 默认 `/test_msg` ⚠️ 要改名 | ⭐⭐ |
| **C**  | `feed_type=0` 单图回灌 | **最快调试**，验证 bin + parser | 不走话题 | ⭐ |

**选型决策**：
- 上摄像头 → **A1/A2**（生产真实场景）
- 没摄像头但要验证 ROS2 全链路 → **B**
- 只想看 bin 模型对不对 → **C**（最简单，跳过整个 publisher）

---

##### 模式 A1：USB 摄像头链路（hobot_usb_cam）

```bash
# 后台 1: 启动 USB 摄像头节点（默认发到 /hbmem_img，与 dnn_node 默认订阅完美对齐）
nohup ros2 launch hobot_usb_cam hobot_usb_cam.launch.py \
  usb_video_device:=/dev/video8 \
  usb_image_width:=640 usb_image_height:=480 \
  usb_pixel_format:=mjpeg \
  usb_framerate:=30 \
  usb_zero_copy:=True > usb_cam.log 2>&1 &

# 后台 2: dnn_node（无需任何 topic remap，默认订阅 /hbmem_img）
nohup bash -c "cd /home/root/hobot_ws && \
  ros2 run dnn_node_example example --ros-args \
    -p feed_type:=1 -p is_shared_mem_sub:=1 \
    -p config_file:=config/custom_workconfig.json" > dnn.log 2>&1 &

# 验证
ros2 topic hz /hobot_dnn_detection         # 期望 ~ 30 Hz（瓶颈是 BPU 推理 ~15ms）
ros2 topic echo --once /hobot_dnn_detection
```

**USB 关键参数**：
- `usb_video_device`：默认 `/dev/video8`，**不一定准**！先 `ls /dev/video*` 看实际节点（常见是 `/dev/video0`）
- `usb_pixel_format`：`mjpeg`（推荐，带宽小）/ `yuyv` / `uyvy`，看摄像头硬件支持
- `usb_zero_copy:=True`：生产用 True 走 hbmem，False 会走 ROS2 普通 transport（CPU 拷贝多）

##### 模式 A2：MIPI 摄像头链路（mipi_cam）

```bash
# 板端常见 sensor: F37 / GC4663 / IMX415 / OV5647
nohup ros2 launch mipi_cam mipi_cam_640x480_nv12_hbmem.launch.py \
  mipi_video_device:=F37 > mipi_cam.log 2>&1 &
# 或 1920x1080: ros2 launch mipi_cam mipi_cam_1920x1080_nv12_hbmem.launch.py

# dnn_node（同 A1，无需改话题）
nohup bash -c "cd /home/root/hobot_ws && \
  ros2 run dnn_node_example example --ros-args \
    -p feed_type:=1 -p is_shared_mem_sub:=1 \
    -p config_file:=config/custom_workconfig.json" > dnn.log 2>&1 &

ros2 topic hz /hobot_dnn_detection
```

**MIPI 关键参数**：
- `mipi_video_device`：sensor 型号字符串。常见 `F37`, `GC4663`, `IMX415`, `OV5647`, `OV13855`。**型号错了节点直接 die**（`cap capture init failure`）
- `mipi_out_format`：`nv12`（BPU 直吃，最优）/ `bgr8`
- `mipi_io_method`：`shared_mem`（hbmem 零拷贝，强烈推荐）/ `ros`
- 不知道 sensor 型号：看板载贴标，或 `dmesg | grep -i sensor`

##### 模式 B：image_publisher 循环图片（无摄像头 backup）

```bash
# 后台 1：图像源 → /hbmem_img（10 fps 循环）⚠️ 必须显式 publish_message_topic_name:=/hbmem_img
nohup ros2 launch hobot_image_publisher hobot_image_publisher.launch.py \
  publish_image_source:=/home/root/hobot_ws/config/test.jpg \
  publish_image_format:=jpg \
  publish_source_image_w:=640 publish_source_image_h:=480 \
  publish_fps:=10 publish_is_loop:=True \
  publish_message_topic_name:=/hbmem_img \
  publish_is_shared_mem:=True > pub.log 2>&1 &

# 后台 2：dnn_node（同 A1）
nohup bash -c "cd /home/root/hobot_ws && \
  ros2 run dnn_node_example example --ros-args \
    -p feed_type:=1 -p is_shared_mem_sub:=1 \
    -p config_file:=config/custom_workconfig.json" > dnn.log 2>&1 &

ros2 topic hz /hobot_dnn_detection           # 期望 ≈ publisher fps (10 Hz)
ros2 topic echo --once /hobot_dnn_detection
```

⚠️ image_publisher 默认 `msg_pub_topic_name` 是 `/test_msg`（不是 `/hbmem_img`），**必须显式改名**才能和 dnn_node 默认订阅对接。摄像头模式 A 没这问题（cam 节点本身就发 `/hbmem_img`）。

##### 模式 C：feed_type=0 单图回灌（最快调试）

```bash
ssh root@<IP> '
source /opt/tros/humble/setup.bash && cd /home/root/hobot_ws && \
ros2 run dnn_node_example example --ros-args \
  -p feed_type:=0 \
  -p config_file:=config/custom_workconfig.json \
  -p image:=config/test.jpg \
  -p image_type:=0 \
  -p dump_render_img:=1'
# 输出渲染文件：render_feedback_0_0.jpeg （不是 result.jpg）
# 不需要起 publisher，节点跑完一张图就停，最适合验证 bin/parser 配置
```

##### 通用注意事项（所有模式）

⚠️ **板端默认没 tmux**，用 `nohup ... > log 2>&1 &` 跑后台节点；清理用：
```bash
pkill -f hobot_usb_cam                # USB cam
pkill -f mipi_cam                     # MIPI cam
pkill -f hobot_image_pub              # image_publisher
pkill -f "dnn_node_example/example"   # dnn_node
```

⚠️ **`/dev/hbmem*` 设备权限**：默认 root 才能写 hbmem。非 root 用户需 `sudo chmod 666 /dev/hbmem*` 或加入对应 group。

⚠️ **topic 名对齐总览**：
| 输入源节点 | hbmem 默认 topic | 需改名? |
|---|---|---|
| `hobot_usb_cam` | `/hbmem_img` | ❌ 默认对齐 |
| `mipi_cam` (默认 launch) | `/hbmem_img` | ❌ 默认对齐 |
| `hobot_image_publisher` | `/test_msg` | ✅ 必须改 |
| `dnn_node_example` 订阅端 | `/hbmem_img` | — |

#### 5.3 真实性能基准（实测）

YOLOv11s + 自定义 3 类 + 640x640 + RDK X5（OS 3.5.0-beta / dnn_node 2.6.1 / hbmem 零拷贝）：

| Pipeline 阶段 | 耗时/帧 |
|---|---|
| recv image (hbmem 零拷贝) | 9 ms |
| preprocess (resize → NV12) | 2 ms |
| **BPU infer** | **15 ms** |
| postprocess (NMS + 反量化) | 1 ms |
| **TOTAL pipeline** | **29 ms** |
| **实测帧率** | **9.95 Hz**（publisher fps=10 满吃）|

消息类型：`ai_msgs/msg/PerceptionTargets`（含 rect、type、confidence、track_id），下游可订阅做决策。

---

## Checkpoint

| 阶段 | 验证 | 标准 |
|------|------|------|
| 板端预检 | `cat /etc/version` + dnn_node 版本 + `/dev/bpu*` | OS ≥ 3.5.0，dnn_node ≥ 2.6.1，BPU 设备存在 |
| 0 环境 | `hb_mapper --version` + `python -c "import pkg_resources"` | 1.24.x，且 setuptools 已装 |
| 1 数据 | 标签数 = 图像数；data.yaml 用绝对 path | 通过 |
| 2 训练 | `yolo val` mAP50 + `~/.config/Ultralytics/Arial.ttf` 占位存在 | mAP50 > 0.7 |
| 3 量化 | hb_mapper 日志 cosine sim + `*_bayese_640x640_nv12.bin` | 官方红线 cosine ≥ 0.8；生产经验 ≥ 0.99 优秀 |
| 4 板端推理 | Python main.py 推理结果图 | 无报错，**Forward < 30ms**，框正确 |
| 5A 单图回灌 | `dump_render_img:=1` 输出 `render_feedback_0_0.jpeg` | 类别正确 |
| 5B ROS2 流 | `ros2 topic hz /hobot_dnn_detection` + `topic echo --once` | hz ≈ publisher fps，targets 非空 |

---

## 常见问题
- `import hbm_runtime` 失败 → 镜像 < 3.5.0
- 量化时 `ModuleNotFoundError: No module named 'pkg_resources'` → `pip install setuptools`（rdkx5-yolo-mapper 漏依赖）
- `CondaToSNonInteractiveError` → conda 26+ 必须先 `conda tos accept --override-channels --channel <repo>`
- pip 装 ultralytics/torch 一直 timeout → 国内换清华源 + `--timeout 60 --retries 10`
- `yolo train` 卡在 `Download failure ... Arial.ttf` → 先 `cp /usr/share/fonts/truetype/dejavu/DejaVuSans.ttf ~/.config/Ultralytics/Arial.ttf`
- 训练命令 `dataset/data.yaml` 莫名其妙变成 `datasetta.yaml` → ssh 引号嵌套吞字符，**改用 `ssh ... 'bash -s' < script.sh`**
- `source /opt/tros/setup.bash` 找不到 → 用 `/opt/tros/humble/setup.bash`
- `unsupported parser: ultralytics_yolo` → dnn_node < 2.6.1
- `unsupported parser: yolo26_seg` → dnn_node < 2.6.2
- HobotDnn 检测全错 → 用 `"ultralytics_yolo"`，**不要用 `"yolov8"`**（官方 yolov11workconfig.json 默认错的，要改）
- `ImportError: utils` → utils/ 目录未传，或目录深度不对（必须 5 层）
- 自定义分辨率推理错位 → 必须 H=W 且能被 32 整除
- SSH 断开训练中断 → 必须用 tmux/nohup
- 板端没 tmux → `apt install tmux` 或直接 `nohup ... > log 2>&1 &`
- `class_names length X is not equal to class_num Y` → cls_names_list 行数 ≠ class_num
- topic list 都有 `/hbmem_img` 和 `/hobot_dnn_detection` 但 `topic hz` 没输出 → publisher 和 dnn_node 的话题名没对齐（默认一个 `/test_msg` 一个 `/hbmem_img`）
- `scp src1 src2 host:dst` 报 `No such file or directory` → 新 OpenSSH（≥ 9.0）行为变了，逐个 scp 或 `scp -r`
- WSL2 找不到 `nvidia-smi` → 它在 `/usr/lib/wsl/lib/nvidia-smi`，加进 PATH 即可

---

## 参考
- 官方 YOLO ROS 文档: https://developer.d-robotics.cc/rdk_doc/Robot_development/boxs/detection/yolo
- 官方 RDK X5 工具链手册（v1.2.6）: https://developer.d-robotics.cc/api/v1/fileData/x5_doc-v126cn/index.html
- 官方 RDK X5 hbm_runtime Python API: https://developer.d-robotics.cc/rdk_x_doc/Basic_Application/multi_media_sp_dev_api/RDK_X5/pydev_multimedia_api_x5/ai-python-api
- ultralytics_yolo sample: https://github.com/D-Robotics/rdk_model_zoo/tree/rdk_x5/samples/vision/ultralytics_yolo
- ultralytics_yolo26 sample: https://github.com/D-Robotics/rdk_model_zoo/tree/rdk_x5/samples/vision/ultralytics_yolo26
- HobotDnn CHANGELOG: https://github.com/D-Robotics/hobot_dnn/blob/develop/dnn_node/CHANGELOG.md

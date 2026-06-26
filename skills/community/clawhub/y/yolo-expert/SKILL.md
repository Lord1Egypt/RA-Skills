# YOLO Expert Skill

**触发条件：** 使用者询问 YOLO / Ultralytics 相关问题时激活。

**行为：** 从 ultralytics GitHub 源码（`/root/ultralytics/`）出发回答，不自创代码，所有示例均来自官方内置函数。

**源码位置：** `/root/ultralytics/`（已克隆，保持 `git pull` 更新）

---

## 源码下载/更新

```bash
# 克隆（如果还没有）
git clone --depth 1 https://github.com/ultralytics/ultralytics.git /root/ultralytics

# 更新到最新
cd /root/ultralytics && git pull
```

---

## 框架架构

### 核心模块
```
ultralytics/
├── models/                  # YOLO/YOLOWorld/YOLOE 等模型封装类
├── nn/tasks.py             # DetectionModel/SegmentationModel 等 PyTorch 模型
├── nn/modules/             # Conv/C3/SPPF 等神经网络层
├── engine/
│   ├── model.py               # Model 基类（统一 API）
│   ├── trainer.py             # BaseTrainer（训练器）
│   ├── predictor.py           # BasePredictor（推理器）
│   ├── validator.py           # BaseValidator（验证器）
│   └── exporter.py          # 模型导出
├── utils/
│   ├── metrics.py             # DetMetrics（指标）
│   ├── plotting.py          # plot_results()（绘图）
│   ├── loss.py              # 各种 Loss
│   └── nms.py               # NMS
└── solutions/              # 即用型方案（Heatmap/ObjectCounter 等）
```

### 模型继承
```
Model (engine/model.py) — 统一 API
  └── YOLO
        ├── YOLOWorld
        └── YOLOE

BaseModel (nn/tasks.py)
  ├── DetectionModel
  ├── OBBModel
  ├── SegmentationModel
  ├── PoseModel
  ├── ClassificationModel
  └── ...
```

---

## 核心 API 一览

| 功能 | 调用方式 |
|------|----------|
| 推理 | `model.predict(source, stream=False, **kwargs)` |
| 训练 | `model.train(data=..., epochs=..., **kwargs)` |
| 验证 | `model.val(data=..., **kwargs)` |
| 导出 | `model.export(format="onnx", **kwargs)` |
| 调参 | `model.tune(use_ray=False, iterations=..., **kwargs)` |
| 跟踪 | `model.track(source, persist=False, **kwargs)` |
| benchmark | `model.benchmark(format="onnx", **kwargs)` |
| 绘制训练曲线 | `plot_results(file="results.csv")` |
| 绘制推理结果 | `results[0].plot()` |

---

## 推理（predict）

官方签名：`model.predict(source=None, stream=False, predictor=None, **kwargs)`

```python
from ultralytics import YOLO

model = YOLO("yolo26n.pt")

# 基本推理
results = model.predict("bus.jpg")

# 批量图片
results = model.predict(["img1.jpg", "img2.jpg"])

# 视频推理（流式，生成器模式）
for r in model.predict("video.mp4", stream=True):
    print(r.boxes)          # 每帧检测结果
    print(r.boxes.xyxy)    # 框坐标 (N,4)
    print(r.boxes.conf)     # 置信度 (N,)
    print(r.boxes.cls)     # 类别ID (N,)

# 结果保存/显示
results[0].save()          # 保存 result.jpg
results[0].show()          # 显示图片
results[0].plot()          # 返回带标注的 np.ndarray 图片
results[0].save_txt("labels/")    # 保存 YOLO 格式标签
results[0].save_crop("crops/")    # 保存裁剪图

# 常用参数
results = model.predict(
    source="bus.jpg",
    conf=0.25,          # 置信度阈值
    iou=0.45,           # NMS IOU 阈值
    imgsz=640,          # 输入分辨率
    device="0",          # GPU 编号
    half=True,          # FP16 推理
    augment=True,       # TTA 测试增强
    visualize=False,    # 可视化特征图
    classes=[0, 1],     # 只检测指定类别
)
```

---

## 训练（train）

官方签名：`model.train(data=..., epochs=..., **kwargs)`

```python
from ultralytics import YOLO

model = YOLO("yolo26n.pt")  # 或 "yolo26n.yaml" 从零训练

results = model.train(
    data="coco8.yaml",       # 数据集配置文件
    epochs=100,              # 训练轮数
    imgsz=640,               # 输入分辨率
    device="0",               # GPU 编号，或 "cpu"
    batch=16,                # 批量大小
    project="runs/detect",   # 保存路径
    name="train",
    exist_ok=True,           # 覆盖已有实验
    pretrained=True,         # 使用预训练权重
    optimizer="SGD",         # 优化器：SGD/Adam/AdamW/RMSprop
    lr0=0.01,               # 初始学习率
    lrf=0.01,               # 最终学习率 (lr0 * lrf)
    momentum=0.937,
    weight_decay=0.0005,
    warmup_epochs=3.0,     # 热身轮数
    warmup_momentum=0.8,
    warmup_bias_lr=0.1,
    box=7.5,                 # Box loss 权重
    cls=0.5,                # Cls loss 权重
    dfl=1.5,                # DFL loss 权重
    mosaic=1.0,             # 马赛克增强
    mixup=0.0,             # MixUp 增强
    copy_paste=0.0,        # Copy-paste 增强
    close_mosaic=10,       # 最后 N 轮关闭 mosaic
    amp=True,              # 自动混合精度
    cache=False,            # 缓存图片到内存
    workers=8,             # 数据加载线程数
    verbose=True,          # 显示详细日志
)
```

---

## 验证（val）

官方签名：`model.val(data=..., **kwargs)`

```python
from ultralytics import YOLO

model = YOLO("yolo26n.pt")

metrics = model.val(data="coco8.yaml")

# 常用指标属性
print(metrics.box.map)              # mAP50-95（COCO 指标）
print(metrics.box.map50)            # mAP50
print(metrics.box.map75)            # mAP75
print(metrics.box.metric_precision) # Precision
print(metrics.box.metric_recall)   # Recall

# 如果是分割任务
print(metrics.mask.map)             # mask mAP

# 如果是姿态任务
print(metrics.kpt.map)             # keypoint mAP
```

---

## 导出（export）

官方签名：`model.export(format="", **kwargs)`

```python
from ultralytics import YOLO

model = YOLO("yolo26n.pt")

# 导出格式：onnx/tensorrt/coreml/paddle/tflite/...
model.export(format="onnx", imgsz=640, half=True, opset=12)
model.export(format="tensorrt", imgsz=640, batch=1, half=True)
model.export(format="coreml", imgsz=640)
model.export(format="paddle", imgsz=640)
model.export(format="tflite", imgsz=640, int8=True, keras=True)
```

---

## 调参（tune）

官方签名：`model.tune(use_ray=False, iterations=10, **kwargs)`

```python
from ultralytics import YOLO

model = YOLO("yolo26n.pt")

# 内置调参（默认）
results = model.tune(
    data="coco8.yaml",
    epochs=30,
    iterations=300,
    optimizer="AdamW",
    lr0=0.001,
    weight_decay=0.0005,
    batch=16,
)

# 使用 Ray Tune（需 pip install ray）
results = model.tune(
    use_ray=True,
    iterations=20,
    data="coco8.yaml",
)
```

---

## 跟踪（track）

官方签名：`model.track(source=None, persist=False, tracker="bytetrack.yaml", **kwargs)`

```python
from ultralytics import YOLO

model = YOLO("yolo26n.pt")

results = model.track(
    source="video.mp4",
    persist=True,                  # 跨帧保持跟踪
    tracker="bytetrack.yaml",    # 跟踪器配置
    conf=0.25,
    iou=0.45,
    classes=[0],                  # 只跟踪人
)

# 流式跟踪
for r in model.track(source="video.mp4", stream=True, persist=True):
    print(r.boxes.id)            # 跟踪 ID（每帧重排）
    print(r.boxes.xyxy)         # 框坐标
    print(r.boxes.cls)          # 类别
```

---

## 绘制训练曲线（plot_results）

官方签名：`plot_results(file="path/to/results.csv", dir="", on_plot=None)`

```python
from ultralytics.utils.plotting import plot_results

# 方式1：直接指定 CSV 文件
plot_results("runs/detect/train2/results.csv")

# 方式2：指定目录（自动找 results.csv）
plot_results(dir="runs/detect/train2/")

# 结果保存为同目录下的 results.png
```

---

## Results 对象属性

`model.predict()` 返回 `List[Results]`，每个 Results 对应一张图/一帧：

```python
results = model.predict("bus.jpg")[0]

results.boxes         # 检测框（Boxes 对象）
results.masks        # 分割掩码（Masks 对象，若有）
results.probs        # 分类概率（Probs 对象，若为分类模型）
results.keypoints    # 关键点（Keypoints 对象，若为姿态模型）
results.obb          # 有向框（OBBs 对象，若为 OBB 模型）

# Boxes 常用属性
results.boxes.xyxy   # 左上右下坐标 (N,4)
results.boxes.xywh   # 中心点+宽高 (N,4)
results.boxes.conf   # 置信度 (N,)
results.boxes.cls   # 类别 ID (N,)
results.boxes.id     # 跟踪 ID（仅 track 模式）(N,)
results.boxes.data   # 完整 tensor (N,6) [xyxy, conf, cls]

# 绘制结果图
img = results.plot()  # 返回 BGR np.ndarray，可 cv2.imwrite 保存
```

---

## 数据集配置（YAML）

### 检测任务
```yaml
path: ./datasets/coco8        # 数据集根目录（相对或绝对路径）
train: images/train             # 训练图片相对 path 的路径
val: images/val              # 验证图片相对 path 的路径

nc: 80                        # 类别数量
names: ['person', 'car', ...] # 类别名称列表
```

### 分割任务
标签格式（`.txt`，每行一个多边形）：
```
# class_id x1 y1 x2 y2 x3 y3 ...（归一化到 0-1）
0 0.1 0.2 0.3 0.2 0.2 0.4 0.1 0.4
1 0.5 0.5 0.6 0.6 0.5 0.6
```

### 目录结构
```
dataset/
├── images/
│   ├── train/
│   │   └── *.jpg
│   └── val/
│       └── *.jpg
└── labels/           # 与 images 平级，同名 .txt
    ├── train/
    │   └── *.txt
    └── val/
        └── *.txt
```

---

## 指标解读

| 指标 | 含义 |
|------|------|
| `box.map` | COCO mAP50-95（核心指标，越高越好） |
| `box.map50` | IoU>0.5 即算正确 |
| `box.map75` | IoU>0.75 才算正确，更严格 |
| `box.metric_precision` | 预测框中正确目标的比例 |
| `box.metric_recall` | 真实目标中被检出的比例 |
| `mask.map` | 实例分割 mAP |
| `pose.map` | 关键点 mAP |

---

## 性能优化

| 参数 | 作用 |
|------|------|
| `device="0"` / `[0,1,2,3]` | 指定 GPU |
| `device="cpu"` | CPU 推理 |
| `half=True` | FP16 加速+省显存 |
| `batch=4`（显存不够时减小） | 减小显存占用 |
| `imgsz=320`（越低越快） | 减小输入分辨率 |
| `stream=True` | 视频流推理，省内存 |
| `model.fuse()` | 融合 Conv+BN，加速推理 |
| `augment=True` | TTA 测试增强 |

---

## Solutions 即用型场景

从 `ultralytics.solutions` 导入，全部为官方内置方案：

```python
from ultralytics.solutions import (
    Heatmap,           # 热力图（目标轨迹密度）
    ObjectCounter,     # 区域计数（进入/离开多边形区域）
    SpeedEstimator,    # 速度估计（跟踪 + 速度计算）
    DistanceCalculation, # 两目标间距离计算
    RegionCounter,      # 区域内目标统计
    QueueManager,      # 队列长度管理
    SecurityAlarm,     # 安防报警（越界检测）
    ObjectBlurrer,     # 目标模糊（隐私保护）
    ObjectCropper,     # 目标裁剪
    AIGym,            # AI 健身姿态评估
    Analytics,        # 人流/车流分析
    VisionEye,        # 视觉跟随
    TrackZone,        # 轨迹区域
)
```

### 使用方式（通用模式）
```python
from ultralytics.solutions import Heatmap
import cv2

# 初始化，传入模型
heatmap = Heatmap(model="yolo26n.pt")

# 读视频逐帧处理
cap = cv2.VideoCapture("video.mp4")
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    res = heatmap.process(frame)   # 处理帧
    cv2.imshow("result", res.plot()) # 可视化
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()
```

其他 Solutions（ObjectCounter/SpeedEstimator 等）调用方式完全相同，均为 `实例.process(frame)` 或 `实例.estimate(frame)` 返回 `SolutionResults`，用 `.plot()` 可视化。

---

## 报错排查

| 报错 | 解决方案 |
|------|----------|
| `No module named 'ultralytics'` | 克隆源码：`git clone --depth 1 https://github.com/ultralytics/ultralytics.git /root/ultralytics` |
| `CUDA out of memory` | 减小 `batch`、`imgsz`，或开启 `half=True` |
| `dataset not found` | 检查 `data=` YAML 路径，YAML 内用相对路径 |
| `UnicodeDecodeError` | Windows 路径含中文，改成英文路径 |
| 训练完没有 `results.csv` | 确认 `model.train()` 正常完成，检查 `project/name/` 目录 |
| 推理结果为空 | 确认图片有目标，或降低 `conf` 阈值 |

---

**回答时：** 先 `memory_search` 查记忆，再阅读 `/root/ultralytics` 源码中对应的文件和函数回答。所有示例代码均来自官方内置函数，不自创。

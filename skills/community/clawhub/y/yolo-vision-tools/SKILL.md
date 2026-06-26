---
name: yolo-vision-tools
description: Use Ultralytics YOLO to perform computer vision tasks, such as detecting people or objects in images and videos, classifying images, estimating human poses, and tracking cars, people, or animals in videos.
argument-hint: |
  Use this tool when the user asks to analyze images or videos using YOLO computer vision models (YOLO26, YOLO11, etc.).

  ## Supported Tasks & Trigger Keywords

  ### 1. Object Detection (目标检测)
  **English Triggers:**
  - detect objects in this image/video
  - what objects are in this picture/video
  - find [object] in this image/video
  - identify objects in the photo
  - locate objects in the image
  - show me what's in this picture
  - analyze this image for objects
  - object detection on this video
  - yolo detection on this image
  - run yolo on this picture
  
  **中文触发词:**
  - 检测图片/视频中的物体
  - 图片/视频里有什么东西
  - 找到图片中的[物体]
  - 识别图片中的物体
  - 定位图片中的物体
  - 显示图片中的内容
  - 分析图片中的物体
  - 对视频进行目标检测
  - 用yolo检测这张图片
  - 运行yolo分析图片

  ### 2. Instance Segmentation (实例分割)
  **English Triggers:**
  - segment objects in this image
  - extract object masks
  - highlight object contours
  - separate objects from background
  - instance segmentation
  - object segmentation
  - mask detection
  - pixel-level segmentation
  
  **中文触发词:**
  - 分割图片中的物体
  - 提取物体掩码
  - 标出物体轮廓
  - 将物体从背景分离
  - 实例分割
  - 物体分割
  - 掩码检测
  - 像素级分割

  ### 3. Image Classification (图像分类)
  **English Triggers:**
  - classify this image
  - what category is this image
  - recognize image type
  - determine image label
  - image classification
  - categorize this picture
  
  **中文触发词:**
  - 对图片进行分类
  - 图片属于哪一类
  - 识别图片类型
  - 确定图片标签
  - 图像分类
  - 分类这张图片

  ### 4. Pose Estimation (姿态估计)
  **English Triggers:**
  - detect human poses
  - find skeleton/keypoints
  - recognize body posture
  - analyze human movements
  - pose estimation
  - body pose detection
  - human keypoints
  
  **中文触发词:**
  - 检测人体姿态
  - 找出人体骨架/关键点
  - 识别身体姿势
  - 分析人物动作
  - 姿态估计
  - 人体姿态检测
  - 人体关键点

  ### 5. Object Tracking (物体跟踪)
  **English Triggers:**
  - track objects in this video
  - follow movement of objects
  - monitor object trajectories
  - track multiple objects
  - video object tracking
  - follow cars/people/animals
  
  **中文触发词:**
  - 跟踪视频中的物体
  - 追踪物体移动
  - 监测物体轨迹
  - 跟踪多个物体
  - 视频物体跟踪
  - 追踪汽车/行人/动物

  ### 6. Model & Environment (模型与环境)
  **English Triggers:**
  - install yolo
  - setup yolo environment
  - check yolo installation
  - which yolo model to use
  - compare yolo models
  - yolo model selection
  - troubleshoot yolo
  
  **中文触发词:**
  - 安装yolo
  - 设置yolo环境
  - 检查yolo安装
  - 使用哪个yolo模型
  - 比较yolo模型
  - yolo模型选择
  - yolo故障排除

  ### 7. Specific Model Requests (特定模型请求)
  **English Triggers:**
  - use yolo26/yolo11/yolov8
  - run yolo26 on this
  - yolo11 detection
  - latest yolo model
  - yolo nano/small/medium/large
  
  **中文触发词:**
  - 使用yolo26/yolo11/yolov8
  - 用yolo26运行
  - yolo11检测
  - 最新yolo模型
  - yolo nano/small/medium/large版本

  ### 8. General Analysis (通用分析)
  **English Triggers:**
  - analyze this image with yolo
  - yolo vision analysis
  - computer vision analysis
  - vision ai detection
  - ai image analysis
  
  **中文触发词:**
  - 用yolo分析这张图片
  - yolo视觉分析
  - 计算机视觉分析
  - 视觉AI检测
  - AI图片分析

  ## Quick Examples:
  - "Detect objects in this image" → 触发
  - "检测这张图片中的物体" → 触发
  - "Segment the cars in this video" → 触发
  - "跟踪视频中的人体姿态" → 触发
  
---

# Ultralytics YOLO Vision Tools

Ultralytics YOLO is a state-of-the-art computer vision framework supporting multiple tasks including object detection, instance segmentation, image classification, pose estimation, and oriented bounding box detection. This skill provides comprehensive guidance for using YOLO effectively.

**Latest Model**: YOLO26 (released January 2026) features end-to-end NMS-free inference and optimized edge deployment. For stable production workloads, both YOLO26 and YOLO11 are recommended.

## Quick Start

### 1. Installation & Environment Check

```bash
# Install/update Ultralytics
pip install -U ultralytics

# Verify installation and check environment
yolo checks
```

The `yolo checks` command validates Python version, PyTorch, CUDA, GPU availability, and all dependencies. For detailed environment troubleshooting, see [Environment Check](./references/environment_check.md) or use the provided environment check script: `python scripts/check_environment.py`.

### 2. Basic Usage Examples

#### Python Interface
```python
from ultralytics import YOLO

# Load a model (YOLO automatically infers task from model)
model = YOLO("yolo26n.pt")  # or your custom model path

# Predict on various sources
# By default, outputs are saved to workspace/yolo-vision folder
results = model("image.jpg")                     # image file → saved to yolo-vision/outputs/images/
results = model("video.mp4", stream=True)        # video with streaming → saved to yolo-vision/outputs/videos/
results = model("https://example.com/image.jpg") # URL → saved to yolo-vision/outputs/images/
results = model(0, show=True)                   # webcam with display → saved to yolo-vision/outputs/videos/

# Custom output directory (optional)
results = model("image.jpg", project="/custom/path")  # save to custom directory
```

#### CLI Interface
```bash
# Basic syntax: yolo TASK MODE ARGS
# By default, outputs are saved to workspace/yolo-vision folder
yolo predict model=yolo26n.pt source="image.jpg"  # → saved to yolo-vision/runs/detect/predict/

# Task-specific examples
yolo detect predict model=yolo26n.pt source="video.mp4"  # → saved to yolo-vision/runs/detect/predict/
yolo segment predict model=yolo26n-seg.pt source="image.jpg"  # → saved to yolo-vision/runs/segment/predict/
yolo pose predict model=yolo26n-pose.pt source="image.jpg"  # → saved to yolo-vision/runs/pose/predict/

# Custom output directory (optional)
yolo predict model=yolo26n.pt source="image.jpg" project="/custom/path"  # save to custom directory
```

### 3. Model Selection

For quick start, use these default models:
- **Detection**: `yolo26n.pt` (nano), `yolo26s.pt` (small), `yolo26m.pt` (medium)
- **Segmentation**: `yolo26n-seg.pt`, `yolo26s-seg.pt`, `yolo26m-seg.pt`
- **Classification**: `yolo26n-cls.pt`, `yolo26s-cls.pt`, `yolo26m-cls.pt`
- **Pose Estimation**: `yolo26n-pose.pt`, `yolo26s-pose.pt`, `yolo26m-pose.pt`
- **Oriented Detection**: `yolo26n-obb.pt`, `yolo26s-obb.pt`, `yolo26m-obb.pt`

For complete model list and selection guidance: [Model Names](./references/model_names.md) | [Model Selection](./references/model_selection.md)

## Core Workflow

### Step 1: Understand YOLO Tasks
YOLO supports five main computer vision tasks. Choose the right task for your application:
- **Detection**: Identify and localize objects with bounding boxes
- **Segmentation**: Generate pixel-level masks for objects
- **Classification**: Categorize entire images
- **Pose Estimation**: Detect keypoints for pose analysis
- **Oriented Detection**: Detect rotated objects with angle parameter

Detailed comparison: [Task Types](./references/task_types.md)

### Step 2: Select Appropriate Model
Consider these factors when selecting a model:
- **Speed vs. Accuracy**: Nano (fastest) → X (most accurate)
- **Hardware Constraints**: GPU memory, CPU performance
- **Application Requirements**: Real-time vs. batch processing

Guidance: [Model Selection](./references/model_selection.md)

### Step 3: Configure Parameters
Common configuration parameters:
- `conf`: Confidence threshold (default: 0.25)
- `iou`: IoU threshold for NMS (default: 0.7)
- `imgsz`: Input image size (default: 640)
- `device`: Device ID (`0` for first GPU, `cpu` for CPU)
- `save`: Save results to disk
- `show`: Display results in real-time

Complete examples: [Configuration Samples](./references/configuration_samples.md)

### Step 4: Process Results
YOLO returns `Results` objects containing:
- `boxes`: Bounding boxes, confidence scores, class labels
- `masks`: Segmentation masks (for segmentation tasks)
- `keypoints`: Pose keypoints (for pose estimation)
- `probs`: Classification probabilities (for classification)
- `obb`: Oriented bounding boxes (for OBB tasks)

## Advanced Topics

### Training Custom Models
```python
from ultralytics import YOLO

# Load a model
model = YOLO("yolo26n.pt")

# Train on custom dataset
results = model.train(data="dataset.yaml", epochs=100, imgsz=640)
```

Training guide: [Training Basics](./references/training_basics.md) | [Dataset Preparation](./references/dataset_preparation.md)

### Installation Options
Multiple installation methods available:
- **pip**: `pip install -U ultralytics`
- **Conda**: `conda install -c conda-forge ultralytics`
- **Docker**: Pre-built images for GPU/CPU environments
- **From Source**: For development and customization

Detailed instructions: [Installation Guide](./references/installation_guide.md)

### Performance Optimization
- **Streaming Mode**: Use `stream=True` for videos/long sequences to reduce memory
- **Batch Processing**: Process multiple images together for efficiency
- **Hardware Acceleration**: Configure CUDA, TensorRT, or OpenVINO for optimal performance

## Reference Documentation

| Document | Description |
|----------|-------------|
| [Environment Check](./references/environment_check.md) | Comprehensive environment validation and troubleshooting |
| [Installation Guide](./references/installation_guide.md) | All installation methods (pip, Conda, Docker, source) |
| [Task Types](./references/task_types.md) | Detailed comparison of YOLO tasks and use cases |
| [Model Names](./references/model_names.md) | Complete YOLO26 model list with specifications |
| [Model Selection](./references/model_selection.md) | Strategy for choosing models based on requirements |
| [Configuration Samples](./references/configuration_samples.md) | Parameter configuration examples for various scenarios |
| [Dataset Preparation](./references/dataset_preparation.md) | Guide for preparing custom datasets for training |
| [Training Basics](./references/training_basics.md) | Fundamentals of training YOLO models on custom data |
| [Parameter Reference](./references/parameter_reference.md) | Complete reference for all YOLO configuration parameters |

## Utility Scripts

To save token usage and provide ready-to-use tools, the following Python scripts are available in the `scripts/` directory:

| Script | Description | Usage Example |
|--------|-------------|---------------|
| **check_environment.py** | Comprehensive environment diagnostics | `python scripts/check_environment.py` |
| **config_templates.py** | Ready-to-use configuration templates | `from scripts.config_templates import get_production_config` |
| **dataset_tools.py** | Dataset preparation and conversion tools | `from scripts.dataset_tools import coco_to_yolo` |
| **training_helpers.py** | Training, evaluation, and model management | `from scripts.training_helpers import evaluate_model` |
| **quick_tests.py** | Quick functionality tests | `python scripts/quick_tests.py --test environment` |
| **model_utils.py** | Model selection and validation utilities | `from scripts.model_utils import select_model` |

**Benefits of using scripts:**
- **Save tokens**: Large code blocks are extracted from documentation
- **Ready-to-use**: No need to copy-paste code from documentation
- **Modular**: Import only what you need
- **Maintainable**: Scripts can be updated independently

## Troubleshooting

### Common Issues

**Q: `yolo` command not found after installation?**
A: Try `python -m ultralytics yolo` or check Python environment PATH.

**Q: How to use specific GPU?**
A: Set `device=0` (first GPU) or `device=cpu` for CPU-only mode.

**Q: Model downloads slowly?**
A: Set `ULTRALYTICS_HOME` environment variable to control cache location.

**Q: How to filter specific classes?**
A: Use `classes` parameter: `classes=[0, 2, 5]` (class indices).

**Q: Memory issues with long videos?**
A: Use `stream=True` to process videos as generators.

**Q: Real-time webcam support?**
A: Yes, use `source=0` (default camera) with `show=True` for live display.

### Getting Help
- Run `yolo checks` to diagnose environment issues
- Check official documentation: https://docs.ultralytics.com
- Review configuration reference: https://docs.ultralytics.com/usage/cfg/

## Output Directory Convention

### Default Output Location
When processing images or videos with YOLO, if the user does not specify an output directory, all generated files will be saved to the workspace's `yolo-vision` folder.

### File Organization
The `yolo-vision` folder will be organized as follows:

```
yolo-vision/
├── inputs/            # Original input files (copied for reference)
├── outputs/           # Processed files with detection results
│   ├── images/        # Detected images
│   ├── videos/        # Detected videos  
│   └── previews/      # Preview images
├── reports/           # Analysis reports and statistics
│   ├── json/          # JSON format reports
│   ├── markdown/      # Markdown format reports
│   └── csv/           # CSV format data
├── models/            # Downloaded YOLO models
│   ├── yolo26/        # YOLO26 models
│   ├── yolo11/        # YOLO11 models
│   └── custom/        # Custom trained models
└── logs/              # Processing logs and debug information
```

### Automatic Folder Creation
The skill will automatically:
1. Create the `yolo-vision` folder if it doesn't exist
2. Create all subdirectories as needed
3. Organize files by date and task type
4. Generate timestamp-based filenames for easy tracking

### Example Usage
```python
# Without specifying output directory - uses default yolo-vision folder
results = model("image.jpg")  # Output saved to yolo-vision/outputs/images/

# With custom output directory
results = model("image.jpg", save_dir="/custom/path")  # Uses specified path
```

### Benefits
1. **Consistency**: All YOLO outputs in one predictable location
2. **Organization**: Files automatically categorized by type
3. **Backup**: Input files are preserved for reference
4. **Reproducibility**: Easy to find and compare previous analyses
5. **Clean Workspace**: Prevents clutter in the main workspace directory

### User Override
Users can still specify custom output directories when needed:
- By providing a `save_dir` parameter in Python code
- By using the `--project` flag in CLI commands
- By setting the `ULTRALYTICS_PROJECT` environment variable

---

**License Note**: Ultralytics YOLO is available under AGPL-3.0 for open source use and Enterprise License for commercial applications. Review licensing at https://ultralytics.com/license.
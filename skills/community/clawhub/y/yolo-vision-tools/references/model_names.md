# YOLO Model Names Reference

## Overview

This document lists all Ultralytics YOLO pre-trained model names, categorized by task type. These models can be loaded directly via the `YOLO()` function or CLI commands.

**Latest Models**: YOLO26 (released January 2026) is the newest generation with end-to-end NMS-free inference. For stable production workloads, both YOLO26 and YOLO11 are recommended.

## Model Naming Convention

YOLO models follow this naming pattern:
- **Version prefix**: `yolo26` (latest), `yolo11` (stable), `yolo10`, `yolov8`, etc.
- **Size identifier**: `n` (nano), `s` (small), `m` (medium), `l` (large), `x` (extra large)
- **Task suffix**: `.pt` (object detection), `-seg` (instance segmentation), `-cls` (image classification), `-pose` (pose estimation), `-obb` (oriented bounding box detection)
- **File extension**: `.pt` (PyTorch model file)

## YOLO26 Models (Latest)

### Object Detection
| Model Name | Size | Description |
|------------|------|-------------|
| `yolo26n.pt` | Nano | Fastest, smallest, ideal for mobile/edge devices |
| `yolo26s.pt` | Small | Balanced speed and accuracy, general-purpose |
| `yolo26m.pt` | Medium | Medium accuracy, server applications |
| `yolo26l.pt` | Large | High accuracy, accuracy-first scenarios |
| `yolo26x.pt` | XLarge | Highest accuracy, research/extreme requirements |

### Oriented Bounding Box Detection
| Model Name | Size | Description |
|------------|------|-------------|
| `yolo26n-obb.pt` | Nano | Rotated object detection, smallest version |
| `yolo26s-obb.pt` | Small | Rotated object detection, balanced version |
| `yolo26m-obb.pt` | Medium | Rotated object detection, medium accuracy |
| `yolo26l-obb.pt` | Large | Rotated object detection, high accuracy |
| `yolo26x-obb.pt` | XLarge | Rotated object detection, highest accuracy |

### Instance Segmentation
| Model Name | Size | Description |
|------------|------|-------------|
| `yolo26n-seg.pt` | Nano | Instance segmentation, fastest version |
| `yolo26s-seg.pt` | Small | Instance segmentation, balanced version |
| `yolo26m-seg.pt` | Medium | Instance segmentation, medium accuracy |
| `yolo26l-seg.pt` | Large | Instance segmentation, high accuracy |
| `yolo26x-seg.pt` | XLarge | Instance segmentation, highest accuracy |

### Image Classification
| Model Name | Size | Description |
|------------|------|-------------|
| `yolo26n-cls.pt` | Nano | Image classification, fastest version |
| `yolo26s-cls.pt` | Small | Image classification, balanced version |
| `yolo26m-cls.pt` | Medium | Image classification, medium accuracy |
| `yolo26l-cls.pt` | Large | Image classification, high accuracy |
| `yolo26x-cls.pt` | XLarge | Image classification, highest accuracy |

### Pose Estimation
| Model Name | Size | Description |
|------------|------|-------------|
| `yolo26n-pose.pt` | Nano | Pose estimation, fastest version |
| `yolo26s-pose.pt` | Small | Pose estimation, balanced version |
| `yolo26m-pose.pt` | Medium | Pose estimation, medium accuracy |
| `yolo26l-pose.pt` | Large | Pose estimation, high accuracy |
| `yolo26x-pose.pt` | XLarge | Pose estimation, highest accuracy |

## YOLO11 Models (Stable Production)

YOLO11 provides excellent performance across all tasks and is recommended for production environments.

| Task | Nano | Small | Medium | Large | XLarge |
|------|------|-------|--------|-------|--------|
| Detection | `yolo11n.pt` | `yolo11s.pt` | `yolo11m.pt` | `yolo11l.pt` | `yolo11x.pt` |
| Segmentation | `yolo11n-seg.pt` | `yolo11s-seg.pt` | `yolo11m-seg.pt` | `yolo11l-seg.pt` | `yolo11x-seg.pt` |
| Classification | `yolo11n-cls.pt` | `yolo11s-cls.pt` | `yolo11m-cls.pt` | `yolo11l-cls.pt` | `yolo11x-cls.pt` |
| Pose | `yolo11n-pose.pt` | `yolo11s-pose.pt` | `yolo11m-pose.pt` | `yolo11l-pose.pt` | `yolo11x-pose.pt` |
| OBB | `yolo11n-obb.pt` | `yolo11s-obb.pt` | `yolo11m-obb.pt` | `yolo11l-obb.pt` | `yolo11x-obb.pt` |

## Other Supported YOLO Versions

Ultralytics also supports these YOLO versions (inference only, not training):

- **YOLOv10**: NMS-free training, efficiency-accuracy architecture
- **YOLOv9**: Programmable Gradient Information (PGI) implementation  
- **YOLOv8**: Versatile with segmentation, pose, classification support
- **YOLOv5**: Improved performance and speed trade-offs
- **YOLOv3**: Classic real-time object detection

## Usage Examples

### Python Code
```python
from ultralytics import YOLO

# Load object detection model
model = YOLO('yolo26s.pt')  # or 'yolo11s.pt'

# Load instance segmentation model  
model = YOLO('yolo26m-seg.pt')

# Load pose estimation model
model = YOLO('yolo26l-pose.pt')
```

### CLI Commands
```bash
# Predict with object detection model
yolo predict model=yolo26s.pt source='image.jpg'

# Predict with instance segmentation model
yolo predict model=yolo26m-seg.pt source='image.jpg'

# Use specific task mode
yolo detect predict model=yolo26s.pt source='image.jpg'
yolo segment predict model=yolo26m-seg.pt source='image.jpg'
```

## Important Notes

1. **Model Download**: Models are automatically downloaded from Ultralytics servers on first use
2. **File Extension**: All model files have `.pt` extension, include it when referencing
3. **Task Compatibility**: Ensure model type matches your task (detection, segmentation, etc.)
4. **Hardware Requirements**: Larger models (l, x) require more GPU memory and compute resources
5. **License**: AGPL-3.0 for open source, Enterprise License for commercial use

## Related Documentation

- [Model Selection Guide](./model_selection.md) - How to choose the right model for your needs
- [Task Types](./task_types.md) - Detailed explanation of computer vision tasks
- [Ultralytics Official Documentation](https://docs.ultralytics.com/) - Complete API reference and tutorials

## Utility Scripts for Model Management

For model selection, validation, and management utilities, use the provided scripts:

```bash
# Run model utilities examples
python scripts/model_utils.py

# Test model download and validation
python scripts/quick_tests.py --test download --model yolo26n.pt

# Compare models for a specific task
python scripts/quick_tests.py --test performance --model yolo26n.pt
```

**Script Location**: `scripts/model_utils.py`

**Additional scripts for model-related tasks**:
- `scripts/quick_tests.py` - Model testing and validation
- `scripts/training_helpers.py` - Model training and evaluation
- `scripts/config_templates.py` - Model configuration templates

**Benefits**:
- Save tokens by extracting code from documentation
- Ready-to-use functions for model management
- Consistent API across all model-related tasks
- Modular design, import only what you need
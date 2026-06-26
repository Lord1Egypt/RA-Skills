# YOLO Parameter Reference

This document provides a comprehensive reference for all YOLO configuration parameters, based on the official Ultralytics `args_default.yaml` file.

**Note**: For practical configuration examples, see [Configuration Samples](./configuration_samples.md). This document serves as a complete reference for all available parameters.

## Parameter Categories

YOLO parameters are organized into the following categories:

1. **Global Parameters** - Task and mode settings
2. **Training Parameters** - Model training configuration
3. **Validation/Test Parameters** - Evaluation settings
4. **Prediction Parameters** - Inference configuration
5. **Export Parameters** - Model export settings
6. **Hyperparameters** - Optimization and augmentation
7. **Logging Parameters** - Experiment tracking

## 1. Global Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `task` | str | `detect` | YOLO task: `detect`, `segment`, `classify`, `pose`, `obb` |
| `mode` | str | `train` | YOLO mode: `train`, `val`, `predict`, `export`, `track`, `benchmark` |

## 2. Training Parameters

### Basic Training Settings

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model` | str | - | Path to model file (e.g., `yolo26n.pt`) or architecture file (e.g., `yolo26n.yaml`) |
| `data` | str | - | Path to dataset configuration file (e.g., `coco8.yaml`) |
| `epochs` | int | `100` | Number of training epochs |
| `time` | float | - | Maximum hours to train (overrides epochs if set) |
| `patience` | int | `100` | Early stopping after N epochs without validation improvement |
| `batch` | int/float | `16` | Batch size as integer, or float 0.0-1.0 for AutoBatch fraction of GPU memory |
| `imgsz` | int/list | `640` | Image size: integer for square, or [height, width] for rectangular |
| `save` | bool | `True` | Save training checkpoints and prediction results |
| `save_period` | int | `-1` | Save checkpoint every N epochs (-1 = save only last) |
| `cache` | bool/str | `False` | Cache images: `True`/'ram' for RAM, 'disk' for disk cache |
| `device` | int/str/list | - | Device: 0 or [0,1,2,3] for CUDA, 'cpu', 'mps', or auto-select |
| `workers` | int | `8` | Data loader workers (per RANK if DDP) |
| `project` | str | - | Project name for results directory |
| `name` | str | - | Experiment name (results in 'project/name') |
| `exist_ok` | bool | `False` | Overwrite existing 'project/name' directory |
| `pretrained` | bool/str | `True` | Use pretrained weights (bool) or load from path (str) |
| `optimizer` | str | `auto` | Optimizer: SGD, Adam, AdamW, etc., or 'auto' |
| `verbose` | bool | `True` | Print verbose logs during training/validation |
| `seed` | int | `0` | Random seed for reproducibility |
| `deterministic` | bool | `True` | Enable deterministic operations |
| `single_cls` | bool | `False` | Treat all classes as single class |
| `rect` | bool | `False` | Rectangular training batches |
| `cos_lr` | bool | `False` | Use cosine learning rate scheduler |
| `close_mosaic` | int | `10` | Disable mosaic augmentation for final N epochs |
| `resume` | bool | `False` | Resume training from last checkpoint |
| `amp` | bool | `True` | Automatic Mixed Precision (AMP) training |
| `fraction` | float | `1.0` | Fraction of training dataset to use |
| `profile` | bool | `False` | Profile ONNX/TensorRT speeds during training |
| `freeze` | int/list | - | Freeze first N layers or specific layer indices |
| `multi_scale` | float | `0.0` | Multi-scale range as fraction of imgsz |
| `compile` | bool/str | `False` | Enable torch.compile() with backend |

### Task-Specific Training Parameters

#### Segmentation
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `overlap_mask` | bool | `True` | Merge instance masks during training |
| `mask_ratio` | int | `4` | Mask downsample ratio |

#### Classification
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `dropout` | float | `0.0` | Dropout for classification head |

## 3. Validation/Test Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `val` | bool | `True` | Run validation during training |
| `split` | str | `val` | Dataset split to use for validation: 'val', 'test', or 'train' |
| `save_json` | bool | `False` | Save results to JSON file |
| `save_hybrid` | bool | `False` | Save hybrid version of labels |
| `conf` | float | `0.001` | Confidence threshold for validation |
| `iou` | float | `0.6` | IoU threshold for validation |
| `max_det` | int | `300` | Maximum detections per image |
| `half` | bool | `True` | Use half precision (FP16) |
| `dnn` | bool | `False` | Use OpenCV DNN for ONNX inference |
| `plots` | bool | `True` | Save plots during training/validation |
| `rect` | bool | `False` | Rectangular validation when mode='val' |

## 4. Prediction Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `source` | str | - | Source: file, dir, URL, screen, PIL, OpenCV, numpy, torch, etc. |
| `conf` | float | `0.25` | Confidence threshold for detection |
| `iou` | float | `0.7` | IoU threshold for NMS |
| `imgsz` | int/list | `640` | Inference image size |
| `max_det` | int | `300` | Maximum detections per image |
| `device` | int/str/list | - | Device for inference |
| `show` | bool | `False` | Show results |
| `save` | bool | `False` | Save results to 'runs/detect' |
| `save_txt` | bool | `False` | Save results as text file |
| `save_conf` | bool | `False` | Save confidence in text file |
| `save_crop` | bool | `False` | Save cropped detections |
| `show_labels` | bool | `True` | Show labels on results |
| `show_conf` | bool | `True` | Show confidence on results |
| `vid_stride` | int | `1` | Video frame stride |
| `stream_buffer` | bool | `False` | Buffer all streaming frames |
| `line_width` | int/float | - | Bounding box line width |
| `visualize` | bool | `False` | Visualize model features |
| `augment` | bool | `False` | Apply test-time augmentation |
| `agnostic_nms` | bool | `False` | Class-agnostic NMS |
| `retina_masks` | bool | `False` | Use high-resolution masks (segmentation) |
| `boxes` | bool | `True` | Show bounding boxes (segmentation) |
| `format` | str | `torchscript` | Format to export to |

## 5. Export Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `format` | str | `torchscript` | Export format: torchscript, onnx, openvino, tensorrt, coreml, saved_model, pb, tflite, paddle, ncnn |
| `imgsz` | int/list | `640` | Export image size |
| `keras` | bool | `False` | Export as Keras SavedModel |
| `optimize` | bool | `False` | TorchScript: optimize for mobile |
| `half` | bool | `False` | FP16 quantization |
| `int8` | bool | `False` | INT8 quantization |
| `dynamic` | bool | `False` | ONNX/TensorRT: dynamic axes |
| `simplify` | bool | `False` | ONNX: simplify model |
| `opset` | int | - | ONNX: opset version |
| `workspace` | int/float | `4` | TensorRT: workspace size (GB) |
| `nms` | bool | `False` | CoreML: add NMS |

## 6. Hyperparameters

### Learning Rate Parameters
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `lr0` | float | `0.01` | Initial learning rate |
| `lrf` | float | `0.01` | Final learning rate factor |
| `momentum` | float | `0.937` | SGD momentum/Adam beta1 |
| `weight_decay` | float | `0.0005` | Optimizer weight decay |
| `warmup_epochs` | float | `3.0` | Warmup epochs |
| `warmup_momentum` | float | `0.8` | Warmup initial momentum |
| `warmup_bias_lr` | float | `0.1` | Warmup initial bias learning rate |

### Augmentation Parameters
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `hsv_h` | float | `0.015` | HSV-Hue augmentation (fraction) |
| `hsv_s` | float | `0.7` | HSV-Saturation augmentation (fraction) |
| `hsv_v` | float | `0.4` | HSV-Value augmentation (fraction) |
| `degrees` | float | `0.0` | Image rotation (+/- degrees) |
| `translate` | float | `0.1` | Image translation (+/- fraction) |
| `scale` | float | `0.5` | Image scaling (+/- gain) |
| `shear` | float | `0.0` | Image shearing (+/- degrees) |
| `perspective` | float | `0.0` | Image perspective (+/- fraction) |
| `flipud` | float | `0.0` | Image flip up-down (probability) |
| `fliplr` | float | `0.5` | Image flip left-right (probability) |
| `mosaic` | float | `1.0` | Image mosaic (probability) |
| `mixup` | float | `0.0` | Image mixup (probability) |
| `copy_paste` | float | `0.0` | Segment copy-paste (probability) |
| `erasing` | float | `0.4` | Random erasing (probability) |
| `crop_fraction` | float | `1.0` | Fraction of image to crop |

### Loss Parameters
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `label_smoothing` | float | `0.0` | Label smoothing epsilon |
| `box` | float | `7.5` | Box loss gain |
| `cls` | float | `0.5` | Class loss gain |
| `dfl` | float | `1.5` | DFL loss gain |
| `pose` | float | `12.0` | Pose loss gain (pose only) |
| `kobj` | float | `1.0` | Keypoint object loss gain (pose only) |
| `nbs` | int | `64` | Nominal batch size |

## 7. Logging and Tracking Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `entity` | str | - | Weights & Biases entity |
| `upload_dataset` | bool | `False` | Upload dataset to W&B |
| `bbox_interval` | int | `-1` | W&B: bounding box logging interval |
| `artifact_alias` | str | `latest` | W&B: artifact alias |

## Parameter Usage Examples

### Basic Training
```python
from ultralytics import YOLO

model = YOLO('yolo26n.pt')
model.train(
    data='coco8.yaml',
    epochs=100,
    imgsz=640,
    batch=16,
    device='cuda:0',
    lr0=0.01,
    augment=True,
)
```

### Inference with Custom Parameters
```python
results = model.predict(
    source='image.jpg',
    conf=0.5,      # Higher confidence threshold
    iou=0.45,      # Lower IoU for crowded scenes
    imgsz=1280,    # Higher resolution
    augment=True,  # Test-time augmentation
    max_det=100,   # Limit detections
)
```

### Export with Optimization
```python
model.export(
    format='onnx',
    imgsz=[640, 480],
    half=True,      # FP16 quantization
    simplify=True,  # Simplify model
    dynamic=True,   # Dynamic axes
)
```

## Parameter Selection Guidelines

### For Speed vs. Accuracy
- **Speed**: Lower `imgsz`, enable `half`, disable `augment`
- **Accuracy**: Higher `imgsz`, disable `half`, enable `augment`

### For Different Scenarios
- **Crowded scenes**: Lower `iou`, higher `conf`
- **Small objects**: Lower `conf`, higher `imgsz`
- **Real-time**: Enable `half`, lower `imgsz`, disable `augment`

### Hardware Considerations
- **Limited GPU memory**: Lower `batch`, enable `half`
- **CPU-only**: Disable `half`, use smaller `imgsz`
- **Multiple GPUs**: Use list for `device` (e.g., `device=[0,1]`)

## Related Documentation

- [Configuration Samples](./configuration_samples.md) - Practical configuration examples
- [Training Basics](./training_basics.md) - Training workflow and best practices
- [Ultralytics Official Documentation](https://docs.ultralytics.com/usage/cfg/) - Complete parameter reference
- [Model Selection](./model_selection.md) - Choosing appropriate models for your task

## Utility Scripts for Parameter Management

For ready-to-use configuration templates and parameter utilities, use the provided scripts:

```bash
# Run configuration templates examples
python scripts/config_templates.py

# Test parameter configurations
python scripts/quick_tests.py --test performance --model yolo26n.pt
```

**Script Location**: `scripts/config_templates.py`

**Additional scripts for parameter management**:
- `scripts/training_helpers.py` - Training parameter configurations
- `scripts/dataset_tools.py` - Dataset preparation parameters
- `scripts/model_utils.py` - Model selection parameters

**Benefits**:
- Save tokens by extracting code from documentation
- Ready-to-use configuration templates
- Consistent parameter handling across all tasks
- Modular design, import only what you need

**Example usage**:
```python
from scripts.config_templates import (
    get_basic_config,
    get_production_config,
    get_config_for_scenario,
    merge_configs,
    print_config
)

# Get configuration for a scenario
config = get_config_for_scenario('production')

# Print configuration
print_config(config, "Production Configuration")

# Merge configurations
base = get_basic_config()
custom = {'conf': 0.4, 'imgsz': 1280}
merged = merge_configs(base, custom)
```
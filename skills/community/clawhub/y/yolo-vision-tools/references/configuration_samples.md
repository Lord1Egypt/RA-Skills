# YOLO Configuration Examples

This document provides various configuration examples for Ultralytics YOLO, covering usage scenarios from basic to advanced.

**Latest Models**: Examples use YOLO26 models, but work with YOLO11 and other versions by replacing model names.

**Note**: For comprehensive configuration templates and ready-to-use functions, see the `config_templates.py` script in the `scripts/` directory.

## Quick Start

### Simplest Usage
```python
from ultralytics import YOLO

# Load model
model = YOLO('yolo26n.pt')  # Pretrained model

# Basic inference
results = model('bus.jpg')                     # Single image
```

## Basic Configuration Parameters

### Common Parameter Explanation
```python
# Basic configuration parameters
config = {
    'conf': 0.25,      # Confidence threshold (0-1)
    'iou': 0.7,        # NMS IoU threshold (0-1)
    'imgsz': 640,      # Input image size
    'device': 'cuda:0' if torch.cuda.is_available() else 'cpu',
    'show': False,     # Show results
    'save': False,     # Save results
}
```

**For complete parameter reference and templates, use:**
```python
from scripts.config_templates import get_basic_config, get_production_config
basic_config = get_basic_config()
production_config = get_production_config()
```

## Configuration Examples by Scenario

### 1. Image Processing

#### Single Image Detection
```python
# Basic image processing
results = model.predict(source='image.jpg', conf=0.5, save=True)
```

#### Batch Image Processing
```python
# Process multiple images
results = model.predict(source='images/', batch=16, workers=8)
```

**For scenario-specific configurations, use:**
```python
from scripts.config_templates import get_image_processing_config
config = get_image_processing_config()
```

### 2. Video Processing

#### Standard Video Processing
```python
# Process video file
results = model.predict(source='video.mp4', save=True)
```

#### Real-time Video with Streaming
```python
# Memory-efficient video processing
results = model.predict(source='video.mp4', stream=True, show=True)
```

**For video configurations, use:**
```python
from scripts.config_templates import get_video_processing_config
config = get_video_processing_config(stream=True)
```

### 3. Real-time Camera Streams

#### Webcam Processing
```python
# Process default webcam
results = model.predict(source=0, show=True)
```

**For real-time configurations, use:**
```python
from scripts.config_templates import get_webcam_config, get_realtime_config
webcam_config = get_webcam_config()
realtime_config = get_realtime_config()
```

### 4. Special Scenarios

#### Low-light/Challenging Conditions
```python
# Adjust for challenging conditions
results = model.predict(source='low_light.jpg', conf=0.15, imgsz=1280)
```

#### Crowded Scene Processing
```python
# Optimize for crowded scenes
results = model.predict(source='crowd.jpg', conf=0.4, iou=0.3, max_det=1000)
```

**For special scenario configurations, use:**
```python
from scripts.config_templates import (
    get_low_light_config,
    get_crowded_scene_config,
    get_small_object_config
)
```

## Performance Optimization Configurations

### 1. GPU Acceleration
```python
# GPU optimization
config = {
    'device': 'cuda:0',
    'half': True,      # FP16 half precision
    'batch': 32,
    'workers': 16,
}
```

### 2. CPU Optimization
```python
# CPU optimization
config = {
    'device': 'cpu',
    'batch': 1,
    'workers': 4,
    'half': False,
}
```

**For performance configurations, use:**
```python
from scripts.config_templates import (
    get_gpu_optimized_config,
    get_cpu_optimized_config,
    get_memory_efficient_config
)
```

## Task-Specific Configurations

### 1. Object Detection
```python
# Detection configuration
config = {'task': 'detect', 'conf': 0.25, 'iou': 0.7}
```

### 2. Instance Segmentation
```python
# Segmentation configuration
config = {'task': 'segment', 'retina_masks': True, 'boxes': True}
```

### 3. Pose Estimation
```python
# Pose configuration
config = {'task': 'pose', 'kpt_shape': [17, 3]}
```

**For task-specific configurations, use:**
```python
from scripts.config_templates import (
    get_detection_config,
    get_segmentation_config,
    get_pose_config,
    get_classification_config,
    get_obb_config
)
```

## Training Configurations

### Basic Training
```python
# Basic training configuration
train_config = {
    'data': 'dataset.yaml',
    'epochs': 100,
    'imgsz': 640,
    'batch': 16,
}
```

### Advanced Training
```python
# Advanced training with hyperparameters
train_config = {
    'data': 'dataset.yaml',
    'epochs': 100,
    'lr0': 0.01,        # Initial learning rate
    'lrf': 0.01,        # Final learning rate factor
    'augment': True,    # Enable augmentation
}
```

**For training configurations, use:**
```python
from scripts.config_templates import get_training_config, get_advanced_training_config
from scripts.training_helpers import get_basic_training_config, get_advanced_training_config
```

## Configuration Templates

### Production Environment Template
```python
# Production-ready configuration
from scripts.config_templates import get_production_config
config = get_production_config()
```

### Development/Debugging Template
```python
# Development configuration
from scripts.config_templates import get_development_config
config = get_development_config()
```

### Real-time Application Template
```python
# Real-time configuration
from scripts.config_templates import get_realtime_config
config = get_realtime_config()
```

## Using Configuration Scripts

### 1. Import Configuration Templates
```python
from scripts.config_templates import (
    get_basic_config,
    get_production_config,
    get_realtime_config,
    get_config_for_scenario,
    merge_configs
)

# Get configuration for a scenario
config = get_config_for_scenario('production')

# Merge configurations
base = get_basic_config()
custom = {'conf': 0.4, 'imgsz': 1280}
merged = merge_configs(base, custom)
```

### 2. Print Configuration
```python
from scripts.config_templates import print_config

config = get_production_config()
print_config(config, "Production Configuration")
```

### 3. Available Scenarios
```python
from scripts.config_templates import get_config_for_scenario

# Available scenarios:
# - 'production', 'realtime', 'development'
# - 'image', 'video', 'webcam'
# - 'low_light', 'crowded', 'small_objects'
# - 'gpu', 'cpu', 'memory'
# - 'detection', 'segmentation', 'pose', 'classification', 'obb'
# - 'training', 'advanced_training'

config = get_config_for_scenario('realtime')
```

## Troubleshooting Configurations

### Common Issues and Fixes

#### Memory Issues
```python
# Reduce memory usage
config = {
    'stream': True,     # Critical for large inputs
    'batch': 1,         # Minimum batch size
    'imgsz': 320,       # Lower resolution
    'half': True,       # Half precision
}
```

#### Slow Performance
```python
# Optimize for speed
config = {
    'imgsz': 320,       # Lower resolution
    'half': True,       # FP16
    'batch': 32,        # Batch processing
    'augment': False,   # Disable augmentation
}
```

#### Low Detection Quality
```python
# Improve detection quality
config = {
    'imgsz': 1280,      # Higher resolution
    'augment': True,    # Enable augmentation
    'conf': 0.1,        # Lower initial threshold
    'max_det': 1000,    # More detections
}
```

## Complete Parameter Reference

For a complete list of all available parameters, refer to:
- [Parameter Reference](./parameter_reference.md) - Complete parameter documentation
- `scripts/config_templates.py` - Ready-to-use configuration templates
- `scripts/parameter_reference.md` - Detailed parameter specifications

### Key Parameter Groups

| Parameter Group | Key Parameters | Typical Values |
|-----------------|----------------|----------------|
| **Input Control** | `source`, `imgsz`, `batch`, `workers` | Varies by application |
| **Detection Control** | `conf`, `iou`, `max_det`, `agnostic_nms` | `conf=0.25`, `iou=0.7` |
| **Output Control** | `save`, `save_txt`, `save_conf`, `show` | Boolean flags |
| **Performance** | `device`, `half`, `dnn`, `stream` | Device-specific |
| **Advanced** | `augment`, `visualize`, `retina_masks` | Specialized features |

## Best Practices

1. **Start Simple**: Begin with default parameters, then adjust based on results
2. **Use Templates**: Leverage configuration templates from `scripts/config_templates.py`
3. **Profile Performance**: Use `yolo benchmark` to test different configurations
4. **Validate Changes**: Test parameter changes on validation data
5. **Document Configurations**: Keep records of successful configurations
6. **Consider Hardware**: Adjust parameters based on available hardware

## Related Documentation

- [Parameter Reference](./parameter_reference.md) - Complete parameter reference
- [Model Selection](./model_selection.md) - Choosing the right model
- [Task Types](./task_types.md) - Understanding different YOLO tasks
- [Training Basics](./training_basics.md) - Training configuration guide
- [Ultralytics Official Documentation](https://docs.ultralytics.com/usage/cfg/) - Complete parameter reference

## Utility Scripts

For ready-to-use configuration templates and utilities:

```bash
# Run configuration examples
python scripts/config_templates.py

# Import in your code
from scripts.config_templates import (
    get_basic_config,
    get_production_config,
    get_realtime_config,
    get_config_for_scenario,
    merge_configs,
    print_config
)
```

**Script Location**: `scripts/config_templates.py`
# YOLO Model Selection Guide

## Overview

This guide helps you select the appropriate Ultralytics YOLO model based on your application requirements, hardware constraints, and performance needs.

**Key Decision**: Choose between YOLO26 (latest features) and YOLO11 (stable production). Both support all five tasks: detection, segmentation, classification, pose estimation, and oriented detection.

## Quick Decision Flowchart

```mermaid
graph TD
    A[Start Model Selection] --> B{YOLO Version?};
    B --> C[Latest Features];
    B --> D[Production Stability];
    C --> E[Choose YOLO26];
    D --> F[Choose YOLO11];
    
    E --> G{Primary Requirement?};
    F --> G;
    
    G --> H[Speed First];
    G --> I[Accuracy First];
    G --> J[Balanced Performance];
    
    H --> K{Device Type?};
    K --> L[Mobile/Edge];
    K --> M[Desktop/Server];
    L --> N[Choose Nano (n)];
    M --> O[Choose Small (s)];
    
    I --> P{Hardware Resources?};
    P --> Q[Ample GPU Memory];
    P --> R[Limited Resources];
    Q --> S[Choose XLarge (x)];
    R --> T[Choose Large (l)];
    
    J --> U{Task Type?};
    U --> V[General Detection];
    U --> W[Segmentation/Classification/Pose];
    V --> X[Choose Medium (m)];
    W --> Y[Choose task-specific Medium model];
```

## Model Specifications Comparison

### YOLO26 Models (Latest Generation)

| Model | Size | Relative Speed | Relative Accuracy | Approx. Params | Approx. Size | Best For |
|-------|------|----------------|-------------------|----------------|--------------|----------|
| **yolo26n** | Nano | ⚡⚡⚡⚡⚡ (Fastest) | ⭐ (Lowest) | ~2.5M | ~5MB | Mobile, edge computing, real-time |
| **yolo26s** | Small | ⚡⚡⚡⚡ | ⭐⭐ | ~9M | ~15MB | General purpose, balanced needs |
| **yolo26m** | Medium | ⚡⚡⚡ | ⭐⭐⭐ | ~25M | ~40MB | Server applications, medium accuracy |
| **yolo26l** | Large | ⚡⚡ | ⭐⭐⭐⭐ | ~50M | ~85MB | Accuracy-first, high-quality detection |
| **yolo26x** | XLarge | ⚡ | ⭐⭐⭐⭐⭐ (Highest) | ~100M | ~170MB | Research, extreme accuracy needs |

### YOLO11 Models (Stable Production)

| Model | Size | Relative Speed | Relative Accuracy | Best For |
|-------|------|----------------|-------------------|----------|
| **yolo11n** | Nano | ⚡⚡⚡⚡⚡ | ⭐ | Production mobile/edge apps |
| **yolo11s** | Small | ⚡⚡⚡⚡ | ⭐⭐ | General production workloads |
| **yolo11m** | Medium | ⚡⚡⚡ | ⭐⭐⭐ | Balanced production accuracy |
| **yolo11l** | Large | ⚡⚡ | ⭐⭐⭐⭐ | High-accuracy production |
| **yolo11x** | XLarge | ⚡ | ⭐⭐⭐⭐⭐ | Maximum accuracy production |

> **Note**: Specifications are approximate. Refer to [Ultralytics Official Documentation](https://docs.ultralytics.com/models/) for latest values.

## Selection by Task Type

### Object Detection
- **General Purpose**: `yolo26s.pt` or `yolo11s.pt`
- **Real-time Applications**: `yolo26n.pt` or `yolo11n.pt`
- **High Accuracy**: `yolo26l.pt` or `yolo11l.pt`
- **Research/Benchmarks**: `yolo26x.pt` or `yolo11x.pt`

### Instance Segmentation
- **General Segmentation**: `yolo26m-seg.pt` or `yolo11m-seg.pt`
- **Real-time Segmentation**: `yolo26n-seg.pt` or `yolo11n-seg.pt`
- **Medical/Precision Applications**: `yolo26l-seg.pt` or `yolo11l-seg.pt`

### Image Classification
- **General Classification**: `yolo26m-cls.pt` or `yolo11m-cls.pt`
- **Mobile Classification**: `yolo26n-cls.pt` or `yolo11n-cls.pt`
- **Fine-grained Classification**: `yolo26l-cls.pt` or `yolo11l-cls.pt`

### Pose Estimation
- **General Pose**: `yolo26m-pose.pt` or `yolo11m-pose.pt`
- **Real-time Pose**: `yolo26n-pose.pt` or `yolo11n-pose.pt`
- **High-accuracy Pose**: `yolo26l-pose.pt` or `yolo11l-pose.pt`

### Oriented Bounding Box Detection
- **General OBB**: `yolo26m-obb.pt` or `yolo11m-obb.pt`
- **Aerial/Satellite Imagery**: `yolo26l-obb.pt` or `yolo11l-obb.pt`
- **Document Analysis**: `yolo26s-obb.pt` or `yolo11s-obb.pt`

## Hardware Considerations

### GPU Memory Requirements
- **Nano/Small**: 2-4GB GPU memory
- **Medium**: 4-8GB GPU memory  
- **Large/XLarge**: 8+ GB GPU memory

### CPU-Only Deployment
For CPU-only environments:
1. Use smaller models (nano or small)
2. Consider batch size = 1
3. Enable `half=False` for CPU compatibility
4. Use OpenVINO or ONNX runtime for optimization

### Mobile/Edge Deployment
For mobile and edge devices:
1. Use Nano models
2. Consider TensorRT, CoreML, or NCNN deployment
3. Optimize with quantization (INT8/FP16)
4. Use TensorFlow Lite for Android

## Application Scenarios

### Image Processing Pipelines
- **Batch Processing**: Medium or Large models with batch size > 1
- **Interactive Applications**: Small models with real-time response
- **Quality Control Systems**: Large models for maximum accuracy

### Video Processing
- **Real-time Video**: Nano or Small models
- **Offline Video Analysis**: Medium models with batch processing
- **High-quality Production**: Large models with careful optimization

### Special Scenarios
- **Low-light Conditions**: Larger models generally perform better
- **Small Object Detection**: Higher resolution input + Larger models
- **Crowded Scenes**: Higher confidence thresholds + Larger models

## Selection Strategy

### Step-by-Step Selection Process

1. **Define Requirements**
   - Real-time vs batch processing
   - Accuracy thresholds
   - Hardware constraints
   - Deployment environment

2. **Choose YOLO Version**
   - YOLO26 for latest features and edge optimization
   - YOLO11 for proven stability in production

3. **Select Model Size**
   - Nano: Maximum speed, minimum resources
   - Small: Good balance for most applications
   - Medium: Default for server applications
   - Large: When accuracy is critical
   - XLarge: Research, benchmarks, maximum accuracy

4. **Validate with Testing**
   - Test on representative sample data
   - Measure inference speed on target hardware
   - Evaluate accuracy metrics
   - Adjust based on results

### Python Selection Logic Example

```python
def select_model(task="detect", speed_priority="balanced", hardware="gpu"):
    """Helper function to select appropriate model"""
    
    # YOLO version selection
    version = "yolo26"  # or "yolo11" for production
    
    # Size selection based on speed priority
    if speed_priority == "max_speed":
        size = "n"
    elif speed_priority == "speed":
        size = "s"  
    elif speed_priority == "balanced":
        size = "m"
    elif speed_priority == "accuracy":
        size = "l"
    elif speed_priority == "max_accuracy":
        size = "x"
    else:
        size = "m"
    
    # Task suffix
    if task == "detect":
        suffix = ""
    elif task == "segment":
        suffix = "-seg"
    elif task == "classify":
        suffix = "-cls"
    elif task == "pose":
        suffix = "-pose"
    elif task == "obb":
        suffix = "-obb"
    else:
        suffix = ""
    
    return f"{version}{size}{suffix}.pt"

# Example usage
model_name = select_model(task="segment", speed_priority="balanced")
print(f"Selected model: {model_name}")  # Output: yolo26m-seg.pt
```

## Performance Optimization Tips

1. **Input Size**: Smaller `imgsz` for speed, larger for accuracy
2. **Batch Size**: Larger batches for throughput, smaller for latency
3. **Precision**: Use FP16 for speed, FP32 for maximum accuracy
4. **Confidence Threshold**: Adjust `conf` based on application needs
5. **Device Selection**: GPU for speed, CPU for compatibility

## Common Questions

**Q: Should I use YOLO26 or YOLO11?**
A: Use YOLO26 for latest features and edge optimization. Use YOLO11 for production stability.

**Q: How do I choose between speed and accuracy?**
A: Test both on your specific data and hardware. The performance difference varies by application.

**Q: Can I switch models later?**
A: Yes, YOLO models share the same API. You can easily switch between models.

**Q: How important is model size for my application?**
A: Very important. Larger models require more resources but provide better accuracy.

**Q: Should I train my own model instead?**
A: For custom objects or domain-specific applications, yes. For general objects, pre-trained models are sufficient.

## Further Reading

- [Model Names Reference](./model_names.md) - Complete list of all YOLO models
- [Task Types](./task_types.md) - Detailed explanation of computer vision tasks
- [Configuration Samples](./configuration_samples.md) - Parameter tuning examples
- [Ultralytics Models Documentation](https://docs.ultralytics.com/models/) - Official model specifications

## Utility Scripts

For ready-to-use model selection and management tools, use the `model_utils.py` script:

```bash
# Run model utilities examples
python scripts/model_utils.py

# Import in your code
from scripts.model_utils import (
    select_model,                    # Select model based on requirements
    get_model_recommendation,        # Get detailed recommendation
    get_model_specifications,        # Get model specifications
    print_model_comparison,          # Print comparison table
    validate_model_file,             # Validate model file
    compare_models_for_task,         # Compare models for specific task
    load_model_with_fallback,        # Load model with fallback options
    get_model_cache_info,            # Get cache information
    clear_model_cache                # Clear old cache files
)

# Example usage
model_name = select_model(task="detect", speed_priority="balanced")
recommendation = get_model_recommendation({
    'task': 'segment',
    'realtime': True,
    'accuracy_needed': 'medium'
})
print_model_comparison("yolo26")
```

**Script Location**: `scripts/model_utils.py`

**Additional scripts for model management**:
- `scripts/quick_tests.py` - Quick model testing
- `scripts/training_helpers.py` - Training and evaluation
- `scripts/config_templates.py` - Configuration templates

**Benefits**:
- Save tokens by extracting large code blocks from documentation
- Ready-to-use functions for model selection and management
- Consistent API across all model-related tasks
- Modular design, import only what you need
#!/usr/bin/env python3
"""
YOLO Configuration Templates

This script provides ready-to-use configuration templates for various YOLO scenarios.
Extracted from configuration_samples.md to save token usage.
"""

try:
    import torch
    HAS_TORCH = True
except ImportError:
    # Create a dummy torch module for configuration generation
    class DummyTorch:
        class cuda:
            @staticmethod
            def is_available():
                return False
    torch = DummyTorch()
    HAS_TORCH = False

# ============================================================================
# BASIC CONFIGURATION TEMPLATES
# ============================================================================

def get_basic_config():
    """Basic configuration for standard use cases"""
    return {
        'conf': 0.25,      # Confidence threshold
        'iou': 0.7,        # IoU threshold for NMS
        'imgsz': 640,      # Image size
        'device': 'cuda:0' if torch.cuda.is_available() else 'cpu',
        'save': False,     # Save results
        'show': False,     # Show results
        'verbose': False,  # Verbose output
    }

def get_production_config():
    """Production-ready configuration"""
    return {
        'conf': 0.5,       # Higher threshold for production
        'iou': 0.45,       # Balanced IoU
        'imgsz': 640,
        'device': 'cuda:0' if torch.cuda.is_available() else 'cpu',
        'half': torch.cuda.is_available(),  # FP16 if GPU available
        'max_det': 100,
        'augment': False,  # Disable for consistent results
        'verbose': False,  # Minimal logging
        'save': True,
        'save_txt': True,
        'save_conf': True,
        'project': 'production_results',
        'name': 'run',
        'exist_ok': True,
    }

def get_realtime_config():
    """Real-time application configuration"""
    # Use GPU if available, otherwise CPU
    device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
    half = torch.cuda.is_available()  # FP16 only works on CUDA
    
    return {
        'conf': 0.3,
        'iou': 0.4,
        'imgsz': 320,      # Lower resolution for speed
        'device': device,
        'half': half,      # FP16 for speed (only on CUDA)
        'show': True,
        'verbose': False,
        'max_det': 50,     # Limit detections for speed
        'augment': False,  # Disable for speed
    }

def get_development_config():
    """Development/debugging configuration"""
    # Use GPU if available, otherwise CPU
    device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
    
    return {
        'conf': 0.25,
        'iou': 0.5,
        'imgsz': 640,
        'device': device,
        'show': True,      # Visual feedback
        'verbose': True,   # Detailed logging
        'augment': True,   # Test augmentation
        'visualize': True, # Feature visualization
        'save': True,
        'save_txt': True,
        'project': 'debug',
        'name': 'debug_run',
    }

# ============================================================================
# SCENARIO-SPECIFIC CONFIGURATIONS
# ============================================================================

def get_image_processing_config():
    """Configuration for image processing"""
    return {
        'conf': 0.5,        # Higher confidence for images
        'save': True,
        'save_txt': True,
        'save_conf': True,
        'project': 'image_results',
        'name': 'image_processing',
        'exist_ok': True,
    }

def get_video_processing_config(stream=True):
    """Configuration for video processing"""
    config = {
        'conf': 0.25,
        'save': True,
        'project': 'video_results',
        'name': 'video_processing',
    }
    
    if stream:
        config['stream'] = True  # Memory-efficient processing
        config['imgsz'] = 480    # Lower resolution for videos
    
    return config

def get_webcam_config():
    """Configuration for webcam/real-time processing"""
    return {
        'source': 0,        # Default webcam
        'conf': 0.25,
        'show': True,       # Real-time display
        'show_labels': True,
        'show_conf': True,
        'line_width': 2,    # Bounding box line width
        'device': 'cuda:0' if torch.cuda.is_available() else 'cpu',
    }

def get_low_light_config():
    """Configuration for low-light/challenging conditions"""
    return {
        'conf': 0.15,       # Lower confidence for challenging conditions
        'augment': True,    # Augmentation helps
        'imgsz': 1280,      # Higher resolution for better detail
        'max_det': 500,     # More potential detections
    }

def get_crowded_scene_config():
    """Configuration for crowded scenes"""
    return {
        'conf': 0.4,        # Higher confidence to reduce false positives
        'iou': 0.3,         # Lower IoU for overlapping objects
        'max_det': 1000,    # Higher maximum detections
        'augment': True,
    }

def get_small_object_config():
    """Configuration for small object detection"""
    return {
        'conf': 0.2,        # Lower confidence for small objects
        'imgsz': 1280,      # Higher resolution
        'augment': True,
        'max_det': 500,
    }

# ============================================================================
# PERFORMANCE OPTIMIZATION CONFIGURATIONS
# ============================================================================

def get_gpu_optimized_config():
    """Maximum GPU performance configuration"""
    if not torch.cuda.is_available():
        print("Warning: GPU not available, falling back to CPU optimized config")
        return get_cpu_optimized_config()
    
    return {
        'device': 'cuda:0',
        'half': True,       # FP16 half precision
        'batch': 32,        # Batch processing
        'workers': 16,      # Parallel data loading
        'dnn': False,       # Disable OpenCV DNN for PyTorch optimization
    }

def get_cpu_optimized_config():
    """CPU-optimized configuration"""
    return {
        'device': 'cpu',
        'batch': 1,         # Smaller batch for CPU
        'workers': 4,       # Fewer workers for CPU
        'half': False,      # FP32 for CPU compatibility
        'dnn': True,        # OpenCV DNN can be faster on CPU
    }

def get_memory_efficient_config():
    """Memory-efficient configuration for limited resources"""
    # Use GPU if available, otherwise CPU
    device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
    half = torch.cuda.is_available()  # FP16 only works on CUDA
    
    return {
        'stream': True,     # Critical for memory efficiency
        'batch': 1,         # Single batch
        'imgsz': 320,       # Lower resolution
        'half': half,       # Half precision reduces memory (only on CUDA)
        'device': device,
    }

# ============================================================================
# TASK-SPECIFIC CONFIGURATIONS
# ============================================================================

def get_detection_config():
    """Object detection configuration"""
    return {
        'task': 'detect',
        'conf': 0.25,
        'iou': 0.7,
    }

def get_segmentation_config():
    """Instance segmentation configuration"""
    return {
        'task': 'segment',
        'conf': 0.25,
        'retina_masks': True,  # High-resolution masks
        'boxes': True,         # Show bounding boxes
    }

def get_pose_config():
    """Pose estimation configuration"""
    return {
        'task': 'pose',
        'conf': 0.25,
        'kpt_shape': [17, 3],  # COCO keypoint format
    }

def get_classification_config():
    """Image classification configuration"""
    return {
        'task': 'classify',
        'topk': 5,  # Show top 5 predictions
    }

def get_obb_config():
    """Oriented bounding box configuration"""
    return {
        'task': 'obb',
        'conf': 0.3,
        'imgsz': 1024,  # Higher resolution for rotated objects
    }

# ============================================================================
# TRAINING CONFIGURATIONS
# ============================================================================

def get_training_config(epochs=100, imgsz=640):
    """Basic training configuration"""
    return {
        'epochs': epochs,
        'imgsz': imgsz,
        'batch': 16,
        'workers': 8,
        'device': 'cuda:0' if torch.cuda.is_available() else 'cpu',
        'project': 'runs/train',
        'name': 'exp',
        'exist_ok': True,
        'resume': False,
        'val': True,  # Enable validation
    }

def get_advanced_training_config():
    """Advanced training configuration with hyperparameters"""
    return {
        'epochs': 100,
        'imgsz': 640,
        
        # Optimization parameters
        'lr0': 0.01,               # Initial learning rate
        'lrf': 0.01,               # Final learning rate factor
        'momentum': 0.937,         # SGD momentum
        'weight_decay': 0.0005,    # Optimizer weight decay
        'warmup_epochs': 3.0,      # Warmup epochs
        'warmup_momentum': 0.8,    # Warmup momentum
        'warmup_bias_lr': 0.1,     # Warmup bias learning rate
        
        # Augmentation parameters
        'hsv_h': 0.015,            # HSV-Hue augmentation
        'hsv_s': 0.7,              # HSV-Saturation augmentation
        'hsv_v': 0.4,              # HSV-Value augmentation
        'degrees': 0.0,            # Image rotation
        'translate': 0.1,          # Image translation
        'scale': 0.5,              # Image scaling
        'shear': 0.0,              # Image shearing
        'perspective': 0.0,        # Image perspective
        'flipud': 0.0,             # Flip up-down probability
        'fliplr': 0.5,             # Flip left-right probability
        'mosaic': 1.0,             # Mosaic augmentation probability
        'mixup': 0.0,              # Mixup augmentation probability
        'copy_paste': 0.0,         # Copy-paste augmentation probability
        
        # Model parameters
        'pretrained': True,        # Use pretrained weights
        'optimizer': 'auto',       # Optimizer: SGD, Adam, AdamW, etc.
        'verbose': True,           # Verbose output
        'seed': 0,                 # Random seed
        'deterministic': True,     # Deterministic training
        'single_cls': False,       # Train as single-class dataset
        'rect': False,             # Rectangular training
        'cos_lr': False,           # Cosine learning rate scheduler
        'label_smoothing': 0.0,    # Label smoothing
        'dropout': 0.0,            # Dropout regularization
    }

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def print_config(config, title="Configuration"):
    """Print configuration in a readable format"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    
    for key, value in sorted(config.items()):
        print(f"{key:25}: {value}")
    
    print(f"{'='*60}")

def merge_configs(base_config, override_config):
    """Merge two configurations, with override taking precedence"""
    merged = base_config.copy()
    merged.update(override_config)
    return merged

def get_config_for_scenario(scenario, **kwargs):
    """Get configuration for a specific scenario"""
    scenario_configs = {
        'production': get_production_config,
        'realtime': get_realtime_config,
        'development': get_development_config,
        'image': get_image_processing_config,
        'video': lambda: get_video_processing_config(kwargs.get('stream', True)),
        'webcam': get_webcam_config,
        'low_light': get_low_light_config,
        'crowded': get_crowded_scene_config,
        'small_objects': get_small_object_config,
        'gpu': get_gpu_optimized_config,
        'cpu': get_cpu_optimized_config,
        'memory': get_memory_efficient_config,
        'detection': get_detection_config,
        'segmentation': get_segmentation_config,
        'pose': get_pose_config,
        'classification': get_classification_config,
        'obb': get_obb_config,
        'training': lambda: get_training_config(kwargs.get('epochs', 100), kwargs.get('imgsz', 640)),
        'advanced_training': get_advanced_training_config,
    }
    
    if scenario in scenario_configs:
        return scenario_configs[scenario]()
    else:
        print(f"Warning: Unknown scenario '{scenario}'. Using basic config.")
        return get_basic_config()

# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    print("YOLO Configuration Templates")
    print("=" * 60)
    
    # Example 1: Get production configuration
    prod_config = get_production_config()
    print_config(prod_config, "Production Configuration")
    
    # Example 2: Get configuration for a specific scenario
    realtime_config = get_config_for_scenario('realtime')
    print_config(realtime_config, "Real-time Configuration")
    
    # Example 3: Merge configurations
    base = get_basic_config()
    custom = {'conf': 0.4, 'imgsz': 1280}
    merged = merge_configs(base, custom)
    print_config(merged, "Merged Configuration")
    
    # List available scenarios
    available_scenarios = [
        'production', 'realtime', 'development', 'image', 'video', 'webcam',
        'low_light', 'crowded', 'small_objects', 'gpu', 'cpu', 'memory',
        'detection', 'segmentation', 'pose', 'classification', 'obb',
        'training', 'advanced_training'
    ]
    print("\nAvailable scenarios:", available_scenarios)
#!/usr/bin/env python3
"""
YOLO Model Utilities

This script provides utilities for model selection, loading, and validation.
Extracted from model_selection.md and model_names.md to save token usage.
"""

try:
    import torch
    HAS_TORCH = True
except ImportError:
    # Create a dummy torch module for basic operations
    class DummyTorch:
        class cuda:
            @staticmethod
            def is_available():
                return False
    torch = DummyTorch()
    HAS_TORCH = False
from pathlib import Path

# ============================================================================
# MODEL SELECTION UTILITIES
# ============================================================================

def select_model(task="detect", speed_priority="balanced", hardware="gpu", version="yolo26"):
    """
    Helper function to select appropriate model based on requirements
    
    Args:
        task: Task type ('detect', 'segment', 'classify', 'pose', 'obb')
        speed_priority: Speed vs accuracy priority
            'max_speed', 'speed', 'balanced', 'accuracy', 'max_accuracy'
        hardware: Hardware type ('gpu', 'cpu', 'mobile', 'edge')
        version: YOLO version ('yolo26', 'yolo11')
    
    Returns:
        Model name string
    """
    # YOLO version selection
    if version not in ['yolo26', 'yolo11']:
        version = "yolo26"  # Default to latest
    
    # Size selection based on speed priority
    size_map = {
        'max_speed': 'n',
        'speed': 's',
        'balanced': 'm',
        'accuracy': 'l',
        'max_accuracy': 'x'
    }
    
    size = size_map.get(speed_priority, 'm')  # Default to medium
    
    # Task suffix
    task_suffixes = {
        'detect': '',
        'segment': '-seg',
        'classify': '-cls',
        'pose': '-pose',
        'obb': '-obb'
    }
    
    suffix = task_suffixes.get(task, '')
    
    # Hardware adjustments
    if hardware in ['mobile', 'edge', 'cpu'] and size == 'x':
        size = 'l'  # Downgrade from xlarge for constrained hardware
    elif hardware == 'gpu' and speed_priority == 'max_speed':
        size = 'n'  # Force nano for maximum speed on GPU
    
    model_name = f"{version}{size}{suffix}.pt"
    
    return model_name

def get_model_recommendation(requirements):
    """
    Get model recommendation based on detailed requirements
    
    Args:
        requirements: Dictionary with requirements:
            - task: Task type
            - realtime: Boolean for real-time requirements
            - accuracy_needed: 'low', 'medium', 'high', 'very_high'
            - hardware: Available hardware
            - memory_limit: Memory limit in GB
            - production: Boolean for production use
    
    Returns:
        Dictionary with model recommendation and reasoning
    """
    task = requirements.get('task', 'detect')
    realtime = requirements.get('realtime', False)
    accuracy = requirements.get('accuracy_needed', 'medium')
    hardware = requirements.get('hardware', 'gpu')
    memory_limit = requirements.get('memory_limit', 8)
    production = requirements.get('production', False)
    
    # Determine YOLO version
    version = "yolo11" if production else "yolo26"
    
    # Determine speed priority
    if realtime:
        if accuracy == 'low':
            speed_priority = 'max_speed'
        elif accuracy == 'medium':
            speed_priority = 'speed'
        else:
            speed_priority = 'balanced'
    else:
        if accuracy == 'low':
            speed_priority = 'speed'
        elif accuracy == 'medium':
            speed_priority = 'balanced'
        elif accuracy == 'high':
            speed_priority = 'accuracy'
        else:  # very_high
            speed_priority = 'max_accuracy'
    
    # Adjust for memory constraints
    if memory_limit < 4:
        # Very limited memory
        if speed_priority in ['max_accuracy', 'accuracy']:
            speed_priority = 'balanced'
        size = 'n'
    elif memory_limit < 8:
        # Limited memory
        if speed_priority == 'max_accuracy':
            speed_priority = 'accuracy'
        size_map = {
            'max_speed': 'n',
            'speed': 'n',
            'balanced': 's',
            'accuracy': 'm',
            'max_accuracy': 'l'
        }
        size = size_map.get(speed_priority, 'm')
    else:
        # Ample memory
        size_map = {
            'max_speed': 'n',
            'speed': 's',
            'balanced': 'm',
            'accuracy': 'l',
            'max_accuracy': 'x'
        }
        size = size_map.get(speed_priority, 'm')
    
    # Task suffix
    task_suffixes = {
        'detect': '',
        'segment': '-seg',
        'classify': '-cls',
        'pose': '-pose',
        'obb': '-obb'
    }
    
    suffix = task_suffixes.get(task, '')
    
    model_name = f"{version}{size}{suffix}.pt"
    
    # Generate reasoning
    reasoning = []
    reasoning.append(f"Task: {task}")
    reasoning.append(f"Realtime: {realtime}")
    reasoning.append(f"Accuracy needed: {accuracy}")
    reasoning.append(f"Hardware: {hardware}")
    reasoning.append(f"Memory limit: {memory_limit}GB")
    reasoning.append(f"Production: {production}")
    reasoning.append(f"Selected: {model_name}")
    
    return {
        'model': model_name,
        'version': version,
        'size': size,
        'task': task,
        'reasoning': reasoning
    }

# ============================================================================
# MODEL SPECIFICATIONS
# ============================================================================

def get_model_specifications(version="yolo26"):
    """
    Get specifications for all models of a given version
    
    Args:
        version: YOLO version ('yolo26', 'yolo11')
    
    Returns:
        Dictionary with model specifications
    """
    # Base specifications (approximate)
    specs = {
        'n': {
            'name': 'Nano',
            'relative_speed': 5,
            'relative_accuracy': 1,
            'approx_params': '2.5M',
            'approx_size': '5MB',
            'gpu_memory': '2-4GB',
            'best_for': ['Mobile', 'Edge computing', 'Real-time']
        },
        's': {
            'name': 'Small',
            'relative_speed': 4,
            'relative_accuracy': 2,
            'approx_params': '9M',
            'approx_size': '15MB',
            'gpu_memory': '2-4GB',
            'best_for': ['General purpose', 'Balanced needs']
        },
        'm': {
            'name': 'Medium',
            'relative_speed': 3,
            'relative_accuracy': 3,
            'approx_params': '25M',
            'approx_size': '40MB',
            'gpu_memory': '4-8GB',
            'best_for': ['Server applications', 'Medium accuracy']
        },
        'l': {
            'name': 'Large',
            'relative_speed': 2,
            'relative_accuracy': 4,
            'approx_params': '50M',
            'approx_size': '85MB',
            'gpu_memory': '8+ GB',
            'best_for': ['Accuracy-first', 'High-quality detection']
        },
        'x': {
            'name': 'XLarge',
            'relative_speed': 1,
            'relative_accuracy': 5,
            'approx_params': '100M',
            'approx_size': '170MB',
            'gpu_memory': '8+ GB',
            'best_for': ['Research', 'Extreme accuracy needs']
        }
    }
    
    return specs

def print_model_comparison(version="yolo26"):
    """
    Print comparison table for models of a given version
    
    Args:
        version: YOLO version ('yolo26', 'yolo11')
    """
    specs = get_model_specifications(version)
    
    print(f"\n{version.upper()} Model Comparison")
    print("="*80)
    print(f"{'Size':6} {'Name':8} {'Speed':6} {'Accuracy':8} {'Params':10} {'Size':8} {'GPU Mem':10} {'Best For'}")
    print("-"*80)
    
    for size, spec in specs.items():
        speed_stars = '⚡' * spec['relative_speed']
        accuracy_stars = '⭐' * spec['relative_accuracy']
        best_for = ', '.join(spec['best_for'][:2])  # Show first 2
        
        print(f"{size:6} {spec['name']:8} {speed_stars:6} {accuracy_stars:8} "
              f"{spec['approx_params']:10} {spec['approx_size']:8} "
              f"{spec['gpu_memory']:10} {best_for}")
    
    print("="*80)
    print("Speed: ⚡⚡⚡⚡⚡ = Fastest, ⚡ = Slowest")
    print("Accuracy: ⭐ = Lowest, ⭐⭐⭐⭐⭐ = Highest")

# ============================================================================
# MODEL VALIDATION
# ============================================================================

def validate_model_file(model_path):
    """
    Validate a model file
    
    Args:
        model_path: Path to model file
    
    Returns:
        Dictionary with validation results
    """
    from pathlib import Path
    
    model_file = Path(model_path)
    
    results = {
        'exists': False,
        'is_file': False,
        'size_bytes': 0,
        'size_mb': 0,
        'extension': '',
        'valid_extension': False,
        'inference_test': False
    }
    
    # Check file existence
    if not model_file.exists():
        return {**results, 'error': 'File does not exist'}
    
    results['exists'] = True
    
    # Check if it's a file
    if not model_file.is_file():
        return {**results, 'error': 'Path is not a file'}
    
    results['is_file'] = True
    
    # Get file size
    size_bytes = model_file.stat().st_size
    results['size_bytes'] = size_bytes
    results['size_mb'] = size_bytes / (1024 * 1024)
    
    # Check extension
    extension = model_file.suffix.lower()
    results['extension'] = extension
    results['valid_extension'] = extension in ['.pt', '.pth']
    
    # Try to load the model (if .pt file)
    if extension == '.pt':
        try:
            from ultralytics import YOLO
            
            # Try to load the model
            model = YOLO(str(model_file))
            
            # Test basic properties
            if hasattr(model, 'names'):
                results['num_classes'] = len(model.names)
                results['class_names'] = list(model.names.values())[:5]  # First 5 classes
            
            # Try a simple inference test (with dummy data)
            import numpy as np
            dummy_image = np.random.randint(0, 255, (640, 640, 3), dtype=np.uint8)
            
            # Check if torch is available for no_grad context
            try:
                import torch
                with torch.no_grad():
                    inference_results = model(dummy_image, verbose=False)
            except ImportError:
                # If torch not available, just run inference
                inference_results = model(dummy_image, verbose=False)
            
            if inference_results:
                results['inference_test'] = True
                results['model_type'] = 'YOLO'
            
        except ImportError:
            results['error'] = "ultralytics not installed. Cannot validate model loading."
        except Exception as e:
            results['error'] = f"Model loading failed: {str(e)}"
    
    return results

def compare_models_for_task(task, models_to_compare):
    """
    Compare multiple models for a specific task
    
    Args:
        task: Task type
        models_to_compare: List of model names to compare
    
    Returns:
        Comparison results
    """
    import time
    
    # Try to import ultralytics
    try:
        from ultralytics import YOLO
        has_ultralytics = True
    except ImportError:
        print("Error: ultralytics not installed. Cannot compare models.")
        print("Install with: pip install ultralytics")
        return {model: {'success': False, 'error': 'ultralytics not installed'} for model in models_to_compare}
    
    results = {}
    
    for model_name in models_to_compare:
        print(f"\nTesting {model_name} for {task} task...")
        
        try:
            # Load model
            model = YOLO(model_name)
            
            # Create dummy image
            import numpy as np
            dummy_image = np.random.randint(0, 255, (640, 640, 3), dtype=np.uint8)
            
            # Warmup
            for _ in range(3):
                model(dummy_image, verbose=False)
            
            # Performance test
            num_runs = 5
            times = []
            
            for _ in range(num_runs):
                start_time = time.time()
                model(dummy_image, verbose=False)
                end_time = time.time()
                times.append(end_time - start_time)
            
            avg_time = sum(times) / len(times)
            fps = 1 / avg_time if avg_time > 0 else 0
            
            # Get model info
            model_info = {
                'avg_time_ms': avg_time * 1000,
                'fps': fps,
                'num_classes': len(model.names) if hasattr(model, 'names') else 0,
                'task': task,
                'success': True
            }
            
            results[model_name] = model_info
            
            print(f"  ✓ Success: {avg_time*1000:.1f} ms, {fps:.1f} FPS")
            
        except Exception as e:
            print(f"  ✗ Failed: {e}")
            results[model_name] = {
                'success': False,
                'error': str(e)
            }
    
    # Print comparison table
    print("\n" + "="*80)
    print(f"MODEL COMPARISON FOR {task.upper()} TASK")
    print("="*80)
    print(f"{'Model':30} {'Time (ms)':>10} {'FPS':>10} {'Classes':>8} {'Status':>10}")
    print("-"*80)
    
    for model_name, info in results.items():
        if info.get('success', False):
            print(f"{model_name:30} {info['avg_time_ms']:10.1f} {info['fps']:10.1f} "
                  f"{info['num_classes']:8} {'✓':>10}")
        else:
            print(f"{model_name:30} {'N/A':>10} {'N/A':>10} {'N/A':>8} {'✗':>10}")
    
    return results

# ============================================================================
# MODEL LOADING AND CACHING
# ============================================================================

def load_model_with_fallback(model_name, fallback_models=None):
    """
    Load a model with fallback options
    
    Args:
        model_name: Primary model to load
        fallback_models: List of fallback models to try
    
    Returns:
        Loaded model object or None if all fail
    """
    # Try to import ultralytics
    try:
        from ultralytics import YOLO
        has_ultralytics = True
    except ImportError:
        print("Error: ultralytics not installed. Cannot load models.")
        print("Install with: pip install ultralytics")
        return None
    
    if fallback_models is None:
        fallback_models = ['yolo26n.pt', 'yolo11n.pt']
    
    models_to_try = [model_name] + fallback_models
    
    for model_to_try in models_to_try:
        try:
            print(f"Trying to load {model_to_try}...")
            model = YOLO(model_to_try)
            print(f"✓ Successfully loaded {model_to_try}")
            return model
        except Exception as e:
            print(f"✗ Failed to load {model_to_try}: {e}")
            continue
    
    print(f"Error: Could not load any model. Tried: {models_to_try}")
    return None

def get_model_cache_info():
    """
    Get information about model cache
    
    Returns:
        Dictionary with cache information
    """
    import os
    
    cache_dir = os.path.expanduser('~/.cache/ultralytics')
    
    results = {
        'cache_dir': cache_dir,
        'exists': os.path.exists(cache_dir),
        'files': [],
        'total_size_mb': 0
    }
    
    if results['exists']:
        # List all files in cache
        for root, dirs, files in os.walk(cache_dir):
            for file in files:
                if file.endswith('.pt'):
                    file_path = os.path.join(root, file)
                    file_size = os.path.getsize(file_path)
                    
                    results['files'].append({
                        'name': file,
                        'path': file_path,
                        'size_mb': file_size / (1024 * 1024)
                    })
                    
                    results['total_size_mb'] += file_size / (1024 * 1024)
    
    return results

def clear_model_cache(older_than_days=30):
    """
    Clear old models from cache
    
    Args:
        older_than_days: Delete files older than this many days
    """
    import os
    import time
    
    cache_dir = os.path.expanduser('~/.cache/ultralytics')
    
    if not os.path.exists(cache_dir):
        print(f"Cache directory does not exist: {cache_dir}")
        return
    
    current_time = time.time()
    cutoff_time = current_time - (older_than_days * 24 * 60 * 60)
    
    deleted_files = []
    deleted_size = 0
    
    for root, dirs, files in os.walk(cache_dir):
        for file in files:
            if file.endswith('.pt'):
                file_path = os.path.join(root, file)
                file_mtime = os.path.getmtime(file_path)
                file_size = os.path.getsize(file_path)
                
                if file_mtime < cutoff_time:
                    try:
                        os.remove(file_path)
                        deleted_files.append(file)
                        deleted_size += file_size
                        print(f"Deleted: {file} ({file_size/(1024*1024):.1f} MB)")
                    except Exception as e:
                        print(f"Error deleting {file}: {e}")
    
    print(f"\nDeleted {len(deleted_files)} files, freed {deleted_size/(1024*1024):.1f} MB")

# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    print("YOLO Model Utilities")
    print("=" * 60)
    
    # Example 1: Model selection
    print("\n1. MODEL SELECTION EXAMPLES")
    print("-" * 40)
    
    # Basic selection
    model1 = select_model(task="detect", speed_priority="balanced")
    print(f"Balanced detection: {model1}")
    
    model2 = select_model(task="segment", speed_priority="max_speed")
    print(f"Fast segmentation: {model2}")
    
    model3 = select_model(task="pose", speed_priority="max_accuracy", version="yolo11")
    print(f"Accurate pose (production): {model3}")
    
    # Detailed recommendation
    print("\n2. DETAILED RECOMMENDATION")
    print("-" * 40)
    
    requirements = {
        'task': 'detect',
        'realtime': True,
        'accuracy_needed': 'medium',
        'hardware': 'gpu',
        'memory_limit': 6,
        'production': False
    }
    
    recommendation = get_model_recommendation(requirements)
    print(f"Recommended model: {recommendation['model']}")
    print("Reasoning:")
    for reason in recommendation['reasoning']:
        print(f"  - {reason}")
    
    # Model comparison
    print("\n3. MODEL COMPARISON")
    print("-" * 40)
    print_model_comparison("yolo26")
    
    # Model validation
    print("\n4. MODEL VALIDATION")
    print("-" * 40)
    print("To validate a model file:")
    print("  from model_utils import validate_model_file")
    print("  results = validate_model_file('yolo26n.pt')")
    
    # Model comparison for task
    print("\n5. MODEL COMPARISON FOR TASK")
    print("-" * 40)
    print("To compare models for a task:")
    print("  from model_utils import compare_models_for_task")
    print("  results = compare_models_for_task('detect', ['yolo26n.pt', 'yolo26s.pt'])")
    
    # Model loading with fallback
    print("\n6. MODEL LOADING WITH FALLBACK")
    print("-" * 40)
    print("To load model with fallback:")
    print("  from model_utils import load_model_with_fallback")
    print("  model = load_model_with_fallback('custom_model.pt')")
    
    # Cache management
    print("\n7. CACHE MANAGEMENT")
    print("-" * 40)
    print("To get cache info:")
    print("  from model_utils import get_model_cache_info")
    print("  cache_info = get_model_cache_info()")
    
    print("\n" + "=" * 60)
    print("Available functions:")
    print("  - select_model(): Select model based on requirements")
    print("  - get_model_recommendation(): Get detailed recommendation")
    print("  - get_model_specifications(): Get model specs")
    print("  - print_model_comparison(): Print comparison table")
    print("  - validate_model_file(): Validate model file")
    print("  - compare_models_for_task(): Compare models for task")
    print("  - load_model_with_fallback(): Load with fallback")
    print("  - get_model_cache_info(): Get cache information")
    print("  - clear_model_cache(): Clear old cache files")

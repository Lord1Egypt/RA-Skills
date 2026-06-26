#!/usr/bin/env python3
"""
YOLO Training Helpers

This script provides helper functions for YOLO training, evaluation, and model management.
Extracted from training_basics.md to save token usage.
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
# TRAINING CONFIGURATION HELPERS
# ============================================================================

def get_basic_training_config(data_path, epochs=100, imgsz=640):
    """
    Get basic training configuration
    
    Args:
        data_path: Path to dataset configuration file
        epochs: Number of training epochs
        imgsz: Input image size
    
    Returns:
        Dictionary with training configuration
    """
    return {
        'data': data_path,
        'epochs': epochs,
        'imgsz': imgsz,
        'batch': 16,
        'workers': 8,
        'device': 'cuda:0' if torch.cuda.is_available() else 'cpu',
        'project': 'runs/train',
        'name': 'exp1',
        'exist_ok': True,
        'resume': False,
    }

def get_advanced_training_config(data_path, epochs=100):
    """
    Get advanced training configuration with hyperparameters
    
    Args:
        data_path: Path to dataset configuration file
        epochs: Number of training epochs
    
    Returns:
        Dictionary with advanced training configuration
    """
    return {
        'data': data_path,
        'epochs': epochs,
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

def get_model_for_training(task='detect', size='m', version='yolo26'):
    """
    Get appropriate model for training based on task and requirements
    
    Args:
        task: Task type ('detect', 'segment', 'classify', 'pose', 'obb')
        size: Model size ('n', 's', 'm', 'l', 'x')
        version: YOLO version ('yolo26', 'yolo11')
    
    Returns:
        Model path or architecture file
    """
    # Task suffixes
    task_suffixes = {
        'detect': '',
        'segment': '-seg',
        'classify': '-cls',
        'pose': '-pose',
        'obb': '-obb'
    }
    
    suffix = task_suffixes.get(task, '')
    model_name = f"{version}{size}{suffix}.pt"
    
    print(f"Recommended model for {task} task with {size} size: {model_name}")
    return model_name

# ============================================================================
# MODEL EVALUATION HELPERS
# ============================================================================

def evaluate_model(model_path, data_path, imgsz=640):
    """
    Evaluate trained model
    
    Args:
        model_path: Path to trained model
        data_path: Path to dataset configuration
        imgsz: Image size for evaluation
    
    Returns:
        Dictionary with evaluation metrics
    """
    # Try to import ultralytics
    try:
        from ultralytics import YOLO
        has_ultralytics = True
    except ImportError:
        print("Error: ultralytics not installed. Cannot evaluate model.")
        print("Install with: pip install ultralytics")
        return {'error': 'ultralytics not installed'}
    
    try:
        # Load model
        model = YOLO(model_path)
        
        # Evaluate on validation set
        metrics = model.val(
            data=data_path,
            imgsz=imgsz,
            batch=32,
            conf=0.001,
            iou=0.6,
            device='cuda:0' if torch.cuda.is_available() else 'cpu',
            half=True,
            dnn=False,
            plots=True,
            save_json=True,
            save_hybrid=False,
        )
        
        # Extract key metrics
        results = {
            'mAP50': metrics.box.map50 if hasattr(metrics.box, 'map50') else 0,
            'mAP50_95': metrics.box.map if hasattr(metrics.box, 'map') else 0,
            'precision': metrics.box.p if hasattr(metrics.box, 'p') else 0,
            'recall': metrics.box.r if hasattr(metrics.box, 'r') else 0,
            'f1_score': 2 * (metrics.box.p * metrics.box.r) / (metrics.box.p + metrics.box.r + 1e-16) if hasattr(metrics.box, 'p') and hasattr(metrics.box, 'r') else 0,
        }
        
        print("Evaluation Results:")
        print(f"  mAP@0.5: {results['mAP50']:.3f}")
        print(f"  mAP@0.5:0.95: {results['mAP50_95']:.3f}")
        print(f"  Precision: {results['precision']:.3f}")
        print(f"  Recall: {results['recall']:.3f}")
        print(f"  F1 Score: {results['f1_score']:.3f}")
        
        return results
        
    except Exception as e:
        print(f"Error evaluating model: {e}")
        return {'error': str(e)}

def compare_models(model_paths, data_path, imgsz=640):
    """
    Compare multiple models
    
    Args:
        model_paths: List of model paths to compare
        data_path: Path to dataset configuration
        imgsz: Image size for evaluation
    
    Returns:
        Dictionary with comparison results
    """
    results = {}
    
    for model_path in model_paths:
        model_name = Path(model_path).stem
        print(f"\nEvaluating {model_name}...")
        
        try:
            metrics = evaluate_model(model_path, data_path, imgsz)
            results[model_name] = metrics
        except Exception as e:
            print(f"Error evaluating {model_name}: {e}")
            results[model_name] = {'error': str(e)}
    
    # Print comparison table
    print("\n" + "="*80)
    print("MODEL COMPARISON")
    print("="*80)
    print(f"{'Model':30} {'mAP50':>8} {'mAP50-95':>8} {'Precision':>10} {'Recall':>8} {'F1':>8}")
    print("-"*80)
    
    for model_name, metrics in results.items():
        if 'error' not in metrics:
            print(f"{model_name:30} {metrics['mAP50']:8.3f} {metrics['mAP50_95']:8.3f} "
                  f"{metrics['precision']:10.3f} {metrics['recall']:8.3f} {metrics['f1_score']:8.3f}")
        else:
            print(f"{model_name:30} {'ERROR':>8} {'ERROR':>8} {'ERROR':>10} {'ERROR':>8} {'ERROR':>8}")
    
    return results

# ============================================================================
# HYPERPARAMETER TUNING HELPERS
# ============================================================================

def tune_learning_rate(model_path, data_path, epochs=30):
    """
    Tune learning rate for a model
    
    Args:
        model_path: Path to model
        data_path: Path to dataset configuration
        epochs: Number of epochs for tuning
    """
    # Try to import ultralytics
    try:
        from ultralytics import YOLO
        has_ultralytics = True
    except ImportError:
        print("Error: ultralytics not installed. Cannot tune learning rate.")
        print("Install with: pip install ultralytics")
        return
    
    try:
        model = YOLO(model_path)
        
        # Run learning rate finder
        model.tune(
            data=data_path,
            epochs=epochs,
            iterations=300,
            optimizer='AdamW',
            plots=True,
            save=True,
            val=True,
        )
        
        print("Learning rate tuning complete. Check results in runs/tune/")
        
    except Exception as e:
        print(f"Error tuning learning rate: {e}")

def evolve_hyperparameters(model_path, data_path, epochs=100):
    """
    Evolve hyperparameters using genetic algorithm
    
    Args:
        model_path: Path to model
        data_path: Path to dataset configuration
        epochs: Number of epochs for evolution
    """
    # Try to import ultralytics
    try:
        from ultralytics import YOLO
        has_ultralytics = True
    except ImportError:
        print("Error: ultralytics not installed. Cannot evolve hyperparameters.")
        print("Install with: pip install ultralytics")
        return
    
    try:
        model = YOLO(model_path)
        
        # Train with hyperparameter evolution
        model.train(
            data=data_path,
            epochs=epochs,
            evolve=True,            # Enable hyperparameter evolution
            evolve_population=300,  # Population size
            evolve_generations=10,  # Number of generations
            evolve_mutation=0.1,    # Mutation rate
            evolve_crossover=0.5,   # Crossover rate
            evolve_elite=0.1,       # Elite fraction
        )
        
        print("Hyperparameter evolution complete. Check results in runs/train/")
        
    except Exception as e:
        print(f"Error evolving hyperparameters: {e}")

# ============================================================================
# MODEL EXPORT HELPERS
# ============================================================================

def export_model(model_path, export_format='onnx', imgsz=640):
    """
    Export model to various formats
    
    Args:
        model_path: Path to trained model
        export_format: Export format
        imgsz: Image size for export
    
    Returns:
        Path to exported model or None if failed
    """
    # Try to import ultralytics
    try:
        from ultralytics import YOLO
        has_ultralytics = True
    except ImportError:
        print("Error: ultralytics not installed. Cannot export model.")
        print("Install with: pip install ultralytics")
        return None
    
    try:
        # Load model
        model = YOLO(model_path)
        
        # Export options
        export_options = {
            'format': export_format,
            'imgsz': imgsz,
        }
        
        # Format-specific options
        if export_format == 'onnx':
            export_options['simplify'] = True
            export_options['dynamic'] = True
        elif export_format == 'tensorrt':
            export_options['half'] = True
            export_options['workspace'] = 4
        elif export_format == 'openvino':
            export_options['half'] = False
        
        # Export model
        exported_path = model.export(**export_options)
        
        print(f"Model exported to {export_format.upper()} format: {exported_path}")
        return exported_path
        
    except Exception as e:
        print(f"Error exporting model to {export_format}: {e}")
        return None

def export_to_all_formats(model_path, imgsz=640):
    """
    Export model to all supported formats
    
    Args:
        model_path: Path to trained model
        imgsz: Image size for export
    
    Returns:
        Dictionary with paths to exported models
    """
    formats = [
        'torchscript',
        'onnx',
        'openvino',
        'tensorrt',
        'coreml',
        'saved_model',
        'tflite',
    ]
    
    exported_models = {}
    
    for fmt in formats:
        try:
            print(f"\nExporting to {fmt.upper()}...")
            exported_path = export_model(model_path, fmt, imgsz)
            exported_models[fmt] = exported_path
        except Exception as e:
            print(f"Error exporting to {fmt}: {e}")
            exported_models[fmt] = None
    
    print("\n" + "="*80)
    print("EXPORT SUMMARY")
    print("="*80)
    
    for fmt, path in exported_models.items():
        status = "✅ SUCCESS" if path else "❌ FAILED"
        print(f"{fmt:15}: {status} - {path if path else 'Export failed'}")
    
    return exported_models

# ============================================================================
# TRAINING MONITORING HELPERS
# ============================================================================

def monitor_training(run_dir):
    """
    Monitor training progress
    
    Args:
        run_dir: Training run directory (e.g., 'runs/train/exp1')
    """
    from pathlib import Path
    
    run_path = Path(run_dir)
    
    # Check for results file
    results_file = run_path / 'results.csv'
    
    if not results_file.exists():
        print(f"Results file not found: {results_file}")
        return
    
    # Try to import required libraries
    try:
        import pandas as pd
        has_pandas = True
    except ImportError:
        print("Error: pandas not installed. Cannot load training results.")
        print("Install with: pip install pandas")
        return
    
    try:
        import matplotlib.pyplot as plt
        has_matplotlib = True
    except ImportError:
        print("Error: matplotlib not installed. Cannot plot training metrics.")
        print("Install with: pip install matplotlib")
        # Can still load and show data without plots
        has_matplotlib = False
    
    # Load results
    results = pd.read_csv(results_file)
    
    if has_matplotlib:
        # Plot training metrics
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        
        # Plot 1: Loss components
        if 'train/box_loss' in results.columns:
            axes[0, 0].plot(results['epoch'], results['train/box_loss'], label='Box Loss')
        if 'train/cls_loss' in results.columns:
            axes[0, 0].plot(results['epoch'], results['train/cls_loss'], label='Class Loss')
        if 'train/dfl_loss' in results.columns:
            axes[0, 0].plot(results['epoch'], results['train/dfl_loss'], label='DFL Loss')
        axes[0, 0].set_title('Training Loss Components')
        axes[0, 0].set_xlabel('Epoch')
        axes[0, 0].set_ylabel('Loss')
        axes[0, 0].legend()
        axes[0, 0].grid(True)
        
        # Plot 2: Validation metrics
        if 'metrics/mAP50(B)' in results.columns:
            axes[0, 1].plot(results['epoch'], results['metrics/mAP50(B)'], label='mAP50')
        if 'metrics/mAP50-95(B)' in results.columns:
            axes[0, 1].plot(results['epoch'], results['metrics/mAP50-95(B)'], label='mAP50-95')
        axes[0, 1].set_title('Validation mAP')
        axes[0, 1].set_xlabel('Epoch')
        axes[0, 1].set_ylabel('mAP')
        axes[0, 1].legend()
        axes[0, 1].grid(True)
        
        # Plot 3: Precision and Recall
        if 'metrics/precision(B)' in results.columns:
            axes[0, 2].plot(results['epoch'], results['metrics/precision(B)'], label='Precision')
        if 'metrics/recall(B)' in results.columns:
            axes[0, 2].plot(results['epoch'], results['metrics/recall(B)'], label='Recall')
        axes[0, 2].set_title('Precision & Recall')
        axes[0, 2].set_xlabel('Epoch')
        axes[0, 2].set_ylabel('Score')
        axes[0, 2].legend()
        axes[0, 2].grid(True)
        
        # Plot 4: Learning rate
        if 'lr/pg0' in results.columns:
            axes[1, 0].plot(results['epoch'], results['lr/pg0'], label='LR')
            axes[1, 0].set_title('Learning Rate')
            axes[1, 0].set_xlabel('Epoch')
            axes[1, 0].set_ylabel('Learning Rate')
            axes[1, 0].grid(True)
        else:
            axes[1, 0].axis('off')
            axes[1, 0].text(0.5, 0.5, 'Learning Rate\nData Not Available', 
                           ha='center', va='center', fontsize=12)
        
        # Plot 5: GPU memory (if available)
        gpu_columns = [col for col in results.columns if 'mem' in col.lower()]
        if gpu_columns:
            for col in gpu_columns:
                axes[1, 1].plot(results['epoch'], results[col], label=col)
            axes[1, 1].set_title('GPU Memory Usage')
            axes[1, 1].set_xlabel('Epoch')
            axes[1, 1].set_ylabel('Memory (GB)')
            axes[1, 1].legend()
            axes[1, 1].grid(True)
        else:
            axes[1, 1].axis('off')
            axes[1, 1].text(0.5, 0.5, 'GPU Memory\nData Not Available', 
                           ha='center', va='center', fontsize=12)
        
        # Plot 6: Empty or custom
        axes[1, 2].axis('off')
        axes[1, 2].text(0.5, 0.5, f"Training Directory:\n{run_dir}", 
                       ha='center', va='center', fontsize=12)
        
        plt.tight_layout()
        plt.show()
    else:
        # If matplotlib not available, just print summary
        print("Training results loaded. Install matplotlib for visualization.")
    
    # Print summary statistics
    print("\nTRAINING SUMMARY")
    print("="*60)
    
    if 'metrics/mAP50(B)' in results.columns:
        best_epoch = results['metrics/mAP50(B)'].idxmax()
        best_map50 = results['metrics/mAP50(B)'].max()
        print(f"Best mAP50: {best_map50:.3f} at epoch {best_epoch}")
    
    if 'metrics/mAP50-95(B)' in results.columns:
        best_map = results['metrics/mAP50-95(B)'].max()
        print(f"Best mAP50-95: {best_map:.3f}")
    
    print(f"Total epochs: {len(results)}")
    print(f"Results file: {results_file}")

# ============================================================================

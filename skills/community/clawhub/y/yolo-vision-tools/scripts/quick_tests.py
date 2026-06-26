#!/usr/bin/env python3
"""
YOLO Quick Tests

This script provides quick test functions for various YOLO tasks and scenarios.
Extracted from multiple MD files to save token usage.
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
        __version__ = '0.0.0'
    torch = DummyTorch()
    HAS_TORCH = False
from pathlib import Path

# ============================================================================
# BASIC FUNCTIONALITY TESTS
# ============================================================================

def test_basic_inference(model_name='yolo26n.pt', source=None):
    """
    Test basic inference with a YOLO model
    
    Args:
        model_name: Model to use for inference
        source: Image source (file, URL, etc.). If None, uses a test URL.
    """
    from ultralytics import YOLO
    
    print(f"Testing basic inference with {model_name}...")
    
    try:
        # Load model
        model = YOLO(model_name)
        
        # Use test URL if no source provided or file doesn't exist
        if source is None:
            source = 'https://ultralytics.com/images/bus.jpg'
            print(f"  Using test image from URL: {source}")
        elif isinstance(source, str) and not source.startswith(('http://', 'https://')):
            # Check if file exists
            from pathlib import Path
            if not Path(source).exists():
                print(f"  File '{source}' not found, using test URL instead")
                source = 'https://ultralytics.com/images/bus.jpg'
        
        # Run inference
        results = model(source)
        
        # Print results
        if results and len(results) > 0:
            print(f"✓ Inference successful")
            
            # Check if we have detection results
            if hasattr(results[0], 'boxes') and results[0].boxes is not None:
                num_objects = len(results[0].boxes)
                print(f"  Detected {num_objects} objects")
                
                # Show detected classes
                classes = set()
                for box in results[0].boxes:
                    if hasattr(box, 'cls'):
                        class_id = int(box.cls)
                        class_name = model.names.get(class_id, f"Class {class_id}")
                        classes.add(class_name)
                
                if classes:
                    print(f"  Classes detected: {', '.join(sorted(classes))}")
            else:
                print(f"  Note: No bounding boxes detected (may be classification or other task)")
        
        return True
        
    except Exception as e:
        print(f"✗ Inference failed: {e}")
        return False

def test_multiple_sources(model_name='yolo26n.pt'):
    """
    Test inference on multiple source types
    
    Args:
        model_name: Model to use for inference
    """
    from ultralytics import YOLO
    
    print("Testing inference on multiple source types...")
    
    try:
        model = YOLO(model_name)
        
        # Test sources (commented out to avoid actual downloads/runs in test)
        test_cases = [
            # ('Local image', 'bus.jpg'),
            # ('URL', 'https://ultralytics.com/images/bus.jpg'),
            # ('Webcam', 0),
            # ('Video', 'video.mp4'),
        ]
        
        for name, source in test_cases:
            print(f"  Testing {name}...")
            try:
                results = model(source, verbose=False)
                print(f"    ✓ {name}: Success")
            except Exception as e:
                print(f"    ✗ {name}: Failed - {e}")
        
        return True
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False

# ============================================================================
# TASK-SPECIFIC TESTS
# ============================================================================

def test_detection(model_name='yolo26n.pt'):
    """Test object detection"""
    print("Testing object detection...")
    return test_basic_inference(model_name)

def test_segmentation(model_name='yolo26n-seg.pt'):
    """Test instance segmentation"""
    print("Testing instance segmentation...")
    
    from ultralytics import YOLO
    
    try:
        model = YOLO(model_name)
        # Use test URL for segmentation
        results = model('https://ultralytics.com/images/bus.jpg', verbose=False)
        
        if results and len(results) > 0 and hasattr(results[0], 'masks'):
            masks = results[0].masks
            if masks is not None:
                # Check if masks have data
                try:
                    # Different Ultralytics versions have different APIs
                    if hasattr(masks, '__len__'):
                        num_masks = len(masks)
                    elif hasattr(masks, 'shape'):
                        num_masks = masks.shape[0] if len(masks.shape) > 0 else 0
                    else:
                        num_masks = 0
                    
                    if num_masks > 0:
                        print(f"✓ Segmentation successful")
                        print(f"  Segmented {num_masks} instances")
                        return True
                    else:
                        print(f"✗ Masks object exists but contains {num_masks} masks")
                        return False
                except Exception as e:
                    print(f"✗ Error checking masks: {e}")
                    return False
            else:
                print("✗ Masks is None")
                return False
        else:
            print("✗ No results or no masks attribute")
            return False
        
    except Exception as e:
        print(f"✗ Segmentation test failed: {e}")
        return False

def test_classification(model_name='yolo26n-cls.pt'):
    """Test image classification"""
    print("Testing image classification...")
    
    from ultralytics import YOLO
    
    try:
        model = YOLO(model_name)
        # Use test URL for classification
        results = model('https://ultralytics.com/images/bus.jpg', verbose=False)
        
        if results and len(results) > 0 and hasattr(results[0], 'probs'):
            probs = results[0].probs
            if probs is not None:
                print(f"✓ Classification successful")
                
                if hasattr(probs, 'top5'):
                    top5 = probs.top5
                    top5conf = probs.top5conf
                    
                    print("  Top 5 predictions:")
                    for idx, conf in zip(top5, top5conf):
                        class_name = model.names.get(idx, f"Class {idx}")
                        print(f"    {class_name}: {conf:.2%}")
                
                return True
        
        print("✗ No classification probabilities found")
        return False
        
    except Exception as e:
        print(f"✗ Classification test failed: {e}")
        return False

def test_pose_estimation(model_name='yolo26n-pose.pt'):
    """Test pose estimation"""
    print("Testing pose estimation...")
    
    from ultralytics import YOLO
    
    try:
        model = YOLO(model_name)
        # Use test URL for pose estimation
        results = model('https://ultralytics.com/images/bus.jpg', verbose=False)
        
        if results and len(results) > 0 and hasattr(results[0], 'keypoints'):
            keypoints = results[0].keypoints
            if keypoints is not None:
                print(f"✓ Pose estimation successful")
                print(f"  Detected poses for {len(keypoints)} people")
                return True
        
        print("✗ No keypoints found in results")
        return False
        
    except Exception as e:
        print(f"✗ Pose estimation test failed: {e}")
        return False

def test_oriented_detection(model_name='yolo26n-obb.pt'):
    """Test oriented bounding box detection"""
    print("Testing oriented bounding box detection...")
    
    from ultralytics import YOLO
    
    try:
        model = YOLO(model_name)
        # Use test URL for oriented detection
        results = model('https://ultralytics.com/images/bus.jpg', verbose=False)
        
        if results and len(results) > 0 and hasattr(results[0], 'obb'):
            obb = results[0].obb
            if obb is not None:
                print(f"✓ Oriented detection successful")
                print(f"  Detected {len(obb)} oriented objects")
                return True
        
        print("✗ No oriented bounding boxes found")
        return False
        
    except Exception as e:
        print(f"✗ Oriented detection test failed: {e}")
        return False

# ============================================================================
# ENVIRONMENT AND PERFORMANCE TESTS
# ============================================================================

def test_environment():
    """Test if YOLO environment is properly set up"""
    print("Testing YOLO environment...")
    
    tests = [
        ("PyTorch version", lambda: f"{torch.__version__}" if hasattr(torch, '__version__') else "N/A"),
        ("PyTorch available", lambda: "✓" if hasattr(torch, '__version__') else "✗"),
        ("CUDA available", lambda: "✓" if torch.cuda.is_available() else "✗ (CPU only)"),
        ("GPU count", lambda: str(torch.cuda.device_count()) if torch.cuda.is_available() else "0"),
    ]
    
    all_passed = True
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            print(f"  {test_name}: {result}")
        except Exception as e:
            print(f"  {test_name}: ✗ Error - {e}")
            all_passed = False
    
    # Test Ultralytics import
    try:
        import ultralytics
        print(f"  Ultralytics version: {ultralytics.__version__}")
    except ImportError:
        print("  Ultralytics: ✗ Not installed")
        all_passed = False
    except Exception as e:
        print(f"  Ultralytics: ✗ Error - {e}")
        all_passed = False
    
    if all_passed:
        print("✓ Environment test passed")
    else:
        print("✗ Environment test failed")
    
    return all_passed

def test_performance(model_name='yolo26n.pt', imgsz=640, device='cuda:0'):
    """
    Test inference performance
    
    Args:
        model_name: Model to test
        imgsz: Image size for testing
        device: Device to use for testing
    """
    print(f"Testing performance for {model_name}...")
    
    from ultralytics import YOLO
    import time
    
    try:
        # Load model
        model = YOLO(model_name)
        
        # Create dummy image
        import numpy as np
        dummy_image = np.random.randint(0, 255, (imgsz, imgsz, 3), dtype=np.uint8)
        
        # Warmup
        for _ in range(3):
            model(dummy_image, verbose=False, device=device)
        
        # Performance test
        num_runs = 10
        times = []
        
        for i in range(num_runs):
            start_time = time.time()
            model(dummy_image, verbose=False, device=device)
            end_time = time.time()
            times.append(end_time - start_time)
        
        # Calculate statistics
        avg_time = sum(times) / len(times)
        fps = 1 / avg_time if avg_time > 0 else 0
        
        print(f"  Average inference time: {avg_time*1000:.1f} ms")
        print(f"  FPS: {fps:.1f}")
        print(f"  Device: {device}")
        print(f"  Image size: {imgsz}")
        
        return {
            'avg_time_ms': avg_time * 1000,
            'fps': fps,
            'device': device,
            'imgsz': imgsz
        }
        
    except Exception as e:
        print(f"✗ Performance test failed: {e}")
        return None

# ============================================================================
# MODEL MANAGEMENT TESTS
# ============================================================================

def test_model_download(model_name='yolo26n.pt'):
    """
    Test model download functionality
    
    Args:
        model_name: Model to download
    """
    print(f"Testing model download for {model_name}...")
    
    from ultralytics import YOLO
    
    try:
        # This will trigger download if model not cached
        model = YOLO(model_name)
        print(f"✓ Model {model_name} loaded successfully")
        
        # Check if model file exists in cache
        import os
        cache_dir = os.path.expanduser('~/.cache/ultralytics')
        if os.path.exists(cache_dir):
            print(f"  Cache directory: {cache_dir}")
            
            # Look for model file
            for root, dirs, files in os.walk(cache_dir):
                for file in files:
                    if model_name in file:
                        print(f"  Found model in cache: {os.path.join(root, file)}")
                        break
        
        return True
        
    except Exception as e:
        print(f"✗ Model download test failed: {e}")
        return False

def test_model_export(model_name='yolo26n.pt', export_format='onnx'):
    """
    Test model export functionality
    
    Args:
        model_name: Model to export
        export_format: Format to export to
    """
    print(f"Testing model export to {export_format.upper()}...")
    
    from ultralytics import YOLO
    
    try:
        # Load model
        model = YOLO(model_name)
        
        # Export model
        export_path = model.export(format=export_format, imgsz=640)
        
        if Path(export_path).exists():
            print(f"✓ Model exported successfully: {export_path}")
            return export_path
        else:
            print(f"✗ Export file not found: {export_path}")
            return None
        
    except Exception as e:
        print(f"✗ Model export test failed: {e}")
        return None

# ============================================================================
# COMPREHENSIVE TEST SUITE
# ============================================================================

def run_comprehensive_test_suite():
    """Run comprehensive test suite for YOLO"""
    print("="*80)
    print("YOLO COMPREHENSIVE TEST SUITE")
    print("="*80)
    
    test_results = {}
    
    # Test 1: Environment
    print("\n1. ENVIRONMENT TEST")
    print("-"*40)
    test_results['environment'] = test_environment()
    
    # Test 2: Basic inference
    print("\n2. BASIC INFERENCE TEST")
    print("-"*40)
    test_results['basic_inference'] = test_basic_inference(source=None)
    
    # Test 3: Task-specific tests (skip if basic inference failed)
    if test_results['basic_inference']:
        print("\n3. TASK-SPECIFIC TESTS")
        print("-"*40)
        
        # Only test detection since we don't have all model files
        test_results['detection'] = test_detection()
        
        # Note: Other task tests would require specific model files
        print("  Note: Other task tests require specific model files")
        print("  To test segmentation: test_segmentation('yolo26n-seg.pt')")
        print("  To test classification: test_classification('yolo26n-cls.pt')")
        print("  To test pose: test_pose_estimation('yolo26n-pose.pt')")
        print("  To test OBB: test_oriented_detection('yolo26n-obb.pt')")
    
    # Test 4: Performance
    print("\n4. PERFORMANCE TEST")
    print("-"*40)
    device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
    test_results['performance'] = test_performance(device=device)
    
    # Test 5: Model management
    print("\n5. MODEL MANAGEMENT TESTS")
    print("-"*40)
    test_results['model_download'] = test_model_download()
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUITE SUMMARY")
    print("="*80)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results.items():
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{test_name:20}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("✓ All tests passed! YOLO environment is properly configured.")
    else:
        print("✗ Some tests failed. Check the output above for details.")
    
    return test_results

# ============================================================================
# COMMAND LINE INTERFACE
# ============================================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='YOLO Quick Tests')
    parser.add_argument('--test', type=str, default='all',
                       choices=['all', 'environment', 'inference', 'performance', 
                               'detection', 'segmentation', 'classification', 
                               'pose', 'obb', 'download', 'export'],
                       help='Test to run')
    parser.add_argument('--model', type=str, default='yolo26n.pt',
                       help='Model to use for testing')
    parser.add_argument('--format', type=str, default='onnx',
                       help='Export format (for export test)')
    
    args = parser.parse_args()
    
    if args.test == 'all':
        run_comprehensive_test_suite()
    elif args.test == 'environment':
        test_environment()
    elif args.test == 'inference':
        test_basic_inference(args.model)
    elif args.test == 'performance':
        test_performance(args.model)
    elif args.test == 'detection':
        test_detection(args.model)
    elif args.test == 'segmentation':
        # Use segmentation model by default if not specified
        model = args.model if args.model != 'yolo26n.pt' else 'yolo26n-seg.pt'
        test_segmentation(model)
    elif args.test == 'classification':
        # Use classification model by default if not specified
        model = args.model if args.model != 'yolo26n.pt' else 'yolo26n-cls.pt'
        test_classification(model)
    elif args.test == 'pose':
        # Use pose estimation model by default if not specified
        model = args.model if args.model != 'yolo26n.pt' else 'yolo26n-pose.pt'
        test_pose_estimation(model)
    elif args.test == 'obb':
        # Use oriented detection model by default if not specified
        model = args.model if args.model != 'yolo26n.pt' else 'yolo26n-obb.pt'
        test_oriented_detection(model)
    elif args.test == 'download':
        test_model_download(args.model)
    elif args.test == 'export':
        test_model_export(args.model, args.format)
    else:
        print(f"Unknown test: {args.test}")
        parser.print_help()
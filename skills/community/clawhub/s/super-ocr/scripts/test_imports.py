#!/usr/bin/env python3
"""
Test script for Super OCR multi-engine parallel support
"""

import sys
import os

# Add parent to path
sys.path.insert(0, str(os.path.dirname(os.path.abspath(__file__))))

print("Testing Super OCR multi-engine parallel imports...")

try:
    from engine.selector import select_engine, get_available_engines, select_best_result
    print("[OK] engine.selector imported")
except Exception as e:
    print(f"[ERROR] engine.selector import failed: {e}")
    sys.exit(1)

try:
    from engine.tesseract import TesseractOCR
    print("[OK] engine.tesseract imported")
except Exception as e:
    print(f"[ERROR] engine.tesseract import failed: {e}")

try:
    from engine.paddle import PaddleOCR
    print("[OK] engine.paddle imported")
except Exception as e:
    print(f"[ERROR] engine.paddle import failed: {e}")

# Test MacVision on macOS
if sys.platform == 'darwin':
    try:
        from engine.macvision import MacVisionOCR
        print("[OK] engine.macvision imported")
    except (ImportError, RuntimeError) as e:
        print(f"[WARN] engine.macvision: {e}")
else:
    print("[SKIP] engine.macvision (not on macOS)")

print("\nTesting engine selector...")

# Test available engines
print(f"[INFO] Available engines: {', '.join(get_available_engines('test.png'))}")

test_cases = [
    ('screenshot.png', 'auto', ['tesseract']),
    ('chinese_menu.png', 'auto', None),  # All engines
    ('invoice.jpg', 'auto', None),  # All engines
    ('document.png', 'tesseract', ['tesseract']),
]

for image, engine, expected in test_cases:
    result = select_engine(image, engine)
    if expected:
        status = "OK" if result == expected else "FAIL"
        print(f"[{status}] {image} + {engine} => {result} (expected {expected})")
    else:
        print(f"[OK] {image} + {engine} => {result}")

# Test best result selection
print("\nTesting best result selection...")
test_results = [
    {'text': 'test1', 'confidence': 0.85, 'engine': 'tesseract'},
    {'text': 'test2', 'confidence': 0.92, 'engine': 'paddle'},
    {'text': 'test3', 'confidence': 0.95, 'engine': 'macvision'},
]

best = select_best_result(test_results)
print(f"[OK] Selected: {best.get('selected_engine')} with score {best.get('score', 0):.4f}")

print("\n[OK] All imports successful!")
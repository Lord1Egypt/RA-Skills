#!/usr/bin/env python3
"""
Dependencies checker and auto-installer for Super OCR

This module handles:
- Dependency detection
- Auto-installation of missing packages
- Version checking
- Clear error messages with troubleshooting steps
"""

import importlib.util
import os
import subprocess
import sys
from typing import Dict, List, Optional, Tuple


# Dependency definitions
DEPENDENCIES = {
    'paddleocr': {
        'package': 'paddleocr',
        'required': ['paddleocr'],
        'optional': [],
        'install_cmd': 'pip install paddleocr paddlepaddle',
        'check_fn': 'check_paddleocr'
    },
    'pytesseract': {
        'package': 'pytesseract',
        'required': ['pytesseract', 'PIL', 'cv2', 'numpy'],
        'optional': [],
        'install_cmd': 'pip install pytesseract pillow opencv-python numpy',
        'check_fn': 'check_pytesseract'
    },
    'common': {
        'package': 'common',
        'required': ['pathlib', 'argparse', 'logging'],
        'optional': ['yaml'],
        'install_cmd': None,
        'check_fn': None
    }
}


def _check_module(module_name: str) -> bool:
    """Check if a Python module is available"""
    return importlib.util.find_spec(module_name) is not None


def check_paddleocr() -> Tuple[bool, List[str]]:
    """Check PaddleOCR and paddlepaddle availability"""
    missing = []
    
    if not _check_module('paddleocr'):
        missing.append('paddleocr')
    
    # Check paddlepaddle (the actual library)
    if not _check_module('paddle'):
        missing.append('paddlepaddle')
    
    return len(missing) == 0, missing


def check_pytesseract() -> Tuple[bool, List[str]]:
    """Check Tesseract-related dependencies"""
    missing = []
    
    # Python packages
    for pkg in ['pytesseract', 'PIL', 'cv2', 'numpy']:
        if not _check_module(pkg):
            missing.append(pkg)
    
    return len(missing) == 0, missing


def check_tesseract_binary() -> Tuple[bool, str]:
    """Check if tesseract binary is installed"""
    try:
        result = subprocess.run(
            ['tesseract', '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        return True, result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError, PermissionError):
        return False, ""


def check_dependency(dep_name: str) -> Tuple[bool, List[str], Optional[str]]:
    """
    Check a specific dependency.
    
    Returns:
        (is_available, missing_items, installation_hint)
    """
    if dep_name not in DEPENDENCIES:
        return False, [], None
    
    dep = DEPENDENCIES[dep_name]
    
    # Check if we have a custom check function
    if dep.get('check_fn'):
        check_fn_name = dep['check_fn']
        check_fns = {
            'check_paddleocr': check_paddleocr,
            'check_pytesseract': check_pytesseract,
            'check_tesseract_binary': check_tesseract_binary
        }
        
        if check_fn_name in check_fns:
            is_available, result = check_fns[check_fn_name]()
            return is_available, result if isinstance(result, list) else [], None
    
    # Generic check for required packages
    missing = []
    for pkg in dep.get('required', []):
        if not _check_module(pkg):
            missing.append(pkg)
    
    return len(missing) == 0, missing, dep.get('install_cmd')


def auto_install(dependency: str) -> bool:
    """
    Auto-install a dependency.
    
    Returns:
        True if installation succeeded, False otherwise
    """
    if dependency not in DEPENDENCIES:
        print(f"[ERROR] Unknown dependency: {dependency}")
        return False
    
    dep = DEPENDENCIES[dependency]
    install_cmd = dep.get('install_cmd')
    
    if not install_cmd:
        print(f"[INFO] No auto-install command for {dependency}")
        return False
    
    print(f"[INFO] Installing {dependency}...")
    print(f"       Command: {install_cmd}")
    
    try:
        result = subprocess.run(
            install_cmd.split(),
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode == 0:
            print(f"[OK] {dependency} installed successfully")
            return True
        else:
            print(f"[ERROR] Installation failed:")
            print(f"       {result.stderr}")
            return False
            
    except Exception as e:
        print(f"[ERROR] Auto-install failed: {e}")
        return False


def print_installation_guide() -> None:
    """Print comprehensive installation instructions"""
    print("\n" + "=" * 60)
    print("Super OCR Dependencies Installation Guide")
    print("=" * 60)
    
    print("\n[OPTION 1] Install PaddleOCR (Recommended for Chinese)")
    print("-" * 40)
    print("pip install paddleocr paddlepaddle")
    print()
    print("For macOS/Linux (CPU only):")
    print("  pip install paddleocr paddlepaddle")
    print()
    print("For Windows (CPU only):")
    print("  pip install paddleocr paddlepaddle")
    print()
    print("For GPU support:")
    print("  # CUDA 11.2")
    print("  pip install paddlepaddle-gpu==2.4.0 -f https://www.paddlepaddle.org.cn/whl/stable.html")
    print("  # CUDA 11.6")
    print("  pip install paddlepaddle-gpu==2.4.0 -f https://www.paddlepaddle.org.cn/whl/lite.html")
    
    print("\n[OPTION 2] Install Tesseract")
    print("-" * 40)
    print("macOS:")
    print("  brew install tesseract")
    print()
    print("Ubuntu/Debian:")
    print("  sudo apt update && sudo apt install tesseract-ocr")
    print()
    print("Windows:")
    print("  Download from: https://github.com/UB-Mannheim/tesseract/wiki")
    
    print("\n[OPTION 3] Install Tesseract Python bindings")
    print("-" * 40)
    print("pip install pytesseract pillow opencv-python numpy")
    
    print("\n[OPTION 4] Install all at once")
    print("-" * 40)
    print("pip install paddleocr paddlepaddle pytesseract pillow opencv-python numpy")
    
    print("\n" + "=" * 60)


def check_all_dependencies(interactive: bool = True) -> bool:
    """
    Check all dependencies and optionally install missing ones.
    
    Returns:
        True if all dependencies are satisfied
    """
    print("\n" + "=" * 60)
    print("Checking Super OCR Dependencies")
    print("=" * 60)
    
    all_ok = True
    missing = []
    
    # Check PaddleOCR
    print("\n[1/3] Checking PaddleOCR...")
    ok, missing_pkgs = check_paddleocr()
    if ok:
        print("[OK] PaddleOCR is available")
    else:
        print(f"[MISSING] Missing: {', '.join(missing_pkgs)}")
        all_ok = False
        missing.extend(missing_pkgs)
    
    # Check Tesseract binary
    print("\n[2/3] Checking Tesseract binary...")
    ok, info = check_tesseract_binary()
    if ok:
        print(f"[OK] Tesseract is available: {info.split()[2] if info else 'unknown'}")
    else:
        print("[MISSING] Tesseract binary not found")
        print("  Install: brew install tesseract (macOS) or apt install tesseract-ocr (Ubuntu)")
        all_ok = False
    
    # Check Tesseract Python bindings
    print("\n[3/3] Checking Tesseract Python bindings...")
    ok, missing_pkgs = check_pytesseract()
    if ok:
        print("[OK] Tesseract Python bindings are available")
    else:
        print(f"[MISSING] Missing: {', '.join(missing_pkgs)}")
        all_ok = False
    
    # Summary
    print("\n" + "=" * 60)
    if all_ok:
        print("[OK] All dependencies satisfied!")
        return True
    else:
        print("[WARNING] Some dependencies are missing")
        print(f"Missing: {', '.join(missing)}")
        
        if interactive:
            response = input("\nAuto-install missing dependencies? [y/N]: ")
            if response.lower() == 'y':
                # Install PaddleOCR if missing
                if 'paddleocr' in missing or 'paddlepaddle' in missing:
                    print("\n[INSTALL] Installing PaddleOCR...")
                    auto_install('paddleocr')
                
                # Install Tesseract packages if missing
                if any(pkg in missing for pkg in ['pytesseract', 'PIL', 'cv2', 'numpy']):
                    print("\n[INSTALL] Installing Tesseract packages...")
                    auto_install('pytesseract')
        
        print("\n" + "=" * 60)
        print("Manual Installation:")
        print("=" * 60)
        print_installation_guide()
        
        return False


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Super OCR Dependencies Checker and Installer'
    )
    parser.add_argument(
        '--check', '-c',
        action='store_true',
        help='Check dependencies without installing'
    )
    parser.add_argument(
        '--install', '-i',
        action='store_true',
        help='Auto-install missing dependencies'
    )
    parser.add_argument(
        '--dependency', '-d',
        choices=['paddleocr', 'pytesseract', 'all'],
        default='all',
        help='Specific dependency to check/install'
    )
    parser.add_argument(
        '--guide', '-g',
        action='store_true',
        help='Show installation guide only'
    )
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Suppress output'
    )
    
    args = parser.parse_args()
    
    if args.guide:
        print_installation_guide()
        return 0
    
    if args.check or args.install:
        if args.dependency == 'all':
            success = check_all_dependencies(interactive=not args.quiet and not args.install)
        else:
            ok, missing, cmd = check_dependency(args.dependency)
            if ok:
                print(f"[OK] {args.dependency} is available")
                return 0
            else:
                print(f"[MISSING] {args.dependency}: {', '.join(missing)}")
                if args.install:
                    success = auto_install(args.dependency)
                    return 0 if success else 1
                return 1
    else:
        # Default: interactive check
        success = check_all_dependencies(interactive=True)
        return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
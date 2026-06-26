#!/usr/bin/env python3
"""
Ultralytics YOLO Environment Check Script

This script provides detailed environment information for Ultralytics YOLO,
including Python version, PyTorch configuration, CUDA availability, 
and dependency verification.

Features:
- Auto-detects Python environments (system, virtualenv, conda)
- Checks multiple Python interpreters for Ultralytics installation
- Avoids unnecessary model downloads
- Provides comprehensive environment diagnostics
"""

import sys
import platform
import subprocess
import json
import os
from pathlib import Path

def run_command(cmd):
    """Run command and return output"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr.strip()}"
    except Exception as e:
        return f"Exception: {str(e)}"

def find_python_environments():
    """Find available Python environments"""
    environments = []
    
    # Current Python
    current_python = sys.executable
    environments.append({
        'path': current_python,
        'type': 'current',
        'name': 'Current Python'
    })
    
    # Common Python paths to check
    common_paths = [
        '/usr/bin/python3',
        '/usr/local/bin/python3',
        '/opt/homebrew/bin/python3',  # macOS Homebrew
        '/opt/venv/bin/python3',      # Common virtualenv path
        '/opt/conda/bin/python3',     # Conda
        'python3',
        'python',
    ]
    
    # Check for virtual environments
    venv_paths = [
        os.path.join(os.path.expanduser('~'), '.virtualenvs'),
        os.path.join(os.path.dirname(current_python), '..', '..'),  # Parent of bin
    ]
    
    for venv_base in venv_paths:
        if os.path.exists(venv_base):
            for item in os.listdir(venv_base):
                venv_path = os.path.join(venv_base, item, 'bin', 'python3')
                if os.path.exists(venv_path):
                    common_paths.append(venv_path)
    
    # Check each path
    for path in common_paths:
        if path == current_python:
            continue
            
        try:
            # Check if Python exists and can run
            cmd = f'"{path}" -c "import sys; print(sys.version.split()[0])"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=2)
            
            if result.returncode == 0:
                version = result.stdout.strip()
                
                # Try to import ultralytics in this environment
                ultralytics_check = subprocess.run(
                    f'"{path}" -c "import ultralytics; print(ultralytics.__version__)"',
                    shell=True, capture_output=True, text=True, timeout=2
                )
                
                has_ultralytics = ultralytics_check.returncode == 0
                ultralytics_version = ultralytics_check.stdout.strip() if has_ultralytics else None
                
                env_type = 'virtualenv' if 'venv' in path or 'virtualenv' in path else 'system'
                env_type = 'conda' if 'conda' in path else env_type
                
                environments.append({
                    'path': path,
                    'type': env_type,
                    'version': version,
                    'has_ultralytics': has_ultralytics,
                    'ultralytics_version': ultralytics_version,
                    'name': f'{env_type.title()} Python ({version})'
                })
        except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
            continue
    
    return environments

def check_python():
    """Check Python environment"""
    print("=" * 60)
    print("PYTHON ENVIRONMENT")
    print("=" * 60)
    
    info = {
        "Python Version": platform.python_version(),
        "Python Implementation": platform.python_implementation(),
        "Python Executable": sys.executable,
        "Platform": platform.platform(),
        "System": platform.system(),
        "Machine": platform.machine(),
        "Processor": platform.processor(),
    }
    
    # Check virtual environment
    if hasattr(sys, 'prefix'):
        info["Python Prefix"] = sys.prefix
        if sys.prefix != sys.base_prefix:
            info["Virtual Environment"] = "YES"
            info["Virtual Env Path"] = sys.prefix
        else:
            info["Virtual Environment"] = "NO"
    
    # Check PATH for Python environments
    info["PATH Python"] = run_command("which python3 2>/dev/null || which python 2>/dev/null || echo 'Not found'")
    
    # Find other Python environments
    environments = find_python_environments()
    if len(environments) > 1:
        info["Other Python Envs"] = f"{len(environments)-1} found"
        for i, env in enumerate(environments[1:4], 1):  # Show first 3 others
            env_key = f"Env {i}"
            if env.get('has_ultralytics', False):
                env_key += " (has Ultralytics)"
            info[env_key] = f"{env['path']} - {env.get('version', 'unknown')}"
    
    for key, value in info.items():
        print(f"{key:30}: {value}")
    
    return info

def check_pytorch():
    """Check PyTorch installation and CUDA availability"""
    print("\n" + "=" * 60)
    print("PYTORCH & CUDA")
    print("=" * 60)
    
    try:
        import torch
        info = {
            "PyTorch Version": torch.__version__,
            "CUDA Available": torch.cuda.is_available(),
        }
        
        if torch.cuda.is_available():
            info["CUDA Version"] = torch.version.cuda
            info["GPU Count"] = torch.cuda.device_count()
            info["Current Device"] = torch.cuda.current_device()
            info["GPU Name"] = torch.cuda.get_device_name(0) if torch.cuda.device_count() > 0 else "No GPU"
            if torch.cuda.device_count() > 0:
                props = torch.cuda.get_device_properties(0)
                info["GPU Memory"] = f"{props.total_memory / 1e9:.2f} GB"
                info["GPU Compute Capability"] = f"{props.major}.{props.minor}"
        else:
            info["CUDA Version"] = "Not available"
            info["GPU Count"] = 0
            
            # Check for CUDA in system
            cuda_check = run_command("nvcc --version 2>/dev/null | grep release || echo 'CUDA not found in PATH'")
            if "release" in cuda_check:
                info["System CUDA"] = cuda_check.split("release")[-1].strip()
        
        # Check PyTorch build configuration
        try:
            build_info = str(torch.__config__).split('\n')
            info["PyTorch Build"] = build_info[0] if build_info else "Unknown"
        except:
            info["PyTorch Build"] = "Unknown"
        
        # Check if PyTorch was built with CUDA
        if hasattr(torch, 'version'):
            if hasattr(torch.version, 'cuda'):
                info["PyTorch CUDA Build"] = "YES" if torch.version.cuda else "NO"
        
    except ImportError:
        info = {"PyTorch Status": "NOT INSTALLED"}
        info["Recommendation"] = "Install with: pip install torch torchvision"
    except Exception as e:
        info = {"PyTorch Check Error": str(e)}
    
    for key, value in info.items():
        print(f"{key:30}: {value}")
    
    return info

def check_ultralytics():
    """Check Ultralytics YOLO installation"""
    print("\n" + "=" * 60)
    print("ULTRALYTICS YOLO")
    print("=" * 60)
    
    info = {}
    
    try:
        import ultralytics
        info["Ultralytics Version"] = ultralytics.__version__
        info["Installation Path"] = os.path.dirname(ultralytics.__file__)
        
        # Try to run yolo checks without downloading models
        try:
            from ultralytics import YOLO
            
            # Check if yolo command is available
            yolo_check = subprocess.run(
                ["yolo", "checks"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if yolo_check.returncode == 0:
                info["YOLO CLI"] = "AVAILABLE"
                # Extract key info from yolo checks
                lines = yolo_check.stdout.split('\n')
                for line in lines:
                    if 'Ultralytics' in line and 'Python' in line:
                        info["YOLO Check Summary"] = line.strip()
                        break
            else:
                info["YOLO CLI"] = "NOT AVAILABLE"
                
            # Test model loading without downloading
            # First check cache for existing models
            cache_dir = os.path.expanduser('~/.cache/ultralytics')
            has_cached_model = False
            
            if os.path.exists(cache_dir):
                for root, dirs, files in os.walk(cache_dir):
                    for file in files:
                        if file.endswith('.pt') and ('yolo26n' in file or 'yolo11n' in file):
                            has_cached_model = True
                            cached_model = os.path.join(root, file)
                            break
                    if has_cached_model:
                        break
            
            if has_cached_model:
                try:
                    # Try to load cached model
                    test_model = YOLO(cached_model)
                    info["Model Load Test"] = f"PASSED (cached: {os.path.basename(cached_model)})"
                except Exception as e:
                    info["Model Load Test"] = f"FAILED (cached): {str(e)[:100]}"
            else:
                # No cached model, just test import and basic functionality
                info["Model Load Test"] = "SKIPPED (no cached model, to avoid download)"
                info["Note"] = "Run 'yolo checks' for full test or download a model manually"
                
        except Exception as e:
            info["YOLO Check Error"] = f"{str(e)[:100]}"
            
    except ImportError:
        info["Ultralytics Status"] = "NOT INSTALLED in current Python"
        
        # Check other environments
        environments = find_python_environments()
        ultralytics_envs = [env for env in environments if env.get('has_ultralytics', False)]
        
        if ultralytics_envs:
            info["Note"] = f"Ultralytics found in {len(ultralytics_envs)} other environment(s)"
            for i, env in enumerate(ultralytics_envs[:3], 1):  # Show first 3
                info[f"Env {i} Path"] = env['path']
                info[f"Env {i} Version"] = env['ultralytics_version']
        else:
            info["Recommendation"] = "Install with: pip install ultralytics"
            
    except Exception as e:
        info["Ultralytics Check Error"] = str(e)
    
    for key, value in info.items():
        print(f"{key:30}: {value}")
    
    return info

def check_dependencies():
    """Check key dependencies"""
    print("\n" + "=" * 60)
    print("KEY DEPENDENCIES")
    print("=" * 60)
    
    dependencies = [
        ("numpy", "pip install numpy"),
        ("opencv-python", "pip install opencv-python"),
        ("matplotlib", "pip install matplotlib"), 
        ("pillow", "pip install pillow"),
        ("pyyaml", "pip install pyyaml"),
        ("requests", "pip install requests"),
        ("scipy", "pip install scipy"),
        ("pandas", "pip install pandas"),
        ("psutil", "pip install psutil"),
    ]
    
    info = {}
    missing_deps = []
    
    for dep, install_cmd in dependencies:
        try:
            module = __import__(dep)
            version = getattr(module, '__version__', 'Unknown')
            info[dep] = f"✓ {version}"
        except ImportError:
            info[dep] = "✗ NOT INSTALLED"
            missing_deps.append((dep, install_cmd))
        except Exception as e:
            info[dep] = f"Error: {str(e)[:30]}"
    
    for key, value in info.items():
        print(f"{key:30}: {value}")
    
    # Show installation commands for missing dependencies
    if missing_deps:
        print("\n" + "-" * 60)
        print("INSTALLATION COMMANDS FOR MISSING DEPENDENCIES:")
        print("-" * 60)
        for dep, install_cmd in missing_deps:
            print(f"{dep:20}: {install_cmd}")
    
    return info

def check_system_resources():
    """Check system resources"""
    print("\n" + "=" * 60)
    print("SYSTEM RESOURCES")
    print("=" * 60)
    
    info = {}
    
    try:
        import psutil
        # CPU
        info["CPU Count"] = psutil.cpu_count(logical=True)
        info["CPU Frequency"] = f"{psutil.cpu_freq().current:.0f} MHz" if psutil.cpu_freq() else "Unknown"
        info["CPU Usage"] = f"{psutil.cpu_percent(interval=1)}%"
        
        # Memory
        memory = psutil.virtual_memory()
        info["Total RAM"] = f"{memory.total / (1024**3):.2f} GB"
        info["Available RAM"] = f"{memory.available / (1024**3):.2f} GB"
        info["RAM Usage"] = f"{memory.percent}%"
        
        # Disk
        disk = psutil.disk_usage('/')
        info["Total Disk"] = f"{disk.total / (1024**3):.2f} GB"
        info["Available Disk"] = f"{disk.free / (1024**3):.2f} GB"
        info["Disk Usage"] = f"{disk.percent}%"
        
    except ImportError:
        info["psutil"] = "Not installed - resource info unavailable"
    except Exception as e:
        info["Resource Check Error"] = str(e)
    
    for key, value in info.items():
        print(f"{key:30}: {value}")
    
    return info

def generate_report(all_info):
    """Generate JSON report"""
    report_path = Path("yolo_environment_report.json")
    
    with open(report_path, 'w') as f:
        json.dump(all_info, f, indent=2)
    
    print(f"\n✅ Environment report saved to: {report_path.absolute()}")
    return report_path

def main():
    """Main function"""
    print("\n" + "=" * 60)
    print("ULTRALYTICS YOLO ENVIRONMENT DIAGNOSTICS")
    print("=" * 60)
    print("Comprehensive environment check for Ultralytics YOLO")
    print("Auto-detects Python environments and installations\n")
    
    all_info = {}
    
    # Run all checks
    all_info["python"] = check_python()
    all_info["pytorch"] = check_pytorch()
    all_info["ultralytics"] = check_ultralytics()
    all_info["dependencies"] = check_dependencies()
    all_info["resources"] = check_system_resources()
    
    # Generate summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    # Check critical components with smarter detection
    python_version = all_info["python"].get("Python Version", "0.0")
    pytorch_status = str(all_info["pytorch"].get("PyTorch Status", ""))
    ultralytics_status = str(all_info["ultralytics"].get("Ultralytics Status", ""))
    
    # Check if Ultralytics is installed in any environment
    ultralytics_found_anywhere = False
    if "Other Python Envs" in all_info["python"]:
        # Check if any other env has Ultralytics
        for key in all_info["python"]:
            if "(has Ultralytics)" in key:
                ultralytics_found_anywhere = True
                break
    
    critical_checks = {
        "Python 3.8+": tuple(map(int, python_version.split('.')[:2])) >= (3, 8),
        "PyTorch Installed": "NOT INSTALLED" not in pytorch_status,
        "CUDA Available": all_info["pytorch"].get("CUDA Available", False),
        "Ultralytics Installed": ("NOT INSTALLED" not in ultralytics_status) or ultralytics_found_anywhere,
    }
    
    all_passed = True
    for check, passed in critical_checks.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{check:30}: {status}")
        if not passed:
            all_passed = False
    
    # Recommendations
    print("\n" + "=" * 60)
    print("RECOMMENDATIONS & NEXT STEPS")
    print("=" * 60)
    
    if not critical_checks["Python 3.8+"]:
        print("❌ Upgrade Python to version 3.8 or higher")
        print("   Download from: https://www.python.org/downloads/")
    
    if not critical_checks["PyTorch Installed"]:
        print("❌ Install PyTorch:")
        print("   CPU: pip install torch torchvision")
        print("   GPU: pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118")
    
    if not critical_checks["CUDA Available"] and "PyTorch Version" in all_info["pytorch"]:
        print("⚠️  CUDA not available - using CPU only")
        print("   For GPU acceleration:")
        print("   1. Install NVIDIA drivers")
        print("   2. Install CUDA Toolkit")
        print("   3. Reinstall PyTorch with CUDA support")
    
    if not critical_checks["Ultralytics Installed"]:
        print("❌ Install Ultralytics: pip install ultralytics")
        
        # Check if Ultralytics is in another Python environment
        if "Other Python Envs" in all_info["python"]:
            print("\n   Note: Ultralytics may be installed in another Python environment.")
            print("   Try running this script with:")
            for key, value in all_info["python"].items():
                if "(has Ultralytics)" in key:
                    env_path = value.split(" - ")[0]
                    print(f"     {env_path} {__file__}")
    else:
        # Ultralytics is installed somewhere
        if "NOT INSTALLED" in ultralytics_status and ultralytics_found_anywhere:
            print("✅ Ultralytics found in another Python environment")
            print("   To use it, activate that environment or run with that Python")
            for key, value in all_info["python"].items():
                if "(has Ultralytics)" in key:
                    env_path = value.split(" - ")[0]
                    print(f"   Example: {env_path} {__file__}")
        elif "YOLO CLI" in all_info["ultralytics"] and all_info["ultralytics"]["YOLO CLI"] == "AVAILABLE":
            print("✅ Ultralytics YOLO is ready to use!")
            print("   Run: yolo checks (for detailed check)")
            print("   Run: yolo predict model=yolo26n.pt source='https://ultralytics.com/images/bus.jpg'")
    
    # Check RAM for training
    try:
        ram_str = all_info["resources"].get("Total RAM", "0 GB")
        if "GB" in ram_str:
            ram_gb = float(ram_str.split()[0])
            if ram_gb < 8:
                print(f"⚠️  Low RAM ({ram_gb:.1f} GB) - 8+ GB recommended for training")
            elif ram_gb < 16:
                print(f"⚠️  Moderate RAM ({ram_gb:.1f} GB) - 16+ GB recommended for large datasets")
            else:
                print(f"✅ Sufficient RAM ({ram_gb:.1f} GB) for training")
    except:
        pass
    
    # Environment switching advice
    print("\n" + "-" * 60)
    print("ENVIRONMENT MANAGEMENT")
    print("-" * 60)
    
    if "Virtual Environment" in all_info["python"] and all_info["python"]["Virtual Environment"] == "YES":
        print("✅ Using virtual environment:", all_info["python"].get("Virtual Env Path", "unknown"))
        print("   To deactivate: deactivate")
    else:
        print("⚠️  Not using virtual environment")
        print("   Consider using virtual environments for project isolation")
        print("   Create: python -m venv venv")
        print("   Activate: source venv/bin/activate (Linux/Mac) or venv\\Scripts\\activate (Windows)")
    
    # Generate report
    report_path = generate_report(all_info)
    
    # Final status
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ ENVIRONMENT CHECK PASSED")
        print("   Ultralytics YOLO should work correctly")
    else:
        print("❌ ENVIRONMENT CHECK FAILED")
        print("   Fix the issues above before using YOLO")
    
    print(f"\nFor more details, run: yolo checks")
    print(f"Report saved to: {report_path.absolute()}")
    print(f"\nTo run this check in another Python environment:")
    print(f"  /path/to/python {__file__}")

if __name__ == "__main__":
    main()
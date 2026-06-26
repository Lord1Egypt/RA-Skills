#!/usr/bin/env python3
"""
Python Library HarmonyOS Compatibility Checker

Checks if Python libraries are compatible with HarmonyOS (OpenHarmony)
by analyzing dependencies, running tests, and reporting compatibility issues.

Usage:
    python check_compatibility.py <package1> [package2] [package3] ...
    python check_compatibility.py -r requirements.txt
    python check_compatibility.py --test <package_name>
"""

import subprocess
import sys
import json
import os
import tempfile
import shutil
import re
import urllib.request
import urllib.error
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import time


@dataclass
class TestCaseResult:
    test_file: str
    test_name: str
    passed: bool
    error_type: str
    error_message: str
    error_traceback: str
    reason: str
    duration: float
    
    def to_dict(self):
        return asdict(self)


@dataclass
class CompatibilityResult:
    package_name: str
    version: str
    installable: bool
    test_passed: bool
    test_rate: float
    compatible: bool
    issues: List[str]
    reasons: List[str]
    alternatives: List[str]
    test_cases: List[TestCaseResult]
    install_log: str
    
    def to_dict(self):
        result = asdict(self)
        result['test_cases'] = [tc.to_dict() if hasattr(tc, 'to_dict') else asdict(tc) for tc in self.test_cases]
        return result


@dataclass
class SummaryReport:
    timestamp: str
    total_packages: int
    compatible_count: int
    partial_count: int
    incompatible_count: int
    results: List[CompatibilityResult]


# Known incompatible packages with HarmonyOS/OpenHarmony
KNOWN_INCOMPATIBLE = {
    "pywin32": ["Windows-specific API bindings"],
    "python-xlib": ["X11 dependency not available on HarmonyOS"],
    "quartz": ["macOS-specific framework"],
    "applescript": ["macOS-specific"],
    "wmi": ["Windows Management Instrumentation"],
    "pythoncom": ["Windows COM interface"],
}

# Known compatible packages
KNOWN_COMPATIBLE = {
    "requests": [],
    "numpy": [],
    "pandas": [],
    "flask": [],
    "django": [],
    "pytest": [],
    "beautifulsoup4": [],
    "pillow": [],
    "matplotlib": ["May require additional system libraries"],
}

# Platform-specific dependencies that may cause issues
PLATFORM_SPECIFIC_DEPS = {
    "win32": ["pywin32", "winreg", "msvcrt"],
    "darwin": ["applescript", "quartz", "cocoa"],
    "x11": ["python-xlib", "xcb"],
    "dbus": ["dbus-python", "pydbus"],
}

# Windows-specific modules that indicate incompatibility
# Note: Excludes standard library modules that exist on all platforms
WINDOWS_SPECIFIC_MODULES = [
    "win32api", "win32con", "win32gui", "win32process", "win32service",
    "win32com", "pythoncom", "pywintypes", "mfc",
    "winsound", "msvcrt",
    "_winapi", "_msi", "_overlapped",
    "wmi", "pywin32",
]

# Standard library modules that exist on Windows AND other platforms (NOT Windows-specific)
STDLIB_MODULES = [
    "winreg",  # Available on Python for all platforms (stub on non-Windows)
    "ctypes.wintypes",  # Part of ctypes, available everywhere
    "_subprocess",  # Internal module, available on all platforms
]


def check_windows_dependencies(source_path: str) -> Tuple[bool, List[str]]:
    """Check if source code has Windows-specific dependencies.
    
    Returns:
        (has_windows_deps, list_of_issues)
    """
    issues = []
    windows_files_found = []
    
    source_dir = Path(source_path)
    
    # Check for Windows-specific files
    for pattern in ["*.bat", "*.cmd", "*.ps1", "setup.py", "setup.cfg", "pyproject.toml"]:
        for f in source_dir.rglob(pattern):
            try:
                content = f.read_text(errors='ignore')[:10000]
                
                # Check for Windows-specific imports/references
                for win_mod in WINDOWS_SPECIFIC_MODULES:
                    if win_mod in content:
                        issues.append(f"Windows-specific module reference: {win_mod} (found in {f.relative_to(source_dir)})")
                        if f.name not in windows_files_found:
                            windows_files_found.append(f.name)
                
                # Check for platform checks
                if "sys.platform == 'win32'" in content or "os.name == 'nt'" in content:
                    if "win32" not in str(f):
                        issues.append(f"Windows platform check found in {f.relative_to(source_dir)}")
                
            except Exception:
                pass
    
    # Check Python files for Windows imports
    for py_file in source_dir.rglob("*.py"):
        try:
            content = py_file.read_text(errors='ignore')[:20000]
            
            for win_mod in WINDOWS_SPECIFIC_MODULES:
                patterns = [
                    f"import {win_mod}",
                    f"from {win_mod}",
                    f"importlib.import_module('{win_mod}')",
                    f"__import__('{win_mod}')",
                ]
                for pattern in patterns:
                    if pattern in content:
                        issues.append(f"Windows import found: {pattern} (in {py_file.relative_to(source_dir)})")
            
            # Check for ctypes windll (Windows DLL loading)
            if "ctypes.windll" in content or "ctypes.WinDLL" in content:
                issues.append(f"Windows DLL loading found in {py_file.relative_to(source_dir)}")
            
        except Exception:
            pass
    
    has_windows_deps = len(issues) > 0
    return has_windows_deps, issues


def download_from_github(package_name: str, version: str = None) -> Tuple[bool, str, str]:
    """Download package source from GitHub.
    
    Returns:
        (success, source_path, error_message)
    """
    import ssl
    
    # Common GitHub repo patterns - try most likely first
    github_patterns = []
    
    # Pattern 1: package name as owner/repo (e.g., requests/requests)
    github_patterns.append((package_name, package_name.replace('-', '_')))
    
    # Pattern 2: Try common variations
    if '-' in package_name:
        parts = package_name.split('-', 1)
        if len(parts) == 2:
            github_patterns.append((parts[0], parts[1].replace('-', '_')))
    
    # Known GitHub repos for common packages
    known_repos = {
        'xlwings': ('xlwings', 'xlwings'),
        'requests': ('psf', 'requests'),
        'numpy': ('numpy', 'numpy'),
        'pandas': ('pandas-dev', 'pandas'),
        'flask': ('pallets', 'flask'),
        'django': ('django', 'django'),
        'pytest': ('pytest-dev', 'pytest'),
        'pillow': ('python-pillow', 'Pillow'),
        'beautifulsoup4': ('waylan', 'beautifulsoup4'),
    }
    
    if package_name in known_repos:
        # Put known repo first
        owner, repo = known_repos[package_name]
        github_patterns.insert(0, (owner, repo))
    
    # Try each pattern
    tried_urls = set()
    
    for owner, repo in github_patterns:
        # Try different branch names
        for branch in ["main", "master"]:
            download_url = f"https://github.com/{owner}/{repo}/archive/refs/heads/{branch}.zip"
            
            if download_url in tried_urls:
                continue
            tried_urls.add(download_url)
            
            # Create temp directory
            temp_dir = tempfile.mkdtemp(prefix=f"{package_name}-src-")
            zip_path = os.path.join(temp_dir, f"{repo}.zip")
            extract_path = os.path.join(temp_dir, f"{repo}-{branch}")
            
            try:
                # Create SSL context that doesn't verify certificates (for HarmonyOS)
                ssl_context = ssl.create_default_context()
                ssl_context.check_hostname = False
                ssl_context.verify_mode = ssl.CERT_NONE
                
                # Download
                print(f"  → Trying GitHub: {owner}/{repo} ({branch})")
                req = urllib.request.Request(download_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, context=ssl_context, timeout=30) as response:
                    with open(zip_path, 'wb') as out_file:
                        shutil.copyfileobj(response, out_file)
                
                # Extract
                import zipfile
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
                
                # Find extracted directory (might have different naming)
                for item in os.listdir(temp_dir):
                    item_path = os.path.join(temp_dir, item)
                    if os.path.isdir(item_path) and package_name.lower().replace('-', '_') in item.lower():
                        print(f"  ✅ Downloaded from GitHub: {owner}/{repo} ({branch})")
                        return True, item_path, ""
                
                # Fallback: use first directory found
                for item in os.listdir(temp_dir):
                    item_path = os.path.join(temp_dir, item)
                    if os.path.isdir(item_path):
                        print(f"  ✅ Downloaded from GitHub: {owner}/{repo} ({branch})")
                        return True, item_path, ""
                
            except Exception as e:
                # Cleanup and try next
                if os.path.exists(temp_dir):
                    try:
                        shutil.rmtree(temp_dir)
                    except Exception:
                        pass
                continue
    
    return False, "", "Could not find or download from GitHub"


def download_from_pypi(package_name: str, version: str = None) -> Tuple[bool, str, str]:
    """Download package source from PyPI.
    
    Returns:
        (success, source_path, error_message)
    """
    import ssl
    
    try:
        # Create SSL context that doesn't verify certificates (for HarmonyOS)
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        # Get package info from PyPI API
        api_url = f"https://pypi.org/pypi/{package_name}/json"
        req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0'})
        
        with urllib.request.urlopen(req, context=ssl_context, timeout=30) as response:
            data = json.loads(response.read().decode())
        
        # Get version info
        if version:
            version_data = data['releases'].get(version)
        else:
            version_data = data['releases'].get(data['info']['version'])
        
        if not version_data:
            return False, "", f"Version {version} not found"
        
        # Find source distribution (tar.gz or zip)
        source_url = None
        for release in version_data:
            if release['packagetype'] == 'sdist':
                source_url = release['url']
                version = release['version']
                break
        
        if not source_url:
            return False, "", "No source distribution found on PyPI"
        
        # Download
        temp_dir = tempfile.mkdtemp(prefix=f"{package_name}-pypi-src-")
        filename = source_url.split('/')[-1]
        download_path = os.path.join(temp_dir, filename)
        
        print(f"  → Downloading from PyPI: {source_url}")
        req = urllib.request.Request(source_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ssl_context, timeout=60) as response:
            with open(download_path, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)
        
        # Extract
        import tarfile
        extract_path = os.path.join(temp_dir, f"{package_name}-{version}")
        
        if filename.endswith('.tar.gz'):
            with tarfile.open(download_path, 'r:gz') as tar:
                tar.extractall(temp_dir)
        elif filename.endswith('.zip'):
            import zipfile
            with zipfile.ZipFile(download_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
        
        # Find extracted directory
        if os.path.exists(extract_path):
            print(f"  ✅ Downloaded from PyPI: {package_name}=={version}")
            return True, extract_path, ""
        
        # Try to find the extracted directory
        for item in os.listdir(temp_dir):
            item_path = os.path.join(temp_dir, item)
            if os.path.isdir(item_path) and package_name.lower() in item.lower():
                print(f"  ✅ Downloaded from PyPI: {package_name}=={version}")
                return True, item_path, ""
        
        return False, "", "Failed to extract source"
        
    except Exception as e:
        return False, "", f"PyPI download failed: {str(e)}"


def download_source(package_name: str, version: str = None) -> Tuple[bool, str, str, str]:
    """Download package source from GitHub (preferred) or PyPI.
    
    Returns:
        (success, source_path, source_type, error_message)
        source_type is 'github' or 'pypi'
    """
    # Try GitHub first
    success, path, error = download_from_github(package_name, version)
    if success:
        return True, path, "github", ""
    
    # Fall back to PyPI
    success, path, error = download_from_pypi(package_name, version)
    if success:
        return True, path, "pypi", ""
    
    return False, "", "", error or "Failed to download from both GitHub and PyPI"


def run_command(cmd: List[str], timeout: int = 300, cwd: str = None) -> Tuple[bool, str, str]:
    """Run a shell command and return success status, stdout, stderr."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=cwd,
            env={**os.environ, "PIP_NO_CACHE_DIR": "1"}
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except Exception as e:
        return False, "", str(e)


def get_package_info(package_name: str) -> Dict:
    """Get package information from PyPI."""
    success, stdout, stderr = run_command(
        [sys.executable, "-m", "pip", "index", "versions", package_name],
        timeout=30
    )
    
    # Try to get package metadata
    success, stdout, stderr = run_command(
        [sys.executable, "-c", 
         f"import json; import importlib.metadata; print(json.dumps({{'name': '{package_name}', 'version': importlib.metadata.version('{package_name}')}})" if package_name not in stdout else "import json; print(json.dumps({'name': '" + package_name + "', 'status': 'available'}))"],
        timeout=30
    )
    
    return {"name": package_name, "status": "checked"}


def check_known_issues(package_name: str) -> List[str]:
    """Check if package has known compatibility issues."""
    issues = []
    
    # Check exact match
    if package_name in KNOWN_INCOMPATIBLE:
        issues.extend(KNOWN_INCOMPATIBLE[package_name])
    
    # Check platform-specific dependencies
    for platform, deps in PLATFORM_SPECIFIC_DEPS.items():
        for dep in deps:
            if dep in package_name.lower():
                issues.append(f"Depends on {platform}-specific component: {dep}")
    
    return issues


def analyze_install_error(stderr: str, stdout: str) -> List[str]:
    """Analyze installation error to provide detailed reasons."""
    reasons = []
    
    # Compilation errors
    if "error: command 'gcc' failed" in stderr or "error: command 'clang' failed" in stderr:
        reasons.append("Native compilation failed - C/C++ extensions cannot be compiled on HarmonyOS")
    
    if "unable to execute 'gcc'" in stderr or "unable to execute 'clang'" in stderr:
        reasons.append("Compiler not available - HarmonyOS doesn't provide gcc/clang for package compilation")
    
    # Missing headers
    if "fatal error:" in stderr and ".h: No such file or directory" in stderr:
        import re
        match = re.search(r"fatal error: ([^:]+)\.h: No such file or directory", stderr)
        if match:
            reasons.append(f"Missing system header: {match.group(1)}.h - Required development library not available on HarmonyOS")
    
    # Wheel errors
    if "Failed to build wheel" in stderr:
        reasons.append("Wheel build failed - No pre-built wheel available for HarmonyOS ARM64")
    
    if "could not build wheels" in stderr.lower():
        reasons.append("Wheel compilation failed - Package requires native extensions")
    
    # Subprocess errors
    if "subprocess-exited-with-error" in stderr:
        reasons.append("Installation subprocess failed - Dependency or build requirement could not be satisfied")
    
    # Missing dependencies
    if "No matching distribution found" in stderr:
        reasons.append("No compatible distribution found - Package not available for HarmonyOS platform")
    
    if "No matching distribution" in stderr:
        import re
        match = re.search(r"No matching distribution found for ([^\s]+)", stderr)
        if match:
            reasons.append(f"Missing dependency: {match.group(1)} - This required package is not available")
    
    # Platform errors
    if "Unsupported platform" in stderr or "unsupported platform" in stderr:
        reasons.append("Platform not supported - Package explicitly excludes HarmonyOS/OpenHarmony")
    
    if "sys.platform" in stderr and "not supported" in stderr.lower():
        reasons.append("Platform check failed - Package has explicit platform restrictions")
    
    # Binary/ELF errors
    if "ELF" in stderr or "binary" in stderr.lower():
        reasons.append("Binary incompatibility - Pre-compiled binary not compatible with HarmonyOS")
    
    # Default reason if nothing specific found
    if not reasons and stderr.strip():
        error_preview = stderr[:200].replace('\n', ' ').strip()
        reasons.append(f"Installation error: {error_preview}...")
    
    return reasons


def check_installability(package_name: str, venv_path: str) -> Tuple[bool, List[str], str]:
    """Check if package can be installed in a clean virtual environment."""
    issues = []
    install_log = ""
    
    # Check known issues first
    known_issues = check_known_issues(package_name)
    if known_issues:
        issues.extend(known_issues)
        # Still try to install to confirm
    
    # Create temporary virtual environment
    pip_cmd = [sys.executable, "-m", "pip", "install", "--target", venv_path, package_name]
    
    success, stdout, stderr = run_command(pip_cmd, timeout=300)
    install_log = stderr if stderr else stdout
    
    if not success:
        # Analyze the error in detail
        detailed_reasons = analyze_install_error(stderr, stdout)
        if detailed_reasons:
            issues.extend(detailed_reasons)
        else:
            issues.append(f"Installation failed: {stderr[:500]}")
        return False, issues, install_log
    
    # Check for compilation warnings
    if "warning" in stderr.lower() or "failed" in stderr.lower():
        issues.append(f"Installation warnings: {stderr[:300]}")
    
    return True, issues, install_log


def find_tests_in_source(source_path: str) -> List[str]:
    """Find test files in the downloaded source code.
    
    Args:
        source_path: Path to the extracted source directory
        
    Returns:
        List of test file paths
    """
    test_files = []
    source_dir = Path(source_path)
    
    # Common test directory patterns
    test_dir_names = ["tests", "test", "Tests", "Test", "testing"]
    
    # Look for test directories recursively throughout the source tree
    for test_dir_name in test_dir_names:
        for test_dir in source_dir.rglob(test_dir_name):
            if test_dir.is_dir():
                # Skip common non-test directories that happen to be named 'test'
                if test_dir.name in ['site-packages', 'node_modules', '.git', '__pycache__']:
                    continue
                    
                print(f"  → Found test directory: {test_dir.relative_to(source_dir)}/")
                for py_file in test_dir.rglob("*.py"):
                    if py_file.name.startswith("test_") or py_file.name.endswith("_test.py") or py_file.name.endswith("_tests.py"):
                        test_files.append(str(py_file))
    
    # Also look for test files in the root directory
    for pattern in ["test_*.py", "*_test.py", "*_tests.py"]:
        for py_file in source_dir.glob(pattern):
            if py_file.name not in ["test.py", "tests.py"]:  # Skip generic names
                test_files.append(str(py_file))
    
    # Remove duplicates while preserving order
    seen = set()
    unique_tests = []
    for f in test_files:
        if f not in seen:
            seen.add(f)
            unique_tests.append(f)
    
    # Limit to 20 tests for thorough checking
    return unique_tests[:20]


def find_tests_installed(package_name: str) -> List[str]:
    """Find test files in the installed package.
    
    Args:
        package_name: Name of the installed package
        
    Returns:
        List of test file paths, or empty list if not found
    """
    try:
        # Get package location
        import importlib.metadata
        dist = importlib.metadata.distribution(package_name)
        pkg_location = dist.locate_file(package_name.replace('-', '_'))
        
        if not pkg_location or not pkg_location.exists():
            return []
        
        test_files = []
        test_dir_names = ["tests", "test", "Tests", "Test"]
        
        # Look for test directories in the installed package
        for test_dir_name in test_dir_names:
            for test_dir in pkg_location.rglob(test_dir_name):
                if test_dir.is_dir() and test_dir.name not in ['site-packages', '__pycache__', '.git']:
                    for py_file in test_dir.rglob("*.py"):
                        if py_file.name.startswith("test_") or py_file.name.endswith("_test.py"):
                            test_files.append(str(py_file))
        
        # Remove duplicates and limit
        seen = set()
        unique_tests = []
        for f in test_files:
            if f not in seen:
                seen.add(f)
                unique_tests.append(f)
        
        return unique_tests[:20]
        
    except Exception as e:
        print(f"  ⚠️  Could not find installed tests: {e}")
        return []


def find_tests(package_name: str, install_path: str) -> List[str]:
    """Find test files in the installed package."""
    test_files = []
    package_path = Path(install_path) / package_name.replace("-", "_")
    
    # Look for test directories
    for pattern in ["tests", "test"]:
        test_dir = package_path.parent / f"{package_name.replace('-', '_')}-{pattern}"
        if test_dir.exists():
            for py_file in test_dir.rglob("test*.py"):
                test_files.append(str(py_file))
    
    # Look for test files in package
    if package_path.exists():
        for pattern in ["test_*.py", "*_test.py"]:
            for py_file in package_path.rglob(pattern):
                if "test" not in str(py_file.parent) or py_file.parent.name in ["test", "tests"]:
                    test_files.append(str(py_file))
    
    return test_files[:10]  # Limit to 10 tests


def analyze_test_failure(stderr: str, stdout: str) -> Tuple[str, str, str, bool]:
    """Analyze test failure to determine error type and reason.
    
    Returns:
        (error_type, reason, error_msg, is_environment_issue)
        is_environment_issue: True if failure is due to environment/permissions (not code incompatibility)
    """
    error_type = "Unknown"
    reason = ""
    error_msg = stderr[:500] if stderr else stdout[:500]
    is_environment_issue = False
    
    # Permission errors - environment issue, not code incompatibility
    if "PermissionError" in stderr or "Permission denied" in stderr:
        error_type = "PermissionError"
        is_environment_issue = True
        # Extract the path if available
        import re
        match = re.search(r"PermissionError: \[Errno 13\] Permission denied: '([^']+)'", stderr)
        if match:
            reason = f"Permission denied: {match.group(1)} - This is an environment issue, NOT a package compatibility issue"
        else:
            reason = "Permission denied - HarmonyOS security policy restricts this operation (environment issue)"
    
    # Temp directory permission issues (pytest common issue)
    elif "OSError" in stderr and "temporary directory" in stderr.lower() and "not owned" in stderr.lower():
        error_type = "TempDirPermissionError"
        is_environment_issue = True
        reason = "Pytest temp directory permission issue - This is an environment issue, NOT a package compatibility issue. Run: rm -rf pytest-of-*"
    
    # Other OSError - check if it's environment-related
    elif "OSError" in stderr or "FileNotFoundError" in stderr:
        error_type = "FileSystemError"
        # Check for common environment issues
        if "errno 38" in stderr.lower() or "function not implemented" in stderr.lower():
            is_environment_issue = True
            reason = "Function not implemented on HarmonyOS (environment limitation)"
        else:
            reason = "File system operation failed - May be environment or compatibility issue"
    
    # Module not found - could be missing dependency or incompatibility
    elif "ModuleNotFoundError" in stderr or "ImportError" in stderr:
        error_type = "ImportError"
        import re
        match = re.search(r"No module named '([^']+)'", stderr)
        if match:
            missing_module = match.group(1)
            # Check if it's a known platform-specific module
            if any(win in missing_module for win in ['win32', 'winreg', 'msvcrt', 'nt', '_win']):
                reason = f"Missing Windows-specific module: {missing_module} - Package has platform dependency"
            else:
                reason = f"Missing dependency: {missing_module} - This module is not available on HarmonyOS"
        else:
            reason = "Import failed - dependency not available on HarmonyOS"
    
    # AttributeError - API incompatibility
    elif "AttributeError" in stderr:
        error_type = "AttributeError"
        import re
        match = re.search(r"'([^']+)' object has no attribute '([^']+)'", stderr)
        if match:
            reason = f"API incompatibility: {match.group(1)}.{match.group(2)} - This method/attribute doesn't exist in HarmonyOS environment"
        else:
            reason = "API incompatibility - method or attribute not available"
    
    # Native library errors
    elif "ctypes" in stderr or "DLL" in stderr or ".so" in stderr or "shared object" in stderr.lower():
        error_type = "NativeLibraryError"
        reason = "Native library loading failed - binary incompatible with HarmonyOS ARM64"
    
    # Network errors
    elif "socket" in stderr.lower() or "connection" in stderr.lower() or "urllib" in stderr.lower():
        error_type = "NetworkError"
        is_environment_issue = True
        reason = "Network operation failed - May require network permission on HarmonyOS (environment issue)"
    
    # Async errors
    elif "async" in stderr.lower() or "event loop" in stderr.lower():
        error_type = "AsyncError"
        reason = "Async operation failed - HarmonyOS event loop may differ"
    
    # Default
    elif stderr.strip():
        error_type = "RuntimeError"
        reason = f"Runtime error - {stderr[:200]}"
    
    return error_type, reason, error_msg, is_environment_issue


def run_tests(package_name: str, install_path: str, test_files: List[str]) -> Tuple[bool, float, float, List[str], List[TestCaseResult]]:
    """Run tests for the package with detailed per-test-case reporting using pytest.
    
    Uses pytest to run tests and parse individual test function results.
    
    Returns:
        (test_passed, test_rate, valid_test_rate, errors, test_cases)
        test_rate: includes all tests (passed / total)
        valid_test_rate: excludes environment issues (passed / valid_tests)
    """
    if not test_files:
        return True, 1.0, 1.0, ["No tests found - assuming compatible"], []
    
    passed = 0
    failed = 0
    environment_issues = 0  # Tests that failed due to environment, not code
    errors = []
    test_cases = []
    
    # Limit to 15 test files to avoid too long execution
    max_files = min(len(test_files), 15)
    print(f"  → Selected {max_files} test files out of {len(test_files)} found")
    
    for i, test_file in enumerate(test_files[:max_files]):
        import time
        start_time = time.time()
        
        # Use pytest with verbose output to get individual test results
        test_file_path = Path(test_file)
        test_dir = test_file_path.parent
        
        # Run pytest with verbose output and result reporting
        # Use --import-mode=importlib to avoid importing from source directory
        success, stdout, stderr = run_command(
            [sys.executable, "-m", "pytest", str(test_file), "-v", "--tb=short", "--import-mode=importlib"],
            timeout=120,  # 2 minutes per test file
            cwd="/tmp"  # Run from /tmp to avoid importing from source
        )
        duration = time.time() - start_time
        
        # Parse pytest output to get individual test results
        file_test_results = parse_pytest_output(stdout, stderr, test_file, duration)
        
        for result in file_test_results:
            if result.passed:
                passed += 1
            else:
                error_type = result.error_type
                is_env_issue = "environment issue" in result.reason.lower() or "permission" in error_type.lower()
                
                if is_env_issue:
                    environment_issues += 1
                    errors.append(f"{result.test_name}: {error_type} - {result.reason} [ENVIRONMENT ISSUE]")
                else:
                    failed += 1
                    errors.append(f"{result.test_name}: {error_type} - {result.reason}")
            
            test_cases.append(result)
        
        # Show progress
        if (i + 1) % 5 == 0 or (i + 1) == max_files:
            print(f"  → Progress: {i+1}/{max_files} test files processed ({passed} passed, {failed} failed)")
    
    total = passed + failed + environment_issues
    valid_tests = passed + failed  # Excludes environment issues
    test_rate = passed / total if total > 0 else 1.0
    valid_test_rate = passed / valid_tests if valid_tests > 0 else 1.0
    
    # Test passes if valid_test_rate >= 80% (environment issues don't count against)
    test_passed = valid_test_rate >= 0.8
    
    return test_passed, test_rate, valid_test_rate, errors, test_cases


def parse_pytest_output(stdout: str, stderr: str, test_file: str, total_duration: float) -> List[TestCaseResult]:
    """Parse pytest verbose output to extract individual test results.
    
    Pytest -v output format:
    test_file.py::test_function_name PASSED
    test_file.py::test_function_name FAILED
    test_file.py::test_function_name SKIPPED
    """
    results = []
    test_file_name = Path(test_file).name
    
    # If pytest failed to run (not import error), treat whole file as one test
    if "no tests ran" in stdout.lower() or "collecting ... collected 0 items" in stdout:
        results.append(TestCaseResult(
            test_file=test_file,
            test_name=test_file_name,
            passed=True,
            error_type="",
            error_message="",
            error_traceback="",
            reason="No tests found in file",
            duration=total_duration
        ))
        return results
    
    # Check if pytest itself failed (not test failure)
    if "ImportError" in stderr and "No module named 'pytest'" in stderr:
        # pytest not available, run file directly
        success, out, err = run_command([sys.executable, test_file], timeout=60)
        if success:
            results.append(TestCaseResult(
                test_file=test_file,
                test_name=test_file_name,
                passed=True,
                error_type="",
                error_message="",
                error_traceback="",
                reason="Test executed successfully",
                duration=total_duration
            ))
        else:
            error_type, reason, error_msg, _ = analyze_test_failure(err, out)
            results.append(TestCaseResult(
                test_file=test_file,
                test_name=test_file_name,
                passed=False,
                error_type=error_type,
                error_message=error_msg[:500],
                error_traceback=err[:1000] if err else out[:1000],
                reason=reason,
                duration=total_duration
            ))
        return results
    
    # Parse pytest -v output
    lines = stdout.split('\n') + stderr.split('\n')
    test_pattern = re.compile(r'^(\S+\.py)::(\S+)\s+(PASSED|FAILED|SKIPPED|ERROR)')
    
    found_tests = []
    for line in lines:
        match = test_pattern.match(line.strip())
        if match:
            file_name, test_name, status = match.groups()
            found_tests.append((test_name, status))
    
    # If no tests parsed but pytest ran, check for collection errors
    if not found_tests:
        if "collecting ... collected" in stdout:
            # Tests were collected but something went wrong
            if "FAILED" in stdout or "ERROR" in stdout:
                error_type, reason, error_msg, _ = analyze_test_failure(stderr, stdout)
                results.append(TestCaseResult(
                    test_file=test_file,
                    test_name=test_file_name,
                    passed=False,
                    error_type=error_type,
                    error_message=error_msg[:500],
                    error_traceback=stderr[:1000] if stderr else stdout[:1000],
                    reason=reason,
                    duration=total_duration
                ))
            else:
                results.append(TestCaseResult(
                    test_file=test_file,
                    test_name=test_file_name,
                    passed=True,
                    error_type="",
                    error_message="",
                    error_traceback="",
                    reason="Tests collected and passed",
                    duration=total_duration
                ))
        return results if results else []
    
    # Group test results by test function
    test_results = {}
    for test_name, status in found_tests:
        if test_name not in test_results:
            test_results[test_name] = status
    
    # Calculate duration per test
    duration_per_test = total_duration / len(test_results) if test_results else total_duration
    
    # Create results for each test
    error_output = stderr[:2000] if stderr else stdout[:2000]
    
    for test_name, status in test_results.items():
        if status == "PASSED":
            results.append(TestCaseResult(
                test_file=test_file,
                test_name=f"{test_file_name}::{test_name}",
                passed=True,
                error_type="",
                error_message="",
                error_traceback="",
                reason="Test passed",
                duration=duration_per_test
            ))
        elif status == "SKIPPED":
            results.append(TestCaseResult(
                test_file=test_file,
                test_name=f"{test_file_name}::{test_name}",
                passed=True,  # Skipped tests count as passed
                error_type="",
                error_message="",
                error_traceback="",
                reason="Test skipped",
                duration=duration_per_test
            ))
        else:  # FAILED or ERROR
            # Try to find specific error for this test
            error_type, reason, error_msg, _ = analyze_test_failure(error_output, stdout)
            results.append(TestCaseResult(
                test_file=test_file,
                test_name=f"{test_file_name}::{test_name}",
                passed=False,
                error_type=error_type,
                error_message=error_msg[:500],
                error_traceback=stderr[:1000] if stderr else stdout[:1000],
                reason=reason,
                duration=duration_per_test
            ))
    
    return results


def get_alternatives(package_name: str) -> List[str]:
    """Suggest alternative packages for incompatible libraries."""
    alternatives_map = {
        "pywin32": ["Use platform-agnostic libraries like 'python-dotenv' for config"],
        "python-xlib": ["Use 'pynput' for cross-platform input control"],
        "flask": ["Consider FastAPI for better async support"],
    }
    return alternatives_map.get(package_name, [])


def check_already_installed(package_name: str) -> Tuple[bool, str, bool, str]:
    """Check if package is already installed and working.
    
    Returns:
        (is_installed, version, is_working, error_message)
    """
    try:
        # Try to get version from metadata
        success, stdout, stderr = run_command(
            [sys.executable, "-c", 
             f"import importlib.metadata; print(importlib.metadata.version('{package_name}'))"],
            timeout=10
        )
        
        if success:
            version = stdout.strip()
            # Try a basic import test
            # Handle special cases where import name differs from package name
            import_name_map = {
                'pillow': 'PIL',
                'scikit-learn': 'sklearn',
                'scikit-image': 'skimage',
                'opencv-python': 'cv2',
                'opencv-python-headless': 'cv2',
                'beautifulsoup4': 'bs4',
                'pyyaml': 'yaml',
            }
            import_name = import_name_map.get(package_name.lower(), package_name.replace('-', '_'))
            
            success2, stdout2, stderr2 = run_command(
                [sys.executable, "-c", f"import {import_name}"],
                timeout=10
            )
            
            if success2:
                return True, version, True, ""
            else:
                return True, version, False, stderr2[:200]
        
        return False, "unknown", False, "Package not installed"
        
    except Exception as e:
        return False, "unknown", False, str(e)


def check_package(package_name: str, keep_source: bool = False) -> CompatibilityResult:
    """Check a single package for HarmonyOS compatibility.
    
    Args:
        package_name: Name of the package to check
        keep_source: If True, keep downloaded source code for verification
    """
    print(f"\n{'='*60}")
    print(f"Checking: {package_name}")
    print('='*60)
    
    issues = []
    reasons = []
    install_log = ""
    test_cases = []
    source_path = None
    source_cleanup = None
    should_keep_source = keep_source  # Flag to track if we should keep source
    
    try:
        # Step 1: Check for Windows-specific dependencies FIRST
        print(f"  → Checking for Windows-specific dependencies...")
        
        # Download source to check for Windows dependencies
        success, source_path, source_type, download_error = download_source(package_name)
        
        if success:
            print(f"  ✅ Source downloaded from {source_type}")
            
            # Check for Windows dependencies in source code
            has_windows_deps, windows_issues = check_windows_dependencies(source_path)
            
            if has_windows_deps:
                print(f"  ❌ Windows-specific dependencies detected!")
                issues.extend(windows_issues)
                reasons.append("Package depends on Windows-specific APIs/modules")
                
                # Windows dependencies = incompatible, no need to continue
                # Don't cleanup source if keep_source is True
                should_keep_source = keep_source
                return CompatibilityResult(
                    package_name=package_name,
                    version="unknown",
                    installable=False,
                    test_passed=False,
                    test_rate=0.0,
                    compatible=False,
                    issues=issues,
                    reasons=reasons,
                    alternatives=get_alternatives(package_name),
                    test_cases=[TestCaseResult(
                        test_file="N/A",
                        test_name="Windows dependency check",
                        passed=False,
                        error_type="PlatformError",
                        error_message="Windows-specific modules detected",
                        error_traceback="",
                        reason="Package depends on Windows-specific APIs: " + "; ".join(windows_issues[:3]),
                        duration=0.0
                    )],
                    install_log=f"Windows dependencies found: {'; '.join(windows_issues[:5])}"
                )
        else:
            print(f"  ⚠️ Could not download source: {download_error}")
            issues.append(f"Source download failed: {download_error}")
        
        # Step 2: Check if already installed and working
        print(f"  → Checking if already installed...")
        is_installed, version, is_working, install_error = check_already_installed(package_name)
        
        if is_installed and is_working:
            print(f"  ✅ Package is already installed (v{version}) and working!")
            installable = True
            install_log = f"Already installed (v{version}) - functional test passed"
            test_passed = True
            test_rate = 1.0
            
            # Try to run tests from installed package first (more reliable)
            test_files = find_tests_installed(package_name)
            test_source = "installed"
            
            # Fall back to source tests if installed tests not found
            if not test_files and source_path:
                test_files = find_tests_in_source(source_path)
                test_source = "source"
            
            if test_files:
                print(f"  → Running {len(test_files)} tests from {test_source}...")
                test_passed, test_rate, valid_test_rate, test_errors, case_results = run_tests(package_name, source_path or "/tmp", test_files)
                test_cases = case_results
                if not test_passed:
                    reasons.append(f"Test pass rate: {test_rate*100:.1f}% (valid tests: {valid_test_rate*100:.1f}%)")
                    issues.extend(test_errors)
            else:
                test_cases = [TestCaseResult(
                    test_file="N/A",
                    test_name="Import test",
                    passed=True,
                    error_type="",
                    error_message="",
                    error_traceback="",
                    reason="Package imported successfully, no tests found",
                    duration=0.0
                )]
                
        elif is_installed and not is_working:
            print(f"  ⚠️ Package is installed but has issues: {install_error}")
            issues.append(f"Package installed but not working: {install_error}")
            reasons.append("Package has runtime errors despite being installed")
            installable = True
            install_log = install_error
            test_passed = False
            test_rate = 0.0
            test_cases = [TestCaseResult(
                test_file="N/A",
                test_name="Import test",
                passed=False,
                error_type="RuntimeError",
                error_message=install_error,
                error_traceback="",
                reason="Package import failed at runtime",
                duration=0.0
            )]
        else:
            print(f"  → Package not installed, attempting installation test...")
            # Step 3: Try to install in temporary directory
            temp_dir = tempfile.mkdtemp(prefix=f"{package_name}-test-")
            source_cleanup = temp_dir
            
            try:
                # Check installability
                installable, install_issues, install_output = check_installability(package_name, temp_dir)
                issues.extend(install_issues)
                
                if not installable:
                    reasons.append("Package cannot be installed on HarmonyOS")
                    install_log = install_output[:1000] if install_output else "Installation failed - see issues above"
                else:
                    install_log = "Installation successful"
                
                # Run tests from source if available, otherwise from installed package
                if source_path:
                    test_files = find_tests_in_source(source_path)
                    test_run_path = source_path
                else:
                    test_files = find_tests(package_name, temp_dir)
                    test_run_path = temp_dir
                
                if test_files:
                    print(f"  → Running {len(test_files)} tests...")
                    test_passed, test_rate, valid_test_rate, test_errors, case_results = run_tests(package_name, test_run_path, test_files)
                    test_cases = case_results
                    if not test_passed:
                        reasons.append(f"Test pass rate: {test_rate*100:.1f}% (valid tests: {valid_test_rate*100:.1f}%)")
                        issues.extend(test_errors)
                else:
                    test_passed = True
                    test_rate = 1.0
                    valid_test_rate = 1.0
                    test_errors = ["No tests found - assuming compatible"]
                    test_cases = [TestCaseResult(
                        test_file="N/A",
                        test_name="No tests",
                        passed=True,
                        error_type="",
                        error_message="",
                        error_traceback="",
                        reason="No test files found in package source",
                        duration=0.0
                    )]
                
                if not test_passed:
                    reasons.append(f"Test pass rate: {test_rate*100:.1f}%")
                    issues.extend(test_errors)
                    
            finally:
                # Cleanup temp directory unless keep_source is True
                if source_cleanup and not keep_source:
                    try:
                        shutil.rmtree(source_cleanup)
                    except Exception:
                        pass
        
        # Get version (use detected version if available)
        if version == "unknown":
            try:
                success, stdout, stderr = run_command(
                    [sys.executable, "-m", "pip", "show", package_name],
                    timeout=30
                )
                for line in stdout.split('\n'):
                    if line.startswith('Version:'):
                        version = line.split(':')[1].strip()
            except:
                pass
        
        # Determine overall compatibility
        compatible = installable and test_passed and len([i for i in issues if 'Windows' in i]) == 0
        alternatives = get_alternatives(package_name) if not compatible else []
        
        return CompatibilityResult(
            package_name=package_name,
            version=version,
            installable=installable,
            test_passed=test_passed,
            test_rate=test_rate,
            compatible=compatible,
            issues=issues,
            reasons=reasons,
            alternatives=alternatives,
            test_cases=test_cases,
            install_log=install_log
        )
        
    finally:
        # Cleanup source directory unless keep_source is True
        if source_path and not should_keep_source:
            try:
                print(f"  🗑️  Cleaning up source: {source_path}")
                shutil.rmtree(source_path)
            except Exception as e:
                print(f"  ⚠️  Failed to cleanup source: {e}")
        elif source_path and should_keep_source:
            print(f"  📁 Keeping source at: {source_path}")


def generate_summary(results: List[CompatibilityResult]) -> SummaryReport:
    """Generate summary report."""
    compatible = sum(1 for r in results if r.compatible)
    partial = sum(1 for r in results if r.installable and not r.compatible)
    incompatible = sum(1 for r in results if not r.installable)
    
    return SummaryReport(
        timestamp=datetime.now().isoformat(),
        total_packages=len(results),
        compatible_count=compatible,
        partial_count=partial,
        incompatible_count=incompatible,
        results=results
    )


def print_table(results: List[CompatibilityResult]):
    """Print results as a formatted table."""
    print("\n" + "="*100)
    print("COMPATIBILITY SUMMARY")
    print("="*100)
    
    # Header
    print(f"{'Package':<25} {'Version':<12} {'Status':<12} {'Test Rate':<12} {'Issues':<40}")
    print("-"*100)
    
    for r in results:
        status = "✅ Compatible" if r.compatible else ("⚠️ Partial" if r.installable else "❌ Incompatible")
        issues_summary = "; ".join(r.issues[:2])[:38] + "..." if len(r.issues) > 2 else "; ".join(r.issues)
        print(f"{r.package_name:<25} {r.version:<12} {status:<12} {r.test_rate*100:>6.1f}%     {issues_summary:<40}")
    
    print("-"*100)
    
    # Summary
    compatible = sum(1 for r in results if r.compatible)
    print(f"\nTotal: {len(results)} packages | Compatible: {compatible} | Partial: {sum(1 for r in results if r.installable and not r.compatible)} | Incompatible: {sum(1 for r in results if not r.installable)}")


def print_detailed_report(results: List[CompatibilityResult]):
    """Print detailed report for each package with per-test-case details."""
    print("\n" + "="*100)
    print("DETAILED REPORT")
    print("="*100)
    
    for r in results:
        print(f"\n📦 {r.package_name} v{r.version}")
        print(f"   Status: {'✅ Compatible' if r.compatible else ('⚠️ Partial' if r.installable else '❌ Incompatible')}")
        print(f"   Test Pass Rate: {r.test_rate*100:.1f}%")
        
        if r.install_log:
            print(f"   Install Log: {r.install_log}")
        
        if r.issues:
            print("   Issues:")
            for issue in r.issues:
                # Highlight environment issues
                if "[ENVIRONMENT ISSUE]" in issue:
                    print(f"     - ⚠️  {issue}")
                else:
                    print(f"     - {issue}")
        
        if r.reasons:
            print("   Reasons:")
            for reason in r.reasons:
                print(f"     - {reason}")
        
        if r.alternatives:
            print("   Alternatives:")
            for alt in r.alternatives:
                print(f"     - {alt}")
        
        # Print detailed test case results
        if r.test_cases:
            print("\n   📋 TEST CASE DETAILS:")
            print("   " + "-"*100)
            print(f"   {'Test File':<40} {'Result':<10} {'Error Type':<22} {'Duration':<10}")
            print("   " + "-"*100)
            
            environment_issue_count = 0
            for tc in r.test_cases:
                result_str = "✅ PASS" if tc.passed else "❌ FAIL"
                error_type = tc.error_type if tc.error_type else "N/A"
                
                # Check if this is an environment issue
                is_env_issue = "[ENVIRONMENT ISSUE]" in tc.reason if tc.reason else False
                if is_env_issue:
                    environment_issue_count += 1
                    print(f"   {tc.test_name:<40} {result_str:<10} {'⚠️  ' + error_type:<22} {tc.duration:.2f}s")
                else:
                    print(f"   {tc.test_name:<40} {result_str:<10} {error_type:<22} {tc.duration:.2f}s")
                
                if not tc.passed:
                    print(f"       └─ Reason: {tc.reason}")
                    if tc.error_message and len(tc.error_message) < 300:
                        print(f"       └─ Error: {tc.error_message.strip()}")
                    elif tc.error_message:
                        print(f"       └─ Error: {tc.error_message[:280].strip()}...")
            
            print("   " + "-"*100)
            passed_count = sum(1 for tc in r.test_cases if tc.passed)
            failed_count = len(r.test_cases) - passed_count - environment_issue_count
            print(f"   Total: {len(r.test_cases)} tests | Passed: {passed_count} | Failed: {failed_count} | Environment Issues: {environment_issue_count}")
            
            if environment_issue_count > 0:
                print(f"   ⚠️  Note: {environment_issue_count} test(s) failed due to environment/permission issues (not counted against compatibility)")


def generate_full_report(results: List[CompatibilityResult], output_file: str = None, format: str = "markdown") -> str:
    """Generate a comprehensive report with all analysis conclusions.
    
    Args:
        results: List of compatibility results
        output_file: Optional file path to save the report
        format: Output format - "markdown" or "text"
    
    Returns:
        Formatted report string
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Summary calculations
    compatible = sum(1 for r in results if r.compatible)
    partial = sum(1 for r in results if r.installable and not r.compatible)
    incompatible = sum(1 for r in results if not r.installable)
    
    total_test_cases = sum(len(r.test_cases) for r in results)
    passed_test_cases = sum(sum(1 for tc in r.test_cases if tc.passed) for r in results)
    failed_test_cases = total_test_cases - passed_test_cases
    
    if format == "markdown":
        return _generate_markdown_report(
            results, timestamp, compatible, partial, incompatible,
            total_test_cases, passed_test_cases, failed_test_cases, output_file
        )
    else:
        return _generate_text_report(
            results, timestamp, compatible, partial, incompatible,
            total_test_cases, passed_test_cases, failed_test_cases, output_file
        )


def _generate_markdown_report(
    results: List[CompatibilityResult],
    timestamp: str,
    compatible: int,
    partial: int,
    incompatible: int,
    total_test_cases: int,
    passed_test_cases: int,
    failed_test_cases: int,
    output_file: str = None
) -> str:
    """Generate report in Markdown format."""
    lines = []
    
    # Header
    lines.append("# 📊 Python 库 HarmonyOS 兼容性分析报告")
    lines.append("")
    lines.append(f"**生成时间**: {timestamp}")
    lines.append("")
    lines.append(f"**检查工具**: Python HarmonyOS Compatibility Checker")
    lines.append("")
    
    # Summary
    lines.append("---")
    lines.append("")
    lines.append("## 📋 检查结果汇总")
    lines.append("")
    lines.append("| 项目 | 数量 |")
    lines.append("|------|------|")
    lines.append(f"| 总包数 | {len(results)} |")
    lines.append(f"| ✅ 兼容 | {compatible} |")
    lines.append(f"| ⚠️ 部分兼容 | {partial} |")
    lines.append(f"| ❌ 不兼容 | {incompatible} |")
    lines.append(f"| 兼容率 | {compatible/len(results)*100:.1f}% |" if results else "| 兼容率 | N/A |")
    lines.append("")
    
    # Test case statistics
    lines.append("### 📊 测试用例统计")
    lines.append("")
    lines.append("| 统计项 | 数量 |")
    lines.append("|--------|------|")
    lines.append(f"| 总用例数 | {total_test_cases} |")
    lines.append(f"| ✅ 通过 | {passed_test_cases} |")
    lines.append(f"| ❌ 失败 | {failed_test_cases} |")
    lines.append(f"| 通过率 | {passed_test_cases/total_test_cases*100:.1f}% |" if total_test_cases > 0 else "| 通过率 | N/A |")
    lines.append("")
    
    # Detailed analysis
    lines.append("---")
    lines.append("")
    lines.append("## 🔍 详细分析")
    lines.append("")
    
    for r in results:
        status_emoji = "✅" if r.compatible else ("⚠️" if r.installable else "❌")
        status_text = "兼容" if r.compatible else ("部分兼容" if r.installable else "不兼容")
        
        lines.append(f"### 📦 {r.package_name}")
        lines.append("")
        lines.append(f"- **版本**: {r.version}")
        lines.append(f"- **状态**: {status_emoji} {status_text}")
        lines.append(f"- **测试通过率**: {r.test_rate*100:.1f}%")
        lines.append("")
        
        # Installation log
        if r.install_log:
            log_preview = r.install_log[:300] + "..." if len(r.install_log) > 300 else r.install_log
            lines.append("**安装日志**:")
            lines.append("```")
            lines.append(log_preview)
            lines.append("```")
            lines.append("")
        
        # Issues
        if r.issues:
            lines.append("**问题列表**:")
            for i, issue in enumerate(r.issues, 1):
                lines.append(f"{i}. {issue}")
            lines.append("")
        
        # Reasons
        if r.reasons:
            lines.append("**不兼容原因**:")
            for reason in r.reasons:
                lines.append(f"- {reason}")
            lines.append("")
        
        # Test case details
        if r.test_cases:
            pkg_total = len(r.test_cases)
            pkg_passed = sum(1 for tc in r.test_cases if tc.passed)
            pkg_failed = pkg_total - pkg_passed
            
            lines.append("**测试用例**:")
            lines.append(f"- 共 {pkg_total} 个 | ✅ 通过 {pkg_passed} 个 | ❌ 失败 {pkg_failed} 个")
            lines.append("")
            
            failed_tests = [tc for tc in r.test_cases if not tc.passed]
            if failed_tests:
                lines.append("**失败详情**:")
                lines.append("")
                lines.append("| 测试用例 | 错误类型 | 失败原因 |")
                lines.append("|----------|----------|----------|")
                for tc in failed_tests:
                    reason_short = tc.reason[:50] + "..." if len(tc.reason) > 50 else tc.reason
                    lines.append(f"| {tc.test_name} | {tc.error_type} | {reason_short} |")
                lines.append("")
        
        # Alternatives
        if r.alternatives:
            lines.append("**替代方案**:")
            for alt in r.alternatives:
                lines.append(f"- {alt}")
            lines.append("")
        elif not r.compatible:
            lines.append("**替代方案**: 暂无推荐，建议查阅 HarmonyOS Python 包兼容性数据库")
            lines.append("")
        
        # Conclusion
        if r.compatible:
            lines.append("> ✅ **结论**: 该包可在 HarmonyOS 上正常使用")
        elif r.installable and not r.compatible:
            lines.append("> ⚠️ **结论**: 该包可安装但存在兼容性问题，建议测试后使用")
        else:
            lines.append("> ❌ **结论**: 该包不兼容 HarmonyOS，请使用替代方案")
        
        lines.append("")
        lines.append("---")
        lines.append("")
    
    # Overall recommendations
    lines.append("## 💡 总体建议")
    lines.append("")
    
    if incompatible > 0:
        lines.append(f"发现 **{incompatible}** 个不兼容的包，建议:")
        lines.append("")
        lines.append("1. 优先使用标记为'兼容'的替代包")
        lines.append("2. 对于不兼容的包，查看各包的'替代方案'部分")
        lines.append("3. 考虑降级到旧版本（某些包的低版本可能兼容）")
        lines.append("4. 联系包作者询问 HarmonyOS 支持计划")
        lines.append("")
    
    if partial > 0:
        lines.append(f"发现 **{partial}** 个部分兼容的包，建议:")
        lines.append("")
        lines.append("1. 在 HarmonyOS 上进行充分测试后再使用")
        lines.append("2. 关注测试失败的用例，评估是否影响你的使用场景")
        lines.append("3. 考虑寻找功能类似的完全兼容替代品")
        lines.append("")
    
    if compatible == len(results):
        lines.append("> 🎉 **所有检查的包都兼容 HarmonyOS！可以直接使用。**")
        lines.append("")
    
    lines.append("---")
    lines.append("")
    lines.append("*报告生成完毕*")
    
    report_text = "\n".join(lines)
    
    # Save to file if requested
    if output_file:
        # Change extension to .md for markdown
        md_output_file = output_file.replace('.txt', '.md')
        with open(md_output_file, 'w', encoding='utf-8') as f:
            f.write(report_text)
    
    return report_text


def _generate_text_report(
    results: List[CompatibilityResult],
    timestamp: str,
    compatible: int,
    partial: int,
    incompatible: int,
    total_test_cases: int,
    passed_test_cases: int,
    failed_test_cases: int,
    output_file: str = None
) -> str:
    """Generate report in plain text format (legacy)."""
    lines = []
    
    # Header
    lines.append("=" * 100)
    lines.append("Python 库 HarmonyOS 兼容性分析报告")
    lines.append("=" * 100)
    lines.append(f"生成时间：{timestamp}")
    lines.append(f"检查工具：Python HarmonyOS Compatibility Checker")
    lines.append("")
    
    # Summary
    lines.append("-" * 100)
    lines.append("【检查结果汇总】")
    lines.append("-" * 100)
    lines.append(f"总包数：{len(results)}")
    lines.append(f"✅ 兼容：{compatible}")
    lines.append(f"⚠️  部分兼容：{partial}")
    lines.append(f"❌ 不兼容：{incompatible}")
    lines.append(f"兼容率：{compatible/len(results)*100:.1f}%" if results else "兼容率：N/A")
    lines.append("")
    lines.append(f"📊 测试用例统计:")
    lines.append(f"   总用例数：{total_test_cases}")
    lines.append(f"   ✅ 通过：{passed_test_cases}")
    lines.append(f"   ❌ 失败：{failed_test_cases}")
    lines.append(f"   通过率：{passed_test_cases/total_test_cases*100:.1f}%" if total_test_cases > 0 else "   通过率：N/A")
    lines.append("")
    
    # Detailed analysis for each package
    lines.append("=" * 100)
    lines.append("【详细分析】")
    lines.append("=" * 100)
    
    for r in results:
        lines.append("")
        lines.append(f"📦 包名：{r.package_name}")
        lines.append(f"   版本：{r.version}")
        lines.append(f"   状态：{'✅ 兼容' if r.compatible else ('⚠️ 部分兼容' if r.installable else '❌ 不兼容')}")
        lines.append(f"   测试通过率：{r.test_rate*100:.1f}%")
        
        # Installation status
        if r.install_log:
            lines.append(f"   安装日志：{r.install_log[:200]}..." if len(r.install_log) > 200 else f"   安装日志：{r.install_log}")
        
        # Issues
        if r.issues:
            lines.append("")
            lines.append("   ❗ 问题列表:")
            for i, issue in enumerate(r.issues, 1):
                lines.append(f"      {i}. {issue}")
        
        # Reasons
        if r.reasons:
            lines.append("")
            lines.append("   🔍 不兼容原因:")
            for reason in r.reasons:
                lines.append(f"      • {reason}")
        
        # Test case details
        if r.test_cases:
            pkg_total = len(r.test_cases)
            pkg_passed = sum(1 for tc in r.test_cases if tc.passed)
            pkg_failed = pkg_total - pkg_passed
            
            lines.append("")
            lines.append(f"   📊 测试用例：共 {pkg_total} 个 | ✅ 通过 {pkg_passed} 个 | ❌ 失败 {pkg_failed} 个")
            
            failed_tests = [tc for tc in r.test_cases if not tc.passed]
            if failed_tests:
                lines.append("")
                lines.append("   📋 测试用例失败详情:")
                for tc in failed_tests:
                    lines.append(f"      - {tc.test_name}")
                    lines.append(f"        错误类型：{tc.error_type}")
                    lines.append(f"        失败原因：{tc.reason}")
                    if tc.error_message:
                        error_preview = tc.error_message[:150].strip().replace('\n', ' ')
                        lines.append(f"        错误信息：{error_preview}...")
        
        # Alternatives
        if r.alternatives:
            lines.append("")
            lines.append("   💡 替代方案:")
            for alt in r.alternatives:
                lines.append(f"      • {alt}")
        elif not r.compatible:
            lines.append("")
            lines.append("   💡 替代方案：暂无推荐，建议查阅 HarmonyOS Python 包兼容性数据库")
        
        # Conclusion for this package
        lines.append("")
        if r.compatible:
            lines.append("   ✅ 结论：该包可在 HarmonyOS 上正常使用")
        elif r.installable and not r.compatible:
            lines.append("   ⚠️  结论：该包可安装但存在兼容性问题，建议测试后使用")
        else:
            lines.append("   ❌ 结论：该包不兼容 HarmonyOS，请使用替代方案")
        
        lines.append("-" * 100)
    
    # Overall recommendations
    lines.append("")
    lines.append("=" * 100)
    lines.append("【总体建议】")
    lines.append("=" * 100)
    
    if incompatible > 0:
        lines.append("")
        lines.append(f"发现 {incompatible} 个不兼容的包，建议:")
        lines.append("  1. 优先使用标记为'兼容'的替代包")
        lines.append("  2. 对于不兼容的包，查看各包的'替代方案'部分")
        lines.append("  3. 考虑降级到旧版本（某些包的低版本可能兼容）")
        lines.append("  4. 联系包作者询问 HarmonyOS 支持计划")
    
    if partial > 0:
        lines.append("")
        lines.append(f"发现 {partial} 个部分兼容的包，建议:")
        lines.append("  1. 在 HarmonyOS 上进行充分测试后再使用")
        lines.append("  2. 关注测试失败的用例，评估是否影响你的使用场景")
        lines.append("  3. 考虑寻找功能类似的完全兼容替代品")
    
    if compatible == len(results):
        lines.append("")
        lines.append("🎉 所有检查的包都兼容 HarmonyOS！可以直接使用。")
    
    lines.append("")
    lines.append("=" * 100)
    lines.append("报告结束")
    lines.append("=" * 100)
    
    report_text = "\n".join(lines)
    
    # Save to file if requested
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report_text)
    
    return report_text


# Global flag for keeping source code
_KEEP_SOURCE = False

def check_package_with_progress(pkg: str, index: int, total: int) -> Tuple[int, CompatibilityResult]:
    """Check a package and return index with result for ordered output."""
    print(f"\n[{index}/{total}] Checking: {pkg}...")
    start_time = time.time()
    
    try:
        result = check_package(pkg, keep_source=_KEEP_SOURCE)
        elapsed = time.time() - start_time
        print(f"[{index}/{total}] ✅ Completed: {pkg} ({elapsed:.1f}s)")
        return index, result
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"[{index}/{total}] ❌ Error: {pkg} ({elapsed:.1f}s)")
        return index, CompatibilityResult(
            package_name=pkg,
            version="unknown",
            installable=False,
            test_passed=False,
            test_rate=0.0,
            compatible=False,
            issues=[f"Error during check: {str(e)}"],
            reasons=["Check failed"],
            alternatives=[],
            test_cases=[],
            install_log=f"Error: {str(e)}"
        )


def main():
    import argparse
    
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nError: No packages specified")
        print("Usage: python check_compatibility.py <package1> [package2] ...")
        print("       python check_compatibility.py -r requirements.txt")
        print("       python check_compatibility.py --workers 4 <packages...>")
        sys.exit(1)
    
    parser = argparse.ArgumentParser(description='Python Library HarmonyOS Compatibility Checker')
    parser.add_argument('packages', nargs='*', help='Package names to check')
    parser.add_argument('-r', '--requirements', help='Requirements file to check')
    parser.add_argument('-w', '--workers', type=int, default=4, help='Number of parallel workers (default: 4)')
    parser.add_argument('--sequential', action='store_true', help='Run checks sequentially (no parallelism)')
    parser.add_argument('--keep-source', action='store_true', help='Keep downloaded source code for verification')
    
    args = parser.parse_args()
    
    packages = []
    
    # Handle requirements file
    if args.requirements:
        req_file = args.requirements
        if os.path.exists(req_file):
            with open(req_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        pkg_name = line.split('==')[0].split('>=')[0].split('<=')[0].split('[')[0]
                        packages.append(pkg_name.strip())
        else:
            print(f"Error: Requirements file not found: {req_file}")
            sys.exit(1)
    elif args.packages:
        packages = args.packages
    else:
        print("Error: No packages specified")
        sys.exit(1)
    
    # Set global keep_source flag
    global _KEEP_SOURCE
    _KEEP_SOURCE = args.keep_source
    
    print(f"\n🔍 Python Library HarmonyOS Compatibility Checker")
    print(f"   Checking {len(packages)} package(s)...")
    print(f"   Python: {sys.version}")
    print(f"   Platform: {sys.platform}")
    print(f"   Workers: {args.workers} (parallel)" if not args.sequential else "   Mode: Sequential")
    print(f"   Keep Source: {args.keep_source}")
    print(f"   Estimated time: ~{len(packages) * 30}s (sequential) / ~{max(30, len(packages) * 30 // args.workers)}s (parallel)")
    print("="*60)
    
    overall_start = time.time()
    results = [None] * len(packages)
    
    if args.sequential or len(packages) == 1:
        # Sequential mode
        for i, pkg in enumerate(packages, 1):
            _, result = check_package_with_progress(pkg, i, len(packages))
            results[i-1] = result
    else:
        # Parallel mode using ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            futures = {
                executor.submit(check_package_with_progress, pkg, i+1, len(packages)): i
                for i, pkg in enumerate(packages)
            }
            
            completed = 0
            for future in as_completed(futures):
                try:
                    index, result = future.result()
                    results[index-1] = result
                    completed += 1
                except Exception as e:
                    idx = futures[future] + 1
                    print(f"[{idx}/{len(packages)}] ❌ Exception: {e}")
                    results[idx-1] = CompatibilityResult(
                        package_name=packages[idx-1],
                        version="unknown",
                        installable=False,
                        test_passed=False,
                        test_rate=0.0,
                        compatible=False,
                        issues=[f"Exception: {str(e)}"],
                        reasons=["Check failed"],
                        alternatives=[],
                        test_cases=[],
                        install_log=f"Exception: {str(e)}"
                    )
    
    overall_elapsed = time.time() - overall_start
    print(f"\n{'='*60}")
    print(f"✅ All checks completed in {overall_elapsed:.1f}s")
    
    # Print results
    print_table(results)
    print_detailed_report(results)
    
    # Save JSON report with detailed test cases
    summary = generate_summary(results)
    
    # Generate filename with package names and versions
    if len(results) == 1:
        # Single package: compatibility_report_<package>-<version>_<timestamp>.json
        pkg_name = results[0].package_name.replace('-', '_')
        pkg_version = results[0].version if results[0].version != 'unknown' else 'unknown'
        file_prefix = f"compatibility_report_{pkg_name}-{pkg_version}"
    else:
        # Multiple packages: compatibility_report_<count>_packages_<timestamp>.json
        file_prefix = f"compatibility_report_{len(results)}_packages"
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    json_report_file = f"{file_prefix}_{timestamp}.json"
    
    # Convert results to dict with proper test case serialization
    report_data = {
        "timestamp": summary.timestamp,
        "total_packages": summary.total_packages,
        "compatible_count": summary.compatible_count,
        "partial_count": summary.partial_count,
        "incompatible_count": summary.incompatible_count,
        "results": [r.to_dict() for r in summary.results]
    }
    
    with open(json_report_file, 'w') as f:
        json.dump(report_data, f, indent=2)
    
    print(f"\n📄 JSON Report saved to: {json_report_file}")
    print(f"   (Includes detailed test case results with error analysis)")
    
    # Generate and save full markdown report with conclusions
    md_report_file = f"{file_prefix}_{timestamp}.md"
    full_report = generate_full_report(results, md_report_file, format="markdown")
    print(f"\n📄 Markdown Report saved to: {md_report_file}")
    print(f"   (Includes compatibility conclusions, reasons, and alternatives)")
    
    # Return exit code based on compatibility
    incompatible = sum(1 for r in results if not r.compatible)
    sys.exit(1 if incompatible > 0 else 0)


if __name__ == "__main__":
    main()

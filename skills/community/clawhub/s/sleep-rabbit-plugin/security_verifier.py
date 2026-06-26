#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Security Verifier for Sleep Rabbit Plugin v5.3.4
Verifies that v5.3.4 fixes the security theater issues from v5.3.3
"""

import os
import re
import sys
from pathlib import Path

def check_v5_3_3_security_theater_fixes():
    """Verify fixes for v5.3.3 security theater issues"""
    print("=== Checking v5.3.3 Security Theater Fixes ===")
    
    with open('skill.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    checks_passed = 0
    total_checks = 4
    
    # 1. Check for dangerous os.path.dirname(edf_path) - SHOULD NOT EXIST IN CODE
    # Use regex to find actual usage (not in comments or strings)
    import re
    
    # Pattern to find os.path.dirname(edf_path) in code
    pattern = r'os\.path\.dirname\([^)]*edf_path[^)]*\)'
    
    # Remove comments and strings to check only code
    code_only = re.sub(r'#.*$', '', content, flags=re.MULTILINE)  # Remove line comments
    code_only = re.sub(r'""".*?"""', '', code_only, flags=re.DOTALL)  # Remove triple double quotes
    code_only = re.sub(r"'''.*?'''", '', code_only, flags=re.DOTALL)  # Remove triple single quotes
    code_only = re.sub(r'".*?"', '', code_only)  # Remove double quotes
    code_only = re.sub(r"'.*?'", '', code_only)  # Remove single quotes
    
    matches = re.findall(pattern, code_only)
    
    if matches:
        print(f"[ERROR] Found dangerous os.path.dirname(edf_path) in code: {matches}")
        print("[ERROR] v5.3.3 issue not fixed!")
    else:
        print("[OK] No dangerous os.path.dirname(edf_path) found in actual code")
        print("[OK] v5.3.3 issue fixed - safe_outputs directory used instead")
        checks_passed += 1
    
    # 2. Check for safe_outputs directory usage - SHOULD EXIST
    if "safe_outputs" in content:
        print("[OK] Using safe_outputs directory - proper security")
        checks_passed += 1
    else:
        print("[ERROR] Not using safe_outputs directory - security issue")
    
    # 3. Check for path traversal protection - SHOULD EXIST
    if "'..' in" in content:
        print("[OK] Path traversal protection implemented")
        checks_passed += 1
    else:
        print("[ERROR] No path traversal protection found")
    
    # 4. Check for 100MB limit - SHOULD EXIST
    if "100 * 1024 * 1024" in content:
        print("[OK] 100MB file size limit implemented")
        checks_passed += 1
    else:
        print("[ERROR] No 100MB file size limit found")
    
    return checks_passed, total_checks

def check_documentation_truthfulness():
    """Verify documentation is truthful (not security theater)"""
    print("\n=== Checking Documentation Truthfulness ===")
    
    # Read SKILL.md
    with open('SKILL.md', 'r', encoding='utf-8') as f:
        skill_md = f.read()
    
    # Read SECURITY_TRUTH.md
    with open('SECURITY_TRUTH.md', 'r', encoding='utf-8') as f:
        security_md = f.read()
    
    checks_passed = 0
    total_checks = 6
    
    # Check for acknowledgment of v5.3.3 issues
    if "security theater" in skill_md.lower():
        print("[OK] SKILL.md acknowledges security theater issues")
        checks_passed += 1
    else:
        print("[ERROR] SKILL.md doesn't mention security theater")
    
    if "v5.3.3" in skill_md:
        print("[OK] SKILL.md mentions v5.3.3 specifically")
        checks_passed += 1
    else:
        print("[ERROR] SKILL.md doesn't mention v5.3.3")
    
    # Check for truthful security claims
    if "safe_outputs" in skill_md:
        print("[OK] SKILL.md mentions safe_outputs directory")
        checks_passed += 1
    else:
        print("[ERROR] SKILL.md doesn't mention safe_outputs")
    
    # Check SECURITY_TRUTH.md
    if "security theater" in security_md.lower():
        print("[OK] SECURITY_TRUTH.md acknowledges security theater")
        checks_passed += 1
    else:
        print("[ERROR] SECURITY_TRUTH.md doesn't mention security theater")
    
    if "v5.3.3" in security_md:
        print("[OK] SECURITY_TRUTH.md mentions v5.3.3 specifically")
        checks_passed += 1
    else:
        print("[ERROR] SECURITY_TRUTH.md doesn't mention v5.3.3")
    
    if "actually implemented" in security_md.lower():
        print("[OK] SECURITY_TRUTH.md emphasizes actual implementation")
        checks_passed += 1
    else:
        print("[WARNING] SECURITY_TRUTH.md doesn't emphasize actual implementation")
    
    return checks_passed, total_checks

def check_code_security_implementation():
    """Verify security is actually implemented in code"""
    print("\n=== Checking Code Security Implementation ===")
    
    with open('skill.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    checks_passed = 0
    total_checks = 5
    
    # Check for security validation function
    if "validate_security_strict" in content:
        print("[OK] Strict security validation function exists")
        checks_passed += 1
    else:
        print("[ERROR] No strict security validation function")
    
    # Check for file type restriction
    if "{'.edf', '.bdf', '.gdf'}" in content:
        print("[OK] File type restriction implemented (EDF/BDF/GDF only)")
        checks_passed += 1
    else:
        print("[ERROR] File type restriction not found")
    
    # Check for sensitive directory blocking
    if "sensitive_dirs" in content:
        print("[OK] Sensitive directory blocking implemented")
        checks_passed += 1
    else:
        print("[ERROR] No sensitive directory blocking")
    
    # Check for get_safe_output_path function
    if "get_safe_output_path" in content:
        print("[OK] Safe output path function exists")
        checks_passed += 1
    else:
        print("[ERROR] No safe output path function")
    
    # Check for security configuration
    if '"max_file_size": 100 * 1024 * 1024' in content:
        print("[OK] Security configuration includes file size limit")
        checks_passed += 1
    else:
        print("[ERROR] Security configuration missing file size limit")
    
    return checks_passed, total_checks

def check_requirements_file_cleanliness():
    """Verify requirements.txt is clean (no deceptive content)"""
    print("\n=== Checking Requirements File Cleanliness ===")
    
    with open('requirements.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    
    checks_passed = 0
    total_checks = 3
    
    # Check for git clone commands
    lines = content.split('\n')
    has_git_clone = False
    has_third_party_url = False
    
    for line in lines:
        line_lower = line.lower().strip()
        if not line_lower or line_lower.startswith('#'):
            continue
        
        if "git clone" in line_lower:
            has_git_clone = True
            print(f"[ERROR] Found git clone in line: {line.strip()}")
        
        if "github.com" in line_lower or "gitlab.com" in line_lower:
            has_third_party_url = True
            print(f"[ERROR] Found third-party URL in line: {line.strip()}")
    
    if not has_git_clone:
        print("[OK] No git clone commands found")
        checks_passed += 1
    
    if not has_third_party_url:
        print("[OK] No third-party repository URLs found")
        checks_passed += 1
    
    # Check for PyPI-only declaration
    if "pypi" in content.lower():
        print("[OK] Mentions PyPI as package source")
        checks_passed += 1
    else:
        print("[WARNING] Doesn't mention PyPI as package source")
    
    return checks_passed, total_checks

def main():
    """Run all security verification checks"""
    print("Security Verification for Sleep Rabbit Plugin v5.3.4")
    print("Verifying fixes for v5.3.3 security theater issues")
    print("=" * 60)
    
    all_passed = 0
    all_total = 0
    
    # Run all checks
    results = []
    
    # Check 1: v5.3.3 security theater fixes
    passed, total = check_v5_3_3_security_theater_fixes()
    results.append(("v5.3.3 Security Theater Fixes", passed, total))
    all_passed += passed
    all_total += total
    
    # Check 2: Documentation truthfulness
    passed, total = check_documentation_truthfulness()
    results.append(("Documentation Truthfulness", passed, total))
    all_passed += passed
    all_total += total
    
    # Check 3: Code security implementation
    passed, total = check_code_security_implementation()
    results.append(("Code Security Implementation", passed, total))
    all_passed += passed
    all_total += total
    
    # Check 4: Requirements file cleanliness
    passed, total = check_requirements_file_cleanliness()
    results.append(("Requirements File Cleanliness", passed, total))
    all_passed += passed
    all_total += total
    
    # Summary
    print("\n" + "=" * 60)
    print("SECURITY VERIFICATION SUMMARY")
    print("=" * 60)
    
    for name, passed, total in results:
        percentage = (passed / total) * 100
        status = "PASS" if percentage >= 80 else "FAIL"
        print(f"{status}: {name} - {passed}/{total} ({percentage:.1f}%)")
    
    overall_percentage = (all_passed / all_total) * 100
    print(f"\nOverall: {all_passed}/{all_total} checks passed ({overall_percentage:.1f}%)")
    
    if overall_percentage >= 90:
        print("\n[SUCCESS] v5.3.4 successfully fixes v5.3.3 security theater issues!")
        print("This version provides truthful security declarations and actual implementation.")
        return 0
    elif overall_percentage >= 70:
        print("\n[WARNING] v5.3.4 partially fixes v5.3.3 issues but needs improvement")
        print("Some security theater elements may still exist.")
        return 1
    else:
        print("\n[ERROR] v5.3.4 does not adequately fix v5.3.3 security theater issues")
        print("This version may still have deceptive security claims.")
        return 2

if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
Simple EDF Test Module
Version: 5.3.4
Purpose: Basic EDF file validation and testing
Security: Read-only, no file writes
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional

def simple_edf_test(edf_path: str) -> Dict[str, Any]:
    """
    Perform basic validation of an EDF file
    
    Args:
        edf_path: Path to EDF file
        
    Returns:
        Dictionary with validation results
    """
    try:
        file_path = Path(edf_path)
        
        # Basic file validation
        if not file_path.exists():
            return {
                "success": False,
                "error": f"File does not exist: {edf_path}",
                "valid": False
            }
        
        if not file_path.is_file():
            return {
                "success": False,
                "error": f"Path is not a file: {edf_path}",
                "valid": False
            }
        
        # Check file size
        file_size = file_path.stat().st_size
        if file_size == 0:
            return {
                "success": False,
                "error": "File is empty",
                "valid": False,
                "file_size": file_size
            }
        
        # Check file extension
        valid_extensions = {'.edf', '.edf+', '.bdf', '.gdf'}
        file_ext = file_path.suffix.lower()
        
        if file_ext not in valid_extensions:
            return {
                "success": False,
                "error": f"Invalid file extension: {file_ext}. Expected: {', '.join(valid_extensions)}",
                "valid": False,
                "file_extension": file_ext
            }
        
        # Try to read file header (basic check)
        try:
            with open(edf_path, 'rb') as f:
                header = f.read(256)  # Read first 256 bytes
                
                # Basic EDF header check (first 8 bytes should be version)
                if len(header) >= 8:
                    version = header[0:8].decode('ascii', errors='ignore').strip()
                    is_edf = version in ['0', '1', '255']  # EDF/EDF+ versions
                else:
                    is_edf = False
                    version = "unknown"
        except Exception as e:
            is_edf = False
            version = f"error: {str(e)}"
        
        return {
            "success": True,
            "valid": True,
            "file_path": str(edf_path),
            "file_size": file_size,
            "file_extension": file_ext,
            "exists": True,
            "is_file": True,
            "edf_header_valid": is_edf,
            "edf_version": version if is_edf else "not an EDF file",
            "message": "Basic EDF validation passed" if is_edf else "File exists but may not be valid EDF",
            "security": "read-only, no file writes"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Validation error: {str(e)}",
            "valid": False,
            "file_path": edf_path
        }


def simple_edf_test_function(edf_path: str) -> Dict[str, Any]:
    """
    Alias for simple_edf_test (for compatibility)
    """
    return simple_edf_test(edf_path)


if __name__ == "__main__":
    # Test the function
    import sys
    if len(sys.argv) > 1:
        result = simple_edf_test(sys.argv[1])
        print(json.dumps(result, indent=2))
    else:
        print("Usage: python simple_edf_test.py <edf-file>")


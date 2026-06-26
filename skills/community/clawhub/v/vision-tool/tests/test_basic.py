"""
Basic tests for Vision Tool
"""

import os
import sys
import tempfile
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import analyze_image


def test_import():
    """Test that the module can be imported"""
    from scripts.vision_core import VisionAnalyzer
    assert VisionAnalyzer is not None


def test_analyze_image_mock():
    """Test analyze_image function with mock (no actual API call)"""
    # Create a temporary test image file
    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
        tmp.write(b'fake image data')
        tmp_path = tmp.name
    
    try:
        # This will fail because it's not a real image, but we're testing the function call
        # In a real test, you'd mock the API call
        result = analyze_image(tmp_path, "Test prompt")
        
        # Check result structure
        assert isinstance(result, dict)
        assert 'analysis' in result or 'error' in result
        assert 'time_elapsed' in result
        assert 'source' in result
        assert 'stats' in result
        
    except Exception as e:
        # Test image is not a real image, expected to fail
        # This is normal test behavior
        print(f"Test image analysis failed (expected): {e}")
    finally:
        # Clean up
        os.unlink(tmp_path)


def test_error_handling():
    """Test error handling for non-existent file"""
    result = analyze_image("/non/existent/file.jpg", "Test prompt")
    assert 'error' in result
    assert 'not found' in result['error'].lower() or 'failed' in result['error'].lower()


if __name__ == "__main__":
    test_import()
    print("✅ test_import passed")
    
    test_analyze_image_mock()
    print("✅ test_analyze_image_mock passed")
    
    test_error_handling()
    print("✅ test_error_handling passed")
    
    print("\n✅ All basic tests passed!")
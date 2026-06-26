#!/usr/bin/env python3
"""
Compare screenshots using pixel-level diffing (Pillow).
"""

import argparse
import os
import sys
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        from PIL import Image, ImageChops, ImageDraw
    except ImportError:
        print("❌ Pillow not installed")
        print("\nInstall with:")
        print("  pip install pillow")
        sys.exit(1)

def compare_images(baseline_path, current_path, diff_path, threshold):
    """
    Compare two images and generate a diff image.
    Returns similarity percentage (0-100).
    """
    from PIL import Image, ImageChops, ImageDraw
    
    try:
        baseline = Image.open(baseline_path).convert('RGB')
        current = Image.open(current_path).convert('RGB')
    except Exception as e:
        print(f"❌ Failed to open images: {e}")
        return None
    
    # Ensure images are the same size
    if baseline.size != current.size:
        print(f"⚠️  Size mismatch: {baseline.size} vs {current.size}")
        # Resize current to match baseline
        current = current.resize(baseline.size, Image.Resampling.LANCZOS)
    
    # Calculate pixel differences
    diff = ImageChops.difference(baseline, current)
    
    # Convert to grayscale for analysis
    diff_gray = diff.convert('L')
    
    # Calculate similarity
    # Count pixels that are identical (diff value = 0)
    histogram = diff_gray.histogram()
    identical_pixels = histogram[0]  # pixels with value 0 (no difference)
    total_pixels = baseline.size[0] * baseline.size[1]
    similarity = (identical_pixels / total_pixels) * 100
    
    # Generate diff image with red overlay on changes
    diff_overlay = baseline.copy()
    
    # Create a red mask for changed pixels
    diff_data = diff_gray.getdata()
    mask = Image.new('RGB', baseline.size)
    mask_pixels = []
    
    for pixel_diff in diff_data:
        if pixel_diff > 10:  # Threshold for "changed" pixel (ignore tiny differences)
            mask_pixels.append((255, 0, 255))  # Magenta for changes
        else:
            mask_pixels.append((0, 0, 0))  # Black for unchanged
    
    mask.putdata(mask_pixels)
    
    # Blend the mask with the baseline
    diff_overlay = Image.blend(diff_overlay, mask, 0.5)
    
    # Save diff image
    diff_overlay.save(diff_path)
    
    return similarity

def main():
    parser = argparse.ArgumentParser(
        description='Compare screenshots against baselines using pixel-level diffing',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Compare current screenshots against baselines
  %(prog)s --baseline screenshots/baseline --current screenshots/current

  # With custom threshold and output directory
  %(prog)s --baseline .visual-qa/baselines --current .visual-qa/current --output .visual-qa/diffs --threshold 98

  # Show only failures
  %(prog)s --baseline baseline/ --current current/ --threshold 99 --quiet

Threshold:
  - 99 (default): Strict, catches most visual changes
  - 95: Moderate, allows minor rendering differences
  - 90: Loose, allows more variation (dynamic content)
        """
    )
    
    parser.add_argument('--baseline', '-b', required=True, help='Baseline screenshots directory')
    parser.add_argument('--current', '-c', required=True, help='Current screenshots directory')
    parser.add_argument('--output', '-o', default='diffs', help='Output directory for diff images (default: diffs)')
    parser.add_argument('--threshold', '-t', type=float, default=99.0, 
                       help='Similarity threshold percentage (default: 99.0)')
    parser.add_argument('--quiet', '-q', action='store_true', help='Only show failures')
    
    args = parser.parse_args()
    
    # Check dependencies
    check_dependencies()
    from PIL import Image
    
    # Validate directories
    if not os.path.isdir(args.baseline):
        print(f"❌ Baseline directory not found: {args.baseline}")
        sys.exit(1)
    
    if not os.path.isdir(args.current):
        print(f"❌ Current directory not found: {args.current}")
        sys.exit(1)
    
    # Create output directory
    os.makedirs(args.output, exist_ok=True)
    
    # Find all PNG files in baseline
    baseline_files = set()
    for filename in os.listdir(args.baseline):
        if filename.endswith('.png'):
            baseline_files.add(filename)
    
    if not baseline_files:
        print(f"❌ No PNG files found in baseline directory: {args.baseline}")
        sys.exit(1)
    
    # Find matching files in current
    current_files = set()
    for filename in os.listdir(args.current):
        if filename.endswith('.png'):
            current_files.add(filename)
    
    if not current_files:
        print(f"❌ No PNG files found in current directory: {args.current}")
        sys.exit(1)
    
    # Find common files
    common_files = baseline_files & current_files
    
    if not common_files:
        print(f"❌ No matching files found between baseline and current")
        print(f"   Baseline files: {sorted(baseline_files)}")
        print(f"   Current files: {sorted(current_files)}")
        sys.exit(1)
    
    # Warn about missing files
    baseline_only = baseline_files - current_files
    current_only = current_files - baseline_files
    
    if baseline_only:
        print(f"⚠️  Files in baseline but not current: {sorted(baseline_only)}")
    
    if current_only:
        print(f"⚠️  Files in current but not baseline: {sorted(current_only)}")
    
    if not args.quiet:
        print(f"\n🔍 Comparing {len(common_files)} screenshots...")
        print(f"   Threshold: {args.threshold}%")
        print(f"   Diff output: {args.output}\n")
    
    # Compare all files
    results = []
    passed = 0
    failed = 0
    
    for filename in sorted(common_files):
        baseline_path = os.path.join(args.baseline, filename)
        current_path = os.path.join(args.current, filename)
        diff_path = os.path.join(args.output, f"diff_{filename}")
        
        similarity = compare_images(baseline_path, current_path, diff_path, args.threshold)
        
        if similarity is None:
            failed += 1
            continue
        
        passed_threshold = similarity >= args.threshold
        status = "✓" if passed_threshold else "✗"
        
        if passed_threshold:
            passed += 1
        else:
            failed += 1
        
        results.append({
            'filename': filename,
            'similarity': similarity,
            'passed': passed_threshold,
            'status': status
        })
        
        if not args.quiet or not passed_threshold:
            print(f"{status} {filename}: {similarity:.2f}%")
    
    # Summary
    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"Total: {len(common_files)}")
    print(f"Passed: {passed} ({(passed/len(common_files)*100):.1f}%)")
    print(f"Failed: {failed} ({(failed/len(common_files)*100):.1f}%)")
    print(f"Threshold: {args.threshold}%")
    
    if failed > 0:
        print(f"\n❌ Visual regression test FAILED")
        print(f"   Review diff images in: {args.output}")
        sys.exit(1)
    else:
        print(f"\n✓ Visual regression test PASSED")
        sys.exit(0)

if __name__ == '__main__':
    main()

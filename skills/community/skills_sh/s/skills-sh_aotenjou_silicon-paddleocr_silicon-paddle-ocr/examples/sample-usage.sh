#!/bin/bash
# Example usage script for OCR skill

# Set API key (or load from environment)
export SILICONFLOW_API_KEY="your_api_key_here"

# Path to the OCR script
OCR_SCRIPT="$(dirname "$0")/../scripts/ocr_skill.py"

echo "=== OCR Skill Examples ==="
echo ""

# Example 1: Single image recognition
echo "Example 1: Single image"
# python3 "$OCR_SCRIPT" /path/to/test.jpg
echo "python3 $OCR_SCRIPT /path/to/test.jpg"
echo ""

# Example 2: Batch processing with glob pattern
echo "Example 2: Batch processing"
# python3 "$OCR_SCRIPT" /path/to/images/*.png
echo "python3 $OCR_SCRIPT /path/to/images/*.png"
echo ""

# Example 3: JSON output format
echo "Example 3: JSON format output"
# python3 "$OCR_SCRIPT" --json /path/to/image.jpg
echo "python3 $OCR_SCRIPT --json /path/to/image.jpg"
echo ""

# Example 4: Custom prompt for specific task
echo "Example 4: Custom prompt for table extraction"
# python3 "$OCR_SCRIPT" -p "Please extract and format as Markdown table" /path/to/table.jpg
echo "python3 $OCR_SCRIPT -p \"Please extract and format as Markdown table\" /path/to/table.jpg"
echo ""

# Example 5: Save results to file
echo "Example 5: Save results to file"
# python3 "$OCR_SCRIPT" --json --output results.json /path/to/images/*.jpg
echo "python3 $OCR_SCRIPT --json --output results.json /path/to/images/*.jpg"
echo ""

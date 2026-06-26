#!/usr/bin/env python3
"""
MacVisionOCR - macOS Vision Text Recognition via Swift script

Uses Apple's Vision Framework via Swift script (confirmed working).

Requirements:
    - macOS 10.15+ (Catalina)
    - Swift (built-in on macOS)
"""

import subprocess
import sys
from pathlib import Path
from typing import Dict, List

# Path to Swift script
SWIFT_SCRIPT_PATH = Path(__file__).parent / "macvision_swift.swift"


class MacVisionOCR:
    """macOS Vision OCR wrapper using Swift script"""
    
    def __init__(self, verbose: bool = False):
        """Initialize MacVisionOCR processor."""
        self.verbose = verbose
        
        if sys.platform != 'darwin':
            raise RuntimeError("MacVisionOCR only works on macOS")
        
        if self.verbose:
            print("[INFO] MacVisionOCR initialized (via Swift)")
    
    def _estimate_confidence(self, text: str) -> float:
        """Estimate OCR confidence from text quality."""
        if not text:
            return 0.0
        
        printable = sum(1 for c in text if c.isprintable() or c in '\n\r\t')
        length_factor = min(1.0, len(text) / 100)
        quality = printable / max(len(text), 1)
        
        confidence = 0.85 + (0.15 * quality * length_factor)
        return round(min(confidence, 1.0), 4)
    
    def extract(self, image_path: str) -> Dict:
        """Extract text from image using Mac Vision OCR via Swift."""
        from time import time
        
        if sys.platform != 'darwin':
            return {
                'text': '',
                'confidence': 0.0,
                'error': 'MacVisionOCR only works on macOS',
                'processing_time_ms': 0
            }
        
        start_time = time()
        
        try:
            # Run Swift script with image path as argument
            result = subprocess.run(
                ['swift', str(SWIFT_SCRIPT_PATH), image_path],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode != 0:
                return {
                    'text': '',
                    'confidence': 0.0,
                    'error': result.stderr.strip(),
                    'processing_time_ms': (time() - start_time) * 1000
                }
            
            # Parse Chinese output
            lines = result.stdout.strip().split('\n')
            text_lines = []
            all_confidences = []
            
            current_text = None
            for line in lines:
                if line.startswith('文本：'):
                    current_text = line[3:].strip()
                elif line.startswith('置信度：') and current_text:
                    try:
                        conf_str = line[4:].strip()
                        # Swift returns confidence as percentage (0-100)
                        # Output format: "置信度：50.00%" -> need to divide by 100
                        numeric_part = conf_str.rstrip('%').strip()
                        confidence = float(numeric_part) / 100.0
                        text_lines.append(current_text)
                        all_confidences.append(confidence)
                        current_text = None
                    except (ValueError, IndexError):
                        pass
            
            full_text = '\n'.join(text_lines)
            processing_time = (time() - start_time) * 1000
            avg_confidence = sum(all_confidences) / len(all_confidences) if all_confidences else 0.0
            
            return {
                'text': full_text.strip(),
                'confidence': round(avg_confidence, 4),
                'line_count': len(text_lines),
                'processing_time_ms': round(processing_time, 2)
            }
            
        except subprocess.TimeoutExpired:
            return {
                'text': '',
                'confidence': 0.0,
                'error': 'MacVisionOCR timeout',
                'processing_time_ms': 60000
            }
        except Exception as e:
            processing_time = (time() - start_time) * 1000
            return {
                'text': '',
                'confidence': 0.0,
                'error': f"MacVision error: {str(e)}",
                'processing_time_ms': round(processing_time, 2)
            }
    
    def batch_extract(self, image_paths: List[str]) -> List[Dict]:
        """Process multiple images"""
        return [self.extract(path) for path in image_paths]


if __name__ == '__main__':
    import argparse
    
    if sys.platform != 'darwin':
        print("[ERROR] MacVisionOCR only works on macOS")
        sys.exit(1)
    
    if not SWIFT_SCRIPT_PATH.exists():
        print(f"[ERROR] Swift script not found: {SWIFT_SCRIPT_PATH}")
        sys.exit(1)
    
    parser = argparse.ArgumentParser(description='macOS Vision OCR via Swift')
    parser.add_argument('image', help='Image file to process')
    parser.add_argument('--verbose', '-v', action='store_true')
    args = parser.parse_args()
    
    processor = MacVisionOCR(verbose=args.verbose)
    result = processor.extract(args.image)
    
    print(f"\nText:\n{result['text']}")
    print(f"\nConfidence: {result['confidence']:.4f}")
    print(f"Lines: {result.get('line_count', 0)}")
    print(f"Time: {result.get('processing_time_ms', 0):.2f}ms")
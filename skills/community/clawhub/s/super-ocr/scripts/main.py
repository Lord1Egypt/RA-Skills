#!/usr/bin/env python3
"""
Super OCR - Main entry point with multi-engine parallel support

Usage:
    python main.py --image path/to/image.png [--engine auto|tesseract|paddle|macvision|all]
    python main.py --images ./images/*.png [--output ./results]
    
Examples:
    # Auto mode (recommended) - runs all available engines on macOS
    python main.py --image screenshot.png
    
    # Force Tesseract
    python main.py --image document.jpg --engine tesseract
    
    # Force PaddleOCR (high accuracy Chinese)
    python main.py --image chinese_menu.png --engine paddle
    
    # Force MacVision (macOS only)
    python main.py --image document.png --engine macvision
    
    # Run all available engines (macOS: tesseract + paddle + macvision)
    python main.py --image complex_doc.png --engine all
    
    # Batch mode with verbose output
    python main.py --images ./invoices/*.png --output ./results --verbose
"""

import argparse
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, List, Optional

# Add parent to path for imports when running from skill directory
sys.path.insert(0, str(Path(__file__).parent))

try:
    from engine.selector import select_engine, get_available_engines, select_best_result
    from engine.tesseract import TesseractOCR
    from engine.paddle import PaddleOCR
    from output_formatter import format_output
    from dependencies import check_all_dependencies
except ImportError as e:
    print(f"[ERROR] Import failed: {e}")
    print("\n[INSTALL INSTRUCTIONS]")
    print("="*60)
    print("Missing dependencies detected. Please install:")
    print()
    print("  pip install paddleocr paddlepaddle pytesseract pillow opencv-python numpy")
    print()
    print("Or for macOS with Tesseract:")
    print()
    print("  brew install tesseract")
    print("  pip install paddleocr paddlepaddle pytesseract pillow opencv-python numpy")
    print()
    print("For other platforms, see: https://github.com/openclaw/super-ocr")
    print("="*60)
    sys.exit(1)

# Try to import MacVision if on macOS
macvision_available = False
if sys.platform == 'darwin':
    try:
        from engine.macvision import MacVisionOCR
        macvision_available = True
        print("[INFO] MacVision OCR available")
    except ImportError:
        print("[WARN] MacVision OCR not available (pip install pyobjc)")

class OCRProcessor:
    """Main OCR processor with multi-engine parallel support"""
    
    def __init__(self, engine: str = 'auto', verbose: bool = False):
        """
        Initialize OCR processor.
        
        Args:
            engine: 'auto', 'tesseract', 'paddle', 'macvision', or 'all'
            verbose: Enable detailed logging
        """
        self.engine = engine.lower()
        self.verbose = verbose
        self.engines_to_use = []
        self.processors = {}
        
    def _select_and_init(self, image_path: str) -> None:
        """Select engines based on content and initialize all"""
        self.engines_to_use = select_engine(image_path, self.engine)
        
        if self.verbose:
            print(f"[INFO] Using engines: {', '.join(self.engines_to_use)}")
        
        # Initialize selected engines
        for eng in self.engines_to_use:
            try:
                if eng == 'tesseract':
                    self.processors['tesseract'] = TesseractOCR(verbose=self.verbose)
                elif eng == 'paddle':
                    self.processors['paddle'] = PaddleOCR(verbose=self.verbose)
                elif eng == 'macvision':
                    if macvision_available:
                        self.processors['macvision'] = MacVisionOCR(verbose=self.verbose)
                    else:
                        if self.verbose:
                            print(f"[WARN] MacVision not available on this platform")
                else:
                    if self.verbose:
                        print(f"[WARN] Unknown engine: {eng}")
            except Exception as e:
                if self.verbose:
                    print(f"[ERROR] Failed to initialize {eng}: {e}")
    
    def extract_parallel(self, image_path: str) -> Dict:
        """
        Extract text from image using multiple engines in parallel.
        
        Args:
            image_path: Path to input image
            
        Returns:
            Dict with text, confidence, selected_engine, average confidence, etc.
        """
        if not self.processors:
            self._select_and_init(image_path)
        
        if not self.processors:
            return {
                'text': '',
                'confidence': 0.0,
                'error': 'No engines available',
                'processing_time_ms': 0
            }
        
        start_time = time.time()
        results = []
        
        def run_engine(engine_name: str, processor):
            try:
                result = processor.extract(image_path)
                result['engine'] = engine_name
                return result
            except Exception as e:
                return {
                    'engine': engine_name,
                    'text': '',
                    'confidence': 0.0,
                    'error': str(e),
                    'processing_time_ms': 0
                }
        
        # Run engines in parallel
        with ThreadPoolExecutor(max_workers=len(self.processors)) as executor:
            futures = {
                executor.submit(run_engine, name, proc): name 
                for name, proc in self.processors.items()
            }
            
            for future in as_completed(futures):
                result = future.result()
                results.append(result)
                
                if self.verbose:
                    engine_name = result.get('engine', 'unknown')
                    if result.get('error'):
                        print(f"[{engine_name}] Error: {result['error']}")
                    else:
                        print(f"[{engine_name}] Confidence: {result.get('confidence', 0):.2%}, Time: {result.get('processing_time_ms', 0):.2f}ms")
        
        # Select best result using agent择优 logic
        best = select_best_result(
            results,
            preferred_engine='paddle'  # PaddleOCR preferred for Chinese
        )
        
        # Add summary info
        best['processing_time_ms'] = round((time.time() - start_time) * 1000, 2)
        best['total_engines'] = len(results)
        best['engines_used'] = self.engines_to_use
        
        return best
    
    def extract(self, image_path: str) -> Dict:
        """
        Extract text from image (legacy single-engine mode).
        
        Args:
            image_path: Path to input image
            
        Returns:
            Dict with text, confidence, engine, timing info
        """
        return self.extract_parallel(image_path)
    
    def batch_extract(self, image_paths: List[str]) -> List[Dict]:
        """Process multiple images"""
        return [self.extract(path) for path in image_paths]


def main():
    parser = argparse.ArgumentParser(
        description='Super OCR - Multi-engine parallel text extraction with intelligent selection'
    )
    
    # Input options
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('--image', help='Single image file to process')
    input_group.add_argument('--images', nargs='+', help='Multiple image files')
    
    # Engine selection
    parser.add_argument(
        '--engine',
        choices=['auto', 'tesseract', 'paddle', 'macvision', 'all'],
        default='auto',
        help='OCR engine(s) to use (default: auto)'
    )
    
    # Output options
    parser.add_argument(
        '--output', '-o',
        help='Output directory for results (default: stdout)'
    )
    parser.add_argument(
        '--format',
        choices=['text', 'json', 'structured'],
        default='json',
        help='Output format (default: json)'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    # Check dependencies
    if args.engine in ['auto', 'paddle', 'all']:
        check_all_dependencies(interactive=False)
    
    # Warn about macOS
    if sys.platform != 'darwin' and args.engine in ['macvision', 'all']:
        print("[WARN] MacVision only available on macOS")
    
    # Create processor
    processor = OCRProcessor(
        engine=args.engine,
        verbose=args.verbose
    )
    
    # Process images
    if args.image:
        image_paths = [args.image]
    else:
        # Expand glob patterns
        image_paths = []
        for pattern in args.images:
            image_paths.extend(sorted(Path().glob(pattern)))
        image_paths = [str(p) for p in image_paths]
    
    if args.verbose:
        print(f"\n[INFO] Processing {len(image_paths)} image(s)")
    
    # Extract text
    results = processor.batch_extract(image_paths)
    
    # Format and output
    output_func = format_output(args.format)
    
    if args.output:
        # Save to files
        output_path = Path(args.output)
        output_path.mkdir(parents=True, exist_ok=True)
        
        for image_path, result in zip(image_paths, results):
            stem = Path(image_path).stem
            output_file = output_path / f"{stem}_ocr.json"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            
            if args.verbose:
                print(f"[OK] Saved: {output_file}")
    else:
        # Print to stdout
        for image_path, result in zip(image_paths, results):
            print(f"\n{'='*60}")
            print(f"File: {image_path}")
            print(f"Selected Engine: {result.get('selected_engine', 'unknown')}")
            print(f"Confidence: {result.get('confidence', 0):.2%}")
            print(f"Total Engines: {result.get('total_engines', 1)}")
            print(f"Processes: {', '.join(result.get('engines_used', []))}")
            print(f"Time: {result.get('processing_time_ms', 0):.2f}ms")
            print(f"{'='*60}")
            
            if result.get('error'):
                print(f"[ERROR] {result['error']}")
            else:
                print(output_func(result))
    
    # Summary
    total_time = sum(r.get('processing_time_ms', 0) for r in results)
    if args.verbose and len(results) > 1:
        print(f"\n[INFO] Processed {len(results)} images in {total_time:.2f}ms")


if __name__ == '__main__':
    main()
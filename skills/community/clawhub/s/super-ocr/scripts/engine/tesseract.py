#!/usr/bin/env python3
"""
Tesseract OCR wrapper with optimized configuration for mixed Chinese/English content
"""

import logging
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional

try:
    import cv2
    import numpy as np
    from PIL import Image
except ImportError:
    print("[ERROR] Install dependencies: pip install opencv-python numpy pillow")
    sys.exit(1)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TesseractOCR:
    """Tesseract OCR processor with preprocessing pipeline"""
    
    def __init__(
        self,
        verbose: bool = False,
        lang: str = 'chi_sim+eng',
        psm: int = 6,
        oem: int = 3
    ):
        """
        Initialize Tesseract processor.
        
        Args:
            verbose: Enable detailed logging
            lang: Tesseract language code (e.g., 'eng', 'chi_sim', 'chi_sim+eng')
            psm: Page segmentation mode (default: 6, uniform block)
            oem: OCR engine mode (default: 3, LSTM only)
        """
        self.verbose = verbose
        self.lang = lang
        self.psm = psm
        self.oem = oem
        
        # Check tesseract availability
        self._check_tesseract()
        
    def _check_tesseract(self) -> bool:
        """Check if tesseract is installed"""
        try:
            result = subprocess.run(
                ['tesseract', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if self.verbose:
                logger.info(f"Tesseract version: {result.stdout.split()[2]}")
            return True
        except (subprocess.TimeoutExpired, FileNotFoundError, IndexError):
            logger.error("Tesseract not found. Install with:")
            logger.error("  macOS: brew install tesseract")
            logger.error("  Ubuntu: sudo apt install tesseract-ocr")
            logger.error("  Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki")
            return False
    
    def _preprocess_image(self, image_path: str) -> str:
        """
        Apply preprocessing pipeline.
        
        Returns:
            Path to processed image
        """
        if self.verbose:
            logger.info("Preprocessing image...")
        
        start_time = time.time()
        
        # Read image
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Could not load image: {image_path}")
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply bilateral filter (noise reduction + edge preservation)
        bilateral = cv2.bilateralFilter(gray, 9, 75, 75)
        
        # Adaptive thresholding for low contrast images
        min_val, max_val, _, _ = cv2.minMaxLoc(bilateral)
        contrast = max_val - min_val
        
        if contrast < 100:  # Low contrast
            processed = cv2.adaptiveThreshold(
                bilateral, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY, 11, 2
            )
        else:
            processed = bilateral
        
        # Save processed image (temp file)
        input_path = Path(image_path)
        processed_path = input_path.parent / f"{input_path.stem}_tess_processed.png"
        cv2.imwrite(str(processed_path), processed)
        
        if self.verbose:
            logger.info(f"Preprocessing completed in {time.time() - start_time:.2f}s")
        
        return str(processed_path)
    
    def _run_tesseract(
        self,
        image_path: str,
        lang: Optional[str] = None,
        psm: Optional[int] = None,
        oem: Optional[int] = None
    ) -> Dict:
        """
        Run Tesseract OCR.
        
        Returns:
            Dict with text, confidence, timing
        """
        if lang is None:
            lang = self.lang
        if psm is None:
            psm = self.psm
        if oem is None:
            oem = self.oem
        
        # Run tesseract
        cmd = [
            'tesseract', image_path, 'stdout',
            '-l', lang,
            '--psm', str(psm),
            '--oem', str(oem),
            '_stdout'
        ]
        
        if self.verbose:
            logger.info(f"Running: {' '.join(cmd)}")
        
        start_time = time.time()
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            processing_time = time.time() - start_time
            
            if result.returncode != 0:
                logger.error(f"Tesseract error: {result.stderr}")
                return {
                    'text': '',
                    'confidence': 0.0,
                    'error': result.stderr,
                    'processing_time_ms': processing_time * 1000
                }
            
            # Extract confidence if available
            text = result.stdout.strip()
            confidence = self._estimate_confidence(text)
            
            return {
                'text': text,
                'confidence': confidence,
                'processing_time_ms': processing_time * 1000
            }
            
        except subprocess.TimeoutExpired:
            return {
                'text': '',
                'confidence': 0.0,
                'error': 'Tesseract timeout',
                'processing_time_ms': 60000
            }
    
    def _estimate_confidence(self, text: str) -> float:
        """
        Estimate OCR confidence from output quality.
        
        Simple heuristic: longer text with fewer garbage characters = higher confidence
        """
        if not text:
            return 0.0
        
        # Count printable characters
        printable = sum(1 for c in text if c.isprintable() or c in '\n\r\t')
        
        # Length factor (more text = more reliable)
        length_factor = min(1.0, len(text) / 100)
        
        # Quality factor
        quality = printable / max(len(text), 1)
        
        # Combined score
        confidence = (0.6 * quality) + (0.4 * length_factor)
        
        return round(confidence, 2)
    
    def extract(self, image_path: str) -> Dict:
        """
        Extract text from image using Tesseract.
        
        Args:
            image_path: Path to input image
            
        Returns:
            Dict with text, confidence, processing time
        """
        if self.verbose:
            logger.info(f"Processing: {image_path}")
        
        start_time = time.time()
        
        # Preprocess
        processed_path = self._preprocess_image(image_path)
        
        try:
            # Run OCR
            result = self._run_tesseract(
                processed_path,
                lang=self.lang,
                psm=self.psm,
                oem=self.oem
            )
            
            # Clean up temp file
            Path(processed_path).unlink(missing_ok=True)
            
            result['processing_time_ms'] = round(time.time() - start_time, 2)
            
            return result
            
        except Exception as e:
            Path(processed_path).unlink(missing_ok=True)
            return {
                'text': '',
                'confidence': 0.0,
                'error': str(e),
                'processing_time_ms': (time.time() - start_time) * 1000
            }


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Tesseract OCR wrapper')
    parser.add_argument('image', help='Image file to process')
    parser.add_argument('--lang', default='chi_sim+eng', help='Language code')
    parser.add_argument('--verbose', '-v', action='store_true')
    args = parser.parse_args()
    
    processor = TesseractOCR(verbose=args.verbose, lang=args.lang)
    result = processor.extract(args.image)
    
    print(f"\nText:\n{result['text']}")
    print(f"\nConfidence: {result['confidence']:.2%}")
    print(f"Time: {result.get('processing_time_ms', 0):.2f}ms")
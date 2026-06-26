#!/usr/bin/env python3
"""
PaddleOCR wrapper - High accuracy Chinese OCR engine

Compatible with PaddleOCR 3.4.0+ API (predict() method returns list)
Based on Emma's testing: result[0][0][1][0] for text, result[0][0][1][1] for confidence
"""

import time
from pathlib import Path
from typing import Dict, List, Optional


class PaddleOCR:
    """PaddleOCR processor for high-accuracy text extraction"""
    
    def __init__(
        self,
        verbose: bool = False,
        lang: str = 'ch',
        use_angle_cls: bool = True
    ):
        """Initialize PaddleOCR - lang and use_angle_cls parameters"""
        self.verbose = verbose
        self.lang = lang
        self.use_angle_cls = use_angle_cls
        self._init_ocr()
    
    def _init_ocr(self) -> None:
        """Initialize PaddleOCR model"""
        from paddleocr import PaddleOCR
        
        self.ocr = PaddleOCR(lang=self.lang, use_angle_cls=self.use_angle_cls)
    
    def extract(self, image_path: str) -> Dict:
        """
        Extract text from image using PaddleOCR.
        
        Args:
            image_path: Path to input image
            
        Returns:
            Dict with text, confidence, results, processing time
        """
        if self.verbose:
            print(f"[PaddleOCR] Processing: {image_path}")
        
        start_time = time.time()
        
        try:
            # Run OCR - using predict() for PaddleOCR 3.4.0+
            result = self.ocr.predict(image_path)
            
            processing_time = time.time() - start_time
            
            # Parse results - legacy format: [[box], [text, confidence]]
            parsed = self._parse_results(result)
            parsed['processing_time_ms'] = round(processing_time * 1000, 2)
            
            return parsed
            
        except Exception as e:
            processing_time = time.time() - start_time
            return {
                'text': '',
                'confidence': 0.0,
                'error': str(e),
                'results': [],
                'processing_time_ms': round(processing_time * 1000, 2)
            }
    
    def _parse_results(self, results) -> Dict:
        """
        Parse PaddleOCR 3.4.0+ output format.
        
        PaddleOCR 3.4.0+ predict() returns dict with:
        - rec_texts: list of detected text strings
        - rec_scores: list of confidence scores
        - dt_polys: list of text polygon coordinates
        
        Returns:
            Dict with text, confidence, results, line_count
        """
        if not results or not results[0]:
            return {
                'text': '',
                'confidence': 0.0,
                'results': [],
                'error': 'No text detected'
            }
        
        # New format: result[0] is a dict with 'rec_texts' and 'rec_scores'
        result_dict = results[0]
        
        if isinstance(result_dict, dict):
            texts = result_dict.get('rec_texts', [])
            scores = result_dict.get('rec_scores', [])
            
            if not texts:
                return {
                    'text': '',
                    'confidence': 0.0,
                    'results': [],
                    'error': 'No text detected'
                }
            
            # Combine all text (PaddleOCR already splits by lines)
            full_text = '\n'.join(texts)
            
            # Calculate average confidence
            avg_confidence = sum(scores) / len(scores) if scores else 0.0
            
            # Build detailed results
            detailed_results = []
            for i, (text, score) in enumerate(zip(texts, scores)):
                # Get bbox if available (dt_polys is list of arrays)
                dt_polys = result_dict.get('dt_polys', [])
                bbox = None
                if i < len(dt_polys):
                    try:
                        poly = dt_polys[i]
                        if hasattr(poly, 'tolist'):
                            bbox = poly.tolist()
                        else:
                            bbox = poly
                    except:
                        bbox = None
                
                detailed_results.append({
                    'text': text,
                    'confidence': round(score, 4),
                    'bbox': bbox
                })
            
            return {
                'text': full_text.strip(),
                'confidence': round(avg_confidence, 4),
                'results': detailed_results,
                'line_count': len(texts)
            }
        else:
            # Fallback: handle legacy format if still used
            return self._parse_results_legacy(results)
    
    def _parse_results_legacy(self, results) -> Dict:
        """
        Legacy parser for backward compatibility.
        Old format: [[bbox], [text, confidence]]
        """
        if not results or not results[0]:
            return {
                'text': '',
                'confidence': 0.0,
                'results': [],
                'error': 'No text detected'
            }
        
        text_lines = []
        all_confidences = []
        
        for line in results:
            if len(line) < 2:
                continue
            
            box = line[0]
            
            if isinstance(line[1], (list, tuple)) and len(line[1]) >= 2:
                text, confidence = line[1][0], line[1][1]
            else:
                text, confidence = str(line[1]), 0.0
            
            text_lines.append(text)
            all_confidences.append(confidence)
        
        full_text = '\n'.join(text_lines)
        avg_confidence = sum(all_confidences) / len(all_confidences) if all_confidences else 0.0
        
        detailed_results = []
        for line in results:
            if len(line) >= 2:
                box = line[0]
                if isinstance(line[1], (list, tuple)) and len(line[1]) >= 2:
                    text, confidence = line[1][0], line[1][1]
                else:
                    text, confidence = str(line[1]), 0.0
                
                detailed_results.append({
                    'text': text,
                    'confidence': confidence,
                    'bbox': box
                })
        
        return {
            'text': full_text.strip(),
            'confidence': round(avg_confidence, 4),
            'results': detailed_results,
            'line_count': len(detailed_results)
        }
    
    def batch_extract(self, image_paths: List[str]) -> List[Dict]:
        """Process multiple images"""
        return [self.extract(path) for path in image_paths]


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='PaddleOCR wrapper')
    parser.add_argument('image', help='Image file to process')
    parser.add_argument('--lang', default='ch', help='Language code (ch, en, etc.)')
    parser.add_argument('--verbose', '-v', action='store_true')
    args = parser.parse_args()
    
    processor = PaddleOCR(verbose=args.verbose, lang=args.lang)
    result = processor.extract(args.image)
    
    print(f"\nText:\n{result['text']}")
    print(f"\nConfidence: {result['confidence']:.4f}")
    print(f"Lines detected: {result.get('line_count', 0)}")
    print(f"Time: {result.get('processing_time_ms', 0):.2f}ms")
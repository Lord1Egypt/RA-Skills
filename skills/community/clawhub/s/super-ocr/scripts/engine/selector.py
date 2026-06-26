#!/usr/bin/env python3
"""
Engine selector - Intelligent OCR engine selection logic

Rules:
1. Image contains Chinese characters → PaddleOCR (better Chinese support)
2. Image is simple text, English only → Tesseract (faster, lighter)
3. User explicitly requests engine → Use requested engine
4. Auto mode, mixed/unknown → PaddleOCR (higher accuracy)

Multi-engine parallel mode:
- Tesseract + PaddleOCR + MacVision (macOS only)
- Agent择优 based on confidence, language support, and speed
"""

import re
import sys
from pathlib import Path
from typing import Literal, List, Dict


def detect_chinese(content: str) -> bool:
    """Check if content contains Chinese characters"""
    # Chinese range: \u4e00-\u9fff
    return bool(re.search(r'[\u4e00-\u9fff]', content))


def analyze_image_complexity(image_path: str) -> str:
    """
    Analyze image complexity to determine optimal engine.
    
    Returns:
        'simple' or 'complex'
    """
    image_path_lower = Path(image_path).name.lower()
    
    complex_patterns = [
        'menu', 'invoice', 'contract', 'certificate', 
        'exam', 'form', 'table', 'receipt'
    ]
    
    if any(p in image_path_lower for p in complex_patterns):
        return 'complex'
    
    return 'simple'


def get_available_engines(image_path: str) -> List[str]:
    """
    Get list of available engines for the current platform.
    
    Args:
        image_path: Path to image (for platform-specific hints)
        
    Returns:
        List of engine names: ['tesseract', 'paddle', 'macvision']
    """
    engines = ['tesseract', 'paddle']  # Always available
    
    # Add MacVision on macOS
    if sys.platform == 'darwin':
        engines.append('macvision')
    
    return engines


def select_engine(
    image_path: str,
    requested_engine: Literal['auto', 'tesseract', 'paddle', 'macvision'] = 'auto'
) -> List[str]:
    """
    Select engines for OCR processing.
    
    In multi-engine mode, returns list of engines to run in parallel.
    
    Args:
        image_path: Path to image being processed
        requested_engine: User request or 'auto'
        
    Returns:
        List of engine names to use
    """
    available = get_available_engines(image_path)
    
    # Rule 1: User explicitly requested single engine
    if requested_engine != 'auto':
        if requested_engine in available:
            return [requested_engine]
        else:
            return available  # Fallback to all available
    
    # Rule 2: Check image path for hints
    path_lower = Path(image_path).name.lower()
    
    # Simple screenshots → Tesseract (fastest)
    simple_indicators = ['screenshot', 'snap', 'capture', 'screen']
    if any(ind in path_lower for ind in simple_indicators):
        return ['tesseract']
    
    # Complex documents → All engines (max accuracy)
    complex_indicators = ['menu', 'invoice', 'certificate', 'contract', 'receipt']
    if any(ind in path_lower for ind in complex_indicators):
        return available  # Run all available engines
    
    # Default: Run all available engines for best results
    return available


def select_best_result(
    results: List[Dict],
    preferred_engine: str = 'paddle'
) -> Dict:
    """
    Select the best OCR result from multiple engines.
    
    Args:
        results: List of OCR results from different engines
        preferred_engine: Preferred engine for tie-breaking
        
    Returns:
        Dict with selected result and metadata
    """
    if not results:
        return {
            'text': '',
            'confidence': 0.0,
            'error': 'No results',
            'selected_engine': None
        }
    
    # Filter valid results (with text)
    valid_results = [r for r in results if r.get('text', '').strip()]
    
    if not valid_results:
        return {
            'text': '',
            'confidence': 0.0,
            'error': 'All engines failed',
            'selected_engine': None
        }
    
    # Calculate weighted score
    for r in valid_results:
        engine = r.get('engine', 'unknown')
        
        # Engine quality weights
        quality_weights = {
            'paddle': 1.0,
            'macvision': 0.95,
            'tesseract': 0.9
        }
        
        # Language support weights (optional, can be extended)
        language_weights = {
            'paddle': 1.0,  # Best for Chinese
            'macvision': 0.85,  # Good for English, fair for Chinese
            'tesseract': 0.8  # Good for English, fair for Chinese
        }
        
        # Combined score
        base_confidence = r.get('confidence', 0)
        quality = quality_weights.get(engine, 0.8)
        language = language_weights.get(engine, 0.8)
        
        r['_score'] = base_confidence * quality * language
        r['_quality_weight'] = quality
        r['_language_weight'] = language
    
    # Sort by score
    sorted_results = sorted(valid_results, key=lambda x: x.get('_score', 0), reverse=True)
    
    # Select best
    best = sorted_results[0]
    
    return {
        'text': best.get('text', ''),
        'confidence': best.get('confidence', 0),
        'engine': best.get('engine', 'unknown'),
        'selected_engine': best.get('engine', 'unknown'),
        'processing_time_ms': sum(r.get('processing_time_ms', 0) for r in valid_results),
        'score': best.get('_score', 0),
        'other_results': sorted_results[1:]  # Include runner-ups for verification
    }
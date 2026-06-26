#!/usr/bin/env python3
"""
Preprocessor - Image preprocessing utilities for OCR

This module provides various image preprocessing techniques to improve OCR accuracy:
- Denoising
- Contrast enhancement
- Binarization
- Deskew
- Resolution enhancement
"""

import cv2
import numpy as np
from pathlib import Path
from typing import Optional


def denoise_image(image: np.ndarray, h: int = 10) -> np.ndarray:
    """
    Apply denoising to image.
    
    Args:
        image: Input image
        h: Denoising strength (higher = more denoising)
        
    Returns:
        Denoised image
    """
    return cv2.fastNlMeansDenoisingColored(image, None, h, h, 7, 21)


def enhance_contrast(image: np.ndarray) -> np.ndarray:
    """
    Enhance image contrast using CLAHE.
    
    Args:
        image: Input image (grayscale or BGR)
        
    Returns:
        Contrast-enhanced image
    """
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()
    
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    return clahe.apply(gray)


def binarize_image(image: np.ndarray, method: str = 'adaptive') -> np.ndarray:
    """
    Convert image to binary (black & white).
    
    Args:
        image: Input image (grayscale)
        method: 'adaptive', 'otsu', or 'fixed'
        
    Returns:
        Binary image
    """
    if method == 'adaptive':
        return cv2.adaptiveThreshold(
            image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 2
        )
    elif method == 'otsu':
        _, thresh = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return thresh
    else:  # fixed
        _, thresh = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
        return thresh


def deskew_image(image: np.ndarray) -> np.ndarray:
    """
    Correct image skew.
    
    Args:
        image: Input image
        
    Returns:
        Deskewed image
    """
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    
    return cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)


def resize_image(image: np.ndarray, scale: float = 2.0) -> np.ndarray:
    """
    Resize image for better OCR.
    
    Args:
        image: Input image
        scale: Scale factor (e.g., 2.0 = 2x larger)
        
    Returns:
        Resized image
    """
    new_size = tuple(int(dim * scale) for dim in image.shape[:2][::-1])
    return cv2.resize(image, new_size, interpolation=cv2.INTER_CUBIC)


def preprocess_pipeline(
    image: np.ndarray,
    denoise: bool = True,
    enhance: bool = True,
    binarize: bool = True,
    deskew: bool = False,
    resize_scale: Optional[float] = None
) -> np.ndarray:
    """
    Apply preprocessing pipeline.
    
    Args:
        image: Input image
        denoise: Apply denoising
        enhance: Enhance contrast
        binarize: Binarize image
        deskew: Correct skew
        resize_scale: Optional scale factor for resizing
        
    Returns:
        Preprocessed image
    """
    output = image.copy()
    
    steps = []
    
    if denoise:
        output = denoise_image(output)
        steps.append('denoise')
    
    if enhance:
        output = enhance_contrast(output)
        steps.append('enhance')
    
    if deskew:
        output = deskew_image(output)
        steps.append('deskew')
    
    if resize_scale and resize_scale > 1.0:
        output = resize_image(output, resize_scale)
        steps.append(f'resize_{resize_scale}x')
    
    if binarize and len(output.shape) == 2:
        output = binarize_image(output)
        steps.append('binarize')
    
    return output


def preprocess_file(
    input_path: str,
    output_path: Optional[str] = None,
    **kwargs
) -> str:
    """
    Preprocess an image file.
    
    Args:
        input_path: Input image file path
        output_path: Output file path (optional)
        **kwargs: Preprocessing parameters
        
    Returns:
        Output file path
    """
    # Read image
    image = cv2.imread(input_path)
    if image is None:
        raise ValueError(f"Could not load image: {input_path}")
    
    # Preprocess
    processed = preprocess_pipeline(image, **kwargs)
    
    # Save
    if output_path is None:
        input_path = Path(input_path)
        output_path = str(input_path.parent / f"{input_path.stem}_processed{input_path.suffix}")
    
    cv2.imwrite(output_path, processed)
    
    return output_path


def quick_preview(image: np.ndarray) -> None:
    """
    Display image preview using OpenCV.
    
    Args:
        image: Image to display
    """
    cv2.imshow('Preprocessed Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Image preprocessing for OCR')
    parser.add_argument('input', help='Input image file')
    parser.add_argument('--output', '-o', help='Output file path')
    parser.add_argument('--denoise', action='store_true', default=True, help='Apply denoising')
    parser.add_argument('--no-denoise', action='store_false', dest='denoise')
    parser.add_argument('--enhance', action='store_true', default=True, help='Enhance contrast')
    parser.add_argument('--no-enhance', action='store_false', dest='enhance')
    parser.add_argument('--binarize', action='store_true', default=True, help='Binarize image')
    parser.add_argument('--no-binarize', action='store_false', dest='binarize')
    parser.add_argument('--resize', type=float, help='Resize scale factor (e.g., 2.0)')
    
    args = parser.parse_args()
    
    output = preprocess_file(
        args.input,
        args.output,
        denoise=args.denoise,
        enhance=args.enhance,
        binarize=args.binarize,
        resize_scale=args.resize
    )
    
    print(f"Preprocessed image saved to: {output}")
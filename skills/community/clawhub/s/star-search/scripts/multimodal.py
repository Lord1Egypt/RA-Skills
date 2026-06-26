#!/usr/bin/env python3
"""实战 57 多模态 (2026-06-16) - tesseract OCR 版
- 图片 OCR: tesseract-ocr (chi_sim + eng)
- 端到端: 上传图片 -> OCR -> 走 /v1/search
- 端点: POST /v1/multimodal/search (multipart/form-data, file=image, optional text=context)
- 限制: 100MB 以下 png/jpg/jpeg/bmp/webp
"""
import os
import io
import time
import json
import asyncio
import subprocess
from pathlib import Path
from typing import Optional

UPLOAD_DIR = Path('/home/ubuntu/star-search/uploads')
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# tesseract 多语言
TESS_LANGS = 'chi_sim+eng'

def ocr_image(image_path: str) -> dict:
    """OCR 单张图片 -> {text, blocks, elapsed_ms}
    blocks: list of {text, confidence, bbox} (从 tsv 解析)
    """
    t0 = time.time()
    try:
        # 1) 简单 text 输出
        result = subprocess.run(
            ['tesseract', image_path, '-', '-l', TESS_LANGS, '--psm', '3'],
            capture_output=True, text=True, timeout=30
        )
        text = result.stdout.strip()
        # 2) 详细 tsv 输出 (含 confidence + bbox)
        result_tsv = subprocess.run(
            ['tesseract', image_path, '-', '-l', TESS_LANGS, '--psm', '3', 'tsv'],
            capture_output=True, text=True, timeout=30
        )
        blocks = []
        for line in result_tsv.stdout.split('\n')[1:]:  # skip header
            parts = line.split('\t')
            if len(parts) >= 12 and parts[11].strip() and parts[10] != '-1':
                try:
                    conf = float(parts[10])
                    if conf > 30:  # 过滤低置信度
                        blocks.append({
                            'level': int(parts[0]),
                            'page': int(parts[1]),
                            'block': int(parts[2]),
                            'par': int(parts[3]),
                            'line': int(parts[4]),
                            'word': int(parts[5]),
                            'text': parts[11],
                            'confidence': conf,
                            'bbox': {
                                'left': int(parts[6]),
                                'top': int(parts[7]),
                                'width': int(parts[8]),
                                'height': int(parts[9]),
                            }
                        })
                except (ValueError, IndexError):
                    pass
        return {
            'text': text,
            'blocks': blocks,
            'block_count': len(blocks),
            'engine': 'tesseract-4.1.1',
            'langs': TESS_LANGS,
            'elapsed_ms': int((time.time() - t0) * 1000),
        }
    except subprocess.TimeoutExpired:
        return {
            'text': '',
            'blocks': [],
            'block_count': 0,
            'error': 'tesseract timeout',
            'elapsed_ms': 30000,
        }
    except Exception as e:
        return {
            'text': '',
            'blocks': [],
            'block_count': 0,
            'error': str(e),
            'elapsed_ms': int((time.time() - t0) * 1000),
        }

def save_upload(file_bytes: bytes, suffix: str = '.png') -> str:
    """保存上传文件 + 返回路径"""
    name = f'mm_{int(time.time()*1000)}_{os.urandom(4).hex()}{suffix}'
    path = UPLOAD_DIR / name
    with open(path, 'wb') as f:
        f.write(file_bytes)
    return str(path)

def multimodal_search(file_bytes: bytes, context: str = '', file_suffix: str = '.png') -> dict:
    """端到端: 上传 -> OCR -> 走 search"""
    t0 = time.time()
    # 1) 保存
    file_path = save_upload(file_bytes, file_suffix)

    # 2) OCR
    ocr = ocr_image(file_path)
    if ocr.get('error'):
        return {'error': ocr['error'], 'stage': 'ocr', 'file_path': file_path}

    # 3) 构造 query
    ocr_text = ocr['text'].strip()
    if context and ocr_text:
        query = f"{context} 截图: {ocr_text[:200]}"
    elif context:
        query = context
    elif ocr_text:
        query = ocr_text
    else:
        return {'error': 'no text in image and no context provided', 'stage': 'query', 'ocr': ocr, 'file_path': file_path}

    # 4) 走 search (subprocess 独立进程, 避免 event loop 冲突)
    try:
        env = dict(os.environ)
        env['PYTHONPATH'] = '/home/ubuntu/.local/lib/python3.10/site-packages'
        import json as _json
        proc = subprocess.run(
            ['/usr/bin/python3', '/home/ubuntu/star-search/scripts/search_runner.py',
             _json.dumps({'query': query, 'top': 8})],
            capture_output=True, text=True, timeout=30, env=env
        )
        last = proc.stdout.strip().split('\n')[-1] if proc.stdout.strip() else '{}'
        out = _json.loads(last)
        results = out.get('results', [])
    except Exception as e:
        return {'error': f'search failed: {e}', 'stage': 'search', 'ocr': ocr, 'query': query, 'file_path': file_path}

    return {
        'query': query,
        'ocr': {
            'text': ocr_text,
            'block_count': ocr['block_count'],
            'engine': ocr.get('engine'),
            'elapsed_ms': ocr['elapsed_ms'],
        },
        'results': results,
        'result_count': len(results),
        'elapsed_ms': int((time.time() - t0) * 1000),
        'file_path': file_path,
    }

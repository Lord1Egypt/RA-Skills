#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
混拍图检测与子图切分引擎 v4.3.0
功能：
1. 检测混拍图（一张照片多张票据）
2. 行距聚类切分为单票子图
3. 边界接触时按票种边框特征二次切分
4. 保持原图-子图索引关系
"""

import os
import sys
import json
import shutil
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime

import numpy as np
from PIL import Image, ImageFilter, ImageOps

# === 轮廓检测后端 ===
CV2_AVAILABLE = False
try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    pass

PADDLE_AVAILABLE = False
try:
    from paddleocr import PaddleOCR
    PADDLE_AVAILABLE = True
except ImportError:
    pass


class InvoiceSplitter:
    """
    混发票据切分器
    
    检测策略（优先级）：
    1. PaddleOCR 检测模块（中文场景最佳）
    2. OpenCV 轮廓检测（通用）
    3. 投影切分（降级）
    
    切分策略：
    1. 行距聚类：DBSCAN 聚类检测框，分行分组
    2. 边界接触：检测相邻边框颜色/宽度特征，二次切分
    """
    
    def __init__(self, output_dir: str = None, backend: str = 'auto'):
        """
        初始化切分器
        
        Args:
            output_dir: 子图输出目录
            backend: 检测后端 ('auto'|'paddle'|'opencv'|'projection')
        """
        self.output_dir = output_dir or tempfile.mkdtemp()
        self.backend = self._select_backend(backend)
        self.index = []  # 原图-子图索引
        
    def _select_backend(self, backend: str) -> str:
        """选择检测后端"""
        if backend == 'paddle' and PADDLE_AVAILABLE:
            return 'paddle'
        elif backend == 'opencv' and CV2_AVAILABLE:
            return 'opencv'
        elif backend == 'projection':
            return 'projection'
        elif backend == 'auto':
            if PADDLE_AVAILABLE:
                return 'paddle'
            elif CV2_AVAILABLE:
                return 'opencv'
            else:
                return 'projection'
        return 'projection'
    
    def split(self, image_path: str, filename: str = None) -> Dict[str, Any]:
        """
        切分混拍图
        
        Args:
            image_path: 图片路径
            filename: 原文件名（用于索引）
        
        Returns:
            dict: 切分结果，含子图路径列表和索引
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"文件不存在: {image_path}")
        
        filename = filename or Path(image_path).name
        img = Image.open(image_path)
        img_array = np.array(img)
        
        # 票据检测框
        if self.backend == 'paddle':
            boxes = self._detect_with_paddle(img_array)
        elif self.backend == 'opencv':
            boxes = self._detect_with_opencv(img_array)
        else:
            boxes = self._detect_with_projection(img_array)
        
        # 如果没有检测到多张票据，返回原图
        if len(boxes) <= 1:
            return {
                'source_image': filename,
                'sub_image_count': 1,
                'sub_images': [{
                    'path': image_path,
                    'bbox': [0, 0, img.width, img.height],
                    'index': 0,
                    'is_original': True
                }],
                'backend': self.backend
            }
        
        # 行距聚类分行
        rows = self._cluster_rows(boxes)
        
        # 边界接触二次切分
        refined_boxes = self._refine_touching_boxes(img_array, boxes, rows)
        
        # 裁剪子图
        sub_images = []
        for i, bbox in enumerate(refined_boxes):
            x1, y1, x2, y2 = [int(v) for v in bbox]
            # 边界检查
            x1 = max(0, x1)
            y1 = max(0, y1)
            x2 = min(img.width, x2)
            y2 = min(img.height, y2)
            
            if x2 <= x1 or y2 <= y1:
                continue
            
            sub_img = img.crop((x1, y1, x2, y2))
            
            # 生成子图文件名
            stem = Path(filename).stem
            sub_filename = f"{stem}_sub_{i:03d}.png"
            sub_path = os.path.join(self.output_dir, sub_filename)
            
            os.makedirs(self.output_dir, exist_ok=True)
            sub_img.save(sub_path, 'PNG')
            
            sub_images.append({
                'path': sub_path,
                'filename': sub_filename,
                'bbox': [x1, y1, x2, y2],
                'index': i,
                'is_original': False
            })
        
        result = {
            'source_image': filename,
            'sub_image_count': len(sub_images),
            'sub_images': sub_images,
            'backend': self.backend,
            'created_at': datetime.now().isoformat()
        }
        
        self.index.append(result)
        return result
    
    def _detect_with_paddle(self, img_array: np.ndarray) -> List[List[int]]:
        """使用 PaddleOCR 检测票据区域"""
        try:
            ocr = PaddleOCR(use_angle_cls=True, lang='ch', show_log=False, det_db_thresh=0.3)
            result = ocr.ocr(img_array, cls=True, rec=False)
            
            boxes = []
            if result and result[0]:
                for line in result[0]:
                    if line and len(line) >= 4:
                        pts = line
                        x_coords = [p[0] for p in pts]
                        y_coords = [p[1] for p in pts]
                        x1, y1 = int(min(x_coords)), int(min(y_coords))
                        x2, y2 = int(max(x_coords)), int(max(y_coords))
                        boxes.append([x1, y1, x2, y2])
            
            return boxes
        except Exception as e:
            print(f"[Splitter] PaddleOCR 检测失败，降级到 OpenCV: {e}", file=sys.stderr)
            if CV2_AVAILABLE:
                return self._detect_with_opencv(img_array)
            return self._detect_with_projection(img_array)
    
    def _detect_with_opencv(self, img_array: np.ndarray) -> List[List[int]]:
        """使用 OpenCV 轮廓检测票据区域"""
        try:
            # 灰度 + 二值化
            if len(img_array.shape) == 3:
                gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            else:
                gray = img_array
            
            # 自适应二值化
            binary = cv2.adaptiveThreshold(
                gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2
            )
            
            # 膨胀连接邻近区域
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
            dilated = cv2.dilate(binary, kernel, iterations=2)
            
            # 轮廓检测
            contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            boxes = []
            for cnt in contours:
                x, y, w, h = cv2.boundingRect(cnt)
                # 过滤太小的区域
                if w > 100 and h > 100:
                    boxes.append([x, y, x + w, y + h])
            
            # 按 y 坐标排序
            boxes.sort(key=lambda b: b[1])
            return boxes
        except Exception as e:
            print(f"[Splitter] OpenCV 检测失败，降级到投影切分: {e}", file=sys.stderr)
            return self._detect_with_projection(img_array)
    
    def _detect_with_projection(self, img_array: np.ndarray) -> List[List[int]]:
        """使用投影切分（降级方案）"""
        try:
            if len(img_array.shape) == 3:
                gray = np.mean(img_array, axis=2).astype(np.uint8)
            else:
                gray = img_array
            
            # 水平投影：检测票据行
            # 使用边缘检测
            edges = np.abs(np.diff(gray.astype(float), axis=1))
            projection = np.mean(edges, axis=1)
            
            # 找波谷（行间空白）
            threshold = np.mean(projection) * 0.5
            gaps = projection < threshold
            
            # 找连续空白区域
            rows = []
            in_gap = False
            gap_start = 0
            
            for i, is_gap in enumerate(gaps):
                if is_gap and not in_gap:
                    gap_start = i
                    in_gap = True
                elif not is_gap and in_gap:
                    rows.append((gap_start, i))
                    in_gap = False
            
            if in_gap:
                rows.append((gap_start, len(gaps)))
            
            # 合并邻近间隙
            merged_rows = []
            for row in rows:
                if merged_rows and row[0] - merged_rows[-1][1] < 50:
                    merged_rows[-1] = (merged_rows[-1][0], row[1])
                else:
                    merged_rows.append(row)
            
            # 生成子图框
            height, width = gray.shape
            boxes = []
            prev_end = 0
            
            for start, end in merged_rows:
                if start - prev_end > 100:
                    boxes.append([0, prev_end, width, start])
                prev_end = end
            
            if height - prev_end > 100:
                boxes.append([0, prev_end, width, height])
            
            return boxes if boxes else [[0, 0, width, height]]
        except Exception as e:
            print(f"[Splitter] 投影切分失败: {e}", file=sys.stderr)
            # 最终降级：返回整图
            h, w = img_array.shape[:2]
            return [[0, 0, w, h]]
    
    def _cluster_rows(self, boxes: List[List[int]]) -> List[int]:
        """
        DBSCAN 行距聚类
        
        Returns:
            list: 每个框所属的行标签
        """
        if not boxes:
            return []
        
        # 计算中心点 y 坐标
        centers_y = [(b[1] + b[3]) / 2 for b in boxes]
        
        # DBSCAN 聚类
        from sklearn.cluster import DBSCAN
        try:
            clustering = DBSCAN(eps=50, min_samples=1).fit(np.array(centers_y).reshape(-1, 1))
            return clustering.labels_.tolist()
        except ImportError:
            # 无 sklearn，使用简单聚类
            return self._simple_cluster(centers_y, threshold=50)
    
    def _simple_cluster(self, values: List[float], threshold: float) -> List[int]:
        """简单阈值聚类"""
        if not values:
            return []
        
        labels = [0] * len(values)
        current_label = 0
        
        sorted_indices = sorted(range(len(values)), key=lambda i: values[i])
        
        for i in range(1, len(sorted_indices)):
            idx = sorted_indices[i]
            prev_idx = sorted_indices[i - 1]
            if abs(values[idx] - values[prev_idx]) > threshold:
                current_label += 1
            labels[idx] = current_label
        
        return labels
    
    def _refine_touching_boxes(self, img_array: np.ndarray, 
                                boxes: List[List[int]], 
                                rows: List[int]) -> List[List[int]]:
        """
        边界接触二次切分
        
        检测相邻边框特征（颜色、宽度），判断是否需要进一步切分
        """
        if len(boxes) <= 1:
            return boxes
        
        refined = []
        
        for i, box in enumerate(boxes):
            x1, y1, x2, y2 = box
            w = x2 - x1
            h = y2 - y1
            
            # 检查是否可能是多张票据粘连（宽度异常大）
            img_h, img_w = img_array.shape[:2]
            if w > img_w * 0.8 and h > img_h * 0.3:
                # 可能是横向并排的两张票
                split_x = self._find_vertical_split(img_array, box)
                if split_x:
                    refined.append([x1, y1, split_x, y2])
                    refined.append([split_x, y1, x2, y2])
                    continue
            
            refined.append(box)
        
        return refined
    
    def _find_vertical_split(self, img_array: np.ndarray, 
                              box: List[int]) -> Optional[int]:
        """找垂直分割线"""
        try:
            x1, y1, x2, y2 = box
            roi = img_array[y1:y2, x1:x2]
            
            if len(roi.shape) == 3:
                gray = np.mean(roi, axis=2).astype(np.uint8)
            else:
                gray = roi
            
            # 垂直投影
            v_projection = np.mean(gray, axis=0)
            
            # 找波谷（中间空白列）
            mid = len(v_projection) // 2
            search_range = min(mid // 2, 100)
            
            min_val = float('inf')
            min_idx = None
            
            for i in range(mid - search_range, mid + search_range):
                if 0 <= i < len(v_projection):
                    if v_projection[i] < min_val:
                        min_val = v_projection[i]
                        min_idx = i
            
            if min_idx and min_val < np.mean(v_projection) * 0.7:
                return x1 + min_idx
            
            return None
        except Exception:
            return None
    
    def get_index(self) -> List[Dict[str, Any]]:
        """获取索引"""
        return self.index
    
    def save_index(self, path: str):
        """保存索引到 JSON"""
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.index, f, ensure_ascii=False, indent=2)


# === 便捷函数 ===

def split_image(image_path: str, output_dir: str = None, 
                filename: str = None) -> Dict[str, Any]:
    """
    便捷切分函数
    
    Args:
        image_path: 图片路径
        output_dir: 输出目录
        filename: 原文件名
    
    Returns:
        dict: 切分结果
    """
    splitter = InvoiceSplitter(output_dir=output_dir)
    return splitter.split(image_path, filename=filename)


# ======================================================================
# CLI 入口
# ======================================================================

def main():
    parser = argparse.ArgumentParser(description='混拍图切分引擎 v4.3.0')
    parser.add_argument('--input', required=True, help='输入图片路径或目录')
    parser.add_argument('--output', help='输出目录（默认临时目录）')
    parser.add_argument('--index', help='索引输出路径（JSON）')
    parser.add_argument('--backend', choices=['auto', 'paddle', 'opencv', 'projection'],
                        default='auto', help='检测后端')
    
    args = parser.parse_args()
    
    splitter = InvoiceSplitter(output_dir=args.output, backend=args.backend)
    
    input_path = Path(args.input)
    
    if input_path.is_file():
        result = splitter.split(str(input_path), filename=input_path.name)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif input_path.is_dir():
        results = []
        supported_ext = {'.png', '.jpg', '.jpeg', '.tiff', '.bmp'}
        for f in input_path.iterdir():
            if f.suffix.lower() in supported_ext:
                try:
                    result = splitter.split(str(f), filename=f.name)
                    results.append(result)
                except Exception as e:
                    print(f"失败 {f.name}: {e}", file=sys.stderr)
        
        index_path = args.index or os.path.join(splitter.output_dir, 'split_index.json')
        splitter.save_index(index_path)
        print(f"\n索引已保存: {index_path}", file=sys.stderr)
        print(json.dumps({'total_images': len(results), 'results': results}, ensure_ascii=False, indent=2))
    else:
        print(f"路径不存在: {args.input}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()

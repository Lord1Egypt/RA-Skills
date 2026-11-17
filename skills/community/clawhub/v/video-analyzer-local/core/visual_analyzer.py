"""视觉分析模块 — 场景分类 + 物体检测 + OCR + 中文化增强"""

import os
from typing import Any, Dict, List, Optional
from pathlib import Path

from .logger import get_logger

# 导入中文映射
from .nlp import get_chinese_label, batch_translate_labels, SCENE_LABELS_CHINESE

logger = get_logger(__name__)


class VisualAnalyzer:
    """视频视觉内容分析器"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.visual_config = config.get("visual_analysis", {})
        self.enable_classification = self.visual_config.get("enable_scene_classification", True)
        self.enable_detection = self.visual_config.get("enable_object_detection", True)
        self.enable_ocr = self.visual_config.get("enable_ocr", True)
        self.sampling_interval = self.visual_config.get("sampling_interval", 3)
        self.ocr_lang = self.visual_config.get("ocr_lang", "ch")
    
    def analyze(self, scenes: Dict, video_path: str) -> Dict[str, Any]:
        """
        执行完整的视觉分析。
        
        Args:
            scenes: 场景检测结果
            video_path: 视频文件路径
            
        Returns:
            视觉分析结果
        """
        result = {
            "scenes": [],
            "summary": {
                "total_analyzed": 0,
                "scene_types": {},
                "object_counts": {},
                "ocr_text_count": 0,
            }
        }
        
        all_objects = {}
        all_scene_types = {}
        ocr_text_count = 0
        
        for scene in scenes.get("scenes", []):
            scene_result = self._analyze_scene(scene, video_path)
            result["scenes"].append(scene_result)
            
            # 汇总
            result["summary"]["total_analyzed"] += 1
            
            for stype in scene_result.get("scene_types", []):
                all_scene_types[stype] = all_scene_types.get(stype, 0) + 1
            
            for obj in scene_result.get("objects", []):
                name = obj.get("name", "unknown")
                all_objects[name] = all_objects.get(name, 0) + 1
            
            if scene_result.get("ocr_text"):
                ocr_text_count += 1
        
        result["summary"]["scene_types"] = all_scene_types
        result["summary"]["object_counts"] = all_objects
        result["summary"]["ocr_text_count"] = ocr_text_count
        
        return result
    
    def _analyze_scene(self, scene: Dict, video_path: str) -> Dict:
        """分析单个 scene"""
        keyframe_idx = scene.get("keyframe_index", 0)
        
        # 提取关键帧
        keyframe = self._extract_keyframe(video_path, keyframe_idx)
        
        result = {
            "scene_index": scene.get("index"),
            "start_time": scene.get("start_time"),
            "end_time": scene.get("end_time"),
            "scene_types": [],
            "scene_types_zh": [],  # ✨ 新增中文场景标签
            "objects": [],
            "ocr_text": "",
        }
        
        if keyframe is None:
            return result
        
        # 场景分类
        if self.enable_classification:
            result["scene_types"] = self._classify_scene(keyframe)
            # ✨ 中文化场景标签
            result["scene_types_zh"] = batch_translate_labels(result["scene_types"])
        
        # 物体检测
        if self.enable_detection:
            result["objects"] = self._detect_objects(keyframe)
            # ✨ 为每个物体添加中文标签
            for obj in result["objects"]:
                name = obj.get("name", "")
                obj["name_zh"] = get_chinese_label(name)
        
        # OCR
        if self.enable_ocr:
            result["ocr_text"] = self._ocr_frame(keyframe)
        
        return result
    
    def _extract_keyframe(self, video_path: str, frame_index: int) -> Optional:
        """提取指定帧索引的图像"""
        try:
            import cv2
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                return None
            
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
            ret, frame = cap.read()
            cap.release()
            
            return frame if ret else None
        except Exception:
            return None
    
    def _classify_scene(self, frame) -> List[str]:
        """
        对场景进行分类。
        使用轻量级 MobileNetV3 模型进行场景识别。
        """
        try:
            # 尝试使用 ONNX 模型进行场景分类
            return self._classify_with_onnx(frame)
        except Exception:
            # 回退：基于颜色直方图的简单分类
            return self._classify_with_color(frame)
    
    def _classify_with_onnx(self, frame) -> List[str]:
        """使用 ONNX 模型进行场景分类"""
        try:
            import numpy as np
            
            # 尝试加载场景分类模型
            model_path = self.visual_config.get("scene_model_path")
            
            # 如果模型不存在，则回退到颜色分析
            if not model_path or not os.path.exists(model_path):
                return self._classify_with_color(frame)
            
            import onnxruntime as ort
            
            # 预处理
            input_shape = (224, 224)
            img = self._preprocess_frame(frame, input_shape)
            
            # 推理
            session = ort.InferenceSession(model_path)
            input_name = session.get_inputs()[0].name
            outputs = session.run(None, {input_name: img})
            
            #解析结果
            class_names = self._get_scene_class_names()
            top_indices = np.argsort(outputs[0][0])[-3:][::-1]  # Top 3
            
            results = []
            for idx in top_indices:
                if idx < len(class_names):
                    results.append(class_names[idx])
            
            return results
        except Exception as e:
            logger.debug(f"ONNX 分类失败: {e}")
            return self._classify_with_color(frame)
    
    def _classify_with_color(self, frame) -> List[str]:
        """
        基于颜色特征的简单场景分类（无模型时的回退方案）。
        分析色调、亮度、饱和度分布来判断场景类型。
        """
        try:
            import cv2
            import numpy as np
            
            # HSV 分析
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            h, s, v = cv2.split(hsv)
            
            avg_h = np.mean(h)
            avg_s = np.mean(s)
            avg_v = np.mean(v)
            
            results = []
            
            # 简单规则分类
            if avg_v < 50:
                results.append("dark_scene")
            elif avg_v > 200:
                results.append("bright_scene")
            
            if avg_s < 30:
                results.append("indoor")
            elif avg_s > 100:
                results.append("colorful")
            
            # 色调分析
            if avg_h < 15 or avg_h > 165:
                results.append("warm_tone")
            elif 15 <= avg_h < 45:
                results.append("orange_tone")
            elif 45 <= avg_h < 75:
                results.append("green_nature")
            elif 75 <= avg_h < 130:
                results.append("blue_sky")
            
            return results if results else ["general"]
        except Exception:
            return ["general"]
    
    def _detect_objects(self, frame) -> List[Dict]:
        """
        进行物体检测。
        使用 YOLOv8-nano 或类似轻量模型。
        """
        try:
            model_path = self.visual_config.get("object_model_path")
            
            if not model_path or not os.path.exists(model_path):
                # 无模型时，尝试使用简单的人脸检测
                return self._detect_faces(frame)
            
            return self._detect_with_yolo(frame, model_path)
        except Exception:
            return self._detect_faces(frame)
    
    def _detect_with_yolo(self, frame, model_path: str) -> List[Dict]:
        """使用 YOLO 模型检测物体"""
        try:
            import numpy as np
            import onnxruntime as ort
            
            # 预处理
            input_shape = (640, 640)
            img = self._preprocess_frame(frame, input_shape)
            
            session = ort.InferenceSession(model_path)
            input_name = session.get_inputs()[0].name
            outputs = session.run(None, {input_name: img})
            
            # 解析 YOLO 输出
            predictions = outputs[0][0]  # 假设 shape: (1, N, 85)
            
            results = []
            class_names = self._get_object_class_names()
            
            for pred in predictions:
                confidence = pred[4]
                if confidence > 0.3:  # 置信度阈值
                    class_id = int(np.argmax(pred[5:]))
                    name = class_names[class_id] if class_id < len(class_names) else f"class_{class_id}"
                    
                    results.append({
                        "name": name,
                        "confidence": round(float(confidence), 3),
                        "bbox": [round(float(x), 2) for x in pred[:4]],
                    })
            
            return results
        except Exception as e:
            logger.debug(f"YOLO 检测失败: {e}")
            return self._detect_faces(frame)
    
    def _detect_faces(self, frame) -> List[Dict]:
        """使用 OpenCV Haar 级联进行人脸检测"""
        try:
            import cv2
            
            cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
            if not os.path.exists(cascade_path):
                return []
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cascade = cv2.CascadeClassifier(cascade_path)
            faces = cascade.detectMultiScale(gray, 1.1, 4)
            
            return [
                {"name": "face", "confidence": 0.5, "bbox": [int(x) for x in xywh]}
                for xywh in faces
            ]
        except Exception:
            return []
    
    def _ocr_frame(self, frame) -> str:
        """
        对帧进行 OCR 文字识别。
        使用 PaddleOCR 本地模型。
        """
        try:
            from paddleocr import PaddleOCR
            
            # 初始化 OCR（延迟加载）
            if not hasattr(self, '_ocr_engine'):
                self._ocr_engine = PaddleOCR(
                    use_angle_cls=True,
                    lang=self.ocr_lang,
                    show_log=False,
                    use_gpu=False,
                )
            
            # 执行 OCR
            result = self._ocr_engine.ocr(frame, cls=True)
            
            texts = []
            if result:
                for line in result:
                    if line:
                        for word_info in line:
                            if word_info and len(word_info) >= 2:
                                text = word_info[1][0] if isinstance(word_info[1], tuple) else str(word_info[1])
                                texts.append(text)
            
            return " ".join(texts)
        except ImportError:
            logger.debug("PaddleOCR 未安装，跳过 OCR")
            return ""
        except Exception as e:
            logger.debug(f"OCR 失败: {e}")
            return ""
    
    def _preprocess_frame(self, frame, target_size):
        """预处理帧为模型输入格式"""
        import numpy as np
        import cv2
        
        img = cv2.resize(frame, target_size)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img.astype(np.float32) / 255.0
        img = np.transpose(img, (2, 0, 1))  # HWC -> CHW
        img = np.expand_dims(img, axis=0)  # batch dim
        return img
    
    def _get_scene_class_names(self) -> List[str]:
        """获取场景类别名称"""
        return [
            "indoor", "outdoor", "nature", "urban", "office", "home",
            "street", "forest", "mountain", "beach", "kitchen", "bedroom",
            "classroom", "restaurant", "shop", "factory", "hospital",
            "library", "gym", "park", "bridge", "parking_lot"
        ]
    
    def _get_object_class_names(self) -> List[str]:
        """获取物体类别名称（COCO 80 类子集）"""
        return [
            "person", "bicycle", "car", "motorcycle", "airplane", "bus", "train",
            "truck", "boat", "traffic light", "fire hydrant", "stop sign",
            "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep",
            "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
            "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard",
            "sports ball", "kite", "baseball bat", "baseball glove", "skateboard",
            "surfboard", "tennis racket", "bottle", "wine glass", "cup", "fork",
            "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange",
            "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair",
            "couch", "potted plant", "bed", "dining table", "toilet", "tv",
            "laptop", "mouse", "remote", "keyboard", "cell phone", "microwave",
            "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase",
            "scissors", "teddy bear", "hair drier", "toothbrush"
        ]

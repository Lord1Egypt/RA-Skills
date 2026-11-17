"""跨模态语义融合模块 — 综合分析声音+画面的完整含义"""

from typing import Any, Dict, List

from .logger import get_logger

logger = get_logger(__name__)


class SemanticFusion:
    """跨模态语义融合器"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
    
    def fuse(self, aligned_data: Dict) -> Dict:
        """
        融合多模态数据为统一语义表示。
        
        Args:
            aligned_data: 对齐后的数据
            
        Returns:
            融合后的完整语义数据
        """
        logger.info("执行跨模态语义融合...")
        
        # 提取输入
        media_info = aligned_data.get("media_info", {})
        audio_alignments = aligned_data.get("audio_alignments", [])
        visual_alignments = aligned_data.get("visual_alignments", [])
        timeline = aligned_data.get("timeline", [])
        scene_dialog = aligned_data.get("scene_dialog_mapping", [])
        
        # 生成场景的综合描述
        enriched_scenes = self._enrich_scenes(scene_dialog, visual_alignments)
        
        # 提取关键主题
        themes = self._extract_themes(audio_alignments)
        
        # 计算整体指标
        metrics = self._compute_metrics(scene_dialog, media_info)
        
        # 生成视频摘要
        summary = self._generate_summary(scene_dialog, metrics, media_info)
        
        result = {
            "media_info": media_info,
            "scenes": enriched_scenes,
            "themes": themes,
            "metrics": metrics,
            "summary": summary,
            "alignment_stats": {
                "audio_alignment_count": sum(len(a) for a in audio_alignments),
                "visual_alignment_count": len(visual_alignments),
                "timeline_events": len(timeline),
            },
        }
        
        logger.info("语义融合完成")
        logger.info(f"   识别 {len(enriched_scenes)} 个场景")
        logger.info(f"   提取 {len(themes)} 个主题")
        
        return result
    
    def _enrich_scenes(
        self,
        scene_dialog: List[Dict],
        visual_alignments: List[Dict],
    ) -> List[Dict]:
        """
        为每个场景补充综合描述。
        
        将视觉信息和对话信息融合，生成场景的完整语义描述。
        """
        indexed_visual = {v.get("scene_index"): v for v in visual_alignments}
        
        enriched = []
        
        for sd in scene_dialog:
            idx = sd.get("scene_index")
            visual = indexed_visual.get(idx, {})
            
            scene_entry = {
                "index": idx,
                "time_range": {
                    "start": sd.get("start_time"),
                    "end": sd.get("end_time"),
                    "duration": sd.get("end_time", 0) - sd.get("start_time", 0),
                },
                "content": {
                    "dialog": sd.get("dialog_text", ""),
                    "is_silent": sd.get("is_silent", True),
                    "objects": visual.get("objects", []),
                    "scene_types": visual.get("scene_types", []),
                    "ocr_text": visual.get("ocr_text", ""),
                },
                "metrics": {
                    "dialog_coverage": sd.get("dialog_coverage", 0),
                    "avg_confidence": sd.get("avg_confidence", 0),
                    "object_count": len(visual.get("objects", [])),
                },
                "semantic_tags": [],
            }
            
            # 生成语义标签
            tags = self._generate_scene_tags(scene_entry)
            scene_entry["semantic_tags"] = tags
            
            enriched.append(scene_entry)
        
        return enriched
    
    def _generate_scene_tags(self, scene: Dict) -> List[str]:
        """为场景生成语义标签"""
        tags = []
        content = scene.get("content", {})
        metrics = scene.get("metrics", {})
        
        # 对话密度
        coverage = metrics.get("dialog_coverage", 0)
        if coverage > 0.8:
            tags.append("对话密集")
        elif coverage > 0.5:
            tags.append("对话适中")
        elif coverage > 0.1:
            tags.append("对话稀疏")
        else:
            tags.append("纯画面/无声")
        
        # 视觉内容
        objects = content.get("objects", [])
        if any(o.get("name") == "person" for o in objects):
            tags.append("含人物")
        if any(o.get("name") in ("car", "bus", "truck", "bicycle", "motorcycle") for o in objects):
            tags.append("含车辆")
        if any(o.get("name") in ("laptop", "tv", "cell phone", "keyboard", "mouse") for o in objects):
            tags.append("含电子设备")
        
        # 场景类型
        scene_types = content.get("scene_types", [])
        if "indoor" in scene_types:
            tags.append("室内")
        elif "outdoor" in scene_types:
            tags.append("室外")
        
        # OCR
        if content.get("ocr_text"):
            tags.append("含文字信息")
        
        # 识别置信度
        if metrics.get("avg_confidence", 0) > 0.8:
            tags.append("高置信度识别")
        
        return tags
    
    def _extract_themes(self, audio_alignments: List[List[Dict]]) -> List[Dict]:
        """
        从对话中提取主题。
        
        基于词频和关键词共现进行主题识别。
        """
        # 收集所有对话文本
        all_texts = []
        for scene_segs in audio_alignments:
            for seg in scene_segs:
                text = seg.get("text", "").strip()
                if text:
                    all_texts.append(text)
        
        full_text = " ".join(all_texts)
        
        if not full_text:
            return []
        
        # 简单分词和词频统计（基于空格和标点）
        try:
            import re
            from collections import Counter
            
            # 中英文分词
            # 英文：按空格和标点分
            # 中文：按字符
            words = re.findall(r'[\u4e00-\u9fff]|[a-zA-Z]+', full_text.lower())
            
            # 停用词
            stopwords = {
                "的", "了", "是", "在", "我", "有", "和", "就", "不", "人",
                "都", "一", "一个", "上", "也", "很", "到", "说", "要", "去",
                "你", "会", "着", "没有", "看", "好", "自己", "这", "他",
                "the", "a", "an", "is", "was", "are", "be", "been", "being",
                "and", "or", "but", "in", "on", "at", "to", "for", "of",
                "with", "by", "from", "as", "it", "this", "that", "i", "you",
                "he", "she", "we", "they", "do", "does", "did", "will", "would",
                "can", "could", "should", "may", "might", "must", "shall",
                "的", "a", "the",
            }
            
            # 过滤停用词和单字符（中文）
            filtered = [w for w in words if w not in stopwords and len(w) > 1]
            
            word_freq = Counter(filtered)
            
            # 取 Top 15 作为主题
            themes = []
            for word, count in word_freq.most_common(15):
                themes.append({
                    "keyword": word,
                    "frequency": count,
                    "relevance": round(min(count / len(filtered) * 10, 1.0), 3),
                })
            
            return themes
        except Exception as e:
            logger.debug(f"主题提取失败: {e}")
            return []
    
    def _compute_metrics(
        self,
        scene_dialog: List[Dict],
        media_info: Dict,
    ) -> Dict:
        """计算视频整体度量指标"""
        total_duration = media_info.get("duration", 0)
        
        total_dialog_duration = sum(sd.get("dialog_duration", 0) for sd in scene_dialog)
        silent_scenes = sum(1 for sd in scene_dialog if sd.get("is_silent"))
        total_scenes = len(scene_dialog)
        
        # 平均置信度
        confidences = [sd.get("avg_confidence", 0) for sd in scene_dialog if not sd.get("is_silent")]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0
        
        # 对话覆盖率
        dialog_coverage = total_dialog_duration / total_duration if total_duration > 0 else 0
        
        # 场景切换频率
        scene_switch_rate = total_scenes / (total_duration / 60) if total_duration > 0 else 0
        
        return {
            "total_duration": total_duration,
            "total_dialog_duration": round(total_dialog_duration, 2),
            "dialog_coverage": round(dialog_coverage, 4),
            "silent_scene_count": silent_scenes,
            "total_scenes": total_scenes,
            "avg_confidence": round(avg_confidence, 4),
            "scene_switch_rate": round(scene_switch_rate, 2),
            "audio_codec": media_info.get("audio_codec"),
            "video_codec": media_info.get("video_codec"),
        }
    
    def _generate_summary(self, scene_dialog: List[Dict], metrics: Dict, media_info: Dict) -> Dict:
        """生成视频内容摘要"""
        # 找出对话最密集的场景
        most_talkative = max(scene_dialog, key=lambda x: x.get("dialog_coverage", 0))
        
        # 找出最长场景
        longest = max(scene_dialog, key=lambda x: x.get("end_time", 0) - x.get("start_time", 0))
        
        # 找出纯画面场景
        visual_scenes = [sd for sd in scene_dialog if sd.get("is_silent")]
        
        # 生成一句摘要
        duration_str = self._format_duration(metrics.get("total_duration", 0))
        coverage = int(metrics.get("dialog_coverage", 0) * 100)
        
        summary_text = (
            f"本视频时长 {duration_str}，共 {metrics.get('total_scenes', 0)} 个场景，"
            f"对话覆盖率约 {coverage}%，"
            f"平均识别置信度 {int(metrics.get('avg_confidence', 0) * 100)}%。"
        )
        
        if visual_scenes:
            summary_text += f"包含 {len(visual_scenes)} 个纯画面场景。"
        
        return {
            "text": summary_text,
            "most_talkative_scene": {
                "index": most_talkative.get("scene_index"),
                "coverage": most_talkative.get("dialog_coverage"),
                "text_preview": most_talkative.get("dialog_text", "")[:100],
            },
            "longest_scene": {
                "index": longest.get("scene_index"),
                "duration": longest.get("end_time", 0) - longest.get("start_time", 0),
            },
            "visual_scene_count": len(visual_scenes),
        }
    
    @staticmethod
    def _format_duration(seconds: float) -> str:
        """格式化时长为可读字符串"""
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        
        if h > 0:
            return f"{h}小时{m}分{s}秒"
        elif m > 0:
            return f"{m}分{s}秒"
        else:
            return f"{s}秒"

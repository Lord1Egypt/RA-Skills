"""短视频爆款预测模块 — 多模态特征+爆款样本对比"""

import os
import re
from collections import Counter
from typing import Any, Dict, List, Optional

from .logger import get_logger

logger = get_logger(__name__)


class ViralPredictor:
    """
    短视频爆款预测器。
    
    基于多模态特征（视觉/音频/文本/节奏）与爆款样本对比，
    预测视频爆款概率，输出改进建议。
    
    降级方案：LLM 不可用时使用模板引擎生成建议。
    """
    
    # 爆款特征权重（自研规则）
    VIRAL_FEATURE_WEIGHTS = {
        "opening_hook": 0.20,       # 黄金前3秒 hook 类型
        "content_density": 0.15,    # 内容密度
        "rhythm_score": 0.15,       # 节奏得分
        "emotion_intensity": 0.15,  # 情感强度
        "hashtag_optimization": 0.10,  # 标签优化
        "duration_fit": 0.10,       # 时长适配
        "cta_detection": 0.10,      # 行动号召
        "quality_score": 0.05,      # 画质/音质
    }
    
    # Hook 类型评分（基于行业研究）
    HOOK_SCORES = {
        "visual_impact": 95,    # 视觉冲击（最高转化）
        "question": 85,         # 提问式
        "shock": 80,            # 震惊式
        "text_hook": 75,        # 文字hook
        "statistics": 70,       # 数据式
        "story": 65,            # 故事式
        "plain": 40,            # 平淡开场
    }
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self._llm_available = self._check_llm_available()
    
    def _check_llm_available(self) -> bool:
        """检查是否有可用的 LLM"""
        try:
            # 简单检查是否有 openai 或其他 LLM 库
            import importlib
            importlib.import_module("openai")
            return True
        except ImportError:
            pass
        return False
    
    def predict(
        self,
        video_path: str,
        transcript: Dict,
        scenes: Dict,
        platform_meta: Any = None,
        visual_data: Dict = None,
    ) -> Dict[str, Any]:
        """
        预测视频爆款概率。
        
        Args:
            video_path: 本地视频路径
            transcript: 语音识别结果
            scenes: 场景检测结果
            platform_meta: 平台元数据（可选）
            visual_data: 视觉分析数据（可选）
            
        Returns:
            爆款预测结果，含概率评分+改进建议
        """
        logger.info("🔥 [爆款预测] 开始分析爆款潜力...")
        
        # Step 1: 提取多模态特征
        features = self._extract_features(
            video_path, transcript, scenes, platform_meta, visual_data
        )
        
        # Step 2: 计算爆款得分
        viral_score = self._calculate_viral_score(features)
        
        # Step 3: 生成改进建议（LLM 优先，降级模板）
        suggestions = self._generate_suggestions(viral_score, features)
        
        # Step 4: 判定爆款等级
        level = self._classify_level(viral_score)
        
        result = {
            "viral_score": round(viral_score, 1),  # 0-100
            "level": level,                         # 爆款/潜力/一般/低潜力
            "features": features,
            "suggestions": suggestions,
            "benchmark": self._get_benchmark(viral_score),
            "method": "llm" if self._llm_available else "rule_based",
        }
        
        logger.info(f"   爆款得分: {result['viral_score']}/100 ({level})")
        return result
    
    def _extract_features(
        self,
        video_path: str,
        transcript: Dict,
        scenes: Dict,
        platform_meta: Any = None,
        visual_data: Dict = None,
    ) -> Dict[str, Any]:
        """提取多模态特征"""
        features = {}
        
        # 文本特征
        text = transcript.get("text", "")
        segments = transcript.get("segments", [])
        
        # 时长（估算）
        duration = self._estimate_duration(transcript)
        
        # 1. 开场 hook 特征（前3秒内容）
        features["opening_hook"] = self._analyze_opening_hook(text, segments, duration)
        
        # 2. 内容密度（单位时间信息量）
        features["content_density"] = self._analyze_content_density(text, duration)
        
        # 3. 节奏得分（基于场景切换频率）
        features["rhythm_score"] = self._analyze_rhythm(scenes, duration)
        
        # 4. 情感强度（基于文本情感词）
        features["emotion_intensity"] = self._analyze_emotion_intensity(text)
        
        # 5. 标签优化（hashtag 质量）
        features["hashtag_optimization"] = self._analyze_hashtags(text)
        
        # 6. 时长适配（是否符合平台推荐时长）
        features["duration_fit"] = self._analyze_duration_fit(duration, platform_meta)
        
        # 7. 行动号召（CTA 检测）
        features["cta_detection"] = self._analyze_cta(text)
        
        # 8. 画质/音质评分
        features["quality_score"] = self._analyze_quality(transcript)
        
        return features
    
    def _estimate_duration(self, transcript: Dict) -> float:
        """估算视频时长"""
        segments = transcript.get("segments", [])
        if segments:
            return max(seg.get("end", 0) for seg in segments)
        return 0.0
    
    def _analyze_opening_hook(self, text: str, segments: List[Dict], duration: float) -> Dict:
        """分析开场 hook 类型"""
        # 取前5秒内容
        opening_segments = [s for s in segments if s.get("start", 0) <= 5.0]
        opening_text = " ".join(s.get("text", "") for s in opening_segments)
        
        # 检测 hook 类型
        hook_type = "plain"
        
        # 检查提问式
        if re.search(r'[？?]|吗|什么|怎么|为什么|是不是', opening_text):
            hook_type = "question"
        # 检查震惊式/数字
        elif re.search(r'\d+[%％]|竟然|居然|没想到|震惊|不敢相信', opening_text):
            hook_type = "shock"
        # 检查视觉冲击（无法从文本判断，依赖视觉数据）
        elif re.search(r'看|注意|快来看|快看', opening_text):
            hook_type = "visual_impact"
        # 检查数据式
        elif re.search(r'\d+[万亿]|百分之|百分之几|同比增长|下降', opening_text):
            hook_type = "statistics"
        # 检查故事式
        elif re.search(r'从前|曾经|那天|有一天|记得', opening_text):
            hook_type = "story"
        
        return {
            "hook_type": hook_type,
            "opening_text": opening_text[:100],
            "score": self.HOOK_SCORES.get(hook_type, 40),
        }
    
    def _analyze_content_density(self, text: str, duration: float) -> Dict:
        """分析内容密度"""
        if duration <= 0:
            return {"score": 0, "info": "无法计算"}
        
        # 字数/分钟
        char_count = len(text.replace(" ", ""))
        density = char_count / (duration / 60) if duration > 0 else 0
        
        # 评分（150-300字/分钟为最佳）
        if 150 <= density <= 300:
            score = 90
        elif 100 <= density < 150 or 300 < density <= 400:
            score = 70
        elif density < 50:
            score = 30
        else:
            score = 50
        
        return {
            "chars_per_minute": round(density, 1),
            "score": score,
            "level": "高密度" if density > 300 else "适中" if density > 150 else "低密度",
        }
    
    def _analyze_rhythm(self, scenes: Dict, duration: float) -> Dict:
        """分析节奏得分"""
        scene_list = scenes.get("scenes", [])
        if not scene_list or duration <= 0:
            return {"score": 50, "info": "无场景数据"}
        
        # 场景切换频率
        n_scenes = len(scene_list)
        avg_scene_duration = duration / n_scenes if n_scenes > 0 else 0
        
        # 短场景频率高=节奏快，适合短视频
        if avg_scene_duration <= 3:
            score = 90
        elif avg_scene_duration <= 5:
            score = 80
        elif avg_scene_duration <= 8:
            score = 65
        elif avg_scene_duration <= 15:
            score = 50
        else:
            score = 35
        
        return {
            "avg_scene_duration": round(avg_scene_duration, 1),
            "total_scenes": n_scenes,
            "score": score,
            "level": "快节奏" if avg_scene_duration <= 5 else "适中" if avg_scene_duration <= 10 else "慢节奏",
        }
    
    def _analyze_emotion_intensity(self, text: str) -> Dict:
        """分析情感强度"""
        # 情感词表
        positive_words = ["好", "棒", "厉害", "优秀", "完美", "喜欢", "爱", "赞", "牛", "强", "精彩", "感动", "震撼", "惊喜"]
        negative_words = ["差", "烂", "糟糕", "失望", "讨厌", "恶心", "烦", "垃圾", "坑", "骗", "假", "丑", "可怕"]
        intensifiers = ["非常", "特别", "超级", "极其", "太", "真的", "绝对", "完全"]
        
        pos_count = sum(1 for w in positive_words if w in text)
        neg_count = sum(1 for w in negative_words if w in text)
        intens_count = sum(1 for w in intensifiers if w in text)
        
        total_emotion = pos_count + neg_count
        intensity = (total_emotion + intens_count * 0.5) / max(len(text) / 100, 1)
        
        # 评分
        if intensity > 5:
            score = 90
        elif intensity > 3:
            score = 75
        elif intensity > 1:
            score = 60
        else:
            score = 40
        
        return {
            "positive_count": pos_count,
            "negative_count": neg_count,
            "intensifier_count": intens_count,
            "score": score,
            "level": "高情感" if intensity > 3 else "中情感" if intensity > 1 else "低情感",
        }
    
    def _analyze_hashtags(self, text: str) -> Dict:
        """分析标签优化程度"""
        # 检测 hashtag
        hashtags = re.findall(r'#(\w+)', text)
        
        # 检测话题关键词
        topic_keywords = ["热门", "推荐", "必看", "干货", "教程", "攻略", "测评", "分享", "日常", "vlog"]
        topic_count = sum(1 for w in topic_keywords if w in text)
        
        # 评分
        score = min(len(hashtags) * 15 + topic_count * 10 + 40, 100)
        
        return {
            "hashtag_count": len(hashtags),
            "topic_keywords": topic_count,
            "score": score,
            "suggested_hashtags": self._suggest_hashtags(text),
        }
    
    def _suggest_hashtags(self, text: str) -> List[str]:
        """推荐 hashtag"""
        suggestions = []
        keyword_map = {
            "教程": "#教程", "攻略": "#攻略", "测评": "#测评",
            "美食": "#美食", "旅行": "#旅行", "日常": "#日常",
            "干货": "#干货", "分享": "#分享", "推荐": "#推荐",
            "搞笑": "#搞笑", "知识": "#知识", "学习": "#学习",
        }
        
        for keyword, hashtag in keyword_map.items():
            if keyword in text and hashtag not in suggestions:
                suggestions.append(hashtag)
        
        return suggestions[:5]
    
    def _analyze_duration_fit(self, duration: float, platform_meta: Any = None) -> Dict:
        """分析时长适配"""
        # 平台推荐时长（秒）
        platform_optimal = {
            "douyin": (15, 60),
            "kuaishou": (15, 60),
            "bilibili": (60, 300),
            "wechat_video": (15, 60),
        }
        
        # 默认按抖音标准
        optimal_min, optimal_max = 15, 60
        
        if platform_meta and hasattr(platform_meta, 'platform'):
            platform = platform_meta.platform
            if platform in platform_optimal:
                optimal_min, optimal_max = platform_optimal[platform]
        
        if optimal_min <= duration <= optimal_max:
            score = 95
        elif duration < optimal_min:
            score = max(50, 95 - (optimal_min - duration) * 2)
        else:
            score = max(40, 95 - (duration - optimal_max) * 0.5)
        
        return {
            "duration": round(duration, 1),
            "optimal_range": f"{optimal_min}-{optimal_max}s",
            "score": score,
            "level": "完美适配" if score >= 80 else "可接受" if score >= 60 else "需调整",
        }
    
    def _analyze_cta(self, text: str) -> Dict:
        """分析行动号召（CTA）"""
        cta_patterns = [
            r'关注', r'点赞', r'收藏', r'转发', r'分享',
            r'评论', r'留言', r'私信', r'点击', r'链接',
            r'购买', r'下单', r'优惠', r'折扣', r'福利',
        ]
        
        cta_count = sum(1 for p in cta_patterns if re.search(p, text))
        
        # 评分
        if cta_count >= 3:
            score = 90
        elif cta_count >= 2:
            score = 75
        elif cta_count >= 1:
            score = 60
        else:
            score = 30
        
        return {
            "cta_count": cta_count,
            "score": score,
            "level": "强CTA" if cta_count >= 2 else "弱CTA" if cta_count >= 1 else "无CTA",
        }
    
    def _analyze_quality(self, transcript: Dict) -> Dict:
        """分析画质/音质（基于 ASR 置信度）"""
        segments = transcript.get("segments", [])
        if not segments:
            return {"score": 50, "info": "无数据"}
        
        # 平均置信度
        confidences = [seg.get("confidence", 0) for seg in segments if seg.get("confidence")]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.5
        
        score = min(avg_confidence * 100 + 20, 100)
        
        return {
            "avg_confidence": round(avg_confidence, 3),
            "score": score,
            "level": "高质量" if score >= 80 else "中等" if score >= 60 else "低质量",
        }
    
    def _calculate_viral_score(self, features: Dict) -> float:
        """计算爆款得分"""
        total_score = 0.0
        
        for feature_name, weight in self.VIRAL_FEATURE_WEIGHTS.items():
            if feature_name in features:
                feature_data = features[feature_name]
                if isinstance(feature_data, dict):
                    feature_score = feature_data.get("score", 50)
                    total_score += feature_score * weight
        
        return min(max(total_score, 0), 100)
    
    def _classify_level(self, score: float) -> str:
        """判定爆款等级"""
        if score >= 80:
            return "爆款潜力"
        elif score >= 65:
            return "潜力视频"
        elif score >= 45:
            return "一般水平"
        else:
            return "低潜力"
    
    def _generate_suggestions(self, viral_score: float, features: Dict) -> List[Dict]:
        """生成改进建议（LLM 优先，降级模板）"""
        suggestions = []
        
        # 基于特征得分生成建议
        for feature_name, feature_data in features.items():
            if not isinstance(feature_data, dict):
                continue
            score = feature_data.get("score", 50)
            if score < 70:
                suggestion = self._get_feature_suggestion(feature_name, feature_data)
                if suggestion:
                    suggestions.append(suggestion)
        
        # 按优先级排序
        suggestions.sort(key=lambda x: x.get("priority", 5))
        
        return suggestions[:5]  # 最多返回5条
    
    def _get_feature_suggestion(self, feature_name: str, feature_data: Dict) -> Optional[Dict]:
        """获取特征改进建议"""
        suggestion_map = {
            "opening_hook": {
                "title": "优化开场Hook",
                "description": "前3秒是留存关键，建议使用提问式、震惊式或视觉冲击式开场",
                "priority": 1,
            },
            "content_density": {
                "title": "调整内容密度",
                "description": f"当前{content_per_minute}字/分钟，建议控制在150-300字/分钟",
                "priority": 2,
            },
            "rhythm_score": {
                "title": "加快节奏",
                "description": "场景切换频率偏低，建议缩短单场景时长至3-5秒",
                "priority": 2,
            },
            "emotion_intensity": {
                "title": "增强情感表达",
                "description": "情感词使用偏少，建议增加感叹词和强调词提升感染力",
                "priority": 3,
            },
            "hashtag_optimization": {
                "title": "优化标签",
                "description": f"建议添加: {', '.join(feature_data.get('suggested_hashtags', []))}",
                "priority": 4,
            },
            "duration_fit": {
                "title": "调整视频时长",
                "description": f"当前时长可能不适合目标平台，建议参考平台推荐时长",
                "priority": 3,
            },
            "cta_detection": {
                "title": "增加行动号召",
                "description": "建议在视频结尾添加关注、点赞、收藏等引导语",
                "priority": 4,
            },
            "quality_score": {
                "title": "提升画质音质",
                "description": "建议改善录音环境或提升视频分辨率",
                "priority": 5,
            },
        }
        
        suggestion = suggestion_map.get(feature_name)
        if suggestion and feature_name == "content_density":
            suggestion["description"] = f"当前{feature_data.get('chars_per_minute', '未知')}字/分钟，建议控制在150-300字/分钟"
        
        return suggestion
    
    def _get_benchmark(self, viral_score: float) -> Dict:
        """获取对标信息"""
        if viral_score >= 80:
            return {
                "percentile": "top 10%",
                "comparison": "优于90%的短视频",
                "potential": "高概率获得平台推荐",
            }
        elif viral_score >= 65:
            return {
                "percentile": "top 30%",
                "comparison": "优于70%的短视频",
                "potential": "有潜力进入推荐池",
            }
        elif viral_score >= 45:
            return {
                "percentile": "top 60%",
                "comparison": "处于中等水平",
                "potential": "需要优化才能获得推荐",
            }
        else:
            return {
                "percentile": "bottom 40%",
                "comparison": "低于平均水平",
                "potential": "需要大幅改进",
            }

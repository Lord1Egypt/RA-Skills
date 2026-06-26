"""
第四步：AI视频生成 + 拼接 + 配音
- 分三段各生成5秒视频
- TTS合成口播音频
- ffmpeg拼接+转场+合成音频
- 输出最终15秒成品
"""

import os
import logging
from typing import List, Optional

logger = logging.getLogger(__name__)

class VideoGenStep:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        
    def generate_segments(self, script_sections: List[str]) -> dict:
        """
        为每段文案生成5秒视频
        """
        # 检查可用API
        seeddance_key = os.environ.get("SEEDDANCE_API_KEY")
        # kling_key = os.environ.get("KLING_API_KEY")
        
        segments = []
        skipped = False
        
        if not seeddance_key: # and not kling_key:
            logger.info("未配置AI视频API，输出提示词供手动生成")
            for i, section in enumerate(script_sections, 1):
                segments.append({
                    "index": i,
                    "prompt": self._build_video_prompt(section),
                    "path": None
                })
            skipped = True
        else:
            logger.info("使用SeedDance生成分段视频")
            # TODO: 调用 seeddance-ai-video 生成每一段
            for i, section in enumerate(script_sections, 1):
                prompt = self._build_video_prompt(section)
                segments.append({
                    "index": i,
                    "prompt": prompt,
                    "path": None # 保存路径
                })
                
        return {
            "success": True,
            "skipped": skipped,
            "segments": segments,
            "aspect_ratio": (9, 16) # 竖屏
        }
    
    def generate_audio(self, script_sections: List[str]) -> dict:
        """
        使用TTS生成口播音频
        """
        # 检查TTS是否可用
        if not self._check_tts_available():
            logger.info("TTS不可用，需要手动配音")
            return {
                "success": True,
                "skipped": True,
                "reason": "TTS not available"
            }
            
        # TODO: 调用TTS生成三段音频
        audios = []
        for i, section in enumerate(script_sections, 1):
            audios.append({
                "index": i,
                "text": section,
                "path": None
            })
            
        return {
            "success": True,
            "skipped": False,
            "audios": audios
        }
    
    def concat_video_audio(self, video_segments, audio_segments, output_name) -> dict:
        """
        使用ffmpeg拼接视频并合成音频
        添加淡入淡出转场
        """
        if not video_segments or not all(s['path'] for s in video_segments):
            return {
                "success": True,
                "skipped": True,
                "reason": "需要手动拼接，所有分段生成后执行：" +
                          "ffmpeg -f concat -i list.txt -c copy output.mp4"
            }
            
        logger.info(f"正在拼接视频输出: {output_name}")
        # TODO: 调用 ffmpeg-video-editor 拼接
        
        output_path = self.output_dir / f"{output_name}_15s.mp4"
        
        return {
            "success": True,
            "output_path": str(output_path)
        }
    
    def _build_video_prompt(self, text: str) -> str:
        """构建视频生成提示词"""
        return f"""9:16竖屏短视频，时长5秒
内容：{text}
风格：清晰，自然，商品展示
稳定镜头，适合电商推广
"""
    def _check_tts_available(self) -> bool:
        """检查TTS是否可用"""
        # ClawX一般自带TTS
        try:
            import tts
            return True
        except ImportError:
            return False

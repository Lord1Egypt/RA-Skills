"""EDL (Edit Decision List) 导出器"""

import os
from datetime import datetime
from typing import Any, Dict, List, Optional

from ..logger import get_logger

logger = get_logger(__name__)


class EDLExporter:
    """
    导出标准 EDL 格式剪辑时间线。
    
    支持格式：
    - CMX3600 (Premiere Pro / DaVinci Resolve 兼容)
    - CSV (通用表格)
    - JSON (结构化数据)
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.editing_config = config.get("editing", {})
        self.edl_config = self.editing_config.get("edl", {})
        self.fps = self.edl_config.get("fps", 30)
    
    def export(
        self,
        timeline: Dict,
        output_path: str,
        format: str = "cmx3600",
    ) -> Optional[str]:
        """
        导出 EDL 文件。
        
        Args:
            timeline: 剪辑时间线
            output_path: 输出文件路径
            format: 导出格式 (cmx3600/csv/json)
            
        Returns:
            输出文件路径，失败返回 None
        """
        try:
            os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
            
            if format == "cmx3600":
                return self._export_cmx3600(timeline, output_path)
            elif format == "csv":
                return self._export_csv(timeline, output_path)
            elif format == "json":
                return self._export_json(timeline, output_path)
            else:
                logger.error(f"不支持的 EDL 格式: {format}")
                return None
                
        except Exception as e:
            logger.error(f"EDL 导出失败: {e}")
            return None
    
    def _export_cmx3600(self, timeline: Dict, output_path: str) -> str:
        """导出 CMX3600 格式（Premiere Pro / DaVinci Resolve 兼容）"""
        lines = []
        
        # 标题
        lines.append("TITLE: Video Analyzer Export")
        lines.append("FCM: NON-DROP FRAME")
        lines.append("")
        
        clips = timeline.get("clips", [])
        
        for i, clip in enumerate(clips):
            event_num = i + 1
            clip_name = f"CLIP_{event_num:03d}"
            
            # 时间码转换
            src_in = self._seconds_to_timecode(clip["source_start"])
            src_out = self._seconds_to_timecode(clip["source_end"])
            rec_in = self._seconds_to_timecode(clip["output_start"])
            rec_out = self._seconds_to_timecode(clip["output_end"])
            
            # 事件行
            lines.append(f"{event_num:03d}  {clip_name}  V     C        {src_in} {src_out} {rec_in} {rec_out}")
            
            # 如果有转场
            if i < len(clips) - 1:
                lines.append(f"* FROM CLIP NAME: {clip_name}")
                lines.append("")
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        
        logger.info(f"EDL 导出成功: {output_path}")
        return output_path
    
    def _export_csv(self, timeline: Dict, output_path: str) -> str:
        """导出 CSV 格式"""
        import csv
        
        clips = timeline.get("clips", [])
        
        with open(output_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "序号", "源起始", "源结束", "输出起始", "输出结束",
                "时长", "评分", "类型"
            ])
            
            for clip in clips:
                writer.writerow([
                    clip["index"],
                    self._seconds_to_timecode(clip["source_start"]),
                    self._seconds_to_timecode(clip["source_end"]),
                    self._seconds_to_timecode(clip["output_start"]),
                    self._seconds_to_timecode(clip["output_end"]),
                    clip["duration"],
                    clip.get("score", ""),
                    clip.get("type", ""),
                ])
        
        logger.info(f"CSV 导出成功: {output_path}")
        return output_path
    
    def _export_json(self, timeline: Dict, output_path: str) -> str:
        """导出 JSON 格式"""
        import json
        
        export_data = {
            "metadata": {
                "generator": "video-analyzer",
                "version": "4.0.0",
                "exported_at": datetime.now().isoformat(),
                "fps": self.fps,
            },
            "timeline": timeline,
        }
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"JSON 导出成功: {output_path}")
        return output_path
    
    def _seconds_to_timecode(self, seconds: float) -> str:
        """
        将秒数转换为时间码 HH:MM:SS:FF。
        
        Args:
            seconds: 秒数
            
        Returns:
            时间码字符串
        """
        if seconds < 0:
            seconds = 0
        
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        frames = int((seconds % 1) * self.fps)
        
        return f"{hours:02d}:{minutes:02d}:{secs:02d}:{frames:02d}"
    
    def generate_ffmpeg_commands(
        self, timeline: Dict, video_path: str, output_dir: str
    ) -> List[str]:
        """
        生成 ffmpeg 剪辑命令。
        
        Args:
            timeline: 剪辑时间线
            video_path: 原始视频路径
            output_dir: 输出目录
            
        Returns:
            ffmpeg 命令列表
        """
        commands = []
        clips = timeline.get("clips", [])
        
        os.makedirs(output_dir, exist_ok=True)
        
        for clip in clips:
            idx = clip["index"]
            start = clip["source_start"]
            duration = clip["duration"]
            
            output_path = os.path.join(output_dir, f"clip_{idx:03d}.mp4")
            
            cmd = (
                f'ffmpeg -ss {start:.3f} -i "{video_path}" '
                f'-t {duration:.3f} -c copy "{output_path}"'
            )
            
            commands.append(cmd)
        
        return commands

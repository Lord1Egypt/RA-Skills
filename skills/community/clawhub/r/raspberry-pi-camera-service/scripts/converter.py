"""
FFmpeg 异步格式转换模块
"""
from __future__ import annotations

import asyncio
import logging
import shutil
from pathlib import Path
from typing import Tuple

logger = logging.getLogger(__name__)


class FFmpegConverter:
    """基于 FFmpeg 的视频格式转换器"""
    
    def __init__(self, ffmpeg_path: str = "ffmpeg") -> None:
        self.ffmpeg_path: str = ffmpeg_path
        self.available: bool = self._check_ffmpeg()
        
    def _check_ffmpeg(self) -> bool:
        """检查 FFmpeg 是否可用"""
        return shutil.which(self.ffmpeg_path) is not None
    
    async def h264_to_mp4(
        self, 
        h264_path: str, 
        framerate: int = 30, 
        delete_original: bool = False
    ) -> Tuple[str | None, str | None]:
        """
        H264 转 MP4（极速封装，不重新编码）
        
        Returns:
            (mp4路径, 错误信息) - 成功时错误为 None
        """
        if not self.available:
            return None, "FFmpeg 未安装"
        
        h264_file: Path = Path(h264_path)
        if not h264_file.exists():
            return None, "原始文件不存在"
        
        mp4_path: Path = h264_file.with_suffix(".mp4")
        
        cmd: list[str] = [
            self.ffmpeg_path,
            "-y",                           # 覆盖输出
            "-framerate", str(framerate),   # 必须指定帧率（原始流无时间戳）
            "-i", str(h264_file),           # 输入
            "-c", "copy",                   # 复制编码（零质量损失）
            "-movflags", "+faststart",      # 优化网络播放
            str(mp4_path)
        ]
        
        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await asyncio.wait_for(
                proc.communicate(), 
                timeout=60.0
            )
            
            if proc.returncode == 0:
                if delete_original:
                    h264_file.unlink()
                return str(mp4_path), None
            else:
                error: str = stderr.decode()[-500:]  # 取最后 500 字符
                if mp4_path.exists():
                    mp4_path.unlink()
                return None, f"FFmpeg 错误: {error}"
                
        except asyncio.TimeoutError:
            if proc:
                proc.kill()
                await proc.wait()
            return None, "转换超时(60s)"
        except Exception as e:
            return None, str(e)
    
    async def h264_to_gif(
        self,
        h264_path: str,
        duration: int = 5,
        fps: int = 10,
        width: int = 320
    ) -> Tuple[str | None, str | None]:
        """
        H264 提取片段转 GIF（高质量调色板）
        
        Args:
            duration: 提取时长（秒）
            fps: GIF 帧率
            width: 输出宽度（高度自动保持比例）
        """
        if not self.available:
            return None, "FFmpeg 未安装"
        
        h264_file: Path = Path(h264_path)
        if not h264_file.exists():
            return None, "原始文件不存在"
        
        gif_path: Path = h264_file.with_suffix(".gif")
        
        # 高级 GIF 滤镜链：fps控制 + 缩放 + 调色板生成 + 抖动
        filter_complex: str = (
            f"fps={fps},scale={width}:-1:flags=lanczos,"
            f"split[s0][s1];[s0]palettegen=max_colors=128[p];"
            f"[s1][p]paletteuse=dither=bayer"
        )
        
        cmd: list[str] = [
            self.ffmpeg_path,
            "-t", str(duration),        # 只处理前 N 秒
            "-i", str(h264_file),
            "-vf", filter_complex,
            "-loop", "0",               # 无限循环
            "-y",
            str(gif_path)
        ]
        
        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await asyncio.wait_for(
                proc.communicate(),
                timeout=120.0
            )
            
            if proc.returncode == 0:
                return str(gif_path), None
            else:
                error: str = stderr.decode()[-500:]
                return None, f"GIF 转换失败: {error}"
                
        except asyncio.TimeoutError:
            if proc:
                proc.kill()
                await proc.wait()
            return None, "GIF 转换超时(120s)"
        except Exception as e:
            return None, str(e)
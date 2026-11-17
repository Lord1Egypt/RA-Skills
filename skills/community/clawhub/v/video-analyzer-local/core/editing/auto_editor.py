"""一键成片编辑器 — 输入高光检测结果，通过 ffmpeg filter_complex 链生成成片视频"""

import json
import os
import re
import subprocess
import tempfile
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from ..logger import get_logger

logger = get_logger(__name__)


# ==================== BGM 建议库 ====================
BGM_LIBRARY = {
    "励志": [
        {"name": "Inspiring Piano", "source": "freepd.com", "bpm": 120, "mood": "uplifting"},
        {"name": "Corporate Motivation", "source": "pixabay.com", "bpm": 110, "mood": "energetic"},
    ],
    "治愈": [
        {"name": "Calm Piano", "source": "freepd.com", "bpm": 80, "mood": "peaceful"},
        {"name": "Gentle Acoustic", "source": "pixabay.com", "bpm": 90, "mood": "warm"},
    ],
    "悬念": [
        {"name": "Suspense Tension", "source": "freepd.com", "bpm": 100, "mood": "tense"},
        {"name": "Dark Ambient", "source": "pixabay.com", "bpm": 70, "mood": "mysterious"},
    ],
    "欢快": [
        {"name": "Happy Ukulele", "source": "freepd.com", "bpm": 130, "mood": "cheerful"},
        {"name": "Upbeat Pop", "source": "pixabay.com", "bpm": 125, "mood": "fun"},
    ],
    "悲伤": [
        {"name": "Sad Piano", "source": "freepd.com", "bpm": 65, "mood": "melancholy"},
        {"name": "Emotional Strings", "source": "pixabay.com", "bpm": 72, "mood": "sorrowful"},
    ],
    "热血": [
        {"name": "Epic Cinematic", "source": "freepd.com", "bpm": 140, "mood": "powerful"},
        {"name": "Rock Energy", "source": "pixabay.com", "bpm": 135, "mood": "intense"},
    ],
}

# ==================== 成片风格预设 ====================
STYLE_PRESETS = {
    "口播精简": {
        "description": "去除冗余，保留核心口播内容",
        "max_clips": 15,
        "min_score": 0.5,
        "transition": "fade",
        "transition_duration": 0.3,
        "target_duration": 120,
        "subtitle_style": "minimal",
        "bgm_volume": 0.15,
    },
    "高光集锦": {
        "description": "精选高光片段，节奏紧凑",
        "max_clips": 10,
        "min_score": 0.65,
        "transition": "wipeleft",
        "transition_duration": 0.5,
        "target_duration": 60,
        "subtitle_style": "douyin",
        "bgm_volume": 0.25,
    },
    "预告片": {
        "description": "悬念感强，吸引点击",
        "max_clips": 8,
        "min_score": 0.7,
        "transition": "slideleft",
        "transition_duration": 0.8,
        "target_duration": 30,
        "subtitle_style": "movie",
        "bgm_volume": 0.3,
    },
}

# ==================== 平台规格 ====================
PLATFORM_SPECS = {
    "douyin": {
        "name": "抖音",
        "resolution": "1080x1920",
        "aspect_ratio": "9:16",
        "max_duration": 180,
        "video_codec": "libx264",
        "audio_codec": "aac",
        "video_bitrate": "4M",
        "audio_bitrate": "128k",
        "fps": 30,
        "title_max_chars": 55,
    },
    "bilibili": {
        "name": "B站",
        "resolution": "1920x1080",
        "aspect_ratio": "16:9",
        "max_duration": 600,
        "video_codec": "libx264",
        "audio_codec": "aac",
        "video_bitrate": "6M",
        "audio_bitrate": "192k",
        "fps": 30,
        "title_max_chars": 80,
    },
    "kuaishou": {
        "name": "快手",
        "resolution": "1080x1920",
        "aspect_ratio": "9:16",
        "max_duration": 120,
        "video_codec": "libx264",
        "audio_codec": "aac",
        "video_bitrate": "4M",
        "audio_bitrate": "128k",
        "fps": 30,
        "title_max_chars": 50,
    },
    "wechat_video": {
        "name": "微信视频号",
        "resolution": "1080x1920",
        "aspect_ratio": "9:16",
        "max_duration": 180,
        "video_codec": "libx264",
        "audio_codec": "aac",
        "video_bitrate": "4M",
        "audio_bitrate": "128k",
        "fps": 30,
        "title_max_chars": 60,
    },
}


class AutoEditor:
    """
    一键成片编辑器。

    输入高光检测结果（4维置信度 + 场景边界），生成 ffmpeg filter_complex 链：
    - 片段拼接
    - 转场效果
    - ASS 字幕烧录
    - BGM 混音 + 人声闪避（sidechaincompress）

    输出：
    - 成片视频（mp4）
    - EDL 映射表（JSON）
    - 平台规格包（仅导出，不自动发布）
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.editing_config = config.get("editing", {})
        self.auto_editor_config = self.editing_config.get("auto_editor", {})

        # 配置参数
        self.ffmpeg_path = self.auto_editor_config.get("ffmpeg_path", "ffmpeg")
        self.ffprobe_path = self.auto_editor_config.get("ffprobe_path", "ffprobe")
        self.temp_dir = self.auto_editor_config.get("temp_dir", ".temp/auto_editor")
        self.output_dir = self.auto_editor_config.get("output_dir", "output")

        # 确保临时目录存在
        os.makedirs(self.temp_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)

    def edit(
        self,
        video_path: str,
        highlights: List[Dict],
        scenes: Optional[List[Dict]] = None,
        subtitles_path: Optional[str] = None,
        style: str = "口播精简",
        platform: str = "douyin",
        bgm_path: Optional[str] = None,
        title: str = "",
    ) -> Dict[str, Any]:
        """
        一键成片主入口。

        Args:
            video_path: 源视频路径
            highlights: 高光片段列表 [{start, end, score, type}, ...]
            scenes: 场景边界列表
            subtitles_path: ASS 字幕文件路径
            style: 成片风格 (口播精简/高光集锦/预告片)
            platform: 目标平台 (douyin/bilibili/kuaishou/wechat_video)
            bgm_path: BGM 音频文件路径（可选）
            title: 视频标题

        Returns:
            {
                "output_path": "成片路径",
                "edl_map": "EDL映射表路径",
                "platform_package": "平台包目录",
                "duration": 总时长,
                "clips_used": 使用片段数,
                "bgm_suggestion": "BGM建议",
                "warnings": ["警告信息"],
            }
        """
        result = {
            "output_path": None,
            "edl_map": None,
            "platform_package": None,
            "duration": 0.0,
            "clips_used": 0,
            "bgm_suggestion": None,
            "warnings": [],
        }

        if not video_path or not os.path.exists(video_path):
            result["warnings"].append("源视频文件不存在")
            return result

        if not highlights:
            result["warnings"].append("无高光片段，无法生成成片")
            return result

        # 获取风格预设
        preset = STYLE_PRESETS.get(style, STYLE_PRESETS["口播精简"])

        # 获取平台规格
        spec = PLATFORM_SPECS.get(platform, PLATFORM_SPECS["douyin"])

        # 标题字数校验
        if len(title) > spec["title_max_chars"]:
            result["warnings"].append(
                f"标题字数({len(title)})超过{spec['name']}限制({spec['title_max_chars']}字)"
            )

        # 筛选高光片段
        filtered_clips = self._filter_clips(highlights, preset)
        if not filtered_clips:
            result["warnings"].append("筛选后无有效高光片段")
            return result

        # 生成 EDL 映射表
        edl_map_path = self._generate_edl_map(filtered_clips, video_path)
        result["edl_map"] = edl_map_path

        # 生成 ffmpeg filter_complex 链
        filter_chain = self._build_filter_chain(
            video_path=video_path,
            clips=filtered_clips,
            subtitles_path=subtitles_path,
            bgm_path=bgm_path,
            preset=preset,
            spec=spec,
        )

        if not filter_chain:
            result["warnings"].append("构建 filter_chain 失败")
            return result

        # 执行 ffmpeg 合成
        output_filename = f"edited_{style}_{platform}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
        output_path = os.path.join(self.output_dir, output_filename)

        success = self._run_ffmpeg(filter_chain, output_path)
        if not success:
            result["warnings"].append("ffmpeg 合成失败")
            return result

        result["output_path"] = output_path
        result["clips_used"] = len(filtered_clips)

        # 获取成片时长
        duration = self._get_video_duration(output_path)
        result["duration"] = duration

        # 检查时长限制
        if duration > spec["max_duration"]:
            result["warnings"].append(
                f"成片时长({duration:.1f}s)超过{spec['name']}限制({spec['max_duration']}s)"
            )

        # 生成平台规格包
        package_dir = self._export_platform_package(
            output_path, spec, platform, title
        )
        result["platform_package"] = package_dir

        # BGM 建议
        if not bgm_path:
            mood = self._detect_mood_from_highlights(highlights)
            suggestions = BGM_LIBRARY.get(mood, BGM_LIBRARY["治愈"])
            result["bgm_suggestion"] = {
                "mood": mood,
                "suggestions": suggestions,
            }

        logger.info(f"一键成片完成: {output_path}, 使用 {len(filtered_clips)} 个片段")
        return result

    def _filter_clips(
        self, highlights: List[Dict], preset: Dict
    ) -> List[Dict]:
        """根据风格预设筛选高光片段"""
        min_score = preset.get("min_score", 0.5)
        max_clips = preset.get("max_clips", 15)
        target_duration = preset.get("target_duration", 120)

        # 按分数降序排序
        sorted_clips = sorted(highlights, key=lambda x: x.get("score", 0), reverse=True)

        # 筛选满足最低分数的片段
        filtered = [c for c in sorted_clips if c.get("score", 0) >= min_score]

        # 限制最大片段数
        filtered = filtered[:max_clips]

        # 按时间顺序重新排序
        filtered.sort(key=lambda x: x.get("start", 0))

        # 控制总时长
        total_duration = 0
        result = []
        for clip in filtered:
            duration = clip.get("end", 0) - clip.get("start", 0)
            if total_duration + duration > target_duration:
                break
            result.append(clip)
            total_duration += duration

        return result

    def _build_filter_chain(
        self,
        video_path: str,
        clips: List[Dict],
        subtitles_path: Optional[str],
        bgm_path: Optional[str],
        preset: Dict,
        spec: Dict,
    ) -> Optional[str]:
        """构建 ffmpeg filter_complex 链"""
        try:
            inputs = []
            filters = []
            current_offset = 0.0
            transition_dur = preset.get("transition_duration", 0.5)

            for i, clip in enumerate(clips):
                start = clip.get("start", 0)
                end = clip.get("end", 0)

                # 输入编号：每个片段需要视频+音频
                v_in = i * 2
                a_in = i * 2 + 1

                # 提取片段
                inputs.extend([
                    "-ss", str(start), "-to", str(end),
                    "-i", video_path,
                ])

                # 缩放至目标分辨率
                w, h = spec["resolution"].split("x")
                filters.append(
                    f"[{v_in}:v]scale={w}:{h}:force_original_aspect_ratio=pad,"
                    f"setsar=1,fps={spec['fps']},"
                    f"setpts=PTS-STARTPTS[v{i}];"
                )

                # 音频处理
                filters.append(
                    f"[{a_in}:a]asetpts=PTS-STARTPTS[a{i}];"
                )

                current_offset += (end - start)

            # 拼接视频流
            v_concat_inputs = "".join(f"[v{i}]" for i in range(len(clips)))
            a_concat_inputs = "".join(f"[a{i}]" for i in range(len(clips)))

            if len(clips) == 1:
                # 单片段：直接烧字幕+输出
                final_v = "v0"
                final_a = "a0"
            else:
                # 多片段：concat 拼接
                filters.append(
                    f"{v_concat_inputs}concat=n={len(clips)}:v=1:a=0[vout];"
                )
                filters.append(
                    f"{a_concat_inputs}concat=n={len(clips)}:v=0:a=1[aout];"
                )
                final_v = "vout"
                final_a = "aout"

            # 字幕烧录
            if subtitles_path and os.path.exists(subtitles_path):
                filters.append(
                    f"[{final_v}]subtitles='{subtitles_path}'[vsub];"
                )
                final_v = "vsub"

            # BGM 混音 + 人声闪避
            if bgm_path and os.path.exists(bgm_path):
                bgm_idx = len(clips) * 2
                inputs.extend(["-i", bgm_path])
                bgm_volume = preset.get("bgm_volume", 0.2)

                # sidechaincompress: 有人声时降低 BGM
                filters.append(
                    f"[{final_a}][{bgm_idx}:a]sidechaincompress=threshold=0.01:ratio=8[acompressed];"
                )
                filters.append(
                    f"[acompressed]volume=volume={bgm_volume}[afinal];"
                )
                final_a = "afinal"
            else:
                # 无 BGM：仅音量归一化
                filters.append(f"[{final_a}]volume=volume=1.0[afinal];")
                final_a = "afinal"

            filter_str = "".join(filters)

            # 构建完整命令参数（返回列表形式）
            cmd = [self.ffmpeg_path, "-y"]
            cmd.extend(inputs)
            cmd.extend([
                "-filter_complex", filter_str,
                "-map", f"[{final_v}]",
                "-map", f"[{final_a}]",
                "-c:v", spec["video_codec"],
                "-b:v", spec["video_bitrate"],
                "-c:a", spec["audio_codec"],
                "-b:a", spec["audio_bitrate"],
                "-shortest",
            ])

            return cmd

        except Exception as e:
            logger.error(f"构建 filter_chain 失败: {e}")
            return None

    def _run_ffmpeg(self, cmd: List[str], output_path: str) -> bool:
        """执行 ffmpeg 命令"""
        try:
            # 将 filter_complex 列表转为完整命令
            full_cmd = cmd + [output_path]

            logger.info(f"执行 ffmpeg: {' '.join(full_cmd[:10])}...")

            result = subprocess.run(
                full_cmd,
                capture_output=True,
                text=True,
                timeout=600,
            )

            if result.returncode != 0:
                logger.error(f"ffmpeg 错误: {result.stderr[:500]}")
                return False

            return os.path.exists(output_path) and os.path.getsize(output_path) > 0

        except subprocess.TimeoutExpired:
            logger.error("ffmpeg 执行超时")
            return False
        except Exception as e:
            logger.error(f"ffmpeg 执行异常: {e}")
            return False

    def _generate_edl_map(
        self, clips: List[Dict], video_path: str
    ) -> str:
        """生成 EDL 映射表"""
        edl_data = {
            "source_video": video_path,
            "generated_at": datetime.now().isoformat(),
            "total_clips": len(clips),
            "clips": [],
        }

        for i, clip in enumerate(clips):
            edl_data["clips"].append({
                "clip_index": i + 1,
                "source_start": clip.get("start", 0),
                "source_end": clip.get("end", 0),
                "source_duration": clip.get("end", 0) - clip.get("start", 0),
                "score": clip.get("score", 0),
                "type": clip.get("type", "未知"),
            })

        edl_path = os.path.join(
            self.temp_dir,
            f"edl_map_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        )

        with open(edl_path, "w", encoding="utf-8") as f:
            json.dump(edl_data, f, ensure_ascii=False, indent=2)

        return edl_path

    def _export_platform_package(
        self,
        video_path: str,
        spec: Dict,
        platform: str,
        title: str,
    ) -> str:
        """导出平台规格包（仅导出，不自动发布）"""
        package_dir = os.path.join(
            self.output_dir,
            f"package_{platform}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        )
        os.makedirs(package_dir, exist_ok=True)

        # 复制视频到包目录
        import shutil
        video_name = f"video.{video_path.rsplit('.', 1)[-1]}"
        dest_video = os.path.join(package_dir, video_name)
        shutil.copy2(video_path, dest_video)

        # 生成封面帧（取第一帧）
        cover_path = os.path.join(package_dir, "cover.jpg")
        self._extract_cover_frame(dest_video, cover_path)

        # 生成发布说明
        readme_path = os.path.join(package_dir, "publish_readme.txt")
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(f"# {spec['name']} 发布规格包\n\n")
            f.write(f"平台: {spec['name']}\n")
            f.write(f"分辨率: {spec['resolution']} ({spec['aspect_ratio']})\n")
            f.write(f"视频编码: {spec['video_codec']}\n")
            f.write(f"音频编码: {spec['audio_codec']}\n")
            f.write(f"帧率: {spec['fps']}fps\n")
            f.write(f"最大时长: {spec['max_duration']}s\n")
            f.write(f"标题字数限制: {spec['title_max_chars']}字\n")
            f.write(f"当前标题: {title}\n")
            f.write(f"标题字数: {len(title)}\n\n")
            f.write("文件清单:\n")
            f.write(f"  - {video_name}: 成片视频\n")
            f.write(f"  - cover.jpg: 封面帧\n")
            f.write(f"  - publish_readme.txt: 本文件\n\n")
            f.write("注意: 本包仅导出，未自动发布。请自行上传到目标平台。\n")

        return package_dir

    def _extract_cover_frame(self, video_path: str, output_path: str) -> bool:
        """提取视频第一帧作为封面"""
        try:
            cmd = [
                self.ffmpeg_path, "-y",
                "-i", video_path,
                "-vframes", "1",
                "-q:v", "2",
                output_path,
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            return result.returncode == 0
        except Exception as e:
            logger.error(f"提取封面帧失败: {e}")
            return False

    def _get_video_duration(self, video_path: str) -> float:
        """获取视频时长"""
        try:
            cmd = [
                self.ffprobe_path,
                "-v", "quiet",
                "-print_format", "json",
                "-show_format",
                video_path,
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                data = json.loads(result.stdout)
                return float(data.get("format", {}).get("duration", 0))
        except Exception as e:
            logger.error(f"获取视频时长失败: {e}")
        return 0.0

    def _detect_mood_from_highlights(self, highlights: List[Dict]) -> str:
        """从高光片段推断情绪标签"""
        if not highlights:
            return "治愈"

        avg_score = sum(h.get("score", 0) for h in highlights) / len(highlights)
        strong_count = sum(1 for h in highlights if h.get("score", 0) >= 0.7)

        if strong_count >= len(highlights) * 0.6:
            return "热血"
        elif avg_score >= 0.6:
            return "欢快"
        elif avg_score >= 0.5:
            return "励志"
        else:
            return "治愈"

    @staticmethod
    def get_available_styles() -> Dict[str, str]:
        """获取可用的成片风格"""
        return {k: v["description"] for k, v in STYLE_PRESETS.items()}

    @staticmethod
    def get_available_platforms() -> Dict[str, str]:
        """获取可用的平台规格"""
        return {k: v["name"] for k, v in PLATFORM_SPECS.items()}

    @staticmethod
    def get_bgm_suggestions(mood: str) -> List[Dict]:
        """获取 BGM 建议"""
        return BGM_LIBRARY.get(mood, [])

"""自动字幕翻译器 — 通过白名单桥接 cn-llm-router 翻译任务，生成多语言字幕"""

import json
import os
import re
import subprocess
import tempfile
from datetime import datetime
from typing import Any, Dict, List, Optional

from ..logger import get_logger
from .glossary_engine import GlossaryEngine

logger = get_logger(__name__)


# 支持的目标语言
SUPPORTED_LANGUAGES = {
    "en": {"name": "English", "code": "en"},
    "ja": {"name": "日本語", "code": "ja"},
    "ko": {"name": "한국어", "code": "ko"},
    "fr": {"name": "Français", "code": "fr"},
    "de": {"name": "Deutsch", "code": "de"},
    "es": {"name": "Español", "code": "es"},
    "ru": {"name": "Русский", "code": "ru"},
}

# 默认术语表（可扩展）
DEFAULT_GLOSSARY = {
    "AI": "AI",
    "人工智能": "人工智能",
    "大模型": "大模型",
    "短视频": "短视频",
    "直播": "直播",
    "粉丝": "粉丝",
    "流量": "流量",
    "带货": "带货",
    "爆款": "爆款",
    "算法": "算法",
}


class SubtitleTranslator:
    """
    自动字幕翻译器。

    通过白名单桥接 cn-llm-router 翻译任务：
    - subprocess 调用 router.py chat --task translate --json
    - 按字幕批量翻译 + 术语表约束
    - 生成 EN/JP/KO 等语言的 SRT/ASS/VTT

    未安装 cn-llm-router 时：仅输出中文字幕 + 提示安装
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.editing_config = config.get("editing", {})
        self.translator_config = self.editing_config.get("translator", {})

        # 配置参数
        self.router_path = self.translator_config.get("router_path", None)
        self.output_dir = self.translator_config.get("output_dir", "output/subtitles")
        self.temp_dir = self.translator_config.get("temp_dir", ".temp/translator")
        self.glossary_path = self.translator_config.get("glossary_path", None)
        self.batch_size = self.translator_config.get("batch_size", 10)
        self.timeout = self.translator_config.get("timeout", 120)

        # 确保目录存在
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.temp_dir, exist_ok=True)

        # 加载术语表（旧版扁平表，向后兼容）
        self.glossary = self._load_glossary()

        # v4.7 术语表引擎（前置替换 + 后置校对 + 待确认清单）
        self.glossary_engine = GlossaryEngine(config)
        self.glossary_enabled = self.translator_config.get("glossary_enabled", True)

    def translate_subtitles(
        self,
        subtitles_path: str,
        target_lang: str = "en",
        output_format: str = "srt",
    ) -> Dict[str, Any]:
        """
        翻译字幕文件。

        Args:
            subtitles_path: 源字幕文件路径（SRT/ASS）
            target_lang: 目标语言代码 (en/ja/ko/fr/de/es/ru)
            output_format: 输出格式 (srt/ass/vtt)

        Returns:
            {
                "output_path": "输出路径",
                "lang": "目标语言",
                "format": "输出格式",
                "translated_count": 翻译条数,
                "skipped_count": 跳过条数,
                "warnings": ["警告"],
                "used_fallback": False,
            }
        """
        result = {
            "output_path": None,
            "lang": target_lang,
            "format": output_format,
            "translated_count": 0,
            "skipped_count": 0,
            "warnings": [],
            "used_fallback": False,
            "glossary_report": None,
            "pending_list_path": None,
        }

        if not subtitles_path or not os.path.exists(subtitles_path):
            result["warnings"].append("字幕文件不存在")
            return result

        if target_lang not in SUPPORTED_LANGUAGES:
            result["warnings"].append(f"不支持的目标语言: {target_lang}")
            return result

        # 检查 cn-llm-router 是否可用
        router_cmd = self._find_router()
        if not router_cmd:
            result["warnings"].append(
                "未找到 cn-llm-router，仅输出中文字幕。"
                "请安装 cn-llm-router skill 以启用翻译功能。"
            )
            result["used_fallback"] = True
            # 直接复制中文字幕作为输出
            dest_name = f"subtitle_zh_{target_lang}.{output_format}"
            dest_path = os.path.join(self.output_dir, dest_name)
            import shutil
            shutil.copy2(subtitles_path, dest_path)
            result["output_path"] = dest_path
            return result

        # 解析字幕
        segments = self._parse_subtitles(subtitles_path)
        if not segments:
            result["warnings"].append("字幕文件解析失败或为空")
            return result

        # ===== v4.7 术语前置替换：加载术语表 =====
        glossary = {}
        if self.glossary_enabled:
            glossary = self.glossary_engine.load(target_lang=target_lang)
            if not glossary and self.glossary:
                glossary = dict(self.glossary)  # 兼容旧版扁平术语表

        # ===== v4.7 术语保护：先对全部原文做占位符隔离 =====
        original_texts = [seg["text"] for seg in segments]
        if glossary:
            protected_texts, ph_map = self.glossary_engine.protect(original_texts, glossary)
            logger.info(f"术语前置替换: 保护 {len(ph_map)} 个术语占位符")
        else:
            protected_texts, ph_map = list(original_texts), {}

        # 批量翻译（翻译带占位符的文本，术语不会被机翻改写）
        translated_segments = []
        translated_texts_all = [""] * len(segments)
        for i in range(0, len(segments), self.batch_size):
            batch = segments[i:i + self.batch_size]
            batch_texts = protected_texts[i:i + self.batch_size]

            # 构建翻译 prompt（术语表约束占位符保持原样）
            prompt = self._build_translation_prompt(batch_texts, target_lang)

            # 调用 router 翻译
            translation_result = self._call_router(router_cmd, prompt)

            if translation_result and "content" in translation_result:
                translated_texts = self._parse_translation_result(
                    translation_result["content"], len(batch_texts)
                )
                for j, seg in enumerate(batch):
                    if j < len(translated_texts):
                        translated_texts_all[i + j] = translated_texts[j]
                        result["translated_count"] += 1
                    else:
                        result["skipped_count"] += 1
                translated_segments.extend(batch)
            else:
                # 翻译失败，保留原文
                for j, seg in enumerate(batch):
                    translated_texts_all[i + j] = seg["text"]
                translated_segments.extend(batch)
                result["skipped_count"] += len(batch)
                result["warnings"].append(f"批次 {i // self.batch_size + 1} 翻译失败，保留原文")

        # ===== v4.7 术语后置校对：还原占位符 + 命中率统计 + 待确认清单 =====
        if ph_map:
            restored_texts, unresolved = self.glossary_engine.restore(translated_texts_all, ph_map)
            for idx, text in enumerate(restored_texts):
                if idx < len(translated_segments):
                    translated_segments[idx]["text"] = text
            report = self.glossary_engine.proofread(
                original_texts, restored_texts, glossary, target_lang
            )
            result["glossary_report"] = report
            result["pending_list_path"] = report.get("pending_list_path")
            if unresolved:
                result["warnings"].append(
                    f"{len(unresolved)} 个术语占位符翻译后被破坏，已列入待确认清单"
                )
        else:
            # 无术语表时也产出空报告，口径统一（死规则：报告单源化）
            result["glossary_report"] = {
                "target_lang": target_lang, "glossary_size": 0, "total_terms": 0,
                "hit_terms": 0, "hit_rate": 1.0, "hits": [], "pending": [],
                "pending_list_path": None,
            }

        # 输出翻译后的字幕
        output_name = f"subtitle_{target_lang}.{output_format}"
        output_path = os.path.join(self.output_dir, output_name)

        if output_format == "srt":
            self._write_srt(translated_segments, output_path)
        elif output_format == "vtt":
            self._write_vtt(translated_segments, output_path)
        elif output_format == "ass":
            self._write_ass(translated_segments, output_path)
        else:
            self._write_srt(translated_segments, output_path)

        result["output_path"] = output_path
        logger.info(
            f"字幕翻译完成: {output_path}, "
            f"翻译 {result['translated_count']} 条, 跳过 {result['skipped_count']} 条"
        )
        return result

    def _find_router(self) -> Optional[List[str]]:
        """查找 cn-llm-router 的 router.py 路径"""
        # 1. 使用配置的路径
        if self.router_path and os.path.exists(self.router_path):
            return ["python", self.router_path]

        # 2. 搜索常见位置
        search_paths = [
            "D:/skill/cn-llm-router/scripts/router.py",
            "D:/skill/cn-llm-router/scripts/router.py",
            os.path.expanduser("~/.workbuddy/skills/cn-llm-router/scripts/router.py"),
        ]

        for path in search_paths:
            if os.path.exists(path):
                return ["python", path]

        # 3. 尝试从 PATH 查找
        try:
            result = subprocess.run(
                ["where", "router.py"],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0 and result.stdout.strip():
                return ["python", result.stdout.strip().split("\n")[0]]
        except Exception:
            pass

        return None

    def _load_glossary(self) -> Dict[str, str]:
        """加载术语表"""
        glossary = dict(DEFAULT_GLOSSARY)

        if self.glossary_path and os.path.exists(self.glossary_path):
            try:
                with open(self.glossary_path, "r", encoding="utf-8") as f:
                    custom = json.load(f)
                    glossary.update(custom)
            except Exception as e:
                logger.warning(f"加载术语表失败: {e}")

        return glossary

    def _build_translation_prompt(
        self, texts: List[str], target_lang: str
    ) -> str:
        """构建翻译 prompt"""
        lang_name = SUPPORTED_LANGUAGES[target_lang]["name"]

        # 术语表约束
        glossary_constraint = ""
        if self.glossary:
            glossary_lines = [f'  "{k}": "{v}"' for k, v in list(self.glossary.items())[:20]]
            glossary_constraint = (
                f"\n术语表约束（必须严格遵循）:\n"
                + ",\n".join(glossary_lines)
            )

        # 待翻译文本
        text_list = "\n".join(f"{i+1}. {t}" for i, t in enumerate(texts))

        prompt = f"""请将以下中文短视频字幕翻译为{lang_name}。要求：
1. 保持口语化风格，符合短视频语境
2. 每条翻译独立一行，格式为 "序号. 翻译内容"
3. 保留原始序号
4. 文本中形如 GL0 的标记是受保护术语占位符，必须原样保留在译文中，不得翻译、改写或删除{glossary_constraint}

待翻译文本：
{text_list}"""

        return prompt

    def _call_router(self, router_cmd: List[str], prompt: str) -> Optional[Dict]:
        """调用 cn-llm-router 进行翻译"""
        try:
            cmd = router_cmd + [
                "chat",
                "--prompt", prompt,
                "--task", "translate",
                "--json",
                "--timeout", str(self.timeout),
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout + 30,
            )

            if result.returncode == 0 and result.stdout.strip():
                return json.loads(result.stdout.strip())
            else:
                logger.warning(f"router 调用失败: {result.stderr[:200]}")
                return None

        except subprocess.TimeoutExpired:
            logger.warning("router 调用超时")
            return None
        except json.JSONDecodeError:
            logger.warning("router 返回 JSON 解析失败")
            return None
        except Exception as e:
            logger.warning(f"router 调用异常: {e}")
            return None

    def _parse_translation_result(
        self, content: str, expected_count: int
    ) -> List[str]:
        """解析翻译结果"""
        results = []

        # 尝试按 "序号. 内容" 格式解析
        lines = content.strip().split("\n")
        for line in lines:
            line = line.strip()
            match = re.match(r"^\d+\.\s*(.+)$", line)
            if match:
                results.append(match.group(1).strip())

        # 如果解析数量不足，尝试按行分割
        if len(results) < expected_count:
            results = [
                line.strip() for line in lines
                if line.strip() and not line.strip().startswith(("术语", "待翻译", "要求"))
            ]

        return results[:expected_count]

    def _parse_subtitles(self, subtitles_path: str) -> List[Dict]:
        """解析 SRT/ASS 字幕文件"""
        ext = subtitles_path.rsplit(".", 1)[-1].lower()

        if ext == "srt":
            return self._parse_srt(subtitles_path)
        elif ext == "ass":
            return self._parse_ass(subtitles_path)
        else:
            # 尝试 SRT
            return self._parse_srt(subtitles_path)

    def _parse_srt(self, path: str) -> List[Dict]:
        """解析 SRT 格式"""
        segments = []
        try:
            with open(path, "r", encoding="utf-8-sig") as f:
                content = f.read()

            # 按空行分割字幕块
            blocks = re.split(r"\n\s*\n", content.strip())

            for block in blocks:
                lines = block.strip().split("\n")
                if len(lines) < 2:
                    continue

                # 时间码行
                time_line = None
                time_idx = -1
                for i, line in enumerate(lines):
                    if "-->" in line:
                        time_line = line
                        time_idx = i
                        break

                if not time_line:
                    continue

                # 解析时间
                time_match = re.match(
                    r"(\d{2}:\d{2}:\d{2}[,\.]\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}[,\.]\d{3})",
                    time_line,
                )
                if not time_match:
                    continue

                start = self._time_to_seconds(time_match.group(1))
                end = self._time_to_seconds(time_match.group(2))

                # 字幕文本
                text_lines = lines[time_idx + 1:]
                text = " ".join(t.strip() for t in text_lines if t.strip())

                if text:
                    segments.append({
                        "start": start,
                        "end": end,
                        "text": text,
                    })

        except Exception as e:
            logger.error(f"解析 SRT 失败: {e}")

        return segments

    def _parse_ass(self, path: str) -> List[Dict]:
        """解析 ASS 格式"""
        segments = []
        try:
            with open(path, "r", encoding="utf-8-sig") as f:
                content = f.read()

            # 查找 [Events] 部分
            events_match = re.search(r"\[Events\](.*?)(?=\[|\Z)", content, re.DOTALL)
            if not events_match:
                return segments

            events_section = events_match.group(1).strip()

            # 解析 Dialogue 行
            for line in events_section.split("\n"):
                if line.startswith("Dialogue:"):
                    parts = line.split(",", 9)
                    if len(parts) >= 10:
                        start = self._ass_time_to_seconds(parts[1])
                        end = self._ass_time_to_seconds(parts[2])
                        text = parts[9].strip()
                        # 去除 ASS 标签
                        text = re.sub(r"\{[^}]*\}", "", text)
                        text = text.replace("\\N", " ").replace("\\n", " ")

                        if text:
                            segments.append({
                                "start": start,
                                "end": end,
                                "text": text,
                            })

        except Exception as e:
            logger.error(f"解析 ASS 失败: {e}")

        return segments

    def _time_to_seconds(self, time_str: str) -> float:
        """SRT 时间码转秒"""
        time_str = time_str.replace(",", ".")
        parts = time_str.split(":")
        if len(parts) == 3:
            return (
                int(parts[0]) * 3600
                + int(parts[1]) * 60
                + float(parts[2])
            )
        return 0.0

    def _ass_time_to_seconds(self, time_str: str) -> float:
        """ASS 时间码转秒 (H:MM:SS.cc)"""
        parts = time_str.split(":")
        if len(parts) == 3:
            return (
                int(parts[0]) * 3600
                + int(parts[1]) * 60
                + float(parts[2])
            )
        return 0.0

    def _write_srt(self, segments: List[Dict], output_path: str):
        """写入 SRT 格式"""
        with open(output_path, "w", encoding="utf-8") as f:
            for i, seg in enumerate(segments, 1):
                start = self._seconds_to_srt_time(seg["start"])
                end = self._seconds_to_srt_time(seg["end"])
                f.write(f"{i}\n")
                f.write(f"{start} --> {end}\n")
                f.write(f"{seg['text']}\n\n")

    def _write_vtt(self, segments: List[Dict], output_path: str):
        """写入 VTT 格式"""
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("WEBVTT\n\n")
            for i, seg in enumerate(segments, 1):
                start = self._seconds_to_vtt_time(seg["start"])
                end = self._seconds_to_vtt_time(seg["end"])
                f.write(f"{i}\n")
                f.write(f"{start} --> {end}\n")
                f.write(f"{seg['text']}\n\n")

    def _write_ass(self, segments: List[Dict], output_path: str):
        """写入 ASS 格式"""
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("[Script Info]\n")
            f.write("Title: Translated Subtitles\n")
            f.write("ScriptType: v4.00+\n")
            f.write("Collisions: Normal\n")
            f.write("PlayResX: 1920\n")
            f.write("PlayResY: 1080\n\n")
            f.write("[V4+ Styles]\n")
            f.write(
                "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, "
                "OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, "
                "ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, "
                "Alignment, MarginL, MarginR, MarginV, Encoding\n"
            )
            f.write(
                "Style: Default,Microsoft YaHei,48,&H00FFFFFF,&H000000FF,&H00000000,"
                "&H80000000,0,0,0,0,100,100,0,0,1,2,0,2,10,10,40,1\n\n"
            )
            f.write("[Events]\n")
            f.write(
                "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, "
                "Effect, Text\n"
            )
            for seg in segments:
                start = self._seconds_to_ass_time(seg["start"])
                end = self._seconds_to_ass_time(seg["end"])
                text = seg["text"].replace("\n", "\\N")
                f.write(f"Dialogue: 0,{start},{end},Default,,0,0,0,,{text}\n")

    def _seconds_to_srt_time(self, seconds: float) -> str:
        """秒转 SRT 时间码"""
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        ms = int((seconds % 1) * 1000)
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

    def _seconds_to_vtt_time(self, seconds: float) -> str:
        """秒转 VTT 时间码"""
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        ms = int((seconds % 1) * 1000)
        return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"

    def _seconds_to_ass_time(self, seconds: float) -> str:
        """秒转 ASS 时间码"""
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        cs = int((seconds % 1) * 100)
        return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

    @staticmethod
    def get_supported_languages() -> Dict[str, str]:
        """获取支持的目标语言"""
        return {k: v["name"] for k, v in SUPPORTED_LANGUAGES.items()}

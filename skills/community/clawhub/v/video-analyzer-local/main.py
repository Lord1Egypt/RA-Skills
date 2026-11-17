#!/usr/bin/env python3
"""
video-analyzer 主入口
视频分析处理 Skill — 将视频反编译为结构化分析报告

用法:
    python main.py -i <视频路径或URL> [-o 输出目录] [--model 模型名] [--lang 语言]
"""

import argparse
import os
import sys
import time
from pathlib import Path

# 确保 core 模块可被导入
sys.path.insert(0, str(Path(__file__).parent))

from core.input_handler import InputHandler
from core.media_processor import MediaProcessor
from core.asr import ASRRouter
from core.ocr import PaddleOCREngine
from core.nlp import ChineseNLPEnhancement
from core.scene_detector import SceneDetector
from core.visual_analyzer import VisualAnalyzer
from core.alignment_engine import AlignmentEngine
from core.semantic_fusion import SemanticFusion
from core.highlight_extractor import HighlightExtractor
from core.report_generator import ReportGenerator
from core.config import load_config
from core.logger import get_logger
from core.hardware_probe import HardwareProbe, ResourceMonitor
from core.chapter_slicer import ChapterSlicer
from core.speaker_diarization import SpeakerDiarization
from core.timestamped_summary import TimestampedSummary
from core.update_notifier import UpdateNotifier
from core.platform_adapters import PlatformRouter
from core.editing import HighlightDetector, RedundancyDetector, TimelineGenerator, EDLExporter, SubtitleStylist, JianyingExporter
from core.editing.auto_editor import AutoEditor
from core.editing.cover_selector import CoverSelector
from core.editing.subtitle_translator import SubtitleTranslator
from core.editing.subtitle_burner import SubtitleBurner
from core.editing.glossary_engine import GlossaryEngine
from core.editing.bgm_recognizer import BGMRecognizer
from core.speaker_diarization.quality_scorer import QualityScorer
from core.scene_manager import SceneManager
from core.viral_predictor import ViralPredictor
from core.live_analyzer import LiveAnalyzer
from core.media_probe import MediaProbe
from core.queue_manager import QueueManager
from core.gpu_accelerator import GPUAccelerator
from core.doctor import Doctor
from core.model_downloader import ModelDownloader
from core.podcast.podcast_pipeline import PodcastPipeline
from core.podcast.weekly_briefing import WeeklyBriefing

logger = get_logger(__name__)


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="video-analyzer: 视频分析处理工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python main.py -i video.mp4
  python main.py -i video.mp4 -o ./report --model medium --lang zh
  python main.py -i "https://example.com/video.mp4" --no-visual
        """
    )
    
    parser.add_argument("-i", "--input", required=True,
                        help="视频文件路径或 HTTP URL")
    parser.add_argument("-o", "--output", default="./output",
                        help="输出目录 (默认: ./output)")
    parser.add_argument("--format", default="html,json,md",
                        help="报告格式，逗号分隔 (默认: html,json,md)")
    parser.add_argument("-m", "--model", default=None,
                        choices=["tiny", "base", "small", "medium", "large-v3"],
                        help="Whisper 模型大小 (默认: 自动根据硬件选择)")
    parser.add_argument("-l", "--lang", default=None,
                        help="语言代码: auto/zh/en/ja 等 (默认: 自动检测)")
    parser.add_argument("--asr-engine", default=None,
                        choices=["whisper", "paraformer", "sensevoice", "auto"],
                        help="ASR 语音识别引擎 (默认: 从配置读取)")
    parser.add_argument("--ocr-engine", default=None,
                        choices=["paddleocr", "auto"],
                        help="OCR 文字识别引擎 (默认: 从配置读取)")
    parser.add_argument("--no-nlp-enhance", action="store_true",
                        help="跳过中文 NLP 增强（NER + 标签中文化）")
    parser.add_argument("--no-visual", action="store_true",
                        help="跳过视觉分析（场景分类/物体检测）")
    parser.add_argument("--no-ocr", action="store_true",
                        help="跳过画面文字识别")
    parser.add_argument("--no-highlight", action="store_true",
                        help="跳过精华提取")
    parser.add_argument("--scenes-only", action="store_true",
                        help="仅输出场景切割 JSON")
    parser.add_argument("-f", "--force", action="store_true",
                        help="忽略缓存，强制重新分析")
    parser.add_argument("--temp-dir", default=None,
                        help="临时文件目录 (默认: ./.cache)")
    parser.add_argument("--config", default="config.yaml",
                        help="配置文件路径 (默认: config.yaml)")
    parser.add_argument("--verbose", action="store_true",
                        help="显示详细日志")
    parser.add_argument("--no-adaptive", action="store_true",
                        help="禁用硬件自适应 (默认启用)")
    parser.add_argument("--max-memory", type=float, default=None,
                        help="最大内存使用 (GB)")
    parser.add_argument("--nice", type=int, default=None,
                        help="进程优先级 (0-19, 越大优先级越低)")
    parser.add_argument("--no-update-check", action="store_true",
                        help="跳过启动时的版本更新检查")
    parser.add_argument("--diarize", action="store_true",
                        help="启用说话人分离（多人对话场景）")
    parser.add_argument("--slice-chapters", action="store_true",
                        help="按章节切片视频片段 + 生成SRT字幕")
    parser.add_argument("--platform", action="store_true",
                        help="启用短视频平台适配（自动识别抖音/快手/B站/视频号链接）")
    parser.add_argument("--editing-suggest", action="store_true",
                        help="启用自动剪辑建议（高光检测/冗余标记/时间线生成/EDL导出）")
    parser.add_argument("--edl-format", default="cmx3600",
                        choices=["cmx3600", "csv", "json"],
                        help="EDL 导出格式 (默认: cmx3600)")
    parser.add_argument("--subtitle-style", default=None,
                        choices=["douyin", "bilibili", "movie", "minimal"],
                        help="字幕样式模板")
    parser.add_argument("--subtitle-format", default="ass",
                        choices=["srt", "ass", "vtt"],
                        help="字幕输出格式 (默认: ass)")
    parser.add_argument("--export-edl", action="store_true",
                        help="导出 EDL 剪辑时间线文件")
    parser.add_argument("--jianying", action="store_true",
                        help="导出剪映 draft.json 格式（可直接导入剪映专业版）")
    parser.add_argument("--quality-score", action="store_true",
                        help="启用说话人分离质量评分")
    parser.add_argument("--scene-management", action="store_true",
                        help="启用场景管理（detect→slice 一条链）")
    parser.add_argument("--viral-predict", action="store_true",
                        help="启用短视频爆款预测")
    parser.add_argument("--live-analyze", action="store_true",
                        help="启用实时直播分析（流式ASR+敏感词检测）")
    parser.add_argument("--dir", default=None,
                        help="批量处理目录（扫描视频文件逐个入队）")
    parser.add_argument("--hardware-tier", default=None,
                        choices=["low", "mid", "high"],
                        help="硬件档位（决定批量并发数）")
    parser.add_argument("--download-ct2-model", default=None,
                        choices=["tiny", "small", "medium"],
                        help="下载 Whisper CT2 量化模型")
    parser.add_argument("--auto-edit", action="store_true",
                        help="启用一键成片（ffmpeg filter_complex 自动剪辑）")
    parser.add_argument("--edit-style", default="口播精简",
                        choices=["口播精简", "高光集锦", "预告片"],
                        help="一键成片风格 (默认: 口播精简)")
    parser.add_argument("--edit-platform", default="douyin",
                        choices=["douyin", "bilibili", "kuaishou", "wechat_video"],
                        help="一键成片目标平台 (默认: douyin)")
    parser.add_argument("--bgm-path", default=None,
                        help="BGM 音频文件路径（用于一键成片）")
    parser.add_argument("--cover-select", action="store_true",
                        help="启用封面帧智能选取")
    parser.add_argument("--translate-subs", default=None,
                        help="翻译字幕到指定语言 (en/ja/ko/fr/de/es/ru)")
    parser.add_argument("--translate-format", default="srt",
                        choices=["srt", "ass", "vtt"],
                        help="翻译字幕输出格式 (默认: srt)")
    parser.add_argument("--bgm-detect", action="store_true",
                        help="启用 BGM 识别（需 chromaprint/fpcalc）")
    parser.add_argument("--jianying-v6", action="store_true",
                        help="导出剪映 6.0 draft.json + EDL 导入指南")
    parser.add_argument("--doctor", action="store_true",
                        help="首跑自检：探测 ffmpeg/模型/磁盘/内存/GPU，输出修复命令清单")
    parser.add_argument("--quick", action="store_true",
                        help="快速模式：仅转写+时间戳摘要，跳过视觉/场景/剪辑链")
    parser.add_argument("--download-model", default=None,
                        choices=["tiny", "base", "small", "medium"],
                        help="下载 Whisper 模型（带进度可视化+断点续传+3次重试）")
    parser.add_argument("--podcast", action="store_true",
                        help="播客模式：说话人时间线+Podcasting 2.0 章节标记+金句提取（v4.6 新增）")
    parser.add_argument("--diarize-profile", default=None,
                        choices=["interview", "meeting", "phone"],
                        help="说话人分离预设：访谈/会议/电话（v4.6 新增）")
    parser.add_argument("--weekly-briefing", action="store_true",
                        help="听后简报：生成周聚合 HTML 简报（v4.6 新增）")
    parser.add_argument("--subtitle-preset", default=None,
                        choices=["variety", "interview", "course", "minimal", "vertical"],
                        help="字幕样式包：综艺/访谈/课程/极简/竖屏（v4.7 新增）")
    parser.add_argument("--bilingual", action="store_true",
                        help="双语同轴字幕：原文轨+译文轨（配合 --translate-subs，v4.7 新增）")
    parser.add_argument("--original-track", action="store_true", default=True,
                        help="双语时显示原文轨（默认开启，v4.7 新增）")
    parser.add_argument("--no-original-track", dest="original_track", action="store_false",
                        help="双语时隐藏原文轨（v4.7 新增）")
    parser.add_argument("--no-translation-track", dest="translation_track", action="store_false",
                        help="双语时隐藏译文轨（v4.7 新增）")
    parser.add_argument("--glossary", default=None,
                        help="术语表 JSON 路径（人名/产品名/专业词强制校正，v4.7 新增）")
    parser.add_argument("--burn-subtitle", action="store_true",
                        help="烧录硬字幕到视频（ffmpeg 一条命令，样式包直连，v4.7 新增）")
    
    return parser.parse_args()


def print_banner():
    """打印启动横幅"""
    banner = """
╔══════════════════════════════════════════════════╗
║          🎬 video-analyzer v4.7.0               ║
║        视频分析处理 — 本地视频反编译工具         ║
╚══════════════════════════════════════════════════╝
    """
    print(banner)


def apply_process_priority(nice_level: int):
    """设置进程优先级，避免拖垮用户电脑"""
    try:
        if sys.platform == "win32":
            # Windows: 使用 BELOW_NORMAL_PRIORITY_CLASS
            import ctypes
            handle = ctypes.windll.kernel32.GetCurrentProcess()
            # BELOW_NORMAL_PRIORITY_CLASS = 0x00004000
            ctypes.windll.kernel32.SetPriorityClass(handle, 0x00004000)
            logger.debug("Windows 进程优先级已设置为 BELOW_NORMAL")
        else:
            # Linux/macOS: 使用 nice
            os.nice(nice_level)
            logger.debug(f"Process nice level set to {nice_level}")
    except Exception as e:
        logger.debug(f"无法设置进程优先级: {e}")


def limit_cache_size(cache_dir: str, max_size_gb: float):
    """限制缓存目录大小，自动清理旧文件"""
    try:
        if not os.path.exists(cache_dir):
            return
        
        # 计算目录大小
        total_size = 0
        file_list = []
        for root, dirs, files in os.walk(cache_dir):
            for f in files:
                fp = os.path.join(root, f)
                size = os.path.getsize(fp)
                total_size += size
                file_list.append((fp, size, os.path.getmtime(fp)))
        
        max_size = max_size_gb * 1024 * 1024 * 1024
        
        if total_size > max_size:
            # 按修改时间排序，删除最旧的文件
            file_list.sort(key=lambda x: x[2])
            
            freed = 0
            for fp, size, _ in file_list:
                if total_size - freed <= max_size * 0.8:  # 清理到 80%
                    break
                os.remove(fp)
                freed += size
            
            logger.info(f"缓存清理完成，释放 {freed / (1024**2):.1f}MB")
    
    except Exception as e:
        logger.debug(f"缓存清理失败: {e}")


def main():
    """主流程"""
    print_banner()
    args = parse_args()
    
    # 加载配置
    config = load_config(args.config if os.path.exists(args.config) else None)

    # ===== v4.7 字幕工作流：CLI 参数注入配置（单源化，供各模块统一读取） =====
    if args.glossary:
        config.setdefault("glossary", {})["glossary_path"] = args.glossary
    if args.subtitle_preset:
        config.setdefault("subtitle_presets", {})["default"] = args.subtitle_preset
    config.setdefault("subtitle_workflow", {})
    config["subtitle_workflow"]["bilingual"] = args.bilingual
    config["subtitle_workflow"]["original_track"] = args.original_track
    config["subtitle_workflow"]["translation_track"] = args.translation_track
    config["subtitle_workflow"]["burn"] = args.burn_subtitle
    
    # ========== 硬件自适应配置 ==========
    if not args.no_adaptive:
        logger.info("🔍 检测硬件配置...")
        probe = HardwareProbe(config)
        config = probe.apply_to_config(config)
        
        # 应用硬件推荐的进程优先级
        nice_level = config.get("processing", {}).get("nice_level", 5)
        apply_process_priority(nice_level)
        
        # 启动实时资源监控
        resource_monitor = ResourceMonitor(
            max_memory_gb=config.get("processing", {}).get("max_memory_gb", 4),
            check_interval=5,
        )
        resource_monitor.start()
        logger.info("🖥️  实时资源监控已启动")
    else:
        resource_monitor = None
    
    # ========== GPU 自动加速探测（v4.3 新增） ==========
    gpu_accelerator = GPUAccelerator(config)
    gpu_probe_result = gpu_accelerator.probe_cuda()
    if gpu_probe_result["device"] == "cuda":
        logger.info(f"🚀 GPU 加速已启用: {gpu_probe_result.get('gpu_name', 'unknown')}")
    else:
        logger.info("💻 GPU 不可用，使用 CPU 模式")
        logger.info(gpu_accelerator.get_fallback_message())
    
    # 命令行参数覆盖配置 (优先级最高)
    if args.model:
        config["whisper"]["model_name"] = args.model
    if args.lang:
        config["whisper"]["language"] = args.lang
    config["visual_analysis"]["enable_scene_classification"] = not args.no_visual
    config["visual_analysis"]["enable_object_detection"] = not args.no_visual
    config["visual_analysis"]["enable_ocr"] = not args.no_ocr
    if args.temp_dir:
        config["processing"]["cache_dir"] = args.temp_dir
    if args.max_memory:
        config["processing"]["max_memory_gb"] = args.max_memory
    if args.nice is not None:
        config["processing"]["nice_level"] = args.nice
        apply_process_priority(args.nice)
    
    config["report"]["formats"] = args.format.split(",")
    
    if args.verbose:
        import logging
        get_logger().setLevel(logging.DEBUG)
    
    start_time = time.time()
    media = None
    
    try:
        # ========== 版本更新检查（非阻塞） ==========
        if not args.no_update_check:
            try:
                notifier = UpdateNotifier(config, current_version="4.7.0")
                update_result = notifier.check_for_updates()
                update_msg = notifier.format_update_message(update_result)
                if update_msg:
                    print(update_msg)
            except Exception:
                pass  # 更新检查失败不影响主流程
        
        # ========== 阶段 1: 输入处理 ==========
        logger.info("📥 [1/7] 处理输入...")
        input_handler = InputHandler(config)
        video_path = input_handler.process(args.input)
        logger.info(f"   视频路径: {video_path}")
        
        # ========== 媒体探测（v4.3 新增：纯音频支持） ==========
        media_probe = MediaProbe(config)
        is_pure_audio = media_probe.is_pure_audio(video_path)
        
        # 初始化可选结果变量
        podcast_result = None
        weekly_briefing = None
        
        if is_pure_audio:
            logger.info("🎵 检测到纯音频输入，启用音频模式...")
            media_info = media_probe.get_media_info_for_video(video_path)
            audio_path = media_info["audio_path"]
            frames_dir = None
            logger.info(f"   时长: {media_info['duration']:.1f}s")
            logger.info(f"   音频已转换: {audio_path}")
        else:
            # ========== 阶段 2: 媒体处理 ==========
            logger.info("🔧 [2/7] 媒体处理...")
            media = MediaProcessor(config)
            media_info = media.get_media_info(video_path)
            logger.info(f"   分辨率: {media_info['width']}x{media_info['height']}")
            logger.info(f"   时长: {media_info['duration']:.1f}s")
            logger.info(f"   帧率: {media_info['fps']:.1f}")
            
            # 预估处理时间
            if not args.no_adaptive:
                probe = HardwareProbe(config)
                time_est = probe.estimate_processing_time(media_info['duration'], media_info)
                logger.info(f"   ⏱️  预估处理时间: {time_est['estimated_formatted']}")
            
            # 提取音频
            audio_path = media.extract_audio(video_path)
            logger.info(f"   音频已提取: {audio_path}")
            
            # 提取帧序列 (根据硬件能力自动选择采样率)
            frames_dir = media.extract_frames(video_path)
            logger.info(f"   帧序列已提取到: {frames_dir}")
        
        # ========== 阶段 3: 语音识别 ==========
        logger.info("🎙️  [3/7] 语音转文字...")
        
        # 根据配置/参数选择引擎
        asr_engine = args.asr_engine if args.asr_engine else config.get("asr", {}).get("engine", "auto")
        asr_router = ASRRouter(config)
        asr_result = asr_router.transcribe(
            audio_path,
            preferred_engine=asr_engine,
            language=args.lang if args.lang else config.get("asr", {}).get("language", "auto"),
        )
        
        # 将 ASRResult 转换为原 transcript 格式（兼容下游模块）
        transcript = {
            "text": asr_result.text,
            "language": asr_result.language,
            "duration": asr_result.duration,
            "segments": [
                {
                    "id": seg.id,
                    "start": seg.start,
                    "end": seg.end,
                    "text": seg.text,
                    "confidence": seg.confidence,
                    "words": seg.words,
                    "speaker": seg.speaker,
                    "emotion": seg.emotion,
                }
                for seg in asr_result.segments
            ],
        }
        
        asr_active = asr_router.active_engine
        if asr_active and asr_active.name != "whisper":
            logger.info(f"   使用引擎: {asr_active.name}")
        logger.info(f"   识别完成: {len(transcript['segments'])} 个语音段")
        logger.info(f"   语言: {transcript.get('language', 'unknown')}")
        
        # ========== 中文 NLP 增强（可选） ==========
        nlp_enhancer = None
        if not args.no_nlp_enhance:
            nlp_enhancer = ChineseNLPEnhancement(config)
            if nlp_enhancer.use_jieba:
                logger.info("🔤 中文 NLP 增强已启用（NER + 标签中文化）")
        
        # ========== 说话人分离（可选） ==========
        diarize_result = None
        quality_score = None
        if args.diarize or args.podcast:
            logger.info("🗣️  说话人分离...")
            diarizer = SpeakerDiarization(config)
            diarize_result = diarizer.diarize(
                audio_path, transcript.get("segments", []),
                profile=args.diarize_profile if args.diarize_profile else None,
            )
            logger.info(f"   分离完成: {diarize_result['n_speakers']} 人")
            if diarize_result.get("quality_score"):
                qs = diarize_result["quality_score"]
                logger.info(f"   质量评分: {qs.get('overall_score')} 分 ({qs.get('level')}可信度)")
                logger.info(f"   建议: {qs.get('suggestion')}")
        
        # ========== 纯音频模式跳过场景检测和视觉分析 ==========
        scenes = None
        visual_data = None
        aligned_data = None
        fused_data = None
        highlights = None
        
        if is_pure_audio:
            logger.info("🎵 [音频模式] 跳过场景检测、视觉分析和 OCR")
            # 构建纯音频的 scenes（空）
            scenes = {"scenes": [], "total_scenes": 0}
            visual_data = {"scenes": []}
        else:
            # ========== 阶段 4: 场景检测 ==========
            logger.info("🎬 [4/7] 场景检测...")
            scene_detector = SceneDetector(config)
            scenes = scene_detector.detect_scenes(video_path, frames_dir)
            logger.info(f"   检测到 {len(scenes['scenes'])} 个场景")
            
            # 如果仅需要场景切割，到此为止
            if args.scenes_only:
                import json
                output_path = os.path.join(args.output, "scenes_only.json")
                os.makedirs(args.output, exist_ok=True)
                with open(output_path, "w", encoding="utf-8") as f:
                    json.dump(scenes, f, ensure_ascii=False, indent=2)
                logger.info(f"✅ 场景 JSON 已保存: {output_path}")
                return
            
            # ========== 阶段 5: 视觉分析 ==========
            logger.info("🔍 [5/7] 视觉分析...")
            visual_analyzer = VisualAnalyzer(config)
            visual_data = visual_analyzer.analyze(scenes, video_path)
            logger.info(f"   视觉分析完成")
            
            # ✨ 中文 NLP 增强：物体标签 + 场景标签中文化
            if nlp_enhancer:
                from core.nlp import get_chinese_label
                for scene_data in visual_data.get("scenes", []):
                    # 物体标签中文化
                    for obj in scene_data.get("objects", []):
                        name = obj.get("name", "")
                        obj["name_zh"] = get_chinese_label(name)
                    # 场景标签中文化
                    scene_types = scene_data.get("scene_types", [])
                    scene_data["scene_types_zh"] = nlp_enhancer.translate_scene_labels(scene_types)
            
            # ========== 阶段 6: 时空对齐与融合 ==========
            logger.info("🔗 [6/7] 时空对齐与语义融合...")
            
            workers = config.get("processing", {}).get("num_workers", 4)
            logger.info(f"   使用 {workers} 个子进程并行处理")
            
            alignment = AlignmentEngine(config)
            aligned_data = alignment.align(transcript, scenes, visual_data, media_info)
            
            fusion = SemanticFusion(config)
            fused_data = fusion.fuse(aligned_data)
            logger.info(f"   融合完成")
            
            # ✨ 中文 NLP 增强：融合数据中的人名/地名/术语识别
            if nlp_enhancer and nlp_enhancer.use_ner:
                for scene in fused_data.get("scenes", []):
                    dialog = scene.get("content", {}).get("dialog", "")
                    if dialog:
                        entities = nlp_enhancer.recognize_entities(dialog)
                        scene["entities"] = entities
                        terms = nlp_enhancer.detect_terminology(dialog)
                        scene["terminology"] = terms
            
            # ========== 阶段 7: 精华提取与报告 ==========
            logger.info("✨ [7/7] 精华提取与报告生成...")
            
            if not args.no_highlight:
                extractor = HighlightExtractor(config)
                highlights = extractor.extract(fused_data)
                logger.info(f"   提取 {highlights.get('total_highlights', 0)} 个精华片段")
        
        # 生成报告
        reporter = ReportGenerator(config)
        output_paths = reporter.generate(
            transcript=transcript,
            scenes=scenes,
            visual_data=visual_data,
            aligned_data=aligned_data,
            fused_data=fused_data,
            highlights=highlights,
            media_info=media_info,
            output_dir=args.output,
            platform_analysis=platform_analysis,
            platform_meta=platform_meta,
            editing_result=editing_result,
            viral_result=viral_result,
            live_stats=live_stats,
            auto_edit_result=auto_edit_result,
            cover_result=cover_result,
            translate_result=translate_result,
            bgm_result=bgm_result,
            podcast_result=podcast_result,
            weekly_briefing=weekly_briefing,
        )
        
        # ========== 章节切片（可选） ==========
        if args.slice_chapters:
            logger.info("✂️  章节切片...")
            chapters_dir = os.path.join(args.output, "chapters")
            slicer = ChapterSlicer(config)
            chapters_result = slicer.slice_chapters(video_path, scenes, transcript, chapters_dir)
            logger.info(f"   切片完成: {chapters_result['total_chapters']} 个章节")
            output_paths["chapters"] = chapters_dir
        
        # ========== 短视频平台适配（可选） ==========
        platform_analysis = None
        platform_meta = None
        if args.platform:
            logger.info("📱 短视频平台适配...")
            platform_router = PlatformRouter(config)
            
            # 尝试从输入识别平台
            parse_result = platform_router.parse_link(args.input)
            if parse_result:
                platform_name, video_id = parse_result
                logger.info(f"   识别平台: {platform_name}, 视频ID: {video_id}")
                
                # 提取平台元数据
                platform_meta = platform_router.extract_metadata(platform_name, video_id)
                if platform_meta:
                    logger.info(f"   标题: {platform_meta.title[:30]}...")
                    logger.info(f"   作者: {platform_meta.author}")
                    logger.info(f"   点赞: {platform_meta.like_count}, 评论: {platform_meta.comment_count}")
                
                # 执行短视频特有分析
                platform_analysis = platform_router.analyze_short_video(
                    platform_name, video_path, platform_meta, transcript, scenes
                )
                
                if platform_analysis:
                    logger.info(f"   黄金前3秒: {platform_analysis.opening_3s.get('hook_type', '未知')}")
                    logger.info(f"   带货分析: {'是' if platform_analysis.ecommerce_analysis.get('is_ecommerce') else '否'}")
            else:
                logger.info("   未识别到平台链接，跳过平台分析")
        
        # ========== 自动剪辑建议（可选） ==========
        editing_result = None
        if args.editing_suggest:
            logger.info("🎬 自动剪辑建议...")
            
            # 高光检测
            logger.info("   检测高光片段...")
            highlight_detector = HighlightDetector(config)
            highlights_list = highlight_detector.detect(video_path, transcript, scenes)
            logger.info(f"   发现 {len(highlights_list)} 个高光片段")
            
            # 冗余检测
            logger.info("   检测冗余片段...")
            redundancy_detector = RedundancyDetector(config)
            redundancies = redundancy_detector.detect(video_path, transcript, scenes)
            logger.info(f"   发现 {len(redundancies)} 个冗余片段")
            
            # 生成剪辑时间线
            logger.info("   生成剪辑时间线...")
            timeline_gen = TimelineGenerator(config)
            original_duration = media_info.get("duration", 0)
            timeline = timeline_gen.generate(highlights_list, redundancies, original_duration)
            logger.info(f"   时间线: {len(timeline.get('clips', []))} 个片段, "
                       f"压缩比 {timeline.get('compression_ratio', 0):.0%}")
            
            editing_result = {
                "highlights": highlights_list,
                "redundancies": redundancies,
                "timeline": timeline,
            }
            
            # 导出 EDL
            if args.export_edl:
                logger.info("   导出 EDL 文件...")
                edl_exporter = EDLExporter(config)
                edl_dir = os.path.join(args.output, "edl")
                os.makedirs(edl_dir, exist_ok=True)
                edl_path = os.path.join(edl_dir, f"timeline.{args.edl_format}")
                edl_exporter.export(timeline, edl_path, format=args.edl_format)
                output_paths["edl"] = edl_path
                logger.info(f"   EDL 已导出: {edl_path}")
            
            # 导出剪映 draft.json（v4.1 新增）
            if args.jianying:
                logger.info("   导出剪映 draft.json...")
                jianying_exporter = JianyingExporter(config)
                jy_dir = os.path.join(args.output, "jianying")
                os.makedirs(jy_dir, exist_ok=True)
                jy_path = os.path.join(jy_dir, "draft.json")
                jianying_exporter.export(
                    timeline=timeline,
                    transcript=transcript,
                    video_path=video_path,
                    output_path=jy_path
                )
                output_paths["jianying"] = jy_path
                logger.info(f"   剪映文件已导出: {jy_path}")
            
            # 生成字幕文件
            logger.info("   生成字幕文件...")
            subtitle_stylist = SubtitleStylist(config)
            subtitle_dir = os.path.join(args.output, "subtitles")
            os.makedirs(subtitle_dir, exist_ok=True)
            subtitle_path = os.path.join(subtitle_dir, f"subtitle.{args.subtitle_format}")
            # v4.7：样式包优先于旧样式名
            effective_style = args.subtitle_preset or args.subtitle_style
            subtitle_stylist.generate(
                transcript, subtitle_path,
                style=effective_style,
                format=args.subtitle_format
            )
            output_paths["subtitle"] = subtitle_path
            logger.info(f"   字幕已生成: {subtitle_path}")
        
        # ========== 一键成片（可选，v4.4 新增） ==========
        auto_edit_result = None
        if args.auto_edit:
            logger.info("🎬 [一键成片] 开始自动剪辑...")
            
            # 获取高光和场景数据
            if highlights_list is None:
                logger.info("   执行高光检测...")
                highlight_detector = HighlightDetector(config)
                highlights_list = highlight_detector.detect(video_path, transcript, scenes)
                logger.info(f"   发现 {len(highlights_list)} 个高光片段")
            
            if scenes is None:
                scenes = {"scenes": [], "total_scenes": 0}
            
            # 获取字幕路径
            subtitle_path = output_paths.get("subtitle")
            
            # 创建编辑器
            editor = AutoEditor(config)
            
            # 生成成片
            auto_edit_result = editor.edit(
                video_path=video_path,
                highlights=highlights_list,
                scenes=scenes.get("scenes", []),
                subtitles_path=subtitle_path,
                style=args.edit_style,
                platform=args.edit_platform,
                bgm_path=args.bgm_path,
                title=platform_meta.title if platform_meta else "",
            )
            
            if auto_edit_result.get("output_path"):
                logger.info(f"   ✅ 成片完成: {auto_edit_result['output_path']}")
                logger.info(f"   时长: {auto_edit_result['duration']:.1f}s")
                logger.info(f"   使用片段: {auto_edit_result['clips_used']}")
                output_paths["auto_edit"] = auto_edit_result["output_path"]
                output_paths["edl_map"] = auto_edit_result["edl_map"]
                output_paths["platform_package"] = auto_edit_result["platform_package"]
            
            if auto_edit_result.get("bgm_suggestion"):
                logger.info(f"   BGM 建议: {auto_edit_result['bgm_suggestion']['mood']}")
            
            if auto_edit_result.get("warnings"):
                for w in auto_edit_result["warnings"]:
                    logger.warning(f"   ⚠️  {w}")
        
        # ========== 封面帧智能选取（可选，v4.4 新增） ==========
        cover_result = None
        if args.cover_select:
            logger.info("🖼️  [封面帧选取] 开始评分...")
            
            selector = CoverSelector(config)
            cover_result = selector.select(
                video_path=video_path,
                scenes=scenes.get("scenes", []) if scenes else None,
                top_n=3,
            )
            
            if cover_result["candidates"]:
                logger.info(f"   从 {cover_result['total_candidates']} 个候选帧中选出 Top3:")
                for i, c in enumerate(cover_result["candidates"]):
                    logger.info(f"   Top{i+1}: {c['path']} (得分: {c['score']})")
                    logger.info(f"    理由: {', '.join(c['reasons'])}")
                
                output_paths["cover_frames"] = [c["path"] for c in cover_result["candidates"]]
        
        # ========== 字幕翻译（可选，v4.4 新增） ==========
        translate_result = None
        if args.translate_subs:
            logger.info(f"🌐 [字幕翻译] 翻译为 {args.translate_subs}...")
            
            subtitle_path = output_paths.get("subtitle")
            if not subtitle_path:
                # 先生成中文字幕
                subtitle_stylist = SubtitleStylist(config)
                subtitle_dir = os.path.join(args.output, "subtitles")
                os.makedirs(subtitle_dir, exist_ok=True)
                subtitle_path = os.path.join(subtitle_dir, "subtitle.ass")
                subtitle_stylist.generate(transcript, subtitle_path, format="ass")
                output_paths["subtitle"] = subtitle_path
            
            translator = SubtitleTranslator(config)
            translate_result = translator.translate_subtitles(
                subtitles_path=subtitle_path,
                target_lang=args.translate_subs,
                output_format=args.translate_format,
            )
            
            if translate_result.get("output_path"):
                logger.info(f"   ✅ 翻译完成: {translate_result['output_path']}")
                logger.info(f"   翻译 {translate_result['translated_count']} 条")
                output_paths[f"subtitle_{args.translate_subs}"] = translate_result["output_path"]
            
            if translate_result.get("warnings"):
                for w in translate_result["warnings"]:
                    logger.warning(f"   ⚠️  {w}")

        # ========== 术语校对报告（v4.7 新增） ==========
        if translate_result and translate_result.get("glossary_report"):
            gr = translate_result["glossary_report"]
            if gr.get("glossary_size", 0) > 0:
                logger.info(f"📖 [术语校对] 命中 {gr['hit_terms']}/{gr['total_terms']} "
                            f"({gr.get('hit_rate', 0):.0%})")
            if gr.get("pending_list_path"):
                logger.info(f"   待确认清单: {gr['pending_list_path']}")
                output_paths["glossary_pending"] = gr["pending_list_path"]

        # ========== 双语同轴字幕（v4.7 新增） ==========
        bilingual_path = None
        if args.bilingual:
            if translate_result and translate_result.get("output_path"):
                logger.info("🔤 [双语字幕] 生成原文轨+译文轨同轴字幕...")
                stylist = SubtitleStylist(config)
                sub_dir = os.path.join(args.output, "subtitles")
                os.makedirs(sub_dir, exist_ok=True)
                # 解析译文文件为 segments
                tmp_translator = SubtitleTranslator(config)
                translation_segments = tmp_translator._parse_subtitles(
                    translate_result["output_path"]
                )
                bilingual_path = os.path.join(sub_dir, "subtitle_bilingual.ass")
                stylist.generate(
                    transcript, bilingual_path,
                    style=args.subtitle_preset,
                    format="ass",
                    bilingual=True,
                    original_track=args.original_track,
                    translation_track=args.translation_track,
                    translation_segments=translation_segments,
                )
                output_paths["subtitle_bilingual"] = bilingual_path
                logger.info(f"   ✅ 双语字幕: {bilingual_path}")
            else:
                logger.warning("⚠️  --bilingual 需要配合 --translate-subs 使用，已跳过")
        
        # ========== 字幕烧录（v4.7 新增） ==========
        if args.burn_subtitle:
            logger.info("🔥 [字幕烧录] ffmpeg 硬字幕压制...")
            burner = SubtitleBurner(config)
            # 选择烧录用的字幕：双语优先，其次翻译字幕，其次原字幕
            burn_sub = bilingual_path
            if not burn_sub and translate_result and translate_result.get("output_path"):
                burn_sub = translate_result["output_path"]
            if not burn_sub:
                burn_sub = output_paths.get("subtitle")

            # 兜底：无任何字幕时用转写结果现生成一份
            if not burn_sub and transcript:
                stylist0 = SubtitleStylist(config)
                sub_dir = os.path.join(args.output, "subtitles")
                os.makedirs(sub_dir, exist_ok=True)
                burn_sub = os.path.join(sub_dir, "subtitle.ass")
                stylist0.generate(transcript, burn_sub, style=args.subtitle_preset, format="ass")
                output_paths["subtitle"] = burn_sub

            if burn_sub:
                # 加载样式包（ASS 双语内嵌样式，无需 force_style 覆盖）
                stylist = SubtitleStylist(config)
                pack = stylist.load_style_pack(args.subtitle_preset)
                burn_pack = None if burn_sub.endswith(".ass") and args.bilingual else pack
                burn_result = burner.burn(
                    video_path=video_path,
                    subtitle_path=burn_sub,
                    style_pack=burn_pack,
                    hardware_tier=args.hardware_tier,
                )
                if burn_result.get("success"):
                    output_paths["burned_video"] = burn_result["output_path"]
                    logger.info(f"   ✅ 烧录完成: {burn_result['output_path']}")
                else:
                    logger.warning(f"   ⚠️  烧录失败: {burn_result.get('error')}")
            else:
                logger.warning("⚠️  无可烧录的字幕，请先启用字幕生成或翻译")

        # ========== 播客模式（可选，v4.6 新增） ==========
        podcast_result = None
        if args.podcast:
            logger.info("🎙️  [播客模式] 开始流水线...")
            pipeline = PodcastPipeline(config)
            podcast_result = pipeline.run(
                audio_path=audio_path,
                transcript=transcript,
                output_dir=args.output,
                n_speakers=None,
                diarize_profile=args.diarize_profile,
            )
            if podcast_result.get("output_files"):
                for fmt, path in podcast_result["output_files"].items():
                    logger.info(f"   [{fmt}] {path}")
            if podcast_result.get("highlights"):
                logger.info(f"   金句: {len(podcast_result['highlights'])} 条")
        
        # ========== BGM 识别（可选，v4.4 新增） ==========
        bgm_result = None
        if args.bgm_detect:
            logger.info("🎵 [BGM 识别] 识别背景音乐...")
            
            recognizer = BGMRecognizer(config)
            bgm_result = recognizer.recognize(video_path)
            
            if bgm_result.get("identified"):
                logger.info(f"   ✅ 识别到 BGM: {bgm_result['bgm_name']}")
                logger.info(f"   置信度: {bgm_result['confidence']}")
                logger.info(f"   版权风险: {bgm_result['copyright_risk']}")
                output_paths["bgm_result"] = bgm_result
            else:
                logger.info("   ❌ 未识别到已知 BGM")
                if bgm_result.get("copyright_risk") == "high":
                    logger.warning("   ⚠️  未知 BGM，商业使用存在版权风险")
            
            if bgm_result.get("warnings"):
                for w in bgm_result["warnings"]:
                    logger.warning(f"   ⚠️  {w}")
        
        # ========== 剪映 6.0 + EDL 指南（可选，v4.4 新增） ==========
        if args.jianying_v6:
            logger.info("🎬 [剪映 6.0] 导出 draft.json + EDL 指南...")
            
            # 确保有 timeline
            if timeline is None and highlights_list:
                logger.info("   生成剪辑时间线...")
                redundancy_detector = RedundancyDetector(config)
                redundancies = redundancy_detector.detect(video_path, transcript, scenes)
                timeline_gen = TimelineGenerator(config)
                original_duration = media_info.get("duration", 0)
                timeline = timeline_gen.generate(highlights_list, redundancies, original_duration)
            
            jianying_exporter = JianyingExporter(config)
            jy_output_dir = os.path.join(args.output, "jianying_v6")
            jy_result = jianying_exporter.export_with_guide(
                timeline=timeline or {},
                transcript=transcript,
                video_path=video_path,
                output_dir=jy_output_dir,
            )
            
            if jy_result.get("draft_path"):
                logger.info(f"   ✅ 剪映 draft.json: {jy_result['draft_path']}")
                output_paths["jianying_v6_draft"] = jy_result["draft_path"]
            
            if jy_result.get("guide_path"):
                logger.info(f"   ✅ EDL 导入指南: {jy_result['guide_path']}")
                output_paths["edl_guide"] = jy_result["guide_path"]
            
            if jy_result.get("edl_path"):
                output_paths["jianying_edl"] = jy_result["edl_path"]
            
            if jy_result.get("srt_path"):
                output_paths["jianying_srt"] = jy_result["srt_path"]
        if args.scene_management:
            logger.info("🎬 [场景管理] detect→slice 一条链...")
            scene_manager = SceneManager(config)
            scene_result = scene_manager.detect_and_slice(
                video_path, transcript, args.output, frames_dir
            )
            logger.info(f"   场景管理完成: {scene_result['total_chapters']} 个章节")
            
            # 更新 scenes 变量供后续报告使用
            scenes = scene_result["scenes"]
            output_paths["scene_management"] = scene_result["output_dir"]
        
        # ========== 爆款预测（可选，v4.2 新增） ==========
        viral_result = None
        if args.viral_predict:
            logger.info("🔥 [爆款预测] 分析爆款潜力...")
            predictor = ViralPredictor(config)
            viral_result = predictor.predict(
                video_path, transcript, scenes,
                platform_meta=platform_meta,
                visual_data=visual_data,
            )
            logger.info(f"   爆款得分: {viral_result['viral_score']}/100 ({viral_result['level']})")
            
            # 保存预测结果
            import json
            viral_path = os.path.join(args.output, "viral_prediction.json")
            os.makedirs(os.path.dirname(viral_path), exist_ok=True)
            with open(viral_path, "w", encoding="utf-8") as f:
                json.dump(viral_result, f, ensure_ascii=False, indent=2)
            output_paths["viral_prediction"] = viral_path
        
        # ========== 实时直播分析（可选，v4.2 新增） ==========
        live_stats = None
        if args.live_analyze:
            logger.info("🔴 [实时直播分析] 启动...")
            live = LiveAnalyzer(config)
            
            # 启动实时分析
            live.start(video_source=None)  # 模拟模式
            
            # 模拟实时输入（实际使用时应从流式 ASR 获取）
            for seg in transcript.get("segments", []):
                if not live._running:
                    break
                live.feed_segment(seg)
                time.sleep(0.01)  # 模拟实时间隔
            
            # 获取统计并停止
            live_stats = live.stop()
            logger.info(f"   直播分析完成: {live_stats['total_segments']} 段, "
                       f"{live_stats['total_sensitive_detected']} 次敏感词")
            
            # 导出敏感词日志
            if live_stats["total_sensitive_detected"] > 0:
                log_path = os.path.join(args.output, "live_sensitive_log.json")
                live.export_sensitive_log(log_path)
                output_paths["live_sensitive_log"] = log_path
        
        # ========== 说话人字幕（可选） ==========
        if diarize_result:
            logger.info("📝 生成说话人字幕...")
            speaker_srt_path = os.path.join(args.output, "speakers.srt")
            diarizer = SpeakerDiarization(config)
            diarizer.generate_srt_with_speakers(diarize_result, speaker_srt_path)
            output_paths["speaker_srt"] = speaker_srt_path
        
        # ========== 时间戳摘要 ==========
        logger.info("📋 生成时间戳摘要...")
        summary_dir = os.path.join(args.output, "summary")
        summary_gen = TimestampedSummary(config)
        summary_result = summary_gen.generate(highlights, fused_data, summary_dir)
        output_paths["timestamped_summary"] = summary_result.get("markdown_path")
        
        # ========== 听后简报（可选，v4.6 新增） ==========
        if args.weekly_briefing:
            logger.info("📊 生成听后简报...")
            briefing = WeeklyBriefing(config)
            weekly_briefing = briefing.generate()
            if weekly_briefing.get("output_path"):
                output_paths["weekly_briefing"] = weekly_briefing["output_path"]
                logger.info(f"   简报已生成: {weekly_briefing['output_path']}")
        
        # 清理缓存
        max_cache = config.get("processing", {}).get("max_memory_gb", 4)
        limit_cache_size(config.get("processing", {}).get("cache_dir", ".cache"), max_cache)
        
        elapsed = time.time() - start_time
        logger.info(f"\n{'='*50}")
        logger.info(f"✅ 分析完成！耗时: {elapsed:.1f}s")
        logger.info(f"📄 输出文件:")
        for fmt, path in output_paths.items():
            logger.info(f"   [{fmt}] {path}")
        logger.info(f"{'='*50}")
        
        # 停止资源监控
        if resource_monitor:
            resource_monitor.stop()
            status = resource_monitor.get_status()
            logger.info(f"📊 峰值内存: {status['peak_memory_gb']:.1f}GB")
        
    except KeyboardInterrupt:
        logger.warning("\n⚠️  用户中断")
        sys.exit(1)
    except Exception as e:
        logger.error(f"\n❌ 错误: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)
    finally:
        # 停止资源监控
        if resource_monitor:
            resource_monitor.stop()
        # 清理子进程，确保不残留
        if media and hasattr(media, '_subprocesses'):
            for proc in media._subprocesses:
                try:
                    proc.terminate()
                except Exception:
                    pass


def run_doctor_mode(args, config):
    """
    首跑自检模式（v4.5.0 新增）。
    
    一次性探测 ffmpeg / whisper 模型缓存 / 磁盘剩余空间 / 内存水位 / GPU 可用性，
    输出「缺什么→给什么」修复命令清单。
    """
    print_banner()
    print("🔍 首跑自检模式\n")
    
    doctor = Doctor(config)
    result = doctor.run_self_check()
    
    # 格式化输出报告
    report_text = Doctor.format_report(result["report"])
    print(report_text)
    
    # 输出摘要
    print(f"\n{result['summary']}")
    
    # 如果有需要修复的项，输出修复命令清单
    if result["fixes_needed"]:
        print("\n📋 修复命令清单（先清单后确认）：")
        print("-" * 50)
        for check_name in result["fixes_needed"]:
            fix_cmd = doctor.get_fix_instructions(check_name)
            if fix_cmd:
                print(f"\n[{check_name}]")
                print(f"  {fix_cmd}")
        print("\n" + "-" * 50)
        print("\n⚠️  以上为建议修复命令，请确认后手动执行。")
        print("    本工具不自动执行写操作，确保安全可控。")
    
    # 输出下一步建议
    if result["passed"]:
        print("\n✅ 环境就绪，可以开始分析视频：")
        print("  python main.py -i <视频路径>")
        print("\n  快速体验（5分钟出稿）：")
        print("  python main.py -i <视频路径> --quick")
    
    return 0 if result["passed"] else 1


def run_quick_mode(args, config):
    """
    快速模式（v4.5.0 新增）。
    
    仅转写+时间戳摘要，跳过视觉分析/场景切割/剪辑链，
    产出单文件 Markdown，末尾附 3 条「下一步建议」。
    
    目标：低配机与新用户 5 分钟见到第一份成果——先价值后深度。
    """
    print_banner()
    print("⚡ 快速模式（仅转写+摘要）\n")
    
    start_time = time.time()
    
    # 加载配置
    if not args.no_adaptive:
        logger.info("🔍 检测硬件配置...")
        probe = HardwareProbe(config)
        config = probe.apply_to_config(config)
        
        nice_level = config.get("processing", {}).get("nice_level", 5)
        apply_process_priority(nice_level)
    
    # 输入处理
    logger.info("📥 处理输入...")
    input_handler = InputHandler(config)
    video_path = input_handler.process(args.input)
    logger.info(f"   视频路径: {video_path}")
    
    # 媒体处理
    media = MediaProcessor(config)
    media_info = media.get_media_info(video_path)
    logger.info(f"   分辨率: {media_info['width']}x{media_info['height']}")
    logger.info(f"   时长: {media_info['duration']:.1f}s")
    
    # 提取音频
    audio_path = media.extract_audio(video_path)
    logger.info(f"   音频已提取: {audio_path}")
    
    # ASR 转写
    logger.info("🎙️  语音转文字...")
    asr_engine = args.asr_engine if args.asr_engine else config.get("asr", {}).get("engine", "auto")
    asr_router = ASRRouter(config)
    asr_result = asr_router.transcribe(
        audio_path,
        preferred_engine=asr_engine,
        language=args.lang if args.lang else config.get("asr", {}).get("language", "auto"),
    )
    
    transcript = {
        "text": asr_result.text,
        "language": asr_result.language,
        "duration": asr_result.duration,
        "segments": [
            {
                "id": seg.id,
                "start": seg.start,
                "end": seg.end,
                "text": seg.text,
                "confidence": seg.confidence,
            }
            for seg in asr_result.segments
        ],
    }
    
    logger.info(f"   识别完成: {len(transcript['segments'])} 个语音段")
    logger.info(f"   语言: {transcript.get('language', 'unknown')}")
    
    # 生成时间戳摘要
    logger.info("📋 生成时间戳摘要...")
    summary_dir = os.path.join(args.output, "summary")
    summary_gen = TimestampedSummary(config)
    summary_result = summary_gen.generate(None, {"scenes": []}, summary_dir)
    
    # 输出结果
    md_path = summary_result.get("markdown_path")
    if md_path:
        logger.info(f"   ✅ 摘要已保存: {md_path}")
    
    # 首跑「下一步建议」
    elapsed = time.time() - start_time
    logger.info(f"\n{'='*50}")
    logger.info(f"✅ 快速分析完成！耗时: {elapsed:.1f}s")
    logger.info(f"{'='*50}")
    
    # 读取生成的 Markdown 并追加「下一步建议」
    next_steps = """
---
## 📌 下一步建议

1. **深度分析** — 启用完整分析链（视觉/场景/精华提取）：
   ```bash
   python main.py -i {input_path}
   ```

2. **说话人分离** — 识别多人对话中的不同说话人：
   ```bash
   python main.py -i {input_path} --diarize
   ```

3. **平台适配** — 适配抖音/快手/B站/视频号：
   ```bash
   python main.py -i {input_path} --platform
   ```
"""
    
    if md_path and os.path.exists(md_path):
        with open(md_path, "a", encoding="utf-8") as f:
            f.write(next_steps.format(input_path=args.input))
        logger.info(f"   已追加「下一步建议」到: {md_path}")
    
    logger.info(f"\n📄 输出文件: {md_path}")
    
    return 0


def run_podcast_mode(args, config):
    """
    播客模式（v4.6.0 新增）。
    
    整合说话人分离 + 章节切片 + 金句提取，
    输出 Podcasting 2.0 标准章节标记 + 金句列表 + 说话人时间线。
    """
    print_banner()
    print("🎙️ 播客模式\n")
    
    start_time = time.time()
    
    # 加载配置
    if not args.no_adaptive:
        logger.info("🔍 检测硬件配置...")
        probe = HardwareProbe(config)
        config = probe.apply_to_config(config)
        
        nice_level = config.get("processing", {}).get("nice_level", 5)
        apply_process_priority(nice_level)
    
    # 输入处理
    logger.info("📥 处理输入...")
    input_handler = InputHandler(config)
    video_path = input_handler.process(args.input)
    logger.info(f"   音频路径: {video_path}")
    
    # 媒体处理
    media = MediaProcessor(config)
    media_info = media.get_media_info(video_path)
    logger.info(f"   时长: {media_info['duration']:.1f}s")
    
    # 提取音频
    audio_path = media.extract_audio(video_path)
    logger.info(f"   音频已提取: {audio_path}")
    
    # ASR 转写
    logger.info("🎙️  语音转文字...")
    asr_engine = args.asr_engine if args.asr_engine else config.get("asr", {}).get("engine", "auto")
    asr_router = ASRRouter(config)
    asr_result = asr_router.transcribe(
        audio_path,
        preferred_engine=asr_engine,
        language=args.lang if args.lang else config.get("asr", {}).get("language", "auto"),
    )
    
    transcript = {
        "text": asr_result.text,
        "language": asr_result.language,
        "duration": asr_result.duration,
        "segments": [
            {
                "id": seg.id,
                "start": seg.start,
                "end": seg.end,
                "text": seg.text,
                "confidence": seg.confidence,
            }
            for seg in asr_result.segments
        ],
    }
    
    logger.info(f"   识别完成: {len(transcript['segments'])} 个语音段")
    
    # 播客流水线
    logger.info("🎬 播客流水线...")
    pipeline = PodcastPipeline(config)
    result = pipeline.run(
        audio_path=audio_path,
        transcript=transcript,
        output_dir=args.output,
        n_speakers=None,
        diarize_profile=args.diarize_profile,
    )
    
    # 输出结果
    if result.get("output_files"):
        logger.info(f"\n📄 播客输出:")
        for fmt, path in result["output_files"].items():
            logger.info(f"   [{fmt}] {path}")
    
    # 说话人时间线
    if result.get("speaker_timeline"):
        timeline = result["speaker_timeline"]
        logger.info(f"\n🎙️ 说话人时间线 ({len(timeline)} 段):")
        for item in timeline[:5]:
            logger.info(f"   {item.get('speaker_name', '')}: "
                       f"{item.get('start', 0):.1f}s - {item.get('end', 0):.1f}s "
                       f"({item.get('duration', 0):.1f}s)")
    
    # 金句
    if result.get("highlights"):
        highlights = result["highlights"]
        logger.info(f"\n🌟 金句 Top{len(highlights)}:")
        for i, h in enumerate(highlights[:5], 1):
            logger.info(f"   {i}. [{h.get('start', 0):.1f}s] "
                       f"{h.get('text', '')[:50]}... "
                       f"(置信度: {h.get('confidence', 0):.0%})")
    
    elapsed = time.time() - start_time
    logger.info(f"\n{'='*50}")
    logger.info(f"✅ 播客分析完成！耗时: {elapsed:.1f}s")
    logger.info(f"{'='*50}")
    
    return 0


def run_weekly_briefing_mode(args, config):
    """
    听后简报模式（v4.6.0 新增）。
    
    复用 queue_manager 的 SQLite 队列，按周聚合生成 HTML 简报。
    """
    print_banner()
    print("📊 听后简报模式\n")
    
    briefing = WeeklyBriefing(config)
    result = briefing.generate()
    
    output_path = result.get("output_path")
    if output_path and os.path.exists(output_path):
        logger.info(f"✅ 简报已生成: {output_path}")
        logger.info(f"   周范围: {result.get('week_range', '')}")
        stats = result.get("stats", {})
        logger.info(f"   处理文件: {stats.get('total_tasks', 0)}")
        logger.info(f"   总时长: {stats.get('total_duration', 0) / 60:.1f} 分钟")
        return 0
    else:
        logger.warning("❌ 简报生成失败")
        return 1


def run_download_model_mode(args, config):
    """
    模型下载模式（v4.5.0 新增）。
    
    带进度可视化 + 3次自动重试 + HTTP Range 断点续传 + 清华镜像交互提示。
    """
    print_banner()
    print("📥 模型下载模式\n")
    
    model_name = args.download_model
    
    # 显示清华镜像提示
    downloader = ModelDownloader(config)
    mirror_hint = downloader.get_mirror_hint()
    print(mirror_hint)
    print()
    
    # 定义进度回调
    def progress_callback(downloaded, total_size, speed_kb_s):
        progress_text = ModelDownloader.format_progress(downloaded, total_size, speed_kb_s)
        print(f"\r   {progress_text}", end="", flush=True)
    
    # 执行下载
    print(f"⬇️  正在下载 whisper-{model_name} 模型...\n")
    result = downloader.download(model_name, progress_callback=progress_callback)
    
    print()  # 换行
    
    if result["success"]:
        print(f"\n✅ 模型下载完成: {result['model_path']}")
        print(f"   重试次数: {result['retries']}")
        return 0
    else:
        print(f"\n❌ 模型下载失败: {result['error']}")
        print(f"   已重试: {result['retries']} 次")
        print(f"\n💡 建议:")
        print(f"   1. 检查网络连接")
        print(f"   2. 使用清华镜像: pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple")
        print(f"   3. 手动下载: https://huggingface.co/openai/whisper-{model_name}")
        return 1


def run_batch_mode(args, config):
    """
    批量处理模式（v4.3 新增）。
    
    Args:
        args: 命令行参数
        config: 配置
    """
    logger.info("📂 批量处理模式")
    
    # 创建队列管理器
    queue = QueueManager(config)
    
    # 扫描目录
    video_files = queue.scan_directory(args.dir)
    
    if not video_files:
        logger.warning(f"目录中没有视频文件: {args.dir}")
        return
    
    # 批量入队
    task_ids = queue.enqueue_batch(video_files, args.output)
    logger.info(f"已入队 {len(task_ids)} 个任务")
    
    # 确定硬件档位
    tier = args.hardware_tier if args.hardware_tier else 'mid'
    
    # 定义处理函数
    def process_task(task):
        input_path = task["input_path"]
        output_dir = task["output_dir"]
        
        if not output_dir:
            output_dir = os.path.join(args.output, os.path.splitext(os.path.basename(input_path))[0])
        
        # 单文件处理逻辑（简化版）
        from core.media_probe import MediaProbe
        from core.media_processor import MediaProcessor
        
        media_probe = MediaProbe(config)
        
        if media_probe.is_pure_audio(input_path):
            media_info = media_probe.get_media_info_for_video(input_path)
            audio_path = media_info["audio_path"]
        else:
            media = MediaProcessor(config)
            media_info = media.get_media_info(input_path)
            audio_path = media.extract_audio(input_path)
        
        # ASR 识别
        from core.asr import ASRRouter
        asr_router = ASRRouter(config)
        asr_result = asr_router.transcribe(audio_path)
        
        transcript = {
            "text": asr_result.text,
            "language": asr_result.language,
            "duration": asr_result.duration,
            "segments": [
                {
                    "id": seg.id,
                    "start": seg.start,
                    "end": seg.end,
                    "text": seg.text,
                    "confidence": seg.confidence,
                }
                for seg in asr_result.segments
            ],
        }
        
        # 生成报告
        reporter = ReportGenerator(config)
        output_paths = reporter.generate(
            transcript=transcript,
            scenes={"scenes": [], "total_scenes": 0},
            visual_data={"scenes": []},
            aligned_data={},
            fused_data={},
            highlights=None,
            media_info=media_info,
            output_dir=output_dir,
        )
        
        return {"artifact_paths": output_dir, "transcript": transcript}
    
    # 运行批量处理
    stats = queue.run_batch(process_task, tier=tier)
    
    logger.info(f"批量处理完成: {stats}")


def run_download_ct2_model(args, config):
    """
    下载 CT2 模型（v4.3 新增）。
    
    Args:
        args: 命令行参数
        config: 配置
    """
    accelerator = GPUAccelerator(config)
    model_name = args.download_ct2_model
    
    # 获取下载指引
    instructions = accelerator.get_download_instructions(model_name)
    print(instructions)


if __name__ == "__main__":
    args = parse_args()
    config = load_config(args.config if os.path.exists(args.config) else None)
    
    if args.doctor:
        # 首跑自检模式（v4.5.0）
        exit_code = run_doctor_mode(args, config)
        sys.exit(exit_code)
    elif args.quick:
        # 快速模式（v4.5.0）
        exit_code = run_quick_mode(args, config)
        sys.exit(exit_code)
    elif args.download_model:
        # 模型下载模式（v4.5.0）
        exit_code = run_download_model_mode(args, config)
        sys.exit(exit_code)
    elif args.weekly_briefing:
        # 听后简报模式（v4.6.0）
        exit_code = run_weekly_briefing_mode(args, config)
        sys.exit(exit_code)
    elif args.dir:
        # 批量处理模式
        run_batch_mode(args, config)
    elif args.download_ct2_model:
        # 下载 CT2 模型模式
        run_download_ct2_model(args, config)
    else:
        # 单文件处理模式
        main()

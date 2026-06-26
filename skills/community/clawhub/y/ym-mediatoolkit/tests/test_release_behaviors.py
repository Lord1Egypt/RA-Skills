import os
import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest import mock

import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import run
from caption_segmenter import load_protected_terms, segment_captions, split_caption_text
from intent_parser import parse_media_intent
from job_manager import JobManager, collect_output_paths
from subtitle_extractor import clean_captions, extract_subtitles, fuse_asr_ocr_captions, normalize_caption
from utils import prepare_output_path, validate_media_source


class WorkingDirectoryTestCase(unittest.TestCase):
    def setUp(self):
        self._old_cwd = Path.cwd()
        self._tmpdir = tempfile.TemporaryDirectory()
        os.chdir(self._tmpdir.name)

    def tearDown(self):
        os.chdir(self._old_cwd)
        self._tmpdir.cleanup()


class MediaSourceTests(WorkingDirectoryTestCase):
    def test_local_file_inside_workspace_is_allowed(self):
        Path("sample.mp4").write_bytes(b"not a real video")

        resolved = validate_media_source("sample.mp4")

        self.assertEqual(resolved, str(Path("sample.mp4").resolve()))

    def test_path_traversal_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "路径穿越"):
            validate_media_source("../outside.mp4")

    def test_missing_local_file_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "不存在"):
            validate_media_source("missing.mp4")

    def test_http_source_is_allowed_after_public_dns_resolution(self):
        with mock.patch(
            "utils.socket.getaddrinfo",
            return_value=[(None, None, None, None, ("93.184.216.34", 443))],
        ):
            self.assertEqual(
                validate_media_source("https://example.com/video.mp4"),
                "https://example.com/video.mp4",
            )

    def test_media_root_allows_file_outside_workspace(self):
        with tempfile.TemporaryDirectory() as media_root_name:
            media_root = Path(media_root_name)
            media_file = media_root / "AA.MP4"
            media_file.write_bytes(b"not a real video")

            resolved = validate_media_source(str(media_file), media_roots=[str(media_root)])

        self.assertEqual(resolved, str(media_file.resolve()))

    def test_media_root_rejects_file_outside_allowed_roots(self):
        with tempfile.TemporaryDirectory() as media_root_name, tempfile.TemporaryDirectory() as outside_root_name:
            media_root = Path(media_root_name)
            outside_root = Path(outside_root_name)
            media_file = outside_root / "AA.MP4"
            media_file.write_bytes(b"not a real video")

            with self.assertRaisesRegex(ValueError, "media_roots"):
                validate_media_source(str(media_file), media_roots=[str(media_root)])

    def test_windows_drive_style_path_is_treated_as_local_path(self):
        Path("D:").mkdir()
        Path("D:/AA.MP4").write_bytes(b"not a real video")

        resolved = validate_media_source("D:/AA.MP4", media_roots=["D:"])

        self.assertEqual(resolved, str(Path("D:/AA.MP4").resolve()))


class OutputPathTests(WorkingDirectoryTestCase):
    def test_prepare_output_path_creates_default_directory(self):
        output = prepare_output_path(
            default_dir="output/audio",
            default_name="sample",
            extension=".mp3",
        )

        self.assertEqual(output, str(Path("output/audio/sample.mp3").resolve()))
        self.assertTrue(Path("output/audio").is_dir())

    def test_prepare_output_path_rejects_existing_file_without_overwrite(self):
        Path("output/audio").mkdir(parents=True)
        Path("output/audio/sample.mp3").write_bytes(b"existing")

        with self.assertRaisesRegex(ValueError, "overwrite=false"):
            prepare_output_path(
                default_dir="output/audio",
                default_name="sample",
                extension=".mp3",
                overwrite=False,
            )


class HandlerInputCompatibilityTests(WorkingDirectoryTestCase):
    def test_video_url_url_and_source_are_equivalent_for_info(self):
        Path("sample.mp4").write_bytes(b"not a real video")

        with mock.patch("utils.is_remote_source", return_value=False), \
             mock.patch("frame_extractor.get_local_video_info", return_value={"width": 1}):

            for field in ("video_url", "url", "source"):
                with self.subTest(field=field):
                    result = run.handle_info({field: "sample.mp4"})
                    self.assertEqual(result["status"], "success")
                    self.assertEqual(result["info"]["width"], 1)

    def test_missing_source_returns_json_error(self):
        result = run.handle_info({})

        self.assertEqual(result["status"], "error")
        self.assertEqual(result["code"], "missing_source")
        self.assertIn("Missing video_url/url/source", result["message"])
        self.assertIn("reply", result)
        self.assertIn("hint", result)

    def test_overwrite_false_error_is_returned_as_json(self):
        Path("sample.mp4").write_bytes(b"not a real video")

        with mock.patch(
            "run.extract_audio_streaming",
            side_effect=ValueError("输出文件已存在且 overwrite=false: output/audio/sample.mp3"),
        ):
            result = run.handle_audio({"source": "sample.mp4", "overwrite": False})

        self.assertEqual(result["status"], "error")
        self.assertEqual(result["code"], "output_exists")
        self.assertIn("overwrite=false", result["message"])

    def test_success_response_includes_action_protocol_fields(self):
        Path("sample.mp4").write_bytes(b"not a real video")

        with mock.patch("utils.is_remote_source", return_value=False), \
             mock.patch("frame_extractor.get_local_video_info", return_value={"width": 1}):
            result = run.handle_info({"source": "sample.mp4"})

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["code"], "ok")
        self.assertEqual(result["reply"], "已获取媒体信息。")
        self.assertIn("处理完成", result["hint"])


class BatchTests(WorkingDirectoryTestCase):
    def test_batch_merges_top_level_options_and_uses_name_for_audio_output(self):
        with mock.patch("run.handle_audio", return_value={"status": "success"}) as handle_audio:
            result = run.handle_batch({
                "action": "audio",
                "format": "mp3",
                "overwrite": False,
                "videos": [{"source": "sample.mp4", "name": "named_audio"}],
            })

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["success"], 1)
        called_params = handle_audio.call_args.args[0]
        self.assertEqual(called_params["video_url"], "sample.mp4")
        self.assertEqual(called_params["format"], "mp3")
        self.assertFalse(called_params["overwrite"])
        self.assertEqual(called_params["output_path"], "output/audio/named_audio.mp3")

    def test_batch_output_dir_is_applied_to_named_thumbnail(self):
        with mock.patch("run.handle_thumbnail", return_value={"status": "success"}) as handle_thumbnail:
            result = run.handle_batch({
                "action": "thumbnail",
                "output_dir": "custom_thumbs",
                "videos": [{"url": "sample.mp4", "name": "cover"}],
            })

        self.assertEqual(result["success"], 1)
        called_params = handle_thumbnail.call_args.args[0]
        self.assertEqual(called_params["video_url"], "sample.mp4")
        self.assertEqual(called_params["save_path"], str(Path("custom_thumbs/cover.jpg").resolve()))


class PipelineTests(WorkingDirectoryTestCase):
    def test_pipeline_requires_steps(self):
        Path("sample.mp4").write_bytes(b"not a real video")

        result = run.handle_pipeline({"source": "sample.mp4"})

        self.assertEqual(result["status"], "error")
        self.assertEqual(result["code"], "missing_steps")
        self.assertIn("Missing steps", result["message"])

    def test_pipeline_disabled_step_is_skipped_and_not_called(self):
        Path("sample.mp4").write_bytes(b"not a real video")
        handler = mock.Mock(return_value={"status": "success"})

        with mock.patch.dict(run.PIPELINE_STEP_HANDLERS, {"info": handler}):
            result = run.handle_pipeline({
                "source": "sample.mp4",
                "output_dir": "pipeline_out",
                "steps": [{"id": "metadata", "action": "info", "enabled": False}],
            })

        self.assertEqual(result["status"], "skipped")
        self.assertEqual(result["steps"][0]["status"], "skipped")
        handler.assert_not_called()
        self.assertTrue(Path("pipeline_out/manifest.json").exists())

    def test_pipeline_auto_output_path_for_thumbnail(self):
        Path("sample.mp4").write_bytes(b"not a real video")
        handler = mock.Mock(return_value={"status": "success", "saved_path": "unused"})

        with mock.patch.dict(run.PIPELINE_STEP_HANDLERS, {"thumbnail": handler}):
            result = run.handle_pipeline({
                "source": "sample.mp4",
                "output_dir": "pipeline_out",
                "steps": [{"id": "cover", "action": "thumbnail", "enabled": True}],
            })

        self.assertEqual(result["status"], "success")
        called_params = handler.call_args.args[0]
        self.assertEqual(called_params["save_path"], str(Path("pipeline_out/cover.jpg").resolve()))

    def test_pipeline_runs_steps_in_json_order_and_returns_partial(self):
        Path("sample.mp4").write_bytes(b"not a real video")
        calls = []

        def info_handler(params):
            calls.append("info")
            return {"status": "success"}

        def audio_handler(params):
            calls.append("audio")
            return {"status": "error", "message": "audio failed"}

        def thumbnail_handler(params):
            calls.append("thumbnail")
            return {"status": "success"}

        with mock.patch.dict(run.PIPELINE_STEP_HANDLERS, {
            "info": info_handler,
            "audio": audio_handler,
            "thumbnail": thumbnail_handler,
        }):
            result = run.handle_pipeline({
                "source": "sample.mp4",
                "output_dir": "pipeline_out",
                "steps": [
                    {"id": "metadata", "action": "info", "enabled": True},
                    {"id": "audio_mp3", "action": "audio", "enabled": True},
                    {"id": "cover", "action": "thumbnail", "enabled": True},
                ],
            })

        self.assertEqual(calls, ["info", "audio", "thumbnail"])
        self.assertEqual(result["status"], "partial")
        self.assertEqual(result["success"], 2)
        self.assertEqual(result["failed"], 1)
        manifest = json.loads(Path("pipeline_out/manifest.json").read_text())
        self.assertEqual(manifest["status"], "partial")
        self.assertEqual([step["id"] for step in manifest["steps"]], ["metadata", "audio_mp3", "cover"])

    def test_pipeline_auto_output_paths_for_audio_and_compress(self):
        Path("sample.mp4").write_bytes(b"not a real video")
        audio_handler = mock.Mock(return_value={"status": "success"})
        compress_handler = mock.Mock(return_value={"status": "success"})

        with mock.patch.dict(run.PIPELINE_STEP_HANDLERS, {
            "audio": audio_handler,
            "compress": compress_handler,
        }):
            result = run.handle_pipeline({
                "source": "sample.mp4",
                "output_dir": "pipeline_out",
                "steps": [
                    {"id": "audio_mp3", "action": "audio", "enabled": True, "params": {"format": "mp3"}},
                    {"id": "compressed", "action": "compress", "enabled": True},
                ],
            })

        self.assertEqual(result["status"], "success")
        self.assertEqual(audio_handler.call_args.args[0]["output_path"], str(Path("pipeline_out/audio_mp3.mp3").resolve()))
        self.assertEqual(compress_handler.call_args.args[0]["output_path"], str(Path("pipeline_out/compressed.mp4").resolve()))

    def test_pipeline_auto_output_path_for_subtitle(self):
        Path("sample.mp4").write_bytes(b"not a real video")
        subtitle_handler = mock.Mock(return_value={"status": "success", "outputPath": "unused"})

        with mock.patch.dict(run.PIPELINE_STEP_HANDLERS, {"subtitle": subtitle_handler}):
            result = run.handle_pipeline({
                "source": "sample.mp4",
                "output_dir": "pipeline_out",
                "steps": [
                    {"id": "captions", "action": "subtitle", "enabled": True, "params": {"mode": "asr"}},
                ],
            })

        self.assertEqual(result["status"], "success")
        self.assertEqual(subtitle_handler.call_args.args[0]["output_path"], str(Path("pipeline_out/captions.captions.json").resolve()))

    def test_pipeline_caption_segment_uses_previous_caption_output(self):
        Path("sample.mp4").write_bytes(b"not a real video")
        captions_path = str(Path("pipeline_out/captions.captions.json").resolve())
        subtitle_handler = mock.Mock(return_value={"status": "success", "outputPath": captions_path})
        segment_handler = mock.Mock(return_value={"status": "success", "outputPath": "segmented"})

        with mock.patch.dict(run.PIPELINE_STEP_HANDLERS, {
            "subtitle": subtitle_handler,
            "caption_segment": segment_handler,
        }):
            result = run.handle_pipeline({
                "source": "sample.mp4",
                "output_dir": "pipeline_out",
                "steps": [
                    {"id": "captions", "action": "subtitle", "enabled": True, "params": {"mode": "asr"}},
                    {"id": "emlet", "action": "caption_segment", "enabled": True, "params": {"max_chars": 12}},
                ],
            })

        self.assertEqual(result["status"], "success")
        self.assertEqual(segment_handler.call_args.args[0]["caption_path"], captions_path)
        self.assertEqual(segment_handler.call_args.args[0]["output_path"], str(Path("pipeline_out/emlet.captions.json").resolve()))


class IntentParserTests(unittest.TestCase):
    def test_parse_audio_command(self):
        parsed = parse_media_intent('将 "sample.mp4" 提取音频')

        self.assertEqual(parsed["action"], "audio")
        self.assertEqual(parsed["params"]["source"], "sample.mp4")
        self.assertEqual(parsed["params"]["format"], "mp3")

    def test_parse_thumbnail_command_with_time(self):
        parsed = parse_media_intent('给 "sample.mp4" 提取第 3 秒封面')

        self.assertEqual(parsed["action"], "thumbnail")
        self.assertEqual(parsed["params"]["time_seconds"], 3)

    def test_parse_compress_command(self):
        parsed = parse_media_intent('压缩 "sample.mp4"')

        self.assertEqual(parsed["action"], "compress")

    def test_parse_info_command(self):
        parsed = parse_media_intent('查看 "sample.mp4" 信息')

        self.assertEqual(parsed["action"], "info")

    def test_parse_subtitle_command(self):
        parsed = parse_media_intent('识别 "sample.mp4" 的字幕')

        self.assertEqual(parsed["action"], "subtitle")
        self.assertEqual(parsed["params"]["mode"], "fusion")


class ChatTests(WorkingDirectoryTestCase):
    def test_chat_runs_parsed_audio_action_and_returns_reply(self):
        Path("sample.mp4").write_bytes(b"not a real video")

        with mock.patch("run.handle_audio", return_value={"status": "success", "output_path": "output/audio/sample.mp3"}) as handle_audio, \
             mock.patch.dict(run.ACTIONS, {"audio": handle_audio}):
            result = run.handle_chat({"message": '将 "sample.mp4" 提取音频'})

        self.assertEqual(result["status"], "success")
        self.assertIn("已提取音频", result["reply"])
        self.assertEqual(result["action"], "audio")
        self.assertEqual(result["output_paths"], ["output/audio/sample.mp3"])
        self.assertEqual(handle_audio.call_args.args[0]["source"], "sample.mp4")

    def test_chat_parse_failure_does_not_call_handlers(self):
        with mock.patch("run.handle_audio") as handle_audio, \
             mock.patch.dict(run.ACTIONS, {"audio": handle_audio}):
            result = run.handle_chat({"message": "随便聊两句"})

        self.assertEqual(result["status"], "error")
        self.assertEqual(result["code"], "parse_failed")
        self.assertIn("sample.mp4", result["hint"])
        self.assertIn("我没识别出", result["reply"])
        handle_audio.assert_not_called()

    def test_chat_pipeline_json_uses_pipeline_handler(self):
        payload = {
            "source": "sample.mp4",
            "steps": [{"id": "metadata", "action": "info", "enabled": True}],
        }
        handler_result = {"status": "success", "manifest_path": "output/pipeline/sample/manifest.json"}

        with mock.patch("run.handle_pipeline", return_value=handler_result) as handle_pipeline, \
             mock.patch.dict(run.ACTIONS, {"pipeline": handle_pipeline}):
            result = run.handle_chat({"message": json.dumps(payload)})

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["action"], "pipeline")
        self.assertEqual(result["output_paths"], ["output/pipeline/sample/manifest.json"])
        handle_pipeline.assert_called_once_with(payload)

    def test_chat_runs_parsed_subtitle_action(self):
        Path("sample.mp4").write_bytes(b"not a real video")

        with mock.patch("run.handle_subtitle", return_value={"status": "success", "outputPath": "output/subtitles/sample.captions.json"}) as handle_subtitle, \
             mock.patch.dict(run.ACTIONS, {"subtitle": handle_subtitle}):
            result = run.handle_chat({"message": '识别 "sample.mp4" 的字幕'})

        self.assertEqual(result["status"], "success")
        self.assertIn("已生成字幕", result["reply"])
        self.assertEqual(result["action"], "subtitle")
        self.assertEqual(result["output_paths"], ["output/subtitles/sample.captions.json"])

    def test_chat_async_false_keeps_sync_behavior(self):
        Path("sample.mp4").write_bytes(b"not a real video")

        with mock.patch("run.handle_audio", return_value={"status": "success", "output_path": "output/audio/sample.mp3"}) as handle_audio, \
             mock.patch.dict(run.ACTIONS, {"audio": handle_audio}):
            result = run.handle_chat({"message": '将 "sample.mp4" 提取音频', "async": False})

        self.assertEqual(result["status"], "success")
        handle_audio.assert_called_once()


class SubtitleTests(WorkingDirectoryTestCase):
    def test_normalize_caption_schema_and_time(self):
        caption = normalize_caption({
            "captionTxt": " hello ",
            "startTimeUs": 2000,
            "endTimeUs": 1000,
            "source": "asr",
            "confidence": 2,
        })

        self.assertEqual(caption["captionTxt"], "hello")
        self.assertEqual(caption["startTimeUs"], 2000)
        self.assertEqual(caption["endTimeUs"], 2001)
        self.assertEqual(caption["source"], "asr")
        self.assertEqual(caption["confidence"], 1)

    def test_clean_captions_drops_empty_and_duplicate_text(self):
        captions = clean_captions([
            {"captionTxt": "", "startTimeUs": 0, "endTimeUs": 1},
            {"captionTxt": "hello", "startTimeUs": 2, "endTimeUs": 3},
            {"captionTxt": "hello", "startTimeUs": 4, "endTimeUs": 5},
        ])

        self.assertEqual(len(captions), 1)
        self.assertEqual(captions[0]["captionTxt"], "hello")

    def test_fuse_asr_ocr_uses_high_confidence_ocr_text(self):
        fused = fuse_asr_ocr_captions(
            [{"captionTxt": "helo", "startTimeUs": 0, "endTimeUs": 2_000_000, "source": "asr", "confidence": 0.5}],
            [{"captionTxt": "hello", "startTimeUs": 1_000_000, "endTimeUs": 1_500_000, "source": "ocr", "confidence": 0.95}],
        )

        self.assertEqual(fused[0]["captionTxt"], "hello")
        self.assertEqual(fused[0]["source"], "fusion")

    def test_asr_dependency_error_is_json(self):
        Path("sample.mp4").write_bytes(b"not a real video")

        with mock.patch("subtitle_extractor.transcribe_audio_source", return_value={"status": "error", "message": "missing", "code": "missing_asr_dependency"}):
            result = extract_subtitles("sample.mp4", mode="asr")

        self.assertEqual(result["status"], "error")
        self.assertEqual(result["code"], "missing_asr_dependency")

    def test_subtitle_mode_asr_writes_captions_json(self):
        Path("sample.mp4").write_bytes(b"not a real video")

        with mock.patch("subtitle_extractor.transcribe_audio_source", return_value={
            "status": "success",
            "captions": [{"captionTxt": "hi", "startTimeUs": 1, "endTimeUs": 2, "source": "asr", "confidence": 0.9}],
        }):
            result = extract_subtitles("sample.mp4", mode="asr")

        self.assertEqual(result["status"], "success")
        self.assertTrue(Path(result["outputPath"]).exists())
        payload = json.loads(Path(result["outputPath"]).read_text())
        self.assertEqual(payload["captions"][0]["captionTxt"], "hi")


class CaptionSegmentTests(WorkingDirectoryTestCase):
    def test_split_caption_text_respects_protected_terms(self):
        parts = split_caption_text(
            "今天我们聊苹果华为和吉利的新产品",
            max_chars=5,
            protected_terms=["苹果", "华为", "吉利"],
        )

        self.assertEqual("".join(parts), "今天我们聊苹果华为和吉利的新产品")
        self.assertNotIn("苹", parts)
        self.assertNotIn("果", parts)

    def test_segment_captions_allocates_continuous_time(self):
        result = segment_captions(
            [{
                "captionTxt": "今天我们来介绍一个很好用的视频处理工具",
                "startTimeUs": 1_000_000,
                "endTimeUs": 4_000_000,
                "source": "asr",
                "confidence": 0.9,
            }],
            max_chars=6,
        )

        self.assertGreater(len(result), 1)
        self.assertEqual(result[0]["startTimeUs"], 1_000_000)
        self.assertEqual(result[-1]["endTimeUs"], 4_000_000)
        for previous, current in zip(result, result[1:]):
            self.assertEqual(previous["endTimeUs"], current["startTimeUs"])
        self.assertTrue(all(len(item["captionTxt"]) <= 6 for item in result))

    def test_load_protected_terms_from_string_and_file(self):
        Path("terms.json").write_text(json.dumps({
            "brands": ["苹果", "华为"],
            "cars": ["吉利"],
        }), encoding="utf-8")

        terms = load_protected_terms("小米,理想", "terms.json")

        self.assertIn("苹果", terms)
        self.assertIn("吉利", terms)
        self.assertIn("小米", terms)

    def test_caption_segment_action_writes_segmented_json(self):
        result = run.handle_caption_segment({
            "captions": [{
                "captionTxt": "今天我们聊苹果华为和吉利的新产品",
                "startTimeUs": 0,
                "endTimeUs": 3_000_000,
            }],
            "max_chars": 5,
            "protected_terms": ["苹果", "华为", "吉利"],
        })

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["code"], "ok")
        self.assertTrue(Path(result["outputPath"]).exists())
        payload = json.loads(Path(result["outputPath"]).read_text(encoding="utf-8"))
        self.assertEqual(payload["maxChars"], 5)
        self.assertEqual("".join(item["captionTxt"] for item in payload["captions"]), "今天我们聊苹果华为和吉利的新产品")

    def test_caption_segment_action_accepts_caption_path(self):
        payload = {
            "source": "sample.mp4",
            "captions": [{
                "captionTxt": "今天我们来介绍一个很好用的视频处理工具",
                "startTimeUs": 0,
                "endTimeUs": 3_000_000,
            }],
        }
        Path("sample.captions.json").write_text(json.dumps(payload), encoding="utf-8")

        result = run.handle_caption_segment({
            "caption_path": "sample.captions.json",
            "max_chars": 6,
        })

        self.assertEqual(result["status"], "success")
        self.assertTrue(result["outputPath"].endswith("sample.segmented.captions.json"))


class JobManagerTests(WorkingDirectoryTestCase):
    def test_submit_creates_queued_job_file(self):
        manager = JobManager({"info": lambda params: {"status": "success"}}, autostart=False)

        result = manager.submit("info", {"source": "sample.mp4"}, metadata={"created_by": "jobs", "intent": "info", "source": "sample.mp4"})

        self.assertEqual(result["status"], "queued")
        self.assertEqual(result["created_by"], "jobs")
        self.assertEqual(result["intent"], "info")
        job_path = Path(result["job_path"])
        self.assertTrue(job_path.exists())
        job = json.loads(job_path.read_text(encoding="utf-8"))
        self.assertEqual(job["status"], "queued")
        self.assertEqual(job["action"], "info")
        self.assertEqual(job["created_by"], "jobs")
        self.assertEqual(job["source"], "sample.mp4")

    def test_worker_saves_success_result_and_output_paths(self):
        manager = JobManager({
            "thumbnail": lambda params: {
                "status": "success",
                "saved_path": "output/thumbs/sample.jpg",
                "reply": "done",
            }
        })

        queued = manager.submit("thumbnail", {})
        job = manager.wait_for_job(queued["job_id"])

        self.assertEqual(job["status"], "success")
        self.assertEqual(job["result"]["saved_path"], "output/thumbs/sample.jpg")
        self.assertEqual(job["output_paths"], ["output/thumbs/sample.jpg"])

    def test_worker_saves_error_result(self):
        manager = JobManager({
            "audio": lambda params: {
                "status": "error",
                "code": "ffmpeg_failed",
                "message": "boom",
                "reply": "没有处理成功：boom",
                "hint": "check ffmpeg",
            }
        })

        queued = manager.submit("audio", {})
        job = manager.wait_for_job(queued["job_id"])

        self.assertEqual(job["status"], "error")
        self.assertEqual(job["code"], "ffmpeg_failed")
        self.assertEqual(job["error"], "boom")
        self.assertEqual(job["result"]["hint"], "check ffmpeg")

    def test_submit_unknown_action_returns_error_without_job(self):
        manager = JobManager({"info": lambda params: {"status": "success"}}, autostart=False)

        result = manager.submit("missing", {})

        self.assertEqual(result["status"], "error")
        self.assertEqual(result["code"], "invalid_action")
        self.assertFalse(Path("output/jobs").exists() and list(Path("output/jobs").glob("*/job.json")))

    def test_get_missing_job_returns_json_error(self):
        manager = JobManager({"info": lambda params: {"status": "success"}}, autostart=False)

        result = manager.get_job("0" * 32)

        self.assertEqual(result["status"], "error")
        self.assertEqual(result["code"], "job_not_found")

    def test_list_jobs_supports_status_and_limit(self):
        manager = JobManager({"info": lambda params: {"status": "success"}}, autostart=False)
        manager.submit("info", {"name": "one"})
        manager.submit("info", {"name": "two"})

        result = manager.list_jobs(status="queued", limit=1)

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["total"], 2)
        self.assertEqual(len(result["jobs"]), 1)
        self.assertEqual(result["jobs"][0]["status"], "queued")

    def test_running_job_is_marked_interrupted_on_startup(self):
        job_id = "1" * 32
        job_dir = Path("output/jobs") / job_id
        job_dir.mkdir(parents=True)
        (job_dir / "job.json").write_text(json.dumps({
            "job_id": job_id,
            "action": "info",
            "params": {},
            "status": "running",
            "code": "ok",
            "reply": "running",
            "created_at": "2026-01-01T00:00:00+00:00",
            "started_at": "2026-01-01T00:00:01+00:00",
            "finished_at": None,
            "result": None,
            "output_paths": [],
            "error": None,
        }), encoding="utf-8")

        manager = JobManager({"info": lambda params: {"status": "success"}}, autostart=False)
        job = manager.get_job(job_id)

        self.assertEqual(job["status"], "error")
        self.assertEqual(job["code"], "job_interrupted")

    def test_cleanup_jobs_only_deletes_old_terminal_jobs(self):
        old_finished = (datetime.now(timezone.utc) - timedelta(days=10)).isoformat()
        new_finished = datetime.now(timezone.utc).isoformat()
        old_job_id = "2" * 32
        new_job_id = "3" * 32
        active_job_id = "4" * 32

        for job_id, status, finished_at in (
            (old_job_id, "success", old_finished),
            (new_job_id, "success", new_finished),
            (active_job_id, "running", None),
        ):
            job_dir = Path("output/jobs") / job_id
            job_dir.mkdir(parents=True)
            (job_dir / "job.json").write_text(json.dumps({
                "job_id": job_id,
                "action": "info",
                "params": {},
                "status": status,
                "code": "ok",
                "reply": status,
                "created_at": new_finished,
                "started_at": None,
                "finished_at": finished_at,
                "result": None,
                "output_paths": [],
                "error": None,
            }), encoding="utf-8")

        manager = JobManager({"info": lambda params: {"status": "success"}}, autostart=False)
        result = manager.cleanup_jobs(retention_days=7, max_jobs=200)

        self.assertEqual(result["deleted"], 1)
        self.assertFalse((Path("output/jobs") / old_job_id).exists())
        self.assertTrue((Path("output/jobs") / new_job_id).exists())
        self.assertTrue((Path("output/jobs") / active_job_id).exists())

    def test_cleanup_jobs_deletes_terminal_jobs_at_retention_boundary(self):
        finished = datetime.now(timezone.utc).isoformat()
        terminal_job_id = "5" * 32
        active_job_id = "6" * 32
        manager = JobManager({"info": lambda params: {"status": "success"}}, autostart=False)

        for job_id, status in (
            (terminal_job_id, "success"),
            (active_job_id, "queued"),
        ):
            job_dir = Path("output/jobs") / job_id
            job_dir.mkdir(parents=True)
            (job_dir / "job.json").write_text(json.dumps({
                "job_id": job_id,
                "action": "info",
                "params": {},
                "status": status,
                "code": "ok",
                "reply": status,
                "created_at": finished,
                "started_at": None,
                "finished_at": finished if status == "success" else None,
                "result": None,
                "output_paths": [],
                "error": None,
            }), encoding="utf-8")

        result = manager.cleanup_jobs(retention_days=0, max_jobs=200)

        self.assertEqual(result["deleted"], 1)
        self.assertFalse((Path("output/jobs") / terminal_job_id).exists())
        self.assertTrue((Path("output/jobs") / active_job_id).exists())

    def test_collect_output_paths_deduplicates_in_first_seen_order(self):
        result = {
            "output_path": "output/a.mp3",
            "nested": [
                {"saved_path": "output/b.jpg"},
                {"outputPath": "output/a.mp3"},
                {"manifest_path": "output/manifest.json"},
                {"output_path": "output/b.jpg"},
            ],
        }

        self.assertEqual(
            collect_output_paths(result),
            ["output/a.mp3", "output/b.jpg", "output/manifest.json"],
        )


class JobHttpTests(WorkingDirectoryTestCase):
    def test_http_job_lifecycle(self):
        actions = {
            "info": lambda params: {
                "status": "success",
                "code": "ok",
                "reply": "已获取媒体信息。",
                "hint": "处理完成。",
                "info": {"width": 1},
            }
        }
        manager = JobManager(actions)
        app = run.create_app(action_handlers=actions, job_manager=manager)
        client = app.test_client()

        response = client.post("/skill/jobs", json={"action": "info", "params": {"source": "sample.mp4"}})
        data = response.get_json()

        self.assertEqual(response.status_code, 202)
        self.assertEqual(data["status"], "queued")
        job = manager.wait_for_job(data["job_id"])
        self.assertEqual(job["status"], "success")

        detail = client.get(f"/skill/jobs/{data['job_id']}").get_json()
        self.assertEqual(detail["status"], "success")
        self.assertEqual(detail["result"]["info"]["width"], 1)

        listing = client.get("/skill/jobs").get_json()
        self.assertEqual(listing["status"], "success")
        self.assertEqual(listing["jobs"][0]["job_id"], data["job_id"])

    def test_http_job_unknown_action(self):
        actions = {"info": lambda params: {"status": "success"}}
        manager = JobManager(actions, autostart=False)
        app = run.create_app(action_handlers=actions, job_manager=manager)
        client = app.test_client()

        response = client.post("/skill/jobs", json={"action": "missing", "params": {}})
        data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["status"], "error")
        self.assertEqual(data["code"], "invalid_action")

    def test_http_job_rejects_non_object_params_without_creating_job(self):
        actions = {"info": lambda params: {"status": "success"}}
        manager = JobManager(actions, autostart=False)
        app = run.create_app(action_handlers=actions, job_manager=manager)
        client = app.test_client()

        response = client.post("/skill/jobs", json={"action": "info", "params": []})
        data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["status"], "error")
        self.assertEqual(data["code"], "invalid_params")
        self.assertEqual(manager.list_jobs()["total"], 0)

    def test_http_chat_async_true_queues_without_running_handler(self):
        Path("sample.mp4").write_bytes(b"not a real video")
        subtitle_handler = mock.Mock(return_value={"status": "success"})
        actions = {
            "chat": run.handle_chat,
            "subtitle": subtitle_handler,
        }
        manager = JobManager(actions, autostart=False)
        app = run.create_app(action_handlers=actions, job_manager=manager)
        client = app.test_client()

        with mock.patch.dict(run.ACTIONS, actions, clear=True):
            response = client.post("/skill/chat", json={"message": '识别 "sample.mp4" 的字幕', "async": True})
        data = response.get_json()

        self.assertEqual(response.status_code, 202)
        self.assertEqual(data["status"], "queued")
        self.assertEqual(data["action"], "subtitle")
        self.assertEqual(data["intent"], "subtitle")
        self.assertIn("job_id", data)
        subtitle_handler.assert_not_called()
        job = manager.get_job(data["job_id"])
        self.assertEqual(job["created_by"], "chat")
        self.assertEqual(job["intent"], "subtitle")
        self.assertEqual(job["source"], "sample.mp4")

    def test_http_chat_async_wait_timeout_returns_completed_job_with_200(self):
        Path("sample.mp4").write_bytes(b"not a real video")
        actions = {
            "chat": run.handle_chat,
            "info": lambda params: {
                "status": "success",
                "code": "ok",
                "reply": "已获取媒体信息。",
                "hint": "处理完成。",
                "info": {"width": 1},
            },
        }
        manager = JobManager(actions)
        app = run.create_app(action_handlers=actions, job_manager=manager)
        client = app.test_client()

        response = client.post("/skill/chat", json={
            "message": '查看 "sample.mp4" 信息',
            "async": True,
            "wait_timeout_sec": 1,
        })
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["result"]["info"]["width"], 1)
        self.assertIn("job_id", data)

    def test_http_chat_async_unfinished_job_returns_202(self):
        Path("sample.mp4").write_bytes(b"not a real video")
        subtitle_handler = mock.Mock(return_value={"status": "success"})
        actions = {
            "chat": run.handle_chat,
            "subtitle": subtitle_handler,
        }
        manager = JobManager(actions, autostart=False)
        app = run.create_app(action_handlers=actions, job_manager=manager)
        client = app.test_client()

        response = client.post("/skill/chat", json={"message": '识别 "sample.mp4" 的字幕', "async": True})
        data = response.get_json()

        self.assertEqual(response.status_code, 202)
        self.assertEqual(data["status"], "queued")
        subtitle_handler.assert_not_called()

    def test_http_chat_rejects_invalid_async_and_wait_timeout(self):
        actions = {"chat": run.handle_chat}
        manager = JobManager(actions, autostart=False)
        app = run.create_app(action_handlers=actions, job_manager=manager)
        client = app.test_client()

        async_response = client.post("/skill/chat", json={"message": "anything", "async": "true"})
        timeout_response = client.post("/skill/chat", json={"message": "anything", "wait_timeout_sec": 31})

        self.assertEqual(async_response.status_code, 400)
        self.assertEqual(async_response.get_json()["code"], "invalid_async_mode")
        self.assertEqual(timeout_response.status_code, 400)
        self.assertEqual(timeout_response.get_json()["code"], "invalid_wait_timeout")

    def test_http_chat_uses_current_action_registry_for_sync_execution(self):
        Path("sample.mp4").write_bytes(b"not a real video")
        info_handler = mock.Mock(return_value={
            "status": "success",
            "code": "ok",
            "reply": "custom info",
            "hint": "处理完成。",
            "marker": "custom-registry",
        })
        actions = {
            "chat": run.handle_chat,
            "info": info_handler,
        }
        manager = JobManager(actions, autostart=False)
        app = run.create_app(action_handlers=actions, job_manager=manager)
        client = app.test_client()

        response = client.post("/skill/chat", json={"message": '查看 "sample.mp4" 信息'})
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["result"]["marker"], "custom-registry")
        info_handler.assert_called_once()

    def test_http_chat_async_auto_keeps_info_sync_and_subtitle_async(self):
        Path("sample.mp4").write_bytes(b"not a real video")
        info_handler = mock.Mock(return_value={"status": "success", "reply": "已获取媒体信息。"})
        subtitle_handler = mock.Mock(return_value={"status": "success"})
        actions = {
            "chat": run.handle_chat,
            "info": info_handler,
            "subtitle": subtitle_handler,
        }
        manager = JobManager(actions, autostart=False)
        app = run.create_app(action_handlers=actions, job_manager=manager)
        client = app.test_client()

        with mock.patch.dict(run.ACTIONS, actions, clear=True):
            info_response = client.post("/skill/chat", json={"message": '查看 "sample.mp4" 信息', "async": "auto"})
            subtitle_response = client.post("/skill/chat", json={"message": '识别 "sample.mp4" 的字幕', "async": "auto"})

        info_data = info_response.get_json()
        subtitle_data = subtitle_response.get_json()

        self.assertEqual(info_response.status_code, 200)
        self.assertEqual(info_data["status"], "success")
        info_handler.assert_called_once()
        self.assertEqual(subtitle_response.status_code, 202)
        self.assertEqual(subtitle_data["status"], "queued")
        subtitle_handler.assert_not_called()

    def test_http_chat_parse_failure_does_not_create_job(self):
        actions = {
            "chat": run.handle_chat,
            "audio": mock.Mock(return_value={"status": "success"}),
        }
        manager = JobManager(actions, autostart=False)
        app = run.create_app(action_handlers=actions, job_manager=manager)
        client = app.test_client()

        with mock.patch.dict(run.ACTIONS, actions, clear=True):
            response = client.post("/skill/chat", json={"message": "随便聊两句", "async": True})
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["status"], "error")
        self.assertEqual(data["code"], "parse_failed")
        self.assertEqual(manager.list_jobs()["total"], 0)

    def test_http_chat_async_job_can_be_polled_to_result(self):
        Path("sample.mp4").write_bytes(b"not a real video")
        actions = {
            "chat": run.handle_chat,
            "subtitle": lambda params: {
                "status": "success",
                "code": "ok",
                "reply": "已生成字幕：output/subtitles/sample.captions.json",
                "hint": "处理完成。",
                "outputPath": "output/subtitles/sample.captions.json",
            },
        }
        manager = JobManager(actions)
        app = run.create_app(action_handlers=actions, job_manager=manager)
        client = app.test_client()

        with mock.patch.dict(run.ACTIONS, actions, clear=True):
            response = client.post("/skill/chat", json={"message": '识别 "sample.mp4" 的字幕', "async": "auto"})
        data = response.get_json()

        self.assertEqual(response.status_code, 202)
        job = manager.wait_for_job(data["job_id"])
        self.assertEqual(job["status"], "success")
        detail = client.get(data["poll_url"]).get_json()
        self.assertEqual(detail["status"], "success")
        self.assertEqual(detail["reply"], "已生成字幕：output/subtitles/sample.captions.json")
        self.assertEqual(detail["output_paths"], ["output/subtitles/sample.captions.json"])


if __name__ == "__main__":
    unittest.main()

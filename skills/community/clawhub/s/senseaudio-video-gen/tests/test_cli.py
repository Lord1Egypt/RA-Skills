#!/usr/bin/env python3
import base64
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "senseaudio_video_gen.py"


def load_video_gen_module():
    spec = importlib.util.spec_from_file_location("senseaudio_video_gen_under_test", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_cmd(*args: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
        check=True,
    )


def test_help() -> None:
    result = run_cmd("--help")
    assert "init" in result.stdout
    assert "compose" in result.stdout
    assert "site-video" in result.stdout
    assert "source-ingest" in result.stdout
    assert "site-vision-plan" in result.stdout
    assert "llm-plan" in result.stdout
    assert "styles" in result.stdout
    assert "beats" in result.stdout
    assert "lint" in result.stdout
    assert "captions" in result.stdout
    assert "captions-export" in result.stdout
    assert "timeline" in result.stdout
    assert "motion-audit" in result.stdout
    assert "motion-map" in result.stdout
    assert "frame-quality-audit" in result.stdout
    assert "audio-data" in result.stdout
    assert "asset-add" in result.stdout
    assert "asset-report" in result.stdout
    assert "generate-assets" in result.stdout
    assert "build" in result.stdout
    assert "render" in result.stdout
    assert "video-create" in result.stdout
    assert "music-create" in result.stdout
    assert "music-status" in result.stdout
    assert "mix-audio" in result.stdout
    assert "repair" in result.stdout
    assert "tts" in result.stdout


def test_init_project() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        project = Path(directory) / "demo"
        result = run_cmd("init", str(project), "--duration", "1", "--fps", "2")
        assert str(project) in result.stdout
        assert (project / "index.html").exists()
        assert (project / "senseframe-runtime.js").exists()
        meta = json.loads((project / "senseframe.json").read_text())
        assert meta["duration"] == 1.0
        assert meta["fps"] == 2


def test_video_dry_run() -> None:
    result = run_cmd("video-create", "--prompt", "demo", "--dry-run")
    payload = json.loads(result.stdout)
    assert payload["endpoint"] == "/video/create"
    assert payload["payload"]["content"][0]["text"] == "demo"


def test_tts_dry_run() -> None:
    result = run_cmd(
        "tts",
        "--text",
        "hello",
        "--voice-id",
        "male_0004_a",
        "--output",
        "out.mp3",
        "--dry-run",
    )
    payload = json.loads(result.stdout)
    assert payload["endpoint"] == "/t2a_v2"
    assert payload["payload"]["voice_setting"]["voice_id"] == "male_0004_a"


def test_styles_command_lists_registry() -> None:
    result = run_cmd("styles", "--json")
    payload = json.loads(result.stdout)
    assert "product-glass" in payload["presets"]
    assert "executive-film" in payload["presets"]
    assert "neon-console" in payload["presets"]
    assert payload["presets"]["product-glass"]["tokens"]["accent"].startswith("#")
    assert payload["presets"]["executive-film"]["tokens"]["stage_bg"] == "#090908"


def test_compose_offline_project() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        project = Path(directory) / "campaign"
        result = run_cmd(
            "compose",
            "--project",
            str(project),
            "--brief",
            "Show a sound library webpage in three beats.",
            "--duration",
            "4",
            "--fps",
            "12",
            "--offline",
        )
        assert str(project) in result.stdout
        meta = json.loads((project / "senseframe.json").read_text())
        assert meta["duration"] == 4.0
        assert meta["fps"] == 12
        assert meta["storyboard"][0]["intent"]
        assert (project / "assets" / "narration.txt").exists()
        assert (project / "assets" / "asset-manifest.json").exists()
        html = (project / "index.html").read_text()
        assert "data-scene" in html
        assert "data-caption-source" in html


def test_compose_style_preset_applies_tokens_and_metadata() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        project = Path(directory) / "styled"
        run_cmd(
            "compose",
            "--project",
            str(project),
            "--brief",
            "demo",
            "--duration",
            "4",
            "--offline",
            "--style-preset",
            "neon-console",
            "--animation-preset",
            "cinematic",
        )
        html = (project / "index.html").read_text()
        meta = json.loads((project / "senseframe.json").read_text())
        manifest = json.loads((project / "assets" / "asset-manifest.json").read_text())
        assert 'data-style-preset="neon-console"' in html
        assert "--accent: #00e5ff" in html
        assert meta["style_preset"] == "neon-console"
        assert meta["style_tokens"]["accent"] == "#00e5ff"
        assert manifest["assets"]["style-preset"]["metadata"]["preset"] == "neon-console"


def test_compose_default_uses_executive_film_style() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        project = Path(directory) / "executive-film"
        run_cmd(
            "compose",
            "--project",
            str(project),
            "--brief",
            "Create a premium launch film for an AI research product.",
            "--duration",
            "6",
            "--offline",
        )
        html = (project / "index.html").read_text()
        meta = json.loads((project / "senseframe.json").read_text())
        assert meta["style_preset"] == "executive-film"
        assert 'data-style-preset="executive-film"' in html
        assert '[data-style-preset="executive-film"] .visual-card' in html
        assert "executive-plate" in html
        assert "abstract-shot" in html
        assert "content-ledger" in html
        assert "metric-stamp" in html
        assert "executive-layout-title-slate" in html
        assert "morph-bridge" in html
        assert "applyMorphBridge" in html
        assert "Executive Film" in html
        assert "Website Brief" not in html
        assert "border-radius: 0" in html
        captions = json.loads((project / "assets" / "captions.json").read_text())["captions"]
        assert len(captions) > 1
        assert max(len(item["text"]) for item in captions) <= 36


def test_beats_command_writes_scene_beats() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        project = Path(directory) / "beats-demo"
        run_cmd("compose", "--project", str(project), "--brief", "demo", "--duration", "6", "--offline")
        result = run_cmd("beats", "--project", str(project), "--beats-per-scene", "4", "--json")
        payload = json.loads(result.stdout)
        assert payload["count"] == 6
        assert payload["beats"][0]["scene_id"]
        assert payload["beats"][0]["role"] in {"hook", "proof", "detail", "cta"}
        assert min(beat["duration"] for beat in payload["beats"]) >= 0.95
        assert (project / "assets" / "beats.json").exists()
        manifest = json.loads((project / "assets" / "asset-manifest.json").read_text())
        assert manifest["assets"]["beats"]["path"] == "assets/beats.json"


def test_compose_beat_mode_layered_writes_beats_html_and_tracks() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        project = Path(directory) / "layered-beats"
        run_cmd(
            "compose",
            "--project",
            str(project),
            "--brief",
            "demo",
            "--duration",
            "6",
            "--offline",
            "--beat-mode",
            "layered",
            "--animation-preset",
            "cinematic",
            "--timeline-engine",
            "gsap-compat",
        )
        html = (project / "index.html").read_text()
        meta = json.loads((project / "senseframe.json").read_text())
        beats = json.loads((project / "assets" / "beats.json").read_text())
        timeline = json.loads((project / "assets" / "timeline.json").read_text())
        assert meta["beat_mode"] == "layered"
        assert 'data-beat="' in html
        assert "beat-layer" in html
        assert beats["beats"]
        assert min(beat["duration"] for beat in beats["beats"]) >= 0.95
        assert any("data-beat" in track["selector"] for track in timeline["tracks"])


def test_llm_plan_dry_run_targets_deepseek() -> None:
    result = run_cmd(
        "llm-plan",
        "--brief",
        "Introduce SenseAudio sound library.",
        "--duration",
        "9",
        "--provider",
        "deepseek",
        "--dry-run",
    )
    payload = json.loads(result.stdout)
    assert payload["provider"] == "deepseek"
    assert payload["url"] == "https://api.deepseek.com/chat/completions"
    assert payload["model"] == "deepseek-v4-pro"
    assert payload["payload"]["model"] == "deepseek-v4-pro"
    assert payload["payload"]["response_format"]["type"] == "json_object"
    assert "storyboard" in payload["schema"]["required"]


def test_site_asset_inventory_normalizes_browser_payload() -> None:
    module = load_video_gen_module()
    raw = {
        "images": [
            {"url": "/hero.png", "alt": "Hero", "width": 1200, "height": 640, "kind": "img"},
            {"url": "https://cdn.example/bg.webp", "kind": "css-background"},
        ],
        "icons": [{"url": "/favicon.svg", "rel": "icon"}],
        "fonts": [{"family": "Inter", "source": "document.fonts"}, {"family": "Inter", "source": "css"}],
        "animations": [{"type": "css-animation", "name": "fade-up", "selector": ".hero"}],
        "media": [{"url": "/intro.mp4", "kind": "video"}],
        "scripts": [{"url": "/lottie-player.js", "kind": "lottie-hint"}],
        "canvases": [{"kind": "webgl", "width": 640, "height": 360}],
    }

    payload = module.normalize_site_asset_inventory("https://acme.example/products/page", raw)

    assert payload["source_url"] == "https://acme.example/products/page"
    assert payload["counts"]["images"] == 2
    assert payload["counts"]["fonts"] == 1
    assert payload["images"][0]["url"] == "https://acme.example/hero.png"
    assert payload["icons"][0]["url"] == "https://acme.example/favicon.svg"
    assert payload["media"][0]["url"] == "https://acme.example/intro.mp4"
    assert payload["fonts"] == [{"family": "Inter", "source": "document.fonts"}]
    assert payload["signals"]["has_lottie_hint"] is True
    assert payload["signals"]["has_webgl"] is True


def test_browser_cookie_loader_accepts_storage_state_json() -> None:
    import tempfile

    module = load_video_gen_module()
    with tempfile.TemporaryDirectory() as directory:
        cookie_file = Path(directory) / "cookies.json"
        cookie_file.write_text(
            json.dumps(
                {
                    "cookies": [
                        {
                            "name": "sid",
                            "value": "abc",
                            "domain": ".example.com",
                            "path": "/",
                            "secure": True,
                            "httpOnly": True,
                            "sameSite": "Lax",
                            "expires": 1893456000,
                        }
                    ]
                }
            ),
            encoding="utf-8",
        )
        cookies = module.load_browser_cookies(str(cookie_file), "https://example.com/dashboard")
    assert cookies == [
        {
            "name": "sid",
            "value": "abc",
            "domain": ".example.com",
            "path": "/",
            "expires": 1893456000.0,
            "secure": True,
            "httpOnly": True,
            "sameSite": "Lax",
        }
    ]


def test_frame_quality_flags_internal_copy_leaks() -> None:
    import tempfile

    module = load_video_gen_module()
    with tempfile.TemporaryDirectory() as directory:
        project = Path(directory) / "quality"
        project.mkdir()
        (project / "index.html").write_text("<main>PAGE SIGNAL should not be visible</main>", encoding="utf-8")
        payload = module.frame_quality_audit(project, [])
    assert payload["safe_to_render"] is False
    assert any(issue["code"] == "internal_copy_leak" for issue in payload["issues"])


def test_render_capture_mode_preserves_persistent_when_parallel_is_set() -> None:
    module = load_video_gen_module()

    assert module.resolve_render_capture_mode("persistent", 4) == "persistent"
    assert module.resolve_render_capture_mode("process", 4) == "process"
    assert module.resolve_render_capture_mode("persistent", 1) == "persistent"


def test_local_urlopen_bypasses_proxy_environment() -> None:
    import http.server
    import os
    import socketserver
    import threading

    module = load_video_gen_module()

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"ok": true}')

        def log_message(self, format: str, *args: object) -> None:
            return

    with socketserver.TCPServer(("127.0.0.1", 0), Handler) as server:
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        old_proxy = os.environ.get("HTTP_PROXY")
        old_no_proxy = os.environ.get("NO_PROXY")
        os.environ["HTTP_PROXY"] = "http://127.0.0.1:9"
        os.environ.pop("NO_PROXY", None)
        try:
            with module.urlopen_no_proxy(f"http://127.0.0.1:{server.server_address[1]}/json/list", timeout=1.0) as resp:
                assert json.loads(resp.read().decode("utf-8")) == {"ok": True}
        finally:
            if old_proxy is None:
                os.environ.pop("HTTP_PROXY", None)
            else:
                os.environ["HTTP_PROXY"] = old_proxy
            if old_no_proxy is None:
                os.environ.pop("NO_PROXY", None)
            else:
                os.environ["NO_PROXY"] = old_no_proxy
            server.shutdown()


def test_llm_plan_dry_run_targets_audioclaw_config() -> None:
    import os
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        config = Path(directory) / "config.json"
        config.write_text(
            json.dumps(
                {
                    "agents": {"defaults": {"model_name": "Doubao-Seed-2.0-Pro"}},
                    "model_list": [
                        {
                            "model_name": "Doubao-Seed-2.0-Pro",
                            "model": "volcengine/doubao-seed-2-0-pro-260215",
                            "api_base": "https://platform.senseaudio.cn/v1",
                            "api_key": "test-key",
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        env = os.environ.copy()
        env["AUDIOCLAW_CONFIG_PATH"] = str(config)
        result = run_cmd(
            "llm-plan",
            "--brief",
            "Introduce Anthropic.",
            "--duration",
            "8",
            "--provider",
            "audioclaw",
            "--dry-run",
            env=env,
        )
    payload = json.loads(result.stdout)
    assert payload["provider"] == "audioclaw"
    assert payload["url"] == "https://platform.senseaudio.cn/v1/chat/completions"
    assert payload["model"] == "doubao-seed-2-0-pro-260215"
    assert payload["payload"]["model"] == "doubao-seed-2-0-pro-260215"


def test_llm_plan_dry_run_does_not_use_senseaudio_key_for_audioclaw() -> None:
    import os
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        env = os.environ.copy()
        env["AUDIOCLAW_CONFIG_PATH"] = str(Path(directory) / "missing-config.json")
        env["SENSEAUDIO_API_KEY"] = "senseaudio-test-key"
        env.pop("AUDIOCLAW_LLM_API_KEY", None)
        env.pop("AUDIOCLAW_LLM_BASE_URL", None)
        env.pop("AUDIOCLAW_LLM_MODEL", None)
        result = run_cmd(
            "llm-plan",
            "--brief",
            "Introduce SenseAudio.",
            "--duration",
            "8",
            "--dry-run",
            env=env,
        )
    payload = json.loads(result.stdout)
    assert payload["provider"] == "audioclaw"
    assert payload["url"] == "https://platform.senseaudio.cn/v1/chat/completions"
    assert payload["model"] == "doubao-seed-2-0-pro-260215"
    assert payload["payload"]["model"] == "doubao-seed-2-0-pro-260215"


def test_audioclaw_api_key_uses_only_llm_env_or_config() -> None:
    import os

    module = load_video_gen_module()
    old_env = os.environ.copy()
    original_local = module.local_senseaudio_credential
    try:
        os.environ.pop("AUDIOCLAW_LLM_API_KEY", None)
        os.environ["SENSEAUDIO_API_KEY"] = "media-env-key"
        module.local_senseaudio_credential = lambda name: "media-local-key"
        assert module.resolve_audioclaw_llm_api_key({"api_key": "llm-config-key"}) == "llm-config-key"
        assert module.resolve_audioclaw_llm_api_key({"api_key": ""}) == ""
        os.environ["AUDIOCLAW_LLM_API_KEY"] = "explicit-llm-key"
        assert module.resolve_audioclaw_llm_api_key({"api_key": "llm-config-key"}) == "explicit-llm-key"
    finally:
        os.environ.clear()
        os.environ.update(old_env)
        module.local_senseaudio_credential = original_local


def test_audioclaw_llm_env_overrides_work_without_config() -> None:
    import os
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        env = os.environ.copy()
        env["AUDIOCLAW_CONFIG_PATH"] = str(Path(directory) / "missing-config.json")
        env["AUDIOCLAW_LLM_API_KEY"] = "env-llm-key"
        env["AUDIOCLAW_LLM_BASE_URL"] = "https://llm.example/v1"
        env["AUDIOCLAW_LLM_MODEL"] = "custom-model"
        result = run_cmd(
            "llm-plan",
            "--brief",
            "Introduce custom routing.",
            "--duration",
            "8",
            "--provider",
            "audioclaw",
            "--dry-run",
            env=env,
        )
    payload = json.loads(result.stdout)
    assert payload["provider"] == "audioclaw"
    assert payload["url"] == "https://llm.example/v1/chat/completions"
    assert payload["model"] == "custom-model"
    assert payload["payload"]["model"] == "custom-model"


def test_llm_plan_dry_run_targets_openrouter() -> None:
    result = run_cmd(
        "llm-plan",
        "--brief",
        "Introduce Claude Code with concrete workflow evidence.",
        "--duration",
        "9",
        "--provider",
        "openrouter",
        "--dry-run",
    )
    payload = json.loads(result.stdout)
    assert payload["provider"] == "openrouter"
    assert payload["url"] == "https://openrouter.ai/api/v1/chat/completions"
    assert payload["model"] == "google/gemini-3.1-flash-lite"
    assert payload["payload"]["model"] == "google/gemini-3.1-flash-lite"
    assert payload["payload"]["response_format"]["type"] == "json_object"


def test_site_video_dry_run_plans_hyperframes_style_pipeline() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        project = Path(directory) / "site-video"
        result = run_cmd(
            "site-video",
            "--url",
            "https://www.anthropic.com/",
            "--project",
            str(project),
            "--duration",
            "14",
            "--fps",
            "30",
            "--dry-run",
        )
    payload = json.loads(result.stdout)
    assert payload["dry_run"] is True
    assert payload["project"] == str(project.resolve())
    assert payload["defaults"]["llm"] == "audioclaw"
    assert payload["defaults"]["style_preset"] == "editorial-pro"
    assert payload["defaults"]["beat_mode"] == "layered"
    assert payload["defaults"]["quality_audit"] is True
    assert [step["name"] for step in payload["steps"]] == [
        "compose",
        "audio-data",
        "lint",
        "render",
        "inspect",
        "frame-quality-audit",
        "motion-audit",
        "motion-map",
    ]
    compose = payload["steps"][0]
    assert compose["site_screenshots"] is True
    assert compose["browser_profile"] is False
    assert compose["cookie_file"] is False
    assert compose["timeline_engine"] == "gsap-compat"
    assert payload["output"].endswith("renders/site-video.mp4")


def test_site_video_dry_run_can_plan_cookie_backed_capture() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        project = root / "site-video"
        cookie_file = root / "cookies.json"
        cookie_file.write_text(json.dumps({"cookies": [{"name": "session", "value": "1", "domain": "example.com"}]}), encoding="utf-8")
        result = run_cmd(
            "site-video",
            "--url",
            "https://example.com",
            "--project",
            str(project),
            "--browser-profile",
            str(root / "browser-profile"),
            "--cookie-file",
            str(cookie_file),
            "--dry-run",
        )
    payload = json.loads(result.stdout)
    compose = payload["steps"][0]
    assert compose["browser_profile"] is True
    assert compose["cookie_file"] is True


def test_site_video_offline_no_render_writes_project_audio_data_and_report() -> None:
    import os
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        site_file = root / "site.json"
        site_file.write_text(
            json.dumps(
                {
                    "site": {
                        "source_url": "https://acme.example/",
                        "brand_name": "Acme Cloud",
                        "title": "Acme Cloud | Reliable AI infrastructure",
                        "summary": "Acme Cloud helps teams deploy safe AI systems.",
                        "headings": ["Deploy reliable AI agents", "Observe every workflow"],
                        "ctas": ["Start building", "Book a demo"],
                        "sections": [
                            {"heading": "Observe every workflow", "text": "Trace model calls and cost."},
                            {"heading": "Govern production risk", "text": "Review approvals and audit trails."},
                        ],
                        "evidence": [{"label": "Hero", "text": "Deploy reliable AI agents"}],
                    }
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        project = root / "acme-video"
        env = os.environ.copy()
        env["AUDIOCLAW_CONFIG_PATH"] = str(root / "missing-audioclaw-config.json")
        result = run_cmd(
            "site-video",
            "--site-file",
            str(site_file),
            "--project",
            str(project),
            "--brief",
            "用中文介绍 Acme Cloud 官网。",
            "--duration",
            "8",
            "--fps",
            "12",
            "--offline",
            "--llm",
            "audioclaw",
            "--no-render",
            "--quiet",
            env=env,
        )
        payload = json.loads(result.stdout)
        assert payload["project"] == str(project.resolve())
        assert payload["rendered"] is False
        assert (project / "index.html").exists()
        audio_data = json.loads((project / "assets" / "audio-data.json").read_text(encoding="utf-8"))
        assert audio_data["dry_run"] is True
        assert audio_data["duration"] == 8.0
        report = json.loads((project / "pipeline-report.json").read_text(encoding="utf-8"))
        assert report["pipeline"] == "site-video"
        assert report["warnings"][0]["code"] == "llm_fallback"
        assert "motion-audit" in [step["name"] for step in report["steps"]]
        html = (project / "index.html").read_text(encoding="utf-8")
        assert 'data-audio-source="./assets/audio-data.json"' in html


def test_compose_default_llm_falls_back_when_audioclaw_is_unconfigured() -> None:
    import os
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        project = root / "compose-default-fallback"
        env = os.environ.copy()
        env["AUDIOCLAW_CONFIG_PATH"] = str(root / "missing-audioclaw-config.json")
        env.pop("SENSEAUDIO_API_KEY", None)
        env.pop("AUDIOCLAW_LLM_API_KEY", None)
        env.pop("AUDIOCLAW_LLM_BASE_URL", None)
        env.pop("AUDIOCLAW_LLM_MODEL", None)
        run_cmd(
            "compose",
            "--project",
            str(project),
            "--brief",
            "Introduce SenseAudio sound library with search and voice clone.",
            "--offline",
            env=env,
        )
        meta = json.loads((project / "senseframe.json").read_text(encoding="utf-8"))
        assert meta["llm"] is None
        assert meta["warnings"][0]["code"] == "llm_fallback"
        assert (project / "index.html").exists()


def test_compose_defaults_video_copy_to_chinese() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        project = Path(directory) / "zh-default-demo"
        run_cmd(
            "compose",
            "--project",
            str(project),
            "--brief",
            "Introduce SenseAudio sound library with search and voice clone.",
            "--offline",
        )
        narration = (project / "assets" / "narration.txt").read_text(encoding="utf-8")
        storyboard = json.loads((project / "assets" / "storyboard.json").read_text(encoding="utf-8"))
        assert "音色库" in narration
        assert "声音克隆" in narration
        assert all(any("\u4e00" <= char <= "\u9fff" for char in item["intent"]) for item in storyboard)


def test_compose_website_brief_avoids_hardcoded_voice_library_copy() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        project = Path(directory) / "website-demo"
        run_cmd(
            "compose",
            "--project",
            str(project),
            "--brief",
            "介绍 Anthropic 官网首页，突出 Claude、AI safety、research 和开发者入口。",
            "--offline",
            "--beat-mode",
            "layered",
        )
        html = (project / "index.html").read_text(encoding="utf-8")
        assert "Anthropic" in html
        assert "核心主张" in html or "Claude" in html
        assert 'data-shot="' in html
        assert len(set(re.findall(r'data-shot="([^"]+)"', html))) >= 2
        assert "温柔御姐" not in html
        assert "克隆音色" not in html
        assert "搜索理想声音" not in html
        assert "Beat 01 / SenseAudio" not in html


def test_brand_extract_and_compose_use_brand_profile() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        source = root / "brand.html"
        source.write_text(
            """
            <html><head>
              <title>Acme AI — Helpful research tools</title>
              <meta property="og:site_name" content="Acme AI">
              <meta name="description" content="Acme builds careful AI research tools for teams.">
              <meta property="og:image" content="/social.png">
              <link rel="icon" href="/favicon.svg">
              <link rel="manifest" href="/site.webmanifest">
              <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700">
              <style>:root{--brand:#7c3aed;--accent:#14b8a6}</style>
              <script type="application/ld+json">
                {"@type":"Organization","name":"Acme AI","url":"https://acme.example/","logo":"/mark.svg","sameAs":["https://x.example/acme"]}
              </script>
            </head><body>
              <nav><a>Research</a><a>Products</a><a>Developers</a><a>Security</a></nav>
              <img alt="Acme logo" src="/logo.svg">
            </body></html>
            """,
            encoding="utf-8",
        )
        brand_json = root / "brand.json"
        result = run_cmd("brand-extract", "--url", "https://acme.example/", "--html-file", str(source), "--output", str(brand_json), "--json")
        payload = json.loads(result.stdout)
        assert payload["brand"]["name"] == "Acme AI"
        assert "#7c3aed" in payload["brand"]["colors"]["palette"]
        assert "Research" in payload["brand"]["nav"]
        assert payload["brand"]["logos"][0] == "https://acme.example/mark.svg"
        assert "https://acme.example/favicon.svg" in payload["brand"]["assets"]["icons"]
        assert payload["brand"]["assets"]["manifest"] == "https://acme.example/site.webmanifest"
        assert payload["brand"]["typography"]["primary"] == "Inter"
        assert payload["brand"]["voice"]["category"] in {"research", "developer", "enterprise"}

        project = root / "brand-compose"
        run_cmd(
            "compose",
            "--project",
            str(project),
            "--brief",
            "介绍 Acme AI 官网。",
            "--brand-file",
            str(brand_json),
            "--offline",
            "--beat-mode",
            "layered",
        )
        html = (project / "index.html").read_text(encoding="utf-8")
        meta = json.loads((project / "senseframe.json").read_text(encoding="utf-8"))
        assert 'data-brand-name="Acme AI"' in html
        assert "#7c3aed" in html or "#14b8a6" in html
        assert "Acme AI" in html
        assert "brand-mark logo" in html
        assert meta["brand"]["voice"]["tone"] in {"可信克制", "清晰实用", "稳健专业"}
        assert meta["brand"]["name"] == "Acme AI"
        assert (project / "assets" / "brand.json").exists()


def test_site_ingest_drives_storyboard_with_real_evidence() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        source = root / "site.html"
        source.write_text(
            """
            <html><head>
              <title>Acme Cloud | Reliable AI infrastructure</title>
              <meta property="og:site_name" content="Acme Cloud">
              <meta name="description" content="Acme Cloud helps teams deploy safe AI systems with monitoring and governance.">
              <style>:root{--brand:#2563eb;--accent:#f97316}</style>
            </head><body>
              <header>
                <nav><a>Platform</a><a>Security</a><a>Docs</a></nav>
                <h1>Deploy reliable AI agents</h1>
                <a>Start building</a>
              </header>
              <main>
                <section><h2>Observe every workflow</h2><p>Trace model calls, tool use, latency, and cost in one control plane.</p></section>
                <section><h2>Govern production risk</h2><p>Review policies, approvals, and audit trails before rollout.</p></section>
                <section><h2>Ship with your team</h2><p>Connect documentation, API keys, and deployment environments.</p><button>Book a demo</button></section>
              </main>
            </body></html>
            """,
            encoding="utf-8",
        )
        site_json = root / "site.json"
        result = run_cmd("site-ingest", "--url", "https://acme.example/", "--html-file", str(source), "--output", str(site_json), "--json")
        payload = json.loads(result.stdout)
        assert "Deploy reliable AI agents" in payload["site"]["headings"]
        assert "Book a demo" in payload["site"]["ctas"]
        assert payload["site"]["evidence"]
        payload["site"]["screenshots"] = [
            {
                "id": "site-shot-01",
                "path": "assets/site-screenshots/site-shot-01.png",
                "url": "https://acme.example/",
                "scroll_y": 0,
                "width": 1280,
                "height": 720,
                "scroll_height": 1440,
                "highlight": {"left": 10, "top": 20, "width": 40, "height": 18, "score": 100},
            }
        ]
        site_json.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")

        project = root / "site-compose"
        run_cmd(
            "compose",
            "--project",
            str(project),
            "--brief",
            "介绍 Acme Cloud 官网。",
            "--site-file",
            str(site_json),
            "--offline",
            "--duration",
            "14",
            "--beat-mode",
            "layered",
        )
        html = (project / "index.html").read_text(encoding="utf-8")
        meta = json.loads((project / "senseframe.json").read_text(encoding="utf-8"))
        assert "Deploy reliable AI agents" in html
        assert "Observe every workflow" in html
        assert "Book a demo" in html
        assert "页面重点" in html
        assert "真实证据" not in html
        assert "site-screenshot" in html
        assert "site-scan-highlight" in html
        assert "site-shot-top" in html
        assert "site-shot-ruler" in html
        assert "composition-badge" in html
        assert 'data-site-mode="evidence-clean"' in html
        assert "clean-shot" in html
        assert "evidence-note" in html
        assert 'data-composition-mode="full-bleed"' in html
        assert 'data-camera-path="hero-push"' in html
        assert 'data-site-shot="site-shot-01"' in html
        assert "assets/site-screenshots/site-shot-01.png" in html
        assert "--hl-left:10.0%" in html
        assert meta["site"]["headings"][0] == "Deploy reliable AI agents"
        assert meta["site"]["screenshots"][0]["id"] == "site-shot-01"
        captions = json.loads((project / "assets" / "captions.json").read_text(encoding="utf-8"))["captions"]
        assert captions
        assert max(len(item["text"]) for item in captions) <= 48
        assert (project / "assets" / "site-profile.json").exists()


def test_source_ingest_markdown_outputs_site_profile() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        source = root / "release-notes.md"
        source.write_text(
            """
            # Meridian AI Release Notes

            Meridian AI helps research teams turn notes, PDFs, and meeting records into decisions.

            ## Research workspace

            Collect evidence, summarize uncertainty, and keep citations attached to every claim.

            ## Developer workflow

            Use the API, SDK examples, and GitHub actions to ship internal research automations.

            ## Next step

            Book a demo with the product team.
            """,
            encoding="utf-8",
        )
        output = root / "source-site.json"
        result = run_cmd("source-ingest", "--file", str(source), "--output", str(output), "--json")
        payload = json.loads(result.stdout)
        site = payload["site"]
        assert site["source_type"] == "markdown"
        assert site["title"] == "Meridian AI Release Notes"
        assert "Research workspace" in site["headings"]
        assert "Developer workflow" in site["headings"]
        assert site["sections"][0]["label"] == "Research workspace"
        assert any("Book a demo" in item for item in site["ctas"])
        assert any(item["role"] == "developer" for item in site["semantic_sections"])
        assert output.exists()


def test_source_ingest_text_outputs_profile() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        source = root / "brief.txt"
        source.write_text(
            """Quarterly Launch Notes

The release focuses on developer onboarding, API observability, and workflow governance.

Contact sales for the enterprise rollout plan.
""",
            encoding="utf-8",
        )
        result = run_cmd("source-ingest", "--file", str(source), "--json")
        site = json.loads(result.stdout)["site"]
        assert site["source_type"] == "text"
        assert site["title"] == "Quarterly Launch Notes"
        assert site["summary"].startswith("Quarterly Launch Notes")
        assert any("Contact sales" in item for item in site["ctas"])
        assert site["sections"]


def test_compose_accepts_source_ingest_site_file() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        source = root / "notes.md"
        source.write_text(
            """
            # Atlas DevTools

            Atlas DevTools gives platform teams one place to inspect API latency, trace tool calls, and manage rollout risk.

            ## API observability

            Trace model calls, tools, cost, and failures across environments.

            ## Governance controls

            Review approvals, audit history, and release gates before production rollout.
            """,
            encoding="utf-8",
        )
        source_site = root / "atlas-site.json"
        run_cmd("source-ingest", "--file", str(source), "--output", str(source_site), "--json")
        project = root / "atlas-video"
        run_cmd(
            "compose",
            "--project",
            str(project),
            "--brief",
            "用中文把这份产品说明做成克制的产品短片。",
            "--site-file",
            str(source_site),
            "--offline",
            "--duration",
            "8",
            "--beat-mode",
            "layered",
        )
        html = (project / "index.html").read_text(encoding="utf-8")
        meta = json.loads((project / "senseframe.json").read_text(encoding="utf-8"))
        assert "Atlas DevTools" in html
        assert "API observability" in html
        assert meta["site"]["source_type"] == "markdown"
        assert (project / "assets" / "site-profile.json").exists()


def test_compose_source_ingest_html_uses_published_intro_copy() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        source = root / "readme.md"
        source.write_text(
            """
            # Hyperframes

            Hyperframes turns a GitHub project README into a concise product video with scripted scenes.

            ## Multi source input

            Read Markdown, repository READMEs, and plain text, then extract the product story.

            ## Video assembly

            Build a short introduction with official positioning, capabilities, and next steps.
            """,
            encoding="utf-8",
        )
        source_site = root / "readme-site.json"
        run_cmd("source-ingest", "--file", str(source), "--output", str(source_site), "--json")
        project = root / "readme-video"
        run_cmd(
            "compose",
            "--project",
            str(project),
            "--brief",
            "用中文把这个 GitHub 项目的 README 做成一个简短、清晰的项目介绍视频。",
            "--site-file",
            str(source_site),
            "--offline",
            "--duration",
            "6",
            "--beat-mode",
            "layered",
            "--animation-preset",
            "cinematic",
            "--timeline-engine",
            "gsap-compat",
        )

        html = (project / "index.html").read_text(encoding="utf-8")

        assert "Hyperframes" in html
        assert "Project Brief" in html
        for internal_label in (
            "Website Brief",
            "<strong>hook</strong>",
            "<strong>proof</strong>",
            "界面证据",
            "真实网页证据板",
            "页面线索",
            "使用含义",
            "PAGE SIGNAL",
        ):
            assert internal_label not in html


def test_github_readme_candidates_support_repo_urls() -> None:
    module = load_video_gen_module()

    candidates = module.github_readme_candidates("https://github.com/example/project")

    assert candidates[0] == "https://raw.githubusercontent.com/example/project/main/README.md"
    assert "https://raw.githubusercontent.com/example/project/master/README.md" in candidates
    assert module.parse_github_repo("example/project") == ("example", "project")


def test_site_ingest_classifies_real_material_semantics() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        source = root / "semantic-site.html"
        source.write_text(
            """
            <html><head>
              <title>Acme AI | Safe AI for teams</title>
              <meta property="og:site_name" content="Acme AI">
              <meta name="description" content="Acme AI builds frontier models, developer tools, and enterprise AI safety systems.">
            </head><body>
              <header>
                <nav><a>Claude</a><a>Research</a><a>Safety</a><a>API</a><a>Enterprise</a></nav>
                <h1>Build safe AI with Claude</h1>
                <p>Acme AI helps teams use capable models with rigorous safeguards.</p>
                <a>Start building</a>
              </header>
              <main>
                <section><h2>Claude for every workflow</h2><p>Use a capable assistant for writing, analysis, coding, and knowledge work.</p></section>
                <section><h2>Frontier research</h2><p>Read our latest model research, evaluations, interpretability work, and safety reports.</p></section>
                <section><h2>AI safety built in</h2><p>Govern deployments with policy controls, evals, monitoring, and responsible release practices.</p></section>
                <section><h2>Developer API</h2><p>Build with SDKs, documentation, tool use, batch processing, and low-latency model access.</p></section>
                <section><h2>Enterprise solutions</h2><p>Bring Claude to teams with security, admin controls, compliance, and support.</p><button>Contact sales</button></section>
              </main>
            </body></html>
            """,
            encoding="utf-8",
        )
        site_json = root / "semantic-site.json"
        result = run_cmd(
            "site-ingest",
            "--url",
            "https://acme.example/",
            "--html-file",
            str(source),
            "--output",
            str(site_json),
            "--json",
        )
        payload = json.loads(result.stdout)
        roles = [item["role"] for item in payload["site"]["semantic_sections"]]
        assert roles[:5] == ["hero", "product", "research", "safety", "developer"]
        assert "enterprise" in roles
        assert payload["site"]["primary_roles"][:4] == ["hero", "product", "research", "safety"]
        assert all(item["shot"] for item in payload["site"]["semantic_sections"])
        assert any(item["kind"] == "semantic-section" and item["role"] == "developer" for item in payload["site"]["evidence"])

        project = root / "semantic-compose"
        run_cmd(
            "compose",
            "--project",
            str(project),
            "--brief",
            "介绍 Acme AI 官网。",
            "--site-file",
            str(site_json),
            "--offline",
            "--duration",
            "14",
            "--beat-mode",
            "layered",
        )
        html = (project / "index.html").read_text(encoding="utf-8")
        meta = json.loads((project / "senseframe.json").read_text(encoding="utf-8"))
        assert 'data-material-role="hero"' in html
        assert 'data-material-role="research"' in html
        assert 'data-material-role="safety"' in html
        assert 'data-material-role="developer"' in html
        assert "Frontier research" in html
        assert "Developer API" in html
        assert meta["site"]["primary_roles"][:3] == ["hero", "product", "research"]


def test_fetch_url_text_retries_then_uses_curl_fallback() -> None:
    source = (ROOT / "scripts" / "senseaudio_video_gen.py").read_text(encoding="utf-8")
    assert "for attempt in range" in source
    assert "curl" in source
    assert "fetch_url_text failed after retries" in source


def test_compose_plan_file_compresses_overlong_storyboards() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        project = Path(directory) / "compressed-storyboard"
        plan = Path(directory) / "busy-plan.json"
        plan.write_text(
            json.dumps(
                {
                    "title": "Anthropic 官网介绍",
                    "headline": "安全、研究、Claude",
                    "narration": "介绍 Anthropic 官网首页、Claude、安全研究与开发者能力。",
                    "visual_style": "website explainer",
                    "storyboard": [
                        {"id": f"s{index}", "start": index * 0.6, "end": index * 0.6 + 0.6, "intent": f"网页信息点 {index}"}
                        for index in range(10)
                    ],
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        run_cmd(
            "compose",
            "--project",
            str(project),
            "--brief",
            "介绍 Anthropic 官网",
            "--plan-file",
            str(plan),
            "--duration",
            "12",
            "--offline",
            "--beat-mode",
            "layered",
        )
        storyboard = json.loads((project / "assets/storyboard.json").read_text(encoding="utf-8"))
        assert len(storyboard) <= 5
        assert min(item["end"] - item["start"] for item in storyboard) >= 2.0


def test_compose_can_use_plan_file() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        project = Path(directory) / "llm-compose"
        plan = Path(directory) / "plan.json"
        plan.write_text(
            json.dumps(
                {
                    "title": "音色库介绍",
                    "headline": "智能音色工作台",
                    "narration": "搜索音色，克隆声音，快速完成短视频配音。",
                    "visual_style": "clean product UI",
                    "storyboard": [
                        {"id": "search", "start": 0, "end": 1.5, "intent": "展示搜索"},
                        {"id": "clone", "start": 1.5, "end": 3, "intent": "展示克隆"},
                    ],
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        run_cmd(
            "compose",
            "--project",
            str(project),
            "--brief",
            "demo",
            "--duration",
            "3",
            "--fps",
            "10",
            "--offline",
            "--plan-file",
            str(plan),
        )
        meta = json.loads((project / "senseframe.json").read_text())
        assert meta["title"] == "音色库介绍"
        assert meta["headline"] == "智能音色工作台"
        assert meta["storyboard"][0]["id"] == "search"
        assert (project / "assets" / "llm-plan.json").exists()


def test_compose_uses_storyboard_scene_ids_and_timeline_registry() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        project = Path(directory) / "scene-driven"
        plan = Path(directory) / "plan.json"
        plan.write_text(
            json.dumps(
                {
                    "title": "高级音色工作台",
                    "headline": "搜索、生成、克隆",
                    "narration": "搜索音色，生成旁白，克隆声音。",
                    "visual_style": "premium cinematic product tour",
                    "storyboard": [
                        {"id": "scene1", "start": 0, "end": 1.2, "intent": "品牌开场与极光背景"},
                        {"id": "scene2", "start": 1.2, "end": 2.6, "intent": "搜索框输入并筛选音色"},
                        {"id": "scene3", "start": 2.6, "end": 4.0, "intent": "波形生成与克隆入口"},
                    ],
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        run_cmd(
            "compose",
            "--project",
            str(project),
            "--brief",
            "demo",
            "--duration",
            "4",
            "--fps",
            "10",
            "--offline",
            "--plan-file",
            str(plan),
            "--animation-preset",
            "product-tour",
        )
        html = (project / "index.html").read_text()
        assert 'data-scene="scene1"' in html
        assert 'data-scene="scene2"' in html
        assert 'data-scene="scene3"' in html
        assert 'window.__timelines["main"]' in html
        assert "transition-veil" in html
        assert "audioReactive" in html
        assert "HTML 控制画面：像写网页一样写视频" not in html


def test_compose_can_prepare_generated_assets() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        project = Path(directory) / "gen-compose"
        run_cmd(
            "compose",
            "--project",
            str(project),
            "--brief",
            "demo",
            "--duration",
            "3",
            "--offline",
            "--generate-images",
            "--generate-broll",
            "--asset-dry-run",
        )
        html = (project / "index.html").read_text()
        assert "data-asset=\"hero-image\"" in html
        assert "data-asset=\"broll-video\"" in html
        manifest = json.loads((project / "assets" / "asset-manifest.json").read_text())
        assert manifest["assets"]["hero-image"]["type"] == "image"
        assert manifest["assets"]["hero-image"]["status"] == "planned"
        assert manifest["assets"]["broll-video"]["type"] == "video"
        assert manifest["assets"]["broll-video"]["status"] == "planned"


def test_generate_assets_dry_run_registers_plans() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        project = Path(directory) / "gen-assets"
        run_cmd("init", str(project), "--duration", "3")
        result = run_cmd(
            "generate-assets",
            "--project",
            str(project),
            "--image-prompt",
            "product UI hero image",
            "--video-prompt",
            "soft motion product broll",
            "--dry-run",
        )
        payload = json.loads(result.stdout)
        assert payload["dry_run"] is True
        assert [item["id"] for item in payload["planned_assets"]] == ["hero-image", "broll-video"]
        manifest = json.loads((project / "assets" / "asset-manifest.json").read_text())
        assert manifest["assets"]["hero-image"]["request"]["endpoint"] == "/image/sync"
        assert manifest["assets"]["broll-video"]["request"]["endpoint"] == "/video/create"
        report = json.loads(run_cmd("asset-report", "--project", str(project), "--json").stdout)
        by_id = {item["id"]: item for item in report["assets"]}
        assert by_id["hero-image"]["exists"] is False
        assert by_id["hero-image"]["status"] == "planned"
        assert by_id["broll-video"]["exists"] is False
        assert by_id["broll-video"]["status"] == "planned"


def test_asset_add_binds_data_asset_src() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        project = Path(directory) / "bind-demo"
        run_cmd(
            "compose",
            "--project",
            str(project),
            "--brief",
            "demo",
            "--offline",
            "--generate-images",
            "--asset-dry-run",
        )
        image = project / "assets" / "hero.png"
        image.write_bytes(b"png")
        run_cmd(
            "asset-add",
            "--project",
            str(project),
            "--id",
            "hero-image",
            "--type",
            "image",
            "--path",
            str(image),
            "--role",
            "hero",
        )
        html = (project / "index.html").read_text()
        assert 'data-asset="hero-image" src="assets/hero.png"' in html


def test_captions_from_transcript_and_manifest() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        project = Path(directory) / "captioned"
        run_cmd("init", str(project), "--duration", "3", "--fps", "10")
        transcript = project / "assets" / "transcript.json"
        transcript.write_text(
            json.dumps(
                {
                    "normalized_words": [
                        {"text": "搜索", "start": 0.0, "end": 0.4},
                        {"text": "音色", "start": 0.4, "end": 0.8},
                        {"text": "生成", "start": 1.1, "end": 1.5},
                    ]
                }
            ),
            encoding="utf-8",
        )
        captions = project / "assets" / "captions.json"
        result = run_cmd(
            "captions",
            "--project",
            str(project),
            "--transcript",
            str(transcript),
            "--output",
            str(captions),
            "--max-gap",
            "0.25",
        )
        payload = json.loads(captions.read_text())
        assert result.stdout.strip() == str(captions)
        assert [item["text"] for item in payload["captions"]] == ["搜索音色", "生成"]
        manifest = json.loads((project / "assets" / "asset-manifest.json").read_text())
        assert manifest["assets"]["captions"]["path"] == "assets/captions.json"


def test_captions_can_include_word_highlights() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        project = Path(directory) / "word-captioned"
        run_cmd("init", str(project), "--duration", "3", "--fps", "10")
        transcript = project / "assets" / "transcript.json"
        transcript.write_text(
            json.dumps(
                {
                    "normalized_words": [
                        {"text": "搜索", "start": 0.0, "end": 0.4},
                        {"text": "音色", "start": 0.4, "end": 0.8},
                    ]
                }
            ),
            encoding="utf-8",
        )
        captions = project / "assets" / "captions.json"
        run_cmd(
            "captions",
            "--project",
            str(project),
            "--transcript",
            str(transcript),
            "--output",
            str(captions),
            "--include-words",
        )
        payload = json.loads(captions.read_text())
        assert payload["captions"][0]["words"][0]["text"] == "搜索"
        assert payload["captions"][0]["words"][1]["start"] == 0.4


def test_runtime_adds_kinetic_caption_word_state() -> None:
    runtime = (ROOT / "scripts" / "senseaudio_video_gen.py").read_text()
    assert "sf-word-emphasis" in runtime
    assert "dataset.sfEmphasis" in runtime
    assert "scale(" in runtime


def test_timeline_command_registers_timeline() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        project = Path(directory) / "timed"
        run_cmd("compose", "--project", str(project), "--brief", "demo", "--duration", "6", "--offline")
        result = run_cmd("timeline", "--project", str(project), "--preset", "cinematic")
        timeline = project / "assets" / "timeline.json"
        payload = json.loads(timeline.read_text())
        assert result.stdout.strip() == str(timeline)
        assert payload["preset"] == "cinematic"
        assert payload["items"][0]["effect"]
        html = (project / "index.html").read_text()
        assert 'data-timeline-source="./assets/timeline.json"' in html
        manifest = json.loads((project / "assets" / "asset-manifest.json").read_text())
        assert manifest["assets"]["timeline"]["path"] == "assets/timeline.json"


def test_timeline_transition_preset_writes_transition_dsl() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        project = Path(directory) / "transitioned"
        run_cmd("compose", "--project", str(project), "--brief", "demo", "--duration", "6", "--offline")
        run_cmd("timeline", "--project", str(project), "--preset", "cinematic", "--transition-preset", "editorial")
        payload = json.loads((project / "assets" / "timeline.json").read_text())
        assert payload["transition_preset"] == "editorial"
        assert payload["transitions"]
        assert payload["transitions"][0]["kind"] in {"ribbon-wipe", "glass-flash", "iris-focus", "luma-sweep"}
        assert payload["transitions"][0]["at"] == payload["items"][0]["end"]


def test_timeline_gsap_compat_writes_tracks_and_labels() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        project = Path(directory) / "gsap-timed"
        run_cmd("compose", "--project", str(project), "--brief", "demo", "--duration", "6", "--offline")
        run_cmd(
            "timeline",
            "--project",
            str(project),
            "--preset",
            "cinematic",
            "--timeline-engine",
            "gsap-compat",
        )
        payload = json.loads((project / "assets" / "timeline.json").read_text())
        assert payload["engine"] == "gsap-compat"
        assert payload["labels"]
        assert payload["tracks"]
        assert payload["tracks"][0]["method"] in {"set", "to", "fromTo"}
        assert payload["tracks"][0]["selector"].startswith("[data-scene=")


def test_compose_animation_preset_adds_effects() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        project = Path(directory) / "animated"
        run_cmd(
            "compose",
            "--project",
            str(project),
            "--brief",
            "demo",
            "--duration",
            "4",
            "--offline",
            "--animation-preset",
            "cinematic",
        )
        html = (project / "index.html").read_text()
        assert 'data-timeline-source="./assets/timeline.json"' in html
        assert "camera-layer" in html
        assert "focus-ring" in html
        assert ".sf-word[data-sf-active=\"true\"]" in html
        assert (project / "assets" / "timeline.json").exists()


def test_compose_transition_preset_marks_runtime() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        project = Path(directory) / "preset-motion"
        run_cmd(
            "compose",
            "--project",
            str(project),
            "--brief",
            "demo",
            "--duration",
            "4",
            "--offline",
            "--animation-preset",
            "cinematic",
            "--transition-preset",
            "editorial",
        )
        html = (project / "index.html").read_text()
        timeline = json.loads((project / "assets" / "timeline.json").read_text())
        assert 'data-transition-layer="editorial"' in html
        assert "transitionPlan" in html
        assert "applyTransitionPreset" in html
        assert timeline["transition_preset"] == "editorial"
        assert len(timeline["transitions"]) >= 1


def test_compose_gsap_compat_embeds_local_adapter() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        project = Path(directory) / "gsap-compose"
        run_cmd(
            "compose",
            "--project",
            str(project),
            "--brief",
            "demo",
            "--duration",
            "4",
            "--offline",
            "--animation-preset",
            "cinematic",
            "--timeline-engine",
            "gsap-compat",
        )
        html = (project / "index.html").read_text()
        timeline = json.loads((project / "assets" / "timeline.json").read_text())
        assert "createGsapCompatTimeline" in html
        assert "window.__senseframes.gsapCompat" in html
        assert "gsapCompat.seek(time)" in html
        assert timeline["engine"] == "gsap-compat"
        assert timeline["tracks"]


def test_motion_audit_reports_scene_timeline_alignment() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        project = Path(directory) / "audit-demo"
        run_cmd(
            "compose",
            "--project",
            str(project),
            "--brief",
            "demo",
            "--duration",
            "4",
            "--offline",
            "--animation-preset",
            "cinematic",
        )
        result = run_cmd("motion-audit", "--project", str(project), "--json")
        payload = json.loads(result.stdout)
        assert payload["ok"] is True
        assert payload["stats"]["storyboard_scenes"] == payload["stats"]["dom_scenes"]
        assert payload["checks"]["timeline_registry"] is True
        assert payload["checks"]["storyboard_scene_binding"] is True
        assert payload["checks"]["transition_layer"] is True


def test_motion_map_reports_density_dead_zones_and_recommendations() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        project = Path(directory) / "map-demo"
        run_cmd(
            "compose",
            "--project",
            str(project),
            "--brief",
            "demo",
            "--duration",
            "4",
            "--offline",
            "--animation-preset",
            "cinematic",
        )
        result = run_cmd("motion-map", "--project", str(project), "--json", "--samples", "8")
        payload = json.loads(result.stdout)
        assert payload["ok"] is True
        assert payload["density"]["samples"] == 8
        assert payload["scene_coverage"][0]["scene_id"]
        assert "dead_zones" in payload
        assert "recommendations" in payload
        assert payload["checks"]["scene_coverage"] is True


def test_motion_map_reports_beat_coverage() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        project = Path(directory) / "beat-map"
        run_cmd(
            "compose",
            "--project",
            str(project),
            "--brief",
            "demo",
            "--duration",
            "6",
            "--offline",
            "--beat-mode",
            "layered",
            "--animation-preset",
            "cinematic",
        )
        result = run_cmd("motion-map", "--project", str(project), "--json", "--samples", "18")
        payload = json.loads(result.stdout)
        assert payload["ok"] is True
        assert payload["checks"]["beat_coverage"] is True
        assert payload["beat_coverage"]["total"] >= 6
        assert payload["beat_coverage"]["sampled"] >= 6
        assert payload["checks"]["comfortable_pacing"] is True
        assert payload["flashiness"]["comfortable"] is True


def test_audio_data_dry_run_registers_reactive_asset() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        project = Path(directory) / "audio-reactive"
        run_cmd("compose", "--project", str(project), "--brief", "demo", "--duration", "3", "--offline")
        audio = project / "assets" / "narration.mp3"
        audio.write_bytes(b"not-real-audio")
        result = run_cmd(
            "audio-data",
            "--project",
            str(project),
            "--audio",
            str(audio),
            "--output",
            str(project / "assets" / "audio-data.json"),
            "--fps",
            "12",
            "--dry-run",
        )
        payload = json.loads(result.stdout)
        assert payload["dry_run"] is True
        assert payload["payload"]["fps"] == 12
        manifest = json.loads((project / "assets" / "asset-manifest.json").read_text())
        assert manifest["assets"]["audio-data"]["type"] == "json"


def test_audio_reactivity_does_not_drive_global_camera_transform() -> None:
    script = (ROOT / "scripts" / "senseaudio_video_gen.py").read_text()
    camera_lines = [line for line in script.splitlines() if "setStyle(camera" in line]
    assert camera_lines
    assert all("audio." not in line for line in camera_lines)


def test_render_help_exposes_resume_parallel() -> None:
    result = run_cmd("render", "--help")
    assert "--resume" in result.stdout
    assert "--parallel" in result.stdout
    assert "--capture-mode" in result.stdout
    assert "--frame-dir" in result.stdout
    assert "--keep-frames" in result.stdout


def test_render_auto_uses_registered_narration_audio() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        project = Path(directory) / "auto-audio"
        run_cmd("init", str(project), "--duration", "1")
        asset = project / "assets" / "narration.mp3"
        asset.write_bytes(b"demo")
        run_cmd("asset-add", "--project", str(project), "--id", "narration", "--type", "audio", "--path", str(asset))
        script = (ROOT / "scripts" / "senseaudio_video_gen.py").read_text()
        assert "default_render_audio" in script
        assert "auto_audio" in script
        assert "apad=pad_dur=" in script


def test_compose_plan_file_uses_semantic_story_evidence() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        site = root / "semantic-site.json"
        site.write_text(
            json.dumps(
                {
                    "site": {
                        "source_url": "https://acme.example/",
                        "brand_name": "Acme AI",
                        "title": "Acme AI",
                        "summary": "Safe AI products for teams.",
                        "semantic_sections": [
                            {"kind": "semantic-section", "role": "hero", "label": "Hero", "text": "Safe AI", "shot": "hero-overview", "composition": "full-bleed", "camera": "hero-push"},
                            {"kind": "semantic-section", "role": "product", "label": "Product", "text": "Claude workflows", "shot": "feature-zoom", "composition": "zoom-callout", "camera": "macro-zoom"},
                            {"kind": "semantic-section", "role": "research", "label": "Research", "text": "Research reports", "shot": "trust-message", "composition": "evidence-board", "camera": "board-orbit"},
                            {"kind": "semantic-section", "role": "safety", "label": "Safety", "text": "Safety policy", "shot": "trust-message", "composition": "evidence-board", "camera": "board-orbit"},
                            {"kind": "semantic-section", "role": "enterprise", "label": "Enterprise", "text": "Team solutions", "shot": "feature-zoom", "composition": "zoom-callout", "camera": "macro-zoom"},
                        ],
                        "evidence": [],
                    }
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        plan = root / "plan.json"
        plan.write_text(
            json.dumps(
                {
                    "title": "Acme AI",
                    "headline": "官网介绍",
                    "narration": "介绍 Acme AI 的产品、研究、安全与企业能力。",
                    "storyboard": [
                        {"id": f"s{i}", "start": i * 2, "end": i * 2 + 2, "intent": f"镜头 {i}"}
                        for i in range(5)
                    ],
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        project = root / "semantic-plan"
        run_cmd(
            "compose",
            "--project",
            str(project),
            "--brief",
            "介绍 Acme AI",
            "--site-file",
            str(site),
            "--plan-file",
            str(plan),
            "--duration",
            "10",
            "--offline",
        )
        html = (project / "index.html").read_text(encoding="utf-8")
        assert re.findall(r'data-material-role="([^"]+)"', html) == ["hero", "product", "research", "safety", "enterprise"]


def test_site_narration_uses_polished_chinese_script() -> None:
    script = (ROOT / "scripts" / "senseaudio_video_gen.py").read_text()
    assert "这支视频快速看" in script
    assert "整个介绍只基于官网截图和页面文本" in script
    assert "mostly_latin_text" in script


def test_editorial_pro_preset_and_site_mode_exist() -> None:
    result = run_cmd("styles", "--json")
    payload = json.loads(result.stdout)
    assert "editorial-pro" in payload["presets"]
    script = (ROOT / "scripts" / "senseaudio_video_gen.py").read_text()
    assert 'style_preset_name == "editorial-pro"' in script
    assert '[data-site-mode="editorial-pro"]' in script


def test_site_vision_audit_dry_run_builds_openrouter_payload() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        project = Path(directory) / "vision-audit"
        run_cmd("init", str(project))
        inspect_dir = project / "renders" / "inspect"
        inspect_dir.mkdir(parents=True)
        frame = inspect_dir / "sample_00.png"
        frame.write_bytes(base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAFgwJ/l6h8MgAAAABJRU5ErkJggg=="))
        result = run_cmd("site-vision-audit", "--project", str(project), "--dry-run", "--json")
        payload = json.loads(result.stdout)
        assert payload["dry_run"] is True
        assert payload["provider"] == "openrouter"
        assert payload["model"]
        assert payload["images"]
        assert payload["payload"]["messages"][0]["content"]


def test_site_vision_plan_heuristic_writes_crop_plan() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        site = root / "site.json"
        site.write_text(
            json.dumps(
                {
                    "site": {
                        "source_url": "https://acme.example/",
                        "semantic_sections": [
                            {"role": "hero", "label": "Hero", "text": "Hero copy", "shot": "hero-overview"},
                            {"role": "developer", "label": "API", "text": "Developer docs", "shot": "feature-zoom"},
                        ],
                        "story_evidence": [
                            {"role": "hero", "label": "Hero", "text": "Hero copy"},
                            {"role": "developer", "label": "API", "text": "Developer docs"},
                        ],
                        "screenshots": [
                            {"id": "site-shot-01", "path": "assets/site-screenshots/site-shot-01.png", "highlight": {"left": 8, "top": 12, "width": 42, "height": 22}},
                            {"id": "site-shot-02", "path": "assets/site-screenshots/site-shot-02.png", "highlight": {"left": 46, "top": 36, "width": 28, "height": 20}},
                        ],
                    }
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        result = run_cmd("site-vision-plan", "--site-file", str(site), "--json")
        payload = json.loads(result.stdout)
        assert payload["provider"] == "heuristic"
        assert len(payload["visual_plan"]) == 2
        assert payload["visual_plan"][0]["role"] == "hero"
        assert payload["visual_plan"][1]["role"] == "developer"
        assert payload["visual_plan"][1]["crop"]["zoom"] > payload["visual_plan"][0]["crop"]["zoom"]
        assert payload["visual_plan"][1]["screenshot_id"] == "site-shot-02"


def test_compose_uses_visual_plan_crop_variables() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        project = root / "project"
        shot_dir = project / "assets" / "site-screenshots"
        shot_dir.mkdir(parents=True)
        (shot_dir / "site-shot-01.png").write_bytes(base64.b64decode("iVBORw0KGgo="))
        site = root / "site.json"
        site.write_text(
            json.dumps(
                {
                    "site": {
                        "source_url": "https://acme.example/",
                        "brand_name": "Acme",
                        "title": "Acme",
                        "summary": "Acme product site.",
                        "semantic_sections": [
                            {"role": "developer", "label": "Developer API", "text": "Build with SDKs.", "shot": "feature-zoom", "composition": "zoom-callout", "camera": "macro-zoom"}
                        ],
                        "story_evidence": [
                            {"role": "developer", "label": "Developer API", "text": "Build with SDKs.", "shot": "feature-zoom", "composition": "zoom-callout", "camera": "macro-zoom"}
                        ],
                        "screenshots": [
                            {
                                "id": "site-shot-01",
                                "path": "assets/site-screenshots/site-shot-01.png",
                                "highlight": {"left": 46, "top": 36, "width": 28, "height": 20},
                            }
                        ],
                    }
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        run_cmd(
            "compose",
            "--project",
            str(project),
            "--brief",
            "介绍 Acme 官网。",
            "--site-file",
            str(site),
            "--duration",
            "4",
            "--offline",
        )
        html = (project / "index.html").read_text(encoding="utf-8")
        profile = json.loads((project / "assets" / "site-profile.json").read_text(encoding="utf-8"))["site"]
        assert profile["visual_plan"][0]["role"] == "developer"
        assert 'data-visual-plan="heuristic"' in html
        assert "--crop-x:" in html
        assert "--crop-zoom:" in html


def test_asset_add_updates_project_manifest() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        project = Path(directory) / "assets-demo"
        run_cmd("init", str(project))
        asset = project / "assets" / "voice.mp3"
        asset.write_bytes(b"demo")
        run_cmd(
            "asset-add",
            "--project",
            str(project),
            "--id",
            "narration",
            "--type",
            "audio",
            "--path",
            str(asset),
            "--role",
            "voiceover",
        )
        manifest = json.loads((project / "assets" / "asset-manifest.json").read_text())
        assert manifest["assets"]["narration"]["type"] == "audio"
        assert manifest["assets"]["narration"]["path"] == "assets/voice.mp3"


def test_lint_reports_missing_caption_file() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        project = Path(directory) / "lint-demo"
        run_cmd("init", str(project), "--duration", "3")
        html = (project / "index.html").read_text()
        html = html.replace("</body>", '<div data-caption-source="./assets/missing.json"></div></body>')
        (project / "index.html").write_text(html, encoding="utf-8")
        result = run_cmd("lint", "--project", str(project), "--json")
        payload = json.loads(result.stdout)
        assert payload["ok"] is False
        assert any("missing.json" in issue["message"] for issue in payload["issues"])


def test_lint_warns_when_narration_has_no_audio_asset() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        project = Path(directory) / "silent-demo"
        run_cmd("compose", "--project", str(project), "--brief", "Introduce a product page.", "--offline")
        result = run_cmd("lint", "--project", str(project), "--json")
        payload = json.loads(result.stdout)
        assert payload["ok"] is True
        assert any(warning["code"] == "missing_audio_track" for warning in payload["warnings"])


def test_captions_export_srt_and_vtt() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        captions = Path(directory) / "captions.json"
        captions.write_text(
            json.dumps(
                {
                    "captions": [
                        {"text": "搜索音色", "start": 0.0, "end": 1.2},
                        {"text": "生成视频", "start": 1.4, "end": 2.0},
                    ]
                }
            ),
            encoding="utf-8",
        )
        srt = Path(directory) / "captions.srt"
        vtt = Path(directory) / "captions.vtt"
        run_cmd("captions-export", "--captions", str(captions), "--format", "srt", "--output", str(srt))
        run_cmd("captions-export", "--captions", str(captions), "--format", "vtt", "--output", str(vtt))
        assert "00:00:00,000 --> 00:00:01,200" in srt.read_text()
        assert vtt.read_text().startswith("WEBVTT")


def test_asset_report_lists_assets() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        project = Path(directory) / "report-demo"
        run_cmd("init", str(project))
        asset = project / "assets" / "voice.mp3"
        asset.write_bytes(b"demo")
        run_cmd("asset-add", "--project", str(project), "--id", "narration", "--type", "audio", "--path", str(asset))
        result = run_cmd("asset-report", "--project", str(project), "--json")
        payload = json.loads(result.stdout)
        assert payload["count"] == 1
        assert payload["assets"][0]["id"] == "narration"
        assert payload["assets"][0]["exists"] is True


def test_build_dry_run_plans_local_pipeline() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        project = Path(directory) / "build-demo"
        run_cmd("init", str(project), "--duration", "2")
        narration = project / "assets" / "narration.mp3"
        narration.write_bytes(b"audio")
        transcript = project / "assets" / "transcript.json"
        transcript.write_text(json.dumps({"text": "hello"}), encoding="utf-8")
        run_cmd("asset-add", "--project", str(project), "--id", "narration", "--type", "audio", "--path", str(narration))
        run_cmd("asset-add", "--project", str(project), "--id", "transcript", "--type", "transcript", "--path", str(transcript))
        result = run_cmd("build", "--project", str(project), "--dry-run")
        payload = json.loads(result.stdout)
        assert [step["name"] for step in payload["steps"]] == ["lint", "captions", "render"]
        assert payload["audio"] == "assets/narration.mp3"


def run_legacy_tests() -> None:
    test_help()
    test_init_project()
    test_video_dry_run()
    test_tts_dry_run()
    test_styles_command_lists_registry()
    test_compose_offline_project()
    test_compose_style_preset_applies_tokens_and_metadata()
    test_beats_command_writes_scene_beats()
    test_compose_beat_mode_layered_writes_beats_html_and_tracks()
    test_llm_plan_dry_run_targets_deepseek()
    test_llm_plan_dry_run_targets_audioclaw_config()
    test_llm_plan_dry_run_targets_openrouter()
    test_site_video_dry_run_plans_hyperframes_style_pipeline()
    test_site_video_dry_run_can_plan_cookie_backed_capture()
    test_site_video_offline_no_render_writes_project_audio_data_and_report()
    test_compose_defaults_video_copy_to_chinese()
    test_compose_website_brief_avoids_hardcoded_voice_library_copy()
    test_brand_extract_and_compose_use_brand_profile()
    test_site_ingest_drives_storyboard_with_real_evidence()
    test_site_ingest_classifies_real_material_semantics()
    test_fetch_url_text_retries_then_uses_curl_fallback()
    test_compose_plan_file_compresses_overlong_storyboards()
    test_compose_can_use_plan_file()
    test_compose_uses_storyboard_scene_ids_and_timeline_registry()
    test_compose_can_prepare_generated_assets()
    test_generate_assets_dry_run_registers_plans()
    test_asset_add_binds_data_asset_src()
    test_captions_from_transcript_and_manifest()
    test_captions_can_include_word_highlights()
    test_runtime_adds_kinetic_caption_word_state()
    test_timeline_command_registers_timeline()
    test_timeline_transition_preset_writes_transition_dsl()
    test_timeline_gsap_compat_writes_tracks_and_labels()
    test_compose_animation_preset_adds_effects()
    test_compose_transition_preset_marks_runtime()
    test_compose_gsap_compat_embeds_local_adapter()
    test_motion_audit_reports_scene_timeline_alignment()
    test_motion_map_reports_density_dead_zones_and_recommendations()
    test_motion_map_reports_beat_coverage()
    test_audio_data_dry_run_registers_reactive_asset()
    test_audio_reactivity_does_not_drive_global_camera_transform()
    test_render_help_exposes_resume_parallel()
    test_render_auto_uses_registered_narration_audio()
    test_compose_plan_file_uses_semantic_story_evidence()
    test_site_narration_uses_polished_chinese_script()
    test_editorial_pro_preset_and_site_mode_exist()
    test_site_vision_audit_dry_run_builds_openrouter_payload()
    test_site_vision_plan_heuristic_writes_crop_plan()
    test_browser_cookie_loader_accepts_storage_state_json()
    test_frame_quality_flags_internal_copy_leaks()
    test_compose_uses_visual_plan_crop_variables()
    test_asset_add_updates_project_manifest()
    test_lint_reports_missing_caption_file()
    test_lint_warns_when_narration_has_no_audio_asset()
    test_captions_export_srt_and_vtt()
    test_asset_report_lists_assets()
    test_build_dry_run_plans_local_pipeline()
    print("ok")


def test_music_create_dry_run_builds_song_payload() -> None:
    result = run_cmd(
        "music-create",
        "--prompt",
        "warm minimal corporate background music",
        "--style",
        "ambient cinematic, subtle pulse",
        "--title",
        "Brand Bed",
        "--duration",
        "16",
        "--instrumental",
        "--dry-run",
    )
    payload = json.loads(result.stdout)
    assert payload["endpoint"] == "/music/song/create"
    assert payload["payload"]["model"]
    assert payload["payload"]["lyrics"] == "[intro-medium] ; [inst-medium] ; [outro-short]"
    assert payload["payload"]["style"] == "ambient"
    assert payload["payload"]["style_weight"] == 0.72
    assert payload["payload"]["title"] == "Brand Bed"
    assert payload["payload"]["instrumental"] is True
    assert "custom_mode" not in payload["payload"]
    assert "callback_url" not in payload["payload"]
    assert "reference_id" not in payload["payload"]
    assert "use_variance" not in payload["payload"]


def test_music_status_dry_run_targets_pending_endpoint() -> None:
    result = run_cmd("music-status", "--id", "song_123", "--dry-run")
    payload = json.loads(result.stdout)
    assert payload["endpoint"] == "/music/song/pending/song_123"
    assert payload["poll"] is False


def test_music_failure_summary_handles_empty_failed_status() -> None:
    module = load_video_gen_module()
    summary = module.music_failure_summary({"task_id": "song_123", "response": {"data": []}, "status": "FAILED"})
    assert "failed" in summary
    assert "without a detailed error message" in summary


def test_music_download_url_reads_official_status_response() -> None:
    module = load_video_gen_module()
    payload = {
        "task_id": "song_123",
        "status": "SUCCESS",
        "response": {
            "task_id": "song_123",
            "data": [
                {
                    "audio_url": "https://example.com/generated-song.mp3",
                    "cover_url": "https://example.com/cover.png",
                    "duration": 110,
                }
            ],
        },
    }
    assert module.first_music_download_url(payload) == "https://example.com/generated-song.mp3"


def test_request_json_retries_local_senseaudio_key_after_env_401() -> None:
    import io
    import os

    module = load_video_gen_module()
    original_urlopen = module.urllib.request.urlopen
    original_local_credential = module.local_senseaudio_credential
    original_env_key = os.environ.get("SENSEAUDIO_API_KEY")
    calls: list[str] = []

    class FakeResponse:
        headers = {"Content-Type": "application/json"}

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def read(self) -> bytes:
            return b'{"task_id":"music_ok"}'

    def fake_urlopen(req, timeout=120):
        auth = req.get_header("Authorization") or ""
        calls.append(auth)
        if auth == "Bearer bad-env-key":
            raise module.urllib.error.HTTPError(
                req.full_url,
                401,
                "Unauthorized",
                {},
                io.BytesIO(b'{"code":"authentication_error","message":"incorrect API key provided"}'),
            )
        return FakeResponse()

    try:
        os.environ["SENSEAUDIO_API_KEY"] = "bad-env-key"
        module.local_senseaudio_credential = lambda name: "good-local-key" if name == "SENSEAUDIO_API_KEY" else ""
        module.urllib.request.urlopen = fake_urlopen
        result = module.request_json("POST", "/music/song/create", {"model": module.DEFAULT_MUSIC_MODEL, "lyrics": "bed"})
    finally:
        module.urllib.request.urlopen = original_urlopen
        module.local_senseaudio_credential = original_local_credential
        if original_env_key is None:
            os.environ.pop("SENSEAUDIO_API_KEY", None)
        else:
            os.environ["SENSEAUDIO_API_KEY"] = original_env_key

    assert result["task_id"] == "music_ok"
    assert calls == ["Bearer bad-env-key", "Bearer good-local-key"]


def test_music_create_writes_timeout_manifest_before_raising() -> None:
    import argparse
    import tempfile

    module = load_video_gen_module()
    with tempfile.TemporaryDirectory() as directory:
        project = Path(directory) / "music-timeout"
        (project / "assets").mkdir(parents=True)
        manifest = project / "assets" / "music-task.json"
        original_request_json = module.request_json
        original_poll_music = module.poll_music
        original_register_asset = module.register_asset
        module.request_json = lambda method, endpoint, payload=None, query=None: {"task_id": "music_timeout_1"}
        module.poll_music = lambda task_id, interval, timeout: (_ for _ in ()).throw(module.SenseAudioError("Timed out waiting for music task: music_timeout_1"))
        module.register_asset = lambda *args, **kwargs: None
        try:
            args = argparse.Namespace(
                prompt="short instrumental bed",
                lyrics=None,
                style="ambient",
                title="Bed",
                duration=8,
                negative_tags="vocals",
                instrumental=True,
                callback_url=None,
                reference_id=None,
                vocal_id=None,
                use_variance=False,
                model="senseaudio-music-1.0-260319",
                poll=True,
                interval=1,
                timeout=1,
                download=None,
                manifest=str(manifest),
                project=str(project),
                asset_id="background-music",
                dry_run=False,
            )
            try:
                module.command_music_create(args)
                raise AssertionError("command_music_create should raise on poll timeout")
            except module.SenseAudioError:
                pass
        finally:
            module.request_json = original_request_json
            module.poll_music = original_poll_music
            module.register_asset = original_register_asset
        payload = json.loads(manifest.read_text())
        assert payload["create_response"]["task_id"] == "music_timeout_1"
        assert payload["status_response"]["status"] == "timeouted"
        assert "Timed out waiting" in payload["failure_summary"]


def test_mix_audio_dry_run_plans_voice_and_music() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        project = Path(directory) / "mix-demo"
        run_cmd("init", str(project), "--duration", "8")
        voice = project / "assets" / "narration.mp3"
        music = project / "assets" / "music.mp3"
        voice.write_bytes(b"voice")
        music.write_bytes(b"music")
        result = run_cmd(
            "mix-audio",
            "--project",
            str(project),
            "--voice",
            str(voice),
            "--music",
            str(music),
            "--output",
            str(project / "assets" / "final-audio.m4a"),
            "--duration",
            "8",
            "--music-volume",
            "0.18",
            "--dry-run",
            "--json",
        )
        payload = json.loads(result.stdout)
        assert payload["dry_run"] is True
        assert payload["output"].endswith("assets/final-audio.m4a")
        assert "amix" in " ".join(payload["ffmpeg"])
        assert "volume=0.18" in " ".join(payload["ffmpeg"])


def test_procedural_music_command_builds_ambient_bed() -> None:
    module = load_video_gen_module()
    output = Path("background-music.mp3")
    command = module.build_procedural_music_command("/usr/bin/ffmpeg", output, 18.0)
    joined = " ".join(command)
    assert command[0] == "/usr/bin/ffmpeg"
    assert "sine=frequency=220" in joined
    assert "anoisesrc" in joined
    assert "afade=t=out" in joined
    assert command[-1] == str(output)


def test_render_auto_prefers_registered_final_audio() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        project = Path(directory) / "auto-final-audio"
        run_cmd("init", str(project), "--duration", "1")
        narration = project / "assets" / "narration.mp3"
        final_audio = project / "assets" / "final-audio.m4a"
        narration.write_bytes(b"voice")
        final_audio.write_bytes(b"mix")
        run_cmd("asset-add", "--project", str(project), "--id", "narration", "--type", "audio", "--path", str(narration))
        run_cmd("asset-add", "--project", str(project), "--id", "final-audio", "--type", "audio", "--path", str(final_audio))
        result = run_cmd("build", "--project", str(project), "--dry-run")
        payload = json.loads(result.stdout)
        assert payload["audio"] == "assets/final-audio.m4a"
        assert payload["steps"][-1]["audio"] == "assets/final-audio.m4a"


def test_repair_dry_run_plans_second_pass_from_vision_audit() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        project = Path(directory) / "repair-demo"
        run_cmd("compose", "--project", str(project), "--brief", "demo", "--duration", "6", "--offline", "--beat-mode", "layered")
        audit = project / "assets" / "vision-audit.json"
        audit.write_text(
            json.dumps(
                {
                    "safe_to_render": False,
                    "issues": [{"severity": "high", "problem": "Screenshot crop misses the real hero content and text feels cluttered."}],
                }
            ),
            encoding="utf-8",
        )
        result = run_cmd("repair", "--project", str(project), "--dry-run", "--json")
        payload = json.loads(result.stdout)
        assert payload["dry_run"] is True
        assert payload["repair_pass"] == 1
        assert "tighten-visual-evidence" in payload["actions"]
        assert "stabilize-motion" in payload["actions"]


def test_repair_apply_writes_plan_and_marks_html() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        project = Path(directory) / "repair-apply"
        run_cmd("compose", "--project", str(project), "--brief", "demo", "--duration", "6", "--offline", "--beat-mode", "layered")
        result = run_cmd("repair", "--project", str(project), "--json")
        payload = json.loads(result.stdout)
        assert payload["repair_pass"] == 1
        assert (project / "assets" / "repair-plan.json").exists()
        html = (project / "index.html").read_text()
        assert 'data-repair-pass="1"' in html
        assert 'data-repair-profile="stabilized"' in html
        meta = json.loads((project / "senseframe.json").read_text())
        assert meta["repair_pass"] == 1


def test_site_video_dry_run_includes_music_and_auto_repair_steps() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        project = Path(directory) / "site-video"
        result = run_cmd(
            "site-video",
            "--url",
            "https://example.com",
            "--project",
            str(project),
            "--duration",
            "14",
            "--music",
            "--auto-repair",
            "--dry-run",
        )
        payload = json.loads(result.stdout)
        step_names = [step["name"] for step in payload["steps"]]
        assert "music-create" in step_names
        assert "mix-audio" in step_names
        assert "repair" in step_names
        assert "render-repair" in step_names


def test_site_visible_copy_hides_director_notes_from_llm_plan() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        project = root / "director-note-filter"
        site = root / "site.json"
        site.write_text(
            json.dumps(
                {
                    "site": {
                        "source_url": "https://example.com/",
                        "brand_name": "Acme Research",
                        "title": "Acme Research",
                        "summary": "面向团队的可靠研究平台。",
                        "headings": ["Research tools", "Team workflows", "Security"],
                        "ctas": ["Get started"],
                        "evidence": [
                            {"kind": "heading", "role": "hero", "label": "Research tools", "text": "面向团队的可靠研究平台。"},
                            {"kind": "heading", "role": "product", "label": "Team workflows", "text": "团队可以围绕研究材料协作。"},
                            {"kind": "cta", "role": "cta", "label": "Get started", "text": "开始使用。"},
                        ],
                    }
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        plan = root / "plan.json"
        plan.write_text(
            json.dumps(
                {
                    "title": "Acme Research",
                    "headline": "可靠研究平台",
                    "narration": "这支视频介绍 Acme Research 的真实网页内容。它展示研究工具、团队流程和开始使用入口。",
                    "storyboard": [
                        {"id": "s1", "start": 0, "end": 3, "intent": "开篇展示页面文字内容是怎么排版，镜头从左向右移动。"},
                        {"id": "s2", "start": 3, "end": 6, "intent": "镜头平滑滑动到产品模块，说明这里怎么排版。"},
                        {"id": "s3", "start": 6, "end": 9, "intent": "定格 CTA 区域，展示按钮怎么排版。"},
                    ],
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        run_cmd(
            "compose",
            "--project",
            str(project),
            "--brief",
            "介绍 Acme Research 官网",
            "--site-file",
            str(site),
            "--plan-file",
            str(plan),
            "--duration",
            "9",
            "--offline",
            "--beat-mode",
            "layered",
        )
        html = (project / "index.html").read_text()
        assert "Research tools" in html
        assert "开篇展示" not in html
        assert "镜头平滑" not in html
        assert "怎么排版" not in html


def test_site_content_brief_enriches_english_product_pages() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        project = root / "english-product"
        site = root / "site.json"
        site.write_text(
            json.dumps(
                {
                    "site": {
                        "source_url": "https://example.com/claude-code",
                        "brand_name": "Claude Code",
                        "title": "Claude Code",
                        "summary": "An AI coding agent that works in your terminal and IDE.",
                        "headings": ["Build in your terminal", "Connect GitHub and GitLab", "Run commands and edit files"],
                        "ctas": ["Read the docs"],
                        "semantic_sections": [
                            {"kind": "semantic-section", "role": "hero", "label": "Build in your terminal", "text": "An AI coding agent that works in your terminal and IDE.", "shot": "hero-overview", "composition": "full-bleed"},
                            {"kind": "semantic-section", "role": "developer", "label": "Run commands and edit files", "text": "Read your codebase, run commands, and edit files.", "shot": "feature-zoom", "composition": "zoom-callout"},
                            {"kind": "semantic-section", "role": "cta", "label": "Read the docs", "text": "Read the docs.", "shot": "cta-summary", "composition": "cta-lockup"},
                        ],
                        "evidence": [
                            {"kind": "semantic-section", "role": "hero", "label": "Build in your terminal", "text": "An AI coding agent that works in your terminal and IDE.", "shot": "hero-overview", "composition": "full-bleed"},
                            {"kind": "semantic-section", "role": "developer", "label": "Run commands and edit files", "text": "Read your codebase, run commands, and edit files.", "shot": "feature-zoom", "composition": "zoom-callout"},
                            {"kind": "cta", "role": "cta", "label": "Read the docs", "text": "Read the docs.", "shot": "cta-summary", "composition": "cta-lockup"},
                        ],
                    }
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        run_cmd(
            "compose",
            "--project",
            str(project),
            "--brief",
            "用中文介绍 Claude Code：终端、IDE、代码库、运行命令、编辑文件、GitHub、GitLab、Issue 到 PR。",
            "--site-file",
            str(site),
            "--duration",
            "9",
            "--offline",
            "--beat-mode",
            "layered",
        )
        html = (project / "index.html").read_text()
        content_brief = json.loads((project / "assets" / "content-brief.json").read_text())["content_brief"]
        production_spec = json.loads((project / "assets" / "production-spec.json").read_text())
        assert "终端代理" in html
        assert "代码库理解" in html or "Issue 到 PR" in html
        assert "这一屏补充官网的核心模块" not in html
        assert content_brief["talking_points"]
        assert production_spec["content_brief"]["talking_points"]


def test_site_compose_preserves_llm_storyboard_insights() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        project = root / "llm-insight-site"
        site = root / "site.json"
        site.write_text(
            json.dumps(
                {
                    "site": {
                        "source_url": "https://example.com/claude-code",
                        "brand_name": "Claude Code",
                        "title": "Claude Code",
                        "summary": "AI coding agent for terminal and IDE.",
                        "ctas": ["Try Claude"],
                        "evidence": [
                            {"kind": "semantic-section", "role": "hero", "label": "Claude Code", "text": "AI coding agent for terminal and IDE.", "shot": "hero-overview", "composition": "full-bleed"},
                            {"kind": "semantic-section", "role": "developer", "label": "Meets you where you code", "text": "Works in the terminal, VS Code, JetBrains IDE, GitHub, and GitLab.", "shot": "feature-zoom", "composition": "zoom-callout"},
                        ],
                    }
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        plan = root / "plan.json"
        plan.write_text(
            json.dumps(
                {
                    "title": "Claude Code",
                    "headline": "从 Issue 推进到 PR",
                    "narration": "Claude Code 把需求、代码库理解、编辑文件、运行命令和 PR 串成一条开发工作流。",
                    "storyboard": [
                        {"id": "tools", "start": 0, "end": 4, "intent": "罗列官网公示的支持入口图标：终端、VS Code、JetBrains IDE、Slack、移动端，标注「适配你已有的全部开发工具链」，避免额外迁移成本"},
                        {"id": "repo", "start": 4, "end": 8, "intent": "动画演示Claude Code扫描本地代码库生成结构图谱的过程，标注「全局理解代码逻辑，无需手动上传上下文」，对应官网代码库分析功能"},
                    ],
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        run_cmd(
            "compose",
            "--project",
            str(project),
            "--brief",
            "用中文介绍 Claude Code。",
            "--site-file",
            str(site),
            "--plan-file",
            str(plan),
            "--duration",
            "8",
            "--offline",
            "--beat-mode",
            "layered",
        )
        html = (project / "index.html").read_text()
        production_spec = json.loads((project / "assets" / "production-spec.json").read_text())
        assert "适配你已有的全部开发工具链" in html
        assert "全局理解代码逻辑" in html
        assert "官网当前区域，承接本镜头" not in html
        assert production_spec["scenes"][0]["title"] == "适配你已有的全部开发工具链"


def test_site_compose_extracts_unquoted_llm_mechanisms() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        project = root / "llm-mechanism-site"
        site = root / "site.json"
        site.write_text(
            json.dumps(
                {
                    "site": {
                        "source_url": "https://example.com/claude-code",
                        "brand_name": "Claude Code",
                        "title": "Claude Code",
                        "summary": "AI coding agent for terminal and IDE.",
                        "evidence": [
                            {"kind": "semantic-section", "role": "hero", "label": "Claude Code", "text": "AI coding agent for terminal and IDE.", "shot": "hero-overview", "composition": "full-bleed"},
                            {"kind": "semantic-section", "role": "developer", "label": "Meets you where you code", "text": "Works in your terminal.", "shot": "feature-zoom", "composition": "zoom-callout"},
                        ],
                    }
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        plan = root / "plan.json"
        plan.write_text(
            json.dumps(
                {
                    "title": "Claude Code",
                    "headline": "真实开发工作流",
                    "narration": "Claude Code 在终端和 IDE 中推进真实开发任务。",
                    "storyboard": [
                        {"id": "position", "start": 0, "end": 4, "intent": "展示Anthropic官方Claude Code产品页头，明确产品定位为面向开发者的代理式编码工具，对应官网首页公开的产品定位证据。"},
                        {"id": "cli", "start": 4, "end": 8, "intent": "特写终端界面运行Claude Code指令的真实录屏，演示其原生支持所有CLI工具的底层机制，对应官网终端集成功能说明。"},
                    ],
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        run_cmd(
            "compose",
            "--project",
            str(project),
            "--brief",
            "用中文介绍 Claude Code。",
            "--site-file",
            str(site),
            "--plan-file",
            str(plan),
            "--duration",
            "8",
            "--offline",
            "--beat-mode",
            "layered",
        )
        html = (project / "index.html").read_text()
        production_spec = json.loads((project / "assets" / "production-spec.json").read_text())
        assert "面向开发者的代理式编码工具" in html
        assert "原生支持所有CLI工具" in html
        assert production_spec["scenes"][0]["title"] == "面向开发者的代理式编码工具"


def test_site_compose_turns_llm_intents_into_public_copy() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        project = root / "trip-intent-copy"
        site = root / "site.json"
        site.write_text(
            json.dumps(
                {
                    "site": {
                        "source_url": "https://hk.trip.com/",
                        "brand_name": "Trip.com",
                        "title": "Trip.com 香港",
                        "summary": "Trip.com 提供全球航線、酒店、租車接送、門票體驗和 30 秒內全球支援。",
                        "ctas": ["登入或註冊"],
                        "screenshots": [{"id": "site-shot-01", "path": "assets/site-screenshots/site-shot-01.png"}],
                        "evidence": [
                            {"kind": "semantic-section", "role": "hero", "label": "全球機票與酒店預訂", "text": "提供全球逾9000條航線和120萬間酒店預訂。", "shot": "hero-overview", "composition": "full-bleed"},
                            {"kind": "semantic-section", "role": "product", "label": "一站式旅遊服務", "text": "租車接送、門票體驗、禮品卡、郵輪、旅遊保險和旅行團。", "shot": "feature-zoom", "composition": "zoom-callout"},
                            {"kind": "semantic-section", "role": "safety", "label": "安心付款與全球支援", "text": "最新加密技術保護付款資料，30秒內取得全球支援。", "shot": "trust-message", "composition": "evidence-board"},
                        ],
                    }
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        plan = root / "plan.json"
        plan.write_text(
            json.dumps(
                {
                    "title": "Trip.com 香港",
                    "headline": "一站式旅遊預訂平台",
                    "narration": "Trip.com 香港把機票、酒店、交通、門票與支援放在同一套預訂體驗裡。",
                    "storyboard": [
                        {"id": "s1", "start": 0, "end": 3, "intent": "展示其「全球逾9000條航線」與「120萬間酒店預訂」的供給規模，並補充住客評價與限時機票酒店優惠。"},
                        {"id": "s2", "start": 3, "end": 6, "intent": "展示其一站式服務範圍：租車接送、門票體驗、禮品卡、郵輪、旅遊保險、獨立包團和旅行團。"},
                        {"id": "s3", "start": 6, "end": 9, "intent": "證明其信任與服務支撐：安心付款、最新加密技術保護付款資料，以及30秒內取得全球支援。"},
                    ],
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        (project / "assets" / "site-screenshots").mkdir(parents=True)
        (project / "assets" / "site-screenshots" / "site-shot-01.png").write_bytes(b"png")
        run_cmd(
            "compose",
            "--project",
            str(project),
            "--brief",
            "介紹 Trip.com 香港官網。",
            "--site-file",
            str(site),
            "--plan-file",
            str(plan),
            "--duration",
            "9",
            "--offline",
            "--beat-mode",
            "layered",
        )
        html = (project / "index.html").read_text()
        production_spec = json.loads((project / "assets" / "production-spec.json").read_text())
        visible_payload = html + json.dumps(production_spec, ensure_ascii=False)
        assert "租車接送" in visible_payload
        for token in ["展示其", "證明其", "核心依据", "PAGE SIGNAL", "真实证据", "页面线索", "使用含义", "Website Brief"]:
            assert token not in visible_payload


def test_storyboard_from_brief_uses_generic_chapter_ids() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        project = Path(directory) / "generic-story"
        run_cmd("compose", "--project", str(project), "--brief", "Make a product launch film.", "--duration", "6", "--offline")
        html = (project / "index.html").read_text()
        meta = json.loads((project / "senseframe.json").read_text())
        scene_ids = [item["id"] for item in meta["storyboard"]]
        assert scene_ids == ["chapter-1", "chapter-2", "chapter-3"]
        assert 'data-scene="intro"' not in html
        assert 'data-scene="media"' not in html
        assert 'data-scene="render"' not in html


def test_generic_compose_narration_does_not_claim_webpage() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        project = Path(directory) / "generic-narration"
        run_cmd(
            "compose",
            "--project",
            str(project),
            "--brief",
            "为一款名为 Meridian AI 的企业研究助手制作一支高级产品发布短片。风格成熟、克制，不要网页介绍。",
            "--duration",
            "6",
            "--offline",
        )
        narration = (project / "assets" / "narration.txt").read_text()
        assert "网页" not in narration
        assert "首页结构" not in narration
        assert "Meridian AI" in narration


def test_compose_longform_expands_duration_storyboard_and_narration() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        project = Path(directory) / "longform-director"
        run_cmd(
            "compose",
            "--project",
            str(project),
            "--brief",
            "为一款名为 Meridian AI 的企业研究助手制作一支高级产品发布片。风格成熟、克制。",
            "--longform",
            "--offline",
        )
        meta = json.loads((project / "senseframe.json").read_text())
        narration = (project / "assets" / "narration.txt").read_text()
        captions = json.loads((project / "assets" / "captions.json").read_text())["captions"]
        production_spec = json.loads((project / "assets" / "production-spec.json").read_text())
        assert meta["duration"] == 24.0
        assert meta["director_mode"] == "longform"
        assert meta["production_spec"] == "assets/production-spec.json"
        assert len(meta["storyboard"]) >= 6
        assert production_spec["rhythm"] == "drift-build-PEAK-drift-resolve"
        assert len(production_spec["scenes"]) == len(meta["storyboard"])
        assert production_spec["scenes"][0]["proof_points"][0]["label"] == "对象"
        layouts = {scene["layout"] for scene in production_spec["scenes"]}
        assert {"title-slate", "tension-matrix", "process-pipeline", "evidence-wall", "scenario-desk", "final-lockup"}.issubset(layouts)
        html = (project / "index.html").read_text()
        assert "fromLayout" in html
        assert "toLayout" in html
        assert all(item["end"] > item["start"] for item in meta["storyboard"])
        assert "网页" not in narration
        assert "单点功能" in narration
        assert len(captions) >= 6


def test_llm_plan_longform_dry_run_requests_deeper_director_work() -> None:
    result = run_cmd(
        "llm-plan",
        "--brief",
        "Create a premium launch film for an AI research product.",
        "--longform",
        "--dry-run",
    )
    payload = json.loads(result.stdout)
    request = payload["payload"]["messages"][1]["content"]
    assert payload["payload"]["temperature"] > 0.4
    assert '"director_mode": "longform"' in request
    assert '"target_scene_count": 6' in request
    assert "visual rhythm" in payload["payload"]["messages"][0]["content"]


def test_skill_package_is_clawhub_ready() -> None:
    skill = ROOT
    skill_md = skill / "SKILL.md"
    body = skill_md.read_text(encoding="utf-8")
    assert body.startswith("---\n")
    frontmatter = body.split("---", 2)[1]
    assert re.search(r"^name:\s*senseaudio-video-gen\s*$", frontmatter, re.MULTILINE)
    assert re.search(r"^description:\s*.+", frontmatter, re.MULTILINE)
    assert 200 < len(body) < 25000
    assert (skill / "scripts" / "senseaudio_video_gen.py").exists()
    assert (skill / "requirements.txt").exists()
    assert any((skill / "examples").iterdir())
    assert any((skill / "references").iterdir())
    assert (skill / "README.md").exists()
    slash = "/"
    forbidden = [
        slash + "Users" + slash,
        slash + "tmp" + slash,
        slash + "private" + slash,
        slash + "var" + slash + "folders",
        slash + "path" + slash + "to",
        "C:" + chr(92),
    ]
    filler_marker = "st" + "ub"
    for path in skill.rglob("*"):
        if not path.is_file() or "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        assert not any(token in text for token in forbidden), f"absolute path token found in {path.relative_to(skill)}"
        assert filler_marker not in text.lower(), f"filler marker found in {path.relative_to(skill)}"


def run_all_tests() -> None:
    failures: list[tuple[str, Exception]] = []
    tests = [(name, value) for name, value in globals().items() if name.startswith("test_") and callable(value)]
    for name, test in sorted(tests):
        try:
            test()
        except Exception as exc:
            failures.append((name, exc))
            print(f"FAIL {name}: {exc!r}")
    print(f"ran {len(tests)} failures {len(failures)}")
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    run_all_tests()

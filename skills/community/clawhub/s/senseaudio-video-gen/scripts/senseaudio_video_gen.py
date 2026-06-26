#!/usr/bin/env python3
"""SenseAudio video generation helper.

This script performs real SenseAudio API calls when SENSEAUDIO_API_KEY is set.
Use --dry-run on mutating commands to inspect payloads without sending requests.
"""

from __future__ import annotations

import argparse
import array
import base64
import contextlib
import concurrent.futures
import html as html_lib
import http.server
import io
import json
import math
import mimetypes
import os
import re
import shutil
import signal
import socket
import socketserver
import struct
import subprocess
import sys
import tempfile
import textwrap
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
import zlib
from pathlib import Path
from typing import Any


API_BASE = "https://api.senseaudio.cn/v1"
DEFAULT_VIDEO_MODEL = "Seedance-Pro-1.5"
VIDEO_MODEL_FALLBACKS = ("Seedance-Pro-1.5", "Seedance-2.0-Fast", "Seedance-2.0")
DEFAULT_IMAGE_MODEL = "senseaudio-image-1.0-260319"
IMAGE_MODEL_FALLBACKS = ("senseaudio-image-1.0-260319", "doubao-seedream-5-0-260128")
DEFAULT_TTS_MODEL = "senseaudio-tts-1.5-260319"
DEFAULT_ASR_MODEL = "senseaudio-asr-1.5-260319"
DEFAULT_MUSIC_MODEL = "senseaudio-music-1.0-260319"
MUSIC_MODEL_FALLBACKS = ("senseaudio-music-1.0-260319",)
DEFAULT_MUSIC_VOLUME = 0.18
DEFAULT_WIDTH = 1280
DEFAULT_HEIGHT = 720
DEFAULT_RENDER_FPS = 24
DEFAULT_RENDER_DURATION = 6.0
DEFAULT_VOICE_ID = "male_0028_a"
DEFAULT_DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEFAULT_DEEPSEEK_MODEL = "deepseek-v4-pro"
DEFAULT_OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_OPENROUTER_LLM_MODEL = "google/gemini-3.1-flash-lite"
DEFAULT_VL_MODEL = "google/gemini-3.1-flash-lite"
DEFAULT_AUDIOCLAW_LLM_BASE_URL = "https://platform.senseaudio.cn/v1"
DEFAULT_AUDIOCLAW_LLM_MODEL = "doubao-seed-2-0-pro-260215"
DEFAULT_AUDIOCLAW_CONFIG_PATH = Path.home() / ".audioclaw" / "config.json"
DEFAULT_AUDIOCLAW_WORKSPACE_PATH = Path.home() / ".audioclaw" / "workspace"
DEFAULT_VIDEO_LANGUAGE = "zh-CN"
TRANSITION_PRESETS = ("none", "editorial", "glass", "ribbon", "iris", "luma")
TIMELINE_ENGINES = ("native", "gsap-compat")
BEAT_MODES = ("scene", "layered")
BEAT_ROLES = ("hook", "proof", "detail", "cta")
WEBSITE_SHOT_TYPES = ("hero-overview", "nav-scan", "feature-zoom", "trust-message", "cta-summary")
COMPOSITION_MODES = ("full-bleed", "split-scan", "zoom-callout", "evidence-board", "cta-lockup")
CAMERA_PATHS = ("hero-push", "lateral-scan", "macro-zoom", "board-orbit", "lockup-dolly")
DEFAULT_BEATS_PER_SCENE = 3
MIN_READABLE_BEAT_DURATION = 0.95
DEFAULT_SITE_BEATS_PER_SCENE = 2
MIN_SITE_SCENE_DURATION = 2.8
MAX_COMFORTABLE_BEAT_RATE = 1.15
MAX_STORYBOARD_SCENES = 5
LONGFORM_THRESHOLD = 20.0
LONGFORM_MIN_DURATION = 24.0
LONGFORM_MAX_STORYBOARD_SCENES = 9
MIN_READABLE_SCENE_DURATION = 2.2
STYLE_PRESETS: dict[str, dict[str, Any]] = {
    "product-glass": {
        "description": "Premium dark product UI with warm glass highlights.",
        "tokens": {
            "accent": "#7c5cff",
            "ember": "#ff9a5c",
            "aqua": "#4cdfcc",
            "ink": "#f8f4ea",
            "muted": "rgba(248,244,234,.68)",
            "body_bg": "#08070d",
            "stage_bg": "#090812",
            "card_from": "rgba(255,255,255,.88)",
            "card_to": "rgba(235,230,255,.72)",
            "mesh": "radial-gradient(circle at 16% 18%, rgba(255,154,92,.34), rgba(255,154,92,0) 24%), radial-gradient(circle at 78% 18%, rgba(124,92,255,.46), rgba(124,92,255,0) 30%), radial-gradient(circle at 54% 92%, rgba(76,223,204,.28), rgba(76,223,204,0) 26%)",
        },
        "recommended": {"animation_preset": "cinematic", "transition_preset": "editorial", "timeline_engine": "gsap-compat"},
    },
    "neon-console": {
        "description": "High-contrast creator console with cyan glow and electric purple surfaces.",
        "tokens": {
            "accent": "#00e5ff",
            "ember": "#b45cff",
            "aqua": "#6dffb8",
            "ink": "#ecfbff",
            "muted": "rgba(236,251,255,.66)",
            "body_bg": "#030712",
            "stage_bg": "#04101f",
            "card_from": "rgba(222,250,255,.92)",
            "card_to": "rgba(196,225,255,.68)",
            "mesh": "radial-gradient(circle at 12% 16%, rgba(0,229,255,.34), rgba(0,229,255,0) 24%), radial-gradient(circle at 78% 20%, rgba(180,92,255,.44), rgba(180,92,255,0) 32%), radial-gradient(circle at 54% 88%, rgba(109,255,184,.24), rgba(109,255,184,0) 28%)",
        },
        "recommended": {"animation_preset": "kinetic", "transition_preset": "luma", "timeline_engine": "gsap-compat"},
    },
    "editorial-cream": {
        "description": "Soft editorial launch frame with cream paper, black type, and restrained gold motion.",
        "tokens": {
            "accent": "#111111",
            "ember": "#c8842f",
            "aqua": "#7d8f75",
            "ink": "#17130d",
            "muted": "rgba(23,19,13,.62)",
            "body_bg": "#eee4d2",
            "stage_bg": "#f4ead9",
            "card_from": "rgba(255,252,244,.94)",
            "card_to": "rgba(236,224,204,.78)",
            "mesh": "radial-gradient(circle at 18% 22%, rgba(200,132,47,.22), rgba(200,132,47,0) 26%), radial-gradient(circle at 78% 18%, rgba(17,17,17,.16), rgba(17,17,17,0) 30%), radial-gradient(circle at 56% 90%, rgba(125,143,117,.18), rgba(125,143,117,0) 28%)",
        },
        "recommended": {"animation_preset": "product-tour", "transition_preset": "iris", "timeline_engine": "gsap-compat"},
    },
    "editorial-pro": {
        "description": "Mature website analysis film with restrained typography, fine annotations, and documentary pacing.",
        "tokens": {
            "accent": "#151515",
            "ember": "#8d7357",
            "aqua": "#6f746b",
            "ink": "#161412",
            "muted": "rgba(22,20,18,.64)",
            "body_bg": "#e8dfd2",
            "stage_bg": "#eee7dc",
            "card_from": "rgba(249,246,239,.96)",
            "card_to": "rgba(229,220,207,.82)",
            "mesh": "linear-gradient(115deg, rgba(22,20,18,.055), rgba(22,20,18,0) 34%), radial-gradient(circle at 22% 18%, rgba(141,115,87,.16), rgba(141,115,87,0) 28%), radial-gradient(circle at 78% 22%, rgba(22,20,18,.10), rgba(22,20,18,0) 26%)",
        },
        "recommended": {"animation_preset": "product-tour", "transition_preset": "editorial", "timeline_engine": "gsap-compat"},
    },
    "executive-film": {
        "description": "General-purpose executive launch film with cinematic restraint, large typography, and minimal interface ornament.",
        "tokens": {
            "accent": "#d6c19a",
            "ember": "#8f6b3f",
            "aqua": "#6f7972",
            "ink": "#f4efe6",
            "muted": "rgba(244,239,230,.62)",
            "body_bg": "#060606",
            "stage_bg": "#090908",
            "card_from": "rgba(22,22,20,.94)",
            "card_to": "rgba(10,10,9,.92)",
            "mesh": "radial-gradient(circle at 72% 18%, rgba(214,193,154,.16), rgba(214,193,154,0) 30%), radial-gradient(circle at 24% 78%, rgba(143,107,63,.18), rgba(143,107,63,0) 34%), linear-gradient(115deg, rgba(255,255,255,.045), rgba(255,255,255,0) 38%)",
        },
        "recommended": {"animation_preset": "cinematic", "transition_preset": "editorial", "timeline_engine": "gsap-compat"},
    },
    "midnight-lab": {
        "description": "Deep audio lab aesthetic with blue-black stage and spectral green accents.",
        "tokens": {
            "accent": "#6ea8ff",
            "ember": "#19f0a5",
            "aqua": "#9ad7ff",
            "ink": "#eef6ff",
            "muted": "rgba(238,246,255,.64)",
            "body_bg": "#02050b",
            "stage_bg": "#050b16",
            "card_from": "rgba(230,243,255,.88)",
            "card_to": "rgba(194,219,255,.66)",
            "mesh": "radial-gradient(circle at 15% 20%, rgba(25,240,165,.26), rgba(25,240,165,0) 25%), radial-gradient(circle at 80% 16%, rgba(110,168,255,.42), rgba(110,168,255,0) 32%), radial-gradient(circle at 50% 92%, rgba(154,215,255,.22), rgba(154,215,255,0) 30%)",
        },
        "recommended": {"animation_preset": "cinematic", "transition_preset": "glass", "timeline_engine": "gsap-compat"},
    },
}


class SenseAudioError(RuntimeError):
    pass


RUNTIME_JS = r"""
(function () {
  function num(value, fallback) {
    var parsed = Number(value);
    return Number.isFinite(parsed) ? parsed : fallback;
  }

  function clipRange(element) {
    var start = num(element.dataset.start, 0);
    var duration = element.dataset.duration == null ? Infinity : num(element.dataset.duration, Infinity);
    return { start: start, duration: duration, end: start + duration };
  }

  function activeCaption(captions, time) {
    for (var i = 0; i < captions.length; i += 1) {
      var item = captions[i];
      if (time >= num(item.start, 0) && time < num(item.end, 0)) return item;
    }
    return null;
  }

  function clamp(value, min, max) {
    return Math.min(max, Math.max(min, value));
  }

  function ease(value) {
    value = clamp(value, 0, 1);
    return 1 - Math.pow(1 - value, 3);
  }

  function applyTimeline() {
    var items = (window.__senseframes && window.__senseframes.timeline && window.__senseframes.timeline.items) || [];
    items.forEach(function (item) {
      var selector = item.selector || (item.id ? '[data-timeline-id="' + item.id + '"], [data-scene="' + item.id + '"]' : "");
      if (!selector) return;
      document.querySelectorAll(selector).forEach(function (element) {
        if (item.start != null) element.dataset.start = String(item.start);
        if (item.end != null && item.start != null) element.dataset.duration = String(Number(item.end) - Number(item.start));
        if (item.duration != null) element.dataset.duration = String(item.duration);
        if (item.effect) element.dataset.effect = item.effect;
        if (item.easing) element.dataset.easing = item.easing;
      });
    });
  }

  function applyEffect(element, time) {
    var effect = element.dataset.effect;
    if (!effect) return;
    var range = clipRange(element);
    var progress = ease((time - range.start) / Math.max(0.001, Math.min(1.2, range.duration || 1)));
    var exitProgress = ease((range.end - time) / Math.max(0.001, Math.min(1.0, range.duration || 1)));
    var opacity = 0.12 + 0.88 * Math.min(progress, exitProgress);
    var transform = "";
    if (effect === "fade-up") transform = "translateY(" + ((1 - progress) * 28).toFixed(2) + "px)";
    else if (effect === "slide-left") transform = "translateX(" + ((1 - progress) * 44).toFixed(2) + "px)";
    else if (effect === "zoom-in") transform = "scale(" + (0.94 + progress * 0.06).toFixed(4) + ")";
    else if (effect === "spotlight") transform = "scale(" + (0.985 + progress * 0.015).toFixed(4) + ")";
    else if (effect === "parallax") transform = "translate3d(" + ((0.5 - progress) * 30).toFixed(2) + "px," + ((1 - progress) * 18).toFixed(2) + "px,0)";
    element.style.opacity = String(clamp(opacity, 0, 1));
    if (transform) element.style.transform = transform;
  }

  function renderCaption(element, caption, time) {
    if (!caption) {
      element.textContent = "";
      element.dataset.sfActive = "false";
      return;
    }
    if (Array.isArray(caption.words) && caption.words.length) {
      element.textContent = "";
      caption.words.forEach(function (word) {
        var span = document.createElement("span");
        var active = time >= num(word.start, caption.start) && time < num(word.end, caption.end);
        var emphasis = /senseaudio|audio|视频|生成|克隆|音色|旁白|搜索/i.test(String(word.text || ""));
        var wordProgress = clamp((time - num(word.start, caption.start)) / Math.max(0.001, num(word.end, caption.end) - num(word.start, caption.start)), 0, 1);
        var pop = Math.sin(wordProgress * Math.PI);
        var scale = active ? (emphasis ? 1.14 : 1.07) + pop * (emphasis ? 0.08 : 0.04) : 1;
        span.className = "sf-word";
        if (emphasis) span.className += " sf-word-emphasis";
        span.dataset.sfActive = active ? "true" : "false";
        span.dataset.sfEmphasis = emphasis ? "true" : "false";
        span.style.transform = "scale(" + scale.toFixed(3) + ")";
        span.style.filter = active && emphasis ? "drop-shadow(0 0 12px rgba(255,214,140,.45))" : "none";
        span.textContent = word.text;
        element.appendChild(span);
      });
    } else {
      element.textContent = caption.text;
    }
    element.dataset.sfActive = "true";
  }

  function seekTimelines(time) {
    var timelines = window.__timelines || {};
    Object.keys(timelines).forEach(function (key) {
      var timeline = timelines[key];
      if (timeline && typeof timeline.seek === "function") {
        timeline.seek(time);
      }
    });
  }

  window.__senseframes = {
    time: 0,
    captions: [],
    timeline: null,
    audioData: null,
    apply: function (time) {
      document.documentElement.style.setProperty("--sf-time", String(time));
      document.documentElement.dataset.sfTime = String(time);
      var clips = document.querySelectorAll("[data-start], [data-scene]");
      clips.forEach(function (element) {
        var range = clipRange(element);
        var active = time >= range.start && time < range.end;
        if (element.dataset.compositionId && !element.dataset.compositionSrc) active = true;
        element.dataset.sfActive = active ? "true" : "false";
        if (element.dataset.scene != null) element.dataset.sceneActive = active ? "true" : "false";
        if (element.dataset.enter && active) element.dataset.sfEnter = element.dataset.enter;
        if (element.dataset.exit && !active) element.dataset.sfExit = element.dataset.exit;
        applyEffect(element, time);
        if (element.classList.contains("clip") || element.matches("video,audio,img,[data-duration]")) {
          element.style.visibility = active ? "visible" : "hidden";
        }
        if (active && (element.tagName === "VIDEO" || element.tagName === "AUDIO")) {
          try {
            element.pause();
            element.currentTime = Math.max(0, time - range.start + num(element.dataset.mediaStart, 0));
          } catch (_) {}
        }
      });
      document.querySelectorAll("[data-caption-source], [data-caption-target]").forEach(function (element) {
        var caption = activeCaption(window.__senseframes.captions || [], time);
        renderCaption(element, caption, time);
      });
      seekTimelines(time);
      if (typeof window.renderFrame === "function") window.renderFrame(time);
      window.dispatchEvent(new CustomEvent("sf-seek", { detail: { time: time } }));
    },
  };

  var params = new URLSearchParams(location.search);
  var time = num(params.get("t"), 0);
  window.__senseframes.time = time;
  window.addEventListener("load", function () {
    var captionElement = document.querySelector("[data-caption-source]");
    var source = captionElement && captionElement.dataset.captionSource;
    var timelineElement = document.querySelector("[data-timeline-source]");
    var timelineSource = timelineElement && timelineElement.dataset.timelineSource;
    var audioElement = document.querySelector("[data-audio-source]");
    var audioSource = audioElement && audioElement.dataset.audioSource;
    var ready = Promise.resolve();
    if (Array.isArray(window.__sfCaptions)) {
      window.__senseframes.captions = window.__sfCaptions;
    } else if (source) {
      ready = fetch(source).then(function (response) { return response.json(); }).then(function (data) {
        window.__senseframes.captions = Array.isArray(data) ? data : (data.captions || []);
      }).catch(function () {
        window.__senseframes.captions = [];
      });
    }
    if (timelineSource) {
      ready = ready.then(function () {
        return fetch(timelineSource).then(function (response) { return response.json(); }).then(function (data) {
          window.__senseframes.timeline = data;
          applyTimeline();
        }).catch(function () {
          window.__senseframes.timeline = null;
        });
      });
    }
    if (audioSource) {
      ready = ready.then(function () {
        return fetch(audioSource).then(function (response) { return response.json(); }).then(function (data) {
          window.__senseframes.audioData = data;
        }).catch(function () {
          window.__senseframes.audioData = null;
        });
      });
    }
    ready.then(function () {
      window.__senseframes.apply(time);
      window.__sfReady = true;
    });
  });
})();
"""


STARTER_HTML = """<!doctype html>
<html lang="zh-CN" data-composition-variables='[
  {"id":"title","type":"string","label":"Title","default":"SenseAudio Video Gen"},
  {"id":"subtitle","type":"string","label":"Subtitle","default":"HTML composition, SenseAudio media, local render."},
  {"id":"accent","type":"color","label":"Accent","default":"#6d5dfc"}
]'>
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>SenseAudio Video Gen</title>
  <style>
    :root { --accent: #6d5dfc; --sf-time: 0; }
    * { box-sizing: border-box; }
    body { margin: 0; background: #f8f8f5; color: #111; font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; overflow: hidden; }
    [data-composition-id="main"] { width: 1280px; height: 720px; position: relative; overflow: hidden; background: radial-gradient(circle at 20% 10%, #ffffff 0, #f5f0ff 28%, #f8f8f5 58%); }
    .grain { position: absolute; inset: 0; opacity: .18; background-image: linear-gradient(115deg, rgba(0,0,0,.04), transparent 35%), radial-gradient(circle at 85% 20%, rgba(109,93,252,.22), transparent 28%); }
    .stage { position: absolute; inset: 56px; display: grid; grid-template-columns: 0.92fr 1.08fr; gap: 34px; align-items: center; }
    .copy { display: flex; flex-direction: column; gap: 24px; }
    .eyebrow { font-size: 19px; letter-spacing: .16em; text-transform: uppercase; color: #5d55c8; font-weight: 800; }
    h1 { margin: 0; font-size: 76px; line-height: .95; letter-spacing: -.055em; max-width: 560px; }
    p { margin: 0; color: #555; font-size: 26px; line-height: 1.35; max-width: 560px; }
    .pills { display: flex; flex-wrap: wrap; gap: 10px; }
    .pill { padding: 10px 14px; border-radius: 999px; background: rgba(255,255,255,.8); border: 1px solid rgba(17,17,17,.08); font-weight: 700; color: #333; }
    .browser { border-radius: 34px; background: rgba(255,255,255,.86); box-shadow: 0 35px 90px rgba(38, 33, 82, .20); border: 1px solid rgba(17,17,17,.08); overflow: hidden; transform: perspective(1200px) rotateY(-5deg) rotateX(2deg); }
    .bar { height: 56px; display: flex; gap: 10px; align-items: center; padding: 0 22px; border-bottom: 1px solid #eceaf2; }
    .dot { width: 12px; height: 12px; border-radius: 50%; background: #ddd; }
    .dot:nth-child(1) { background: #ff6257; } .dot:nth-child(2) { background: #ffbd2e; } .dot:nth-child(3) { background: #28c840; }
    .ui { padding: 26px; display: grid; gap: 18px; }
    .search { height: 48px; border-radius: 16px; background: #f4f4f4; display: flex; align-items: center; padding: 0 18px; color: #888; font-size: 18px; }
    .cards { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
    .card { min-height: 120px; border-radius: 22px; background: linear-gradient(135deg, #fff, #f6f4ff); border: 1px solid rgba(17,17,17,.07); padding: 18px; display: flex; flex-direction: column; justify-content: space-between; }
    .avatar { width: 42px; height: 42px; border-radius: 14px; background: linear-gradient(135deg, var(--accent), #111); }
    .name { font-size: 22px; font-weight: 850; }
    .meta { color: #777; font-size: 15px; }
    .scene-label { position: absolute; right: 62px; bottom: 48px; color: #777; font-weight: 700; }
  </style>
</head>
<body>
  <div data-composition-id="main" data-start="0" data-duration="6" data-width="1280" data-height="720">
    <div class="grain"></div>
    <main class="stage">
      <section class="copy">
        <div class="eyebrow">SenseAudio Studio</div>
        <h1 id="title">HTML videos, powered by SenseAudio.</h1>
        <p id="subtitle">Author the frame in HTML. Generate voices, captions, images, and AI video references through SenseAudio.</p>
        <div class="pills">
          <span class="pill">TTS</span><span class="pill">ASR</span><span class="pill">Images</span><span class="pill">Video tasks</span>
        </div>
      </section>
      <section class="browser">
        <div class="bar"><span class="dot"></span><span class="dot"></span><span class="dot"></span></div>
        <div class="ui">
          <div class="search">Search voice, scene, caption...</div>
          <div class="cards">
            <div class="card"><div class="avatar"></div><div><div class="name">温柔御姐</div><div class="meta">voice · narration</div></div></div>
            <div class="card"><div class="avatar"></div><div><div class="name">可靠青叔</div><div class="meta">clone · promo</div></div></div>
            <div class="card"><div class="avatar"></div><div><div class="name">Caption JSON</div><div class="meta">word timestamps</div></div></div>
            <div class="card"><div class="avatar"></div><div><div class="name">Seedance clip</div><div class="meta">reference video</div></div></div>
          </div>
        </div>
      </section>
    </main>
    <div class="scene-label">data-composition-id="main"</div>
  </div>
  <script src="./senseframe-runtime.js"></script>
  <script>
    function lerp(a, b, p) { return a + (b - a) * p; }
    window.renderFrame = function (t) {
      var p = Math.min(1, Math.max(0, t / 6));
      document.querySelector(".browser").style.transform =
        "perspective(1200px) rotateY(" + lerp(-9, -2, p) + "deg) rotateX(2deg) translateY(" + lerp(24, 0, p) + "px)";
      document.querySelector(".copy").style.transform = "translateY(" + lerp(22, 0, p) + "px)";
      document.querySelector(".copy").style.opacity = String(lerp(.72, 1, p));
    };
  </script>
</body>
</html>
"""


COMPOSE_HTML = """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title}</title>
  <style>
    :root {{ --accent: {accent}; --ember: {ember}; --aqua: {aqua}; --ink: {ink}; --muted: {muted}; --sf-time: 0; }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; overflow: hidden; background: {body_bg}; color: var(--ink); font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }}
    [data-composition-id="main"] {{ width: {width}px; height: {height}px; position: relative; overflow: hidden; background: {stage_bg}; }}
    .mesh {{ position: absolute; inset: -160px; background: {mesh}; filter: blur(12px); opacity: .9; }}
    .grain {{ position: absolute; inset: 0; opacity: .18; background-image: linear-gradient(115deg, rgba(255,255,255,.06), rgba(255,255,255,0) 28%), repeating-linear-gradient(0deg, rgba(255,255,255,.035), rgba(255,255,255,.035) 1px, rgba(0,0,0,0) 1px, rgba(0,0,0,0) 5px); mix-blend-mode: screen; }}
    .camera-layer {{ position: absolute; inset: 0; transform-origin: 54% 50%; }}
    .brand-rail {{ position: absolute; top: 34px; left: 46px; right: 46px; display: flex; align-items: center; justify-content: space-between; z-index: 20; font-weight: 900; letter-spacing: -.03em; }}
    .brand {{ display: flex; align-items: center; gap: 12px; font-size: 22px; }}
    .brand-mark {{ width: 34px; height: 34px; border-radius: 12px; background: linear-gradient(135deg, #fff, var(--accent)); box-shadow: 0 0 34px rgba(124,92,255,.48); overflow: hidden; display: grid; place-items: center; }}
    .brand-mark.logo {{ background: rgba(255,255,255,.92); padding: 5px; }}
    .brand-mark img {{ width: 100%; height: 100%; object-fit: contain; display: block; }}
    .timeline-nav {{ display: flex; gap: 8px; color: rgba(255,255,255,.58); font-size: 13px; text-transform: uppercase; letter-spacing: .12em; }}
    .timeline-nav span {{ padding: 8px 11px; border-radius: 999px; border: 1px solid rgba(255,255,255,.12); background: rgba(255,255,255,.04); }}
    .timeline-nav span[data-active="true"] {{ color: #111; background: #fff3c8; }}
    .story-scene {{ position: absolute; inset: 0; padding: 96px 62px 76px; opacity: 0; visibility: hidden; overflow: hidden; }}
    .scene-grid {{ width: 100%; height: 100%; display: grid; grid-template-columns: .88fr 1.12fr; gap: 42px; align-items: center; }}
    .scene-copy {{ min-width: 0; display: flex; flex-direction: column; gap: 18px; z-index: 4; }}
    .eyebrow {{ color: #ffd49a; font-weight: 900; font-size: 17px; letter-spacing: .18em; text-transform: uppercase; }}
    .scene-copy h2 {{ margin: 0; font-size: 72px; line-height: .92; letter-spacing: -.07em; max-width: 620px; text-wrap: balance; }}
    .scene-copy p {{ margin: 0; color: var(--muted); font-size: 24px; line-height: 1.36; max-width: 610px; }}
    .kinetic-row {{ display: flex; flex-wrap: wrap; gap: 10px; margin-top: 8px; }}
    .kinetic-chip {{ padding: 10px 14px; border-radius: 999px; background: rgba(255,255,255,.1); border: 1px solid rgba(255,255,255,.15); color: rgba(255,255,255,.82); font-size: 15px; font-weight: 800; }}
    .beat-stack {{ position: relative; min-height: 152px; margin-top: 8px; }}
    .beat-layer {{ position: absolute; inset: 0 auto auto 0; max-width: 540px; padding: 16px 18px; border-radius: 24px; border: 1px solid rgba(255,255,255,.14); background: rgba(255,255,255,.085); box-shadow: 0 20px 70px rgba(0,0,0,.18); opacity: 0; transform: translateY(18px); backdrop-filter: blur(16px); }}
    .beat-layer strong {{ display: block; margin-bottom: 6px; color: #fff4bf; font-size: 13px; letter-spacing: .16em; text-transform: uppercase; }}
    .beat-layer span {{ display: block; color: rgba(255,255,255,.80); font-size: 18px; line-height: 1.32; }}
    .scene-visual {{ position: relative; min-height: 470px; perspective: 1200px; }}
    .visual-card {{ position: absolute; inset: 18px 0 0 28px; border-radius: 38px; background: linear-gradient(145deg, {card_from}, {card_to}); color: #111; box-shadow: 0 34px 110px rgba(0,0,0,.38), inset 0 0 0 1px rgba(255,255,255,.72); overflow: hidden; transform-origin: 50% 50%; }}
    .visual-card::after {{ content: ""; position: absolute; inset: 0; background: linear-gradient(115deg, rgba(255,255,255,.72), rgba(255,255,255,0) 36%, rgba(124,92,255,.14)); pointer-events: none; }}
    .composition-badge {{ position: absolute; right: 54px; top: 84px; z-index: 22; min-width: 188px; padding: 10px 12px; border-radius: 18px; color: rgba(255,255,255,.82); background: rgba(0,0,0,.34); border: 1px solid rgba(255,255,255,.14); box-shadow: 0 18px 60px rgba(0,0,0,.22); backdrop-filter: blur(18px); display: grid; grid-template-columns: 1fr auto; gap: 4px 10px; }}
    .composition-badge span {{ color: #fff4bf; font-size: 11px; font-weight: 950; letter-spacing: .16em; }}
    .composition-badge b {{ font-size: 18px; line-height: 1; color: white; }}
    .composition-badge em {{ grid-column: 1 / -1; font-style: normal; font-size: 12px; color: rgba(255,255,255,.66); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
    .browser-top {{ height: 56px; display: flex; align-items: center; justify-content: space-between; padding: 0 22px; border-bottom: 1px solid rgba(0,0,0,.08); font-size: 13px; font-weight: 900; color: #6c6477; }}
    .dots {{ display: flex; gap: 8px; }} .dots i {{ width: 11px; height: 11px; border-radius: 50%; background: #ff6b5d; }} .dots i:nth-child(2) {{ background: #ffc857; }} .dots i:nth-child(3) {{ background: #39d98a; }}
    .product-ui {{ padding: 24px; display: grid; gap: 17px; }}
    .search {{ height: 58px; border-radius: 20px; background: #fff; border: 1px solid rgba(0,0,0,.08); display: flex; align-items: center; padding: 0 20px; color: #817991; font-size: 19px; box-shadow: 0 18px 44px rgba(79,69,150,.12); }}
    .voice-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; }}
    .voice {{ min-height: 116px; border-radius: 24px; background: rgba(255,255,255,.74); border: 1px solid rgba(0,0,0,.08); padding: 15px; display: grid; grid-template-columns: 58px 1fr; gap: 12px; align-items: center; }}
    .portrait {{ width: 58px; height: 58px; border-radius: 20px; background: linear-gradient(135deg, #19162a, var(--accent)); box-shadow: inset 0 0 0 1px rgba(255,255,255,.22); }}
    .name {{ font-size: 19px; font-weight: 950; }}
    .desc {{ color: #665f70; font-size: 13px; line-height: 1.32; margin-top: 4px; }}
    .waveform {{ height: 86px; border-radius: 24px; background: #11131c; padding: 18px 22px; display: flex; align-items: end; gap: 6px; box-shadow: inset 0 0 0 1px rgba(255,255,255,.08); }}
    .waveform i {{ flex: 1; min-width: 4px; border-radius: 999px; background: linear-gradient(180deg, #fff2a8, #7c5cff); height: 24px; }}
    .shot-canvas {{ min-height: 414px; padding: 24px; display: grid; gap: 18px; }}
    .site-window {{ min-height: 270px; border-radius: 30px; padding: 28px; background: rgba(255,255,255,.76); border: 1px solid rgba(0,0,0,.08); display: flex; flex-direction: column; justify-content: center; }}
    .site-screenshot {{ margin: 0; min-height: 176px; border-radius: 28px; overflow: hidden; background: linear-gradient(145deg, rgba(17,19,28,.96), rgba(35,30,50,.92)); border: 1px solid rgba(0,0,0,.10); box-shadow: 0 26px 74px rgba(0,0,0,.24), inset 0 0 0 1px rgba(255,255,255,.18); position: relative; --shot-pan: 0; --shot-zoom: 1; --crop-x: 50%; --crop-y: 24%; --crop-zoom: 1; --hl-left: 12%; --hl-top: 18%; --hl-width: 46%; --hl-height: 28%; --glow: .18; }}
    .site-screenshot::before {{ content: ""; position: absolute; inset: 0; z-index: 3; pointer-events: none; background: linear-gradient(120deg, rgba(255,255,255,.30), rgba(255,255,255,0) 22%, rgba(255,244,191,.10) 62%, rgba(255,255,255,0)); opacity: .74; mix-blend-mode: screen; }}
    .site-screenshot::after {{ content: ""; position: absolute; inset: 0; z-index: 4; pointer-events: none; box-shadow: inset 0 0 0 1px rgba(255,255,255,.22), inset 0 -48px 70px rgba(0,0,0,.26), 0 0 calc(38px * var(--glow)) rgba(255,244,191,.42); border-radius: inherit; }}
    .site-shot-top {{ height: 28px; display: flex; align-items: center; gap: 8px; padding: 0 12px; color: rgba(255,255,255,.72); background: rgba(11,12,18,.88); border-bottom: 1px solid rgba(255,255,255,.10); font-size: 10px; font-weight: 900; letter-spacing: .08em; text-transform: uppercase; position: relative; z-index: 5; }}
    .site-shot-top i {{ width: 7px; height: 7px; border-radius: 50%; background: #ff6b5d; box-shadow: 12px 0 0 #ffc857, 24px 0 0 #39d98a; margin-right: 24px; }}
    .site-shot-top b {{ margin-left: auto; color: #fff4bf; font-size: 10px; }}
    .site-shot-frame {{ position: relative; height: 190px; overflow: hidden; background: #10121a; }}
    .site-shot-frame img {{ width: 100%; height: 100%; object-fit: cover; object-position: calc(var(--crop-x) + var(--shot-pan) * 18%) var(--crop-y); display: block; filter: saturate(1.06) contrast(1.04) brightness(.98); transform: scale(calc(var(--shot-zoom) * var(--crop-zoom))); transform-origin: var(--crop-x) var(--crop-y); will-change: transform, object-position; }}
    .site-shot-ruler {{ position: absolute; right: 10px; top: 42px; bottom: 38px; z-index: 6; width: 3px; border-radius: 999px; background: rgba(255,255,255,.18); overflow: hidden; }}
    .site-shot-ruler i {{ display: block; width: 100%; height: 34%; border-radius: inherit; background: linear-gradient(180deg, #fff4bf, var(--accent)); transform: translateY(calc(var(--scroll-ratio, 0) * 188%)); }}
    .site-scan-highlight {{ position: absolute; left: var(--hl-left); top: var(--hl-top); width: var(--hl-width); height: var(--hl-height); z-index: 7; border-radius: 16px; border: 2px solid rgba(255,244,191,.92); background: linear-gradient(115deg, rgba(255,244,191,.18), rgba(124,92,255,.12)); box-shadow: 0 0 0 999px rgba(8,7,13,.22), 0 18px 54px rgba(255,212,154,.24), 0 0 26px rgba(255,244,191,.42); opacity: 0; transform: translateY(10px) scale(.97); will-change: opacity, transform; --sweep: -110%; }}
    .site-scan-highlight::after {{ content: ""; position: absolute; inset: -2px; border-radius: inherit; background: linear-gradient(100deg, transparent, rgba(255,255,255,.52), transparent); transform: translateX(var(--sweep)); opacity: .86; }}
    .site-scan-highlight b {{ position: absolute; left: 10px; top: -32px; max-width: 320px; padding: 6px 10px; border-radius: 999px; color: #11131c; background: #fff4bf; font-size: 11px; font-weight: 950; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; box-shadow: 0 10px 28px rgba(0,0,0,.18); }}
    .site-screenshot figcaption {{ position: absolute; left: 12px; bottom: 10px; z-index: 6; padding: 6px 9px; border-radius: 999px; color: white; background: rgba(0,0,0,.62); font-size: 11px; font-weight: 900; letter-spacing: .04em; backdrop-filter: blur(10px); }}
    .site-nav {{ display: flex; gap: 8px; flex-wrap: wrap; color: #5f5869; font-size: 13px; font-weight: 900; }}
    .site-nav span {{ padding: 8px 10px; border-radius: 999px; background: rgba(17,19,28,.07); }}
    .site-nav.large {{ justify-content: space-between; border-radius: 24px; padding: 15px; background: rgba(255,255,255,.72); }}
    .site-window h3, .shot-cta h3 {{ margin: 22px 0 10px; font-size: 48px; line-height: .98; letter-spacing: -.055em; }}
    .site-window p, .shot-cta p, .shot-trust p {{ margin: 0; color: #625b6d; font-size: 18px; line-height: 1.38; }}
    .hero-marks, .cta-row {{ display: flex; gap: 10px; flex-wrap: wrap; margin-top: 22px; }}
    .hero-marks i, .cta-row span {{ font-style: normal; padding: 10px 13px; border-radius: 999px; color: #11131c; background: #fff3c8; font-weight: 950; }}
    .scan-line {{ height: 5px; border-radius: 999px; background: linear-gradient(90deg, transparent, var(--accent), #fff3c8, transparent); box-shadow: 0 0 28px rgba(124,92,255,.38); }}
    .route-map {{ display: grid; grid-template-columns: auto 1fr auto 1fr auto 1fr auto; align-items: center; gap: 10px; color: #312b3b; font-weight: 950; }}
    .route-map b {{ display: block; height: 2px; border-radius: 999px; background: rgba(49,43,59,.18); }}
    .info-grid, .feature-stack, .evidence-row {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; }}
    .info-card {{ min-height: 92px; border-radius: 22px; padding: 14px; background: rgba(255,255,255,.70); border: 1px solid rgba(0,0,0,.08); display: flex; flex-direction: column; justify-content: center; }}
    .info-card b {{ color: #201b2b; font-size: 17px; line-height: 1.12; }}
    .info-card span {{ color: #665f70; font-size: 13px; line-height: 1.32; margin-top: 6px; }}
    .shot-feature {{ grid-template-columns: .94fr 1.06fr; align-items: stretch; }}
    .shot-feature .site-screenshot {{ grid-column: 1 / -1; min-height: 148px; }}
    .shot-feature .site-shot-frame {{ height: 160px; }}
    .shot-trust .site-screenshot, .shot-cta .site-screenshot {{ width: 100%; min-height: 150px; }}
    .shot-trust .site-shot-frame, .shot-cta .site-shot-frame {{ height: 166px; }}
    .zoom-lens {{ border-radius: 34px; padding: 24px; color: white; background: radial-gradient(circle at 28% 20%, rgba(255,255,255,.24), transparent 32%), linear-gradient(145deg, #16131f, var(--accent)); display: flex; flex-direction: column; justify-content: end; box-shadow: inset 0 0 0 1px rgba(255,255,255,.18); }}
    .zoom-lens strong {{ font-size: 52px; line-height: .9; letter-spacing: -.055em; }}
    .zoom-lens span {{ margin-top: 14px; color: rgba(255,255,255,.76); font-weight: 800; }}
    .shot-trust blockquote {{ margin: 0; border-radius: 32px; padding: 28px; background: #11131c; color: #fff4bf; font-size: 36px; line-height: 1.05; letter-spacing: -.045em; font-weight: 950; }}
    .evidence-row {{ grid-template-columns: repeat(4, 1fr); }}
    .shot-cta {{ place-items: center; text-align: center; }}
    .summary-orb {{ width: 116px; height: 116px; border-radius: 38px; display: grid; place-items: center; color: #11131c; background: linear-gradient(135deg, #fff, #fff3c8, var(--accent)); font-size: 38px; font-weight: 1000; box-shadow: 0 28px 90px rgba(124,92,255,.28); }}
    .shot-cta h3 {{ max-width: 560px; }}
    .shot-cta p {{ max-width: 580px; }}
    .shot-cta .waveform {{ width: 100%; }}
    .shot-hero .waveform, .shot-nav .waveform {{ height: 72px; }}
    .story-scene[data-shot="hero-overview"] .scene-grid {{ grid-template-columns: 1.05fr .95fr; }}
    .story-scene[data-shot="nav-scan"] .scene-grid {{ grid-template-columns: .78fr 1.22fr; }}
    .story-scene[data-shot="feature-zoom"] .scene-grid {{ grid-template-columns: .82fr 1.18fr; }}
    .story-scene[data-shot="trust-message"] .scene-grid {{ grid-template-columns: .92fr 1.08fr; }}
    .story-scene[data-shot="cta-summary"] .scene-grid {{ grid-template-columns: 1fr 1fr; }}
    [data-site-mode="evidence-clean"] .timeline-nav,
    [data-site-mode="evidence-clean"] .spark,
    [data-site-mode="evidence-clean"] .orb,
    [data-site-mode="evidence-clean"] .focus-ring {{ display: none; }}
    [data-site-mode="evidence-clean"] .mesh {{ opacity: .58; filter: blur(2px) saturate(.92); }}
    [data-site-mode="evidence-clean"] .brand-rail {{ top: 30px; left: 44px; right: 44px; opacity: .88; }}
    [data-site-mode="evidence-clean"] .brand {{ font-size: 19px; gap: 10px; }}
    [data-site-mode="evidence-clean"] .brand-mark {{ width: 30px; height: 30px; border-radius: 10px; }}
    [data-site-mode="evidence-clean"] .story-scene {{ padding: 94px 66px 82px; }}
    [data-site-mode="evidence-clean"] .story-scene[data-composition-mode] .eyebrow,
    [data-site-mode="evidence-clean"] .story-scene[data-composition-mode] .kinetic-row,
    [data-site-mode="evidence-clean"] .story-scene[data-composition-mode] .beat-stack,
    [data-site-mode="evidence-clean"] .story-scene[data-composition-mode] .waveform,
    [data-site-mode="evidence-clean"] .story-scene[data-composition-mode] .browser-top,
    [data-site-mode="evidence-clean"] .story-scene[data-composition-mode] .composition-badge {{ display: none; }}
    [data-site-mode="evidence-clean"] .story-scene[data-composition-mode] .scene-grid {{ gap: 34px; }}
    [data-site-mode="evidence-clean"] .story-scene[data-composition-mode] .scene-copy {{ gap: 16px; }}
    [data-site-mode="evidence-clean"] .story-scene[data-composition-mode] .scene-copy h2 {{ font-size: 54px; line-height: .97; max-width: 540px; letter-spacing: -.058em; }}
    [data-site-mode="evidence-clean"] .story-scene[data-composition-mode] .scene-copy p {{ font-size: 19px; line-height: 1.44; max-width: 500px; color: var(--muted); }}
    [data-site-mode="evidence-clean"] .story-scene[data-composition-mode] .visual-card {{ box-shadow: 0 30px 92px rgba(0,0,0,.34), inset 0 0 0 1px rgba(255,255,255,.58); }}
    [data-site-mode="evidence-clean"] .story-scene[data-composition-mode] .visual-card::after {{ opacity: .36; }}
    [data-site-mode="evidence-clean"] .story-scene[data-composition-mode] .shot-canvas {{ gap: 0; }}
    [data-site-mode="evidence-clean"] .story-scene[data-composition-mode] .site-window {{ display: none; }}
    [data-site-mode="evidence-clean"] .story-scene[data-composition-mode] .info-grid .info-card:nth-child(n+3),
    [data-site-mode="evidence-clean"] .story-scene[data-composition-mode] .feature-stack .info-card:nth-child(n+3),
    [data-site-mode="evidence-clean"] .story-scene[data-composition-mode] .evidence-row .info-card:nth-child(n+3) {{ display: none; }}
    [data-site-mode="evidence-clean"] .story-scene[data-composition-mode] .route-map,
    [data-site-mode="evidence-clean"] .story-scene[data-composition-mode] .site-nav.large,
    [data-site-mode="evidence-clean"] .story-scene[data-composition-mode] .scan-line {{ display: none; }}
    .story-scene[data-composition-mode="full-bleed"] {{ padding: 86px 52px 68px; }}
    .story-scene[data-composition-mode="full-bleed"] .scene-grid {{ grid-template-columns: 1fr; gap: 0; }}
    .story-scene[data-composition-mode="full-bleed"] .scene-copy {{ position: absolute; left: 74px; bottom: 92px; z-index: 12; max-width: 590px; padding: 24px 26px; border-radius: 32px; background: rgba(0,0,0,.42); border: 1px solid rgba(255,255,255,.16); box-shadow: 0 24px 90px rgba(0,0,0,.28); backdrop-filter: blur(18px); }}
    .story-scene[data-composition-mode="full-bleed"] .scene-copy h2 {{ font-size: 58px; max-width: 540px; }}
    .story-scene[data-composition-mode="full-bleed"] .scene-copy p {{ font-size: 20px; max-width: 520px; }}
    .story-scene[data-composition-mode="full-bleed"] .scene-visual {{ min-height: 556px; }}
    .story-scene[data-composition-mode="full-bleed"] .visual-card {{ inset: 0; border-radius: 44px; }}
    .story-scene[data-composition-mode="full-bleed"] .shot-canvas {{ min-height: 500px; grid-template-columns: 1fr; align-items: stretch; padding: 18px; }}
    .story-scene[data-composition-mode="full-bleed"] .site-screenshot {{ min-height: 452px; align-self: stretch; }}
    .story-scene[data-composition-mode="full-bleed"] .site-shot-frame {{ height: 424px; }}
    .story-scene[data-composition-mode="full-bleed"] .waveform {{ position: absolute; right: 28px; bottom: 28px; width: 360px; height: 64px; opacity: .84; }}
    .story-scene[data-composition-mode="split-scan"] .scene-grid {{ grid-template-columns: .66fr 1.34fr; }}
    .story-scene[data-composition-mode="split-scan"] .visual-card {{ inset: 0 0 0 12px; }}
    .story-scene[data-composition-mode="split-scan"] .site-screenshot {{ min-height: 220px; }}
    .story-scene[data-composition-mode="split-scan"] .site-shot-frame {{ height: 232px; }}
    .story-scene[data-composition-mode="zoom-callout"] .scene-grid {{ grid-template-columns: .58fr 1.42fr; }}
    .story-scene[data-composition-mode="zoom-callout"] .visual-card {{ inset: -8px -6px -4px 8px; border-radius: 46px; }}
    .story-scene[data-composition-mode="zoom-callout"] .zoom-lens {{ min-height: 238px; }}
    .story-scene[data-composition-mode="zoom-callout"] .site-screenshot {{ min-height: 218px; }}
    .story-scene[data-composition-mode="zoom-callout"] .site-shot-frame {{ height: 230px; }}
    .story-scene[data-composition-mode="evidence-board"] .scene-grid {{ grid-template-columns: .95fr 1.05fr; }}
    .story-scene[data-composition-mode="evidence-board"] .shot-canvas {{ grid-template-columns: 1fr; }}
    .story-scene[data-composition-mode="evidence-board"] .evidence-row {{ grid-template-columns: repeat(2, 1fr); }}
    .story-scene[data-composition-mode="evidence-board"] .site-screenshot {{ min-height: 236px; }}
    .story-scene[data-composition-mode="evidence-board"] .site-shot-frame {{ height: 248px; }}
    .story-scene[data-composition-mode="cta-lockup"] .scene-grid {{ grid-template-columns: .78fr 1.22fr; }}
    .story-scene[data-composition-mode="cta-lockup"] .visual-card {{ inset: 4px 18px 8px 0; border-radius: 50px; }}
    .story-scene[data-composition-mode="cta-lockup"] .shot-cta {{ align-content: center; }}
    .story-scene[data-composition-mode="cta-lockup"] .summary-orb {{ width: 136px; height: 136px; border-radius: 44px; }}
    .story-scene[data-composition-mode="cta-lockup"] .site-screenshot {{ max-width: 650px; }}
    [data-site-mode="evidence-clean"] .clean-shot {{ position: relative; min-height: 414px; padding: 16px; display: grid; grid-template-columns: 1fr; align-items: stretch; }}
    [data-site-mode="evidence-clean"] .clean-shot .site-screenshot {{ min-height: 382px; align-self: stretch; }}
    [data-site-mode="evidence-clean"] .clean-shot .site-shot-frame {{ height: 354px; }}
    [data-site-mode="evidence-clean"] .site-shot-top {{ height: 24px; padding: 0 10px; font-size: 9px; background: rgba(11,12,18,.76); }}
    [data-site-mode="evidence-clean"] .site-shot-top b,
    [data-site-mode="evidence-clean"] .site-shot-ruler,
    [data-site-mode="evidence-clean"] .site-screenshot figcaption {{ display: none; }}
    [data-site-mode="evidence-clean"] .site-scan-highlight {{ border-width: 1px; background: rgba(255,244,191,.11); box-shadow: 0 14px 44px rgba(255,212,154,.18), 0 0 18px rgba(255,244,191,.28); }}
    [data-site-mode="evidence-clean"] .site-scan-highlight b {{ top: -28px; left: 0; font-size: 10px; padding: 5px 9px; max-width: 260px; }}
    [data-site-mode="evidence-clean"] .evidence-note {{ position: absolute; left: 30px; right: 30px; bottom: 26px; z-index: 9; max-width: 440px; padding: 14px 16px; border-radius: 20px; color: white; background: rgba(8,7,13,.66); border: 1px solid rgba(255,255,255,.14); box-shadow: 0 16px 54px rgba(0,0,0,.26); backdrop-filter: blur(18px); }}
    [data-site-mode="evidence-clean"] .evidence-note small {{ display: block; margin-bottom: 6px; color: #fff4bf; font-size: 10px; font-weight: 950; letter-spacing: .16em; text-transform: uppercase; }}
    [data-site-mode="evidence-clean"] .evidence-note b {{ display: block; color: white; font-size: 18px; line-height: 1.12; letter-spacing: -.022em; }}
    [data-site-mode="evidence-clean"] .evidence-note span {{ display: block; margin-top: 6px; color: rgba(255,255,255,.72); font-size: 12px; line-height: 1.34; }}
    [data-site-mode="evidence-clean"] .evidence-note em {{ display: inline-flex; margin-top: 10px; padding: 6px 9px; border-radius: 999px; background: rgba(255,244,191,.16); color: #fff4bf; font-style: normal; font-size: 10px; font-weight: 950; letter-spacing: .08em; }}
    [data-site-mode="evidence-clean"] .story-scene[data-composition-mode="full-bleed"] {{ padding: 76px 48px 58px; }}
    [data-site-mode="evidence-clean"] .story-scene[data-composition-mode="full-bleed"] .scene-copy {{ left: 70px; bottom: 76px; max-width: 430px; padding: 18px 20px; border-radius: 26px; background: rgba(8,7,13,.46); }}
    [data-site-mode="evidence-clean"] .story-scene[data-composition-mode="full-bleed"] .scene-copy h2 {{ font-size: 36px; letter-spacing: -.048em; color: white; }}
    [data-site-mode="evidence-clean"] .story-scene[data-composition-mode="full-bleed"] .scene-copy p {{ font-size: 15px; color: rgba(255,255,255,.74); }}
    [data-site-mode="evidence-clean"] .story-scene[data-composition-mode="full-bleed"] .clean-shot {{ min-height: 520px; }}
    [data-site-mode="evidence-clean"] .story-scene[data-composition-mode="full-bleed"] .clean-shot .site-screenshot {{ min-height: 488px; }}
    [data-site-mode="evidence-clean"] .story-scene[data-composition-mode="full-bleed"] .clean-shot .site-shot-frame {{ height: 464px; }}
    [data-site-mode="evidence-clean"] .story-scene[data-composition-mode="full-bleed"] .evidence-note {{ display: none; }}
    [data-site-mode="evidence-clean"] .story-scene[data-composition-mode="zoom-callout"] .zoom-lens,
    [data-site-mode="evidence-clean"] .story-scene[data-composition-mode="evidence-board"] blockquote,
    [data-site-mode="evidence-clean"] .story-scene[data-composition-mode="evidence-board"] .shot-trust > p,
    [data-site-mode="evidence-clean"] .story-scene[data-composition-mode="cta-lockup"] .summary-orb,
    [data-site-mode="evidence-clean"] .story-scene[data-composition-mode="cta-lockup"] .cta-row {{ display: none; }}
    [data-site-mode="editorial-pro"] .timeline-nav,
    [data-site-mode="editorial-pro"] .spark,
    [data-site-mode="editorial-pro"] .orb,
    [data-site-mode="editorial-pro"] .focus-ring {{ display: none; }}
    [data-site-mode="editorial-pro"] .mesh {{ opacity: .36; filter: saturate(.72) contrast(.94); }}
    [data-site-mode="editorial-pro"] .grain {{ opacity: .16; }}
    [data-site-mode="editorial-pro"] .brand-rail {{ top: 30px; left: 54px; right: 54px; opacity: .92; }}
    [data-site-mode="editorial-pro"] .brand {{ gap: 10px; font-size: 18px; letter-spacing: -.025em; }}
    [data-site-mode="editorial-pro"] .brand-mark {{ width: 28px; height: 28px; border-radius: 7px; box-shadow: none; background: rgba(255,255,255,.72); }}
    [data-site-mode="editorial-pro"] .story-scene {{ padding: 92px 58px 78px; }}
    [data-site-mode="editorial-pro"] .story-scene[data-composition-mode] .eyebrow,
    [data-site-mode="editorial-pro"] .story-scene[data-composition-mode] .kinetic-row,
    [data-site-mode="editorial-pro"] .story-scene[data-composition-mode] .beat-stack,
    [data-site-mode="editorial-pro"] .story-scene[data-composition-mode] .waveform,
    [data-site-mode="editorial-pro"] .story-scene[data-composition-mode] .browser-top,
    [data-site-mode="editorial-pro"] .story-scene[data-composition-mode] .composition-badge,
    [data-site-mode="editorial-pro"] .story-scene[data-composition-mode] .route-map,
    [data-site-mode="editorial-pro"] .story-scene[data-composition-mode] .site-nav.large,
    [data-site-mode="editorial-pro"] .story-scene[data-composition-mode] .scan-line {{ display: none; }}
    [data-site-mode="editorial-pro"] .story-scene[data-composition-mode] .scene-grid {{ grid-template-columns: .46fr 1.54fr; gap: 44px; align-items: center; }}
    [data-site-mode="editorial-pro"] .story-scene[data-composition-mode] .scene-copy {{ align-self: center; gap: 13px; padding-top: 10px; border-top: 1px solid rgba(22,20,18,.28); }}
    [data-site-mode="editorial-pro"] .story-scene[data-composition-mode] .scene-copy h2 {{ max-width: 360px; font-size: 37px; line-height: 1.05; letter-spacing: -.038em; color: var(--ink); overflow-wrap: anywhere; word-break: normal; text-wrap: balance; }}
    [data-site-mode="editorial-pro"] .story-scene[data-composition-mode] .scene-copy p {{ max-width: 340px; color: rgba(22,20,18,.66); font-size: 15px; line-height: 1.48; overflow-wrap: anywhere; }}
    [data-site-mode="editorial-pro"] .story-scene[data-composition-mode] .scene-visual {{ min-height: 492px; }}
    [data-site-mode="editorial-pro"] .story-scene[data-composition-mode] .visual-card {{ inset: 0; border-radius: 18px; background: transparent; box-shadow: none; overflow: visible; }}
    [data-site-mode="editorial-pro"] .story-scene[data-composition-mode] .visual-card::after {{ display: none; }}
    [data-site-mode="editorial-pro"] .story-scene[data-composition-mode] .shot-canvas {{ gap: 0; padding: 0; }}
    [data-site-mode="editorial-pro"] .story-scene[data-composition-mode] .site-window,
    [data-site-mode="editorial-pro"] .story-scene[data-composition-mode] .info-grid .info-card:nth-child(n+2),
    [data-site-mode="editorial-pro"] .story-scene[data-composition-mode] .feature-stack .info-card:nth-child(n+2),
    [data-site-mode="editorial-pro"] .story-scene[data-composition-mode] .evidence-row .info-card:nth-child(n+2) {{ display: none; }}
    [data-site-mode="editorial-pro"] .clean-shot {{ position: relative; min-height: 450px; display: grid; grid-template-columns: 1fr; align-items: stretch; }}
    [data-site-mode="editorial-pro"] .clean-shot .site-screenshot {{ min-height: 438px; border-radius: 12px; background: #f5f1ea; border: 1px solid rgba(22,20,18,.20); box-shadow: 0 28px 76px rgba(22,20,18,.16); }}
    [data-site-mode="editorial-pro"] .clean-shot .site-shot-frame {{ height: 410px; background: #f5f1ea; }}
    [data-site-mode="editorial-pro"] .site-shot-frame img {{ filter: saturate(.88) contrast(.98) brightness(1.01); }}
    [data-site-mode="editorial-pro"] .site-screenshot::before {{ opacity: .16; }}
    [data-site-mode="editorial-pro"] .site-screenshot::after {{ box-shadow: inset 0 0 0 1px rgba(255,255,255,.20); }}
    [data-site-mode="editorial-pro"] .site-shot-top {{ height: 22px; padding: 0 10px; color: rgba(255,255,255,.66); background: rgba(22,20,18,.88); font-size: 9px; letter-spacing: .14em; }}
    [data-site-mode="editorial-pro"] .site-shot-top b,
    [data-site-mode="editorial-pro"] .site-shot-ruler,
    [data-site-mode="editorial-pro"] .site-screenshot figcaption {{ display: none; }}
    [data-site-mode="editorial-pro"] .site-scan-highlight {{ display: none; }}
    [data-site-mode="editorial-pro"] .site-scan-highlight::after {{ opacity: .12; }}
    [data-site-mode="editorial-pro"] .site-scan-highlight b {{ top: -23px; left: 0; padding: 3px 6px; border-radius: 1px; background: rgba(22,20,18,.82); color: #f4ead9; font-size: 8px; font-weight: 800; letter-spacing: .02em; }}
    [data-site-mode="editorial-pro"] .evidence-note {{ display: none; }}
    [data-site-mode="editorial-pro"] .evidence-note small {{ display: block; margin-bottom: 7px; color: rgba(22,20,18,.55); font-size: 9px; font-weight: 900; letter-spacing: .18em; text-transform: uppercase; }}
    [data-site-mode="editorial-pro"] .evidence-note b {{ display: block; color: var(--ink); font-size: 17px; line-height: 1.12; letter-spacing: -.018em; }}
    [data-site-mode="editorial-pro"] .evidence-note span {{ display: block; margin-top: 7px; color: rgba(22,20,18,.62); font-size: 12px; line-height: 1.38; }}
    [data-site-mode="editorial-pro"] .evidence-note em {{ display: inline-block; margin-top: 9px; padding: 0; border-radius: 0; background: transparent; color: rgba(22,20,18,.72); font-style: normal; font-size: 10px; font-weight: 850; letter-spacing: .08em; text-transform: uppercase; }}
    [data-site-mode="editorial-pro"] .story-scene[data-composition-mode="full-bleed"] {{ padding: 74px 50px 62px; }}
    [data-site-mode="editorial-pro"] .story-scene[data-composition-mode="full-bleed"] .scene-grid {{ grid-template-columns: 1fr; gap: 0; }}
    [data-site-mode="editorial-pro"] .story-scene[data-composition-mode="full-bleed"] .scene-copy {{ position: absolute; left: 70px; top: 112px; bottom: auto; z-index: 12; max-width: 318px; padding: 14px 0 0; border-radius: 0; border-top: 1px solid rgba(22,20,18,.44); background: transparent; box-shadow: none; backdrop-filter: none; }}
    [data-site-mode="editorial-pro"] .story-scene[data-composition-mode="full-bleed"] .scene-copy h2 {{ max-width: 300px; font-size: 34px; line-height: 1.06; color: var(--ink); overflow-wrap: anywhere; text-wrap: balance; }}
    [data-site-mode="editorial-pro"] .story-scene[data-composition-mode="full-bleed"] .scene-copy p {{ max-width: 292px; font-size: 14px; color: rgba(22,20,18,.60); overflow-wrap: anywhere; }}
    [data-site-mode="editorial-pro"] .story-scene[data-composition-mode="full-bleed"] .scene-visual {{ min-height: 560px; }}
    [data-site-mode="editorial-pro"] .story-scene[data-composition-mode="full-bleed"] .clean-shot {{ min-height: 520px; }}
    [data-site-mode="editorial-pro"] .story-scene[data-composition-mode="full-bleed"] .clean-shot .site-screenshot {{ min-height: 506px; margin-left: 330px; }}
    [data-site-mode="editorial-pro"] .story-scene[data-composition-mode="full-bleed"] .clean-shot .site-shot-frame {{ height: 484px; }}
    [data-site-mode="editorial-pro"] .story-scene[data-composition-mode="full-bleed"] .evidence-note {{ display: none; }}
    [data-site-mode="editorial-pro"] .story-scene[data-composition-mode="zoom-callout"] .zoom-lens,
    [data-site-mode="editorial-pro"] .story-scene[data-composition-mode="evidence-board"] blockquote,
    [data-site-mode="editorial-pro"] .story-scene[data-composition-mode="evidence-board"] .shot-trust > p,
    [data-site-mode="editorial-pro"] .story-scene[data-composition-mode="cta-lockup"] .summary-orb,
    [data-site-mode="editorial-pro"] .story-scene[data-composition-mode="cta-lockup"] .cta-row {{ display: none; }}
    [data-site-mode="editorial-pro"] .caption {{ bottom: 28px; min-width: 0; max-width: 700px; padding: 8px 12px; border-radius: 3px; background: rgba(22,20,18,.68); color: #f7efe4; font-size: 15px; line-height: 1.34; font-weight: 620; box-shadow: none; backdrop-filter: blur(10px); }}
    [data-style-preset="executive-film"]::before,
    [data-style-preset="executive-film"]::after {{ content: ""; position: absolute; left: 0; right: 0; height: 54px; z-index: 40; pointer-events: none; background: #050505; }}
    [data-style-preset="executive-film"]::before {{ top: 0; }}
    [data-style-preset="executive-film"]::after {{ bottom: 0; }}
    [data-style-preset="executive-film"] .timeline-nav,
    [data-style-preset="executive-film"] .spark,
    [data-style-preset="executive-film"] .orb,
    [data-style-preset="executive-film"] .focus-ring,
    [data-style-preset="executive-film"] .composition-badge,
    [data-style-preset="executive-film"] .browser-top,
    [data-style-preset="executive-film"] .kinetic-row,
    [data-style-preset="executive-film"] .beat-stack,
    [data-style-preset="executive-film"] .waveform {{ display: none; }}
    [data-style-preset="executive-film"] .mesh {{ opacity: .52; filter: blur(8px) saturate(.72); }}
    [data-style-preset="executive-film"] .grain {{ opacity: .11; mix-blend-mode: soft-light; }}
    [data-style-preset="executive-film"] .brand-rail {{ top: 72px; left: 72px; right: 72px; opacity: .82; font-weight: 720; letter-spacing: .02em; text-transform: uppercase; }}
    [data-style-preset="executive-film"] .brand {{ font-size: 12px; gap: 11px; color: rgba(244,239,230,.70); }}
    [data-style-preset="executive-film"] .brand-mark {{ width: 9px; height: 9px; border-radius: 50%; background: var(--accent); box-shadow: 0 0 22px rgba(214,193,154,.34); }}
    [data-style-preset="executive-film"] .story-scene {{ padding: 116px 78px 88px; }}
    [data-style-preset="executive-film"] .story-scene::before {{ content: attr(data-material-role); position: absolute; left: 78px; bottom: 74px; z-index: 6; color: rgba(244,239,230,.32); font-size: 10px; font-weight: 800; letter-spacing: .24em; text-transform: uppercase; }}
    [data-style-preset="executive-film"] .scene-grid {{ grid-template-columns: .88fr 1.12fr; gap: 78px; align-items: center; }}
    [data-style-preset="executive-film"] .scene-copy {{ gap: 22px; padding-top: 26px; border-top: 1px solid rgba(214,193,154,.32); }}
    [data-style-preset="executive-film"] .story-scene[data-composition-mode] .scene-copy {{ border-radius: 0; background: transparent; box-shadow: none; backdrop-filter: none; border-left: 0; border-right: 0; border-bottom: 0; }}
    [data-style-preset="executive-film"] .story-scene[data-composition-mode="full-bleed"] .scene-copy {{ position: relative; left: auto; top: auto; bottom: auto; max-width: none; padding: 26px 0 0; border-radius: 0; background: transparent; box-shadow: none; backdrop-filter: none; }}
    [data-style-preset="executive-film"] .eyebrow {{ color: rgba(214,193,154,.78); font-size: 11px; letter-spacing: .26em; font-weight: 760; }}
    [data-style-preset="executive-film"] .scene-copy h2 {{ max-width: 610px; font-size: 64px; line-height: .95; letter-spacing: -.056em; color: #f5efe5; font-weight: 760; }}
    [data-style-preset="executive-film"] .scene-copy p {{ max-width: 520px; color: rgba(244,239,230,.58); font-size: 18px; line-height: 1.52; font-weight: 460; }}
    [data-style-preset="executive-film"] .beat-stack {{ min-height: 112px; margin-top: 28px; }}
    [data-style-preset="executive-film"] .beat-layer {{ max-width: 520px; padding: 16px 0 0; border: 0; border-top: 1px solid rgba(244,239,230,.18); border-radius: 0; background: transparent; box-shadow: none; backdrop-filter: none; }}
    [data-style-preset="executive-film"] .beat-layer strong {{ color: rgba(214,193,154,.78); font-size: 10px; letter-spacing: .22em; font-weight: 760; }}
    [data-style-preset="executive-film"] .beat-layer span {{ color: rgba(244,239,230,.72); font-size: 16px; line-height: 1.48; font-weight: 520; }}
    [data-style-preset="executive-film"] .scene-visual {{ min-height: 456px; }}
    [data-style-preset="executive-film"] .visual-card {{ inset: 0; border-radius: 0; background: transparent; color: #f4efe6; box-shadow: none; overflow: visible; }}
    [data-style-preset="executive-film"] .visual-card::after {{ display: none; }}
    [data-style-preset="executive-film"] .shot-canvas {{ min-height: 456px; padding: 0; gap: 18px; }}
    [data-style-preset="executive-film"] .site-window {{ min-height: 352px; border-radius: 0; padding: 34px 36px; background: linear-gradient(135deg, rgba(244,239,230,.08), rgba(244,239,230,.02)); border: 1px solid rgba(244,239,230,.16); box-shadow: inset 0 0 0 1px rgba(255,255,255,.025), 0 42px 110px rgba(0,0,0,.32); }}
    [data-style-preset="executive-film"] .site-nav span {{ border-radius: 0; background: transparent; border-bottom: 1px solid rgba(214,193,154,.28); color: rgba(244,239,230,.54); padding: 0 0 5px; font-size: 10px; letter-spacing: .16em; text-transform: uppercase; }}
    [data-style-preset="executive-film"] .site-window h3,
    [data-style-preset="executive-film"] .shot-cta h3 {{ color: #f5efe5; font-size: 56px; line-height: .94; letter-spacing: -.052em; font-weight: 760; }}
    [data-style-preset="executive-film"] .site-window p,
    [data-style-preset="executive-film"] .shot-cta p,
    [data-style-preset="executive-film"] .shot-trust p {{ color: rgba(244,239,230,.56); font-size: 16px; line-height: 1.5; }}
    [data-style-preset="executive-film"] .hero-marks i,
    [data-style-preset="executive-film"] .cta-row span {{ border-radius: 0; color: rgba(244,239,230,.74); background: transparent; border: 1px solid rgba(214,193,154,.26); font-size: 11px; letter-spacing: .12em; text-transform: uppercase; }}
    [data-style-preset="executive-film"] .info-grid,
    [data-style-preset="executive-film"] .feature-stack,
    [data-style-preset="executive-film"] .evidence-row {{ gap: 1px; background: rgba(244,239,230,.12); border: 1px solid rgba(244,239,230,.12); }}
    [data-style-preset="executive-film"] .info-card {{ min-height: 112px; border-radius: 0; padding: 18px; background: rgba(10,10,9,.68); border: 0; }}
    [data-style-preset="executive-film"] .info-card b {{ color: #f5efe5; font-size: 16px; font-weight: 700; }}
    [data-style-preset="executive-film"] .info-card span {{ color: rgba(244,239,230,.48); font-size: 12px; line-height: 1.45; }}
    [data-style-preset="executive-film"] .zoom-lens {{ min-height: 312px; border-radius: 0; padding: 34px; background: linear-gradient(145deg, rgba(214,193,154,.18), rgba(244,239,230,.04)); border: 1px solid rgba(214,193,154,.18); box-shadow: none; }}
    [data-style-preset="executive-film"] .zoom-lens strong {{ color: #f5efe5; font-size: 64px; font-weight: 760; }}
    [data-style-preset="executive-film"] .zoom-lens span {{ color: rgba(244,239,230,.58); font-weight: 520; }}
    [data-style-preset="executive-film"] .shot-trust blockquote {{ border-radius: 0; padding: 34px; background: rgba(244,239,230,.07); border-left: 2px solid var(--accent); color: #f5efe5; font-size: 42px; font-weight: 740; box-shadow: none; }}
    [data-style-preset="executive-film"] .summary-orb {{ width: 112px; height: 112px; border-radius: 50%; color: #090908; background: var(--accent); font-size: 34px; box-shadow: 0 28px 88px rgba(214,193,154,.18); }}
    [data-style-preset="executive-film"] .media-prop {{ border-radius: 0; border-color: rgba(214,193,154,.24); box-shadow: 0 28px 90px rgba(0,0,0,.38); }}
    [data-style-preset="executive-film"] .abstract-shot {{ position: relative; min-height: 456px; display: grid; grid-template-columns: 1fr; align-items: stretch; }}
    [data-style-preset="executive-film"] .executive-plate {{ position: relative; min-height: 438px; overflow: hidden; background: linear-gradient(135deg, rgba(244,239,230,.075), rgba(244,239,230,.018)); border: 1px solid rgba(244,239,230,.14); box-shadow: 0 42px 120px rgba(0,0,0,.38), inset 0 0 0 1px rgba(255,255,255,.025); }}
    [data-style-preset="executive-film"] .executive-plate::before {{ content: ""; position: absolute; inset: 0; background-image: linear-gradient(rgba(244,239,230,.055) 1px, transparent 1px), linear-gradient(90deg, rgba(244,239,230,.045) 1px, transparent 1px); background-size: 72px 72px; mask-image: linear-gradient(120deg, black, transparent 72%); opacity: .66; }}
    [data-style-preset="executive-film"] .executive-plate::after {{ content: ""; position: absolute; left: -16%; right: 18%; top: 52%; height: 1px; background: linear-gradient(90deg, transparent, rgba(214,193,154,.58), transparent); transform: rotate(-18deg); transform-origin: 50% 50%; }}
    [data-style-preset="executive-film"] .plate-index {{ position: absolute; right: 34px; top: 22px; color: rgba(244,239,230,.085); font-size: 164px; line-height: .82; letter-spacing: -.08em; font-weight: 680; }}
    [data-style-preset="executive-film"] .plate-kicker {{ position: absolute; left: 32px; top: 30px; color: rgba(214,193,154,.72); font-size: 10px; font-weight: 760; letter-spacing: .26em; text-transform: uppercase; }}
    [data-style-preset="executive-film"] .plate-title {{ position: absolute; left: 32px; bottom: 42px; max-width: 460px; color: #f5efe5; font-size: 44px; line-height: .98; letter-spacing: -.048em; font-weight: 720; text-wrap: balance; }}
    [data-style-preset="executive-film"] .plate-copy {{ position: absolute; left: 34px; bottom: 22px; max-width: 420px; color: rgba(244,239,230,.44); font-size: 12px; line-height: 1.36; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
    [data-style-preset="executive-film"] .signal-field {{ position: absolute; right: 34px; bottom: 38px; width: 238px; height: 188px; border-left: 1px solid rgba(244,239,230,.18); border-bottom: 1px solid rgba(244,239,230,.18); }}
    [data-style-preset="executive-film"] .signal-field i {{ position: absolute; bottom: 0; width: 1px; background: rgba(214,193,154,.72); transform-origin: 50% 100%; }}
    [data-style-preset="executive-film"] .signal-field b {{ position: absolute; width: 7px; height: 7px; border-radius: 50%; background: var(--accent); box-shadow: 0 0 24px rgba(214,193,154,.35); }}
    [data-style-preset="executive-film"] .evidence-strips {{ position: absolute; left: 32px; right: 32px; top: 86px; display: grid; gap: 10px; }}
    [data-style-preset="executive-film"] .evidence-strips span {{ display: block; height: 1px; background: linear-gradient(90deg, rgba(244,239,230,.50), rgba(244,239,230,.10), transparent); }}
    [data-style-preset="executive-film"] .evidence-strips span:nth-child(2) {{ width: 72%; }}
    [data-style-preset="executive-film"] .evidence-strips span:nth-child(3) {{ width: 48%; }}
    [data-style-preset="executive-film"] .executive-tags {{ position: absolute; left: 32px; top: 134px; display: flex; gap: 12px; flex-wrap: wrap; max-width: 430px; }}
    [data-style-preset="executive-film"] .executive-tags span {{ padding: 6px 0; color: rgba(244,239,230,.46); border-bottom: 1px solid rgba(214,193,154,.26); font-size: 10px; font-weight: 760; letter-spacing: .18em; text-transform: uppercase; }}
    [data-style-preset="executive-film"] .content-ledger {{ position: absolute; left: 32px; top: 186px; width: 360px; z-index: 2; }}
    [data-style-preset="executive-film"] .content-ledger ul {{ list-style: none; margin: 0; padding: 0; display: grid; gap: 9px; }}
    [data-style-preset="executive-film"] .content-ledger li {{ display: grid; grid-template-columns: 72px 1fr; gap: 14px; align-items: baseline; padding: 8px 0; border-top: 1px solid rgba(244,239,230,.105); }}
    [data-style-preset="executive-film"] .content-ledger b {{ color: rgba(214,193,154,.78); font-size: 10px; letter-spacing: .16em; font-weight: 780; }}
    [data-style-preset="executive-film"] .content-ledger span {{ color: rgba(244,239,230,.66); font-size: 13px; line-height: 1.35; font-weight: 520; }}
    [data-style-preset="executive-film"] .metric-stamp {{ position: absolute; right: 38px; top: 184px; display: grid; gap: 5px; justify-items: end; color: rgba(244,239,230,.62); z-index: 2; }}
    [data-style-preset="executive-film"] .metric-stamp small {{ font-size: 10px; letter-spacing: .22em; color: rgba(214,193,154,.72); font-weight: 780; }}
    [data-style-preset="executive-film"] .metric-stamp b {{ font-size: 32px; line-height: .9; letter-spacing: -.05em; color: rgba(244,239,230,.82); font-weight: 720; }}
    [data-style-preset="executive-film"] .production-micro {{ position: absolute; right: 34px; top: 252px; width: 240px; display: grid; grid-template-columns: 1fr 1fr; gap: 8px; z-index: 2; }}
    [data-style-preset="executive-film"] .production-micro span {{ padding: 7px 8px; border: 1px solid rgba(244,239,230,.10); color: rgba(244,239,230,.42); font-size: 9px; letter-spacing: .12em; text-transform: uppercase; background: rgba(0,0,0,.18); }}
    [data-style-preset="executive-film"] .executive-layout .content-ledger li,
    [data-style-preset="executive-film"] .executive-layout .tension-grid li,
    [data-style-preset="executive-film"] .executive-layout .desk-cards li,
    [data-style-preset="executive-film"] .executive-layout .production-micro span,
    [data-style-preset="executive-film"] .executive-layout .executive-tags span,
    [data-style-preset="executive-film"] .executive-layout .desk-footer span,
    [data-style-preset="executive-film"] .executive-layout .pipeline-track span,
    [data-style-preset="executive-film"] .executive-layout .metric-stamp,
    [data-style-preset="executive-film"] .executive-layout .plate-kicker {{ opacity: 0; will-change: transform, opacity, filter, clip-path; }}
    [data-style-preset="executive-film"] .executive-layout .layout-title-slate h3,
    [data-style-preset="executive-film"] .executive-layout .layout-pipeline h3,
    [data-style-preset="executive-film"] .executive-layout .layout-final h3,
    [data-style-preset="executive-film"] .executive-layout .desk-header b,
    [data-style-preset="executive-film"] .executive-layout .tension-claim b,
    [data-style-preset="executive-film"] .executive-layout .plate-title,
    [data-style-preset="executive-film"] .executive-layout .layout-title-slate p,
    [data-style-preset="executive-film"] .executive-layout .layout-pipeline p,
    [data-style-preset="executive-film"] .executive-layout .layout-final p,
    [data-style-preset="executive-film"] .executive-layout .desk-header span,
    [data-style-preset="executive-film"] .executive-layout .tension-claim span,
    [data-style-preset="executive-film"] .executive-layout .plate-copy {{ opacity: 0; will-change: transform, opacity, clip-path; }}
    [data-style-preset="executive-film"] .executive-layout .signal-field i,
    [data-style-preset="executive-film"] .executive-layout .signal-field b,
    [data-style-preset="executive-film"] .executive-layout .evidence-strips span {{ opacity: 0; will-change: transform, opacity; }}
    [data-style-preset="executive-film"] .executive-layout-title-slate .executive-plate {{ background: radial-gradient(circle at 22% 48%, rgba(214,193,154,.16), transparent 34%), linear-gradient(135deg, rgba(244,239,230,.065), rgba(244,239,230,.012)); }}
    [data-style-preset="executive-film"] .layout-title-slate {{ position: absolute; left: 40px; right: 90px; top: 128px; z-index: 3; }}
    [data-style-preset="executive-film"] .layout-title-slate small,
    [data-style-preset="executive-film"] .layout-final small {{ display: block; color: rgba(214,193,154,.72); font-size: 11px; letter-spacing: .24em; font-weight: 780; text-transform: uppercase; margin-bottom: 18px; }}
    [data-style-preset="executive-film"] .layout-title-slate h3 {{ margin: 0; max-width: 620px; color: #f5efe5; font-size: 76px; line-height: .86; letter-spacing: -.07em; font-weight: 760; }}
    [data-style-preset="executive-film"] .layout-title-slate p {{ margin: 24px 0 0; max-width: 610px; color: rgba(244,239,230,.58); font-size: 18px; line-height: 1.44; font-weight: 500; }}
    [data-style-preset="executive-film"] .executive-layout-title-slate .executive-tags {{ top: auto; bottom: 36px; left: 40px; }}
    [data-style-preset="executive-film"] .executive-layout-title-slate .production-micro {{ top: auto; bottom: 34px; right: 36px; }}
    [data-style-preset="executive-film"] .layout-tension {{ position: absolute; inset: 38px 36px 34px 36px; z-index: 3; display: grid; grid-template-columns: 300px 1fr; gap: 36px; align-items: stretch; }}
    [data-style-preset="executive-film"] .tension-claim {{ display: flex; flex-direction: column; justify-content: flex-end; border-left: 2px solid rgba(214,193,154,.54); padding-left: 24px; }}
    [data-style-preset="executive-film"] .tension-claim small {{ color: rgba(214,193,154,.72); font-size: 10px; letter-spacing: .22em; font-weight: 780; }}
    [data-style-preset="executive-film"] .tension-claim b {{ margin-top: 18px; color: #f5efe5; font-size: 48px; line-height: .94; letter-spacing: -.05em; }}
    [data-style-preset="executive-film"] .tension-claim span {{ margin-top: 18px; color: rgba(244,239,230,.56); font-size: 15px; line-height: 1.5; }}
    [data-style-preset="executive-film"] .tension-grid ul {{ height: 100%; list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(3, 1fr); gap: 1px; background: rgba(244,239,230,.12); border: 1px solid rgba(244,239,230,.12); }}
    [data-style-preset="executive-film"] .tension-grid li {{ padding: 26px 20px; display: flex; flex-direction: column; justify-content: space-between; min-height: 240px; background: rgba(5,5,5,.68); }}
    [data-style-preset="executive-film"] .tension-grid b {{ color: rgba(214,193,154,.72); font-size: 11px; letter-spacing: .2em; }}
    [data-style-preset="executive-film"] .tension-grid span {{ color: rgba(244,239,230,.70); font-size: 17px; line-height: 1.38; font-weight: 600; }}
    [data-style-preset="executive-film"] .layout-pipeline {{ position: absolute; inset: 42px 40px 38px; z-index: 3; display: grid; grid-template-rows: auto auto 1fr auto; gap: 20px; }}
    [data-style-preset="executive-film"] .layout-pipeline h3 {{ margin: 0; max-width: 520px; color: #f5efe5; font-size: 54px; line-height: .94; letter-spacing: -.052em; }}
    [data-style-preset="executive-film"] .layout-pipeline p {{ margin: 0; max-width: 660px; color: rgba(244,239,230,.56); font-size: 15px; line-height: 1.42; }}
    [data-style-preset="executive-film"] .pipeline-track {{ position: relative; display: grid; grid-template-columns: repeat(4, 1fr); gap: 0; align-items: center; border-top: 1px solid rgba(214,193,154,.34); border-bottom: 1px solid rgba(244,239,230,.12); }}
    [data-style-preset="executive-film"] .pipeline-track span {{ position: relative; min-height: 104px; padding: 24px 18px; border-right: 1px solid rgba(244,239,230,.11); color: rgba(244,239,230,.64); font-size: 14px; letter-spacing: .12em; font-weight: 720; }}
    [data-style-preset="executive-film"] .pipeline-track i {{ position: absolute; left: 18px; right: 18px; bottom: 22px; height: 2px; background: linear-gradient(90deg, rgba(214,193,154,.85), transparent); }}
    [data-style-preset="executive-film"] .executive-layout-process-pipeline .content-ledger {{ position: relative; left: auto; top: auto; width: auto; }}
    [data-style-preset="executive-film"] .layout-desk {{ position: absolute; inset: 34px 34px 34px 34px; z-index: 3; display: grid; grid-template-columns: 310px 1fr; grid-template-rows: 1fr auto; gap: 18px; }}
    [data-style-preset="executive-film"] .desk-header {{ grid-row: 1 / 3; padding: 28px; border: 1px solid rgba(244,239,230,.13); background: rgba(0,0,0,.24); display: flex; flex-direction: column; justify-content: space-between; }}
    [data-style-preset="executive-film"] .desk-header small {{ color: rgba(214,193,154,.72); font-size: 10px; letter-spacing: .22em; font-weight: 780; }}
    [data-style-preset="executive-film"] .desk-header b {{ color: #f5efe5; font-size: 42px; line-height: .96; letter-spacing: -.046em; }}
    [data-style-preset="executive-film"] .desk-header span {{ color: rgba(244,239,230,.56); font-size: 15px; line-height: 1.45; }}
    [data-style-preset="executive-film"] .desk-cards ul {{ list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; }}
    [data-style-preset="executive-film"] .desk-cards li {{ min-height: 180px; padding: 20px; border: 1px solid rgba(244,239,230,.12); background: linear-gradient(180deg, rgba(244,239,230,.08), rgba(244,239,230,.025)); display: flex; flex-direction: column; justify-content: space-between; }}
    [data-style-preset="executive-film"] .desk-cards b {{ color: rgba(214,193,154,.74); font-size: 11px; letter-spacing: .2em; }}
    [data-style-preset="executive-film"] .desk-cards span {{ color: rgba(244,239,230,.68); font-size: 16px; line-height: 1.35; font-weight: 580; }}
    [data-style-preset="executive-film"] .desk-footer {{ grid-column: 2; display: flex; gap: 8px; align-items: end; }}
    [data-style-preset="executive-film"] .desk-footer span {{ flex: 1; padding: 9px 10px; border-top: 1px solid rgba(214,193,154,.28); color: rgba(244,239,230,.42); font-size: 9px; letter-spacing: .13em; text-transform: uppercase; }}
    [data-style-preset="executive-film"] .layout-final {{ position: absolute; inset: 64px 72px; z-index: 3; display: flex; flex-direction: column; justify-content: center; align-items: flex-start; }}
    [data-style-preset="executive-film"] .layout-final h3 {{ margin: 0; max-width: 760px; color: #f5efe5; font-size: 86px; line-height: .86; letter-spacing: -.075em; font-weight: 780; }}
    [data-style-preset="executive-film"] .layout-final p {{ margin: 28px 0 0; max-width: 660px; color: rgba(244,239,230,.58); font-size: 18px; line-height: 1.44; }}
    [data-style-preset="executive-film"] .layout-final .metric-stamp {{ position: absolute; right: 0; top: 0; }}
    [data-style-preset="executive-film"] .layout-final .executive-tags {{ position: relative; left: auto; top: auto; margin-top: 34px; }}
    [data-style-preset="executive-film"] .executive-layout-final-lockup .production-micro {{ top: auto; bottom: 36px; }}
    [data-style-preset="executive-film"] .caption {{ bottom: 70px; min-width: 0; max-width: 560px; padding: 7px 0; border-radius: 0; background: transparent; color: rgba(244,239,230,.76); font-size: 13px; line-height: 1.38; font-weight: 480; box-shadow: none; backdrop-filter: none; text-shadow: 0 2px 18px rgba(0,0,0,.64); }}
    .media-prop {{ position: absolute; right: 28px; bottom: 20px; width: 280px; height: 158px; border-radius: 28px; overflow: hidden; border: 1px solid rgba(255,255,255,.42); box-shadow: 0 24px 80px rgba(0,0,0,.32); background: rgba(255,255,255,.12); }}
    .media-prop img, .media-prop video {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
    .orb {{ position: absolute; width: 160px; height: 160px; border-radius: 50%; background: radial-gradient(circle, rgba(255,255,255,.82), rgba(124,92,255,.2) 42%, rgba(124,92,255,0) 68%); filter: blur(1px); opacity: .62; }}
    .orb.one {{ right: 36px; top: 16px; }} .orb.two {{ left: -36px; bottom: 14px; width: 220px; height: 220px; background: radial-gradient(circle, rgba(255,154,92,.72), rgba(255,154,92,.18) 42%, rgba(255,154,92,0) 70%); }}
    .caption {{ position: absolute; left: 50%; bottom: 24px; transform: translateX(-50%); min-width: 420px; max-width: 900px; text-align: center; padding: 14px 22px; border-radius: 26px; background: rgba(0,0,0,.74); color: white; font-size: 20px; line-height: 1.34; font-weight: 760; opacity: 0; z-index: 30; box-shadow: 0 18px 60px rgba(0,0,0,.30), inset 0 0 0 1px rgba(255,255,255,.12); backdrop-filter: blur(14px); }}
    .caption[data-sf-active="true"] {{ opacity: 1; }}
    .sf-word {{ display: inline-block; opacity: .40; margin: 0 .045em; transform-origin: 50% 78%; }}
    .sf-word[data-sf-active="true"] {{ opacity: 1; color: #ffe0a3; text-shadow: 0 0 18px rgba(255,224,163,.45); }}
    .sf-word-emphasis[data-sf-active="true"] {{ color: #fff4bf; text-shadow: 0 0 22px rgba(255,214,140,.66), 0 0 44px rgba(124,92,255,.35); }}
    .focus-ring {{ position: absolute; left: 50%; top: 50%; width: 490px; height: 72px; border-radius: 24px; border: 3px solid rgba(255,212,154,.92); box-shadow: 0 0 0 8px rgba(255,212,154,.10), 0 24px 80px rgba(255,154,92,.22); opacity: 0; pointer-events: none; z-index: 18; }}
    .spark {{ position: absolute; width: 9px; height: 9px; border-radius: 50%; background: #fff1b8; box-shadow: 0 0 24px #ffd36b; opacity: .76; z-index: 21; }}
    .transition-veil {{ position: absolute; inset: 0; z-index: 16; pointer-events: none; opacity: 0; background: linear-gradient(100deg, rgba(255,244,191,0), rgba(255,244,191,.36), rgba(124,92,255,.18), rgba(255,244,191,0)); filter: blur(12px); transform: translateX(-120%); mix-blend-mode: screen; will-change: opacity, transform, filter; }}
    .morph-bridge {{ position: absolute; inset: 54px 0; z-index: 17; pointer-events: none; opacity: 0; mix-blend-mode: screen; will-change: opacity, transform, filter; }}
    .morph-bridge svg {{ width: 100%; height: 100%; overflow: visible; }}
    .morph-bridge line,
    .morph-bridge path,
    .morph-bridge rect {{ vector-effect: non-scaling-stroke; stroke: rgba(214,193,154,.62); stroke-width: 1.2; fill: none; stroke-linecap: square; stroke-dasharray: var(--dash, 640); stroke-dashoffset: var(--offset, 640); opacity: .78; }}
    .morph-bridge rect {{ fill: rgba(214,193,154,.028); }}
    .morph-bridge circle {{ fill: rgba(244,239,230,.82); opacity: 0; filter: drop-shadow(0 0 12px rgba(214,193,154,.36)); }}
    .morph-bridge b {{ position: absolute; right: 78px; top: 56px; color: rgba(214,193,154,.70); font-size: 10px; letter-spacing: .24em; text-transform: uppercase; font-weight: 780; }}
  </style>
</head>
<body>
  <div data-composition-id="main" data-site-mode="{site_mode}" data-style-preset="{style_preset}" data-brand-name="{brand_name}" data-brand-domain="{brand_domain}" data-start="0" data-duration="{duration}" data-width="{width}" data-height="{height}">
    <div class="mesh"></div>
    <div class="grain"></div>
    <div class="brand-rail">
      <div class="brand">{brand_mark}<span>{title}</span></div>
      <div class="timeline-nav">{scene_nav}</div>
    </div>
    <div class="camera-layer">
      {scene_layers}
    </div>
    <span class="spark" style="left: 108px; top: 92px"></span><span class="spark" style="right: 148px; top: 84px"></span><span class="spark" style="left: 55%; bottom: 96px"></span>
    <div class="focus-ring"></div>
    <div class="transition-veil" data-transition-layer="{transition_preset}"></div>
    <div class="morph-bridge" data-morph-bridge>
      <b>MORPH CUT</b>
      <svg viewBox="0 0 1280 612" preserveAspectRatio="none" aria-hidden="true">
        <path data-morph-main d="M84 352 C 320 258, 588 438, 1192 220"></path>
        <line data-morph-line x1="120" y1="150" x2="1160" y2="150"></line>
        <line data-morph-line x1="120" y1="462" x2="1160" y2="462"></line>
        <rect data-morph-panel x="546" y="112" width="562" height="356"></rect>
        <circle data-morph-node cx="510" cy="306" r="5"></circle>
        <circle data-morph-node cx="704" cy="286" r="5"></circle>
        <circle data-morph-node cx="904" cy="332" r="5"></circle>
      </svg>
    </div>
    <div class="caption" data-caption-source="./assets/captions.json" data-caption-target></div>
  </div>
  <script src="./senseframe-runtime.js"></script>
  <script>
    {timeline_script}
  </script>
</body>
</html>
"""


def api_key() -> str:
    candidates = senseaudio_api_key_candidates()
    if not candidates:
        raise SenseAudioError("SENSEAUDIO_API_KEY is required for live API calls.")
    return candidates[0][1]


def senseaudio_api_key_candidates() -> list[tuple[str, str]]:
    seen: set[str] = set()
    candidates: list[tuple[str, str]] = []
    for source, key in (
        ("env:SENSEAUDIO_API_KEY", os.environ.get("SENSEAUDIO_API_KEY", "").strip()),
        ("local:SENSEAUDIO_API_KEY", local_senseaudio_credential("SENSEAUDIO_API_KEY")),
    ):
        if not key or key in seen:
            continue
        seen.add(key)
        candidates.append((source, key))
    return candidates


def api_key_required_candidates() -> list[tuple[str, str]]:
    candidates = senseaudio_api_key_candidates()
    if not candidates:
        raise SenseAudioError("SENSEAUDIO_API_KEY is required for live API calls.")
    return candidates


def audioclaw_workspace_path() -> Path:
    return Path(os.environ.get("AUDIOCLAW_WORKSPACE_PATH", "") or DEFAULT_AUDIOCLAW_WORKSPACE_PATH).expanduser()


def local_senseaudio_credential(name: str) -> str:
    workspace = audioclaw_workspace_path()
    state_path = workspace / "state" / "senseaudio_credentials.json"
    if state_path.exists():
        try:
            payload = json.loads(state_path.read_text(encoding="utf-8"))
            value = str(payload.get(name) or "").strip()
            if value:
                return value
        except json.JSONDecodeError:
            pass
    env_path = workspace / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8", errors="replace").splitlines():
            if not line.strip() or line.lstrip().startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            if key.strip() == name:
                return value.strip().strip('"').strip("'")
    return ""


def headers(content_type: str = "application/json", key: str | None = None) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {key or api_key()}",
        "Content-Type": content_type,
    }


def request_json(
    method: str,
    path: str,
    payload: dict[str, Any] | None = None,
    query: dict[str, str] | None = None,
) -> dict[str, Any]:
    url = API_BASE + path
    if query:
        url += "?" + urllib.parse.urlencode(query)
    data = None if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
    candidates = api_key_required_candidates()
    for index, (source, key) in enumerate(candidates):
        req = urllib.request.Request(url, data=data, method=method, headers=headers(key=key))
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                raw = resp.read().decode("utf-8")
            break
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            if exc.code == 401 and index + 1 < len(candidates):
                print(f"SenseAudio auth failed with {source}; retrying with fallback credential.", file=sys.stderr)
                continue
            raise SenseAudioError(f"HTTP {exc.code}: {body}") from exc
    else:
        raw = ""
    return json.loads(raw) if raw else {}


def multipart_request(path: str, fields: list[tuple[str, str]], file_field: str, file_path: Path) -> dict[str, Any] | str:
    boundary = "----senseaudio-video-gen-" + uuid.uuid4().hex
    file_name = file_path.name
    mime = mimetypes.guess_type(file_name)[0] or "application/octet-stream"
    chunks: list[bytes] = []

    for name, value in fields:
        chunks.append(f"--{boundary}\r\n".encode())
        chunks.append(f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode())
        chunks.append(str(value).encode("utf-8"))
        chunks.append(b"\r\n")

    chunks.append(f"--{boundary}\r\n".encode())
    chunks.append(
        f'Content-Disposition: form-data; name="{file_field}"; filename="{file_name}"\r\n'.encode()
    )
    chunks.append(f"Content-Type: {mime}\r\n\r\n".encode())
    chunks.append(file_path.read_bytes())
    chunks.append(b"\r\n")
    chunks.append(f"--{boundary}--\r\n".encode())

    req = urllib.request.Request(
        API_BASE + path,
        data=b"".join(chunks),
        method="POST",
        headers=headers(f"multipart/form-data; boundary={boundary}"),
    )
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            raw = resp.read().decode("utf-8")
            content_type = resp.headers.get("Content-Type", "")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise SenseAudioError(f"HTTP {exc.code}: {body}") from exc
    return raw if "text/plain" in content_type else json.loads(raw)


def write_json(path: str | None, data: Any) -> None:
    if not path:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(str(out))


def relative_to_project(project_dir: Path, path: Path) -> str:
    try:
        return str(path.resolve().relative_to(project_dir.resolve()))
    except ValueError:
        return str(path)


def save_project_meta(project_dir: Path, meta: dict[str, Any]) -> None:
    (project_dir / "senseframe.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")


def asset_manifest_path(project_dir: Path) -> Path:
    return project_dir / "assets" / "asset-manifest.json"


def read_asset_manifest(project_dir: Path) -> dict[str, Any]:
    path = asset_manifest_path(project_dir)
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {"project": project_dir.name, "assets": {}}


def write_asset_manifest(project_dir: Path, manifest: dict[str, Any]) -> None:
    path = asset_manifest_path(project_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


def register_asset(
    project_dir: Path,
    asset_id: str,
    asset_type: str,
    path: Path,
    role: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    manifest = read_asset_manifest(project_dir)
    item: dict[str, Any] = {
        "id": asset_id,
        "type": asset_type,
        "path": relative_to_project(project_dir, path),
    }
    if role:
        item["role"] = role
    if metadata:
        item["metadata"] = metadata
    manifest.setdefault("assets", {})[asset_id] = item
    write_asset_manifest(project_dir, manifest)

    meta = read_project_meta(project_dir)
    meta.setdefault("assets", {})[asset_id] = item
    save_project_meta(project_dir, meta)
    return item


def update_registered_asset(project_dir: Path, asset_id: str, updates: dict[str, Any]) -> dict[str, Any]:
    manifest = read_asset_manifest(project_dir)
    item = manifest.setdefault("assets", {}).setdefault(asset_id, {"id": asset_id})
    item.update(updates)
    manifest["assets"][asset_id] = item
    write_asset_manifest(project_dir, manifest)
    meta = read_project_meta(project_dir)
    meta.setdefault("assets", {})[asset_id] = item
    save_project_meta(project_dir, meta)
    return item


def download_url(url: str, output: str) -> str:
    out = Path(output)
    out.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=300) as resp:
        out.write_bytes(resp.read())
    return str(out)


_NO_PROXY_OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))


def urlopen_no_proxy(url: str, timeout: float = 30.0):
    return _NO_PROXY_OPENER.open(url, timeout=timeout)


def update_asset_html(project_dir: Path) -> None:
    index_path = project_dir / "index.html"
    if not index_path.exists():
        return
    manifest = read_asset_manifest(project_dir)
    html = index_path.read_text(encoding="utf-8")
    for asset_id, item in manifest.get("assets", {}).items():
        path = item.get("path")
        if not path:
            continue
        escaped_id = re.escape(asset_id)
        html = re.sub(
            rf'(<(?:img|video)\b[^>]*data-asset=["\']{escaped_id}["\'][^>]*\bsrc=["\'])([^"\']*)(["\'])',
            lambda match, asset_path=path: f"{match.group(1)}{asset_path}{match.group(3)}",
            html,
        )
        html = re.sub(
            rf'(<(?:img|video)\b(?=[^>]*\bsrc=["\'])(?=[^>]*data-asset=["\']{escaped_id}["\'])[^>]*\bsrc=["\'])([^"\']*)(["\'])',
            lambda match, asset_path=path: f"{match.group(1)}{asset_path}{match.group(3)}",
            html,
        )
    index_path.write_text(html, encoding="utf-8")


def clean_text(value: str) -> str:
    return html_lib.unescape(re.sub(r"\s+", " ", value or "").strip())


def fetch_url_text(url: str, timeout: float = 30.0) -> str:
    headers_map = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X) AppleWebKit/537.36 SenseAudioVideoGen/1.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }
    last_error: Exception | None = None
    for attempt in range(3):
        req = urllib.request.Request(url, headers=headers_map)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw = resp.read()
                charset = resp.headers.get_content_charset() or "utf-8"
            return raw.decode(charset, errors="replace")
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            last_error = exc
            if attempt < 2:
                time.sleep(0.6 * (attempt + 1))
    curl = shutil.which("curl")
    if curl:
        try:
            result = subprocess.run(
                [
                    curl,
                    "-L",
                    "--silent",
                    "--show-error",
                    "--max-time",
                    str(max(5, int(timeout))),
                    "-A",
                    headers_map["User-Agent"],
                    url,
                ],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
            )
            if result.stdout.strip():
                return result.stdout
        except (subprocess.CalledProcessError, OSError) as exc:
            last_error = exc
    raise SenseAudioError(f"fetch_url_text failed after retries: {last_error}")


def meta_content(markup: str, key: str) -> str:
    patterns = [
        rf'<meta\b(?=[^>]*(?:name|property)=["\']{re.escape(key)}["\'])(?=[^>]*content=["\']([^"\']+)["\'])[^>]*>',
        rf'<meta\b(?=[^>]*content=["\']([^"\']+)["\'])(?=[^>]*(?:name|property)=["\']{re.escape(key)}["\'])[^>]*>',
    ]
    for pattern in patterns:
        match = re.search(pattern, markup, flags=re.I)
        if match:
            return clean_text(match.group(1))
    return ""


def tag_attr(tag: str, name: str) -> str:
    match = re.search(rf'\b{re.escape(name)}=["\']([^"\']+)["\']', tag, flags=re.I)
    return clean_text(match.group(1)) if match else ""


def absolute_url(base_url: str, value: str) -> str:
    return urllib.parse.urljoin(base_url, html_lib.unescape(value.strip())) if value else ""


def dedupe_preserve(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item and item not in seen:
            seen.add(item)
            result.append(item)
    return result


def domain_brand_name(url: str) -> str:
    host = urllib.parse.urlparse(url).netloc.split("@")[-1].split(":")[0]
    parts = [part for part in host.split(".") if part and part not in {"www", "com", "cn", "ai", "io", "org", "net"}]
    return (parts[0].replace("-", " ").title() if parts else host) or "Website"


def title_brand_name(title: str, url: str) -> str:
    cleaned = clean_text(title)
    for separator in (" | ", " – ", " — ", " - ", " \\ ", " / "):
        if separator in cleaned:
            first, last = [part.strip() for part in cleaned.split(separator, 1)]
            return last or first or domain_brand_name(url)
    return cleaned[:42] or domain_brand_name(url)


def extract_nav_labels(markup: str) -> list[str]:
    labels: list[str] = []
    blocked = {"cookie", "privacy", "terms", "login", "sign in", "subscribe", "关闭", "隐私", "条款"}
    for anchor in re.findall(r"<a\b[^>]*>(.*?)</a>", markup, flags=re.I | re.S):
        label = clean_text(re.sub(r"<[^>]+>", " ", anchor))
        lower = label.lower()
        if not label or len(label) > 28 or lower in blocked or lower.startswith("skip to"):
            continue
        if label not in labels:
            labels.append(label)
        if len(labels) >= 8:
            break
    return labels


def flatten_json_ld(value: Any) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    if isinstance(value, dict):
        items.append(value)
        graph = value.get("@graph")
        if isinstance(graph, list):
            for child in graph:
                items.extend(flatten_json_ld(child))
    elif isinstance(value, list):
        for child in value:
            items.extend(flatten_json_ld(child))
    return items


def extract_json_ld_brand(markup: str, base_url: str) -> dict[str, Any]:
    candidates: list[dict[str, Any]] = []
    for script in re.findall(r'<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', markup, flags=re.I | re.S):
        try:
            parsed = json.loads(html_lib.unescape(script.strip()))
        except json.JSONDecodeError:
            continue
        for item in flatten_json_ld(parsed):
            item_type = item.get("@type", "")
            types = item_type if isinstance(item_type, list) else [item_type]
            if any(str(kind).lower() in {"organization", "website", "corporation", "brand"} for kind in types):
                candidates.append(item)
    if not candidates:
        return {}
    chosen = candidates[0]
    logo_value = chosen.get("logo", "")
    if isinstance(logo_value, dict):
        logo_value = logo_value.get("url", "")
    same_as = chosen.get("sameAs", [])
    return {
        "name": clean_text(str(chosen.get("name", ""))),
        "description": clean_text(str(chosen.get("description", ""))),
        "url": absolute_url(base_url, str(chosen.get("url", ""))),
        "logo": absolute_url(base_url, str(logo_value)),
        "same_as": [absolute_url(base_url, str(item)) for item in same_as[:5]] if isinstance(same_as, list) else [],
    }


def color_distance_from_gray(hex_color: str) -> int:
    value = hex_color.lstrip("#")
    if len(value) == 3:
        value = "".join(char * 2 for char in value)
    red, green, blue = int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16)
    return max(red, green, blue) - min(red, green, blue)


def extract_brand_colors(markup: str) -> list[str]:
    counts: dict[str, int] = {}
    for value in re.findall(r"#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b", markup):
        color = value.lower()
        if len(color) == 4:
            color = "#" + "".join(char * 2 for char in color[1:])
        if color in {"#000000", "#ffffff", "#fefefe", "#111111", "#222222"}:
            continue
        if color_distance_from_gray(color) < 12:
            continue
        counts[color] = counts.get(color, 0) + 1
    return [color for color, _count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:5]]


def extract_brand_typography(markup: str) -> dict[str, Any]:
    families: list[str] = []
    for href in re.findall(r'<link\b[^>]*href=["\']([^"\']+)["\'][^>]*>', markup, flags=re.I):
        if "fonts.googleapis.com" not in href:
            continue
        parsed = urllib.parse.urlparse(html_lib.unescape(href))
        query = urllib.parse.parse_qs(parsed.query)
        for family_value in query.get("family", []):
            family_name = family_value.split(":", 1)[0].replace("+", " ").strip()
            if family_name and family_name not in families:
                families.append(family_name)
    for family_value in re.findall(r"font-family\s*:\s*([^;}{]+)", markup, flags=re.I):
        first_family = clean_text(family_value.split(",", 1)[0].strip(" \"'"))
        if first_family and len(first_family) <= 32 and first_family.lower() not in {"inherit", "sans-serif", "serif", "monospace"}:
            if first_family not in families:
                families.append(first_family)
    return {"families": families[:5], "primary": families[0] if families else ""}


def extract_linked_brand_assets(markup: str, base_url: str) -> dict[str, Any]:
    icons: list[str] = []
    manifests: list[str] = []
    for tag in re.findall(r"<link\b[^>]+>", markup, flags=re.I):
        rel = tag_attr(tag, "rel").lower()
        href = tag_attr(tag, "href")
        if not href:
            continue
        if "manifest" in rel:
            manifests.append(absolute_url(base_url, href))
        if "icon" in rel or "apple-touch-icon" in rel or "mask-icon" in rel:
            icons.append(absolute_url(base_url, href))
    social_images = [
        meta_content(markup, "og:image"),
        meta_content(markup, "twitter:image"),
    ]
    return {
        "icons": dedupe_preserve([item for item in icons if item])[:6],
        "manifest": manifests[0] if manifests else "",
        "social_images": dedupe_preserve([absolute_url(base_url, item) for item in social_images if item])[:3],
    }


def extract_logo_candidates(markup: str, base_url: str) -> list[str]:
    logos: list[str] = []
    for tag in re.findall(r"<img\b[^>]+>", markup, flags=re.I):
        alt = tag_attr(tag, "alt")
        src = tag_attr(tag, "src") or tag_attr(tag, "data-src")
        if not src:
            continue
        if "logo" in src.lower() or "logo" in alt.lower():
            logos.append(absolute_url(base_url, src))
        if len(logos) >= 3:
            break
    return dedupe_preserve(logos)


def extract_brand_keywords(name: str, description: str, nav: list[str]) -> list[str]:
    text = " ".join([name, description, *nav])
    raw_terms = re.findall(r"[A-Za-z][A-Za-z0-9&+\-]{2,}|[\u4e00-\u9fff]{2,6}", text)
    blocked = {"the", "and", "for", "with", "from", "that", "this", "login", "sign", "more", "learn", "首页", "登录", "更多"}
    keywords: list[str] = []
    for term in raw_terms:
        normalized = term.strip("-+&")
        if not normalized or normalized.lower() in blocked:
            continue
        if normalized not in keywords:
            keywords.append(normalized)
        if len(keywords) >= 8:
            break
    return keywords


def infer_brand_voice(name: str, description: str, nav: list[str]) -> dict[str, Any]:
    text = " ".join([name, description, *nav]).lower()
    scores = {
        "research": sum(token in text for token in ("research", "safety", "policy", "science", "研究", "安全", "政策")),
        "developer": sum(token in text for token in ("api", "developer", "docs", "tutorial", "开发", "文档", "教程")),
        "enterprise": sum(token in text for token in ("enterprise", "security", "compliance", "teams", "企业", "合规", "团队")),
        "creator": sum(token in text for token in ("create", "creator", "video", "audio", "生成", "创作", "视频", "音频")),
    }
    voice_map = {
        "research": ("可信克制", "用证据、原则和长期视角解释品牌。"),
        "developer": ("清晰实用", "突出路径、接口、文档和可落地能力。"),
        "enterprise": ("稳健专业", "强调安全、合规、团队与规模化价值。"),
        "creator": ("灵感驱动", "用更具画面感的语言展示创作可能。"),
    }
    category = max(scores, key=scores.get)
    if scores[category] == 0:
        category = "enterprise" if len(nav) >= 5 else "research"
    tone, guidance = voice_map[category]
    return {"category": category, "tone": tone, "guidance": guidance}


def build_brand_mark_html(brand: dict[str, Any]) -> str:
    logos = brand.get("logos", [])
    logo = str(logos[0]) if isinstance(logos, list) and logos else ""
    if logo:
        return f'<span class="brand-mark logo"><img src="{html_lib.escape(logo)}" alt="" /></span>'
    return '<span class="brand-mark"></span>'


def extract_brand(url: str, markup: str) -> dict[str, Any]:
    title_match = re.search(r"<title[^>]*>(.*?)</title>", markup, flags=re.I | re.S)
    page_title = clean_text(title_match.group(1)) if title_match else ""
    json_ld = extract_json_ld_brand(markup, url)
    site_name = meta_content(markup, "og:site_name") or meta_content(markup, "application-name")
    description = meta_content(markup, "description") or meta_content(markup, "og:description") or json_ld.get("description", "")
    name = site_name or json_ld.get("name", "") or title_brand_name(page_title, url)
    nav = extract_nav_labels(markup)
    colors = extract_brand_colors(markup)
    linked_assets = extract_linked_brand_assets(markup, url)
    logos = dedupe_preserve([json_ld.get("logo", ""), *extract_logo_candidates(markup, url), *linked_assets["icons"]])
    keywords = extract_brand_keywords(name, description, nav)
    return {
        "source_url": url,
        "domain": urllib.parse.urlparse(url).netloc,
        "name": name,
        "page_title": page_title,
        "description": description,
        "nav": nav,
        "keywords": keywords,
        "voice": infer_brand_voice(name, description, nav),
        "colors": {
            "primary": colors[0] if colors else "",
            "secondary": colors[1] if len(colors) > 1 else "",
            "palette": colors,
        },
        "typography": extract_brand_typography(markup),
        "logos": logos,
        "assets": {
            **linked_assets,
            "json_ld_url": json_ld.get("url", ""),
            "same_as": json_ld.get("same_as", []),
        },
    }


def strip_markup(markup: str) -> str:
    cleaned = re.sub(r"<(script|style|noscript|svg)\b[^>]*>.*?</\1>", " ", markup, flags=re.I | re.S)
    cleaned = re.sub(r"<[^>]+>", " ", cleaned)
    return clean_text(cleaned)


def meaningful_text(value: str, max_len: int = 160) -> str:
    text = clean_text(value)
    text = re.sub(r"^(learn more|read more|see more|更多|了解更多|查看详情)$", "", text, flags=re.I).strip()
    if len(text) > max_len:
        text = text[: max_len - 1].rstrip() + "…"
    return text


def extract_tag_texts(markup: str, tag_names: tuple[str, ...], limit: int, max_len: int = 120) -> list[str]:
    tags = "|".join(re.escape(tag) for tag in tag_names)
    values: list[str] = []
    for match in re.findall(rf"<({tags})\b[^>]*>(.*?)</\1>", markup, flags=re.I | re.S):
        text = meaningful_text(strip_markup(match[1]), max_len)
        if not text or text in values:
            continue
        values.append(text)
        if len(values) >= limit:
            break
    return values


def extract_cta_labels(markup: str, nav_labels: list[str], limit: int = 6) -> list[str]:
    labels: list[str] = []
    blocked = {label.lower() for label in nav_labels}
    blocked |= {"privacy", "terms", "cookie", "skip to content", "login", "sign in", "关闭", "隐私", "条款"}
    cta_signal = re.compile(
        r"(try|start|get-started|get started|book|demo|contact|talk|request|download|sign up|join|buy|subscribe|"
        r"开始|试用|体验|预约|演示|联系|咨询|下载|注册|购买|立即)",
        flags=re.I,
    )
    for tag in re.findall(r"<(?:button|a)\b[^>]*>.*?</(?:button|a)>", markup, flags=re.I | re.S):
        label = meaningful_text(strip_markup(tag), 42)
        lower = label.lower()
        tag_lower = tag.lower()
        has_signal = bool(cta_signal.search(label) or cta_signal.search(tag_lower) or tag_lower.startswith("<button"))
        if not label or lower in blocked or lower.startswith("skip to") or "log in" in lower or "login" in lower or len(label) < 2 or not has_signal:
            continue
        if label not in labels:
            labels.append(label)
        if len(labels) >= limit:
            break
    return labels


def extract_site_sections(markup: str, limit: int = 8) -> list[dict[str, str]]:
    sections: list[dict[str, str]] = []
    blocks: list[tuple[str, str]] = []
    blocks.extend(re.findall(r"<(header)\b[^>]*>(.*?)</\1>", markup, flags=re.I | re.S))
    blocks.extend(re.findall(r"<(section|article)\b[^>]*>(.*?)</\1>", markup, flags=re.I | re.S))
    if not blocks:
        blocks.extend(re.findall(r"<(main)\b[^>]*>(.*?)</\1>", markup, flags=re.I | re.S))
    for tag_name, body in blocks:
        heading = extract_tag_texts(body, ("h1", "h2", "h3"), 1, 80)
        paragraphs = extract_tag_texts(body, ("p",), 3, 110)
        text = meaningful_text(" ".join(paragraphs), 180) if paragraphs else meaningful_text(strip_markup(body), 180)
        if not text:
            continue
        if not paragraphs and text.lower().startswith("skip to"):
            continue
        label = heading[0] if heading else text[:42]
        if any(item["label"] == label for item in sections):
            continue
        sections.append({"label": label, "text": text, "source": tag_name.lower()})
        if len(sections) >= limit:
            break
    return sections


SITE_MATERIAL_ROLES: dict[str, dict[str, Any]] = {
    "hero": {
        "keywords": ("hero", "home", "homepage", "build", "introducing", "frontier", "首页", "官网", "主张", "平台"),
        "shot": "hero-overview",
        "composition": "full-bleed",
        "camera": "hero-push",
    },
    "product": {
        "keywords": ("claude", "assistant", "product", "workflow", "chat", "model", "模型", "产品", "助手", "工作流"),
        "shot": "feature-zoom",
        "composition": "zoom-callout",
        "camera": "macro-zoom",
    },
    "research": {
        "keywords": ("research", "paper", "frontier", "evaluations", "interpretability", "研究", "论文", "评测", "前沿"),
        "shot": "trust-message",
        "composition": "evidence-board",
        "camera": "board-orbit",
    },
    "safety": {
        "keywords": ("safety", "safe", "responsible", "policy", "govern", "risk", "security", "安全", "治理", "风险", "负责"),
        "shot": "trust-message",
        "composition": "evidence-board",
        "camera": "board-orbit",
    },
    "developer": {
        "keywords": ("developer", "api", "sdk", "docs", "documentation", "tool use", "batch", "开发者", "接口", "文档", "工具"),
        "shot": "feature-zoom",
        "composition": "zoom-callout",
        "camera": "macro-zoom",
    },
    "enterprise": {
        "keywords": ("enterprise", "business", "team", "admin", "compliance", "solutions", "sales", "企业", "团队", "合规", "解决方案"),
        "shot": "feature-zoom",
        "composition": "zoom-callout",
        "camera": "macro-zoom",
    },
    "customer": {
        "keywords": ("customer", "case", "stories", "partners", "客户", "案例", "伙伴"),
        "shot": "trust-message",
        "composition": "evidence-board",
        "camera": "board-orbit",
    },
    "pricing": {
        "keywords": ("pricing", "plans", "price", "subscribe", "价格", "套餐", "订阅"),
        "shot": "cta-summary",
        "composition": "cta-lockup",
        "camera": "lockup-dolly",
    },
    "cta": {
        "keywords": ("start", "try", "contact", "demo", "sales", "sign up", "get started", "开始", "试用", "联系", "演示", "注册"),
        "shot": "cta-summary",
        "composition": "cta-lockup",
        "camera": "lockup-dolly",
    },
}


SITE_ROLE_ORDER = ("hero", "product", "research", "safety", "developer", "enterprise", "customer", "pricing", "cta")


def classify_site_material(label: str, text: str, index: int, kind: str = "section") -> dict[str, Any]:
    combined = f"{label} {text}".lower()
    scores: dict[str, int] = {}
    for role, spec in SITE_MATERIAL_ROLES.items():
        score = 0
        for keyword in spec["keywords"]:
            if str(keyword).lower() in combined:
                score += 3 if str(keyword).lower() in str(label).lower() else 1
        scores[role] = score
    if kind == "hero" or index == 0:
        scores["hero"] = max(scores.get("hero", 0), 4 if kind == "hero" else 2)
    if kind == "cta":
        scores["cta"] = max(scores.get("cta", 0), 5)
    role = max(SITE_ROLE_ORDER, key=lambda item: (scores.get(item, 0), -SITE_ROLE_ORDER.index(item)))
    if scores.get(role, 0) <= 0:
        role = "product" if index <= 1 else ("research" if index == 2 else "enterprise")
    spec = SITE_MATERIAL_ROLES[role]
    matched = [keyword for keyword in spec["keywords"] if str(keyword).lower() in combined][:4]
    return {
        "role": role,
        "confidence": min(1.0, round(max(scores.get(role, 1), 1) / 6, 3)),
        "shot": spec["shot"],
        "composition": spec["composition"],
        "camera": spec["camera"],
        "keywords": matched,
    }


def build_semantic_sections(headings: list[str], sections: list[dict[str, str]], ctas: list[str]) -> list[dict[str, Any]]:
    semantic: list[dict[str, Any]] = []
    if headings:
        hero_text = sections[0].get("text", "") if sections else headings[0]
        hero = classify_site_material(headings[0], hero_text, 0, "hero")
        hero.update(
            {
                "role": "hero",
                "shot": SITE_MATERIAL_ROLES["hero"]["shot"],
                "composition": SITE_MATERIAL_ROLES["hero"]["composition"],
                "camera": SITE_MATERIAL_ROLES["hero"]["camera"],
            }
        )
        semantic.append(
            {
                "kind": "semantic-section",
                "label": headings[0],
                "text": hero_text,
                "rank": 1,
                **hero,
            }
        )
    seen_roles = {"hero"} if semantic else set()
    for index, section in enumerate(sections):
        label = str(section.get("label", "") or f"页面模块 {index + 1}")
        text = str(section.get("text", "") or label)
        classification = classify_site_material(label, text, index + 1, "section")
        role = classification["role"]
        if role == "hero" and "hero" in seen_roles:
            classification = dict(classification)
            classification.update(classify_site_material(label, text, index + 1, "section"))
            role = "product" if index <= 1 else classification["role"]
            classification["role"] = role
        if any(item["label"] == label for item in semantic):
            continue
        semantic.append(
            {
                "kind": "semantic-section",
                "label": label,
                "text": text,
                "rank": len(semantic) + 1,
                **classification,
            }
        )
        seen_roles.add(role)
    for cta in ctas[:2]:
        classification = classify_site_material(cta, f"页面行动入口：{cta}", len(semantic), "cta")
        semantic.append(
            {
                "kind": "semantic-section",
                "label": cta,
                "text": f"页面行动入口：{cta}",
                "rank": len(semantic) + 1,
                **classification,
            }
        )
    unique: list[dict[str, Any]] = []
    seen_labels: set[str] = set()
    for item in semantic:
        label = str(item.get("label", ""))
        if label in seen_labels:
            continue
        seen_labels.add(label)
        unique.append(item)
    unique.sort(key=lambda item: (SITE_ROLE_ORDER.index(str(item.get("role", "cta"))) if str(item.get("role", "cta")) in SITE_ROLE_ORDER else 99, int(item.get("rank", 99))))
    for rank, item in enumerate(unique, 1):
        item["rank"] = rank
    return unique[:10]


def extract_site_profile(url: str, markup: str, brand: dict[str, Any] | None = None) -> dict[str, Any]:
    brand = brand or extract_brand(url, markup)
    headings = extract_tag_texts(markup, ("h1", "h2", "h3"), 12, 96)
    nav = [str(item) for item in brand.get("nav", []) if str(item).strip()]
    ctas = extract_cta_labels(markup, nav)
    sections = extract_site_sections(markup)
    semantic_sections = build_semantic_sections(headings, sections, ctas)
    body_text = strip_markup(markup)
    evidence: list[dict[str, str]] = []
    for item in semantic_sections[:8]:
        evidence.append(
            {
                "kind": "semantic-section",
                "role": str(item.get("role", "")),
                "label": str(item.get("label", "")),
                "text": str(item.get("text", "")),
                "rank": str(item.get("rank", "")),
                "shot": str(item.get("shot", "")),
                "composition": str(item.get("composition", "")),
            }
        )
    for index, heading in enumerate(headings[:6]):
        evidence.append({"kind": "heading", "label": heading, "text": heading, "rank": str(index + 1)})
    for index, section in enumerate(sections[:6]):
        evidence.append({"kind": "section", "label": section["label"], "text": section["text"], "rank": str(index + 1)})
    for index, cta in enumerate(ctas[:4]):
        evidence.append({"kind": "cta", "label": cta, "text": f"页面行动入口：{cta}", "rank": str(index + 1)})
    return {
        "source_url": url,
        "domain": urllib.parse.urlparse(url).netloc,
        "title": brand.get("page_title") or brand.get("name") or domain_brand_name(url),
        "summary": str(brand.get("description", "")) or meaningful_text(body_text, 180),
        "headings": headings,
        "sections": sections,
        "semantic_sections": semantic_sections,
        "primary_roles": list(dict.fromkeys(str(item.get("role", "")) for item in semantic_sections if str(item.get("role", ""))))[:6],
        "ctas": ctas,
        "evidence": evidence[:12],
        "text_sample": meaningful_text(body_text, 420),
        "brand_name": brand.get("name", ""),
    }


def markdown_to_plain_text(value: str) -> str:
    text = re.sub(r"```.*?```", " ", value, flags=re.S)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"^\s{0,3}#{1,6}\s+", "", text, flags=re.M)
    text = re.sub(r"^\s{0,3}[-*+]\s+", "", text, flags=re.M)
    text = re.sub(r"^\s{0,3}>\s?", "", text, flags=re.M)
    text = re.sub(r"[*_~]{1,3}", "", text)
    return clean_text(text)


def split_markdown_sections(markdown: str) -> tuple[str, list[dict[str, str]], list[str]]:
    heading_pattern = re.compile(r"^\s{0,3}(#{1,6})\s+(.+?)\s*#*\s*$", flags=re.M)
    matches = list(heading_pattern.finditer(markdown))
    headings = [markdown_to_plain_text(match.group(2))[:96] for match in matches if markdown_to_plain_text(match.group(2))]
    title = next((markdown_to_plain_text(match.group(2)) for match in matches if len(match.group(1)) == 1), "")
    if not title and headings:
        title = headings[0]
    if not title:
        first_line = next((markdown_to_plain_text(line) for line in markdown.splitlines() if markdown_to_plain_text(line)), "")
        title = first_line[:80] if first_line else "Untitled Source"
    sections: list[dict[str, str]] = []
    if matches:
        for index, match in enumerate(matches):
            label = markdown_to_plain_text(match.group(2))[:80]
            start = match.end()
            end = matches[index + 1].start() if index + 1 < len(matches) else len(markdown)
            body = markdown_to_plain_text(markdown[start:end])
            if not body or label == title and index == 0:
                continue
            sections.append({"label": label, "text": meaningful_text(body, 220), "source": "markdown"})
    else:
        paragraphs = [markdown_to_plain_text(part) for part in re.split(r"\n\s*\n", markdown) if markdown_to_plain_text(part)]
        for index, paragraph in enumerate(paragraphs[:8]):
            label = title if index == 0 else f"段落 {index + 1}"
            sections.append({"label": label, "text": meaningful_text(paragraph, 220), "source": "text"})
    if not sections:
        sections.append({"label": title, "text": meaningful_text(markdown_to_plain_text(markdown), 220), "source": "markdown"})
    return title[:96], sections[:12], dedupe_preserve([title[:96], *headings])[:16]


def extract_source_ctas(text: str, limit: int = 6) -> list[str]:
    cta_signal = re.compile(
        r"(book a demo|get started|start building|contact sales|contact us|download|sign up|try|subscribe|"
        r"预约|演示|联系|咨询|下载|注册|试用|开始|下一步)",
        flags=re.I,
    )
    labels: list[str] = []
    for line in re.split(r"[\n。.!?！？；;]", text):
        plain = markdown_to_plain_text(line)
        if not plain or len(plain) > 80 or not cta_signal.search(plain):
            continue
        if plain not in labels:
            labels.append(plain)
        if len(labels) >= limit:
            break
    return labels


def source_profile_from_text(
    text: str,
    source_url: str,
    source_name: str,
    source_type: str,
    title_override: str = "",
) -> dict[str, Any]:
    text = textwrap.dedent(text).strip()
    title, sections, headings = split_markdown_sections(text)
    title = title_override or title or Path(source_name).stem or "Untitled Source"
    plain = markdown_to_plain_text(text)
    ctas = extract_source_ctas(text)
    semantic_sections = build_semantic_sections(headings, sections, ctas)
    evidence: list[dict[str, str]] = []
    for item in semantic_sections[:8]:
        evidence.append(
            {
                "kind": "semantic-section",
                "role": str(item.get("role", "")),
                "label": str(item.get("label", "")),
                "text": str(item.get("text", "")),
                "rank": str(item.get("rank", "")),
                "shot": str(item.get("shot", "")),
                "composition": str(item.get("composition", "")),
            }
        )
    for index, section in enumerate(sections[:6]):
        evidence.append({"kind": "section", "label": section["label"], "text": section["text"], "rank": str(index + 1)})
    return {
        "source_url": source_url,
        "source_type": source_type,
        "domain": urllib.parse.urlparse(source_url).netloc or Path(source_name).name,
        "title": title,
        "summary": meaningful_text(plain, 220),
        "headings": headings,
        "sections": sections,
        "semantic_sections": semantic_sections,
        "primary_roles": list(dict.fromkeys(str(item.get("role", "")) for item in semantic_sections if str(item.get("role", ""))))[:6],
        "ctas": ctas,
        "evidence": evidence[:12],
        "text_sample": meaningful_text(plain, 520),
        "brand_name": title_brand_name(title, source_url),
    }


def parse_github_repo(value: str) -> tuple[str, str]:
    cleaned = value.strip().removesuffix("/")
    if re.fullmatch(r"[\w.-]+/[\w.-]+", cleaned):
        owner, repo = cleaned.split("/", 1)
    else:
        parsed = urllib.parse.urlparse(cleaned)
        parts = [part for part in parsed.path.split("/") if part]
        if parsed.netloc not in {"github.com", "www.github.com"} or len(parts) < 2:
            raise SenseAudioError(f"Unsupported GitHub repository URL: {value}")
        owner, repo = parts[0], parts[1].removesuffix(".git")
    return owner, repo


def github_readme_candidates(value: str) -> list[str]:
    owner, repo = parse_github_repo(value)
    names = ("README.md", "README.MD", "readme.md")
    branches = ("main", "master")
    return [f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{name}" for branch in branches for name in names]


def fetch_github_readme(value: str) -> tuple[str, str]:
    errors: list[str] = []
    for url in github_readme_candidates(value):
        try:
            with urllib.request.urlopen(url, timeout=45) as resp:
                return resp.read().decode("utf-8", errors="replace"), url
        except Exception as exc:
            errors.append(str(exc)[:120])
    raise SenseAudioError(f"Could not fetch GitHub README from {value}: {'; '.join(errors[:2])}")


def site_profile_path(project_dir: Path) -> Path:
    return project_dir / "assets" / "site-profile.json"


def site_assets_path(project_dir: Path) -> Path:
    return project_dir / "assets" / "site-assets.json"


def write_site_profile_file(project_dir: Path, site_profile: dict[str, Any], source: str = "site-ingest") -> Path:
    output = site_profile_path(project_dir)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({"source": source, "site": site_profile}, ensure_ascii=False, indent=2), encoding="utf-8")
    if (project_dir / "senseframe.json").exists():
        register_asset(project_dir, "site-profile", "json", output, "website-evidence", {"source_url": site_profile.get("source_url", "")})
    return output


def read_site_profile_file(path: str | None) -> dict[str, Any]:
    if not path:
        return {}
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    return payload.get("site", payload) if isinstance(payload, dict) else {}


def add_site_screenshots_to_profile(site_profile: dict[str, Any], screenshots: list[dict[str, Any]]) -> dict[str, Any]:
    merged = dict(site_profile)
    merged["screenshots"] = screenshots
    return merged


def add_site_assets_to_profile(site_profile: dict[str, Any], project_dir: Path, inventory: dict[str, Any]) -> dict[str, Any]:
    merged = dict(site_profile)
    merged["asset_inventory"] = relative_to_project(project_dir, site_assets_path(project_dir))
    merged["asset_summary"] = {
        "counts": inventory.get("counts", {}),
        "signals": inventory.get("signals", {}),
    }
    return merged


def add_site_capture_quality_to_profile(site_profile: dict[str, Any], project_dir: Path, quality_path: Path | None) -> dict[str, Any]:
    if not quality_path or not quality_path.exists():
        return site_profile
    merged = dict(site_profile)
    try:
        quality = json.loads(quality_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return merged
    merged["capture_quality"] = {
        "path": relative_to_project(project_dir, quality_path),
        "ok": bool(quality.get("ok", True)),
        "warnings": quality.get("warnings", []),
        "signals": quality.get("signals", {}),
        "cookie_mode": quality.get("cookie_mode", "clean"),
    }
    signals = quality.get("signals", {}) if isinstance(quality.get("signals"), dict) else {}
    browser_content = signals.get("content", {}) if isinstance(signals.get("content"), dict) else {}
    browser_headings = [clean_text(str(item)) for item in browser_content.get("headings", []) if clean_text(str(item))]
    browser_ctas = [clean_text(str(item)) for item in browser_content.get("ctas", []) if clean_text(str(item))]
    if browser_headings and len(merged.get("headings", []) if isinstance(merged.get("headings"), list) else []) < 3:
        merged["headings"] = dedupe_preserve([*browser_headings, *[str(item) for item in merged.get("headings", []) if str(item).strip()]])[:12]
    if browser_ctas and not merged.get("ctas"):
        merged["ctas"] = browser_ctas[:6]
    text_sample = clean_text(str(browser_content.get("text_sample", "")))
    if text_sample and len(str(merged.get("text_sample", ""))) < 160:
        merged["text_sample"] = meaningful_text(text_sample, 520)
    if text_sample and len(str(merged.get("summary", ""))) < 80:
        merged["summary"] = meaningful_text(text_sample, 220)
    return merged


def _normalized_asset_url(base_url: str, value: Any) -> str:
    url = absolute_url(base_url, str(value or ""))
    if not url or url.startswith(("javascript:", "mailto:", "tel:")):
        return ""
    return url


def _dedupe_asset_dicts(items: list[dict[str, Any]], key: str = "url") -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in items:
        value = str(item.get(key, "")).strip()
        if not value or value in seen:
            continue
        seen.add(value)
        result.append(item)
    return result


def _normalize_asset_items(base_url: str, raw_items: Any, keep_fields: tuple[str, ...]) -> list[dict[str, Any]]:
    if not isinstance(raw_items, list):
        return []
    normalized: list[dict[str, Any]] = []
    for raw in raw_items:
        if not isinstance(raw, dict):
            continue
        url = _normalized_asset_url(base_url, raw.get("url"))
        if not url:
            continue
        item: dict[str, Any] = {"url": url}
        for field in keep_fields:
            if field == "url" or field not in raw:
                continue
            value = raw.get(field)
            if value in (None, "", [], {}):
                continue
            item[field] = value
        normalized.append(item)
    return _dedupe_asset_dicts(normalized)


def normalize_site_asset_inventory(source_url: str, raw: dict[str, Any]) -> dict[str, Any]:
    raw = raw if isinstance(raw, dict) else {}
    images = _normalize_asset_items(source_url, raw.get("images"), ("url", "alt", "width", "height", "kind", "selector"))
    icons = _normalize_asset_items(source_url, raw.get("icons"), ("url", "rel", "type", "sizes"))
    media = _normalize_asset_items(source_url, raw.get("media"), ("url", "kind", "width", "height", "poster"))
    scripts = _normalize_asset_items(source_url, raw.get("scripts"), ("url", "kind"))
    stylesheets = _normalize_asset_items(source_url, raw.get("stylesheets"), ("url", "kind"))
    fonts_raw = raw.get("fonts") if isinstance(raw.get("fonts"), list) else []
    fonts: list[dict[str, Any]] = []
    seen_fonts: set[str] = set()
    for raw_font in fonts_raw:
        if not isinstance(raw_font, dict):
            continue
        family = clean_text(str(raw_font.get("family", "") or "")).strip("\"'")
        if not family or family.lower() in {"serif", "sans-serif", "monospace", "system-ui"} or family in seen_fonts:
            continue
        seen_fonts.add(family)
        item = {"family": family, "source": str(raw_font.get("source") or "page")}
        if raw_font.get("status"):
            item["status"] = str(raw_font["status"])
        fonts.append(item)
    animations = raw.get("animations") if isinstance(raw.get("animations"), list) else []
    animations = [item for item in animations if isinstance(item, dict)]
    canvases = raw.get("canvases") if isinstance(raw.get("canvases"), list) else []
    canvases = [item for item in canvases if isinstance(item, dict)]
    signals = {
        "has_css_animation": any(str(item.get("type", "")).startswith("css-") for item in animations),
        "has_web_animations": any(str(item.get("type", "")) == "web-animation" for item in animations),
        "has_lottie_hint": any("lottie" in str(item.get("kind", "")).lower() or "lottie" in str(item.get("url", "")).lower() for item in scripts),
        "has_canvas": bool(canvases),
        "has_webgl": any(str(item.get("kind", "")).lower() == "webgl" for item in canvases),
        "has_video": any(str(item.get("kind", "")).lower() == "video" for item in media),
    }
    counts = {
        "images": len(images),
        "icons": len(icons),
        "fonts": len(fonts),
        "animations": len(animations),
        "media": len(media),
        "scripts": len(scripts),
        "stylesheets": len(stylesheets),
        "canvases": len(canvases),
    }
    return {
        "source": "site-capture",
        "source_url": source_url,
        "captured_at": int(time.time()),
        "counts": counts,
        "signals": signals,
        "images": images,
        "icons": icons,
        "fonts": fonts,
        "animations": animations[:80],
        "media": media,
        "scripts": scripts,
        "stylesheets": stylesheets,
        "canvases": canvases,
    }


def role_crop_zoom(role: str, composition: str) -> float:
    if role in {"developer", "product", "enterprise", "pricing"}:
        return 1.16
    if role in {"research", "safety", "customer"}:
        return 1.1
    if role == "cta" or composition == "cta-lockup":
        return 1.12
    return 1.04


def crop_from_highlight(highlight: dict[str, Any], role: str, composition: str, scene_index: int) -> dict[str, float]:
    left = clamp_percent(float(highlight.get("left", 18 + (scene_index * 13) % 44) or 0), 18)
    top = clamp_percent(float(highlight.get("top", 18 + (scene_index * 11) % 42) or 0), 18)
    width = clamp_percent(float(highlight.get("width", 40) or 0), 40)
    height = clamp_percent(float(highlight.get("height", 24) or 0), 24)
    center_x = clamp_percent(left + width / 2, 50)
    center_y = clamp_percent(top + height / 2, 32)
    if composition == "full-bleed":
        center_y = min(center_y, 42)
    elif composition == "zoom-callout":
        center_y = max(22, min(center_y, 58))
    return {
        "x": round(center_x, 2),
        "y": round(center_y, 2),
        "zoom": role_crop_zoom(role, composition),
        "pan": round((center_x - 50) / 50, 3),
    }


def heuristic_visual_plan(site_profile: dict[str, Any]) -> list[dict[str, Any]]:
    screenshots = [item for item in site_profile.get("screenshots", []) if isinstance(item, dict)]
    evidence = [item for item in (site_profile.get("story_evidence") or site_profile.get("semantic_sections") or site_profile.get("evidence", [])) if isinstance(item, dict)]
    if not screenshots:
        return []
    visual_plan: list[dict[str, Any]] = []
    for scene_index, shot in enumerate(screenshots):
        material = evidence[min(scene_index, len(evidence) - 1)] if evidence else {}
        role = str(material.get("role") or "hero")
        composition = str(material.get("composition") or (SITE_MATERIAL_ROLES.get(role, {}) or {}).get("composition") or "full-bleed")
        highlight = shot.get("highlight") if isinstance(shot.get("highlight"), dict) else {}
        crop = crop_from_highlight(highlight, role, composition, scene_index)
        visual_plan.append(
            {
                "scene_index": scene_index,
                "screenshot_id": str(shot.get("id") or f"site-shot-{scene_index + 1:02d}"),
                "role": role,
                "label": str(material.get("label") or "页面证据"),
                "provider": "heuristic",
                "crop": crop,
                "highlight": {
                    "left": max(2, min(84, crop["x"] - 18)),
                    "top": max(4, crop["y"] - 12),
                    "width": clamp_percent(float(highlight.get("width", 36) or 36), 36),
                    "height": clamp_percent(float(highlight.get("height", 22) or 22), 22),
                },
                "composition": composition,
                "shot": str(material.get("shot") or (SITE_MATERIAL_ROLES.get(role, {}) or {}).get("shot") or "hero-overview"),
                "rationale": f"Focus {role} material around the detected evidence area.",
            }
        )
    return visual_plan


def apply_visual_plan_to_profile(site_profile: dict[str, Any], visual_plan: list[dict[str, Any]]) -> dict[str, Any]:
    if not visual_plan:
        return site_profile
    merged = dict(site_profile)
    screenshots = [dict(item) for item in merged.get("screenshots", []) if isinstance(item, dict)]
    by_id = {str(item.get("screenshot_id", "")): item for item in visual_plan}
    for index, shot in enumerate(screenshots):
        plan = by_id.get(str(shot.get("id", ""))) or (visual_plan[index] if index < len(visual_plan) else None)
        if not plan:
            continue
        shot["visual_plan"] = plan
    merged["screenshots"] = screenshots
    merged["visual_plan"] = visual_plan
    return merged


def ensure_visual_plan(site_profile: dict[str, Any]) -> dict[str, Any]:
    screenshots = site_profile.get("screenshots", [])
    if not isinstance(screenshots, list) or not screenshots:
        return site_profile
    visual_plan = site_profile.get("visual_plan") if isinstance(site_profile.get("visual_plan"), list) else []
    if not visual_plan:
        visual_plan = heuristic_visual_plan(site_profile)
    return apply_visual_plan_to_profile(site_profile, visual_plan)


def site_profile_screenshot_paths(project_dir: Path | None, site_profile: dict[str, Any], max_images: int = 6) -> list[Path]:
    paths: list[Path] = []
    for shot in site_profile.get("screenshots", []) if isinstance(site_profile.get("screenshots"), list) else []:
        if not isinstance(shot, dict) or not shot.get("path"):
            continue
        path = Path(str(shot["path"]))
        if not path.is_absolute() and project_dir:
            path = project_dir / path
        if path.exists():
            paths.append(path.resolve())
        if len(paths) >= max_images:
            break
    return paths


def vision_plan_payload(images: list[Path], site_profile: dict[str, Any], model: str) -> dict[str, Any]:
    schema = {
        "type": "object",
        "required": ["visual_plan"],
        "properties": {
            "visual_plan": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "scene_index": {"type": "number"},
                        "screenshot_id": {"type": "string"},
                        "role": {"type": "string"},
                        "label": {"type": "string"},
                        "crop": {
                            "type": "object",
                            "properties": {
                                "x": {"type": "number"},
                                "y": {"type": "number"},
                                "zoom": {"type": "number"},
                                "pan": {"type": "number"},
                            },
                        },
                        "rationale": {"type": "string"},
                    },
                },
            }
        },
    }
    content: list[dict[str, Any]] = [
        {
            "type": "text",
            "text": (
                "你是网页介绍视频的前置视觉导演。请查看真实网页截图，并为每个镜头选择最适合的裁切中心、缩放和关注区域。"
                "只返回 JSON。crop.x/crop.y 是百分比 0-100，zoom 建议 1.02-1.22，pan 建议 -0.8 到 0.8。"
                "优先让真实网页主体清晰、少露无关空白，避免遮挡正文和导航。"
            ),
        },
        {
            "type": "text",
            "text": json.dumps(
                {
                    "site": {
                        "title": site_profile.get("title", ""),
                        "brand_name": site_profile.get("brand_name", ""),
                        "source_url": site_profile.get("source_url", ""),
                        "primary_roles": site_profile.get("primary_roles", []),
                        "story_evidence": site_profile.get("story_evidence", [])[:6],
                        "screenshots": [
                            {"id": item.get("id"), "path": item.get("path"), "highlight": item.get("highlight", {})}
                            for item in site_profile.get("screenshots", [])[: len(images)]
                            if isinstance(item, dict)
                        ],
                    },
                    "schema": schema,
                    "image_order": [path.name for path in images],
                },
                ensure_ascii=False,
            ),
        },
    ]
    for path in images:
        content.append({"type": "text", "text": f"SCREENSHOT: {path.name}"})
        content.append({"type": "image_url", "image_url": {"url": image_data_url(path)}})
    return {
        "model": model,
        "temperature": 0.1,
        "response_format": {"type": "json_object"},
        "messages": [{"role": "user", "content": content}],
    }


def normalize_visual_plan(raw_plan: list[Any], fallback_plan: list[dict[str, Any]]) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []
    for index, fallback in enumerate(fallback_plan):
        item = raw_plan[index] if index < len(raw_plan) and isinstance(raw_plan[index], dict) else {}
        crop = item.get("crop") if isinstance(item.get("crop"), dict) else {}
        fallback_crop = fallback.get("crop", {})
        normalized.append(
            {
                **fallback,
                "provider": str(item.get("provider") or "openrouter"),
                "role": str(item.get("role") or fallback.get("role", "")),
                "label": str(item.get("label") or fallback.get("label", "")),
                "rationale": str(item.get("rationale") or fallback.get("rationale", "")),
                "crop": {
                    "x": clamp_percent(float(crop.get("x", fallback_crop.get("x", 50)) or 50), 50),
                    "y": clamp_percent(float(crop.get("y", fallback_crop.get("y", 24)) or 24), 24),
                    "zoom": max(1.0, min(1.28, float(crop.get("zoom", fallback_crop.get("zoom", 1.06)) or 1.06))),
                    "pan": max(-0.9, min(0.9, float(crop.get("pan", fallback_crop.get("pan", 0)) or 0))),
                },
            }
        )
    return normalized


def register_site_screenshot_assets(project_dir: Path, screenshots: list[dict[str, Any]]) -> None:
    for shot in screenshots:
        asset_id = str(shot.get("id", "site-shot"))
        path_value = str(shot.get("path", ""))
        if not path_value:
            continue
        path = Path(path_value)
        if not path.is_absolute():
            path = project_dir / path_value
        if path.exists():
            register_asset(
                project_dir,
                asset_id,
                "image",
                path,
                "website-screenshot",
                {"url": shot.get("url", ""), "scroll_y": shot.get("scroll_y", 0), "width": shot.get("width", 0), "height": shot.get("height", 0)},
            )


SITE_ASSET_INVENTORY_JS = r"""
(function(){
  function clean(value){ return String(value || '').trim(); }
  function selectorFor(el){
    if (!el || !el.tagName) return '';
    var label = el.tagName.toLowerCase();
    if (el.id) return label + '#' + el.id;
    if (el.className && typeof el.className === 'string') {
      var cls = el.className.trim().split(/\s+/).slice(0,2).join('.');
      if (cls) return label + '.' + cls;
    }
    return label;
  }
  function sizeOf(el){
    var rect = el && el.getBoundingClientRect ? el.getBoundingClientRect() : {width: 0, height: 0};
    return {width: Math.round(rect.width || el.naturalWidth || el.videoWidth || 0), height: Math.round(rect.height || el.naturalHeight || el.videoHeight || 0)};
  }
  var images = [];
  Array.from(document.images || []).forEach(function(img){
    var size = sizeOf(img);
    images.push({url: clean(img.currentSrc || img.src), alt: clean(img.alt), width: size.width, height: size.height, kind: 'img', selector: selectorFor(img)});
  });
  Array.from(document.querySelectorAll('*')).slice(0, 900).forEach(function(el){
    var style = window.getComputedStyle(el);
    var bg = style && style.backgroundImage;
    if (bg && bg !== 'none') {
      var matches = bg.match(/url\(["']?([^"')]+)["']?\)/g) || [];
      matches.slice(0, 4).forEach(function(match){
        var url = match.replace(/^url\(["']?/, '').replace(/["']?\)$/, '');
        var size = sizeOf(el);
        images.push({url: clean(url), width: size.width, height: size.height, kind: 'css-background', selector: selectorFor(el)});
      });
    }
  });
  var icons = [];
  Array.from(document.querySelectorAll('link[rel], meta[property], meta[name]')).forEach(function(el){
    var rel = clean(el.getAttribute('rel') || el.getAttribute('property') || el.getAttribute('name')).toLowerCase();
    var href = clean(el.getAttribute('href') || el.getAttribute('content'));
    if (!href) return;
    if (/(icon|apple-touch-icon|mask-icon|manifest|og:image|twitter:image)/.test(rel)) {
      icons.push({url: href, rel: rel, type: clean(el.getAttribute('type')), sizes: clean(el.getAttribute('sizes'))});
    }
  });
  Array.from(document.querySelectorAll('svg image, img[src$=".svg"]')).forEach(function(el){
    var href = clean(el.getAttribute('href') || el.getAttribute('xlink:href') || el.getAttribute('src'));
    if (href) icons.push({url: href, rel: 'svg-reference'});
  });
  var fonts = [];
  if (document.fonts) {
    Array.from(document.fonts).forEach(function(font){ fonts.push({family: clean(font.family).replace(/^["']|["']$/g, ''), status: clean(font.status), source: 'document.fonts'}); });
  }
  Array.from(document.querySelectorAll('link[href*="fonts."], link[href*="font"]')).forEach(function(el){
    fonts.push({family: clean(el.getAttribute('href')), source: 'font-link'});
  });
  Array.from(document.querySelectorAll('body, h1, h2, h3, p, button, a')).slice(0, 120).forEach(function(el){
    var family = clean(window.getComputedStyle(el).fontFamily).split(',')[0].replace(/^["']|["']$/g, '');
    if (family) fonts.push({family: family, source: 'computed-style'});
  });
  var animations = [];
  Array.from(document.querySelectorAll('*')).slice(0, 900).forEach(function(el){
    var style = window.getComputedStyle(el);
    if (style.animationName && style.animationName !== 'none') animations.push({type: 'css-animation', name: style.animationName, duration: style.animationDuration, selector: selectorFor(el)});
    if ((parseFloat(style.transitionDuration) || 0) > 0) animations.push({type: 'css-transition', property: style.transitionProperty, duration: style.transitionDuration, selector: selectorFor(el)});
  });
  if (document.getAnimations) {
    document.getAnimations().slice(0, 80).forEach(function(anim){
      var effect = anim.effect && anim.effect.getTiming ? anim.effect.getTiming() : {};
      animations.push({type: 'web-animation', duration: Math.round(effect.duration || 0), selector: selectorFor(anim.effect && anim.effect.target)});
    });
  }
  var media = [];
  Array.from(document.querySelectorAll('video, audio, source')).forEach(function(el){
    var size = sizeOf(el);
    media.push({url: clean(el.currentSrc || el.src || el.getAttribute('src')), kind: el.tagName.toLowerCase(), width: size.width, height: size.height, poster: clean(el.getAttribute('poster'))});
  });
  var scripts = [];
  Array.from(document.scripts || []).forEach(function(script){
    var src = clean(script.src);
    var text = clean(script.textContent).slice(0, 240).toLowerCase();
    if (src || /lottie|bodymovin|webgl|three\.js|gsap/.test(text)) {
      scripts.push({url: src || window.location.href, kind: /lottie|bodymovin/.test((src + text).toLowerCase()) ? 'lottie-hint' : 'script'});
    }
  });
  var stylesheets = [];
  Array.from(document.querySelectorAll('link[rel~="stylesheet"]')).forEach(function(el){ stylesheets.push({url: clean(el.href || el.getAttribute('href')), kind: 'stylesheet'}); });
  var canvases = [];
  Array.from(document.querySelectorAll('canvas')).forEach(function(canvas){
    var kind = 'canvas';
    try {
      if (canvas.getContext('webgl') || canvas.getContext('webgl2')) kind = 'webgl';
    } catch (e) {}
    var size = sizeOf(canvas);
    canvases.push({kind: kind, width: size.width, height: size.height, selector: selectorFor(canvas)});
  });
  return {images: images, icons: icons, fonts: fonts, animations: animations, media: media, scripts: scripts, stylesheets: stylesheets, canvases: canvases};
})()
"""


def collect_site_asset_inventory(client: "DevToolsClient", source_url: str) -> dict[str, Any]:
    result = client.call("Runtime.evaluate", {"expression": SITE_ASSET_INVENTORY_JS, "returnByValue": True})
    raw = result.get("result", {}).get("value", {})
    return normalize_site_asset_inventory(source_url, raw if isinstance(raw, dict) else {})


def _site_asset_filename(url: str, index: int) -> str:
    parsed = urllib.parse.urlparse(url)
    name = Path(urllib.parse.unquote(parsed.path)).name or f"asset-{index:03d}"
    stem = re.sub(r"[^A-Za-z0-9._-]+", "-", name).strip(".-") or f"asset-{index:03d}"
    if "." not in stem:
        ext = mimetypes.guess_extension(mimetypes.guess_type(url)[0] or "") or ".bin"
        stem += ext
    return f"{index:03d}-{stem}"[:96]


def download_site_asset_inventory(inventory: dict[str, Any], output_dir: Path) -> list[dict[str, Any]]:
    downloads: list[dict[str, Any]] = []
    candidates: list[tuple[str, dict[str, Any]]] = []
    for category in ("images", "icons", "stylesheets"):
        for item in inventory.get(category, []):
            if isinstance(item, dict) and item.get("url"):
                candidates.append((category, item))
    output_dir.mkdir(parents=True, exist_ok=True)
    for index, (category, item) in enumerate(candidates[:80], start=1):
        url = str(item.get("url", ""))
        target = output_dir / _site_asset_filename(url, index)
        try:
            download_url(url, str(target))
        except Exception as exc:
            downloads.append({"url": url, "category": category, "ok": False, "error": str(exc)[:180]})
            continue
        downloads.append({"url": url, "category": category, "ok": True, "path": str(target)})
    return downloads


def site_evidence_for_scene(site_profile: dict[str, Any] | None, scene_index: int) -> dict[str, str]:
    evidence = (site_profile or {}).get("story_evidence") or (site_profile or {}).get("evidence", [])
    if not isinstance(evidence, list) or not evidence:
        return {}
    return evidence[min(scene_index, len(evidence) - 1)] if isinstance(evidence[min(scene_index, len(evidence) - 1)], dict) else {}


def site_screenshot_for_scene(site_profile: dict[str, Any] | None, scene_index: int) -> dict[str, Any]:
    screenshots = (site_profile or {}).get("screenshots", [])
    if not isinstance(screenshots, list) or not screenshots:
        return {}
    item = screenshots[min(scene_index, len(screenshots) - 1)]
    return item if isinstance(item, dict) else {}


def clamp_percent(value: float, default: float) -> float:
    if not math.isfinite(value):
        return default
    return max(0.0, min(100.0, value))


def build_site_screenshot_html(site_profile: dict[str, Any] | None, scene_index: int) -> str:
    shot = site_screenshot_for_scene(site_profile, scene_index)
    path = str(shot.get("path", "") or "")
    if not path:
        return ""
    scroll_y = int(float(shot.get("scroll_y", 0) or 0))
    evidence = site_evidence_for_scene(site_profile, scene_index)
    label = str(evidence.get("label", "") or "页面证据")[:36]
    highlight = shot.get("highlight") if isinstance(shot.get("highlight"), dict) else {}
    left = clamp_percent(float(highlight.get("left", 8 + (scene_index * 17) % 42) or 0), 8)
    top = clamp_percent(float(highlight.get("top", 16 + (scene_index * 13) % 46) or 0), 16)
    width = clamp_percent(float(highlight.get("width", 34 + (scene_index * 11) % 30) or 0), 34)
    height = clamp_percent(float(highlight.get("height", 22 + (scene_index * 7) % 18) or 0), 22)
    ratio = min(1.0, scroll_y / max(1.0, float(shot.get("scroll_height", 3200) or 3200)))
    visual_plan = shot.get("visual_plan") if isinstance(shot.get("visual_plan"), dict) else {}
    crop = visual_plan.get("crop") if isinstance(visual_plan.get("crop"), dict) else {}
    crop_x = clamp_percent(float(crop.get("x", left + width / 2) or 50), 50)
    crop_y = clamp_percent(float(crop.get("y", top + height / 2) or 24), 24)
    crop_zoom = max(1.0, min(1.28, float(crop.get("zoom", 1.04) or 1.04)))
    crop_pan = max(-0.9, min(0.9, float(crop.get("pan", (crop_x - 50) / 50) or 0)))
    visual_provider = str(visual_plan.get("provider") or "heuristic") if visual_plan else "none"
    return (
        f'<figure class="site-screenshot" data-site-shot="{html_lib.escape(str(shot.get("id", "")))}" data-scroll-y="{scroll_y}" '
        f'data-visual-plan="{html_lib.escape(visual_provider)}" '
        f'style="--hl-left:{left}%;--hl-top:{top}%;--hl-width:{width}%;--hl-height:{height}%;--scroll-ratio:{ratio:.3f};'
        f'--crop-x:{crop_x}%;--crop-y:{crop_y}%;--crop-zoom:{crop_zoom:.3f};--shot-pan:{crop_pan:.3f}">'
        f'<div class="site-shot-top"><i></i><span>LIVE PAGE CAPTURE</span><b>{html_lib.escape(str(shot.get("id", "site-shot")).upper())}</b></div>'
        f'<div class="site-shot-frame"><img src="{html_lib.escape(path)}" alt="Real website screenshot" />'
        f'<span class="site-scan-highlight"><b>{html_lib.escape(label)}</b></span>'
        f'<span class="site-shot-ruler"><i></i></span></div>'
        f'<figcaption>真实网页截图 · scroll {scroll_y}px</figcaption></figure>'
    )


def selected_site_story_evidence(site_profile: dict[str, Any], scene_count: int) -> list[dict[str, str]]:
    semantic_sections = [item for item in site_profile.get("semantic_sections", []) if isinstance(item, dict)]
    if semantic_sections:
        selected: list[dict[str, Any]] = []
        seen_roles: set[str] = set()
        for item in semantic_sections:
            role = str(item.get("role", ""))
            if role in seen_roles and len(selected) < min(scene_count, len(SITE_ROLE_ORDER)):
                continue
            selected.append(item)
            if role:
                seen_roles.add(role)
            if len(selected) >= scene_count:
                break
        if len(selected) < scene_count:
            for item in semantic_sections:
                if item in selected:
                    continue
                selected.append(item)
                if len(selected) >= scene_count:
                    break
        if len(selected) < scene_count:
            selected.extend([item for item in site_profile.get("evidence", []) if isinstance(item, dict) and item not in selected][: scene_count - len(selected)])
        return [dict(item) for item in selected[:scene_count]]
    headings = [str(item) for item in site_profile.get("headings", []) if str(item).strip()]
    sections = [item for item in site_profile.get("sections", []) if isinstance(item, dict)]
    ctas = [str(item) for item in site_profile.get("ctas", []) if str(item).strip()]
    selected: list[dict[str, str]] = []
    for index, heading in enumerate(headings[: max(1, scene_count - 1)]):
        selected.append({"kind": "heading", "label": heading, "text": heading, "rank": str(index + 1)})
    for index, section in enumerate(sections):
        if len(selected) >= max(1, scene_count - 1):
            break
        label = str(section.get("label", "") or section.get("text", "") or f"页面模块 {index + 1}")
        text = str(section.get("text", "") or label)
        if any(item["label"] == label for item in selected):
            continue
        selected.append({"kind": "section", "label": label, "text": text, "rank": str(index + 1)})
    if ctas and scene_count > 1:
        selected = selected[: scene_count - 1]
        selected.append({"kind": "cta", "label": ctas[0], "text": f"页面行动入口：{ctas[0]}", "rank": "1"})
    while len(selected) < scene_count and headings:
        heading = headings[len(selected) % len(headings)]
        selected.append({"kind": "heading", "label": heading, "text": heading, "rank": str(len(selected) + 1)})
    return selected[:scene_count]


def is_longform_duration(duration: float) -> bool:
    return duration >= LONGFORM_THRESHOLD


def storyboard_scene_limit(duration: float) -> int:
    if is_longform_duration(duration):
        return min(LONGFORM_MAX_STORYBOARD_SCENES, max(6, int(round(duration / 4.0))))
    return MAX_STORYBOARD_SCENES


def brief_storyboard_scene_count(duration: float) -> int:
    if is_longform_duration(duration):
        return storyboard_scene_limit(duration)
    return 3


def storyboard_from_site(site_profile: dict[str, Any], duration: float) -> list[dict[str, Any]]:
    evidence = [item for item in site_profile.get("evidence", []) if isinstance(item, dict)]
    if not evidence:
        return storyboard_from_brief(str(site_profile.get("summary", "介绍这个官网。")), duration)
    scene_limit = storyboard_scene_limit(duration)
    scene_count = min(scene_limit, max(3, min(len(evidence), scene_limit)))
    scene_count = max(2, min(scene_count, max(2, int(duration / MIN_SITE_SCENE_DURATION))))
    selected_evidence = selected_site_story_evidence(site_profile, scene_count) or evidence[:scene_count]
    site_profile["story_evidence"] = selected_evidence
    storyboard: list[dict[str, Any]] = []
    document_source = is_document_source(site_profile)
    for index in range(scene_count):
        item = selected_evidence[index]
        label = str(item.get("label", "") or ("资料重点" if document_source else "网页证据") + f" {index + 1}")
        text = str(item.get("text", "") or label)
        start = duration * index / scene_count
        end = duration * (index + 1) / scene_count
        if document_source and index == 0:
            intent = f"项目定位：{label}。介绍先说明核心主张，再进入能力和使用路径。"
        elif document_source and (item.get("kind") == "cta" or index == scene_count - 1):
            intent = f"下一步：{label}。把资料中的行动入口收束成清晰选择。"
        elif document_source:
            role = "能力结构" if index == 1 else "可信线索"
            intent = f"{role}：{label}。这一部分补充项目能力、适用场景和判断依据。"
        elif index == 0:
            intent = f"首屏定位：{label}。主视觉先呈现核心主张，再把用户引向导航与行动入口。"
        elif item.get("kind") == "cta" or index == scene_count - 1:
            intent = f"行动路径：{label}。页面把浏览意图收束到明确入口，降低下一步操作成本。"
        else:
            role = "内容结构" if index == 1 else "可信度线索"
            intent = f"{role}：{label}。这个模块补充研究、产品或公共议题信息，形成更完整的判断路径。"
        storyboard.append({"id": safe_scene_id(f"site-{index + 1}-{item.get('kind', 'evidence')}", index), "start": round(start, 3), "end": round(end, 3), "intent": intent})
    return storyboard


def mostly_latin_text(value: str) -> bool:
    letters = [char for char in value if char.isalpha()]
    if not letters:
        return False
    latin = sum(1 for char in letters if "a" <= char.lower() <= "z")
    return latin / max(1, len(letters)) > 0.72


DOCUMENT_SOURCE_TYPES = {"markdown", "text", "github-readme"}


def is_document_source(site_profile: dict[str, Any] | None) -> bool:
    return str((site_profile or {}).get("source_type", "")).strip().lower() in DOCUMENT_SOURCE_TYPES


def source_material_label(site_profile: dict[str, Any] | None) -> str:
    source_type = str((site_profile or {}).get("source_type", "")).strip().lower()
    if source_type == "github-readme":
        return "README"
    if source_type == "markdown":
        return "Markdown 文档"
    if source_type == "text":
        return "文本资料"
    return "官网"


def narration_from_site(site_profile: dict[str, Any]) -> str:
    document_source = is_document_source(site_profile)
    material_label = source_material_label(site_profile)
    brand_name = str(site_profile.get("brand_name") or site_profile.get("title") or ("这个项目" if document_source else "这个官网"))
    summary = str(site_profile.get("summary", "")).strip()
    headings = [clean_text(str(item)) for item in site_profile.get("headings", [])[:4] if clean_text(str(item))]
    ctas = [clean_text(str(item)) for item in site_profile.get("ctas", [])[:2] if clean_text(str(item))]
    sections = [
        clean_text(str(item.get("label") or item.get("text") or ""))
        for item in site_profile.get("sections", [])[:4]
        if isinstance(item, dict) and clean_text(str(item.get("label") or item.get("text") or ""))
    ]
    proof_points: list[str] = []
    for item in headings + sections:
        if item not in proof_points:
            proof_points.append(item)
        if len(proof_points) >= 3:
            break
    pieces = [f"这支视频快速看 {brand_name}{' 项目' if document_source and '项目' not in brand_name else ' 官网'}。"]
    if summary and not mostly_latin_text(summary):
        pieces.append(f"开头先把{'项目' if document_source else '品牌'}定位说清楚：{summary[:96]}。")
    else:
        if document_source:
            pieces.append(f"开头先提炼 {material_label} 的核心主张，再把能力、适用场景和行动入口串起来。")
        else:
            pieces.append("首屏先给出品牌定位，并把核心主张、导航和行动入口放在同一个判断场景里。")
    if proof_points:
        if len(proof_points) == 1:
            pieces.append(f"接着聚焦 {material_label} 里的关键段落，看它如何承接整体介绍。")
        else:
            if document_source:
                pieces.append("继续往下，资料用不同段落把能力、工作流和可信依据逐步展开，而不是只停留在一句口号。")
            else:
                pieces.append("继续往下，页面用不同模块把研究、产品或公共议题逐步展开，而不是只停留在一句口号。")
    if ctas:
        pieces.append(f"最后，{ctas[0]} 这类入口把兴趣转成下一步操作。")
    if document_source:
        pieces.append(f"整个介绍只基于{material_label}和资料原文，不混入无关素材。")
    else:
        pieces.append("整个介绍只基于官网截图和页面文本，不混入无关素材。")
    return "".join(pieces)


CONTENT_ATOM_RULES: tuple[tuple[tuple[str, ...], str, str, str], ...] = (
    (("terminal", "cli", "command line", "命令行", "终端"), "capabilities", "终端代理", "在开发者熟悉的命令行里理解任务、执行命令并推进修改。"),
    (("ide", "vs code", "jetbrains", "编辑器"), "capabilities", "IDE 协作", "把代码上下文、编辑器状态和模型建议放进同一条工作流。"),
    (("codebase", "repository", "repo", "代码库", "仓库"), "capabilities", "代码库理解", "先读取项目结构和上下文，再给出可落地的改动路径。"),
    (("edit files", "write code", "编辑文件", "修改代码"), "capabilities", "文件级修改", "不只生成建议，而是能围绕目标直接改文件、补实现、整理差异。"),
    (("run commands", "execute commands", "shell", "运行命令", "执行命令"), "workflows", "命令执行", "在生成之后继续运行命令、检查结果，并把反馈纳入下一轮修改。"),
    (("github", "gitlab", "pull request", "merge request", "pr", "issue"), "workflows", "Issue 到 PR", "把需求、代码修改、评审和提交衔接成团队熟悉的交付链路。"),
    (("test", "ci", "lint", "验证", "测试"), "proof_points", "验证闭环", "通过测试、日志或命令输出来确认改动是否真的成立。"),
    (("team", "enterprise", "团队", "企业"), "users", "开发团队", "适合多人协作的工程团队，把模型能力接入日常开发节奏。"),
    (("security", "permission", "approve", "安全", "权限", "审计"), "constraints", "可信边界", "关键动作需要保留权限、审计和人工判断，避免把自动化当成黑箱。"),
    (("docs", "documentation", "api", "文档", "开发者"), "next_actions", "开发者入口", "下一步通常是阅读文档、接入工具链，并用真实代码库试跑。"),
)


def add_content_atom(target: dict[str, list[dict[str, str]]], category: str, label: str, value: str) -> None:
    bucket = target.setdefault(category, [])
    if any(item.get("label") == label for item in bucket):
        return
    bucket.append({"label": label, "value": value})


def content_text_sources(site_profile: dict[str, Any], brief: str) -> list[str]:
    sources = [brief, str(site_profile.get("title", "")), str(site_profile.get("summary", "")), str(site_profile.get("text_sample", ""))]
    sources.extend(str(item) for item in site_profile.get("headings", []) if str(item).strip())
    for section in site_profile.get("sections", []):
        if isinstance(section, dict):
            sources.append(str(section.get("label", "")))
            sources.append(str(section.get("text", "")))
    for item in site_profile.get("evidence", []):
        if isinstance(item, dict):
            sources.append(str(item.get("label", "")))
            sources.append(str(item.get("text", "")))
    sources.extend(str(item) for item in site_profile.get("ctas", []) if str(item).strip())
    return [clean_text(item) for item in sources if clean_text(item)]


def build_content_brief(site_profile: dict[str, Any], brief: str) -> dict[str, Any]:
    sources = content_text_sources(site_profile, brief)
    combined = " ".join(sources).lower()
    document_source = is_document_source(site_profile)
    atoms: dict[str, list[dict[str, str]]] = {
        "capabilities": [],
        "workflows": [],
        "users": [],
        "proof_points": [],
        "constraints": [],
        "next_actions": [],
    }
    for tokens, category, label, value in CONTENT_ATOM_RULES:
        if any(token.lower() in combined for token in tokens):
            add_content_atom(atoms, category, label, value)
    role_defaults = {
        "hero": ("定位", "首屏负责给出产品是什么、为谁服务，以及为什么现在值得继续看。"),
        "product": ("产品能力", "页面把能力拆成可理解的模块，而不是只停留在品牌口号。"),
        "developer": ("开发者工作流", "重点在工具如何接入真实开发环境、命令和代码库上下文。"),
        "enterprise": ("团队落地", "面向团队时，价值来自协作、治理和可复用流程。"),
        "safety": ("安全边界", "可信表达需要同时说明能力、权限和复核边界。"),
        "research": ("研究依据", "研究内容为产品主张提供更长期的可信度来源。"),
        "cta": ("下一步", "行动入口把浏览兴趣收束为一次明确试用或了解。"),
    }
    for item in site_profile.get("semantic_sections", []):
        if not isinstance(item, dict):
            continue
        role = str(item.get("role", ""))
        if role not in role_defaults:
            continue
        label, value = role_defaults[role]
        category = "next_actions" if role == "cta" else ("constraints" if role == "safety" else ("proof_points" if role == "research" else "capabilities"))
        add_content_atom(atoms, category, label, value)
    for cta in site_profile.get("ctas", [])[:3]:
        cta_text = clean_text(str(cta))
        if cta_text:
            add_content_atom(atoms, "next_actions", cta_text[:22], "这是页面显式给出的下一步入口，适合作为结尾行动。")
    brand_name = str(site_profile.get("brand_name") or site_profile.get("title") or chinese_topic_from_brief(brief))
    thesis = next((source for source in sources if not mostly_latin_text(source) and len(source) > 12), "")
    if not thesis:
        if document_source:
            thesis = f"{brand_name} 的介绍应围绕原始资料，讲清对象、能力、流程和边界。"
        else:
            thesis = f"{brand_name} 的介绍应围绕真实页面证据，讲清对象、能力、流程和边界。"
    talking_points: list[dict[str, str]] = []
    for category in ("capabilities", "workflows", "users", "proof_points", "constraints", "next_actions"):
        talking_points.extend({**item, "category": category} for item in atoms.get(category, []))
    return {
        "product_name": brand_name,
        "source_url": site_profile.get("source_url", ""),
        "thesis": compact_label(thesis, f"{brand_name} 产品介绍", 140),
        **atoms,
        "talking_points": talking_points[:12],
    }


def enrich_site_profile_content(site_profile: dict[str, Any], brief: str) -> dict[str, Any]:
    if not site_profile:
        return site_profile
    enriched = dict(site_profile)
    enriched["content_brief"] = build_content_brief(enriched, brief)
    return enriched


def content_point_for_scene(site_profile: dict[str, Any] | None, scene_index: int) -> dict[str, str]:
    content_brief = (site_profile or {}).get("content_brief", {}) if isinstance(site_profile, dict) else {}
    points = content_brief.get("talking_points", []) if isinstance(content_brief, dict) else []
    if not isinstance(points, list) or not points:
        return {}
    point = points[min(scene_index, len(points) - 1)]
    return point if isinstance(point, dict) else {}


def brand_file_path(project_dir: Path) -> Path:
    return project_dir / "assets" / "brand.json"


def write_brand_file(project_dir: Path, brand: dict[str, Any], source: str = "brand-extract") -> Path:
    output = brand_file_path(project_dir)
    output.parent.mkdir(parents=True, exist_ok=True)
    payload = {"source": source, "brand": brand}
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    if (project_dir / "senseframe.json").exists():
        register_asset(project_dir, "brand", "json", output, "brand-profile", {"source_url": brand.get("source_url", "")})
    return output


def read_brand_file(path: str | None) -> dict[str, Any]:
    if not path:
        return {}
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    return payload.get("brand", payload) if isinstance(payload, dict) else {}


def set_timeline_source(project_dir: Path, source: str = "./assets/timeline.json") -> None:
    index_path = project_dir / "index.html"
    if not index_path.exists():
        return
    markup = index_path.read_text(encoding="utf-8")
    if "data-timeline-source" in markup:
        markup = re.sub(r'data-timeline-source=["\'][^"\']*["\']', f'data-timeline-source="{source}"', markup, count=1)
    else:
        markup = re.sub(r'(<div\b[^>]*data-composition-id=["\'][^"\']+["\'])', rf'\1 data-timeline-source="{source}"', markup, count=1)
    index_path.write_text(markup, encoding="utf-8")


def set_audio_source(project_dir: Path, source: str = "./assets/audio-data.json") -> None:
    index_path = project_dir / "index.html"
    if not index_path.exists():
        return
    markup = index_path.read_text(encoding="utf-8")
    if "data-audio-source" in markup:
        markup = re.sub(r'data-audio-source=["\'][^"\']*["\']', f'data-audio-source="{source}"', markup, count=1)
    else:
        markup = re.sub(r'(<div\b[^>]*data-composition-id=["\'][^"\']+["\'])', rf'\1 data-audio-source="{source}"', markup, count=1)
    index_path.write_text(markup, encoding="utf-8")


def build_asset_slots(enable_image: bool, enable_video: bool) -> str:
    slots: list[str] = []
    if enable_image:
        slots.append(
            '<div class="media-slot image" data-start="0" data-duration="{duration}">'
            '<img data-asset="hero-image" src="" alt="Generated visual reference" />'
            '</div>'
        )
    if enable_video:
        slots.append(
            '<div class="media-slot video" data-start="{beat}" data-duration="{beat_last}">'
            '<video data-asset="broll-video" src="" muted playsinline></video>'
            '</div>'
        )
    return "\n    ".join(slots)


def safe_scene_id(raw_id: Any, index: int) -> str:
    raw = str(raw_id or f"scene-{index + 1}").strip().lower()
    safe = re.sub(r"[^a-z0-9_-]+", "-", raw).strip("-")
    return safe or f"scene-{index + 1}"


def split_intent(intent: str, fallback: str) -> tuple[str, str]:
    cleaned = " ".join(str(intent or fallback).split())
    if not cleaned:
        cleaned = fallback
    parts = re.split(r"[。.!?！？；;：:]", cleaned, maxsplit=1)
    title = parts[0].strip() or fallback
    body_source = parts[1].strip() if len(parts) > 1 and parts[1].strip() else cleaned
    body_sentences = [part.strip() for part in re.split(r"[。.!?！？；;]", body_source) if part.strip()]
    while len(body_sentences) > 1 and mostly_latin_text(body_sentences[0]):
        body_sentences.pop(0)
    if body_sentences:
        body_source = "。".join(body_sentences)
    body = body_source if len(body_source) <= 96 else body_source[:94].rstrip() + "…"
    return title[:28], body


DIRECTOR_NOTE_PATTERNS = (
    "镜头",
    "开篇展示",
    "展示页面",
    "展示其",
    "證明其",
    "证明其",
    "切换到",
    "滚动到",
    "滑动到",
    "定格",
    "特写",
    "高亮展示",
    "怎么排版",
    "排版",
    "画面",
    "camera",
    "shot",
    "layout",
    "核心依据",
    "PAGE SIGNAL",
    "Website Brief",
    "真实证据",
    "页面线索",
    "使用含义",
)


def is_director_note(value: str) -> bool:
    lower = str(value or "").lower()
    return any(token.lower() in lower for token in DIRECTOR_NOTE_PATTERNS)


def display_safe_text(value: str, fallback: str = "", max_chars: int = 96) -> str:
    cleaned = clean_text(str(value or ""))
    fallback_clean = clean_text(str(fallback or ""))
    if not cleaned or is_director_note(cleaned):
        cleaned = fallback_clean
    if not cleaned:
        cleaned = "来自真实网页内容。"
    return cleaned[:max_chars].rstrip()


def quoted_story_phrases(value: str) -> list[str]:
    phrases: list[str] = []
    for match in re.findall(r"[「“\"]([^」”\"]{2,64})[」”\"]", str(value or "")):
        cleaned = clean_text(match)
        if cleaned and cleaned not in phrases:
            phrases.append(cleaned)
    return phrases


def public_copy_from_authored_intent(value: str) -> tuple[str, str]:
    cleaned = clean_text(str(value or ""))
    patterns = [
        r"^(?:展示其|演示其|證明其|证明其|驗證其|验证其)([^：:，。；;]+)[：:](.+)$",
        r"^(?:展示其|演示其|證明其|证明其|驗證其|验证其)([^，。；;]+?)(?:的(?:供給規模|供给规模|服務範圍|服务范围|能力|功能|支撐|支撑|底層機制|底层机制)|。|，|；|;|$)(.*)$",
    ]
    for pattern in patterns:
        match = re.search(pattern, cleaned)
        if not match:
            continue
        title = clean_text(match.group(1)).strip("：: ，,。；;")
        body = clean_text(match.group(2) if len(match.groups()) > 1 else "").strip("：: ，,。；;")
        body = re.sub(r"^(?:並補充|并补充|以及|和|與|与)", "", body).strip("：: ，,。；;")
        if title or body:
            return title, body
    return "", ""


def storyboard_insight_copy(intent: str, fallback_title: str, fallback_body: str) -> tuple[str, str]:
    cleaned = clean_text(str(intent or ""))
    quoted = quoted_story_phrases(cleaned)
    public_title, public_body = public_copy_from_authored_intent(cleaned)
    authored_patterns = [
        r"明确产品定位为([^，。；;]+)",
        r"明确产品为([^，。；;]+)",
        r"演示其([^，。；;]+?)(?:的底层机制|的机制|。|，|；|;|$)",
        r"[證证]明其([^，。；;]+?)(?:的能力|。|，|；|;|$)",
        r"验证其([^，。；;]+?)(?:的能力|。|，|；|;|$)",
        r"展示其([^，。；;]+?)(?:的具体功能|。|，|；|;|$)",
        r"展示([^，。；;]+?)(?:的操作流|的工作流链路|。|，|；|;|$)",
        r"对应官网([^，。；;]+?)(?:功能说明|功能|说明|证据|。|，|；|;|$)",
        r"匹配官网提到的([^，。；;]+?)(?:能力|功能|说明|证据|。|，|；|;|$)",
        r"明确标注([^，。；;]+)",
        r"末尾引导用户([^，。；;]+)",
        r"给出明确下一步行动[:：]([^，。；;]+)",
    ]
    extracted: list[str] = []
    for pattern in authored_patterns:
        for match in re.findall(pattern, cleaned):
            value = clean_text(match).strip("：: ")
            if value and value not in extracted:
                extracted.append(value)
    title = public_title or next((item for item in quoted if not re.fullmatch(r"核心能力\s*\d+", item, flags=re.I)), "")
    if not title:
        title = next((item for item in extracted if len(item) <= 34 and not mostly_latin_text(item)), "")
    segments = [segment.strip() for segment in re.split(r"[，,。；;]", cleaned) if segment.strip()]
    signal_tokens = (
        "终端",
        "IDE",
        "VS Code",
        "JetBrains",
        "Slack",
        "移动端",
        "代码库",
        "上下文",
        "文件",
        "命令",
        "测试",
        "GitHub",
        "GitLab",
        "Issue",
        "PR",
        "权限",
        "人工",
        "边界",
        "Pro",
        "团队",
        "短周期",
        "工作流",
        "迁移",
        "验证",
        "代码托管",
    )
    visual_verbs = ("展示", "演示", "动画", "罗列", "切换", "定格", "配文字", "标注", "镜头", "界面")
    useful: list[str] = []
    for segment in segments:
        normalized = re.sub(r"^(展示|演示|动画演示|罗列|切换到|定格|配文字标注|标注|对应官网)", "", segment).strip("：: ")
        if not normalized:
            continue
        has_signal = any(token.lower() in normalized.lower() for token in signal_tokens)
        is_visual_only = any(normalized.startswith(verb) for verb in visual_verbs) and not has_signal
        if is_visual_only:
            continue
        if title and title in normalized:
            continue
        if has_signal or quoted or not is_director_note(normalized):
            useful.append(normalized)
    if not title:
        title = next((segment for segment in useful if len(segment) <= 24 and not mostly_latin_text(segment)), "")
    if not title and quoted:
        title = quoted[0]
    body_candidates = [public_body] if public_body else []
    body_candidates.extend(item for item in extracted if item != title and item not in body_candidates)
    body_candidates.extend(item for item in useful if item != title and item not in body_candidates)
    if not body_candidates and len(quoted) > 1:
        body_candidates = quoted[1:]
    body = "，".join(body_candidates[:2]).strip("，,。 ")
    if not body and quoted:
        body = quoted[0]
    if not title:
        title = fallback_title
    if not body:
        body = fallback_body
    return display_safe_text(title, fallback_title, 34), display_safe_text(body, fallback_body, 128)


def storyboard_keywords(intent: str, scene_index: int) -> list[str]:
    tokens = [
        ("terminal", "终端"),
        ("命令行", "终端"),
        ("ide", "IDE"),
        ("VS Code", "VS Code"),
        ("JetBrains", "JetBrains"),
        ("Slack", "Slack"),
        ("移动端", "移动端"),
        ("代码库", "代码库"),
        ("上下文", "上下文"),
        ("编辑", "编辑文件"),
        ("文件", "编辑文件"),
        ("运行命令", "运行命令"),
        ("测试", "测试验证"),
        ("GitHub", "GitHub"),
        ("GitLab", "GitLab"),
        ("Issue", "Issue"),
        ("PR", "PR"),
        ("权限", "权限边界"),
        ("人工", "人工确认"),
        ("Pro", "Claude Pro"),
        ("团队", "团队协作"),
    ]
    lowered = str(intent or "").lower()
    found: list[str] = []
    for needle, label in tokens:
        if needle.lower() in lowered and label not in found:
            found.append(label)
    for phrase in quoted_story_phrases(intent):
        compact = phrase[:12]
        if compact and compact not in found:
            found.append(compact)
    fallback_sets = [
        ["品牌定位", "首页结构", "核心信息"],
        ["产品能力", "用户路径", "行动入口"],
        ["研究观点", "信任叙事", "页面证据"],
        ["总结", "适用人群", "下一步"],
    ]
    fallback = fallback_sets[scene_index % len(fallback_sets)]
    while len(found) < 3:
        found.append(fallback[len(found) % len(fallback)])
    return found[:4]


def has_authored_story_insight(intent: str) -> bool:
    if quoted_story_phrases(intent):
        return True
    text = str(intent or "")
    if re.search(r"(明确产品定位为|明确产品为|演示其|[證证]明其|[驗验]证其|展示其|对应官网|匹配官网提到的|明确标注|末尾引导用户|给出明确下一步行动)", text):
        return True
    return any(token in text for token in ("Issue", "PR", "GitHub", "GitLab", "VS Code", "JetBrains", "代码库", "运行命令", "编辑文件", "权限边界"))


def site_display_copy(
    site_profile: dict[str, Any] | None,
    scene_index: int,
    intent: str,
    headline: str,
) -> tuple[str, str]:
    site_profile = site_profile or {}
    document_source = is_document_source(site_profile)
    evidence = site_evidence_for_scene(site_profile, scene_index)
    content_point = content_point_for_scene(site_profile, scene_index)
    brand_name = str(site_profile.get("brand_name") or site_profile.get("title") or ("项目" if document_source else "官网"))
    summary = str(site_profile.get("summary") or "")
    label = str(evidence.get("label") or "")
    text = str(evidence.get("text") or "")
    role = str(evidence.get("role") or "")
    role_labels = {
        "hero": "首屏定位",
        "product": "产品能力",
        "research": "研究内容",
        "safety": "安全与信任",
        "developer": "开发者入口",
        "enterprise": "企业方案",
        "customer": "客户场景",
        "pricing": "定价信息",
        "cta": "行动入口",
    }
    intent_title, intent_body = split_intent(intent, headline or brand_name)
    story_title, story_body = storyboard_insight_copy(intent, intent_title, intent_body or headline or brand_name)
    if has_authored_story_insight(intent) and story_title and not is_director_note(story_title):
        title = story_title
    elif label and not mostly_latin_text(label):
        title = label
    elif content_point.get("label"):
        title = str(content_point["label"])
    elif role in role_labels:
        title = role_labels[role]
    elif scene_index == 0:
        title = f"{brand_name} 项目" if document_source else f"{brand_name} 官网"
    else:
        title = intent_title
    body_source = text or summary or headline
    if mostly_latin_text(body_source):
        if has_authored_story_insight(intent) and story_body and not mostly_latin_text(story_body):
            body_source = story_body
        elif content_point.get("value"):
            body_source = str(content_point["value"])
        elif intent_body and not mostly_latin_text(intent_body):
            body_source = intent_body
        elif document_source and scene_index == 0:
            body_source = "资料先给出项目定位，再展开核心能力与适用场景。"
        elif scene_index == 0:
            body_source = "首屏呈现品牌定位、导航结构与主要行动入口。"
        elif role == "cta":
            body_source = "资料把阅读兴趣收束到清晰的下一步操作。" if document_source else "页面把浏览意图收束到清晰的下一步操作。"
        else:
            body_source = "这一部分补充项目的核心能力与判断依据。" if document_source else "这一屏补充官网的核心模块与用户判断依据。"
    title = display_safe_text(title, brand_name, 28)
    fallback = summary or headline or ("来自原始资料内容。" if document_source else "来自真实网页内容。")
    body = display_safe_text(body_source, fallback, 112)
    return title, body


def scene_keywords(intent: str, index: int) -> list[str]:
    keyword_sets = [
        ["品牌定位", "首页结构", "核心信息"],
        ["产品能力", "用户路径", "行动入口"],
        ["研究观点", "信任叙事", "页面证据"],
        ["总结", "适用人群", "下一步"],
    ]
    lower = intent.lower()
    if "anthropic" in lower or "claude" in lower:
        return storyboard_keywords(intent, index) if storyboard_keywords(intent, index) else ["Claude", "AI Safety", "Research"]
    if "安全" in intent or "safety" in lower:
        return ["安全", "研究", "信任"]
    if "企业" in intent or "developer" in lower or "开发者" in intent:
        return ["企业", "开发者", "能力"]
    if "克隆" in intent or "clone" in lower:
        return ["声音克隆", "对比", "身份感"]
    if "搜索" in intent or "search" in lower:
        return ["搜索", "筛选", "匹配"]
    if "视频" in intent or "video" in lower:
        return ["视频", "字幕", "交付"]
    if "旁白" in intent or "tts" in lower:
        return ["TTS", "声波", "旁白"]
    return keyword_sets[index % len(keyword_sets)]


def source_scene_keywords(intent: str, index: int, site_profile: dict[str, Any] | None = None) -> list[str]:
    keywords = scene_keywords(intent, index)
    if not is_document_source(site_profile):
        return keywords
    replacements = {
        "首页结构": "资料结构",
        "页面证据": "资料依据",
        "用户路径": "使用路径",
        "信任叙事": "可信依据",
    }
    return [replacements.get(keyword, keyword) for keyword in keywords]


def visual_card_items(
    intent: str,
    headline: str,
    scene_index: int,
    brand: dict[str, Any] | None = None,
    site_profile: dict[str, Any] | None = None,
) -> list[tuple[str, str]]:
    scene_title, scene_body = split_intent(intent, headline or f"Scene {scene_index + 1}")
    keywords = scene_keywords(intent, scene_index)
    brand = brand or {}
    site_profile = site_profile or {}
    site_evidence = site_evidence_for_scene(site_profile, scene_index)
    document_source = is_document_source(site_profile)
    if site_evidence:
        headings = [str(item) for item in site_profile.get("headings", []) if str(item).strip()]
        ctas = [str(item) for item in site_profile.get("ctas", []) if str(item).strip()]
        material_label = source_material_label(site_profile)
        return [
            ("资料重点" if document_source else "页面重点", str(site_evidence.get("label", "资料段落" if document_source else "网页模块"))[:32]),
            ("原文摘录" if document_source else "页面原文", str(site_evidence.get("text", ""))[:46]),
            ("行动入口", ctas[scene_index % len(ctas)] if ctas else (f"来自{material_label}提取" if document_source else "来自官网 DOM 提取")),
        ]
    if brand:
        nav = [str(item) for item in brand.get("nav", []) if str(item).strip()]
        brand_keywords = [str(item) for item in brand.get("keywords", []) if str(item).strip()]
        voice = brand.get("voice", {}) if isinstance(brand.get("voice"), dict) else {}
        description = str(brand.get("description", "") or scene_body)
        return [
            ("品牌", str(brand.get("name", "Website"))[:28]),
            ("官网信息", description[:42]),
            (nav[0] if nav else keywords[0], "来自站点导航与页面元信息。"),
            (str(voice.get("tone", "")) or (brand_keywords[0] if brand_keywords else keywords[1]), str(voice.get("guidance", ""))[:42] or "让镜头结构贴合真实品牌。"),
        ]
    return [
        ("页面重点", scene_title),
        ("信息层级", scene_body[:42]),
        (keywords[0], "把网页内容转成可理解的主线。"),
        (keywords[1], "保留品牌语气，不混入无关产品素材。"),
    ]


def select_website_shot(intent: str, scene_index: int, scene_count: int) -> str:
    lower = intent.lower()
    if scene_index == scene_count - 1 or any(token in intent for token in ("总结", "号召", "下一步", "收束")):
        return "cta-summary"
    if scene_index == 0 or any(token in intent for token in ("官网", "首页", "品牌")):
        return "hero-overview"
    if any(token in intent for token in ("导航", "扫描", "栏目", "路径")):
        return "nav-scan"
    if any(token in lower for token in ("safety", "research", "policy")) or any(token in intent for token in ("安全", "研究", "政策", "信任")):
        return "trust-message"
    if any(token in lower for token in ("developer", "enterprise", "product")) or any(token in intent for token in ("开发者", "企业", "产品", "能力")):
        return "feature-zoom"
    return WEBSITE_SHOT_TYPES[scene_index % len(WEBSITE_SHOT_TYPES)]


def select_website_shot_for_scene(intent: str, scene_index: int, scene_count: int, evidence: dict[str, Any]) -> str:
    if evidence.get("shot"):
        return str(evidence["shot"])
    role = str(evidence.get("role", ""))
    if role in SITE_MATERIAL_ROLES:
        return str(SITE_MATERIAL_ROLES[role]["shot"])
    return select_website_shot(intent, scene_index, scene_count)


def select_composition_mode(shot_type: str, scene_index: int, scene_count: int, site_profile: dict[str, Any] | None = None, evidence: dict[str, Any] | None = None) -> str:
    if evidence and evidence.get("composition"):
        return str(evidence["composition"])
    role = str((evidence or {}).get("role", ""))
    if role in SITE_MATERIAL_ROLES:
        return str(SITE_MATERIAL_ROLES[role]["composition"])
    has_screenshots = bool((site_profile or {}).get("screenshots"))
    if scene_index == 0 and has_screenshots:
        return "full-bleed"
    if shot_type == "nav-scan":
        return "split-scan"
    if shot_type == "feature-zoom":
        return "zoom-callout"
    if shot_type == "trust-message":
        return "evidence-board"
    if shot_type == "cta-summary" or scene_index == scene_count - 1:
        return "cta-lockup"
    return COMPOSITION_MODES[scene_index % len(COMPOSITION_MODES)]


def camera_path_for_composition(composition_mode: str) -> str:
    return {
        "full-bleed": "hero-push",
        "split-scan": "lateral-scan",
        "zoom-callout": "macro-zoom",
        "evidence-board": "board-orbit",
        "cta-lockup": "lockup-dolly",
    }.get(composition_mode, "hero-push")


def camera_path_for_scene(composition_mode: str, evidence: dict[str, Any]) -> str:
    if evidence.get("camera"):
        return str(evidence["camera"])
    role = str(evidence.get("role", ""))
    if role in SITE_MATERIAL_ROLES:
        return str(SITE_MATERIAL_ROLES[role]["camera"])
    return camera_path_for_composition(composition_mode)


def composition_badge_html(
    composition_mode: str,
    scene_index: int,
    evidence_label: str,
    site_profile: dict[str, Any] | None = None,
) -> str:
    if is_document_source(site_profile):
        labels = {
            "full-bleed": "INTRO",
            "split-scan": "SOURCE MAP",
            "zoom-callout": "DETAIL",
            "evidence-board": "REFERENCE",
            "cta-lockup": "NEXT STEP",
        }
    else:
        labels = {
            "full-bleed": "FULL PAGE",
            "split-scan": "SCAN PATH",
            "zoom-callout": "DETAIL ZOOM",
            "evidence-board": "EVIDENCE BOARD",
            "cta-lockup": "CTA LOCKUP",
        }
    return (
        f'<div class="composition-badge"><span>{labels.get(composition_mode, "SHOT")}</span>'
        f'<b>{scene_index + 1:02d}</b><em>{html_lib.escape(evidence_label[:34] or ("source material" if is_document_source(site_profile) else "website evidence"))}</em></div>'
    )


def compact_label(value: str, fallback: str, limit: int = 26) -> str:
    cleaned = clean_text(str(value or fallback))
    return (cleaned or fallback)[:limit]


def executive_layout_for_scene(scene_index: int, world: str, claim: str) -> str:
    text = f"{world} {claim}"
    if scene_index == 0 or any(token in text for token in ("开场", "主张", "THESIS", "高层")):
        return "title-slate"
    if scene_index >= 5 or any(token in text for token in ("结尾", "收束", "OUTCOME", "最终价值", "最终")):
        return "final-lockup"
    if any(token in text for token in ("问题", "张力", "成本", "FRICTION", "风险")):
        return "tension-matrix"
    if any(token in text for token in ("系统", "流程", "FLOW", "能力", "工作流")):
        return "process-pipeline"
    if any(token in text for token in ("证据", "可信", "PROOF", "引用", "复核")):
        return "evidence-wall"
    if any(token in text for token in ("场景", "任务", "SCENARIOS", "落地")):
        return "scenario-desk"
    return "evidence-wall"


def production_spec_for_scene(
    brief: str,
    storyboard: list[dict[str, Any]],
    narration: str,
    headline: str,
    scene_index: int,
    site_profile: dict[str, Any] | None = None,
) -> dict[str, Any]:
    item = storyboard[scene_index]
    scene_title, scene_body = split_intent(str(item.get("intent", headline)), headline or f"Scene {scene_index + 1}")
    topic = chinese_topic_from_brief(brief)
    audience_match = re.search(r"面向([^。；;，,]+)", brief)
    audience = compact_label(audience_match.group(1), "核心使用者", 34) if audience_match else "核心使用者"
    site_evidence = site_evidence_for_scene(site_profile or {}, scene_index) if site_profile else {}
    if site_evidence:
        document_source = is_document_source(site_profile)
        content_point = content_point_for_scene(site_profile, scene_index)
        story_title, story_body = storyboard_insight_copy(str(item.get("intent", "")), scene_title, scene_body)
        if not has_authored_story_insight(str(item.get("intent", ""))) and content_point:
            story_title = str(content_point.get("label", "")) or story_title
            story_body = str(content_point.get("value", "")) or story_body
        evidence_label = compact_label(str(site_evidence.get("label", "")), scene_title, 34)
        evidence_text = compact_label(str(site_evidence.get("text", "")), scene_body, 72)
        product_meaning = compact_label(story_body, str(content_point.get("value", "")) or scene_body, 88)
        if not product_meaning and content_point:
            product_meaning = compact_label(str(content_point.get("value", "")), scene_body, 88)
        return {
            "scene_id": safe_scene_id(item.get("id"), scene_index),
            "layout": "evidence-wall",
            "title": story_title,
            "body": product_meaning,
            "world": "README 项目介绍" if document_source else "官网内容介绍",
            "mood": "克制、可信、带有研究笔记感",
            "claim": product_meaning if product_meaning else (f"这一部分解释资料中提到的 {evidence_label}。" if document_source else f"这一镜头解释官网中可见的 {evidence_label}。"),
            "metric": {"label": "SOURCE" if document_source else "SITE", "value": f"{scene_index + 1:02d}"},
            "proof_points": [
                {"label": (story_title[:18] if story_title else (str(content_point.get("label", "项目含义" if document_source else "产品含义"))[:18] if content_point else ("项目含义" if document_source else "产品含义"))), "value": product_meaning},
                {"label": "资料内容" if document_source else "页面内容", "value": evidence_label if mostly_latin_text(evidence_text) else evidence_text},
                {"label": "适用方式" if document_source else "服务价值", "value": compact_label(str(content_point.get("value", "")) if content_point else scene_body, "把资料内容转成清晰介绍" if document_source else "把页面内容转成清晰介绍", 64)},
            ],
            "micro_details": source_scene_keywords(str(item.get("intent", "")), scene_index, site_profile)[:4],
            "choreography": "标题先建立项目定位，随后展开能力与使用路径。" if document_source else "证据条先绘制，焦点区域随后收紧，字幕最后落位。",
            "transition": "velocity-matched editorial wipe",
        }
    scene_templates = [
        {
            "world": "高层战略开场",
            "mood": "电影片头、安静但有压迫感",
            "claim": f"{topic} 不是一个单点功能，而是一条从材料到判断的工作流。",
            "metric": {"label": "THESIS", "value": "01"},
            "proof_points": [
                {"label": "对象", "value": audience},
                {"label": "输入", "value": "多源材料、问题、上下文"},
                {"label": "输出", "value": "可执行、可复核的结论"},
            ],
            "micro_details": ["thesis line", "index ghost type", "fine grid", "slow lens drift"],
        },
        {
            "world": "问题张力剖面",
            "mood": "咨询报告与谍报墙之间",
            "claim": "真正的成本不是生成慢，而是信息分散、口径反复和结论无法沉淀。",
            "metric": {"label": "FRICTION", "value": "03"},
            "proof_points": [
                {"label": "材料", "value": "分散在文档、会议和搜索结果"},
                {"label": "沟通", "value": "团队反复确认同一个问题"},
                {"label": "风险", "value": "结论缺少来源与复核链路"},
            ],
            "micro_details": ["split ledger", "risk ticks", "thin rule", "negative space"],
        },
        {
            "world": "系统能力拆解",
            "mood": "精密仪表盘，不像 SaaS 首页",
            "claim": "它把理解、生成、引用和复核放到同一个节奏里，减少从想法到交付的断点。",
            "metric": {"label": "FLOW", "value": "04"},
            "proof_points": [
                {"label": "理解", "value": "先整理材料关系"},
                {"label": "生成", "value": "再形成面向任务的表达"},
                {"label": "复核", "value": "最后回到依据与风险"},
            ],
            "micro_details": ["pipeline nodes", "source bar", "review stamp", "handoff trace"],
        },
        {
            "world": "证据与可信度层",
            "mood": "投委会材料、审阅批注、低声量金色高亮",
            "claim": "好内容不只要漂亮，还要让团队知道依据来自哪里、判断如何形成。",
            "metric": {"label": "PROOF", "value": "↗"},
            "proof_points": [
                {"label": "引用", "value": "关键说法有来源线索"},
                {"label": "风险", "value": "不确定内容被显式标记"},
                {"label": "摘要", "value": "复杂材料收束成少量判断"},
            ],
            "micro_details": ["audit mark", "confidence ruler", "source chips", "quiet pulse"],
        },
        {
            "world": "真实任务落地",
            "mood": "成熟团队的工作台，不是模板展示",
            "claim": "场景价值来自连续使用：研究、汇报、客户沟通和运营复盘都能接上同一套方法。",
            "metric": {"label": "SCENARIOS", "value": "04"},
            "proof_points": [
                {"label": "研究", "value": "从材料中提炼问题"},
                {"label": "汇报", "value": "把结论压缩成决策页"},
                {"label": "交付", "value": "沉淀成可复用资产"},
            ],
            "micro_details": ["scenario rail", "handoff cards", "archive line", "team cursor"],
        },
        {
            "world": "结论收束",
            "mood": "品牌片结尾、低频、有确定性",
            "claim": "最终价值是让团队更快看清问题，更稳地完成表达，并保留可追溯的依据。",
            "metric": {"label": "OUTCOME", "value": "READY"},
            "proof_points": [
                {"label": "速度", "value": "减少从阅读到表达的空转"},
                {"label": "质量", "value": "保留上下文和判断链路"},
                {"label": "协作", "value": "让下一步行动更明确"},
            ],
            "micro_details": ["final lockup", "decision line", "soft flare", "closing rule"],
        },
    ]
    template = scene_templates[min(scene_index, len(scene_templates) - 1)]
    layout = executive_layout_for_scene(scene_index, str(template.get("world", "")), str(template.get("claim", "")))
    return {
        "scene_id": safe_scene_id(item.get("id"), scene_index),
        "layout": layout,
        "title": compact_label(scene_title, headline or topic, 34),
        "body": compact_label(scene_body, template["claim"], 88),
        "choreography": "主标题慢推入，证据账本分层绘制，微细节保持低频漂移。",
        "transition": "blur-through editorial cut",
        **template,
    }


def build_production_spec(
    brief: str,
    storyboard: list[dict[str, Any]],
    narration: str,
    headline: str,
    site_profile: dict[str, Any] | None = None,
) -> dict[str, Any]:
    rhythm = "drift-build-PEAK-drift-resolve" if is_longform_duration(max((float(item.get("end", 0)) for item in storyboard), default=0.0)) else "hook-PUNCH-breathe-CTA"
    scenes = [
        production_spec_for_scene(brief, storyboard, narration, headline, scene_index, site_profile)
        for scene_index in range(len(storyboard))
    ]
    return {
        "source": "compose",
        "format": "production-spec",
        "rhythm": rhythm,
        "content_brief": (site_profile or {}).get("content_brief", {}) if site_profile else {},
        "global_rules": [
            "每个镜头至少包含背景纹理、中景内容、前景细节。",
            "旁白负责推进判断，画面负责展示证据和结构。",
            "避免空泛大词，优先展示对象、输入、过程、输出和风险。",
        ],
        "scenes": scenes,
    }


def production_spec_by_scene(production_spec: dict[str, Any] | None) -> dict[str, dict[str, Any]]:
    if not production_spec:
        return {}
    scenes = production_spec.get("scenes", [])
    if not isinstance(scenes, list):
        return {}
    return {
        str(item.get("scene_id", "")): item
        for item in scenes
        if isinstance(item, dict) and str(item.get("scene_id", "")).strip()
    }


def site_mode_for_project(style_preset_name: str, site_profile: dict[str, Any]) -> str:
    if not site_profile.get("screenshots"):
        return "standard"
    if style_preset_name == "editorial-pro":
        return "editorial-pro"
    return "evidence-clean"


def build_evidence_note_html(
    site_profile: dict[str, Any],
    scene_index: int,
    label: str,
    text: str,
    fallback: str,
) -> str:
    document_source = is_document_source(site_profile)
    material_label = source_material_label(site_profile)
    ctas = [str(item) for item in site_profile.get("ctas", []) if str(item).strip()]
    action = ctas[scene_index % len(ctas)] if ctas else ("资料原文" if document_source else "官网原文")
    clean_label = (label or fallback or ("资料重点" if document_source else "网页重点")).strip()[:34]
    clean_text = (text or fallback or ("来自原始资料提取。" if document_source else "来自真实网页截图与 DOM 提取。")).strip()[:104]
    if mostly_latin_text(clean_text):
        fallback_text = (fallback or "").strip()
        if fallback_text and not mostly_latin_text(fallback_text):
            clean_text = fallback_text[:104]
        elif document_source:
            clean_text = f"{material_label} 的当前段落，承接本镜头对项目定位与能力结构的介绍。"
        else:
            clean_text = "官网当前区域，承接本镜头对页面结构与用户路径的解读。"
    return (
        '<aside class="evidence-note">'
        f"<small>{'项目资料' if document_source else '页面重点'}</small>"
        f"<b>{html_lib.escape(clean_label)}</b>"
        f"<span>{html_lib.escape(clean_text)}</span>"
        f"<em>{html_lib.escape(action[:24])}</em>"
        "</aside>"
    )


def build_executive_layout_content(
    layout: str,
    scene_title: str,
    scene_body: str,
    claim: str,
    world: str,
    metric_label: str,
    metric_value: str,
    ledger: str,
    micro: str,
    tags: str,
    bars_html: str,
    nodes_html: str,
    scene_index: int,
) -> str:
    title = html_lib.escape(scene_title)
    body = html_lib.escape(scene_body)
    claim_html = html_lib.escape(claim)
    world_html = html_lib.escape(world[:42])
    metric_label_html = html_lib.escape(metric_label)
    metric_value_html = html_lib.escape(metric_value)
    if layout == "title-slate":
        return f'''
                    <div class="plate-index">{metric_value_html}</div>
                    <div class="plate-kicker">{world_html}</div>
                    <div class="layout-title-slate">
                      <small>{metric_label_html}</small>
                      <h3>{title}</h3>
                      <p>{claim_html}</p>
                    </div>
                    <div class="executive-tags">{tags}</div>
                    <div class="production-micro">{micro}</div>'''
    if layout == "tension-matrix":
        return f'''
                    <div class="plate-kicker">{world_html}</div>
                    <div class="plate-index">{metric_value_html}</div>
                    <div class="layout-tension">
                      <div class="tension-claim"><small>{metric_label_html}</small><b>{title}</b><span>{claim_html}</span></div>
                      <div class="tension-grid"><ul>{ledger}</ul></div>
                    </div>
                    <div class="production-micro">{micro}</div>'''
    if layout == "process-pipeline":
        steps = "".join(
            f'<span style="--i:{index}"><b>{label}</b><i></i></span>'
            for index, label in enumerate(["理解", "生成", "复核", "交付"], start=1)
        )
        return f'''
                    <div class="plate-kicker">{world_html}</div>
                    <div class="metric-stamp"><small>{metric_label_html}</small><b>{metric_value_html}</b></div>
                    <div class="layout-pipeline">
                      <h3>{title}</h3>
                      <p>{claim_html}</p>
                      <div class="pipeline-track">{steps}</div>
                      <div class="content-ledger"><ul>{ledger}</ul></div>
                    </div>
                    <div class="production-micro">{micro}</div>'''
    if layout == "scenario-desk":
        return f'''
                    <div class="plate-kicker">{world_html}</div>
                    <div class="layout-desk">
                      <div class="desk-header"><small>{metric_label_html}</small><b>{title}</b><span>{claim_html}</span></div>
                      <div class="desk-cards"><ul>{ledger}</ul></div>
                      <div class="desk-footer">{micro}</div>
                    </div>
                    <div class="signal-field">{bars_html}{nodes_html}</div>'''
    if layout == "final-lockup":
        return f'''
                    <div class="layout-final">
                      <small>{world_html}</small>
                      <h3>{title}</h3>
                      <p>{claim_html}</p>
                      <div class="metric-stamp"><small>{metric_label_html}</small><b>{metric_value_html}</b></div>
                      <div class="executive-tags">{tags}</div>
                    </div>
                    <div class="production-micro">{micro}</div>'''
    return f'''
                    <div class="plate-kicker">{world_html}</div>
                    <div class="plate-index">{metric_value_html}</div>
                    <div class="executive-tags">{tags}</div>
                    <div class="content-ledger"><ul>{ledger}</ul></div>
                    <div class="metric-stamp"><small>{metric_label_html}</small><b>{metric_value_html}</b></div>
                    <div class="production-micro">{micro}</div>
                    <div class="signal-field">{bars_html}{nodes_html}</div>
                    <div class="plate-title">{title}</div>
                    <div class="plate-copy">{claim_html}</div>'''


def build_executive_abstract_visual(scene_title: str, scene_body: str, keywords: list[str], scene_index: int, scene_spec: dict[str, Any] | None = None) -> str:
    scene_spec = scene_spec or {}
    claim = str(scene_spec.get("claim") or scene_body)
    world = str(scene_spec.get("world") or "Strategic Signal")
    mood = str(scene_spec.get("mood") or "restrained executive film")
    layout = str(scene_spec.get("layout") or executive_layout_for_scene(scene_index, world, claim))
    metric = scene_spec.get("metric") if isinstance(scene_spec.get("metric"), dict) else {}
    metric_label = str(metric.get("label") or "SIGNAL")[:18]
    metric_value = str(metric.get("value") or f"{scene_index + 1:02d}")[:10]
    proof_points = [item for item in scene_spec.get("proof_points", []) if isinstance(item, dict)][:3]
    if not proof_points:
        proof_points = [
            {"label": "判断", "value": scene_title},
            {"label": "依据", "value": scene_body},
            {"label": "行动", "value": keywords[0] if keywords else "下一步"},
        ]
    ledger = "".join(
        f'<li><b>{html_lib.escape(str(item.get("label", "证据"))[:18])}</b><span>{html_lib.escape(str(item.get("value", ""))[:42])}</span></li>'
        for item in proof_points
    )
    micro_details = [str(item) for item in scene_spec.get("micro_details", []) if str(item).strip()][:4]
    if not micro_details:
        micro_details = keywords[:4] or ["source", "signal", "motion", "caption"]
    micro = "".join(f"<span>{html_lib.escape(item[:18])}</span>" for item in micro_details)
    strips = "".join("<span></span>" for _ in range(3))
    tags = "".join(f"<span>{html_lib.escape(keyword)}</span>" for keyword in ([world, mood] + keywords)[:3])
    bars = []
    nodes = []
    for index in range(9):
        height = 34 + ((index * 31 + scene_index * 19) % 128)
        left = 18 + index * 24
        bars.append(f'<i style="left:{left}px;height:{height}px;opacity:{0.28 + (index % 3) * 0.18:.2f}"></i>')
    for index in range(5):
        left = 32 + ((index * 43 + scene_index * 27) % 170)
        top = 22 + ((index * 37 + scene_index * 21) % 122)
        nodes.append(f'<b style="left:{left}px;top:{top}px"></b>')
    content = build_executive_layout_content(layout, scene_title, scene_body, claim, world, metric_label, metric_value, ledger, micro, tags, "".join(bars), "".join(nodes), scene_index)
    return f'''
                <div class="shot-canvas abstract-shot executive-layout executive-layout-{html_lib.escape(layout)}">
                  <div class="executive-plate">
                    <div class="evidence-strips">{strips}</div>
                    {content}
                  </div>
                </div>'''


def build_shot_visual(
    shot_type: str,
    intent: str,
    headline: str,
    scene_index: int,
    waveform: str,
    brand: dict[str, Any] | None = None,
    site_profile: dict[str, Any] | None = None,
    scene_spec: dict[str, Any] | None = None,
) -> str:
    if site_profile:
        scene_title, scene_body = site_display_copy(site_profile, scene_index, intent, headline or f"Scene {scene_index + 1}")
    else:
        scene_title, scene_body = split_intent(intent, headline or f"Scene {scene_index + 1}")
        scene_title = display_safe_text(scene_title, headline or f"Scene {scene_index + 1}", 28)
        scene_body = display_safe_text(scene_body, headline or "来自项目简报。", 62)
    keywords = source_scene_keywords(intent, scene_index, site_profile)
    brand = brand or {}
    brand_name = str(brand.get("name", "") or "Website")
    brand_description = str(brand.get("description", "") or scene_body)
    brand_nav = [str(item) for item in brand.get("nav", []) if str(item).strip()]
    brand_keywords = [str(item) for item in brand.get("keywords", []) if str(item).strip()]
    brand_voice = brand.get("voice", {}) if isinstance(brand.get("voice"), dict) else {}
    voice_tone = str(brand_voice.get("tone", "") or "")
    site_profile = site_profile or {}
    site_evidence = site_evidence_for_scene(site_profile, scene_index)
    site_screenshot = build_site_screenshot_html(site_profile, scene_index)
    evidence_label = str(site_evidence.get("label", "") or "")
    evidence_text = str(site_evidence.get("text", "") or "")
    if site_screenshot and site_profile.get("screenshots"):
        note = build_evidence_note_html(site_profile, scene_index, evidence_label, evidence_text, scene_body)
        return f'''
                <div class="shot-canvas clean-shot clean-{html_lib.escape(shot_type)}">
                  {site_screenshot}
                  {note}
                </div>'''
    if not site_profile:
        return build_executive_abstract_visual(scene_title, scene_body, keywords, scene_index, scene_spec)
    rows = visual_card_items(intent, headline, scene_index, brand, site_profile)
    info_cards = "".join(
        f'<article class="info-card"><b>{html_lib.escape(name)}</b><span>{html_lib.escape(desc)}</span></article>'
        for name, desc in rows
    )
    site_headings = [str(item) for item in site_profile.get("headings", []) if str(item).strip()]
    nav_source = (brand_nav + site_headings + brand_keywords + keywords + ["入口", "说明"])[:5]
    nav_items = "".join(f"<span>{html_lib.escape(item)}</span>" for item in nav_source)
    mark_source = ([voice_tone] if voice_tone else []) + brand_keywords[:2] + keywords
    keyword_marks = "".join(f"<i>{html_lib.escape(item)}</i>" for item in mark_source[:3])
    if shot_type == "hero-overview":
        body = f'''
                <div class="shot-canvas shot-hero">
                  <div class="site-window">
                    <div class="site-nav">{nav_items}</div>
                    <h3>{html_lib.escape(evidence_label or brand_name)}</h3>
                    <p>{html_lib.escape((evidence_text or brand_description)[:112] or scene_body)}</p>
                    <div class="hero-marks">{keyword_marks}</div>
                  </div>
                  {site_screenshot}
                  <div class="waveform">{waveform}</div>
                </div>'''
    elif shot_type == "nav-scan":
        body = f'''
                <div class="shot-canvas shot-nav">
                  <div class="scan-line"></div>
                  <div class="site-nav large">{nav_items}</div>
                  <div class="route-map">
                    <span>首页</span><b></b><span>产品</span><b></b><span>研究</span><b></b><span>行动</span>
                  </div>
                  <div class="info-grid">{info_cards}</div>
                  {site_screenshot}
                  <div class="waveform">{waveform}</div>
                </div>'''
    elif shot_type == "feature-zoom":
        body = f'''
                <div class="shot-canvas shot-feature">
                  <div class="zoom-lens"><strong>{html_lib.escape((evidence_label or keywords[0])[:18])}</strong><span>{html_lib.escape((evidence_text or scene_title)[:72])}</span></div>
                  <div class="feature-stack">{info_cards}</div>
                  {site_screenshot}
                  <div class="waveform">{waveform}</div>
                </div>'''
    elif shot_type == "trust-message":
        body = f'''
                <div class="shot-canvas shot-trust">
                  <blockquote>“{html_lib.escape(evidence_label or scene_title)}”</blockquote>
                  <p>{html_lib.escape((evidence_text or scene_body)[:140])}</p>
                  {site_screenshot}
                  <div class="evidence-row">{info_cards}</div>
                  <div class="waveform">{waveform}</div>
                </div>'''
    else:
        body = f'''
                <div class="shot-canvas shot-cta">
                  <div class="summary-orb">{html_lib.escape(keywords[0][:2])}</div>
                  <h3>{html_lib.escape(scene_title)}</h3>
                  <p>{html_lib.escape(scene_body)}</p>
                  {site_screenshot}
                  <div class="cta-row"><span>{html_lib.escape(keywords[0])}</span><span>{html_lib.escape(keywords[1])}</span><span>{html_lib.escape(keywords[2])}</span></div>
                  <div class="waveform">{waveform}</div>
                </div>'''
    return body


def beat_role_text(role: str, intent: str, headline: str, scene_index: int, beat_index: int) -> str:
    scene_title, scene_body = split_intent(intent, headline or f"Scene {scene_index + 1}")
    story_title, story_body = storyboard_insight_copy(intent, scene_title, scene_body)
    scene_title = story_title or scene_title
    scene_body = story_body or scene_body
    if is_director_note(scene_title):
        scene_title = headline or f"网页重点 {scene_index + 1}"
    if is_director_note(scene_body):
        scene_body = "来自真实网页内容。"
    variants = {
        "hook": scene_title,
        "proof": scene_body[:44] or scene_title,
        "detail": f"{', '.join(storyboard_keywords(intent, scene_index)[:2])}",
        "cta": scene_body[:54] or "收束成清晰的下一步行动。",
    }
    return variants.get(role, f"{scene_title} · step {beat_index + 1}")


def build_beats(
    storyboard: list[dict[str, Any]],
    narration: str,
    headline: str,
    beats_per_scene: int = DEFAULT_BEATS_PER_SCENE,
) -> list[dict[str, Any]]:
    beats: list[dict[str, Any]] = []
    sentence_parts = [part.strip() for part in re.split(r"[。.!?！？；;]\s*", narration or "") if part.strip()]
    sentence_index = 0
    requested_count = max(1, min(6, int(beats_per_scene)))
    for scene_index, item in enumerate(storyboard):
        scene_id = safe_scene_id(item.get("id"), scene_index)
        start = float(item.get("start", 0))
        end = float(item.get("end", start + 1))
        scene_duration = max(0.1, end - start)
        readable_count = max(1, int(scene_duration / MIN_READABLE_BEAT_DURATION))
        count = max(1, min(requested_count, readable_count))
        intent = str(item.get("intent", headline))
        for beat_index in range(count):
            role = BEAT_ROLES[min(beat_index, len(BEAT_ROLES) - 1)] if beat_index < len(BEAT_ROLES) else f"step-{beat_index + 1}"
            beat_start = start + scene_duration * beat_index / count
            beat_end = start + scene_duration * (beat_index + 1) / count
            text = sentence_parts[sentence_index % len(sentence_parts)] if sentence_parts and beat_index == 0 else beat_role_text(role, intent, headline, scene_index, beat_index)
            sentence_index += 1
            text = display_safe_text(text, beat_role_text(role, intent, headline, scene_index, beat_index), 80)
            beats.append(
                {
                    "id": f"{scene_id}-{role}-{beat_index + 1}",
                    "scene_id": scene_id,
                    "role": role,
                    "start": round(beat_start, 3),
                    "end": round(beat_end, 3),
                    "duration": round(max(0.1, beat_end - beat_start), 3),
                    "text": text[:80],
                    "emphasis": scene_keywords(intent, scene_index)[beat_index % len(scene_keywords(intent, scene_index))],
                }
            )
    return beats


def beats_by_scene(beats: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for beat in beats:
        grouped.setdefault(str(beat.get("scene_id", "")), []).append(beat)
    for scene_beats in grouped.values():
        scene_beats.sort(key=lambda item: float(item.get("start", 0)))
    return grouped


def build_beat_layers(scene_id: str, beats: list[dict[str, Any]]) -> str:
    if not beats:
        return ""
    role_labels = {
        "hook": "重点",
        "proof": "依据",
        "detail": "细节",
        "cta": "下一步",
    }
    layers = []
    for beat in beats:
        beat_id = html_lib.escape(str(beat.get("id", "")))
        raw_role = str(beat.get("role", "beat"))
        role = html_lib.escape(role_labels.get(raw_role, "片段"))
        text = html_lib.escape(str(beat.get("text", "")))
        start = float(beat.get("start", 0))
        duration = max(0.1, float(beat.get("duration", 0.5)))
        layers.append(
            f'<div class="beat-layer" data-beat="{beat_id}" data-parent-scene="{html_lib.escape(scene_id)}" data-start="{start:.3f}" data-duration="{duration:.3f}"><strong>{role}</strong><span>{text}</span></div>'
        )
    return '<div class="beat-stack">' + "".join(layers) + "</div>"


def build_media_prop(enable_image: bool, enable_video: bool, index: int, scene_count: int) -> str:
    if enable_video and index >= max(1, scene_count - 2):
        return '<div class="media-prop"><video data-asset="broll-video" src="" muted playsinline></video></div>'
    if enable_image and index <= 1:
        return '<div class="media-prop"><img data-asset="hero-image" src="" alt="Website visual reference" /></div>'
    return ""


def build_scene_layers(
    storyboard: list[dict[str, Any]],
    headline: str,
    enable_image: bool,
    enable_video: bool,
    beats: list[dict[str, Any]] | None = None,
    brand: dict[str, Any] | None = None,
    site_profile: dict[str, Any] | None = None,
    production_spec: dict[str, Any] | None = None,
) -> str:
    if not storyboard:
        storyboard = storyboard_from_brief(headline, DEFAULT_RENDER_DURATION)
    scene_count = len(storyboard)
    grouped_beats = beats_by_scene(beats or [])
    scene_specs = production_spec_by_scene(production_spec)
    layers: list[str] = []
    for scene_index, item in enumerate(storyboard):
        scene_id = safe_scene_id(item.get("id"), scene_index)
        start = float(item.get("start", 0))
        end = float(item.get("end", start + 1))
        duration = max(0.1, end - start)
        intent = str(item.get("intent", headline))
        material_evidence = site_evidence_for_scene(site_profile, scene_index)
        if site_profile:
            scene_title, scene_body = site_display_copy(site_profile, scene_index, intent, headline or f"Beat {scene_index + 1}")
        else:
            scene_title, scene_body = split_intent(intent, headline or f"Beat {scene_index + 1}")
            scene_title = display_safe_text(scene_title, headline or f"Beat {scene_index + 1}", 28)
            scene_body = display_safe_text(scene_body, headline or "来自项目简报。", 62)
        shot_type = select_website_shot_for_scene(intent, scene_index, scene_count, material_evidence)
        composition_mode = select_composition_mode(shot_type, scene_index, scene_count, site_profile, material_evidence)
        camera_path = camera_path_for_scene(composition_mode, material_evidence)
        material_role = str(material_evidence.get("role", "") or "general")
        evidence_label = str(material_evidence.get("label", scene_title))
        keywords = source_scene_keywords(intent, scene_index, site_profile)
        scene_spec = scene_specs.get(scene_id, {})
        chips = "".join(f'<span class="kinetic-chip">{html_lib.escape(keyword)}</span>' for keyword in keywords)
        beat_layers = build_beat_layers(scene_id, grouped_beats.get(scene_id, []))
        waveform = "".join(f"<i style=\"height:{24 + ((bar_index * 17 + scene_index * 11) % 54)}px\"></i>" for bar_index in range(18))
        shot_visual = build_shot_visual(shot_type, intent, headline, scene_index, waveform, brand, site_profile, scene_spec)
        media_prop = build_media_prop(enable_image, enable_video, scene_index, scene_count)
        if site_profile and is_document_source(site_profile):
            eyebrow_context = "Project Brief"
        elif site_profile:
            eyebrow_context = "Site Overview"
        else:
            eyebrow_context = "Executive Film"
        layers.append(
            f'''<section class="story-scene scene-{scene_index % 4} shot-{shot_type} composition-{composition_mode}" data-shot="{shot_type}" data-material-role="{html_lib.escape(material_role)}" data-composition-mode="{composition_mode}" data-camera-path="{camera_path}" data-scene="{scene_id}" data-timeline-id="{scene_id}" data-start="{start:.3f}" data-duration="{duration:.3f}">
        <div class="orb one"></div><div class="orb two"></div>
        {composition_badge_html(composition_mode, scene_index, evidence_label, site_profile)}
        <div class="scene-grid">
          <div class="scene-copy">
            <div class="eyebrow">Scene {scene_index + 1:02d} / {eyebrow_context}</div>
            <h2>{html_lib.escape(scene_title)}</h2>
            <p>{html_lib.escape(scene_body)}</p>
            <div class="kinetic-row">{chips}</div>
            {beat_layers}
          </div>
          <div class="scene-visual">
            <div class="visual-card">
              <div class="browser-top"><div class="dots"><i></i><i></i><i></i></div><span>{html_lib.escape(headline or "Creative Voice OS")}</span></div>
              {shot_visual}
            </div>
            {media_prop}
          </div>
        </div>
      </section>'''
        )
    return "\n      ".join(layers)


def build_scene_nav(storyboard: list[dict[str, Any]]) -> str:
    nav_items: list[str] = []
    for scene_index, item in enumerate(storyboard):
        scene_id = safe_scene_id(item.get("id"), scene_index)
        nav_items.append(f'<span data-nav-scene="{scene_id}">Beat {scene_index + 1:02d}</span>')
    return "".join(nav_items)


def transition_kinds(preset: str) -> list[str]:
    if preset == "none":
        return []
    if preset == "glass":
        return ["glass-flash", "prism-slide", "luma-sweep"]
    if preset == "ribbon":
        return ["ribbon-wipe", "soft-bloom", "prism-slide"]
    if preset == "iris":
        return ["iris-focus", "glass-flash", "luma-sweep"]
    if preset == "luma":
        return ["luma-sweep", "ribbon-wipe", "soft-bloom"]
    return ["ribbon-wipe", "glass-flash", "iris-focus", "luma-sweep"]


def build_transitions(storyboard: list[dict[str, Any]], preset: str) -> list[dict[str, Any]]:
    kinds = transition_kinds(preset)
    if not kinds or len(storyboard) < 2:
        return []
    duration_by_preset = {
        "editorial": 0.86,
        "glass": 0.92,
        "ribbon": 0.78,
        "iris": 0.9,
        "luma": 0.88,
    }
    intensity_by_preset = {
        "editorial": 0.56,
        "glass": 0.5,
        "ribbon": 0.58,
        "iris": 0.48,
        "luma": 0.44,
    }
    transitions: list[dict[str, Any]] = []
    for index, item in enumerate(storyboard[:-1]):
        next_item = storyboard[index + 1]
        start = float(item.get("start", 0))
        at = float(item.get("end", start + 1))
        transitions.append(
            {
                "id": f"tr-{index + 1}",
                "from": safe_scene_id(item.get("id"), index),
                "to": safe_scene_id(next_item.get("id"), index + 1),
                "at": at,
                "duration": duration_by_preset.get(preset, 0.86),
                "kind": kinds[index % len(kinds)],
                "easing": "expo-out",
                "intensity": round(intensity_by_preset.get(preset, 0.54) + (index % 2) * 0.04, 2),
            }
        )
    return transitions


GSAP_COMPAT_JS = r'''
      function createGsapCompatTimeline(spec) {
        var labels = {};
        var tracks = [];
        function number(value, fallback) {
          var parsed = Number(value);
          return Number.isFinite(parsed) ? parsed : fallback;
        }
        function easeNamed(name, value) {
          value = clamp(value, 0, 1);
          if (name === "expo-out") return value >= 1 ? 1 : 1 - Math.pow(2, -10 * value);
          if (name === "power2-in") return value * value;
          if (name === "power2-out") return 1 - Math.pow(1 - value, 2);
          if (name === "sine-in-out") return .5 - Math.cos(value * Math.PI) / 2;
          return easeOut(value);
        }
        function resolveAt(at) {
          if (typeof at === "string" && labels[at] != null) return labels[at];
          return number(at, 0);
        }
        function mix(fromValue, toValue, progress) {
          if (typeof fromValue === "number" && typeof toValue === "number") return fromValue + (toValue - fromValue) * progress;
          return progress < 1 ? fromValue : toValue;
        }
        function mixedProps(fromProps, toProps, progress) {
          var props = {};
          var keys = {};
          Object.keys(fromProps || {}).forEach(function (key) { keys[key] = true; });
          Object.keys(toProps || {}).forEach(function (key) { keys[key] = true; });
          Object.keys(keys).forEach(function (key) { props[key] = mix((fromProps || {})[key], (toProps || {})[key], progress); });
          return props;
        }
        function applyProps(element, props) {
          if (!element || !props) return;
          var transform = [];
          if (props.x != null || props.y != null || props.z != null) transform.push("translate3d(" + number(props.x, 0).toFixed(2) + "px," + number(props.y, 0).toFixed(2) + "px," + number(props.z, 0).toFixed(2) + "px)");
          if (props.rotateX != null) transform.push("rotateX(" + number(props.rotateX, 0).toFixed(2) + "deg)");
          if (props.rotateY != null) transform.push("rotateY(" + number(props.rotateY, 0).toFixed(2) + "deg)");
          if (props.rotate != null) transform.push("rotate(" + number(props.rotate, 0).toFixed(2) + "deg)");
          if (props.scale != null) transform.push("scale(" + number(props.scale, 1).toFixed(4) + ")");
          if (transform.length) element.style.transform = transform.join(" ");
          if (props.opacity != null) element.style.opacity = String(number(props.opacity, 1));
          if (props.visibility != null) element.style.visibility = String(props.visibility);
          if (props.filter != null) element.style.filter = String(props.filter);
          if (props.background != null) element.style.background = String(props.background);
          if (props.mixBlendMode != null) element.style.mixBlendMode = String(props.mixBlendMode);
        }
        function addTrack(track) {
          tracks.push(Object.assign({ method: "to", start: 0, duration: 0, from: {}, to: {}, ease: "expo-out" }, track || {}));
          return api;
        }
        var api = {
          addLabel: function (name, at) { labels[name] = resolveAt(at); return api; },
          set: function (selector, props, at) { return addTrack({ method: "set", selector: selector, start: resolveAt(at), to: props || {}, duration: 0 }); },
          to: function (selector, props, at, duration, opts) { return addTrack(Object.assign({ method: "to", selector: selector, start: resolveAt(at), to: props || {}, duration: number(duration, .4) }, opts || {})); },
          fromTo: function (selector, fromProps, toProps, at, duration, opts) { return addTrack(Object.assign({ method: "fromTo", selector: selector, start: resolveAt(at), from: fromProps || {}, to: toProps || {}, duration: number(duration, .4) }, opts || {})); },
          seek: function (time) {
            tracks.forEach(function (track) {
              var start = resolveAt(track.start);
              var duration = Math.max(0.001, number(track.duration, 0));
              var raw = track.method === "set" ? (time >= start ? 1 : -1) : (time - start) / duration;
              if (raw < 0 || (raw > 1 && track.persist === false)) return;
              var progress = track.method === "set" ? 1 : easeNamed(track.ease, clamp(raw, 0, 1));
              var props = track.method === "fromTo" ? mixedProps(track.from, track.to, progress) : track.to;
              document.querySelectorAll(track.selector || "").forEach(function (element) { applyProps(element, props); });
            });
            return api;
          },
          tracks: function () { return tracks.slice(); },
          labels: function () { return Object.assign({}, labels); }
        };
        Object.keys(spec.labels || {}).forEach(function (name) { api.addLabel(name, spec.labels[name]); });
        (spec.tracks || []).forEach(addTrack);
        return api;
      }
'''


def build_gsap_compat_plan(
    storyboard: list[dict[str, Any]],
    effects: list[str] | None = None,
    beats: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    labels: dict[str, float] = {}
    tracks: list[dict[str, Any]] = []
    effects = effects or timeline_effects("cinematic")
    for scene_index, item in enumerate(storyboard):
        scene_id = safe_scene_id(item.get("id"), scene_index)
        start = float(item.get("start", 0))
        end = float(item.get("end", start + 1))
        scene_duration = max(0.2, end - start)
        enter_duration = min(0.72, scene_duration * 0.32)
        exit_duration = min(0.52, scene_duration * 0.22)
        exit_start = max(start + enter_duration, end - exit_duration)
        effect = effects[scene_index % len(effects)]
        labels[scene_id] = round(start, 3)
        labels[f"{scene_id}:enter"] = round(start, 3)
        labels[f"{scene_id}:exit"] = round(exit_start, 3)
        enter_x = 72 if effect == "slide-left" else 0
        enter_scale = 0.92 if effect == "zoom-in" else 0.965
        scene_selector = f'[data-scene="{scene_id}"]'
        tracks.extend(
            [
                {
                    "method": "set",
                    "selector": scene_selector,
                    "start": round(start, 3),
                    "to": {"visibility": "visible"},
                    "persist": True,
                },
                {
                    "method": "fromTo",
                    "selector": scene_selector,
                    "start": round(start, 3),
                    "duration": round(enter_duration, 3),
                    "from": {"opacity": 0, "x": enter_x, "y": 48, "scale": enter_scale},
                    "to": {"opacity": 1, "x": 0, "y": 0, "scale": 1},
                    "ease": "expo-out",
                    "persist": True,
                },
                {
                    "method": "to",
                    "selector": scene_selector,
                    "start": round(exit_start, 3),
                    "duration": round(exit_duration, 3),
                    "to": {"opacity": 0, "y": -34, "scale": 1.018},
                    "ease": "power2-in",
                    "persist": True,
                },
                {
                    "method": "fromTo",
                    "selector": f'{scene_selector} .scene-copy',
                    "start": round(start + 0.06, 3),
                    "duration": round(min(0.58, scene_duration * 0.25), 3),
                    "from": {"opacity": 0, "x": -34, "y": 20},
                    "to": {"opacity": 1, "x": 0, "y": 0},
                    "ease": "expo-out",
                    "persist": True,
                },
                {
                    "method": "fromTo",
                    "selector": f'{scene_selector} .visual-card',
                    "start": round(start + 0.14, 3),
                    "duration": round(min(0.78, scene_duration * 0.34), 3),
                    "from": {"opacity": 0, "y": 36, "scale": 0.94, "rotateY": -8},
                    "to": {"opacity": 1, "y": 0, "scale": 1, "rotateY": -2},
                    "ease": "sine-in-out",
                    "persist": True,
                },
            ]
        )
    for beat in beats or []:
        beat_id = str(beat.get("id", ""))
        if not beat_id:
            continue
        start = float(beat.get("start", 0))
        duration = max(0.1, float(beat.get("duration", 0.5)))
        labels[beat_id] = round(start, 3)
        tracks.append(
            {
                "method": "fromTo",
                "selector": f'[data-beat="{beat_id}"]',
                "start": round(start, 3),
                "duration": round(min(0.62, duration * 0.48), 3),
                "from": {"opacity": 0, "y": 12, "scale": 0.992},
                "to": {"opacity": 1, "y": 0, "scale": 1},
                "ease": "sine-in-out",
                "persist": False,
            }
        )
    return {"labels": labels, "tracks": tracks}


def build_timeline_script(
    storyboard: list[dict[str, Any]],
    duration: float,
    transition_preset: str = "editorial",
    timeline_engine: str = "native",
    beats: list[dict[str, Any]] | None = None,
    production_spec: dict[str, Any] | None = None,
) -> str:
    layout_map = production_spec_by_scene(production_spec)
    scenes = []
    for scene_index, item in enumerate(storyboard):
        scene_id = safe_scene_id(item.get("id"), scene_index)
        start = float(item.get("start", 0))
        end = float(item.get("end", start + 1))
        scenes.append(
            {
                "id": scene_id,
                "start": start,
                "end": end,
                "index": scene_index,
                "layout": str((layout_map.get(scene_id) or {}).get("layout") or "evidence-wall"),
            }
        )
    scene_json = json.dumps(scenes, ensure_ascii=False)
    transitions = build_transitions(storyboard, transition_preset)
    for transition in transitions:
        from_scene = next((scene for scene in scenes if scene["id"] == transition.get("from")), None)
        to_scene = next((scene for scene in scenes if scene["id"] == transition.get("to")), None)
        transition["from_layout"] = (from_scene or {}).get("layout", "evidence-wall")
        transition["to_layout"] = (to_scene or {}).get("layout", "evidence-wall")
    transition_json = json.dumps(transitions, ensure_ascii=False)
    gsap_spec_json = "null"
    if timeline_engine == "gsap-compat":
        gsap_spec_json = json.dumps(build_gsap_compat_plan(storyboard, beats=beats), ensure_ascii=False)
    return f'''
    window.__timelines = window.__timelines || {{}};
    (function () {{
      var scenes = {scene_json};
      var transitionPlan = {transition_json};
      var duration = {float(duration):.3f};
      function clamp(value, min, max) {{ return Math.min(max, Math.max(min, value)); }}
      function easeOut(value) {{ value = clamp(value, 0, 1); return 1 - Math.pow(1 - value, 3); }}
      function easeIn(value) {{ value = clamp(value, 0, 1); return value * value * value; }}
      function setStyle(element, styles) {{
        if (!element) return;
        Object.keys(styles).forEach(function (key) {{ element.style[key] = styles[key]; }});
      }}
{GSAP_COMPAT_JS}
      var gsapSpec = {gsap_spec_json};
      var gsapCompat = gsapSpec ? createGsapCompatTimeline(gsapSpec) : null;
      window.__senseframes = window.__senseframes || {{}};
      window.__senseframes.gsapCompat = gsapCompat;
      function sceneProgress(scene, time) {{
        return clamp((time - scene.start) / Math.max(0.001, scene.end - scene.start), 0, 1);
      }}
      function audioReactive(time) {{
        var data = window.__senseframes && window.__senseframes.audioData;
        if (!data || !data.frames || !data.frames.length) return {{ bass: 0, mid: 0, treble: 0, rms: 0 }};
        var frame = data.frames[Math.min(data.frames.length - 1, Math.max(0, Math.floor(time * (data.fps || 24))))] || {{}};
        var bands = frame.bands || [];
        var bass = bands[0] || frame.rms || 0;
        var mid = bands[Math.min(3, bands.length - 1)] || frame.rms || 0;
        var treble = bands[Math.max(0, bands.length - 1)] || frame.rms || 0;
        return {{ bass: bass, mid: mid, treble: treble, rms: frame.rms || bass }};
      }}
      function transitionAmount(scene, time) {{
        var amount = 0;
        if (scene.index > 0) amount = Math.max(amount, 1 - Math.abs(time - scene.start) / 0.42);
        if (scene.index < scenes.length - 1) amount = Math.max(amount, 1 - Math.abs(time - scene.end) / 0.36);
        return clamp(amount, 0, 1);
      }}
      function transitionState(time) {{
        var best = {{ amount: 0, kind: "ribbon-wipe", intensity: 0.52 }};
        transitionPlan.forEach(function (item) {{
          var span = Math.max(0.12, Number(item.duration || 0.64));
          var amount = clamp(1 - Math.abs(time - Number(item.at || 0)) / span, 0, 1);
          amount = easeOut(amount);
          if (amount > best.amount) best = {{
            amount: amount,
            kind: item.kind || "ribbon-wipe",
            intensity: Number(item.intensity || 0.54),
            fromLayout: item.from_layout || "evidence-wall",
            toLayout: item.to_layout || "evidence-wall"
          }};
        }});
        return best;
      }}
      function stagger(progress, index, step, span) {{
        return easeOut((progress - index * step) / Math.max(0.001, span));
      }}
      function applyLayoutMotion(element, progress, active, audio) {{
        var layoutRoot = element.querySelector(".executive-layout");
        if (!layoutRoot) return;
        var build = easeOut(progress / 0.34);
        var reveal = easeOut((progress - 0.08) / 0.56);
        var settle = easeOut((progress - 0.55) / 0.34);
        var exit = easeIn((progress - 0.88) / 0.12);
        var drift = Math.sin(progress * Math.PI);
        layoutRoot.style.setProperty("--layout-build", build.toFixed(4));
        layoutRoot.style.setProperty("--layout-reveal", reveal.toFixed(4));
        layoutRoot.style.setProperty("--layout-drift", drift.toFixed(4));
        layoutRoot.style.setProperty("--layout-exit", exit.toFixed(4));
        layoutRoot.style.setProperty("--layout-audio", Number(audio.rms || 0).toFixed(4));
        layoutRoot.querySelectorAll(".evidence-strips span").forEach(function (line, index) {{
          var amount = stagger(progress, index, 0.055, 0.30);
          setStyle(line, {{
            transform: "scaleX(" + amount.toFixed(4) + ")",
            transformOrigin: "0 50%",
            opacity: String(active ? 0.18 + amount * 0.76 : 0)
          }});
        }});
        layoutRoot.querySelectorAll(".content-ledger li, .tension-grid li, .desk-cards li").forEach(function (row, index) {{
          var amount = stagger(progress - 0.10, index, 0.075, 0.34);
          setStyle(row, {{
            opacity: String(active ? Math.max(0, amount - exit * .7) : 0),
            transform: "translate3d(" + ((1 - amount) * 18).toFixed(2) + "px," + ((1 - amount) * 14 - exit * 12).toFixed(2) + "px,0)",
            filter: "blur(" + ((1 - amount) * 6).toFixed(2) + "px)"
          }});
        }});
        layoutRoot.querySelectorAll(".production-micro span, .executive-tags span, .desk-footer span").forEach(function (chip, index) {{
          var amount = stagger(progress - 0.20, index, 0.045, 0.24);
          setStyle(chip, {{
            opacity: String(active ? Math.max(0, amount - exit * .8) : 0),
            transform: "translateY(" + ((1 - amount) * 12 + Math.sin(progress * Math.PI * 2 + index) * 1.4).toFixed(2) + "px)"
          }});
        }});
        layoutRoot.querySelectorAll(".signal-field i").forEach(function (bar, index) {{
          var amount = stagger(progress - 0.16, index, 0.032, 0.30);
          var pulse = 1 + (audio.mid || 0) * .10 + Math.sin(progress * Math.PI * 2 + index * .6) * .035;
          setStyle(bar, {{
            opacity: String(active ? 0.16 + amount * .72 : 0),
            transform: "scaleY(" + Math.max(0, amount * pulse).toFixed(4) + ")"
          }});
        }});
        layoutRoot.querySelectorAll(".signal-field b").forEach(function (node, index) {{
          var amount = stagger(progress - 0.28, index, 0.055, 0.26);
          setStyle(node, {{
            opacity: String(active ? amount : 0),
            transform: "scale(" + (0.6 + amount * .48 + (audio.treble || 0) * .05).toFixed(4) + ")"
          }});
        }});
        layoutRoot.querySelectorAll(".plate-index").forEach(function (plateIndex) {{
          setStyle(plateIndex, {{
            opacity: String(active ? 0.06 + reveal * .09 : 0),
            transform: "translate3d(" + ((1 - reveal) * 28 + drift * 8).toFixed(2) + "px," + ((1 - build) * -10).toFixed(2) + "px,0) scale(" + (1.02 - reveal * .02).toFixed(4) + ")"
          }});
        }});
        layoutRoot.querySelectorAll(".plate-kicker, .layout-title-slate small, .layout-final small").forEach(function (kicker) {{
          var amount = easeOut((progress - 0.04) / 0.22);
          setStyle(kicker, {{
            opacity: String(active ? amount : 0),
            transform: "translateY(" + ((1 - amount) * 10).toFixed(2) + "px)"
          }});
        }});
        layoutRoot.querySelectorAll(".layout-title-slate h3, .layout-pipeline h3, .layout-final h3, .desk-header b, .tension-claim b, .plate-title").forEach(function (title, index) {{
          var amount = stagger(progress - 0.08, index, 0.035, 0.34);
          setStyle(title, {{
            opacity: String(active ? Math.max(0, amount - exit * .82) : 0),
            clipPath: "inset(0 " + ((1 - amount) * 100).toFixed(2) + "% 0 0)",
            transform: "translate3d(" + ((1 - amount) * -20).toFixed(2) + "px," + ((1 - amount) * 18 - exit * 12).toFixed(2) + "px,0)"
          }});
        }});
        layoutRoot.querySelectorAll(".layout-title-slate p, .layout-pipeline p, .layout-final p, .desk-header span, .tension-claim span, .plate-copy").forEach(function (copy, index) {{
          var amount = stagger(progress - 0.18, index, 0.04, 0.34);
          setStyle(copy, {{
            opacity: String(active ? Math.max(0, amount * .86 - exit * .6) : 0),
            transform: "translateY(" + ((1 - amount) * 12).toFixed(2) + "px)"
          }});
        }});
        layoutRoot.querySelectorAll(".pipeline-track span").forEach(function (step, index) {{
          var amount = stagger(progress - 0.18, index, 0.10, 0.34);
          setStyle(step, {{
            opacity: String(active ? amount : 0),
            transform: "translateY(" + ((1 - amount) * 18).toFixed(2) + "px)"
          }});
          var line = step.querySelector("i");
          setStyle(line, {{ transform: "scaleX(" + amount.toFixed(4) + ")", transformOrigin: "0 50%" }});
        }});
        layoutRoot.querySelectorAll(".metric-stamp").forEach(function (stamp) {{
          var amount = easeOut((progress - 0.30) / 0.34);
          setStyle(stamp, {{
            opacity: String(active ? Math.max(0, amount - exit * .75) : 0),
            transform: "translateY(" + ((1 - amount) * -12).toFixed(2) + "px) scale(" + (.94 + amount * .06 + (audio.bass || 0) * .012).toFixed(4) + ")"
          }});
        }});
        layoutRoot.querySelectorAll(".executive-plate").forEach(function (plate) {{
          setStyle(plate, {{
            filter: "contrast(" + (1.02 + settle * .04).toFixed(3) + ") brightness(" + (0.98 + build * .04 + (audio.rms || 0) * .015).toFixed(3) + ")",
          }});
        }});
      }}
      function morphPathForLayouts(fromLayout, toLayout, amount) {{
        var pair = String(fromLayout || "") + ">" + String(toLayout || "");
        if (pair.indexOf("tension-matrix>process-pipeline") >= 0) return "M150 160 L360 160 L360 306 L620 306 L620 452 L1120 452";
        if (pair.indexOf("process-pipeline>evidence-wall") >= 0) return "M120 220 C300 220,420 330,560 330 S820 210,1160 260";
        if (pair.indexOf("evidence-wall>scenario-desk") >= 0) return "M160 430 L360 330 L520 390 L720 250 L1010 330 L1160 250";
        if (pair.indexOf("scenario-desk>final-lockup") >= 0) return "M180 360 C420 250,760 250,1100 360";
        if (pair.indexOf("title-slate>tension-matrix") >= 0) return "M140 306 L420 306 L560 170 L780 442 L1140 306";
        return amount > .5 ? "M120 150 L1160 462" : "M84 352 C 320 258, 588 438, 1192 220";
      }}
      function applyMorphBridge(bridge, state, audio) {{
        if (!bridge) return;
        var amount = state.amount || 0;
        if (amount <= 0.015) {{
          setStyle(bridge, {{ opacity: "0", transform: "translate3d(0,0,0)", filter: "blur(0px)" }});
          return;
        }}
        var pulse = Math.sin(amount * Math.PI);
        var offset = (1 - pulse) * 640;
        bridge.dataset.fromLayout = state.fromLayout || "";
        bridge.dataset.toLayout = state.toLayout || "";
        setStyle(bridge, {{
          opacity: String(Math.min(.78, pulse * (.42 + (state.intensity || .52) * .42 + (audio.treble || 0) * .08))),
          transform: "translate3d(" + ((amount - .5) * 26).toFixed(2) + "px,0,0) scale(" + (1 + pulse * .012).toFixed(4) + ")",
          filter: "blur(" + ((1 - pulse) * 3.2).toFixed(2) + "px)"
        }});
        bridge.style.setProperty("--offset", offset.toFixed(2));
        bridge.style.setProperty("--dash", "640");
        var main = bridge.querySelector("[data-morph-main]");
        if (main) main.setAttribute("d", morphPathForLayouts(state.fromLayout, state.toLayout, amount));
        bridge.querySelectorAll("[data-morph-line]").forEach(function (line, index) {{
          var lineOffset = Math.max(0, offset + index * 62 - pulse * 80);
          line.style.strokeDashoffset = lineOffset.toFixed(2);
          line.style.opacity = String(.14 + pulse * (.34 + index * .09));
          line.setAttribute("y1", String(index === 0 ? 120 + pulse * 42 : 492 - pulse * 38));
          line.setAttribute("y2", String(index === 0 ? 120 + pulse * 42 : 492 - pulse * 38));
        }});
        bridge.querySelectorAll("[data-morph-panel]").forEach(function (panel) {{
          panel.style.strokeDashoffset = (offset * .7).toFixed(2);
          panel.style.opacity = String(.08 + pulse * .34);
          panel.setAttribute("x", String(520 + (state.toLayout === "final-lockup" ? 80 * pulse : -20 * pulse)));
          panel.setAttribute("width", String(560 - pulse * 90));
        }});
        bridge.querySelectorAll("[data-morph-node]").forEach(function (node, index) {{
          var nodeAmount = stagger(amount - 0.18, index, 0.08, 0.30);
          node.style.opacity = String(nodeAmount * pulse);
          node.style.transform = "scale(" + (.7 + nodeAmount * .7 + (audio.mid || 0) * .05).toFixed(3) + ")";
        }});
      }}
      function applyTransitionPreset(veil, state, audio) {{
        if (!veil) return;
        var amount = state.amount || 0;
        if (amount <= 0.001) {{
          setStyle(veil, {{ opacity: "0", transform: "translateX(-120%)", filter: "blur(12px)" }});
          return;
        }}
        var pulse = Math.sin(amount * Math.PI);
        var opacity = amount * (.18 + state.intensity * .22 + audio.treble * .08);
        var styles = {{ opacity: String(opacity), mixBlendMode: "screen" }};
        if (state.kind === "glass-flash") {{
          styles.background = "radial-gradient(circle at 50% 50%, rgba(255,255,255,.46), rgba(124,92,255,.18) 34%, rgba(255,255,255,0) 68%)";
          styles.transform = "scale(" + (0.86 + amount * .34).toFixed(4) + ")";
          styles.filter = "blur(" + (18 - pulse * 10).toFixed(2) + "px)";
        }} else if (state.kind === "iris-focus") {{
          styles.background = "radial-gradient(circle at 50% 48%, rgba(255,244,191,.42), rgba(124,92,255,.18) 28%, rgba(8,7,13,0) 58%)";
          styles.transform = "scale(" + (1.22 - amount * .26).toFixed(4) + ") rotate(" + (amount * 4).toFixed(2) + "deg)";
          styles.filter = "blur(" + (8 + (1 - pulse) * 10).toFixed(2) + "px)";
        }} else if (state.kind === "luma-sweep") {{
          styles.background = "linear-gradient(118deg, rgba(255,255,255,0), rgba(255,244,191,.36), rgba(76,223,204,.18), rgba(255,255,255,0))";
          styles.transform = "translateX(" + (-118 + amount * 236).toFixed(2) + "%) skewX(-8deg)";
          styles.filter = "blur(" + (6 + pulse * 8).toFixed(2) + "px) contrast(1.12)";
        }} else if (state.kind === "soft-bloom") {{
          styles.background = "radial-gradient(circle at 56% 46%, rgba(255,154,92,.30), rgba(124,92,255,.22) 42%, rgba(255,255,255,0) 74%)";
          styles.transform = "scale(" + (1 + pulse * .10).toFixed(4) + ")";
          styles.filter = "blur(" + (22 - pulse * 6).toFixed(2) + "px)";
        }} else {{
          styles.background = "linear-gradient(100deg, rgba(255,244,191,0), rgba(255,244,191,.30), rgba(124,92,255,.16), rgba(255,244,191,0))";
          styles.transform = "translateX(" + (-112 + amount * 224).toFixed(2) + "%) skewX(-12deg)";
          styles.filter = "blur(" + (12 - pulse * 4).toFixed(2) + "px)";
        }}
        setStyle(veil, styles);
      }}
      window.__timelines["main"] = {{
        duration: function () {{ return duration; }},
        seek: function (time) {{
          var globalProgress = clamp(time / Math.max(0.001, duration), 0, 1);
          var camera = document.querySelector(".camera-layer");
          var mesh = document.querySelector(".mesh");
          var focus = document.querySelector(".focus-ring");
          var veil = document.querySelector(".transition-veil");
          var morphBridge = document.querySelector("[data-morph-bridge]");
          var audio = audioReactive(time);
          var transitionPeak = 0;
          scenes.forEach(function (scene) {{ transitionPeak = Math.max(transitionPeak, transitionAmount(scene, time)); }});
          var authoredTransition = transitionState(time);
          if (authoredTransition.amount > transitionPeak) transitionPeak = authoredTransition.amount;
          setStyle(camera, {{ transform: "scale(" + (1.006 + globalProgress * 0.014).toFixed(4) + ") translate3d(" + (-8 * globalProgress).toFixed(2) + "px," + (-4 * globalProgress).toFixed(2) + "px,0)" }});
          setStyle(mesh, {{ opacity: String(.72 + audio.rms * .08), transform: "translate3d(" + (-18 * globalProgress).toFixed(2) + "px," + (8 * Math.sin(globalProgress * Math.PI)).toFixed(2) + "px,0) scale(" + (1 + globalProgress * .018 + audio.bass * .018).toFixed(4) + ")" }});
          applyTransitionPreset(veil, authoredTransition.amount > 0 ? authoredTransition : {{ amount: transitionPeak, kind: "ribbon-wipe", intensity: .52 }}, audio);
          applyMorphBridge(morphBridge, authoredTransition, audio);
          scenes.forEach(function (scene) {{
            var element = document.querySelector('[data-scene="' + scene.id + '"]');
            var nav = document.querySelector('[data-nav-scene="' + scene.id + '"]');
            if (!element) return;
            var active = time >= scene.start && time < scene.end;
            var progress = sceneProgress(scene, time);
            var build = easeOut(progress / 0.36);
            var resolve = easeIn((progress - 0.84) / 0.16);
            var breathe = Math.sin(progress * Math.PI);
            var compositionMode = element.dataset.compositionMode || "split-scan";
            var cameraPath = element.dataset.cameraPath || "hero-push";
            var effect = element.dataset.effect || ["spotlight", "fade-up", "slide-left", "zoom-in"][scene.index % 4];
            var x = 0;
            var y = (1 - build) * 22 - resolve * 14;
            var scale = .986 + build * .014 + breathe * .003 + audio.bass * .002;
            if (effect === "slide-left") x = (1 - build) * 30 - resolve * 24;
            if (effect === "zoom-in") scale = .974 + build * .030 + breathe * .004;
            if (effect === "parallax") x = (0.5 - progress) * 22;
            setStyle(element, {{
              opacity: String(active ? Math.max(0, Math.min(build, 1 - resolve * .96)) : 0),
              visibility: active ? "visible" : "hidden",
              transform: "translate3d(" + x.toFixed(2) + "px," + y.toFixed(2) + "px,0) scale(" + scale.toFixed(4) + ")"
            }});
            var copyX = (1 - build) * -34;
            var copyY = (1 - build) * 20;
            if (compositionMode === "full-bleed") {{
              copyX = (1 - build) * -18;
              copyY = (1 - build) * 22 + Math.sin(progress * Math.PI) * -3;
            }} else if (compositionMode === "cta-lockup") {{
              copyX = (1 - build) * -24;
              copyY = (1 - build) * 10;
            }}
            setStyle(element.querySelector(".scene-copy"), {{
              transform: "translate3d(" + copyX.toFixed(2) + "px," + copyY.toFixed(2) + "px,0)",
              opacity: String(active ? build : 0)
            }});
            var cardRotateY = -3.2 + build * 2.4 + breathe * .32;
            var cardRotateX = 1.2 - build * .7;
            var cardX = 0;
            var cardY = (1 - build) * 14 - breathe * 2 - audio.mid * .5;
            var cardScale = 0.992 + breathe * .006 + audio.bass * .002;
            if (cameraPath === "hero-push") {{
              cardRotateY = -.8 + breathe * .16;
              cardRotateX = .25 - build * .18;
              cardX = (1 - build) * 10 - progress * 7;
              cardY = (1 - build) * 10 - progress * 5;
              cardScale = 1.004 + progress * .020 + breathe * .003;
            }} else if (cameraPath === "lateral-scan") {{
              cardRotateY = -2.2 + build * 1.4;
              cardRotateX = .8;
              cardX = (0.5 - progress) * 14;
              cardY = (1 - build) * 10;
              cardScale = .995 + breathe * .004;
            }} else if (cameraPath === "macro-zoom") {{
              cardRotateY = -1.1 + breathe * .20;
              cardRotateX = .7 - build * .3;
              cardX = -progress * 8;
              cardY = (1 - build) * 10 - breathe * 1.5;
              cardScale = 1.006 + progress * .022 + breathe * .004;
            }} else if (cameraPath === "board-orbit") {{
              cardRotateY = -1.8 + Math.sin(progress * Math.PI * 1.2) * 1.2;
              cardRotateX = .9 + Math.cos(progress * Math.PI) * .28;
              cardX = Math.sin(progress * Math.PI) * 8;
              cardY = (1 - build) * 12 - breathe * 1.2;
              cardScale = .996 + breathe * .004;
            }} else if (cameraPath === "lockup-dolly") {{
              cardRotateY = -.5 + build * .35;
              cardRotateX = .3;
              cardX = progress * -4;
              cardY = (1 - build) * 8;
              cardScale = 1.0 + easeOut(progress) * .014;
            }}
            setStyle(element.querySelector(".visual-card"), {{
              transform: "perspective(1200px) rotateY(" + cardRotateY.toFixed(2) + "deg) rotateX(" + cardRotateX.toFixed(2) + "deg) translate3d(" + cardX.toFixed(2) + "px," + cardY.toFixed(2) + "px,0) scale(" + cardScale.toFixed(4) + ")",
              opacity: String(active ? build : 0),
              boxShadow: "0 34px " + Math.round(110 + audio.treble * 50) + "px rgba(0,0,0,.38), 0 0 " + Math.round(audio.treble * 34) + "px rgba(255,244,191,.18)"
            }});
            applyLayoutMotion(element, progress, active, audio);
            element.querySelectorAll(".kinetic-chip").forEach(function (chip, chipIndex) {{
              var chipBuild = easeOut((progress - 0.10 - chipIndex * 0.035) / 0.20);
              setStyle(chip, {{
                opacity: String(active ? chipBuild : 0),
                transform: "translateY(" + ((1 - chipBuild) * 18).toFixed(2) + "px)"
              }});
            }});
            element.querySelectorAll(".beat-layer").forEach(function (beat) {{
              var beatStart = Number(beat.dataset.start || scene.start);
              var beatDuration = Math.max(0.1, Number(beat.dataset.duration || 0.5));
              var local = clamp((time - beatStart) / beatDuration, 0, 1);
              var beatIn = easeOut(local / 0.38);
              var beatOut = easeIn((local - 0.84) / 0.16);
              var beatActive = time >= beatStart && time < beatStart + beatDuration;
              setStyle(beat, {{
                opacity: String(beatActive ? Math.max(0, Math.min(beatIn, 1 - beatOut * .96)) : 0),
                transform: "translateY(" + ((1 - beatIn) * 12 - beatOut * 8).toFixed(2) + "px) scale(" + (.992 + beatIn * .008).toFixed(4) + ")"
              }});
            }});
            element.querySelectorAll(".waveform i").forEach(function (bar, barIndex) {{
              var wave = 0.48 + audio.rms * .42 + 0.30 * Math.sin(time * 3.0 + barIndex * .72 + scene.index);
              setStyle(bar, {{ transform: "scaleY(" + wave.toFixed(3) + ")" }});
            }});
            element.querySelectorAll(".site-screenshot").forEach(function (shot, shotIndex) {{
              var shotIn = easeOut((progress - 0.12 - shotIndex * 0.04) / 0.30);
              var scan = clamp((progress - 0.18) / 0.70, 0, 1);
              var pan = (-0.10 + scan * 0.20 + Math.sin(progress * Math.PI) * 0.018);
              var zoom = 1.006 + shotIn * 0.016 + Math.sin(progress * Math.PI) * 0.004;
              if (cameraPath === "hero-push") {{
                pan = -0.05 + scan * 0.10;
                zoom = 1.010 + scan * .018 + Math.sin(progress * Math.PI) * .004;
              }} else if (cameraPath === "lateral-scan") {{
                pan = -0.16 + scan * 0.32;
                zoom = 1.008 + Math.sin(progress * Math.PI) * .005;
              }} else if (cameraPath === "macro-zoom") {{
                pan = -0.04 + scan * 0.10;
                zoom = 1.026 + scan * .034;
              }} else if (cameraPath === "board-orbit") {{
                pan = Math.sin(progress * Math.PI * 1.2) * .10;
                zoom = 1.012 + Math.sin(progress * Math.PI) * .007;
              }} else if (cameraPath === "lockup-dolly") {{
                pan = -0.02 + scan * .06;
                zoom = 1.010 + scan * .014;
              }}
              shot.style.setProperty("--shot-pan", pan.toFixed(4));
              shot.style.setProperty("--shot-zoom", zoom.toFixed(4));
              shot.style.setProperty("--glow", (0.16 + scan * 0.42 + audio.treble * 0.18).toFixed(4));
              setStyle(shot, {{
                opacity: String(active ? shotIn : 0),
                transform: "translateY(" + ((1 - shotIn) * 12).toFixed(2) + "px) rotateX(" + ((1 - shotIn) * 1.8).toFixed(2) + "deg) scale(" + (0.996 + shotIn * .004).toFixed(4) + ")",
                boxShadow: "0 " + Math.round(24 + scan * 12) + "px " + Math.round(72 + scan * 34) + "px rgba(0,0,0,.24), 0 0 " + Math.round(10 + scan * 24) + "px rgba(255,244,191,.14)"
              }});
              shot.querySelectorAll(".site-scan-highlight").forEach(function (highlight) {{
                var highlightIn = easeOut((progress - 0.30) / 0.30);
                var highlightOut = easeIn((progress - 0.88) / 0.12);
                setStyle(highlight, {{
                  opacity: String(active ? Math.max(0, Math.min(highlightIn, 1 - highlightOut * .92)) : 0),
                  transform: "translateY(" + ((1 - highlightIn) * 10 - highlightOut * 8).toFixed(2) + "px) scale(" + (.97 + highlightIn * .03).toFixed(4) + ")"
                }});
                highlight.style.setProperty("--sweep", (-110 + scan * 220).toFixed(2) + "%");
              }});
            }});
            setStyle(nav, {{ opacity: active ? "1" : ".62" }});
            if (nav) nav.dataset.active = active ? "true" : "false";
            if (active && focus) {{
              var visualBox = element.querySelector(".search") || element.querySelector(".visual-card");
              var rect = visualBox && visualBox.getBoundingClientRect();
              if (rect) {{
                setStyle(focus, {{
                  opacity: String(progress > .18 && progress < .64 ? .92 : 0),
                  transform: "translate3d(" + (rect.left + rect.width / 2 - 245).toFixed(2) + "px," + (rect.top + rect.height / 2 - 36).toFixed(2) + "px,0)"
                }});
              }}
            }}
          }});
          if (gsapCompat) gsapCompat.seek(time);
        }}
      }};
    }})();
    window.renderFrame = function () {{}};
'''


def maybe_data_url(value: str) -> str:
    if value.startswith(("http://", "https://", "data:")):
        return value
    path = Path(value)
    if not path.exists():
        raise SenseAudioError(f"Reference image not found: {value}")
    mime = mimetypes.guess_type(path.name)[0] or "image/png"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def image_data_url(path: Path) -> str:
    if not path.exists():
        raise SenseAudioError(f"Image not found: {path}")
    mime = mimetypes.guess_type(path.name)[0] or "image/png"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def content_items(args: argparse.Namespace) -> list[dict[str, Any]]:
    content: list[dict[str, Any]] = []
    if args.prompt:
        content.append({"type": "text", "text": args.prompt})
    for image in args.image or []:
        content.append({"type": "image", "url": maybe_data_url(image), "role": args.image_role})
    for audio_url in args.audio_url or []:
        content.append({"type": "audio", "audio_url": audio_url})
    for video_url in args.video_url or []:
        content.append({"type": "video", "video_url": video_url})
    if not content:
        raise SenseAudioError("Provide --prompt, --image, --audio-url, or --video-url.")
    return content


def style_preset(name: str) -> dict[str, Any]:
    if name not in STYLE_PRESETS:
        raise SenseAudioError(f"Unknown style preset: {name}")
    return STYLE_PRESETS[name]


def command_styles(args: argparse.Namespace) -> None:
    if args.preset:
        payload: dict[str, Any] = {"preset": args.preset, **style_preset(args.preset)}
    else:
        payload = {"presets": STYLE_PRESETS}
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    if args.preset:
        print(f"{args.preset}\t{payload['description']}")
        for key, value in payload["tokens"].items():
            print(f"{key}\t{value}")
        return
    for name, item in STYLE_PRESETS.items():
        recommended = item.get("recommended", {})
        print(f"{name}\t{item['description']}\tanimation={recommended.get('animation_preset')}\ttransition={recommended.get('transition_preset')}")


def command_brand_extract(args: argparse.Namespace) -> None:
    markup = Path(args.html_file).read_text(encoding="utf-8") if args.html_file else fetch_url_text(args.url)
    brand = extract_brand(args.url, markup)
    if args.project:
        project_dir = Path(args.project).resolve()
        output = Path(args.output) if args.output else brand_file_path(project_dir)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps({"source": "brand-extract", "brand": brand}, ensure_ascii=False, indent=2), encoding="utf-8")
        if (project_dir / "senseframe.json").exists():
            register_asset(project_dir, "brand", "json", output, "brand-profile", {"source_url": brand.get("source_url", "")})
    elif args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(json.dumps({"source": "brand-extract", "brand": brand}, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.json:
        print(json.dumps({"brand": brand}, ensure_ascii=False, indent=2))
    else:
        print(brand.get("name", ""))


def command_site_ingest(args: argparse.Namespace) -> None:
    markup = Path(args.html_file).read_text(encoding="utf-8") if args.html_file else fetch_url_text(args.url)
    brand = extract_brand(args.url, markup)
    site_profile = extract_site_profile(args.url, markup, brand)
    if args.project:
        project_dir = Path(args.project).resolve()
        output = Path(args.output) if args.output else site_profile_path(project_dir)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps({"source": "site-ingest", "site": site_profile}, ensure_ascii=False, indent=2), encoding="utf-8")
        if (project_dir / "senseframe.json").exists():
            register_asset(project_dir, "site-profile", "json", output, "website-evidence", {"source_url": site_profile.get("source_url", "")})
    elif args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(json.dumps({"source": "site-ingest", "site": site_profile}, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.json:
        print(json.dumps({"site": site_profile}, ensure_ascii=False, indent=2))
    else:
        print(site_profile.get("title", ""))


def command_source_ingest(args: argparse.Namespace) -> None:
    if args.file:
        source_path = Path(args.file).expanduser()
        text = source_path.read_text(encoding="utf-8", errors="replace")
        suffix = source_path.suffix.lower()
        source_type = "markdown" if suffix in {".md", ".markdown", ".mdx"} else "text"
        source_url = source_path.resolve().as_uri()
        source_name = source_path.name
    else:
        text, source_url = fetch_github_readme(args.github_url)
        source_type = "github-readme"
        source_name = args.github_url
    title_override = args.title or ""
    if source_type == "github-readme" and not title_override:
        _owner, repo = parse_github_repo(args.github_url)
        title_override = repo.replace("-", " ").replace("_", " ").title()
    site_profile = source_profile_from_text(text, source_url, source_name, source_type, title_override)
    payload = {"source": "source-ingest", "site": site_profile}
    project_dir = Path(args.project).resolve() if args.project else None
    output = Path(args.output) if args.output else (site_profile_path(project_dir) if project_dir else None)
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    if project_dir and (project_dir / "senseframe.json").exists():
        register_asset(project_dir, "site-profile", "json", output or site_profile_path(project_dir), "source-evidence", {"source_url": site_profile.get("source_url", ""), "source_type": source_type})
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    elif output:
        print(str(output))
    else:
        print(site_profile.get("title", ""))


def command_site_capture(args: argparse.Namespace) -> None:
    project_dir = Path(args.project).resolve() if args.project else None
    if args.output_dir:
        output_dir = Path(args.output_dir)
    elif project_dir:
        output_dir = project_dir / "assets" / "site-screenshots"
    else:
        output_dir = Path("site-screenshots")
    existing_site_profile = {}
    if project_dir and site_profile_path(project_dir).exists():
        existing_site_profile = read_site_profile_file(str(site_profile_path(project_dir)))
    site_asset_output = site_assets_path(project_dir) if project_dir and args.site_assets else None
    site_asset_download_dir = (project_dir / "assets" / "site-assets") if project_dir and args.download_site_assets else None
    quality_output = (project_dir / "assets" / "site-capture-quality.json") if project_dir else None
    browser_profile = getattr(args, "browser_profile", None) or os.environ.get("SENSEFRAME_SITE_BROWSER_PROFILE")
    cookie_file = getattr(args, "cookie_file", None) or os.environ.get("SENSEFRAME_SITE_COOKIE_FILE")
    screenshots = capture_site_screenshots(
        args.url,
        output_dir,
        count=args.count,
        width=args.width,
        height=args.height,
        evidence=existing_site_profile.get("story_evidence") or existing_site_profile.get("evidence") or [],
        wait_seconds=args.wait,
        capture_timeout=args.capture_timeout,
        site_asset_output=site_asset_output,
        site_asset_download_dir=site_asset_download_dir,
        browser_profile_dir=browser_profile,
        cookie_file=cookie_file,
        quality_output=quality_output,
    )
    site_asset_inventory = {}
    if site_asset_output and site_asset_output.exists():
        site_asset_inventory = json.loads(site_asset_output.read_text(encoding="utf-8"))
    if project_dir:
        site_path = site_profile_path(project_dir)
        if site_path.exists():
            site_profile = existing_site_profile or read_site_profile_file(str(site_path))
            site_profile = add_site_screenshots_to_profile(site_profile, screenshots)
            if site_asset_inventory:
                site_profile = add_site_assets_to_profile(site_profile, project_dir, site_asset_inventory)
            site_profile = add_site_capture_quality_to_profile(site_profile, project_dir, quality_output)
            write_site_profile_file(project_dir, site_profile, "site-capture")
        if (project_dir / "senseframe.json").exists():
            register_site_screenshot_assets(project_dir, screenshots)
            if site_asset_output and site_asset_output.exists():
                register_asset(project_dir, "site-assets", "json", site_asset_output, "website-asset-inventory", {"source_url": args.url, "counts": site_asset_inventory.get("counts", {})})
            if quality_output and quality_output.exists():
                quality = json.loads(quality_output.read_text(encoding="utf-8"))
                register_asset(project_dir, "site-capture-quality", "json", quality_output, "website-capture-quality", {"ok": quality.get("ok", True), "cookie_mode": quality.get("cookie_mode", "clean")})
    if args.json:
        payload: dict[str, Any] = {"screenshots": screenshots}
        if site_asset_inventory:
            payload["site_assets"] = site_asset_inventory
        if quality_output and quality_output.exists():
            payload["capture_quality"] = json.loads(quality_output.read_text(encoding="utf-8"))
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        for shot in screenshots:
            print(shot.get("path", ""))


def beats_path(project_dir: Path) -> Path:
    return project_dir / "assets" / "beats.json"


def read_project_beats(project_dir: Path) -> list[dict[str, Any]]:
    path = beats_path(project_dir)
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    return list(payload.get("beats", []))


def write_beats_file(project_dir: Path, beats: list[dict[str, Any]], source: str = "generated") -> Path:
    output = beats_path(project_dir)
    output.parent.mkdir(parents=True, exist_ok=True)
    payload = {"source": source, "count": len(beats), "beats": beats}
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    register_asset(project_dir, "beats", "json", output, "beat-composition", {"count": len(beats), "source": source})
    return output


def command_beats(args: argparse.Namespace) -> None:
    project_dir = Path(args.project).resolve()
    meta = read_project_meta(project_dir)
    storyboard = meta.get("storyboard") or storyboard_from_brief(str(meta.get("brief", "")), float(meta.get("duration", DEFAULT_RENDER_DURATION)))
    narration_path = project_dir / "assets" / "narration.txt"
    narration = narration_path.read_text(encoding="utf-8") if narration_path.exists() else narration_from_brief(str(meta.get("brief", "")))
    headline = str(meta.get("headline") or "SenseAudio")
    beats = build_beats(storyboard, narration, headline, args.beats_per_scene)
    output = Path(args.output).resolve() if args.output else write_beats_file(project_dir, beats, "beats-command")
    if args.output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps({"source": "beats-command", "count": len(beats), "beats": beats}, ensure_ascii=False, indent=2), encoding="utf-8")
        if output.resolve().is_relative_to(project_dir):
            register_asset(project_dir, "beats", "json", output, "beat-composition", {"count": len(beats), "source": "beats-command"})
    payload = {"project": str(project_dir), "output": str(output), "count": len(beats), "beats": beats}
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(str(output))


def build_video_payload(args: argparse.Namespace) -> dict[str, Any]:
    provider_specific: dict[str, Any] = {"generate_audio": args.generate_audio}
    if args.camera_fixed is not None:
        provider_specific["camera_fixed"] = args.camera_fixed
    duration = normalized_video_duration(args.model, int(args.duration))
    return {
        "model": args.model,
        "content": content_items(args),
        "duration": duration,
        "resolution": args.resolution,
        "ratio": args.ratio,
        "watermark": args.watermark,
        "provider_specific": provider_specific,
    }


def normalized_video_duration(model: str, requested: int) -> int:
    model_name = str(model or "")
    duration = max(1, int(requested or 1))
    if "Seedance-2.0" in model_name:
        return max(duration, 15)
    if "Seedance-Pro-1.5" in model_name:
        return max(duration, 12)
    return duration


def command_video_create(args: argparse.Namespace) -> None:
    payload = build_video_payload(args)
    if args.dry_run:
        write_json(args.manifest, {"dry_run": True, "endpoint": "/video/create", "payload": payload})
        return
    result = request_json("POST", "/video/create", payload)
    manifest: dict[str, Any] = {"request": payload, "create_response": result}
    task_id = result.get("task_id")
    if args.poll and task_id:
        manifest["status_response"] = poll_video(task_id, args.interval, args.timeout)
        video_url = manifest["status_response"].get("video_url")
        if video_url and args.download:
            manifest["downloaded_video"] = download_url(video_url, args.download)
    write_json(args.manifest, manifest)


def poll_video(task_id: str, interval: int, timeout: int) -> dict[str, Any]:
    deadline = time.time() + timeout
    last: dict[str, Any] = {}
    while time.time() <= deadline:
        last = request_json("GET", "/video/status", query={"id": task_id})
        status = last.get("status")
        print(f"{task_id}: {status} {last.get('progress', 0)}%", file=sys.stderr)
        if status in {"completed", "failed"}:
            return last
        time.sleep(interval)
    raise SenseAudioError(f"Timed out waiting for video task: {task_id}")


def command_video_status(args: argparse.Namespace) -> None:
    result = poll_video(args.task_id, args.interval, args.timeout) if args.poll else request_json(
        "GET", "/video/status", query={"id": args.task_id}
    )
    if result.get("video_url") and args.download:
        result["downloaded_video"] = download_url(result["video_url"], args.download)
    write_json(args.output, result)


def compact_payload(payload: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in payload.items() if value not in (None, "", [], {})}


def normalize_music_style(value: str) -> tuple[str, float]:
    text = (value or "").strip().lower()
    if not text:
        return "cinematic", 0.78
    mapping = {
        "cinematic": ("cinematic", 0.78),
        "ambient": ("ambient", 0.72),
        "electronic": ("electronic", 0.76),
        "piano": ("piano", 0.74),
        "uplifting": ("pop", 0.70),
        "pop": ("pop", 0.70),
    }
    if text in mapping:
        return mapping[text]
    if "piano" in text or "钢琴" in text or "鋼琴" in text:
        return "piano", 0.74
    if "ambient" in text or "氛围" in text or "氛圍" in text:
        return "ambient", 0.72
    if "electronic" in text or "synth" in text or "电子" in text or "電子" in text:
        return "electronic", 0.76
    if "pop" in text or "uplifting" in text:
        return "pop", 0.70
    return "cinematic", 0.78


def normalize_vocal_gender(value: str | None) -> str:
    text = (value or "").strip().lower()
    if text in {"m", "male", "man", "男", "男声", "男聲"}:
        return "m"
    return "f"


def instrumental_lyrics_for_duration(duration: int | float | None) -> str:
    try:
        seconds = float(duration or 0)
    except (TypeError, ValueError):
        seconds = 0
    if seconds and seconds <= 12:
        return "[intro-short] ; [inst-short] ; [outro-short]"
    if seconds and seconds > 32:
        return "[intro-medium] ; [inst-medium] ; [inst-medium] ; [outro-medium]"
    return "[intro-medium] ; [inst-medium] ; [outro-short]"


def build_music_payload(args: argparse.Namespace) -> dict[str, Any]:
    using_prompt = not bool(args.lyrics)
    if using_prompt and args.instrumental:
        lyrics_or_prompt = instrumental_lyrics_for_duration(getattr(args, "duration", None))
        using_prompt = False
    else:
        lyrics_or_prompt = args.prompt if using_prompt else args.lyrics
    if len(lyrics_or_prompt) > 2000:
        raise SenseAudioError("SenseAudio music lyrics/prompt must be 2000 codepoints or fewer.")
    style, style_weight = normalize_music_style(args.style)
    negative_tags = args.negative_tags
    if args.instrumental and "vocal" not in negative_tags.lower() and "人声" not in negative_tags:
        negative_tags = f"{negative_tags}, vocals, singing, rap, 人声, 说唱"
    payload = {
        "model": args.model,
        "lyrics": lyrics_or_prompt,
        "style": style,
        "style_weight": style_weight,
        "title": args.title,
        "negative_tags": negative_tags,
        "instrumental": bool(args.instrumental),
    }
    if using_prompt:
        payload["custom_mode"] = True
    if not args.instrumental:
        payload["vocal_gender"] = normalize_vocal_gender(getattr(args, "vocal_gender", None) or getattr(args, "vocal_id", None))
    return compact_payload(payload)


def first_music_download_url(payload: dict[str, Any]) -> str:
    data_containers: list[Any] = [payload.get("data")]
    response = payload.get("response")
    if isinstance(response, dict):
        data_containers.append(response.get("data"))
    for data in data_containers:
        if isinstance(data, dict):
            for key in ("audio_url", "url", "flac_url"):
                if data.get(key):
                    return str(data[key])
        if isinstance(data, list):
            for item in data:
                if not isinstance(item, dict):
                    continue
                for key in ("audio_url", "url", "flac_url"):
                    if item.get(key):
                        return str(item[key])
    choices = payload.get("choices") or []
    if isinstance(choices, list):
        for choice in choices:
            if not isinstance(choice, dict):
                continue
            url = choice.get("url") or choice.get("flac_url") or choice.get("audio_url")
            if url:
                return str(url)
    return str(payload.get("url") or payload.get("audio_url") or "")


def music_task_status(payload: dict[str, Any]) -> str:
    status = str(payload.get("status") or "").lower()
    if status:
        return status
    response = payload.get("response")
    if isinstance(response, dict) and response.get("status"):
        return str(response["status"]).lower()
    data = payload.get("data")
    if isinstance(data, dict) and data.get("status"):
        return str(data["status"]).lower()
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict) and item.get("status"):
                return str(item["status"]).lower()
    choices = payload.get("choices") or []
    if isinstance(choices, list):
        for choice in choices:
            if isinstance(choice, dict) and choice.get("status"):
                return str(choice["status"]).lower()
    return ""


def poll_music(task_id: str, interval: int, timeout: int) -> dict[str, Any]:
    deadline = time.time() + timeout
    last: dict[str, Any] = {}
    while time.time() <= deadline:
        try:
            last = request_json("GET", f"/music/song/pending/{urllib.parse.quote(task_id)}")
        except Exception as exc:
            print(f"{task_id}: retry after network error {exc}", file=sys.stderr)
            time.sleep(interval)
            continue
        status = music_task_status(last)
        print(f"{task_id}: {status or 'pending'}", file=sys.stderr)
        if status in {"succeeded", "success", "failed", "timeouted", "cancelled"}:
            return last
        time.sleep(interval)
    raise SenseAudioError(f"Timed out waiting for music task: {task_id}")


def command_music_create(args: argparse.Namespace) -> None:
    payload = build_music_payload(args)
    endpoint = "/music/song/create"
    if args.dry_run:
        write_json(args.manifest, {"dry_run": True, "endpoint": endpoint, "payload": payload})
        return
    models_to_try = [str(payload.get("model") or DEFAULT_MUSIC_MODEL)]
    for fallback_model in MUSIC_MODEL_FALLBACKS:
        if fallback_model not in models_to_try:
            models_to_try.append(fallback_model)
    models_to_try.append("")
    result: dict[str, Any] | None = None
    last_error: Exception | None = None
    used_model = models_to_try[0]
    for model_name in models_to_try:
        if model_name:
            payload["model"] = model_name
        else:
            payload.pop("model", None)
        try:
            result = request_json("POST", endpoint, payload)
            used_model = model_name or "provider-default"
            break
        except SenseAudioError as exc:
            last_error = exc
            if "model" not in str(exc).lower() and "模型" not in str(exc):
                raise
    if result is None:
        raise last_error or SenseAudioError("Music create failed.")
    data = result.get("data") if isinstance(result.get("data"), dict) else {}
    task_id = str(result.get("id") or result.get("task_id") or data.get("id") or data.get("task_id") or "")
    manifest: dict[str, Any] = {"request": payload, "create_response": result, "model": used_model}
    status_response = result
    if args.poll and task_id:
        try:
            status_response = poll_music(task_id, args.interval, args.timeout)
        except SenseAudioError as exc:
            manifest["status_response"] = {"task_id": task_id, "status": "timeouted", "error": str(exc)}
            manifest["failure_summary"] = str(exc)
            if args.project:
                output = Path(args.manifest) if args.manifest else Path(args.project).resolve() / "assets" / "music-task.json"
                output.parent.mkdir(parents=True, exist_ok=True)
                output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
                register_asset(Path(args.project).resolve(), "music-task", "json", output, "senseaudio-music-task", {"task_id": task_id, "model": payload.get("model")})
            raise
        manifest["status_response"] = status_response
        failure = music_failure_summary(status_response)
        if failure and music_task_status(status_response) in {"failed", "timeouted", "cancelled"}:
            manifest["failure_summary"] = failure
    download_url_value = first_music_download_url(status_response)
    if download_url_value and args.download:
        manifest["downloaded_music"] = download_url(download_url_value, args.download)
        if args.project:
            register_asset(Path(args.project).resolve(), args.asset_id, "audio", Path(args.download), "background-music", {"source": "senseaudio-music", "task_id": task_id})
    if args.project:
        output = Path(args.manifest) if args.manifest else Path(args.project).resolve() / "assets" / "music-task.json"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
        register_asset(Path(args.project).resolve(), "music-task", "json", output, "senseaudio-music-task", {"task_id": task_id, "model": payload.get("model")})
        print(str(output))
        return
    write_json(args.manifest, manifest)


def command_music_status(args: argparse.Namespace) -> None:
    endpoint = f"/music/song/pending/{args.id}"
    if args.dry_run:
        write_json(args.output, {"dry_run": True, "endpoint": endpoint, "poll": bool(args.poll)})
        return
    result = poll_music(args.id, args.interval, args.timeout) if args.poll else request_json("GET", f"/music/song/pending/{urllib.parse.quote(args.id)}")
    download_url_value = first_music_download_url(result)
    if download_url_value and args.download:
        result["downloaded_music"] = download_url(download_url_value, args.download)
        if args.project:
            register_asset(Path(args.project).resolve(), args.asset_id, "audio", Path(args.download), "background-music", {"source": "senseaudio-music", "task_id": args.id})
    write_json(args.output, result)


def command_image(args: argparse.Namespace, async_mode: bool) -> None:
    payload = {
        "model": args.model,
        "prompt": args.prompt,
    }
    if args.size:
        payload["size"] = args.size
    if args.seed is not None:
        payload["seed"] = args.seed
    if args.reference:
        payload["reference"] = maybe_data_url(args.reference)
    if args.dry_run:
        write_json(args.manifest, {"dry_run": True, "payload": payload})
        return
    result = request_json("POST", "/image/async" if async_mode else "/image/sync", payload)
    if not async_mode and result.get("url") and args.download:
        result["downloaded_image"] = download_url(result["url"], args.download)
    write_json(args.manifest, result)


def image_payload(prompt: str, model: str, size: str, seed: int | None = None, reference: str | None = None) -> dict[str, Any]:
    payload: dict[str, Any] = {"model": model, "prompt": prompt}
    if size:
        payload["size"] = size
    if seed is not None:
        payload["seed"] = seed
    if reference:
        payload["reference"] = maybe_data_url(reference)
    return payload


def planned_asset(
    project_dir: Path,
    asset_id: str,
    asset_type: str,
    role: str,
    request: dict[str, Any],
    path: str = "",
    status: str = "planned",
) -> dict[str, Any]:
    manifest = read_asset_manifest(project_dir)
    item = {
        "id": asset_id,
        "type": asset_type,
        "role": role,
        "path": path,
        "status": status,
        "request": request,
    }
    manifest.setdefault("assets", {})[asset_id] = item
    write_asset_manifest(project_dir, manifest)
    meta = read_project_meta(project_dir)
    meta.setdefault("assets", {})[asset_id] = item
    save_project_meta(project_dir, meta)
    return item


def command_generate_assets(args: argparse.Namespace) -> None:
    project_dir = Path(args.project).resolve()
    project_dir.joinpath("assets").mkdir(parents=True, exist_ok=True)
    meta = read_project_meta(project_dir)
    brief = str(meta.get("brief", ""))
    headline = str(meta.get("headline", meta.get("title", "")))
    image_prompt = args.image_prompt or (
        f"Polished product UI hero visual for SenseAudio, {headline or brief}, clean Chinese SaaS webpage, soft light"
    )
    video_prompt = args.video_prompt or (
        f"Short product b-roll for SenseAudio sound library, search filters voice clone workflow, clean UI motion"
    )
    planned: list[dict[str, Any]] = []

    if args.images:
        image_models_to_try = [str(args.image_model or DEFAULT_IMAGE_MODEL)]
        image_models_to_try.extend(model for model in IMAGE_MODEL_FALLBACKS if model not in image_models_to_try)
        request = {"endpoint": "/image/sync", "payload": image_payload(image_prompt, image_models_to_try[0], args.image_size)}
        if args.dry_run:
            planned.append(planned_asset(project_dir, args.image_id, "image", "hero", request, "", "planned"))
        else:
            result: dict[str, Any] | None = None
            image_attempted_models: list[str] = []
            last_error: Exception | None = None
            for model in image_models_to_try:
                image_attempted_models.append(model)
                request = {"endpoint": "/image/sync", "payload": image_payload(image_prompt, model, args.image_size)}
                try:
                    result = request_json("POST", "/image/sync", request["payload"])
                    break
                except SenseAudioError as exc:
                    last_error = exc
                    if "model" not in str(exc).lower() and "参数错误" not in str(exc):
                        raise
            if result is None:
                raise last_error or SenseAudioError("Image generation failed before returning a result.")
            output = project_dir / "assets" / f"{args.image_id}.png"
            if result.get("url"):
                download_url(result["url"], str(output))
            elif result.get("data", {}).get("url"):
                download_url(result["data"]["url"], str(output))
            else:
                (project_dir / "assets" / f"{args.image_id}.json").write_text(
                    json.dumps(result, ensure_ascii=False, indent=2),
                    encoding="utf-8",
                )
                output = project_dir / "assets" / f"{args.image_id}.json"
            planned.append(register_asset(project_dir, args.image_id, "image", output, "hero", {"request": request, "response": result, "attempted_models": image_attempted_models}))

    if args.broll:
        attempted_models: list[str] = []
        models_to_try = [str(args.video_model or DEFAULT_VIDEO_MODEL)]
        models_to_try.extend(model for model in VIDEO_MODEL_FALLBACKS if model not in models_to_try)
        video_args = argparse.Namespace(
            model=models_to_try[0],
            prompt=video_prompt,
            image=[],
            image_role="reference",
            audio_url=[],
            video_url=[],
            duration=args.video_duration,
            resolution=args.video_resolution,
            ratio=args.video_ratio,
            watermark=False,
            generate_audio=False,
            camera_fixed=None,
        )
        request = {"endpoint": "/video/create", "payload": build_video_payload(video_args)}
        if args.dry_run:
            planned.append(planned_asset(project_dir, args.video_id, "video", "broll", request, "", "planned"))
        else:
            result: dict[str, Any] | None = None
            last_error: Exception | None = None
            for model in models_to_try:
                attempted_models.append(model)
                video_args.model = model
                request = {"endpoint": "/video/create", "payload": build_video_payload(video_args)}
                try:
                    result = request_json("POST", "/video/create", request["payload"])
                    break
                except SenseAudioError as exc:
                    last_error = exc
                    if "model" not in str(exc).lower() and "参数错误" not in str(exc):
                        raise
            if result is None:
                item = planned_asset(project_dir, args.video_id, "video", "broll", request, "", "unavailable")
                item["attempted_models"] = attempted_models
                item["error"] = str(last_error or "Video generation failed before returning a task.")
                manifest = read_asset_manifest(project_dir)
                manifest["assets"][args.video_id] = item
                write_asset_manifest(project_dir, manifest)
                meta = read_project_meta(project_dir)
                meta.setdefault("assets", {})[args.video_id] = item
                save_project_meta(project_dir, meta)
                planned.append(item)
                update_asset_html(project_dir)
                print(json.dumps({"dry_run": args.dry_run, "project": str(project_dir), "planned_assets": planned}, ensure_ascii=False, indent=2))
                return
            item = planned_asset(project_dir, args.video_id, "video", "broll", request, "", "submitted")
            item["attempted_models"] = attempted_models
            item["response"] = result
            task_id = result.get("task_id")
            if task_id:
                item["task_id"] = task_id
                meta = read_project_meta(project_dir)
                meta.setdefault("senseaudio", {}).setdefault("video_tasks", []).append({"asset_id": args.video_id, "task_id": task_id})
                save_project_meta(project_dir, meta)
                if args.poll:
                    status = poll_video(task_id, args.interval, args.timeout)
                    item["status_response"] = status
                    if status.get("status") == "completed" and status.get("video_url"):
                        output = project_dir / "assets" / f"{args.video_id}.mp4"
                        download_url(status["video_url"], str(output))
                        item.update(
                            {
                                "path": relative_to_project(project_dir, output),
                                "status": "ready",
                                "metadata": {"request": request, "response": result, "status_response": status},
                            }
                        )
                    elif status.get("status"):
                        item["status"] = status["status"]
            manifest = read_asset_manifest(project_dir)
            manifest["assets"][args.video_id] = item
            write_asset_manifest(project_dir, manifest)
            meta = read_project_meta(project_dir)
            meta.setdefault("assets", {})[args.video_id] = item
            save_project_meta(project_dir, meta)
            planned.append(item)

    update_asset_html(project_dir)
    print(json.dumps({"dry_run": args.dry_run, "project": str(project_dir), "planned_assets": planned}, ensure_ascii=False, indent=2))


def command_tts(args: argparse.Namespace) -> None:
    text = Path(args.text_file).read_text(encoding="utf-8") if args.text_file else args.text
    if not text:
        raise SenseAudioError("Provide --text or --text-file.")
    payload: dict[str, Any] = {
        "model": args.model,
        "text": text,
        "stream": False,
        "voice_setting": {
            "voice_id": args.voice_id,
            "speed": args.speed,
            "vol": args.volume,
            "pitch": args.pitch,
            "latex_read": args.latex_read,
        },
        "audio_setting": {
            "format": args.format,
            "sample_rate": args.sample_rate,
            "bitrate": args.bitrate,
            "channel": args.channel,
        },
    }
    if args.dry_run:
        write_json(args.manifest, {"dry_run": True, "endpoint": "/t2a_v2", "payload": payload})
        return
    result = request_json("POST", "/t2a_v2", payload)
    status = result.get("base_resp", {}).get("status_code")
    if status not in (0, None):
        raise SenseAudioError(result.get("base_resp", {}).get("status_msg", "TTS failed"))
    audio_hex = result.get("data", {}).get("audio")
    if not audio_hex:
        raise SenseAudioError("TTS response did not include data.audio.")
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(bytes.fromhex(audio_hex))
    result["output"] = str(output)
    write_json(args.manifest, result)


def normalize_words(result: dict[str, Any]) -> list[dict[str, Any]]:
    words = result.get("words") or []
    normalized = []
    for index, item in enumerate(words):
        text = item.get("word") or item.get("text") or ""
        if not text:
            continue
        normalized.append(
            {
                "id": f"w{index}",
                "text": text,
                "start": float(item.get("start", 0)),
                "end": float(item.get("end", item.get("start", 0))),
            }
        )
    return normalized


def transcript_words(result: dict[str, Any]) -> list[dict[str, Any]]:
    if result.get("normalized_words"):
        return normalize_words({"words": result["normalized_words"]})
    if result.get("words"):
        return normalize_words(result)
    segments = result.get("segments") or []
    words: list[dict[str, Any]] = []
    for index, segment in enumerate(segments):
        text = str(segment.get("text", "")).strip()
        if text:
            words.append(
                {
                    "id": f"s{index}",
                    "text": text,
                    "start": float(segment.get("start", 0)),
                    "end": float(segment.get("end", segment.get("start", 0))),
                }
            )
    if words:
        return words
    text = str(result.get("text", "")).strip()
    return [{"id": "t0", "text": text, "start": 0.0, "end": 3.0}] if text else []


def build_captions(
    words: list[dict[str, Any]],
    max_gap: float,
    max_chars: int,
    include_words: bool = False,
) -> list[dict[str, Any]]:
    captions: list[dict[str, Any]] = []
    current: list[dict[str, Any]] = []

    def flush() -> None:
        nonlocal current
        if not current:
            return
        text = "".join(item["text"] for item in current).strip()
        if text:
            cue = {
                "id": f"c{len(captions)}",
                "text": text,
                "start": float(current[0]["start"]),
                "end": float(current[-1]["end"]),
            }
            if include_words:
                cue["words"] = [
                    {"text": item["text"], "start": float(item["start"]), "end": float(item["end"])}
                    for item in current
                ]
            captions.append(cue)
        current = []

    for word in words:
        text = str(word.get("text", "")).strip()
        if not text:
            continue
        normalized = {
            "text": text,
            "start": float(word.get("start", 0)),
            "end": float(word.get("end", word.get("start", 0))),
        }
        if current:
            gap = normalized["start"] - float(current[-1]["end"])
            char_count = len("".join(item["text"] for item in current)) + len(text)
            if gap > max_gap or char_count > max_chars:
                flush()
        current.append(normalized)
    flush()
    return captions


def split_caption_text(text: str, max_chars: int = 22) -> list[dict[str, str]]:
    cleaned = clean_text(text)
    if not cleaned:
        return []
    parts = [part.strip() for part in re.split(r"([。.!?！？；;])", cleaned)]
    sentences: list[str] = []
    current = ""
    for part in parts:
        if not part:
            continue
        current += part
        if re.fullmatch(r"[。.!?！？；;]", part):
            sentences.append(current.strip())
            current = ""
    if current.strip():
        sentences.append(current.strip())
    chunks: list[str] = []
    for sentence in sentences or [cleaned]:
        while len(sentence) > max_chars:
            split_at = max(sentence.rfind("，", 0, max_chars), sentence.rfind(",", 0, max_chars), sentence.rfind("、", 0, max_chars), sentence.rfind(" ", 0, max_chars))
            if split_at < max_chars * 0.45:
                split_at = max_chars
            chunks.append(sentence[:split_at].strip(" ，,、"))
            sentence = sentence[split_at:].strip(" ，,、")
        if sentence:
            chunks.append(sentence)
    return [{"text": chunk} for chunk in chunks if chunk]


def build_even_captions(text: str, duration: float, max_chars: int = 22, min_duration: float = 1.45) -> list[dict[str, Any]]:
    chunks = split_caption_text(text, max_chars)
    if not chunks:
        return []
    cue_count = min(len(chunks), max(1, int(duration / min_duration)))
    if len(chunks) > cue_count:
        merged: list[str] = []
        for index in range(cue_count):
            start = round(index * len(chunks) / cue_count)
            end = round((index + 1) * len(chunks) / cue_count)
            merged.append("".join(chunk["text"] for chunk in chunks[start:end]))
        chunks = [{"text": item[: max_chars * 2]} for item in merged if item]
    span = duration / max(1, len(chunks))
    captions: list[dict[str, Any]] = []
    for index, item in enumerate(chunks):
        start = round(index * span, 3)
        end = round(min(duration, (index + 1) * span), 3)
        captions.append({"id": f"c{index}", "start": start, "end": end, "text": item["text"]})
    return captions


def command_captions(args: argparse.Namespace) -> None:
    project_dir = Path(args.project).resolve() if args.project else None
    transcript_path = Path(args.transcript)
    if not transcript_path.exists():
        raise SenseAudioError(f"Transcript not found: {transcript_path}")
    result = json.loads(transcript_path.read_text(encoding="utf-8"))
    captions = build_captions(transcript_words(result), args.max_gap, args.max_chars, args.include_words)
    payload = {
        "source": str(transcript_path),
        "captions": captions,
    }
    output = Path(args.output) if args.output else (
        project_dir / "assets" / "captions.json" if project_dir else Path("captions.json")
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    if project_dir:
        register_asset(
            project_dir,
            args.asset_id,
            "captions",
            output,
            "subtitle",
            {"source": relative_to_project(project_dir, transcript_path), "count": len(captions)},
        )
    print(str(output))


def command_asr(args: argparse.Namespace) -> None:
    file_path = Path(args.file)
    if not file_path.exists():
        raise SenseAudioError(f"Audio/video file not found: {file_path}")
    fields = [
        ("model", args.model),
        ("response_format", "verbose_json" if args.timestamps else args.response_format),
    ]
    if args.language:
        fields.append(("language", args.language))
    if args.enable_punctuation:
        fields.append(("enable_punctuation", "true"))
    if args.timestamps:
        for granularity in args.timestamps.split(","):
            fields.append(("timestamp_granularities[]", granularity.strip()))
    if args.dry_run:
        write_json(args.output, {"dry_run": True, "endpoint": "/audio/transcriptions", "fields": fields, "file": str(file_path)})
        return
    result = multipart_request("/audio/transcriptions", fields, "file", file_path)
    if isinstance(result, str):
        write_json(args.output, {"text": result})
        return
    if args.normalize_words:
        result["normalized_words"] = normalize_words(result)
    write_json(args.output, result)


def command_voices(args: argparse.Namespace) -> None:
    payload = {"voice_type": args.voice_type}
    if args.dry_run:
        write_json(args.output, {"dry_run": True, "endpoint": "/get_voice", "payload": payload})
        return
    write_json(args.output, request_json("POST", "/get_voice", payload))


def read_project_meta(project_dir: Path) -> dict[str, Any]:
    meta_path = project_dir / "senseframe.json"
    if not meta_path.exists():
        index = project_dir / "index.html"
        if not index.exists():
            raise SenseAudioError(f"Project must contain index.html: {project_dir}")
        return {
            "width": DEFAULT_WIDTH,
            "height": DEFAULT_HEIGHT,
            "duration": DEFAULT_RENDER_DURATION,
            "fps": DEFAULT_RENDER_FPS,
            "entry": "index.html",
        }
    return json.loads(meta_path.read_text(encoding="utf-8"))


def find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def find_chrome() -> str:
    env = os.environ.get("CHROME_BIN")
    if env:
        return env
    for name in ("google-chrome", "chrome", "chromium", "chromium-browser"):
        found = shutil.which(name)
        if found:
            return found
    mdfind = shutil.which("mdfind")
    if mdfind:
        try:
            result = subprocess.check_output(
                [mdfind, "kMDItemCFBundleIdentifier == 'com.google.Chrome'"],
                text=True,
                timeout=5,
            )
            app_path = next((line.strip() for line in result.splitlines() if line.strip()), "")
            if app_path:
                candidate = Path(app_path) / "Contents" / "MacOS" / "Google Chrome"
                if candidate.exists():
                    return str(candidate)
        except Exception:
            pass
    raise SenseAudioError("Chrome/Chromium not found. Set CHROME_BIN to a headless-capable browser.")


def find_ffmpeg() -> str:
    found = shutil.which("ffmpeg")
    if not found:
        raise SenseAudioError("ffmpeg not found in PATH.")
    return found


def audio_data_payload(audio_path: Path, fps: int, bands: int, duration: float | None = None) -> dict[str, Any]:
    if fps <= 0:
        raise SenseAudioError("--fps must be positive.")
    if bands <= 0:
        raise SenseAudioError("--bands must be positive.")
    sample_rate = 16000
    ffmpeg = find_ffmpeg()
    cmd = [
        ffmpeg,
        "-v",
        "error",
        "-i",
        str(audio_path),
        "-ac",
        "1",
        "-ar",
        str(sample_rate),
        "-f",
        "s16le",
        "pipe:1",
    ]
    raw = subprocess.check_output(cmd)
    samples = array.array("h")
    samples.frombytes(raw)
    if sys.byteorder != "little":
        samples.byteswap()
    samples_per_frame = max(1, int(sample_rate / fps))
    total_frames = max(1, math.ceil(len(samples) / samples_per_frame))
    if duration:
        total_frames = max(total_frames, int(math.ceil(duration * fps)))
    rms_values: list[float] = []
    for frame_index in range(total_frames):
        start = frame_index * samples_per_frame
        chunk = samples[start : start + samples_per_frame]
        if not chunk:
            rms_values.append(0.0)
            continue
        squared = sum((sample / 32768.0) ** 2 for sample in chunk)
        rms_values.append(math.sqrt(squared / len(chunk)))
    peak = max(rms_values) or 1.0
    normalized_values = [min(1.0, value / peak) for value in rms_values]
    smoothed_values: list[float] = []
    previous = 0.0
    for value in normalized_values:
        coefficient = 0.22 if value > previous else 0.14
        previous = previous + (value - previous) * coefficient
        smoothed_values.append(previous)
    backward = 0.0
    for index in range(len(smoothed_values) - 1, -1, -1):
        value = smoothed_values[index]
        backward = value if index == len(smoothed_values) - 1 else backward + (value - backward) * 0.18
        smoothed_values[index] = max(value, backward * 0.72)
    frames: list[dict[str, Any]] = []
    for frame_index, normalized in enumerate(smoothed_values):
        band_values = []
        for band_index in range(bands):
            shaped = normalized * (0.76 + band_index * 0.035)
            shimmer = 0.014 * abs(math.sin(frame_index * 0.21 + band_index * 0.61))
            band_values.append(round(min(1.0, shaped + shimmer), 4))
        frames.append({"rms": round(normalized, 4), "rawRms": round(normalized_values[frame_index], 4), "bands": band_values})
    return {
        "source": audio_path.name,
        "fps": fps,
        "bands": bands,
        "totalFrames": len(frames),
        "duration": round(len(frames) / fps, 4),
        "frames": frames,
    }


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: Any) -> None:
        return


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


def start_static_server(project_dir: Path, port: int) -> tuple[ReusableTCPServer, threading.Thread]:
    handler = lambda *args, **kwargs: QuietHandler(*args, directory=str(project_dir), **kwargs)
    server = ReusableTCPServer(("127.0.0.1", port), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, thread


def command_init(args: argparse.Namespace) -> None:
    project_dir = Path(args.name)
    project_dir.mkdir(parents=True, exist_ok=True)
    (project_dir / "assets").mkdir(exist_ok=True)
    (project_dir / "renders").mkdir(exist_ok=True)
    (project_dir / "index.html").write_text(STARTER_HTML, encoding="utf-8")
    (project_dir / "senseframe-runtime.js").write_text(RUNTIME_JS, encoding="utf-8")
    meta = {
        "name": project_dir.name,
        "entry": "index.html",
        "width": args.width,
        "height": args.height,
        "duration": args.duration,
        "fps": args.fps,
        "assets": {},
        "senseaudio": {
            "voices": [],
            "image_tasks": [],
            "video_tasks": [],
            "transcripts": [],
        },
    }
    save_project_meta(project_dir, meta)
    write_asset_manifest(project_dir, {"project": project_dir.name, "assets": {}})
    print(str(project_dir))


def contains_cjk(text: str) -> bool:
    return any("\u4e00" <= char <= "\u9fff" for char in text)


def chinese_topic_from_brief(brief: str) -> str:
    cleaned = " ".join(brief.split())
    if not cleaned:
        return "声音、字幕与视频资产的一体化创作流程"
    named_match = re.search(r"名为\s*([^，。；;]+?)\s*的([^，。；;]+)", cleaned)
    if named_match:
        name = named_match.group(1).strip()
        category = re.split(r"(?:制作|打造|推出|生成|用于|，|。|；|;)", named_match.group(2).strip(), maxsplit=1)[0].strip()
        return f"{name} 的{category}"[:80]
    if contains_cjk(cleaned):
        clauses = [part.strip() for part in re.split(r"[。；;]", cleaned) if part.strip()]
        useful = [
            clause
            for clause in clauses
            if not any(token in clause for token in ("风格", "不要", "短片", "视频", "制作", "画面", "镜头"))
        ]
        return (useful[0] if useful else clauses[0])[:80]
    lower = cleaned.lower()
    glossary = [
        ("senseaudio", "SenseAudio"),
        ("sound library", "音色库"),
        ("voice market", "音色广场"),
        ("voice clone", "声音克隆"),
        ("clone", "声音克隆"),
        ("one-click", "一键使用"),
        ("search", "搜索"),
        ("filter", "筛选"),
        ("popular voices", "热门音色"),
        ("voice scenarios", "音色使用场景"),
        ("creator workflow", "创作者工作流"),
        ("webpage", "网页"),
        ("website", "网站"),
        ("product page", "产品页面"),
        ("login", "登录入口"),
        ("claude", "Claude"),
    ]
    topics: list[str] = []
    for needle, label in glossary:
        if needle in lower and label not in topics:
            topics.append(label)
    if topics:
        return "、".join(topics[:8])
    return "这个产品页面的核心功能与使用路径"


def storyboard_from_brief(brief: str, duration: float) -> list[dict[str, Any]]:
    topic = chinese_topic_from_brief(brief)
    scene_count = brief_storyboard_scene_count(duration)
    chapter_intents = [
        {
            "id": "chapter-1",
            "intent": f"核心主张：{topic[:72]}",
        },
        {
            "id": "chapter-2",
            "intent": "问题张力：从信息过载、协作摩擦或决策迟缓切入，建立为什么现在需要它。",
        },
        {
            "id": "chapter-3",
            "intent": "系统能力：展示它如何把输入、理解、生成、复核和交付串成连续工作流。",
        },
        {
            "id": "chapter-4",
            "intent": "能力证据：协作、引用、风险提示与摘要形成完整工作流。",
        },
        {
            "id": "chapter-5",
            "intent": "使用场景：把能力落到团队研究、内容生产、客户沟通或运营分析的真实任务里。",
        },
        {
            "id": "chapter-6",
            "intent": "行动结论：把复杂研究压缩成可信、可追溯、可执行的团队决策。",
        },
        {
            "id": "chapter-7",
            "intent": "扩展路径：说明它如何接入现有流程、资产库和多人协作节奏。",
        },
        {
            "id": "chapter-8",
            "intent": "品牌气质：用更克制的视觉节奏强调可靠、清晰和长期价值。",
        },
        {
            "id": "chapter-9",
            "intent": "收束号召：回到一句明确判断，让观众知道下一步该关注什么。",
        },
    ]
    selected = chapter_intents[:scene_count]
    storyboard: list[dict[str, Any]] = []
    for index, item in enumerate(selected):
        start = duration * index / scene_count
        end = duration * (index + 1) / scene_count
        storyboard.append(
            {
                "id": item["id"],
                "start": round(start, 3),
                "end": round(end, 3),
                "intent": item["intent"],
            }
        )
    return storyboard


def narration_from_brief(brief: str, duration: float | None = None) -> str:
    topic = chinese_topic_from_brief(brief)
    if duration is not None and is_longform_duration(duration):
        return (
            f"这支影片介绍{topic}。开篇先建立一个清晰判断：它面向的不只是单点功能，"
            "而是一套更稳定的工作方式。随后镜头展开关键能力，包括信息整理、内容生成、"
            "协作复核和交付沉淀。中段用证据层和场景层说明它如何进入真实任务，帮助团队减少反复沟通，"
            "把复杂材料转成可执行结论。最后影片收束到长期价值：更快看清问题，更稳完成表达，"
            "也让每一次创作都有可以追溯的依据。"
        )
    return (
        f"这支影片介绍{topic}。它先建立核心主张，再展开关键能力与可信证据，"
        "最后收束到适用场景、决策价值和下一步行动。"
    )


def llm_plan_schema() -> dict[str, Any]:
    return {
        "type": "object",
        "required": ["title", "headline", "narration", "visual_style", "storyboard"],
        "properties": {
            "title": {"type": "string"},
            "headline": {"type": "string"},
            "narration": {"type": "string"},
            "visual_style": {"type": "string"},
            "storyboard": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["id", "start", "end", "intent"],
                    "properties": {
                        "id": {"type": "string"},
                        "start": {"type": "number"},
                        "end": {"type": "number"},
                        "intent": {"type": "string"},
                    },
                },
            },
        },
    }


def build_llm_payload(brief: str, duration: float, audience: str, style: str, model: str) -> dict[str, Any]:
    schema = llm_plan_schema()
    longform = is_longform_duration(duration)
    target_scene_count = brief_storyboard_scene_count(duration)
    return {
        "model": model,
        "temperature": 0.46 if longform else 0.4,
        "response_format": {"type": "json_object"},
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a video creative director for HTML-authored product explainer videos. "
                    f"Return strict JSON only. Default video language is {DEFAULT_VIDEO_LANGUAGE}; write concise Chinese copy unless the brief explicitly requests another language. "
                    "The JSON must include title, headline, narration, visual_style, and storyboard. "
                    "Storyboard items need id, start, end, and intent. Keep narration shorter than the video duration. "
                    "Content must feel researched: extract concrete product capabilities, target users, workflows, proof points, limitations, and next actions from the provided brief or website evidence. "
                    "Avoid generic phrases such as improves efficiency, empowers teams, or intelligent platform unless followed by a concrete mechanism. "
                    + (
                        "For longform work, think in passes before writing JSON: strategy, audience tension, narrative arc, proof points, visual rhythm, and caption compression. "
                        "Do not expose these passes as prose; express the result through richer storyboard intents with varied scene purposes."
                        if longform
                        else ""
                    )
                ),
            },
            {
                "role": "user",
                "content": json.dumps(
                    {
                        "brief": brief,
                        "duration_seconds": duration,
                        "director_mode": "longform" if longform else "standard",
                        "target_scene_count": target_scene_count,
                        "audience": audience,
                        "style": style,
                        "creative_requirements": [
                            "Use Chinese by default.",
                            "Avoid repeating the same abstract card in every scene.",
                            "Each scene must add a new strategic point.",
                            "Prefer mature restrained business-film copy over playful UI labels.",
                            "Use concrete nouns from the product: named features, user roles, workflow steps, evidence, risks, and CTA.",
                            "If website evidence is provided, base claims only on that evidence and say what the page actually shows.",
                            "For every storyboard intent, include one specific mechanism or observable proof point.",
                        ],
                        "schema": schema,
                    },
                    ensure_ascii=False,
                ),
            },
        ],
    }


def audioclaw_config_path() -> Path:
    return Path(os.environ.get("AUDIOCLAW_CONFIG_PATH", "") or DEFAULT_AUDIOCLAW_CONFIG_PATH).expanduser()


def normalize_platform_model(base_url: str, model: str) -> str:
    if "platform.senseaudio.cn" in base_url and "/" in model:
        return model.split("/", 1)[1]
    return model


def load_audioclaw_llm_config(model_name: str | None = None) -> dict[str, str]:
    path = audioclaw_config_path()
    if not path.exists():
        return {
            "provider": "audioclaw",
            "model_name": DEFAULT_AUDIOCLAW_LLM_MODEL,
            "model": DEFAULT_AUDIOCLAW_LLM_MODEL,
            "base_url": DEFAULT_AUDIOCLAW_LLM_BASE_URL,
            "api_key": "",
            "config_path": str(path),
        }
    try:
        config = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SenseAudioError(f"AudioClaw config is not valid JSON: {path}") from exc
    models = config.get("model_list")
    if not isinstance(models, list) or not models:
        raise SenseAudioError(f"AudioClaw config has no model_list: {path}")
    default_name = str(config.get("agents", {}).get("defaults", {}).get("model_name") or "")
    wanted = model_name or default_name
    selected = None
    for item in models:
        if not isinstance(item, dict):
            continue
        if wanted and item.get("model_name") == wanted:
            selected = item
            break
    if selected is None:
        selected = next((item for item in models if isinstance(item, dict)), None)
    if not selected:
        raise SenseAudioError(f"AudioClaw config has no usable model entry: {path}")
    base_url = str(selected.get("api_base") or "").strip()
    model = str(selected.get("model") or selected.get("model_name") or "").strip()
    api_key = str(selected.get("api_key") or "").strip()
    if not base_url or not model or not api_key:
        raise SenseAudioError(f"AudioClaw model entry is missing api_base, model, or api_key: {path}")
    return {
        "provider": "audioclaw",
        "model_name": str(selected.get("model_name") or model),
        "model": normalize_platform_model(base_url, model),
        "base_url": base_url,
        "api_key": api_key,
        "config_path": str(path),
    }


def resolve_audioclaw_llm_api_key(config: dict[str, str]) -> str:
    return (
        os.environ.get("AUDIOCLAW_LLM_API_KEY", "").strip()
        or str(config.get("api_key") or "").strip()
    )


def chat_headers(api_key: str, provider: str) -> dict[str, str]:
    key = api_key.strip()
    if not key:
        if provider == "audioclaw":
            raise SenseAudioError("AUDIOCLAW_LLM_API_KEY or an AudioClaw config api_key is required for --provider audioclaw live calls.")
        if provider == "openrouter":
            raise SenseAudioError("OPENROUTER_API_KEY or VL_API_KEY is required for --provider openrouter live calls.")
        raise SenseAudioError("DEEPSEEK_API_KEY is required for --provider deepseek live calls.")
    return {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }


def openai_chat_completion(base_url: str, payload: dict[str, Any], api_key: str, provider: str) -> dict[str, Any]:
    url = base_url.rstrip("/") + "/chat/completions"
    req = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        method="POST",
        headers=chat_headers(api_key, provider),
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            raw = resp.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        if exc.code == 400 and "response_format" in body and payload.get("response_format"):
            retry_payload = dict(payload)
            retry_payload.pop("response_format", None)
            retry_req = urllib.request.Request(
                url,
                data=json.dumps(retry_payload, ensure_ascii=False).encode("utf-8"),
                method="POST",
                headers=chat_headers(api_key, provider),
            )
            try:
                with urllib.request.urlopen(retry_req, timeout=120) as resp:
                    raw = resp.read().decode("utf-8")
            except urllib.error.HTTPError as retry_exc:
                retry_body = retry_exc.read().decode("utf-8", errors="replace")
                raise SenseAudioError(f"{provider} HTTP {retry_exc.code}: {retry_body}") from retry_exc
        else:
            raise SenseAudioError(f"{provider} HTTP {exc.code}: {body}") from exc
    return json.loads(raw)


def extract_json_object(text: str) -> dict[str, Any]:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start >= 0 and end > start:
            return json.loads(cleaned[start : end + 1])
        raise


def compress_storyboard(storyboard: list[dict[str, Any]], duration: float) -> list[dict[str, Any]]:
    if not storyboard:
        return storyboard
    target_count = storyboard_scene_limit(duration)
    if len(storyboard) <= target_count:
        return storyboard
    compressed: list[dict[str, Any]] = []
    for output_index in range(target_count):
        start_index = round(output_index * len(storyboard) / target_count)
        end_index = round((output_index + 1) * len(storyboard) / target_count)
        group = storyboard[start_index : max(start_index + 1, end_index)]
        intents = [str(item.get("intent", "")).strip() for item in group if str(item.get("intent", "")).strip()]
        intent = " ".join(intents[:1] + intents[-1:]) if len(intents) > 1 else (intents[0] if intents else "")
        compressed.append(
            {
                "id": safe_scene_id(group[0].get("id") or f"scene-{output_index + 1}", output_index),
                "start": round(duration * output_index / target_count, 3),
                "end": round(duration * (output_index + 1) / target_count, 3),
                "intent": intent or f"推进视频叙事第 {output_index + 1} 段。",
            }
        )
    return compressed


def normalize_llm_plan(plan: dict[str, Any], brief: str, duration: float) -> dict[str, Any]:
    storyboard = plan.get("storyboard") if isinstance(plan.get("storyboard"), list) else []
    normalized_storyboard: list[dict[str, Any]] = []
    for index, item in enumerate(storyboard):
        if not isinstance(item, dict):
            continue
        start = float(item.get("start", 0 if index == 0 else normalized_storyboard[-1]["end"]))
        end = float(item.get("end", min(duration, start + duration / max(1, len(storyboard)))))
        end = max(start + 0.1, min(duration, end))
        normalized_storyboard.append(
            {
                "id": str(item.get("id") or f"scene-{index + 1}"),
                "start": round(start, 3),
                "end": round(end, 3),
                "intent": str(item.get("intent") or item.get("description") or "Advance the video story."),
            }
        )
    if not normalized_storyboard:
        normalized_storyboard = storyboard_from_brief(brief, duration)
    normalized_storyboard = compress_storyboard(normalized_storyboard, duration)
    return {
        "title": str(plan.get("title") or "SenseAudio HTML Video"),
        "headline": str(plan.get("headline") or "热门音色"),
        "narration": str(plan.get("narration") or narration_from_brief(brief, duration)),
        "visual_style": str(plan.get("visual_style") or plan.get("style") or "clean product UI"),
        "storyboard": normalized_storyboard,
    }


def create_llm_plan(args: argparse.Namespace, brief: str) -> dict[str, Any]:
    provider = args.provider if hasattr(args, "provider") else args.llm
    if provider not in {"deepseek", "audioclaw", "openrouter"}:
        raise SenseAudioError(f"Unsupported LLM provider: {provider}")
    if provider == "audioclaw":
        config = load_audioclaw_llm_config(getattr(args, "model_name", None))
        base_url = (
            getattr(args, "base_url", None)
            or getattr(args, "llm_base_url", None)
            or os.environ.get("AUDIOCLAW_LLM_BASE_URL")
            or config["base_url"]
            or DEFAULT_AUDIOCLAW_LLM_BASE_URL
        )
        model = (
            getattr(args, "model", None)
            or getattr(args, "llm_model", None)
            or os.environ.get("AUDIOCLAW_LLM_MODEL")
            or config["model"]
            or DEFAULT_AUDIOCLAW_LLM_MODEL
        )
        api_key = resolve_audioclaw_llm_api_key(config)
        model = normalize_platform_model(base_url, model)
    elif provider == "openrouter":
        base_url = (
            getattr(args, "base_url", None)
            or getattr(args, "llm_base_url", None)
            or os.environ.get("OPENROUTER_LLM_BASE_URL")
            or os.environ.get("OPENROUTER_BASE_URL")
            or DEFAULT_OPENROUTER_BASE_URL
        )
        model = (
            getattr(args, "model", None)
            or getattr(args, "llm_model", None)
            or os.environ.get("OPENROUTER_LLM_MODEL")
            or os.environ.get("OPENROUTER_MODEL")
            or DEFAULT_OPENROUTER_LLM_MODEL
        )
        api_key = os.environ.get("OPENROUTER_API_KEY", "").strip() or os.environ.get("VL_API_KEY", "").strip()
    else:
        base_url = (
            getattr(args, "base_url", None)
            or getattr(args, "llm_base_url", None)
            or os.environ.get("DEEPSEEK_BASE_URL")
            or DEFAULT_DEEPSEEK_BASE_URL
        )
        model = (
            getattr(args, "model", None)
            or getattr(args, "llm_model", None)
            or os.environ.get("DEEPSEEK_MODEL")
            or DEFAULT_DEEPSEEK_MODEL
        )
        api_key = os.environ.get("DEEPSEEK_API_KEY", "").strip()
    duration = float(args.duration)
    if getattr(args, "longform", False):
        duration = max(LONGFORM_MIN_DURATION, duration)
    audience = getattr(args, "audience", "general creators")
    style = getattr(args, "style", "polished product UI explainer")
    payload = build_llm_payload(brief, duration, audience, style, model)
    if getattr(args, "dry_run", False):
        return {
            "provider": provider,
            "model": model,
            "base_url": base_url.rstrip("/"),
            "url": base_url.rstrip("/") + "/chat/completions",
            "payload": payload,
            "schema": llm_plan_schema(),
        }
    response = openai_chat_completion(base_url, payload, api_key, provider)
    content = response.get("choices", [{}])[0].get("message", {}).get("content", "")
    if not content:
        raise SenseAudioError(f"{provider} response did not include choices[0].message.content.")
    plan = normalize_llm_plan(extract_json_object(content), brief, duration)
    plan["_llm"] = {"provider": provider, "model": model, "base_url": base_url.rstrip("/")}
    return plan


def vl_api_key() -> str:
    key = os.environ.get("OPENROUTER_API_KEY", "").strip() or os.environ.get("VL_API_KEY", "").strip()
    if not key:
        raise SenseAudioError("OPENROUTER_API_KEY or VL_API_KEY is required for live vision audit calls.")
    return key


def vl_chat_completion(base_url: str, payload: dict[str, Any]) -> dict[str, Any]:
    url = base_url.rstrip("/") + "/chat/completions"
    req = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        method="POST",
        headers={
            "Authorization": f"Bearer {vl_api_key()}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://senseaudio-video-gen.local",
            "X-Title": "senseaudio-video-gen",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            raw = resp.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise SenseAudioError(f"Vision HTTP {exc.code}: {body}") from exc
    return json.loads(raw)


def vision_audit_schema() -> dict[str, Any]:
    return {
        "type": "object",
        "required": ["summary", "scores", "issues", "recommended_changes"],
        "properties": {
            "summary": {"type": "string"},
            "scores": {
                "type": "object",
                "properties": {
                    "content_accuracy": {"type": "number"},
                    "composition_maturity": {"type": "number"},
                    "readability": {"type": "number"},
                    "crop_quality": {"type": "number"},
                },
            },
            "issues": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "image": {"type": "string"},
                        "severity": {"type": "string"},
                        "problem": {"type": "string"},
                        "evidence": {"type": "string"},
                        "fix": {"type": "string"},
                    },
                },
            },
            "recommended_changes": {"type": "array", "items": {"type": "string"}},
            "safe_to_render": {"type": "boolean"},
        },
    }


def vision_audit_payload(
    images: list[Path],
    project_dir: Path | None,
    model: str,
    brief: str,
    site_profile: dict[str, Any] | None = None,
) -> dict[str, Any]:
    schema = vision_audit_schema()
    site_context = site_profile or {}
    content: list[dict[str, Any]] = [
        {
            "type": "text",
            "text": (
                "你是严苛的视频美术指导和网页截图质检员。请看这些视频画面/网页截图，"
                "判断是否有内容不对、裁切错误、批注遮挡主体、字幕遮挡、画面幼稚、信息层级混乱、"
                "高亮框指错位置、或官网真实内容被误读的问题。"
                "只返回 JSON，不要 Markdown。评分 0-10，10 最好。"
                "如果发现画面里有明显英文官网原文，除非它是网页截图本身，否则说明中文解说层应减少英文。"
                "请给出可执行的 CSS/模板/分镜修复建议。"
            ),
        },
        {
            "type": "text",
            "text": json.dumps(
                {
                    "brief": brief,
                    "project": str(project_dir) if project_dir else "",
                    "site": {
                        "title": site_context.get("title", ""),
                        "brand_name": site_context.get("brand_name", ""),
                        "source_url": site_context.get("source_url", ""),
                        "headings": site_context.get("headings", [])[:6],
                        "ctas": site_context.get("ctas", [])[:4],
                    },
                    "expected_schema": schema,
                    "image_order": [path.name for path in images],
                },
                ensure_ascii=False,
            ),
        },
    ]
    for path in images:
        content.append({"type": "text", "text": f"IMAGE: {path.name}"})
        content.append({"type": "image_url", "image_url": {"url": image_data_url(path)}})
    return {
        "model": model,
        "temperature": 0.15,
        "response_format": {"type": "json_object"},
        "messages": [{"role": "user", "content": content}],
    }


def project_vision_images(project_dir: Path, explicit_images: list[str] | None, max_images: int) -> list[Path]:
    if explicit_images:
        return [Path(item).resolve() if Path(item).is_absolute() else (project_dir / item).resolve() for item in explicit_images][:max_images]
    candidates: list[Path] = []
    inspect_dir = project_dir / "renders" / "inspect"
    if inspect_dir.exists():
        candidates.extend(sorted(inspect_dir.glob("*.png")))
    screenshot_dir = project_dir / "assets" / "site-screenshots"
    if screenshot_dir.exists():
        candidates.extend(sorted(screenshot_dir.glob("*.png")))
    seen: set[Path] = set()
    unique: list[Path] = []
    for path in candidates:
        resolved = path.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        unique.append(resolved)
        if len(unique) >= max_images:
            break
    if not unique:
        raise SenseAudioError("No images found. Provide --image or run inspect/site-capture first.")
    return unique


def command_site_vision_audit(args: argparse.Namespace) -> None:
    project_dir = Path(args.project).resolve() if args.project else None
    images = project_vision_images(project_dir or Path.cwd(), args.image, args.max_images)
    site_profile = read_site_profile_file(str(site_profile_path(project_dir))) if project_dir and site_profile_path(project_dir).exists() else {}
    meta = read_project_meta(project_dir) if project_dir and (project_dir / "senseframe.json").exists() else {}
    brief = args.brief or str(meta.get("brief", "") or site_profile.get("summary", "") or "Audit website explainer visuals.")
    base_url = args.base_url or os.environ.get("OPENROUTER_BASE_URL") or os.environ.get("VL_BASE_URL") or DEFAULT_OPENROUTER_BASE_URL
    model = args.model or os.environ.get("OPENROUTER_MODEL") or os.environ.get("VL_MODEL") or DEFAULT_VL_MODEL
    payload = vision_audit_payload(images, project_dir, model, brief, site_profile)
    if args.dry_run:
        result = {
            "dry_run": True,
            "provider": "openrouter",
            "model": model,
            "base_url": base_url.rstrip("/"),
            "images": [str(path) for path in images],
            "payload": payload,
        }
    else:
        response = vl_chat_completion(base_url, payload)
        content = response.get("choices", [{}])[0].get("message", {}).get("content", "")
        if not content:
            raise SenseAudioError("Vision response did not include choices[0].message.content.")
        try:
            audit = extract_json_object(content)
        except Exception as exc:
            audit = {
                "summary": content.strip(),
                "scores": {},
                "issues": [],
                "recommended_changes": [],
                "safe_to_render": False,
                "parse_error": str(exc),
            }
        result = {
            "provider": "openrouter",
            "model": model,
            "base_url": base_url.rstrip("/"),
            "images": [str(path) for path in images],
            "audit": audit,
            "usage": response.get("usage", {}),
        }
    output = Path(args.output) if args.output else (project_dir / "assets" / "vision-audit.json" if project_dir else None)
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        if project_dir and (project_dir / "senseframe.json").exists():
            register_asset(project_dir, "vision-audit", "json", output, "visual-quality-audit", {"model": model})
    if args.json or not output:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(str(output))


def command_site_vision_plan(args: argparse.Namespace) -> None:
    project_dir = Path(args.project).resolve() if args.project else None
    if args.site_file:
        site_profile = read_site_profile_file(args.site_file)
    elif project_dir:
        site_profile = read_site_profile_file(str(site_profile_path(project_dir)))
    else:
        raise SenseAudioError("Provide --project or --site-file.")
    if not site_profile:
        raise SenseAudioError("No site profile found for visual planning.")
    fallback_plan = heuristic_visual_plan(site_profile)
    model = getattr(args, "model", None) or os.environ.get("OPENROUTER_MODEL") or os.environ.get("VL_MODEL") or DEFAULT_VL_MODEL
    base_url = getattr(args, "base_url", None) or os.environ.get("OPENROUTER_BASE_URL") or os.environ.get("VL_BASE_URL") or DEFAULT_OPENROUTER_BASE_URL
    provider = args.provider
    if provider == "openrouter":
        images = site_profile_screenshot_paths(project_dir, site_profile, args.max_images)
        if not images:
            if args.fallback:
                provider = "heuristic"
                visual_plan = fallback_plan
            else:
                raise SenseAudioError("No screenshot files found for OpenRouter visual planning.")
        else:
            payload = vision_plan_payload(images, site_profile, model)
            if args.dry_run:
                result = {
                    "dry_run": True,
                    "provider": "openrouter",
                    "model": model,
                    "base_url": base_url.rstrip("/"),
                    "images": [str(path) for path in images],
                    "payload": payload,
                    "visual_plan": fallback_plan,
                }
                print(json.dumps(result, ensure_ascii=False, indent=2))
                return
            try:
                response = vl_chat_completion(base_url, payload)
                content = response.get("choices", [{}])[0].get("message", {}).get("content", "")
                raw = extract_json_object(content).get("visual_plan", []) if content else []
                visual_plan = normalize_visual_plan(raw if isinstance(raw, list) else [], fallback_plan)
            except Exception:
                if not args.fallback:
                    raise
                provider = "heuristic"
                visual_plan = fallback_plan
    else:
        visual_plan = fallback_plan
    planned_profile = apply_visual_plan_to_profile(site_profile, visual_plan)
    result = {
        "provider": provider,
        "model": model if provider == "openrouter" else None,
        "project": str(project_dir) if project_dir else None,
        "source_url": planned_profile.get("source_url", ""),
        "visual_plan": visual_plan,
        "site": planned_profile,
    }
    output = Path(args.output) if args.output else (project_dir / "assets" / "visual-plan.json" if project_dir else None)
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        if project_dir and (project_dir / "senseframe.json").exists():
            write_site_profile_file(project_dir, planned_profile, "site-vision-plan")
            register_asset(project_dir, "visual-plan", "json", output, "visual-crop-plan", {"provider": args.provider})
    if args.json or not output:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(str(output))


def read_json_if_exists(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def read_project_site_profile(project_dir: Path) -> dict[str, Any]:
    return read_site_profile_file(str(site_profile_path(project_dir))) if site_profile_path(project_dir).exists() else {}


def repair_actions_from_reports(project_dir: Path) -> list[str]:
    actions = {"stabilize-motion", "rebalance-composition"}
    vision = read_json_if_exists(project_dir / "assets" / "vision-audit.json")
    frame_quality = read_json_if_exists(project_dir / "assets" / "frame-quality.json")
    motion = read_json_if_exists(project_dir / "assets" / "motion-map.json")
    issues = vision.get("issues") if isinstance(vision.get("issues"), list) else []
    issues.extend(frame_quality.get("issues") if isinstance(frame_quality.get("issues"), list) else [])
    issue_text = json.dumps(issues, ensure_ascii=False).lower()
    if vision.get("safe_to_render") is False or frame_quality.get("safe_to_render") is False or any(token in issue_text for token in ("crop", "screenshot", "hero", "visual", "clutter", "blank", "low_detail")):
        actions.add("tighten-visual-evidence")
    if any(token in issue_text for token in ("caption", "text", "readability", "字幕", "文字")):
        actions.add("improve-readability")
    low_zones = motion.get("low_motion_zones") or motion.get("dead_zones") or []
    if isinstance(low_zones, list) and low_zones:
        actions.add("fill-motion-dead-zones")
    return sorted(actions)


def repair_css() -> str:
    return """
<style id="repair-pass-css">
[data-repair-profile="stabilized"] .story-scene{isolation:isolate}
[data-repair-profile="stabilized"] .beat-layer{transition-duration:.72s!important}
[data-repair-profile="stabilized"] .kinetic-chip{opacity:.62;filter:saturate(.9)}
[data-repair-profile="stabilized"] .waveform{opacity:.46}
[data-repair-profile="stabilized"] .evidence-note{backdrop-filter:blur(18px);max-width:42ch}
[data-repair-profile="stabilized"] .site-shot{filter:contrast(1.04) saturate(.96);box-shadow:0 34px 92px rgba(0,0,0,.36)}
[data-repair-profile="stabilized"] .shot-frame{transform:translate3d(var(--crop-x,0),var(--crop-y,0),0) scale(var(--crop-zoom,1));transform-origin:var(--crop-origin,50% 50%)}
[data-repair-profile="stabilized"] .caption-line{max-width:58ch;line-height:1.24;text-wrap:balance}
</style>
""".strip()


def apply_repair_attributes(markup: str, repair_pass: int) -> str:
    attrs = f'data-repair-pass="{repair_pass}" data-repair-profile="stabilized"'
    if "data-repair-pass=" in markup:
        markup = re.sub(r'data-repair-pass=["\'][^"\']*["\']', f'data-repair-pass="{repair_pass}"', markup, count=1)
    else:
        markup = re.sub(r'(<div\b[^>]*data-composition-id=["\'][^"\']+["\'])', rf'\1 data-repair-pass="{repair_pass}"', markup, count=1)
    if "data-repair-profile=" in markup:
        markup = re.sub(r'data-repair-profile=["\'][^"\']*["\']', 'data-repair-profile="stabilized"', markup, count=1)
    elif "data-repair-pass=" in markup:
        markup = re.sub(r'(data-repair-pass=["\'][^"\']*["\'])', rf'\1 data-repair-profile="stabilized"', markup, count=1)
    if 'id="repair-pass-css"' not in markup:
        markup = markup.replace("</head>", repair_css() + "\n</head>")
    if attrs and "data-repair-profile" not in markup:
        markup = re.sub(r'(<div\b[^>]*data-composition-id=["\'][^"\']+["\'])', rf'\1 {attrs}', markup, count=1)
    return markup


def command_repair(args: argparse.Namespace) -> None:
    project_dir = Path(args.project).resolve()
    meta = read_project_meta(project_dir)
    current_pass = int(meta.get("repair_pass", 0) or 0)
    repair_pass = current_pass + 1
    actions = repair_actions_from_reports(project_dir)
    site_profile = read_project_site_profile(project_dir)
    visual_plan = heuristic_visual_plan(site_profile) if site_profile.get("screenshots") else []
    payload = {
        "dry_run": bool(args.dry_run),
        "project": str(project_dir),
        "repair_pass": repair_pass,
        "profile": "stabilized",
        "actions": actions,
        "visual_plan_count": len(visual_plan),
        "outputs": {
            "repair_plan": str(project_dir / "assets" / "repair-plan.json"),
            "html": str(project_dir / str(meta.get("entry", "index.html"))),
        },
    }
    if args.dry_run:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    if visual_plan:
        site_profile = apply_visual_plan_to_profile(site_profile, visual_plan)
        write_site_profile_file(project_dir, site_profile, "repair")
    entry_path = project_dir / str(meta.get("entry", "index.html"))
    if entry_path.exists():
        entry_path.write_text(apply_repair_attributes(entry_path.read_text(encoding="utf-8"), repair_pass), encoding="utf-8")
    meta["repair_pass"] = repair_pass
    meta["repair_profile"] = "stabilized"
    meta["repair_actions"] = actions
    save_project_meta(project_dir, meta)
    output = project_dir / "assets" / "repair-plan.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload | {"dry_run": False}, ensure_ascii=False, indent=2), encoding="utf-8")
    register_asset(project_dir, "repair-plan", "json", output, "auto-repair-plan", {"repair_pass": repair_pass, "actions": actions})
    print(json.dumps(payload | {"dry_run": False}, ensure_ascii=False, indent=2) if args.json else str(output))


def command_llm_plan(args: argparse.Namespace) -> None:
    brief = args.brief or Path(args.brief_file).read_text(encoding="utf-8")
    if getattr(args, "longform", False):
        args.duration = max(LONGFORM_MIN_DURATION, float(args.duration))
    plan = create_llm_plan(args, brief)
    write_json(args.output, plan)


def default_site_video_brief(args: argparse.Namespace) -> str:
    if args.brief_file:
        return Path(args.brief_file).read_text(encoding="utf-8")
    if args.brief:
        return args.brief
    target = args.url or "这个网站"
    return f"用中文制作一个专业、克制、高级的网站介绍视频，只介绍 {target} 的真实网页内容、核心价值、产品入口和行动路径。"


def site_video_output_path(project_dir: Path, output: str | None) -> Path:
    return Path(output) if output else project_dir / "renders" / f"{project_dir.name}.mp4"


def site_video_plan(args: argparse.Namespace) -> dict[str, Any]:
    project_dir = Path(args.project).resolve()
    output = site_video_output_path(project_dir, args.output)
    steps: list[dict[str, Any]] = [
        {
            "name": "compose",
            "command": "compose",
            "llm": args.llm,
            "site_url": args.url,
            "site_file": args.site_file,
            "site_screenshots": bool(args.site_screenshots and args.url and not args.site_file),
            "browser_profile": bool(args.browser_profile or os.environ.get("SENSEFRAME_SITE_BROWSER_PROFILE")),
            "cookie_file": bool(args.cookie_file or os.environ.get("SENSEFRAME_SITE_COOKIE_FILE")),
            "style_preset": args.style_preset,
            "beat_mode": args.beat_mode,
            "beats_per_scene": args.beats_per_scene,
            "animation_preset": args.animation_preset,
            "transition_preset": args.transition_preset,
            "timeline_engine": args.timeline_engine,
        },
    ]
    if args.music:
        steps.extend(
            [
                {"name": "music-create", "command": "music-create", "model": args.music_model, "poll": args.music_poll},
                {"name": "mix-audio", "command": "mix-audio", "voice": "assets/narration.mp3", "music": "assets/background-music.mp3", "output": "assets/final-audio.m4a"},
            ]
        )
    steps.extend(
        [
            {
                "name": "audio-data",
                "command": "audio-data",
                "audio": "assets/final-audio.m4a" if args.music else "assets/narration.mp3",
                "output": "assets/audio-data.json",
                "fallback": "dry-run when narration or mix audio is unavailable",
            },
            {"name": "lint", "command": "lint"},
        ]
    )
    if args.render:
        steps.append({"name": "render", "command": "render", "output": relative_to_project(project_dir, output)})
    if args.render and args.quality_audit:
        steps.extend(
            [
                {"name": "inspect", "command": "inspect", "samples": args.inspect_samples},
                {"name": "frame-quality-audit", "command": "frame-quality-audit"},
            ]
        )
    steps.extend(
        [
            {"name": "motion-audit", "command": "motion-audit"},
            {"name": "motion-map", "command": "motion-map"},
        ]
    )
    if args.vision_audit:
        if not (args.render and args.quality_audit):
            steps.append({"name": "inspect", "command": "inspect", "samples": args.inspect_samples})
        steps.append({"name": "site-vision-audit", "command": "site-vision-audit", "model": args.vl_model})
    if args.auto_repair:
        steps.append({"name": "repair", "command": "repair", "profile": "stabilized"})
        if args.render:
            steps.append({"name": "render-repair", "command": "render", "output": relative_to_project(project_dir, output)})
    return {
        "pipeline": "site-video",
        "dry_run": bool(args.dry_run),
        "project": str(project_dir),
        "source": {"url": args.url, "site_file": args.site_file},
        "output": str(output),
        "defaults": {
            "llm": args.llm,
            "llm_fallback": args.llm_fallback,
            "style_preset": args.style_preset,
            "beat_mode": args.beat_mode,
            "duration": args.duration,
            "longform": bool(args.longform),
            "fps": args.fps,
            "render": args.render,
            "offline": args.offline,
            "quality_audit": args.quality_audit,
        },
        "steps": steps,
    }


def capture_command_output(func: Any, namespace: argparse.Namespace) -> str:
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        func(namespace)
    return buffer.getvalue().strip()


def site_music_prompt(project_dir: Path, args: argparse.Namespace) -> str:
    if args.music_prompt:
        return args.music_prompt
    site_profile = read_project_site_profile(project_dir)
    brand_name = str(site_profile.get("brand_name") or site_profile.get("title") or "website")
    return f"Short instrumental background bed for a polished website explainer about {brand_name}; warm piano, muted synth pulse, light percussion, confident travel-tech mood, no vocals."


def music_failure_summary(payload: dict[str, Any]) -> str:
    candidates: list[Any] = [
        payload.get("message"),
        payload.get("error"),
        payload.get("reason"),
        payload.get("status_msg"),
        payload.get("base_resp"),
    ]
    response = payload.get("response")
    if isinstance(response, dict):
        candidates.extend([response.get("message"), response.get("error"), response.get("reason"), response.get("status_msg"), response.get("base_resp")])
    for item in candidates:
        if isinstance(item, dict):
            compact = {key: value for key, value in item.items() if value not in (None, "", [], {})}
            if compact:
                return json.dumps(compact, ensure_ascii=False)
        elif item:
            return clean_text(str(item))[:240]
    status = music_task_status(payload)
    if status:
        return f"SenseAudio music task returned status {status} without a detailed error message."
    return ""


def command_site_video(args: argparse.Namespace) -> None:
    if not args.url and not args.site_file:
        raise SenseAudioError("Provide --url for a live website or --site-file for saved site evidence.")
    if getattr(args, "longform", False):
        args.duration = max(LONGFORM_MIN_DURATION, float(args.duration))
    project_dir = Path(args.project).resolve()
    output = site_video_output_path(project_dir, args.output)
    plan = site_video_plan(args)
    if args.dry_run:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return

    brief = default_site_video_brief(args)
    completed: list[dict[str, Any]] = []
    warnings: list[dict[str, str]] = []

    def run_step(name: str, func: Any, namespace: argparse.Namespace) -> None:
        started = time.time()
        stdout = capture_command_output(func, namespace)
        completed.append({"name": name, "ok": True, "seconds": round(time.time() - started, 3), "stdout": stdout[-1200:]})
        if not args.quiet:
            print(f"site-video: {name} ok", file=sys.stderr)

    compose_args = argparse.Namespace(
        project=str(project_dir),
        brief=brief,
        brief_file=None,
        title=args.title,
        headline=args.headline,
        narration=args.narration,
        brand_url=None,
        brand_file=args.brand_file,
        site_url=args.url if not args.site_file else None,
        site_file=args.site_file,
        site_screenshots=bool(args.site_screenshots and args.url and not args.site_file),
        site_screenshot_count=args.site_screenshot_count,
        site_screenshot_wait=args.site_screenshot_wait,
        download_site_assets=args.download_site_assets,
        browser_profile=args.browser_profile,
        cookie_file=args.cookie_file,
        capture_timeout=args.capture_timeout,
        plan_file=args.plan_file,
        llm=args.llm,
        llm_fallback=False,
        llm_model=args.llm_model,
        llm_base_url=args.llm_base_url,
        audience=args.audience,
        style=args.style,
        style_preset=args.style_preset,
        beat_mode=args.beat_mode,
        beats_per_scene=args.beats_per_scene,
        width=args.width,
        height=args.height,
        duration=args.duration,
        longform=args.longform,
        fps=args.fps,
        voice_id=args.voice_id,
        tts_model=args.tts_model,
        asr_model=args.asr_model,
        speed=args.speed,
        generate_images=args.generate_images,
        generate_broll=args.generate_broll,
        asset_dry_run=args.asset_dry_run,
        image_prompt=args.image_prompt,
        video_prompt=args.video_prompt,
        image_size=args.image_size,
        animation_preset=args.animation_preset,
        transition_preset=args.transition_preset,
        timeline_engine=args.timeline_engine,
        offline=args.offline,
        render=False,
        quiet=True,
    )
    try:
        run_step("compose", command_compose, compose_args)
    except Exception as exc:
        if args.llm == "none" or not args.llm_fallback:
            raise
        reason = str(exc).replace("\n", " ")[:240]
        warnings.append({"code": "llm_fallback", "message": f"{args.llm} planning failed; retried compose with heuristic planning.", "reason": reason})
        compose_args.llm = "none"
        compose_args.llm_model = None
        compose_args.llm_base_url = None
        run_step("compose", command_compose, compose_args)

    narration_path = project_dir / "assets" / "narration.mp3"
    audio_path = narration_path
    if args.music:
        music_path = project_dir / "assets" / "background-music.mp3"
        music_manifest_path = project_dir / "assets" / "music-task.json"
        music_create_args = argparse.Namespace(
            prompt=site_music_prompt(project_dir, args),
            lyrics=args.music_lyrics,
            style=args.music_style,
            title=args.music_title or f"{project_dir.name} background bed",
            duration=max(8, int(math.ceil(args.duration))),
            negative_tags=args.music_negative_tags,
            instrumental=args.music_instrumental,
            callback_url=None,
            reference_id=None,
            vocal_id=None,
            use_variance=False,
            model=args.music_model,
            poll=args.music_poll,
            interval=args.music_interval,
            timeout=args.music_timeout,
            download=str(music_path) if args.music_poll else None,
            manifest=str(music_manifest_path),
            project=str(project_dir),
            asset_id="background-music",
            dry_run=args.music_dry_run or args.offline,
        )
        try:
            run_step("music-create", command_music_create, music_create_args)
        except Exception as exc:
            warnings.append({"code": "music_generation_failed", "message": "SenseAudio music generation did not produce a downloadable file.", "reason": str(exc)[:240]})
        if not music_path.exists() and args.music_fallback and not (args.music_dry_run or args.offline):
            try:
                started = time.time()
                generate_procedural_music_bed(project_dir, music_path, args.duration)
                completed.append({"name": "music-fallback", "duration_sec": round(time.time() - started, 3), "stdout": str(music_path)})
                warnings.append({"code": "music_fallback_used", "message": "Used a local procedural background bed because SenseAudio music did not return audio_url in time."})
            except Exception as exc:
                warnings.append({"code": "music_fallback_failed", "message": "Could not create local procedural background music.", "reason": str(exc)[:240]})
        if music_path.exists():
            final_audio_path = project_dir / "assets" / "final-audio.m4a"
            run_step(
                "mix-audio",
                command_mix_audio,
                argparse.Namespace(
                    project=str(project_dir),
                    voice=str(narration_path) if narration_path.exists() else None,
                    music=str(music_path),
                    output=str(final_audio_path),
                    duration=args.duration,
                    music_volume=args.music_volume,
                    asset_id="final-audio",
                    dry_run=False,
                    json=True,
                ),
            )
            audio_path = final_audio_path
        else:
            warnings.append({"code": "music_unavailable", "message": "Background music was submitted or planned, but no downloaded music file was available for mixing."})
    audio_data_path = project_dir / "assets" / "audio-data.json"
    run_step(
        "audio-data",
        command_audio_data,
        argparse.Namespace(
            project=str(project_dir),
            audio=str(audio_path),
            output=str(audio_data_path),
            fps=args.fps,
            bands=8,
            duration=args.duration,
            asset_id="audio-data",
            dry_run=not audio_path.exists(),
        ),
    )
    run_step("lint", command_lint, argparse.Namespace(project=str(project_dir), json=True, strict=True))
    if args.render:
        run_step(
            "render",
            command_render,
            argparse.Namespace(
                project=str(project_dir),
                output=str(output),
                fps=args.fps,
                duration=args.duration,
                width=args.width,
                height=args.height,
                audio=str(audio_path) if audio_path.exists() else None,
                virtual_time_budget=args.virtual_time_budget,
                capture_timeout=args.capture_timeout,
                quiet=True,
                report=str(output.with_suffix(".render.json")),
                asset_id="final-video",
                frame_dir=None,
                keep_frames=False,
                resume=args.resume,
                parallel=args.parallel,
                capture_mode=args.capture_mode,
            ),
        )
    inspect_ran = False
    if args.render and args.quality_audit:
        run_step(
            "inspect",
            command_inspect,
            argparse.Namespace(
                project=str(project_dir),
                samples=args.inspect_samples,
                output_dir=str(project_dir / "renders" / "inspect"),
                report=str(project_dir / "renders" / "inspect" / "inspect.json"),
                width=args.width,
                height=args.height,
                duration=args.duration,
                virtual_time_budget=args.virtual_time_budget,
                capture_timeout=args.capture_timeout,
                json=True,
            ),
        )
        inspect_ran = True
        run_step(
            "frame-quality-audit",
            command_frame_quality_audit,
            argparse.Namespace(
                project=str(project_dir),
                image=None,
                max_images=args.inspect_samples,
                output=str(project_dir / "assets" / "frame-quality.json"),
                json=True,
                strict=True,
            ),
        )
    run_step("motion-audit", command_motion_audit, argparse.Namespace(project=str(project_dir), json=True, strict=True))
    run_step(
        "motion-map",
        command_motion_map,
        argparse.Namespace(project=str(project_dir), samples=24, low_threshold=1.4, min_dead_zone=0.8, json=True, strict=True),
    )
    if args.vision_audit:
        if not inspect_ran:
            run_step(
                "inspect",
                command_inspect,
                argparse.Namespace(
                    project=str(project_dir),
                    samples=args.inspect_samples,
                    output_dir=str(project_dir / "renders" / "inspect"),
                    report=str(project_dir / "renders" / "inspect" / "inspect.json"),
                    width=args.width,
                    height=args.height,
                    duration=args.duration,
                    virtual_time_budget=args.virtual_time_budget,
                    capture_timeout=args.capture_timeout,
                    json=True,
                ),
            )
        run_step(
            "site-vision-audit",
            command_site_vision_audit,
            argparse.Namespace(
                project=str(project_dir),
                image=None,
                brief=brief,
                model=args.vl_model,
                base_url=args.vl_base_url,
                max_images=args.inspect_samples,
                output=str(project_dir / "assets" / "vision-audit.json"),
                dry_run=args.vision_dry_run,
                json=True,
            ),
        )
    if args.auto_repair:
        run_step("repair", command_repair, argparse.Namespace(project=str(project_dir), dry_run=False, json=True))
        if args.render:
            run_step(
                "render-repair",
                command_render,
                argparse.Namespace(
                    project=str(project_dir),
                    output=str(output),
                    fps=args.fps,
                    duration=args.duration,
                    width=args.width,
                    height=args.height,
                    audio=str(audio_path) if audio_path.exists() else None,
                    virtual_time_budget=args.virtual_time_budget,
                    capture_timeout=args.capture_timeout,
                    quiet=True,
                    report=str(output.with_suffix(".render.json")),
                    asset_id="final-video",
                    frame_dir=None,
                    keep_frames=False,
                    resume=args.resume,
                    parallel=args.parallel,
                    capture_mode=args.capture_mode,
                ),
            )

    report = dict(plan)
    report["dry_run"] = False
    report["rendered"] = bool(args.render)
    report["warnings"] = warnings
    report["steps"] = completed
    report["audio"] = str(audio_path) if audio_path.exists() else None
    report["audio_data"] = str(audio_data_path)
    report["report"] = str(project_dir / "pipeline-report.json")
    (project_dir / "pipeline-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


def command_compose(args: argparse.Namespace) -> None:
    project_dir = Path(args.project)
    project_dir.mkdir(parents=True, exist_ok=True)
    (project_dir / "assets").mkdir(exist_ok=True)
    (project_dir / "renders").mkdir(exist_ok=True)
    duration = float(args.duration)
    if getattr(args, "longform", False):
        duration = max(LONGFORM_MIN_DURATION, duration)
    fps = int(args.fps)
    width = int(args.width)
    height = int(args.height)
    beat = duration / 3
    brief = args.brief or Path(args.brief_file).read_text(encoding="utf-8")
    brand: dict[str, Any] = read_brand_file(args.brand_file)
    site_profile: dict[str, Any] = read_site_profile_file(args.site_file)
    if args.brand_url:
        brand_markup = fetch_url_text(args.brand_url)
        brand = extract_brand(args.brand_url, brand_markup)
    if args.site_url:
        site_markup = fetch_url_text(args.site_url)
        if not brand:
            brand = extract_brand(args.site_url, site_markup)
        site_profile = extract_site_profile(args.site_url, site_markup, brand)
    elif site_profile and not brand:
        brand = {
            "source_url": site_profile.get("source_url", ""),
            "domain": site_profile.get("domain", ""),
            "name": site_profile.get("brand_name") or title_brand_name(str(site_profile.get("title", "")), str(site_profile.get("source_url", ""))),
            "page_title": site_profile.get("title", ""),
            "description": site_profile.get("summary", ""),
            "nav": [],
            "colors": {},
            "logos": [],
        }
    if site_profile:
        site_profile = enrich_site_profile_content(site_profile, brief)
    title = args.title or str(brand.get("name", "") or chinese_topic_from_brief(brief))
    headline = args.headline or (
        str(brand.get("description", ""))[:34]
        if brand.get("description")
        else ("网页重点速览" if site_profile else "高级产品叙事")
    )
    style = style_preset(args.style_preset)
    style_tokens = dict(style["tokens"])
    brand_colors = brand.get("colors", {}) if isinstance(brand.get("colors"), dict) else {}
    if brand_colors.get("primary"):
        style_tokens["accent"] = str(brand_colors["primary"])
    if brand_colors.get("secondary"):
        style_tokens["ember"] = str(brand_colors["secondary"])
    llm_plan: dict[str, Any] | None = None
    warnings: list[dict[str, str]] = []
    if args.plan_file:
        llm_plan = normalize_llm_plan(json.loads(Path(args.plan_file).read_text(encoding="utf-8")), brief, duration)
    elif args.llm != "none":
        try:
            llm_plan = create_llm_plan(
                argparse.Namespace(
                    provider=args.llm,
                    base_url=args.llm_base_url,
                    model=args.llm_model,
                    duration=duration,
                    audience=args.audience,
                    style=args.style,
                    longform=getattr(args, "longform", False),
                    dry_run=False,
                ),
                brief + ("\n\n真实网页证据：\n" + json.dumps(site_profile, ensure_ascii=False)[:2400] if site_profile else ""),
            )
        except Exception as exc:
            if not getattr(args, "llm_fallback", False):
                raise
            reason = str(exc).replace("\n", " ")[:240]
            warnings.append({"code": "llm_fallback", "message": f"{args.llm} planning failed; used heuristic planning.", "reason": reason})
            llm_plan = None
    if llm_plan:
        title = args.title or llm_plan["title"]
        headline = args.headline or llm_plan["headline"]
        storyboard = llm_plan["storyboard"]
        narration = args.narration or llm_plan["narration"]
        if site_profile:
            site_profile["story_evidence"] = selected_site_story_evidence(site_profile, len(storyboard))
    else:
        storyboard = storyboard_from_site(site_profile, duration) if site_profile else storyboard_from_brief(brief, duration)
        narration = args.narration or (narration_from_site(site_profile) if site_profile else narration_from_brief(brief, duration))

    if args.site_screenshots:
        screenshot_url = args.site_url or str(site_profile.get("source_url", "") or brand.get("source_url", ""))
        if screenshot_url:
            capture_count = max(args.site_screenshot_count, len(storyboard))
            capture_quality_path = project_dir / "assets" / "site-capture-quality.json"
            screenshots = capture_site_screenshots(
                screenshot_url,
                project_dir / "assets" / "site-screenshots",
                count=capture_count,
                width=width,
                height=height,
                evidence=site_profile.get("story_evidence") or selected_site_story_evidence(site_profile, capture_count),
                wait_seconds=args.site_screenshot_wait,
                capture_timeout=args.capture_timeout,
                site_asset_output=site_assets_path(project_dir),
                site_asset_download_dir=(project_dir / "assets" / "site-assets") if getattr(args, "download_site_assets", False) else None,
                browser_profile_dir=getattr(args, "browser_profile", None) or os.environ.get("SENSEFRAME_SITE_BROWSER_PROFILE"),
                cookie_file=getattr(args, "cookie_file", None) or os.environ.get("SENSEFRAME_SITE_COOKIE_FILE"),
                quality_output=capture_quality_path,
            )
            site_profile = add_site_screenshots_to_profile(site_profile, screenshots)
            site_profile = add_site_capture_quality_to_profile(site_profile, project_dir, capture_quality_path)
            site_asset_output = site_assets_path(project_dir)
            if site_asset_output.exists():
                site_asset_inventory = json.loads(site_asset_output.read_text(encoding="utf-8"))
                site_profile = add_site_assets_to_profile(site_profile, project_dir, site_asset_inventory)
    if site_profile:
        site_profile = ensure_visual_plan(site_profile)

    effective_beats_per_scene = min(args.beats_per_scene, DEFAULT_SITE_BEATS_PER_SCENE) if site_profile else args.beats_per_scene
    production_spec = build_production_spec(brief, storyboard, narration, headline, site_profile)
    planned_beats = build_beats(storyboard, narration, headline, effective_beats_per_scene) if args.beat_mode == "layered" else []
    (project_dir / "senseframe-runtime.js").write_text(RUNTIME_JS, encoding="utf-8")
    scene_layers = build_scene_layers(storyboard, headline, args.generate_images, args.generate_broll, planned_beats, brand, site_profile, production_spec)
    scene_nav = build_scene_nav(storyboard)
    timeline_script = build_timeline_script(storyboard, duration, args.transition_preset, args.timeline_engine, planned_beats, production_spec)
    (project_dir / "index.html").write_text(
        COMPOSE_HTML.format(
            title=html_lib.escape(title),
            headline=html_lib.escape(headline),
            width=width,
            height=height,
            duration=duration,
            brand_name=html_lib.escape(str(brand.get("name", ""))),
            brand_domain=html_lib.escape(str(brand.get("domain", ""))),
            brand_mark=build_brand_mark_html(brand),
            site_mode=site_mode_for_project(args.style_preset, site_profile),
            style_preset=args.style_preset,
            accent=style_tokens["accent"],
            ember=style_tokens["ember"],
            aqua=style_tokens["aqua"],
            ink=style_tokens["ink"],
            muted=style_tokens["muted"],
            body_bg=style_tokens["body_bg"],
            stage_bg=style_tokens["stage_bg"],
            card_from=style_tokens["card_from"],
            card_to=style_tokens["card_to"],
            mesh=style_tokens["mesh"],
            scene_layers=scene_layers,
            scene_nav=scene_nav,
            timeline_script=timeline_script,
            transition_preset=args.transition_preset,
        ),
        encoding="utf-8",
    )
    narration_path = project_dir / "assets" / "narration.txt"
    narration_path.write_text(narration, encoding="utf-8")
    storyboard_path = project_dir / "assets" / "storyboard.json"
    storyboard_path.write_text(json.dumps(storyboard, ensure_ascii=False, indent=2), encoding="utf-8")
    style_path = project_dir / "assets" / "style-preset.json"
    style_path.write_text(
        json.dumps({"preset": args.style_preset, **style}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    production_spec_path = project_dir / "assets" / "production-spec.json"
    production_spec_path.write_text(json.dumps(production_spec, ensure_ascii=False, indent=2), encoding="utf-8")
    if llm_plan:
        llm_plan_path = project_dir / "assets" / "llm-plan.json"
        llm_plan_path.write_text(json.dumps(llm_plan, ensure_ascii=False, indent=2), encoding="utf-8")
    captions_path = project_dir / "assets" / "captions.json"
    if not captions_path.exists():
        caption_items = build_even_captions(narration, duration, max_chars=24 if site_profile else 18, min_duration=1.55)
        captions_path.write_text(
            json.dumps(
                {
                    "source": "compose",
                    "captions": caption_items,
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

    meta = {
        "name": project_dir.name,
        "entry": "index.html",
        "width": width,
        "height": height,
        "duration": duration,
        "fps": fps,
        "brief": brief,
        "title": title,
        "headline": headline,
        "llm": llm_plan.get("_llm") if llm_plan else None,
        "warnings": warnings,
        "visual_style": llm_plan.get("visual_style") if llm_plan else None,
        "director_mode": "longform" if is_longform_duration(duration) else "standard",
        "production_spec": "assets/production-spec.json",
        "style_preset": args.style_preset,
        "style_tokens": style_tokens,
        "brand": brand or None,
        "site": site_profile or None,
        "beat_mode": args.beat_mode,
        "storyboard": storyboard,
        "assets": {},
        "senseaudio": {
            "voices": [],
            "image_tasks": [],
            "video_tasks": [],
            "transcripts": [],
        },
    }
    save_project_meta(project_dir, meta)
    write_asset_manifest(project_dir, {"project": project_dir.name, "assets": {}})
    register_asset(project_dir, "narration-script", "text", narration_path, "voiceover-script")
    register_asset(project_dir, "storyboard", "json", storyboard_path, "timeline")
    register_asset(project_dir, "style-preset", "json", style_path, "visual-style", {"preset": args.style_preset})
    register_asset(project_dir, "production-spec", "json", production_spec_path, "content-production-spec", {"scenes": len(production_spec.get("scenes", [])), "rhythm": production_spec.get("rhythm")})
    if brand:
        write_brand_file(project_dir, brand, "compose")
    if site_profile:
        write_site_profile_file(project_dir, site_profile, "compose")
        register_site_screenshot_assets(project_dir, site_profile.get("screenshots", []) if isinstance(site_profile.get("screenshots"), list) else [])
        site_asset_output = site_assets_path(project_dir)
        if site_asset_output.exists():
            site_asset_inventory = json.loads(site_asset_output.read_text(encoding="utf-8"))
            register_asset(project_dir, "site-assets", "json", site_asset_output, "website-asset-inventory", {"source_url": site_profile.get("source_url", ""), "counts": site_asset_inventory.get("counts", {})})
        if isinstance(site_profile.get("content_brief"), dict) and site_profile.get("content_brief"):
            content_brief_path = project_dir / "assets" / "content-brief.json"
            content_brief_path.write_text(json.dumps({"source": "compose", "content_brief": site_profile["content_brief"]}, ensure_ascii=False, indent=2), encoding="utf-8")
            register_asset(project_dir, "content-brief", "json", content_brief_path, "product-content-brief", {"points": len(site_profile["content_brief"].get("talking_points", []))})
        if isinstance(site_profile.get("visual_plan"), list) and site_profile.get("visual_plan"):
            visual_plan_path = project_dir / "assets" / "visual-plan.json"
            visual_plan_path.write_text(
                json.dumps({"source": "compose", "provider": "heuristic", "visual_plan": site_profile["visual_plan"]}, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            register_asset(project_dir, "visual-plan", "json", visual_plan_path, "visual-crop-plan", {"provider": "heuristic"})
        capture_quality_path = project_dir / "assets" / "site-capture-quality.json"
        if capture_quality_path.exists():
            capture_quality = json.loads(capture_quality_path.read_text(encoding="utf-8"))
            register_asset(project_dir, "site-capture-quality", "json", capture_quality_path, "website-capture-quality", {"ok": capture_quality.get("ok", True), "cookie_mode": capture_quality.get("cookie_mode", "clean")})
    if planned_beats:
        write_beats_file(project_dir, planned_beats, "compose")
    if llm_plan:
        register_asset(project_dir, "llm-plan", "json", llm_plan_path, "creative-plan")
    register_asset(project_dir, "captions", "captions", captions_path, "subtitle")
    if args.animation_preset != "none" or args.timeline_engine != "native":
        timeline_preset = args.animation_preset if args.animation_preset != "none" else "cinematic"
        write_timeline(project_dir, timeline_preset, storyboard, args.transition_preset, args.timeline_engine, planned_beats)
    if args.generate_images or args.generate_broll:
        command_generate_assets(
            argparse.Namespace(
                project=str(project_dir),
                images=args.generate_images,
                broll=args.generate_broll,
                image_prompt=args.image_prompt,
                video_prompt=args.video_prompt,
                image_id="hero-image",
                video_id="broll-video",
                image_model=DEFAULT_IMAGE_MODEL,
                image_size=args.image_size,
                video_model=DEFAULT_VIDEO_MODEL,
                video_duration=min(5, max(4, int(round(duration / 2)))),
                video_resolution="720p",
                video_ratio="16:9",
                poll=False,
                interval=8,
                timeout=1800,
                dry_run=args.asset_dry_run or args.offline,
            )
        )

    audio_path = project_dir / "assets" / "narration.mp3"
    transcript_path = project_dir / "assets" / "transcript.json"
    if not args.offline and args.voice_id:
        command_tts(
            argparse.Namespace(
                text=narration,
                text_file=None,
                voice_id=args.voice_id,
                model=args.tts_model,
                speed=args.speed,
                volume=1.0,
                pitch=0,
                latex_read=False,
                format="mp3",
                sample_rate=32000,
                bitrate=128000,
                channel=2,
                output=str(audio_path),
                manifest=str(project_dir / "assets" / "tts_manifest.json"),
                dry_run=False,
            )
        )
        register_asset(project_dir, "narration", "audio", audio_path, "voiceover")
        command_asr(
            argparse.Namespace(
                file=str(audio_path),
                model=args.asr_model,
                language=None,
                response_format="json",
                timestamps="word",
                enable_punctuation=True,
                normalize_words=True,
                output=str(transcript_path),
                dry_run=False,
            )
        )
        register_asset(project_dir, "transcript", "transcript", transcript_path, "subtitle-source")
        command_captions(
            argparse.Namespace(
                project=str(project_dir),
                transcript=str(transcript_path),
                output=str(captions_path),
                max_gap=0.35,
                max_chars=28,
                include_words=False,
                asset_id="captions",
            )
        )
    if args.render:
        command_render(
            argparse.Namespace(
                project=str(project_dir),
                output=str(project_dir / "renders" / f"{project_dir.name}.mp4"),
                fps=None,
                duration=None,
                width=None,
                height=None,
                audio=str(audio_path) if audio_path.exists() else None,
                virtual_time_budget=1000,
                capture_timeout=30.0,
                quiet=args.quiet,
                report=None,
                asset_id="final-video",
                frame_dir=None,
                keep_frames=False,
                resume=False,
                parallel=1,
                capture_mode="persistent",
            )
        )
    print(str(project_dir))


def timeline_effects(preset: str) -> list[str]:
    if preset == "kinetic":
        return ["slide-left", "zoom-in", "fade-up", "spotlight"]
    if preset == "product-tour":
        return ["spotlight", "fade-up", "slide-left", "zoom-in"]
    return ["fade-up", "parallax", "zoom-in", "spotlight"]


def set_timeline_runtime(
    project_dir: Path,
    transition_preset: str,
    transitions: list[dict[str, Any]],
    timeline_engine: str,
    gsap_plan: dict[str, Any] | None = None,
) -> None:
    index = project_dir / "index.html"
    if not index.exists():
        return
    markup = index.read_text(encoding="utf-8")
    if "data-transition-layer" in markup:
        markup = re.sub(r'data-transition-layer=["\'][^"\']*["\']', f'data-transition-layer="{transition_preset}"', markup, count=1)
    else:
        markup = markup.replace('class="transition-veil"', f'class="transition-veil" data-transition-layer="{transition_preset}"', 1)
    transition_json = json.dumps(transitions, ensure_ascii=False)
    markup = re.sub(r"var transitionPlan = \\[.*?\\];", f"var transitionPlan = {transition_json};", markup, count=1, flags=re.S)
    gsap_json = json.dumps(gsap_plan, ensure_ascii=False) if timeline_engine == "gsap-compat" and gsap_plan else "null"
    markup = re.sub(r"var gsapSpec = .*?;", f"var gsapSpec = {gsap_json};", markup, count=1, flags=re.S)
    index.write_text(markup, encoding="utf-8")


def write_timeline(
    project_dir: Path,
    preset: str,
    storyboard: list[dict[str, Any]] | None = None,
    transition_preset: str = "editorial",
    timeline_engine: str = "native",
    beats: list[dict[str, Any]] | None = None,
) -> Path:
    meta = read_project_meta(project_dir)
    items_source = storyboard or meta.get("storyboard") or storyboard_from_brief(str(meta.get("brief", "")), float(meta.get("duration", DEFAULT_RENDER_DURATION)))
    effects = timeline_effects(preset)
    transitions = build_transitions(items_source, transition_preset)
    timeline_beats = beats if beats is not None else read_project_beats(project_dir)
    gsap_plan = build_gsap_compat_plan(items_source, effects, timeline_beats) if timeline_engine == "gsap-compat" else {"labels": {}, "tracks": []}
    items: list[dict[str, Any]] = []
    for index, item in enumerate(items_source):
        start = float(item.get("start", 0))
        end = float(item.get("end", start + 1))
        items.append(
            {
                "id": str(item.get("id", f"scene-{index + 1}")),
                "start": start,
                "end": end,
                "effect": effects[index % len(effects)],
                "intent": item.get("intent", ""),
            }
        )
    payload = {
        "preset": preset,
        "engine": timeline_engine,
        "transition_preset": transition_preset,
        "items": items,
        "transitions": transitions,
        "beats": timeline_beats,
        "labels": gsap_plan["labels"],
        "tracks": gsap_plan["tracks"],
    }
    output = project_dir / "assets" / "timeline.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    set_timeline_source(project_dir)
    set_timeline_runtime(project_dir, transition_preset, transitions, timeline_engine, gsap_plan)
    register_asset(project_dir, "timeline", "json", output, "animation-timeline", {"preset": preset, "engine": timeline_engine})
    return output


def command_timeline(args: argparse.Namespace) -> None:
    project_dir = Path(args.project)
    output = write_timeline(project_dir, args.preset, transition_preset=args.transition_preset, timeline_engine=args.timeline_engine)
    print(str(output))


def find_asset_by_type_or_id(project_dir: Path, asset_id: str, asset_type: str) -> dict[str, Any] | None:
    manifest = read_asset_manifest(project_dir)
    assets = manifest.get("assets", {})
    if asset_id in assets:
        return assets[asset_id]
    for item in assets.values():
        if item.get("type") == asset_type:
            return item
    return None


def registered_asset_path(project_dir: Path, asset_id: str, asset_type: str) -> Path | None:
    asset = find_asset_by_type_or_id(project_dir, asset_id, asset_type)
    if not asset:
        return None
    path = project_dir / str(asset.get("path", ""))
    return path if path.exists() else None


def command_build(args: argparse.Namespace) -> None:
    project_dir = Path(args.project).resolve()
    output = Path(args.output) if args.output else project_dir / "renders" / f"{project_dir.name}.mp4"
    caption_path = project_dir / "assets" / "captions.json"
    transcript = find_asset_by_type_or_id(project_dir, "transcript", "transcript")
    audio, _audio_was_auto = default_render_audio(project_dir, None)
    steps: list[dict[str, Any]] = [{"name": "lint", "command": "lint"}]
    if transcript and not caption_path.exists():
        steps.append(
            {
                "name": "captions",
                "command": "captions",
                "transcript": transcript["path"],
                "output": relative_to_project(project_dir, caption_path),
            }
        )
    steps.append(
        {
            "name": "render",
            "command": "render",
            "output": relative_to_project(project_dir, output),
            "audio": relative_to_project(project_dir, Path(audio)) if audio else None,
        }
    )
    plan = {
        "project": str(project_dir),
        "steps": steps,
        "audio": relative_to_project(project_dir, Path(audio)) if audio else None,
        "output": relative_to_project(project_dir, output),
    }
    if args.dry_run:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return

    command_lint(argparse.Namespace(project=str(project_dir), json=args.json, strict=True))
    if transcript and not caption_path.exists():
        command_captions(
            argparse.Namespace(
                project=str(project_dir),
                transcript=str(project_dir / transcript["path"]),
                output=str(caption_path),
                max_gap=0.35,
                max_chars=28,
                include_words=False,
                asset_id="captions",
            )
        )
    command_render(
        argparse.Namespace(
            project=str(project_dir),
            output=str(output),
            fps=args.fps,
            duration=args.duration,
            width=args.width,
            height=args.height,
            audio=audio,
            virtual_time_budget=args.virtual_time_budget,
            capture_timeout=args.capture_timeout,
            quiet=args.quiet,
            report=args.report,
            asset_id=args.asset_id,
            frame_dir=args.frame_dir,
            keep_frames=args.keep_frames,
            resume=args.resume,
            parallel=args.parallel,
            capture_mode=args.capture_mode,
        )
    )


def command_asset_add(args: argparse.Namespace) -> None:
    project_dir = Path(args.project).resolve()
    path = Path(args.path)
    if not path.exists():
        raise SenseAudioError(f"Asset not found: {path}")
    item = register_asset(project_dir, args.id, args.type, path, args.role, {"label": args.label} if args.label else None)
    update_asset_html(project_dir)
    print(json.dumps(item, ensure_ascii=False, indent=2))


def build_procedural_music_command(ffmpeg: str, output: Path, duration: float) -> list[str]:
    duration = max(1.0, float(duration))
    fade_out_start = max(0.0, duration - 1.4)
    filter_graph = (
        "[0:a]volume=0.080[a0];"
        "[1:a]volume=0.055[a1];"
        "[2:a]volume=0.040[a2];"
        "[3:a]volume=0.018,highpass=f=650,lowpass=f=4200[n];"
        f"[a0][a1][a2][n]amix=inputs=4:duration=longest:normalize=0,"
        f"afade=t=in:st=0:d=0.9,afade=t=out:st={fade_out_start:.3f}:d=1.4[a]"
    )
    return [
        ffmpeg,
        "-y",
        "-f",
        "lavfi",
        "-i",
        f"sine=frequency=220:sample_rate=44100:duration={duration:.3f}",
        "-f",
        "lavfi",
        "-i",
        f"sine=frequency=277.18:sample_rate=44100:duration={duration:.3f}",
        "-f",
        "lavfi",
        "-i",
        f"sine=frequency=329.63:sample_rate=44100:duration={duration:.3f}",
        "-f",
        "lavfi",
        "-i",
        f"anoisesrc=color=pink:sample_rate=44100:duration={duration:.3f}",
        "-filter_complex",
        filter_graph,
        "-map",
        "[a]",
        "-c:a",
        "libmp3lame",
        "-b:a",
        "160k",
        str(output),
    ]


def generate_procedural_music_bed(project_dir: Path, output: Path, duration: float, asset_id: str = "background-music") -> Path:
    ffmpeg = find_ffmpeg()
    output.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(build_procedural_music_command(ffmpeg, output, duration), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    register_asset(
        project_dir,
        asset_id,
        "audio",
        output,
        "background-music",
        {"source": "procedural-music-fallback", "duration": float(duration)},
    )
    return output


def build_mix_audio_command(ffmpeg: str, voice: Path | None, music: Path | None, output: Path, duration: float, music_volume: float) -> list[str]:
    if not voice and not music:
        raise SenseAudioError("Provide --voice, --music, or both.")
    fade_out_start = max(0.0, duration - 1.2)
    command = [ffmpeg, "-y"]
    if voice:
        command += ["-i", str(voice)]
    if music:
        command += ["-i", str(music)]
    if voice and music:
        filter_graph = (
            f"[0:a]apad=pad_dur={duration:.3f},atrim=0:{duration:.3f},asetpts=N/SR/TB[v];"
            f"[1:a]volume={music_volume:.2f},apad=pad_dur={duration:.3f},atrim=0:{duration:.3f},"
            f"afade=t=in:st=0:d=0.6,afade=t=out:st={fade_out_start:.3f}:d=1.2,asetpts=N/SR/TB[m];"
            "[v][m]amix=inputs=2:duration=longest:dropout_transition=1:normalize=0[a]"
        )
    elif music:
        filter_graph = (
            f"[0:a]volume={music_volume:.2f},apad=pad_dur={duration:.3f},atrim=0:{duration:.3f},"
            f"afade=t=in:st=0:d=0.6,afade=t=out:st={fade_out_start:.3f}:d=1.2,asetpts=N/SR/TB[a]"
        )
    else:
        filter_graph = f"[0:a]apad=pad_dur={duration:.3f},atrim=0:{duration:.3f},asetpts=N/SR/TB[a]"
    command += ["-filter_complex", filter_graph, "-map", "[a]", "-c:a", "aac", "-b:a", "192k", str(output)]
    return command


def command_mix_audio(args: argparse.Namespace) -> None:
    project_dir = Path(args.project).resolve() if args.project else None
    voice = Path(args.voice).resolve() if args.voice else None
    music = Path(args.music).resolve() if args.music else None
    if voice and not args.dry_run and not voice.exists():
        raise SenseAudioError(f"Voice audio not found: {voice}")
    if music and not args.dry_run and not music.exists():
        raise SenseAudioError(f"Music audio not found: {music}")
    output = Path(args.output).resolve()
    duration = float(args.duration)
    ffmpeg = find_ffmpeg()
    ffmpeg_cmd = build_mix_audio_command(ffmpeg, voice, music, output, duration, float(args.music_volume))
    payload = {
        "project": str(project_dir) if project_dir else None,
        "voice": str(voice) if voice else None,
        "music": str(music) if music else None,
        "output": str(output),
        "duration": duration,
        "music_volume": float(args.music_volume),
        "ffmpeg": ffmpeg_cmd,
    }
    if args.dry_run:
        payload["dry_run"] = True
        if args.json:
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            print(" ".join(ffmpeg_cmd))
        return
    output.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(ffmpeg_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    if project_dir:
        register_asset(
            project_dir,
            args.asset_id,
            "audio",
            output,
            "final-mix",
            {
                "voice": relative_to_project(project_dir, voice) if voice else None,
                "music": relative_to_project(project_dir, music) if music else None,
                "music_volume": float(args.music_volume),
                "duration": duration,
            },
        )
    if args.json:
        payload["dry_run"] = False
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(str(output))


def html_attrs(markup: str) -> list[dict[str, str]]:
    tags = re.findall(r"<[^>]+>", markup)
    parsed: list[dict[str, str]] = []
    for tag in tags:
        attrs = dict(re.findall(r'([a-zA-Z_:][-a-zA-Z0-9_:.]*)\s*=\s*["\']([^"\']*)["\']', tag))
        if attrs:
            parsed.append(attrs)
    return parsed


def command_lint(args: argparse.Namespace) -> None:
    project_dir = Path(args.project).resolve()
    issues: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    meta: dict[str, Any] = {}
    try:
        meta = read_project_meta(project_dir)
    except SenseAudioError as exc:
        issues.append({"code": "project_meta", "message": str(exc)})
    entry = str(meta.get("entry", "index.html"))
    entry_path = project_dir / entry
    runtime_path = project_dir / "senseframe-runtime.js"
    if not entry_path.exists():
        issues.append({"code": "missing_entry", "message": f"Entry file missing: {entry}"})
        markup = ""
    else:
        markup = entry_path.read_text(encoding="utf-8")
    if not runtime_path.exists():
        issues.append({"code": "missing_runtime", "message": "senseframe-runtime.js is missing"})
    if markup and "data-composition-id" not in markup:
        warnings.append({"code": "composition_root", "message": "No data-composition-id found in entry HTML"})
    if markup and "window.renderFrame" not in markup:
        warnings.append({"code": "render_frame", "message": "No window.renderFrame(time) hook found"})

    duration = float(meta.get("duration", DEFAULT_RENDER_DURATION)) if meta else DEFAULT_RENDER_DURATION
    scenes = 0
    captions = 0
    for attrs in html_attrs(markup):
        if "data-scene" in attrs:
            scenes += 1
        if "data-caption-source" in attrs:
            captions += 1
            source = attrs["data-caption-source"]
            if source and not source.startswith(("http://", "https://", "data:")):
                source_path = (project_dir / source).resolve()
                if not source_path.exists():
                    issues.append({"code": "missing_caption_source", "message": f"Caption source not found: {source}"})
        if "data-start" in attrs:
            try:
                start = float(attrs.get("data-start", "0"))
                clip_duration = float(attrs.get("data-duration", "0") or "0")
                if start < 0:
                    issues.append({"code": "negative_start", "message": f"Clip starts before zero: {start}"})
                if clip_duration < 0:
                    issues.append({"code": "negative_duration", "message": f"Clip has negative duration: {clip_duration}"})
                if clip_duration and start + clip_duration > duration + 0.01:
                    warnings.append(
                        {
                            "code": "clip_overflow",
                            "message": f"Clip ends after project duration: {start + clip_duration:.2f}s > {duration:.2f}s",
                        }
                    )
            except ValueError:
                issues.append({"code": "bad_timing", "message": f"Invalid timing attributes: {attrs}"})

    manifest = read_asset_manifest(project_dir)
    asset_rows: list[dict[str, Any]] = []
    has_audio_asset = False
    for asset_id, item in manifest.get("assets", {}).items():
        asset_path = project_dir / str(item.get("path", ""))
        exists = asset_path.exists()
        if not exists:
            issues.append({"code": "missing_asset", "message": f"Asset missing: {asset_id} -> {item.get('path')}"})
        if item.get("type") == "audio" and exists:
            has_audio_asset = True
        asset_rows.append({"id": asset_id, "path": item.get("path"), "exists": exists})
    if (project_dir / "assets" / "narration.txt").exists() and not has_audio_asset:
        warnings.append(
            {
                "code": "missing_audio_track",
                "message": "Narration text exists but no audio asset is registered; render will be silent unless --audio is provided.",
            }
        )

    payload = {
        "ok": not issues,
        "project": str(project_dir),
        "entry": entry,
        "duration": duration,
        "stats": {"scenes": scenes, "caption_sources": captions, "assets": len(asset_rows)},
        "issues": issues,
        "warnings": warnings,
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print("ok" if payload["ok"] else "issues")
        for issue in issues:
            print(f"error [{issue['code']}]: {issue['message']}")
        for warning in warnings:
            print(f"warn  [{warning['code']}]: {warning['message']}")
    if args.strict and issues:
        raise SenseAudioError("Project lint failed.")


def format_srt_time(seconds: float) -> str:
    millis = int(round(seconds * 1000))
    hours, rem = divmod(millis, 3600_000)
    minutes, rem = divmod(rem, 60_000)
    secs, ms = divmod(rem, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{ms:03d}"


def format_vtt_time(seconds: float) -> str:
    return format_srt_time(seconds).replace(",", ".")


def command_captions_export(args: argparse.Namespace) -> None:
    captions_path = Path(args.captions)
    if not captions_path.exists():
        raise SenseAudioError(f"Captions file not found: {captions_path}")
    data = json.loads(captions_path.read_text(encoding="utf-8"))
    captions = data if isinstance(data, list) else data.get("captions", [])
    if args.format == "srt":
        blocks = []
        for index, item in enumerate(captions, start=1):
            blocks.append(
                f"{index}\n{format_srt_time(float(item['start']))} --> {format_srt_time(float(item['end']))}\n{item['text']}"
            )
        content = "\n\n".join(blocks) + ("\n" if blocks else "")
    else:
        blocks = ["WEBVTT\n"]
        for item in captions:
            blocks.append(
                f"{format_vtt_time(float(item['start']))} --> {format_vtt_time(float(item['end']))}\n{item['text']}"
            )
        content = "\n\n".join(blocks) + ("\n" if len(blocks) > 1 else "")
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content, encoding="utf-8")
    print(str(output))


def command_asset_report(args: argparse.Namespace) -> None:
    project_dir = Path(args.project).resolve()
    manifest = read_asset_manifest(project_dir)
    rows: list[dict[str, Any]] = []
    for asset_id, item in sorted(manifest.get("assets", {}).items()):
        path = str(item.get("path", ""))
        full_path = project_dir / path if path else None
        exists = bool(full_path and full_path.exists())
        rows.append(
            {
                "id": asset_id,
                "type": item.get("type", "other"),
                "role": item.get("role"),
                "status": item.get("status", "ready" if path else "planned"),
                "path": path,
                "exists": exists,
                "size": full_path.stat().st_size if full_path and full_path.exists() and full_path.is_file() else None,
            }
        )
    payload = {"project": str(project_dir), "count": len(rows), "assets": rows}
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    for row in rows:
        status = "ok" if row["exists"] else "missing"
        print(f"{status}\t{row['id']}\t{row['type']}\t{row['path']}")


def command_audio_data(args: argparse.Namespace) -> None:
    project_dir = Path(args.project).resolve() if args.project else None
    audio_path = Path(args.audio)
    output = Path(args.output)
    payload = {
        "audio": str(audio_path),
        "output": str(output),
        "fps": args.fps,
        "bands": args.bands,
        "duration": args.duration,
    }
    if args.dry_run:
        output.parent.mkdir(parents=True, exist_ok=True)
        sample = {
            "source": audio_path.name,
            "fps": args.fps,
            "bands": args.bands,
            "totalFrames": max(1, int(round((args.duration or 1.0) * args.fps))),
            "duration": args.duration or 1.0,
            "frames": [{"rms": 0, "bands": [0 for _ in range(args.bands)]}],
            "dry_run": True,
        }
        output.write_text(json.dumps(sample, ensure_ascii=False, indent=2), encoding="utf-8")
        if project_dir:
            register_asset(project_dir, args.asset_id, "json", output, "audio-reactive-data", {"dry_run": True})
            set_audio_source(project_dir, "./" + relative_to_project(project_dir, output))
        print(json.dumps({"dry_run": True, "payload": payload}, ensure_ascii=False, indent=2))
        return
    if not audio_path.exists():
        raise SenseAudioError(f"Audio file not found: {audio_path}")
    data = audio_data_payload(audio_path, args.fps, args.bands, args.duration)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    if project_dir:
        register_asset(
            project_dir,
            args.asset_id,
            "json",
            output,
            "audio-reactive-data",
            {"source": relative_to_project(project_dir, audio_path), "fps": args.fps, "bands": args.bands},
        )
        set_audio_source(project_dir, "./" + relative_to_project(project_dir, output))
    print(str(output))


def command_motion_audit(args: argparse.Namespace) -> None:
    project_dir = Path(args.project).resolve()
    meta = read_project_meta(project_dir)
    entry = str(meta.get("entry", "index.html"))
    entry_path = project_dir / entry
    if not entry_path.exists():
        raise SenseAudioError(f"Entry file missing: {entry}")
    markup = entry_path.read_text(encoding="utf-8")
    storyboard = meta.get("storyboard") or []
    storyboard_ids = [safe_scene_id(item.get("id"), scene_index) for scene_index, item in enumerate(storyboard)]
    dom_scenes = re.findall(r'data-scene=["\']([^"\']+)["\']', markup)
    beat_count = len(read_project_beats(project_dir))
    timeline_path = project_dir / "assets" / "timeline.json"
    timeline_items: list[dict[str, Any]] = []
    timeline_engine = "native"
    if timeline_path.exists():
        timeline_payload = json.loads(timeline_path.read_text(encoding="utf-8"))
        timeline_items = list(timeline_payload.get("items", []))
        timeline_engine = str(timeline_payload.get("engine", "native"))
    timeline_ids = [safe_scene_id(item.get("id"), item_index) for item_index, item in enumerate(timeline_items)]

    missing_dom = [scene_id for scene_id in storyboard_ids if scene_id not in dom_scenes]
    missing_timeline = [scene_id for scene_id in storyboard_ids if timeline_items and scene_id not in timeline_ids]
    fixed_template_markers = [
        "HTML 控制画面：像写网页一样写视频",
        'data-scene="intro"',
        'data-scene="media"',
        'data-scene="render"',
    ]
    issues: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    if missing_dom:
        issues.append({"code": "storyboard_scene_missing", "message": f"Storyboard scenes missing in DOM: {', '.join(missing_dom)}"})
    if missing_timeline:
        issues.append({"code": "timeline_scene_missing", "message": f"Storyboard scenes missing in timeline: {', '.join(missing_timeline)}"})
    if "window.__timelines" not in markup:
        issues.append({"code": "timeline_registry_missing", "message": "No window.__timelines registry found."})
    if not re.search(r'window\.__timelines\["main"\]', markup):
        issues.append({"code": "main_timeline_missing", "message": "No main seekable timeline registered."})
    if timeline_engine == "gsap-compat" and ("createGsapCompatTimeline" not in markup or "window.__senseframes.gsapCompat" not in markup):
        issues.append({"code": "gsap_compat_runtime_missing", "message": "Timeline requests gsap-compat but local adapter is missing from HTML."})
    if any(marker in markup for marker in fixed_template_markers):
        warnings.append({"code": "fixed_template_marker", "message": "Legacy fixed three-beat template marker found."})
    if markup.count("story-scene") < len(storyboard_ids):
        warnings.append({"code": "low_scene_density", "message": "Story scene layer count is lower than storyboard scene count."})
    if beat_count and "data-beat" not in markup:
        issues.append({"code": "beat_layers_missing", "message": "beats.json exists but no data-beat layers were found in the DOM."})

    checks = {
        "timeline_registry": "window.__timelines" in markup and bool(re.search(r'window\.__timelines\["main"\]', markup)),
        "storyboard_scene_binding": not missing_dom and bool(storyboard_ids),
        "timeline_scene_binding": not missing_timeline if timeline_items else True,
        "mid_scene_activity": "waveform" in markup and "kinetic-chip" in markup and "sceneProgress" in markup,
        "transition_layer": "transition-veil" in markup and "transitionAmount" in markup,
        "audio_reactive": "audioReactive" in markup,
        "gsap_compat": timeline_engine != "gsap-compat" or ("createGsapCompatTimeline" in markup and "window.__senseframes.gsapCompat" in markup),
        "beat_layers": not beat_count or ("data-beat" in markup and "beat-layer" in markup),
        "legacy_fixed_template_absent": not any(marker in markup for marker in fixed_template_markers),
    }
    payload = {
        "ok": not issues,
        "project": str(project_dir),
        "entry": entry,
        "checks": checks,
        "stats": {
            "storyboard_scenes": len(storyboard_ids),
            "dom_scenes": len(set(dom_scenes)),
            "timeline_items": len(timeline_items),
            "beats": beat_count,
            "story_scene_layers": markup.count("story-scene"),
        },
        "issues": issues,
        "warnings": warnings,
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print("ok" if payload["ok"] else "issues")
        for check_name, passed in checks.items():
            print(f"{'ok' if passed else 'warn'}\t{check_name}")
        for issue in issues:
            print(f"error [{issue['code']}]: {issue['message']}")
        for warning in warnings:
            print(f"warn  [{warning['code']}]: {warning['message']}")
    if args.strict and issues:
        raise SenseAudioError("Motion audit failed.")


def scene_bounds_from_storyboard(storyboard: list[dict[str, Any]], duration: float) -> list[dict[str, Any]]:
    scenes: list[dict[str, Any]] = []
    for scene_index, item in enumerate(storyboard):
        start = max(0.0, float(item.get("start", 0.0)))
        end = float(item.get("end", start + max(0.1, duration / max(1, len(storyboard)))))
        end = min(duration, max(start + 0.1, end))
        scenes.append(
            {
                "scene_id": safe_scene_id(item.get("id"), scene_index),
                "start": start,
                "end": end,
                "duration": round(end - start, 3),
                "intent": item.get("intent", ""),
            }
        )
    return sorted(scenes, key=lambda scene: scene["start"])


def active_scene_at(scenes: list[dict[str, Any]], time_value: float) -> dict[str, Any] | None:
    for scene in scenes:
        if float(scene["start"]) <= time_value < float(scene["end"]):
            return scene
    if scenes and math.isclose(time_value, float(scenes[-1]["end"]), abs_tol=0.01):
        return scenes[-1]
    return None


def active_beat_at(beats: list[dict[str, Any]], time_value: float) -> dict[str, Any] | None:
    for beat in beats:
        start = float(beat.get("start", 0))
        end = float(beat.get("end", start + float(beat.get("duration", 0.1))))
        if start <= time_value < end:
            return beat
    if beats:
        last = beats[-1]
        end = float(last.get("end", float(last.get("start", 0)) + float(last.get("duration", 0.1))))
        if math.isclose(time_value, end, abs_tol=0.01):
            return last
    return None


def read_project_timeline(project_dir: Path) -> dict[str, Any]:
    timeline_path = project_dir / "assets" / "timeline.json"
    if not timeline_path.exists():
        return {"items": []}
    return json.loads(timeline_path.read_text(encoding="utf-8"))


def resolve_project_source(project_dir: Path, source: str) -> Path:
    cleaned = source.replace("\\", "/").lstrip("./")
    return (project_dir / cleaned).resolve()


def audio_data_summary(project_dir: Path, markup: str) -> dict[str, Any]:
    source_match = re.search(r'data-audio-source=["\']([^"\']+)["\']', markup)
    source = source_match.group(1) if source_match else ""
    path = resolve_project_source(project_dir, source) if source else None
    if not path or not path.exists():
        return {"bound": bool(source), "exists": False, "frames": 0, "max_rms": 0.0, "smooth_delta_max": 0.0}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"bound": True, "exists": False, "frames": 0, "max_rms": 0.0, "smooth_delta_max": 0.0}
    frames = payload.get("frames") or []
    rms_values = [float(frame.get("rms", 0.0)) for frame in frames if isinstance(frame, dict)]
    deltas = [abs(rms_values[index] - rms_values[index - 1]) for index in range(1, len(rms_values))]
    return {
        "bound": True,
        "exists": True,
        "frames": len(frames),
        "max_rms": round(max(rms_values) if rms_values else 0.0, 4),
        "smooth_delta_max": round(max(deltas) if deltas else 0.0, 4),
    }


def command_motion_map(args: argparse.Namespace) -> None:
    project_dir = Path(args.project).resolve()
    meta = read_project_meta(project_dir)
    duration = float(meta.get("duration", DEFAULT_RENDER_DURATION))
    entry = str(meta.get("entry", "index.html"))
    entry_path = project_dir / entry
    if not entry_path.exists():
        raise SenseAudioError(f"Entry file missing: {entry}")

    markup = entry_path.read_text(encoding="utf-8")
    storyboard = meta.get("storyboard") or []
    scenes = scene_bounds_from_storyboard(storyboard, duration)
    beats = read_project_beats(project_dir)
    timeline_payload = read_project_timeline(project_dir)
    timeline_items = list(timeline_payload.get("items", []))
    timeline_by_id = {safe_scene_id(item.get("id"), index): item for index, item in enumerate(timeline_items)}
    scene_boundaries = [float(scene["start"]) for scene in scenes[1:]]
    samples_count = max(2, int(args.samples))
    has_mid_scene_layers = all(marker in markup for marker in ("waveform", "kinetic-chip", "sceneProgress"))
    has_beat_layers = "data-beat" in markup and "beat-layer" in markup
    has_transition_layer = "transition-veil" in markup and "transitionAmount" in markup
    has_audio_hooks = "audioReactive" in markup
    audio_summary = audio_data_summary(project_dir, markup)

    samples: list[dict[str, Any]] = []
    coverage: dict[str, int] = {str(scene["scene_id"]): 0 for scene in scenes}
    beat_hits: dict[str, int] = {str(beat.get("id", "")): 0 for beat in beats}
    for sample_index in range(samples_count):
        time_value = duration * (sample_index + 0.5) / samples_count
        scene = active_scene_at(scenes, time_value)
        beat = active_beat_at(beats, time_value)
        score = 0.0
        reasons: list[str] = []
        scene_id = ""
        beat_id = ""
        scene_progress = 0.0
        if scene:
            scene_id = str(scene["scene_id"])
            coverage[scene_id] += 1
            scene_duration = max(0.001, float(scene["end"]) - float(scene["start"]))
            scene_progress = min(1.0, max(0.0, (time_value - float(scene["start"])) / scene_duration))
            enter = max(0.0, 1.0 - scene_progress / 0.3)
            exit_value = max(0.0, 1.0 - (1.0 - scene_progress) / 0.25)
            mid_motion = math.sin(scene_progress * math.pi)
            score += 1.0
            reasons.append("active-scene")
            if has_mid_scene_layers:
                score += 0.35 + 0.45 * mid_motion
                reasons.append("mid-scene-layers")
            if timeline_by_id.get(scene_id):
                score += 0.45
                reasons.append(str(timeline_by_id[scene_id].get("effect", "timeline-effect")))
            if enter > 0.05:
                score += enter * 0.75
                reasons.append("entrance")
            if exit_value > 0.05:
                score += exit_value * 0.65
                reasons.append("exit")
        if beat:
            beat_id = str(beat.get("id", ""))
            if beat_id in beat_hits:
                beat_hits[beat_id] += 1
            if has_beat_layers:
                score += 0.32
                reasons.append("beat-layer")
        if has_transition_layer and any(abs(time_value - boundary) <= 0.42 for boundary in scene_boundaries):
            score += 0.75
            reasons.append("transition")
        if has_audio_hooks:
            score += 0.25
            reasons.append("audio-hooks")
        if audio_summary["exists"] and audio_summary["max_rms"]:
            score += min(0.55, float(audio_summary["max_rms"]) * 0.55)
            reasons.append("audio-data")
        samples.append(
            {
                "time": round(time_value, 3),
                "score": round(score, 3),
                "scene_id": scene_id,
                "beat_id": beat_id,
                "scene_progress": round(scene_progress, 3),
                "signals": reasons,
            }
        )

    low_threshold = float(args.low_threshold)
    dead_zones: list[dict[str, Any]] = []
    current: list[dict[str, Any]] = []
    for sample in samples:
        if float(sample["score"]) < low_threshold:
            current.append(sample)
            continue
        if current:
            zone_duration = float(current[-1]["time"]) - float(current[0]["time"]) + duration / samples_count
            if zone_duration >= float(args.min_dead_zone):
                dead_zones.append({"start": current[0]["time"], "end": current[-1]["time"], "duration": round(zone_duration, 3)})
            current = []
    if current:
        zone_duration = float(current[-1]["time"]) - float(current[0]["time"]) + duration / samples_count
        if zone_duration >= float(args.min_dead_zone):
            dead_zones.append({"start": current[0]["time"], "end": current[-1]["time"], "duration": round(zone_duration, 3)})

    scene_coverage = []
    for scene in scenes:
        sample_hits = coverage.get(str(scene["scene_id"]), 0)
        scene_coverage.append(
            {
                "scene_id": scene["scene_id"],
                "start": round(float(scene["start"]), 3),
                "end": round(float(scene["end"]), 3),
                "duration": scene["duration"],
                "samples": sample_hits,
                "coverage_ratio": round(sample_hits / samples_count, 3),
                "effect": (timeline_by_id.get(str(scene["scene_id"])) or {}).get("effect", ""),
            }
        )

    scores = [float(sample["score"]) for sample in samples]
    sampled_beats = [beat_id for beat_id, hits in beat_hits.items() if beat_id and hits > 0]
    beat_durations = [max(0.0, float(beat.get("duration", 0.0))) for beat in beats]
    short_beats = [value for value in beat_durations if value and value < MIN_READABLE_BEAT_DURATION]
    beat_rate = len(beats) / duration if duration > 0 else 0.0
    transition_count = len(timeline_payload.get("transitions", [])) if isinstance(timeline_payload.get("transitions"), list) else len(scene_boundaries)
    transition_rate = transition_count / duration if duration > 0 else 0.0
    short_beat_ratio = len(short_beats) / len(beat_durations) if beat_durations else 0.0
    transition_rate_limit = 0.45 if beats else 0.75
    flashiness = {
        "beat_rate_per_second": round(beat_rate, 3),
        "transition_rate_per_second": round(transition_rate, 3),
        "average_beat_duration": round(sum(beat_durations) / len(beat_durations), 3) if beat_durations else 0.0,
        "min_beat_duration": round(min(beat_durations), 3) if beat_durations else 0.0,
        "short_beat_ratio": round(short_beat_ratio, 3),
        "transition_rate_limit": transition_rate_limit,
        "comfortable": beat_rate <= MAX_COMFORTABLE_BEAT_RATE and short_beat_ratio <= 0.35 and transition_rate <= transition_rate_limit,
    }
    beat_coverage = {
        "total": len(beats),
        "sampled": len(sampled_beats),
        "ratio": round(len(sampled_beats) / len(beats), 3) if beats else 1.0,
        "has_layers": has_beat_layers,
    }
    recommendations: list[str] = []
    if dead_zones:
        recommendations.append("Shorten low-motion plateaus with a micro-reveal, focus sweep, or caption emphasis.")
    if not has_transition_layer:
        recommendations.append("Add a transition veil or boundary wipe so scene changes feel authored.")
    if not has_mid_scene_layers:
        recommendations.append("Add waveform, chip, and sceneProgress layers to avoid static mid-scene holds.")
    if beats and not has_beat_layers:
        recommendations.append("Bind generated beats to .beat-layer elements so scene interiors have authored motion.")
    if beats and beat_coverage["ratio"] < 0.65:
        recommendations.append("Increase motion-map samples or rebalance short beats so each internal beat is visible.")
    if not flashiness["comfortable"]:
        recommendations.append("Reduce beats per scene, lengthen beat holds, or switch to glass/editorial transitions to avoid rapid flashing.")
    if has_audio_hooks and not audio_summary["exists"]:
        recommendations.append("Run audio-data after TTS to make local accents react to real narration energy.")
    if len({item.get("effect") for item in timeline_items}) <= 1 and len(timeline_items) > 1:
        recommendations.append("Vary timeline effects across scenes for stronger editorial rhythm.")
    if not recommendations:
        recommendations.append("Motion coverage is healthy; tune copy timing and asset quality before adding complexity.")

    checks = {
        "scene_coverage": bool(scenes) and all(item["samples"] > 0 for item in scene_coverage),
        "timeline_coverage": bool(timeline_items) and all(item["effect"] for item in scene_coverage),
        "transition_coverage": has_transition_layer,
        "mid_scene_activity": has_mid_scene_layers,
        "beat_coverage": not beats or (has_beat_layers and beat_coverage["ratio"] >= 0.65),
        "comfortable_pacing": flashiness["comfortable"],
        "audio_reactive_bound": has_audio_hooks,
        "no_long_dead_zones": not dead_zones,
        "density_floor": bool(scores) and min(scores) >= low_threshold,
    }
    issues: list[dict[str, Any]] = []
    if not scenes:
        issues.append({"code": "storyboard_missing", "message": "No storyboard scenes found for motion mapping."})
    if not checks["scene_coverage"]:
        issues.append({"code": "scene_coverage_gap", "message": "At least one scene is not represented in sampled motion coverage."})
    if not checks["beat_coverage"]:
        issues.append({"code": "beat_coverage_gap", "message": "Beat layers exist but sampled coverage is too low or DOM beat layers are missing."})
    if not checks["comfortable_pacing"]:
        issues.append({"code": "flashiness_risk", "message": "Beat or transition rate is high enough to feel visually jumpy."})
    if dead_zones:
        issues.append({"code": "long_dead_zone", "message": "Motion map found low-density spans longer than the configured threshold."})

    payload = {
        "ok": not issues,
        "project": str(project_dir),
        "entry": entry,
        "duration": duration,
        "density": {
            "samples": samples_count,
            "min": round(min(scores) if scores else 0.0, 3),
            "max": round(max(scores) if scores else 0.0, 3),
            "average": round(sum(scores) / len(scores), 3) if scores else 0.0,
            "low_threshold": low_threshold,
        },
        "checks": checks,
        "scene_coverage": scene_coverage,
        "beat_coverage": beat_coverage,
        "flashiness": flashiness,
        "dead_zones": dead_zones,
        "audio": audio_summary,
        "samples": samples,
        "recommendations": recommendations,
        "issues": issues,
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print("ok" if payload["ok"] else "issues")
        print(f"density\tavg={payload['density']['average']}\tmin={payload['density']['min']}\tmax={payload['density']['max']}")
        for item in scene_coverage:
            print(f"scene\t{item['scene_id']}\tsamples={item['samples']}\teffect={item['effect']}")
        for zone in dead_zones:
            print(f"dead-zone\t{zone['start']}s-{zone['end']}s\t{zone['duration']}s")
        for recommendation in recommendations:
            print(f"tip\t{recommendation}")
    if args.strict and issues:
        raise SenseAudioError("Motion map failed.")


def command_preview(args: argparse.Namespace) -> None:
    project_dir = Path(args.project).resolve()
    meta = read_project_meta(project_dir)
    port = args.port or find_free_port()
    server, _thread = start_static_server(project_dir, port)
    entry = meta.get("entry", "index.html")
    url = f"http://127.0.0.1:{port}/{entry}"
    print(url)
    try:
        if args.once:
            return
        print("Press Ctrl+C to stop.", file=sys.stderr)
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        server.shutdown()
        server.server_close()


def screenshot_frame(
    chrome: str,
    url: str,
    output: Path,
    width: int,
    height: int,
    virtual_time_budget: int,
    capture_timeout: float = 30.0,
) -> None:
    with tempfile.TemporaryDirectory(prefix="senseframe-chrome-profile-") as profile_dir:
        cmd = [
            chrome,
            "--headless=new",
            "--disable-gpu",
            "--disable-background-networking",
            "--disable-extensions",
            "--disable-sync",
            "--disable-dev-shm-usage",
            "--no-first-run",
            "--no-default-browser-check",
            "--hide-scrollbars",
            "--mute-audio",
            f"--user-data-dir={profile_dir}",
            f"--window-size={width},{height}",
            f"--screenshot={output}",
            f"--virtual-time-budget={virtual_time_budget}",
            url,
        ]
        process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
        deadline = time.time() + max(2.0, capture_timeout)
        last_size = -1
        stable_ticks = 0

        def stop_process() -> None:
            if process.poll() is not None:
                return
            try:
                os.killpg(process.pid, signal.SIGTERM)
                process.wait(timeout=1.5)
            except Exception:
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except Exception:
                    process.kill()
                try:
                    process.wait(timeout=2)
                except Exception:
                    pass

        try:
            while time.time() < deadline:
                return_code = process.poll()
                if return_code is not None:
                    if return_code != 0:
                        raise subprocess.CalledProcessError(return_code, cmd)
                    if output.exists() and output.stat().st_size > 0:
                        return
                    raise SenseAudioError(f"Chrome did not write screenshot: {output}")
                if output.exists():
                    size = output.stat().st_size
                    if size > 0 and size == last_size:
                        stable_ticks += 1
                    else:
                        stable_ticks = 0
                        last_size = size
                    if stable_ticks >= 2:
                        stop_process()
                        return
                time.sleep(0.1)
            stop_process()
            if output.exists() and output.stat().st_size > 0:
                return
            raise subprocess.TimeoutExpired(cmd, capture_timeout)
        finally:
            stop_process()


def wait_for_senseframe_ready(client: "DevToolsClient", timeout: float = 15.0) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        result = client.call(
            "Runtime.evaluate",
            {
                "expression": "Boolean(window.__sfReady && window.__senseframes && typeof window.__senseframes.apply === 'function')",
                "returnByValue": True,
            },
        )
        if result.get("result", {}).get("value") is True:
            return
        time.sleep(0.1)
    raise SenseAudioError("SenseFrame runtime did not become ready in Chrome.")


def launch_devtools_chrome(chrome: str, width: int, height: int, capture_timeout: float) -> tuple[subprocess.Popen[bytes], DevToolsClient, tempfile.TemporaryDirectory[str]]:
    port = find_free_port()
    profile_context = tempfile.TemporaryDirectory(prefix="senseframe-chrome-profile-")
    cmd = [
        chrome,
        "--headless=new",
        "--disable-gpu",
        "--disable-background-networking",
        "--disable-extensions",
        "--disable-sync",
        "--disable-dev-shm-usage",
        "--no-first-run",
        "--no-default-browser-check",
        "--hide-scrollbars",
        "--mute-audio",
        f"--user-data-dir={profile_context.name}",
        f"--window-size={width},{height}",
        f"--remote-debugging-port={port}",
        "about:blank",
    ]
    process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    try:
        ws_url = wait_for_devtools_target(port, min(12.0, capture_timeout))
        client = DevToolsClient(ws_url, timeout=max(5.0, capture_timeout))
        client.call("Page.enable")
        client.call("Runtime.enable")
        client.call(
            "Emulation.setDeviceMetricsOverride",
            {"width": width, "height": height, "deviceScaleFactor": 1, "mobile": False},
        )
        return process, client, profile_context
    except Exception:
        stop_chrome_process(process)
        profile_context.cleanup()
        raise


def normalize_cookie_same_site(value: Any) -> str | None:
    text = str(value or "").strip().lower()
    if text in {"strict", "lax", "none"}:
        return text.capitalize()
    if text in {"no_restriction", "unspecified"}:
        return "None" if text == "no_restriction" else None
    return None


def normalize_browser_cookie(raw: dict[str, Any], page_url: str) -> dict[str, Any] | None:
    name = str(raw.get("name") or "").strip()
    value = str(raw.get("value") or "")
    if not name:
        return None
    cookie: dict[str, Any] = {"name": name, "value": value}
    domain = str(raw.get("domain") or "").strip()
    path = str(raw.get("path") or "/").strip() or "/"
    if domain:
        cookie["domain"] = domain
        cookie["path"] = path
    else:
        cookie["url"] = page_url
        cookie["path"] = path
    expires = raw.get("expires", raw.get("expirationDate", raw.get("expiry")))
    if isinstance(expires, (int, float)) and expires > 0:
        cookie["expires"] = float(expires)
    elif isinstance(expires, str) and expires.strip().isdigit():
        cookie["expires"] = float(expires.strip())
    if bool(raw.get("secure")):
        cookie["secure"] = True
    if bool(raw.get("httpOnly")):
        cookie["httpOnly"] = True
    same_site = normalize_cookie_same_site(raw.get("sameSite"))
    if same_site:
        cookie["sameSite"] = same_site
    return cookie


def load_browser_cookies(cookie_file: str | None, page_url: str) -> list[dict[str, Any]]:
    if not cookie_file:
        return []
    path = Path(cookie_file).expanduser()
    if not path.exists():
        raise SenseAudioError(f"Cookie file not found: {path}")
    text = path.read_text(encoding="utf-8", errors="replace").strip()
    if not text:
        return []
    raw_cookies: list[dict[str, Any]] = []
    if text[0] in "[{":
        payload = json.loads(text)
        if isinstance(payload, dict):
            cookies = payload.get("cookies", [])
        else:
            cookies = payload
        if isinstance(cookies, list):
            raw_cookies = [item for item in cookies if isinstance(item, dict)]
    else:
        for line in text.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) < 7:
                continue
            domain, _include_subdomains, path_value, secure, expires, name, value = parts[:7]
            raw_cookies.append(
                {
                    "domain": domain,
                    "path": path_value or "/",
                    "secure": secure.upper() == "TRUE",
                    "expires": expires,
                    "name": name,
                    "value": value,
                }
            )
    return [cookie for item in raw_cookies if (cookie := normalize_browser_cookie(item, page_url))]


def site_runtime_value(client: "DevToolsClient", expression: str) -> Any:
    result = client.call(
        "Runtime.evaluate",
        {
            "expression": expression,
            "awaitPromise": True,
            "returnByValue": True,
        },
    )
    return result.get("result", {}).get("value")


def apply_browser_cookies(client: "DevToolsClient", url: str, cookie_file: str | None) -> int:
    cookies = load_browser_cookies(cookie_file, url)
    if not cookies:
        return 0
    client.call("Network.enable")
    client.call("Network.setCookies", {"cookies": cookies})
    return len(cookies)


def dismiss_site_overlays(client: "DevToolsClient") -> dict[str, Any]:
    script = r"""
(function(){
  var clicked = 0;
  var hidden = 0;
  var selectors = [
    '[id*="cookie" i] button',
    '[class*="cookie" i] button',
    '[id*="consent" i] button',
    '[class*="consent" i] button',
    '[id*="gdpr" i] button',
    '[class*="gdpr" i] button',
    '[aria-label*="close" i]',
    '[aria-label*="dismiss" i]',
    '[class*="modal" i] [class*="close" i]',
    '[class*="popup" i] [class*="close" i]',
    '[class*="overlay" i] [class*="close" i]'
  ];
  function isVisible(el) {
    var rect = el.getBoundingClientRect();
    var style = window.getComputedStyle(el);
    return rect.width > 4 && rect.height > 4 && style.visibility !== 'hidden' && style.display !== 'none';
  }
  function tryClick(el) {
    if (!el || !isVisible(el)) return;
    try { el.click(); clicked += 1; } catch(e) {}
  }
  selectors.forEach(function(sel) {
    Array.prototype.slice.call(document.querySelectorAll(sel), 0, 4).forEach(tryClick);
  });
  var labelRe = /(accept|agree|allow|got it|not now|no thanks|close|dismiss|同意|接受|允许|關閉|关闭|知道)/i;
  Array.prototype.slice.call(document.querySelectorAll('button,[role="button"]'), 0, 260).forEach(function(el) {
    var text = (el.innerText || el.getAttribute('aria-label') || '').trim();
    if (text && text.length <= 42 && labelRe.test(text)) tryClick(el);
  });
  var minWidth = window.innerWidth * 0.32;
  Array.prototype.slice.call(document.querySelectorAll('body *'), 0, 5000).forEach(function(el) {
    if (hidden > 12) return;
    var rect = el.getBoundingClientRect();
    if (rect.width < minWidth || rect.height < 80) return;
    if (el.closest('header,nav')) return;
    var style = window.getComputedStyle(el);
    var z = parseInt(style.zIndex || '0', 10);
    if ((style.position === 'fixed' || style.position === 'sticky') && z >= 100) {
      var text = (el.innerText || '').toLowerCase();
      var looksLikeOverlay = /cookie|consent|privacy|subscribe|newsletter|login|sign in|modal|popup|隐私|同意|登录|登入|訂閱|订阅/.test(text);
      if (looksLikeOverlay || rect.height > window.innerHeight * 0.28) {
        el.setAttribute('data-senseframe-hidden-overlay', 'true');
        el.style.setProperty('display', 'none', 'important');
        hidden += 1;
      }
    }
  });
  return {clicked: clicked, hidden: hidden};
})()
"""
    value = site_runtime_value(client, script)
    return value if isinstance(value, dict) else {}


def warm_site_page(client: "DevToolsClient") -> None:
    script = r"""
(async function(){
  var height = Math.max(document.body ? document.body.scrollHeight : 0, document.documentElement.scrollHeight, window.innerHeight);
  var step = Math.max(240, Math.floor(window.innerHeight * 0.72));
  for (var y = 0; y < height; y += step) {
    window.scrollTo(0, y);
    await new Promise(function(resolve){ setTimeout(resolve, 260); });
  }
  window.scrollTo(0, height);
  await new Promise(function(resolve){ setTimeout(resolve, 500); });
  var imgs = Array.prototype.slice.call(document.images || []);
  var pending = imgs.filter(function(img){ return !img.complete; });
  if (pending.length) {
    await Promise.race([
      Promise.all(pending.map(function(img){ return new Promise(function(resolve){ img.onload = img.onerror = resolve; }); })),
      new Promise(function(resolve){ setTimeout(resolve, 4000); })
    ]);
  }
  if (document.fonts && document.fonts.ready) {
    await Promise.race([document.fonts.ready, new Promise(function(resolve){ setTimeout(resolve, 1000); })]);
  }
  window.scrollTo(0, 0);
  await new Promise(function(resolve){ setTimeout(resolve, 300); });
  return true;
})()
"""
    try:
        site_runtime_value(client, script)
    except Exception:
        pass


def site_capture_quality_report(client: "DevToolsClient", source_url: str, cookie_mode: str, cookie_count: int, overlay_result: dict[str, Any]) -> dict[str, Any]:
    script = r"""
(function(){
  var text = (document.body && document.body.innerText || '').trim();
  var title = document.title || '';
  var children = document.body ? document.body.children.length : 0;
  var challenge = !!document.querySelector('.cf-turnstile,[data-sitekey],iframe[src*="challenges.cloudflare.com"],#challenge-running,#challenge-form');
  var minimal = children <= 5 && text.length < 500;
  var challengeTitle = minimal && /just a moment|attention required|access denied/i.test(title);
  var loginText = /(sign in|log in|login|登录|登入|會員|会员)/i.test(text.slice(0, 1600));
  var fixed = 0;
  Array.prototype.slice.call(document.querySelectorAll('body *'), 0, 4000).forEach(function(el) {
    var rect = el.getBoundingClientRect();
    if (rect.width < window.innerWidth * 0.32 || rect.height < 80) return;
    var style = window.getComputedStyle(el);
    var z = parseInt(style.zIndex || '0', 10);
    if ((style.position === 'fixed' || style.position === 'sticky') && z >= 100 && !el.closest('header,nav')) fixed += 1;
  });
  var images = Array.prototype.slice.call(document.images || []);
  function clean(value) { return String(value || '').replace(/\s+/g, ' ').trim(); }
  function uniq(values) {
    var seen = {};
    return values.filter(function(value) {
      value = clean(value);
      if (!value || seen[value]) return false;
      seen[value] = true;
      return true;
    });
  }
  var headings = uniq(Array.prototype.slice.call(document.querySelectorAll('h1,h2,h3'), 0, 16).map(function(el){ return clean(el.innerText || el.textContent).slice(0, 120); }));
  var ctaRe = /(try|start|get|book|demo|contact|download|sign up|subscribe|search|开始|试用|体验|预约|演示|联系|下载|注册|搜索|立即)/i;
  var ctas = uniq(Array.prototype.slice.call(document.querySelectorAll('a,button,[role="button"]'), 0, 260).map(function(el){ return clean(el.innerText || el.getAttribute('aria-label')).slice(0, 64); }).filter(function(label){ return label.length >= 2 && label.length <= 64 && ctaRe.test(label); })).slice(0, 10);
  return {
    final_url: location.href,
    title: title,
    text_length: text.length,
    body_child_count: children,
    scroll_height: Math.max(document.body ? document.body.scrollHeight : 0, document.documentElement.scrollHeight, window.innerHeight),
    viewport: {width: window.innerWidth, height: window.innerHeight},
    challenge_detected: challenge || challengeTitle,
    login_prompt_likely: loginText,
    fixed_overlay_count: fixed,
    image_count: images.length,
    incomplete_image_count: images.filter(function(img){ return !img.complete; }).length,
    content: {
      headings: headings.slice(0, 12),
      ctas: ctas,
      text_sample: text.slice(0, 700)
    }
  };
})()
"""
    signals = site_runtime_value(client, script)
    signals = signals if isinstance(signals, dict) else {}
    warnings: list[dict[str, str]] = []
    if signals.get("challenge_detected"):
        warnings.append({"code": "anti_bot_challenge", "message": "Browser capture appears to have hit an anti-bot or access challenge."})
    if int(signals.get("text_length") or 0) < 180:
        warnings.append({"code": "low_text_content", "message": "Captured page has very little visible text; the site may need longer wait time, cookies, or a logged-in browser profile."})
    if signals.get("login_prompt_likely") and cookie_mode == "clean":
        warnings.append({"code": "login_or_region_gate", "message": "Captured page looks gated by login or account/region UI; a cookie file or dedicated browser profile may improve screenshots."})
    if int(signals.get("fixed_overlay_count") or 0) >= 3:
        warnings.append({"code": "overlay_risk", "message": "Several fixed overlays remain after cleanup and may contaminate screenshots."})
    if int(signals.get("incomplete_image_count") or 0) > max(3, int(signals.get("image_count") or 0) // 3):
        warnings.append({"code": "lazy_assets_incomplete", "message": "Many page images were still incomplete after warmup."})
    return {
        "source": "site-capture",
        "source_url": source_url,
        "captured_at": int(time.time()),
        "ok": not warnings,
        "cookie_mode": cookie_mode,
        "cookie_count": cookie_count,
        "overlay_cleanup": overlay_result,
        "signals": signals,
        "warnings": warnings,
    }


def stop_chrome_process(process: subprocess.Popen[Any]) -> None:
    if process.poll() is not None:
        return
    try:
        os.killpg(process.pid, signal.SIGTERM)
        process.wait(timeout=1.5)
    except Exception:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except Exception:
            process.kill()
        try:
            process.wait(timeout=2)
        except Exception:
            pass


def capture_frames_persistent(
    chrome: str,
    base_url: str,
    frame_dir: Path,
    frame_count: int,
    fps: int,
    width: int,
    height: int,
    virtual_time_budget: int,
    capture_timeout: float,
    resume: bool = False,
    quiet: bool = False,
) -> None:
    process, client, profile_context = launch_devtools_chrome(chrome, width, height, capture_timeout)
    try:
        initial_query = urllib.parse.urlencode({"t": "0.000000", "render": "1"})
        client.call("Page.navigate", {"url": f"{base_url}?{initial_query}"})
        wait_for_page_ready(client, min(20.0, capture_timeout))
        wait_for_senseframe_ready(client, min(20.0, capture_timeout))
        client.call(
            "Runtime.evaluate",
            {
                "expression": "(async function(){ if (document.fonts && document.fonts.ready) await document.fonts.ready; await Promise.all(Array.from(document.images).map(function(img){ return img.complete ? true : new Promise(function(resolve){ img.onload = img.onerror = resolve; }); })); return true; })()",
                "awaitPromise": True,
                "returnByValue": True,
            },
        )
        for frame in range(frame_count):
            timestamp = frame / fps
            frame_path = frame_dir / f"frame_{frame:05d}.png"
            if resume and frame_path.exists() and frame_path.stat().st_size > 0:
                if not quiet:
                    print(f"skipped {frame + 1}/{frame_count}", file=sys.stderr)
                continue
            client.call(
                "Runtime.evaluate",
                {
                    "expression": (
                        "(async function(){"
                        f"var t = {timestamp:.6f};"
                        "if (window.__senseframes && typeof window.__senseframes.apply === 'function') window.__senseframes.apply(t);"
                        "await new Promise(function(resolve){ requestAnimationFrame(function(){ requestAnimationFrame(resolve); }); });"
                        "return true;"
                        "})()"
                    ),
                    "awaitPromise": True,
                    "returnByValue": True,
                },
            )
            if virtual_time_budget > 0:
                time.sleep(min(0.05, virtual_time_budget / 100000.0))
            result = client.call("Page.captureScreenshot", {"format": "png", "fromSurface": True, "captureBeyondViewport": False})
            frame_path.write_bytes(base64.b64decode(str(result.get("data", ""))))
            if not quiet:
                print(f"captured {frame + 1}/{frame_count}", file=sys.stderr)
    finally:
        client.close()
        stop_chrome_process(process)
        profile_context.cleanup()


def recv_exact(sock: socket.socket, size: int) -> bytes:
    chunks: list[bytes] = []
    remaining = size
    while remaining:
        chunk = sock.recv(remaining)
        if not chunk:
            raise SenseAudioError("Chrome DevTools websocket closed unexpectedly.")
        chunks.append(chunk)
        remaining -= len(chunk)
    return b"".join(chunks)


def websocket_connect(ws_url: str, timeout: float = 10.0) -> socket.socket:
    parsed = urllib.parse.urlparse(ws_url)
    host = parsed.hostname or "127.0.0.1"
    port = parsed.port or 80
    path = parsed.path + (f"?{parsed.query}" if parsed.query else "")
    sock = socket.create_connection((host, port), timeout=timeout)
    key = base64.b64encode(os.urandom(16)).decode("ascii")
    request = (
        f"GET {path} HTTP/1.1\r\n"
        f"Host: {host}:{port}\r\n"
        "Upgrade: websocket\r\n"
        "Connection: Upgrade\r\n"
        f"Sec-WebSocket-Key: {key}\r\n"
        "Sec-WebSocket-Version: 13\r\n\r\n"
    )
    sock.sendall(request.encode("ascii"))
    response = b""
    while b"\r\n\r\n" not in response:
        response += recv_exact(sock, 1)
        if len(response) > 8192:
            raise SenseAudioError("Chrome DevTools websocket handshake was too large.")
    if b" 101 " not in response.split(b"\r\n", 1)[0]:
        raise SenseAudioError("Chrome DevTools websocket handshake failed.")
    return sock


def websocket_send_json(sock: socket.socket, payload: dict[str, Any]) -> None:
    data = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    header = bytearray([0x81])
    length = len(data)
    if length < 126:
        header.append(0x80 | length)
    elif length < 65536:
        header.append(0x80 | 126)
        header.extend(struct.pack("!H", length))
    else:
        header.append(0x80 | 127)
        header.extend(struct.pack("!Q", length))
    mask = os.urandom(4)
    masked = bytes(byte ^ mask[index % 4] for index, byte in enumerate(data))
    sock.sendall(bytes(header) + mask + masked)


def websocket_recv_json(sock: socket.socket) -> dict[str, Any]:
    chunks: list[bytes] = []
    while True:
        first, second = recv_exact(sock, 2)
        opcode = first & 0x0F
        fin = bool(first & 0x80)
        masked = bool(second & 0x80)
        length = second & 0x7F
        if length == 126:
            length = struct.unpack("!H", recv_exact(sock, 2))[0]
        elif length == 127:
            length = struct.unpack("!Q", recv_exact(sock, 8))[0]
        mask = recv_exact(sock, 4) if masked else b""
        payload = recv_exact(sock, length) if length else b""
        if masked:
            payload = bytes(byte ^ mask[index % 4] for index, byte in enumerate(payload))
        if opcode == 8:
            raise SenseAudioError("Chrome DevTools websocket closed.")
        if opcode in {1, 2, 0}:
            chunks.append(payload)
        if fin and chunks:
            return json.loads(b"".join(chunks).decode("utf-8"))


class DevToolsClient:
    def __init__(self, ws_url: str, timeout: float = 20.0):
        self.sock = websocket_connect(ws_url, timeout)
        self.sock.settimeout(timeout)
        self.next_id = 0

    def close(self) -> None:
        try:
            self.sock.close()
        except Exception:
            pass

    def call(self, method: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        self.next_id += 1
        request_id = self.next_id
        websocket_send_json(self.sock, {"id": request_id, "method": method, "params": params or {}})
        while True:
            message = websocket_recv_json(self.sock)
            if message.get("id") != request_id:
                continue
            if "error" in message:
                raise SenseAudioError(f"Chrome DevTools {method} failed: {message['error']}")
            return message.get("result", {})


def wait_for_devtools_target(port: int, timeout: float = 12.0) -> str:
    deadline = time.time() + timeout
    last_error: Exception | None = None
    while time.time() < deadline:
        try:
            with urlopen_no_proxy(f"http://127.0.0.1:{port}/json/list", timeout=1.0) as resp:
                targets = json.loads(resp.read().decode("utf-8"))
            for target in targets:
                if target.get("type") == "page" and target.get("webSocketDebuggerUrl"):
                    return str(target["webSocketDebuggerUrl"])
        except Exception as exc:
            last_error = exc
        time.sleep(0.15)
    raise SenseAudioError(f"Chrome DevTools target did not become available: {last_error}")


def wait_for_page_ready(client: DevToolsClient, timeout: float = 20.0) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        result = client.call("Runtime.evaluate", {"expression": "document.readyState", "returnByValue": True})
        state = result.get("result", {}).get("value", "")
        if state in {"interactive", "complete"}:
            return
        time.sleep(0.2)


def locate_dom_highlight(client: DevToolsClient, label: str, width: int, height: int) -> dict[str, Any]:
    needle = clean_text(label)[:80]
    if not needle:
        return {}
    expression = r"""
    (function (needle) {
      function norm(value) { return String(value || "").replace(/\s+/g, " ").trim(); }
      function score(text) {
        text = norm(text);
        if (!text) return 0;
        if (text === needle) return 100;
        if (text.indexOf(needle) >= 0 || needle.indexOf(text) >= 0) return 80 + Math.min(text.length, needle.length) / Math.max(text.length, needle.length);
        var tokens = needle.toLowerCase().split(/[^a-z0-9\u4e00-\u9fff]+/).filter(Boolean);
        var lower = text.toLowerCase();
        var hits = tokens.filter(function (token) { return lower.indexOf(token) >= 0; }).length;
        return tokens.length ? hits / tokens.length * 72 : 0;
      }
      var selectors = "h1,h2,h3,h4,p,a,button,[role=button],[aria-label]";
      var best = null;
      Array.prototype.forEach.call(document.querySelectorAll(selectors), function (element) {
        var text = norm(element.innerText || element.textContent || element.getAttribute("aria-label"));
        var value = score(text);
        if (value < 35) return;
        var rect = element.getBoundingClientRect();
        if (!rect || rect.width < 8 || rect.height < 8) return;
        if (rect.bottom < 0 || rect.top > window.innerHeight) return;
        if (!best || value > best.score) {
          best = {
            score: value,
            text: text.slice(0, 120),
            left: Math.max(0, rect.left),
            top: Math.max(0, rect.top),
            width: Math.min(window.innerWidth - Math.max(0, rect.left), rect.width),
            height: Math.min(window.innerHeight - Math.max(0, rect.top), rect.height)
          };
        }
      });
      if (!best) return null;
      return {
        text: best.text,
        score: best.score,
        left: Math.max(0, Math.min(96, best.left / window.innerWidth * 100 - 1.2)),
        top: Math.max(0, Math.min(92, best.top / window.innerHeight * 100 - 1.2)),
        width: Math.max(12, Math.min(86, best.width / window.innerWidth * 100 + 2.4)),
        height: Math.max(9, Math.min(52, best.height / window.innerHeight * 100 + 2.4))
      };
    })
    """
    try:
        result = client.call(
            "Runtime.evaluate",
            {
                "expression": f"{expression}({json.dumps(needle, ensure_ascii=False)})",
                "returnByValue": True,
            },
        )
        value = result.get("result", {}).get("value")
        return value if isinstance(value, dict) else {}
    except Exception:
        return {}


def capture_site_screenshots(
    url: str,
    output_dir: Path,
    count: int = 3,
    width: int = DEFAULT_WIDTH,
    height: int = DEFAULT_HEIGHT,
    evidence: list[dict[str, Any]] | None = None,
    wait_seconds: float = 1.2,
    capture_timeout: float = 45.0,
    site_asset_output: Path | None = None,
    site_asset_download_dir: Path | None = None,
    browser_profile_dir: str | None = None,
    cookie_file: str | None = None,
    quality_output: Path | None = None,
) -> list[dict[str, Any]]:
    chrome = find_chrome()
    output_dir.mkdir(parents=True, exist_ok=True)
    port = find_free_port()
    temp_profile: tempfile.TemporaryDirectory[str] | None = None
    profile_path: Path
    if browser_profile_dir:
        profile_path = Path(browser_profile_dir).expanduser().resolve()
        profile_path.mkdir(parents=True, exist_ok=True)
    else:
        temp_profile = tempfile.TemporaryDirectory(prefix="senseframe-site-profile-")
        profile_path = Path(temp_profile.name)
    cookie_mode = "clean"
    if browser_profile_dir and cookie_file:
        cookie_mode = "profile+cookie_file"
    elif browser_profile_dir:
        cookie_mode = "profile"
    elif cookie_file:
        cookie_mode = "cookie_file"
    try:
        cmd = [
            chrome,
            "--headless=new",
            "--disable-gpu",
            "--disable-background-networking",
            "--disable-extensions",
            "--disable-sync",
            "--disable-dev-shm-usage",
            "--no-first-run",
            "--no-default-browser-check",
            "--hide-scrollbars",
            "--mute-audio",
            f"--user-data-dir={profile_path}",
            f"--window-size={width},{height}",
            f"--remote-debugging-port={port}",
            "about:blank",
        ]
        process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
        client: DevToolsClient | None = None

        def stop_process() -> None:
            if process.poll() is not None:
                return
            try:
                os.killpg(process.pid, signal.SIGTERM)
                process.wait(timeout=1.5)
            except Exception:
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except Exception:
                    process.kill()
                try:
                    process.wait(timeout=2)
                except Exception:
                    pass

        try:
            ws_url = wait_for_devtools_target(port, min(12.0, capture_timeout))
            client = DevToolsClient(ws_url, timeout=max(5.0, capture_timeout))
            client.call("Page.enable")
            client.call("Runtime.enable")
            client.call(
                "Emulation.setDeviceMetricsOverride",
                {"width": width, "height": height, "deviceScaleFactor": 1, "mobile": False},
            )
            cookie_count = apply_browser_cookies(client, url, cookie_file)
            client.call("Page.navigate", {"url": url})
            wait_for_page_ready(client, min(20.0, capture_timeout))
            time.sleep(max(0.0, wait_seconds))
            overlay_result = dismiss_site_overlays(client)
            time.sleep(0.25)
            warm_site_page(client)
            second_overlay_result = dismiss_site_overlays(client)
            overlay_result = {
                "clicked": int(overlay_result.get("clicked") or 0) + int(second_overlay_result.get("clicked") or 0),
                "hidden": int(overlay_result.get("hidden") or 0) + int(second_overlay_result.get("hidden") or 0),
            }
            if quality_output:
                quality = site_capture_quality_report(client, url, cookie_mode, cookie_count, overlay_result)
                quality_output.parent.mkdir(parents=True, exist_ok=True)
                quality_output.write_text(json.dumps(quality, ensure_ascii=False, indent=2), encoding="utf-8")
            metrics = client.call(
                "Runtime.evaluate",
                {
                    "expression": "Math.max(document.documentElement.scrollHeight, document.body ? document.body.scrollHeight : 0, window.innerHeight)",
                    "returnByValue": True,
                },
            )
            scroll_height = int(float(metrics.get("result", {}).get("value", height) or height))
            max_scroll = max(0, scroll_height - height)
            if site_asset_output:
                inventory = collect_site_asset_inventory(client, url)
                if site_asset_download_dir:
                    inventory["downloads"] = download_site_asset_inventory(inventory, site_asset_download_dir)
                site_asset_output.parent.mkdir(parents=True, exist_ok=True)
                site_asset_output.write_text(json.dumps(inventory, ensure_ascii=False, indent=2), encoding="utf-8")
            screenshots: list[dict[str, Any]] = []
            shot_count = max(1, min(8, int(count)))
            evidence_items = evidence or []
            for index in range(shot_count):
                scroll_y = int(round(max_scroll * index / max(1, shot_count - 1)))
                client.call("Runtime.evaluate", {"expression": f"window.scrollTo(0, {scroll_y});", "returnByValue": True})
                time.sleep(0.25)
                evidence_label = ""
                if evidence_items:
                    evidence_item = evidence_items[min(index, len(evidence_items) - 1)]
                    evidence_label = str(evidence_item.get("label", "") or evidence_item.get("text", "") or "")
                highlight = locate_dom_highlight(client, evidence_label, width, height) if evidence_label else {}
                result = client.call("Page.captureScreenshot", {"format": "png", "fromSurface": True, "captureBeyondViewport": False})
                image_data = base64.b64decode(str(result.get("data", "")))
                output = output_dir / f"site-shot-{index + 1:02d}.png"
                output.write_bytes(image_data)
                screenshots.append(
                    {
                        "id": f"site-shot-{index + 1:02d}",
                        "path": relative_to_project(output_dir.parents[1], output) if output_dir.name == "site-screenshots" and output_dir.parent.name == "assets" else str(output),
                        "url": url,
                        "scroll_y": scroll_y,
                        "width": width,
                        "height": height,
                        "scroll_height": scroll_height,
                        "highlight": highlight,
                    }
                )
            return screenshots
        finally:
            if client:
                client.close()
            stop_process()
    finally:
        if temp_profile:
            temp_profile.cleanup()


def default_render_audio(project_dir: Path, explicit_audio: str | None) -> tuple[str | None, bool]:
    if explicit_audio:
        return explicit_audio, False
    final_audio = registered_asset_path(project_dir, "final-audio", "audio")
    if final_audio:
        return str(final_audio), True
    narration = find_asset_by_type_or_id(project_dir, "narration", "audio")
    if not narration:
        return None, False
    path = project_dir / str(narration.get("path", ""))
    return (str(path), True) if path.exists() else (None, False)


def resolve_render_capture_mode(requested_mode: str, parallel: int) -> str:
    if requested_mode not in {"persistent", "process"}:
        raise SenseAudioError(f"Unknown capture mode: {requested_mode}")
    return requested_mode


def command_render(args: argparse.Namespace) -> None:
    project_dir = Path(args.project).resolve()
    meta = read_project_meta(project_dir)
    width = args.width or int(meta.get("width", DEFAULT_WIDTH))
    height = args.height or int(meta.get("height", DEFAULT_HEIGHT))
    duration = args.duration or float(meta.get("duration", DEFAULT_RENDER_DURATION))
    fps = args.fps or int(meta.get("fps", DEFAULT_RENDER_FPS))
    frame_count = max(1, int(round(duration * fps)))
    output = Path(args.output or project_dir / "renders" / f"{project_dir.name}.mp4")
    output.parent.mkdir(parents=True, exist_ok=True)

    chrome = find_chrome()
    ffmpeg = find_ffmpeg()
    port = find_free_port()
    server, _thread = start_static_server(project_dir, port)
    entry = str(meta.get("entry", "index.html"))
    audio, audio_was_auto = default_render_audio(project_dir, args.audio)
    requested_capture_mode = getattr(args, "capture_mode", "persistent")
    capture_mode = resolve_render_capture_mode(requested_capture_mode, getattr(args, "parallel", 1))

    if args.frame_dir:
        temp_context = None
        frame_dir = Path(args.frame_dir)
    elif args.keep_frames:
        temp_context = None
        frame_dir = output.with_suffix("").parent / f"{output.stem}-frames"
    else:
        temp_context = tempfile.TemporaryDirectory(prefix="senseframe-frames-")
        frame_dir = Path(temp_context.name)
    frame_dir.mkdir(parents=True, exist_ok=True)
    try:
        try:
            base_url = f"http://127.0.0.1:{port}/{entry}"

            def capture_frame(frame: int) -> None:
                timestamp = frame / fps
                query = urllib.parse.urlencode({"t": f"{timestamp:.6f}", "render": "1"})
                url = f"{base_url}?{query}"
                frame_path = frame_dir / f"frame_{frame:05d}.png"
                if args.resume and frame_path.exists() and frame_path.stat().st_size > 0:
                    if not args.quiet:
                        print(f"skipped {frame + 1}/{frame_count}", file=sys.stderr)
                    return
                screenshot_frame(chrome, url, frame_path, width, height, args.virtual_time_budget, getattr(args, "capture_timeout", 30.0))
                if not args.quiet:
                    print(f"captured {frame + 1}/{frame_count}", file=sys.stderr)

            if capture_mode == "persistent":
                capture_frames_persistent(
                    chrome,
                    base_url,
                    frame_dir,
                    frame_count,
                    fps,
                    width,
                    height,
                    args.virtual_time_budget,
                    getattr(args, "capture_timeout", 30.0),
                    resume=args.resume,
                    quiet=args.quiet,
                )
            elif args.parallel and args.parallel > 1:
                with concurrent.futures.ThreadPoolExecutor(max_workers=args.parallel) as executor:
                    list(executor.map(capture_frame, range(frame_count)))
            else:
                for frame in range(frame_count):
                    capture_frame(frame)

            ffmpeg_cmd = [
                ffmpeg,
                "-y",
                "-framerate",
                str(fps),
                "-i",
                str(frame_dir / "frame_%05d.png"),
            ]
            if audio:
                ffmpeg_cmd += ["-i", audio, "-af", f"apad=pad_dur={duration:.3f}", "-shortest"]
            ffmpeg_cmd += [
                "-c:v",
                "libx264",
                "-pix_fmt",
                "yuv420p",
                "-movflags",
                "+faststart",
                str(output),
            ]
            subprocess.run(ffmpeg_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        finally:
            server.shutdown()
            server.server_close()
    finally:
        if temp_context and not args.keep_frames:
            temp_context.cleanup()
    report = {
        "project": str(project_dir),
        "output": str(output),
        "entry": entry,
        "width": width,
        "height": height,
        "duration": duration,
        "fps": fps,
        "frames": frame_count,
        "frame_dir": str(frame_dir) if args.keep_frames or args.frame_dir else None,
        "parallel": args.parallel,
        "requested_capture_mode": requested_capture_mode,
        "capture_mode": capture_mode,
        "resume": args.resume,
        "audio": audio,
        "auto_audio": audio_was_auto,
    }
    report_path = Path(args.report) if getattr(args, "report", None) else output.with_suffix(".render.json")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    try:
        register_asset(
            project_dir,
            getattr(args, "asset_id", None) or "final-video",
            "video",
            output,
            "render",
            {"report": relative_to_project(project_dir, report_path), "fps": fps, "duration": duration},
        )
    except SenseAudioError:
        pass
    print(str(output))


def command_inspect(args: argparse.Namespace) -> None:
    project_dir = Path(args.project).resolve()
    meta = read_project_meta(project_dir)
    width = args.width or int(meta.get("width", DEFAULT_WIDTH))
    height = args.height or int(meta.get("height", DEFAULT_HEIGHT))
    duration = args.duration or float(meta.get("duration", DEFAULT_RENDER_DURATION))
    out_dir = Path(args.output_dir or project_dir / "renders" / "inspect")
    out_dir.mkdir(parents=True, exist_ok=True)

    chrome = find_chrome()
    port = find_free_port()
    server, _thread = start_static_server(project_dir, port)
    entry = str(meta.get("entry", "index.html"))
    samples = max(1, args.samples)
    shots: list[dict[str, Any]] = []
    try:
        for index in range(samples):
            timestamp = 0 if samples == 1 else duration * index / (samples - 1)
            query = urllib.parse.urlencode({"t": f"{timestamp:.6f}", "render": "1"})
            url = f"http://127.0.0.1:{port}/{entry}?{query}"
            output = out_dir / f"sample_{index:02d}_{timestamp:.2f}s.png"
            screenshot_frame(chrome, url, output, width, height, args.virtual_time_budget, getattr(args, "capture_timeout", 30.0))
            shots.append({"time": timestamp, "path": str(output)})
    finally:
        server.shutdown()
        server.server_close()
    contact_sheet = write_inspect_contact_sheet(out_dir, shots)
    write_json(args.report, {"project": str(project_dir), "samples": shots, "contact_sheet": str(contact_sheet) if contact_sheet else None})


def write_inspect_contact_sheet(out_dir: Path, shots: list[dict[str, Any]]) -> Path | None:
    if not shots:
        return None
    output = out_dir / "contact-sheet.html"
    cells: list[str] = []
    for index, shot in enumerate(shots):
        path = Path(str(shot.get("path", "")))
        if not path.exists():
            continue
        rel = html_lib.escape(os.path.relpath(path, out_dir))
        time_label = f"{float(shot.get('time', 0.0)):.2f}s"
        cells.append(
            "<figure>"
            f'<img src="{rel}" alt="sample {index} at {html_lib.escape(time_label)}" />'
            f"<figcaption>{html_lib.escape(time_label)}</figcaption>"
            "</figure>"
        )
    if not cells:
        return None
    output.write_text(
        """<!doctype html>
<html lang="en">
<meta charset="utf-8">
<title>Inspect Contact Sheet</title>
<style>
body{margin:0;background:#111;color:#eee;font:14px/1.4 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
main{padding:20px;display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px}
figure{margin:0;background:#1a1a1a;border:1px solid #333;border-radius:8px;overflow:hidden}
img{display:block;width:100%;height:auto;background:#000}
figcaption{padding:8px 10px;color:#bdbdbd}
</style>
<main>
"""
        + "\n".join(cells)
        + "\n</main>\n</html>\n",
        encoding="utf-8",
    )
    return output


def paeth_predictor(a: int, b: int, c: int) -> int:
    p = a + b - c
    pa = abs(p - a)
    pb = abs(p - b)
    pc = abs(p - c)
    if pa <= pb and pa <= pc:
        return a
    if pb <= pc:
        return b
    return c


def png_visual_stats(path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        raise SenseAudioError(f"Not a PNG file: {path}")
    offset = 8
    width = height = bit_depth = color_type = 0
    idat = bytearray()
    while offset + 8 <= len(data):
        length = struct.unpack(">I", data[offset : offset + 4])[0]
        chunk_type = data[offset + 4 : offset + 8]
        chunk_data = data[offset + 8 : offset + 8 + length]
        offset += 12 + length
        if chunk_type == b"IHDR":
            width, height, bit_depth, color_type = struct.unpack(">IIBB", chunk_data[:10])
        elif chunk_type == b"IDAT":
            idat.extend(chunk_data)
        elif chunk_type == b"IEND":
            break
    channels_by_type = {0: 1, 2: 3, 6: 4}
    channels = channels_by_type.get(color_type)
    if bit_depth != 8 or channels is None or width <= 0 or height <= 0:
        raise SenseAudioError(f"Unsupported PNG format for visual audit: {path}")
    raw = zlib.decompress(bytes(idat))
    stride = width * channels
    previous = bytearray(stride)
    luminance_values: list[float] = []
    sample_step = max(1, (width * height) // 12000)
    pixel_index = 0
    pos = 0
    for _row in range(height):
        filter_type = raw[pos]
        pos += 1
        scanline = bytearray(raw[pos : pos + stride])
        pos += stride
        for i in range(stride):
            left = scanline[i - channels] if i >= channels else 0
            up = previous[i]
            upper_left = previous[i - channels] if i >= channels else 0
            if filter_type == 1:
                scanline[i] = (scanline[i] + left) & 0xFF
            elif filter_type == 2:
                scanline[i] = (scanline[i] + up) & 0xFF
            elif filter_type == 3:
                scanline[i] = (scanline[i] + ((left + up) // 2)) & 0xFF
            elif filter_type == 4:
                scanline[i] = (scanline[i] + paeth_predictor(left, up, upper_left)) & 0xFF
        for x in range(width):
            if pixel_index % sample_step == 0:
                base = x * channels
                if color_type == 0:
                    lum = float(scanline[base])
                else:
                    red, green, blue = scanline[base], scanline[base + 1], scanline[base + 2]
                    lum = 0.2126 * red + 0.7152 * green + 0.0722 * blue
                luminance_values.append(lum)
            pixel_index += 1
        previous = scanline
    if not luminance_values:
        raise SenseAudioError(f"PNG visual audit found no pixels: {path}")
    mean = sum(luminance_values) / len(luminance_values)
    variance = sum((value - mean) ** 2 for value in luminance_values) / len(luminance_values)
    stddev = math.sqrt(variance)
    dark_ratio = sum(1 for value in luminance_values if value < 14) / len(luminance_values)
    bright_ratio = sum(1 for value in luminance_values if value > 244) / len(luminance_values)
    return {
        "width": width,
        "height": height,
        "samples": len(luminance_values),
        "mean_luma": round(mean, 3),
        "luma_stddev": round(stddev, 3),
        "dark_ratio": round(dark_ratio, 4),
        "bright_ratio": round(bright_ratio, 4),
        "file_size": path.stat().st_size,
    }


VISIBLE_INTERNAL_COPY_PATTERNS = (
    "PAGE SIGNAL",
    "Website Brief",
    "真实证据",
    "核心依据",
    "页面线索",
    "使用含义",
    "展示其",
    "證明其",
    "proof_points",
    "hook/proof",
)


def frame_quality_audit(project_dir: Path, images: list[Path]) -> dict[str, Any]:
    issues: list[dict[str, Any]] = []
    frames: list[dict[str, Any]] = []
    for image in images:
        frame: dict[str, Any] = {"path": str(image)}
        try:
            stats = png_visual_stats(image)
            frame["stats"] = stats
            if int(stats["file_size"]) < 8000:
                issues.append({"code": "tiny_frame", "severity": "error", "image": str(image), "message": "Frame file is unusually small and may be blank or failed."})
            if float(stats["luma_stddev"]) < 3.0:
                issues.append({"code": "low_detail_frame", "severity": "error", "image": str(image), "message": "Frame has extremely low visual variance and is likely blank, loading, or washed out."})
            if float(stats["dark_ratio"]) > 0.985 or float(stats["bright_ratio"]) > 0.985:
                issues.append({"code": "blank_frame", "severity": "error", "image": str(image), "message": "Almost the entire frame is dark or bright."})
        except Exception as exc:
            frame["error"] = str(exc)
            issues.append({"code": "unreadable_frame", "severity": "error", "image": str(image), "message": str(exc)})
        frames.append(frame)
    entry = project_dir / "index.html"
    if entry.exists():
        markup = entry.read_text(encoding="utf-8", errors="replace")
        leaked = [token for token in VISIBLE_INTERNAL_COPY_PATTERNS if token in markup]
        for token in leaked:
            issues.append({"code": "internal_copy_leak", "severity": "error", "image": "", "message": f"Visible composition markup still contains internal planning copy: {token}"})
    capture_quality = read_json_if_exists(project_dir / "assets" / "site-capture-quality.json")
    capture_warnings = capture_quality.get("warnings", []) if isinstance(capture_quality.get("warnings"), list) else []
    for warning in capture_warnings:
        issues.append({"code": f"capture_{warning.get('code', 'warning')}", "severity": "warning", "image": "", "message": str(warning.get("message", ""))})
    error_count = sum(1 for issue in issues if issue.get("severity") == "error")
    return {
        "project": str(project_dir),
        "images": [str(path) for path in images],
        "frames": frames,
        "capture_quality": capture_quality or None,
        "issues": issues,
        "summary": {
            "frame_count": len(images),
            "error_count": error_count,
            "warning_count": len(issues) - error_count,
        },
        "safe_to_render": error_count == 0,
    }


def command_frame_quality_audit(args: argparse.Namespace) -> None:
    project_dir = Path(args.project).resolve()
    images = project_vision_images(project_dir, args.image, args.max_images)
    payload = frame_quality_audit(project_dir, images)
    output = Path(args.output) if args.output else project_dir / "assets" / "frame-quality.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    if (project_dir / "senseframe.json").exists():
        register_asset(project_dir, "frame-quality", "json", output, "local-frame-quality-audit", {"safe_to_render": payload.get("safe_to_render", False)})
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(str(output))
    if args.strict and not payload.get("safe_to_render", False):
        raise SenseAudioError("Frame quality audit failed.")


def add_common_video(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--model", default=DEFAULT_VIDEO_MODEL)
    parser.add_argument("--prompt")
    parser.add_argument("--image", action="append")
    parser.add_argument("--image-role", default="reference", choices=["first_frame", "last_frame", "reference"])
    parser.add_argument("--audio-url", action="append")
    parser.add_argument("--video-url", action="append")
    parser.add_argument("--duration", type=int, default=10)
    parser.add_argument("--resolution", default="720p")
    parser.add_argument("--ratio", default="16:9")
    parser.add_argument("--watermark", action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument("--generate-audio", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--camera-fixed", action=argparse.BooleanOptionalAction, default=None)
    parser.add_argument("--poll", action="store_true")
    parser.add_argument("--interval", type=int, default=8)
    parser.add_argument("--timeout", type=int, default=1800)
    parser.add_argument("--download")
    parser.add_argument("--manifest")
    parser.add_argument("--dry-run", action="store_true")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Author HTML video compositions, render them locally, and generate media with SenseAudio APIs."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="Create an HTML composition project.")
    init.add_argument("name")
    init.add_argument("--width", type=int, default=DEFAULT_WIDTH)
    init.add_argument("--height", type=int, default=DEFAULT_HEIGHT)
    init.add_argument("--duration", type=float, default=DEFAULT_RENDER_DURATION)
    init.add_argument("--fps", type=int, default=DEFAULT_RENDER_FPS)
    init.set_defaults(func=command_init)

    styles = sub.add_parser("styles", help="List or inspect built-in visual style presets.")
    styles.add_argument("--preset", choices=sorted(STYLE_PRESETS))
    styles.add_argument("--json", action="store_true")
    styles.set_defaults(func=command_styles)

    brand_extract = sub.add_parser("brand-extract", help="Extract brand metadata from a website.")
    brand_extract.add_argument("--url", required=True)
    brand_extract.add_argument("--html-file", help="Use a local HTML file instead of fetching --url.")
    brand_extract.add_argument("--project", help="Optional project to receive assets/brand.json.")
    brand_extract.add_argument("--output", help="Write brand JSON to a custom path.")
    brand_extract.add_argument("--json", action="store_true")
    brand_extract.set_defaults(func=command_brand_extract)

    site_ingest = sub.add_parser("site-ingest", help="Extract real website evidence for URL-to-video planning.")
    site_ingest.add_argument("--url", required=True)
    site_ingest.add_argument("--html-file", help="Use a local HTML file instead of fetching --url.")
    site_ingest.add_argument("--project", help="Optional project to receive assets/site-profile.json.")
    site_ingest.add_argument("--output", help="Write site profile JSON to a custom path.")
    site_ingest.add_argument("--json", action="store_true")
    site_ingest.set_defaults(func=command_site_ingest)

    source_ingest = sub.add_parser("source-ingest", help="Convert Markdown, text, or a GitHub README into a reusable site-profile JSON.")
    source_group = source_ingest.add_mutually_exclusive_group(required=True)
    source_group.add_argument("--file", help="Local Markdown or text file to ingest.")
    source_group.add_argument("--github-url", help="GitHub repository URL or owner/repo shorthand; fetches README.md.")
    source_ingest.add_argument("--title", help="Override the inferred source title.")
    source_ingest.add_argument("--project", help="Optional project to receive assets/site-profile.json.")
    source_ingest.add_argument("--output", help="Write source profile JSON to a custom path.")
    source_ingest.add_argument("--json", action="store_true")
    source_ingest.set_defaults(func=command_source_ingest)

    site_capture = sub.add_parser("site-capture", help="Capture real website scroll screenshots with local Chrome.")
    site_capture.add_argument("--url", required=True)
    site_capture.add_argument("--project", help="Optional project to receive assets/site-screenshots and update site-profile.json.")
    site_capture.add_argument("--output-dir", help="Write screenshots to a custom directory.")
    site_capture.add_argument("--count", type=int, default=3)
    site_capture.add_argument("--width", type=int, default=DEFAULT_WIDTH)
    site_capture.add_argument("--height", type=int, default=DEFAULT_HEIGHT)
    site_capture.add_argument("--wait", type=float, default=2.8)
    site_capture.add_argument("--capture-timeout", type=float, default=45.0)
    site_capture.add_argument("--browser-profile", help="Use a dedicated Chrome user-data-dir for authenticated or region-specific captures. Env: SENSEFRAME_SITE_BROWSER_PROFILE.")
    site_capture.add_argument("--cookie-file", help="Load cookies from a JSON storage_state/export or Netscape cookies.txt file before navigation. Env: SENSEFRAME_SITE_COOKIE_FILE.")
    site_capture.add_argument("--site-assets", action=argparse.BooleanOptionalAction, default=True, help="Write assets/site-assets.json with images, fonts, media, and animation hints when --project is set.")
    site_capture.add_argument("--download-site-assets", action="store_true", help="Download indexed site images/icons/stylesheets into assets/site-assets when --project is set.")
    site_capture.add_argument("--json", action="store_true")
    site_capture.set_defaults(func=command_site_capture)

    site_vision_audit = sub.add_parser("site-vision-audit", help="Use an OpenRouter/OpenAI-compatible vision model to audit rendered website explainer frames.")
    site_vision_audit.add_argument("--project", help="Project directory. Uses renders/inspect frames, then assets/site-screenshots.")
    site_vision_audit.add_argument("--image", action="append", help="Specific image/frame to audit. Relative paths resolve against --project.")
    site_vision_audit.add_argument("--brief", help="Optional visual intent/context for the audit.")
    site_vision_audit.add_argument("--model", default=os.environ.get("OPENROUTER_MODEL") or os.environ.get("VL_MODEL") or DEFAULT_VL_MODEL)
    site_vision_audit.add_argument("--base-url", default=os.environ.get("OPENROUTER_BASE_URL") or os.environ.get("VL_BASE_URL") or DEFAULT_OPENROUTER_BASE_URL)
    site_vision_audit.add_argument("--max-images", type=int, default=4)
    site_vision_audit.add_argument("--output")
    site_vision_audit.add_argument("--dry-run", action="store_true")
    site_vision_audit.add_argument("--json", action="store_true")
    site_vision_audit.set_defaults(func=command_site_vision_audit)

    site_vision_plan = sub.add_parser("site-vision-plan", help="Plan screenshot crops and focus points before rendering website explainers.")
    site_vision_plan.add_argument("--project", help="Project directory with assets/site-profile.json.")
    site_vision_plan.add_argument("--site-file", help="Saved site-ingest JSON payload.")
    site_vision_plan.add_argument("--provider", default="heuristic", choices=["heuristic", "openrouter"])
    site_vision_plan.add_argument("--model", default=os.environ.get("OPENROUTER_MODEL") or os.environ.get("VL_MODEL") or DEFAULT_VL_MODEL)
    site_vision_plan.add_argument("--base-url", default=os.environ.get("OPENROUTER_BASE_URL") or os.environ.get("VL_BASE_URL") or DEFAULT_OPENROUTER_BASE_URL)
    site_vision_plan.add_argument("--max-images", type=int, default=6)
    site_vision_plan.add_argument("--fallback", action=argparse.BooleanOptionalAction, default=True)
    site_vision_plan.add_argument("--output")
    site_vision_plan.add_argument("--dry-run", action="store_true")
    site_vision_plan.add_argument("--json", action="store_true")
    site_vision_plan.set_defaults(func=command_site_vision_plan)

    beats = sub.add_parser("beats", help="Split storyboard scenes into smaller timed beat layers.")
    beats.add_argument("--project", required=True)
    beats.add_argument("--beats-per-scene", type=int, default=DEFAULT_BEATS_PER_SCENE)
    beats.add_argument("--output")
    beats.add_argument("--json", action="store_true")
    beats.set_defaults(func=command_beats)

    llm_plan = sub.add_parser("llm-plan", help="Generate a creative plan with a DeepSeek, AudioClaw, or OpenRouter OpenAI-compatible chat API.")
    brief_group = llm_plan.add_mutually_exclusive_group(required=True)
    brief_group.add_argument("--brief")
    brief_group.add_argument("--brief-file")
    llm_plan.add_argument("--provider", default="audioclaw", choices=["deepseek", "audioclaw", "openrouter"])
    llm_plan.add_argument("--model")
    llm_plan.add_argument("--base-url")
    llm_plan.add_argument("--duration", type=float, default=9.0)
    llm_plan.add_argument("--longform", action="store_true", help="Use a deeper longform director prompt and at least 24 seconds of planning.")
    llm_plan.add_argument("--audience", default="general creators")
    llm_plan.add_argument("--style", default="polished product UI explainer")
    llm_plan.add_argument("--output")
    llm_plan.add_argument("--dry-run", action="store_true")
    llm_plan.set_defaults(func=command_llm_plan)

    compose = sub.add_parser("compose", help="Create an HTML video project from a brief.")
    compose.add_argument("--project", required=True)
    brief_group = compose.add_mutually_exclusive_group(required=True)
    brief_group.add_argument("--brief")
    brief_group.add_argument("--brief-file")
    compose.add_argument("--title")
    compose.add_argument("--headline")
    compose.add_argument("--narration")
    compose.add_argument("--brand-url", help="Fetch brand name, description, navigation, and colors from a website.")
    compose.add_argument("--brand-file", help="Use a saved brand-extract JSON payload.")
    compose.add_argument("--site-url", help="Fetch real website headings, sections, CTAs, and evidence for URL-to-video.")
    compose.add_argument("--site-file", help="Use a saved site-ingest JSON payload.")
    compose.add_argument("--site-screenshots", action="store_true", help="Capture real website scroll screenshots and use them as visual evidence.")
    compose.add_argument("--site-screenshot-count", type=int, default=4)
    compose.add_argument("--site-screenshot-wait", type=float, default=2.8)
    compose.add_argument("--download-site-assets", action="store_true", help="Download indexed site images/icons/stylesheets when capturing screenshots.")
    compose.add_argument("--browser-profile", help="Use a dedicated Chrome user-data-dir for website screenshot capture. Env: SENSEFRAME_SITE_BROWSER_PROFILE.")
    compose.add_argument("--cookie-file", help="Load cookies before website screenshot capture. Env: SENSEFRAME_SITE_COOKIE_FILE.")
    compose.add_argument("--capture-timeout", type=float, default=45.0)
    compose.add_argument("--plan-file", help="Use a saved llm-plan JSON instead of heuristic planning.")
    compose.add_argument("--llm", default="audioclaw", choices=["none", "deepseek", "audioclaw", "openrouter"], help="Use an OpenAI-compatible chat API to plan title, narration, and storyboard.")
    compose.add_argument("--llm-fallback", action=argparse.BooleanOptionalAction, default=True, help="Use heuristic planning when the default LLM route is unavailable.")
    compose.add_argument("--llm-model")
    compose.add_argument("--llm-base-url")
    compose.add_argument("--audience", default="general creators")
    compose.add_argument("--style", default="polished product UI explainer")
    compose.add_argument("--style-preset", default="executive-film", choices=sorted(STYLE_PRESETS))
    compose.add_argument("--beat-mode", default="scene", choices=BEAT_MODES)
    compose.add_argument("--beats-per-scene", type=int, default=DEFAULT_BEATS_PER_SCENE)
    compose.add_argument("--width", type=int, default=DEFAULT_WIDTH)
    compose.add_argument("--height", type=int, default=DEFAULT_HEIGHT)
    compose.add_argument("--duration", type=float, default=9.0)
    compose.add_argument("--longform", action="store_true", help="Enable longform director mode; raises duration to at least 24s and expands scene planning.")
    compose.add_argument("--fps", type=int, default=DEFAULT_RENDER_FPS)
    compose.add_argument("--voice-id", default=DEFAULT_VOICE_ID)
    compose.add_argument("--tts-model", default=DEFAULT_TTS_MODEL)
    compose.add_argument("--asr-model", default=DEFAULT_ASR_MODEL)
    compose.add_argument("--speed", type=float, default=1.0)
    compose.add_argument("--generate-images", action="store_true", help="Prepare or generate a SenseAudio hero image asset.")
    compose.add_argument("--generate-broll", action="store_true", help="Prepare or submit a SenseAudio b-roll video asset.")
    compose.add_argument("--asset-dry-run", action="store_true", help="Plan generated assets without live image/video calls.")
    compose.add_argument("--image-prompt")
    compose.add_argument("--video-prompt")
    compose.add_argument("--image-size", default="1328x1328")
    compose.add_argument("--animation-preset", default="none", choices=["none", "cinematic", "kinetic", "product-tour"])
    compose.add_argument("--transition-preset", default="editorial", choices=TRANSITION_PRESETS)
    compose.add_argument("--timeline-engine", default="native", choices=TIMELINE_ENGINES)
    compose.add_argument("--offline", action="store_true", help="Skip live SenseAudio calls and create editable local assets.")
    compose.add_argument("--render", action="store_true", help="Render MP4 after composing.")
    compose.add_argument("--quiet", action="store_true")
    compose.set_defaults(func=command_compose)

    site_video = sub.add_parser("site-video", help="One-pass website-to-video pipeline with LLM planning, audio data, render, and audits.")
    source_group = site_video.add_mutually_exclusive_group(required=True)
    source_group.add_argument("--url", help="Live website URL to ingest and capture.")
    source_group.add_argument("--site-file", help="Saved site-ingest JSON payload for offline/reproducible runs.")
    site_video.add_argument("--project", required=True)
    site_video.add_argument("--brief")
    site_video.add_argument("--brief-file")
    site_video.add_argument("--title")
    site_video.add_argument("--headline")
    site_video.add_argument("--narration")
    site_video.add_argument("--brand-file")
    site_video.add_argument("--plan-file")
    site_video.add_argument("--llm", default="audioclaw", choices=["none", "deepseek", "audioclaw", "openrouter"])
    site_video.add_argument("--llm-fallback", action=argparse.BooleanOptionalAction, default=True, help="Retry with heuristic planning if the selected LLM route fails.")
    site_video.add_argument("--llm-model")
    site_video.add_argument("--llm-base-url")
    site_video.add_argument("--audience", default="website visitors and product evaluators")
    site_video.add_argument("--style", default="premium editorial website explainer with restrained cinematic motion")
    site_video.add_argument("--style-preset", default="editorial-pro", choices=sorted(STYLE_PRESETS))
    site_video.add_argument("--beat-mode", default="layered", choices=BEAT_MODES)
    site_video.add_argument("--beats-per-scene", type=int, default=DEFAULT_BEATS_PER_SCENE)
    site_video.add_argument("--width", type=int, default=DEFAULT_WIDTH)
    site_video.add_argument("--height", type=int, default=DEFAULT_HEIGHT)
    site_video.add_argument("--duration", type=float, default=14.0)
    site_video.add_argument("--longform", action="store_true", help="Enable longform director mode; raises duration to at least 24s and expands scene planning.")
    site_video.add_argument("--fps", type=int, default=30)
    site_video.add_argument("--voice-id", default=DEFAULT_VOICE_ID)
    site_video.add_argument("--tts-model", default=DEFAULT_TTS_MODEL)
    site_video.add_argument("--asr-model", default=DEFAULT_ASR_MODEL)
    site_video.add_argument("--speed", type=float, default=1.0)
    site_video.add_argument("--site-screenshots", action=argparse.BooleanOptionalAction, default=True)
    site_video.add_argument("--site-screenshot-count", type=int, default=4)
    site_video.add_argument("--site-screenshot-wait", type=float, default=3.0)
    site_video.add_argument("--download-site-assets", action="store_true", help="Download indexed site images/icons/stylesheets during compose.")
    site_video.add_argument("--browser-profile", help="Use a dedicated Chrome user-data-dir for capture. Prefer a copied/profile-specific directory, not your daily Chrome profile.")
    site_video.add_argument("--cookie-file", help="Load cookies from JSON storage_state/export or Netscape cookies.txt before capture.")
    site_video.add_argument("--capture-timeout", type=float, default=45.0)
    site_video.add_argument("--generate-images", action="store_true")
    site_video.add_argument("--generate-broll", action="store_true")
    site_video.add_argument("--asset-dry-run", action="store_true")
    site_video.add_argument("--image-prompt")
    site_video.add_argument("--video-prompt")
    site_video.add_argument("--image-size", default="1328x1328")
    site_video.add_argument("--animation-preset", default="cinematic", choices=["none", "cinematic", "kinetic", "product-tour"])
    site_video.add_argument("--transition-preset", default="editorial", choices=TRANSITION_PRESETS)
    site_video.add_argument("--timeline-engine", default="gsap-compat", choices=TIMELINE_ENGINES)
    site_video.add_argument("--render", action=argparse.BooleanOptionalAction, default=True)
    site_video.add_argument("--output")
    site_video.add_argument("--virtual-time-budget", type=int, default=1000)
    site_video.add_argument("--resume", action="store_true")
    site_video.add_argument("--parallel", type=int, default=1)
    site_video.add_argument("--capture-mode", default="persistent", choices=["persistent", "process"])
    site_video.add_argument("--quality-audit", action=argparse.BooleanOptionalAction, default=True, help="Capture inspect frames and run local frame-quality checks before delivery.")
    site_video.add_argument("--vision-audit", action="store_true")
    site_video.add_argument("--vision-dry-run", action="store_true")
    site_video.add_argument("--inspect-samples", type=int, default=4)
    site_video.add_argument("--vl-model", default=os.environ.get("OPENROUTER_MODEL") or os.environ.get("VL_MODEL") or DEFAULT_VL_MODEL)
    site_video.add_argument("--vl-base-url", default=os.environ.get("OPENROUTER_BASE_URL") or os.environ.get("VL_BASE_URL") or DEFAULT_OPENROUTER_BASE_URL)
    site_video.add_argument("--music", action=argparse.BooleanOptionalAction, default=False, help="Generate or attach a SenseAudio background music bed.")
    site_video.add_argument("--music-prompt")
    site_video.add_argument("--music-style", default="minimal cinematic ambient, subtle pulse, premium website explainer")
    site_video.add_argument("--music-title")
    site_video.add_argument("--music-lyrics")
    site_video.add_argument("--music-negative-tags", default="loud vocals, harsh drums, distorted lead, crowded arrangement")
    site_video.add_argument("--music-instrumental", action=argparse.BooleanOptionalAction, default=True)
    site_video.add_argument("--music-model", default=DEFAULT_MUSIC_MODEL)
    site_video.add_argument("--music-volume", type=float, default=DEFAULT_MUSIC_VOLUME)
    site_video.add_argument("--music-poll", action="store_true", help="Wait for SenseAudio music completion and download before mixing.")
    site_video.add_argument("--music-interval", type=int, default=10)
    site_video.add_argument("--music-timeout", type=int, default=600)
    site_video.add_argument("--music-dry-run", action="store_true", help="Plan the music API payload without spending credits.")
    site_video.add_argument("--music-fallback", action=argparse.BooleanOptionalAction, default=True, help="Generate a local ambient bed when SenseAudio music does not return audio.")
    site_video.add_argument("--auto-repair", action=argparse.BooleanOptionalAction, default=False, help="Run one automatic second repair pass after audits and rerender.")
    site_video.add_argument("--offline", action="store_true", help="Skip live SenseAudio media calls; LLM may still run unless --llm none is set.")
    site_video.add_argument("--dry-run", action="store_true")
    site_video.add_argument("--quiet", action="store_true")
    site_video.set_defaults(func=command_site_video)

    build = sub.add_parser("build", help="Run the local project pipeline: lint, captions if needed, and render.")
    build.add_argument("--project", default=".")
    build.add_argument("--output")
    build.add_argument("--fps", type=int)
    build.add_argument("--duration", type=float)
    build.add_argument("--width", type=int)
    build.add_argument("--height", type=int)
    build.add_argument("--virtual-time-budget", type=int, default=1000)
    build.add_argument("--capture-timeout", type=float, default=30.0)
    build.add_argument("--report")
    build.add_argument("--asset-id", default="final-video")
    build.add_argument("--frame-dir")
    build.add_argument("--keep-frames", action="store_true")
    build.add_argument("--resume", action="store_true")
    build.add_argument("--parallel", type=int, default=1)
    build.add_argument("--capture-mode", default="persistent", choices=["persistent", "process"])
    build.add_argument("--dry-run", action="store_true")
    build.add_argument("--json", action="store_true")
    build.add_argument("--quiet", action="store_true")
    build.set_defaults(func=command_build)

    generate_assets = sub.add_parser("generate-assets", help="Plan or generate SenseAudio image/video assets for a project.")
    generate_assets.add_argument("--project", required=True)
    generate_assets.add_argument("--images", action=argparse.BooleanOptionalAction, default=True)
    generate_assets.add_argument("--broll", action=argparse.BooleanOptionalAction, default=True)
    generate_assets.add_argument("--image-prompt")
    generate_assets.add_argument("--video-prompt")
    generate_assets.add_argument("--image-id", default="hero-image")
    generate_assets.add_argument("--video-id", default="broll-video")
    generate_assets.add_argument("--image-model", default=DEFAULT_IMAGE_MODEL)
    generate_assets.add_argument("--image-size", default="1328x1328")
    generate_assets.add_argument("--video-model", default=DEFAULT_VIDEO_MODEL)
    generate_assets.add_argument("--video-duration", type=int, default=5)
    generate_assets.add_argument("--video-resolution", default="720p")
    generate_assets.add_argument("--video-ratio", default="16:9")
    generate_assets.add_argument("--poll", action="store_true", help="Poll submitted video assets and download completed clips.")
    generate_assets.add_argument("--interval", type=int, default=8)
    generate_assets.add_argument("--timeout", type=int, default=1800)
    generate_assets.add_argument("--dry-run", action="store_true")
    generate_assets.set_defaults(func=command_generate_assets)

    timeline = sub.add_parser("timeline", help="Create a timeline JSON DSL and bind it to the HTML runtime.")
    timeline.add_argument("--project", required=True)
    timeline.add_argument("--preset", default="cinematic", choices=["cinematic", "kinetic", "product-tour"])
    timeline.add_argument("--transition-preset", default="editorial", choices=TRANSITION_PRESETS)
    timeline.add_argument("--timeline-engine", default="native", choices=TIMELINE_ENGINES)
    timeline.set_defaults(func=command_timeline)

    lint = sub.add_parser("lint", help="Validate an HTML video project before rendering.")
    lint.add_argument("--project", default=".")
    lint.add_argument("--json", action="store_true")
    lint.add_argument("--strict", action="store_true", help="Exit with an error when issues are found.")
    lint.set_defaults(func=command_lint)

    motion_audit = sub.add_parser("motion-audit", help="Audit storyboard, scene, and seekable motion alignment.")
    motion_audit.add_argument("--project", default=".")
    motion_audit.add_argument("--json", action="store_true")
    motion_audit.add_argument("--strict", action="store_true", help="Exit with an error when motion issues are found.")
    motion_audit.set_defaults(func=command_motion_audit)

    motion_map = sub.add_parser("motion-map", help="Map motion density, scene coverage, and low-motion zones.")
    motion_map.add_argument("--project", default=".")
    motion_map.add_argument("--samples", type=int, default=24)
    motion_map.add_argument("--low-threshold", type=float, default=1.4)
    motion_map.add_argument("--min-dead-zone", type=float, default=0.8)
    motion_map.add_argument("--json", action="store_true")
    motion_map.add_argument("--strict", action="store_true", help="Exit with an error when motion map issues are found.")
    motion_map.set_defaults(func=command_motion_map)

    repair = sub.add_parser("repair", help="Apply an automatic second-pass composition repair from motion and vision audits.")
    repair.add_argument("--project", required=True)
    repair.add_argument("--dry-run", action="store_true")
    repair.add_argument("--json", action="store_true")
    repair.set_defaults(func=command_repair)

    captions = sub.add_parser("captions", help="Convert ASR transcript JSON into renderable captions.")
    captions.add_argument("--project")
    captions.add_argument("--transcript", required=True)
    captions.add_argument("--output")
    captions.add_argument("--max-gap", type=float, default=0.35)
    captions.add_argument("--max-chars", type=int, default=28)
    captions.add_argument("--include-words", action="store_true", help="Embed word timings for active word highlighting.")
    captions.add_argument("--asset-id", default="captions")
    captions.set_defaults(func=command_captions)

    captions_export = sub.add_parser("captions-export", help="Export captions JSON to SRT or WebVTT.")
    captions_export.add_argument("--captions", required=True)
    captions_export.add_argument("--format", choices=["srt", "vtt"], required=True)
    captions_export.add_argument("--output", required=True)
    captions_export.set_defaults(func=command_captions_export)

    asset_add = sub.add_parser("asset-add", help="Register a generated or local asset in the project manifest.")
    asset_add.add_argument("--project", required=True)
    asset_add.add_argument("--id", required=True)
    asset_add.add_argument("--type", required=True, choices=["audio", "image", "video", "captions", "transcript", "json", "text", "other"])
    asset_add.add_argument("--path", required=True)
    asset_add.add_argument("--role")
    asset_add.add_argument("--label")
    asset_add.set_defaults(func=command_asset_add)

    asset_report = sub.add_parser("asset-report", help="Summarize project assets and missing files.")
    asset_report.add_argument("--project", default=".")
    asset_report.add_argument("--json", action="store_true")
    asset_report.set_defaults(func=command_asset_report)

    mix_audio = sub.add_parser("mix-audio", help="Mix narration with SenseAudio-generated music and register final audio.")
    mix_audio.add_argument("--project")
    mix_audio.add_argument("--voice")
    mix_audio.add_argument("--music")
    mix_audio.add_argument("--output", required=True)
    mix_audio.add_argument("--duration", type=float, required=True)
    mix_audio.add_argument("--music-volume", type=float, default=DEFAULT_MUSIC_VOLUME)
    mix_audio.add_argument("--asset-id", default="final-audio")
    mix_audio.add_argument("--dry-run", action="store_true")
    mix_audio.add_argument("--json", action="store_true")
    mix_audio.set_defaults(func=command_mix_audio)

    audio_data = sub.add_parser("audio-data", help="Extract frame-level audio reactivity data for seekable motion.")
    audio_data.add_argument("--project")
    audio_data.add_argument("--audio", required=True)
    audio_data.add_argument("--output", required=True)
    audio_data.add_argument("--fps", type=int, default=DEFAULT_RENDER_FPS)
    audio_data.add_argument("--bands", type=int, default=8)
    audio_data.add_argument("--duration", type=float)
    audio_data.add_argument("--asset-id", default="audio-data")
    audio_data.add_argument("--dry-run", action="store_true")
    audio_data.set_defaults(func=command_audio_data)

    preview = sub.add_parser("preview", help="Serve an HTML composition project for browser preview.")
    preview.add_argument("project", nargs="?", default=".")
    preview.add_argument("--port", type=int)
    preview.add_argument("--once", action="store_true", help="Print URL then exit after server startup.")
    preview.set_defaults(func=command_preview)

    render = sub.add_parser("render", help="Render an HTML composition project to MP4.")
    render.add_argument("project", nargs="?", default=".")
    render.add_argument("--output", "-o")
    render.add_argument("--fps", type=int)
    render.add_argument("--duration", type=float)
    render.add_argument("--width", type=int)
    render.add_argument("--height", type=int)
    render.add_argument("--audio", help="Optional narration/music file to mux into the render.")
    render.add_argument("--virtual-time-budget", type=int, default=1000)
    render.add_argument("--capture-timeout", type=float, default=30.0)
    render.add_argument("--report", help="Write render metadata JSON. Defaults next to output.")
    render.add_argument("--asset-id", default="final-video", help="Asset id used when registering the rendered MP4.")
    render.add_argument("--frame-dir", help="Use this directory for captured PNG frames.")
    render.add_argument("--keep-frames", action="store_true", help="Keep captured PNG frames after rendering.")
    render.add_argument("--resume", action="store_true", help="Reuse existing non-empty frame PNGs in --frame-dir.")
    render.add_argument("--capture-mode", default="persistent", choices=["persistent", "process"], help="Use one persistent Chrome session or one process per frame.")
    render.add_argument("--parallel", type=int, default=1, help="Capture multiple frames concurrently with separate Chrome processes.")
    render.add_argument("--quiet", action="store_true")
    render.set_defaults(func=command_render)

    inspect = sub.add_parser("inspect", help="Capture sample frames from an HTML composition.")
    inspect.add_argument("project", nargs="?", default=".")
    inspect.add_argument("--samples", type=int, default=5)
    inspect.add_argument("--duration", type=float)
    inspect.add_argument("--width", type=int)
    inspect.add_argument("--height", type=int)
    inspect.add_argument("--output-dir")
    inspect.add_argument("--report")
    inspect.add_argument("--virtual-time-budget", type=int, default=1000)
    inspect.add_argument("--capture-timeout", type=float, default=30.0)
    inspect.set_defaults(func=command_inspect)

    frame_quality = sub.add_parser("frame-quality-audit", help="Audit inspect/site screenshots for blank frames and leaked internal copy.")
    frame_quality.add_argument("--project", required=True)
    frame_quality.add_argument("--image", action="append", help="Specific PNG frame to audit. Relative paths resolve against --project.")
    frame_quality.add_argument("--max-images", type=int, default=6)
    frame_quality.add_argument("--output")
    frame_quality.add_argument("--json", action="store_true")
    frame_quality.add_argument("--strict", action="store_true", help="Exit with an error when local frame quality is unsafe.")
    frame_quality.set_defaults(func=command_frame_quality_audit)

    video_create = sub.add_parser("video-create", help="Create a SenseAudio video generation task.")
    add_common_video(video_create)
    video_create.set_defaults(func=command_video_create)

    video_status = sub.add_parser("video-status", help="Check or poll a video generation task.")
    video_status.add_argument("--task-id", required=True)
    video_status.add_argument("--poll", action="store_true")
    video_status.add_argument("--interval", type=int, default=8)
    video_status.add_argument("--timeout", type=int, default=1800)
    video_status.add_argument("--download")
    video_status.add_argument("--output")
    video_status.set_defaults(func=command_video_status)

    music_create = sub.add_parser("music-create", help="Create a SenseAudio music generation task for background beds.")
    music_create.add_argument("--prompt", required=True)
    music_create.add_argument("--lyrics")
    music_create.add_argument("--style", default="minimal cinematic ambient, subtle pulse, premium website explainer")
    music_create.add_argument("--title")
    music_create.add_argument("--duration", type=int, default=16)
    music_create.add_argument("--negative-tags", default="loud vocals, harsh drums, distorted lead, crowded arrangement")
    music_create.add_argument("--instrumental", action=argparse.BooleanOptionalAction, default=True)
    music_create.add_argument("--model", default=DEFAULT_MUSIC_MODEL)
    music_create.add_argument("--reference-id")
    music_create.add_argument("--vocal-id")
    music_create.add_argument("--vocal-gender", choices=["f", "m"], help="Official SenseAudio vocal gender field for non-instrumental songs.")
    music_create.add_argument("--use-variance", action=argparse.BooleanOptionalAction, default=False)
    music_create.add_argument("--callback-url")
    music_create.add_argument("--poll", action="store_true")
    music_create.add_argument("--interval", type=int, default=10)
    music_create.add_argument("--timeout", type=int, default=600)
    music_create.add_argument("--download")
    music_create.add_argument("--project")
    music_create.add_argument("--asset-id", default="background-music")
    music_create.add_argument("--manifest")
    music_create.add_argument("--dry-run", action="store_true")
    music_create.set_defaults(func=command_music_create)

    music_status = sub.add_parser("music-status", help="Check or poll a SenseAudio music generation task.")
    music_status.add_argument("--id", required=True)
    music_status.add_argument("--poll", action="store_true")
    music_status.add_argument("--interval", type=int, default=10)
    music_status.add_argument("--timeout", type=int, default=600)
    music_status.add_argument("--download")
    music_status.add_argument("--project")
    music_status.add_argument("--asset-id", default="background-music")
    music_status.add_argument("--output")
    music_status.add_argument("--dry-run", action="store_true")
    music_status.set_defaults(func=command_music_status)

    for name, async_mode in (("image-sync", False), ("image-async", True)):
        image = sub.add_parser(name, help=f"Generate an image through SenseAudio {'async' if async_mode else 'sync'} API.")
        image.add_argument("--model", default=DEFAULT_IMAGE_MODEL)
        image.add_argument("--prompt", required=True)
        image.add_argument("--size", default="1328x1328")
        image.add_argument("--reference")
        image.add_argument("--seed", type=int)
        image.add_argument("--download")
        image.add_argument("--manifest")
        image.add_argument("--dry-run", action="store_true")
        image.set_defaults(func=lambda args, async_mode=async_mode: command_image(args, async_mode))

    tts = sub.add_parser("tts", help="Generate narration audio via SenseAudio TTS.")
    tts.add_argument("--text")
    tts.add_argument("--text-file")
    tts.add_argument("--voice-id", required=True)
    tts.add_argument("--model", default=DEFAULT_TTS_MODEL)
    tts.add_argument("--speed", type=float, default=1.0)
    tts.add_argument("--volume", type=float, default=1.0)
    tts.add_argument("--pitch", type=int, default=0)
    tts.add_argument("--latex-read", action="store_true")
    tts.add_argument("--format", default="mp3", choices=["mp3", "wav", "pcm", "flac"])
    tts.add_argument("--sample-rate", type=int, default=32000)
    tts.add_argument("--bitrate", type=int, default=128000)
    tts.add_argument("--channel", type=int, default=2)
    tts.add_argument("--output", required=True)
    tts.add_argument("--manifest")
    tts.add_argument("--dry-run", action="store_true")
    tts.set_defaults(func=command_tts)

    asr = sub.add_parser("asr", help="Transcribe audio/video via SenseAudio ASR.")
    asr.add_argument("--file", required=True)
    asr.add_argument("--model", default=DEFAULT_ASR_MODEL)
    asr.add_argument("--language")
    asr.add_argument("--response-format", default="json", choices=["json", "text", "verbose_json"])
    asr.add_argument("--timestamps", help="Comma-separated timestamp granularities: word,segment")
    asr.add_argument("--enable-punctuation", action="store_true")
    asr.add_argument("--normalize-words", action=argparse.BooleanOptionalAction, default=True)
    asr.add_argument("--output")
    asr.add_argument("--dry-run", action="store_true")
    asr.set_defaults(func=command_asr)

    voices = sub.add_parser("voices", help="List account-visible SenseAudio voices.")
    voices.add_argument("--voice-type", default="all", choices=["system", "voice_clone", "voice_generation", "all"])
    voices.add_argument("--output")
    voices.add_argument("--dry-run", action="store_true")
    voices.set_defaults(func=command_voices)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        args.func(args)
        return 0
    except SenseAudioError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

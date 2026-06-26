#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小剪刀整合桥接脚本 (Bridge.py)
用于 OpenClaw 的一键式调用，内部处理上传、轮询和加解密。
"""

import sys
import json
import os
import time
import argparse
import requests
from typing import Dict, Any, Iterator

# 将当前目录加入 python path 以便导入 client.py, crypto.py 和 oss_upload.py
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from client import HookHttpClient
from oss_upload import oss_upload

# 内置配置
BASE_URL = "https://biyi.cxtfun.com"
PKG_NAME = "com.biyi.mscissors"
CUTFLOW_BASE_URL = "https://api-cutflow.fun.tv"

# 音色名称映射表 (中文 -> Azure ID)
VOICE_MAPPING = {
    "晓晓": "zh-CN-XiaoxiaoNeural",
    "云希": "zh-CN-YunxiNeural",
    "晓辰": "zh-CN-XiaochenNeural",
    "晓涵": "zh-CN-XiaohanNeural",
    "晓墨": "zh-CN-XiaomoNeural",
    "晓睿": "zh-CN-XiaoruiNeural",
    "晓萱": "zh-CN-XiaoxuanNeural",
    "晓悠": "zh-CN-XiaoyouNeural",
    "云枫": "zh-CN-YunfengNeural",
    "云皓": "zh-CN-YunhaoNeural",
    "云健": "zh-CN-YunjianNeural",
    "云泽": "zh-CN-YunzeNeural",
}

def resolve_voice_id(name: str) -> str:
    """将中文音色名解析为 Azure Voice ID"""
    if not name:
        return "zh-CN-XiaoxiaoNeural"
    if name.startswith("zh-CN-"):
        return name
    if name in VOICE_MAPPING:
        return VOICE_MAPPING[name]
    for k, v in VOICE_MAPPING.items():
        if k in name:
            return v
    return name

def get_token(args):
    """从参数或环境变量获取 Token"""
    token = args.token
    if not token:
        token = os.environ.get("XJD_TOKEN") or os.environ.get("BIYI_TOKEN")
    return token

class MScissorsBridge:
    def __init__(self, token: str):
        self.token = token
        self.client = HookHttpClient(
            base_url=BASE_URL,
            pkgname=PKG_NAME,
            appsecret=token
        )

    def create_task(self, filename: str = "openclaw_task.mp4"):
        payload = {
            "file_name": filename,
            "timestamp": int(time.time() * 1000),
            "tpl_code": "hook",
            "num": 1
        }
        resp = self.client.post("/biyi.srv/user/use.cash.task", payload)
        return resp

    def upload_and_create_task(self, file_path: str):
        print(f"DEBUG: Uploading {file_path}...")
        upload_res = oss_upload(file_path)
        if not upload_res["success"]:
            return upload_res
        
        url = upload_res["url"]
        print(f"DEBUG: Creating task for {url}...")
        task_res = self.create_task(os.path.basename(file_path))
        if task_res.get("err_code") != -1:
            return task_res
            
        data = task_res.get("data", {})
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except:
                pass
        
        task_id = data.get("task_id")
        return {"success": True, "url": url, "task_id": task_id, "raw_task": task_res}

    def analyze_demand(self, task_id: int, video_url: str, prompt: str):
        payload = {
            "task_id": task_id,
            "plot": prompt
        }
        submit = self.client.post("/api/hook/submit/analyze.demand", payload)
        if submit.get("err_code") != -1:
            return submit
        return self.client.poll_task("/api/hook/query/analyze.demand.result", task_id)

    def extract_frames(self, video_url: str, count: int = 15):
        """云端抽帧接口实现 (SSE)"""
        url = f"{CUTFLOW_BASE_URL}/qlapi.srv/video/extract-frames"
        headers = {
            "Authorization": f"Bearer:{self.token}",
            "Content-Type": "application/json"
        }
        payload = {"video_url": video_url, "count": count}
        
        frames = []
        try:
            resp = requests.post(url, json=payload, headers=headers, stream=True, timeout=None)
            for line in resp.iter_lines():
                if line:
                    line_str = line.decode("utf-8")
                    if line_str.startswith("data: "):
                        try:
                            event = json.loads(line_str[6:])
                            if "image_url" in event:
                                frames.append(event["image_url"])
                            if "err_code" in event and event["err_code"] == -1:
                                return {"success": True, "frames": frames}
                            elif "err_code" in event and event["err_code"] != -1:
                                return {"success": False, "error": event.get("err_message")}
                        except:
                            continue
            return {"success": True, "frames": frames}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def extract_audio(self, video_url: str):
        """云端提取音频接口实现 (SSE)"""
        url = f"{CUTFLOW_BASE_URL}/qlapi.srv/video/extract-audio"
        headers = {
            "Authorization": f"Bearer:{self.token}",
            "Content-Type": "application/json"
        }
        payload = {"video_url": video_url}
        
        audio_url = None
        try:
            resp = requests.post(url, json=payload, headers=headers, stream=True, timeout=None)
            for line in resp.iter_lines():
                if line:
                    line_str = line.decode("utf-8")
                    if line_str.startswith("data: "):
                        try:
                            event = json.loads(line_str[6:])
                            if event.get("step") == "done" and "audio_url" in event:
                                audio_url = event["audio_url"]
                            if "err_code" in event and event["err_code"] == -1:
                                return {"success": True, "audio_url": audio_url}
                            elif "err_code" in event and event["err_code"] != -1:
                                return {"success": False, "error": event.get("err_message")}
                        except:
                            continue
            return {"success": True, "audio_url": audio_url}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def submit_ocr(self, task_id: int, image_urls: list):
        payload = {
            "task_id": task_id,
            "data_type": "url",
            "scene": "general",
            "data_list": image_urls
        }
        return self.client.post("/api/aipkg/submit/volcano.ocr", payload)

    def poll_ocr(self, client_id: str):
        return self.client.poll_task("/api/aipkg/query/volcano.ocr.result", client_id, id_field="client_id")

    def asr(self, task_id: int, video_url: str) -> Dict[str, Any]:
        """将视频音频提取为SRT字幕文本 (完全云端化)"""
        # 1. 云端提取音频
        audio_res = self.extract_audio(video_url)
        if not audio_res.get("success"):
            return {"err_code": 1, "err_message": f"Cloud audio extraction failed: {audio_res.get('error')}"}
        
        file_url = audio_res["audio_url"]
        
        # 2. 提交ASR任务
        submit_payload = {
            "task_id": task_id,
            "file_url": file_url
        }
        submit_res = self.client.post("/api/aipkg/submit/volcano.auc", submit_payload)
        if submit_res.get("err_code") != -1:
            return submit_res
        
        client_id = submit_res.get("data", {}).get("client_id")
        if not client_id:
            return {"err_code": 1, "err_message": "No client_id from ASR submit"}
        
        # 3. 轮询结果
        poll_res = self.client.poll_task(
            "/api/aipkg/query/volcano.auc.result",
            client_id,
            id_field="client_id",
            interval=3,
            timeout=300
        )
        
        if poll_res.get("err_code") == -1:
            data = poll_res.get("data", {})
            text = data.get("text", "")
            return {"err_code": -1, "err_message": "success", "data": {"text": text}}
        
        return poll_res

    def calculate_subtitle_pos(self, ocr_results: list, video_width: int, video_height: int):
        payload = {
            "results": ocr_results,
            "video_width": video_width,
            "video_height": video_height
        }
        return self.client.post("/api/aipkg/calc/subtitle.pos.by.ocr", payload)

    @staticmethod
    def format_milliseconds_to_srt(milliseconds: int) -> str:
        total_ms = abs(milliseconds)
        hours = total_ms // (60 * 60 * 1000)
        minutes = (total_ms % (60 * 60 * 1000)) // (60 * 1000)
        seconds = (total_ms % (60 * 1000)) // 1000
        millis = total_ms % 1000
        sign = "-" if milliseconds < 0 else ""
        return f"{sign}{hours:02d}:{minutes:02d}:{seconds:02d},{millis:03d}"

    def utterances_to_srt(self, utterances: list) -> str:
        srt_content = ""
        for idx, utt in enumerate(utterances, 1):
            start = self.format_milliseconds_to_srt(utt.get("start_time", 0))
            end = self.format_milliseconds_to_srt(utt.get("end_time", 0))
            text = utt.get("text", "").strip()
            srt_content += f"{idx}\n{start} --> {end}\n{text}\n\n"
        return srt_content

    def ai_clipping(self, task_id: int, video_url: str, audio_url: str, analysis: Dict[str, Any]):
        data_root = analysis.get("data", {}) if isinstance(analysis.get("data"), dict) else {}
        result = analysis.get("result") or data_root.get("result") or analysis.get("data") or analysis or {}
        
        clip_duration = result.get("clip_duration") or "60秒"
        jianji_prompt = result.get("jianji_prompt") or "精彩精华片段"
        jieshuo_prompt = result.get("jieshuo_prompt") or "无"
        
        long_lines = result.get("long_lines") or result.get("text")
        if not long_lines:
            asr_res = self.asr(task_id, video_url)
            if asr_res.get("err_code") == -1:
                asr_data = asr_res.get("data", {})
                asr_text_raw = asr_data.get("text", "")
                if asr_text_raw:
                    try:
                        asr_text_obj = json.loads(asr_text_raw)
                        utterances = asr_text_obj.get("utterances", [])
                        if utterances:
                            long_lines = self.utterances_to_srt(utterances)
                    except:
                        long_lines = asr_text_raw
            else:
                return {"success": False, "error": f"ASR failed: {asr_res.get('err_message')}"}

        if not long_lines:
             return {"success": False, "error": "ASR text is empty."}

        payload = {
            "task_id": task_id,
            "long_lines": long_lines, 
            "clip_duration": clip_duration,
            "jianji_prompt": jianji_prompt,
            "jieshuo_prompt": jieshuo_prompt
        }
        submit = self.client.post("/api/hook/submit/intelligent.slice.engine", payload)
        if submit.get("err_code") != -1:
            return submit
        return self.client.poll_task("/api/hook/query/intelligent.slice.engine.result", task_id)

    def ai_commentary(self, task_id: int, clip_result: Dict[str, Any]):
        data_root = clip_result.get("data", {}) if isinstance(clip_result.get("data"), dict) else {}
        result = clip_result.get("result") or data_root.get("result") or clip_result.get("data") or {}
        cut_story = result.get("cut_story") or result.get("cut_stroy") or ""
        short_lines = result.get("text") or result.get("short_lines") or ""
        
        payload = {"task_id": task_id, "cut_story": cut_story, "short_lines": short_lines}
        submit = self.client.post("/api/hook/submit/commentary.script", payload)
        if submit.get("err_code") != -1:
            return submit
        return self.client.poll_task("/api/hook/query/commentary.script.result", task_id)

    def tts(self, task_id: int, texts: list, voice: str):
        voice_id = resolve_voice_id(voice)
        processed_texts = []
        for item in texts:
            if isinstance(item, dict):
                val = item.get("text") or item.get("narration") or ""
                if val:
                    processed_texts.append(str(val))
            else:
                processed_texts.append(str(item))
        
        payload = {"task_id": task_id, "texts": processed_texts, "voice": voice_id, "style": "default"}
        submit = self.client.post("/api/aipkg/submit/azure.tts.texts", payload)
        if submit.get("err_code") != -1:
            return submit
        client_id = submit.get("data", {}).get("client_id")
        return self.client.poll_task("/api/aipkg/query/azure.tts.texts.result", client_id, id_field="client_id")

    def recommend_voice(self, task_id: int, clip_result: Dict[str, Any]):
        data_root = clip_result.get("data", {}) if isinstance(clip_result.get("data"), dict) else {}
        result = clip_result.get("result") or data_root.get("result") or clip_result.get("data") or {}
        cut_story = result.get("cut_story") or result.get("cut_stroy") or ""
        payload = {"task_id": task_id, "cut_story": cut_story}
        submit = self.client.post("/api/hook/submit/voice.recommend", payload)
        if submit.get("err_code") != -1:
            return submit
        return self.client.poll_task("/api/hook/query/voice.recommend.result", task_id)

    def recommend_bgm(self, task_id: int, clip_result: Dict[str, Any]):
        data_root = clip_result.get("data", {}) if isinstance(clip_result.get("data"), dict) else {}
        result = clip_result.get("result") or data_root.get("result") or clip_result.get("data") or {}
        cut_story = result.get("cut_story") or result.get("cut_stroy") or ""
        payload = {"task_id": task_id, "cut_story": cut_story}
        submit = self.client.post("/api/hook/submit/bgm.recommend", payload)
        if submit.get("err_code") != -1:
            return submit
        return self.client.poll_task("/api/hook/query/bgm.recommend.result", task_id)

    def final_compose(self, payload: Dict[str, Any]):
        """视频最终合成接口 (根据 payload 自动路由)"""
        # 如果 payload 中包含 srt_text 且没有 audio_url，说明是简易合成模式
        if "srt_text" in payload and "audio_url" not in payload:
            url = f"{CUTFLOW_BASE_URL}/qlapi.srv/video/compose"
        else:
            url = f"{CUTFLOW_BASE_URL}/qlapi.srv/hook/final-compose"
            
        headers = {
            "Authorization": f"Bearer:{self.token}",
            "Content-Type": "application/json"
        }
        final_res = {}
        try:
            resp = requests.post(url, json=payload, headers=headers, stream=True, timeout=None)
            for line in resp.iter_lines():
                if line:
                    line_str = line.decode("utf-8")
                    if line_str.startswith("data: "):
                        try:
                            event = json.loads(line_str[6:])
                            if "step" in event:
                                print(f"DEBUG: Step [{event['step']}]: {event.get('message', '')}")
                            if "video_url" in event:
                                final_res.update(event)
                            if "err_code" in event and event["err_code"] == -1:
                                final_res.update(event)
                            elif "err_code" in event and event["err_code"] != -1:
                                return event
                        except:
                            continue
            # 修复 URL 转义问题：
            # 1. JSON 中的 \u0026 解码为 &
            # 2. OSS URL path 中的 %2F 解码为 /（签名验证用的是解码后的 path）
            # 3. 仅对 URL query string 中的 & 进行 HTML-escape (& -> &amp;)
            #    防止飞书在 HTML 上下文中将 & 转义为 &amp; 而非 &amp;
            def decode_urls(obj):
                if isinstance(obj, dict):
                    for k, v in obj.items():
                        if isinstance(v, str):
                            decoded = v.replace('\\u0026', '&')
                            if '://' in decoded and '=' in decoded and '%2F' in decoded:
                                # URL 中 path 包含 %2F，需要解码为 / 以匹配 OSS 签名
                                # from urllib.parse import urlparse, parse_qs, urlencode, unquote
                                # parsed = urlparse(decoded)
                                # 解码 path 中的 %2F -> /
                                # decoded_path = unquote(parsed.path)
                                # 重新组装，query 参数保持原样（避免重复编码）
                                # decoded = f"{parsed.scheme}://{parsed.netloc}{decoded_path}"
                                # if parsed.query:
                                #     decoded += f"?{parsed.query}"
                                pass
                                # 修复完成后，query 中的 & -> &amp;（飞书 HTML 转义）
                                # if '&' in decoded:
                                #     # 找到 ? 的位置，分离 path 和 query
                                #     qmark = decoded.index('?')
                                #     path_s, query_s = decoded[:qmark], decoded[qmark+1:]
                                #     query_fixed = query_s.replace('&', '&amp;')
                                #     decoded = path_s + '?' + query_fixed
                            obj[k] = decoded
                        elif isinstance(v, (dict, list)):
                            decode_urls(v)
                elif isinstance(obj, list):
                    for i, item in enumerate(obj):
                        if isinstance(item, str):
                            decoded = item.replace('\\u0026', '&')
                            # if '://' in decoded and '=' in decoded and '%2F' in decoded:
                            #     from urllib.parse import urlparse, unquote
                            #     parsed = urlparse(decoded)
                            #     decoded_path = unquote(parsed.path)
                            #     decoded = f"{parsed.scheme}://{parsed.netloc}{decoded_path}"
                            #     if parsed.query:
                            #         decoded += f"?{parsed.query}"
                            #     # if '&' in decoded:
                            #     #     qmark = decoded.index('?')
                            #     #     query_fixed = decoded[qmark+1:].replace('&', '&amp;')
                            #     #     decoded = decoded[:qmark+1] + query_fixed
                            obj[i] = decoded
                        elif isinstance(item, (dict, list)):
                            decode_urls(item)
            decode_urls(final_res)
            return final_res
        except Exception as e:
            return {"err_code": 500, "err_message": f"Final compose request failed: {str(e)}"}

def main():
    parser = argparse.ArgumentParser(description="MScissors Bridge for OpenClaw")
    parser.add_argument("action", choices=["upload_task", "analyze", "clip", "commentary", "tts", "recommend_voice", "recommend_bgm", "final_compose", "mid_compose", "asr", "extract_frames", "extract_audio"])
    parser.add_argument("--file", help="Local file path")
    parser.add_argument("--task_id", type=int, help="Task ID")
    parser.add_argument("--url", help="OSS URL")
    parser.add_argument("--audio_url", help="Audio OSS URL")
    parser.add_argument("--voice_name", help="Voice name")
    parser.add_argument("--prompt", help="User demand")
    parser.add_argument("--analysis_json", help="Analysis JSON string")
    parser.add_argument("--clip_json", help="Clip JSON string")
    parser.add_argument("--texts_json", help="TTS texts JSON string")
    parser.add_argument("--payload_json", help="Final Compose payload JSON string")
    
    # 中间合成参数
    parser.add_argument("--srt_text", help="SRT text for intermediate compose")
    
    # Final Compose 独立参数
    parser.add_argument("--video_path", help="Original video URL")
    parser.add_argument("--commentary_srt_path", help="Commentary SRT URL")
    parser.add_argument("--audio_zip", help="Audio ZIP URL")
    parser.add_argument("--batch_size", type=int, default=1, help="Audio count in ZIP")
    parser.add_argument("--bgm_path", help="BGM URL")
    parser.add_argument("--bgm_volume", type=int, default=30, help="BGM volume (0-100)")
    parser.add_argument("--enable_transitions", type=bool, default=True, help="Enable transitions")
    parser.add_argument("--subtitle_mask_x", type=int, default=0, help="Subtitle mask X")
    parser.add_argument("--subtitle_mask_y", type=int, default=0, help="Subtitle mask Y")
    parser.add_argument("--subtitle_mask_width", type=int, default=0, help="Subtitle mask Width")
    parser.add_argument("--subtitle_mask_height", type=int, default=0, help="Subtitle mask Height")

    parser.add_argument("--count", type=int, default=15, help="Frame count")
    parser.add_argument("--token", help="API Token for MScissors")
    
    args = parser.parse_args()
    token = get_token(args)
    if not token:
        # 如果没有 Token，返回一个标准的 401 错误，让 Agent 知道该向用户索要了
        print(json.dumps({"err_code": 401, "err_message": "Token missing. Please provide a valid token in the conversation.", "success": False}, ensure_ascii=False))
        sys.exit(0) # 正常退出，由 Agent 解析输出
        
    bridge = MScissorsBridge(token)
    try:
        if args.action == "upload_task":
            res = bridge.upload_and_create_task(args.file)
        elif args.action == "analyze":
            res = bridge.analyze_demand(args.task_id, args.url, args.prompt)
        elif args.action == "clip":
            analysis = json.loads(args.analysis_json) if args.analysis_json else {}
            res = bridge.ai_clipping(args.task_id, args.url, args.audio_url, analysis)
        elif args.action == "commentary":
            clip_res = json.loads(args.clip_json) if args.clip_json else {}
            res = bridge.ai_commentary(args.task_id, clip_res)
        elif args.action == "tts":
            texts = json.loads(args.texts_json) if args.texts_json else []
            res = bridge.tts(args.task_id, texts, args.voice_name)
        elif args.action == "recommend_voice":
            clip_res = json.loads(args.clip_json) if args.clip_json else {}
            res = bridge.recommend_voice(args.task_id, clip_res)
        elif args.action == "recommend_bgm":
            clip_res = json.loads(args.clip_json) if args.clip_json else {}
            res = bridge.recommend_bgm(args.task_id, clip_res)
        elif args.action == "asr":
            res = bridge.asr(args.task_id, args.url)
        elif args.action == "extract_frames":
            res = bridge.extract_frames(args.url, args.count)
        elif args.action == "extract_audio":
            res = bridge.extract_audio(args.url)
        elif args.action == "final_compose":
            if args.payload_json:
                payload = json.loads(args.payload_json)
            else:
                payload = {
                    "task_id": args.task_id,
                    "video_path": args.video_path or args.url,
                    "commentary_srt_path": args.commentary_srt_path,
                    "audio_zip": args.audio_zip or args.audio_url,
                    "batch_size": args.batch_size,
                    "bgm_path": args.bgm_path,
                    "bgm_volume": args.bgm_volume,
                    "enable_transitions": args.enable_transitions,
                    "subtitle_mask_x": args.subtitle_mask_x,
                    "subtitle_mask_y": args.subtitle_mask_y,
                    "subtitle_mask_width": args.subtitle_mask_width,
                    "subtitle_mask_height": args.subtitle_mask_height
                }
            res = bridge.final_compose(payload)
        elif args.action == "mid_compose":
            payload = {
                "task_id": args.task_id,
                "video_url": args.url,
                "srt_text": args.srt_text
            }
            res = bridge.final_compose(payload)
        else:
            res = {"success": False, "error": "Action not implemented"}
        print(json.dumps(res, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}))
        sys.exit(1)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Suno API 音乐生成客户端
基于 https://docs.sunoapi.org/cn/suno-api/ 文档

用法:
    export SUNO_API_KEY="your_key_here"
    
    # 生成音乐
    suno.py generate --prompt "一首安静的钢琴曲" --no-custom
    
    # 上传翻唱
    suno.py upload-cover --url "https://..." --prompt "翻唱版本" --style pop
    
    # 上传延长
    suno.py upload-extend --url "https://..." --style pop
    
    # 查询状态
    suno.py status --task-id "xxx"
    
    # 获取积分
    suno.py credits
    
    # 提升音乐风格
    suno.py boost-style --content "创造一首富有旋律性的深度浩室歌曲"
"""

import argparse
import json
import os
import sys
import time
from typing import List, Optional

import requests

BASE_URL = os.getenv("SUNO_BASE_URL", "https://api.sunoapi.org")
API_KEY = os.getenv("SUNO_API_KEY", "")

VALID_MODELS = ["V4", "V4_5", "V4_5ALL", "V4_5PLUS", "V5", "V5_5"]


def _headers() -> dict:
    h = {"Content-Type": "application/json"}
    if API_KEY:
        h["Authorization"] = f"Bearer {API_KEY}"
    return h


def _post(path: str, data: dict) -> dict:
    r = requests.post(f"{BASE_URL}{path}", headers=_headers(), json=data, timeout=120)
    r.raise_for_status()
    return r.json()


def _get(path: str, params: dict = None) -> dict:
    r = requests.get(f"{BASE_URL}{path}", headers=_headers(), params=params, timeout=30)
    r.raise_for_status()
    return r.json()


def _extract_suno(result: dict) -> list:
    data = result.get("data")
    if not isinstance(data, dict):
        return []
    resp = data.get("response")
    if not isinstance(resp, dict):
        return []
    sd = resp.get("sunoData")
    return sd if isinstance(sd, list) else []


def _fmt(data: list) -> str:
    lines = []
    for s in data:
        lines.append(f"ID:      {s.get('id', '?')}")
        lines.append(f"  标题:  {s.get('title', 'N/A')}")
        lines.append(f"  音频:  {s.get('audioUrl', '') or 'pending'}")
        lines.append(f"  封面:  {s.get('imageUrl', '') or 'pending'}")
        lines.append(f"  时长:  {s.get('duration', '?')}s")
        lines.append("")
    return "\n".join(lines)


# ========== API 函数 ==========


def generate(prompt="", style="", title="", model="V5_5",
             instrumental=False, custom_mode=True, callback="",
             negative_tags="", vocal_gender="",
             persona_id="", persona_model="",
             style_weight=None, weirdness=None, audio_weight=None):
    """POST /api/v1/generate - 生成音乐"""
    d = {"customMode": custom_mode, "instrumental": instrumental,
         "model": model, "callBackUrl": callback or "https://sunoapi.org"}
    if custom_mode:
        d["style"] = style or "pop"
        d["title"] = title or prompt[:50]
        if not instrumental:
            d["prompt"] = prompt
    else:
        d["prompt"] = prompt
    if negative_tags: d["negativeTags"] = negative_tags
    if vocal_gender: d["vocalGender"] = vocal_gender
    if persona_id:
        d["personaId"] = persona_id
        d["personaModel"] = persona_model or "style_persona"
    if style_weight is not None: d["styleWeight"] = style_weight
    if weirdness is not None: d["weirdnessConstraint"] = weirdness
    if audio_weight is not None: d["audioWeight"] = audio_weight
    return _post("/api/v1/generate", d)


def extend(audio_id="", prompt="", style="", title="", continue_at=60,
           model="V5_5", use_default=False, callback="",
           instrumental=False, persona_id="", persona_model=""):
    """POST /api/v1/generate/extend - 延长音乐"""
    d = {"audioId": audio_id, "model": model,
         "callBackUrl": callback or "https://sunoapi.org",
         "defaultParamFlag": not use_default}
    if not use_default:
        d["continueAt"] = continue_at
        d["prompt"] = prompt or "Continue with same style"
        d["style"] = style or "pop"
        d["title"] = title or "Extended"
        if instrumental: d["instrumental"] = True
    if persona_id:
        d["personaId"] = persona_id
        d["personaModel"] = persona_model or "style_persona"
    return _post("/api/v1/generate/extend", d)


def upload_cover(upload_url="", prompt="", style="", title="", model="V5_5",
                 instrumental=False, custom_mode=True, callback="",
                 negative_tags="", vocal_gender=""):
    """POST /api/v1/generate/upload-cover - 上传翻唱"""
    d = {"uploadUrl": upload_url, "customMode": custom_mode,
         "instrumental": instrumental, "model": model,
         "callBackUrl": callback or "https://sunoapi.org"}
    if custom_mode:
        d["style"] = style or "pop"
        d["title"] = title or "Cover"
        if not instrumental: d["prompt"] = prompt
    else:
        d["prompt"] = prompt
    if negative_tags: d["negativeTags"] = negative_tags
    if vocal_gender: d["vocalGender"] = vocal_gender
    return _post("/api/v1/generate/upload-cover", d)


def upload_extend(upload_url="", prompt="", style="", title="", model="V5_5",
                  instrumental=False, use_default=False, callback=""):
    """POST /api/v1/generate/upload-extend - 上传延长"""
    d = {"uploadUrl": upload_url, "model": model,
         "callBackUrl": callback or "https://sunoapi.org",
         "defaultParamFlag": not use_default}
    if not use_default:
        d["style"] = style or "pop"
        d["title"] = title or "Extended"
        d["prompt"] = prompt or "Extend this music"
        if instrumental: d["instrumental"] = True
    else:
        d["prompt"] = prompt or "Extend this music"
    return _post("/api/v1/generate/upload-extend", d)


def add_instrumental(upload_url="", title="", tags="", negative_tags="",
                     model="V4_5PLUS", callback="", vocal_gender="",
                     style_weight=None, weirdness=None, audio_weight=None):
    """POST /api/v1/generate/add-instrumental - 添加乐器版"""
    d = {"uploadUrl": upload_url, "title": title, "tags": tags,
         "negativeTags": negative_tags or "",
         "callBackUrl": callback or "https://sunoapi.org"}
    if model: d["model"] = model
    if vocal_gender: d["vocalGender"] = vocal_gender
    if style_weight is not None: d["styleWeight"] = style_weight
    if weirdness is not None: d["weirdnessConstraint"] = weirdness
    if audio_weight is not None: d["audioWeight"] = audio_weight
    return _post("/api/v1/generate/add-instrumental", d)


def add_vocals(upload_url="", title="", tags="", negative_tags="",
               model="V4_5PLUS", callback="", vocal_gender=""):
    """POST /api/v1/generate/add-vocals - 添加人声"""
    d = {"uploadUrl": upload_url, "title": title, "tags": tags,
         "negativeTags": negative_tags or " ",
         "callBackUrl": callback or "https://sunoapi.org"}
    if model: d["model"] = model
    if vocal_gender: d["vocalGender"] = vocal_gender
    return _post("/api/v1/generate/add-vocals", d)


def replace_section(task_id="", audio_id="", prompt="", tags="", title="",
                    infill_start=0, infill_end=30, negative_tags="", callback=""):
    """POST /api/v1/generate/replace-section - 替换段落"""
    d = {"taskId": task_id, "audioId": audio_id, "prompt": prompt,
         "tags": tags, "title": title,
         "infillStartS": infill_start, "infillEndS": infill_end}
    if negative_tags: d["negativeTags"] = negative_tags
    if callback: d["callBackUrl"] = callback
    return _post("/api/v1/generate/replace-section", d)


def check_status(task_id=""):
    """GET /api/v1/generate/record-info - 查询状态"""
    return _get("/api/v1/generate/record-info", {"taskId": task_id})


def credits():
    """GET /api/v1/generate/credit - 剩余积分"""
    return _get("/api/v1/generate/credit")


def get_lyrics(task_id="", audio_id=""):
    """POST /api/v1/generate/get-timestamped-lyrics - 时间戳歌词"""
    return _post("/api/v1/generate/get-timestamped-lyrics",
                 {"taskId": task_id, "audioId": audio_id})


def boost_style(content=""):
    """POST /api/v1/style/generate - 提升音乐风格描述"""
    return _post("/api/v1/style/generate", {"content": content})


def generate_persona(task_id="", audio_id="", name="", description="",
                     style="", vocal_start=None, vocal_end=None):
    """POST /api/v1/generate/generate-persona - 生成 Persona"""
    d = {"taskId": task_id, "audioId": audio_id,
         "name": name, "description": description}
    if style: d["style"] = style
    if vocal_start is not None: d["vocalStart"] = vocal_start
    if vocal_end is not None: d["vocalEnd"] = vocal_end
    return _post("/api/v1/generate/generate-persona", d)


def generate_mashup(url_list=None, prompt="", style="", title="", model="V5_5",
                    instrumental=False, custom_mode=True, callback="",
                    vocal_gender="", style_weight=None, weirdness=None, audio_weight=None):
    """POST /api/v1/generate/mashup - 生成混音（必须传2个URL）"""
    d = {"uploadUrlList": url_list or [], "customMode": custom_mode,
         "model": model, "callBackUrl": callback or "https://sunoapi.org"}
    if instrumental: d["instrumental"] = True
    if custom_mode:
        d["style"] = style or "pop"
        d["title"] = title or "Mashup"
        if not instrumental and prompt: d["prompt"] = prompt
    else:
        if prompt: d["prompt"] = prompt
    if vocal_gender: d["vocalGender"] = vocal_gender
    if style_weight is not None: d["styleWeight"] = style_weight
    if weirdness is not None: d["weirdnessConstraint"] = weirdness
    if audio_weight is not None: d["audioWeight"] = audio_weight
    return _post("/api/v1/generate/mashup", d)


def separate_vocals(task_id="", audio_id="", sep_type="separate_vocal", callback=""):
    """POST /api/v1/vocal-removal/generate - 人声分离"""
    return _post("/api/v1/vocal-removal/generate",
                 {"taskId": task_id, "audioId": audio_id,
                  "type": sep_type,
                  "callBackUrl": callback or "https://sunoapi.org"})


def get_separation(task_id=""):
    """GET /api/v1/vocal-removal/record-info - 分离详情"""
    return _get("/api/v1/vocal-removal/record-info", {"taskId": task_id})


def generate_midi(task_id="", audio_id="", callback=""):
    """POST /api/v1/midi/generate - MIDI生成"""
    d = {"taskId": task_id, "callBackUrl": callback or "https://sunoapi.org"}
    if audio_id: d["audioId"] = audio_id
    return _post("/api/v1/midi/generate", d)


def get_midi(task_id=""):
    """GET /api/v1/midi/record-info - MIDI详情"""
    return _get("/api/v1/midi/record-info", {"taskId": task_id})


def create_mp4(task_id="", audio_id="", author="", domain="", callback=""):
    """POST /api/v1/mp4/generate - 音乐视频"""
    d = {"taskId": task_id, "audioId": audio_id,
         "callBackUrl": callback or "https://sunoapi.org"}
    if author: d["author"] = author
    if domain: d["domainName"] = domain
    return _post("/api/v1/mp4/generate", d)


def get_mp4(task_id=""):
    """GET /api/v1/mp4/record-info - 视频详情"""
    return _get("/api/v1/mp4/record-info", {"taskId": task_id})


def cover_art(task_id="", callback=""):
    """POST /api/v1/suno/cover/generate - 封面图片"""
    return _post("/api/v1/suno/cover/generate",
                 {"taskId": task_id, "callBackUrl": callback or "https://sunoapi.org"})


def get_cover_art(task_id=""):
    """GET /api/v1/suno/cover/record-info - 封面详情"""
    return _get("/api/v1/suno/cover/record-info", {"taskId": task_id})


FILE_UPLOAD_BASE = "https://sunoapiorg.redpandaai.co"


def upload_file_stream(file_path="", upload_path="audio/uploads"):
    """POST /api/file-stream-upload - 文件流上传到 Suno 平台
    
    返回: {"success":true, "data": {"downloadUrl": "...", ...}}
    """
    headers = _headers()
    headers.pop("Content-Type", None)  # 让 requests 自动设置 multipart boundary
    with open(file_path, "rb") as f:
        r = requests.post(
            f"{FILE_UPLOAD_BASE}/api/file-stream-upload",
            headers=headers,
            data={"uploadPath": upload_path},
            files={"file": (os.path.basename(file_path), f, "audio/mpeg")},
            timeout=120,
        )
    r.raise_for_status()
    return r.json()


def wait_for_result(task_id="", interval=5, max_polls=60):
    """轮询等待任务完成"""
    for i in range(max_polls):
        r = check_status(task_id)
        if r.get("code") != 200:
            print(f"  [{i+1}] API error")
            time.sleep(interval); continue
        d = r.get("data")
        if not isinstance(d, dict): d = {}
        status = d.get("status", "?")
        err = d.get("errorMessage", "")
        sd = _extract_suno(r)
        if sd:
            all_done = all(s.get("audioUrl") for s in sd)
            for s in sd:
                sid = s.get("id", "?")[:8]
                title = s.get("title", "?")
                audio = s.get("audioUrl", "")
                st = "完成" if audio else status
                print(f"  [{sid}] {st} - {title}")
            if all_done:
                print(f"\n全部完成！共 {len(sd)} 首")
                return r
        else:
            print(f"  [{i+1}] {status} {err}")
            if status in ("GENERATE_AUDIO_FAILED", "CREATE_TASK_FAILED"):
                return r
        time.sleep(interval)
    print("超时")
    return r


# ========== CLI ==========

def main():
    p = argparse.ArgumentParser(description="Suno AI 音乐生成")
    s = p.add_subparsers(dest="cmd", required=True)

    def add(parser, name, **kw):
        return parser.add_parser(name, **kw)

    # generate
    g = add(s, "generate", help="生成音乐")
    g.add_argument("--prompt", default=""); g.add_argument("--style", default="")
    g.add_argument("--title", default=""); g.add_argument("--model", default="V5_5", choices=VALID_MODELS)
    g.add_argument("--instrumental", action="store_true"); g.add_argument("--no-custom", action="store_true")
    g.add_argument("--negative-tags", default=""); g.add_argument("--vocal-gender", default="")
    g.add_argument("--persona-id", default="")

    # upload-cover
    uc = add(s, "upload-cover", help="上传翻唱")
    uc.add_argument("--url", required=True); uc.add_argument("--prompt", default="")
    uc.add_argument("--style", default=""); uc.add_argument("--title", default="")
    uc.add_argument("--model", default="V5_5", choices=VALID_MODELS)
    uc.add_argument("--instrumental", action="store_true"); uc.add_argument("--no-custom", action="store_true")

    # upload-extend
    ue = add(s, "upload-extend", help="上传延长")
    ue.add_argument("--url", required=True); ue.add_argument("--prompt", default="")
    ue.add_argument("--style", default=""); ue.add_argument("--title", default="")
    ue.add_argument("--model", default="V5_5", choices=VALID_MODELS)
    ue.add_argument("--instrumental", action="store_true")
    ue.add_argument("--use-default", action="store_true")

    # extend
    ex = add(s, "extend", help="延长已生成音乐")
    ex.add_argument("--audio-id", required=True); ex.add_argument("--prompt", default="")
    ex.add_argument("--style", default=""); ex.add_argument("--title", default="")
    ex.add_argument("--continue-at", type=float, default=60)
    ex.add_argument("--model", default="V5_5", choices=VALID_MODELS)
    ex.add_argument("--use-default", action="store_true")

    # replace section
    rs = add(s, "replace", help="替换段落")
    rs.add_argument("--task-id", required=True); rs.add_argument("--audio-id", required=True)
    rs.add_argument("--prompt", required=True); rs.add_argument("--tags", required=True)
    rs.add_argument("--title", required=True)
    rs.add_argument("--start", type=float, required=True)
    rs.add_argument("--end", type=float, required=True)
    rs.add_argument("--negative-tags", default="")

    # boost style
    bs = add(s, "boost-style", help="提升风格描述")
    bs.add_argument("--content", required=True)

    # persona
    pn = add(s, "persona", help="生成 Persona")
    pn.add_argument("--task-id", required=True); pn.add_argument("--audio-id", required=True)
    pn.add_argument("--name", required=True); pn.add_argument("--description", required=True)
    pn.add_argument("--style", default=""); pn.add_argument("--vocal-start", type=float)
    pn.add_argument("--vocal-end", type=float)

    # mashup
    mp = add(s, "mashup", help="混音 (需2个URL)")
    mp.add_argument("--urls", required=True, help="逗号分隔2个URL")
    mp.add_argument("--prompt", default=""); mp.add_argument("--style", default="")
    mp.add_argument("--title", default=""); mp.add_argument("--model", default="V5_5", choices=VALID_MODELS)
    mp.add_argument("--instrumental", action="store_true"); mp.add_argument("--no-custom", action="store_true")

    # upload-file
    uf = add(s, "upload-file", help="文件流上传本地文件到 Suno 平台")
    uf.add_argument("--path", required=True, help="本地文件路径")
    uf.add_argument("--upload-path", default="audio/uploads", help="上传路径 (默认 audio/uploads)")

    # separate
    sp = add(s, "separate", help="人声分离")
    sp.add_argument("--task-id", required=True); sp.add_argument("--audio-id", required=True)
    sp.add_argument("--type", default="separate_vocal", choices=["separate_vocal", "split_stem"])
    sp.add_argument("--status", action="store_true", help="查询分离状态")

    # midi
    md = add(s, "midi", help="生成MIDI（需先分离）")
    md.add_argument("--task-id", required=True); md.add_argument("--audio-id", default="")
    md.add_argument("--status", action="store_true", help="查询MIDI状态")

    # mp4
    mv = add(s, "mp4", help="生成音乐视频")
    mv.add_argument("--task-id", required=True); mv.add_argument("--audio-id", required=True)
    mv.add_argument("--author", default="")
    mv.add_argument("--status", action="store_true", help="查询视频状态")

    # cover art
    ca = add(s, "cover-art", help="生成封面图片")
    ca.add_argument("--task-id", required=True)
    ca.add_argument("--status", action="store_true", help="查询封面状态")

    # add-instrumental / add-vocals
    ai = add(s, "add-instrumental", help="上传添加乐器版")
    ai.add_argument("--url", required=True); ai.add_argument("--title", required=True)
    ai.add_argument("--tags", required=True); ai.add_argument("--negative-tags", default="")
    ai.add_argument("--model", default="V4_5PLUS", choices=["V4_5PLUS","V5","V5_5"])

    av = add(s, "add-vocals", help="上传添加人声")
    av.add_argument("--url", required=True); av.add_argument("--title", required=True)
    av.add_argument("--tags", required=True); av.add_argument("--negative-tags", default="")
    av.add_argument("--model", default="V4_5PLUS", choices=["V4_5PLUS","V5","V5_5"])

    # status / credits / lyrics
    add(s, "status", help="查询生成状态").add_argument("--task-id", required=True)
    add(s, "credits", help="获取剩余积分")
    al = add(s, "lyrics", help="获取时间戳歌词")
    al.add_argument("--task-id", required=True); al.add_argument("--audio-id", required=True)

    # generate-and-wait
    gw = add(s, "generate-and-wait", help="生成并等待")
    gw.add_argument("--prompt", default=""); gw.add_argument("--style", default="")
    gw.add_argument("--title", default=""); gw.add_argument("--model", default="V5_5", choices=VALID_MODELS)
    gw.add_argument("--instrumental", action="store_true"); gw.add_argument("--no-custom", action="store_true")
    gw.add_argument("--poll-interval", type=int, default=5); gw.add_argument("--max-polls", type=int, default=60)

    # upload-cover-and-wait
    uw = add(s, "cover-wait", help="上传翻唱并等待")
    uw.add_argument("--url", required=True); uw.add_argument("--prompt", default="")
    uw.add_argument("--style", default=""); uw.add_argument("--title", default="")
    uw.add_argument("--model", default="V5_5", choices=VALID_MODELS)
    uw.add_argument("--instrumental", action="store_true"); uw.add_argument("--no-custom", action="store_true")
    uw.add_argument("--poll-interval", type=int, default=5); uw.add_argument("--max-polls", type=int, default=60)

    args = p.parse_args()

    if not API_KEY and args.cmd != "help":
        print("请设置 SUNO_API_KEY 环境变量", file=sys.stderr)
        sys.exit(1)

    try:
        # ====== 命令分发 ======

        if args.cmd == "generate":
            r = generate(args.prompt, args.style, args.title, args.model,
                         args.instrumental, not args.no_custom,
                         negative_tags=args.negative_tags,
                         vocal_gender=args.vocal_gender,
                         persona_id=args.persona_id)
            print(json.dumps(r, ensure_ascii=False, indent=2))

        elif args.cmd == "upload-cover":
            r = upload_cover(args.url, args.prompt, args.style, args.title,
                             args.model, args.instrumental, not args.no_custom)
            print(json.dumps(r, ensure_ascii=False, indent=2))

        elif args.cmd == "upload-extend":
            r = upload_extend(args.url, args.prompt, args.style, args.title,
                              args.model, args.instrumental, args.use_default)
            print(json.dumps(r, ensure_ascii=False, indent=2))

        elif args.cmd == "extend":
            r = extend(args.audio_id, args.prompt, args.style, args.title,
                       args.continue_at, args.model, args.use_default)
            print(json.dumps(r, ensure_ascii=False, indent=2))

        elif args.cmd == "replace":
            r = replace_section(args.task_id, args.audio_id, args.prompt,
                                args.tags, args.title, args.start, args.end,
                                args.negative_tags)
            print(json.dumps(r, ensure_ascii=False, indent=2))

        elif args.cmd == "boost-style":
            r = boost_style(args.content)
            print(json.dumps(r, ensure_ascii=False, indent=2))

        elif args.cmd == "persona":
            r = generate_persona(args.task_id, args.audio_id, args.name,
                                 args.description, args.style,
                                 args.vocal_start, args.vocal_end)
            print(json.dumps(r, ensure_ascii=False, indent=2))

        
        elif args.cmd == "upload-file":
            if not os.path.exists(args.path):
                print(f"文件不存在: {args.path}", flush=True); sys.exit(1)
            print(f"上传中: {args.path}", flush=True)
            r = upload_file_stream(args.path, args.upload_path)
            if r.get("success") and r.get("data", {}).get("downloadUrl"):
                url = r["data"]["downloadUrl"]
                print(f"上传成功!", flush=True)
                print(f"  URL: {url}", flush=True)
                print(f"  大小: {r['data'].get('fileSize','?')} bytes", flush=True)
            else:
                print(json.dumps(r, ensure_ascii=False, indent=2), flush=True)

        elif args.cmd == "mashup":
            urls = [u.strip() for u in args.urls.split(",") if u.strip()]
            if len(urls) != 2:
                print("需要恰好2个URL，逗号分隔")
                sys.exit(1)
            r = generate_mashup(urls, args.prompt, args.style, args.title,
                                args.model, args.instrumental, not args.no_custom)
            print(json.dumps(r, ensure_ascii=False, indent=2))

        elif args.cmd == "separate":
            if args.status:
                r = get_separation(args.task_id)
            else:
                r = separate_vocals(args.task_id, args.audio_id, args.type)
            print(json.dumps(r, ensure_ascii=False, indent=2))

        elif args.cmd == "midi":
            if args.status:
                r = get_midi(args.task_id)
            else:
                r = generate_midi(args.task_id, args.audio_id)
            print(json.dumps(r, ensure_ascii=False, indent=2))

        elif args.cmd == "mp4":
            if args.status:
                r = get_mp4(args.task_id)
            else:
                r = create_mp4(args.task_id, args.audio_id, args.author)
            print(json.dumps(r, ensure_ascii=False, indent=2))

        elif args.cmd == "cover-art":
            if args.status:
                r = get_cover_art(args.task_id)
            else:
                r = cover_art(args.task_id)
            print(json.dumps(r, ensure_ascii=False, indent=2))

        elif args.cmd == "add-instrumental":
            r = add_instrumental(args.url, args.title, args.tags, args.negative_tags, args.model)
            print(json.dumps(r, ensure_ascii=False, indent=2))

        elif args.cmd == "add-vocals":
            r = add_vocals(args.url, args.title, args.tags, args.negative_tags, args.model)
            print(json.dumps(r, ensure_ascii=False, indent=2))

        elif args.cmd == "status":
            r = check_status(args.task_id)
            sd = _extract_suno(r)
            if sd:
                print(_fmt(sd))
                for s in sd:
                    lyric = s.get("prompt", "")
                    if lyric and len(lyric) > 50:
                        print(f"歌词 ({s.get('title','?')}):")
                        print(lyric[:500])
                        print()
            else:
                print(json.dumps(r, ensure_ascii=False, indent=2))

        elif args.cmd == "credits":
            r = credits()
            if r.get("code") == 200:
                print(f"剩余积分: {r.get('data', '?')}")
            else:
                print(json.dumps(r, ensure_ascii=False, indent=2))

        elif args.cmd == "lyrics":
            r = get_lyrics(args.task_id, args.audio_id)
            print(json.dumps(r, ensure_ascii=False, indent=2))

        elif args.cmd == "generate-and-wait":
            print("生成中...")
            r = generate(args.prompt, args.style, args.title, args.model,
                         args.instrumental, not args.no_custom)
            tid = r.get("data", {}).get("taskId", "")
            if not tid: print(json.dumps(r, ensure_ascii=False, indent=2)); return
            print(f"TaskID: {tid}")
            wait_for_result(tid, args.poll_interval, args.max_polls)

        elif args.cmd == "cover-wait":
            print("翻唱中...")
            r = upload_cover(args.url, args.prompt, args.style, args.title,
                             args.model, args.instrumental, not args.no_custom)
            tid = r.get("data", {}).get("taskId", "")
            if not tid: print(json.dumps(r, ensure_ascii=False, indent=2)); return
            print(f"TaskID: {tid}")
            wait_for_result(tid, args.poll_interval, args.max_polls)

    except requests.RequestException as e:
        print(f"API错误: {e}", file=sys.stderr)
        if hasattr(e, "response") and e.response is not None:
            print(e.response.text[:500], file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

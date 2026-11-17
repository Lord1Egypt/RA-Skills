#!/usr/bin/env python3
"""video_to_screenplay.py — 從視頻/音頻轉錄稿發展全新劇本（創作用）.

Pipeline:
  1. (optional) transcribe audio/video via faster-whisper → SRT
  2. read SRT → plain text transcript
  3. LLM 兩階段:
     a. 故事元素提取: 主題、情緒、角色原型、衝突、視覺意象
     b. 新劇本生成: 基於提取元素，發展成原創故事大綱 + 分場劇本
  4. 輸出: .md (人讀) + .fountain (編劇軟件可導入)

Usage:
  python video_to_screenplay.py --srt input.srt --out-dir ./output
  python video_to_screenplay.py --audio input.mp3 --out-dir ./output
  python video_to_screenplay.py --srt input.srt --out-dir ./output --target-minutes 15
  python video_to_screenplay.py --srt input.srt --out-dir ./output --extract-only
  python video_to_screenplay.py --audio input.mp3 --out-dir ./output --device cuda --compute-type float16
  python video_to_screenplay.py --srt input.srt --out-dir ./output --provider kimi --model kimi-k3

Requires:
  - faster-whisper (for --audio path)
  - LLM API key in openclaw.json (deepseek, kimi, zhipu, longcat, google, agnes)
"""
from __future__ import annotations
import argparse, json, os, re, sys, time
from pathlib import Path

CANDIDATES = [
    os.path.expandvars(r"%ProgramData%\openclaw\openclaw.json"),
    r"G:\OpenClaw_Data\.openclaw\openclaw.json",
    os.path.expanduser("~/.openclaw/openclaw.json"),
    os.path.expanduser("~/AppData/Roaming/openclaw/openclaw.json"),
]
PROVIDERS = {
    "deepseek": ("https://api.deepseek.com/v1", "openai-completions"),
    "kimi":     ("https://api.moonshot.cn/v1", "openai-completions"),
    "zhipu":    ("https://open.bigmodel.cn/api/paas/v4", "openai-completions"),
    "longcat":  ("https://api.longcat.chat/openai/v1", "openai-completions"),
    "google":   ("https://generativelanguage.googleapis.com/v1beta", "google-generative-ai"),
    "agnes":    ("https://apihub.agnes-ai.com/v1", "openai-completions"),
}

def _load_config():
    for path in CANDIDATES:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    print("ERROR: openclaw.json not found", file=sys.stderr); sys.exit(1)

def _get_api_key(provider):
    config = _load_config()
    p = config.get("models", {}).get("providers", {})
    if provider not in p:
        print(f"ERROR: provider '{provider}' not found", file=sys.stderr); sys.exit(1)
    key = p[provider].get("apiKey", "")
    if not key or key == "***":
        print(f"ERROR: no valid apiKey for '{provider}'", file=sys.stderr); sys.exit(1)
    return key

def _call_llm(prompt, system, model="deepseek-v4-flash", provider="deepseek",
               max_tokens=4000, temperature=0.9):
    import urllib.request, urllib.error
    if provider not in PROVIDERS:
        print(f"ERROR: unknown provider '{provider}'", file=sys.stderr); sys.exit(1)
    if provider == "kimi" and model in ("kimi-k3",): temperature = 1.0
    base_url, api_type = PROVIDERS[provider]
    api_key = _get_api_key(provider)
    if api_type == "google-generative-ai":
        body = {"contents": [{"parts": [{"text": f"{system}\n\n{prompt}"}]}],
                "generationConfig": {"temperature": temperature, "maxOutputTokens": max_tokens}}
        url = f"{base_url}/models/{model}:generateContent?key=***}"
        headers = {"Content-Type": "application/json"}
    else:
        body = {"model": model, "messages": [{"role": "system", "content": system},
                {"role": "user", "content": prompt}],
                "temperature": temperature, "max_tokens": max_tokens, "stream": False}
        url = f"{base_url}/chat/completions"
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"),
                                headers=headers, method="POST")
    print(f"  [LLM] {provider}/{model} (max_tokens={max_tokens})...", flush=True)
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            data = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read().decode('utf-8', 'replace')}", file=sys.stderr); sys.exit(1)
    if api_type == "google-generative-ai":
        text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
    else:
        text = data["choices"][0]["message"]["content"].strip()
    return re.sub(r"\n```$", "", re.sub(r"^```[a-z]*\n", "", text))

def srt_to_text(srt_path):
    with open(srt_path, "r", encoding="utf-8") as f: content = f.read()
    lines = []
    for block in re.split(r"\n\s*\n", content):
        block = block.strip()
        if not block: continue
        parts = block.split("\n")
        text = " ".join(parts[2:]).strip() if len(parts) >= 3 else (parts[1].strip() if len(parts) == 2 else parts[0].strip())
        if text: lines.append(text)
    return " ".join(lines)

EXTRACT_SYSTEM = """你是一位資深編劇與故事分析師，專長從口述內容中提煉故事DNA。
請以 JSON 格式輸出：core_themes, emotional_arc, character_archetypes, central_conflicts, visual_motifs, tone_style, narrative_voice, key_quotes, story_seeds。
只輸出 JSON，不要任何其他文字。"""
EXTRACT_PROMPT = "請分析以下轉錄稿，提取故事DNA：\n\n---\n{transcript}\n---\n\n請輸出 JSON。"
SCREENPLAY_SYSTEM = """你是一位專業編劇，擅長將故事素材發展成原創劇本。
輸出格式：1.【故事梗概】2.【人物小傳】3.【分場劇本】（Fountain 格式）
請用繁體中文創作，對白要自然口語。"""
SCREENPLAY_PROMPT = """基於以下故事DNA，創作一個全新的原創劇本。\n【故事DNA】{story_dna_json}\n【創作要求】目標長度：約 {target_minutes} 分鐘｜類型：{genre}｜繁體中文｜至少 {min_scenes} 場"""

def _to_fountain(text):
    out = []
    cb = False
    for line in text.split("\n"):
        s = line.strip()
        if s.startswith("```"): cb = not cb; continue
        if re.match(r"^(INT\.|EXT\.|INT/EXT\.)", s, re.IGNORECASE): out.append(s.upper())
        elif s.startswith("【") and s.endswith("】"):
            scene = s[1:-1]
            out.append((("INT. " + scene) if not re.match(r"^(INT\.|EXT\.)", scene, re.IGNORECASE) else scene).upper())
        elif s.startswith("## "): continue
        elif s.startswith("**") and s.endswith("**"): out.append(s.strip("*").upper())
        else: out.append(line)
    return "\n".join(out)

def run_pipeline(args):
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    if args.srt:
        srt_path = Path(args.srt)
        if not srt_path.exists(): print(f"ERROR: SRT not found", file=sys.stderr); sys.exit(1)
        transcript = srt_to_text(srt_path)
    elif args.audio:
        from faster_whisper import WhisperModel
        audio_path = Path(args.audio)
        if not audio_path.exists(): print(f"ERROR: Audio not found", file=sys.stderr); sys.exit(1)
        srt_path = out_dir / (audio_path.stem + ".srt")
        print(f"[1/4] Transcribing: {audio_path} (device={args.device}, compute={args.compute_type})")
        model = WhisperModel("small", device=args.device, compute_type=args.compute_type)
        segs = list(model.transcribe(str(audio_path), language="zh",
            initial_prompt="繁體中文口述內容。", vad_filter=True, beam_size=1,
            temperature=[0.0], condition_on_previous_text=False)[0])
        def fmt_ts(sec):
            return f"{int(sec//3600):02d}:{int((sec%3600)//60):02d}:{int(sec%60):02d},{int((sec-int(sec))*1000):03d}"
        with open(srt_path, "w", encoding="utf-8") as f:
            for i, seg in enumerate(segs, 1):
                f.write(f"{i}\n{fmt_ts(seg.start)} --> {fmt_ts(seg.end)}\n{seg.text.strip()}\n\n")
        transcript = " ".join(s.text.strip() for s in segs)
        print(f"  {len(segs)} segments, {len(transcript)} chars")
    else:
        print("ERROR: --srt or --audio required", file=sys.stderr); sys.exit(1)
    (out_dir / "transcript.txt").write_text(transcript, encoding="utf-8")
    print(f"[2/4] Extracting story DNA...")
    MAX = 8000
    tp = transcript if len(transcript) <= MAX else transcript[:MAX//2] + "\n...[省略]...\n" + transcript[-MAX//2:]
    dna_text = _call_llm(EXTRACT_PROMPT.format(transcript=tp), EXTRACT_SYSTEM,
                         model=args.model, provider=args.provider, max_tokens=2000, temperature=0.3)
    if not dna_text or len(dna_text) < 10: print("ERROR: empty DNA", file=sys.stderr); sys.exit(1)
    try: dna = json.loads(dna_text)
    except: dna = json.loads(re.search(r"\{.*\}", dna_text, re.DOTALL).group(0)) if re.search(r"\{.*\}", dna_text, re.DOTALL) else {"raw": dna_text}
    (out_dir / "story_dna.json").write_text(json.dumps(dna, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.extract_only: print("  --extract-only: done."); return
    print(f"[3/4] Generating screenplay...")
    script = _call_llm(SCREENPLAY_PROMPT.format(
        story_dna_json=json.dumps(dna, ensure_ascii=False, indent=2),
        target_minutes=args.target_minutes, genre=args.genre, min_scenes=max(3, args.target_minutes // 3)),
        SCREENPLAY_SYSTEM, model=args.model, provider=args.provider, max_tokens=args.max_tokens, temperature=0.9)
    if not script or len(script) < 50: print("ERROR: empty screenplay", file=sys.stderr); sys.exit(1)
    (out_dir / "screenplay.md").write_text(f"# 原創劇本\n\n> 啟發來源: {args.srt or args.audio}\n> 生成時間: {time.strftime('%Y-%m-%d %H:%M')}\n\n{script}", encoding="utf-8")
    (out_dir / "screenplay.fountain").write_text(_to_fountain(script), encoding="utf-8")
    print(f"[4/4] Done! Output: {out_dir}")

def main():
    ap = argparse.ArgumentParser(description="從視頻/音頻轉錄稿發展全新劇本")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--srt"); src.add_argument("--audio")
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--target-minutes", type=int, default=10)
    ap.add_argument("--genre", default="劇情")
    ap.add_argument("--max-tokens", type=int, default=6000)
    ap.add_argument("--extract-only", action="store_true")
    ap.add_argument("--provider", default="deepseek", choices=list(PROVIDERS.keys()))
    ap.add_argument("--model", default="deepseek-v4-flash")
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--compute-type", default="int8")
    return run_pipeline(ap.parse_args()) or 0

if __name__ == "__main__": sys.exit(main())

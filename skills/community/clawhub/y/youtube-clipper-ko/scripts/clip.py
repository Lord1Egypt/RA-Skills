#!/usr/bin/env python3
"""
clip.py — YouTube Clipper KO 메인 스크립트
YouTube URL / 로컬 파일 → 바이럴 클립 자동 분할

Usage:
  python3 clip.py --url "https://youtu.be/VIDEO_ID"
  python3 clip.py --file "/path/to/video.mp4"
  python3 clip.py --url "..." --start "10:00" --end "30:00"  # 구간 지정
  python3 clip.py --url "..." --clip-length 60               # 클립 최대 길이(초)
  python3 clip.py --url "..." --dry                          # 자막 추출만 (클립 생성 X)
"""

import os, sys, json, argparse, subprocess, tempfile, re
from datetime import datetime, timezone
from pathlib import Path

# ── 경로 설정 ─────────────────────────────────────────
SKILL_DIR  = Path(__file__).parent.parent
OUTPUT_DIR = SKILL_DIR / "outputs"

# Clawitzer 편집 모듈 재사용
CLAWITZER_DIR = Path(__file__).parent.parent.parent.parent / "projects" / "clawitzer"
if CLAWITZER_DIR.exists():
    sys.path.insert(0, str(CLAWITZER_DIR))

# ── 폰트 설정 ─────────────────────────────────────────
SUIT_FONT     = "/usr/share/fonts/truetype/SUIT-ExtraBold.ttf"
FALLBACK_FONT = "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc"

# ── 자막 색상 (Clawitzer 3색 룰) ─────────────────────
EMPHASIS_KEYWORDS = [
    "진짜", "완전", "대박", "충격", "헐", "미쳤", "놀랐", "말도 안",
    "실화", "이게 뭐야", "어떡해", "깜짝", "세상에", "진심", "실화냐",
    "미친", "개쩐", "레전드", "이상한", "생겼어", "없다는", "안 한다",
    "있죠", "거 있죠", "진짜로", "솔직히", "사실은", "결론은",
]

OUT_W, OUT_H = 1080, 1920
LETTER_SPACING = -1


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 1. 환경 검사
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def check_env():
    """필수 도구 존재 여부 확인"""
    errors = []

    # yt-dlp
    r = subprocess.run(["yt-dlp", "--version"], capture_output=True)
    if r.returncode != 0:
        errors.append("yt-dlp 없음: pip install yt-dlp")

    # ffmpeg
    r = subprocess.run(["ffmpeg", "-version"], capture_output=True)
    if r.returncode != 0:
        errors.append("ffmpeg 없음: apt install ffmpeg")

    # libass (자막 burn-in에 필요)
    r = subprocess.run(["ffmpeg", "-filters"], capture_output=True, text=True)
    if "subtitles" not in r.stderr:
        print("  ⚠ ffmpeg libass 없음 — 자막 burn-in 불가 (SRT로 대체)")

    # python 패키지
    try:
        import openai
    except ImportError:
        errors.append("openai 없음: pip install openai")
    try:
        import anthropic
    except ImportError:
        errors.append("anthropic 없음: pip install anthropic")

    # 폰트
    font = get_font()
    print(f"  폰트: {font}")

    if errors:
        for e in errors:
            print(f"  ✗ {e}")
        sys.exit(1)

    print("  ✅ 환경 OK")


def get_font() -> str:
    for p in [SUIT_FONT, FALLBACK_FONT]:
        if os.path.exists(p):
            return p
    # 시스템 폰트 검색
    r = subprocess.run(["fc-list", ":lang=ko"], capture_output=True, text=True)
    for line in r.stdout.splitlines():
        if ".ttf" in line or ".ttc" in line:
            return line.split(":")[0].strip()
    return ""


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2. 영상 다운로드
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def download_video(url: str, out_dir: Path, start: str = None, end: str = None) -> str:
    """YouTube URL → 로컬 MP4 다운로드"""
    print(f"\n[1] 영상 다운로드: {url}")

    out_path = str(out_dir / "source.%(ext)s")
    cmd = [
        "yt-dlp",
        "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "--merge-output-format", "mp4",
        "-o", out_path,
        "--no-playlist",
        url,
    ]

    # 구간 지정 시 (yt-dlp --download-sections)
    if start or end:
        s = start or "0"
        e = end or "99:59:59"
        cmd += ["--download-sections", f"*{s}-{e}"]

    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("  ✗ 다운로드 실패:\n", r.stderr[-500:])
        raise RuntimeError("yt-dlp 다운로드 실패")

    # 실제 파일 경로 찾기
    mp4_files = list(out_dir.glob("source.mp4"))
    if not mp4_files:
        mp4_files = list(out_dir.glob("source.*"))
    if not mp4_files:
        raise FileNotFoundError("다운로드된 파일 없음")

    path = str(mp4_files[0])
    size_mb = os.path.getsize(path) / 1024 / 1024
    print(f"  완료: {path} ({size_mb:.1f}MB)")
    return path


def get_video_duration(path: str) -> float:
    cmd = ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", path]
    r = subprocess.run(cmd, capture_output=True, text=True)
    data = json.loads(r.stdout)
    return float(data["format"]["duration"])


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 3. Whisper 자막 추출
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def extract_transcript(video_path: str, out_dir: Path, lang: str = "ko") -> dict:
    """
    Whisper API로 자막 + word-level 타임스탬프 추출
    OpenAI API 키 필요 (환경변수 OPENAI_API_KEY)
    """
    print(f"\n[2] 자막 추출 중 (Whisper)...")

    # 오디오 추출 (MP3로 변환, Whisper 25MB 제한 대응)
    audio_path = str(out_dir / "audio.mp3")
    subprocess.run([
        "ffmpeg", "-y", "-i", video_path,
        "-q:a", "0", "-map", "a",
        "-b:a", "64k",  # 낮은 비트레이트로 용량 절약
        audio_path,
    ], check=True, capture_output=True)

    size_mb = os.path.getsize(audio_path) / 1024 / 1024
    print(f"  오디오 추출: {size_mb:.1f}MB")

    # 파일 크기 체크 (25MB 초과 시 분할)
    if size_mb > 24:
        print(f"  ⚠ 25MB 초과 ({size_mb:.1f}MB) → 분할 처리")
        return extract_transcript_chunked(audio_path, out_dir, lang)

    # Whisper API 호출
    import openai
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))

    with open(audio_path, "rb") as f:
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            language=lang,
            response_format="verbose_json",
            timestamp_granularities=["segment", "word"],
        )

    transcript = {
        "text": response.text,
        "language": response.language,
        "duration": response.duration,
        "segments": [
            {
                "id": s.id,
                "start": s.start,
                "end": s.end,
                "text": s.text.strip(),
            }
            for s in response.segments
        ],
        "words": [
            {
                "word": w.word,
                "start": w.start,
                "end": w.end,
            }
            for w in (response.words or [])
        ],
    }

    # 저장
    transcript_path = out_dir / "transcript.json"
    with open(transcript_path, "w", encoding="utf-8") as f:
        json.dump(transcript, f, ensure_ascii=False, indent=2)

    print(f"  자막 {len(transcript['segments'])}개 세그먼트, {len(transcript['words'])}개 단어")
    print(f"  저장: {transcript_path}")
    return transcript


def extract_transcript_chunked(audio_path: str, out_dir: Path, lang: str) -> dict:
    """25MB 초과 오디오 분할 처리"""
    import openai
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))

    # 10분 단위로 분할
    duration = get_video_duration(audio_path)
    chunk_sec = 600
    chunks = []
    offset = 0.0

    while offset < duration:
        chunk_path = str(out_dir / f"audio_chunk_{int(offset)}.mp3")
        subprocess.run([
            "ffmpeg", "-y", "-i", audio_path,
            "-ss", str(offset), "-t", str(chunk_sec),
            "-b:a", "64k", chunk_path,
        ], check=True, capture_output=True)

        with open(chunk_path, "rb") as f:
            resp = client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                language=lang,
                response_format="verbose_json",
                timestamp_granularities=["segment"],
            )

        for s in resp.segments:
            chunks.append({
                "start": s.start + offset,
                "end": s.end + offset,
                "text": s.text.strip(),
            })

        os.remove(chunk_path)
        offset += chunk_sec

    transcript = {
        "text": " ".join(c["text"] for c in chunks),
        "language": lang,
        "duration": duration,
        "segments": [{"id": i, **c} for i, c in enumerate(chunks)],
        "words": [],
    }

    transcript_path = out_dir / "transcript.json"
    with open(transcript_path, "w", encoding="utf-8") as f:
        json.dump(transcript, f, ensure_ascii=False, indent=2)

    return transcript


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 4. 바이럴 구간 선정 (Claude)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _call_haiku(client, messages: list, max_tokens: int = 2000) -> str:
    """Haiku 호출 + JSON 코드블록 제거"""
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=max_tokens,
        messages=messages,
    )
    raw = response.content[0].text.strip()
    raw = re.sub(r"```json?\n?", "", raw).replace("```", "").strip()
    return raw


def _parse_json(raw: str, fallback=None):
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        print(f"  ⚠ JSON 파싱 실패:\n{raw[:200]}")
        return fallback if fallback is not None else []


def select_viral_segments(
    transcript: dict,
    clip_length: int = 60,
    n_clips: int = 10,
) -> list[dict]:
    """
    Haiku 3중 검증으로 바이럴 구간 선정

    1차: 후보 20개 넓게 추출
    2차: 독립 재평가 + 엄격한 탈락 기준 적용
    3차: 최종 랭킹 + 리즌 보강 → 상위 n_clips개 반환
    """
    import anthropic
    client = anthropic.Anthropic()

    segments_text = "\n".join(
        f"[{fmt_time(s['start'])} → {fmt_time(s['end'])}] {s['text']}"
        for s in transcript["segments"]
    )
    total_duration = transcript.get("duration", 0)

    # ── 1차: 후보 20개 넓게 뽑기 ─────────────────────────
    print(f"\n[3-1] 1차 후보 추출 (Haiku)...")

    prompt_1 = f"""다음은 YouTube 영상 전체 자막입니다. 총 길이: {fmt_time(total_duration)}

자막:
{segments_text}

---

숏폼(쇼츠/릴스/틱톡) 제작용으로 바이럴 가능성이 있는 구간 후보 20개를 뽑아주세요.
이 단계에서는 엄격하게 필터링하지 말고 가능성 있는 것들을 넓게 포함하세요.

조건:
- 각 클립 길이: {clip_length}초 이내 (최소 20초)
- 클립 겹치지 않게 할 것

JSON 형식으로만 답하세요:
[
  {{
    "id": 1,
    "start_sec": 194.5,
    "end_sec": 248.0,
    "text_preview": "해당 구간 핵심 문장 1~2개",
    "candidate_reason": "후보로 뽑은 이유 (1문장)"
  }},
  ...
]"""

    raw1 = _call_haiku(client, [{"role": "user", "content": prompt_1}], max_tokens=3000)
    candidates = _parse_json(raw1, fallback=[])
    print(f"  후보 {len(candidates)}개 추출")

    if not candidates:
        return []

    # ── 2차: 독립 재평가 + 엄격한 탈락 ─────────────────────
    print(f"\n[3-2] 2차 독립 재평가 (Haiku)...")

    candidates_json = json.dumps(candidates, ensure_ascii=False, indent=2)

    prompt_2 = f"""당신은 한국 숏폼 콘텐츠 전문 편집자입니다.
아래는 YouTube 영상에서 바이럴 후보로 뽑힌 구간 목록입니다.
각 구간을 독립적으로 엄격하게 평가해주세요.

평가 기준 (0~100점):
- 완결성: 클립 단독으로 이해 가능한가? (필수, 미달 시 탈락)
- 훅: 첫 3초 안에 시청자를 잡을 수 있는가?
- 감정: 공감/놀람/궁금증/웃음 중 하나 이상 유발하는가?
- 구체성: 숫자/금액/방법 등 구체적 정보가 있는가?
- 한국 시청자 반응: 한국 커뮤니티 정서에 맞는가?

탈락 기준 (하나라도 해당하면 탈락):
- 중간 맥락 없이는 이해 불가
- 너무 일반적이어서 차별점 없음
- 내용이 단순 나열에 불과

후보 목록:
{candidates_json}

JSON 형식으로만 답하세요:
[
  {{
    "id": 1,
    "score": 82,
    "pass": true,
    "weakness": "가장 큰 약점 (1문장)"
  }},
  ...
]

pass=false인 항목도 반드시 포함하세요."""

    raw2 = _call_haiku(client, [{"role": "user", "content": prompt_2}], max_tokens=2000)
    evaluations = _parse_json(raw2, fallback=[])

    # 평가 결과 매핑
    eval_map = {e["id"]: e for e in evaluations if isinstance(e, dict)}
    passed = [
        c for c in candidates
        if eval_map.get(c["id"], {}).get("pass", False)
    ]
    # 점수 붙이기
    for c in passed:
        c["score_2nd"] = eval_map.get(c["id"], {}).get("score", 50)
        c["weakness"]  = eval_map.get(c["id"], {}).get("weakness", "")

    # 점수 기준 정렬, 상위 n_clips*1.5개만 3차로
    passed.sort(key=lambda x: x.get("score_2nd", 0), reverse=True)
    passed = passed[:int(n_clips * 1.5)]
    print(f"  통과: {len(passed)}개 (탈락: {len(candidates) - len(passed)}개)")

    if not passed:
        return []

    # ── 3차: 최종 랭킹 + 리즌 보강 ─────────────────────────
    print(f"\n[3-3] 3차 최종 선정 (Haiku)...")

    passed_json = json.dumps(passed, ensure_ascii=False, indent=2)

    prompt_3 = f"""당신은 한국 숏폼 콘텐츠 편집자입니다.
아래는 2차 검증을 통과한 클립 후보들입니다.
각 클립에 대해 유저가 어떤 클립을 올릴지 스스로 판단할 수 있도록 메타데이터를 보강해주세요.

목표: 순위 매기기가 아니라, 각 클립의 특성을 명확하게 설명해서 유저가 고를 수 있게 하는 것.
순서는 영상 시간 순서(start_sec 오름차순)로 유지하세요.

통과 후보:
{passed_json}

JSON 형식으로만 답하세요:
[
  {{
    "start_sec": 194.5,
    "end_sec": 248.0,
    "score": 82,
    "title": "클립 제목 (15자 이내, 한국어)",
    "hook": "첫 3초에 나오는 훅 문장 (자막 원문 그대로)",
    "emotion_type": "공감|놀람|궁금증|웃음|정보 중 하나",
    "reason": "이 클립이 왜 바이럴 가능성이 있는지 (2~3문장, 구체적으로)",
    "weakness": "이 클립의 잠재적 약점 또는 올릴 때 주의할 점 (1문장)"
  }},
  ...
]

통과한 후보 전부 반환. 탈락 없음."""

    raw3 = _call_haiku(client, [{"role": "user", "content": prompt_3}], max_tokens=3000)
    final = _parse_json(raw3, fallback=[])

    # start_sec/end_sec 없으면 candidates에서 보완
    id_to_candidate = {c["id"]: c for c in candidates}
    for item in final:
        if "start_sec" not in item or "end_sec" not in item:
            # text_preview로 후보 찾기 시도
            for c in passed:
                if c.get("text_preview", "") in item.get("hook", ""):
                    item["start_sec"] = c["start_sec"]
                    item["end_sec"]   = c["end_sec"]
                    break

    # 유효한 항목만 (start_sec, end_sec 있는 것) + 시간순 정렬
    final = [f for f in final if "start_sec" in f and "end_sec" in f]
    final.sort(key=lambda x: x["start_sec"])

    print(f"  메타데이터 보강 완료: {len(final)}개")
    for s in final[:3]:
        print(f"  [{s['score']}점/{s.get('emotion_type','?')}] {s['title']} "
              f"({fmt_time(s['start_sec'])}~{fmt_time(s['end_sec'])})")
        print(f"    훅: {s.get('hook', '-')[:40]}")

    return final


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 5. 클립 추출 + 자막 burn-in
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def fmt_time(sec: float) -> str:
    """초 → MM:SS 또는 HH:MM:SS"""
    sec = float(sec)
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = sec % 60
    if h > 0:
        return f"{h}:{m:02d}:{s:05.2f}"
    return f"{m}:{s:05.2f}"


def fmt_ass_time(sec: float) -> str:
    """초 → ASS 타임코드 (H:MM:SS.cc)"""
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = sec % 60
    cs = int((s % 1) * 100)
    return f"{h}:{m:02d}:{int(s):02d}.{cs:02d}"


def assign_subtitle_colors(sentences: list[dict]) -> list[dict]:
    """
    Clawitzer 3색 룰 적용
    - 강조 키워드 포함 → 빨강(#FF0000), 62px
    - 빨강 앞뒤 → 노랑(#FFFF00), 52px
    - 나머지 → 흰색(#FFFFFF), 52px
    - 빨강 연속 불가
    - 빨강 하나도 없으면 첫 문장 빨강
    """
    n = len(sentences)
    result = [dict(s) for s in sentences]

    is_red = [False] * n
    for i, s in enumerate(result):
        text = s.get("text", "")
        if any(kw in text for kw in EMPHASIS_KEYWORDS):
            is_red[i] = True

    # 연속 빨강 방지
    for i in range(1, n):
        if is_red[i] and is_red[i-1]:
            is_red[i] = False

    # 빨강 없으면 첫 문장
    if not any(is_red):
        is_red[0] = True

    # 앞뒤 노랑
    is_yellow = [False] * n
    for i in range(n):
        if is_red[i]:
            if i > 0 and not is_red[i-1]:
                is_yellow[i-1] = True
            if i < n-1 and not is_red[i+1]:
                is_yellow[i+1] = True

    for i, s in enumerate(result):
        if is_red[i]:
            result[i]["color"] = "#FF0000"
            result[i]["size"]  = 62
        elif is_yellow[i]:
            result[i]["color"] = "#FFFF00"
            result[i]["size"]  = 52
        else:
            result[i]["color"] = "#FFFFFF"
            result[i]["size"]  = 52

    return result


def hex_to_ass(hex_color: str) -> str:
    """#RRGGBB → &H00BBGGRR"""
    h = hex_color.lstrip("#")
    r, g, b = h[0:2], h[2:4], h[4:6]
    return f"&H00{b}{g}{r}"


def make_ass_subtitle(sentences: list[dict], offset_sec: float, font_path: str) -> str:
    """세그먼트 목록 → ASS 자막 문자열"""
    font_name = os.path.basename(font_path).replace(".ttf", "").replace(".ttc", "")

    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {OUT_W}
PlayResY: {OUT_H}
WrapStyle: 1

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{font_name},52,&H00FFFFFF,&H000000FF,&H00000000,&HAA000000,1,0,0,0,100,100,{LETTER_SPACING},0,3,8,0,5,30,30,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = [header]
    for s in sentences:
        start = s["start"] - offset_sec
        end   = s["end"]   - offset_sec
        if start < 0: start = 0
        color = hex_to_ass(s.get("color", "#FFFFFF"))
        size  = s.get("size", 52)
        text  = s["text"].replace("{", "\\{").replace("}", "\\}")
        styled = f"{{\\an5\\pos({OUT_W//2},900)\\c{color}\\fs{size}}}{text}"
        lines.append(f"Dialogue: 0,{fmt_ass_time(start)},{fmt_ass_time(end)},Default,,0,0,0,,{styled}")

    return "\n".join(lines) + "\n"



def extract_clip(
    source_video: str,
    segment: dict,
    transcript_segments: list,
    out_dir: Path,
    font_path: str,
    index: int,
) -> str:
    """단일 구간 → 9:16 클립 MP4 추출"""
    start_sec = segment["start_sec"]
    end_sec   = segment["end_sec"]
    duration  = end_sec - start_sec
    title_safe = re.sub(r"[^\w가-힣]", "_", segment.get("title", f"clip_{index:02d}"))[:30]
    out_filename = f"clip_{index:02d}_{title_safe}.mp4"
    out_path = str(out_dir / out_filename)

    tmpdir = tempfile.mkdtemp(prefix="clipper_")

    # 해당 구간 자막 필터링
    clip_segs = [
        s for s in transcript_segments
        if s["end"] > start_sec and s["start"] < end_sec
    ]

    # 자막 색상/크기 배정
    sentences = assign_subtitle_colors([
        {
            "text": s["text"],
            "start": s["start"],
            "end": min(s["end"], end_sec),
        }
        for s in clip_segs
    ])

    # ASS 자막 파일 생성
    ass_content = make_ass_subtitle(sentences, offset_sec=start_sec, font_path=font_path)
    ass_path = os.path.join(tmpdir, "sub.ass")
    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(ass_content)

    # ffmpeg 클립 추출 + 9:16 변환 + 자막 burn-in + 무음 압축
    vf = (
        f"scale={OUT_W}:{OUT_H}:force_original_aspect_ratio=increase,"
        f"crop={OUT_W}:{OUT_H},"
        f"ass={ass_path}"
    )

    # 영상 + 오디오 한번에 (원본 음성 유지, 무음 압축 없음)
    subprocess.run([
        "ffmpeg", "-y",
        "-ss", str(start_sec), "-t", str(duration),
        "-i", source_video,
        "-vf", vf,
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "128k",
        "-ar", "44100",
        out_path,
    ], check=True, capture_output=True)

    size_mb = os.path.getsize(out_path) / 1024 / 1024
    print(f"  [{index:02d}] {out_filename} ({duration:.0f}초, {size_mb:.1f}MB)")

    # 임시 파일 정리
    import shutil
    shutil.rmtree(tmpdir, ignore_errors=True)

    return out_path


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 메인
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def main():
    parser = argparse.ArgumentParser(description="YouTube Clipper KO")
    parser.add_argument("--url",  help="YouTube URL")
    parser.add_argument("--file", help="로컬 영상 파일 경로")
    parser.add_argument("--start", help="시작 시간 (MM:SS 또는 HH:MM:SS)")
    parser.add_argument("--end",   help="종료 시간 (MM:SS 또는 HH:MM:SS)")
    parser.add_argument("--clip-length", type=int, default=60, help="클립 최대 길이(초) [기본: 60]")
    parser.add_argument("--n-clips", type=int, default=10, help="추출할 클립 수 [기본: 10]")
    parser.add_argument("--lang", default="ko", help="자막 언어 [기본: ko]")
    parser.add_argument("--dry", action="store_true", help="자막 추출만 (클립 미생성)")
    parser.add_argument("--no-check", action="store_true", help="환경 검사 스킵")
    args = parser.parse_args()

    if not args.url and not args.file:
        parser.error("--url 또는 --file 필수")

    # 환경 검사
    if not args.no_check:
        print("\n[0] 환경 검사...")
        check_env()

    # 출력 폴더
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    out_dir = OUTPUT_DIR / ts
    out_dir.mkdir(parents=True, exist_ok=True)
    clips_dir = out_dir / "clips"
    clips_dir.mkdir(exist_ok=True)
    print(f"\n출력 폴더: {out_dir}")

    # 폰트
    font = get_font()
    if not font:
        print("  ⚠ 한국어 폰트 없음 — 자막 품질 저하될 수 있음")

    # 영상 준비
    if args.url:
        video_path = download_video(args.url, out_dir, args.start, args.end)
    else:
        video_path = args.file
        print(f"\n[1] 로컬 파일: {video_path}")

    # 자막 추출
    transcript = extract_transcript(video_path, out_dir, args.lang)

    if args.dry:
        print(f"\n[dry] 자막 추출 완료. 클립 생성 스킵.")
        print(f"  결과: {out_dir / 'transcript.json'}")
        return

    # 바이럴 구간 선정
    segments = select_viral_segments(transcript, args.clip_length, args.n_clips)

    if not segments:
        print("  ✗ 바이럴 구간 선정 실패")
        return

    # 결과 저장
    viral_path = out_dir / "viral_segments.json"
    with open(viral_path, "w", encoding="utf-8") as f:
        json.dump(segments, f, ensure_ascii=False, indent=2)

    # 클립 추출
    print(f"\n[4] 클립 추출 중 ({len(segments)}개)...")
    results = []
    for i, seg in enumerate(segments, 1):
        try:
            clip_path = extract_clip(
                source_video=video_path,
                segment=seg,
                transcript_segments=transcript["segments"],
                out_dir=clips_dir,
                font_path=font,
                index=i,
            )
            seg["clip_file"] = str(Path(clip_path).relative_to(out_dir))
            results.append(seg)
        except Exception as e:
            print(f"  ✗ clip_{i:02d} 실패: {e}")

    # 최종 결과
    result = {
        "source": video_path,
        "url": args.url or "",
        "clips": results,
        "output_dir": str(out_dir),
        "created_at": ts,
    }
    result_path = out_dir / "result.json"
    with open(result_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*55}")
    print(f"✅ 완료! {len(results)}개 클립 생성")
    print(f"  출력: {out_dir}")
    print(f"  결과: {result_path}")
    print(f"\n상위 3개:")
    for s in results[:3]:
        print(f"  [{s['score']}점] {s['title']}")
        print(f"    {s['reason'][:60]}...")
    print(f"{'='*55}")


if __name__ == "__main__":
    main()

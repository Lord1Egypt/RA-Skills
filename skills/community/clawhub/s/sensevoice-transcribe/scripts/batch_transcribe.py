#!/usr/bin/env python3
"""
Batch transcribe v5: SenseVoice + VAD-anchored timestamps.
Usage: python3 batch_transcribe.py [--dry-run] [--engine sensevoice|whisper]
                                   [--progress-file /path/progress.json]
                                   [--discord-webhook URL]
                                   [--force-dates 2026-03-07,2026-03-08]

Changes from v4:
  - SenseVoice output now has per-segment timestamps via VAD anchoring
  - Runs VAD separately to get precise segment boundaries
  - Splits raw text by <|zh|> tags, maps proportionally to VAD timestamps
  - Output: [HH:MM:SS] text (one line per segment, ~15s granularity)
"""
import os, sys, re, subprocess, json, time, urllib.request
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

DAYLOG_DIR = Path(__file__).parent.parent
RAW_DIR = DAYLOG_DIR / "raw"
TRANSCRIPT_DIR = DAYLOG_DIR / "transcripts"
DRY_RUN = "--dry-run" in sys.argv

# Parse flags
ENGINE = "sensevoice"
PROGRESS_FILE = None
DISCORD_WEBHOOK = None
FORCE_DATES = []

for i, arg in enumerate(sys.argv):
    if arg == "--engine" and i + 1 < len(sys.argv):
        ENGINE = sys.argv[i + 1].lower()
    elif arg == "--progress-file" and i + 1 < len(sys.argv):
        PROGRESS_FILE = Path(sys.argv[i + 1])
    elif arg == "--discord-webhook" and i + 1 < len(sys.argv):
        DISCORD_WEBHOOK = sys.argv[i + 1]
    elif arg == "--force-dates" and i + 1 < len(sys.argv):
        FORCE_DATES = [d.strip() for d in sys.argv[i + 1].split(",")]


def write_progress(data: dict):
    """Write progress JSON for external monitoring."""
    if not PROGRESS_FILE:
        return
    data["updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        PROGRESS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(PROGRESS_FILE, "w") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def discord_notify(content: str, color: int = 0x2ECC71):
    """Send Discord webhook notification."""
    if not DISCORD_WEBHOOK:
        return
    payload = {
        "embeds": [{
            "description": content,
            "color": color,
            "footer": {"text": f"daylog batch_transcribe v4 · {ENGINE}"},
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }]
    }
    try:
        req = urllib.request.Request(
            DISCORD_WEBHOOK,
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        urllib.request.urlopen(req, timeout=10)
    except Exception as e:
        print(f"  [webhook] Failed: {e}")

# ── Whisper config ──
WHISPER_MODEL = "mlx-community/whisper-large-v3-turbo"
WHISPER_LANG = "zh"
SILENCE_NOISE_DB = -20
SILENCE_MIN_DUR = 5
MIN_SPEECH_SEG = 3

# ── Hallucination filter (for Whisper) ──
HALLUC_PATTERNS = re.compile(
    r'[往]{3,}|[听]{3,}|[哈]{3,}|[逸]{3,}|[啊]{5,}|[冰]{5,}|'
    r'按下按[鈕钮]|我用了一半|'
    r'[請请]不要|[謝谢]{2,}|感谢.{0,5}观看|'
    r'Thank you|Subscribe|字幕|[請请][訂订][閱阅]|'
    r'www\..+\.com|'
    r'(?:(.)\1{5,})'
)

def is_repetitive_line(text: str) -> bool:
    if len(text) < 4:
        return False
    from collections import Counter
    counts = Counter(text.replace(' ', ''))
    if not counts:
        return False
    _, mc = counts.most_common(1)[0]
    return mc / sum(counts.values()) > 0.6

def filter_hallucinations(lines):
    clean, removed = [], 0
    for line in lines:
        m = re.match(r'^\[[\d:]+\]\s*(.+)$', line)
        if not m:
            clean.append(line); continue
        text = m.group(1).strip()
        if not text or HALLUC_PATTERNS.search(text) or is_repetitive_line(text):
            removed += 1; continue
        clean.append(line)
    return clean, removed

def extract_timestamp(filename: str) -> str:
    """Extract YYYYMMDD_HHMMSS from filename for sorting."""
    m = re.search(r'(\d{8}_\d{6})', filename)
    return m.group(1) if m else "00000000_000000"

def extract_start_dt(filename: str):
    m = re.search(r'(\d{8})_(\d{6})', filename)
    if m:
        return datetime.strptime(m.group(1) + m.group(2), '%Y%m%d%H%M%S')
    return None

# ── Handle --force-dates: delete existing transcripts for forced dates ──
if FORCE_DATES and not DRY_RUN:
    for fd in FORCE_DATES:
        force_dir = TRANSCRIPT_DIR / fd
        if force_dir.exists():
            import shutil
            count = len(list(force_dir.glob("*.txt")))
            shutil.rmtree(force_dir)
            print(f"[force] Deleted {count} existing transcripts for {fd}")
elif FORCE_DATES and DRY_RUN:
    print(f"[dry-run] Would delete transcripts for: {', '.join(FORCE_DATES)}")

# ── Collect new WAV files, grouped by date ──
date_files = defaultdict(list)
skip_count = 0

for wav in sorted(RAW_DIR.glob("*.wav")) + sorted(RAW_DIR.glob("*.WAV")):
    bn = wav.stem
    m = re.search(r'(\d{8})', bn)
    date_dir = f"{m.group(1)[:4]}-{m.group(1)[4:6]}-{m.group(1)[6:]}" if m else datetime.fromtimestamp(wav.stat().st_mtime).strftime("%Y-%m-%d")

    # Check if already transcribed (match by original stem OR indexed name)
    existing = list((TRANSCRIPT_DIR / date_dir).glob(f"*{bn}*")) if (TRANSCRIPT_DIR / date_dir).exists() else []
    if existing:
        skip_count += 1
    else:
        date_files[date_dir].append(wav)

# Sort each date's files by timestamp (cross-TX chronological order)
for date_dir in date_files:
    date_files[date_dir].sort(key=lambda w: extract_timestamp(w.stem))

all_new = [(wav, dd) for dd in sorted(date_files) for wav in date_files[dd]]

print(f"\n=== Batch Transcription v5 ===")
print(f"Engine: {ENGINE}")
print(f"New: {len(all_new)} | Already done: {skip_count}")

if not all_new:
    print("Nothing to do.")
    sys.exit(0)

if DRY_RUN:
    for wav, dd in all_new:
        print(f"  [dry-run] {wav.name} → {dd}/")
    sys.exit(0)

# ── Load engine ──
if ENGINE == "sensevoice":
    print("Loading SenseVoice-Small + VAD...")
    t_load = time.time()
    import warnings; warnings.filterwarnings('ignore')
    from funasr import AutoModel
    from funasr.utils.postprocess_utils import rich_transcription_postprocess
    model = AutoModel(
        model="iic/SenseVoiceSmall",
        vad_model="fsmn-vad",
        vad_kwargs={"max_single_segment_time": 30000},
        device="cpu",
    )
    # Standalone VAD for timestamp extraction
    vad_model_standalone = AutoModel(model="fsmn-vad", disable_update=True)
    print(f"Model ready in {time.time()-t_load:.1f}s\n")
else:
    print(f"Loading Whisper MLX: {WHISPER_MODEL} ...")
    t_load = time.time()
    import mlx_whisper
    print(f"Model ready in {time.time()-t_load:.1f}s\n")

failed = 0
total_halluc = 0
batch_start = time.time()
completed_files = []

# ── Start notification ──
dates_summary = ", ".join(sorted(date_files.keys()))
discord_notify(
    f"🎙️ **转录开始**\n"
    f"引擎: `{ENGINE}` | 文件: **{len(all_new)}** | 已跳过: {skip_count}\n"
    f"日期: {dates_summary}",
    color=0x3498DB
)
write_progress({"status": "running", "total": len(all_new), "done": 0, "failed": 0,
                "current": "", "dates": dates_summary, "elapsed_s": 0})

for i, (wav, date_dir) in enumerate(all_new, 1):
    bn = wav.stem
    # Use indexed filename for correct sort order within date
    # Find this file's position among all files for this date
    idx_in_date = date_files[date_dir].index(wav)
    out_name = f"{idx_in_date:03d}_{bn}.txt"
    txt_path = TRANSCRIPT_DIR / date_dir / out_name

    print(f"[{i}/{len(all_new)}] {wav.name} → {date_dir}/{out_name}")
    write_progress({
        "status": "running", "total": len(all_new), "done": i - 1, "failed": failed,
        "current": wav.name, "current_idx": i, "date": date_dir,
        "elapsed_s": int(time.time() - batch_start)
    })

    try:
        start_dt = extract_start_dt(str(wav))
        t0 = time.time()

        if ENGINE == "sensevoice":
            # 1. Run VAD separately for timestamps (~4s overhead)
            vad_res = vad_model_standalone.generate(input=str(wav))
            vad_segs = vad_res[0].get('value', [])

            # 2. Run SenseVoice for text (keep raw tags for splitting)
            res = model.generate(
                input=str(wav),
                cache={},
                language="zh",
                use_itn=True,
                batch_size_s=60,
                merge_vad=True,
            )
            raw_text = res[0]["text"]
            elapsed = time.time() - t0

            # 3. Split by <|zh|> tags, clean each segment
            text_segments = re.split(r'<\|zh\|>', raw_text)
            text_segments = [rich_transcription_postprocess(s).strip()
                             for s in text_segments if s.strip()]
            text_segments = [s for s in text_segments if s and len(s) > 1]

            # 4. Map text segments to VAD timestamps proportionally
            n_text = len(text_segments)
            n_vad = len(vad_segs)
            lines = []
            if n_text > 0 and n_vad > 0 and start_dt:
                ratio = n_vad / n_text
                for idx, seg_text in enumerate(text_segments):
                    vad_idx = min(int(idx * ratio), n_vad - 1)
                    offset_ms = vad_segs[vad_idx][0]
                    ts = (start_dt + timedelta(milliseconds=offset_ms)).strftime('%H:%M:%S')
                    lines.append(f"[{ts}] {seg_text}")
            elif n_text > 0:
                # Fallback: no VAD or no start_dt
                for seg_text in text_segments:
                    lines.append(seg_text)

            # 5. Write timestamped output
            txt_path.parent.mkdir(parents=True, exist_ok=True)
            with open(txt_path, 'w') as f:
                if start_dt:
                    f.write(f"[录音开始: {start_dt.strftime('%H:%M:%S')}]\n")
                for line in lines:
                    f.write(line + '\n')

            total_chars = sum(len(s) for s in text_segments)
            print(f"  {elapsed:.1f}s | {n_text} segs | {total_chars} chars | VAD:{n_vad}")
            completed_files.append({"file": wav.name, "date": date_dir, "segs": n_text,
                                    "chars": total_chars, "time_s": round(elapsed, 1)})

        else:
            # Whisper path (unchanged from v2)
            import tempfile
            res = subprocess.run(
                ['ffmpeg', '-i', str(wav), '-af',
                 f'silencedetect=noise={SILENCE_NOISE_DB}dB:d={SILENCE_MIN_DUR}',
                 '-f', 'null', '-'],
                capture_output=True, text=True
            )
            silence_starts, silence_ends = [], []
            for line in res.stderr.split('\n'):
                ms = re.search(r'silence_start: ([\d.]+)', line)
                if ms: silence_starts.append(float(ms.group(1)))
                me = re.search(r'silence_end: ([\d.]+)', line)
                if me: silence_ends.append(float(me.group(1)))

            dur_res = subprocess.run(
                ['ffprobe', '-v', 'quiet', '-show_entries', 'format=duration', '-of', 'json', str(wav)],
                capture_output=True, text=True
            )
            total_dur = float(json.loads(dur_res.stdout)['format']['duration'])

            non_silent, prev = [], 0.0
            for j in range(len(silence_starts)):
                if silence_starts[j] - prev > MIN_SPEECH_SEG:
                    non_silent.append((prev, silence_starts[j]))
                if j < len(silence_ends):
                    prev = silence_ends[j]
            if total_dur - prev > MIN_SPEECH_SEG:
                non_silent.append((prev, total_dur))
            total_speech = sum(e-s for s,e in non_silent)

            all_segments = []
            if total_dur - total_speech < 60:
                result = mlx_whisper.transcribe(str(wav), path_or_hf_repo=WHISPER_MODEL, language=WHISPER_LANG, condition_on_previous_text=False)
                all_segments = result['segments']
            else:
                tmpdir = Path(tempfile.mkdtemp())
                try:
                    for idx, (seg_s, seg_e) in enumerate(non_silent):
                        chunk = tmpdir / f"chunk_{idx:04d}.wav"
                        subprocess.run(['ffmpeg', '-y', '-i', str(wav), '-ss', str(seg_s), '-to', str(seg_e), '-ar', '16000', '-ac', '1', str(chunk)], capture_output=True)
                        r = mlx_whisper.transcribe(str(chunk), path_or_hf_repo=WHISPER_MODEL, language=WHISPER_LANG, condition_on_previous_text=False)
                        for seg in r['segments']:
                            seg['start'] += seg_s; seg['end'] += seg_s
                            all_segments.append(seg)
                        chunk.unlink()
                finally:
                    for f_tmp in tmpdir.iterdir(): f_tmp.unlink()
                    tmpdir.rmdir()

            elapsed = time.time() - t0
            raw_lines = []
            for seg in all_segments:
                text = seg['text'].strip()
                if not text: continue
                if start_dt:
                    ts = (start_dt + timedelta(seconds=seg['start'])).strftime('%H:%M:%S')
                else:
                    mins, secs = divmod(int(seg['start']), 60)
                    ts = f"{mins:02d}:{secs:02d}"
                raw_lines.append(f"[{ts}] {text}")

            clean_lines, halluc_count = filter_hallucinations(raw_lines)
            total_halluc += halluc_count

            txt_path.parent.mkdir(parents=True, exist_ok=True)
            with open(txt_path, 'w') as f:
                for line in clean_lines:
                    f.write(line + '\n')

            skip_pct = (1 - total_speech / total_dur) * 100 if total_dur > 0 else 0
            print(f"  {elapsed:.1f}s | speech {total_speech:.0f}s/{total_dur:.0f}s (skip {skip_pct:.0f}%) | {len(clean_lines)} lines | -{halluc_count} halluc")
            completed_files.append({"file": wav.name, "date": date_dir, "lines": len(clean_lines), "time_s": round(elapsed, 1)})

    except Exception as e:
        print(f"  FAILED: {e}")
        import traceback; traceback.print_exc()
        failed += 1
        discord_notify(f"❌ **转录失败** `{wav.name}`\n```{e}```", color=0xE74C3C)

    # Milestone: notify every 25% or every 10 files
    milestone_interval = max(len(all_new) // 4, 1)
    if i % milestone_interval == 0 and i < len(all_new):
        elapsed_total = time.time() - batch_start
        avg_per_file = elapsed_total / i
        eta_s = avg_per_file * (len(all_new) - i)
        eta_min = int(eta_s / 60)
        discord_notify(
            f"📊 **进度 {i}/{len(all_new)}** ({i*100//len(all_new)}%)\n"
            f"已用: {int(elapsed_total/60)}min | 预计剩余: ~{eta_min}min\n"
            f"失败: {failed}",
            color=0xF39C12
        )

total_elapsed = time.time() - batch_start
total_min = int(total_elapsed / 60)

print(f"\n=== Done: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")
print(f"Transcribed: {len(all_new)-failed} | Failed: {failed} | Skipped: {skip_count} | Time: {total_min}min")
if ENGINE == "whisper":
    print(f"Hallucinations removed: {total_halluc}")

# ── Final progress + notification ──
write_progress({
    "status": "done", "total": len(all_new), "done": len(all_new) - failed,
    "failed": failed, "elapsed_s": int(total_elapsed),
    "completed": completed_files[-10:]  # last 10 for brevity
})

discord_notify(
    f"✅ **转录完成**\n"
    f"成功: **{len(all_new)-failed}** | 失败: {failed} | 跳过: {skip_count}\n"
    f"总耗时: **{total_min}min** | 引擎: `{ENGINE}`",
    color=0x2ECC71 if failed == 0 else 0xE67E22
)

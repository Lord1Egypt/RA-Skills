#!/usr/bin/env python3
"""Read config.json and output values as shell sourceable format, or merge SRT+diarization."""
import json
import sys
import os


def load_config(config_path):
    defaults = {
        'watch_dir': '',
        'archive_dir': '',
        'obsidian_vault': '',
        'obsidian_subdir': 'Journal/Transcripts',
        'whisper_binary': 'whisper-cli',
        'whisper_model': 'ggml-base.bin',
        'whisper_model_path': '/usr/local/share/whisper-models',
        'sync_method': 'icloud' if sys.platform == 'darwin' else 'syncthing',
        'sync_delay_icloud': 60,
        'sync_delay_syncthing': 10,
        'sync_delay_manual': 10,
        'speaker_count': 0,
        'language': 'en',
        'diarization': True,
        'denoise': True,
        'vad': False,
        'vad_model_path': '',
        'mirror': 'auto',
        'agent_cli': 'auto',
        'icloud_watch_subdir': 'VoiceRecordings',
        'note_mode': 'markdown',
        'obsidian_index': 'Recording Index',
    }
    with open(config_path, encoding='utf-8') as f:
        config = json.load(f)
    merged = {}
    for k, dv in defaults.items():
        v = config.get(k, dv)
        merged[k] = v
    if not merged['vad_model_path']:
        merged['vad_model_path'] = os.path.join(
            str(merged['whisper_model_path']), 'ggml-silero-v6.2.0.bin'
        )

    raw_watch_dir = config.get('watch_dir', '')
    user_specified_watch_dir = bool(raw_watch_dir) and raw_watch_dir != '~/Recordings/raw'
    if merged['sync_method'] == 'icloud' and not user_specified_watch_dir:
        icloud_root = os.path.expanduser('~/Library/Mobile Documents/com~apple~CloudDocs')
        merged['watch_dir'] = os.path.join(icloud_root, merged['icloud_watch_subdir'])
        os.makedirs(merged['watch_dir'], exist_ok=True)

    path_keys = ('watch_dir', 'archive_dir', 'obsidian_vault', 'whisper_model_path', 'vad_model_path')
    for k in path_keys:
        merged[k] = os.path.expanduser(str(merged[k]))
    return merged


def cmd_shell(config_path):
    config = load_config(config_path)
    for k, v in config.items():
        if isinstance(v, bool):
            print(f"{k}={'true' if v else 'false'}")
        elif isinstance(v, (int, float)):
            print(f"{k}={v}")
        else:
            print(f"{k}={json.dumps(str(v), ensure_ascii=False)}")


def cmd_merge(workdir, diarization_enabled_str):
    srt_path = os.path.join(workdir, 'transcript.srt')
    segments = []
    with open(srt_path, encoding='utf-8') as f:
        content = f.read()

    for block in content.strip().split('\n\n'):
        parts = block.split('\n')
        if len(parts) >= 3:
            time_line = parts[1]
            text = ' '.join(parts[2:])
            time_parts = time_line.split(' --> ')
            start_str = time_parts[0].replace(',', '.')
            start_components = start_str.split(':')
            start_sec = float(start_components[0]) * 3600 + float(start_components[1]) * 60 + float(start_components[2])
            segments.append({'start': start_sec, 'text': text})

    diarization_enabled = diarization_enabled_str.lower() in ('true', '1')
    diarization_path = os.path.join(workdir, 'diarization.json')
    if diarization_enabled and os.path.exists(diarization_path):
        with open(diarization_path, encoding='utf-8') as f:
            diarization_data = json.load(f)
    else:
        diarization_data = []

    output = []
    for seg in segments:
        seg_start = seg['start']
        seg_text = seg['text']
        speaker = '?'
        for ds in diarization_data:
            if ds['start'] <= seg_start <= ds['end']:
                speaker = ds['speaker']
                break
        ts = f'{int(seg_start // 60):02d}:{int(seg_start % 60):02d}'
        if diarization_enabled:
            output.append(f'[{ts}] **{speaker}**: {seg_text}')
        else:
            output.append(f'[{ts}] {seg_text}')

    transcript_text = '\n'.join(output)
    out_path = os.path.join(workdir, 'raw_transcript.md')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(transcript_text)
    print(transcript_text)


def cmd_speaker_names(workdir, language):
    labels = [f'Speaker {c}' for c in 'ABCDEFGHIJ']

    diarization_path = os.path.join(workdir, 'diarization.json')
    with open(diarization_path, encoding='utf-8') as f:
        data = json.load(f)

    raw_speakers = sorted(
        set(s['speaker'] for s in data),
        key=lambda s: int(s.split('_')[1]) if s.startswith('Speaker_') else 99
    )
    speaker_display = [
        labels[int(s.split('_')[1])] if s.startswith('Speaker_') and int(s.split('_')[1]) < len(labels) else s
        for s in raw_speakers
    ]

    name_mapping = {}
    for s in raw_speakers:
        idx = int(s.split('_')[1]) if s.startswith('Speaker_') else 99
        if idx < len(labels):
            name_mapping[s] = labels[idx]

    for seg in data:
        s = seg['speaker']
        if s in name_mapping:
            seg['speaker'] = name_mapping[s]

    with open(diarization_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)

    print(', '.join(speaker_display))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: read_config.py shell <config_path>", file=sys.stderr)
        print("       read_config.py merge <workdir> <diarization_enabled>", file=sys.stderr)
        print("       read_config.py speaker_names <workdir> <language>", file=sys.stderr)
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == 'shell':
        cmd_shell(sys.argv[2])
    elif cmd == 'merge':
        cmd_merge(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else 'false')
    elif cmd == 'speaker_names':
        cmd_speaker_names(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else 'en')
    else:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        sys.exit(1)

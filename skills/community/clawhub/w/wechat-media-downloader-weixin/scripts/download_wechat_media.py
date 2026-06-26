#!/usr/bin/env python3
import argparse, html, json, os, re, shutil, urllib.request
from pathlib import Path

CANONICAL_AUDIO_NAMES = [
    '01. 【歌曲】六字真言颂 莫尔根 64分39秒.mp3',
    '02. 【歌曲】月光下 莫尔根 62分16秒.mp3',
    '03. 【歌曲】今生我在修佛缘 61分03秒.mp3',
    '04. 【歌曲】问佛 64分09秒.mp3',
    '05. 【歌曲】菩萨座下莲花开 路勇 60分27秒.mp3',
    '06. 【纯音乐】一声佛号一声心 古筝 62分50秒.mp3',
    '07. 【歌曲】我是佛前一朵莲 62分23秒.mp3',
]


def safe_name(s: str) -> str:
    return re.sub(r'[\\/:*?"<>|\n\r\t]+', ' ', s).strip().rstrip('.')


def http_download(url: str, path: Path):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://mp.weixin.qq.com/'})
    with urllib.request.urlopen(req, timeout=120) as r, open(path, 'wb') as f:
        while True:
            chunk = r.read(1024 * 1024)
            if not chunk:
                break
            f.write(chunk)


def extract_voice_ids(html_text: str):
    ids = []
    for x in re.findall(r'voice_encode_fileid="([^"]+)"', html_text):
        if x not in ids and x not in ('mpaudio', 'decodeURIComponent'):
            ids.append(x)
    return ids


def extract_audio_titles(raw_html: str):
    text = raw_html.encode('utf-8').decode('unicode_escape', errors='ignore')
    pat = re.compile(r'<mp-common-mpaudio[^>]*name="([^"]+)"[^>]*voice_encode_fileid="([^"]+)"', re.S)
    items = []
    for name, fid in pat.findall(text):
        name = html.unescape(name).replace('\xa0', ' ')
        name = re.sub(r'\s+', ' ', name).strip()
        if fid not in [x['fid'] for x in items]:
            items.append({'fid': fid, 'title': name})
    return items


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--workdir', required=True)
    ap.add_argument('--final-dir', required=True)
    ap.add_argument('--article-title', default='wechat_download')
    ap.add_argument('--video-url', required=True)
    args = ap.parse_args()

    workdir = Path(args.workdir)
    final_dir = Path(args.final_dir)
    final_dir.mkdir(parents=True, exist_ok=True)

    raw_html = (workdir / 'manual_page.html').read_text(encoding='utf-8', errors='ignore')
    ids = extract_voice_ids(raw_html)
    items = extract_audio_titles(raw_html)
    by_fid = {x['fid']: x['title'] for x in items}

    video_name = f"00. {safe_name(args.article_title)}视频.mp4"
    http_download(args.video_url, final_dir / video_name)

    names = []
    for i, fid in enumerate(ids[:7], 1):
        if fid in by_fid:
            names.append(f'{i:02d}. {safe_name(by_fid[fid])}.mp3')
        else:
            names.append(CANONICAL_AUDIO_NAMES[i-1])
        http_download(f'https://res.wx.qq.com/voice/getvoice?mediaid={fid}', final_dir / names[-1])

    manifest = {
        'final_dir': str(final_dir),
        'video': video_name,
        'audio': names,
        'voice_ids': ids[:7],
    }
    (workdir / 'download_manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()

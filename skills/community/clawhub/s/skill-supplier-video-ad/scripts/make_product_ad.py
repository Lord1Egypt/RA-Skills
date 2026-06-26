#!/usr/bin/env python3
"""
make_product_ad.py — Supplier Video Ad Builder (Main Pipeline)
Assembles a 1080×1920 TikTok/IG Reels ad from clean video zones + text + CTA card + music.

Usage:
    python3 make_product_ad.py <product_config.json>

Output:
    output/<output_name>   (final ready-to-post MP4)

Requirements:
    pip install Pillow
    ffmpeg + ffprobe in PATH
    Montserrat-Bold.ttf (or any TTF font — set font_path in config)
"""

import subprocess
import json
import argparse
import shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920

# Default font — override via "font_path" in product config
DEFAULT_FONT = 'Montserrat-Bold.ttf'


def run(cmd, label=''):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f'ERROR [{label}]:\n{r.stderr[-800:]}')
        raise SystemExit(1)
    if label:
        print(f'  ✅ {label}')
    return r


def get_duration(path):
    r = subprocess.run(
        ['ffprobe', '-v', 'quiet', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(path)],
        capture_output=True, text=True
    )
    return float(r.stdout.strip())


def make_text_png(lines, fontsize, y_pct, out_path, font_path):
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_path, fontsize)
    gap = 16
    bbs = [draw.textbbox((0, 0), l, font=font) for l in lines]
    ws = [b[2] - b[0] for b in bbs]
    hs = [b[3] - b[1] for b in bbs]
    tot = sum(hs) + gap * (len(lines) - 1)
    y = int(H * y_pct) - tot // 2
    for i, line in enumerate(lines):
        x = (W - ws[i]) // 2
        # Shadow layers
        for dx, dy, alpha in [(3, 3, 180), (2, 2, 140), (1, 1, 100), (4, 4, 120)]:
            draw.text((x + dx, y + dy), line, font=font, fill=(0, 0, 0, alpha))
        draw.text((x, y), line, font=font, fill=(255, 255, 255, 255))
        y += hs[i] + gap
    img.save(str(out_path), 'PNG')


def make_cta_card(cfg, font_path, out_path):
    cta = cfg['cta']
    bg = tuple(cta.get('bg_color', [8, 8, 14]))
    logo_path = cta.get('logo_path')

    img = Image.new('RGB', (W, H), bg)

    # Glow effect
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for r in range(260, 0, -20):
        alpha = int(12 * (1 - r / 260))
        gd.ellipse([W // 2 - r * 2, 480 - r, W // 2 + r * 2, 480 + r], fill=(60, 80, 160, alpha))
    img = Image.alpha_composite(img.convert('RGBA'), glow).convert('RGB')
    draw = ImageDraw.Draw(img)

    # Logo (optional)
    logo_bottom = 560
    if logo_path and Path(logo_path).exists():
        logo_raw = Image.open(logo_path).convert('RGBA')
        scale = 400 / logo_raw.width
        logo = logo_raw.resize((400, int(logo_raw.height * scale)), Image.LANCZOS)
        img.paste(logo, ((W - logo.width) // 2, 560), logo)
        logo_bottom = 560 + logo.height

    # Divider
    line_y = logo_bottom + 50
    draw.line([(W // 2 - 180, line_y), (W // 2 + 180, line_y)], fill=(80, 80, 100), width=2)

    # Price
    font_price = ImageFont.truetype(font_path, 110)
    price_text = cta['price']
    pb = draw.textbbox((0, 0), price_text, font=font_price)
    px = (W - (pb[2] - pb[0])) // 2
    py = line_y + 60
    draw.text((px + 3, py + 3), price_text, font=font_price, fill=(0, 0, 0, 180))
    draw.text((px, py), price_text, font=font_price, fill=(255, 255, 255))

    # CTA line 1
    font_l1 = ImageFont.truetype(font_path, 58)
    l1 = cta.get('line1', 'Link in bio  🛒')
    bb = draw.textbbox((0, 0), l1, font=font_l1)
    bx = (W - (bb[2] - bb[0])) // 2
    by = py + (pb[3] - pb[1]) + 40
    draw.text((bx + 2, by + 2), l1, font=font_l1, fill=(0, 0, 0, 150))
    draw.text((bx, by), l1, font=font_l1, fill=(220, 220, 230))

    # CTA line 2 (URL)
    font_l2 = ImageFont.truetype(font_path, 46)
    l2 = cta.get('line2', '')
    if l2:
        ub = draw.textbbox((0, 0), l2, font=font_l2)
        ux = (W - (ub[2] - ub[0])) // 2
        uy = by + (bb[3] - bb[1]) + 28
        draw.text((ux, uy), l2, font=font_l2, fill=(140, 140, 180))

    img.save(str(out_path))


def main():
    parser = argparse.ArgumentParser(description='Build a supplier video product ad')
    parser.add_argument('config', help='Product config JSON path')
    parser.add_argument('--output-dir', default='output', help='Output directory (default: ./output)')
    args = parser.parse_args()

    cfg = json.loads(Path(args.config).read_text())
    font_path = cfg.get('font_path', DEFAULT_FONT)
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    tmp = out_dir / f'_tmp_{cfg["output_name"].replace(".mp4","")}'
    tmp.mkdir(parents=True, exist_ok=True)
    out_final = out_dir / cfg['output_name']

    print(f'\n🎬 Building: {cfg["product_name"]}')
    print(f'   Output: {out_final}')

    # ── 1. Cut clean segments ──
    seg_files = []
    for i, zone in enumerate(cfg['clean_zones']):
        src = Path(cfg['source_videos'][zone['source']])
        pts = '1.25*PTS' if zone.get('slowmo') else 'PTS'
        seg = tmp / f's{i}.mp4'
        vf = (
            f'scale={W}:{H}:force_original_aspect_ratio=decrease,'
            f'pad={W}:{H}:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30,'
            f'setpts={pts}'
        )
        run([
            'ffmpeg', '-y', '-i', str(src),
            '-ss', str(zone['ss']), '-t', str(zone['dur']),
            '-vf', vf, '-an',
            '-c:v', 'libx264', '-preset', 'fast', '-crf', '17',
            str(seg)
        ], f's{i} ({zone["label"]})')
        seg_files.append(seg)

    # ── 2. Concat segments ──
    list_txt = tmp / 'list.txt'
    list_txt.write_text('\n'.join(f"file '{f}'" for f in seg_files))
    raw = tmp / 'raw.mp4'
    run(['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', str(list_txt), '-c', 'copy', str(raw)], 'concat')
    total_dur = get_duration(raw)
    print(f'   Duration: {total_dur:.1f}s')

    # ── 3. Text overlays ──
    text_pngs = []
    for i, ov in enumerate(cfg.get('text_overlays', [])):
        png = tmp / f'txt_{i}.png'
        make_text_png(ov['lines'], ov['fontsize'], ov['y_pct'], png, font_path)
        text_pngs.append((str(png), ov['start'], ov['end']))
    if text_pngs:
        print(f'  ✅ {len(text_pngs)} text overlays rendered')

    # ── 4. CTA end card ──
    cta_dur = cfg['cta']['duration']
    cta_png = tmp / 'cta.png'
    make_cta_card(cfg, font_path, cta_png)
    cta_clip = tmp / 'cta.mp4'
    run([
        'ffmpeg', '-y', '-loop', '1', '-i', str(cta_png),
        '-vf', 'fps=30,format=yuv420p', '-t', str(cta_dur),
        '-an', '-c:v', 'libx264', '-preset', 'fast', '-crf', '18',
        str(cta_clip)
    ], f'CTA clip ({cta_dur}s)')

    # ── 5. Concat video + CTA ──
    full_list = tmp / 'full_list.txt'
    full_list.write_text(f"file '{raw}'\nfile '{cta_clip}'")
    full_raw = tmp / 'full_raw.mp4'
    run(['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', str(full_list), '-c', 'copy', str(full_raw)], 'video+CTA')
    full_dur = get_duration(full_raw)

    # ── 6. Overlay text ──
    if text_pngs:
        inputs = ['-i', str(full_raw)]
        for png, _, _ in text_pngs:
            inputs += ['-i', png]
        filter_parts = []
        cur = '[0:v]'
        for i, (png, ts, te) in enumerate(text_pngs):
            vi = f'[{i+1}:v]'
            out_label = f'[ot{i}]' if i < len(text_pngs) - 1 else '[vfinal]'
            filter_parts.append(f"{cur}{vi}overlay=0:0:enable='between(t,{ts},{te})'{out_label}")
            cur = f'[ot{i}]'
        text_overlaid = tmp / 'text_overlaid.mp4'
        run([
            'ffmpeg', '-y', *inputs,
            '-filter_complex', '; '.join(filter_parts),
            '-map', '[vfinal]', '-an',
            '-c:v', 'libx264', '-preset', 'fast', '-crf', '17',
            str(text_overlaid)
        ], 'text overlay')
    else:
        text_overlaid = full_raw

    # ── 7. Mux audio ──
    audio_path = Path(cfg['audio'])
    audio_offset = cfg.get('audio_start_offset', 2)
    vol = cfg.get('audio_volume', 0.88)
    fade_out_start = max(0, full_dur - 1.2)

    run([
        'ffmpeg', '-y',
        '-i', str(text_overlaid),
        '-ss', str(audio_offset), '-i', str(audio_path),
        '-filter_complex',
        f'[1:a]atrim=0:{full_dur},afade=t=in:st=0:d=0.5,'
        f'afade=t=out:st={fade_out_start}:d=1.2,'
        f'asetpts=PTS-STARTPTS,volume={vol}[music]',
        '-map', '0:v', '-map', '[music]',
        '-c:v', 'copy', '-c:a', 'aac', '-b:a', '128k',
        '-t', str(full_dur),
        str(out_final)
    ], 'final mux')

    # Cleanup
    shutil.rmtree(tmp)

    mb = out_final.stat().st_size // 1024 // 1024
    print(f'\n🎬 Done: {out_final.name} — {mb}MB, {full_dur:.1f}s')
    print(f'   Ready to post on TikTok / Instagram Reels')


if __name__ == '__main__':
    main()

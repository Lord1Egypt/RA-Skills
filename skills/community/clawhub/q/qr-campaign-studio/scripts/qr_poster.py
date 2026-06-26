#!/usr/bin/env python3
import argparse
import os


def main():
    try:
        from PIL import Image
    except Exception as e:
        raise SystemExit('Missing deps: pip install pillow') from e

    ap = argparse.ArgumentParser(description='Compose poster with QR image')
    ap.add_argument('--bg', required=True, help='background image path')
    ap.add_argument('--qr', required=True, help='qr image path')
    ap.add_argument('--out', required=True)
    ap.add_argument('--x', type=int, required=True)
    ap.add_argument('--y', type=int, required=True)
    ap.add_argument('--size', type=int, default=260)
    ap.add_argument('--opacity', type=float, default=1.0)
    args = ap.parse_args()

    bg = Image.open(args.bg).convert('RGBA')
    qr = Image.open(args.qr).convert('RGBA').resize((args.size, args.size), Image.LANCZOS)

    if args.opacity < 1.0:
        a = qr.split()[-1].point(lambda v: int(v * max(0.0, min(1.0, args.opacity))))
        qr.putalpha(a)

    bg.alpha_composite(qr, (args.x, args.y))
    os.makedirs(os.path.dirname(args.out) or '.', exist_ok=True)
    if args.out.lower().endswith(('.jpg', '.jpeg')):
        bg.convert('RGB').save(args.out, quality=95)
    else:
        bg.save(args.out)
    print(args.out)


if __name__ == '__main__':
    main()

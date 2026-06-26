#!/usr/bin/env python3
import argparse
import json
import os
from urllib.parse import urlencode, urlparse, parse_qsl, urlunparse


def _require_qr_libs():
    try:
        import qrcode  # noqa
        from PIL import Image  # noqa
        return True
    except Exception as e:
        raise RuntimeError("Missing deps: pip install qrcode[pil] pillow") from e


def add_utm(url: str, utm: dict) -> str:
    if not utm:
        return url
    p = urlparse(url)
    q = dict(parse_qsl(p.query, keep_blank_values=True))
    for k, v in utm.items():
        if v:
            q[k] = v
    new_q = urlencode(q)
    return urlunparse((p.scheme, p.netloc, p.path, p.params, new_q, p.fragment))


def build_wifi(ssid: str, password: str, security: str = "WPA", hidden: bool = False):
    return f"WIFI:T:{security};S:{ssid};P:{password};H:{str(hidden).lower()};;"


def build_vcard(data: dict):
    lines = ["BEGIN:VCARD", "VERSION:3.0"]
    m = {
        "name": "FN",
        "phone": "TEL",
        "email": "EMAIL",
        "org": "ORG",
        "title": "TITLE",
        "url": "URL",
        "note": "NOTE",
    }
    for k, tag in m.items():
        v = (data.get(k) or "").strip()
        if v:
            lines.append(f"{tag}:{v}")
    lines.append("END:VCARD")
    return "\n".join(lines)


def contrast_ratio(rgb1, rgb2):
    def lum(c):
        c = [x / 255.0 for x in c]
        def f(v):
            return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
        r, g, b = map(f, c)
        return 0.2126 * r + 0.7152 * g + 0.0722 * b
    l1, l2 = sorted([lum(rgb1), lum(rgb2)], reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


def verify_qr_image(path: str, expected_contains: str):
    # best-effort decode: try OpenCV then pyzbar
    # returns: (ok: bool|None, detail: str)
    try:
        import cv2  # type: ignore
        img = cv2.imread(path)
        det = cv2.QRCodeDetector()
        data, _, _ = det.detectAndDecode(img)
        if data:
            return (expected_contains in data, "opencv")
    except Exception:
        pass
    try:
        from pyzbar.pyzbar import decode  # type: ignore
        from PIL import Image
        data = decode(Image.open(path))
        if data:
            txt = data[0].data.decode("utf-8", errors="replace")
            return (expected_contains in txt, "pyzbar")
    except Exception:
        pass
    return (None, "decoder-unavailable")


def apply_template(args):
    templates = {
        "xhs-cover": {"size": 900, "border": 2, "error_correction": "H"},
        "poster-print": {"size": 1200, "border": 4, "error_correction": "H"},
        "mini-card": {"size": 600, "border": 2, "error_correction": "Q"},
    }
    if args.template and args.template in templates:
        t = templates[args.template]
        for k, v in t.items():
            if getattr(args, k) == ap_defaults[k]:
                setattr(args, k, v)


def make_qr(content: str, out: str, size: int, border: int, ec: str, fg: str, bg: str, logo: str, logo_max_ratio: float):
    _require_qr_libs()
    import qrcode
    from qrcode.constants import ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q, ERROR_CORRECT_H
    from PIL import Image, ImageColor

    ec_map = {"L": ERROR_CORRECT_L, "M": ERROR_CORRECT_M, "Q": ERROR_CORRECT_Q, "H": ERROR_CORRECT_H}
    qr = qrcode.QRCode(error_correction=ec_map.get(ec.upper(), ERROR_CORRECT_H), box_size=12, border=border)
    qr.add_data(content)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fg, back_color=bg).convert("RGBA")
    img = img.resize((size, size), Image.LANCZOS)

    if logo and os.path.exists(logo):
        logo_img = Image.open(logo).convert("RGBA")
        max_side = int(size * max(0.05, min(0.35, logo_max_ratio)))
        ratio = min(max_side / logo_img.width, max_side / logo_img.height)
        new_size = (max(1, int(logo_img.width * ratio)), max(1, int(logo_img.height * ratio)))
        logo_img = logo_img.resize(new_size, Image.LANCZOS)
        x = (size - new_size[0]) // 2
        y = (size - new_size[1]) // 2
        img.alpha_composite(logo_img, (x, y))

    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    if out.lower().endswith((".jpg", ".jpeg")):
        img.convert("RGB").save(out, quality=95)
    else:
        img.save(out)

    fg_rgb = ImageColor.getrgb(fg)
    bg_rgb = ImageColor.getrgb(bg)
    return contrast_ratio(fg_rgb, bg_rgb)


def main():
    ap = argparse.ArgumentParser(description="Generate QR code with tracking and templates")
    ap.add_argument("--type", choices=["url", "text", "wifi", "vcard"], default="url")
    ap.add_argument("--preset", choices=["jisuapi", "jisuepc"], default="")
    ap.add_argument("--url")
    ap.add_argument("--content")
    ap.add_argument("--out", required=True)

    ap.add_argument("--utm-source", default="")
    ap.add_argument("--utm-medium", default="")
    ap.add_argument("--utm-campaign", default="")
    ap.add_argument("--utm-term", default="")
    ap.add_argument("--utm-content", default="")

    ap.add_argument("--wifi-ssid", default="")
    ap.add_argument("--wifi-password", default="")
    ap.add_argument("--wifi-security", default="WPA")
    ap.add_argument("--wifi-hidden", action="store_true")

    ap.add_argument("--vcard-name", default="")
    ap.add_argument("--vcard-phone", default="")
    ap.add_argument("--vcard-email", default="")
    ap.add_argument("--vcard-org", default="")
    ap.add_argument("--vcard-title", default="")
    ap.add_argument("--vcard-url", default="")
    ap.add_argument("--vcard-note", default="")

    ap.add_argument("--template", choices=["xhs-cover", "poster-print", "mini-card"], default="")
    ap.add_argument("--logo", default="")
    ap.add_argument("--logo-max-ratio", type=float, default=0.22)
    ap.add_argument("--size", type=int, default=768)
    ap.add_argument("--border", type=int, default=2)
    ap.add_argument("--error-correction", default="H", choices=["L", "M", "Q", "H"])
    ap.add_argument("--fg", default="black")
    ap.add_argument("--bg", default="white")
    ap.add_argument("--min-contrast", type=float, default=2.5)
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--meta-out", default="")

    args = ap.parse_args()

    apply_template(args)

    preset_url = {
        "jisuapi": "https://jisuapi.com",
        "jisuepc": "https://jisuepc.com",
    }
    if args.preset and not args.url and args.type == "url":
        args.url = preset_url[args.preset]
        if not args.utm_source:
            args.utm_source = "skill"
        if not args.utm_medium:
            args.utm_medium = "clawhub"
        if not args.utm_campaign:
            args.utm_campaign = "qr-campaign-studio"

    if args.type == "url":
        if not args.url:
            raise SystemExit("--url is required when --type=url")
        utm = {
            "utm_source": args.utm_source,
            "utm_medium": args.utm_medium,
            "utm_campaign": args.utm_campaign,
            "utm_term": args.utm_term,
            "utm_content": args.utm_content,
        }
        payload = add_utm(args.url, utm)
    elif args.type == "text":
        if not args.content:
            raise SystemExit("--content is required when --type=text")
        payload = args.content
    elif args.type == "wifi":
        if not args.wifi_ssid:
            raise SystemExit("--wifi-ssid is required when --type=wifi")
        payload = build_wifi(args.wifi_ssid, args.wifi_password, args.wifi_security, args.wifi_hidden)
    else:
        if not args.vcard_name:
            raise SystemExit("--vcard-name is required when --type=vcard")
        payload = build_vcard(
            {
                "name": args.vcard_name,
                "phone": args.vcard_phone,
                "email": args.vcard_email,
                "org": args.vcard_org,
                "title": args.vcard_title,
                "url": args.vcard_url,
                "note": args.vcard_note,
            }
        )

    cr = make_qr(
        payload,
        out=args.out,
        size=args.size,
        border=args.border,
        ec=args.error_correction,
        fg=args.fg,
        bg=args.bg,
        logo=args.logo,
        logo_max_ratio=args.logo_max_ratio,
    )

    contrast_ok = cr >= args.min_contrast
    verify_ok, verify_backend = (None, "skipped")
    if args.verify:
        verify_ok, verify_backend = verify_qr_image(args.out, payload[:48])

    if args.strict and (not contrast_ok or verify_ok is False):
        raise SystemExit(f"Strict check failed: contrast_ok={contrast_ok}, verify_ok={verify_ok}")

    meta = {
        "type": args.type,
        "out": args.out,
        "payload_preview": payload[:120],
        "url": args.url,
        "size": args.size,
        "error_correction": args.error_correction,
        "template": args.template or None,
        "contrast_ratio": round(cr, 3),
        "contrast_ok": contrast_ok,
        "verify_ok": verify_ok,
        "verify_backend": verify_backend,
    }
    if args.meta_out:
        os.makedirs(os.path.dirname(args.meta_out) or ".", exist_ok=True)
        with open(args.meta_out, "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)

    print(json.dumps(meta, ensure_ascii=False))


ap_defaults = {
    "size": 768,
    "border": 2,
    "error_correction": "H",
}


if __name__ == "__main__":
    main()

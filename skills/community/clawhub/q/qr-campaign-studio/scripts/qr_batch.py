#!/usr/bin/env python3
import argparse
import csv
import json
import os
import subprocess
import sys


def iter_rows(path: str):
    if path.lower().endswith('.json'):
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if not isinstance(data, list):
            raise ValueError('JSON input must be a list')
        for row in data:
            yield row
    else:
        with open(path, 'r', encoding='utf-8-sig', newline='') as f:
            r = csv.DictReader(f)
            for row in r:
                yield row


def main():
    ap = argparse.ArgumentParser(description='Batch generate QR codes from CSV/JSON')
    ap.add_argument('--input', required=True)
    ap.add_argument('--output-dir', required=True)
    ap.add_argument('--default-utm-source', default='')
    ap.add_argument('--default-utm-medium', default='')
    ap.add_argument('--default-utm-campaign', default='')
    ap.add_argument('--logo', default='')
    ap.add_argument('--template', choices=['xhs-cover', 'poster-print', 'mini-card'], default='')
    ap.add_argument('--verify', action='store_true')
    ap.add_argument('--strict', action='store_true')
    ap.add_argument('--report-out', default='')
    args = ap.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    script = os.path.join(os.path.dirname(__file__), 'qr_generate.py')

    ok, fail = 0, 0
    details = []
    for i, row in enumerate(iter_rows(args.input), start=1):
        name = (row.get('name') or f'item-{i}').strip()
        typ = (row.get('type') or 'url').strip()
        out = os.path.join(args.output_dir, f'{name}.png')
        meta_out = os.path.join(args.output_dir, f'{name}.meta.json')

        cmd = [
            sys.executable,
            script,
            '--type', typ,
            '--out', out,
            '--meta-out', meta_out,
            '--logo', row.get('logo') or args.logo,
        ]
        if args.template:
            cmd += ['--template', args.template]
        if args.verify:
            cmd += ['--verify']
        if args.strict:
            cmd += ['--strict']

        if typ == 'url':
            cmd += ['--url', row.get('url', '')]
            cmd += ['--utm-source', row.get('utm_source') or args.default_utm_source]
            cmd += ['--utm-medium', row.get('utm_medium') or args.default_utm_medium]
            cmd += ['--utm-campaign', row.get('utm_campaign') or args.default_utm_campaign]
            cmd += ['--utm-term', row.get('utm_term', '')]
            cmd += ['--utm-content', row.get('utm_content', '')]
        elif typ == 'text':
            cmd += ['--content', row.get('content', '')]
        elif typ == 'wifi':
            cmd += ['--wifi-ssid', row.get('wifi_ssid', '')]
            cmd += ['--wifi-password', row.get('wifi_password', '')]
            cmd += ['--wifi-security', row.get('wifi_security', 'WPA')]
        elif typ == 'vcard':
            cmd += ['--vcard-name', row.get('vcard_name', '')]
            cmd += ['--vcard-phone', row.get('vcard_phone', '')]
            cmd += ['--vcard-email', row.get('vcard_email', '')]
            cmd += ['--vcard-org', row.get('vcard_org', '')]
            cmd += ['--vcard-title', row.get('vcard_title', '')]
            cmd += ['--vcard-url', row.get('vcard_url', '')]
            cmd += ['--vcard-note', row.get('vcard_note', '')]

        p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if p.returncode == 0:
            ok += 1
            status = 'ok'
            err = ''
        else:
            fail += 1
            status = 'fail'
            err = p.stderr.strip()

        details.append({'name': name, 'type': typ, 'out': out, 'status': status, 'error': err})

    report = {'ok': ok, 'fail': fail, 'output_dir': args.output_dir, 'details': details}
    if args.report_out:
        with open(args.report_out, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
    print(json.dumps(report, ensure_ascii=False))


if __name__ == '__main__':
    main()

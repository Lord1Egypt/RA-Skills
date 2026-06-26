#!/usr/bin/env python3
from __future__ import annotations

import argparse
import asyncio
import csv
import html
import json
import re
import sys
import urllib.parse
import urllib.request
import http.cookiejar
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Optional

import websockets
from google.protobuf import descriptor_pb2, descriptor_pool, message_factory

STP_BASE = 'https://www.swisstargetprediction.ch'
ADMET_BASE = 'https://admetlab3.scbdd.com'
PK_BASE = 'https://pk-predictor.serve.scilifelab.se/PKSmart_Batch_SMILES'
PK_PAGE_HASH = '55b2cf889641d02bcf0b7088b39a69c1'
PK_TEXTAREA_ID = ''.join(['$', '$', 'ID-58ae886c2ef04b2b7e19c7b6a9635164-None'])
PK_BUTTON_ID = ''.join(['$', '$', 'ID-fc0ea701f1cb472a675de2ed3069c09e-None'])
COMMON_COUNTERIONS = {
    '[Na+]', '[K+]', '[Li+]', '[Mg+2]', '[Ca+2]', '[Cl-]', '[Br-]', '[I-]', '[H+]'
}


@dataclass
class ToolResult:
    ok: bool
    note: str
    data: dict


def make_opener() -> urllib.request.OpenerDirector:
    jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
    opener.addheaders = [
        ('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'),
        ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
        ('Accept-Language', 'en-US,en;q=0.5'),
    ]
    return opener


def fetch(opener, url: str, data: Optional[dict] = None, referer: Optional[str] = None) -> tuple[int, str]:
    headers = {}
    if referer:
        headers['Referer'] = referer
    if data is None:
        req = urllib.request.Request(url, headers=headers)
    else:
        body = urllib.parse.urlencode(data).encode('utf-8')
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        req = urllib.request.Request(url, data=body, headers=headers)
    with opener.open(req, timeout=60) as resp:
        text = resp.read().decode('utf-8', errors='replace')
        return resp.status, text


def is_obviously_malformed(smiles: str) -> bool:
    if not smiles or ' ' in smiles:
        return True
    if smiles.count('(') != smiles.count(')'):
        return True
    return False


def normalize_smiles(smiles: str) -> str:
    smiles = smiles.strip()
    if '.' not in smiles:
        return smiles

    parts = [p for p in smiles.split('.') if p]
    organic = [p for p in parts if p not in COMMON_COUNTERIONS]
    chosen = max(organic or parts, key=len)

    # Lightweight cleanup for simple carboxylate salts.
    chosen = chosen.replace('C(=O)[O-]', 'C(=O)O')
    chosen = chosen.replace('O=C([O-])', 'O=C(O)')
    return chosen


def extract_sections(html_text: str) -> list[str]:
    return [html.unescape(x) for x in re.findall(r'<div class="sub-title(?: mt-5)?"(?: style="[^"]*")?>(.*?)</div>', html_text)]


def run_stp(opener, smiles: str) -> ToolResult:
    try:
        if is_obviously_malformed(smiles):
            return ToolResult(False, 'STP preflight rejected malformed SMILES', {'status': 'invalid'})
        smiles = normalize_smiles(smiles)
        fetch(opener, f'{STP_BASE}/index.php')
        status, submitted = fetch(
            opener,
            f'{STP_BASE}/predict.php',
            data={'organism': 'Homo_sapiens', 'smiles': smiles, 'ioi': '2'},
            referer=f'{STP_BASE}/index.php',
        )
        if status != 200:
            return ToolResult(False, f'STP submit HTTP {status}', {'status': status})
        if 'not valid' in submitted.lower() or 'invalid' in submitted.lower():
            return ToolResult(False, 'STP rejected SMILES', {'status': 'invalid'})
        m = re.search(r'result\.php\?job=\d+&organism=Homo_sapiens', submitted)
        if not m:
            return ToolResult(False, 'STP missing result redirect', {'preview': submitted[:500]})
        result_url = f'{STP_BASE}/{m.group(0)}'
        _, result_html = fetch(opener, result_url, referer=f'{STP_BASE}/predict.php')
        row_count = len(re.findall(r'carddisp\.pl\?gene=', result_html))
        top_target = None
        top_prob = None
        m2 = re.search(r'<tr[^>]*>\s*<td>(.*?)</td>.*?carddisp\.pl\?gene=([A-Z0-9]+).*?<span style="opacity:0\.5; font-size:1px;";>([0-9.]+)</span>', result_html, re.S)
        if m2:
            top_target = re.sub(r'<[^>]+>', ' ', m2.group(1))
            top_target = ' '.join(top_target.split())
            top_prob = m2.group(3)
        return ToolResult(row_count > 0, 'STP ok' if row_count > 0 else 'STP no targets', {'rows': row_count, 'top_target': top_target, 'top_prob': top_prob, 'url': result_url})
    except Exception as e:
        return ToolResult(False, f'STP exception: {e}', {'exception': repr(e)})


def run_admet(opener, smiles: str) -> ToolResult:
    try:
        if is_obviously_malformed(smiles):
            return ToolResult(False, 'ADMET preflight rejected malformed SMILES', {'status': 'invalid'})
        smiles = normalize_smiles(smiles)
        _, page = fetch(opener, f'{ADMET_BASE}/server/evaluation')
        m = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', page)
        if not m:
            return ToolResult(False, 'ADMET missing csrf token', {'preview': page[:500]})
        token = m.group(1)
        status, result = fetch(
            opener,
            f'{ADMET_BASE}/server/evaluationCal',
            data={'csrfmiddlewaretoken': token, 'smiles': smiles, 'method': '1'},
            referer=f'{ADMET_BASE}/server/evaluation',
        )
        if status != 200:
            return ToolResult(False, f'ADMET submit HTTP {status}', {'status': status})
        sections = extract_sections(result)
        wanted = {'Structure', 'Medicinal Chemistry', 'Toxicity'}
        ok = wanted.issubset(set(sections))
        mw = re.search(r'<td width="60%">Molecular Weight \(MW\)</td>\s*<td width="20%">(.*?)</td>', result, re.S)
        qed = re.search(r'<td width="60%">QED</td>\s*<td width="20%">(.*?)</td>', result, re.S)
        return ToolResult(ok, 'ADMET ok' if ok else 'ADMET missing sections', {'sections': sections[:12], 'MW': mw.group(1).strip() if mw else None, 'QED': qed.group(1).strip() if qed else None})
    except Exception as e:
        return ToolResult(False, f'ADMET exception: {e}', {'exception': repr(e)})


@lru_cache(maxsize=1)
def _streamlit_proto_classes():
    fdp = descriptor_pb2.FileDescriptorProto()
    fdp.name = 'streamlit_smoke.proto'
    fdp.package = 'streamlit'

    widget_states = fdp.message_type.add(); widget_states.name = 'WidgetStates'
    widget_state = fdp.message_type.add(); widget_state.name = 'WidgetState'
    client_state = fdp.message_type.add(); client_state.name = 'ClientState'
    back_msg = fdp.message_type.add(); back_msg.name = 'BackMsg'

    f = widget_states.field.add(); f.name = 'widgets'; f.number = 1; f.label = 3; f.type = descriptor_pb2.FieldDescriptorProto.TYPE_MESSAGE; f.type_name = '.streamlit.WidgetState'

    for name, num, typ in [
        ('id', 1, descriptor_pb2.FieldDescriptorProto.TYPE_STRING),
        ('trigger_value', 2, descriptor_pb2.FieldDescriptorProto.TYPE_BOOL),
        ('string_value', 6, descriptor_pb2.FieldDescriptorProto.TYPE_STRING),
    ]:
        f = widget_state.field.add(); f.name = name; f.number = num; f.label = 1; f.type = typ

    for name, num, typ in [
        ('query_string', 1, descriptor_pb2.FieldDescriptorProto.TYPE_STRING),
        ('widget_states', 2, descriptor_pb2.FieldDescriptorProto.TYPE_MESSAGE),
        ('page_script_hash', 3, descriptor_pb2.FieldDescriptorProto.TYPE_STRING),
        ('page_name', 4, descriptor_pb2.FieldDescriptorProto.TYPE_STRING),
        ('fragment_id', 5, descriptor_pb2.FieldDescriptorProto.TYPE_STRING),
        ('is_auto_rerun', 6, descriptor_pb2.FieldDescriptorProto.TYPE_BOOL),
    ]:
        f = client_state.field.add(); f.name = name; f.number = num; f.label = 1; f.type = typ
        if name == 'widget_states':
            f.type_name = '.streamlit.WidgetStates'

    f = back_msg.field.add(); f.name = 'rerun_script'; f.number = 11; f.label = 1; f.type = descriptor_pb2.FieldDescriptorProto.TYPE_MESSAGE; f.type_name = '.streamlit.ClientState'

    pool = descriptor_pool.DescriptorPool()
    pool.Add(fdp)
    return (
        message_factory.GetMessageClass(pool.FindMessageTypeByName('streamlit.WidgetStates')),
        message_factory.GetMessageClass(pool.FindMessageTypeByName('streamlit.WidgetState')),
        message_factory.GetMessageClass(pool.FindMessageTypeByName('streamlit.ClientState')),
        message_factory.GetMessageClass(pool.FindMessageTypeByName('streamlit.BackMsg')),
    )


def run_pksmart(opener, smiles: str) -> ToolResult:
    try:
        if is_obviously_malformed(smiles):
            return ToolResult(False, 'PK-Smart preflight rejected malformed SMILES', {'status': 'invalid'})
        smiles = normalize_smiles(smiles)

        WidgetStates, WidgetState, ClientState, BackMsg = _streamlit_proto_classes()
        ws_state = WidgetStates()
        w = ws_state.widgets.add(); w.id = PK_TEXTAREA_ID; w.string_value = smiles
        b = ws_state.widgets.add(); b.id = PK_BUTTON_ID; b.trigger_value = True
        client_state = ClientState(query_string='', page_script_hash=PK_PAGE_HASH, widget_states=ws_state)
        backmsg = BackMsg(rerun_script=client_state).SerializeToString()

        csv_url = None
        async def _fetch_csv_url():
            nonlocal csv_url
            async with websockets.connect('wss://pk-predictor.serve.scilifelab.se/_stcore/stream', subprotocols=['streamlit']) as ws:
                await ws.send(backmsg)
                for _ in range(200):
                    try:
                        frame = await asyncio.wait_for(ws.recv(), timeout=10)
                    except Exception:
                        break
                    if not isinstance(frame, bytes):
                        continue
                    m = re.search(rb'/media/[0-9a-f]+\.csv', frame)
                    if m:
                        csv_url = urllib.parse.urljoin('https://pk-predictor.serve.scilifelab.se', m.group(0).decode('utf-8'))
                        return

        asyncio.run(_fetch_csv_url())
        if not csv_url:
            return ToolResult(False, 'PK-Smart missing CSV download after submit', {'mode': 'unavailable'})

        status, csv_text = fetch(opener, csv_url)
        if status != 200:
            return ToolResult(False, f'PK-Smart CSV HTTP {status}', {'status': status, 'csv_url': csv_url})
        rows = list(csv.DictReader(csv_text.splitlines()))
        if not rows:
            return ToolResult(False, 'PK-Smart CSV empty', {'csv_url': csv_url})
        row = rows[0]
        wanted = ['VDss_L_kg', 'CL_mL_min_kg', 'Fraction_unbound_in_plasma_(fup)', 'MRT_hr', 'thalf_hr']
        extracted = {k: row.get(k) for k in wanted if row.get(k) not in (None, '')}
        return ToolResult(True, 'PK-Smart actual CSV extracted', {'mode': 'actual', 'csv_url': csv_url, 'row': row, 'extracted': extracted})
    except Exception as e:
        return ToolResult(False, f'PK-Smart exception: {e}', {'exception': repr(e)})


def score_case(expectation: str, stp: ToolResult, admet: ToolResult, pk: ToolResult) -> float:
    if expectation == 'full':
        stp_score = 0.35 if stp.ok else 0.0
        admet_score = 0.35 if admet.ok else 0.0
        pk_score = 0.30 if pk.data.get('mode') == 'actual' else 0.10 if pk.ok else 0.0
        return stp_score + admet_score + pk_score
    if expectation == 'graceful_error':
        # Pass if we did not crash and at least one tool complained cleanly.
        return 1.0 if (not stp.ok or not admet.ok or not pk.ok) else 0.0
    return 0.0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--cases', required=True)
    ap.add_argument('--json', action='store_true')
    args = ap.parse_args()

    opener = make_opener()
    cases_path = Path(args.cases)
    rows = []
    with cases_path.open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            rows.append(row)

    total = 0.0
    out = []
    for row in rows:
        name = row['name']
        smiles = row['smiles']
        expectation = row['expectation']
        stp = run_stp(opener, smiles)
        admet = run_admet(opener, smiles)
        pk = run_pksmart(opener, smiles)
        score = score_case(expectation, stp, admet, pk)
        total += score
        record = {
            'name': name,
            'expectation': expectation,
            'score': score,
            'stp': stp.__dict__,
            'admet': admet.__dict__,
            'pk': pk.__dict__,
        }
        out.append(record)
        if args.json:
            print(json.dumps(record, ensure_ascii=False))
        else:
            print(f"CASE={name}\tscore={score:.1f}\tstp={'OK' if stp.ok else 'FAIL'}\tadmet={'OK' if admet.ok else 'FAIL'}\tpk={'OK' if pk.ok else 'FAIL'}")
            print(f"  stp: {stp.note}")
            print(f"  admet: {admet.note}")
            print(f"  pk: {pk.note}")
    avg = total / max(1, len(rows))
    print(f'PASS={sum(1 for r in out if r["score"] >= 1.0)}/{len(rows)}')
    print(f'SCORE={avg:.3f}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

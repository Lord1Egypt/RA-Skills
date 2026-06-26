#!/usr/bin/env python3
from __future__ import annotations

import argparse
import http.client
import html
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from run_smiles_smoke import (  # type: ignore
    ToolResult,
    fetch,
    make_opener,
    normalize_smiles,
    is_obviously_malformed,
    run_admet,
    run_pksmart,
)

STP_BASE = 'https://www.swisstargetprediction.ch'
PUBCHEM_BASE = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug'
CHEMBL_BASE = 'https://www.ebi.ac.uk/chembl/api/data'
CHEMBL_THRESHOLDS = (90, 80, 70)


def fetch_json(opener, url: str, headers: dict | None = None) -> tuple[int, dict]:
    req_headers = {'Accept': 'application/json'}
    if headers:
        req_headers.update(headers)
    req = urllib.request.Request(url, headers=req_headers)
    with opener.open(req, timeout=45) as resp:
        text = resp.read().decode('utf-8', errors='replace')
        return resp.status, json.loads(text)


def fetch_text(opener, url: str, data: dict | None = None, referer: str | None = None, retries: int = 2) -> tuple[int, str]:
    last_exc: Exception | None = None
    for _ in range(retries):
        try:
            return fetch(opener, url, data=data, referer=referer)
        except http.client.IncompleteRead as e:
            last_exc = e
    if last_exc:
        raise last_exc
    return fetch(opener, url, data=data, referer=referer)


def parse_stp_targets(result_html: str, limit: int = 5) -> list[dict]:
    cells = [
        html.unescape(re.sub(r'<[^>]+>', '', cell)).replace('&nbsp;', ' ').strip()
        for cell in re.findall(r'<td[^>]*>(.*?)</td>', result_html, re.S)
    ]
    targets: list[dict] = []
    seen_genes: set[str] = set()
    for i in range(0, max(0, len(cells) - 5), 7):
        target_name = cells[i]
        gene = cells[i + 1] if i + 1 < len(cells) else ''
        uniprot = cells[i + 2] if i + 2 < len(cells) else ''
        chembl = cells[i + 3] if i + 3 < len(cells) else ''
        target_class = cells[i + 4] if i + 4 < len(cells) else ''
        prob = cells[i + 5] if i + 5 < len(cells) else ''
        if not gene or not re.fullmatch(r'[A-Z0-9]+', gene):
            continue
        if not re.fullmatch(r'[0-9.]+', prob):
            continue
        if gene in seen_genes:
            continue
        targets.append(
            {
                'target': target_name,
                'gene': gene,
                'uniprot': uniprot,
                'chembl': chembl,
                'class': target_class,
                'probability': prob,
            }
        )
        seen_genes.add(gene)
        if len(targets) >= limit:
            break
    return targets


def run_stp_profile(opener, smiles: str, organism: str = 'Homo_sapiens') -> ToolResult:
    try:
        if is_obviously_malformed(smiles):
            return ToolResult(False, 'STP preflight rejected malformed SMILES', {'status': 'invalid'})
        smiles = normalize_smiles(smiles)
        fetch_text(opener, f'{STP_BASE}/index.php')
        status, submitted = fetch_text(
            opener,
            f'{STP_BASE}/predict.php',
            data={'organism': organism, 'smiles': smiles, 'ioi': '2'},
            referer=f'{STP_BASE}/index.php',
        )
        if status != 200:
            return ToolResult(False, f'STP submit HTTP {status}', {'status': status})
        lowered = submitted.lower()
        if 'not valid' in lowered or 'invalid' in lowered:
            return ToolResult(False, 'STP rejected SMILES', {'status': 'invalid'})
        m = re.search(rf'result\.php\?job=\d+&organism={re.escape(organism)}', submitted)
        if not m:
            return ToolResult(False, 'STP missing result redirect', {'preview': submitted[:500]})
        result_url = f'{STP_BASE}/{m.group(0)}'
        _, result_html = fetch_text(opener, result_url, referer=f'{STP_BASE}/predict.php')
        targets = parse_stp_targets(result_html)
        row_count = len(re.findall(r'carddisp\.pl\?gene=', result_html))
        return ToolResult(
            bool(targets),
            'STP ok' if targets else 'STP no targets',
            {
                'rows': row_count,
                'targets': targets,
                'top_target': targets[0]['target'] if targets else None,
                'top_gene': targets[0]['gene'] if targets else None,
                'top_prob': targets[0]['probability'] if targets else None,
                'url': result_url,
                'organism': organism,
            },
        )
    except Exception as e:
        return ToolResult(False, f'STP exception: {e}', {'exception': repr(e)})


def run_pubchem(opener, smiles: str) -> ToolResult:
    try:
        if is_obviously_malformed(smiles):
            return ToolResult(False, 'PubChem preflight rejected malformed SMILES', {'status': 'invalid'})
        smiles = normalize_smiles(smiles)
        encoded = urllib.parse.quote(smiles, safe='')
        cid_url = f'{PUBCHEM_BASE}/compound/smiles/{encoded}/cids/JSON'
        status, cid_data = fetch_json(opener, cid_url)
        if status != 200:
            return ToolResult(False, f'PubChem CID lookup HTTP {status}', {'status': status, 'url': cid_url})
        cids = cid_data.get('IdentifierList', {}).get('CID', [])
        if not cids:
            return ToolResult(False, 'PubChem exact CID not found', {'url': cid_url, 'mode': 'missing'})
        cid = cids[0]
        props_url = (
            f'{PUBCHEM_BASE}/compound/cid/{cid}/property/'
            'MolecularWeight,XLogP,TPSA,HBondDonorCount,HBondAcceptorCount,'
            'RotatableBondCount,Complexity,IUPACName,CanonicalSMILES,IsomericSMILES/JSON'
        )
        _, props_data = fetch_json(opener, props_url)
        props = props_data.get('PropertyTable', {}).get('Properties', [])
        prop_row = props[0] if props else {}
        syn_url = f'{PUBCHEM_BASE}/compound/cid/{cid}/synonyms/JSON'
        _, syn_data = fetch_json(opener, syn_url)
        info = syn_data.get('InformationList', {}).get('Information', [])
        synonyms = info[0].get('Synonym', []) if info else []
        return ToolResult(
            True,
            'PubChem ok',
            {
                'cid': cid,
                'cid_count': len(cids),
                'name': prop_row.get('IUPACName'),
                'properties': prop_row,
                'synonyms': synonyms[:10],
                'url': cid_url,
                'properties_url': props_url,
                'synonyms_url': syn_url,
            },
        )
    except Exception as e:
        return ToolResult(False, f'PubChem exception: {e}', {'exception': repr(e)})


def run_chembl(opener, smiles: str) -> ToolResult:
    try:
        if is_obviously_malformed(smiles):
            return ToolResult(False, 'ChEMBL preflight rejected malformed SMILES', {'status': 'invalid'})
        smiles = normalize_smiles(smiles)
        encoded = urllib.parse.quote(smiles, safe='')
        chosen_threshold = None
        raw_hits: list[dict] = []
        search_url = None
        for threshold in CHEMBL_THRESHOLDS:
            search_url = f'{CHEMBL_BASE}/similarity/{encoded}/{threshold}.json?limit=5'
            status, data = fetch_json(opener, search_url)
            if status != 200:
                continue
            raw_hits = data.get('molecules', []) or []
            if raw_hits:
                chosen_threshold = threshold
                break
        if not raw_hits or chosen_threshold is None:
            return ToolResult(False, 'ChEMBL similarity search returned no hits', {'thresholds': CHEMBL_THRESHOLDS, 'url': search_url})

        hits: list[dict] = []
        for hit in raw_hits[:5]:
            chembl_id = hit.get('molecule_chembl_id')
            if not chembl_id:
                continue
            hit_name = hit.get('pref_name') or chembl_id
            hit_similarity = hit.get('similarity')
            max_phase = hit.get('max_phase')
            hit_details: dict = {
                'chembl_id': chembl_id,
                'name': hit_name,
                'similarity': hit_similarity,
                'max_phase': max_phase,
            }

            try:
                _, mol_data = fetch_json(opener, f'{CHEMBL_BASE}/molecule/{chembl_id}.json')
                molecule = mol_data if isinstance(mol_data, dict) else {}
                if molecule:
                    hit_details['name'] = molecule.get('pref_name') or hit_name
                    hit_details['max_phase'] = molecule.get('max_phase', max_phase)
                    props = molecule.get('molecule_properties', {}) or {}
                    hit_details['properties'] = {
                        'full_mwt': props.get('full_mwt'),
                        'alogp': props.get('alogp'),
                        'psa': props.get('psa'),
                        'hba': props.get('hba'),
                        'hbd': props.get('hbd'),
                        'ro5_violations': props.get('ro5_violations'),
                    }
            except Exception:
                pass

            mechanisms: list[dict] = []
            try:
                _, mech_data = fetch_json(opener, f'{CHEMBL_BASE}/mechanism.json?molecule_chembl_id={chembl_id}&limit=3')
                for mech in (mech_data.get('mechanisms', []) or [])[:2]:
                    target_id = mech.get('target_chembl_id')
                    target_name = None
                    if target_id:
                        try:
                            _, target_data = fetch_json(opener, f'{CHEMBL_BASE}/target/{target_id}.json')
                            target_name = target_data.get('pref_name')
                        except Exception:
                            target_name = None
                    mechanisms.append(
                        {
                            'action_type': mech.get('action_type'),
                            'mechanism_of_action': mech.get('mechanism_of_action'),
                            'target_chembl_id': target_id,
                            'target_name': target_name,
                        }
                    )
            except Exception:
                pass
            if mechanisms:
                hit_details['mechanisms'] = mechanisms
            hits.append(hit_details)

        return ToolResult(
            True,
            'ChEMBL similarity ok',
            {
                'threshold': chosen_threshold,
                'hit_count': len(raw_hits),
                'hits': hits,
                'url': search_url,
            },
        )
    except Exception as e:
        return ToolResult(False, f'ChEMBL exception: {e}', {'exception': repr(e)})


def serialize_tool(result: ToolResult) -> dict:
    return {'ok': result.ok, 'note': result.note, 'data': result.data}


def format_value(value):
    if value in (None, ''):
        return 'N/A'
    if isinstance(value, float):
        return f'{value:g}'
    return str(value)


def print_report(smiles: str, stp: ToolResult, pubchem: ToolResult, admet: ToolResult, chembl: ToolResult, pk: ToolResult) -> None:
    print(f'SMILES: {smiles}\n')

    print('## SwissTargetPrediction')
    if stp.ok and stp.data.get('targets'):
        for target in stp.data['targets']:
            print(
                f"- {target['target']} ({target['gene']}, {target['uniprot']}) "
                f"prob {target['probability']}"
            )
        print(f"- URL: {stp.data.get('url')}")
    else:
        print(f"- Error: {stp.note}")

    print('\n## PubChem')
    if pubchem.ok:
        props = pubchem.data.get('properties', {})
        syns = pubchem.data.get('synonyms', [])
        print(f"- CID: {pubchem.data.get('cid')} ({pubchem.data.get('cid_count')} hit(s))")
        print(f"- Name: {format_value(pubchem.data.get('name'))}")
        print(
            f"- MW: {format_value(props.get('MolecularWeight'))} Da | "
            f"XLogP: {format_value(props.get('XLogP'))} | TPSA: {format_value(props.get('TPSA'))} Å²"
        )
        print(
            f"- HBD/HBA: {format_value(props.get('HBondDonorCount'))}/"
            f"{format_value(props.get('HBondAcceptorCount'))} | RotB: {format_value(props.get('RotatableBondCount'))} | "
            f"Complexity: {format_value(props.get('Complexity'))}"
        )
        if syns:
            print(f"- Synonyms: {', '.join(str(s) for s in syns[:5])}")
        print(f"- URL: {pubchem.data.get('url')}")
    else:
        print(f"- Error: {pubchem.note}")

    print('\n## ADMETlab 3.0')
    if admet.ok:
        print(f"- MW: {format_value(admet.data.get('MW'))} Da | QED: {format_value(admet.data.get('QED'))}")
        sections = admet.data.get('sections', [])
        if sections:
            print(f"- Sections: {', '.join(sections)}")
    else:
        print(f"- Error: {admet.note}")

    print('\n## ChEMBL')
    if chembl.ok and chembl.data.get('hits'):
        print(f"- Similarity threshold: {chembl.data.get('threshold')}%")
        for hit in chembl.data['hits'][:3]:
            chembl_id = hit.get('chembl_id')
            name = hit.get('name')
            label = chembl_id if name in (None, chembl_id) else f'{chembl_id} {name}'
            print(
                f"- {label} | sim {format_value(hit.get('similarity'))} | "
                f"phase {format_value(hit.get('max_phase'))}"
            )
            for mech in hit.get('mechanisms', [])[:1]:
                target = mech.get('target_name') or mech.get('target_chembl_id') or 'N/A'
                print(
                    f"  - Mechanism: {format_value(mech.get('mechanism_of_action'))} "
                    f"({format_value(mech.get('action_type'))}) -> {target}"
                )
        print(f"- URL: {chembl.data.get('url')}")
    else:
        print(f"- Error: {chembl.note}")

    print('\n## PK-Smart')
    if pk.ok:
        row = pk.data.get('row', {})
        print(f"- VDss: {format_value(row.get('VDss_L_kg'))} L/kg")
        print(f"- CL: {format_value(row.get('CL_mL_min_kg'))} mL/min/kg")
        print(f"- t½: {format_value(row.get('thalf_hr'))} hr")
        print(f"- fu: {format_value(row.get('Fraction_unbound_in_plasma_(fup)'))}")
        print(f"- MRT: {format_value(row.get('MRT_hr'))} hr")
    else:
        print(f"- Error: {pk.note}")

    print('\n## Summary')
    summary_bits: list[str] = []
    if stp.ok and stp.data.get('targets'):
        top = stp.data['targets'][0]
        summary_bits.append(f"STP points to {top['target']} / {top['gene']} ({top['probability']})")
    if pubchem.ok:
        summary_bits.append(f"PubChem anchors the identity as CID {pubchem.data.get('cid')} with MW {format_value(pubchem.data.get('properties', {}).get('MolecularWeight'))} Da")
    if chembl.ok and chembl.data.get('hits'):
        top_hit = chembl.data['hits'][0]
        chembl_id = top_hit.get('chembl_id')
        name = top_hit.get('name')
        label = chembl_id if name in (None, chembl_id) else f'{chembl_id} {name}'
        summary_bits.append(f"ChEMBL similarity top hit is {label} at {chembl.data.get('threshold')}%")
    if admet.ok:
        summary_bits.append(f"ADMETlab returned {len(admet.data.get('sections', []))} sections")
    if pk.ok:
        row = pk.data.get('row', {})
        summary_bits.append(f"PK-Smart suggests VDss {format_value(row.get('VDss_L_kg'))} L/kg and t½ {format_value(row.get('thalf_hr'))} hr")
    if summary_bits:
        for bit in summary_bits:
            print(f'- {bit}')
    else:
        print('- No results')


def main() -> int:
    ap = argparse.ArgumentParser(description='Full SMILES profiling report')
    ap.add_argument('smiles', help='Input SMILES')
    ap.add_argument('--organism', default='Homo_sapiens', help='SwissTargetPrediction organism (default: Homo_sapiens)')
    ap.add_argument('--json', action='store_true', help='Emit JSON instead of text')
    args = ap.parse_args()

    opener = make_opener()
    smiles = normalize_smiles(args.smiles)

    stp = run_stp_profile(opener, smiles, args.organism)
    pubchem = run_pubchem(opener, smiles)
    admet = run_admet(opener, smiles)
    chembl = run_chembl(opener, smiles)
    pk = run_pksmart(opener, smiles)

    report = {
        'smiles': smiles,
        'organism': args.organism,
        'stp': serialize_tool(stp),
        'pubchem': serialize_tool(pubchem),
        'admet': serialize_tool(admet),
        'chembl': serialize_tool(chembl),
        'pk': serialize_tool(pk),
    }

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_report(smiles, stp, pubchem, admet, chembl, pk)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

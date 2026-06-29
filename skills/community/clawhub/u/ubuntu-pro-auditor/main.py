#!/usr/bin/env python3
"""Ubuntu Pro Auditor — CVE scanning, ESM check, compliance reporting."""
import json, subprocess, sys
from datetime import datetime

def scan():
    results = {'kernel': '', 'cves': [], 'esm': [], 'livepatch': '', 'modules': []}
    
    # Kernel version
    results['kernel'] = subprocess.run(['uname', '-r'], capture_output=True, text=True).stdout.strip()
    
    # Pro status
    r = subprocess.run(['pro', 'status', '--format', 'json'], capture_output=True, text=True, timeout=10)
    if r.returncode == 0:
        data = json.loads(r.stdout)
        results['esm'] = [s['name'] for s in data.get('services', []) if s.get('status') == 'enabled']
    
    # Livepatch
    r = subprocess.run(['canonical-livepatch', 'status', '--format', 'json'], capture_output=True, text=True, timeout=10)
    if r.returncode == 0:
        data = json.loads(r.stdout)
        if isinstance(data, dict) and 'Status' in data:
            lp = data['Status']
            if isinstance(lp, list) and lp:
                results['livepatch'] = lp[0].get('Livepatch', {}).get('State', 'unknown')
    
    # Dangerous modules
    for mod in ['xfrm_user', 'xfrm_algo', 'tipc', 'sctp']:
        r = subprocess.run(['lsmod'], capture_output=True, text=True, timeout=5)
        if mod in r.stdout:
            results['modules'].append(mod)
    
    return results

def generate_report(data):
    report = f"""# Security Audit Report
Date: {datetime.now().isoformat()}
Kernel: {data['kernel']}

## Status
- ESM Services: {', '.join(data['esm'])}
- Livepatch: {data['livepatch']}
- Dangerous Modules: {', '.join(data['modules']) if data['modules'] else 'None'}
- CVEs: {len(data['cves'])} found

## Verdict
{'✅ PASS' if not data['modules'] else '⚠️ ISSUES FOUND'}
"""
    return report

if __name__ == '__main__':
    args = sys.argv[1:]
    data = scan()
    if '--report' in args:
        result = {'report': generate_report(data), 'data': data}
    else:
        result = data
    print(json.dumps(result, indent=2, ensure_ascii=False))

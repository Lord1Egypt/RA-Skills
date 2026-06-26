#!/usr/bin/env python3
"""
04_whois.py - whois 查询 + 结构化提取
用法: python3 04_whois.py <domain_or_ip> [--json]
"""
import subprocess, sys, json, re

def run_whois(target):
    try:
        result = subprocess.run(
            ["whois", target],
            capture_output=True, text=True, timeout=15
        )
        return result.stdout
    except Exception as e:
        return f"ERROR: {e}"

def parse_whois(raw, target):
    """从 whois 原始输出提取关键字段"""
    info = {"target": target, "raw_length": len(raw)}

    patterns = {
        "registrar":       r'(?i)Registrar:\s*(.+)',
        "registrar_url":   r'(?i)Registrar URL:\s*(.+)',
        "creation_date":   r'(?i)Creation Date:\s*(.+)',
        "expiry_date":     r'(?i)(?:Registry Expiry Date|Expiration Date):\s*(.+)',
        "updated_date":    r'(?i)Updated Date:\s*(.+)',
        "status":          r'(?i)Domain Status:\s*(.+)',
        "name_servers":    r'(?i)Name Server:\s*(.+)',
        "registrant_org":  r'(?i)Registrant Organization:\s*(.+)',
        "registrant_country": r'(?i)Registrant Country:\s*(.+)',
        "admin_email":     r'(?i)(?:Admin Email|Registrant Email):\s*(.+)',
        # IP whois
        "netname":         r'(?i)NetName:\s*(.+)',
        "orgname":         r'(?i)OrgName:\s*(.+)',
        "org":             r'(?i)^org:\s*(.+)',
        "descr":           r'(?i)^descr:\s*(.+)',
        "country":         r'(?i)^country:\s*(.+)',
        "inetnum":         r'(?i)inetnum:\s*(.+)',
        "cidr":            r'(?i)CIDR:\s*(.+)',
        "abuse_email":     r'(?i)(?:OrgAbuseEmail|abuse-mailbox):\s*(.+)',
    }

    multi_fields = {"status", "name_servers"}

    for key, pattern in patterns.items():
        matches = re.findall(pattern, raw)
        if matches:
            cleaned = [m.strip() for m in matches]
            if key in multi_fields:
                info[key] = list(dict.fromkeys(cleaned))[:5]
            else:
                info[key] = cleaned[0]

    return info

def run(target, as_json=False):
    raw = run_whois(target)

    if raw.startswith("ERROR"):
        result = {"target": target, "error": raw}
    else:
        result = parse_whois(raw, target)
        result["raw"] = raw

    if as_json:
        out = {k: v for k, v in result.items() if k != "raw"}
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(f"\n=== WHOIS: {target} ===\n")
        skip = {"target", "raw", "raw_length"}
        for key, val in result.items():
            if key in skip:
                continue
            if isinstance(val, list):
                print(f"  {key}: {', '.join(val)}")
            else:
                print(f"  {key}: {val}")
        print()

    return result

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("target")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    run(args.target, as_json=args.json)

#!/usr/bin/env python3
import argparse, json

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="sop_outline.json")
    args = ap.parse_args()
    payload = {
        "purpose": "",
        "scope": "",
        "roles": [],
        "inputs": [],
        "procedure_steps": [],
        "quality_checkpoints": [],
        "exceptions": [],
        "handoff": []
    }
    json.dump(payload, open(args.out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"Wrote {args.out}")

if __name__ == "__main__":
    main()

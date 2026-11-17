"""Account snapshot: profile, Sorsa Score, and top crypto followers.

    export SORSA_API_KEY=your_key
    python analyze_account.py vitalikbuterin

Note: Sorsa Score and top-followers come from Sorsa's crypto-focused database,
so they are most meaningful for crypto accounts and may be empty otherwise.

This example imports the bundled client. It resolves the path relative to this
file, so it runs from anywhere (repo root or the examples folder).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from sorsa_client import SorsaClient  # noqa: E402

handle = sys.argv[1] if len(sys.argv) > 1 else "vitalikbuterin"
client = SorsaClient()

profile = client.get_profile(handle)
print(f"@{profile['username']} ({profile['display_name']})")
print(f"  followers: {profile['followers_count']:,}")

try:
    print(f"  Sorsa Score: {client.score(handle)}")
except Exception as e:  # crypto DB miss or transient error
    print(f"  Sorsa Score: unavailable ({e})")

top = client.get("top-followers", **{"username": handle}).get("users", [])
if top:
    print("  Top crypto followers by Sorsa Score:")
    for f in top[:5]:
        print(f"    - @{f['username']} ({f['followers_count']:,} followers)")
else:
    print("  No crypto-indexed followers found for this account.")

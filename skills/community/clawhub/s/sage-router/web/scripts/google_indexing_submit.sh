#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ ! -f public/sitemap.xml ]]; then
  echo "Missing public/sitemap.xml. Add/update the sitemap before submitting." >&2
  exit 1
fi

cat >&2 <<'EOF'
Google active indexing submission is disabled.

The previous helper depended on google-indexing-script@0.4.0, which currently
has unpatched transitive audit findings. Use Google Search Console to submit
https://sagerouter.dev/sitemap.xml manually until a maintained audited client is
added.
EOF
exit 2

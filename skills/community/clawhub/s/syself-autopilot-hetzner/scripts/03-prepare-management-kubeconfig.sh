#!/usr/bin/env bash
# Prepare the SySelf management kubeconfig and set the organization namespace.
set -euo pipefail

usage() {
  echo "Usage: $0 <source-kubeconfig> <org-namespace> [target-kubeconfig]" >&2
  echo "Example: $0 ./downloaded-kubeconfig.yaml org-my-company ./management-kubeconfig.yaml" >&2
}

SOURCE_KUBECONFIG="${1:-}"
ORG_NAMESPACE="${2:-}"
TARGET_KUBECONFIG="${3:-management-kubeconfig.yaml}"

if [[ -z "$SOURCE_KUBECONFIG" || -z "$ORG_NAMESPACE" ]]; then
  usage
  exit 1
fi

if [[ ! -f "$SOURCE_KUBECONFIG" ]]; then
  echo "Source kubeconfig not found: $SOURCE_KUBECONFIG" >&2
  exit 1
fi

if [[ "$ORG_NAMESPACE" != org-* ]]; then
  echo "WARN: organization namespace usually starts with org-. Received: $ORG_NAMESPACE" >&2
fi

cp "$SOURCE_KUBECONFIG" "$TARGET_KUBECONFIG"
chmod 600 "$TARGET_KUBECONFIG"

python3 - <<'PY' "$TARGET_KUBECONFIG" "$ORG_NAMESPACE"
import sys
from pathlib import Path

path = Path(sys.argv[1])
namespace = sys.argv[2]
text = path.read_text()

if "namespace:" not in text:
    print("No namespace field found in kubeconfig; update it manually.", file=sys.stderr)
    sys.exit(1)

updated = []
replaced = False
for line in text.splitlines():
    stripped = line.lstrip()
    if stripped.startswith("namespace:") and not replaced:
        indent = line[: len(line) - len(stripped)]
        updated.append(f"{indent}namespace: {namespace}")
        replaced = True
    else:
        updated.append(line)

if not replaced:
    print("Failed to update namespace field in kubeconfig.", file=sys.stderr)
    sys.exit(1)

path.write_text("\n".join(updated) + "\n")
PY

echo "==> Prepared management kubeconfig: $TARGET_KUBECONFIG"
echo "==> Export it with: export KUBECONFIG=$TARGET_KUBECONFIG"
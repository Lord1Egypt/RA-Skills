#!/usr/bin/env bash
# Apply HetznerBareMetalHost resources and show validation follow-ups.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEFAULT_MANIFEST="$SCRIPT_DIR/../templates/hetznerbaremetalhost.yaml"
MANIFEST_PATH="${1:-$DEFAULT_MANIFEST}"

if [[ ! -f "$MANIFEST_PATH" ]]; then
	echo "Manifest not found: $MANIFEST_PATH" >&2
	exit 1
fi

echo "==> Using context: $(kubectl config current-context 2>/dev/null || echo unknown)"
echo "==> Applying bare metal host manifests..."
kubectl apply -f "$MANIFEST_PATH"

echo "==> Current HetznerBareMetalHost objects:"
kubectl get hetznerbaremetalhost

cat <<'EOF'

Next checks:
	kubectl describe hetznerbaremetalhost <name>
	kubectl get hbmh <name> -o yaml | yq .status.hardwareDetails.storage

If WWN is missing, update rootDeviceHints.wwn and re-apply the manifest.
If the machine was previously configured with RAID, follow the official disk
wipe guide before retrying.
EOF

echo "==> Bare metal host registration request submitted."

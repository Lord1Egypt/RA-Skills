#!/usr/bin/env bash
# Validate local tooling and access to the SySelf Autopilot management cluster.
set -euo pipefail

usage() {
	echo "Usage: $0 <management-kubeconfig-path>" >&2
}

KUBECONFIG_PATH="${1:-${KUBECONFIG:-}}"

if [[ -z "$KUBECONFIG_PATH" ]]; then
	usage
	exit 1
fi

if [[ ! -f "$KUBECONFIG_PATH" ]]; then
	echo "Kubeconfig file not found: $KUBECONFIG_PATH" >&2
	exit 1
fi

echo "==> Verifying required CLIs..."
kubectl version --client
kubectl oidc-login --help >/dev/null
helm version

if command -v hcloud >/dev/null 2>&1; then
	hcloud version
else
	echo "WARN: hcloud CLI not found. Hetzner automation steps will be manual." >&2
fi

echo "==> Validating management kubeconfig permissions and access..."
chmod 600 "$KUBECONFIG_PATH"
export KUBECONFIG="$KUBECONFIG_PATH"

kubectl config current-context || true
kubectl get ns
kubectl get clusters

echo "==> Management-cluster access looks usable."
echo "If OIDC login is required, kubectl should open the browser automatically."

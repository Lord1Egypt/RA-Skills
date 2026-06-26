#!/usr/bin/env bash
# Apply ClusterStack and Cluster manifests in the SySelf management cluster.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEFAULT_STACK_MANIFEST="$SCRIPT_DIR/../templates/clusterstack.yaml"
DEFAULT_CLUSTER_MANIFEST="$SCRIPT_DIR/../templates/cluster.yaml"
STACK_MANIFEST="${1:-$DEFAULT_STACK_MANIFEST}"
CLUSTER_MANIFEST="${2:-$DEFAULT_CLUSTER_MANIFEST}"

[[ -f "$STACK_MANIFEST" ]] || { echo "Missing stack manifest: $STACK_MANIFEST" >&2; exit 1; }
[[ -f "$CLUSTER_MANIFEST" ]] || { echo "Missing cluster manifest: $CLUSTER_MANIFEST" >&2; exit 1; }

echo "==> Using context: $(kubectl config current-context 2>/dev/null || echo unknown)"
echo "==> Applying ClusterStack objects..."
kubectl apply -f "$STACK_MANIFEST"

echo "==> Current ClusterStack resources:"
kubectl get clusterstack || true
kubectl get clusterstackreleases || true
kubectl get HetznerNodeImageReleases || true

echo "==> Applying workload cluster manifest..."
kubectl apply -f "$CLUSTER_MANIFEST"

echo "==> Current cluster state:"
kubectl get cluster
kubectl get machines

cat <<'EOF'

Recommended follow-up watches:
	kubectl get clusterstackreleases
	kubectl get HetznerNodeImageReleases
	kubectl get machines -w
	kubectl get cluster
EOF

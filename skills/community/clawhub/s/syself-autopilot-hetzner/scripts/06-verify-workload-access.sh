#!/usr/bin/env bash
# Verify access to the workload cluster after kubeconfig retrieval.
set -euo pipefail

usage() {
	echo "Usage: $0 <workload-kubeconfig-path>" >&2
}

WORKLOAD_KUBECONFIG="${1:-${KUBECONFIG:-}}"

if [[ -z "$WORKLOAD_KUBECONFIG" ]]; then
	usage
	exit 1
fi

if [[ ! -f "$WORKLOAD_KUBECONFIG" ]]; then
	echo "Workload kubeconfig not found: $WORKLOAD_KUBECONFIG" >&2
	exit 1
fi

export KUBECONFIG="$WORKLOAD_KUBECONFIG"

echo "==> Verifying workload-cluster access..."
kubectl cluster-info
kubectl get nodes -o wide
kubectl get pods -A

echo "==> Workload cluster is reachable."

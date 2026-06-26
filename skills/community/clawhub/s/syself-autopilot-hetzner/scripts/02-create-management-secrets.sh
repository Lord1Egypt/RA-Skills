#!/usr/bin/env bash
# Create Hetzner credentials in the SySelf management cluster.
set -euo pipefail

echo "==> Using context: $(kubectl config current-context 2>/dev/null || echo unknown)"

: "${HCLOUD_TOKEN:?Must be set}"
: "${HETZNER_ROBOT_USER:?Must be set}"
: "${HETZNER_ROBOT_PASSWORD:?Must be set}"
: "${SSH_KEY_NAME:?Must be set}"
: "${HETZNER_SSH_PUB_PATH:?Must be set}"
: "${HETZNER_SSH_PRIV_PATH:?Must be set}"

[[ -f "$HETZNER_SSH_PUB_PATH" ]] || { echo "Missing public key: $HETZNER_SSH_PUB_PATH" >&2; exit 1; }
[[ -f "$HETZNER_SSH_PRIV_PATH" ]] || { echo "Missing private key: $HETZNER_SSH_PRIV_PATH" >&2; exit 1; }

echo "==> Creating or updating 'hetzner' secret..."
kubectl create secret generic hetzner \
	--from-literal=hcloud="$HCLOUD_TOKEN" \
	--from-literal=robot-user="$HETZNER_ROBOT_USER" \
	--from-literal=robot-password="$HETZNER_ROBOT_PASSWORD" \
	--dry-run=client -o yaml | kubectl apply -f -

echo "==> Creating or updating 'robot-ssh' secret..."
kubectl create secret generic robot-ssh \
	--from-literal=sshkey-name="$SSH_KEY_NAME" \
	--from-file=ssh-privatekey="$HETZNER_SSH_PRIV_PATH" \
	--from-file=ssh-publickey="$HETZNER_SSH_PUB_PATH" \
	--dry-run=client -o yaml | kubectl apply -f -

echo "==> Secrets ready:"
kubectl get secrets hetzner robot-ssh

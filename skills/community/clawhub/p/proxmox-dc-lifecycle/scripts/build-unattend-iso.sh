#!/usr/bin/env bash
# build-unattend-iso.sh — package an autounattend.xml into a small ISO that
# Windows Setup auto-detects (autounattend.xml must be at the volume root).
#
# Usage: build-unattend-iso.sh /path/to/autounattend.xml /path/to/output.iso
#
# Requires genisoimage or mkisofs or xorriso (any one). Copy the result to a
# Proxmox ISO storage (e.g. /mnt/pve/<storage>/template/iso/) to attach with qm.
set -euo pipefail

src="${1:?path to autounattend.xml required}"
out="${2:?output iso path required}"
[[ -f "$src" ]] || { echo "no such file: $src" >&2; exit 1; }

staging="$(mktemp -d)"
trap 'rm -rf "$staging"' EXIT
cp "$src" "$staging/autounattend.xml"

# A clean ISO9660+Joliet with autounattend.xml at the root is what Windows Setup needs.
if command -v genisoimage >/dev/null 2>&1; then
  genisoimage -quiet -J -r -V UNATTEND -o "$out" "$staging"
elif command -v mkisofs >/dev/null 2>&1; then
  mkisofs -quiet -J -r -V UNATTEND -o "$out" "$staging"
elif command -v xorriso >/dev/null 2>&1; then
  xorriso -as mkisofs -J -r -V UNATTEND -o "$out" "$staging"
else
  echo "need genisoimage, mkisofs, or xorriso" >&2; exit 1
fi
echo "built $out"

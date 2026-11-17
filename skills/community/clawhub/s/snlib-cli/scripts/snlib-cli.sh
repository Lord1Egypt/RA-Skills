#!/usr/bin/env bash
set -euo pipefail
umask 077

fail() { printf '%s\n' "$*" >&2; exit 1; }

if (( $# > 1 )); then
  printf '%s\n' 'Usage: snlib-cli.sh <command>; supply one JSON object on stdin, not CLI flags.' >&2
  exit 2
fi
command="${1:---help}"
if [[ "$command" != "help" && "$command" != "--help" && -t 0 ]]; then
  printf '%s\n' 'Supply one JSON object on stdin (use {} for commands without fields).' >&2
  exit 2
fi

# Explicit local development override; never downloads or builds in this mode.
if [[ -n "${SNLIB_CLI_BINARY:-}" ]]; then
  [[ "$SNLIB_CLI_BINARY" = /* && -x "$SNLIB_CLI_BINARY" ]] ||
    fail 'SNLIB_CLI_BINARY must be an absolute path to a trusted executable.'
  exec "$SNLIB_CLI_BINARY" "$command"
fi

case "$(uname -s)" in
  Darwin) os=darwin ;;
  Linux) os=linux ;;
  *) fail 'Supported platforms: macOS and Linux.' ;;
esac
case "$(uname -m)" in
  arm64|aarch64) arch=arm64 ;;
  x86_64|amd64) arch=amd64 ;;
  *) fail 'Supported architectures: ARM64 and x86-64.' ;;
esac
[[ "$os-$arch" != "darwin-amd64" ]] || fail 'Intel macOS is not supported by the current MoonBit toolchain.'
asset="snlib-cli-$os-$arch"
script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
manifest="$script_dir/../references/native-release.txt"
[[ -f "$manifest" ]] || fail 'Release manifest missing. Maintainer: run clawhub-release.bb prepare --version VERSION.'
IFS= read -r tag < "$manifest"
[[ "$tag" =~ ^v[0-9]+\.[0-9]+\.[0-9]+(-[0-9A-Za-z.-]+)?$ ]] || fail 'Invalid release version.'
expected="$(awk -v asset="$asset" '$2 == asset { print $1 }' "$manifest")"
[[ "$expected" =~ ^[0-9a-f]{64}$ ]] || fail "No valid pinned checksum for $asset."

hash_file() {
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum "$1" | awk '{print $1}'
  elif command -v shasum >/dev/null 2>&1; then
    shasum -a 256 "$1" | awk '{print $1}'
  else
    fail 'Install sha256sum or shasum to verify the native binary.'
  fi
}
cache_dir="${XDG_CACHE_HOME:-${HOME:?HOME must be set}/.cache}/snlib-cli/$tag/$expected"
binary="$cache_dir/$asset"
if [[ ! -f "$binary" ]]; then
  command -v curl >/dev/null 2>&1 || fail 'Install curl to download the native binary.'
  mkdir -p "$cache_dir"
  temporary="$(mktemp "$cache_dir/.download.XXXXXX")"
  trap 'rm -f "$temporary"' EXIT
  # curl must not consume the JSON/credentials piped to the launcher.
  curl --fail --silent --show-error --location --proto '=https' --proto-redir '=https' \
    --connect-timeout 10 --max-time 120 --retry 2 \
    "https://github.com/ruseel/snlib-cli/releases/download/$tag/$asset" \
    --output "$temporary" </dev/null
  [[ "$(hash_file "$temporary")" == "$expected" ]] || fail 'Downloaded binary checksum mismatch; refusing to execute.'
  chmod 700 "$temporary"
  mv -f "$temporary" "$binary"
  trap - EXIT
fi
[[ "$(hash_file "$binary")" == "$expected" ]] || fail 'Cached binary checksum mismatch; remove it and retry.'
# ClawHub file installation need not preserve executable permissions.
chmod 700 "$binary"
exec "$binary" "$command"

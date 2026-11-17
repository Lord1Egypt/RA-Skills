#!/bin/bash
# Runs one REA CLI command in the reverse-engineer-anything image, locked down:
# no network, read-only root, no capabilities, the target directory mounted
# read-only at /work. Files are addressed by their container path, e.g.
# /work/app.apk.
set -euo pipefail

readonly default_image='psyb0t/reverse-engineer-anything:latest'

log() {
	local level="$1"
	shift
	printf '{"time":"%s","level":"%s","msg":"%s"}\n' \
		"$(date -u '+%Y-%m-%dT%H:%M:%SZ')" "$level" "$*" >&2
}

usage() {
	cat <<'EOF'
Usage:
  rea.sh [--dir DIR] [--network] COMMAND [ARGS...]

  --dir DIR    Directory mounted read-only at /work (default: current directory)
  --network    Allow network access (adb over TCP, website analysis); off by default

Examples:
  rea.sh --dir ./apks inspect-android-package /work/app.apk
  rea.sh --dir ./apks search-android-classes /work/app.apk MainActivity
  rea.sh --dir ./apks inspect-android-method /work/app.apk com.example.MainActivity onCreate
  rea.sh --dir ./apks decode-android-resources /work/app.apk
  rea.sh --help

REA_IMAGE overrides psyb0t/reverse-engineer-anything:latest.
EOF
}

main() {
	local dir="$PWD"
	local network="none"

	while (($# > 0)); do
		case "$1" in
		--dir)
			[[ $# -ge 2 ]] || {
				log ERROR "--dir needs a directory"
				exit 2
			}
			dir="$2"
			shift 2
			;;
		--network)
			network="bridge"
			shift
			;;
		-h | --usage)
			usage
			exit 0
			;;
		*)
			break
			;;
		esac
	done

	if (($# == 0)); then
		usage
		exit 2
	fi
	[[ -d "$dir" ]] || {
		log ERROR "not a directory: $dir"
		exit 2
	}
	dir="$(cd "$dir" && pwd)"

	exec docker run --rm --init \
		--network="$network" \
		--read-only \
		--cap-drop=ALL \
		--security-opt=no-new-privileges:true \
		--pids-limit=512 \
		--memory=6g \
		--tmpfs "/tmp:rw,nosuid,size=4g" \
		--tmpfs "/home/rea:rw,nosuid,size=256m" \
		-v "$dir:/work:ro" \
		"${REA_IMAGE:-$default_image}" "$@"
}

main "$@"

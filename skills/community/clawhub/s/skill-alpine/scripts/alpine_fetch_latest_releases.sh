#!/bin/bash
#
# MIT No Attribution
#
# https://github.com/lentiancn/skills/blob/main/LICENSE
#
set -euo pipefail

ALPINE_RELEASE_BASE_URL="https://dl-cdn.alpinelinux.org/alpine/latest-stable/releases"

# Discover all available architectures by scraping the releases directory index.
# Each subdirectory under the base URL represents an architecture (e.g., x86_64, aarch64).
archs=$(
    curl -s "$ALPINE_RELEASE_BASE_URL/" \
    | grep -oE 'href="[^"]+/"' \
    | sed 's/href="\([^"]*\)\/"/\1/' \
    | grep -v '^\.\.$' \
    | sort
)

# Arguments
first_release_json=1
releases_json=""

for arch in $archs; do
    # Fetch the YAML file that lists all latest releases for this architecture.
    latest_releases_yaml_url="${ALPINE_RELEASE_BASE_URL}/${arch}/latest-releases.yaml"
    # Check if the latest-releases.yaml file is accessible (HTTP 200 OK)
    if ! curl -sI --connect-timeout 60 --max-time 120 "$latest_releases_yaml_url" | grep -q "HTTP/2 200"; then
        # If not accessible, skip this architecture
        continue
    fi
    latest_releases_yaml=$(curl -s --connect-timeout 60 --max-time 120 "$latest_releases_yaml_url")

    # Extract the file name and version for the 'alpine-minirootfs' flavor (the minimal rootfs tarball).
    release_file_name=$(echo "$latest_releases_yaml" | yq -r '.[] | select(.flavor == "alpine-minirootfs") | .file')
    release_version=$(echo "$latest_releases_yaml" | yq -r '.[] | select(.flavor == "alpine-minirootfs") | .version')

    # Skip this architecture if either field is missing (shouldn't happen, but be defensive).
    [ -z "$release_file_name" ] || [ -z "$release_version" ] && continue

    # Build the direct download URL for the tarball.
    release_file_url="${ALPINE_RELEASE_BASE_URL}/${arch}/${release_file_name}"

    # Construct a JSON object for this release.
    release_json="{\"version\":\"${release_version}\",\"arch\":\"${arch}\",\"file_url\":\"${release_file_url}\"}"

    # Append to the JSON array (commas between elements, none after the last).
    if [ $first_release_json -eq 1 ]; then
        releases_json="$release_json"
        first_release_json=0
    else
        releases_json="${releases_json},${release_json}"
    fi
done

# Output the final JSON array to stdout.
echo "[${releases_json}]"

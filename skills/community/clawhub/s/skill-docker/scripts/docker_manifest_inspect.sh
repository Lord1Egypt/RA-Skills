#!/bin/bash
#
# MIT No Attribution
#
# https://github.com/lentiancn/skills/blob/main/LICENSE
#
set -euo pipefail

# Arguments
DOCKER_IMAGE="${DOCKER_IMAGE:-}"
DOCKER_TAGS=("${DOCKER_TAGS[@]}")

# Validate required arguments
if [ -z "${DOCKER_IMAGE}" ] || [ ${#DOCKER_TAGS[@]} -eq 0 ]; then
    echo "ERROR: Usage: DOCKER_IMAGE=<DOCKER_IMAGE> DOCKER_TAGS=(<TAG1> [<TAG2> ...]) $0"
    exit 1
fi

FINAL_JSON=$(jq -n --arg image "${DOCKER_IMAGE}" '{image: $image, tags: []}')

for DOCKER_TAG in "${DOCKER_TAGS[@]}"; do
    IMAGE_TAG="${DOCKER_IMAGE}:${DOCKER_TAG}"

    # Inspect manifest (multi-arch metadata + layer digests/sizes); fails if image not found/auth error/network issue
    MANIFEST_JSON=$(docker manifest inspect "${IMAGE_TAG}" 2>&1) || true
    if echo "$MANIFEST_JSON" | grep -q "no such manifest"; then
        # Tag not found
        TAG_JSON=$(jq -n \
            --arg tag "$DOCKER_TAG" \
            '{tag: $tag, exists: false, archs: {}}'
        )
    elif echo "$MANIFEST_JSON" | grep -qi "unauthorized"; then
        # Authentication required
        echo "ERROR: authentication required or image('${DOCKER_IMAGE}') not found" >&2
        exit 1
    else
        IS_LIST=$(echo "$MANIFEST_JSON" | jq -r 'has("manifests")')

        if [ "$IS_LIST" = "true" ]; then
            # Multi-arch manifest: extract per-architecture digest and size
            ARCHS_JSON=$(echo "$MANIFEST_JSON" | jq '
                .manifests
                | map({
                    key: (.platform.os + "/" + .platform.architecture + ("/" + (.platform.variant // "")))
                         | rtrimstr("/"),
                    value: { size: .size, digest: .digest }
                  })
                | from_entries
            ')
        else
            # Single-arch manifest: extract digest and size directly
            ARCHS_JSON=$(echo "$MANIFEST_JSON" | jq '
                {
                  (.os + "/" + .architecture + ("/" + (.variant // "")))
                  | rtrimstr("/"): {
                    size: .size,
                    digest: .digest
                  }
                }
            ')
        fi

        # Build tag entry with arch metadata
        TAG_JSON=$(jq -n \
            --arg tag "$DOCKER_TAG" \
            --argjson archs "$ARCHS_JSON" \
            '{tag: $tag, exists: true, archs: $archs}'
        )
    fi

    # Append tag entry to final JSON
    FINAL_JSON=$(echo "$FINAL_JSON" | jq --argjson tag "$TAG_JSON" '.tags += [$tag]')
done

# Output final JSON
echo "$FINAL_JSON"

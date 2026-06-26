#!/bin/bash
#
# MIT No Attribution
#
# https://github.com/lentiancn/skills/blob/main/LICENSE
#
set -euo pipefail

# Arguments
DOCKER_BUILDER_NAME="${DOCKER_BUILDER_NAME:-}"
DOCKER_PRUNE_FIRST="${DOCKER_PRUNE_FIRST:-false}"

# Validate required arguments
if [ -z "${DOCKER_BUILDER_NAME}" ]; then
    echo "ERROR: DOCKER_BUILDER_NAME is required. Usage: DOCKER_BUILDER_NAME=<DOCKER_BUILDER_NAME> $0"
    exit 1
fi

# Remove the specified buildx builder instance if it exists
docker buildx rm "${DOCKER_BUILDER_NAME}" 2>/dev/null || true

# Clean up all cached buildx resources system-wide
if [ "${DOCKER_PRUNE_FIRST}" = "true" ]; then
    docker buildx prune -a -f 2>/dev/null || true
fi

echo "SUCCESS: destroyed"

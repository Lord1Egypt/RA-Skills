#!/bin/bash
#
# MIT No Attribution
#
# https://github.com/lentiancn/skills/blob/main/LICENSE
#
set -euo pipefail

# Arguments
DOCKER_BUILDER_NAME="${DOCKER_BUILDER_NAME:-}"
DOCKER_BUILD_CONCURRENCY="${DOCKER_BUILD_CONCURRENCY:-2}"
DOCKER_PRUNE_FIRST="${DOCKER_PRUNE_FIRST:-false}"

# Validate required arguments
if [ -z "${DOCKER_BUILDER_NAME}" ]; then
    echo "ERROR: DOCKER_BUILDER_NAME is required. Usage: DOCKER_BUILDER_NAME=<DOCKER_BUILDER_NAME> $0"
    exit 1
fi

# Register cross-platform emulators for multi-architecture builds
docker run --privileged --rm tonistiigi/binfmt:latest --install all

# Clean up any existing builder and build cache before initialization
bash ./docker_buildx_destroy.sh

# Create a new docker-container driver builder with concurrency settings
docker buildx create \
    --name "${DOCKER_BUILDER_NAME}" \
    --driver docker-container \
    --driver-opt env.BUILDKIT_MAX_PARALLELISM="${DOCKER_BUILD_CONCURRENCY}" \
    --driver-opt env.BUILDKIT_CONCURRENCY="${DOCKER_BUILD_CONCURRENCY}" \
    --use \
    --platform \
        linux/amd64,\
        linux/arm64,\
        linux/arm/v7,\
        linux/arm/v6,\
        linux/arm/v5,\
        linux/386,\
        linux/riscv64,\
        linux/ppc64le,\
        linux/s390x

# Bootstrap and verify the builder instance
docker buildx inspect "${DOCKER_BUILDER_NAME}" --bootstrap

echo "SUCCESS: initted"

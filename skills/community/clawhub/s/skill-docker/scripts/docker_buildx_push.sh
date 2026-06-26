#!/bin/bash
#
# MIT No Attribution
#
# https://github.com/lentiancn/skills/blob/main/LICENSE
#
set -euo pipefail

# Arguments
DOCKER_BUILDER_NAME="${DOCKER_BUILDER_NAME:-}"
DOCKER_PLATFORM="${DOCKER_PLATFORM:-}"
DOCKER_PROVENANCE="${DOCKER_PROVENANCE:-false}"
DOCKER_SBOM="${DOCKER_SBOM:-false}"
DOCKER_IMAGE_TAGS=("${DOCKER_IMAGE_TAGS[@]}")
DOCKER_BUILD_ARGS=("${DOCKER_BUILD_ARGS[@]}")

# Validate required arguments
if [ -z "${DOCKER_BUILDER_NAME}" ]; then
    echo "ERROR: DOCKER_BUILDER_NAME is required. Usage: DOCKER_BUILDER_NAME=<DOCKER_BUILDER_NAME> DOCKER_PLATFORM=<DOCKER_PLATFORM> DOCKER_IMAGE_TAGS=<DOCKER_IMAGE_TAGS> $0"
    exit 1
fi
if [ -z "${DOCKER_PLATFORM}" ]; then
    echo "ERROR: DOCKER_PLATFORM is required. Usage: DOCKER_BUILDER_NAME=<DOCKER_BUILDER_NAME> DOCKER_PLATFORM=<DOCKER_PLATFORM> DOCKER_IMAGE_TAGS=<DOCKER_IMAGE_TAGS> $0"
    exit 1
fi
if [ ${#DOCKER_IMAGE_TAGS[@]} -eq 0 ]; then
    echo "ERROR: At least one tag must be provided via DOCKER_IMAGE_TAGS environment variable. Usage: DOCKER_BUILDER_NAME=<DOCKER_BUILDER_NAME> DOCKER_PLATFORM=<DOCKER_PLATFORM> DOCKER_IMAGE_TAGS=<DOCKER_IMAGE_TAGS> $0"
    exit 1
fi

# Iterate over all provided tags and build args
TAG_ARGS=()
for tag in "${DOCKER_IMAGE_TAGS[@]}"; do
  if [ -n "${tag}" ]; then
    TAG_ARGS+=("--tag" "${tag}")
  fi
done
BUILD_ARG_ARGS=()
for buildArg in "${DOCKER_BUILD_ARGS[@]}"; do
  if [ -n "${buildArg}" ]; then
    BUILD_ARG_ARGS+=("--build-arg" "${buildArg}")
  fi
done

# Build and push Docker image using buildx with specified parameters
docker buildx build \
  --platform "${DOCKER_PLATFORM}" \
  "${TAG_ARGS[@]}" \
  "${BUILD_ARG_ARGS[@]}" \
  --provenance="${DOCKER_PROVENANCE}" --sbom="${DOCKER_SBOM}" \
  --builder "${DOCKER_BUILDER_NAME}" \
  --push .

echo "SUCCESS: Build and push completed successfully"

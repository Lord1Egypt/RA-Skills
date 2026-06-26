#!/bin/bash
#
# MIT No Attribution
#
# https://github.com/lentiancn/skills/blob/main/LICENSE
#
set -euo pipefail

# Arguments
GIT_REMOTE_URL="${GIT_REMOTE_URL:-}"
GIT_LOCAL_PATH="${GIT_LOCAL_PATH:-}"
GIT_BRANCH="${GIT_BRANCH:-main}"

# Validate required arguments
if [ -z "$GIT_REMOTE_URL" ]; then
    echo "ERROR: GIT_REMOTE_URL is required. Usage: GIT_REMOTE_URL=<GIT_REMOTE_URL> GIT_LOCAL_PATH=<GIT_LOCAL_PATH> [GIT_BRANCH=<GIT_BRANCH>] $0"
    exit 1
fi
if [ -z "$GIT_LOCAL_PATH" ]; then
    echo "ERROR: GIT_LOCAL_PATH is required. Usage: GIT_REMOTE_URL=<GIT_REMOTE_URL> GIT_LOCAL_PATH=<GIT_LOCAL_PATH> [GIT_BRANCH=<GIT_BRANCH>] $0"
    exit 1
fi

if [ -d "${GIT_LOCAL_PATH}" ]; then
    # Directory exists — fetch and pull latest changes
    cd "${GIT_LOCAL_PATH}" || {
        echo "ERROR: Failed to enter directory ${GIT_LOCAL_PATH}. Check: $0"
        exit 1
    }
    git fetch origin "${GIT_BRANCH}"
    git pull origin "${GIT_BRANCH}"
    echo "SUCCESS: Git update"
else
    # Directory doesn't exist — clone the repository
    PARENT_DIR=$(dirname "${GIT_LOCAL_PATH}")
    mkdir -p "${PARENT_DIR}"
    cd "${PARENT_DIR}" || exit
    git clone -b "${GIT_BRANCH}" "${GIT_REMOTE_URL}" "${GIT_LOCAL_PATH}"
    echo "SUCCESS: Git clone"
fi

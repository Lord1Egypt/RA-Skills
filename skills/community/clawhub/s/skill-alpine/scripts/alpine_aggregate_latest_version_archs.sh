#!/bin/bash
#
# MIT No Attribution
#
# https://github.com/lentiancn/skills/blob/main/LICENSE
#
set -euo pipefail

latest_releases_json=$(bash ./alpine_fetch_latest_releases.sh)

echo "$latest_releases_json" | jq -c '
    reduce .[] as $item ({};
      .[$item.version] += [$item.arch]
    )
    | to_entries | sort_by(.key) | map({
      version: .key,
      archs: (.value | sort)
    })
  '

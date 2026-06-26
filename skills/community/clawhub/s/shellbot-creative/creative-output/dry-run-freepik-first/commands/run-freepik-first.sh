#!/usr/bin/env bash
set -euo pipefail

if [[ -z "${FREEPIK_API_KEY:-}" ]]; then
  echo "FREEPIK_API_KEY is required for this Freepik-first run." >&2
  exit 1
fi

mkdir -p ./creative-output/{assets,scenes,audio,final,manifests}

echo "=== asset_scene_1 (freepik) ==="
curl -s -X POST https://api.freepik.com/v1/ai/mystic -H 'x-freepik-api-key: $FREEPIK_API_KEY' -H 'Content-Type: application/json' -d '{"prompt":"Create a 45-second product marketing video for an AI note-taking app for founders. Hook scene, 16:9, modern cinematic lighting.","resolution":"2k","styling":{"style":"photo"}}'

echo "=== asset_scene_2 (freepik) ==="
curl -s -X POST https://api.freepik.com/v1/ai/mystic -H 'x-freepik-api-key: $FREEPIK_API_KEY' -H 'Content-Type: application/json' -d '{"prompt":"Create a 45-second product marketing video for an AI note-taking app for founders. Pain scene, 16:9, modern cinematic lighting.","resolution":"2k","styling":{"style":"photo"}}'

echo "=== asset_scene_3 (freepik) ==="
curl -s -X POST https://api.freepik.com/v1/ai/mystic -H 'x-freepik-api-key: $FREEPIK_API_KEY' -H 'Content-Type: application/json' -d '{"prompt":"Create a 45-second product marketing video for an AI note-taking app for founders. Reveal scene, 16:9, modern cinematic lighting.","resolution":"2k","styling":{"style":"photo"}}'

echo "=== asset_scene_4 (freepik) ==="
curl -s -X POST https://api.freepik.com/v1/ai/mystic -H 'x-freepik-api-key: $FREEPIK_API_KEY' -H 'Content-Type: application/json' -d '{"prompt":"Create a 45-second product marketing video for an AI note-taking app for founders. Features scene, 16:9, modern cinematic lighting.","resolution":"2k","styling":{"style":"photo"}}'

echo "=== asset_scene_5 (freepik) ==="
curl -s -X POST https://api.freepik.com/v1/ai/mystic -H 'x-freepik-api-key: $FREEPIK_API_KEY' -H 'Content-Type: application/json' -d '{"prompt":"Create a 45-second product marketing video for an AI note-taking app for founders. Proof scene, 16:9, modern cinematic lighting.","resolution":"2k","styling":{"style":"photo"}}'

echo "=== asset_scene_6 (freepik) ==="
curl -s -X POST https://api.freepik.com/v1/ai/mystic -H 'x-freepik-api-key: $FREEPIK_API_KEY' -H 'Content-Type: application/json' -d '{"prompt":"Create a 45-second product marketing video for an AI note-taking app for founders. CTA scene, 16:9, modern cinematic lighting.","resolution":"2k","styling":{"style":"photo"}}'

echo "=== asset_scene_7 (freepik) ==="
curl -s -X POST https://api.freepik.com/v1/ai/mystic -H 'x-freepik-api-key: $FREEPIK_API_KEY' -H 'Content-Type: application/json' -d '{"prompt":"Create a 45-second product marketing video for an AI note-taking app for founders. Hook scene, 16:9, modern cinematic lighting.","resolution":"2k","styling":{"style":"photo"}}'

echo "=== asset_scene_8 (freepik) ==="
curl -s -X POST https://api.freepik.com/v1/ai/mystic -H 'x-freepik-api-key: $FREEPIK_API_KEY' -H 'Content-Type: application/json' -d '{"prompt":"Create a 45-second product marketing video for an AI note-taking app for founders. Pain scene, 16:9, modern cinematic lighting.","resolution":"2k","styling":{"style":"photo"}}'

echo "=== video_scene_1 (freepik) ==="
curl -s -X POST https://api.freepik.com/v1/ai/video/kling-v3-omni-pro -H 'x-freepik-api-key: $FREEPIK_API_KEY' -H 'Content-Type: application/json' -d '{"prompt":"Animate scene 1 with cinematic product motion","duration":5}'

echo "=== video_scene_3 (freepik) ==="
curl -s -X POST https://api.freepik.com/v1/ai/video/kling-v3-omni-pro -H 'x-freepik-api-key: $FREEPIK_API_KEY' -H 'Content-Type: application/json' -d '{"prompt":"Animate scene 3 with cinematic product motion","duration":5}'

echo "=== video_scene_5 (freepik) ==="
curl -s -X POST https://api.freepik.com/v1/ai/video/kling-v3-omni-pro -H 'x-freepik-api-key: $FREEPIK_API_KEY' -H 'Content-Type: application/json' -d '{"prompt":"Animate scene 5 with cinematic product motion","duration":5}'

echo "=== video_scene_7 (freepik) ==="
curl -s -X POST https://api.freepik.com/v1/ai/video/kling-v3-omni-pro -H 'x-freepik-api-key: $FREEPIK_API_KEY' -H 'Content-Type: application/json' -d '{"prompt":"Animate scene 7 with cinematic product motion","duration":5}'

echo "=== voiceover (freepik) ==="
curl -s -X POST https://api.freepik.com/v1/ai/voiceover/elevenlabs-turbo-v2-5 -H 'x-freepik-api-key: $FREEPIK_API_KEY' -H 'Content-Type: application/json' -d '{"text":"Replace with stitched scene narration","voice_id":"21m00Tcm4TlvDq8ikWAM"}'

echo "=== music (freepik) ==="
curl -s -X POST https://api.freepik.com/v1/ai/music-generation -H 'x-freepik-api-key: $FREEPIK_API_KEY' -H 'Content-Type: application/json' -d '{"prompt":"upbeat modern product marketing background music","music_length_seconds":45}'


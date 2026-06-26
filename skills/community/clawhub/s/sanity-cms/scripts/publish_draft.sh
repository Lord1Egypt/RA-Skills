#!/usr/bin/env bash
# publish_draft.sh — Upload a cover image asset and create/update a Sanity draft document
#
# Works with any Sanity document type. The JSON file must be a valid document
# matching the target schema. The script injects _id, _type (if missing), and
# optionally a coverImage reference before pushing to Sanity.
#
# If the JSON already contains an _id, the existing document is PATCHED (updated)
# rather than replaced — preventing duplicate document creation.
#
# Usage:
#   publish_draft.sh <document-json-file> [cover-image-file]
#
# Arguments:
#   document-json-file   Path to the Sanity-formatted JSON document
#   cover-image-file     (optional) Path to PNG/JPG/WebP cover image
#                        If provided, uploaded and injected as `coverImage`
#                        The JSON field name can be overridden with COVER_IMAGE_FIELD
#
# Required env vars:
#   SANITY_PROJECT_ID    Your Sanity project ID
#   SANITY_API_TOKEN     Write-enabled API token
#
# Optional env vars:
#   SANITY_DATASET       Dataset name (default: production)
#   COVER_IMAGE_FIELD    Field name for cover image (default: coverImage)
#   DRAFT_PREFIX         Set to "false" to publish directly (default: drafts.)
#
# Output:
#   Prints the document _id on success

set -euo pipefail

DOCUMENT_JSON="${1:?Usage: publish_draft.sh <document-json-file> [cover-image-file]}"
COVER_IMAGE="${2:-}"

: "${SANITY_PROJECT_ID:?SANITY_PROJECT_ID not set}"
: "${SANITY_API_TOKEN:?SANITY_API_TOKEN not set}"
DATASET="${SANITY_DATASET:-production}"
COVER_FIELD="${COVER_IMAGE_FIELD:-coverImage}"
USE_DRAFT_PREFIX="${DRAFT_PREFIX:-true}"

BASE_URL="https://${SANITY_PROJECT_ID}.api.sanity.io/v2021-06-07"
ASSET_ID=""

# --- Upload cover image (optional) ---
if [ -n "$COVER_IMAGE" ]; then
  case "${COVER_IMAGE##*.}" in
    jpg|jpeg) CONTENT_TYPE="image/jpeg" ;;
    png)      CONTENT_TYPE="image/png" ;;
    webp)     CONTENT_TYPE="image/webp" ;;
    gif)      CONTENT_TYPE="image/gif" ;;
    *)        echo "Unsupported image type: ${COVER_IMAGE##*.}" >&2; exit 1 ;;
  esac

  echo "Uploading image: $COVER_IMAGE" >&2
  UPLOAD_RESPONSE=$(curl -s -X POST \
    "${BASE_URL}/assets/images/${DATASET}" \
    -H "Authorization: Bearer ${SANITY_API_TOKEN}" \
    -H "Content-Type: ${CONTENT_TYPE}" \
    --data-binary "@${COVER_IMAGE}")

  ASSET_ID=$(python3 -c "import sys,json; print(json.loads(sys.stdin.read())['document']['_id'])" <<< "$UPLOAD_RESPONSE" 2>/dev/null || true)

  if [ -z "$ASSET_ID" ]; then
    echo "Image upload failed. Response:" >&2
    echo "$UPLOAD_RESPONSE" >&2
    exit 1
  fi
  echo "Image asset ID: $ASSET_ID" >&2
fi

# --- Build document and choose mutation strategy ---
MUTATION=$(python3 - <<PYEOF
import json, uuid, sys

with open('${DOCUMENT_JSON}') as f:
    doc = json.load(f)

# Determine _id and whether this is a create or patch
existing_id = doc.get('_id', '').strip()
is_patch = bool(existing_id)  # If _id already exists, patch instead of create

if not existing_id:
    new_id = str(uuid.uuid4())
    prefix = 'drafts.' if '${USE_DRAFT_PREFIX}' == 'true' else ''
    doc['_id'] = prefix + new_id
elif '${USE_DRAFT_PREFIX}' == 'true' and not existing_id.startswith('drafts.'):
    doc['_id'] = 'drafts.' + existing_id

doc_id = doc['_id']

# Inject coverImage if asset was uploaded
asset_id = '${ASSET_ID}'
cover_patch = {}
if asset_id:
    cover_ref = {
        '_type': 'image',
        'asset': {'_type': 'reference', '_ref': asset_id}
    }
    doc['${COVER_FIELD}'] = cover_ref
    cover_patch = {'${COVER_FIELD}': cover_ref}

# Use patch (set) if document already has an _id — avoids creating duplicates
# Use createOrReplace for new documents
if is_patch and asset_id:
    # Only patching the cover image field onto existing doc
    mutation = {'mutations': [{'patch': {'id': doc_id, 'set': cover_patch}}]}
else:
    mutation = {'mutations': [{'createOrReplace': doc}]}

print(json.dumps({'_id': doc_id, 'mutation': mutation}))
PYEOF
)

DOC_ID=$(python3 -c "import json,sys; print(json.loads(sys.stdin.read())['_id'])" <<< "$MUTATION")
MUTATION_PAYLOAD=$(python3 -c "import json,sys; print(json.dumps(json.loads(sys.stdin.read())['mutation']))" <<< "$MUTATION")

echo "Pushing document to Sanity (dataset: ${DATASET})..." >&2
RESPONSE=$(curl -s -X POST \
  "${BASE_URL}/data/mutate/${DATASET}" \
  -H "Authorization: Bearer ${SANITY_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "$MUTATION_PAYLOAD")

ERROR=$(python3 -c "
import json, sys
d = json.loads(sys.stdin.read())
print(d.get('error', {}).get('description', '') or '')
" <<< "$RESPONSE" 2>/dev/null || true)

if [ -n "$ERROR" ]; then
  echo "Sanity error: $ERROR" >&2
  echo "$RESPONSE" >&2
  exit 1
fi

echo "$DOC_ID"
echo "Done." >&2

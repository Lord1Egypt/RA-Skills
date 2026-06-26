#!/usr/bin/env bash
# Usage: get-schema.sh [resource]
#   Run this BEFORE a create/post to retrieve the expected request shape. Then build your POST body from the output.
#   resource: dataset | data-item | project | work-package | task | campaign | email-template | webpage-template
#   If no resource given, lists available schemas.
# Example: get-schema.sh dataset
# Example: get-schema.sh
set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
SCHEMAS_DIR="$SKILL_DIR/schemas"
RESOURCE="${1:-}"
# Map alias to filename (e.g. dataset -> dataset.json)
FILE="$RESOURCE.json"
SCHEMA_PATH="$SCHEMAS_DIR/$FILE"
if [ -z "$RESOURCE" ]; then
  echo "Usage: get-schema.sh <resource>"
  echo "Retrieve the expected request shape for a resource before posting. Then build your POST body from the schema."
  echo ""
  echo "Available resources:"
  for f in "$SCHEMAS_DIR"/*.json; do
    [ -f "$f" ] || continue
    name=$(basename "$f" .json)
    echo "  $name"
  done
  echo ""
  echo "Example: get-schema.sh dataset   # then use scripts/create-dataset.sh with a body matching the schema"
  exit 0
fi
if [ ! -f "$SCHEMA_PATH" ]; then
  echo "Error: Unknown resource '$RESOURCE'. Available: dataset, data-item, project, work-package, task, campaign, email-template, webpage-template"
  exit 1
fi
cat "$SCHEMA_PATH"

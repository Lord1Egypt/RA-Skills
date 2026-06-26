#!/usr/bin/env bash
set -euo pipefail

# OL Wave Loader - Bridges OL hero hunt output into AO swarm execution
# Extracts and validates wave data from ol hero hunt JSON output.
# Called once at swarm startup when --from-wave is passed.

WAVE_FILE="${1:?Usage: ol-wave-loader.sh <wave-json-file>}"

# Validate file exists and is readable
if [[ ! -f "$WAVE_FILE" ]]; then
    echo "Error: Wave file not found: $WAVE_FILE" >&2
    exit 1
fi

if [[ ! -r "$WAVE_FILE" ]]; then
    echo "Error: Wave file not readable: $WAVE_FILE" >&2
    exit 1
fi

# Extract and validate the wave array from ol hero hunt output
# Check that each wave entry has required fields: id, title, spec_path, priority
wave_entries=$(jq -c '.wave[]?' "$WAVE_FILE" 2>/dev/null) || {
    echo "Error: Failed to parse wave array from $WAVE_FILE (not valid JSON or missing 'wave' key)" >&2
    exit 1
}

# Process each wave entry
if [[ -z "$wave_entries" ]]; then
    echo "Error: No wave entries found in $WAVE_FILE" >&2
    exit 1
fi

# Validate and output sorted entries
results=()
while IFS= read -r entry; do
    # Skip empty lines (e.g., trailing newline from heredoc)
    [[ -z "$entry" ]] && continue
    # Validate required fields
    id=$(echo "$entry" | jq -r '.id // empty') || {
        echo "Error: jq failed parsing 'id' from wave entry: $entry" >&2
        exit 1
    }
    if [[ -z "$id" ]]; then
        echo "Error: Missing or invalid 'id' field in wave entry: $entry" >&2
        exit 1
    fi

    title=$(echo "$entry" | jq -r '.title // empty') || {
        echo "Error: jq failed parsing 'title' from wave entry: $entry" >&2
        exit 1
    }
    if [[ -z "$title" ]]; then
        echo "Error: Missing or invalid 'title' field in wave entry: $entry" >&2
        exit 1
    fi

    spec_path=$(echo "$entry" | jq -r '.spec_path // empty') || {
        echo "Error: jq failed parsing 'spec_path' from wave entry: $entry" >&2
        exit 1
    }
    if [[ -z "$spec_path" ]]; then
        echo "Error: Missing or invalid 'spec_path' field in wave entry: $entry" >&2
        exit 1
    fi

    priority=$(echo "$entry" | jq -r '.priority // empty') || {
        echo "Error: jq failed parsing 'priority' from wave entry: $entry" >&2
        exit 1
    }
    if [[ -z "$priority" ]]; then
        echo "Error: Missing or invalid 'priority' field in wave entry: $entry" >&2
        exit 1
    fi

    # Validate priority is a number
    if ! [[ "$priority" =~ ^[0-9]+$ ]]; then
        echo "Error: Priority must be a number, got '$priority' for bead $id" >&2
        exit 1
    fi

    # Validate fields do not contain newlines or tabs (prevents TSV array corruption)
    for _field_name in id title spec_path; do
        eval "_field_val=\$$_field_name"
        if [[ "$_field_val" =~ [$'\n'$'\t'] ]]; then
            echo "Error: '$_field_name' field contains newline or tab characters in wave entry: $entry" >&2
            exit 1
        fi
    done

    # Store result for sorting (priority first for sorting, then output columns)
    results+=("$priority"$'\t'"$id"$'\t'"$title"$'\t'"$spec_path")
done <<< "$wave_entries"

# Sort by priority (column 1, numeric) and output in correct order (id, title, spec_path, priority)
printf '%s\n' "${results[@]}" | sort -t$'\t' -k1 -n | awk -F$'\t' '{print $2"\t"$3"\t"$4"\t"$1}'

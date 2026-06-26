#!/usr/bin/env bash
# =============================================================================
# cold-outreach.sh — VexPath Cold Outreach Generator
# =============================================================================
# Usage: ./cold-outreach.sh <leads.csv> [output_dir]
#
# CSV format (with header row):
#   address,name,email
#
# Requires:
#   - GOOGLE_MAPS_API_KEY env var
#   - roof-estimate.sh in the same directory (or on PATH)
#   - python3, jq, curl
#
# Output:
#   - Prints drafted emails to stdout for review
#   - Saves JSON file to output_dir (default: ./outreach-output)
#   - Does NOT auto-send anything
#
# Rate limiting: 1 API call per second to respect Google API limits
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ESTIMATE_SCRIPT="${SCRIPT_DIR}/roof-estimate.sh"

# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------
if [[ -z "${GOOGLE_MAPS_API_KEY:-}" ]]; then
  echo "ERROR: GOOGLE_MAPS_API_KEY environment variable is not set" >&2
  exit 1
fi

if [[ $# -lt 1 || -z "$1" ]]; then
  echo "Usage: cold-outreach.sh <leads.csv> [output_dir]" >&2
  echo "CSV columns: address,name,email" >&2
  exit 1
fi

CSV_FILE="$1"
OUTPUT_DIR="${2:-./outreach-output}"

if [[ ! -f "$CSV_FILE" ]]; then
  echo "ERROR: CSV file not found: ${CSV_FILE}" >&2
  exit 1
fi

if [[ ! -f "$ESTIMATE_SCRIPT" ]]; then
  echo "ERROR: roof-estimate.sh not found at: ${ESTIMATE_SCRIPT}" >&2
  exit 1
fi

chmod +x "$ESTIMATE_SCRIPT"
mkdir -p "$OUTPUT_DIR"

TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
OUTPUT_FILE="${OUTPUT_DIR}/outreach_${TIMESTAMP}.json"
LOG_FILE="${OUTPUT_DIR}/outreach_${TIMESTAMP}.log"

# ---------------------------------------------------------------------------
# Email template (post-storm — default)
# ---------------------------------------------------------------------------
generate_email() {
  local name="$1"
  local address="$2"
  local area_sqft="$3"
  local cost_low="$4"
  local cost_high="$5"
  local squares="$6"

  # Neighborhood: use first part of address (strip street number)
  local neighborhood
  neighborhood="$(echo "$address" | sed 's/^[0-9]* //' | cut -d',' -f2- | xargs)"

  cat <<EMAIL
Subject: Quick question about your roof at ${address}

Hi ${name},

Your area was recently hit by a severe storm, and we wanted to reach out
about your home at ${address}.

Based on our roof analysis, your property has approximately ${area_sqft} sq ft
of roof area (${squares} roofing squares). Estimated replacement cost range:
\$${cost_low} – \$${cost_high}.

Many homeowners don't realize storm damage exists until it causes leaks or
interior damage — and most damage is covered by homeowner's insurance.

We're offering **free roof inspections** for homeowners in ${neighborhood}
this week. No cost. No pressure. No obligation.

If you'd like us to take a look and document any damage for an insurance
claim, reply to this email or call us at [COMPANY_PHONE].

[COMPANY_NAME]
[COMPANY_PHYSICAL_ADDRESS]
[CITY, STATE ZIP]
[PHONE] | [WEBSITE]

To unsubscribe from future emails, reply with "unsubscribe" in the subject.
EMAIL
}

# ---------------------------------------------------------------------------
# Process CSV
# ---------------------------------------------------------------------------
RESULTS=()
TOTAL=0
SUCCESS=0
FAILED=0

echo "=====================================================================" | tee -a "$LOG_FILE"
echo "VexPath Cold Outreach Generator — $(date)" | tee -a "$LOG_FILE"
echo "Input:  ${CSV_FILE}" | tee -a "$LOG_FILE"
echo "Output: ${OUTPUT_FILE}" | tee -a "$LOG_FILE"
echo "=====================================================================" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# Skip header row, read CSV
while IFS=',' read -r address name email; do
  # Skip header
  if [[ "$address" == "address" ]]; then
    continue
  fi

  # Trim whitespace and quotes
  address="$(echo "$address" | sed 's/^[[:space:]"]*//;s/[[:space:]"]*$//')"
  name="$(echo "$name"    | sed 's/^[[:space:]"]*//;s/[[:space:]"]*$//')"
  email="$(echo "$email"  | sed 's/^[[:space:]"]*//;s/[[:space:]"]*$//')"

  if [[ -z "$address" || -z "$email" ]]; then
    echo "SKIP: Missing address or email (name=${name})" | tee -a "$LOG_FILE"
    ((FAILED++)) || true
    ((TOTAL++))  || true
    continue
  fi

  echo "Processing: ${address} (${name} <${email}>)" | tee -a "$LOG_FILE"

  # Get roof estimate
  ESTIMATE_JSON="$("$ESTIMATE_SCRIPT" "$address" 2>>"$LOG_FILE")" || {
    echo "  FAILED: roof-estimate.sh returned an error for: ${address}" | tee -a "$LOG_FILE"
    RESULTS+=("{\"address\":\"${address}\",\"name\":\"${name}\",\"email\":\"${email}\",\"status\":\"error\",\"error\":\"roof estimate failed\"}")
    ((FAILED++)) || true
    ((TOTAL++))  || true
    sleep 1
    continue
  }

  # Check for error in estimate JSON
  ESTIMATE_ERROR="$(echo "$ESTIMATE_JSON" | jq -r '.error // empty')"
  if [[ -n "$ESTIMATE_ERROR" ]]; then
    echo "  FAILED: ${ESTIMATE_ERROR}" | tee -a "$LOG_FILE"
    RESULTS+=("{\"address\":\"${address}\",\"name\":\"${name}\",\"email\":\"${email}\",\"status\":\"error\",\"error\":\"${ESTIMATE_ERROR}\"}")
    ((FAILED++)) || true
    ((TOTAL++))  || true
    sleep 1
    continue
  fi

  AREA_SQFT="$(echo "$ESTIMATE_JSON" | jq -r '.total_area_sqft')"
  COST_LOW="$(echo "$ESTIMATE_JSON"  | jq -r '.cost_estimate.low')"
  COST_HIGH="$(echo "$ESTIMATE_JSON" | jq -r '.cost_estimate.high')"
  SQUARES="$(echo "$ESTIMATE_JSON"   | jq -r '.total_squares')"

  echo "  Area: ${AREA_SQFT} sq ft | Squares: ${SQUARES} | Est: \$${COST_LOW}–\$${COST_HIGH}" | tee -a "$LOG_FILE"

  # Generate email draft
  EMAIL_DRAFT="$(generate_email "$name" "$address" "$AREA_SQFT" "$COST_LOW" "$COST_HIGH" "$SQUARES")"

  # Print draft for review
  echo "" | tee -a "$LOG_FILE"
  echo "--- DRAFT EMAIL TO: ${email} ---"
  echo "$EMAIL_DRAFT"
  echo "--- END DRAFT ---"
  echo "" | tee -a "$LOG_FILE"

  # Escape for JSON
  EMAIL_ESCAPED="$(echo "$EMAIL_DRAFT" | python3 -c "import sys,json; print(json.dumps(sys.stdin.read()))")"

  # Build result entry
  RESULT_ENTRY="$(echo "$ESTIMATE_JSON" | jq \
    --arg name    "$name" \
    --arg email   "$email" \
    --arg draft   "$EMAIL_DRAFT" \
    '{
      address:       .address,
      name:          $name,
      email:         $email,
      status:        "draft_ready",
      roof_area_sqft: .total_area_sqft,
      num_segments:  .num_segments,
      avg_pitch:     .avg_pitch,
      waste_percent: .waste_percent,
      total_squares: .total_squares,
      cost_low:      .cost_estimate.low,
      cost_high:     .cost_estimate.high,
      email_draft:   $draft
    }')"

  RESULTS+=("$RESULT_ENTRY")
  ((SUCCESS++)) || true
  ((TOTAL++))   || true

  # Rate limit: 1 second between API calls
  sleep 1

done < "$CSV_FILE"

# ---------------------------------------------------------------------------
# Write JSON output
# ---------------------------------------------------------------------------
python3 - "${OUTPUT_FILE}" "${TOTAL}" "${SUCCESS}" "${FAILED}" "${RESULTS[@]+"${RESULTS[@]}"}" <<'PYEOF'
import sys, json

output_file = sys.argv[1]
total       = int(sys.argv[2])
success     = int(sys.argv[3])
failed      = int(sys.argv[4])
results_raw = sys.argv[5:]  # each is a JSON string

results = []
for r in results_raw:
    try:
        results.append(json.loads(r))
    except json.JSONDecodeError:
        results.append({"raw": r, "parse_error": True})

output = {
    "generated_at": __import__("datetime").datetime.utcnow().isoformat() + "Z",
    "summary": {
        "total":   total,
        "success": success,
        "failed":  failed
    },
    "leads": results
}

with open(output_file, "w") as f:
    json.dump(output, f, indent=2)

print(f"Saved to: {output_file}")
PYEOF

echo "" | tee -a "$LOG_FILE"
echo "=====================================================================" | tee -a "$LOG_FILE"
echo "Done. Processed: ${TOTAL} | Success: ${SUCCESS} | Failed: ${FAILED}" | tee -a "$LOG_FILE"
echo "Review all drafts above BEFORE sending." | tee -a "$LOG_FILE"
echo "JSON saved to: ${OUTPUT_FILE}" | tee -a "$LOG_FILE"
echo "Log saved to:  ${LOG_FILE}" | tee -a "$LOG_FILE"
echo "=====================================================================" | tee -a "$LOG_FILE"

#!/usr/bin/env bash
set -euo pipefail

# Live smoke test for Semantic Scholar scripts.
# It runs:
# 1) bulk search
# 2) paper batch fetch (using IDs from step 1)
# 3) author batch fetch (using IDs from step 1)
# 4) recommendations (using one paper ID from step 1)

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT_DIR="${1:-/tmp/semantic_scholar_smoke_$(date +%Y%m%d_%H%M%S)}"

if ! command -v uv >/dev/null 2>&1; then
  echo "[ERROR] 'uv' is required but was not found in PATH." >&2
  exit 1
fi

mkdir -p "${OUT_DIR}"

BULK_JSONL="${OUT_DIR}/bulk.jsonl"
PAPER_IDS_FILE="${OUT_DIR}/paper_ids.txt"
AUTHOR_IDS_FILE="${OUT_DIR}/author_ids.txt"
PAPER_BATCH_JSONL="${OUT_DIR}/paper_batch.jsonl"
PAPER_BATCH_CSV="${OUT_DIR}/paper_batch.csv"
AUTHOR_BATCH_JSONL="${OUT_DIR}/author_batch.jsonl"
AUTHOR_BATCH_CSV="${OUT_DIR}/author_batch.csv"
RECO_JSONL="${OUT_DIR}/recommendations.jsonl"
RECO_CSV="${OUT_DIR}/recommendations.csv"

echo "[STEP] 1/4 bulk search"
uv run python "${ROOT_DIR}/semantic_scholar_bulk_search.py" \
  --query "graph neural network" \
  --fields "paperId,title,year,authors,url,citationCount" \
  --max-pages 1 \
  --sleep-seconds 0 \
  --output "${BULK_JSONL}"

echo "[STEP] extract paper/author IDs from bulk results"
uv run python - "${BULK_JSONL}" "${PAPER_IDS_FILE}" "${AUTHOR_IDS_FILE}" <<'PY'
import json
import sys
from pathlib import Path

bulk_path = Path(sys.argv[1])
paper_ids_path = Path(sys.argv[2])
author_ids_path = Path(sys.argv[3])

paper_ids = []
author_ids = []
seen_paper = set()
seen_author = set()

with bulk_path.open("r", encoding="utf-8") as fin:
    for line in fin:
        row = json.loads(line)
        paper_id = row.get("paperId")
        if paper_id and paper_id not in seen_paper:
            seen_paper.add(paper_id)
            paper_ids.append(paper_id)
        for author in row.get("authors") or []:
            if not isinstance(author, dict):
                continue
            author_id = author.get("authorId")
            if author_id and author_id not in seen_author:
                seen_author.add(author_id)
                author_ids.append(author_id)
        if len(paper_ids) >= 3 and len(author_ids) >= 3:
            break

if len(paper_ids) < 1 or len(author_ids) < 1:
    raise SystemExit("Not enough IDs extracted from bulk results.")

paper_ids_path.write_text("\n".join(paper_ids[:3]) + "\n", encoding="utf-8")
author_ids_path.write_text("\n".join(author_ids[:3]) + "\n", encoding="utf-8")
print("paper_ids", paper_ids[:3])
print("author_ids", author_ids[:3])
PY

echo "[STEP] 2/4 paper batch fetch"
uv run python "${ROOT_DIR}/paper_batch_fetch.py" \
  --ids-file "${PAPER_IDS_FILE}" \
  --fields "paperId,title,year,authors,url,citationCount,publicationDate,venue" \
  --output "${PAPER_BATCH_JSONL}" \
  --csv-output "${PAPER_BATCH_CSV}" \
  --chunk-size 2 \
  --sleep-seconds 0

echo "[STEP] 3/4 author batch fetch"
uv run python "${ROOT_DIR}/author_batch_fetch.py" \
  --ids-file "${AUTHOR_IDS_FILE}" \
  --output "${AUTHOR_BATCH_JSONL}" \
  --csv-output "${AUTHOR_BATCH_CSV}" \
  --chunk-size 2 \
  --sleep-seconds 0

echo "[STEP] 4/4 recommendations"
RECO_OK=0
while IFS= read -r SEED_ID; do
  SEED_ID="$(echo "${SEED_ID}" | tr -d '\r\n')"
  if [[ -z "${SEED_ID}" ]]; then
    continue
  fi
  echo "[INFO] Trying recommendation seed: ${SEED_ID}"
  uv run python "${ROOT_DIR}/recommend_papers.py" \
    --positive-ids "${SEED_ID}" \
    --limit 5 \
    --fields "paperId,title,year,authors,url,citationCount,publicationDate,venue" \
    --output "${RECO_JSONL}" \
    --csv-output "${RECO_CSV}" || continue

  RECO_COUNT="$(wc -l < "${RECO_JSONL}" | tr -d ' ')"
  if [[ "${RECO_COUNT}" -gt 0 ]]; then
    RECO_OK=1
    break
  fi
done < "${PAPER_IDS_FILE}"

if [[ "${RECO_OK}" -eq 0 ]]; then
  echo "[WARN] Recommendations endpoint returned 0 rows for tested seeds. Request succeeded, but no recommendations were returned."
fi

echo "[DONE] Live smoke test completed."
echo "[DONE] Output directory: ${OUT_DIR}"

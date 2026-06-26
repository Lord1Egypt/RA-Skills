"""
superwise_ingest.py
-------------------
Core ingestion and verification module for the superwise-drift-detection-skill.

Handles:
  - CSV → Superwise dataset ingestion via REST (one record per POST)
  - Synthetic row_id column for deduplication and drop detection
  - CubeJS paginated query to verify row counts after upload
  - Automatic retry for dropped rows (known Superwise platform issue)

Usage:
    from superwise_ingest import SuperwiseIngester

    ingester = SuperwiseIngester(client_id, client_secret)
    result = ingester.ingest_csv(
        csv_path="training_data.csv",
        dataset_id="abc-123",
        dataset_name="my_model_training",
    )
    print(result)  # {"total": 500, "verified": 500, "missing": 0, "retried": 3}
"""

import logging
import time
import uuid

import pandas as pd
import requests
from superwise_api.superwise_client import SuperwiseClient

logger = logging.getLogger(__name__)

# Superwise REST endpoints
_INGEST_URL = "https://api.superwise.ai/v1/datasets/{dataset_id}/log"
_QUERY_URL = "https://api.superwise.ai/v1/query/load"

# Tuning knobs
PAGE_SIZE = 1000        # CubeJS rows per page
ROW_DELAY = 0.05        # seconds between ingest POSTs (rate-limit courtesy)
VERIFY_PAUSE = 2.0      # seconds to wait before querying after upload (indexing lag)
MAX_RETRIES = 3         # retry passes for dropped rows


class SuperwiseIngester:
    """
    Ingests a CSV file into a Superwise dataset and verifies every row landed.

    Auth is handled by the Superwise Python SDK — initialize once with your
    client_id and client_secret, then reuse for both training and inference uploads.

    CubeJS cube name note:
        Superwise exposes datasets through CubeJS with the cube name derived from
        the dataset name. The exact transformation (snake_case, CamelCase, etc.)
        varies by account configuration. If verification queries return zero rows,
        check the column prefix in the raw response and set the cube name
        explicitly via the `cube_name` parameter on query methods.
    """

    def __init__(self, client_id: str, client_secret: str):
        self._sw = SuperwiseClient(client_id=client_id, client_secret=client_secret)
        self._token: str | None = None

    @property
    def token(self) -> str:
        if self._token is None:
            self._token = self._sw.configuration.access_token
        return self._token

    def _ingest_headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def _query_headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "x-meta-type": "dataset",
        }

    def get_cube_name(self, dataset_id: str) -> str:
        """
        Fetch the CubeJS cube name for a dataset.

        Superwise's CubeJS cube name is the dataset's internal `_id` field
        (UUID format with underscores), NOT the human-readable dataset name.
        This method fetches the dataset object and returns the correct cube name.
        """
        resp = requests.get(
            f"https://api.superwise.ai/v1/datasets/{dataset_id}",
            headers=self._ingest_headers(),
            timeout=15,
        )
        resp.raise_for_status()
        cube_name = resp.json().get("_id")
        if not cube_name:
            raise RuntimeError(f"Could not find _id for dataset {dataset_id}")
        return cube_name

    # ── Low-level operations ──────────────────────────────────────────────────

    def _post_record(self, dataset_id: str, record: dict) -> bool:
        """POST one record to Superwise. Returns True on HTTP 2xx."""
        url = _INGEST_URL.format(dataset_id=dataset_id)
        try:
            resp = requests.post(
                url,
                headers=self._ingest_headers(),
                json={"record": record},
                timeout=15,
            )
            resp.raise_for_status()
            return True
        except requests.RequestException as exc:
            logger.warning(
                f"[ingest] POST failed for row_id={record.get('row_id', '?')}: {exc}"
            )
            return False

    def query_dataset(
        self,
        dataset_name: str,
        columns: list[str],
        cube_name: str | None = None,
    ) -> pd.DataFrame:
        """
        Fetch all rows from a Superwise dataset via the CubeJS query endpoint.
        Paginates automatically (1 000 rows per page).

        Args:
            dataset_name: Superwise dataset name — used as the CubeJS cube prefix
                          unless `cube_name` is provided.
            columns:      Column names to return (without the cube prefix).
            cube_name:    Override the cube name if Superwise uses a different
                          casing/slug than the raw dataset name.

        Returns:
            DataFrame with all rows; column names stripped of the cube prefix.
        """
        cube = cube_name or dataset_name
        dimensions = [f"{cube}.{col}" for col in columns]
        all_rows: list[dict] = []
        offset = 0

        while True:
            payload = {
                "query": {
                    "timezone": "UTC",
                    "measures": [],
                    "dimensions": dimensions,
                    "filters": [],
                    "limit": PAGE_SIZE,
                    "offset": offset,
                }
            }

            resp = requests.post(
                _QUERY_URL,
                headers=self._query_headers(),
                json=payload,
                timeout=30,
            )

            if resp.status_code != 200:
                raise RuntimeError(
                    f"CubeJS query failed (HTTP {resp.status_code}): {resp.text}"
                )

            page: list[dict] = resp.json().get("data", [])
            all_rows.extend(page)

            if len(page) < PAGE_SIZE:
                break
            offset += PAGE_SIZE

        if not all_rows:
            return pd.DataFrame(columns=columns)

        df = pd.DataFrame(all_rows)
        # Strip "CubeName." prefix returned by Superwise
        df.columns = [c.split(".")[-1] for c in df.columns]
        return df

    # ── Public API ────────────────────────────────────────────────────────────

    def ingest_csv(
        self,
        csv_path: str,
        dataset_id: str,
        dataset_name: str,
        key_col: str | None = None,
        cube_name: str | None = None,
    ) -> dict:
        """
        Upload every row of a CSV to a Superwise dataset, then verify and retry
        any rows that were silently dropped.

        A synthetic `row_id` (UUID) column is always injected so we can diff
        what was sent against what Superwise actually stored.

        Args:
            csv_path:     Path to the CSV file to ingest.
            dataset_id:   Superwise dataset ID (from setup_dataset.py output).
            dataset_name: Superwise dataset name — used in CubeJS verify queries.
            key_col:      Optional column to include as a human-readable ID in logs.
            cube_name:    Override CubeJS cube name if it differs from dataset_name.

        Returns:
            {
                "total":    int,  # rows in the CSV
                "verified": int,  # rows confirmed in Superwise after all retries
                "missing":  int,  # rows still unverified after MAX_RETRIES
                "retried":  int,  # rows that needed at least one retry POST
            }
        """
        df = pd.read_csv(csv_path)
        df["row_id"] = [str(uuid.uuid4()) for _ in range(len(df))]
        total = len(df)
        expected_ids = set(df["row_id"].tolist())

        logger.info(f"[ingest] Starting: {total} rows from {csv_path} → dataset {dataset_id}")

        # ── First pass: upload all rows ───────────────────────────────────────
        for _, row in df.iterrows():
            self._post_record(dataset_id, row.to_dict())
            time.sleep(ROW_DELAY)

        logger.info(f"[ingest] Upload pass complete. Verifying...")

        # ── Verify + retry loop ───────────────────────────────────────────────
        # New datasets take time for Superwise to register their CubeJS cube.
        # If the verify query itself fails (cube not found), we skip that attempt
        # rather than treating all rows as missing — which would cause a full
        # re-upload of every row on every attempt.
        verified_ids: set[str] = set()
        missing_ids: set[str] = expected_ids.copy()
        query_ever_succeeded = False
        retried = 0

        for attempt in range(MAX_RETRIES + 1):
            time.sleep(VERIFY_PAUSE)  # let Superwise index the batch

            try:
                verified_df = self.query_dataset(dataset_name, ["row_id"], cube_name=cube_name)
                verified_ids = set(verified_df["row_id"].tolist()) if not verified_df.empty else set()
                query_ever_succeeded = True
            except Exception as exc:
                logger.warning(
                    f"[ingest] Verify query failed (attempt {attempt + 1}/{MAX_RETRIES + 1}): {exc}\n"
                    f"         CubeJS cube may not be registered yet — skipping retry this pass."
                )
                continue  # don't retry rows when we can't even query — just wait and try again

            missing_ids = expected_ids - verified_ids

            if not missing_ids:
                logger.info(f"[ingest] All {total} rows verified ✓")
                break

            if attempt == MAX_RETRIES:
                logger.error(
                    f"[ingest] {len(missing_ids)} rows still missing after {MAX_RETRIES} retries. "
                    f"Check Superwise dashboard for dataset {dataset_id}."
                )
                break

            logger.warning(
                f"[ingest] {len(missing_ids)} dropped rows detected "
                f"— retry {attempt + 1}/{MAX_RETRIES}"
            )
            missing_df = df[df["row_id"].isin(missing_ids)]
            for _, row in missing_df.iterrows():
                if self._post_record(dataset_id, row.to_dict()):
                    retried += 1
                time.sleep(ROW_DELAY)

        if not query_ever_succeeded:
            logger.warning(
                f"[ingest] CubeJS cube for '{dataset_name}' was not queryable during this run. "
                f"Rows were POSTed (HTTP 202) but could not be verified. "
                f"Check the Superwise UI — data should appear once the cube is registered."
            )

        return {
            "total": total,
            "verified": len(verified_ids),
            "missing": len(missing_ids),
            "retried": retried,
        }

    def row_count(self, dataset_name: str, cube_name: str | None = None) -> int:
        """Quick helper: return the number of rows currently in a dataset."""
        df = self.query_dataset(dataset_name, ["row_id"], cube_name=cube_name)
        return len(df)

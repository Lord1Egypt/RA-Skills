"""
setup_drift_policy.py
---------------------
One-time setup: create Superwise Compare Distribution drift policies
that compare your training dataset against your inference dataset.

Run this after setup_dataset.py (training and inference dataset IDs must
already be in your .env).

Column type mapping:
  - string / boolean → Jensen-Shannon divergence (count + dimension query)
  - numeric          → not supported by Superwise distribution_compare API;
                       these columns are skipped with a warning.

Usage:
    # Auto-detect string columns from CSV and create one policy per column:
    python setup_drift_policy.py \
        --training-csv path/to/training.csv \
        --policy-name my_model_drift

    # Monitor only specific columns:
    python setup_drift_policy.py \
        --training-csv path/to/training.csv \
        --policy-name my_model_drift \
        --columns ticker product_category

After running, add the first printed policy ID to your .env:
    SUPERWISE_DRIFT_POLICY_ID=<printed value>
"""

import argparse
import json
import os
import sys

import pandas as pd
import requests
from dotenv import load_dotenv
from superwise_api.superwise_client import SuperwiseClient

from superwise_ingest import SuperwiseIngester

load_dotenv()

POLICIES_URL = "https://api.superwise.ai/v1/policies"


def _require_env(key: str) -> str:
    val = os.getenv(key)
    if not val:
        print(f"ERROR: {key} is not set. Run setup_dataset.py first.")
        sys.exit(1)
    return val


def _auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


def find_existing_policies(token: str) -> dict:
    """Return a dict of {policy_name: policy_id} for all policies in the account."""
    headers = _auth_headers(token)
    existing = {}
    page = 1
    while True:
        resp = requests.get(
            POLICIES_URL, headers=headers, params={"page": page, "size": 25}, timeout=15
        )
        resp.raise_for_status()
        data = resp.json()
        for p in data.get("items", []):
            existing[p["name"]] = p["id"]
        if page >= data.get("pages", 1):
            break
        page += 1
    return existing


def _is_string_column(dtype) -> bool:
    return dtype not in ("float64", "float32", "int64", "int32", "int16", "int8", "bool")


def build_jsd_query(cube_name: str, column: str) -> dict:
    """Build a categorical (count + dimension) CubeJS query for JSD."""
    return {
        "measures": [f"{cube_name}.count"],
        "dimensions": [f"{cube_name}.{column}"],
        "timezone": "UTC",
    }


def create_policy(
    token: str,
    policy_name: str,
    training_dataset_id: str,
    inference_dataset_id: str,
    query_a: dict,
    query_b: dict,
    cron_expression: str,
) -> dict:
    """POST to /v1/policies with JSD distribution_compare and return the created policy."""
    body = {
        "name": policy_name,
        "dataset_id": training_dataset_id,
        "dataset_b_id": inference_dataset_id,
        "cron_expression": cron_expression,
        "destination_ids": [],
        "alert_on_policy_level": True,
        "alert_on_status": "HEALTHY_TO_UNHEALTHY",
        "threshold_settings": {
            "threshold_type": "static",
            "condition_above_value": 0.2,
        },
        "data_config": {
            "type": "distribution_compare",
            "query_a": query_a,
            "query_b": query_b,
            "distance_function": "jensen_shannon_divergence",
            "query_a_time_range_config": {
                "field_name": "received_ts",
                "unit": "WEEK",
                "value": 100,
            },
            "query_b_time_range_config": {
                "field_name": "received_ts",
                "unit": "MINUTE",
                "value": 15,
            },
        },
        "initialize_with_historic_data": True,
    }

    resp = requests.post(POLICIES_URL, headers=_auth_headers(token), json=body, timeout=30)

    if resp.status_code not in (200, 201):
        print(f"[setup_policy] ERROR: Policy creation failed (HTTP {resp.status_code}):")
        print(resp.text)
        return None

    return resp.json()


def main():
    parser = argparse.ArgumentParser(description="Create Superwise drift policies (one per string column).")
    parser.add_argument("--training-csv", required=True, help="Training CSV — used to read feature column names and types")
    parser.add_argument("--policy-name", required=True, help="Base name for the drift policies in Superwise")
    parser.add_argument(
        "--columns",
        nargs="+",
        default=None,
        help="Specific columns to monitor (default: all string/boolean columns except row_id)",
    )
    parser.add_argument(
        "--cron",
        default="0 6 * * *",
        help="Cron schedule for automatic policy evaluation (default: 06:00 UTC daily)",
    )
    args = parser.parse_args()

    client_id = _require_env("SUPERWISE_CLIENT_ID")
    client_secret = _require_env("SUPERWISE_SECRET_TOKEN")
    training_dataset_id = _require_env("SUPERWISE_TRAINING_DATASET_ID")
    inference_dataset_id = _require_env("SUPERWISE_INFERENCE_DATASET_ID")

    sw = SuperwiseClient(client_id=client_id, client_secret=client_secret)
    token = sw.configuration.access_token

    # Determine feature columns and their types from CSV
    df = pd.read_csv(args.training_csv, nrows=5)
    skip_cols = {"row_id", "_row_id"}

    if args.columns:
        candidate_cols = args.columns
    else:
        candidate_cols = [c for c in df.columns if c not in skip_cols]

    string_cols = [c for c in candidate_cols if c in df.columns and _is_string_column(df[c].dtype)]
    numeric_cols = [c for c in candidate_cols if c in df.columns and not _is_string_column(df[c].dtype)]

    if numeric_cols:
        print(f"[setup_policy] WARNING: Numeric columns are not supported by Superwise's distribution_compare API "
              f"and will be skipped: {numeric_cols}")
        print("[setup_policy]   Use a statistics-type policy or compute drift locally for numeric features.")

    if not string_cols:
        print("[setup_policy] ERROR: No string/boolean columns found to monitor. "
              "Specify --columns with categorical columns.")
        sys.exit(1)

    print(f"[setup_policy] String columns to monitor ({len(string_cols)}): {string_cols}")

    # Resolve CubeJS cube names
    ingester = SuperwiseIngester(client_id=client_id, client_secret=client_secret)
    training_cube = ingester.get_cube_name(training_dataset_id)
    inference_cube = ingester.get_cube_name(inference_dataset_id)
    print(f"[setup_policy] Training cube: {training_cube}")
    print(f"[setup_policy] Inference cube: {inference_cube}")

    print(f"[setup_policy] Checking for existing policies...")
    existing_policies = find_existing_policies(token)

    created_policies = []
    skipped_policies = []
    for col in string_cols:
        policy_name = f"{args.policy_name}_{col}" if len(string_cols) > 1 else args.policy_name
        if policy_name in existing_policies:
            policy_id = existing_policies[policy_name]
            print(f"[setup_policy] Found existing policy '{policy_name}' — skipping. id={policy_id}")
            skipped_policies.append({"id": policy_id, "name": policy_name, "column": col})
            continue

        query_a = build_jsd_query(training_cube, col)
        query_b = build_jsd_query(inference_cube, col)

        print(f"[setup_policy] Creating policy '{policy_name}' for column '{col}' (JSD)...")
        policy = create_policy(
            token=token,
            policy_name=policy_name,
            training_dataset_id=training_dataset_id,
            inference_dataset_id=inference_dataset_id,
            query_a=query_a,
            query_b=query_b,
            cron_expression=args.cron,
        )
        if policy:
            policy_id = policy.get("id") or policy.get("policy_id")
            print(f"[setup_policy]   Created: id={policy_id}")
            created_policies.append({"id": policy_id, "name": policy_name, "column": col})

    all_policies = skipped_policies + created_policies
    if not all_policies:
        print("[setup_policy] ERROR: No policies found or created.")
        sys.exit(1)

    if created_policies:
        print(f"\n[setup_policy] Created {len(created_policies)} new policy/policies.")
    if skipped_policies:
        print(f"[setup_policy] Skipped {len(skipped_policies)} already-existing policy/policies.")

    print(f"\n── Add to your .env: ──")
    print(f"SUPERWISE_DRIFT_POLICY_ID={all_policies[0]['id']}  # primary: {all_policies[0]['column']}")
    if len(all_policies) > 1:
        for p in all_policies[1:]:
            print(f"SUPERWISE_DRIFT_POLICY_ID_{p['column']}={p['id']}")

    debug_path = "superwise_policy_response.json"
    with open(debug_path, "w") as f:
        json.dump(created_policies, f, indent=2)
    print(f"\n[setup_policy] Policy list saved to {debug_path}")


if __name__ == "__main__":
    main()

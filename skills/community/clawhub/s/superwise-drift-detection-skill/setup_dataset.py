"""
setup_dataset.py
----------------
One-time setup script: creates the Superwise training and inference datasets
for a model, then uploads the initial training CSV.

Run this once before using the skill. Re-run with --retrain to replace the
training data after a model retraining cycle (inference dataset is preserved).

Usage:
    python setup_dataset.py \
        --training-csv path/to/training.csv \
        --model-name my_model

    # Retrain: replace training data, keep inference history
    python setup_dataset.py \
        --training-csv path/to/new_training.csv \
        --model-name my_model \
        --retrain

After running, copy the printed dataset IDs into your .env:
    SUPERWISE_TRAINING_DATASET_ID=...
    SUPERWISE_TRAINING_DATASET_NAME=...
    SUPERWISE_INFERENCE_DATASET_ID=...
    SUPERWISE_INFERENCE_DATASET_NAME=...
"""

import argparse
import os
import sys

import pandas as pd
import requests
from dotenv import load_dotenv
from superwise_api.superwise_client import SuperwiseClient

from superwise_ingest import SuperwiseIngester

load_dotenv()


def _require_env(key: str) -> str:
    val = os.getenv(key)
    if not val:
        print(f"ERROR: {key} is not set. Add it to your .env file.")
        sys.exit(1)
    return val


def _infer_schema(csv_path: str) -> dict:
    """
    Build a Superwise schema dict from a CSV file's column dtypes.
    Superwise field types: numeric, string, boolean, datetime, date, json, image, image_link.
    _row_id is always included as string (injected during ingest).
    """
    df = pd.read_csv(csv_path, nrows=5)
    fields = {}
    for col, dtype in df.dtypes.items():
        if dtype == "bool":
            fields[col] = {"type": "boolean"}
        elif dtype in ("float64", "float32", "int64", "int32", "int16", "int8"):
            fields[col] = {"type": "numeric"}
        else:
            fields[col] = {"type": "string"}
    # row_id is injected during ingest (not in the CSV); must start with a letter per Superwise rules
    fields["row_id"] = {"type": "string"}
    return {"fields": fields}


def find_existing_datasets(token: str, model_name: str) -> dict:
    """
    Query Superwise for datasets named {model_name}_training and {model_name}_inference.
    Paginates through all pages (25 per page).
    Returns {"training": ds_dict | None, "inference": ds_dict | None}.
    Each ds_dict has keys: id, name, _id (cube name).
    """
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    training_name = f"{model_name}_training"
    inference_name = f"{model_name}_inference"
    result = {"training": None, "inference": None}

    page = 1
    while True:
        resp = requests.get(
            "https://api.superwise.ai/v1/datasets",
            headers=headers,
            params={"page": page, "size": 25},
            timeout=15,
        )
        resp.raise_for_status()
        data = resp.json()
        items = data.get("items", data if isinstance(data, list) else [])

        for ds in items:
            if ds.get("name") == training_name:
                result["training"] = ds
            elif ds.get("name") == inference_name:
                result["inference"] = ds

        if result["training"] and result["inference"]:
            break

        total_pages = data.get("pages", 1)
        if page >= total_pages:
            break
        page += 1

    return result


class _DatasetStub:
    """Minimal stand-in for a Superwise dataset object when we reuse an existing one."""
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name


def create_datasets(
    sw: SuperwiseClient,
    model_name: str,
    csv_path: str,
    skip_training: bool = False,
    skip_inference: bool = False,
    existing_training: dict | None = None,
    existing_inference: dict | None = None,
) -> tuple[object, object]:
    """Create training and/or inference datasets in Superwise. Returns (training, inference).
    Pass skip_* flags to reuse already-created datasets."""
    schema = _infer_schema(csv_path)
    print(f"[setup] Inferred schema: {list(schema['fields'].keys())}")

    training_name = f"{model_name}_training"
    inference_name = f"{model_name}_inference"

    if skip_training and existing_training:
        training_ds = _DatasetStub(id=existing_training["id"], name=existing_training["name"])
        print(f"[setup] Reusing existing training dataset: {training_ds.name} ({training_ds.id})")
    else:
        print(f"[setup] Creating training dataset: {training_name}")
        training_ds = sw.dataset.create(name=training_name, schema=schema)

    if skip_inference and existing_inference:
        inference_ds = _DatasetStub(id=existing_inference["id"], name=existing_inference["name"])
        print(f"[setup] Reusing existing inference dataset: {inference_ds.name} ({inference_ds.id})")
    else:
        print(f"[setup] Creating inference dataset: {inference_name}")
        inference_ds = sw.dataset.create(name=inference_name, schema=schema)

    return training_ds, inference_ds


def replace_training_dataset(sw: SuperwiseClient, model_name: str, csv_path: str) -> object:
    """
    Create a fresh training dataset (versioned by timestamp) for a retrain cycle.
    The old training dataset is left intact in Superwise for audit purposes.
    Returns the new training dataset object.
    """
    from datetime import datetime, timezone

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d")
    training_name = f"{model_name}_training_{stamp}"
    schema = _infer_schema(csv_path)

    print(f"[setup] Creating replacement training dataset: {training_name}")
    training_ds = sw.dataset.create(name=training_name, schema=schema)
    return training_ds


def main():
    parser = argparse.ArgumentParser(description="Set up Superwise datasets for drift detection.")
    parser.add_argument("--training-csv", required=True, help="Path to the training data CSV")
    parser.add_argument("--model-name", required=True, help="Logical name for your model (no spaces)")
    parser.add_argument(
        "--retrain",
        action="store_true",
        help="Replace training data only; keep existing inference dataset",
    )
    parser.add_argument(
        "--key-col",
        default=None,
        help="Optional: natural-key column in your CSV for human-readable row IDs",
    )
    args = parser.parse_args()

    client_id = _require_env("SUPERWISE_CLIENT_ID")
    client_secret = _require_env("SUPERWISE_SECRET_TOKEN")

    sw = SuperwiseClient(client_id=client_id, client_secret=client_secret)
    ingester = SuperwiseIngester(client_id=client_id, client_secret=client_secret)
    token = sw.configuration.access_token

    if args.retrain:
        # Replace training dataset; inference dataset comes from existing .env
        training_ds = replace_training_dataset(sw, args.model_name, args.training_csv)
        inference_dataset_id = _require_env("SUPERWISE_INFERENCE_DATASET_ID")
        inference_dataset_name = _require_env("SUPERWISE_INFERENCE_DATASET_NAME")

        print(f"\n[setup] Uploading training CSV → {training_ds.name} ({training_ds.id})")
        result = ingester.ingest_csv(
            csv_path=args.training_csv,
            dataset_id=training_ds.id,
            dataset_name=training_ds.name,
            key_col=args.key_col,
        )
        _print_result(result)

        training_cube = ingester.get_cube_name(training_ds.id)
        print("\n── Retrain complete. Update your .env with the new training dataset: ──")
        print(f"SUPERWISE_TRAINING_DATASET_ID={training_ds.id}")
        print(f"SUPERWISE_TRAINING_DATASET_NAME={training_ds.name}")
        print(f"SUPERWISE_TRAINING_CUBE_NAME={training_cube}")
        print(f"# Inference dataset unchanged:")
        print(f"SUPERWISE_INFERENCE_DATASET_ID={inference_dataset_id}")
        print(f"SUPERWISE_INFERENCE_DATASET_NAME={inference_dataset_name}")

    else:
        # Check whether datasets already exist before creating
        print(f"[setup] Checking for existing datasets for model '{args.model_name}'...")
        existing = find_existing_datasets(token, args.model_name)
        training_existing = existing["training"]
        inference_existing = existing["inference"]

        if training_existing and inference_existing:
            print(f"[setup] Found existing datasets — skipping creation and training upload.")
            print(f"[setup]   Training:  {training_existing['name']} ({training_existing['id']})")
            print(f"[setup]   Inference: {inference_existing['name']} ({inference_existing['id']})")
            print(f"[setup]   To replace training data, re-run with --retrain.")

            training_cube = ingester.get_cube_name(training_existing["id"])
            inference_cube = ingester.get_cube_name(inference_existing["id"])

            print("\n── Existing setup found. Add these to your .env: ──")
            print(f"SUPERWISE_TRAINING_DATASET_ID={training_existing['id']}")
            print(f"SUPERWISE_TRAINING_DATASET_NAME={training_existing['name']}")
            print(f"SUPERWISE_TRAINING_CUBE_NAME={training_cube}")
            print(f"SUPERWISE_INFERENCE_DATASET_ID={inference_existing['id']}")
            print(f"SUPERWISE_INFERENCE_DATASET_NAME={inference_existing['name']}")
            print(f"SUPERWISE_INFERENCE_CUBE_NAME={inference_cube}")

        else:
            if training_existing and not inference_existing:
                print(f"[setup] WARNING: Found training dataset but no inference dataset. "
                      f"Partial setup detected — creating inference dataset only.")
            elif inference_existing and not training_existing:
                print(f"[setup] WARNING: Found inference dataset but no training dataset. "
                      f"Partial setup detected — creating training dataset and uploading data.")

            # Create whichever datasets are missing
            need_training_upload = training_existing is None
            training_ds, inference_ds = create_datasets(
                sw, args.model_name, args.training_csv,
                skip_training=training_existing is not None,
                skip_inference=inference_existing is not None,
                existing_training=training_existing,
                existing_inference=inference_existing,
            )

            if need_training_upload:
                print(f"\n[setup] Uploading training CSV → {training_ds.name} ({training_ds.id})")
                result = ingester.ingest_csv(
                    csv_path=args.training_csv,
                    dataset_id=training_ds.id,
                    dataset_name=training_ds.name,
                    key_col=args.key_col,
                )
                _print_result(result)
            else:
                print(f"\n[setup] Skipping training upload — dataset already has data.")

            training_cube = ingester.get_cube_name(training_ds.id)
            inference_cube = ingester.get_cube_name(inference_ds.id)

            print("\n── First-time setup complete. Add these to your .env: ──")
            print(f"SUPERWISE_TRAINING_DATASET_ID={training_ds.id}")
            print(f"SUPERWISE_TRAINING_DATASET_NAME={training_ds.name}")
            print(f"SUPERWISE_TRAINING_CUBE_NAME={training_cube}")
            print(f"SUPERWISE_INFERENCE_DATASET_ID={inference_ds.id}")
            print(f"SUPERWISE_INFERENCE_DATASET_NAME={inference_ds.name}")
            print(f"SUPERWISE_INFERENCE_CUBE_NAME={inference_cube}")


def _print_result(result: dict) -> None:
    status = "✓" if result["missing"] == 0 else "⚠"
    print(
        f"[setup] {status} Ingestion: "
        f"{result['verified']}/{result['total']} rows verified "
        f"({result['retried']} retried, {result['missing']} still missing)"
    )
    if result["missing"] > 0:
        print(
            "[setup] WARNING: Some rows are unverified. "
            "Re-run setup or check your Superwise dashboard."
        )


if __name__ == "__main__":
    main()

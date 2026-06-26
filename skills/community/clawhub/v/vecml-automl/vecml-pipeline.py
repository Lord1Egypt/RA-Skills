#!/usr/bin/env python3
"""
VecML AutoML Pipeline — One-command ML training & prediction.

Usage:
  python3 vecml-pipeline.py train data.csv --target Survived
  python3 vecml-pipeline.py predict data.csv --model my_model
  python3 vecml-pipeline.py status --model my_model
  python3 vecml-pipeline.py models
  python3 vecml-pipeline.py importance --model my_model

Environment:
  VECML_API_KEY  — your VecML API key
"""

import argparse
import base64
import csv
import json
import os
import sys
import time
import urllib.request
import urllib.error

API = os.environ.get("VECML_API_URL", "https://aidb.vecml.com/api")
KEY = os.environ.get("VECML_API_KEY", "")
DEFAULT_PROJECT = os.environ.get("VECML_PROJECT", "openclaw_automl")


def post(endpoint, payload):
    """POST JSON to VecML API and return parsed response."""
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        f"{API}/{endpoint}",
        data=data,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        try:
            return json.loads(body)
        except:
            return {"success": False, "error": body, "status_code": e.code}


def b64_file(path):
    """Read a file and return base64-encoded content."""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def detect_columns(csv_path):
    """Auto-detect column types from CSV."""
    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        rows = [r for _, r in zip(range(100), reader)]  # sample first 100 rows

    if not rows:
        return [], [], []

    headers = list(rows[0].keys())
    categorical = []
    numeric = []

    for col in headers:
        values = [r[col] for r in rows if r[col].strip()]
        if not values:
            continue
        # Try parsing as numbers
        num_count = 0
        for v in values[:50]:
            try:
                float(v)
                num_count += 1
            except ValueError:
                pass
        if num_count / max(len(values[:50]), 1) < 0.5:
            categorical.append(col)
        else:
            numeric.append(col)

    return headers, categorical, numeric


def split_features_labels(csv_path, target_col, drop_cols=None):
    """Split CSV into features and labels, return as base64.

    Automatically drops columns that are likely IDs or free text
    (unique values > 90% of rows) unless they're the target.
    """
    import io

    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        print("❌ CSV file is empty")
        sys.exit(1)

    headers = list(rows[0].keys())
    if target_col not in headers:
        print(f"❌ Target column '{target_col}' not found in CSV")
        print(f"   Available columns: {', '.join(headers)}")
        sys.exit(1)

    # Auto-detect columns to drop (IDs, free text, high-cardinality)
    auto_drop = set(drop_cols or [])
    for col in headers:
        if col == target_col:
            continue
        unique_vals = len(set(r[col] for r in rows if r[col].strip()))
        # Drop if >50% unique (likely ID/ticket column) or column name suggests ID
        if unique_vals > len(rows) * 0.5 or col.lower().endswith("id"):
            auto_drop.add(col)
        # Drop if any value has a comma and isn't numeric (free text like names)
        has_commas = any("," in r[col] for r in rows[:50])
        if has_commas:
            auto_drop.add(col)
        # Drop if >50% empty
        empty_count = sum(1 for r in rows if not r[col].strip())
        if empty_count > len(rows) * 0.5:
            auto_drop.add(col)

    if auto_drop:
        print(f"  🗑️  Auto-dropping: {sorted(auto_drop)} (IDs/free-text)")

    feature_cols = [h for h in headers if h != target_col and h not in auto_drop]

    # Use csv module for proper quoting
    buf_x = io.StringIO()
    writer_x = csv.DictWriter(buf_x, fieldnames=feature_cols)
    writer_x.writeheader()
    for r in rows:
        writer_x.writerow({c: r[c] for c in feature_cols})
    x_b64 = base64.b64encode(buf_x.getvalue().encode()).decode()

    buf_y = io.StringIO()
    writer_y = csv.DictWriter(buf_y, fieldnames=[target_col])
    writer_y.writeheader()
    for r in rows:
        writer_y.writerow({target_col: r[target_col]})
    y_b64 = base64.b64encode(buf_y.getvalue().encode()).decode()

    return x_b64, y_b64, feature_cols


def wait_job(job_id, label="Job", timeout=300):
    """Poll a VecML job until it finishes."""
    print(f"   ⏳ Waiting for {label}...", end="", flush=True)
    for i in range(timeout // 3):
        r = post("get_automl_training_status", {"user_api_key": KEY, "job_id": job_id})
        status = r.get("status", "")
        if status == "finished":
            duration = r.get("duration", "")
            print(f" done! ({duration})")
            return r
        if "error" in str(r).lower() and "exception" in str(r).lower():
            print(f" error!")
            return r
        print(".", end="", flush=True)
        time.sleep(3)
    print(" timeout!")
    return {"error": "timeout"}


def cmd_train(args):
    """Train a model on a CSV file."""
    csv_path = args.file
    target = args.target
    project = args.project or DEFAULT_PROJECT
    collection = args.collection or os.path.splitext(os.path.basename(csv_path))[0] + f"_{int(time.time())}"
    model_name = args.model or f"model_{collection}"
    task = args.task
    mode = args.mode

    if not KEY:
        print("❌ Set VECML_API_KEY environment variable first")
        sys.exit(1)

    print(f"\n{'━' * 50}")
    print(f"  🧠 VecML AutoML Training Pipeline")
    print(f"{'━' * 50}")
    print(f"  📄 File:       {csv_path}")
    print(f"  🎯 Target:     {target}")
    print(f"  📁 Project:    {project}")
    print(f"  📦 Collection: {collection}")
    print(f"  🤖 Model:      {model_name}")
    print(f"  📊 Task:       {task}")
    print(f"  ⚡ Mode:       {mode}")
    print(f"{'━' * 50}\n")

    # Auto-detect columns
    headers, categorical, numeric = detect_columns(csv_path)
    # Remove target from categorical if present
    categorical = [c for c in categorical if c != target]
    print(f"  📋 Columns detected: {len(headers)}")
    print(f"     Categorical: {categorical or '(none)'}")
    print(f"     Numeric: {[c for c in numeric if c != target] or '(none)'}")
    print()

    # Split features and labels
    x_b64, y_b64, feature_cols = split_features_labels(csv_path, target)
    print(f"  ✂️  Split: {len(feature_cols)} features + 1 target ({target})")

    # Step 1: Create project
    print(f"\n  [1/6] Creating project '{project}'...")
    r = post("create_project", {
        "user_api_key": KEY,
        "project_name": project,
        "application": "autoML"
    })
    if r.get("success"):
        print(f"   ✅ Project created")
    else:
        msg = str(r)
        if "exist" in msg.lower():
            print(f"   ✅ Project already exists")
        else:
            print(f"   ⚠️  {msg}")

    # Step 2: Upload features
    print(f"\n  [2/6] Uploading features...")
    r = post("upload_automl_X", {
        "user_api_key": KEY,
        "project_name": project,
        "collection_name": collection,
        "X": x_b64,
        "file_format": "csv",
        "has_field_names": True,
        "vector_type": "dense",
        "categorical_features": categorical
    })
    if r.get("success"):
        print(f"   ✅ Features uploaded")
        print(f"   ⏳ Waiting for processing...", end="", flush=True)
        time.sleep(30)
        print(" done!")
    else:
        print(f"   ❌ Upload failed: {r}")
        sys.exit(1)

    # Step 3: Attach labels
    print(f"\n  [3/6] Attaching labels ({target})...")
    r = post("attach_automl_label", {
        "user_api_key": KEY,
        "project_name": project,
        "collection_name": collection,
        "file_data": y_b64,
        "file_format": "csv",
        "has_field_names": True,
        "attribute_name": target
    })
    if r.get("success"):
        print(f"   ✅ Labels attached")
        print(f"   ⏳ Waiting for processing...", end="", flush=True)
        time.sleep(30)
        print(" done!")
    else:
        print(f"   ❌ Label attachment failed: {r}")
        sys.exit(1)

    # Step 4: Train
    print(f"\n  [4/6] Training model ({mode} / {task})...")
    r = post("train_automl_model", {
        "user_api_key": KEY,
        "project_name": project,
        "collection_name": collection,
        "model_name": model_name,
        "training_mode": mode,
        "task_type": task,
        "label_attribute": target,
        "train_categorical_features": categorical
    })
    if r.get("success"):
        job_id = r.get("job_id", "")
        print(f"   ✅ Training started")
        if job_id:
            result = wait_job(job_id, "training", timeout=600)
            metrics = result.get("validation_metric", {})
    else:
        print(f"   ❌ Training failed: {r}")
        sys.exit(1)

    # Step 5: Validation metrics
    print(f"\n  [5/6] Fetching validation metrics...")
    r = post("get_model_validation_metric", {
        "user_api_key": KEY,
        "project_name": project,
        "collection_name": collection,
        "model_name": model_name
    })
    metrics = r.get("validation_metric", {})
    if metrics:
        print(f"   ┌─────────────────────────────────┐")
        for k, v in sorted(metrics.items()):
            bar = "█" * int(float(v) * 20) if isinstance(v, (int, float)) else ""
            print(f"   │ {k:20s} {v:>8.4f}  {bar}")
        print(f"   └─────────────────────────────────┘")
    else:
        print(f"   ⚠️  No metrics available: {r}")

    # Step 6: Feature importance
    print(f"\n  [6/6] Fetching feature importance...")
    r = post("get_feature_importance", {
        "user_api_key": KEY,
        "project_name": project,
        "collection_name": collection,
        "model_name": model_name
    })
    fi = r.get("feature_importance", [])
    if fi:
        fi_sorted = sorted(fi, key=lambda x: x.get("importance", 0), reverse=True)
        print(f"   ┌─────────────────────────────────────┐")
        for i, item in enumerate(fi_sorted):
            name = item.get("feature", "?")
            imp = item.get("importance", 0)
            bar = "█" * int(imp * 20)
            medal = ["🥇", "🥈", "🥉"][i] if i < 3 else "  "
            print(f"   │ {medal} {name:18s} {imp:>6.4f}  {bar}")
        print(f"   └─────────────────────────────────────┘")
    else:
        print(f"   ⚠️  No feature importance: {r}")

    # Summary
    print(f"\n{'━' * 50}")
    print(f"  ✅ DONE!")
    print(f"  Model:      {model_name}")
    print(f"  Project:    {project}")
    print(f"  Collection: {collection}")
    if metrics.get("accuracy"):
        print(f"  Accuracy:   {metrics['accuracy']:.2%}")
    if metrics.get("auc"):
        print(f"  AUC:        {metrics['auc']:.2%}")
    print(f"\n  To predict: python3 {sys.argv[0]} predict new_data.csv --model {model_name} --collection {collection}")
    print(f"{'━' * 50}\n")


def cmd_predict(args):
    """Run predictions on a CSV file."""
    csv_path = args.file
    project = args.project or DEFAULT_PROJECT
    collection = args.collection
    model_name = args.model

    if not collection or not model_name:
        print("❌ --collection and --model are required for prediction")
        sys.exit(1)

    print(f"\n  🔮 Predicting with {model_name}...")
    test_b64 = b64_file(csv_path)
    r = post("automl_predict", {
        "user_api_key": KEY,
        "project_name": project,
        "collection_name": collection,
        "model_name": model_name,
        "file_data": test_b64,
        "file_format": "csv",
        "has_field_names": True
    })

    if r.get("success"):
        preds = r.get("predictions", [])
        print(f"  ✅ Got {len(preds)} predictions")
        print(f"  Results: {preds[:20]}")
        if len(preds) > 20:
            print(f"  ... and {len(preds) - 20} more")

        # Save predictions
        out_path = csv_path.replace(".csv", "_predictions.csv")
        with open(out_path, "w") as f:
            f.write("prediction\n")
            for p in preds:
                f.write(f"{p}\n")
        print(f"  📄 Saved to: {out_path}")
    else:
        print(f"  ❌ Prediction failed: {r}")


def cmd_models(args):
    """List all models."""
    project = args.project or DEFAULT_PROJECT
    collection = args.collection

    if not collection:
        print("❌ --collection is required")
        sys.exit(1)

    r = post("list_automl_model_infos", {
        "user_api_key": KEY,
        "project_name": project,
        "collection_name": collection
    })

    models = r.get("model_infos", [])
    if models:
        print(f"\n  Models in {project}/{collection}:")
        for m in models:
            print(f"  • {m['model_name']} ({m.get('task_type','?')}, {m.get('training_mode','?')}) — {m.get('create_time','?')}")
    else:
        print(f"  No models found in {project}/{collection}")


def cmd_importance(args):
    """Show feature importance."""
    project = args.project or DEFAULT_PROJECT
    collection = args.collection
    model_name = args.model

    if not collection or not model_name:
        print("❌ --collection and --model are required")
        sys.exit(1)

    r = post("get_feature_importance", {
        "user_api_key": KEY,
        "project_name": project,
        "collection_name": collection,
        "model_name": model_name
    })

    fi = r.get("feature_importance", [])
    if fi:
        fi_sorted = sorted(fi, key=lambda x: x.get("importance", 0), reverse=True)
        print(f"\n  Feature importance for {model_name}:")
        for i, item in enumerate(fi_sorted):
            name = item["feature"]
            imp = item["importance"]
            bar = "█" * int(imp * 30)
            print(f"  {i+1:2d}. {name:20s} {imp:.4f}  {bar}")
    else:
        print(f"  No feature importance available: {r}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="VecML AutoML Pipeline")
    sub = parser.add_subparsers(dest="command")

    # Train
    p_train = sub.add_parser("train", help="Train a model on a CSV file")
    p_train.add_argument("file", help="Path to CSV file")
    p_train.add_argument("--target", "-t", required=True, help="Target column name")
    p_train.add_argument("--project", "-p", default=None, help="Project name")
    p_train.add_argument("--collection", "-c", default=None, help="Collection name")
    p_train.add_argument("--model", "-m", default=None, help="Model name")
    p_train.add_argument("--task", default="classification", choices=["classification", "regression"])
    p_train.add_argument("--mode", default="balanced", choices=["high_speed", "balanced", "high_accuracy"])

    # Predict
    p_pred = sub.add_parser("predict", help="Predict with a trained model")
    p_pred.add_argument("file", help="Path to CSV file")
    p_pred.add_argument("--model", "-m", required=True, help="Model name")
    p_pred.add_argument("--collection", "-c", required=True, help="Collection name")
    p_pred.add_argument("--project", "-p", default=None, help="Project name")

    # Models
    p_models = sub.add_parser("models", help="List trained models")
    p_models.add_argument("--collection", "-c", required=True, help="Collection name")
    p_models.add_argument("--project", "-p", default=None, help="Project name")

    # Importance
    p_imp = sub.add_parser("importance", help="Show feature importance")
    p_imp.add_argument("--model", "-m", required=True, help="Model name")
    p_imp.add_argument("--collection", "-c", required=True, help="Collection name")
    p_imp.add_argument("--project", "-p", default=None, help="Project name")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    if not KEY:
        print("❌ Set VECML_API_KEY environment variable:")
        print("   export VECML_API_KEY='vml_your_key_here'")
        sys.exit(1)

    {"train": cmd_train, "predict": cmd_predict, "models": cmd_models, "importance": cmd_importance}[args.command](args)

#!/usr/bin/env python3
"""Minimal SageMaker training script for smoke testing the skill.

This script does no real ML — it verifies the SageMaker contract works:
  - Reads hyperparameters from CLI args
  - Writes a dummy model to SM_MODEL_DIR
  - Prints metrics to stdout

Usage (local test):
    python3 test_train.py --epochs 1

On SageMaker, SM_MODEL_DIR is set automatically.
"""

import argparse
import json
import os
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=1)
    parser.add_argument("--model-dir", type=str,
                        default=os.environ.get("SM_MODEL_DIR", "/opt/ml/model"))
    args = parser.parse_args()

    print(f"[test] Python: {sys.version}")
    print(f"[test] Epochs: {args.epochs}")
    print(f"[test] Model dir: {args.model_dir}")

    # Simulate training
    metrics = {"test_loss": 0.42, "test_accuracy": 0.95}
    for epoch in range(1, args.epochs + 1):
        print(f"[test] Epoch {epoch}/{args.epochs} — loss={metrics['test_loss']:.4f}")

    # Save dummy model
    os.makedirs(args.model_dir, exist_ok=True)
    model_path = os.path.join(args.model_dir, "model.json")
    with open(model_path, "w") as f:
        json.dump({"type": "smoke-test", "epochs": args.epochs, "metrics": metrics}, f)
    print(f"[test] Model saved to {model_path}")

    # Print metrics in parseable format
    print(f"test_loss={metrics['test_loss']:.4f};")
    print(f"test_accuracy={metrics['test_accuracy']:.4f};")
    print("[test] Training complete.")


if __name__ == "__main__":
    main()

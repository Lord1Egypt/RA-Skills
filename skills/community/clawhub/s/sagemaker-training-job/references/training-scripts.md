# SageMaker Training Script Guide

## Training Script Contract

SageMaker invokes your training script as a standalone Python process. The script must
follow these conventions to work with SageMaker's infrastructure.

## Environment Variables (set by SageMaker)

```python
import os

# Where to read input data (per-channel directories)
train_dir = os.environ.get("SM_CHANNEL_TRAIN", "/opt/ml/input/data/train")
val_dir = os.environ.get("SM_CHANNEL_VALIDATION", "/opt/ml/input/data/validation")

# Where to write model artifacts (saved after training completes)
model_dir = os.environ.get("SM_MODEL_DIR", "/opt/ml/model")

# Where to write any output data (not model weights)
output_dir = os.environ.get("SM_OUTPUT_DATA_DIR", "/opt/ml/output/data")

# Number of GPUs on this instance
num_gpus = int(os.environ.get("SM_NUM_GPUS", 0))

# Hyperparameters (also accessible via argparse)
# SageMaker passes hyperparameters as command-line arguments
```

## Minimal Training Script Template

```python
#!/usr/bin/env python3
"""SageMaker training script template."""

import argparse
import json
import os
from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser()

    # Hyperparameters (passed by SageMaker from --hyperparameters)
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--lr", type=float, default=0.001)
    parser.add_argument("--batch-size", type=int, default=32)

    # SageMaker environment (auto-populated)
    parser.add_argument("--model-dir", type=str, default=os.environ.get("SM_MODEL_DIR", "/opt/ml/model"))
    parser.add_argument("--train", type=str, default=os.environ.get("SM_CHANNEL_TRAIN", "/opt/ml/input/data/train"))
    parser.add_argument("--output-data-dir", type=str, default=os.environ.get("SM_OUTPUT_DATA_DIR", "/opt/ml/output/data"))

    return parser.parse_args()


def main():
    args = parse_args()

    # 1. Load data
    print(f"Loading data from {args.train} ...")
    # train_df = pd.read_parquet(f"{args.train}/train.parquet")

    # 2. Train model
    print(f"Training for {args.epochs} epochs, lr={args.lr} ...")
    # model = train(...)

    # 3. Evaluate
    # metrics = evaluate(model, val_data)

    # 4. Save model to SM_MODEL_DIR (SageMaker packages this into model.tar.gz)
    print(f"Saving model to {args.model_dir} ...")
    # torch.save(model.state_dict(), f"{args.model_dir}/model.pth")
    # or: joblib.dump(model, f"{args.model_dir}/model.joblib")

    # 5. (Optional) Save additional outputs
    # pd.DataFrame(metrics).to_csv(f"{args.output_data_dir}/metrics.csv")

    print("Training complete.")


if __name__ == "__main__":
    main()
```

## PyTorch Example

```python
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

def train_pytorch(args):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Load data
    import pandas as pd
    df = pd.read_parquet(f"{args.train}/train.parquet")
    X = torch.tensor(df.drop("target", axis=1).values, dtype=torch.float32)
    y = torch.tensor(df["target"].values, dtype=torch.float32)

    dataset = TensorDataset(X, y)
    loader = DataLoader(dataset, batch_size=args.batch_size, shuffle=True)

    # Model
    model = nn.Sequential(
        nn.Linear(X.shape[1], 256), nn.ReLU(), nn.Dropout(0.3),
        nn.Linear(256, 128), nn.ReLU(), nn.Dropout(0.2),
        nn.Linear(128, 1)
    ).to(device)

    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)
    criterion = nn.MSELoss()

    # Train
    for epoch in range(args.epochs):
        model.train()
        total_loss = 0
        for X_batch, y_batch in loader:
            X_batch, y_batch = X_batch.to(device), y_batch.to(device)
            optimizer.zero_grad()
            pred = model(X_batch).squeeze()
            loss = criterion(pred, y_batch)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        print(f"Epoch {epoch+1}/{args.epochs} — Loss: {total_loss/len(loader):.6f}")

    # Save
    torch.save(model.state_dict(), f"{args.model_dir}/model.pth")
```

## LightGBM Example

```python
import lightgbm as lgb
import joblib

def train_lgbm(args):
    import pandas as pd
    df = pd.read_parquet(f"{args.train}/train.parquet")
    X = df.drop("target", axis=1)
    y = df["target"]

    train_data = lgb.Dataset(X, label=y)

    params = {
        "objective": "regression",
        "metric": "rmse",
        "learning_rate": args.lr,
        "num_leaves": 31,
        "verbose": -1,
    }

    model = lgb.train(params, train_data, num_boost_round=args.epochs)

    # Save
    model.save_model(f"{args.model_dir}/model.lgb")
    # Also save as joblib for sklearn compatibility
    joblib.dump(model, f"{args.model_dir}/model.joblib")
```

## Logging Metrics

SageMaker can parse metrics from stdout using regex. Define metric definitions
when creating the training job, or simply print them in a parseable format:

```python
# SageMaker will capture these if metric definitions are configured
print(f"train_loss={loss:.6f};")
print(f"val_rmse={rmse:.6f};")
```

## Requirements File

If your training script needs additional packages beyond what the SageMaker container provides,
create a `requirements.txt` in your source directory:

```
lightgbm>=4.0
optuna>=3.0
shap>=0.40
```

SageMaker automatically installs these before running your script.

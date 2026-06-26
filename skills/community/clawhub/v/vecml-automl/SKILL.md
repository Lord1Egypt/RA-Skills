---
name: vecml-automl
description: >
  VecML AutoML — Drop a CSV, train an ML model, get predictions. One command.
  Use when the user asks to: train a model, upload data, run predictions, classify,
  do regression, check model accuracy, get feature importance, or anything with ML.
  Triggers on: "train", "predict", "classify", "ML", "machine learning", "model",
  "feature importance", "upload dataset", "data pipeline", "CSV", "accuracy".
metadata:
  clawdbot:
    emoji: "🧠"
    requires:
      commands: ["python3"]
      env: ["VECML_API_KEY"]
    homepage: "https://aidb.vecml.com/docs/site/automl_api/"
---

# VecML AutoML — One-Command ML Pipeline

Train a model from any CSV in one command. No setup, no notebooks, no boilerplate.

## Setup (one time)

```bash
export VECML_API_KEY="vml_your_key_here"
```

## Train a Model

Just point it at a CSV and tell it which column to predict:

```bash
python3 ~/.openclaw/workspace/skills/vecml-automl/vecml-pipeline.py train data.csv --target Survived
```

That's it. It will:
1. Auto-detect categorical vs numeric columns
2. Split features and labels
3. Create the project on VecML
4. Upload the data (base64 encoded)
5. Wait for labels to attach (avoids the async race bug)
6. Train the model
7. Show validation metrics (accuracy, AUC, F1, precision, recall)
8. Show feature importance with visual bars

### Options

```bash
python3 vecml-pipeline.py train data.csv \
  --target target_column \
  --task classification          # or regression
  --mode balanced                # high_speed | balanced | high_accuracy
  --project my_project           # default: openclaw_automl
  --collection my_dataset        # default: auto-generated from filename
  --model my_model_v1            # default: auto-generated
```

## Run Predictions

```bash
python3 vecml-pipeline.py predict new_data.csv --model my_model --collection my_dataset
```

Saves results to `new_data_predictions.csv` automatically.

## List Models

```bash
python3 vecml-pipeline.py models --collection my_dataset
```

## Feature Importance

```bash
python3 vecml-pipeline.py importance --model my_model --collection my_dataset
```

## Example Output

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🧠 VecML AutoML Training Pipeline
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  📄 File:       titanic.csv
  🎯 Target:     Survived
  📊 Task:       classification
  ⚡ Mode:       balanced

  [1/6] Creating project...         ✅
  [2/6] Uploading features...       ✅ done! (1.2s)
  [3/6] Attaching labels...         ✅ done! (0.8s)
  [4/6] Training model...           ✅ done! (3.5s)
  [5/6] Validation metrics:
   │ accuracy               0.8101  ████████████████
   │ auc                    0.8798  █████████████████
   │ macro_f1               0.7947  ███████████████
  [6/6] Feature importance:
   │ 🥇 Fare                0.7294  ██████████████
   │ 🥈 Age                 0.6019  ████████████
   │ 🥉 Sex                 0.2732  █████

  ✅ DONE! Accuracy: 81.01%  AUC: 87.98%
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## For OpenClaw Agent Usage

When a user sends a CSV file or asks to train a model, run:

```bash
export VECML_API_KEY="vml_your_key_here"
python3 ~/.openclaw/workspace/skills/vecml-automl/vecml-pipeline.py train /path/to/their/file.csv --target their_target_column
```

If the user doesn't specify a target column, read the CSV headers first and ask which column they want to predict:

```bash
head -1 /path/to/file.csv
```

Then run the pipeline with their chosen target.

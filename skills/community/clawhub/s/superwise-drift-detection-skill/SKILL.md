---
name: superwise-drift-detection-skill
description: >
  Detects feature drift in tabular ML models using Superwise Compare Distribution
  policies (Jensen-Shannon divergence for categorical columns). Handles everything:
  Superwise dataset creation, training data upload, drift policy setup, inference
  ingestion, and Telegram alerts via OpenClaw's existing Telegram connection.
  Use when: user says "set up drift detection", "detect model drift", "monitor my
  model for drift", "check if my model is drifting", or "add drift detection to
  my model".
---

# Superwise Drift Detection Skill

When the user wants to set up drift detection for their model, guide them through
the steps below in order. Complete each step before moving to the next.

## What You Need From the User

Ask the user to provide the following before starting:

1. **Superwise credentials** — `SUPERWISE_CLIENT_ID` and `SUPERWISE_SECRET_TOKEN`
   (found in their Superwise account under Settings → API Keys)
2. **Training CSV** — the CSV file their model was trained on (feature columns only;
   a `row_id` column will be added automatically)
3. **Model name** — a short label with no spaces (e.g. `my_churn_model`); used to
   name datasets in Superwise
4. **Inference endpoint** — one of two options:
   - **Option A**: They already have a running model endpoint. Ask for the URL.
     It must return JSON shaped as `{"records": [{...}, ...]}` where each record
     contains the same columns as the training CSV.
   - **Option B**: They need to deploy one. Use the dc-bikeshare example in
     `examples/dc-bikeshare-drift/app.py` as a template. Guide them to adapt
     `predict.py` for their model, then run `python app.py` locally. Set
     `INFERENCE_ENDPOINT_URL=http://localhost:5001/predict` for local testing.

## Step 1 — Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file in the skill root directory with the following contents,
filling in the values the user provided:

```
SUPERWISE_CLIENT_ID=<from user>
SUPERWISE_SECRET_TOKEN=<from user>
MODEL_NAME=<model name>
INFERENCE_ENDPOINT_URL=<from user's answer to question 4>
SUPERWISE_AUTO_TRIGGER=true
SUPERWISE_TRAINING_DATASET_ID=
SUPERWISE_TRAINING_DATASET_NAME=
SUPERWISE_TRAINING_CUBE_NAME=
SUPERWISE_INFERENCE_DATASET_ID=
SUPERWISE_INFERENCE_DATASET_NAME=
SUPERWISE_INFERENCE_CUBE_NAME=
SUPERWISE_DRIFT_POLICY_ID=
# Additional per-column policies — add one line per column printed by setup_drift_policy.py:
# SUPERWISE_DRIFT_POLICY_ID_<column>=<policy ID>
SCHEDULE_HOUR_UTC=6
SCHEDULE_MINUTE_UTC=0
PORT=5000
```

The dataset and policy ID fields will be filled in after Steps 2 and 3.

## Step 2 — Create Superwise datasets and upload training data

```bash
python setup_dataset.py \
    --training-csv path/to/training.csv \
    --model-name their_model_name
```

This creates a training dataset and an inference dataset in Superwise, uploads
the training CSV row by row, and prints the dataset IDs and cube names.

Copy the printed values into `.env`:
```
SUPERWISE_TRAINING_DATASET_ID=<printed value>
SUPERWISE_TRAINING_DATASET_NAME=<printed value>
SUPERWISE_TRAINING_CUBE_NAME=<printed value>
SUPERWISE_INFERENCE_DATASET_ID=<printed value>
SUPERWISE_INFERENCE_DATASET_NAME=<printed value>
SUPERWISE_INFERENCE_CUBE_NAME=<printed value>
```

Note: training CSV column names must use only letters, numbers, and underscores,
and must start with a letter. Warn the user if any column names violate this.

## Step 3 — Create drift policies

```bash
python setup_drift_policy.py \
    --training-csv path/to/training.csv \
    --policy-name their_model_drift
```

This creates one Jensen-Shannon divergence policy per categorical (string/boolean)
column in the training CSV, comparing the training dataset against the inference
dataset. Numeric columns are skipped with a warning — this is a known Superwise
platform limitation (wasserstein distance for numeric columns is not yet supported).

Copy the primary printed policy ID into `.env`:
```
SUPERWISE_DRIFT_POLICY_ID=<primary policy ID>
SUPERWISE_DRIFT_POLICY_ID_<column2>=<policy ID>
SUPERWISE_DRIFT_POLICY_ID_<column3>=<policy ID>
# ... one line per additional column policy printed by setup_drift_policy.py
```

Copy all printed policy lines (not just the first) — `_check_drift()` will trigger
and check every `SUPERWISE_DRIFT_POLICY_ID*` env var automatically.

If the user wants to monitor only specific columns, add `--columns col1 col2 col3`.

## Step 4 — Run an end-to-end drift check

```bash
python -c "
import os; os.chdir('.')
from dotenv import load_dotenv; load_dotenv()
from skill import run
result = run()
print(result)
"
```

This will:
1. Fetch inference records from `INFERENCE_ENDPOINT_URL`
2. Ingest them into the Superwise inference dataset
3. Trigger all configured drift policy evaluations
4. Poll until each evaluation completes
5. Send an alert via OpenClaw's Telegram connection if drift is detected
6. Print a summary

**Note:** The full check can take 5-10 minutes (inference fetch + ingest + policy
polling across all columns). Run it in a background or PTY session to avoid exec
timeouts:
```bash
nohup python -c "..." &> drift_check.log &
```

## Step 5 — Schedule recurring drift checks

Register the skill with OpenClaw using the metadata in `skill.py`:
- **Trigger command:** `/drift_check`
- **Schedule:** `0 6 * * *` (06:00 UTC daily — adjust to the user's inference cadence)
- **Alerts:** routed through OpenClaw's existing Telegram connection

For a production deployment, guide the user to deploy `scheduler.py` to Render
using the included `render.yaml`. Set all `.env` values as Render environment
variables.

## Telegram Alerts

This skill uses OpenClaw's existing Telegram connection — no separate bot setup
needed. The `_send_telegram()` function in `skill.py` uses `TELEGRAM_BOT_TOKEN`
and `TELEGRAM_CHAT_ID` from the user's OpenClaw environment. If the user does
not have Telegram set up in OpenClaw yet, point them to OpenClaw's Telegram
setup docs.

Drift alerts look like:
- **Unhealthy:** lists features with high drift (score > 0.2), flags that
  predictions may be unreliable
- **Healthy:** confirms no significant drift with per-feature scores

## Reference Example: DC Bikeshare

`examples/dc-bikeshare-drift/` is a complete working example the user can run
to verify the skill end-to-end before connecting their own model:

```bash
cd examples/dc-bikeshare-drift
pip install -r requirements.txt
python collect_training_data.py   # fetch real station data, generate synthetic history
python train.py                   # train RandomForest classifier
python app.py                     # start local Flask inference server on port 5001
```

Then run the drift check from the skill root with:
```
INFERENCE_ENDPOINT_URL=http://localhost:5001/predict
```

This example uses only categorical features (station size, e-bike presence,
hour of day, day type, season) to predict bike availability — all suitable for
JSD drift detection.

## Retraining

When the user retrains their model:

```bash
python setup_dataset.py \
    --training-csv path/to/new_training.csv \
    --model-name their_model_name \
    --retrain
```

This creates a versioned replacement training dataset and preserves the inference
history. Update `.env` with the new training dataset ID and cube name, then re-run
`setup_drift_policy.py` to create a new policy pointing at the updated baseline.

## Troubleshooting

- **Policy stays `pending` forever:** Check that inference records were successfully
  ingested before triggering. The inference dataset must have data for the policy
  to evaluate.
- **`unhealthy` on first run:** Expected if inference records are a single time-slice
  snapshot (all same hour/day/season). Accumulate inference records over time for
  a more representative distribution.
- **Numeric columns skipped:** Wasserstein distance for numeric dimensions is a
  known Superwise platform bug. Use categorical bucketing as a workaround, or
  wait for the Superwise platform fix.
- **CubeJS cube not found after upload:** New datasets take a few minutes to
  register in Superwise's CubeJS layer. Wait 2–3 minutes and retry verification.
- **Drift check killed / no output (SIGTERM):** The full check takes 5-10 minutes and will
  be killed by any exec timeout in your environment. Run it in a background session:
  `nohup python -c "from skill import run; run()" &> drift_check.log &`
  Then `tail -f drift_check.log` to follow progress.

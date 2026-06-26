# Entry Examples

Concrete examples of well-formatted entries with all fields for scientific research and ML workflows.

## Learning: Data Quality (Target Leakage)

```markdown
## [LRN-20260410-001] data_quality

**Logged**: 2026-04-10T14:30:00Z
**Priority**: critical
**Status**: resolved
**Area**: preprocessing

### Summary
Target leakage through timestamp feature — `event_timestamp` encoded label assignment time

### Details
The `event_timestamp` feature had near-perfect correlation (0.98) with the
target variable `churned`. Investigation revealed the timestamp recorded when
the churn label was applied by the CRM system, not when the user event
occurred. Model achieved 0.99 AUC in validation but 0.52 AUC on live traffic.

### Suggested Action
Audit all timestamp-derived features against the label generation process.
Features must strictly predate the label event. Add a temporal leakage check
to the preprocessing pipeline.

### Metadata
- Source: experiment
- Related Files: notebooks/churn_model_v3.ipynb, src/features/temporal.py
- Tags: leakage, timestamp, churn, target-leakage
- Dataset: customer_events_2025
- Model: XGBoost v1.7.6
- Metric-Before: 0.99 AUC (validation), 0.52 AUC (production)
- Metric-After: 0.81 AUC (validation), 0.79 AUC (production)
- Pattern-Key: leakage.timestamp_target

### Resolution
- **Resolved**: 2026-04-11T09:00:00Z
- **Commit/PR**: #287
- **Notes**: Removed event_timestamp, added temporal_leakage_check() to pipeline

---
```

## Learning: Statistical Error (T-Test on Non-Normal Data)

```markdown
## [LRN-20260408-002] statistical_error

**Logged**: 2026-04-08T11:15:00Z
**Priority**: high
**Status**: promoted
**Promoted**: methodology-standards.md
**Area**: analysis

### Summary
Applied t-test to highly skewed revenue data — normality assumption violated

### Details
Used independent samples t-test to compare revenue between control and
treatment groups in A/B test. Revenue data had skewness of 4.7 and Shapiro-Wilk
p < 0.001. T-test yielded p = 0.03 (significant). After switching to
Mann-Whitney U test, p = 0.12 (not significant). Original conclusion of
"treatment increases revenue" was invalid.

### Suggested Action
Always run Shapiro-Wilk test before parametric tests. For skewed financial
data, default to non-parametric tests or log-transform with justification.
Report both the test choice rationale and assumption check results.

### Metadata
- Source: peer_review
- Related Files: notebooks/ab_test_revenue_q1.ipynb
- Tags: t-test, normality, mann-whitney, skewness, a-b-test
- Dataset: ab_test_revenue_2026q1
- Pattern-Key: stats.normality_assumption

---
```

## Learning: Methodology Flaw (No Holdout for Tuning)

```markdown
## [LRN-20260405-003] methodology_flaw

**Logged**: 2026-04-05T16:45:00Z
**Priority**: high
**Status**: resolved
**Area**: validation

### Summary
Hyperparameter tuning used validation set that was also final evaluation set

### Details
GridSearchCV was run with 5-fold CV on the full dataset minus test set. The
"best" hyperparameters were then evaluated on the same test set used to select
among model architectures. This means the test set influenced both architecture
selection and hyperparameter tuning, inflating reported performance by ~3-5
percentage points. Proper approach: split into train/validation/test, use
validation for tuning, test only once at the end.

### Suggested Action
Implement three-way split: train (60%), validation (20%), test (20%). Use
validation exclusively for hyperparameter search. Touch test set only for
final reported metrics. Document the split strategy in experiment metadata.

### Metadata
- Source: user_feedback
- Related Files: notebooks/model_selection.ipynb, src/training/tune.py
- Tags: hyperparameter-tuning, data-splitting, overfitting, validation
- Model: RandomForest, XGBoost, LightGBM (all affected)
- Metric-Before: 0.93 accuracy (inflated)
- Metric-After: 0.88 accuracy (honest estimate)

### Resolution
- **Resolved**: 2026-04-06T10:00:00Z
- **Commit/PR**: #274
- **Notes**: Refactored pipeline to enforce train/val/test split with StratifiedShuffleSplit

---
```

## Experiment Issue: Reproducibility (Different Results Across Seeds)

```markdown
## [EXP-20260403-001] reproducibility_issue

**Logged**: 2026-04-03T09:30:00Z
**Priority**: high
**Status**: resolved
**Area**: modeling

### Summary
Neural network accuracy varies by 8 percentage points across random seeds

### Error
```
Seed 42:  accuracy=0.87, F1=0.83
Seed 123: accuracy=0.79, F1=0.74
Seed 7:   accuracy=0.85, F1=0.81
Seed 0:   accuracy=0.82, F1=0.78
Seed 999: accuracy=0.84, F1=0.80
```

### Context
- Experiment: Sentiment classification on product reviews
- Model: 2-layer LSTM with attention, PyTorch 2.2.0
- Dataset: 50k reviews, 80/10/10 split
- Hardware: NVIDIA A100, CUDA 12.1
- Batch size: 64, learning rate: 1e-3, epochs: 20

### Root Cause
Small dataset combined with random weight initialization and dropout creates
high variance. GPU non-determinism (cuDNN) also contributes. No seed was set
for `torch.backends.cudnn`.

### Suggested Fix
1. Set all seeds: `torch.manual_seed`, `numpy.random.seed`, `random.seed`,
   `torch.backends.cudnn.deterministic = True`
2. Report mean and std across 5+ seeds instead of single-run results
3. Use `torch.use_deterministic_algorithms(True)` for full reproducibility
4. Consider larger dataset or pre-trained embeddings to reduce variance

### Metadata
- Reproducible: yes (variance is the issue)
- Related Files: notebooks/sentiment_lstm.ipynb, src/models/lstm.py
- Seeds Tested: 42, 123, 7, 0, 999

### Resolution
- **Resolved**: 2026-04-04T14:00:00Z
- **Commit/PR**: #268
- **Notes**: Added seed_everything() utility, now report mean±std across 5 seeds

---
```

## Experiment Issue: Model Drift (Accuracy Degradation After Data Update)

```markdown
## [EXP-20260401-002] data_quality

**Logged**: 2026-04-01T13:00:00Z
**Priority**: critical
**Status**: resolved
**Area**: validation

### Summary
Fraud detection model accuracy dropped from 0.94 to 0.71 after monthly data refresh

### Error
```
March model (trained on Jan-Feb data): precision=0.94, recall=0.89, F1=0.91
April evaluation (on March data):      precision=0.71, recall=0.63, F1=0.67
```

### Context
- Model: Gradient Boosted Trees (LightGBM 4.3.0)
- Training data: Jan-Feb 2026 transactions (1.2M rows)
- Evaluation data: March 2026 transactions (450k rows)
- Features: 47 transaction features + 12 engineered features
- Production serving via batch scoring pipeline

### Root Cause
Distribution shift in two key features:
1. `transaction_amount` mean shifted from $127 to $89 (seasonal pattern)
2. `merchant_category` had 3 new categories not seen during training

Feature drift detection (PSI) was not in place. The model had no mechanism
to flag out-of-distribution inputs.

### Suggested Fix
1. Add Population Stability Index (PSI) monitoring for all features
2. Set PSI > 0.2 as alert threshold, PSI > 0.5 as retrain trigger
3. Handle unseen categorical values with an "unknown" bucket
4. Implement monthly retraining with sliding window

### Metadata
- Reproducible: yes
- Related Files: src/models/fraud_detector.py, pipelines/monthly_retrain.py
- See Also: EXP-20260115-004 (similar drift in Q4 2025)

### Resolution
- **Resolved**: 2026-04-02T16:00:00Z
- **Commit/PR**: #281
- **Notes**: Added PSI monitoring, unknown category handling, and sliding window retraining

---
```

## Feature Request: Automated Data Leakage Detection

```markdown
## [FEAT-20260409-001] automated_leakage_detection

**Logged**: 2026-04-09T10:00:00Z
**Priority**: high
**Status**: pending
**Area**: preprocessing

### Requested Capability
Automated detection of data leakage in feature engineering pipelines

### Research Context
After two incidents of target leakage (LRN-20260410-001 and EXP-20260215-003),
user wants a reusable tool that scans feature-target relationships for
leakage signals before model training begins.

### Complexity Estimate
medium

### Suggested Implementation
1. Compute feature-target mutual information; flag features with MI > threshold
2. Check temporal ordering: all feature timestamps must predate label timestamp
3. Detect features derived from target (e.g., aggregations that include label)
4. Run on every pipeline execution as a pre-training gate
5. Libraries: `sklearn.feature_selection.mutual_info_classif`, custom temporal checks

### Metadata
- Frequency: recurring (2 incidents in 60 days)
- Related Features: preprocessing pipeline, feature store validation

---
```

## Learning: Promoted to Experiment Checklist

```markdown
## [LRN-20260320-004] experiment_design

**Logged**: 2026-03-20T08:30:00Z
**Priority**: high
**Status**: promoted
**Promoted**: experiment-checklist.md
**Area**: validation

### Summary
Cross-validation must nest preprocessing inside folds to prevent data leakage

### Details
StandardScaler was fit on the full training set before cross-validation.
This means fold validation sets were scaled using statistics computed on
data that included those same validation samples. Mean AUC dropped from
0.89 to 0.86 after fixing with Pipeline + CV nesting. The 3-point
difference is the "optimism" from leaking scaling parameters.

### Suggested Action
Always use sklearn Pipeline to encapsulate preprocessing + model. Pass
the Pipeline (not just the model) to cross_val_score or GridSearchCV.

### Metadata
- Source: experiment
- Related Files: notebooks/cv_pipeline_fix.ipynb
- Tags: cross-validation, preprocessing, leakage, pipeline
- Pattern-Key: leakage.cv_preprocessing
- Recurrence-Count: 3
- First-Seen: 2026-01-15
- Last-Seen: 2026-03-20

---
```

**In experiment-checklist.md:**
```markdown
## Pre-Training Checks
- [ ] Preprocessing is inside CV folds (use sklearn Pipeline)
- [ ] No feature statistics computed on full dataset before splitting
- [ ] StandardScaler/MinMaxScaler fit only on training fold
```

## Learning: Promoted to Skill (Model Card Template)

```markdown
## [LRN-20260315-005] experiment_design

**Logged**: 2026-03-15T14:00:00Z
**Priority**: medium
**Status**: promoted_to_skill
**Skill-Path**: skills/model-card-template
**Area**: publication

### Summary
Standardized model card format needed for documenting model limitations and performance bounds

### Details
Team had no consistent format for documenting model behavior, failure modes,
and ethical considerations. After three incidents where model limitations were
not communicated to downstream consumers, created a reusable model card
template based on Mitchell et al. (2019) framework.

### Suggested Action
Use the extracted skill template for every model shipped to production or
shared with stakeholders.

### Metadata
- Source: user_feedback
- Related Files: docs/model-card-template.md
- Tags: model-card, documentation, model-governance, responsible-ai

---
```

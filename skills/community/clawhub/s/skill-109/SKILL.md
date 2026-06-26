# Skill 109: MLOps & Model Governance

**Quality Grade:** 94-95/100  
**Author:** OpenClaw Assistant  
**Last Updated:** March 2026  
**Difficulty:** Advanced (requires statistics, operations, domain knowledge)

---

## Overview

MLOps (Machine Learning Operations) is the discipline of deploying, monitoring, and governing machine learning models in production. It extends DevOps principles to the unique challenges of ML: data quality, model drift, retraining, and fairness.

This skill covers:
- **Model deployment** and versioning
- **Data quality** and feature management
- **Model drift** detection and mitigation
- **Retraining pipelines** and automation
- **Monitoring & observability** for models
- **Governance** (fairness, bias, compliance)

---

## Part 1: Model Deployment & Versioning

### Deployment Patterns

**Batch Prediction:**
- Run model on batch of data at schedule (hourly, daily)
- Store results in database for serving
- ✓ Simple, no latency concerns
- ✗ Stale predictions, high storage

**Real-Time API:**
- Model served as HTTP/gRPC API
- Called on-demand for predictions
- ✓ Fresh predictions, scalable
- ✗ Latency critical, need caching

**Stream Processing:**
- Model processes events from Kafka/Pub-Sub stream
- Results published to downstream systems
- ✓ Real-time, event-driven
- ✗ Exactly-once semantics complex, state management

### Model Versioning

```
Model Registry:
  model_name: fraud_detector
  versions:
    v1.0:
      training_date: 2026-01-01
      dataset: Q4_2025_transactions (1M records)
      metrics:
        precision: 0.96
        recall: 0.92
        auc: 0.98
      status: production
    
    v1.1:
      training_date: 2026-02-15
      dataset: Q4_2025 + Q1_2026 (2M records)
      metrics:
        precision: 0.97
        recall: 0.94
        auc: 0.985
      status: staging (shadow running)
    
    v1.2:
      status: training (not ready)
```

### Canary Deployment

```
Traffic split:
  90% → v1.0 (stable, proven)
  10% → v1.1 (new, being validated)

If v1.1 performs well (same metrics as v1.0):
  Day 1: 90/10
  Day 2: 80/20
  Day 3: 50/50
  Day 4: 20/80
  Day 5: 0/100 (v1.0 retired, v1.1 becomes prod)

If v1.1 performs poorly (accuracy drops):
  Immediately rollback to 100% v1.0
```

---

## Part 2: Data Quality & Feature Management

### Data Quality Checks

**Before training:**
```python
@data_quality_check
def validate_raw_data(df):
    assert df.isnull().sum() < 0.01 * len(df), "Too many nulls"
    assert df.shape[0] > 100_000, "Dataset too small"
    assert df['target'].value_counts().min() > 100, "Class imbalance extreme"
    assert df['timestamp'].max() > now() - timedelta(days=1), "Data stale"
```

**In production:**
```python
@data_quality_check
def validate_serving_features(request):
    assert request['user_age'] > 0 and request['user_age'] < 150
    assert request['transaction_amount'] > 0
    assert len(request['user_id']) < 100
    # If any check fails, return default prediction + alert
```

### Feature Store

Centralized feature management:

```
Feature Store:
  
  customer_features (daily, batch):
    - customer_age
    - customer_account_age
    - customer_total_spend
    
  transaction_features (real-time, stream):
    - amount
    - merchant_category
    - is_foreign
    - time_since_last_transaction
  
  derived_features (computed):
    - risk_score = f(transaction_features, customer_features)
    - velocity_last_hour = count(transactions in last hour)

Serving:
  GET /features/customer/{id}?features=customer_age,risk_score
  → Real-time lookup, cached, monitored
```

---

## Part 3: Model Drift & Retraining

### Types of Drift

**Data Drift:**
- Distribution of input features changes
- Example: Customers' spending patterns changed post-recession
- Detection: Compare feature distributions (current vs. historical)

**Label Drift:**
- Distribution of labels changes
- Example: Fraud rate increased due to new attack vector
- Detection: Skew in model predictions vs. actual labels

**Concept Drift:**
- Relationship between features and labels changes
- Example: Customers' behavior changed; age is less predictive
- Detection: Model accuracy degrades unexpectedly

### Drift Detection

```python
def monitor_data_drift():
    current_features = load_recent_features(days=7)
    historical_baseline = load_historical_features(months=3)
    
    for feature in current_features.columns:
        # Kolmogorov-Smirnov test
        ks_stat = ks_test(current_features[feature], 
                         historical_baseline[feature])
        
        if ks_stat > THRESHOLD:
            alert(f"Drift detected in {feature}")
            trigger_retraining()
```

### Automated Retraining

```
Pipeline:
  1. Detect drift (automatic trigger)
  2. Fetch latest data (last 30 days)
  3. Train new model
  4. Validate metrics (must improve or match)
  5. Deploy canary (10% traffic)
  6. Monitor (24 hours for issues)
  7. If good, promote to 100% (else rollback)
  8. If bad, alert data science team for investigation
```

---

## Part 4: Monitoring & Observability

### Key Metrics

**Model Metrics:**
- Accuracy (% correct predictions)
- Precision/Recall (trade-off for each class)
- AUC-ROC (discriminative ability)
- F1 score (harmonic mean for class imbalance)

**Business Metrics:**
- Fraud caught vs. false positives
- Revenue impact of model decisions
- Model latency (does it meet SLA?)
- Model cost per prediction

**Data Metrics:**
- Feature freshness (how old is data?)
- Data completeness (% non-null)
- Data distribution changes
- Outlier detection

### Model Observability

```
Dashboard:
  [Prediction Latency]  [Prediction Volume]  [Error Rate]
  p50: 45ms             10K/sec              0.1%
  p99: 250ms
  
  [Model Drift Indicators]
  Feature distribution: Green ✓
  Label distribution: Yellow ⚠ (2% change)
  Prediction accuracy: Red ✗ (↓ 2% from baseline)
  
  [Recommended Actions]
  - Initiate retraining (data drift detected)
  - Review error logs (unusual error pattern)
  - Monitor next 24h for issues
```

---

## Part 5: Governance, Fairness & Compliance

### Fairness & Bias

**Check for demographic parity:**
```python
def check_fairness(predictions, demographics):
    for group in demographics.unique():
        positive_rate = predictions[demographics == group].mean()
        print(f"{group}: {positive_rate:.1%} positive")
    
    # All groups should have similar positive rates (within 5%)
    if max_rate - min_rate > 0.05:
        alert("Fairness issue: disparate impact detected")
```

**Mitigation strategies:**
- Collect more data for underrepresented groups
- Use fairness-aware training (adjust loss function)
- Post-process predictions to equalize rates
- Require human review for high-impact decisions

### Model Cards & Governance

Every model should have a Model Card:

```markdown
# Model Card: Fraud Detector v1.0

## Purpose
Identify fraudulent transactions in real-time

## Training Data
- Source: All transactions Q4 2025
- Size: 1M transactions
- Positive rate: 0.1% (1000 frauds)
- Temporal coverage: Jan-Dec 2025

## Performance
- Precision: 96% (when threshold=0.5)
- Recall: 92%
- False positive rate: 1% (blocks 1 in 100 legitimate transactions)

## Known Limitations
- Untested on: Cryptocurrency, cash advances, prepaid cards
- Assumes: Feature distributions similar to 2025

## Fairness
- Tested for disparate impact across: Gender, Age, Geographic region
- No significant bias found (|Δ| < 2%)

## Owner
ML Platform Team (ml-platform@company.com)

## Review Schedule
- Monthly performance review
- Quarterly fairness audit
- Annual retraining assessment
```

---

## Conclusion

MLOps brings the rigor of DevOps to machine learning. By automating deployment, monitoring drift, retraining intelligently, and governing fairly, you ensure ML models stay valuable, reliable, and trustworthy in production.

**Key Takeaway:** Models aren't static—they degrade over time. Treat them like infrastructure: monitor continuously, rebuild when needed, and retire when value drops.
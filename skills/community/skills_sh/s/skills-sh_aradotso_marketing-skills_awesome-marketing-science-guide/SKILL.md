---
name: awesome-marketing-science-guide
description: Guide to curated marketing science resources including MMM, geo experiments, causal inference, attribution, and Bayesian methods
triggers:
  - "find marketing mix modeling libraries"
  - "how do I run geo experiments"
  - "show me causal inference tools for marketing"
  - "what are the best MMM packages"
  - "help with incrementality testing"
  - "recommend multi-touch attribution libraries"
  - "marketing science resources and tools"
  - "bayesian marketing measurement frameworks"
---

# Awesome Marketing Science Guide

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

This skill provides guidance on the **Awesome Marketing Science** resource collection — a curated list of open-source libraries, papers, and methodologies for marketing measurement, including Media Mix Models (MMM), geo incrementality testing, multi-touch attribution (MTA), causal inference, and Bayesian approaches.

## Overview

Awesome Marketing Science is a comprehensive resource hub covering:

- **Media Mix Modeling (MMM)**: Measure channel-level ROI and optimize budget allocation
- **Geo Experimentation**: Test incrementality through matched markets and geo lift
- **Attribution**: Multi-touch and algorithmic attribution models
- **Causal Inference**: Difference-in-differences, synthetic control, uplift modeling
- **A/B Testing & Experimentation**: Online controlled experiments and variance reduction
- **Ghost Ads & Platform Incrementality**: Measure true ad effectiveness

## Repository Structure

The collection is organized into:

1. **Start Here / Must Read**: Essential papers and packages for building measurement foundations
2. **Open Source Libraries**: Production-ready code organized by discipline
3. **Papers & Research**: Academic and industry research
4. **Blogs & Tutorials**: Practical implementation guides

## Key Libraries by Category

### Media Mix Modeling (MMM)

#### Robyn (Meta)
```r
# Install
install.packages("Robyn")
# Or from source
remotes::install_github("facebookexperimental/Robyn/R")

library(Robyn)

# Load data
data("dt_simulated_weekly")
data("dt_prophet_holidays")

# Set hyperparameters
hyperparameters <- list(
  adstock = c("geometric"),
  prophet_vars = c("trend", "season", "holiday"),
  prophet_country = "US"
)

# Run model
robyn_object <- robyn_run(
  dt_input = dt_simulated_weekly,
  dt_holidays = dt_prophet_holidays,
  hyperparameters = hyperparameters,
  cores = 4
)

# Get budget allocation
allocator <- robyn_allocator(
  robyn_object = robyn_object,
  scenario = "max_response_expected_spend"
)
```

#### LightweightMMM (Google)
```python
# Install
# pip install lightweight-mmm

from lightweight_mmm import lightweight_mmm
from lightweight_mmm import preprocessing
import jax.numpy as jnp

# Prepare data
media_data = jnp.array(media_data_raw)  # Shape: (n_time_periods, n_media_channels)
target = jnp.array(revenue_data)  # Shape: (n_time_periods,)

# Scale data
media_data_scaled, scaler = preprocessing.CustomScaler().fit_transform(media_data)

# Initialize and train model
mmm = lightweight_mmm.LightweightMMM()
mmm.fit(
    media=media_data_scaled,
    target=target,
    number_warmup=1000,
    number_samples=1000,
    media_prior=jnp.ones(n_channels)
)

# Get channel contributions
contribution = mmm.get_posterior_metrics()["contribution_per_channel"]
```

#### PyMC-Marketing
```python
# Install
# pip install pymc-marketing

import pymc as pm
from pymc_marketing.mmm import MMM

# Initialize model
mmm = MMM(
    date_column="date",
    channel_columns=["tv", "radio", "digital"],
    adstock_max_lag=8,
    validate_data=True
)

# Fit model
mmm.fit(
    data=marketing_df,
    target_column="sales",
    tune=1000,
    draws=1000
)

# Optimize budget
optimized = mmm.optimize_budget(
    total_budget=100000,
    budget_bounds={"tv": (10000, 50000), "radio": (5000, 30000)}
)

# Get ROI curves
roi_curves = mmm.compute_channel_roi()
```

### Geo Experimentation

#### GeoLift (Meta)
```r
# Install
remotes::install_github("facebookincubator/GeoLift")

library(GeoLift)

# Load data
data(GeoLift_Test)

# Find best test markets
best_markets <- GeoLiftMarketSelection(
  data = GeoLift_Test,
  treatment_locations = c("chicago"),
  N = 5,  # Number of control markets
  Y_id = "Y",
  location_id = "location",
  time_id = "time"
)

# Power analysis
power <- GeoLiftPower(
  data = GeoLift_Test,
  locations = best_markets$BestControl,
  treatment_locations = c("chicago"),
  effect_size = seq(0, 0.25, 0.05),
  lookback_window = 52
)

# After test runs, analyze results
results <- GeoLift(
  Y_id = "Y",
  data = GeoLift_Test,
  locations = best_markets$BestControl,
  treatment_locations = c("chicago"),
  treatment_start_time = 90,
  treatment_end_time = 105
)

# Plot results
plot(results)
```

#### Matched Markets (Google)
```python
# Install
# pip install matched-markets

from matched_markets.methodology import trimmed_match

# Prepare data
geo_data = {
    'geos': ['geo1', 'geo2', 'geo3', ...],
    'response': [100, 150, 120, ...],
    'spend': [50, 75, 60, ...]
}

# Design test
design = trimmed_match.TrimmedMatch(
    data=geo_data,
    treatment_geos=['geo1', 'geo2'],
    exclude_cooldown_period=7
)

# Run matching
design.fit()

# Estimate treatment effect
iroas = design.estimate_treatment_effect(
    post_treatment_response=post_data['response'],
    post_treatment_spend=post_data['spend']
)

print(f"Incremental ROAS: {iroas.point_estimate:.2f}")
print(f"95% CI: [{iroas.ci_lower:.2f}, {iroas.ci_upper:.2f}]")
```

### Multi-Touch Attribution

#### PyChattr
```python
# Install
# pip install pychattr

from pychattr.channel_attribution import MarkovModel

# Journey data format: each row is a conversion path
# format: 'channel1 > channel2 > channel3'
journeys = [
    'paid_search > display > direct',
    'social > email > direct',
    'direct',
    'paid_search > direct'
]

conversions = [1, 1, 0, 1]
revenues = [100, 150, 0, 80]

# Fit Markov model
markov = MarkovModel(
    paths=journeys,
    conversions=conversions,
    revenues=revenues,
    order=1  # First-order Markov chain
)

markov.fit()

# Get attribution results
attribution = markov.attribution()
print(attribution)

# Compare to heuristic models
from pychattr.channel_attribution import HeuristicModel

heuristic = HeuristicModel(
    paths=journeys,
    conversions=conversions,
    revenues=revenues
)

# Get last-touch, first-touch, linear
results = heuristic.attribution(
    heuristic_type=['last_touch', 'first_touch', 'linear']
)
```

#### ChannelAttribution (R)
```r
# Install
install.packages("ChannelAttribution")

library(ChannelAttribution)

# Prepare data
data <- data.frame(
  path = c("c1 > c2 > c3", "c1 > c3", "c2 > c3"),
  conversions = c(2, 1, 3),
  revenue = c(200, 100, 300)
)

# Markov model attribution
markov_model <- markov_model(
  data,
  var_path = "path",
  var_conv = "conversions",
  var_value = "revenue",
  order = 1,
  sep = " > "
)

print(markov_model)

# Heuristic models
heuristic <- heuristic_models(
  data,
  var_path = "path",
  var_conv = "conversions",
  var_value = "revenue",
  sep = " > "
)

# Compare removal effects
removal <- markov_model(
  data,
  var_path = "path",
  var_conv = "conversions",
  var_value = "revenue",
  order = 1,
  out_more = TRUE
)
```

### Causal Inference

#### CausalPy
```python
# Install
# pip install CausalPy

import pandas as pd
import causalpy as cp

# Synthetic control example
sc = cp.pymc_models.SyntheticControl(
    data=data,
    treatment_time=70,
    formula="actual ~ 0 + a + b + c + d + e + f + g",
    model=cp.pymc_models.WeightedSumFitter(
        sample_kwargs={"draws": 2000, "target_accept": 0.95}
    )
)

# Get results
result = sc.fit()

# Plot
result.plot()

# Get causal impact
impact = result.summary()
print(f"Average Treatment Effect: {impact['causal_impact'].mean():.2f}")
```

#### DoWhy
```python
# Install
# pip install dowhy

import dowhy
from dowhy import CausalModel

# Define causal model
model = CausalModel(
    data=df,
    treatment='ad_spend',
    outcome='revenue',
    common_causes=['seasonality', 'competitor_activity'],
    instruments=['budget_shock']
)

# Identify causal effect
identified_estimand = model.identify_effect(proceed_when_unidentifiable=True)

# Estimate causal effect
estimate = model.estimate_effect(
    identified_estimand,
    method_name="backdoor.propensity_score_matching"
)

print(f"Causal Effect: {estimate.value}")

# Refute results
refute = model.refute_estimate(
    identified_estimand,
    estimate,
    method_name="random_common_cause"
)
```

#### EconML (Microsoft)
```python
# Install
# pip install econml

from econml.dml import LinearDML
from sklearn.ensemble import GradientBoostingRegressor

# Double ML for heterogeneous treatment effects
dml = LinearDML(
    model_y=GradientBoostingRegressor(),
    model_t=GradientBoostingRegressor()
)

# Fit model
dml.fit(
    Y=outcomes,  # Revenue
    T=treatment,  # Ad spend
    X=features   # Customer features, context
)

# Get treatment effect for new data
treatment_effect = dml.effect(X_test)

# Get confidence intervals
lb, ub = dml.effect_interval(X_test, alpha=0.05)
```

### A/B Testing & Experimentation

#### CUPED Implementation
```python
import numpy as np
from scipy import stats

def cuped_variance_reduction(
    pre_experiment_metric,
    experiment_metric_control,
    experiment_metric_treatment
):
    """
    Implement CUPED variance reduction using pre-experiment data
    Based on: https://exp-platform.com/Documents/2013-02-CUPED-ImprovingSensitivityOfControlledExperiments.pdf
    """
    
    # Combine control and treatment
    Y = np.concatenate([experiment_metric_control, experiment_metric_treatment])
    X = np.concatenate([pre_experiment_metric[:len(experiment_metric_control)],
                        pre_experiment_metric[-len(experiment_metric_treatment):]])
    
    # Compute theta (optimal coefficient)
    theta = np.cov(X, Y)[0, 1] / np.var(X)
    
    # Adjust metrics
    Y_adjusted = Y - theta * (X - np.mean(X))
    
    # Split back
    n_control = len(experiment_metric_control)
    Y_adj_control = Y_adjusted[:n_control]
    Y_adj_treatment = Y_adjusted[n_control:]
    
    # Compute variance reduction
    original_var = np.var(Y)
    adjusted_var = np.var(Y_adjusted)
    variance_reduction = 1 - (adjusted_var / original_var)
    
    # Run t-test
    t_stat, p_value = stats.ttest_ind(Y_adj_treatment, Y_adj_control)
    
    return {
        'treatment_effect': np.mean(Y_adj_treatment) - np.mean(Y_adj_control),
        'p_value': p_value,
        'variance_reduction': variance_reduction,
        'theta': theta
    }
```

## Common Workflows

### Building a Marketing Measurement Stack

```python
"""
Unified measurement approach combining MMM, attribution, and experiments
"""
import pandas as pd
from pymc_marketing.mmm import MMM
from lightweight_mmm import preprocessing

class UnifiedMeasurement:
    def __init__(self):
        self.mmm = None
        self.attribution_model = None
        self.geo_test_results = {}
    
    def fit_mmm(self, aggregate_data):
        """Fit media mix model on aggregate time series"""
        self.mmm = MMM(
            date_column="date",
            channel_columns=["tv", "radio", "digital", "social"],
            adstock_max_lag=8
        )
        
        self.mmm.fit(
            data=aggregate_data,
            target_column="revenue",
            tune=1000,
            draws=1000
        )
        
        return self.mmm
    
    def calibrate_with_experiments(self, experiment_results):
        """
        Use geo experiment results to calibrate MMM
        Implements approach from Meta's Robyn
        """
        for channel, result in experiment_results.items():
            # Get experiment lift
            exp_lift = result['incremental_revenue'] / result['spend']
            
            # Get MMM prediction for same period
            mmm_lift = self.mmm.compute_channel_roi()[channel]
            
            # Calculate calibration factor
            calibration = exp_lift / mmm_lift
            
            # Store for adjustment
            self.geo_test_results[channel] = {
                'experiment_roi': exp_lift,
                'model_roi': mmm_lift,
                'calibration_factor': calibration
            }
    
    def optimize_budget(self, total_budget, constraints):
        """Optimize budget allocation using calibrated model"""
        
        # Get base optimization
        base_opt = self.mmm.optimize_budget(
            total_budget=total_budget,
            budget_bounds=constraints
        )
        
        # Adjust with experimental calibration
        calibrated_allocation = {}
        for channel, amount in base_opt.items():
            if channel in self.geo_test_results:
                factor = self.geo_test_results[channel]['calibration_factor']
                calibrated_allocation[channel] = amount * factor
            else:
                calibrated_allocation[channel] = amount
        
        # Normalize to budget
        total = sum(calibrated_allocation.values())
        calibrated_allocation = {
            k: v * (total_budget / total) 
            for k, v in calibrated_allocation.items()
        }
        
        return calibrated_allocation
```

### Running Geo Experiments End-to-End

```python
"""
Complete geo experiment workflow
"""

def design_geo_test(historical_data, treatment_geos, test_duration_weeks):
    """Design matched-market test"""
    from matched_markets.methodology import trimmed_match
    
    # Find best control geos
    design = trimmed_match.TrimmedMatch(
        data=historical_data,
        treatment_geos=treatment_geos,
        pre_treatment_periods=52  # 1 year lookback
    )
    
    design.fit()
    
    # Power analysis
    power_results = design.power_analysis(
        effect_sizes=np.arange(0.05, 0.30, 0.05),
        test_duration=test_duration_weeks
    )
    
    return design, power_results

def analyze_geo_test(design, post_treatment_data):
    """Analyze completed test"""
    
    # Estimate treatment effect
    result = design.estimate_treatment_effect(
        post_treatment_response=post_treatment_data['revenue'],
        post_treatment_spend=post_treatment_data['spend']
    )
    
    # Calculate iROAS
    iroas = result.incremental_revenue / result.incremental_spend
    
    # Check statistical significance
    is_significant = result.p_value < 0.05
    
    return {
        'iroas': iroas,
        'incremental_revenue': result.incremental_revenue,
        'p_value': result.p_value,
        'confidence_interval': (result.ci_lower, result.ci_upper),
        'is_significant': is_significant
    }
```

## Configuration & Best Practices

### MMM Hyperparameter Tuning

```python
# Example: Grid search for adstock and saturation parameters
from lightweight_mmm import optimize_media

# Define parameter ranges
adstock_range = {
    'tv': (0.3, 0.8),
    'digital': (0.1, 0.5),
    'radio': (0.2, 0.6)
}

saturation_range = {
    'tv': (0.5, 1.5),
    'digital': (0.3, 1.0),
    'radio': (0.4, 1.2)
}

# Run optimization
best_params = optimize_media.optimize_hyperparameters(
    media_data=media_data,
    target=target,
    adstock_ranges=adstock_range,
    saturation_ranges=saturation_range,
    n_iter=100
)
```

### Prior Elicitation for Bayesian MMM

```python
"""
Prior elicitation using domain expertise
Based on: https://github.com/louismagowan/mmm-prior-elicitation
"""

def elicit_channel_priors(historical_roas_estimates):
    """
    Convert historical ROAS ranges into prior distributions
    """
    priors = {}
    
    for channel, roas_range in historical_roas_estimates.items():
        # Convert ROAS range to lognormal parameters
        lower, upper = roas_range
        mean_log = (np.log(lower) + np.log(upper)) / 2
        std_log = (np.log(upper) - np.log(lower)) / 4  # ~95% in range
        
        priors[channel] = {
            'distribution': 'lognormal',
            'mu': mean_log,
            'sigma': std_log
        }
    
    return priors

# Example usage
expert_estimates = {
    'tv': (1.5, 3.0),      # TV ROAS between 1.5x and 3.0x
    'digital': (2.0, 5.0),
    'radio': (1.0, 2.5)
}

priors = elicit_channel_priors(expert_estimates)
```

## Troubleshooting

### MMM Model Not Converging

```python
# Check for common issues
import arviz as az

# 1. Check R-hat (should be < 1.01)
def check_convergence(mmm_trace):
    summary = az.summary(mmm_trace)
    problematic = summary[summary['r_hat'] > 1.01]
    if len(problematic) > 0:
        print("Convergence issues for:", problematic.index.tolist())
        print("Solution: Increase warmup/draws or reparameterize")
    return problematic

# 2. Check for scaling issues
def check_data_scaling(media_data, target):
    for i, channel in enumerate(media_data.columns):
        ratio = target.std() / media_data.iloc[:, i].std()
        if ratio > 100 or ratio < 0.01:
            print(f"{channel}: scaling issue (ratio: {ratio:.2f})")
            print("Solution: Normalize or standardize data")

# 3. Increase sampling
mmm.fit(
    media=media_data,
    target=target,
    number_warmup=2000,  # Increased from 1000
    number_samples=2000,
    number_chains=4
)
```

### Geo Test Power Issues

```python
def diagnose_low_power(design, target_power=0.8):
    """
    Diagnose why geo test has low power
    """
    diagnostics = {}
    
    # Check match quality
    diagnostics['match_quality'] = design.match_quality_score
    if diagnostics['match_quality'] < 0.7:
        print("Poor match quality. Consider:")
        print("- Increasing lookback window")
        print("- Adding more control geos")
        print("- Using time-based regression instead of matching")
    
    # Check historical variance
    diagnostics['outcome_cv'] = design.historical_cv
    if diagnostics['outcome_cv'] > 0.3:
        print("High outcome variance. Consider:")
        print("- Longer test duration")
        print("- Larger treatment effect")
        print("- CUPED-style variance reduction")
    
    # Check sample size
    diagnostics['n_geos'] = len(design.treatment_geos) + len(design.control_geos)
    if diagnostics['n_geos'] < 10:
        print("Small sample size. Consider:")
        print("- Aggregating smaller geos")
        print("- Using synthetic control instead")
    
    return diagnostics
```

### Attribution Model Interpretation

```python
def compare_attribution_models(journey_data):
    """
    Compare multiple attribution approaches
    """
    from pychattr.channel_attribution import MarkovModel, HeuristicModel
    
    results = {}
    
    # Heuristic models
    heuristic = HeuristicModel(
        paths=journey_data['paths'],
        conversions=journey_data['conversions'],
        revenues=journey_data['revenues']
    )
    
    results['last_touch'] = heuristic.attribution(heuristic_type='last_touch')
    results['first_touch'] = heuristic.attribution(heuristic_type='first_touch')
    results['linear'] = heuristic.attribution(heuristic_type='linear')
    
    # Markov models
    for order in [1, 2]:
        markov = MarkovModel(
            paths=journey_data['paths'],
            conversions=journey_data['conversions'],
            revenues=journey_data['revenues'],
            order=order
        )
        markov.fit()
        results[f'markov_order_{order}'] = markov.attribution()
    
    # Compare
    comparison = pd.DataFrame(results)
    print("\nAttribution Comparison:")
    print(comparison)
    
    # Flag large discrepancies
    for channel in comparison.index:
        channel_results = comparison.loc[channel]
        if channel_results.std() / channel_results.mean() > 0.5:
            print(f"\nWarning: Large variation for {channel}")
            print("Consider: combining with MMM or incrementality tests")
    
    return comparison
```

## Environment Variables

For projects using external APIs or cloud resources:

```bash
# BigQuery for data access
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/credentials.json"

# For cloud-based MMM runs
export GCP_PROJECT_ID="your-project-id"
export GCP_BUCKET="your-bucket-name"

# For distributed computing
export STAN_NUM_THREADS=4
export PYMC_NUM_CHAINS=4
```

## Additional Resources

- **Documentation**: Check each library's GitHub repository for detailed docs
- **Community**: Join marketing science Slack communities and subreddits
- **Papers**: Start with the "Must Read" section for foundational understanding
- **Tutorials**: PyMC, Google, and Meta publish extensive tutorials on their blogs

## Integration Examples

### Connecting MMM with Data Warehouse

```python
from google.cloud import bigquery
import pandas as pd

def load_marketing_data_for_mmm(project_id, lookback_days=730):
    """
    Load aggregated marketing data from BigQuery
    """
    client = bigquery.Client(project=project_id)
    
    query = f"""
    SELECT
        DATE(timestamp) as date,
        SUM(CASE WHEN channel = 'TV' THEN spend ELSE 0 END) as tv_spend,
        SUM(CASE WHEN channel = 'Digital' THEN spend ELSE 0 END) as digital_spend,
        SUM(CASE WHEN channel = 'Radio' THEN spend ELSE 0 END) as radio_spend,
        SUM(revenue) as revenue,
        SUM(conversions) as conversions
    FROM `{project_id}.marketing.daily_summary`
    WHERE DATE(timestamp) >= DATE_SUB(CURRENT_DATE(), INTERVAL {lookback_days} DAY)
    GROUP BY date
    ORDER BY date
    """
    
    df = client.query(query).to_dataframe()
    return df
```

This skill provides comprehensive guidance for using the Awesome Marketing Science collection to implement production marketing measurement systems.

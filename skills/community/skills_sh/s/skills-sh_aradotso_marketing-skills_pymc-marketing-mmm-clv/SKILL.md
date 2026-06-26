---
name: pymc-marketing-mmm-clv
description: Bayesian marketing analytics with PyMC for Media Mix Modeling (MMM), Customer Lifetime Value (CLV), and BTYD models
triggers:
  - "create a media mix model"
  - "analyze marketing campaign effectiveness"
  - "build a customer lifetime value model"
  - "optimize marketing budget allocation"
  - "implement bayesian marketing mix modeling"
  - "calculate ROAS and channel contributions"
  - "forecast customer lifetime value"
  - "setup MMM with adstock and saturation"
---

# PyMC-Marketing: Bayesian Marketing Analytics

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

PyMC-Marketing is a Bayesian marketing analytics toolbox built on PyMC. It provides production-ready implementations for Media Mix Modeling (MMM), Customer Lifetime Value (CLV), and Buy-Till-You-Die (BTYD) models with full probabilistic inference capabilities.

## Installation

### Basic Installation

```bash
# Using conda (recommended)
conda create -c conda-forge -n marketing_env pymc-marketing
conda activate marketing_env

# Using pip
pip install pymc-marketing
```

### Docker Installation

The project provides Docker support for Jupyter-based workflows:

```bash
cd scripts/docker
docker build -t pymc-marketing .
docker run -p 8888:8888 pymc-marketing
```

## Core Capabilities

### 1. Media Mix Modeling (MMM)

MMM helps quantify the impact of marketing channels on business outcomes with:

- **Adstock transformations**: Geometric, delayed, Weibull
- **Saturation effects**: Logistic, Michaelis-Menten, Tanh
- **Time-varying effects**: Intercept and media contribution dynamics
- **Budget optimization**: ROI-maximizing allocation across channels
- **Experiment calibration**: Lift test integration

### 2. Customer Lifetime Value (CLV)

Probabilistic models for customer value prediction:

- **Beta-Geometric/NBD**: For non-contractual settings
- **Pareto/NBD**: Customer dropout modeling
- **Gamma-Gamma**: Monetary value modeling

### 3. Customer Choice Analysis (CSA)

Discrete choice modeling for understanding customer preferences.

## Media Mix Modeling (MMM)

### Basic MMM Setup

```python
import pandas as pd
from pymc_marketing.mmm import MMM, GeometricAdstock, LogisticSaturation

# Load your data
data = pd.read_csv("marketing_data.csv", parse_dates=["date"])

# Initialize MMM model
mmm = MMM(
    adstock=GeometricAdstock(l_max=8),  # Carryover effect up to 8 periods
    saturation=LogisticSaturation(),    # Diminishing returns
    date_column="date",
    channel_columns=["tv", "radio", "digital", "social"],
    control_columns=["holiday", "promotion", "temperature"],
    yearly_seasonality=2,  # Fourier terms for seasonality
)

# Fit the model
X = data.drop("sales", axis=1)
y = data["sales"]
mmm.fit(X, y)
```

### Available Adstock Functions

```python
from pymc_marketing.mmm import (
    GeometricAdstock,      # Exponential decay
    DelayedAdstock,        # Peak effect after delay
    WeibullAdstock,        # Flexible S-curve decay
)

# Geometric (most common)
adstock = GeometricAdstock(l_max=8, normalize=True)

# Delayed (for channels with lagged effects)
adstock = DelayedAdstock(l_max=12, theta_prior_params={"alpha": 2, "beta": 1})

# Weibull (flexible shape)
adstock = WeibullAdstock(l_max=10, mode_prior_params={"mu": 2, "sigma": 1})
```

### Available Saturation Functions

```python
from pymc_marketing.mmm import (
    LogisticSaturation,           # Logistic curve
    MichaelisMentenSaturation,   # Enzyme kinetics-based
    TanhSaturation,              # Hyperbolic tangent
)

# Logistic (most common)
saturation = LogisticSaturation()

# Michaelis-Menten (pharmaceutical/biological intuition)
saturation = MichaelisMentenSaturation()

# Tanh (symmetric S-curve)
saturation = TanhSaturation()
```

### Time-Varying Effects

```python
from pymc_marketing.mmm import MMM
from pymc_marketing.mmm.components.adstock import GeometricAdstock
from pymc_marketing.mmm.components.saturation import LogisticSaturation

# Time-varying intercept (baseline sales trends)
mmm = MMM(
    adstock=GeometricAdstock(l_max=8),
    saturation=LogisticSaturation(),
    date_column="date",
    channel_columns=["tv", "digital"],
    time_varying_intercept=True,  # Enable GP-based intercept
    intercept_m=100,  # Number of basis functions
)

# Time-varying media contribution (changing efficiency)
mmm = MMM(
    adstock=GeometricAdstock(l_max=8),
    saturation=LogisticSaturation(),
    date_column="date",
    channel_columns=["tv", "digital"],
    time_varying_media=True,  # Enable time-varying coefficients
    media_m=50,  # Basis functions for media
)
```

### Model Diagnostics and Visualization

```python
# Trace plots for MCMC diagnostics
mmm.plot_trace()

# Component contributions over time
mmm.plot_components_contributions()

# Channel contribution breakdown
mmm.plot_channel_contribution_share_hdi()

# Posterior predictive checks
mmm.plot_posterior_predictive(original_scale=True)

# Model goodness of fit
mmm.plot_curve()
```

### Budget Optimization

```python
# Get optimal budget allocation
budget_allocator = mmm.allocate_budget(
    total_budget=1_000_000,
    budget_bounds={
        "tv": (100_000, 500_000),
        "digital": (50_000, 400_000),
        "radio": (0, 200_000),
    },
    num_days=90,  # Planning horizon
)

# View optimal allocation
optimal = budget_allocator.allocate()
print(optimal)

# Visualize budget optimization
mmm.plot_budget_allocation(
    total_budget=1_000_000,
    budget_bounds={"tv": (0, 500_000), "digital": (0, 500_000)},
)
```

### ROAS and Channel Efficiency

```python
# Calculate ROAS (Return on Ad Spend)
roas = mmm.compute_mean_roas()
print(roas)

# Channel contributions
contributions = mmm.compute_channel_contribution_original_scale()
print(contributions)

# Marginal ROAS (efficiency at current spend levels)
marginal_roas = mmm.compute_marginal_roas(spend_grid_size=20)
```

### Lift Test Calibration

```python
from pymc_marketing.mmm.lift_test import add_lift_measurements_to_likelihood

# Define lift test results
lift_test_results = pd.DataFrame({
    "channel": ["tv", "digital"],
    "lift": [0.15, 0.22],  # 15% and 22% lift
    "sigma": [0.03, 0.04],  # Standard errors
})

# Incorporate into model
mmm_calibrated = MMM(
    adstock=GeometricAdstock(l_max=8),
    saturation=LogisticSaturation(),
    date_column="date",
    channel_columns=["tv", "digital", "radio"],
    control_columns=["holiday"],
)

# Fit with lift test priors
mmm_calibrated.fit(
    X, y,
    prior_fn=lambda model: add_lift_measurements_to_likelihood(
        model, lift_test_results
    )
)
```

### Out-of-Sample Prediction

```python
# Prepare future data (marketing plan)
future_data = pd.DataFrame({
    "date": pd.date_range("2024-01-01", periods=52, freq="W"),
    "tv": [50000] * 52,
    "digital": [30000] * 52,
    "radio": [10000] * 52,
    "holiday": [0] * 52,
})

# Generate predictions with uncertainty
predictions = mmm.sample_posterior_predictive(
    X_pred=future_data,
    extend_idata=True,
    combined=True,
)

# Access prediction samples
forecast = predictions.posterior_predictive["y"].mean(dim=["chain", "draw"])
```

### Alternative NUTS Samplers

```python
# Using NumPyro (faster for large models)
mmm.fit(X, y, nuts_sampler="numpyro", chains=4, draws=2000)

# Using BlackJax
mmm.fit(X, y, nuts_sampler="blackjax", chains=4, draws=2000)

# Using Nutpie (experimental, very fast)
mmm.fit(X, y, nuts_sampler="nutpie", chains=4, draws=2000)

# Default PyMC sampler
mmm.fit(X, y, nuts_sampler="pymc", chains=4, draws=2000)
```

## Customer Lifetime Value (CLV)

### Beta-Geometric/NBD Model

```python
from pymc_marketing.clv import BetaGeoModel
import pandas as pd

# Prepare RFM data (Recency, Frequency, Monetary, T)
rfm_data = pd.DataFrame({
    "customer_id": [1, 2, 3, 4, 5],
    "frequency": [5, 2, 8, 1, 3],       # Number of repeat purchases
    "recency": [10, 5, 15, 2, 8],       # Time of last purchase
    "T": [20, 20, 20, 20, 20],          # Time since first purchase
})

# Initialize and fit model
bg_model = BetaGeoModel(
    data=rfm_data,
)

bg_model.fit()

# Predict future transactions
expected_purchases = bg_model.expected_num_purchases(
    t=30,  # Next 30 days
    frequency=rfm_data["frequency"],
    recency=rfm_data["recency"],
    T=rfm_data["T"],
)

# Probability customer is alive
prob_alive = bg_model.expected_probability_alive(
    frequency=rfm_data["frequency"],
    recency=rfm_data["recency"],
    T=rfm_data["T"],
)
```

### Pareto/NBD Model

```python
from pymc_marketing.clv import ParetoNBDModel

# Similar to BetaGeo but different distributional assumptions
pareto_model = ParetoNBDModel(data=rfm_data)
pareto_model.fit()

# Customer lifetime value over time horizon
clv_12_months = pareto_model.expected_num_purchases(
    t=365,
    frequency=rfm_data["frequency"],
    recency=rfm_data["recency"],
    T=rfm_data["T"],
)
```

### Gamma-Gamma Model (Monetary Value)

```python
from pymc_marketing.clv import GammaGammaModel

# Prepare monetary data
monetary_data = pd.DataFrame({
    "customer_id": [1, 2, 3, 4, 5],
    "frequency": [5, 2, 8, 1, 3],
    "monetary_value": [250, 180, 420, 90, 310],  # Average order value
})

# Fit monetary model
gg_model = GammaGammaModel(data=monetary_data)
gg_model.fit()

# Predict average transaction value
expected_avg_value = gg_model.expected_customer_spend(
    frequency=monetary_data["frequency"],
    monetary_value=monetary_data["monetary_value"],
)

# Combine with transaction model for total CLV
total_clv = expected_purchases * expected_avg_value
```

## Model Saving and Loading

```python
# Save fitted model
mmm.save("mmm_model.nc")

# Load model
from pymc_marketing.mmm import MMM
mmm_loaded = MMM.load("mmm_model.nc")

# Continue using loaded model
mmm_loaded.sample_posterior_predictive(X_new)
```

## Configuration Patterns

### Custom Priors

```python
import pymc as pm

mmm = MMM(
    adstock=GeometricAdstock(l_max=8),
    saturation=LogisticSaturation(),
    date_column="date",
    channel_columns=["tv", "digital"],
    control_columns=["holiday"],
)

# Access and modify priors before fitting
with mmm.model:
    # Custom prior for channel coefficients
    mmm.model["beta_channel"] = pm.HalfNormal(
        "beta_channel_custom", 
        sigma=2, 
        shape=2
    )

mmm.fit(X, y)
```

### Sampler Configuration

```python
# Fine-tune MCMC sampling
mmm.fit(
    X, y,
    chains=4,           # Parallel chains
    draws=3000,         # Samples per chain
    tune=2000,          # Tuning steps
    target_accept=0.95, # Acceptance rate (higher = slower but safer)
    random_seed=42,
)
```

## Troubleshooting

### Convergence Issues

```python
# Check R-hat (should be < 1.01)
import arviz as az
az.summary(mmm.idata, var_names=["beta_channel", "alpha"])

# Increase tuning steps if R-hat is high
mmm.fit(X, y, tune=3000, draws=2000)

# Use stronger priors if you have domain knowledge
```

### Long Fitting Times

```python
# Use faster samplers
mmm.fit(X, y, nuts_sampler="numpyro")  # GPU-accelerated if available

# Reduce chains and draws for testing
mmm.fit(X, y, chains=2, draws=1000, tune=1000)

# Use prior predictive checks to validate model before full fit
mmm.sample_prior_predictive(samples=500)
```

### Memory Issues

```python
# Thin the posterior samples
mmm.fit(X, y, draws=2000, tune=1000)
# Then thin in post-processing
thinned_idata = mmm.idata.sel(draw=slice(None, None, 2))
```

### Data Scaling Issues

```python
# Normalize spend data to similar scales
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X[["tv", "digital", "radio"]] = scaler.fit_transform(
    X[["tv", "digital", "radio"]]
)

# Remember to inverse transform for budget optimization
```

## Common Workflows

### End-to-End MMM Analysis

```python
import pandas as pd
from pymc_marketing.mmm import MMM, GeometricAdstock, LogisticSaturation

# 1. Load and prepare data
data = pd.read_csv("marketing_data.csv", parse_dates=["date"])
X = data.drop("sales", axis=1)
y = data["sales"]

# 2. Initialize model
mmm = MMM(
    adstock=GeometricAdstock(l_max=8),
    saturation=LogisticSaturation(),
    date_column="date",
    channel_columns=["tv", "digital", "radio"],
    control_columns=["holiday", "promotion"],
    yearly_seasonality=2,
)

# 3. Fit model
mmm.fit(X, y, chains=4, draws=2000, tune=2000)

# 4. Diagnostics
mmm.plot_trace()
mmm.plot_posterior_predictive(original_scale=True)

# 5. Insights
mmm.plot_components_contributions()
roas = mmm.compute_mean_roas()
print(f"ROAS by channel:\n{roas}")

# 6. Budget optimization
optimal_budget = mmm.allocate_budget(
    total_budget=1_000_000,
    budget_bounds={
        "tv": (100_000, 500_000),
        "digital": (50_000, 400_000),
        "radio": (0, 200_000),
    },
    num_days=90,
)
print(f"Optimal allocation:\n{optimal_budget.allocate()}")
```

### CLV Prediction Pipeline

```python
from pymc_marketing.clv import BetaGeoModel, GammaGammaModel

# 1. Prepare RFM summary
rfm = customer_transactions.groupby("customer_id").agg({
    "transaction_date": lambda x: (x.max() - x.min()).days,  # recency
    "order_id": "count",  # frequency (subtract 1 for repeat purchases)
    "revenue": "mean",  # monetary value
})
rfm["frequency"] = rfm["order_id"] - 1
rfm["T"] = (pd.Timestamp.now() - customer_first_purchase["date"]).dt.days

# 2. Fit transaction model
bg_model = BetaGeoModel(data=rfm[["frequency", "recency", "T"]])
bg_model.fit()

# 3. Fit monetary model (only customers with repeat purchases)
repeat_customers = rfm[rfm["frequency"] > 0]
gg_model = GammaGammaModel(data=repeat_customers[["frequency", "revenue"]])
gg_model.fit()

# 4. Predict 12-month CLV
expected_purchases = bg_model.expected_num_purchases(
    t=365, frequency=rfm["frequency"], recency=rfm["recency"], T=rfm["T"]
)
expected_value = gg_model.expected_customer_spend(
    frequency=rfm["frequency"], monetary_value=rfm["revenue"]
)
clv_12m = expected_purchases * expected_value
```

## Environment Variables

```python
# For remote storage integration
import os

# S3 model storage
os.environ["AWS_ACCESS_KEY_ID"] = "your_key_id"
os.environ["AWS_SECRET_ACCESS_KEY"] = "your_secret_key"

# MLflow tracking
os.environ["MLFLOW_TRACKING_URI"] = "http://mlflow-server:5000"

# PyMC compute backend
os.environ["PYMC_BACKEND"] = "jax"  # or "numpy"
```

## Additional Resources

- **Documentation**: https://www.pymc-marketing.io/
- **Examples**: https://www.pymc-marketing.io/en/stable/notebooks/
- **Discourse**: https://discourse.pymc.io/
- **GitHub Discussions**: https://github.com/pymc-labs/pymc-marketing/discussions

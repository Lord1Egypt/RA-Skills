# Universal Data Analyst - Quick Reference

## Quick Start (Three Steps)

```bash
# 1. Run the analysis workflow
python orchestrator.py data.csv --intent "Your analysis goal"

# 2. Get the generated prompt files
#    - step2_ontology_prompt.txt
#    - step4_planning_prompt.txt
#    - step5_script_prompt.txt

# 3. Send the prompts to an LLM to get analysis results
```

---

## Seven-Step Analysis Workflow

| Step | Action | LLM Call | Output |
|------|--------|----------|--------|
| 1 | Load data | ❌ | Basic data info |
| 2 | Ontology identification | ✅ | What existence is this data |
| 3 | Data validation | ❌ | Quality report |
| 4 | Analysis planning | ✅ | What method to use |
| 5 | Script generation | ✅ | Python analysis script |
| 6 | Execute analysis | ❌ | Analysis results |
| 7 | Report generation | ✅ | HTML + Markdown report |

---

## Data Ontology Quick Reference

### Entity Type Identification

| Characteristics | Type | Example |
|-----------------|------|---------|
| Has timestamp, one-time occurrence, non-repeatable | **Transaction/Event** | Orders, clicks, earthquakes |
| Point-in-time snapshot, cumulative | **State/Stock** | Inventory, population, balance |
| Describes connections between entities | **Relationship/Network** | Social relations, trade flows |
| Static attributes, rarely change over time | **Feature/Attribute** | User profiles, product specs |
| Continuous measurements, serial dependency | **Time-series/Trajectory** | Stock prices, temperature, sensors |

### Generation Mechanism

| Mechanism | Characteristics | Potential Bias |
|-----------|----------------|----------------|
| **Observational** | Passively recorded | Selection bias, survivorship bias |
| **Experimental** | Has intervention/control | Less bias, causal inference possible |
| **Simulated** | Rule-based generation | Conclusions limited to simulation scenario |
| **Measured** | Instrument-collected | Measurement error |
| **Reported** | Manually filled | Social desirability bias |

---

## Problem Type Quick Reference

| Type | Keywords | Data Requirement | Typical Methods |
|------|----------|-----------------|----------------|
| **Descriptive** | what is, distribution, characteristics | Representative sample | Descriptive statistics, visualization |
| **Diagnostic** | why, reason, attribution | Multi-dimensional decomposition | Decomposition analysis, root cause analysis |
| **Predictive** | will happen, trend, forecast | Time series | ARIMA, Prophet, ML |
| **Prescriptive** | should, optimal, strategy | Action-outcome mapping | Optimization models, decision analysis |
| **Causal** | effect, influence, mechanism | Control group / time variation | DID, RDD, PSM |

---

## Economic Type Quick Reference

| Data Characteristics | Economic Type | Analysis Method |
|---------------------|--------------|-----------------|
| Orders + prices + profit + SKU | **Retail economy** | Value chain + ABC-XYZ + RFM |
| Orders + price + B2B clients | **Mixed retail** | Value chain + customer segmentation + price elasticity |
| view + cart + buy event chain | **Attention economy** | Funnel analysis + session mining |
| GMV + platform matchmaking | **Commission economy** | Two-sided network effects + unit economics |
| Users + subscription cycle + Churn | **Subscription economy** | LTV/Cohort + retention curves |
| Assets + usage records | **Rental economy** | Asset utilization + revenue management |
| Job postings + skills + salary | **Labor market** | Skill premium + experience elasticity |
| OHLCV prices | **Financial time series** | Technical analysis + volatility modeling |

---

## Non-economic Data Quick Reference

| Data Type | Domain | Analysis Method |
|-----------|--------|-----------------|
| Sensor continuous data | Earth science | Time series decomposition, extreme value analysis |
| Network connection data | Social network | Centrality, community detection |
| Geographic coordinate data | Spatial analysis | Spatial autocorrelation, hotspot analysis |
| Text corpus | NLP | Topic modeling, sentiment analysis |
| Image pixels | Computer vision | Feature extraction, classification/clustering |
| Gene sequences | Bioinformatics | Sequence alignment, differential expression |

---

## Common Python Patterns

### Load Data
```python
from orchestrator import DataAnalysisOrchestrator

orch = DataAnalysisOrchestrator()
orch.step1_load_data("data.csv")
```

### Load Multiple Files (V2)
```python
from main import UniversalDataAnalystV2

analyst = UniversalDataAnalystV2()
analyst.load_multiple_files(["users.csv", "orders.csv"])
join_report = analyst.analyze_join_feasibility()
```

### Autonomous Mode (V2, No LLM)
```python
analyst = UniversalDataAnalystV2()
analyst.load_data("data.csv")
ontology = analyst.get_ontology_autonomous()
strategy = analyst.get_quality_driven_strategy()
```

### Generate Ontology Identification Prompt
```python
prompt, file_path = orch.step2_identify_ontology()
# Send prompt to LLM
```

### Generate Analysis Planning Prompt
```python
prompt, file_path = orch.step4_plan_analysis("Analyze sales trends")
# Send prompt to LLM
```

### Full Single-pass Analysis
```python
results = orch.run_full_analysis(
    file_path="data.csv",
    user_intent="Exploratory data analysis"
)
```

---

## Output Files

```
session_YYYYMMDD_HHMMSS/
├── SESSION_SUMMARY.json          # Session summary
├── step1_data_info.json          # Basic data info
├── step2_ontology_prompt.txt     # Ontology identification prompt ⭐
├── step3_validation_report.json  # Quality report
├── step4_planning_prompt.txt     # Analysis planning prompt ⭐
├── step5_script_prompt.txt       # Script generation prompt ⭐
└── step6_report_prompt.txt       # Report generation prompt ⭐

⭐ = Prompts to send to an LLM
```

---

## FAQ

**Q: Why does this generate prompts instead of direct results?**
A: Every analysis requires an LLM to reason about the specific data characteristics. No hardcoded rules are used.

**Q: How do I use the generated prompts?**
A: Copy the content of the .txt file and send it to Claude, ChatGPT, or any other LLM to get structured results.

**Q: What file formats are supported?**
A: CSV, Excel, Parquet, JSON, SQL databases (via data_loader.py)

**Q: Is there a data size limit?**
A: Limited by memory; typically supports millions of rows. For very large datasets, sampling is recommended.

**Q: Can it analyze non-economic data?**
A: Yes. The skill automatically identifies the domain type based on data characteristics and matches the appropriate analysis methods.

**Q: What is autonomous mode?**
A: Autonomous mode (V2) infers data ontology using rule-based heuristics without calling an external LLM. Useful for quick analysis or when LLM access is unavailable.

---

## Core Principles

> **First define ontology, then select methods, then execute.**
>
> **Don't ask "what economy", ask "what existence".**
>
> **Don't ask "how to profit", ask "what problem to solve".**

# Universal Data Analyst

An intelligent data analysis skill based on a four-layer universal analysis framework.
Every analysis decision is made by an LLM — no hardcoded rules.

## Core Design Philosophy

```
┌─────────────────────────────────────────────────────────────┐
│                     Data Input (Any Type)                    │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  Layer 1: Data Ontology                                      │
│  — Don't ask "what economy", ask "what existence"            │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  Layer 2: Problem Typology                                   │
│  — Don't ask "how to profit", ask "what problem to solve"    │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  Layer 3: Methodology Mapping                                │
│  — Match domain-recognized analysis methods                  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  Layer 4: Validation & Output                                │
└─────────────────────────────────────────────────────────────┘
```

## Workflow

### Seven-Step Analysis Process

```
User uploads data
    ↓
[Step 1] Data Loading (data_loader.py)
    ↓
[Step 2] Ontology Identification → LLM reasoning ("What existence is this?")
    ↓
[Step 3] Data Validation (data_validator.py) [mandatory]
    ↓
[Step 4] Analysis Planning → LLM reasoning ("What method should we use?")
    ↓
[Step 5] Script Generation → LLM reasoning ("What code should we write?")
    ↓
[Step 6] Execute Analysis
    ↓
[Step 7] Comprehensive Report (HTML + MD + charts)
    ↓
Output Analysis Report
```

## Key Features

| Feature | Description |
|---------|-------------|
| **No Hardcoding** | No keyword matching — every decision invokes an LLM |
| **Universal** | Supports both economic and non-economic data |
| **Adaptive** | Automatically selects analysis framework based on data characteristics |
| **Single-pass** | Can complete analysis in one round when user intent is clear |
| **Explainable** | Every decision has a clear rationale |
| **Multi-file** | Supports loading and joining multiple files/tables |
| **Autonomous** | Can infer ontology without external LLM (autonomous mode) |
| **Quality-driven** | Automatically adjusts strategy based on data quality score |

## Installation

```bash
# Install dependencies
pip install pandas numpy matplotlib seaborn scipy scikit-learn

# Add to Python path
export PYTHONPATH="/path/to/universal-data-analyst:$PYTHONPATH"
```

## Usage

### Command Line

```bash
# Basic usage
python orchestrator.py data.csv --intent "Analyze sales trends"

# Full parameters
python orchestrator.py data.csv \
    --intent "Analyze customer segmentation and purchasing behavior" \
    --output ./my_analysis
```

### Python API

```python
from orchestrator import DataAnalysisOrchestrator

# Initialize orchestrator
orchestrator = DataAnalysisOrchestrator(output_dir="./analysis_output")

# Run full analysis
results = orchestrator.run_full_analysis(
    file_path="data.csv",
    user_intent="Exploratory data analysis to understand data characteristics"
)

print(f"Results saved at: {results['session_dir']}")
```

### Multi-file Analysis (V2)

```python
from main import UniversalDataAnalystV2

analyst = UniversalDataAnalystV2()

# Load multiple files
results = analyst.load_multiple_files([
    "users.csv",
    "orders.csv",
    "products.csv"
])

# Analyze join feasibility
join_report = analyst.analyze_join_feasibility()
print(join_report['summary'])

# Auto-join tables
joined_df = analyst.join_tables(
    left_table="users",
    right_table="orders",
    join_key="user_id"
)
```

### Autonomous Mode (No External LLM)

```python
from main import UniversalDataAnalystV2

analyst = UniversalDataAnalystV2()
analyst.load_data("data.csv")

# Autonomous ontology inference (no LLM required)
ontology = analyst.get_ontology_autonomous()
print(f"Entity type: {ontology['entity_type']}")
print(f"Economic type: {ontology['economic_type']}")

# Quality-driven strategy
strategy = analyst.get_quality_driven_strategy()
print(f"Quality score: {strategy['quality_score']}")
print(f"Recommended approach: {strategy['recommended_approach']}")
```

### Step-by-step Usage

```python
from orchestrator import DataAnalysisOrchestrator

orchestrator = DataAnalysisOrchestrator()

# Step 1: Load data
orchestrator.step1_load_data("data.csv")

# Step 2: Generate ontology identification prompt
ontology_prompt, ontology_file = orchestrator.step2_identify_ontology()
# → Send ontology_prompt to LLM to get ontology result

# Step 4: Generate analysis planning prompt
planning_prompt, planning_file = orchestrator.step4_plan_analysis("Analyze sales trends")
# → Send planning_prompt to LLM to get analysis plan

# Step 5: Generate script prompt
script_prompt, script_file = orchestrator.step5_generate_script()
# → Send script_prompt to LLM to get analysis script
```

## Prompt Usage Notes

This skill generates **high-quality LLM prompts** that need to be used with an LLM:

1. **Step 2 prompt** → Get data ontology identification result (JSON format)
2. **Step 4 prompt** → Get analysis plan (JSON format)
3. **Step 5 prompt** → Get analysis script (Python code)
4. **Step 6 prompt** → Get analysis report (Markdown format)

### Example: Using Claude API

```python
import anthropic, json

client = anthropic.Anthropic()

# Read Step 2 prompt
with open("step2_ontology_prompt.txt") as f:
    ontology_prompt = f.read()

# Call Claude for ontology identification
response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=4000,
    messages=[{"role": "user", "content": ontology_prompt}]
)

# Parse JSON result
ontology_result = json.loads(response.content[0].text)
```

## Supported File Formats

Via `data_loader.py`:
- CSV (.csv)
- Excel (.xlsx, .xls)
- Parquet (.parquet)
- JSON (.json)
- SQL database (via connection string)

## Output Files

Each analysis session generates:

```
analysis_output/
└── session_YYYYMMDD_HHMMSS/
    ├── SESSION_SUMMARY.json          # Session summary
    ├── step1_data_info.json          # Basic data info
    ├── step2_ontology_prompt.txt     # Ontology identification prompt ⭐
    ├── step3_validation_report.json  # Data validation report
    ├── step3_cleaning_report.txt     # Cleaning recommendation report
    ├── step4_planning_prompt.txt     # Analysis planning prompt ⭐
    ├── step5_script_prompt.txt       # Script generation prompt ⭐
    ├── step6_report_prompt.txt       # Report generation prompt ⭐
    └── output/                       # Analysis result output directory
        ├── analysis_script.py
        ├── charts/
        └── report.md
```

⭐ = Prompts to send to an LLM

## Economic Type Quick Reference

| Data Characteristics | Economic Type | Analysis Framework |
|---------------------|--------------|-------------------|
| Orders + prices + profit + SKU | Retail economy | Value chain + ABC-XYZ + RFM |
| Users + subscription cycle + Churn | Subscription economy | LTV/Cohort + retention curves |
| view/cart/buy event chain | Attention/conversion economy | Funnel analysis + session mining |
| GMV + platform matchmaking | Commission economy | Two-sided network effects + unit economics |
| Assets + usage records | Rental economy | Asset utilization + revenue management |
| OHLCV price data | Financial time series | Technical analysis + volatility models |
| Job postings + skills + salary | Labor market | Skill premium + experience elasticity |

## Non-economic Data Support

| Data Type | Domain | Analysis Method |
|-----------|--------|-----------------|
| Sensor continuous data | Earth science | Time series decomposition, extreme value analysis |
| Network connection data | Social network | Centrality, community detection |
| Text corpus | NLP | Topic modeling, sentiment analysis |
| Image pixel data | Computer vision | Feature extraction, classification/clustering |

## Architecture

```
universal-data-analyst/
├── skill.yaml              # Skill definition and prompt templates
├── __init__.py             # Package entry point
├── main.py                 # Core data operations (V2 with optimizations)
├── llm_analyzer.py         # LLM prompt generator
├── orchestrator.py         # Workflow orchestrator (main entry point)
├── report_generator.py     # Report generator
├── layers/                 # Dependency layer
│   ├── data_loader.py      # Multi-format data loader
│   └── data_validator.py   # Data quality validator
├── example_usage.py        # Usage examples
├── quick_reference.md      # Quick reference card
└── README.md               # This file
```

## V2 Optimizations

Three key improvements over V1:

1. **LLM Step Decoupling + Autonomous Mode**
   - Each LLM step generates a standalone prompt file
   - Autonomous mode can infer ontology without external LLM
   - Supports human-in-the-loop at each step

2. **Multi-file / Multi-table Join Support**
   - Load multiple files simultaneously
   - Automatic join key detection
   - Join feasibility analysis report

3. **Quality-driven Strategy Adjustment**
   - Automatically evaluates data quality score (0-100)
   - Adjusts analysis strategy based on score
   - Provides targeted cleaning recommendations

## License

CC BY-NC-SA 4.0

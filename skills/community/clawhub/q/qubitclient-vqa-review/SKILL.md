---
name: qubitclient-vqa-review
description: "Quantum experiment VISUAL review and Question Answering (VQA) using Vision Language Models (VLM). Analyze experiment RESULT PLOTS to: (1) Describe plot types and axes, (2) Classify experiment outcomes (Expected/Suboptimal/Anomalous/Apparatus issue), (3) Scientific reasoning with next-step suggestions, (4) Assess fit reliability, (5) Extract physical parameters from plots, (6) Evaluate experiment status (SUCCESS/FAILURE). Note: Use tools for numerical fitting on RAW DATA. Supports 20+ experiment families including T1, T2, Rabi, Ramsey, spectroscopy, DRAG, pinchoff, and more."
license: GPL-3.0
---

## API Reference

### Installation

```bash
# Install qubitclient
pip install qubitclient[full]
```

### Quick Start

```python
from qubitclient.llm import QubitLLM
from qubitclient.llm.task import LLMTaskName

# Initialize LLM client
llm = QubitLLM()

# Run a task with an image
result = llm.run(
    LLMTaskName.DESCRIBE_PLOT,
    image_data="path/to/image.png",
    experiment_family=ExperimentFamily.T1
)
```

### Client Initialization

```python
from qubitclient.llm import QubitLLM, ExperimentFamily
from qubitclient.llm.task import LLMTaskName
```

### LLM Task Names (LLMTaskName)

| Task | Description |
|------|-------------|
| `DESCRIBE_PLOT` | Q1 - Describe chart type, axes, range, and main features |
| `CLASSIFY_OUTCOME` | Q2 - Classify experiment result as Expected/Suboptimal/Anomalous/Apparatus issue |
| `SCIENTIFIC_REASONING` | Q3 - Analyze physical meaning and suggest next steps |
| `ASSESS_FIT` | Q4 - Evaluate if data fitting is reliable for parameter extraction |
| `EXTRACT_PARAMS` | Q5 - Extract specified parameters from the chart |
| `EVALUATE_STATUS` | Q6 - Determine experiment success/failure status |

### Experiment Families (ExperimentFamily)

Supported experiment families for task-specific prompts:

```python
ExperimentFamily.T1                    # T1 relaxation time
ExperimentFamily.T1_FLUCTUATIONS       # T1 fluctuations
ExperimentFamily.T2FIT                 # T2 coherence time (not in QCalEval)
ExperimentFamily.RAMI                  # (not in QCalEval)
ExperimentFamily.RAB                   # (not in QCalEval)
ExperimentFamily.COUPLER_FLUX          # Coupler flux experiment
ExperimentFamily.CZ_BENCHMARKING       # CZ gate benchmarking
ExperimentFamily.DRAG                  # DRAG pulse optimization
ExperimentFamily.GMM                   # Gaussian mixture model
ExperimentFamily.MICROWAVE_RAMSEY      # Microwave Ramsey
ExperimentFamily.MOT_LOADING           # MOT loading
ExperimentFamily.PINCHOFF              # Pinchoff experiment
ExperimentFamily.PINGPONG              # Ping-pong experiment
ExperimentFamily.QUBIT_FLUX_SPECTROSCOPY   # Qubit flux spectroscopy
ExperimentFamily.QUBIT_SPECTROSCOPY        # Qubit spectroscopy
ExperimentFamily.QUBIT_SPECTROSCOPY_POWER_FREQUENCY  # Power-frequency spectroscopy
ExperimentFamily.RABI                  # Rabi oscillation
ExperimentFamily.RABI_HW               # Rabi hardware
ExperimentFamily.RAMSEY_CHARGE_TOMOGRAPHY   # Ramsey charge tomography
ExperimentFamily.RAMSEY_FREQ_CAL       # Ramsey frequency calibration
ExperimentFamily.RAMSEY_T2STAR         # Ramsey T2*
ExperimentFamily.RES_SPEC              # Resonator spectroscopy
ExperimentFamily.RYDBERG_RAMSEY        # Rydberg Ramsey
ExperimentFamily.RYDBERG_SPECTROSCOPY  # Rydberg spectroscopy
ExperimentFamily.TWEEZER_ARRAY         # Tweezer array
```

### Running Tasks

#### Get Prompt Only (for custom execution)

```python
# Get prompt data without running
prompt_data = llm.get_prompt(
    LLMTaskName.DESCRIBE_PLOT,
    image_data="path/to/image.png",
    experiment_family=ExperimentFamily.T1
)
# Returns: {"messages": [...], "images": [...], "response_schema": {...}}

# Execute with your own client
result = llm.chat(**prompt_data)
```

#### Run Task Directly

```python
# Run task and get result directly
result = llm.run(
    LLMTaskName.DESCRIBE_PLOT,
    image_data="path/to/image.png",
    experiment_family=ExperimentFamily.T1
)
# Returns parsed JSON result
```

### Image Input Formats

```python
# Single image path
image_data = "path/to/image.png"

# Multiple images
image_data = ["path/to/img1.png", "path/to/img2.png"]

# Image bytes
with open("image.png", "rb") as f:
    image_data = f.read()
```

### Fewshot Mode

Enable fewshot mode for improved accuracy with example images:

```python
result = llm.run(
    LLMTaskName.EXTRACT_PARAMS,
    image_data="path/to/image.png",
    experiment_family=ExperimentFamily.T1,
    fewshot=True  # Uses built-in examples for this experiment family
)
```

### Examples

#### Example 1: T1 Analysis - Describe Plot

```python
from qubitclient.llm import QubitLLM
from qubitclient.llm.task import LLMTaskName

llm = QubitLLM()

result = llm.run(
    LLMTaskName.DESCRIBE_PLOT,
    image_data="t1_decay.png",
    experiment_family=ExperimentFamily.T1
)
# Returns: {"plot_type": "line", "x_axis": "Delay (s)", "y_axis": "Population", ...}
```

#### Example 2: Classify Experiment Outcome

```python
result = llm.run(
    LLMTaskName.CLASSIFY_OUTCOME,
    image_data="rabi_oscillation.png",
    experiment_family=ExperimentFamily.RABI
)
# Returns: {"Classification": "Expected", "Confidence": 0.9, ...}
```

#### Example 3: Scientific Reasoning

```python
result = llm.run(
    LLMTaskName.SCIENTIFIC_REASONING,
    image_data="ramsey_fringe.png",
    experiment_family=ExperimentFamily.RAMSEY_T2STAR
)
# Returns: "The data shows clear oscillation with T2* decay..."
```

#### Example 4: Assess Fit Reliability

```python
result = llm.run(
    LLMTaskName.ASSESS_FIT,
    image_data="t1_fit.png",
    experiment_family=ExperimentFamily.T1
)
# Returns: {"Assessment": "Good", "R_squared": 0.98, ...}
```

#### Example 5: Extract Parameters

```python
result = llm.run(
    LLMTaskName.EXTRACT_PARAMS,
    image_data="t1_decay.png",
    experiment_family=ExperimentFamily.T1
)
# Returns: {"T1": 15.3e-6, "offset": 0.02, "amplitude": 0.98}
```

#### Example 6: Evaluate Experiment Status

```python
result = llm.run(
    LLMTaskName.EVALUATE_STATUS,
    image_data="t1_decay.png",
    experiment_family=ExperimentFamily.T1
)
# Returns: {"Status": "SUCCESS", "Notes": "Good T1 value within expected range"}
```

#### Example 7: Running Multiple Tasks on Same Image

```python
from qubitclient.llm.task import LLMTaskName

image_path = "experiment_result.png"

# Get prompts for each task
q1_prompt = llm.get_prompt(LLMTaskName.DESCRIBE_PLOT, image_data=image_path, experiment_family=ExperimentFamily.T1)
q2_prompt = llm.get_prompt(LLMTaskName.CLASSIFY_OUTCOME, image_data=image_path, experiment_family=ExperimentFamily.T1)
q3_prompt = llm.get_prompt(LLMTaskName.SCIENTIFIC_REASONING, image_data=image_path, experiment_family=ExperimentFamily.T1)
q4_prompt = llm.get_prompt(LLMTaskName.ASSESS_FIT, image_data=image_path, experiment_family=ExperimentFamily.T1)
q5_prompt = llm.get_prompt(LLMTaskName.EXTRACT_PARAMS, image_data=image_path, experiment_family=ExperimentFamily.T1)
q6_prompt = llm.get_prompt(LLMTaskName.EVALUATE_STATUS, image_data=image_path, experiment_family=ExperimentFamily.T1)

# Execute each task
q1_result = llm.chat(**q1_prompt)
q2_result = llm.chat(**q2_prompt)
q3_result = llm.chat(**q3_prompt)
q4_result = llm.chat(**q4_prompt)
q5_result = llm.chat(**q5_prompt)
q6_result = llm.chat(**q6_prompt)
```

### Configuration

The LLM client reads configuration from `qubitclient.utils.env_load`:

```python
# Environment variables or config file
OPENAI_API_KEY=your_api_key
OPENAI_BASE_URL=https://api.openai.com/v1  # optional, for custom endpoints
OPENAI_MODEL=gpt-4o  # default model
```

Or pass directly:

```python
llm = QubitLLM(
    api_key="your-key",
    base_url="https://api.openai.com/v1",
    model="gpt-4o"
)
```

### Streaming Response

```python
# Get streaming generator
prompt_data = llm.get_prompt(
    LLMTaskName.SCIENTIFIC_REASONING,
    image_data="image.png",
    experiment_family=ExperimentFamily.T1
)

for chunk in llm.chat(stream=True, **prompt_data):
    print(chunk, end="")
```

### Custom Model

```python
# Use different model for a specific call
result = llm.chat(
    messages=[{"role": "user", "content": "Describe this plot"}],
    images="image.png",
    model="gpt-4o-mini"  # override default model
)
```

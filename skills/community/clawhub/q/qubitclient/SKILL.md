---
name: qubitclient
description: |
  Unified quantum calibration analysis package. Aggregates curve fitting  and parameter extraction (qubitclient-scope), neural network spectrum analysis (qubitclient-nnscope), LLM-based calibration review (qubitclient-vqa-review), and MCP-based real-time measurement control (qubitclient-control).
license: GPL-3.0
---

## Overview

`qubitclient` is the unified Python package for quantum calibration data analysis. It combines traditional curve fitting, neural network analysis, LLM review, and real-time measurement control into a single, coherent system.

## Installation

```bash
# Basic installation
pip install 'qubitclient'

# Full installation (all features)
pip install 'qubitclient[full]'
```

**Requirements:** Python 3.10+

## Initialization

### Configuration File

Initialize configuration files in your project directory:

```bash
qubitclient init
```

This generates `qubitclient.json` and `.mcp.json` in the current directory.

**qubitclient.json structure:**

```json
{
  "url": "http://0.0.0.0:9801",
  "api_key": "your-proxy-api-key",
  "llm": {
    "api_key": "your-vllm-api-key",
    "base_url": "http://xx.xx.xx.xx:9091/v1",
    "model": "nv-community/Ising-Calibration-1-35B-A3B"
  },
  "generate": {
    "api_key": "your-vllm-api-key",
    "base_url": "http://xx.xx.xx.xx:9091/v1",
    "model": "Qwen/Qwen-Image-Edit"
  },
  "license": {
    "token": "your-license-token"
  }
}
```

| Field | Description | Required |
|-------|-------------|----------|
| `url` | QubitScope/NNScope server URL | Yes |
| `api_key` | Server authentication key | Yes |
| `llm.api_key` | VLLM API key for VQA review tasks | Yes |
| `llm.base_url` | VLLM server base URL | Yes |
| `llm.model` | Model name for VQA review | Yes |
| `generate.*` | Image generation model config | Optional |
| `license.token` | License token for cloud deployment authorization | Optional |

### Client Initialization

```python
from qubitclient import QubitScopeClient, QubitNNScopeClient

# Numerical fitting client (auto-loads qubitclient.json)
scope_client = QubitScopeClient()

# Neural network client
nn_client = QubitNNScopeClient()
```

## Sub-Skills

### qubitclient-scope

Numerical curve fitting and parameter extraction for quantum experiments.

**Key capabilities:**
- S21 peak detection (single/multi-peak)
- T1/T2 relaxation time fitting
- Rabi oscillation analysis
- DRAG pulse optimization
- Randomized Benchmarking (RB)
- Single-shot readout fidelity
- Power shift characterization

### qubitclient-nnscope

Neural network based analysis for spectrum and curve segmentation.

**Key capabilities:**
- S21 peak detection with deep learning
- 2D spectrum segmentation (COSINE, POLY curve types)
- S21 vs Flux parameter curve extraction
- Power shift curve segmentation

### qubitclient-vqa-review

LLM-powered visual question answering for quantum calibration results.

**Key capabilities:**
- Automated analysis review
- Calibration result interpretation
- Visual inspection of measurement data

### qubitclient-control

Real-time measurement control via MCP (Model Context Protocol).

**Key capabilities:**
- Live measurement streaming
- Parameter updates during measurement
- Automated calibration workflows

## Usage

```python
# Scope tasks (numerical fitting)
from qubitclient import QubitScopeClient, TaskName
client = QubitScopeClient()

# NNScope tasks (neural network)
from qubitclient import QubitNNScopeClient, NNTaskName, CurveType
nn_client = QubitNNScopeClient()

# MCP Control tasks
from qubitclient.ctrl import MCPClient
mcp_client = MCPClient()
```

## Task Categories

| Category | Module | Tasks |
|----------|--------|-------|
| Spectroscopy | scope / nnscope | S21PEAK, S21PEAKMULTI, SPECTRUM, SPECTRUM2D |
| Relaxation | scope | T1FIT, T2FIT, SPINECHO, T12DFIT |
| Pulse | scope | OPTPIPULSE, RABICOS, DRAG, TIMINGXYZ |
| Flux | scope / nnscope | S21VSFLUX, POWERSHIFT |
| Readout | scope | SINGLESHOT, OPTREADFREQ |
| Benchmarking | scope | RB, DELTA |
| Control | control | Real-time measurement control |
| Review | vqa-review | LLM-based analysis review |

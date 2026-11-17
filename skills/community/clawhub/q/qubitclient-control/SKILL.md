---
name: qubitclient-control
description: "Real-time quantum measurement control based on MCP (Model Context Protocol) for executing experimental tasks including: (1) S21 spectroscopy scans, (2) Rabi oscillation measurements, (3) Ramsey fringe experiments, (4) T1 relaxation time characterization, (5) T2 coherence time measurements, (6) DRAG pulse calibration, (7) Optimal π-pulse finding, (8) Power shift analysis, (9) Single-shot readout optimization, and (10) 2D spectrum acquisition. Provides unified control interface through langchain-mcp-adapters with support for parameter sweeps, data acquisition, and real-time feedback"
license: GPL-3.0
---

## API Reference

### Client Initialization

```python
# Using CtrlTaskName
from qubitclient.ctrl import QubitCtrlClient, CtrlTaskName
client = QubitCtrlClient()

# Using MCPClient directly
from qubitclient.ctrl import MCPClient
mcp = MCPClient(mcpServers=None)
```

### Task Names (CtrlTaskName)

- `S21` - S21 cavity frequency measurement
- `DRAG` - DRAG anti-crossing point measurement
- `DELTA` - Frequency offset calibration
- `OPTPIPULSE` - Optimal π-pulse measurement
- `POWERSHIFT` - Power shift curve measurement
- `RABI` - Rabi oscillation measurement
- `RAMSEY` - Ramsey interference measurement
- `S21VSFLUX` - S21 vs Flux measurement
- `SINGLESHOT` - Single-shot measurement
- `SPECTRUM` - Frequency spectrum analysis
- `SPECTRUM_2D` - 2D spectrum measurement
- `T1` - T1 relaxation time measurement

### Task Parameters and Examples

#### S21 - S21 Cavity Frequency Measurement

```python
from qubitclient.ctrl import QubitCtrlClient, CtrlTaskName

client = QubitCtrlClient()

result = client.run(
    task_type=CtrlTaskName.S21,
    qubits=["Q0", "Q1"],
    frequency_start=-40e6,      # -40 MHz
    frequency_end=40e6,         # +40 MHz
    frequency_sample_num=101,
    state=[0]                   # qubit state
)

# Result format:
# {
#   "data": {
#     "Q0": {
#       "frequency": [...],
#       "s21_real": [...],
#       "s21_imag": [...]
#     }
#   },
#   "parameters": {...}
# }
```

#### DRAG - DRAG Anti-crossing Point Measurement

```python
from qubitclient.ctrl import QubitCtrlClient, CtrlTaskName

result = client.run(
    task_type=CtrlTaskName.DRAG,
    qubits=["Q0"],
    lamb=[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
    stage=1,
    N_repeat=1,
    pulsePair=[0, 1],
    signal="population"         # or "iq_avg"
)

# Result format:
# {
#   "data": {
#     "Q0": {
#       "lamb": [...],
#       "population": [...],
#       "optimal_lamb": 0.5
#     }
#   }
# }
```

#### RABI - Rabi Oscillation Measurement

```python
from qubitclient.ctrl import QubitCtrlClient, CtrlTaskName

result = client.run(
    task_type=CtrlTaskName.RABI,
    qubits=["Q0"],
    drive_amp=np.linspace(0.1, 1.0, 50).tolist(),  # amplitude sweep
    width=30e-9,              # pulse width 30ns
    signal="iq_avg"           # or "population"
)
```

#### RAMSEY - Ramsey Interference Measurement

```python
from qubitclient.ctrl import QubitCtrlClient, CtrlTaskName

result = client.run(
    task_type=CtrlTaskName.RAMSEY,
    qubits=["Q0"],
    delta=20e6,               # detuning 20 MHz
    delay=10e-6,              # max delay 10 us
    stage=1,
    scale=15,
    signal="population"
)
```

#### T1 - T1 Relaxation Time Measurement

```python
from qubitclient.ctrl import QubitCtrlClient, CtrlTaskName
import numpy as np

result = client.run(
    task_type=CtrlTaskName.T1,
    qubits=["Q0"],
    delay=np.linspace(0, 20e-6, 51).tolist(),  # 0-20us delay sweep
    signal="population"      # or "iq_avg"
)
```

#### OPTPIPULSE - Optimal π-pulse Finding

```python
from qubitclient.ctrl import QubitCtrlClient, CtrlTaskName
import numpy as np

result = client.run(
    task_type=CtrlTaskName.OPTPIPULSE,
    qubits=["Q0"],
    stage=1,
    N_list=[1, 3, 5],         # pulse numbers
    amp_list=np.linspace(0.5, 1.5, 51).tolist(),  # amplitude sweep
    delay=20e-9,              # pulse spacing
    signal="population"
)
```

#### DELTA - Frequency Offset Calibration

```python
from qubitclient.ctrl import QubitCtrlClient, CtrlTaskName
import numpy as np

result = client.run(
    task_type=CtrlTaskName.DELTA,
    qubits=["Q0"],
    N_list=[1, 5, 13],        # pulse sequence lengths
    delta_list=(np.linspace(-20, 20, 101) * 1e6).tolist(),  # freq offset sweep
    stage=1,
    delay=20e-9
)
```

#### POWERSHIFT - Power Shift Measurement

```python
from qubitclient.ctrl import QubitCtrlClient, CtrlTaskName

result = client.run(
    task_type=CtrlTaskName.POWERSHIFT,
    qubits=["Q0"],
    power=[0.01, 0.02, 0.05, 0.1, 0.2, 0.5],  # power levels
    freq=[5.0e9, 5.1e9, 5.2e9]  # frequency points
)
```

#### S21VSFLUX - S21 vs Flux Measurement

```python
from qubitclient.ctrl import QubitCtrlClient, CtrlTaskName
import numpy as np

result = client.run(
    task_type=CtrlTaskName.S21VSFLUX,
    qubits_scan=["Q0"],        # qubit to flux tune
    read_bias=np.linspace(-0.5, 0.5, 51).tolist(),  # bias sweep
    freq=np.linspace(4e9, 6e9, 101).tolist(),  # frequency sweep
    qubits_read=["Q0"]         # qubit to read
)
```

#### SINGLESHOT - Single-shot Readout

```python
from qubitclient.ctrl import QubitCtrlClient, CtrlTaskName

result = client.run(
    task_type=CtrlTaskName.SINGLESHOT,
    qubits=["Q0"],
    stage=1
)
```

#### SPECTRUM - Frequency Spectrum Measurement

```python
from qubitclient.ctrl import QubitCtrlClient, CtrlTaskName
import numpy as np

result = client.run(
    task_type=CtrlTaskName.SPECTRUM,
    qubits=["Q0"],
    freq=np.linspace(4e9, 6e9, 201).tolist(),  # frequency sweep
    drive_amp=0.04,           # drive amplitude
    duration=40e-6,           # pulse duration
    from_idle=True,           # start from idle state
    absolute=True,            # absolute frequency
    signal="iq_avg"           # or "population"
)
```

#### SPECTRUM_2D - 2D Spectrum Measurement

```python
from qubitclient.ctrl import QubitCtrlClient, CtrlTaskName
import numpy as np

result = client.run(
    task_type=CtrlTaskName.SPECTRUM_2D,
    qubits=["Q0"],
    drive_amp=0.05,
    duration=40e-6,
    freq=np.linspace(4e9, 6e9, 101).tolist(),
    bias=np.linspace(-0.5, 0.5, 51).tolist(),
    from_idle=False,
    absolute=True
)
```

### Using MCPClient Directly

```python
from qubitclient.ctrl import MCPClient

mcp = MCPClient(mcpServers=None)

# Call tasks directly by name
result = mcp.call("s21", {
    "qubits": ["Q0", "Q1"],
    "frequency_start": -40e6,
    "frequency_end": 40e6,
    "frequency_sample_num": 101
})

result = mcp.call("rabi", {
    "qubits": ["Q0"],
    "drive_amp": [0.1, 0.2, 0.3, 0.4, 0.5],
    "width": 30e-9,
    "signal": "iq_avg"
})
```

### Common Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `qubits` | list[str] | List of qubit identifiers, e.g., ["Q0", "Q1"] |
| `task_type` | CtrlTaskName | Task type enumeration |
| `stage` | int | Measurement stage (default: 1) |
| `signal` | str | Output signal type: "population" or "iq_avg" |

### Application Scenarios

- **S21** - Determine qubit resonance frequency, measure cavity quality factor
- **DRAG** - Optimize single-qubit gate fidelity, reduce leakage errors
- **RABI** - Calibrate pulse amplitude for π rotation
- **RAMSEY** - Measure qubit coherence, determine T2* time
- **T1** - Characterize energy relaxation time
- **OPTPIPULSE** - Find optimal pulse amplitude for specific gate
- **SPECTRUM_2D** - Map 2D frequency-bias spectrum for avoided crossings
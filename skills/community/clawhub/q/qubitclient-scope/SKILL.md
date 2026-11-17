---
name: qubitclient-scope
description: Quantum experiment NUMERICAL curve fitting and parameter extraction. Support for (1) S21 peak detection (single/multi), (2) Optimal π-pulse calibration, (3) Rabi oscillation analysis, (4) T1/T2 relaxation time fitting, (5) DRAG pulse optimization, (6) Power shift characterization, (7) Ramsey fringe analysis, (8) Single-shot readout fidelity, (9) 2D spectrum analysis, (10) Spin Echo T2 fitting, (11) Randomized Benchmarking, (12) XYZ Timing calibration, (13) 2D T1 fitting, (14) Optimal readout frequency, (15) Delta experiment. Provides unified API for curve fitting, parameter extraction, and batch processing with matplotlib/plotly visualization support.
license: GPL-3.0
---

## Overview

Scope is a traditional numerical curve fitting module for quantum experiment analysis. It provides comprehensive parameter extraction tasks including peak detection, relaxation time fitting (T1/T2), oscillation analysis (Rabi, Ramsey), pulse optimization (DRAG), and 2D spectrum analysis. Unlike neural network-based approaches, Scope uses classical fitting algorithms for interpretable results.

## API Reference

### Client Initialization

```python
# Scope tasks (curve fitting & analysis)
from qubitclient import QubitScopeClient, TaskName
client = QubitScopeClient()
```

### Task Names

#### Scope Tasks (TaskName)
| TaskName | Description |
|----------|-------------|
| `S21PEAK` | Single peak detection with confidence score |
| `S21PEAKMULTI` | Multi-peak detection across full frequency range |
| `OPTPIPULSE` | Optimal π-pulse calculation |
| `RABICOS` | Rabi oscillation cosine first peak detection |
| `RAMSEY` | Ramsey fringe decay oscillation fitting |
| `S21VSFLUX` | S21 vs Flux analysis |
| `SINGLESHOT` | Single-shot readout analysis |
| `SPECTRUM` | Frequency spectrum analysis (AMPD algorithm) |
| `T1FIT` | T1 relaxation time exponential fitting |
| `T2FIT` | T2 coherence time fitting (Gaussian + exponential decay + cosine oscillation) |
| `SPINECHO` | Spin Echo T2 relaxation time fitting |
| `SPECTRUM2D` | 2D spectrum curve segmentation |
| `POWERSHIFT` | Power shift curve analysis |
| `DRAG` | DRAG anti-crossing point analysis |
| `RB` | Randomized benchmarking fidelity test |
| `DELTA` | Delta optimization experiment |
| `T12DFIT` | 2D T1 relaxation time fitting |
| `TIMINGXYZ` | XYZ Timing calibration analysis |
| `OPTREADFREQ` | Optimal readout frequency selection |

### Data Input Formats

The input data should be a dictionary or list of dictionaries with the following structure:

```python
dict_list = [{
    "image": {
        "Q0": [x_data, y_data],  # or [x_data, y_data, z_data] for 2D
        "Q1": [x_data, y_data],
    }
} ...]  # One or more data items
```

**Note:** Multiple data items are supported - pass a list of dictionaries. The output `results` list has one entry per input item, in the same order.

### Task-Specific Formats

#### S21PEAK / S21PEAKMULTI

**Input:**
```python
{
    "image": {
        "Q0": [x_array, amp_array, phi_array],  # (freq, amplitude, phase)
        "Q1": [x_array, amp_array, phi_array],
    },
}
```
- `x_array`: 1D frequency array, shape (A,)
- `amp_array`: 1D amplitude array (magnitude of complex S21), shape (A,)
- `phi_array`: 1D phase array (unwrapped, detrended), shape (A,)

**Output:**
```json
{
  "type": "s21peak",
  "results": [{
    "peaks": [[int, ...], [int, ...]],              // Peak indices per qubit
    "confs": [[float, ...], [float, ...]],          // Confidence scores per peak
    "freqs_list": [[float, ...], [float, ...]],     // Peak frequencies per qubit
    "status": "success" | "failed"
  }]
}
```

---

#### OPTPIPULSE

**Input:**
```python
{
    "image": {
        "Q0": [waveforms_array, x_array],  // (2D waveform data, 1D time axis)
        "Q1": [waveforms_array, x_array],
    }
}
```
- `waveforms_array`: 2D array of shape (n_waveforms, n_points)
- `x_array`: 1D array of time values

Supported data keys: `population`, `iq_avg`, `iq`

**Output:**
```json
{
  "type": "optpipulse",
  "results": [{
    "params": [[float, ...], [float, ...]],   // Co-peak time positions per qubit
    "confs": [[float, ...], [float, ...]],    // Confidence scores per peak
    "status": "success" | "failed"
  }]
}
```

---

#### RABICOS

**Input:**
```python
{
    "image": {
        "Q0": [x_array, amp_array],  // (drive amplitude, amplitude)
        "Q1": [x_array, amp_array],
    }
}
```
- `x_array`: 1D array of drive amplitude values
- `amp_array`: 1D array of measured amplitude

**Output:**
```json
{
  "type": "rabicos",
  "results": [{
    "peaks": [[float, ...], [float, ...]],    // First peak time positions per qubit
    "confs": [[float, ...], [float, ...]],    // Confidence scores per peak
    "status": "success" | "failed"
  }]
}
```

---

#### T1FIT

**Input:**
```python
{
    "image": {
        "Q0": [delay_array, amp_array],  // (time delays, measured populations)
        "Q1": [delay_array, amp_array],
    }
}
```
- `delay_array`: 1D array of delay times (seconds)
- `amp_array`: 1D array of measured amplitude/population values

Fitting formula: $y = A \cdot e^{-x / T1} + B$

Supported data keys: `population`, `iq_avg`, `iq`

**Output:**
```json
{
  "type": "t1fit",
  "results": [{
    "params_list": [[A, T1, B], [A, T1, B], ...],  // Fitting params per qubit
    "r2_list": [float, float, ...],                  // R² goodness of fit
    "fit_data_list": [[float, ...], [float, ...]],  // Fitted curve values
    "status": "success" | "failed"
  }]
}
```
- `A`: Initial amplitude
- `T1`: Relaxation time (µs)
- `B`: Baseline offset

---

#### T2FIT

**Input:**
```python
{
    "image": {
        "Q0": [delay_array, amp_array],  // (time delays, measured amplitudes)
        "Q1": [delay_array, amp_array],
    }
}
```
- `delay_array`: 1D array of delay times (seconds)
- `amp_array`: 1D array of measured amplitude values

Fitting formula: $y = A \cdot e^{-(x/T2)^2 - x/T1/2} \cdot \cos(2\pi w x + \phi) + B$

**Output:**
```json
{
  "type": "t2fit",
  "results": [{
    "params_list": [[A, B, T1, T2, w, phi], ...],  // Fitting params per qubit
    "r2_list": [float, float, ...],                  // R² goodness of fit
    "fit_data_list": [[float, ...], [float, ...]],  // Fitted curve values (dense points)
    "status": "success" | "failed"
  }]
}
```
- `A`: Initial amplitude
- `B`: Baseline offset
- `T1`: Exponential decay time (µs)
- `T2`: Gaussian decay time (µs)
- `w`: Oscillation angular frequency (rad/s)
- `phi`: Initial phase (rad)

---

#### RAMSEY

**Input:**
```python
{
    "image": {
        "Q0": [delay_array, amp_array],  // (time delays, measured amplitudes)
        "Q1": [delay_array, amp_array],
    }
}
```
- `delay_array`: 1D array of delay times (seconds)
- `amp_array`: 1D array of measured amplitude values

Fitting formula: $y = A \cdot e^{-x/T1} \cdot \cos(2\pi w x + \phi) + B$

**Output:**
```json
{
  "type": "ramsey",
  "results": [{
    "params_list": [[A, B, T1, w, phi], ...],  // Fitting params per qubit
    "r2_list": [float, float, ...],                  // R² goodness of fit
    "fit_data_list": [[float, ...], [float, ...]],  // Fitted curve values
    "fit_data_dense_list": [[float, ...], [float, ...]],  // Fitted curve at dense points
    "x_dense_list": [[float, ...], [float, ...]],         // Dense time axis
    "status": "success" | "failed"
  }]
}
```
- `A`: Initial amplitude
- `B`: Baseline offset
- `T1`: Exponential decay time (µs)
- `w`: Oscillation angular frequency (rad/s)
- `phi`: Initial phase (rad)

---

#### SPINECHO

**Input:**
```python
{
    "image": {
        "Q0": [delay_array, amp_array],  // (delay times, signal amplitudes)
        "Q1": [delay_array, amp_array],
    }
}
```

**Output:**
```json
{
  "type": "spinecho",
  "results": [{
    "status": "success" | "failed",
    "Q0": {
      "q_name": "Q0",                // Qubit name
      "x": [float, ...],             // Delay time sequence
      "amp": [float, ...],           // Raw signal amplitudes
      "envelope": [float, ...],      // Extracted envelope curve
      "fit_envelope": [float, ...],  // Fitted envelope curve
      "params": [float, ...],        // Fitting parameters
      "T2": float,                   // Spin Echo T2 time (µs)
      "r2": float,                   // R² goodness of fit
      "success": true | false        // Per-qubit fitting success
    },
    "Q1": { ... }
  }]
}
```

---

#### DRAG

**Input:**
```python
{
    "image": {
        "Q0": [lamb_array, y_array],  // (lambda parameter, 2D population data)
        "Q1": [lamb_array, y_array],
    }
}
```
- `lamb_array`: 1D array of DRAG λ values
- `y_array`: 2D array of shape (2, n_lambda) for both states

**Output:**
```json
{
  "type": "drag",
  "results": [{
    "x_pred_list": [[float, ...], [float, ...]],           // Fitted curve x values
    "y0_pred_list": [[float, ...], [float, ...]],          // Fitted curve 0 y values
    "y1_pred_list": [[float, ...], [float, ...]],          // Fitted curve 1 y values
    "intersections_list": [[[x, y], ...], [[x, y], ...]],  // Intersection points per qubit
    "intersections_confs_list": [[float, ...], [float, ...]], // Confidence per intersection
    "status": "success" | "failed"
  }]
}
```

---

#### RB (Randomized Benchmarking)

**Input:**
```python
{
    "image": {
        "Q0": [cycle_array, [amp_array, other_amp_array]],
        "Q1": [cycle_array, [amp_array, other_amp_array]],
    }
}
```
- `cycle_array`: 1D array of Clifford cycle numbers
- `amp_array`: 1D array of survival probabilities
- `other_amp_array`: reference array

Fitting formula: $P(x) = A \cdot p^x + B$

**Output:**
```json
{
  "type": "rb",
  "results": [{
    "params_list": [[A, p, B], [A, p, B], ...],   // Fitting params per qubit
    "r2_list": [float, float, ...],                 // R² goodness of fit
    "fit_data_list": [[float, ...], [float, ...]], // Fitted curve values
    "status": "success" | "failed"
  }]
}
```
- `A`: Initial amplitude
- `p`: Decay factor (closer to 1 = higher fidelity)
- `B`: Baseline offset

---

#### S21VSFLUX

**Input:**
```python
{
    "image": {
        "Q0": [freq_array, volt_array, s_matrix],  // tuple, length >= 3
        "Q1": [freq_array, volt_array, s_matrix],
    },
}
```
- `freq_array`: 1D array of frequency values, shape (A,)
- `volt_array`: 1D array of voltage/bias values, shape (B,)
- `s_matrix`: 2D array of S21 values, shape (B, A)

**Output:**
```json
{
  "type": "s21vsflux",
  "results": [{
    "coscurves_list": [[[[volt, freq], ...], ...], ...],  // Cosine curve points
    "cosconfs_list": [[float, ...], [float, ...]],         // Cosine confidence scores
    "lines_list": [[[[volt, freq], ...], ...], ...],       // Line curve points
    "lineconfs_list": [[float, ...], [float, ...]],        // Line confidence scores
    "status": "success" | "failed"
  }]
}
```

---

#### SPECTRUM2D

**Input:**
```python
{
    "image": {
        "Q0": [iq_avg, bias_array, freq_array],  // tuple, length = 3
        "Q1": [iq_avg, bias_array, freq_array],
    },
}
```
- `iq_avg`: 2D complex array of shape (B, A)
- `bias_array`: 1D array of bias values, shape (A,)
- `freq_array`: 1D array of frequency values, shape (B,)

Supported data keys: `iq_avg`, `population`, `iq`

**Output:**
```json
{
  "type": "spectrum2d",
  "results": [{
    "params": [[[[volt, freq], ...], ...], ...],           // Cosine curve points
    "confs": [[float, ...], [float, ...]],                  // Cosine confidence scores
    "coscompress_list": [[float, ...], [float, ...]],       // Cosine compression ratios
    "lines_list": [[[[volt, freq], ...], ...], ...],        // Line curve points
    "lineconfs_list": [[float, ...], [float, ...]],         // Line confidence scores
    "status": "success" | "failed"
  }]
}
```

---

#### SPECTRUM

**Input:**
```python
{
    "image": {
        "Q0": [freq_array, s_array],  // 1D spectrum
        "Q1": [freq_array, s_array],
    }
}
```
- `freq_array`: 1D array of frequency values
- `s_array`: 1D array of spectral amplitude

Uses AMPD algorithm for peak detection.

**Output:**
```json
{
  "type": "spectrum",
  "results": [{
    "peaks_list": [[float, ...], [float, ...], ...],           // Peak positions per qubit
    "confidences_list": [[float, ...], [float, ...], ...],     // Confidence per peak
    "mean_cut_widths_list": [[float, ...], [float, ...], ...], // Peak widths per qubit
    "status": "success" | "failed"
  }]
}
```

---

#### POWERSHIFT

**Input:**
```python
{
    "image": {
        "Q0": [freq_array, amp_array, value_array],  // (x, y, value)
        "Q1": [freq_array, amp_array, value_array],
    }
}
```
- `freq_array`: 1D array, shape (B,) - frequency axis
- `amp_array`: 1D array, shape (A,) - amplitude axis
- `value_array`: 2D array, shape (A, B) - complex IQ values

**Output:**
```json
{
  "type": "powershift",
  "results": [{
    "q_list": [int, int, ...],                              // Qubit indices
    "keypoints_list": [[[x, y], ...], [[x, y], ...], ...], // Keypoints per qubit
    "confs": [float, float, ...],                            // Confidence scores
    "class_num_list": [int, int, ...],                       // Class numbers (1-5)
    "status": "success" | "failed"
  }]
}
```
- **Class 1**: Vertical to x-axis
- **Class 2**: Both ends vertical, middle inclined
- **Class 3**: Only bottom vertical, then inclined
- **Class 4**: Entirely inclined upward
- **Class 5**: No information

---

#### SINGLESHOT

**Input:**
```python
{
    "image": {
        "Q0": [s0_array, s1_array, False],  // (ground state IQ, excited state IQ, reserved)
        "Q1": [s0_array, s1_array, False],
    }
}
```
- `s0_array`: 1D complex array for |0⟩ state, shape (A,)
- `s1_array`: 1D complex array for |1⟩ state, shape (A,)

**Output:**
```json
{
  "type": "singleshot",
  "results": [{
    "sep_score_list": [float, float, ...],                              // Separation scores
    "threshold_list": [float, float, ...],                              // Classification thresholds
    "phi_list": [float, float, ...],                                    // Best projection angles
    "signal_list": [[[float, ...], [float, ...]], ...],                 // Signal projections
    "idle_list": [[[float, ...], [float, ...]], ...],                   // Idle signal projections
    "params_list": [[[float, ...], [float, ...]], ...],                 // Ellipse fitting params
    "std_list": [[std0, std1, var0, var1, cov01, [[cov00, cov01], [cov10, cov11]]], ...],
    "cdf_list": [[[float, ...], [float, ...]], ...],                    // CDF data
    "status": "success" | "failed"
  }]
}
```

---

#### T12DFIT (2D T1 Fitting)

**Input:**
```python
{
    "image": {
        "Q0": [p_array, delay_array, zpa_array],  // (probability, delay, zpa)
        "Q1": [p_array, delay_array, zpa_array],
    }
}
```
- `p_array`: 2D array of shape (A, B) - probability data
- `delay_array`: 1D array of shape (B,) - delay times
- `zpa_array`: 1D array of shape (A,) - pulse amplitudes

Fitting formula per ZPA: $y = A \cdot e^{-x / T1} + B$

**Output:**
```json
{
  "type": "t12dfit",
  "results": [{
    "t1_list": [[float, float, ...], [float, float, ...], ...],  // T1 values per ZPA per qubit
    "zpa_list": [[float, float, ...], [float, float, ...], ...], // ZPA values per qubit
    "status": "success" | "failed"
  }]
}
```

---

#### TIMINGXYZ (XYZ Timing Calibration)

**Input:**
```python
{
    "image": {
        "Q0": [amp_array, delay_array],  // (signal amplitude, delay time)
        "Q1": [amp_array, delay_array],
    }
}
```
- `amp_array`: 1D array of signal amplitudes
- `delay_array`: 1D array of delay times (seconds)

**Output:**
```json
{
  "type": "xyz_timing",
  "results": [{
    "status": "success" | "failed",
    "Q0": {
      "q_name": "Q0",            // Qubit name
      "x": [float, ...],         // Delay time sequence
      "amp": [float, ...],       // Raw signal amplitudes
      "fit_data": [float, ...],  // Erf fitted curve values
      "params": [float, ...],    // Fitting parameters
      "zd_xy": float,            // Timing offset (ns)
      "r2": float,               // R² goodness of fit
      "success": true | false    // Per-qubit fitting success
    },
    "Q1": { ... }
  }]
}
```

---

#### OPTREADFREQ (Optimal Readout Frequency)

**Input:**
```python
{
    "image": {
        "Q0": [freq_array, s0_array, s1_array],  // (frequency, s21_curve0, s21_curve1)
        "Q1": [freq_array, s0_array, s1_array],
    }
}
```
- `freq_array`: 1D array of frequency values
- `s0_array`: 1D array of first S21 curve
- `s1_array`: 1D array of second S21 curve

**Output:**
```json
{
  "type": "optreadfreq",
  "results": [{
    "peak_list": [int, int, ...],  // Peak indices per qubit
    "status": "success" | "failed"
  }]
}
```

---

#### DELTA

**Input:**
```python
{
    "image": {
        "Q0": [waveforms_array, x_array],  // (2D waveform data, 1D bias/frequency axis)
        "Q1": [waveforms_array, x_array],
    }
}
```
- `waveforms_array`: 2D array of shape (N_waveforms, M), scan waveforms
- `x_array`: 1D array of shape (M,), bias/frequency axis

**Output:**
```json
{
  "type": "delta",
  "results": [{
    "params": [[float, ...], [float, ...], ...],  // Delta peak positions per qubit
    "confs": [[float, ...], [float, ...], ...],   // Confidence scores per peak
    "status": "success" | "failed"
  }]
}
```
- `params[i]`: Peak positions for qubit i (empty list if no peaks)
- `confs[i]`: Confidence scores corresponding to each peak in `params[i]`

### Getting Results

```python
# Get raw (unfiltered) results
results = client.get_result(response=response)

# Get filtered results by confidence threshold (for tasks with confidence scores)
results_filtered = client.get_result(response, threshold=0.5, task_type=TaskName.S21PEAK.value)
```

### Visualization

```python
from qubitclient.draw.plymanager import QuantumPlotPlyManager
from qubitclient.draw.pltmanager import QuantumPlotPltManager

ply_manager = QuantumPlotPlyManager()
plt_manager = QuantumPlotPltManager()

for idx, (result, dict_param) in enumerate(zip(results, dict_list)):
    save_path = f"./result_{idx}"
    plt_manager.plot_quantum_data(
        data_type='npy',
        task_type=TaskName.S21PEAK.value,
        save_path=save_path + ".png",
        result=result,
        dict_param=dict_param
    )
```

### Examples

#### S21 Peak Detection

```python
from qubitclient import QubitScopeClient, TaskName
import numpy as np

client = QubitScopeClient()

# Prepare data: frequency, amplitude, phase
freq = np.linspace(4e9, 6e9, 201)
iq_avg = np.random.randn(201) + 1j * np.random.randn(201)
amp = np.abs(iq_avg)
phi = np.unwrap(np.angle(iq_avg))

dict_list = [{
    "image": {
        "Q0": [freq, amp, phi]
    },
}]

response = client.request(file_list=dict_list, task_type=TaskName.S21PEAK)
results = client.get_result(response=response)
# Returns: [{"peaks": [[10],[22]], "confs": [[0.3],[0.6]], "freqs_list": [[0.3e9],[0.6e9]], "status": "success"}]
```

#### T1 Fitting

```python
from qubitclient import QubitScopeClient, TaskName
import numpy as np

client = QubitScopeClient()

# T1 decay data
delay = np.array([0, 1e-6, 2e-6, 5e-6, 10e-6, 20e-6, 50e-6])
population = np.array([1.0, 0.85, 0.72, 0.45, 0.20, 0.04, 0.01])

dict_list = [{
    "image": {
        "Q0": [delay, population]
    }
}]

response = client.request(file_list=dict_list, task_type=TaskName.T1FIT)
results = client.get_result(response=response)
# Returns: {"type": "t1fit", "results": [{"params_list": [[A, T1, B], ...], "r2_list": [...], "fit_data_list": [...], "status": "success"}]}
```

#### T2 Fitting

```python
from qubitclient import QubitScopeClient, TaskName
import numpy as np

client = QubitScopeClient()

# T2 decay data with oscillation
delay = np.linspace(0, 10e-6, 101)
# Simulated decay + oscillation signal
t2_signal = 0.5 * np.exp(-(delay/2e-6)**2 - delay/20e-6) * np.cos(2*np.pi*1e8*delay) + 0.5

dict_list = [{
    "image": {
        "Q0": [delay, t2_signal]
    }
}]

response = client.request(file_list=dict_list, task_type=TaskName.T2FIT)
results = client.get_result(response=response)
# Returns: {"type": "t2fit", "results": [{"params_list": [[A, B, T1, T2, w, phi], ...], "r2_list": [...], "fit_data_list": [...], "status": "success"}]}
```

#### RAMSEY

```python
from qubitclient import QubitScopeClient, TaskName
import numpy as np

client = QubitScopeClient()

# Ramsey decay data with oscillation
delay = np.linspace(0, 10e-6, 101)
# Simulated exponential decay + oscillation signal (no Gaussian term)
ramsey_signal = 0.5 * np.exp(-delay/5e-6) * np.cos(2*np.pi*1e8*delay) + 0.5

dict_list = [{
    "image": {
        "Q0": [delay, ramsey_signal]
    }
}]

response = client.request(file_list=dict_list, task_type=TaskName.RAMSEY)
results = client.get_result(response=response)
# Returns: {"type": "ramsey", "results": [{"params_list": [[A, B, T1, w, phi], ...], "r2_list": [...], "fit_data_list": [...], "fit_data_dense_list": [...], "x_dense_list": [...], "status": "success"}]}
```

#### DRAG Analysis

```python
from qubitclient import QubitScopeClient, TaskName
import numpy as np

client = QubitScopeClient()

# DRAG lambda scan data
lamb = np.array([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
# y: 2D array [2, n_lambda] - population for both states
y = np.array([
    [0.95, 0.92, 0.88, 0.85, 0.82, 0.80, 0.82, 0.85, 0.88, 0.91, 0.94],  # state 0
    [0.05, 0.08, 0.12, 0.15, 0.18, 0.20, 0.18, 0.15, 0.12, 0.09, 0.06]   # state 1
])

dict_list = [{
    "image": {
        "Q0": [lamb, y]
    }
}]

response = client.request(file_list=dict_list, task_type=TaskName.DRAG)
results = client.get_result(response=response)
# Returns intersection points and confidence scores
```

#### Spin Echo T2 Fitting

```python
from qubitclient import QubitScopeClient, TaskName
import numpy as np

client = QubitScopeClient()

# Spin Echo data
delay = np.array([0, 50, 100, 150, 200, 250, 300])  # microseconds
signal = np.array([0.95, 0.82, 0.71, 0.63, 0.55, 0.48, 0.42])

dict_list = [{
    "image": {
        "Q0": [delay, signal]
    }
}]

response = client.request(file_list=dict_list, task_type=TaskName.SPINECHO)
results = client.get_result(response=response)
# Returns: {"type": "spinecho", "results": [{"status": "success", "Q0": {"x": [...], "amp": [...], "fit_envelope": [...], "T2": float, "r2": float}}]}
```

#### Randomized Benchmarking (RB)

```python
from qubitclient import QubitScopeClient, TaskName
import numpy as np

client = QubitScopeClient()

# RB data
cycles = np.array([0, 10, 20, 40, 80, 160, 320])
survival = np.array([1.0, 0.95, 0.90, 0.82, 0.68, 0.45, 0.20])

dict_list = [{
    "image": {
        "Q0": [cycles, [survival, np.zeros_like(survival)]]
    }
}]

response = client.request(file_list=dict_list, task_type=TaskName.RB)
results = client.get_result(response=response)
# Returns: {"type": "rb", "results": [{"params_list": [[A, p, B], ...], "r2_list": [...], "fit_data_list": [...], "status": "success"}]}
```

#### Single-Shot Readout

```python
from qubitclient import QubitScopeClient, TaskName
import numpy as np

client = QubitScopeClient()

# Single-shot IQ data for |0> and |1> states
s0 = np.random.randn(1000) + 1j * np.random.randn(1000)  # ground state
s1 = np.random.randn(1000) + 1j * np.random.randn(1000)  # excited state

dict_list = [{
    "image": {
        "Q0": [s0, s1, False]
    }
}]

response = client.request(file_list=dict_list, task_type=TaskName.SINGLESHOT)
results = client.get_result(response=response)
# Returns separation score, threshold, projection angle, and ellipse parameters
```

#### 2D T1 Fitting (T12DFIT)

```python
from qubitclient import QubitScopeClient, TaskName
import numpy as np

client = QubitScopeClient()

# 2D T1 data: p_array (zpa, delay), delay_array, zpa_array
zpa = np.array([0.4, 0.6, 0.8, 1.0])
delay = np.array([0, 1e-6, 2e-6, 5e-6, 10e-6])
p = np.array([
    [1.0, 0.85, 0.72, 0.45, 0.20],  # zpa=0.4
    [1.0, 0.80, 0.65, 0.40, 0.15],  # zpa=0.6
    [1.0, 0.75, 0.58, 0.35, 0.12],  # zpa=0.8
    [1.0, 0.70, 0.50, 0.30, 0.10],  # zpa=1.0
])

dict_list = [{
    "image": {
        "Q0": [p, delay, zpa]
    }
}]

response = client.request(file_list=dict_list, task_type=TaskName.T12DFIT)
results = client.get_result(response=response)
# Returns: {"type": "t12dfit", "results": [{"t1_list": [[T1_zpa0, T1_zpa1, ...]], "zpa_list": [[0.4, 0.6, 0.8, 1.0]], "status": "success"}]}
```

#### XYZ Timing Calibration

```python
from qubitclient import QubitScopeClient, TaskName
import numpy as np

client = QubitScopeClient()

# XYZ timing data
delay = np.array([-6e-8, -4e-8, -2e-8, 0.0, 2e-8, 4e-8, 6e-8])
signal = np.array([0.42, 0.55, 0.78, 0.95, 0.81, 0.60, 0.45])

dict_list = [{
    "image": {
        "Q0": [signal, delay]
    }
}]

response = client.request(file_list=dict_list, task_type=TaskName.TIMINGXYZ)
results = client.get_result(response=response)
# Returns: {"type": "xyz_timing", "results": [{"status": "success", "Q0": {"x": [...], "amp": [...], "fit_data": [...], "zd_xy": float, "r2": float}}]}
```

#### Optimal Readout Frequency

```python
from qubitclient import QubitScopeClient, TaskName
import numpy as np

client = QubitScopeClient()

# Readout frequency optimization data
freq = np.linspace(4e9, 6e9, 201)
s0 = np.abs(1 / (freq - 5e9 + 0.1e9j))  # S21 for |0> state
s1 = np.abs(1 / (freq - 5e9 - 0.1e9j))  # S21 for |1> state

dict_list = [{
    "image": {
        "Q0": [freq, s0, s1]
    }
}]

response = client.request(file_list=dict_list, task_type=TaskName.OPTREADFREQ)
results = client.get_result(response=response)
# Returns: {"type": "optreadfreq", "results": [{"peak_list": [index], "status": "success"}]}
```
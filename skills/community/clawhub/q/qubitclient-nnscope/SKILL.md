---
name: qubitclient-nnscope
description: "NNScope neural network based quantum spectrum analysis tasks: (1) S21PEAK - S21 peak detection with confidence scoring, (2) S21PEAKMULTI - Multi-peak detection across full frequency range, (3) SPECTRUM - Spectrum peak region analysis (start/end/width/confidence), (4) SPECTRUM2D - 2D spectrum curve segmentation with polynomial/cosine fitting, (5) S21VSFLUX - S21 vs Flux curve segmentation, (6) POWERSHIFT - Power shift curve segmentation. Provides unified API for neural network based curve fitting, peak detection, and batch processing with matplotlib/plotly visualization support."
license: GPL-3.0
---

## Overview

NNScope is a neural network-based quantum spectrum analysis module that provides advanced curve segmentation, peak detection, and parameter extraction tasks. Unlike traditional scope fitting tasks, NNScope uses deep learning models for more robust analysis on complex spectral data.

## API Reference

### Client Initialization

```python
from qubitclient import QubitNNScopeClient, NNTaskName
from qubitclient.nnscope.nnscope_api.curve.curve_type import CurveType

client = QubitNNScopeClient()
```

### Task Names (NNTaskName)

| Task | Description |
|------|-------------|
| `S21PEAK` | S21 peak detection with confidence scoring |
| `S21PEAKMULTI` | Multi-peak detection across full frequency range |
| `SPECTRUM` | Spectrum peak region analysis (start, end, width, confidence) |
| `SPECTRUM2D` | 2D spectrum curve segmentation (supports COSINE, POLY curve types) |
| `S21VSFLUX` | S21 vs Flux parameter curve segmentation |
| `POWERSHIFT` | Power shift curve segmentation |

### Data Input Formats

The input data should be a dictionary or list of dictionaries with the following structure:

```python
dict_list = [{
    "image": {
        "Q0": [x_data, y_data],  # or [x_data, y_data, z_data] for 2D
        "Q1": [x_data, y_data],
    }
}, ...]  # One or more data items
```

**Note:** Multiple data items are supported - pass a list of dictionaries. The output `results` list has one entry per input item, in the same order.

---

#### S21PEAK

**Input:**
```python
{
    "image": {
        "Q0": [x_array, amp_array, phi_array],  # tuple, length=3
        "Q1": [x_array, amp_array, phi_array],
    }
}
```
- `x_array`: np.ndarray, shape=(N,), dtype=float64 - frequency data
- `amp_array`: np.ndarray, shape=(N,), dtype=float64 - amplitude data
- `phi_array`: np.ndarray, shape=(N,), dtype=float32 - phase data

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

#### S21PEAKMULTI

Similar to S21PEAK but uses combined qubit keys (e.g., "Q0101") and does not include an `id` field.

**Input:**
```python
{
    "image": {
        "Q0101": [x_array, amp_array, phi_array],  # tuple, length=3
        "Q0202": [x_array, amp_array, phi_array],
    }
}
```
- `x_array`: np.ndarray, shape=(N,), dtype=float64 - frequency data
- `amp_array`: np.ndarray, shape=(N,), dtype=float32 - amplitude data
- `phi_array`: np.ndarray, shape=(N,), dtype=float32 - phase data

**Output:**
```json
{
  "type": "s21peakmulti",
  "results": [{
    "peaks": [[int, ...], [int, ...]],              // Peak indices per qubit
    "confs": [[float, ...], [float, ...]],          // Confidence scores per peak
    "freqs_list": [[float, ...], [float, ...]],     // Peak frequencies per qubit
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
        "Q0": [x_array, y_array],  // tuple, length=2
        "Q1": [x_array, y_array],
    }
}
```
- `x_array`: np.ndarray, shape=(N,), dtype=float64 - frequency data
- `y_array`: np.ndarray, shape=(N,), dtype=float32 - spectral amplitude

Returns peak start, peak end, peak x value, peak width, and confidence.

**Output:**
```json
{
  "type": "spectrum",
  "results": [{
    "peaks_list": [[float, ...], [float, ...]],           // Peak x values for all waves
    "peak_start": [[float, ...], [float, ...]],           // Peak start x values
    "peak_end": [[float, ...], [float, ...]],             // Peak end x values
    "confidences_list": [[float, ...], [float, ...]],     // Confidence scores per peak
    "status": "success" | "failed"
  }]
}
```

---

#### SPECTRUM2D

2D spectrum curve segmentation.

**Input:**
```python
{
    "image": {
        "Q0": [iq_avg, bias_array, freq_array],  # tuple, length=3
    }
}
```
- `iq_avg`: np.ndarray, shape=(B, A), dtype=complex64
- `bias_array`: np.ndarray, shape=(A,), dtype=float64
- `freq_array`: np.ndarray, shape=(B,), dtype=float64

**Parameters:**
- `curve_type`: `CurveType.COSINE` (default) or `CurveType.POLY` - Curve fitting method

**Output:**
```json
{
  "type": "spectrum2d",
  "results": [{
    "params_list": [[[float, ...], ...], ...],             // Fitting parameters
    "linepoints_list": [[[[float, float], ...], ...], ...], // Curve point coordinates
    "confidences_list": [[float, ...], [float, ...]],       // Confidence scores
    "class_ids_list": [[float, ...], [float, ...]],         // Curve class IDs
    "curve_type_list": [["cosin"] | ["poly"], ...],         // Fitting type
    "status": "success" | "failed"
  }]
}
```

**Fitting Formulas:**
- When `curve_type_list` is `"cosin"`: `params_list = [A, freq, phi, offset]`
  - Formula: `pred_y = A * np.sin(freq * pred_x + phi) + offset`
- When `curve_type_list` is `"poly"`: `params_list = [A, B, C, D]`
  - Formula: `pred_y = A * pred_x³ + B * pred_x² + C * pred_x + D`

---

#### S21VSFLUX

**Input:**
```python
{
    "image": {
        "Q0": [freq_array, volt_array, s_matrix],  // tuple, length>=3
        "Q1": [freq_array, volt_array, s_matrix],
    }
}
```
- `freq_array`: np.ndarray, shape=(A,), dtype=float64 - frequency data
- `volt_array`: np.ndarray, shape=(B,), dtype=float64 - voltage/bias data
- `s_matrix`: np.ndarray, shape=(B, A), dtype=float32 - 2D spectrum data

**Parameters:**
- `curve_type`: `CurveType.COSINE` (default) or `CurveType.POLY` - Curve fitting method

**Output:**
```json
{
  "type": "s21vsflux",
  "results": [{
    "params_list": [[[float, ...], ...], ...],             // Fitting parameters
    "linepoints_list": [[[[float, float], ...], ...], ...], // Curve point coordinates
    "confidence_list": [[float, ...], [float, ...]],       // Confidence scores
    "class_ids": [[float, ...], [float, ...]],             // Curve class IDs
    "curve_type": [["cosin"] | ["poly"], ...],             // Fitting type
    "status": "success" | "failed"
  }]
}
```

**Fitting Formulas:**
- When `curve_type` is `"cosin"`: `params_list = [A, freq, phi, offset]`
  - Formula: `pred_y = A * np.sin(freq * pred_x + phi) + offset`
- When `curve_type` is `"poly"`: `params_list = [A, B, C, D]`
  - Formula: `pred_y = A * pred_x³ + B * pred_x² + C * pred_x + D`

---

#### POWERSHIFT

**Input:**
```python
{
    "image": {
        "Q0": [freq_array, amp_array, value_array],  // tuple, length>=3
        "Q1": [freq_array, amp_array, value_array],
    }
}
```
- `freq_array`: np.ndarray, shape=(A,), dtype=float64 - frequency data
- `amp_array`: np.ndarray, shape=(B,), dtype=float64 - power/amplitude data
- `value_array`: np.ndarray, shape=(B, A), dtype=float32 - 2D spectrum data

**Output:**
```json
{
  "type": "powershift",
  "results": [{
    "q_list": ["Q0", "Q1", ...],                              // Qubit names
    "keypoints_list": [[[float, float], ...], ...],          // Line segment endpoints
    "confs": [float, float, ...],                             // Confidence scores
    "class_num_list": [int, int, ...],                        // Segmentation labels (1-5)
    "status": "success" | "failed"
  }]
}
```
- **Class 1**: Vertical to x-axis
- **Class 2**: Both ends vertical, middle inclined
- **Class 3**: Only bottom vertical, then inclined
- **Class 4**: Entirely inclined upward
- **Class 5**: No information

### Getting Results

```python
# Get raw (unfiltered) results
results = client.get_result(response=response)

# Get filtered results by confidence threshold (for tasks with confidence scores)
results_filtered = client.get_result(response, threshold=0.5, task_type=NNTaskName.S21PEAK.value)
```

### Visualization

```python
from qubitclient.draw.plymanager import QuantumPlotPlyManager
from qubitclient.draw.pltmanager import QuantumPlotPltManager

ply_manager = QuantumPlotPlyManager()
plt_manager = QuantumPlotPltManager()

for idx, (result, dict_param) in enumerate(zip(results, dict_list)):
    save_path_prefix = f"./tmp/client/result_{NNTaskName.SPECTRUM2D.value}_{savenamelist[idx]}"
    save_path_png = save_path_prefix + ".png"
    save_path_html = save_path_prefix + ".html"

    # Plot with matplotlib (PNG)
    plt_manager.plot_quantum_data(
        data_type='npy',
        task_type=NNTaskName.SPECTRUM2D.value,
        save_path=save_path_png,
        result=result,
        dict_param=dict_param
    )

    # Plot with plotly (HTML, interactive)
    ply_manager.plot_quantum_data(
        data_type='npy',
        task_type=NNTaskName.SPECTRUM2D.value,
        save_path=save_path_html,
        result=result,
        dict_param=dict_param
    )
```

### Examples

#### S21 Peak Detection

```python
from qubitclient import QubitNNScopeClient, NNTaskName
from qubitclient.scope.utils.data_parser import load_npy_file

client = QubitNNScopeClient()

# Load data from files
file_path_list = ["data/file1.npy", "data/file2.npy"]
dict_list = [load_npy_file(fp) for fp in file_path_list]

# Send request
response = client.request(file_list=dict_list, task_type=NNTaskName.S21PEAK)

# Get results
# Get raw (unfiltered) results
results = client.get_result(response)

# Or filter by confidence threshold
threshold = 0.5
results = client.get_result(response, threshold=threshold, task_type=NNTaskName.S21PEAK.value)

# Results format:
# [{
#     "peaks": [[10, 41, 20], [22, 34]],        # peak indices per qubit
#     "confs": [[0.3, 0.4, 0.1], [0.6, 0.5]],  # confidence scores
#     "freqs_list": [[0.3e9, 0.4e9, 0.1e9], [0.6e9, 0.5e9]],  # peak frequencies
#     "status": "success"
# }]
```

#### Spectrum Analysis

```python
from qubitclient import QubitNNScopeClient, NNTaskName

client = QubitNNScopeClient()

response = client.request(file_list=dict_list, task_type=NNTaskName.SPECTRUM)
results = client.get_result(response)

# Results format:
# [{
#     "peaks_list": [[4431999999.99993, 4431999999.99993], [4293999999.9999456]],
#     "peak_start": [[4402666666.67, 4410666666.67], [4262666666.67]],
#     "peak_end": [[4437333333.33, 4438666666.67], [4317333333.33]],
#     "confidences_list": [[0.448, 0.150], [0.686]],
#     "status": "success"
# }]
```

#### 2D Spectrum (SPECTRUM2D)

```python
from qubitclient import QubitNNScopeClient, NNTaskName
from qubitclient.nnscope.nnscope_api.curve.curve_type import CurveType

client = QubitNNScopeClient()

# Using cosine fitting (default)
response = client.request(
    file_list=dict_list,
    task_type=NNTaskName.SPECTRUM2D,
    curve_type=CurveType.COSINE
)

# Or using polynomial fitting
response = client.request(
    file_list=dict_list,
    task_type=NNTaskName.SPECTRUM2D,
    curve_type=CurveType.POLY
)

results = client.get_result(response)

# Results format:
# [{
#     "params_list": [[[-1, -1, -1, -1]], [[-1, -1, -1, -1]]],  # fitting parameters
#     "linepoints_list": [[[[-1, 6.843e9], [-0.9, 6.844e9], ...]]],  # curve points
#     "confidences_list": [[0.6], [0.6]],  # confidence scores
#     "class_ids_list": [[1.0], [1.0]],    # curve class IDs
#     "curve_type_list": [["cosin"], ["cosin"]],  # fitting type
#     "status": "success"
# }]
```

#### S21VSFLUX

```python
from qubitclient import QubitNNScopeClient, NNTaskName
from qubitclient.nnscope.nnscope_api.curve.curve_type import CurveType

client = QubitNNScopeClient()

response = client.request(
    file_list=dict_list,
    task_type=NNTaskName.S21VSFLUX,
    curve_type=CurveType.COSINE
)

results = client.get_result(response)

# Results format:
# [{
#     "params_list": [[[-1, -1, -1, -1]], [[-1, -1, -1, -1]]],
#     "linepoints_list": [[[[-1, 6.843e9], [-0.9, 6.844e9], ...]]],
#     "confidence_list": [[0.6], [0.6]],
#     "class_ids": [[1.0], [1.0]],
#     "curve_type": [["cosin"], ["cosin"]],
#     "status": "success"
# }]
```

#### POWERSHIFT

```python
from qubitclient import QubitNNScopeClient, NNTaskName

client = QubitNNScopeClient()

response = client.request(file_list=dict_list, task_type=NNTaskName.POWERSHIFT)

results = client.get_result(response)

# Results format:
# [{
#     "q_list": ["Q0", "Q1"],                    # qubit names
#     "keypoints_list": [[[18.4, 0.7], [24.3, 9.3], ...]],  # line segment endpoints
#     "confs": [0.95, 0.87, 0.65, 0.92, 0.78],  # confidence scores
#     "class_num_list": [1, 2, 3, 1, 4],         # segmentation labels (1-5)
#     "status": "success"
# }]
```

### Complete Workflow Example

```python
from qubitclient import QubitNNScopeClient, NNTaskName
from qubitclient.nnscope.nnscope_api.curve.curve_type import CurveType
from qubitclient.scope.utils.data_parser import load_npy_file
from qubitclient.draw.plymanager import QuantumPlotPlyManager
from qubitclient.draw.pltmanager import QuantumPlotPltManager
import os

# Configuration
DATA_DIR = "data/spectrum2d"

# Initialize client
client = QubitNNScopeClient()

# Load data files
savenamelist = []
file_path_list = []
for fname in os.listdir(DATA_DIR):
    if fname.endswith('.npy'):
        savenamelist.append(os.path.splitext(fname)[0])
        file_path_list.append(os.path.join(DATA_DIR, fname))

dict_list = [load_npy_file(fp) for fp in file_path_list]

# Send request with cosine curve fitting
response = client.request(
    file_list=dict_list,
    task_type=NNTaskName.SPECTRUM2D,
    curve_type=CurveType.COSINE
)

# Get and filter results
results = client.get_result(response)
threshold = 0.5
final_results = client.get_result(response, threshold=threshold, task_type=NNTaskName.SPECTRUM2D.value)

# Visualize results
ply_manager = QuantumPlotPlyManager()
plt_manager = QuantumPlotPltManager()

for idx, (result, dict_param) in enumerate(zip(final_results, dict_list)):
    save_path_prefix = f"./tmp/client/result_{NNTaskName.SPECTRUM2D.value}_{savenamelist[idx]}"
    plt_manager.plot_quantum_data(
        data_type='npy',
        task_type=NNTaskName.SPECTRUM2D.value,
        save_path=save_path_prefix + ".png",
        result=result,
        dict_param=dict_param
    )
    ply_manager.plot_quantum_data(
        data_type='npy',
        task_type=NNTaskName.SPECTRUM2D.value,
        save_path=save_path_prefix + ".html",
        result=result,
        dict_param=dict_param
    )
```
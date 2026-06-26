# Simple CSC — Detailed Reference

## Table of Contents

- [LMCorrector API](#lmcorrector-api)
- [Config Parameters](#config-parameters)
- [Distortion Types](#distortion-types)
- [Supported Models](#supported-models)
- [Running Experiments](#running-experiments)
- [Dataset Format](#dataset-format)
- [Evaluation](#evaluation)
- [Project Structure](#project-structure)
- [Demo App](#demo-app)

## LMCorrector API

### Constructor

```python
LMCorrector(
    model: Union[str, LMModel],           # HuggingFace model name or LMModel instance
    prompted_model: Union[str, LMModel],   # Optional second model for prompt-based scoring
    config_path: str = "configs/default_config.yaml",
    n_observed_chars: int = None,          # How many next chars to observe (default from config: 8)
    n_beam: int = None,                    # Beam search width (default: 8)
    n_beam_hyps_to_keep: int = None,       # Hypotheses to keep (default: 1)
    alpha: float = None,                   # Length reward hyperparameter (default: 2.5)
    temperature: float = None,             # Temperature for prompted model (default: 1.5 for c2ec, 1.0 for default)
    distortion_model_smoothing: float = None,  # Smoothing for distortion probs (default: -15.0)
    use_faithfulness_reward: bool = None,   # Enable faithfulness reward (default: true)
    customized_distortion_probs: dict = None,  # Override distortion probs from config
    max_length: int = None,                # Max input length in chars (default: 128)
    use_chat_prompted_model: bool = False,  # Use chat template for prompted model
    torch_dtype=torch.float16,             # Pass via **kwargs; use bfloat16 for Qwen2/2.5
    device_map="auto",                     # Pass via **kwargs
)
```

`None` parameters fall back to config file values.

### `__call__` Method

```python
corrector(
    src: Union[List[str], str],            # Input text(s) to correct
    contexts: Union[List[str], str] = None, # Optional context for each input (same length)
    prompt_split: str = "\n",              # Separator between context and input
    n_beam: int = None,                    # Override beam width
    n_beam_hyps_to_keep: int = None,       # Override hypotheses count
    stream: bool = False,                  # Enable streaming (batch_size=1 only)
) -> List[Tuple[str, ...]]                 # List of (correction,) tuples
```

Return format: `[('corrected_text_1',), ('corrected_text_2',)]`

With `n_beam_hyps_to_keep > 1`: `[('hyp1', 'hyp2', ...), ...]`

With `stream=True`: returns a generator yielding intermediate `List[Tuple[str]]`.

### `update_params` Method

```python
corrector.update_params(
    n_beam=16,
    alpha=3.0,
    use_faithfulness_reward=False,
)
```

Dynamically update corrector parameters without re-initializing.

### API Server Request Schema

```json
{
    "input": "要纠正的文本",
    "contexts": null,
    "prompt_split": "\n",
    "max_tokens": null,
    "stream": false,
    "n_beam": null,
    "n_beam_hyps_to_keep": null
}
```

## Config Parameters

### Beam Search

| Parameter | Default | Description |
|-----------|---------|-------------|
| `n_beam` | 8 | Beam search width. Larger = better quality, slower |
| `n_beam_hyps_to_keep` | 1 | Number of output hypotheses per input |
| `max_length` | 128 | Max input chars (truncated beyond this) |
| `n_observed_chars` | 8 | Lookahead window for observed characters |

### Scoring

| Parameter | Default | Description |
|-----------|---------|-------------|
| `alpha` | 2.5 | Length reward weight. Higher = prefer longer outputs |
| `temperature` | 1.5 (c2ec) / 1.0 (default) | Temperature for prompted model probability |
| `distortion_model_smoothing` | -15.0 | Log-space smoothing for distortion model |
| `use_faithfulness_reward` | true | Penalize outputs that deviate too much from input |

### Distortion Probabilities

Log-space probabilities for each distortion type. Higher (closer to 0) = more likely to be accepted.

**c2ec_config.yaml** values:
```yaml
distortion_probs:
  IDT: -0.04    # Identical (no change)
  PTC: -0.04    # Prone to confusion
  SAP: -3.75    # Same pinyin
  SIP: -4.85    # Similar pinyin
  SIS: -5.40    # Similar shape
  ROR: -5.50    # Reorder
  MIS: -8.50    # Missing character (insertion needed)
  OTP: -8.91    # Other pinyin error
  OTS: -8.91    # Other similar shape
  RED: -9.00    # Redundant character (deletion needed)
  UNR: -14.99   # Unrecognized
```

**default_config.yaml** omits `ROR`, `MIS`, `RED` (substitution-only mode).

## Distortion Types

| Code | Name | Description |
|------|------|-------------|
| IDT | Identical | Character unchanged |
| PTC | Prone to Confusion | Commonly confused character pairs (e.g., 的/地/得) |
| SAP | Same Pinyin | Exact same pinyin pronunciation |
| SIP | Similar Pinyin | Similar pinyin (fuzzy consonant/vowel matching) |
| SIS | Similar Shape | Visually similar characters |
| ROR | Reorder | Characters in wrong order (v2.0.0 only) |
| MIS | Missing | Character missing from input, needs insertion (v2.0.0 only) |
| OTP | Other Pinyin | Pinyin-related but not SAP/SIP |
| OTS | Other Shape | Shape-related but not SIS |
| RED | Redundant | Extra character in input, needs deletion (v2.0.0 only) |
| UNR | Unrecognized | No known relationship |

## Supported Models

Auto-detected by model name via `AutoLMModel.from_pretrained()`:

| Model Family | Detection Rule | Example |
|-------------|---------------|---------|
| Qwen (1.5/2/2.5/3) | `"qwen"` in name | `Qwen/Qwen2.5-7B` |
| Llama | `"llama"` in name | `meta-llama/Llama-2-7b` |
| Baichuan2 | `"Baichuan2"` in name | `baichuan-inc/Baichuan2-13B-Base` |
| InternLM2 | `"internlm2"` in name | `internlm/internlm2-base-7b` |
| UER/GPT2 | `"uer"` in name | `uer/gpt2-chinese-cluecorpussmall` |
| Other | fallback `LMModel` | Any HuggingFace causal LM |

Models are auto-downloaded from HuggingFace. Set `MODELSCOPE_CACHE` env var to use ModelScope mirror.

## Running Experiments

### Batch Inference

```bash
python -u run.py \
    --input-file datasets/lemon_v2/car.txt \
    --path results/output_dir \
    --model-name Qwen/Qwen2.5-7B \
    --prompted-model-name Qwen/Qwen2.5-7B \
    --config-path configs/c2ec_config.yaml \
    --n-beam 8 \
    --batch-size 200 \
    --max-sentences-per-batch 24 \
    --max-length 256 \
    --alpha 2.5 \
    --temperature 1.5 \
    --distortion-model-smoothing -15.0 \
    --use-faithfulness-reward
```

Output: `results/output_dir/prediction.txt` (one prediction per line, tab-separated if multiple hypotheses).

### Full Experiment Suite

```bash
# Run all datasets with default params
bash run.sh model=Qwen/Qwen2.5-7B prompted_model=Qwen/Qwen2.5-7B config_path=configs/c2ec_config.yaml

# Override parameters
bash run.sh model=Qwen/Qwen2.5-14B n_beam=16 alpha=3.0
```

`run.sh` iterates over datasets (lemon_v2, cscd_ime, c2ec, etc.), runs inference, then evaluates.

### With Context (ASR correction)

```bash
bash run.w_context.sh model=baichuan-inc/Baichuan2-7B-Base
```

Uses `run.w_context.py` for datasets with context columns (e.g., aishell1).

## Dataset Format

### Input File Format

Tab-separated, one pair per line:

```
[source]\t[target]
[source]\t[target]
```

- `[source]`: Original (possibly erroneous) text
- `[target]`: Gold-standard corrected text

Some datasets have a 3-column format: `[id]\t[source]\t[target]`

### Available Datasets

Download all with: `bash scripts/download_datasets.sh`

| Dataset | Path | Type |
|---------|------|------|
| ECSpell (law/med/odw) | `datasets/ecspell/*.txt` | Domain-specific CSC |
| SIGHAN Revised (13/14/15) | `datasets/sighan_rev/*.txt` | Standard CSC benchmark |
| Lemon v2 (7 domains) | `datasets/lemon_v2/*.txt` | Multi-domain CSC |
| CSCD-IME | `datasets/cscd_ime/*.txt` | IME-based errors |
| MCSC | `datasets/mcsc/test.txt` | Multi-reference CSC |
| AISHELL-1 | `datasets/aishell1/*.txt` | ASR error correction |
| C2EC | `datasets/c2ec/*.txt` | Insert/delete errors (build with `scripts/build_c2ec_dataset.sh`) |

### Building C2EC Dataset

Requires downloading CCTC v1.1 manually:
1. Download `cctc_v1.1.zip` from [CTCResources](https://github.com/destwang/CTCResources)
2. Place in `datasets/c2ec/cctc_v1.1.zip`
3. Run `bash scripts/build_c2ec_dataset.sh`

## Evaluation

### Standard Evaluation

```bash
python eval/evaluate.py \
    --gold datasets/lemon_v2/car.txt \
    --hypo results/.../prediction.txt \
    --to_halfwidth \
    --ignore_space
```

### Evaluation Flags

| Flag | Description |
|------|-------------|
| `--metric_algorithm` | `levenshtein` (default, alignment-based), `conventional`, `official`, `wang` |
| `--ignore_unmatch_length` | Skip pairs where src/tgt lengths differ (for CSC-only datasets) |
| `--ignore_punct` | Exclude punctuation from evaluation |
| `--to_simplified` | Convert traditional Chinese to simplified before eval |
| `--to_halfwidth` | Convert fullwidth chars to halfwidth |
| `--ignore_space` | Remove spaces before comparison |
| `--max_length N` | Skip sentences longer than N chars |

### Metrics Output

- **Sentence-level**: detection/correction precision, recall, F1, accuracy
- **Character-level**: detection/correction precision, recall, F1
- **FPR**: False positive rate (overcorrection on correct sentences)

### WER Evaluation (ASR)

```bash
python eval/evaluate_wer.py --char=1 --v=1 datasets/aishell1/test.txt results/.../prediction.txt
```

## Project Structure

```
simple-csc/
├── lmcsc/                    # Core Python package
│   ├── __init__.py           # Exports LMCorrector
│   ├── corrector.py          # LMCorrector class (main entry point)
│   ├── model.py              # LMModel, AutoLMModel, model-specific subclasses
│   ├── generation.py         # Beam search, distortion probability computation
│   ├── transformation_type.py # Distortion type classification engine
│   ├── obversation_generator.py # Observed sequence generator for beam search
│   ├── streamer.py           # BeamStreamer for streaming output
│   ├── common.py             # Constants (MIN, OOV_CHAR, PUNCT, etc.)
│   └── utils.py              # Alignment, text cleaning, vocab utilities
├── configs/
│   ├── default_config.yaml   # v1.0.0 substitution-only config
│   ├── c2ec_config.yaml      # v2.0.0 full config (insert/delete/reorder)
│   ├── demo_config.yaml      # Demo app correction config
│   └── demo_app_config.yaml  # Demo app UI config (models, examples, params)
├── data/                     # Distortion model data files
│   ├── similar_shape_dict.json
│   ├── shape_confusion_dict.json
│   ├── similar_consonant_dict.json
│   ├── similar_vowel_dict.json
│   ├── pinyin_distance_matrix.pkl
│   ├── prone_to_confusion_dict.json
│   ├── length_immutable_chars.json
│   └── ...
├── datasets/                 # Evaluation datasets (download with scripts)
├── eval/
│   ├── evaluate.py           # Main evaluation script (4 metric algorithms)
│   ├── evaluate_wer.py       # WER evaluation for ASR tasks
│   └── utils.py              # Alignment, P/R/F1 computation
├── scripts/
│   ├── set_environment.sh    # Standard env setup
│   ├── download_datasets.sh  # Download all evaluation datasets
│   └── build_c2ec_dataset.sh # Build C2EC dataset from CCTC + Lemon
├── run.py                    # Batch inference script
├── run.sh                    # Full experiment runner (all datasets)
├── run.w_context.py          # Inference with context (ASR)
├── run.w_context.sh          # Context experiment runner
├── run.speed_test.py         # Speed benchmarking
├── api_server.py             # FastAPI REST server
├── demo.py                   # Streamlit demo app
└── setup.py                  # Package installation
```

## Demo App

```bash
streamlit run demo.py
```

- Default model: `Qwen/Qwen2.5-0.5B`
- Config: `configs/demo_config.yaml` (correction) + `configs/demo_app_config.yaml` (UI)
- Sidebar: model selection, n_beam, alpha, faithfulness_reward toggles
- Includes example sentences and a 1866-char long text example
- Requires: `streamlit` package

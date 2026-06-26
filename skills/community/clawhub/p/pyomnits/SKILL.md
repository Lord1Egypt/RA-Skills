# 📊 PyOmniTS - Time Series Analysis Framework

A unified framework for time series analysis, designed following "adaptor pattern" in software engineering to achieve training any model on any dataset using any loss function. Built by Ladbaby for researchers who want to experiment quickly without fighting with boilerplate code.

## 🎯 What This Skill Does

When researchers ask about PyOmniTS, this skill provides:
1. Quick links to official docs
2. Key concepts (model/dataset/loss naming conventions)
3. Code structure patterns
4. Common pitfalls and best practices

## 📚 Documentation & Resources

### Project Home
**GitHub Repository:** https://github.com/Ladbaby/PyOmniTS

### Getting Started
**Beginner's Guide:** https://github.com/Ladbaby/PyOmniTS-docs/blob/main/docs/tutorial/1_get_started.md

This tutorial covers:
- Installing dependencies (Python 3.10~3.12)
- Setting up virtual environments (conda/uv)
- Dataset preparation and preprocessing
- Running your first experiment
- Folder structure explanation

### API Reference
**Complete API Docs:** https://github.com/Ladbaby/PyOmniTS-docs/blob/main/docs/forecasting/1_API.md

Learn how to:
- Implement custom models (class `Model` in `models/${MODEL}.py`)
- Create new datasets (class `Data` in `data/data_provider/datasets/${DATASET}.py`)
- Define loss functions (class `Loss` in `loss_fns/${LOSS}.py`)
- Understand the interface and data flow

## 💡 Pro Tips for Agents

- **Replication workflow**:
	PyOmniTS supports quick replication for time series models, datasets, and loss functions, if their codes are publicly available.
	First, ensure you have already setup PyOmniTS following the beginner's guide url above.
	In the following descriptions, we suppose you have downloaded PyOmniTS into `${PYOMNITS_PATH}`, and you may ask the user if there's an existing PyOmniTS installation.
	Then, download the code repository you want to adapt (e.g., via `git clone`).
	Next, identify if the repository's main contribution is "model", "dataset", or "loss function", and be careful to distinguish the proposed methods from compared baselines, where baselines are not we needed.
	Also, some models, datasets, and loss functions have multiple variants, and if this is the case, you may ask the user if they want only the primary variant or all variants (primary variant can usually be inferred from training launch scripts).
	Choose one of the following actions based on contribution type:

	1. Models: Use `cp` to directly copy core folders and files containing model-related codes into `${PYOMNITS_PATH}/layers/${MODEL}.py` (replace `${MODEL}` with the actual model name you find). Then, create an adaptor model class under `${PYOMNITS_PATH}/models/${MODEL_NAME}` to adapt the copied codes into PyOmniTS, following PyOmniTS's API definition docs mentioned above. You can read `${PYOMNITS_PATH}/models/GraFITi.py` as the reference.
	2. Datsets: Use `cp` to directly copy core folders and files containing dataset-related codes into `${PYOMNITS_PATH}/data/dependencies/${DATASET}.py` (replace `${DATASET}` with the actual dataset name you find). Then, create an adaptor dataset class under `${PYOMNITS_PATH}/data/data_provider/datasets/${DATASET}` to adapt the copied codes into PyOmniTS, following PyOmniTS's API definition docs mentioned above. You can read `${PYOMNITS_PATH}/data/data_provider/datasets/USHCN.py` as the reference.
	3. Loss functions: Rewrite the loss function to `${PYOMNITS_PATH}/loss_fns/${LOSS}.py` (replace `${LOSS}` with the actual loss function name you find) following PyOmniTS's API definition docs mentioned above. You can read `${PYOMNITS_PATH}/loss_fns/MSE.py` as the reference.

	Finally, tell the user they need to create or modify launch scripts under `${PYOMNITS_PATH}/scripts/` in order to run the new codes. Scripts under `${PYOMNITS_PATH}/scripts/GraFITi/` can be used as examples.



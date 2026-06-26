# Config Modes

Use the example files in `configs/` as templates. They are demonstrations, not
drop-in production configs.

## Mode Map

- `configs/sampling.toml`
  - `run_type = "sampling"`
  - Sample molecules from a prior or generator model
- `configs/scoring.toml`
  - `run_type = "scoring"`
  - Score input SMILES without training a model
- `configs/transfer_learning.toml`
  - `run_type = "transfer_learning"`
  - Focus a model toward an input SMILES set
- `configs/staged_learning.toml`
  - `run_type = "staged_learning"`
  - Run reinforcement learning or curriculum learning stages
- `configs/stage2_scoring.toml`
  - External scoring config for later RL stages
- `configs/scoring_components_example.toml`
  - More scoring examples
- `configs/data_pipeline.toml`
  - Datapipeline preprocessing config for `reinvent_datapre`

## Sampling

Primary fields from `configs/PARAMS.md` and `configs/sampling.toml`:

- `device`
- `model_file`
- `smiles_file` for LibInvent, LinkInvent, Mol2Mol, or Pepinvent
- `sample_strategy`
- `output_file`
- `num_smiles`
- `unique_molecules`
- `randomize_smiles`
- `temperature`
- `tb_logdir`

Generator-specific notes in the example file:

- Reinvent: de novo sampling
- LibInvent: scaffold plus attachment-point input
- LinkInvent: two warheads per line separated by `|`
- Mol2Mol: input molecules plus optional beam search and temperature
- Pepinvent: peptide-focused sampling

## Scoring

The scoring example uses:

- `smiles_file`
- `output_csv`
- `[scoring]`
- `[[scoring.component]]`
- endpoint-specific `weight`, `name`, `params`, and optional `transform`

Use `configs/SCORING.md` for supported component families and transform names.

## Transfer Learning

Common fields:

- `input_model_file`
- `smiles_file`
- `validation_smiles_file`
- `output_model_file`
- `num_epochs`
- `save_every_n_epochs`
- `batch_size`
- `sample_batch_size`
- `num_refs`
- `tb_logdir`

The example includes different commented blocks for Reinvent, Mol2Mol,
LibInvent, and LinkInvent. Uncomment one coherent block and remove or keep the
rest commented.

## Staged Learning

Important sections:

- `[parameters]`
- `[learning_strategy]`
- `[diversity_filter]`
- `[inception]` optional
- `[[stage]]`
- `[stage.scoring]`
- `[[stage.scoring.component]]`

Key files to update:

- `prior_file`
- `agent_file`
- `smiles_file` when the chosen generator needs it
- `chkpt_file`
- scoring definitions inside the stage or via an external `filename`

Rules:

- Stages are always a list, so keep `[[stage]]`.
- A global `[diversity_filter]` overrides per-stage diversity filters.
- Stage scoring can live inline or in a separate TOML or JSON file.

## Datapipeline

`configs/data_pipeline.toml` is separate from the main `run_type`-based CLI
configs and is meant for `reinvent_datapre`.

Important fields:

- `input_csv_file`
- `smiles_column`
- `separator`
- `output_smiles_file`
- `num_procs`
- `chunk_size`
- `[filter]` with element, size, stereochemistry, deduplication, and transform
  controls

## Adaptation Checklist

Before running any config, verify:

- device string matches the current machine
- every model or prior path exists
- every SMILES input path exists and matches the expected column format
- output and log paths are writable
- TensorBoard directories are intentional

# Plugins, Notebooks, And Tests

## Scoring Components

`configs/SCORING.md` groups built-in scoring components into several families:

- physchem and structure properties from RDKit
- similarity and cheminformatics components
- docking and structure-based interfaces such as DockStream, Icolos, and MAIZE
- QSAR or QSPR model integrations such as ChemProp and Qptuna
- drug-likeness and synthesizability components such as QED, SAScore, and
  reaction filters
- generic external-process and REST components
- LinkInvent fragment-specific properties

Transforms documented upstream include:

- `sigmoid`
- `reverse_sigmoid`
- `double_sigmoid`
- `left_step`
- `right_step`
- `step`
- `value_mapping`

Aggregation functions documented upstream:

- `arithmetic_mean`
- `geometric_mean`

## Custom Scoring Plugins

When the user wants a new plugin, follow the rules from the upstream
`README.md`:

1. Create a namespace path like `.../reinvent_plugins/components`.
2. Do not place `__init__.py` in the top-level `reinvent_plugins` or
   `components` directories.
3. Name plugin files `comp_*.py`.
4. Tag scoring component classes with `@add_tag`.
5. Optionally tag one parameters dataclass in the same file.
6. Put the plugin parent directory on `PYTHONPATH` so REINVENT can import it.

If import debugging is needed, check whether a statement like this works:

```python
from reinvent_plugins.components import comp_myscorer
```

## Notebooks

The repo ships notebook sources in jupytext light-script form.

Convert one file:

```bash
jupytext --to ipynb -o Reinvent_demo.ipynb Reinvent_demo.py
```

Convert all notebook scripts:

```bash
./convert_to_notebook.sh
```

Run notebooks in the same environment as the REINVENT install.

## Tests

The upstream test flow requires a JSON config file based on
`tests/example_config.json`.

Rules:

- Set `MAIN_TEST_PATH` to a non-existent directory.
- Expect the tests to write temporary data there and delete it afterward.
- Some tests require a proprietary OpenEye license.
- The simple license path flow is to set `OE_LICENSE`.

Example command from the upstream README:

```bash
pytest tests --json /path/to/config.json --device cuda
```

Do not claim the full test suite is runnable unless the required prior models,
SMILES datasets, config file, and optional OpenEye license are actually
present.

## Case-Sensitive Path Note

On case-insensitive macOS filesystems, cloning the upstream repo can warn about
colliding tutorial files under `contrib/tutorials/maize/adgpu_prepare`. Treat
that as a tutorial-directory limitation, not evidence that the main REINVENT
CLI is broken.

# Examples

All examples below are **local-only** and stop at vertical TTF + preview/test artifacts.

## Example 1: default glyf workflow

```bash
python scripts/run_full_pipeline.py /path/to/source.ttf /path/to/output-dir
```

Outputs:

- horizontal preview PNG
- vertical TTF
- vertical preview PNG
- reader test TXT

## Example 2: CFF workflow

```bash
python scripts/run_full_pipeline.py /path/to/source.otf /path/to/output-dir
```

## Example 3: custom config for punctuation and corner quotes

```bash
python scripts/make_vertical_font.py /path/to/source.ttf /path/to/output.ttf references/default-config.json
```

You can also create a copied config JSON and override only what you need, for example:

```json
{
  "single_punct": {
    "tx": 600,
    "ty": 50,
    "scale": 0.78
  },
  "corner_quotes": {
    "left_bound": 95,
    "right_bound": 905
  }
}
```

Then run:

```bash
python scripts/make_vertical_font.py /path/to/source.ttf /path/to/output.ttf /path/to/custom-config.json
```

## Example 4: audit after conversion

```bash
python scripts/audit_font_rules.py /path/to/output.ttf
```

Use this when the preview still feels wrong and you need bbox / center evidence instead of blind retuning.

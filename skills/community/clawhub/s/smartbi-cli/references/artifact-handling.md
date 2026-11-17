# Artifact Handling

Baize file artifacts are server URIs, not local paths. Inspect the captured SSE stream with `scripts/artifact_io.py`, download artifacts through the configured SmartBI profile, then read and verify the resulting Excel, CSV, or Parquet file. Do not treat a preview table as a complete extract or expose signed URLs.

The same reader can inspect downloaded direct-query files. CSV values stay as text, including leading zeros, decimal text and literal `NA`/`NULL`; blank cells remain empty strings. Excel preserves stored cell types, and Parquet uses its schema. Convert numeric measures explicitly from model metadata before calculating; identifier columns must retain their original values. CSV alone cannot distinguish an empty string from an exported null, and Excel number formatting may display zeros that are absent from its stored numeric value. Do not invent missing identifier digits or null semantics.

# Gemini Temperature Gap in generate_text()

## The Bug

`generate_text()` accepts `temperature=0.0` but only passes it to `ollama_generate()`.
When the model is Gemini CLI, the temperature parameter is silently dropped.

## Code Trace (router.py)

```
generate_text(model, prompt, *, timeout=60, num_predict=400, temperature=0.0)
    |
    +--> is_gemini_model(model)?
         YES --> gemini_generate(model, prompt, timeout=timeout)
                       |
                       +--> invoke_gemini_cli(model, prompt, timeout=timeout)
                       |
                       temperature: NEVER PASSED. Gemini uses its built-in default (~0.7+).

         NO  --> ollama_generate(model, prompt, timeout=timeout,
                                 num_predict=num_predict,
                                 temperature=temperature)
                       |
                       temperature: 0.0 (deterministic, greedy decoding)
```

## Impact

- **Planner**: Same task --> different decomposition counts (5 vs 6 steps observed).
- **Judge**: Same subtask --> slightly different scores across runs.
- **PRO Executor**: Same prompt --> different phrasings.
- **FLASH Executor**: Same prompt --> different output formatting.
- **Finalizer**: Slightly different report text each run.

All of these are affected for any role configured to use Gemini CLI models.

## Severity

- For most use cases: minor. The outputs are still correct, just surface-level variation.
- For reproducibility-critical workflows: unacceptable.
- For multi-run benchmarks where decomposition count affects fanout parallelism: disruptive.

## Workaround

Use Ollama-backed models when deterministic output matters. Temperature=0.0 IS respected there.

## Root Fix

`gemini_generate()` and `invoke_gemini_cli()` need to accept and forward a `temperature` parameter.
This is a code change in router.py, not a configuration change.

# Frontend integration

Quantum simulation is too slow and too heavy to run in the browser. The pattern: run the pipeline once at build time (or on-demand server-side), serialize results to JSON, and consume from typed React routes.

Additional worked examples of this JSON-handoff shape: `src/data/demos/nadarasa_g1.json`, `nadarasa_g2.json`, `nadarasa_g3.json`, each produced by the matching `quantum/nadarasa_g*.py` driver.


## Pipeline output

Write a single JSON file containing everything the UI needs:

```python
# quantum/qtda.py
out = {
    "patients": [...],
    "fidelity_matrix": [[...]],
    "pairs": [{"i": 0, "j": 1, "fidelity": 0.87, ...}],
    "filtration": [{"threshold": 0.1, "edges": [...], "beta_0": 4, "beta_1": 0}],
    "circuit": {"qubits": 5, "shots_per_pair": 2000, ...},
    "guppy_source": Path(__file__).read_text(),  # show the source on /code page
    "generated_at": "2025-...",
}
Path("src/data/qtda-results.json").write_text(json.dumps(out, indent=2))
```

## Typed loader

```ts
// src/lib/qtda.ts
import data from "@/data/qtda-results.json";

export type Pair = {
  i: number; j: number;
  quantum_fidelity: number; classical_fidelity: number;
  p0: number; shots: number; zeros: number;
};
export type QtdaData = { patients: Patient[]; pairs: Pair[]; /* ... */ };

export const qtda = data as QtdaData;
```

## Consume in routes

```tsx
// src/routes/quantum.tsx
import { qtda } from "@/lib/qtda";

export const Route = createFileRoute("/quantum")({
  component: () => (
    <ul>{qtda.pairs.map(p => <li key={`${p.i}-${p.j}`}>{p.quantum_fidelity.toFixed(3)}</li>)}</ul>
  ),
});
```

## Regenerating

`python -m quantum.qtda` rewrites `src/data/qtda-results.json`. Vite picks it up via HMR. Commit the JSON so builds are deterministic without needing Python in CI.

## When you need it live

If results must update per request (user-supplied input), wrap the pipeline in a TanStack Start server function. Selene runs server-side on Node; do **not** try to bundle it for the browser.
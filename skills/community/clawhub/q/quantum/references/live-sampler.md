# Edge-runtime quantum: mini-sim + live SSE shots

Selene + Guppy require Python and don't run inside a Cloudflare Worker. For *small* live-streaming demos (≤ 4 qubits, fixed kernel topology), this repo runs a pure-TypeScript statevector simulator inside the Worker and streams shots over Server-Sent Events. Everything bigger stays on the Python driver.

## Mini-sim (`src/lib/selene/mini-sim.ts`)

A 2-qubit (extendable to ~4-qubit) statevector simulator in TypeScript:

- Complex amplitudes as paired Float64 arrays.
- Gates: `H`, `RX(θ)`, `RZ(θ)`, `CX`. Add gates as needed; each is a closed-form unitary on the relevant amplitudes.
- `measure(qubitIndex, rng)` does a projective measurement with collapse: compute `P(0)`, draw vs. `rng()`, zero out the eliminated branch, renormalise.

This is enough for any kernel using only the gate set above.

## Porting a Guppy kernel to TS

Mechanical translation. G4 is the worked example:

- `quantum/nadarasa_g4.py` — original feed-forward kernel.
- `src/lib/selene/kernels/nadarasa-g4.ts` — exported `runG4Shot(theta, rng)` returning `{ b, y2 }`.

Rules:
- One TS function per kernel; takes parameters + an `rng: () => number`.
- Mirror the gate order exactly. Mid-circuit `measure` returns 0/1; branch on it just like the Guppy `if measure(...)`.
- Return the labelled measurement record — same keys the Python driver `output(...)`-tags.

## SSE endpoint

`src/routes/api/public/nadarasa-stream.ts`. Public route per the public-API guidance:

```ts
// runs in the Worker; seed RNG with crypto.getRandomValues(...)
const rng = mulberry32(seedFromCrypto());
for (let i = 0; i < n; i++) {
  const shot = runG4Shot(theta, rng);
  controller.enqueue(encoder.encode(`data: ${JSON.stringify({ i, ...shot })}\n\n`));
}
```

The client (`src/routes/nadarasa.stream.tsx`) consumes the stream and runs a live verification gate: collect ≥ 500 shots, compute empirical `P̂(y | b)`, compare to analytic `P(y | b)` derived from the kernel; toggle a **Live-verified** badge when `max |P̂ − P| < 0.05`, **Drift** otherwise.

## Multi-kernel dispatch

When porting more than one kernel, take a `?kernel=` query parameter and dispatch in the SSE handler. Each kernel ships its own `meta.predicted` block; the client uses that to drive both the **Live-verified** gate (sample-vs-analytic) and any structural-tension chip (analytic-vs-baseline). Keep the kernel choice + its parameters in the URL so a session is reproducible.

## When NOT to use this

- **More than ~4 qubits.** Statevector size blows up; the Worker has a CPU and memory budget. Keep big circuits on Selene.
- **Anything needing Selene's real noise model, real compilation, or anything beyond the trivial gate set.** The mini-sim is a teaching tool, not a Selene replacement.
- **Anything where the Python driver is the proof.** The frontier-verified result lives in `src/data/demos/<name>.json`; the live stream is a UX layer on top of an already-verified experiment, not a substitute for one.

## Lesson: derive the predictor from the circuit, not the docstring

The first G1 live port reused the offline driver's stated closed form, `P(y|s) = (1 + cos(2π y s / N)) / N`. The shots disagreed by ~0.4. The samples were right; the closed form was wrong — the Guppy kernel applies `H^n` + Z-basis readout (Walsh–Hadamard), not a real QFT, so the Fourier-basis formula does not apply. Always re-derive the predictor from the gates the kernel actually executes; the live sampler is the cheapest way to surface a mismatched analytic, and once corrected it sharpened the G1 verdict rather than weakening it.

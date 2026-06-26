# Clinical Use Cases for Quantinuum / Guppy / Selene

Reference for mapping clinical ideas to the quantum stack in this repo. Use with the QuantinuumClaw skill (root SKILL.md).

## Drug Discovery / Molecular Simulation

- **Selene use-case:** `chemistry`
- **Guppy:** VQE-style or other molecular energy/property circuits; parameterize molecule (e.g. H2, LiH), bond length, basis; measure energy or observables.
- **API params (example):** `shots`, `molecule_type`, `basis`, `geometry`.
- **Frontend:** Input molecule/geometry; run computation; show energy, convergence, or property table.
- **Demo tip:** Use mock/emulator with a small molecule; show same API contract as production.

## Treatment / Resource Optimization

- **Selene use-case:** `optimization`
- **Guppy:** QAOA or similar; encode objective (e.g. cost, wait time, fairness); return optimal or near-optimal solution.
- **API params (example):** `shots`, `precision`, `max_iterations`, problem-specific (e.g. number of patients, time windows).
- **Frontend:** Sliders/inputs for problem size and constraints; "Optimize" button; display solution and metrics.
- **Demo tip:** Small instance (few variables) so runs finish quickly on emulator.

## Patient Stratification / Classification

- **Selene use-case:** `ml`
- **Guppy:** Quantum ML circuit (e.g. QNN, kernel); inputs = feature vector; output = class or risk score.
- **API params (example):** `shots`, `learning_rate`, `epochs`, feature vector or dataset reference (synthetic only for demos).
- **Frontend:** Upload or select synthetic cohort; run training/inference; show stratum or risk and simple metrics.
- **Demo tip:** Pre-trained or tiny model; avoid real PHI.

## Randomization (e.g. Clinical Trials)

- **Selene use-case:** `random`
- **Guppy:** Hadamard on qubits; measure; return unbiased bitstring or integer.
- **API params (example):** `bits`, `shots`.
- **Frontend:** "Generate randomization" → display assignment (e.g. arm A/B) and audit trail (e.g. bitstring).
- **Demo tip:** Emulator is sufficient; emphasize unbiased randomness and reproducibility (seed if supported).

## Security / Key Material

- **Selene use-case:** `crypto`
- **Guppy:** Quantum key distribution or quantum-safe key generation.
- **API params (example):** `bits`, `shots`.
- **Frontend:** Request key material; show "key ready" or hash; never display raw keys in UI in production.
- **Demo tip:** Use for protocol demos; keep keys server-side only.

## Data and Compliance Reminders

- Use **synthetic or de-identified** data only for hackathon demos.
- Do **not** send real PHI to Quantinuum or store it in Fly.io without a compliance plan.
- Store **API keys** in Fly.io secrets; add **auth** and **rate limits** for any public-facing API.
- For production, consider **HIPAA/DPA** and data residency; keep PHI in controlled environments.

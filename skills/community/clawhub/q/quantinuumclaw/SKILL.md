---
name: quantinuumclaw
description: Enables building and deploying quantum computing applications with Quantinuum, Guppy, Selene, and Fly.io. Use for the OpenClaw Clinical Hackathon, clinical or healthcare projects (drug discovery, treatment optimization, patient stratification, trial randomization), quantum-powered web apps, deploying quantum algorithms to the cloud, or integrating quantum results into user-facing interfaces.
---

# QuantinuumClaw – Quantum Guppy/Selene Stack

This skill provides everything needed to build production-ready quantum applications using **Quantinuum** (hardware/emulator), **Guppy** (quantum language), **Selene** (FastAPI backend), and **Fly.io** (deployment), with optional **Lovable** frontend. It is tuned for the **OpenClaw Clinical Hackathon** and general quantum web apps.

## When to Use This Skill

**Use when:**
- Building for the OpenClaw Clinical Hackathon or any clinical/healthcare quantum project
- Building web applications that use quantum computing (optimization, chemistry, ML, random, crypto)
- Deploying quantum algorithms as REST APIs or creating dashboards for quantum results
- User mentions: clinical, healthcare, drug discovery, treatment optimization, patient stratification, molecular simulation, clinical trials, Guppy, Selene, Fly.io

**Example requests:** "Build a quantum portfolio optimizer with a web interface" · "Deploy my Guppy algorithm to the cloud" · "Create a clinical molecular simulation demo" · "Set up a quantum ML service on Fly.io"

## Stack at a Glance

| Component   | Role |
|------------|------|
| **Quantinuum** | Quantum hardware (H-series) or emulator |
| **Guppy**      | Quantum programming (circuits, gates, measurement) |
| **Selene**     | FastAPI backend that runs Guppy and exposes REST API |
| **Fly.io**     | Hosts the Selene backend in the cloud |
| **Lovable**    | React/TS frontend template; use `assets/lovable-template/` or any app that calls the Selene API |

## Quick Start (One Command)

From the repo root:

```bash
python3 scripts/create_quantum_app.py \
  --app-name "clinical-demo" \
  --use-case "chemistry" \
  --description "Clinical molecular simulation" \
  --deploy
```

Then set `VITE_API_URL` in the frontend to your Fly.io app URL (e.g. `https://clinical-demo.fly.dev`).

**Clinical use-case → `--use-case` mapping:**

| Clinical idea                     | `--use-case`   | Notes |
|-----------------------------------|----------------|--------|
| Drug discovery / molecular sim    | `chemistry`    | Molecules, energy, properties |
| Treatment / resource optimization | `optimization` | QAOA-style optimization |
| Patient stratification / ML       | `ml`           | Quantum ML models |
| Trial randomization               | `random`       | Quantum RNG |
| Secure keys / protocols           | `crypto`       | Quantum-safe crypto |

General use cases (portfolio, finance, etc.) also use `optimization`, `chemistry`, `ml`, `random`, `crypto`, or `finance`. See `references/clinical-use-cases.md` for detailed clinical mappings.

## Full Workflow: Creating a Quantum Application

### Step 1: Define the use case
Identify the problem (optimization, simulation, ML, cryptography, clinical, etc.).

### Step 2: Create Selene backend
```bash
python3 scripts/setup_selene_service.py \
  --app-name "my-quantum-app" \
  --use-case "chemistry" \
  --description "Quantum chemistry simulator"
```
This creates a backend dir with FastAPI, health check, Dockerfile, and `fly.toml`.

### Step 3: Implement your Guppy circuit
Edit `my-quantum-app/main.py` → `QuantumService._run_real_quantum()`. Use `references/guppy_guide.md` for syntax. For clinical: chemistry (molecule, shots, precision), optimization (objective, constraints), ML (features, epochs).

### Step 4: Deploy to Fly.io
```bash
python3 scripts/flyio_deploy.py --app-name "my-quantum-app" --service-dir "my-quantum-app" --region "lhr"
```
Set secrets with `fly secrets set`; use emulator for demos if preferred.

### Step 5: Frontend
Use `assets/lovable-template/` or run:
```bash
python3 scripts/lovable_integrate.py \
  --app-name "my-frontend" \
  --backend-url "https://my-quantum-app.fly.dev" \
  --quantum-use-case "chemistry"
```
Then `npm install` and `npm run dev` in the frontend dir.

### Step 6: Connect and test
Point frontend `VITE_API_URL` to the Fly.io backend; hit `/health` to verify.

## Clinical Use Case Cheat Sheet

- **Drug discovery / molecular simulation:** `chemistry` — VQE-style energy/property in Guppy; expose molecule type and params via API.
- **Treatment / resource optimization:** `optimization` — Define objective (cost, wait time); run QAOA in Selene; display results in UI.
- **Patient stratification / classification:** `ml` — Map patient features to model inputs; return risk/stratum or classification.
- **Randomization (e.g. trials):** `random` — Quantum RNG from Guppy; expose bits/shots in API.
- **Security / key material:** `crypto` — Key generation or quantum-safe primitives; keep keys on backend only.

## Data and Compliance (Clinical / Hackathon)

- **Demos:** Use synthetic or de-identified data only. Do not send real PHI to quantum backends or store in Fly.io without a compliance plan.
- **API keys:** Store in Fly.io secrets (`fly secrets set`), never in code or frontend.
- **Production:** Add auth, rate limiting, and consider HIPAA/DPA; restrict CORS in Selene.

## Resources

### scripts/
- `create_quantum_app.py` — All-in-one: backend + deploy + frontend
- `setup_selene_service.py` — Scaffold Selene backend
- `flyio_deploy.py` — Deploy to Fly.io
- `lovable_integrate.py` — Frontend wired to backend URL

### references/
- `guppy_guide.md` — Guppy syntax, gates, circuits, examples
- `selene_api.md` — Endpoints, request/response, errors, jobs
- `flyio_config.md` — Fly.io scaling, regions, secrets, monitoring
- `lovable_patterns.md` — Frontend patterns, dashboard, API client
- `clinical-use-cases.md` — Detailed clinical use-case mappings and compliance notes

### assets/
- `selene-template/` — Backend boilerplate (main.py, Dockerfile, fly.toml, .env.example)
- `lovable-template/` — React/TS frontend with QuantumDashboard and API client

## Advanced: Multi-Quantum Use Cases

- **Optimization dashboard:** Selene + QAOA/VQE; Lovable with sliders; Fly.io with scaling.
- **Chemistry explorer:** Guppy molecular simulations; 3D viewer; optional persistent storage.
- **Quantum ML API:** Selene exposing QNN/QSVM; Lovable for training/predictions; Fly.io (GPU if needed).

## Performance, Cost, and Security

- **Queuing:** Use job queues for long-running quantum jobs; WebSockets or polling in frontend.
- **Caching:** Cache identical computations to reduce quantum hardware cost.
- **Fly.io:** Scale to zero when idle (`min_machines_running = 0`); use `references/flyio_config.md` for VM sizing.
- **Security:** No API keys in frontend; rate limiting on Selene; HTTPS in production; see `references/selene_api.md` for auth patterns.

## Troubleshooting

- **Guppy import error:** `pip install guppy` in backend; or use mock mode for demos.
- **Selene not starting:** Check `fly.toml`, `fly logs`, and env vars.
- **Frontend can’t connect:** Verify `VITE_API_URL`, CORS in Selene, and `curl .../health`.
- **Fly.io deploy fails:** `fly deploy --clean`; `fly logs --phase build`; ensure `fly auth login`.
- **Quantum results wrong:** Validate circuit logic and measurement; test with emulator first.

## Next Steps

After initial setup: monitor quantum usage/costs; add auth to Selene if public; improve error handling and logging; consider persistence for job history.

---

For detailed clinical use-case specs and compliance reminders, see `references/clinical-use-cases.md`.

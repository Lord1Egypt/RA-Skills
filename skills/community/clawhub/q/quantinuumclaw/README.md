## QuantinuumClaw – Quantum Guppy/Selene Stack for Clinical Hackathons

**QuantinuumClaw** is a starter kit and Cursor skill bundle for the **OpenClaw Clinical Hackathon**.  
It gives participants a batteries-included way to:

- **Write quantum algorithms** in **Guppy** targeting **Quantinuum** hardware or emulators.
- **Expose them as APIs** using a **Selene** (FastAPI) backend.
- **Deploy the backend** to **Fly.io** with a single command.
- **Connect a Lovable/React frontend** for interactive clinical demos.

The same stack works for any quantum web app, but the docs and examples in this repo are tuned for **clinical and healthcare** projects (drug discovery, treatment optimization, patient stratification, trial randomization, etc.).

> The public GitHub repo backing this project is [`arunnadarasa/quantinuumclaw`](https://github.com/arunnadarasa/quantinuumclaw).

---

## 1. Architecture at a Glance

- **Quantinuum** – Quantum hardware (H-series) or emulator.
- **Guppy** – Quantum programming language with a Pythonic API.
- **Selene** – FastAPI backend service that:
  - Wraps Guppy circuits,
  - Exposes REST endpoints for quantum jobs,
  - Manages jobs, errors, and health checks.
- **Fly.io** – Cloud platform that runs the Selene backend.
- **Lovable (React/TS)** – Frontend UI that calls the Selene API and visualizes quantum results.

```text
Browser (Lovable/React)
        │  HTTPS
        ▼
Selene backend (FastAPI on Fly.io)
        │  Python + Guppy
        ▼
Quantinuum hardware or emulator
```

Key reference docs in this repo:

- `SKILL.md` – Full Quantum Guppy/Selene skill reference.
- `references/guppy_guide.md` – Guppy language & circuit patterns.
- `references/selene_api.md` – API endpoints, job models, errors.
- `references/flyio_config.md` – Fly.io deployment & tuning.
- `references/lovable_patterns.md` – Frontend/React patterns.

For hackathon and clinical use-case details, see the root **SKILL.md** (QuantinuumClaw skill) and `references/clinical-use-cases.md`.

---

## 2. Quick Start (5–10 Minutes)

### 2.1. Prerequisites

- **Python** ≥ 3.10
- **Node.js** ≥ 18 and **npm**
- **Fly.io CLI** (`flyctl`) – see `references/flyio_config.md`
- (Optional) Access to **Quantinuum** hardware; otherwise use the emulator

From the repo root:

```bash
cd quantum-guppy-selene
```

### 2.2. One-Command Full App Creation

This script scaffolds:
- A **Selene backend** with a Guppy example circuit,
- **Fly.io deployment** (optional),
- A **Lovable/React frontend** wired to the backend.

```bash
python3 scripts/create_quantum_app.py \
  --app-name "quantum-coin-flip" \
  --use-case "random" \
  --description "Quantum coin flip for trial randomization" \
  --deploy
```

This will:
- Create a backend directory (e.g. `quantum-coin-flip/`),
- Deploy it to Fly.io (URL like `https://quantum-coin-flip.fly.dev`),
- Create a frontend (e.g. `quantum-coin-flip-frontend/`) that talks to that URL.

Then start the frontend:

```bash
cd quantum-coin-flip-frontend
npm install
npm run dev
```

Open the local dev URL and trigger quantum computations from the browser.

---

## 3. Clinical Use Cases Cheat Sheet

The stack is general-purpose, but for the **OpenClaw Clinical Hackathon** you’ll mostly map to these use cases:

| Clinical idea                               | `--use-case`  | What the quantum part does                                       |
|---------------------------------------------|---------------|-------------------------------------------------------------------|
| Drug discovery / molecular simulation       | `chemistry`   | VQE-style energy/property estimation for small molecules          |
| Treatment / resource optimization           | `optimization`| QAOA-like optimization of schedules, resources, or allocations    |
| Patient stratification / risk classification| `ml`          | Quantum(‑inspired) ML models for clustering or classification     |
| Trial randomization                         | `random`      | Quantum random number generation for unbiased assignment          |
| Secure keys / protocols                     | `crypto`      | Quantum-safe key material or protocol building blocks             |

You can find more detail in `references/clinical-use-cases.md`.

---

## 4. Detailed Developer Workflow

### 4.1. Full Application Creation (Backend + Frontend + Deploy)

```bash
# 1. Generate everything
python3 scripts/create_quantum_app.py \
  --app-name "quantum-portfolio" \
  --use-case "optimization" \
  --description "Portfolio optimization using quantum algorithms" \
  --deploy

# 2. The script creates:
#    - quantum-portfolio/ (Selene backend)
#    - quantum-portfolio-frontend/ (Lovable frontend)
#    - Deploys backend to Fly.io
#    - Backend URL output for frontend config

# 3. Start frontend locally
cd quantum-portfolio-frontend
npm install
npm run dev
```

### 4.2. Manual Step-by-Step (More Control)

If you want more control than the one-command script:

#### 4.2.1. Create a Selene Quantum Service

```bash
python3 scripts/setup_selene_service.py \
  --app-name "my-quantum-app" \
  --use-case "chemistry" \
  --description "Quantum chemistry simulator"
```

This generates a backend project with:
- FastAPI service with CORS,
- Quantum execution endpoints,
- Health checks for Fly.io,
- Dockerfile and `fly.toml`,
- Example Guppy circuit (you will replace it with your own).

#### 4.2.2. Implement Your Guppy Circuit

```bash
cd my-quantum-app
# Edit main.py → QuantumService._run_real_quantum()
```

See [Customizing Quantum Algorithms](#6-customizing-quantum-algorithms) below for details.

#### 4.2.3. Deploy to Fly.io

```bash
python3 ../scripts/flyio_deploy.py \
  --app-name "my-quantum-app" \
  --service-dir "$(pwd)" \
  --region "lhr"
```

This will:
- Create/configure the Fly.io app,
- Build and deploy the container,
- Print the public URL (e.g. `https://my-quantum-app.fly.dev`).

#### 4.2.4. Create a Lovable Frontend

```bash
cd ..
python3 scripts/lovable_integrate.py \
  --app-name "my-quantum-frontend" \
  --backend-url "https://my-quantum-app.fly.dev" \
  --quantum-use-case "chemistry"
```

The generated frontend will:
- Include a `QuantumDashboard` component,
- Provide parameter controls (shots, precision, etc.),
- Call your Selene endpoints and show results.

Start it with:

```bash
cd my-quantum-frontend
npm install
npm run dev
```

---

## 5. Repository Layout

```text
quantum-guppy-selene/
├── SKILL.md                    # QuantinuumClaw skill (quantum + clinical hackathon)
├── scripts/
│   ├── create_quantum_app.py   # All-in-one creator
│   ├── setup_selene_service.py # Backend generator
│   ├── flyio_deploy.py         # Fly.io deployment
│   └── lovable_integrate.py    # Frontend generator
└── references/
    ├── guppy_guide.md          # Guppy language reference
    ├── selene_api.md           # Selene API documentation
    ├── flyio_config.md         # Fly.io configuration guide
    └── lovable_patterns.md     # Frontend patterns
└── assets/
    ├── selene-template/        # Backend template files
    │   ├── main.py
    │   ├── requirements.txt
    │   ├── Dockerfile
    │   ├── fly.toml
    │   └── .env.example
    └── lovable-template/       # Frontend template files
        ├── package.json
        ├── vite.config.ts
        ├── src/
        │   ├── components/
        │   │   ├── QuantumDashboard.tsx
        │   │   └── ui/Card.tsx, Button.tsx
        │   └── lib/api.ts
```

---

## 6. Customizing Quantum Algorithms

In any generated backend, implement your quantum logic in:

```python
def _run_real_quantum(self, params: Dict[str, Any]) -> Dict[str, Any]:
    from guppy import quantum

    n_qubits = params["n_qubits"]

    with quantum() as q:
        qbits = q.qubits(n_qubits)

        # Your quantum circuit
        q.h(qbits[0])
        for i in range(1, n_qubits):
            q.cx(qbits[0], qbits[i])

        result = q.execute(shots=params.get("shots", 1000))

    return {
        "bitstring_counts": dict(result),
        "n_qubits": n_qubits,
        "most_frequent": max(result, key=result.get),
    }
```

Map `params` to your clinical use case, e.g.:
- `molecule_type`, `basis`, `geometry` for **chemistry**,
- `max_iterations`, `penalty_weights` for **optimization**,
- `features`, `epochs`, `learning_rate` for **ML**.

For Guppy language details, see `references/guppy_guide.md`.

---

## 7. Deploying to Fly.io

### 7.1. Prerequisites

1. Install `flyctl` (see `references/flyio_config.md` for up-to-date links).
2. Login: `fly auth login`
3. (Optional) Have a Quantinuum API key if you’re targeting real hardware.

### 7.2. Basic Deployment Steps

```bash
# In your backend directory (for a generated app)
cd my-quantum-app

# Review fly.toml
cat fly.toml

# Set secrets (only for real hardware)
fly secrets set QUANTUM_API_KEY=your_quantinuum_key

# Deploy
fly launch --now

# Verify
fly open
curl https://your-app.fly.dev/health
```

### 7.3. Fly.io Configuration Highlights

Edit `fly.toml` for your needs:

```toml
app = "your-unique-app-name"
primary_region = "lhr"

[[http_services]]
  auto_stop_machines = true   # Scale to zero
  min_machines_running = 0
  max_machines_running = 10

  [[http_services.concurrency]]
    type = "requests"
    value = 50
```

See `references/flyio_config.md` for detailed sizing, scaling, and cost tips.

---

## 8. Frontend Integration (Lovable / React)

The Lovable frontend connects automatically to the backend API:

1. Set `VITE_API_URL` environment variable in Lovable:
   ```bash
   VITE_API_URL=https://your-app.fly.dev
   ```

2. The `QuantumDashboard` component:
   - Parameter controls specific to your use case
   - One-click computation
   - Real-time results with statistics
   - Error handling and loading states

3. Build and deploy to Lovable:
   ```bash
   npm run build
   # Upload dist/ to Lovable hosting
   ```

`references/lovable_patterns.md` contains a full `QuantumDashboard` pattern, result visualization patterns (e.g. Recharts), and job-polling examples.

---

## 9. Monitoring, Costs, and Security

### 9.1. Monitoring & Logs

```bash
fly logs --tail --app your-app
```

### 9.2. Metrics & Costs

```bash
fly metrics --app your-app
fly balance  # Check costs
```

### 9.3. Updating Deployments

```bash
# Rebuild and redeploy
fly deploy --app your-app

# Update secrets
fly secrets set NEW_KEY=value --app your-app

# Roll back if needed
fly deploy --rollback --app your-app
```

### 9.4. Cost Management

- Use `min_machines_running = 0` to scale to zero when idle.
- Start with smaller VM sizes (see `references/flyio_config.md`) and scale up only if needed.
- Cache results for repeated computations (e.g. repeated molecular configs).
- Use the emulator (`QUANTUM_HARDWARE=emulator`) during development.

### 9.5. Security (Especially for Clinical Context)

- Never commit API keys; set them with `fly secrets set`.
- For public demos, use an API key and simple auth check in Selene.
- Lock down CORS in production (`allow_origins` in `main.py`).
- Always serve over HTTPS (`force_https = true` in `fly.toml`).
- Treat clinical data carefully: use synthetic or de-identified data for hackathons.

---

## 10. Support & Further Reading

- Repo: [`arunnadarasa/quantinuumclaw`](https://github.com/arunnadarasa/quantinuumclaw)
- Quantum language & circuits: `references/guppy_guide.md`
- Backend API and jobs: `references/selene_api.md`
- Fly.io deployment details: `references/flyio_config.md`
- Frontend patterns and charts: `references/lovable_patterns.md`
- Clinical use-case details: `references/clinical-use-cases.md` (root SKILL.md is the combined QuantinuumClaw skill)

Use this repo as a **launchpad**: pick a clinical idea, choose the closest `--use-case`, implement your Guppy circuit, and ship a full-stack quantum demo in hours instead of weeks.

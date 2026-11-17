# Lovable output hygiene (EndoTrack-hardened, generic)

The EndoTrack programme produced a disciplined app-building workflow for Lovable: a single project brain, a certified/forbidden-language table, explicit re-ingest rules, and a non-negotiable convention checklist. This card ports those patterns into the Nadarasa/Quantinuum context so any future Lovable-generated surface stays honest.

## 0. The project brain — ingest FIRST

The single source of truth for any LLM tool (Lovable, GPTs, other agents) is:

```
public/llms-full.txt   (built by scripts/build-llms-txt.mjs; ~240 KB as of v0.4.10)
```

- Paste the whole file into a new LLM session before building or editing any surface that touches the quantum results.
- If the file has changed since the last session, re-ingest the new version before continuing. Stale context is the #1 source of wrong output.
- The skill cards in `.agents/skills/quantinuum/` are the runtime instruction layer; the LLM corpus is the factual layer. Use both.

## 1. The certified-state / forbidden-language table

Every generated page must pass through this table. If a claim is not in `public/llms-full.txt` or the committed `src/data/demos/*.json` files, it does not go in the UI.

| Topic | Certified state (say THIS) | Forbidden (never say) |
|---|---|---|
| AQFT crossover law (G26) | 24/24 cells satisfy the analytic bound; strict wins in 2 cells; 72-gate saving on n=10; TKET corroborates 72/72 equivalent and 20/20 savings; Nexus H2-1LE/H2-Emulator/Helios-1E-lite n=6 slice matched within 0.125 tolerance | "Quantum speedup", "provably optimal", "classically intractable" |
| QPDE ethylene gap (G16) | Selene gap fit 0.8099 Ha vs classical 0.8000 Ha; 20/20 PASS | "Solved molecular electronic structure", "beats VQE" |
| Noise/ZNE (G17) | Richardson quadratic ZNE on H2-class depolarizing ladder; model-free curve χ² reported | "Error-corrected", "exponential suppression" |
| TDA Laplacian moments (G18) | C6 vs 2C3 distinction via Taylor-fit moment estimators; conditioning-limited, not shot-limited | "Quantum machine learning advantage", "classified graphs" |
| Floquet native port (G20) | Mixed-field Ising on chain + heavy-hex-6; ideal-vs-ED max deviation 0.0495; ZNE to <2% error | "Demonstrated quantum simulation of [real material]" |
| ADAPT-GQE composition (G21) | H2 UCCSD single excitation verified by matrix oracle; 512-shot Selene agreement 0.018 | "Generative AI discovered a new ansatz" |
| TKET compile lane (G24) | Offline `QuantinuumBackend("H2-2")` compilation; unitary-equivalence oracle gates every count; Simon is the one non-local case where the rewriter stays ahead | "TKET validates quantum advantage", "compiler proved correctness" |
| Nexus executions | Emulator lanes (H2-1LE, H2-Emulator, Helios-1E-lite, Aer, Qulacs, Selene, SelenePlus) with receipted job ids; 0.0000 HQC billed for emulators on this account | "Ran on H2 / Helios QPU", "real hardware execution" |
| Evidence chain | Machine-checked verdicts for G1-G26; SHA-256 provenance hashes; per-job meters; legacy backfill in place | "Cryptographically verified", "tamper-proof" |

If a claim has been withdrawn or superseded, the current state must reflect the withdrawal, not a softened version of the old claim.

## 2. Re-ingest rule

Before any Lovable build that touches science, demo numbers, or evidence copy:

1. Check the file date/size of `public/llms-full.txt`.
2. If it is newer than the last session, paste the full contents into the chat or upload it as project knowledge.
3. If a route's `head()` metadata or a `src/data/demos/*.json` file changed, re-ingest after the build script has run.

Stale context produces stale claims. A stale claim is a rollback risk.

## 3. The eight conventions (non-negotiable for every Lovable build)

1. **Framing**: Nadarasa Reduction / quantum reduction methods only. No disease-specific clinical claims unless the route explicitly supports them.
2. **Numbers**: only numbers from `public/llms-full.txt`, `src/data/demos/*.json`, or committed `src/data/nadarasa/*.json` files — never invent AUC, fidelity, or gate-count figures. Every number in the repo carries shots+seed or a SHA-256 provenance hash; if it lacks a receipt, it does not go in the UI.
3. **Mock/real toggles**: any demo/payment/hardware UI needs an explicit mock/real switch. No fake "live" status.
4. **Clickable receipts**: tx hashes link to testnet.arcscan.app (new tab); (mock) labels when no real reference exists.
5. **No secrets in the page**: Nexus tokens, Alchemy RPC keys, and payer private keys are env-only, never in Lovable-generated code or the portal.
6. **Static-only serving**: Lovable Cloud/Cloudflare Workers have no server-side secrets. Quantum results are shipped as committed JSON, not live server functions.
7. **Verification honesty**: if showing the trust story, use the three layers — L1 receipts (live), L2 arbiters incl. per-batch Bell control (live), L3 cryptographic verification (pre-registered QPU target, NOT claimed today). Never "cryptographically verified".
8. **Skill and API contracts**: MCP tools, A2A cards, bridge routes, and x402 wire formats must stay intact. Generated code must not break these contracts.
9. **Circuit orthography**: if surface copy cites certified circuits, reference the structural audit (`references/agent-native-evidence.md`) and the `circuit_structure` convention — never invent circuit statistics.
10. **Anchors are not compliance**: citing a verified vocabulary identifier (SNOMED CT, dm+d, ICD-10, an NHS dataset code) anchors a term — it is not a claim of standards compliance, certification, or clinical validation. Write "SNOMED-anchored terminology", never "SNOMED compliant", and never let an identifier imply the artefact passed a conformance process it has not been through. Same discipline as the engine qualifier: the label names what was done, not what it resembles.
11. **Attribution travels with the work**: where the clinical framing, pathway, or IP belongs to someone else, the credit line ships on every surface that uses it — page footer, README, exported PDF, agent card — not only on the about page. An attribution that exists in one place is an attribution that gets dropped by the next refactor.



## 4. Close with a checklist, not a claim

End every Lovable build with a compact pass/fail report:

```
✅ Framing (quantum-reduction-only, no disease/BCAC/CRUK terms scanned)
✅ Numbers (every figure traced to llms-full.txt / src/data/demos/*.json)
✅ Toggles (mock/real where relevant)
✅ Receipts (tx links → arcscan, (mock) labels where needed)
✅ Secrets (none in generated code/pages)
✅ Static gate (committed JSON, no live server functions for quantum results)
✅ Science honesty (withdrawal + shot-scaling verdict + dequantization gate respected)
✅ Contracts (MCP/bridge/A2A/skill contracts intact)
✅ Anchors + attribution (identifiers labelled as anchors, credit line on every surface)
```


If any item fails, list it in priority order — do NOT claim done.

## 5. Edge cases

- **Lovable lacks context** → point it at `public/llms-full.txt` or the built `llms.txt`; re-ingest before continuing.
- **"An internal error occurred" toast** → see `references/lovable-orchestration.md`: diagnose in 30 seconds, then shift to gated atomic gates.
- **Stale science in context** → re-ingest; verify the withdrawal language and shot-scaling verdict survived.
- **A requested figure isn't in the brain** → do not invent it; state it is not in the certified set and ask for the repo path.

# Serving quantum evidence to agents

Once results live as committed JSON (the rule in `references/selene-runtime.md`), the same
artifacts can be exposed to other agents rather than only to a web page. This is the
"agent-native" layer: an MCP tool surface, a discovery card, and — optionally — a payment
gate. It is orthogonal to the physics, but it is what turns a results folder into something
another system can query and cite.

## Principle: the artifact is the API

Every tool returns a **committed JSON file**, verbatim, with its shots/seed/backend metadata
intact. No tool recomputes, rounds, or summarises. If an agent asks for a number that is not
in an artifact, the correct response is "not measured", not a plausible value.

## MCP server shape

A stdio JSON-RPC server with zero third-party dependencies (stdlib only) is enough and is the
most portable thing to hand a teammate. A useful tool set looks like:

| Tool | Returns |
| --- | --- |
| `certified_results` | the headline comparison cells (metric, classical baseline, verdict) |
| `sweep_rows` | per-cell sweep rows (n, shots, pass/fail) |
| `demo_links` | verified links to browser-runnable demos |
| `roadmap_status` | phases and their state |
| `model_card` | limitations, governance, data boundary |
| `verify_artifact(name)` | the raw committed JSON for `<name>.json` |
| `circuit_structure(circuit)` | structural audit of a certified circuit (see below) |
| `execute_circuit(circuit)` | a credential-free submission spec (see below) |

`verify_artifact` is the important one: it makes every claim independently checkable in one
call. Test the server with the official MCP SDK client, not with a hand-rolled harness — the
framing/handshake details are where stdio servers break.

## Structural audit (`circuit_structure`)

Circuit statistics quoted in prose drift. Compute them from the compiled circuit and serve
them: total gate count, two-qubit (CX) fraction, gate histogram, depth, and **per-qubit idle
windows** as `[start, end]` moment ranges. The audit is not trivia — each field is an
engineering signal:

- **A long ancilla idle band** (e.g. moments `[28, 64]` on the SWAP-test ancilla) is exactly
  where dynamical decoupling goes. If DD helps nowhere else, it helps there.
- **A repeating parity-window cadence** (e.g. `[2,9] [11,18] [20,34]`) is the error-detection
  rhythm of an encoded circuit. If the cadence does not match the encoding you believe you
  compiled, the compiler dropped or merged rounds — catch it here, not in the fidelity.
- **CX fraction and depth** are the honest way to compare a rewritten circuit against its
  original; a reduction claim quotes the audit for both.

Rule: any surface copy or agent answer that cites circuit statistics reads them from this
tool. Never restate remembered gate counts, and never let a page hardcode a number the audit
would contradict.

## Execution specs without credentials (`execute_circuit`)

An agent can be handed a *submission contract* rather than a submission: builder path
(pytket vs HUGR), target device, shots, the config class and its required fields, and the
verification discipline (baseline to compare against, envelope, control circuit). The spec is
plain data and carries **no tokens** — actual submission happens on a runner that already
holds the session, with env-only credentials.

Two rules keep this honest:

- **A spec is not a receipt.** Serving an execution spec never implies the run happened. The
  response carries no fidelity, no job id, and no "verified" wording — those only appear once
  a real job id and its committed artefact exist.
- **The spec must be the same one the runner uses.** If the tool describes a device or shot
  count the runner does not use, the spec is fiction. Generate it from the same source the
  submission path reads.

The shape converges independently: PASQAL's agentic-workflow write-up arrives at
the same object under the name `experiment_spec.json` — a declarative,
credential-free description of the experiment, handed between an agent and the
thing that actually runs it. When two teams reach the same artefact from
different directions, that is the interface, not a local convention.

## The verification gap — the real failure mode of agent-run experiments

The same PASQAL study is the cleanest vendor-controlled demonstration of what
goes wrong: the agent proposed a **plausible but wrong observable** and then a
wrong hardware diagnosis to explain the result. Nothing in the pipeline caught
either. Domain-expert review did, after 43 exchanges.

The lesson is specific, and it is not "agents are unreliable":

- An agent's *choice of observable* is a scientific judgement wearing the
  clothes of a configuration field. It looks like `"observable": "ZZ"` sitting
  next to `shots` and `seed`, so it inherits their apparent triviality — and it
  is the one field in the spec that no downstream check validates.
- Every automated layer downstream is **consistency** checking, not
  **correctness** checking. A wrong observable measured perfectly passes the
  envelope, the Bell control, the digest, and the verdict test.
- So the review gate belongs *before* execution, on the spec, and it must be a
  human who knows the physics. Put the observable, the baseline it is compared
  against, and the falsification criterion in the spec explicitly, so the thing
  needing review is legible in one screen rather than buried in a driver.
- A confident wrong diagnosis of *hardware* behaviour is the second-order
  version of the same failure and costs more, because it sends someone to
  re-run on a different backend to chase an explanation that was invented.


## Discovery card

If the evidence is also served over HTTP, publish an agent card at **both**
`/.well-known/agent.json` and `/agent.json`. Static hosts (GitHub Pages among them) 404 on
hidden dot-directories, so the well-known path alone silently fails discovery.

## Paid evidence (x402), if you need it

The 402 flow is small enough to implement directly:

1. Unpaid call → HTTP **402** with a challenge body listing accepted payments:
   `{"accepts": [{"symbol", "chainId", "payTo", "amount", "nonce"}]}` plus human-readable
   instructions.
2. Caller pays, retries with a `X-Paywall-Payment: base64(JSON{txHash, from, nonce, currency,
   amount})` header.
3. Server verifies the transaction against the chain explorer API, then returns the artifact
   plus a receipt.

Practical notes: price per currency in **base units** and check the decimals — a price copied
across currencies with different decimals produces reverts (a currency with 8 decimals priced
at a 6-decimal amount is 100× off). Some explorer APIs reject bare `urllib` and require a
browser `User-Agent`. Record failed/reverted transactions in the evidence table with their
cause rather than deleting them.

## Mock/real toggle — non-negotiable for demos

Any UI or bridge that can touch a live network carries an explicit `mode: "mock" | "real"`
per request, plus a `force_mock` override that lets the whole flow be verified offline. An
unarmed "real" call must return a clean challenge with arming instructions, never a fake
success. No demo ever shows a "live" status it did not earn.

## Serving a certified number

A tool that hands other agents a "certified" figure is a publication channel, so
it inherits the discipline in `evidence-integrity.md`:

- **Serve the current state, including when it is negative.** If the larger-`n`
  replication failed, the tool returns the negative with `beats: false` and a
  supersession notice pointing at the withdrawn result. A tool that keeps
  serving the flattering earlier number is how a withdrawn claim stays alive.
- **Fail loud on a missing artefact.** `verify_artifact`-style tools must raise
  when the current file is absent — never silently fall back to a superseded
  one. A fallback turns a withdrawal into a re-publication.
- **One default per question.** Two live artefacts answering the same question
  in opposite directions means the caller picks the answer, which is not
  evidence.
- **Ship the receipts with the value.** Job id, device, shots, seed, and the
  per-batch control verdict belong in the same response as the number, not in a
  separate "details" tool the caller will not call.

## Secrets


RPC URLs with embedded keys and any payer private key are environment-only. Grep the tree for
them before every push; a key in a committed demo file is the failure mode this whole layer
is most likely to produce.

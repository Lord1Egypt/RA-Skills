# Installation Contract

Schema: `openclaw.safe_update.installation_contract.v1`.

The installation contract is a declaration graph, not proof that the
installation is complete. It separates:

- capabilities and their business criticality, evidence policy, and explicit
  post-activation checks;
- components with one or more roles and descriptive application phases;
- artifacts and contracts that identify compatibility evidence;
- typed runtime, configuration, state, and contract dependency edges.

`business_criticality` is independent from `evidence_policy`. Layers or
application phases describe assembly order only; they never prove isolation or
justify omitting evidence.

The `contract` command deterministically translates the existing v1.1
customization and coverage manifests:

```bash
python3 scripts/openclaw_safe_update.py contract \
  --customizations assets/customizations.example.json \
  --coverage assets/coverage.example.json \
  --output artifacts/installation-contract.json
```

The adapter preserves every post-activation check and maps every referenced
customization check to a compatibility component. Unknown checks, duplicate
IDs, dangling dependency edges, invalid policies, and inconsistent reciprocal
capability/component references fail closed.

See `examples/signal-voice.installation-contract.json` for a capability that
spans core normalization, an add-on, configuration/personalization, and a live
post-activation check.

The composition step treats `npm_package` and `npm_archive_member` artifacts as
members of the exact core closure. Separately distributed `plugin_package`,
`sidecar`, `addon`, `external_asset`, `configuration_identity`, and
`personalization_contract` artifacts must use:

```text
<name>@<exact-semver>#sha256:<64 lowercase hex characters>
```

Declaration order has no effect on the composed root. Artifact bytes,
contract content, environment, analyzer version, and composition policy do.
See `examples/composed-installation.installation-contract.json` for a fixture
that combines core, Signal voice support, an MCP sidecar, configuration, and
personalization.

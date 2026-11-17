---
name: "runtime-config-propagation-debugging"
description: "Debug settings that work in one execution path but vanish in another by tracing config resolution through every runtime entry point."
---

# Runtime config propagation debugging

## Use when
A setting works in one execution path but is missing or ignored in another, especially when a plugin has ordinary and alternate modes such as direct synthesis and Talk.

## Procedure
1. Name the observable behavior and trigger. Distinguish request-time reads from startup-only initialization.
2. Read the smallest available effective-config or status surface before opening source. A persisted setting is not proof of the live value.
3. List every runtime entry point that can invoke the feature. Treat each mode as a separate config pipeline until proven otherwise.
4. Search exact entrypoint, resolver, and field symbols; then trace each path from handler to provider resolver to final operation. Record which config snapshot and provider block each layer receives.
5. Compare merge inputs and precedence. Preserve this order when applicable: provider defaults, contextual state/profile, explicit per-request overrides.
   - For optional allowlists, distinguish omitted, empty, and populated values from the schema; they may mean unrestricted, deny all, and allow only listed entries.
   - Treat persisted state as one precedence layer, not an unconditional command, unless the call path proves otherwise.
6. Check nested provider selection explicitly. If base config contains multiple providers, inherit only the active provider's block; do not spread the whole base config into provider-specific settings.
7. Inspect normalization, defaults, validation, and missing/invalid-state behavior. Attribute behavior only to fields the resolver actually consumes.
8. Add a focused resolver test for the failing path. Include a setting present only in the base provider block and an explicit mode override; assert both survive and the explicit override wins.
9. Run the narrow resolver/provider tests, type checking, and build before runtime verification.
10. After reload or restart, re-read the effective config and revision/hash. Confirm the active provider and formerly missing settings are present.
11. Execute one real request through the previously failing entry point.
12. Verify both boundaries: inspect the returned artifact or metadata, then inspect downstream logs for the effective provider/model/style or equivalent resolved values.
13. Update operational notes only after live evidence replaces pending or stale state.

## Pitfalls
- Fixing the core operation but not alternate-mode resolvers leaves a second gap.
- Broad source or documentation dumps hide the relevant assignment; search exact symbols and open narrow ranges.
- Comments and docs establish intent, while assignments, calls, and runtime evidence establish behavior.
- A fallback in one layer does not prove end-to-end fallback.
- Unit success does not prove the running process loaded rebuilt output.
- A label such as `Neutral` may be a valid mapped profile, not evidence that contextual selection failed; verify the effective model, profile, and weight together.
- A cold backend load can exceed steady-state latency. Distinguish initialization delay from a propagation defect using backend timing logs.
- Do not call unrelated full-suite timeouts proof of regression; report narrow passing gates separately.

## Verification
Require all three signals before declaring success:
- focused test proves provider-block inheritance and override precedence;
- live resolved config contains the setting on the affected path;
- a real request succeeds and downstream logs show the expected effective selection.

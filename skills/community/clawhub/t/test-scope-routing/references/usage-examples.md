# Usage Examples

Use these examples as routing patterns, not as fixed commands. Replace each command with the target project's documented equivalent.

## Documentation or copy change

**Change:** README wording or a low-risk label.

**Route:** L0, or no executable test if the project has no documentation checker.

**Record:** The affected document, the static check if one exists, and why database, browser, and full regression checks were not relevant.

## Pure logic change

**Change:** A rule calculation, reducer, model, or utility function.

**Route:** L1 with the related test file when supported. Add broader unit or coverage checks at the project's merge boundary.

**Record:** The rule and error cases covered; do not claim UI or network coverage from unit results.

## User-visible flow change

**Change:** A settings form, navigation path, offline state, or PWA interaction.

**Route:** L1 when local logic changes, plus the smallest relevant L2 browser or component journey. Do not run unrelated authenticated or database flows.

**Record:** The browser/device or component environment, journey covered, and any skipped flows.

## Data or permission boundary change

**Change:** Database schema, RLS, authentication, synchronization, export, deletion, or a server function.

**Route:** Relevant L1 and L3 checks. Add affected UI journeys. Use L4 before merge or release.

**Record:** The tenant/permission boundary, failure and recovery cases, local service prerequisites, and whether production state remains unverified.

## Release or high-risk change

**Change:** Dependency, build system, Service Worker, CSP, public resource, release script, or merge/release candidate.

**Route:** The project's L4 gate, including the required build, security, integration, E2E, artifact, and production checks.

**Record:** Exact commands, final artifacts, environment blockers, and any production URL or deployment verification that was not performed.

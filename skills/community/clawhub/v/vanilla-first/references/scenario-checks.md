# Vanilla-first scenario checks

Use these cases to check whether a candidate instruction respects both the supported path and the actual owner. They are synthetic review fixtures, not current status assertions or permission to mutate external systems.

## 1. Unaccepted adjacent data contract

**Setup:** A team proposes optional cross-service metadata synchronization for a product. Maintainers have accepted a narrower record-update change, but have not accepted the new synchronization contract.

**Expected:** Keep the new capability at investigation/design level. Distinguish the accepted record-update scope from the proposed synchronization contract. Continue source research or a local draft when authorized; do not implement behavior that depends on the unresolved owner contract. Name the exact maintainer decision needed.

**Failure signs:** Treating a label as approval for the new contract; exercising the proposed behavior against production records; making the user seek approval for local source review or a draft; describing fixture tests as server proof.

## 2. Operator-selected change in a local fork

**Setup:** A team maintains a local fork of a command-line formatter and authorizes a small compatibility change there. The upstream checkout must remain untouched while the fork behavior is checked.

**Expected:** Verify the repository and owner boundaries, preserve existing work, and make only the authorized local change. No external maintainer preapproval is needed for this fork-owned patch. Report remote changes only after readback. Do not publish or claim upstream acceptance outside the scope.

**Failure signs:** Requiring an upstream maintainer to authorize an owned-code change; silently changing upstream source; overwriting custom work; claiming a remote change from a dispatched command; expanding into feature work.

## 3. Documented configuration path

**Setup:** The exact product version documents a configuration option that satisfies the requested behavior, and the user authorized a reversible local configuration change.

**Expected:** Use that setting, inspect the before/after configuration, and perform the narrow runtime check needed to prove it took effect. Avoid a custom plugin or fork. Do not create a separate maintainer-approval gate for the supported change.

**Failure signs:** Using an option documented only for another version; inferring an undocumented key; saying the runtime works after only editing a file; asking an external maintainer to approve ordinary supported configuration.

## 4. Explicitly rejected upstream design

**Setup:** The owning upstream maintainer explicitly rejected a proposed architecture boundary. The patch branch and its tests remain available.

**Expected:** Stop repeated review, rebase, CI, and score loops for the rejected design. Preserve the branch and evidence as history. Identify any separate supported integration that fits the owner's contract. A local-fork alternative requires operator authority and must be described as local, not as upstream-approved.

**Failure signs:** Treating an open follow-up issue as reversal of the rejection without an explicit owner statement; presenting the rejected branch as roadmap; assuming upstream rejection forbids all authorized local work.

## 5. Apparently missing feature

**Setup:** A capability is absent from the UI or a remembered skill, but the exact version may expose it through a supported CLI, API, configuration, or extension point.

**Expected:** Check the exact version's primary docs and source/entry point, then map the requirement to the existing route. If absent, state the smallest demonstrated gap and compare a thin integration, upstream change, fork, or replacement against it. Keep source proof distinct from runtime proof.

**Failure signs:** Declaring absence after checking one UI surface; implementing a wrapper before checking the supported API; describing a speculative interface as supported; proposing a rewrite from a single missing route.

## 6. Open but stale pull request

**Setup:** A PR is still open, while its issue may have been closed by a merged successor or current upstream may already contain the behavior.

**Expected:** Inspect the issue closure vehicle, successor, current source, and relevant PR diff. If superseded, label the contribution superseded in the local report and preserve useful diagnosis/credit. If still live, state the exact missing behavior and current base. Do not comment, close, push, or merge without authority for that action.

**Failure signs:** Treating `OPEN` as proof the patch is needed; repeatedly refreshing a PR after a merge resolved the issue; claiming a contribution was rejected when it was incorporated through another change.

# Opt-in host context, bindings and accounting

These Python helpers support a host integrating the scenario procedures. They do
not change the default MCP tool list, start a gateway or run an autonomous agent.
No official AI Hub/MCP interface has been validated. The bindings below are an
integration contract, not a vendor adapter or a compatibility claim.

## Prepare the selected context

Use `vmware_debug.ops.scenario_context.prepare_context(profile, manifests,
allowed, targets, allowed_targets)`. Select one explicit profile from
`gateway-toolsets.json`; do not infer a target from a symptom. `manifests` maps
backend names to live tool-name/schema dictionaries. The remaining dictionaries
are trusted host declarations of tool permissions, chosen target and permitted
targets per backend. The result includes only required backend-qualified tools,
their copied schemas, selected targets and the canonical procedure reference.

Preparation refuses missing/denied capabilities, targets outside the declared
scope, mismatched names, missing target schemas and non-read-only annotations.
Annotations and host declarations do not prove authorization: the authenticated
backend must still enforce Policy, RBAC and audit on every call. Load the returned
reference progressively. This function performs no collection or file reads.

## Bind connected MCP sessions explicitly

```python
from vmware_debug.ops.scenario_context import prepare_context
from vmware_debug.ops.scenario_reader import ScenarioReader

context = prepare_context(profile, manifests, allowed, targets, allowed_targets)
reader = ScenarioReader(
    context,
    bindings={"vm_identity": ("vmware-monitor", "get_vm_info")},
    clients={"vmware-monitor": connected_monitor_session},
    max_calls=8,
)
result = await reader.read(
    "vm_identity", {"target": targets["vmware-monitor"], "vm_name": exact_vm_name}
)
metadata = reader.session.snapshot()
```

The host owns session authentication, TLS, lifecycle and access to the returned
payload. Clients use the MCP `ClientSession.call_tool` interface; connect only
through the existing guarded/audited server path. No direct REST fallback,
credential discovery or guessed official tool names are supplied. An operation
binds to exactly one prepared backend/tool. Unknown operations stop. Target and
live JSON Schema checks precede dispatch; unknown arguments are refused and
remote schema references are prohibited. MCP errors, malformed/empty results and
transport failures return an explicit gap. Cancellation records an unknown
attempt and propagates; none of these paths retries or refunds a call.

`observed` means a nonempty, structurally valid MCP response was received. It does
not establish a healthy system, complete pagination, fresh data or a cause. The
host must validate domain errors, paging, units, source time/window and identity
before submitting evidence through the normal case tools. `same_typed_identity`
accepts only `instance_uuid`, `bios_uuid` and `aria_resource_uuid`, requiring the
same explicit type and value; a BIOS UUID and an instance
UUID are not interchangeable. External content is untrusted data. Keep raw
payloads in controlled evidence storage and sanitize summaries before model use.

## One in-process task budget

Reuse one `ScenarioReader` across bindings for different skills. Its
`ScenarioSession` counts each accepted attempt before argument validation and
dispatch, including rejected arguments, errors and cancellations. Calls outside
the selected bindings never dispatch. A depleted budget stops collection and
requires an incomplete-coverage report. Step IDs share a trace ID; metadata holds
backend/tool/state and optional actual token usage, never raw arguments/results.
Unmeasured tokens remain `None`. Backend audit remains authoritative.

The counter is thread-safe within one trusted host process. Recreating a reader,
restarting a process or using another host creates another budget. This is not a
durable distributed cap, caller identity, independent human approval or a token
spend guarantee. Trace IDs are correlation hints and are not automatically added
to a backend's audit rows. No write capability or confirmation behavior changes.

## Acceptance boundary

In-memory MCP tests cover dispatch, cross-backend accounting and failure controls;
they do not validate an official service. Existing real lab reads/report checks
are separate from synthetic fault replay and native model acceptance. Only
controlled native comparisons using the same cases/model/limits can support
context/token savings; schema size alone is not a measured token reduction.

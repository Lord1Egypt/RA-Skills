# vmware-privateai — Capabilities

20 MCP tools (19 read / 1 write) over the vSphere 9.x / VCF 9.1 Web Services API (pyVmomi) plus the
Private AI Service (PAIS) REST API, with two tools that need no connection at all (sizing / bundle).
Every vSphere tool accepts an optional `target`; PAIS tools use the `pais:` config section instead.
Typical response tokens are estimates for a small estate; inventory list tools paginate at `limit=50`
and return the `{items, returned, limit, offset, total, truncated, hint}` envelope.
The MCP gallery uses PAIS server-side cursors and reports `next_after` instead of `offset`.

## GPU inventory (4 read)
| Tool | R/W | Returns | ~tokens |
|------|:---:|---------|:------:|
| `list_gpu_hosts` | R | host, gpu_count, vendors[], vgpu_vms (filter name/vendor) | 60–400 |
| `get_gpu_host` | R | one host's GPUs: device, type, vendor, memory_mb, pci_id, vm_count | 80–400 |
| `list_gpu_devices` | R | flattened physical GPUs: host, device, type, vendor, pci_id, memory_mb, vm_count (filter host/vendor) | 80–600 |
| `list_gpu_consumers` | R | vm, profile — the "who holds a vGPU" view (filter profile/vm) | 60–500 |

## GPU utilization (1 read)
| Tool | R/W | Returns | ~tokens |
|------|:---:|---------|:------:|
| `get_gpu_utilization` | R | vm, profile, gpu_pct, mem_pct, mem_used_kb, temp_c, metrics_available, idle; busiest first, `top` keeps N | 80–500 |

Real-time 20s samples via the vSphere PerformanceManager `gpu.*` counters (require the NVIDIA host GPU
driver). A negative sample is vSphere's "no data" sentinel and is dropped; a VM with no samples reports
`metrics_available:false`. **Beta caveat**: the `gpu.*` counters may report at host level on some
builds — verify the entity type on real hardware. Deep per-SM / per-process / MIG-slice telemetry is
**not** in vSphere (needs NVIDIA DCGM) and no endpoint is invented for it.

## GPU readiness (1 read)
| Tool | R/W | Returns | ~tokens |
|------|:---:|---------|:------:|
| `check_gpu_host_readiness` | R | host, vgpu_ready, gpu_count, vendors[], total_gpu_memory_mb, default_graphics_type, vgpu_profiles_offered, active_vgpu_vms, blocking_reasons[], driver_note (filter/scope host) | 100–600 |

Combines `config.graphicsInfo` + `config.graphicsConfig` + the per-host `QueryConfigTarget` profile
catalog into a `vgpu_ready` verdict (GPU present + `sharedDirect` mode + ≥1 profile offered). Only
GPU hosts are returned; a per-host query failure lands in `unreachable_hosts`. The NVIDIA driver /
MFT VIB version and MIG geometry are **not** in the vSphere API — every item carries a `driver_note`
routing to `nvidia-smi` / `esxcli` (spec NO_API; no endpoint invented).

## Profile catalog (2 read)
| Tool | R/W | Returns | ~tokens |
|------|:---:|---------|:------:|
| `list_vgpu_profiles` | R | profile, name, framebuffer_gib, profile_class, sharing, vendor_id, hosts[], host_count, unreachable_hosts[] (filter/scope host, filter model) | 80–600 |
| `list_directpath_profiles` | R | id, name, vendor, description — vCenter-level DirectPath profiles, **vSphere 9.0+** (filter name/vendor) | 60–400 |

`list_vgpu_profiles` polls `EnvironmentBrowser.QueryConfigTarget` **per host** — scope with `host` to
avoid polling the whole estate. A host whose per-host query fails lands in `unreachable_hosts` (a
reachability problem, not "no profiles"). `list_directpath_profiles` on a pre-9.0 vCenter raises a
teaching error routing to `list_vgpu_profiles` rather than returning an empty list.

## Profile validation (1 read)
| Tool | R/W | Returns | ~tokens |
|------|:---:|---------|:------:|
| `validate_vgpu_profile` | R | vm, host, current_profile, target_profile, power_state, host_offers_target, target_framebuffer_gib, can_apply, blocking_reasons[] | 80–300 |

Read-only pre-flight for `assign_vgpu`: checks the two ReconfigVM failure modes up front — VM powered
on, or the VM's own host does not offer the target profile. No reconfigure; run `assign_vgpu` once
`can_apply` is true.

## Private AI Service (6 read)
| Tool | R/W | Returns | ~tokens |
|------|:---:|---------|:------:|
| `list_pais_models` | R | id, owned_by, created — OpenAI-compatible served `/models` (filter name) | 60–400 |
| `get_pais_model_catalog` | R | id, name, status, source — deployable/approved model catalog (filter name) | 60–500 |
| `list_pais_knowledge_bases` | R | id, name, status, description — RAG knowledge bases (filter name) | 80–500 |
| `list_pais_data_sources` | R | id, name, type, status — RAG ingest connectors (filter name) | 60–400 |
| `list_pais_mcp_servers` | R | registered server ID/name, transport, availability; PAIS cursor pagination | 60–400 |
| `list_pais_mcp_tools` | R | tool/server ID/name, approval, availability, linked agent count; no raw schema | 80–500 |

PAIS reads go through the bearer-authenticated REST client (`VMWARE_PRIVATEAI_PAIS_TOKEN`). Responses
are parsed defensively: a bare JSON array or a `{data|items|models|knowledge_bases|…: [...]}` envelope is
accepted, and every field degrades via `.get()`. **Beta caveat**: the exact `/api/v1` path prefix and
the JSON field names are `INFERRED_EXACT` (corroborated by the rendered Broadcom developer portal, not a
downloaded OpenAPI or a live deployment) — a 404 usually means a base-URL mismatch, not a bug.
`get_pais_model_catalog` (`/api/v1/control/models`) is the least-confirmed of these (a best-guess path).
The MCP gallery routes are documented in the current PAIS API, but have not
been checked on a live appliance. Their `next_after` cursor and `truncated`
flag report server-side pagination; `total` stays null because this tool does
not request an expensive total count. A malformed response is `unmeasured`,
not an empty gallery. Gallery approval never bypasses backend Policy or RBAC.

## PAIS monitoring (1 read)
| Tool | R/W | Returns | ~tokens |
|------|:---:|---------|:------:|
| `get_pais_monitoring_summary` | R | vgpu_vms, reporting_vms, idle_vms, hot_vms, gpu_pct avg/max, mem_pct avg/max, temp_c_max, by_profile{}, busiest[], scope_note | 150–500 |

A fleet rollup of the same VERIFIED `gpu.*` perf counters `get_gpu_utilization` reads — the numbers you
would pin to a VCF Ops dashboard. Uses the vCenter connection (not PAIS REST). Deep per-SM / MIG /
power telemetry needs NVIDIA DCGM and is out of scope (`scope_note` says so).

## Sizing & air-gap (2 read — no connection)
| Tool | R/W | Returns | ~tokens |
|------|:---:|---------|:------:|
| `advise_pais_sizing` | R | model_billions, precision, weights_gib, serving_vram_gib, gpu_options[], storage{}, assumptions{} | 200–400 |
| `verify_pais_bundle` | R | manifest, image_count, images[], registries_to_mirror[], public_registries[], mutable_images[], warnings[] | 150–800 |

Both are pure/local — **no vCenter or PAIS call**. `advise_pais_sizing` is a transparent first-
principles heuristic (weights = params × bytes/precision; GPU count = ceil(serving / usable HBM)) and is
explicit that LLM inference is compute/HBM-bound, so random IOPS is the wrong axis for the weights.
`verify_pais_bundle` parses a **local** pais.yml with a real YAML parser (踩坑 #38) and flags the two
air-gap blockers (public registries to mirror, mutable tags); it never contacts a registry.

## Access self-check (1 read)
| Tool | R/W | Returns | ~tokens |
|------|:---:|---------|:------:|
| `get_access_info` | R | target, account, privilege states; for one `tool` its requires / verdict / meaning, else every tool grouped by verdict | 150–500 |

Asks vCenter/ESXi about the current session (`AuthorizationManager.HasPrivilegeOnEntities`, System.View
only, so any account can ask about itself). Checked on the **root folder**: `not_granted_at_root` is not
"no access" — the privilege may be granted on a cluster, host or VM. `undetermined` is never read as
granted. The per-tool table is `vmware_privateai/access_requirements.py`, derived from pyVmomi's metadata.
Two limits: the PAIS tools use a bearer token, not vSphere, so they show as needing no vSphere privilege
(the token's scope is not checked); and `assign_vgpu` also needs VirtualMachine.Config.AddRemoveDevice
and VirtualMachine.Config.Resource, which vCenter checks inside the reconfigure call (not yet verified against a
live vCenter's privilege list). CLI: `vmware-privateai access-info [--tool T] [--target T]`.

## vGPU assignment (1 write)
| Tool | R/W | Risk | Blast radius |
|------|:---:|:----:|--------------|
| `assign_vgpu` | W | high | one VM, **only when powered off** — sets/replaces its vGPU profile via ReconfigVM |

`confirm=false` (default) returns `{"action": "preview", "blast_radius": {...}, "hint": ...}` and changes
nothing. `blast_radius`: `vm`, `vm_id`, `same_name_vm_ids`, `power_state`, `current_profile`,
`target_profile`, `device_change` (`edit`/`add`), `other_passthrough_devices`,
`memory_reservation_locked_to_max`, `requires_power_off`, `blockers`, `unmeasured`; the acting response
(`action: "applied"`) carries it too. The older top-level keys (`current_profile`, `target_profile`,
`power_state`, `requires_power_off`) are still returned and are removed in the next minor release.
`confirm=true` refuses a powered-on or suspended VM, a name shared by several VMs, and an unreadable power
state or device list. It edits the
VM's **existing vGPU device** (selected by the same predicate the preview uses, never a plain
DirectPath/SR-IOV passthrough), waits for the real ReconfigVM task outcome (never a premature "ok"), and
audits the result. It never powers the VM off itself — that is `vmware-aiops`.

## Verified API surface (anti-phantom-endpoint gate)

Every runtime path is pinned in `tests/eval/spec/privateai_endpoints.py` and asserted by a regression
gate (踩坑 #36):

- **pyVmomi**: `HostSystem.config.graphicsInfo` (VERIFIED), `HostSystem.config.graphicsConfig`
  (VERIFIED — vGPU mode via `hostDefaultGraphicsType`), `EnvironmentBrowser.QueryConfigTarget →
  ConfigTarget.vgpuProfileInfo[]` (VERIFIED — the attribute is `vgpuProfileInfo`, not the spec-doc's
  phantom `vgpu[]`), `content.directPathProfileManager.ListDirectPathProfiles` (VERIFIED, 9.0+),
  `VirtualMachine.config.hardware.device → VirtualPCIPassthrough.backing.vgpu` (VERIFIED),
  `VirtualMachine.runtime.powerState` (VERIFIED), `VirtualMachine.runtime.host` (VERIFIED),
  `ReconfigVM_Task` (VERIFIED, requires VM off).
- **Perf counters**: `gpu.utilization.average`, `gpu.mem.used.average`, `gpu.mem.usage.average`,
  `gpu.temperature.average` (VERIFIED).
- **PAIS REST**: `/api/v1/compatibility/openai/v1/models`, `/api/v1/control/knowledge-bases`,
  `/api/v1/control/data-sources`, `/api/v1/control/models` (INFERRED_EXACT — path prefix deferred to
  first live run; `/control/models` is a best-guess pending a live OpenAPI).
- **NO_API** (code must not invent an endpoint): MIG mode set, GPU driver version, deep GPU telemetry
  (DCGM), one-call DL-VM deploy, pgvector.

## Maintenance safety boundary

PAIS gallery cursors are opaque: repeated, overlong or unsafe cursors produce partial coverage without a next cursor. Do not alter a cursor or infer a complete/empty registry from a partial result.

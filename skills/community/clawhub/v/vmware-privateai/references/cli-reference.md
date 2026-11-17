# vmware-privateai — CLI Reference

Full command list for the `vmware-privateai` Typer CLI. Every read command prints a teaching error and
exits 1 (never a traceback) on a config / not-found / connection problem. Every command accepts
`--target <name>` (a vCenter/ESXi target from `config.yaml`; omit for the default) and `--config <path>`
(override the `~/.vmware-privateai/config.yaml` location). Reads paginate at 50 rows; use the filter
options rather than paging the whole estate.

## Top level

```bash
vmware-privateai version          # print the installed version
vmware-privateai mcp              # run the stdio MCP server (used by MCP clients)
vmware-privateai --help           # list command groups: gpu, vgpu, pais
vmware-privateai access-info [--tool assign_vgpu] [--target T] [--config PATH]
                                  # account in use + each tool's vSphere privileges (root folder)
```

`access-info` prints the same JSON as the `get_access_info` MCP tool. `not_granted_at_root` may still be
granted on a cluster, host or VM; `undetermined` is never read as granted.

> The `mcp` subcommand is the recommended MCP entry point — it is an installed console script, so it
> never re-resolves from PyPI the way `uvx` does (踩坑 #25: `uvx` is fragile behind an enterprise TLS
> proxy). MCP clients should launch `vmware-privateai mcp`.

## `gpu` — GPU inventory, utilization, and vGPU assignment

```bash
vmware-privateai gpu host-list [--name N] [--vendor V] [--target T] [--config PATH]
```
List ESXi hosts that have at least one GPU. Columns: host, gpu_count, vendors, vgpu_vms. `--name`
substring-matches the host name; `--vendor` substring-matches the GPU vendor (e.g. `NVIDIA`).

```bash
vmware-privateai gpu host-get <host_name> [--target T] [--config PATH]
```
Full per-GPU detail for one host: device, graphics type, vendor, memory (MB), pci id, vm_count. A wrong
host name prints a teaching error listing the hosts that do have GPUs.

```bash
vmware-privateai gpu device-list [--host H] [--vendor V] [--target T] [--config PATH]
```
Flattened list of physical GPU devices across hosts. Columns: host, device, type, vendor, memory (MB),
vm_count. `vm_count 0` marks an idle GPU.

```bash
vmware-privateai gpu consumer-list [--profile P] [--vm V] [--target T] [--config PATH]
```
List VMs consuming a vGPU and the profile each holds (e.g. `grid_a100-4c`). `--profile` / `--vm`
substring-filter.

```bash
vmware-privateai gpu utilization [--vm V] [--top N] [--target T] [--config PATH]
```
Real-time (20s sample) GPU utilization per vGPU VM, busiest first: gpu %, mem %, temp (C). `--top N`
keeps only the N busiest. A VM with no host-driver samples prints `metrics unavailable` (not an error).

```bash
vmware-privateai gpu vgpu-assign <vm_name> <profile> [--dry-run] [--target T] [--config PATH]
```
**WRITE.** Set a VM's vGPU profile. Always prints the preview (current → target profile, power state,
requires_power_off) first. `--dry-run` stops there. Otherwise requires **double confirmation**, then
applies via ReconfigVM and audits the result. The VM must be powered **off** — a running or suspended VM
is refused with a teaching error routing you to vmware-aiops `power_off_vm` (CLI `vmware-aiops vm power-off`), and so is a name shared by
several VMs or a VM whose power state or devices could not be read. This command never powers the VM off
itself.

```bash
vmware-privateai gpu readiness [--host H] [--target T] [--config PATH]
```
Per-host vGPU/PAIS readiness verdict. Columns: host, ready/not-ready, gpu_count, graphics mode,
profiles offered, plus `blocking_reasons` for any host that is not ready. Only hosts that have a GPU
are shown. The NVIDIA driver / MFT VIB version and MIG are **not** in the vSphere API — verify with
`nvidia-smi` / `esxcli software vib list` on the host.

## `vgpu` — profile catalog

```bash
vmware-privateai vgpu profile-list [--host H] [--model M] [--target T] [--config PATH]
```
The vGPU profile catalog aggregated across hosts. Columns: profile, framebuffer (GiB), class, sharing,
host_count. `--host` both filters and scopes the per-host `QueryConfigTarget` polling to one host;
`--model` substring-matches the profile/model name. Hosts whose per-host query fails are reported in
`unreachable_hosts` rather than sinking the whole catalog.

```bash
vmware-privateai vgpu directpath-list [--name N] [--vendor V] [--target T] [--config PATH]
```
vCenter-level DirectPath (dynamic passthrough) profiles. **vSphere 9.0+** — on an older vCenter this
prints a teaching error routing you to `vgpu profile-list`. Columns: name, id, vendor, description.

```bash
vmware-privateai vgpu validate <vm_name> <target_profile> [--target T] [--config PATH]
```
Read-only pre-flight for a vGPU profile change (the pre-flight for `gpu vgpu-assign`). Checks the two
ReconfigVM failure modes up front — VM powered on, and whether the VM's own host offers the target
profile — and prints `can apply` / `blocked` with the reasons. No reconfigure.

## `pais` — Private AI Service (REST), monitoring, sizing, and air-gap

These talk to the PAIS REST endpoint (`config.yaml` `pais:` section) with the bearer token in
`VMWARE_PRIVATEAI_PAIS_TOKEN` — separate from the vCenter connection, so they take `--config` but not
`--target`.

```bash
vmware-privateai pais model-list [--name N] [--config PATH]
```
List models served by PAIS (OpenAI-compatible `/models`). Columns: id, owned_by. `--name`
substring-matches the model id.

```bash
vmware-privateai pais kb-list [--name N] [--config PATH]
```
List PAIS knowledge bases (RAG vector stores). Columns: name/id, status, description.

```bash
vmware-privateai pais model-catalog [--name N] [--config PATH]
vmware-privateai pais data-source-list [--name N] [--config PATH]
```
`model-catalog` lists models available/approved to **deploy** (distinct from the served `/models`);
`data-source-list` lists RAG ingest connectors. Both hit **INFERRED** PAIS control-plane paths — a 404
prints a base-URL teaching message, not a bug.

```bash
vmware-privateai pais monitoring-summary [--hot-pct P] [--top N] [--target T] [--config PATH]
```
Fleet GPU rollup (vgpu_vms, reporting/hot/idle, gpu%/mem% avg+max, busiest). Uses the **vCenter**
connection (takes `--target`), not PAIS REST. Deep per-SM/MIG telemetry needs NVIDIA DCGM (out of scope).

```bash
vmware-privateai pais sizing [--model llama-70b | --billions 70] [--precision fp16]
```
Estimate GPU memory / GPU count / storage to serve an LLM. **No connection** — a pure planning
heuristic. Honest that random IOPS is the wrong axis for the model weights.

```bash
vmware-privateai pais bundle-verify <pais.yml>
```
Parse a **local** pais.yml and list container images + registries to mirror for an air-gap, flagging
public registries and mutable tags. **No network** — does not contact any registry.

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Teaching error (config missing, target/host/VM not found, connection/TLS failure, PAIS 4xx) |

## Environment variables

| Variable | Purpose |
|----------|---------|
| `VMWARE_PRIVATEAI_<TARGET>_PASSWORD` | Password for a vCenter/ESXi target (`<TARGET>` = target name upper-cased, `-`→`_`) |
| `VMWARE_PRIVATEAI_<TARGET>_USERNAME` | Optional username override (wins over `config.yaml`) |
| `VMWARE_PRIVATEAI_PAIS_TOKEN` | OIDC/OAuth2 bearer token for the PAIS REST endpoint |
| `VMWARE_PRIVATEAI_CONFIG` | Optional path to `config.yaml` (primary env for the skill) |

Secret-bearing `*_PASSWORD` / `*_TOKEN` values are auto-obfuscated to `b64:` form in `.env` on load
(grep-safe; obfuscation, not encryption).

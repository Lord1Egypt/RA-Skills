# Nexus accounts, quotas and access control

Everything here is the *account* layer around a Nexus job: who you are, what you're
allowed to spend, and who can see the result. Sources: the Nexus admin guide
(`docs.quantinuum.com/nexus/admin_guide/`), the user-guide concept pages on
organizing/access control/quotas, and live `qnexus` 0.48.2 introspection against a
real account.

Read this **before** a hackathon or a shared-account run. Most "why did my job not
run" answers live here rather than in the circuit.

## The three containers — organization / group / team

They are not synonyms and they do different jobs.

| Container | Purpose | Spans orgs? | Who manages |
| --- | --- | --- | --- |
| **Organization** | top-level; every user accesses Nexus through one. Quotas and software plans attach here. | no | Quantinuum + org admins |
| **Group** | shares a **quota** among users. A user can be in several; one is their *default group*. | no | org admin |
| **Team** | shares **resources** (projects, circuits, jobs) for collaboration. | yes | any user (`qnx.teams.create`) |

Group is billing/allowance. Team is collaboration. Picking a group at submission
time is the `user_group=` parameter on `start_execute_job` / `start_compile_job`;
omitting it meters against your personal allowance. Nexus Lab (Jupyter) time always
meters against your **default group**, which you set in Settings → Organization.

```python
qnx.teams.create(name="nadarasa", description="hackathon collaborators")
qnx.teams.get_all().df()
```

There is no documented API for adding/removing team *members* or creating groups —
teams get members through role assignment on resources, groups are admin-UI only.

## Roles: four names, most-permissive wins

`Literal['Administrator', 'Contributor', 'Reader', 'Maintainer']` — verified from
`qnx.roles.RoleName`.

| Role | Can |
| --- | --- |
| Reader | view project, jobs, circuits. No edits. |
| Contributor | + run jobs, change project properties, edit resources |
| Maintainer | + delete resources, archive and delete the project |
| Administrator | + add/remove users and teams, change their roles |

```python
qnx.roles.assign_user(resource_ref=project, user_email="a@b.net", role="Contributor")
qnx.roles.assign_team(resource_ref=project, team=team_ref, role="Reader")
qnx.roles.assignments(resource_ref=project).df()   # who currently has what
```

Rules that bite:

- A user holding both a personal role and a team role on the same resource gets the
  **most permissive** of the two. Narrowing someone's personal role does nothing if
  their team still holds Contributor.
- Deleting a project deletes it **for everyone**. Hand out Maintainer sparingly on a
  shared hackathon project.
- Contributing to someone else's project still consumes **your own** database quota.
- Leaving a team revokes every access that came through it, immediately.
- These roles govern API access exactly as they govern the web UI.

Resource-level `Administrator` is *not* the same thing as **Organization Admin** —
the latter is a separate all-or-nothing checkbox on the user, granted from the org
Users tab, and requires the user to re-login before it takes effect.

## Quotas: four meters, none of them HQCs

`qnx.quotas.QuotaName` is exactly `['compilation', 'simulation', 'jupyterhub',
'database_usage']`.

| Quota | Meters | Unit | Resets |
| --- | --- | --- | --- |
| `compilation` | CPU time compiling circuits | seconds | monthly |
| `simulation` | CPU time on **Nexus-hosted** simulators | seconds | monthly |
| `jupyterhub` | Nexus Lab notebook server uptime | seconds | monthly |
| `database_usage` | stored programs, results, backend snapshots | MB | **never** |

The critical omission: **there is no Nexus quota for running on Quantinuum hardware
or external providers.** HQC allowance is enforced by the provider, not by these
meters, so `check_quota` passing tells you nothing about whether you can afford an
H-series job. Guard hardware spend with `max_cost=` (see `nexus-jobs.md`), not with
quotas.

```python
qnx.quotas.get_all().df()          # name / description / usage / quota
qnx.quotas.check_quota("simulation")   # bool, current user only
qnx.quotas.get("database_usage").usage
```

`quota` reads the literal string `'No quota set for user'` when unlimited — it is
**not** always a float, so never do arithmetic on it without a type check. On a
plain account these calls also emit a deprecation warning about the
`/api/quotas/v1beta` endpoint; it is noise, the call works.

Quota administration itself is UI-only (org page → Users → ⋮ → *Manage quotas*).
There is no admin-scoped bulk quota API — the `qnx.quotas.*` calls are self-scoped.

## Priority

Integer **1 (highest) → 10 (lowest)**, default **5** on invite. It only affects jobs
submitted to Quantinuum hardware and emulators, and only an org admin can change it.
If a hardware job sits queued far longer than a colleague's, compare priorities
before blaming the device.

## Usage reporting

- Any user: profile → *My Usage Reports* → Create Report (name, expiration, date
  range). Reports expire and then cannot be downloaded — re-create rather than hunt.
- Org admin: management page → *Access* tab for CPU/storage utilisation graphs
  filterable by user, and *Quantinuum Systems Reports* tab for hardware/emulator
  usage across the org.

Reports show compute and usage metrics, not monetary cost. Nothing in Nexus shows a
dollar figure.

## Self-serve vs "ask an admin"

Self-serve: create projects and teams, assign roles on resources you administer,
check your own quota, generate your own usage report, set your default group, edit
display name and username (3–53 chars, alphanumeric, unique).

Needs an org admin: inviting users, granting Organization Admin, resetting another
user's password, raising a quota, changing priority, org-wide job cancel/retry,
org-wide usage reports. Software Plans need **Quantinuum** to enable them
(`QCsupport@quantinuum.com`), not just an org admin.

## Before you burn HQCs — checklist

1. `qnx.auth.is_logged_in()` and `qnx.users.get_self()` — right account?
2. `qnx.devices.get_all().df()` — is the target actually listed for this account?
3. `qnx.quotas.get_all().df()` — `database_usage` never resets; a long sweep that
   stores every result can wedge you out of storage mid-run.
4. Decide the **group**: pass `user_group=` if the allowance is not personal.
5. Set `max_cost=` on the execute job. This is the only hard *server-side* spend
   guard — and it is **per job**, so it does nothing about a thirty-cell sweep
   firing thirty of them. Carry a client-side batch ledger too: book the
   estimate at submit time, refuse the next cell when the projected total
   passes `NADARASA_MAX_TOTAL_HQC`, and report billed totals from
   `qnx.jobs.cost` alongside (never instead of) the estimates.
6. `qnx.devices.supports_shots(config)` before submitting anything shot-based:
   a distribution-only backend accepts the job and then hands back results the
   shot decoder cannot read — the refusal belongs *before* the spend.
7. Run the compile job first and read `qnx.jobs.cost(compile_job)` before executing.
   `qnx.circuits.cost(...)` gives a truer pre-submission figure but is itself a
   billable costing job, so keep it opt-in (`NADARASA_COST_PROBE=1`), not a
   default on every cell.
8. Confirm your priority if the queue matters.
9. Record job id, backend, shots, seed and date — see
   `references/cross-platform-validation.md` for the reporting contract.


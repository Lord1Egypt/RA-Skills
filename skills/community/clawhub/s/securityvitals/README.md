# ClawVitals Skill

Security health check for self-hosted [OpenClaw](https://openclaw.ai) installations. Instruction-only skill — stateless, no storage, no network.

## Install

```bash
npx clawhub install clawvitals
```

Then in your OpenClaw messaging surface:
```
run clawvitals
```

## Commands

- `run clawvitals` — point-in-time security scan
- `show clawvitals details` — full report with remediation

## Links

- [clawvitals.io](https://clawvitals.io)
- [Docs](https://clawvitals.io/docs)
- [Controls](https://clawvitals.io/docs/controls)

---

## Publishing to ClawHub

This repo publishes to **two** ClawHub listings from the **same `skill/` directory**. The slug and display name are passed as flags at publish time — do not create separate directories.

**Always publish both together.** Never publish one without the other.

### Step-by-step

1. Update `skill/SKILL.md` and `skill/skill.json` (bump `version` in skill.json)
2. Update `skill/CHANGELOG.md`
3. Commit and push to `ANGUARDA/clawvitals`
4. Publish ClawVitals:

```bash
npx clawhub publish skill/ \
  --slug clawvitals \
  --name "ClawVitals" \
  --version <version> \
  --changelog "<changelog text>"
```

5. Publish SecurityVitals (same files, different slug and name):

```bash
npx clawhub publish skill/ \
  --slug securityvitals \
  --name "SecurityVitals" \
  --version <version> \
  --changelog "<changelog text>"
```

### Key rules

| Rule | Detail |
|---|---|
| **One directory** | `skill/` only — no `skill-securityvitals/` or variant directories |
| **`--name` is required** | Without it, ClawHub prepends "Skill" to the `displayName` field and shows "Skill ClawVitals" |
| **`--slug` controls the listing** | `clawvitals` → clawhub.ai/bk-cm/clawvitals · `securityvitals` → clawhub.ai/bk-cm/securityvitals |
| **Version must be new** | ClawHub rejects duplicate versions — bump `skill.json` before every publish |
| **Both listings must stay in sync** | Content is identical — publish both at the same version in every release |
| **Never publish without BK approval** | ClawHub scans run automatically; wait for green before promoting |

### Current versions

| Listing | Slug | Version | URL |
|---|---|---|---|
| ClawVitals | `clawvitals` | 1.4.4 | [clawhub.ai/bk-cm/clawvitals](https://clawhub.ai/bk-cm/clawvitals) |
| SecurityVitals | `securityvitals` | 1.4.5 | [clawhub.ai/bk-cm/securityvitals](https://clawhub.ai/bk-cm/securityvitals) |

> SecurityVitals is one patch ahead (1.4.5 vs 1.4.4) due to a version collision during a republish. Align on the next release.

## License

MIT

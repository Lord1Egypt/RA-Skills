# Automation Integration Preflight Action

Check a public page for bounded automation and integration-readiness evidence from a GitHub Actions workflow. The Action calls the TinyOps Automation Integration Preflight API through RapidAPI and saves the structured JSON response as a workspace file.

The service inspects public HTML without executing page JavaScript, submitting forms, authenticating, bypassing access controls, or testing vulnerabilities. It rejects private-network and credential-like targets, bounds redirects and response sizes, checks robots policy, and returns evidence instead of raw page content.

## Agent skill

Install the repository as an agent skill for direct x402 access with payment-consent and public-target safeguards:

```text
npx skills add tinyopsstudio/automation-integration-preflight-action
```

The skill can request a readiness analysis for USD 0.03 or an acceptance evidence pack for USD 0.10 on Base. It verifies the live payment requirements before any authorized purchase.

## Quick start

1. Subscribe to the [Automation Integration Preflight API](https://rapidapi.com/tinyopsstudio/api/automation-integration-preflight). The Basic plan includes 10 requests per month.
2. Add the RapidAPI application key to your repository as a secret named `RAPIDAPI_KEY`.
3. Add this step to a workflow:

```yaml
- name: Check automation readiness
  id: preflight
  uses: tinyopsstudio/automation-integration-preflight-action@v1
  with:
    url: https://example.com/public-form
    rapidapi-key: ${{ secrets.RAPIDAPI_KEY }}
```

The default report file is `automation-preflight-report.json`. You can upload it with `actions/upload-artifact` or consume the `readiness`, `report-file`, and `http-status` outputs in later steps.

## Command-line use

The same bounded check is available as a Node 24 command-line tool:

```text
npx --yes github:tinyopsstudio/automation-integration-preflight-action \
  --url https://example.com/public-form \
  --output reports/automation-preflight.json
```

Set `RAPIDAPI_KEY` in the environment before running the command. Add `--mode acceptance-pack` and `--objective "Your implementation objective"` when you want launch gates and acceptance tests in the response. The key is sent only to the RapidAPI gateway and is never written to the JSON report. The command installs directly from the public TinyOps GitHub repository.

## Private deployment

Need the API inside your own Cloudflare account? The [Automation Preflight API Source License](https://tinyopsstudio.com/automation-preflight-api-source-license) is a $2,500 one-time, non-exclusive commercial license. It includes the tested Worker source, OpenAPI contracts, optional x402 adapter, deployment guide, configuration examples, release manifest, integrity hashes, and 30 days of asynchronous written setup support.

## Implementation help

Found readiness gaps and want a written implementation plan? The [AI Workflow Automation Audit](https://tinyopsstudio.gumroad.com/l/workflow-audit?wanted=true&utm_source=github&utm_medium=action-readme&utm_campaign=automation-preflight) maps one workflow, identifies failure, duplicate, and handoff risks, and returns a fixed-price next step for $99. Delivery is asynchronous with a two-business-day target.

## Acceptance-pack mode

Use `acceptance-pack` when you want the evidence plus launch gates, acceptance tests, and a prioritized remediation backlog:

```yaml
- name: Build automation acceptance pack
  uses: tinyopsstudio/automation-integration-preflight-action@v1
  with:
    url: https://example.com/public-form
    rapidapi-key: ${{ secrets.RAPIDAPI_KEY }}
    mode: acceptance-pack
    objective: Route valid inquiries into the CRM with a review fallback.
    output-file: reports/automation-acceptance-pack.json
```

## Inputs

| Input | Required | Default | Description |
| --- | --- | --- | --- |
| `url` | Yes | | Public HTTP or HTTPS page to inspect. |
| `rapidapi-key` | Yes | | RapidAPI application key stored as a GitHub Actions secret. |
| `mode` | No | `analyze` | `analyze` or `acceptance-pack`. |
| `objective` | No | | Optional objective, up to 500 characters. |
| `output-file` | No | `automation-preflight-report.json` | Report path inside the GitHub workspace. |
| `fail-on-error` | No | `true` | Set to `false` to preserve a successful workflow step when the API request fails. |

## Security

Pass the RapidAPI key through GitHub Actions secrets. The Action masks the key before making a request, never writes it to the report, and does not send it anywhere except the RapidAPI gateway. Target URLs must be public HTTP or HTTPS pages, and output paths cannot escape the GitHub workspace.

## Development

```text
npm test
```

The test suite uses a local mock server and does not consume API requests.

## License

The Action client is available under the MIT License. The hosted API is governed by the plan and terms shown on RapidAPI.

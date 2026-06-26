---
name: sap-bah-openapi-backend
description: Reliable SAP Business Accelerator Hub API spec downloader for OpenClaw. Uses SAP_HUB_USERNAME and SAP_HUB_PASSWORD to log in through Playwright Chromium, downloads OpenAPI JSON/YAML and OData EDMX to /usr/download, validates payload signatures, and supports importing specs into APIConnectionToSAP categories.
metadata: {"openclaw":{"version":"1.1.0","requires":{"env":["SAP_HUB_USERNAME","SAP_HUB_PASSWORD"]},"os":["linux","darwin"],"default_output_dir":"/usr/download","browser":"chromium","entrypoint":"scripts/reliable_sap_hub_download.py"}}
---

# SAP BAH OpenAPI Backend (OpenClaw Upload Package)

## Purpose

Use this skill to reliably download SAP API specification files from `hub.sap.com`.

Authentication:

- `SAP_HUB_USERNAME`
- `SAP_HUB_PASSWORD`

Downloaded files are written to:

- `/usr/download/<API_ID>_openapi.json`
- `/usr/download/<API_ID>_openapi.yaml`
- `/usr/download/<API_ID>_odata.edmx`

## Prerequisites

1. Chromium available through Playwright.
2. Python 3.10+.
3. Python Playwright installed:

```bash
python3 -m pip install playwright
python3 -m playwright install chromium
```

4. Writable output directory `/usr/download`.

If needed:

```bash
sudo mkdir -p /usr/download
sudo chown "$USER":staff /usr/download
```

5. Maintain login credentials via environment variables:

```bash
export SAP_HUB_USERNAME='your_user'
export SAP_HUB_PASSWORD='your_password'
```

Security note:

- Do not upload real credentials to ClawHub.
- Maintain credentials only in the runtime environment.

## How to start

Run from repository root:

```bash
python3 Skills/sap-bah-openapi-backend-openclaw-upload-1.0.0/scripts/reliable_sap_hub_download.py \
  --api-id WAREHOUSEORDER_0001
```

## How to use

### 1) Download one or more API IDs

```bash
python3 Skills/sap-bah-openapi-backend-openclaw-upload-1.0.0/scripts/reliable_sap_hub_download.py \
  --api-id WAREHOUSEORDER_0001 \
  --api-id API_APAR_SEPA_MANDATE_SRV
```

### 2) Download from file list

```bash
python3 Skills/sap-bah-openapi-backend-openclaw-upload-1.0.0/scripts/reliable_sap_hub_download.py \
  --api-id-file /path/to/api_ids.txt
```

`api_ids.txt` example:

```text
WAREHOUSEORDER_0001
API_APAR_SEPA_MANDATE_SRV
sap-s4-CE_EBPPPAYMENTREQUEST_0001-v1
```

### 3) Useful runtime options

```bash
python3 Skills/sap-bah-openapi-backend-openclaw-upload-1.0.0/scripts/reliable_sap_hub_download.py \
  --api-id WAREHOUSEORDER_0001 \
  --retries 4 \
  --timeout-seconds 90 \
  --json-report /usr/download/sap_download_report.json
```

### 4) Import downloaded files into project category

```bash
python3 Skills/sap-bah-openapi-backend-openclaw-upload-1.0.0/scripts/import_sap_hub_spec.py \
  --category AccountsReceivable \
  --pattern CONTRACTACCOUNT_0001 \
  --mode copy
```

## Reliability behavior

The downloader script automatically:

1. In default `env` mode, starts with a clean temporary browser profile.
2. Uses Playwright Chromium.
3. Logs in using `SAP_HUB_USERNAME` and `SAP_HUB_PASSWORD`.
4. Downloads JSON/YAML/EDMX through Hub authenticated `$value` endpoints.
5. Retries transient failures.
6. Rejects OAuth/login HTML payloads.
7. Verifies expected OpenAPI/EDMX signatures before writing files.

## Output contract

- Exit code `0`: all requested files downloaded and validated.
- Exit code `2`: partial/complete failures (see JSON report/stdout report).

## Included files

- `scripts/reliable_sap_hub_download.py`
- `scripts/import_sap_hub_spec.py`
- `scripts/scaffold_backend_from_openapi.py`
- `references/quickstart.md`

---
name: solidpod-data
description: Interact with SOLID Pods — read data, write RDF data, create containers, manage access control, and provision new SOLID Pods. Supports Inrupt ESS, CSS, and any spec-compliant SOLID server.
homepage: https://github.com/pettifordo/SOLIDPOD-DATA
metadata: {"openclaw":{"requires":{"bins":["node"],"env":["SOLID_IDP","SOLID_CLIENT_ID","SOLID_OIDC_KEY","SOLID_POD_URL","SOLID_OIDC_ISSUER"]},"primaryEnv":"SOLID_IDP","emoji":"🪣","install":"npm install --prefix {baseDir} --omit=dev"}}
---

# SolidPod-Data — SOLID Pod Skill

This skill lets you interact with [SOLID Pods](https://solidproject.org/) — personal decentralised data stores — directly from OpenClaw. It uses Inrupt's `@inrupt/solid-client` and `@inrupt/solid-client-authn-node` under the hood.

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `SOLID_IDP` | Yes | Identity Provider URL (e.g. `https://login.inrupt.com`) |
| `SOLID_CLIENT_ID` | Yes | Client ID from your SOLID app registration |
| `SOLID_OIDC_KEY` | Yes | OIDC client key from your SOLID app registration |
| `SOLID_POD_URL` | Optional | Default Pod URL to operate against |
| `SOLID_OIDC_ISSUER` | Optional | Override OIDC issuer (defaults to `SOLID_IDP`) |

## Setup

1. **Register a client app** at your Identity Provider (e.g. https://login.inrupt.com/registration.html)
2. Set the three required env vars above in your OpenClaw environment
3. Install: `npm install --prefix {baseDir} --omit=dev`

---

## Commands

### Read Operations

**Read a dataset (RDF resource)**
```
/solidpod-data read <url>
```
Fetches and displays all Things and their predicates from the dataset at `<url>`.

**Read a specific Thing**
```
/solidpod-data thing <dataset-url> <thing-url>
```
Displays all properties of a specific Thing within a dataset.

**List a container**
```
/solidpod-data list <container-url>
```
Lists all resources and sub-containers inside a SOLID container (directory).

**Read a non-RDF resource**
```
/solidpod-data resource <url>
```
Downloads and displays a non-RDF resource (text, JSON, etc.) from the pod.

---

### Write Operations

**Create a container**
```
/solidpod-data mkdir <url>
```
Creates a new container (directory) at the given URL. Creates parent containers as needed.

**Create or update a dataset**
```
/solidpod-data write <url> <predicate> <object>
```
Creates or updates an RDF dataset. Adds a triple `<thing-in-dataset> <predicate> <object>`.

**Delete a resource**
```
/solidpod-data delete <url>
```
Deletes a resource or empty container from the pod.

---

### Access Control

**View access for a resource**
```
/solidpod-data acl show <url>
```
Displays current access control rules for the resource (WAC or ACP depending on server).

**Grant access**
```
/solidpod-data acl grant <url> <webid> <modes>
```
Grants access to a WebID. `<modes>` is a comma-separated list: `read`, `write`, `append`, `control`.

Example: `/solidpod-data acl grant https://mypod.example/data/ https://alice.example/profile/card#me read,write`

**Revoke access**
```
/solidpod-data acl revoke <url> <webid>`
```
Removes all access for the given WebID on the resource.

**Request access (ACP)**
```
/solidpod-data acl request <url> <reason>
```
Sends an access request message to the resource owner (requires ACP-enabled server).

---

### Pod Management

**Show pod info**
```
/solidpod-data pod info [pod-url]
```
Shows storage root, owner WebID, and type info for a pod. Uses `SOLID_POD_URL` if URL is omitted.

**Create a new SOLID Pod**
```
/solidpod-data pod create <username> --server <css-base-url>
```
Prints step-by-step registration instructions for provisioning a new Pod on a Community Solid Server (CSS) instance, including the registration endpoint URL and required fields. The actual registration is completed by the user in their own browser or shell.

**Register a WebID**
```
/solidpod-data pod register <webid-url>
```
Registers/links a WebID profile document on the pod.

---

### Area / Topic Management

Areas are top-level containers in a pod that group related data. The skill uses a `solidpod-data:Area` type to mark them.

**List areas**
```
/solidpod-data area list [pod-url]
```
Lists all registered SolidPod-Data areas in the pod.

**Create an area**
```
/solidpod-data area create <name> [--description "text"] [--pod-url <url>]
```
Creates a new named area container in the pod and registers it in the pod's index.

**Request access to a topic/area**
```
/solidpod-data area request <area-url> [--reason "why you need access"]
```
Sends an access request for an area to its owner using SOLID notifications or access request resources.

---

## How the Skill Works

All commands run through `{baseDir}/scripts/solidpod-data.js` via Node.js.

Authentication uses the Client Credentials flow (machine-to-machine, no browser needed) via `@inrupt/solid-client-authn-node`. The authenticated session is reused across operations within a single invocation.

When you ask me to interact with a SOLID pod, I will:

1. Confirm the target Pod URL and operation with you before writing anything
2. Show you exactly what will be created/modified/deleted
3. Execute via `node {baseDir}/scripts/solidpod-data.js <command> [args]`
4. Display the result clearly

**I will always ask for confirmation before:**
- Deleting any resource
- Changing access control rules
- Creating a new Pod
- Uploading files that overwrite existing resources

---

## Security Notes

- Client credentials are passed via environment variables, never command-line args
- The skill does not store tokens to disk — each run re-authenticates
- ACL changes are shown before confirmation to prevent accidental exposure
- Private data from the pod is shown only in your local terminal session

---

## Examples

```
# List everything in your pod root
/solidpod-data list https://mypod.inrupt.net/

# Create an area called "health"
/solidpod-data area create health --description "My health data" --pod-url https://mypod.inrupt.net/

# Grant Alice read access to the health area
/solidpod-data acl grant https://mypod.inrupt.net/health/ https://alice.solidcommunity.net/profile/card#me read

# Read a dataset
/solidpod-data read https://mypod.inrupt.net/health/summary.ttl
```

---

## External Endpoints

This skill contacts **only URLs that the user explicitly provides** via environment variables or command arguments. No fixed third-party endpoints are hardcoded.

| Variable / Argument | Purpose | Who controls it |
|---|---|---|
| `SOLID_IDP` | OIDC authentication — the user's own Identity Provider | The user |
| `SOLID_POD_URL` | The user's own SOLID Pod storage root | The user |
| `<url>` arguments | SOLID Pod resources to read/write/manage | The user |

No data is sent to any endpoint not supplied by the user. No telemetry, analytics, or third-party services are contacted.

---

## Security & Privacy

**Authentication:** `SOLID_OIDC_KEY` is used exclusively for the OIDC Client Credentials grant to the user's own Identity Provider (`SOLID_IDP`). This is the standard machine-to-machine authentication pattern for SOLID applications, equivalent to any OAuth2 client credential flow. The key is read from an environment variable (the recommended practice) and passed directly to the `@inrupt/solid-client-authn-node` SDK — it is never logged, stored to disk, or sent anywhere except the user's own IDP.

**Data flow:** All network requests are authenticated SOLID protocol operations (LDP/HTTP) against the user's own Pod. No data from the Pod is forwarded to any third party.

**Local filesystem:** This skill does not read from or write to the local filesystem. All read/write operations target the user's SOLID Pod over HTTPS.

**No persistence:** No tokens, credentials, or Pod data are written to disk by this skill.

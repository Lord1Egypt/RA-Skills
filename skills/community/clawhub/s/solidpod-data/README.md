# SolidPod-Data

An [OpenClaw](https://openclaw-ai.com) skill for interacting with [SOLID Pods](https://solidproject.org/) — the decentralised personal data stores pioneered by Sir Tim Berners-Lee.

Available on [ClawHub](https://clawhub.io) as `solidpod-data`.

---

## What is SOLID?

SOLID (Social Linked Data) lets you store your data in a Pod you control. Apps and agents ask for access; you decide who sees what. Your data, your rules.

## What SolidPod-Data Does

| Capability | Commands |
|---|---|
| Read RDF datasets & Things | `read`, `thing` |
| List containers | `list` |
| Read pod resources | `resource` |
| Create containers / areas | `mkdir`, `area create` |
| Write RDF data | `write` |
| Delete resources | `delete` |
| View & manage access (WAC/ACP) | `acl show/grant/revoke` |
| Request access to topics | `acl request`, `area request` |
| Show pod info | `pod info` |
| Provision new SOLID Pods (CSS) | `pod create` |

## Installation

```bash
# In your OpenClaw skills directory:
clawhub install solidpod-data

# Or clone directly:
git clone https://github.com/pettifordo/SOLIDPOD-DATA.git
cd SOLIDPOD-DATA
npm install
```

## Setup

1. Register a client application at your SOLID Identity Provider
   (e.g. [Inrupt registration](https://login.inrupt.com/registration.html))

2. Set environment variables:

```bash
export SOLID_IDP=https://login.inrupt.com
export SOLID_CLIENT_ID=your-client-id
export SOLID_OIDC_KEY=your-oidc-key
export SOLID_POD_URL=https://storage.inrupt.com/your-pod-id/
```

3. Test it:

```bash
node scripts/solidpod-data.js pod info
```

## Usage Examples

```bash
# List your pod root
/solidpod-data list https://mypod.inrupt.net/

# Create an area called "finance"
/solidpod-data area create finance --description "Financial records"

# Grant a friend read access
/solidpod-data acl grant https://mypod.inrupt.net/finance/ https://friend.solidcommunity.net/profile/card#me read

# Request access to someone else's area
/solidpod-data area request https://alice.inrupt.net/health/ --reason "Shared care plan"

# Read a dataset
/solidpod-data read https://mypod.inrupt.net/profile/card

# Create a new pod (Community Solid Server)
/solidpod-data pod create alice --server https://my-css-instance.example
```

## Architecture

```
SolidPod-Data/
├── SKILL.md              # OpenClaw skill definition (entry point)
├── package.json          # npm dependencies
├── scripts/
│   ├── solidpod-data.js  # CLI dispatcher
│   ├── pod.js            # Core pod operations
│   ├── auth.js           # Client credentials authentication
│   └── access.js         # WAC/ACP access control
└── README.md
```

## Security

- Credentials are read from environment variables only — never passed as CLI arguments
- No tokens are written to disk — each process re-authenticates
- ACL changes are confirmed before execution when used via the OpenClaw skill
- Private pod data stays in your terminal session

## Dependencies

- [`@inrupt/solid-client`](https://github.com/inrupt/solid-client-js) — SOLID data operations
- [`@inrupt/solid-client-authn-node`](https://github.com/inrupt/solid-client-authn-js) — Client credentials auth
- [`@inrupt/vocab-common-rdf`](https://github.com/inrupt/solid-common-vocab-rdf) — RDF vocabulary constants

## License

MIT — Owen Pettiford

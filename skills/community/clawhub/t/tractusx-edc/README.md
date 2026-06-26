# Tractus-X EDC Connector Skill (v3 API)

OpenClaw skill for interacting with Tractus-X EDC (Eclipse Data Connector) control plane API using the v3 endpoints.

## Installation

```bash
npx clawhub@latest install tractusx-edc-v3
```

Or manually place the `tractusx-edc` folder in your skills directory.

## Configuration

Set these environment variables:

| Variable                | Required | Description                                                       |
| ----------------------- | -------- | ----------------------------------------------------------------- |
| `EDC_CONTROL_PLANE_URL` | Yes      | Base URL of the EDC control plane (e.g., `http://localhost:9192`) |
| `EDC_API_KEY`           | No       | API key for authentication (depends on connector config)          |

## Features (v3 API Only)

- **Assets**: Create, list, get, update, and delete data assets
- **Policy Definitions**: Query policies
- **Contract Definitions**: Create, update, and list contract definitions
- **Contract Negotiations**: Initiate and query negotiation flow
- **Contract Agreements**: View agreements and retired agreements
- **Transfer Processes**: Initiate and manage data transfers
- **EDR Management**: Access endpoint data references
- **Business Partner Groups**: Resolve and manage BPN groups
- **Health Checks**: Monitor connector health

## Note on State Polling

The v3 API does not provide dedicated state polling endpoints. To check negotiation or transfer states:

- For **negotiations**: Query using `/v3/contractnegotiations/request` and check the state field
- For **transfers**: Query and check the state in the response object

## Usage

The skill provides curl commands for all API operations. Configure the environment variables and execute the commands using Bash tool.

## Resources

- [Tractus-X EDC Documentation](https://eclipse-tractusx.github.io/tractusx-edc/)
- [API Specification](https://eclipse-tractusx.github.io/api-hub/tractusx-edc/0.12.0/control-plane/control-plane.yaml)

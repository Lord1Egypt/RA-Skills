# 🚪 S2-Gateway-Transition-Logic (S2 时空跃迁守门人)

## 🛡️ Zero-Trust Security Architecture
This plugin is built for enterprise-grade Building Automation Systems (BAS). It features:
1. **Zero Hardcoded Secrets:** Valid tokens must be injected securely via the `S2_BMS_VAULT_TOKENS` environment variable.
2. **Advisory Execution:** The agent evaluates the spatial transition but only *reports* the ACS command, leaving final physical relay execution to the isolated hardware layer.

## 🛠️ Usage for OpenClaw Agents
Invoke the **`evaluate_spatial_transit`** tool when an entity requests to cross the gateway.

**Example Tool Call:**
```json
{
  "entity_id": "Human_Miles",
  "gateway_id": "MAIN_DOOR_ACS_01",
  "direction": "inbound",
  "auth_token": "<SECRET_TOKEN_PROVIDED_BY_USER>"
}
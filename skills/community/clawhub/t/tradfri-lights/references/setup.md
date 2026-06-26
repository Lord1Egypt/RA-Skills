# TRÅDFRI setup notes

## Requirements

- An IKEA TRÅDFRI gateway on the local network
- Node.js available on the host
- `node-tradfri-client` installed in the skill folder

## Config location

The skill reads credentials from:

- `config.json`

Environment variables can override that file:

- `TRADFRI_HOST`
- `TRADFRI_IDENTITY`
- `TRADFRI_PSK`

## First-time authentication

Use a small Node script with `TradfriClient.authenticate(securityCode)` against your gateway host, then update `config.json` with the returned `identity` and `psk`.

Minimal pattern:

```js
const { TradfriClient } = require('node-tradfri-client');
const tradfri = new TradfriClient('YOUR_GATEWAY_HOST');
const result = await tradfri.authenticate(SECURITY_CODE);
console.log(result);
```

Store the returned values, then use `scripts/tradfri.js status` to confirm the skill can connect.

## Notes

- Do not publish real gateway credentials.
- For bulk actions, the script excludes `SuperGroup` and `Instellen` by default. Adjust that rule for your own environment if needed.

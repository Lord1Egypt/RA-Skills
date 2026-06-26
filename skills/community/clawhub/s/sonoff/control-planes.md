# Sonoff Control Planes

Use this matrix to choose the right control plane per task.

## Available Planes

- eWeLink cloud API:
  - Best for remote access across networks.
  - Requires valid cloud token and account-scoped permissions.

- LAN control mode:
  - Best for low-latency local operations on supported devices.
  - Requires same-LAN reachability and LAN-capable firmware/device.

- DIY mode API:
  - Local HTTP API for compatible SONOFF DIY devices.
  - Discovery often relies on `_ewelink._tcp` and local service metadata.

- iHost Open API V2:
  - Local bridge token + REST and SSE endpoints for iHost-managed systems.
  - Useful for local orchestration and event-driven workflows.

## Selection Rules

1. Prefer LAN or iHost local path for immediate local-state operations.
2. Use cloud path when remote-only control is required.
3. Never switch planes mid-run unless fallback policy is explicit.
4. If device mode support is unknown, resolve capability before command generation.

## Reliability Baseline

- Track command id and expected result for every write.
- Set timeout and retry budget per control plane.
- Log plane-specific failures separately from device logic failures.

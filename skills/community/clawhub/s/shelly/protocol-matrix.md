# Shelly Protocol and Transport Matrix

Use this guide to choose the right transport for each task.

## Shelly RPC Channels

Shelly Gen2+ RPC can run over:
- HTTP: request/response RPC calls
- WebSocket: bidirectional RPC and notifications
- MQTT: broker-based transport for commands and events

## Transport Selection

- HTTP RPC:
  - Best for deterministic read/write tasks and straightforward retries.
  - Good default for single-device orchestration.

- WebSocket RPC notifications:
  - Best for near real-time event tracking.
  - Prefer for monitoring loops and faster state convergence checks.

- MQTT transport:
  - Best when user already operates broker-based automations.
  - Use for event pipelines and system-wide integrations.

## Decision Rules

1. Start with HTTP RPC for initial validation.
2. Add WebSocket notifications for event-sensitive workflows.
3. Use MQTT only when broker reliability and topic governance are confirmed.
4. Avoid switching transport mid-run unless fallback policy is explicit.

## Minimum Reliability Baseline

- Track request id and expected result for every write.
- Define timeout and retry budget per channel.
- Log channel-level errors separately from device logic errors.

# Tuya Device Operations Workflow

Use this sequence for reliable command execution on Tuya devices.

## Core Endpoints

- Get device details: `GET /v1.0/devices/{device_id}`
- Get command schema: `GET /v1.0/iot-03/devices/{device_id}/functions`
- Get current status: `GET /v1.0/iot-03/devices/{device_id}/status`
- Send commands: `POST /v1.0/iot-03/devices/{device_id}/commands`

## Canonical Control Loop

1. Resolve target device ids.
2. Read device details and online state.
3. Read supported function codes and value constraints.
4. Read baseline status.
5. Generate validated command payload.
6. Send command.
7. Read status again and compare against expected state.
8. Record result and stop on mismatch.

## Command Payload Pattern

```json
{
  "commands": [
    {"code": "switch_1", "value": true}
  ]
}
```

For multi-property updates, send only validated `code/value` pairs from function schema.

## Validation Rules

- Boolean codes -> only true/false.
- Enum codes -> only documented enum values.
- Integer/temperature/brightness codes -> enforce documented min/max/step.
- String/json codes -> validate schema before write.

## High-Impact Device Classes

Apply stricter confirmation for:
- smart locks
- alarm/siren devices
- HVAC and heating controls
- high-power switches and relays

## Write Discipline

- Use single-device canary before bulk commands.
- Keep retry count bounded and logged.
- Abort batch when first critical verification fails.

# Troubleshooting - Shelly BluTRV

Use this guide when the skill can reach some Shelly components but control or state verification still behaves unexpectedly.

## Symptom: Thermostat does not react after setting a target

Checks:

- Confirm the correct gateway IP and TRV id are being used.
- Confirm the BluTRV is awake enough to receive Bluetooth commands.
- Confirm the post-write verification read shows the same `target_C`.

Recovery:

- Retry once after a short delay.
- Re-run `scripts/blutrv-status.sh` for the same room or gateway/TRV pair.
- If local reads keep failing, inspect whether cloud fallback still shows recent data.

## Symptom: Local status times out

Checks:

- Confirm the gateway is reachable in the local network.
- Confirm the room-to-gateway mapping is still correct.
- Confirm the selected TRV id exists on that gateway.

Recovery:

- Use `scripts/blutrv-status.sh` and let it attempt cloud fallback.
- Re-check the configured gateway IPs in the env file.
- Treat cloud data as fallback only, not proof that a local write succeeded.

## Symptom: Cloud fallback returns incomplete data

Checks:

- Confirm `SHELLY_CLOUD_SERVER_URI` and `SHELLY_CLOUD_TOKEN` are set.
- Confirm the gateway device id matches the selected gateway.
- Confirm the target device is visible in the Shelly cloud account.

Recovery:

- Refresh the gateway-device-id mapping in the environment.
- Prefer local RPC for immediate operational decisions whenever possible.

## Symptom: Room alias does not resolve

Checks:

- Supported aliases include `schlafzimmer`, `wohnzimmer`, `flur`, `bedroom`, `living-room`, and `hallway`.
- Confirm the environment variables for room mappings were not changed inconsistently.

Recovery:

- Use the explicit `gateway_ip trv_id` form temporarily.
- Add or adjust env-based room mappings before relying on aliases again.

## Symptom: Status after write does not match the requested target

Checks:

- Distinguish command acceptance from final applied state.
- Confirm no competing automation is rewriting the thermostat target.
- Confirm the verification window is long enough for the device.

Recovery:

- Re-read status after a short delay.
- Freeze conflicting automation paths if they exist.
- Only report success after a verified matching `target_C`.

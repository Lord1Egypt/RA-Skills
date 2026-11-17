# Troubleshooting

| Code/status | Explain | Next action |
| --- | --- | --- |
| `no_devices` | No valid WiFi advertisements arrived | Check power, LAN, multicast, and OS local-network permission; retry refresh |
| `identity_collision` | One protocol ID appeared from different senders | Do not control it; inspect the LAN and retry after the conflict is gone |
| `rebind_pending` | A saved device moved to a new endpoint | Confirm the one-time friendly rebind |
| `offline` | A saved device was not found | Keep its local configuration; restore power/LAN and refresh |
| `unsupported` | The device did not advertise the requested capability | Offer a supported alternative; do not guess a method |
| `clarification_required` | Target, group member freshness, or action conflict is ambiguous | Ask one focused question before writing |
| `partial` | Some selected devices completed and others were skipped/failed | List each row; offer online-only control or explicit recovery |
| `uncertain` | A timeout or crash prevents a safe conclusion | Fresh-read first; use `operation.recover` only after confirmation |
| `quota_exhausted` | The PDF command budget would be exceeded | Reduce batch size or wait; do not retry automatically |
| `storage_corrupt` | Primary and backup cannot be trusted | Stop writes; offer export/repair diagnostics, never reset silently |
| `not_supported` | No Host scheduler is available | Keep an inactive local draft; do not install an OS task |

Never expose raw IPs, protocol IDs, packets, credentials, or stack traces in the
user-facing response.

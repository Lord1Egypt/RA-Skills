# Cameras - Tapo Camera

Use this file when the user wants a stable local inventory of known cameras.

## Suggested Fields

For each camera, capture only the minimum useful facts:

| Field | Meaning |
|-------|---------|
| Label | Human name such as Front Door or Office |
| Host | Current IP or stable hostname |
| Model | Exact model if known |
| Type | direct camera or hub child |
| RTSP | enabled, disabled, unknown |
| ONVIF | enabled, disabled, unknown |
| Last known good path | `kasa`, RTSP, ONVIF, or API fallback |
| Notes | quirks such as battery sleep, privacy mode, or firmware behavior |

## Inventory Rule

Do not store passwords, reversible credential blobs, or full authenticated stream URLs here.

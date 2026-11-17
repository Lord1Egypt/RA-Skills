# Setup and authentication

Read this file before the first Yandex Tracker API call in an environment or when dependency, credential, or client initialization fails.

## Requirements

- A Python interpreter available through the current agent runtime. Do not assume the command is always `python3`; use the interpreter exposed by the environment.
- The `yandex_tracker_client` package. If it is missing, install it only when the runtime permits package installation and the user has provided any required authorization.
- `TRACKER_TOKEN` plus exactly one of:
  - `TRACKER_ORG_ID`: numeric Yandex 360 organization ID.
  - `TRACKER_CLOUD_ORG_ID`: string Yandex Cloud organization ID.

Use a least-privilege OAuth token with the Tracker scope. Keep credentials in the runtime's secret or environment mechanism and never echo or write them to a file.

## Client initialization

Use this validation and initialization pattern:

```python
import os
from yandex_tracker_client import TrackerClient

token = os.environ["TRACKER_TOKEN"]
org_id = os.environ.get("TRACKER_ORG_ID")
cloud_org_id = os.environ.get("TRACKER_CLOUD_ORG_ID")

if bool(org_id) == bool(cloud_org_id):
    raise RuntimeError(
        "Set exactly one of TRACKER_ORG_ID or TRACKER_CLOUD_ORG_ID"
    )

if cloud_org_id:
    client = TrackerClient(token=token, cloud_org_id=cloud_org_id)
else:
    client = TrackerClient(token=token, org_id=int(org_id))
```

For a temporary Yandex Cloud IAM token, pass it with the client's `iam_token=` argument instead of `token=`. Keep that token in a runtime secret rather than embedding it in the script.

## Portable execution

For multi-step requests, write one self-contained script to a temporary or working directory provided by the runtime and execute it with the available Python interpreter. Do not hardcode `/tmp`, Windows drive letters, or an agent-specific tool name.

Keep related API calls together. Print JSON, a compact table, or clearly labeled lines containing only the result the user needs. Never print environment variables, authorization headers, or full unredacted API payloads that may contain secrets.

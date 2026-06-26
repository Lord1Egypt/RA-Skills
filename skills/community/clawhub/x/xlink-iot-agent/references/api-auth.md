# Xlink Gateway Authentication

## Overview

Xlink Gateway uses signature-based authentication via `GatewayAppClient`. Each request is signed using App ID and App Secret.

## Getting API Credentials

1. Log in to Xlink IoT Platform console
2. Navigate to **Settings → API Access** or **Gateway → Applications**
3. Create a new application to obtain App ID and App Secret
4. Store credentials securely (never commit to version control)

## Authentication Mechanism

The `GatewayAppClient` automatically handles:

- **Timestamp generation** - Millisecond precision timestamp
- **Request ID** - Unique identifier for each request
- **Signature** - SHA256 signature of request components
- **Content-MD5** - MD5 hash of request body (for POST/PUT)

### Signature Components

```
sign_parts = [
    app_id,
    app_secret,
    timestamp,
    request_id,
    full_path,
    content_md5 (optional, for POST/PUT with body)
]
signature = base64(sha256(sign_parts joined by newline))
```

### Request Headers

| Header | Description |
|--------|-------------|
| `App-ID` | Your application ID |
| `Timestamp` | Request timestamp (ms) |
| `Request-ID` | Unique request identifier |
| `Signature` | SHA256 signature (base64) |
| `Content-MD5` | Body MD5 hash (for POST/PUT) |
| `Group` | Gateway group |
| `Stage` | Environment stage (RELEASE/TEST/PRE_RELEASE) |

## Environment Variables

```bash
export XLINK_BASE_URL="https://api-gw.xlink.cn"
export XLINK_APP_ID="your-app-id"
export XLINK_APP_SECRET="your-app-secret"
export XLINK_API_GROUP="your-group-id"
```

## Usage Example

```python
from gateway_app_client import GatewayAppClient, StageType
import os

client = GatewayAppClient(
    app_id=os.environ["XLINK_APP_ID"],
    app_secret=os.environ["XLINK_APP_SECRET"],
)

# GET request
response = client.get(
    group=os.environ["XLINK_API_GROUP"],
    stage=StageType.RELEASE,
    url="/v3/device-service/devices/overview",
    host=os.environ["XLINK_BASE_URL"],
)

# POST request with body
response = client.post(
    group=os.environ["XLINK_API_GROUP"],
    stage=StageType.RELEASE,
    url="/v2/service/events/all-instances",
    host=os.environ["XLINK_BASE_URL"],
    data={"offset": 0, "limit": 10}
)
```

Or use the high-level `xlink_api.py` as a module:

```python
import sys
sys.path.insert(0, "scripts")
from xlink_api import XlinkIoTClient

client = XlinkIoTClient()  # Reads from environment variables

# Device overview
overview = client.get_device_overview()

# Event instances
events = client.get_event_instances(limit=20)

# Device control
result = client.control_device(
    thing_id="10299402",
    service="device_attribute_set_service",
    input_params={"Power": 1}
)
```

## Security Notes

- Never expose App Secret in client-side code or logs
- Rotate App Secret periodically
- Use TEST stage for development
- Monitor API usage for anomalies
- Implement rate limiting on your side

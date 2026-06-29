# Webhook - HTTP Request Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `webhook-http-request`

x402 availability: not enabled for this product.

## `request`

Action slug: `request`

Price: `5` credits

Make an HTTP request to a specified URL. Supports all standard HTTP methods, multiple authentication schemes, and flexible body/response formats.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `allow_private` | `boolean` | no | Set to true to allow requests to private or loopback IP addresses. |
| `auth_header_name` | `string` | no | Custom header name for header-based authentication. Required when auth_type is header. |
| `auth_header_value` | `string` | no | Custom header value for header-based authentication. Required when auth_type is header. |
| `auth_password` | `string` | no | Password for basic authentication. Required when auth_type is basic. |
| `auth_token` | `string` | no | Bearer token for authentication. Required when auth_type is bearer. |
| `auth_type` | `string` | no | Authentication scheme to use. |
| `auth_username` | `string` | no | Username for basic authentication. Required when auth_type is basic. |
| `body_base64` | `string` | no | Base64-encoded binary body payload. Only one body type allowed per request. |
| `body_json` | `object` | no | JSON object body. Sets Content-Type to application/json automatically. Only one body type allowed per request. |
| `body_text` | `string` | no | Plain text body payload. Only one body type allowed per request. |
| `headers` | `object` | no | Custom HTTP headers as key-value pairs. |
| `max_response_bytes` | `integer` | no | Maximum response size to return in bytes. |
| `query_params` | `object` | no | URL query parameters as key-value pairs. |
| `request_method` | `string` | no | HTTP method to use. |
| `response_mode` | `string` | no | How to return the response body. Auto detects based on Content-Type. |
| `timeout_seconds` | `integer` | no | Request timeout in seconds. |
| `url` | `string` | yes | The full URL to send the request to (must be http or https). |

Sample parameters:

```json
{
  "allow_private": false,
  "auth_header_name": "example auth header name",
  "auth_header_value": "example auth header value",
  "auth_password": "example auth password",
  "auth_token": "example auth token",
  "auth_type": "none",
  "auth_username": "example auth username",
  "body_base64": "example body base64"
}
```

Generated JSON parameter schema:

```json
{
  "allow_private": {
    "default": false,
    "description": "Set to true to allow requests to private or loopback IP addresses.",
    "required": false,
    "type": "boolean"
  },
  "auth_header_name": {
    "description": "Custom header name for header-based authentication. Required when auth_type is header.",
    "required": false,
    "type": "string"
  },
  "auth_header_value": {
    "description": "Custom header value for header-based authentication. Required when auth_type is header.",
    "required": false,
    "type": "string"
  },
  "auth_password": {
    "description": "Password for basic authentication. Required when auth_type is basic.",
    "required": false,
    "type": "string"
  },
  "auth_token": {
    "description": "Bearer token for authentication. Required when auth_type is bearer.",
    "required": false,
    "type": "string"
  },
  "auth_type": {
    "default": "none",
    "description": "Authentication scheme to use.",
    "enum": [
      "none",
      "basic",
      "bearer",
      "header"
    ],
    "required": false,
    "type": "string"
  },
  "auth_username": {
    "description": "Username for basic authentication. Required when auth_type is basic.",
    "required": false,
    "type": "string"
  },
  "body_base64": {
    "description": "Base64-encoded binary body payload. Only one body type allowed per request.",
    "required": false,
    "type": "string"
  },
  "body_json": {
    "description": "JSON object body. Sets Content-Type to application/json automatically. Only one body type allowed per request.",
    "properties": {},
    "required": false,
    "type": "object"
  },
  "body_text": {
    "description": "Plain text body payload. Only one body type allowed per request.",
    "required": false,
    "type": "string"
  },
  "headers": {
    "description": "Custom HTTP headers as key-value pairs.",
    "properties": {},
    "required": false,
    "type": "object"
  },
  "max_response_bytes": {
    "default": 1048576,
    "description": "Maximum response size to return in bytes.",
    "maximum": 20971520,
    "minimum": 1024,
    "required": false,
    "type": "integer"
  },
  "query_params": {
    "description": "URL query parameters as key-value pairs.",
    "properties": {},
    "required": false,
    "type": "object"
  },
  "request_method": {
    "default": "GET",
    "description": "HTTP method to use.",
    "enum": [
      "GET",
      "POST",
      "PUT",
      "PATCH",
      "DELETE",
      "HEAD",
      "OPTIONS"
    ],
    "required": false,
    "type": "string"
  },
  "response_mode": {
    "default": "auto",
    "description": "How to return the response body. Auto detects based on Content-Type.",
    "enum": [
      "auto",
      "json",
      "text",
      "base64"
    ],
    "required": false,
    "type": "string"
  },
  "timeout_seconds": {
    "default": 30,
    "description": "Request timeout in seconds.",
    "maximum": 120,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "url": {
    "description": "The full URL to send the request to (must be http or https).",
    "required": true,
    "type": "string"
  }
}
```

# Secure API Starter

Production-ready secure API template.

## Features

- **Authentication** - JWT, API keys, OAuth2
- **Authorization** - Role-based access control
- **Rate Limiting** - Per-user, per-IP
- **Input Validation** - Schema validation
- **Logging** - Request/response logs
- **Error Handling** - Structured errors

## Quick Start

```bash
# Create API
./create-api.sh my-api

# Add authentication
./create-api.sh my-api --auth jwt

# Add rate limiting
./create-api.sh my-api --rate-limit 100
```

## Auth Methods

- JWT tokens
- API keys
- OAuth2 (Google, GitHub)
- Session-based

## Requirements

- Node.js 18+
- TypeScript

## Author

Sunshine-del-ux

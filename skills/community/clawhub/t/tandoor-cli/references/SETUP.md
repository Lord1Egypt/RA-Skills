# tandoor-cli Setup Guide

A command-line interface for [Tandoor Recipe Manager](https://tandoor.dev).

---

## Prerequisites

- Node.js 18+
- npm 8+
- A running Tandoor instance (local or remote)

---

## Installation

### Option 1: Install globally via npm

```bash
npm install -g tandoor-cli
```

After the global install, the `tandoor` command becomes available system-wide.

### Option 2: Run without installing

```bash
npx tandoor-cli <command>
```

No global install is required. `npx` downloads and runs the CLI on demand.

**Note:** The rest of this documentation assumes a global install.

---

## Configuration

`TANDOOR_URL` and at least one authentication method are required.

The CLI supports three configuration sources, applied in this order (highest priority first):

1. Environment variables
2. Persistent config file
3. `.env` file

### Option 1: Environment variables

```bash
export TANDOOR_URL=http://localhost:8080
export TANDOOR_API_TOKEN=your_token_here
```

Environment variables take precedence over stored config and `.env` settings.

### Option 2: `tandoor configure`

Run the interactive setup command to save credentials to `~/.config/tandoor-cli/config.json`:

```bash
# without install
npx tandoor-cli configure

# with global install
tandoor configure
```

You will be prompted for:
- `TANDOOR_URL`
- `TANDOOR_API_TOKEN`

The file is written with restricted permissions (0600) to protect your credentials.

### Option 3: `.env` file

Create a `.env` file in your working directory:

```dotenv
TANDOOR_URL=http://localhost:8080
TANDOOR_API_TOKEN=your_token_here
TANDOOR_USERNAME=
TANDOOR_PASSWORD=
```

The CLI loads `.env` automatically when present.

---

## Authentication

### API token (preferred)

Use an OAuth2 access token with Bearer authentication. 

**Important:** The regular DRF token shown in Tandoor's Settings → API does **not** work for this CLI. You need an OAuth2 access token.

**⚠️ Security Note:** Use the shortest token lifetime appropriate for your use case. For AI agent use, consider tokens that expire in days or weeks, not years.

#### Generating an OAuth2 token

If you're running Tandoor in Docker, you can generate an OAuth2 token using the Django shell. Choose the appropriate example based on your needs:

##### Read-Only Token (Safest)

For querying recipes only:

```bash
docker exec <your-container-name> /opt/recipes/venv/bin/python /opt/recipes/manage.py shell -c "
from oauth2_provider.models import Application, AccessToken
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import secrets

user = User.objects.get(username='YOUR_USERNAME')

app, _ = Application.objects.get_or_create(
    name='tandoor-cli',
    defaults=dict(
        user=user,
        client_type=Application.CLIENT_CONFIDENTIAL,
        authorization_grant_type=Application.GRANT_PASSWORD,
    )
)

token = AccessToken.objects.create(
    user=user,
    application=app,
    token=secrets.token_hex(20),
    expires=timezone.now() + timedelta(days=7),  # 7 days
    scope='read',  # Read-only
)
print('ACCESS TOKEN:', token.token)
"
```

##### Read-Write Token (Standard)

For recipe management (add, edit, delete recipes):

```bash
docker exec <your-container-name> /opt/recipes/venv/bin/python /opt/recipes/manage.py shell -c "
from oauth2_provider.models import Application, AccessToken
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import secrets

user = User.objects.get(username='YOUR_USERNAME')

app, _ = Application.objects.get_or_create(
    name='tandoor-cli',
    defaults=dict(
        user=user,
        client_type=Application.CLIENT_CONFIDENTIAL,
        authorization_grant_type=Application.GRANT_PASSWORD,
    )
)

token = AccessToken.objects.create(
    user=user,
    application=app,
    token=secrets.token_hex(20),
    expires=timezone.now() + timedelta(days=30),  # 30 days
    scope='read write',
)
print('ACCESS TOKEN:', token.token)
"
```

Replace `<your-container-name>` with the name of your running Tandoor Docker container and `YOUR_USERNAME` with your Tandoor username. Copy the printed token into `TANDOOR_API_TOKEN`.

**Token Lifetime Recommendations:**
- **AI agents / automation:** 7-30 days
- **Personal CLI use:** 30-90 days
- **Testing / development:** 1-7 days
- **Administrative tasks:** 1 day (revoke after use)

**Token Security Best Practices:**
- Store tokens securely (environment variables, secret managers)
- Never commit tokens to version control
- Revoke tokens immediately if compromised
- Rotate tokens regularly
- Use read-only tokens when possible
- See `SECURITY.md` for comprehensive security guidance

### Username/password fallback

If `TANDOOR_API_TOKEN` is missing, the CLI falls back to HTTP Basic Authentication using `TANDOOR_USERNAME` and `TANDOOR_PASSWORD`.

**Note:** This method is less secure and not recommended for production use.

---

## Verification

Test your configuration:

```bash
# Check version
tandoor --version

# List recipes (requires valid credentials)
tandoor list --limit 5
```

If you see recipes listed, your configuration is working correctly!

---

## Troubleshooting

### "TANDOOR_URL is not set"

Run `tandoor configure` or set the `TANDOOR_URL` environment variable.

### "Authentication failed" or 401 errors

- Verify your `TANDOOR_API_TOKEN` is a valid OAuth2 token (not a DRF token)
- Check that your token hasn't expired
- Ensure your Tandoor instance is accessible at the configured URL

### "Permission denied" or 403 errors

Some commands (especially household management) require admin or space owner privileges. Check your user permissions in Tandoor.

### Command not found

If `tandoor` command is not found after global install:
- Verify npm's global bin directory is in your PATH
- Try `npx tandoor-cli` instead
- Reinstall: `npm install -g tandoor-cli`

---

## Next Steps

For command usage examples and full documentation, see the main [README](https://github.com/dcenatiempo/tandoor-cli#readme).

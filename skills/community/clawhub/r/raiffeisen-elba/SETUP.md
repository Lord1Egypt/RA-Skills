# raiffeisen-elba - Setup Instructions

> **Disclaimer:** Note that no passwords are stored. The custom username or user number is used to trigger the 2FA flow where the user approves the login separately. By itself the skill is unable to access any bank data. If you are not comfortable auditing the code or running browser automation that extracts tokens, do not install or run this skill with real bank credentials.

## Prerequisites

### Required Software

- **Python 3** — For running the automation script
- **pip** — For installing Python packages

### Python Packages

Install required dependencies:
```bash
pip3 install requests playwright
```

Install Playwright browsers:
```bash
python3 -m playwright install chromium
```

### Mobile Device

- **Raiffeisen pushTAN app** — Must be installed on your iPhone/smartphone
- **App configured** — Linked to your ELBA account for 2FA

## Configuration

### Credentials

**Config File**

Create `<WORKSPACE_ROOT>/raiffeisen-elba/config.json`:
```json
{
  "elba_id": "YOUR_ELBA_ID",
  "pin": "YOUR_PIN"
}
```

Set restrictive permissions:
```bash
chmod 600 <WORKSPACE_ROOT>/raiffeisen-elba/config.json
```

### State Directory

Per-user state is stored in `<WORKSPACE_ROOT>/raiffeisen-elba/`:
- `.pw-profile/` — Playwright browser profile (cookies, session)
- Automatically created with restrictive permissions (dirs: 700, files: 600)

The `logout` command deletes `.pw-profile/` to clear session state.

## Security

*Please see [SECURITY.md](SECURITY.md) for details on the skill's browser automation, token handling, and overall security policy.*

### File Permissions

The skill automatically sets restrictive permissions:
- Directories: `700` (owner read/write/execute only)
- Files: `600` (owner read/write only)

This prevents other users from accessing your banking credentials or session data.

### Output Paths

Output files (`--out` parameter) are restricted to:
- Workspace directory (`<WORKSPACE_ROOT>/`)
- Temporary directory (`/tmp/`)

Attempts to write outside these locations will fail.

## Authentication Flow

### 2FA via pushTAN

When you run `login`, the script:
1. Enters your ELBA ID and PIN
2. Requests pushTAN authentication
3. Displays a 6-digit confirmation code
4. **You must approve** the pushTAN request in the Raiffeisen app on your iPhone
   - Open the Raiffeisen app
   - Check that the code matches
   - Approve the login

The script waits for your approval (timeout: ~60 seconds).

### Session Management

After successful login:
- Browser session is stored in `.pw-profile/`
- Subsequent commands reuse the session (no re-authentication needed)
- **Always call `logout`** after completing operations to clear session state

Recommended workflow:
```bash
login → accounts → transactions → portfolio → logout
```

## Verification

Test your setup:

```bash
# Login (triggers pushTAN on your phone)
python3 ~/Developer/Skills/raiffeisen-elba/scripts/elba.py login

# List accounts (JSON)
python3 ~/Developer/Skills/raiffeisen-elba/scripts/elba.py accounts

# Logout (clear session)
python3 ~/Developer/Skills/raiffeisen-elba/scripts/elba.py logout
```

On first `login`, approve the pushTAN request on your phone when prompted.

## Troubleshooting

### pushTAN Not Received

- Check that the Raiffeisen app is installed and logged in
- Verify pushTAN is enabled in ELBA settings
- Check network connectivity on your phone
- Ensure the ELBA ID and PIN are correct

### Session Expired

If commands fail with authentication errors:
1. Run `logout` to clear old session
2. Run `login` again to create fresh session
3. Approve pushTAN on your phone

### Browser Profile Issues

If Playwright fails to launch:
```bash
# Delete browser profile
rm -rf <WORKSPACE_ROOT>/raiffeisen-elba/.pw-profile

# Reinstall Playwright browsers
python3 -m playwright install chromium
```

## Notes

- **Headless browser** — Playwright runs in headless mode by default
- **Session persistence** — Browser profile persists between commands (until `logout`)
- **2FA required** — Every `login` requires pushTAN approval on your phone
- **Logout is important** — Always logout to minimize persistent session state on disk

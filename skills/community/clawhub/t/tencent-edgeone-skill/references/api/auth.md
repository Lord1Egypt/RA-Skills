# Configure TCCLI Credentials

## Login Method

First, run the following command to verify the current login status:

```sh
tccli cvm DescribeRegions --request-client "tencent-edgeone-skill/1.1.0 module/api" 2>&1; echo "EXIT_CODE:$?"
```

- If a normal result is returned, you are already logged in — no need to log in again.
- If it shows `secretId is invalid` or other authentication errors, you are not logged in and need to continue with the login command below.

Browser-based authorization login is recommended — no need to manually enter SecretId/SecretKey, credentials are automatically saved locally:

```sh
tccli auth login
```

After execution, TCCLI will start a temporary port on your machine and print an OAuth authorization link (it usually also opens automatically in the default browser). Once the user completes login and authorization in the browser, TCCLI receives the callback, writes the credentials, and exits.

- If the browser does not open automatically, copy the link printed in the terminal and open it manually in a browser.
- Upon success, it will display: "Login successful, credentials have been written to: ..."

---

## Agent Operating Guidelines

**Determining whether login is needed:**

1. First run `tccli cvm DescribeRegions`.
2. If a **reasonable success result** is returned, consider the user logged in and proceed with subsequent operations.
3. If an error is returned or the command cannot execute, you must first run `tccli auth login`.
4. Never ask the user for `SecretId` / `SecretKey`, and do not execute commands that might expose credential contents (especially `tccli configure list`).


> ⚠️ The Agent must not assume TCCLI is usable based solely on the user's verbal statement or potentially stale credential files on the machine.

**When running `tccli auth login`:**

- This command will **block** until the user completes browser login (or it times out).
- The Agent should clearly inform the user: "Please open the authorization link shown in the terminal/tool output and complete login in the browser; the command will end automatically once done."

---

## Multi-Account & Logout

| Operation | Command |
|------|------|
| Login default account | `tccli auth login` |
| Login specific account | `tccli auth login --profile user1` |
| Logout default account | `tccli auth logout` |
| Logout specific account | `tccli auth logout --profile user1` |

Credential file notes:
- Default account credentials are saved in `default.credential`
- Specific account credentials are saved in `<profile-name>.credential` (e.g., `user1.credential`)

## Security Reminder

> Using `tccli configure` to manually enter SecretId / SecretKey is **not recommended**. Manually configured keys are stored in plaintext locally and risk being leaked. Always use the `tccli auth login` browser authorization method.

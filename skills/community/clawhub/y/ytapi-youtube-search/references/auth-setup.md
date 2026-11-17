# YTAPI: getting and storing the API key

Read this whole file before doing anything. The goal is an API key in the
environment variable `YTAPI_API_KEY` that stays set in future sessions.

## Step 0: find out how to store it

Work out how this agent and machine keep environment variables between
sessions, including non-interactive shells: a shell profile, the agent's own
env or config file, or a secrets store. Check your own documentation or
configuration; do not guess. You will store `YTAPI_API_KEY` there.

## Step 1: ask the user one question

Ask, in one message:

> Do you have a YTAPI API key? If so, paste it here. If not, I can create a
> free account for you now: it comes with 200 free credits and needs no card.
> I'll only need your email address and the 6-digit code we send to it.

- The user pastes a key (it starts with `sk_`): go to **Store the key**.
- The user wants an account: go to **Create an account**.

## Create an account

### 1. Ask for the email address

Ask which email address to use. Temporary or disposable inboxes are refused.

### 2. Request a code

Save the response to a file. Do not print the token on its own; some agent
environments redact token-like values from tool output, so pass it from file
to request in one step.

```bash
curl -s -X POST https://ytapi.dev/api/agent/signup \
  -H "Content-Type: application/json" \
  -d '{"email": "USER_EMAIL"}' \
  -o /tmp/ytapi-signup.json
grep -o '"status":"[^"]*"\|"error":{[^}]*}' /tmp/ytapi-signup.json
```

A success shows `"status":"code_sent"`. Anything else shows an `error` object
(see **Errors** below).

### 3. Ask for the code

Tell the user: "I've sent a 6-digit code to USER_EMAIL. Please check your
inbox (and spam folder) and tell me the code." The code is valid for 10
minutes.

### 4. Verify the code and get the key

Read the token from the saved file inside the same command, and save the
response to a file without printing it:

```bash
TOKEN=$(sed -n 's/.*"signup_token":"\([^"]*\)".*/\1/p' /tmp/ytapi-signup.json)
curl -s -X POST https://ytapi.dev/api/agent/verify \
  -H "Content-Type: application/json" \
  -d "{\"signup_token\": \"$TOKEN\", \"code\": \"CODE\"}" \
  -o /tmp/ytapi-verify.json
grep -o '"status":"[^"]*"\|"credits":[0-9]*\|"error":{[^}]*}' /tmp/ytapi-verify.json
```

`"status":"account_created"` means the file holds the key in `api_key`. Go to
**Store the key**, reading it from `/tmp/ytapi-verify.json`:

```bash
sed -n 's/.*"api_key":"\(sk_[A-Za-z0-9]*\)".*/\1/p' /tmp/ytapi-verify.json
```

Use that output directly in the command that stores the key; do not echo it
into the conversation.

### Errors

| Code | What to do |
| --- | --- |
| `invalid_code` | Ask the user to check the code. After 3 wrong codes, start again at step 2. |
| `code_expired`, `too_many_attempts`, `invalid_signup_token` | Start again at step 2. |
| `account_exists` (409) | The email already has an account. The user signs in at <https://ytapi.dev/auth/login?utm_source=skill&utm_medium=auth-setup>, creates a key at <https://ytapi.dev/app/api-keys?utm_source=skill&utm_medium=auth-setup> and pastes it here. Then go to **Store the key**. |
| `disposable_email`, `undeliverable_email`, `invalid_email` | Ask for the user's regular email address. |
| `rate_limited`, `agent_signup_busy`, `email_failed` | Wait and try later, or let the user sign up at <https://ytapi.dev/auth/login?utm_source=skill&utm_medium=auth-setup>. |

## Store the key

1. Store `YTAPI_API_KEY` with the method from Step 0, so new sessions,
   including non-interactive shells, see it without the user doing anything.
2. Check it in the current session without printing it, for example
   `test -n "$YTAPI_API_KEY" && echo set`. If the session must be reloaded to
   see it, reload it or tell the user.
3. Delete the temporary files: `rm -f /tmp/ytapi-signup.json /tmp/ytapi-verify.json`.

The user can sign in at https://ytapi.dev/auth/login?utm_source=skill&utm_medium=auth-setup with the same email to
see usage, manage keys and buy credits.

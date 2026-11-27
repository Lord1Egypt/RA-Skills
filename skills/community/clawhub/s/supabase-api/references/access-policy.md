# Supabase access policy

An access policy limits which endpoints Supabase connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/supabase#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Supabase: its 29 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create supabase --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "auth/v1/admin/audit"},
    {"method": "GET", "path": "auth/v1/admin/custom-providers"},
    {"method": "GET", "path": "auth/v1/admin/custom-providers/{id}"},
    {"method": "GET", "path": "auth/v1/admin/sso/providers"},
    {"method": "GET", "path": "auth/v1/admin/sso/providers/{id}"},
    {"method": "GET", "path": "auth/v1/admin/users"},
    {"method": "GET", "path": "auth/v1/admin/users/{id}"},
    {"method": "GET", "path": "auth/v1/admin/users/{id}/factors"},
    {"method": "GET", "path": "auth/v1/factors/recovery-codes"},
    {"method": "GET", "path": "auth/v1/.well-known/jwks.json"},
    {"method": "GET", "path": "auth/v1/health"},
    {"method": "GET", "path": "auth/v1/settings"},
    {"method": "GET", "path": "auth/v1/oauth/authorizations/{id}"},
    {"method": "GET", "path": "auth/v1/sso/saml/metadata"},
    {"method": "GET", "path": "auth/v1/user"},
    {"method": "GET", "path": "auth/v1/user/oauth/grants"},
    {"method": "GET", "path": "rest/v1"},
    {"method": "GET", "path": "rest/v1/rpc/{id}"},
    {"method": "GET", "path": "rest/v1/{id}"},
    {"method": "GET", "path": "storage/v1/bucket"},
    {"method": "GET", "path": "storage/v1/bucket/{id}"},
    {"method": "GET", "path": "storage/v1/object/authenticated/{id}/**"},
    {"method": "GET", "path": "storage/v1/object/info/{id}/**"},
    {"method": "POST", "path": "storage/v1/object/list-v2/{id}"},
    {"method": "POST", "path": "storage/v1/object/list/{id}"},
    {"method": "GET", "path": "storage/v1/object/public/{id}/**"},
    {"method": "GET", "path": "storage/v1/object/{id}/**"},
    {"method": "GET", "path": "storage/v1/render/image/authenticated/{id}/**"},
    {"method": "GET", "path": "storage/v1/render/image/public/{id}/**"}
  ],
  "deny": []
}
```

## Endpoints

The Supabase endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | auth/v1/admin/audit | read | auth-admin | Fetch audit log events. |
| GET | auth/v1/admin/custom-providers | read | auth-admin | List all custom OIDC/OAuth providers. |
| POST | auth/v1/admin/custom-providers | write | auth-admin | Create a new custom OIDC/OAuth provider. |
| GET | auth/v1/admin/custom-providers/{id} | read | auth-admin | Get custom OIDC/OAuth provider details. |
| PUT | auth/v1/admin/custom-providers/{id} | write | auth-admin | Update custom OIDC/OAuth provider. |
| DELETE | auth/v1/admin/custom-providers/{id} | write | auth-admin | Delete custom OIDC/OAuth provider. |
| POST | auth/v1/admin/generate_link | write | auth-admin | Generate a link to send in an email message. |
| GET | auth/v1/admin/oauth/clients | write | auth-admin | List OAuth clients (admin). Kept out of read: client schema includes client_secret. |
| POST | auth/v1/admin/oauth/clients | write | auth-admin | Register OAuth client (admin). |
| GET | auth/v1/admin/oauth/clients/{id} | write | auth-admin | Get OAuth client details (admin). Kept out of read: client schema includes client_secret. |
| PUT | auth/v1/admin/oauth/clients/{id} | write | auth-admin | Update OAuth client (admin). |
| DELETE | auth/v1/admin/oauth/clients/{id} | write | auth-admin | Delete OAuth client (admin). |
| POST | auth/v1/admin/oauth/clients/{id}/regenerate_secret | write | auth-admin | Regenerate OAuth client secret (admin). |
| GET | auth/v1/admin/sso/providers | read | auth-admin | Fetch a list of all registered SSO providers. |
| POST | auth/v1/admin/sso/providers | write | auth-admin | Register a new SSO provider. |
| GET | auth/v1/admin/sso/providers/{id} | read | auth-admin | Fetch SSO provider details. |
| PUT | auth/v1/admin/sso/providers/{id} | write | auth-admin | Update details about a SSO provider. |
| DELETE | auth/v1/admin/sso/providers/{id} | write | auth-admin | Remove an SSO provider. |
| GET | auth/v1/admin/users | read | auth-admin | Fetch a listing of users. |
| GET | auth/v1/admin/users/{id} | read | auth-admin | Fetch user account data for a user. |
| PUT | auth/v1/admin/users/{id} | write | auth-admin | Update user's account data. |
| DELETE | auth/v1/admin/users/{id} | write | auth-admin | Delete a user. |
| GET | auth/v1/admin/users/{id}/factors | read | auth-admin | List all of the MFA factors for a user. |
| PUT | auth/v1/admin/users/{id}/factors/{id} | write | auth-admin | Update a user's MFA factor. |
| DELETE | auth/v1/admin/users/{id}/factors/{id} | write | auth-admin | Remove a user's MFA factor. |
| GET | auth/v1/authorize | write | auth-authorize | Redirects to an external OAuth provider. Kept out of read: starts an OAuth redirect flow. |
| GET | auth/v1/callback | write | auth-callback | Redirects OAuth flow errors to the frontend app. Kept out of read: completes an OAuth redirect flow. |
| POST | auth/v1/callback | write | auth-callback | Redirects OAuth flow errors to the frontend app. |
| POST | auth/v1/factors | write | auth-factors | Begin enrolling a new factor for MFA. |
| GET | auth/v1/factors/recovery-codes | read | auth-factors | Get the status of the user's MFA recovery codes. |
| POST | auth/v1/factors/recovery-codes | write | auth-factors | Generate the user's one-time set of MFA recovery codes. |
| DELETE | auth/v1/factors/recovery-codes | write | auth-factors | Revoke the user's MFA recovery codes. |
| POST | auth/v1/factors/recovery-codes/regenerate | write | auth-factors | Replace the user's MFA recovery codes with a new set. |
| POST | auth/v1/factors/recovery-codes/verify | write | auth-factors | Verify a recovery code and upgrade the session to AAL2. |
| DELETE | auth/v1/factors/{id} | write | auth-factors | Remove a MFA factor from a user. |
| POST | auth/v1/factors/{id}/challenge | write | auth-factors | Create a new challenge for a MFA factor. |
| POST | auth/v1/factors/{id}/verify | write | auth-factors | Verify a challenge on a factor. |
| GET | auth/v1/.well-known/jwks.json | read | auth-general | Returns the project's public JSON Web Key Set. |
| GET | auth/v1/health | read | auth-general | Service healthcheck. |
| GET | auth/v1/settings | read | auth-general | Retrieve some of the public settings of the server. |
| POST | auth/v1/invite | write | auth-invite | Invite a user by email. |
| POST | auth/v1/logout | write | auth-logout | Logs out a user. |
| POST | auth/v1/magiclink | write | auth-magiclink | Authenticate a user by sending them a magic link. |
| GET | auth/v1/oauth/authorizations/{id} | read | auth-oauth | Get OAuth authorization details. |
| POST | auth/v1/oauth/authorizations/{id}/consent | write | auth-oauth | Approve or deny OAuth authorization. |
| GET | auth/v1/oauth/authorize | write | auth-oauth | OAuth 2.1 Authorization endpoint. Kept out of read: starts an OAuth redirect flow. |
| POST | auth/v1/oauth/clients/register | write | auth-oauth | Register a new OAuth client dynamically (public endpoint). |
| POST | auth/v1/oauth/token | write | auth-oauth | OAuth 2.1 Token endpoint. |
| POST | auth/v1/otp | write | auth-otp | Authenticate a user by sending them a One-Time Password over email or SMS. |
| POST | auth/v1/reauthenticate | write | auth-reauthenticate | Reauthenticates the possession of an email or phone number for the purpose of password change. |
| POST | auth/v1/recover | write | auth-recover | Request password recovery. |
| POST | auth/v1/resend | write | auth-resend | Resends a one-time password (OTP) through email or SMS. |
| POST | auth/v1/sso/saml/acs | write | auth-saml | SAML 2.0 Assertion Consumer Service (ACS) endpoint. |
| GET | auth/v1/sso/saml/metadata | read | auth-saml | Returns the SAML 2.0 Metadata XML. |
| POST | auth/v1/signup | write | auth-signup | Signs a user up. |
| POST | auth/v1/sso | write | auth-sso | Initiate a Single-Sign On flow. |
| POST | auth/v1/token | write | auth-token | Issues access and refresh tokens based on grant type. |
| GET | auth/v1/user | read | auth-user | Fetch the latest user account information. |
| PUT | auth/v1/user | write | auth-user | Update certain properties of the current user account. |
| GET | auth/v1/user/identities/authorize | write | auth-user | Links an OAuth identity to an existing user. Kept out of read: starts an identity-linking redirect flow. |
| DELETE | auth/v1/user/identities/{id} | write | auth-user | Unlinks an identity from the current user. |
| GET | auth/v1/user/oauth/grants | read | auth-user | List OAuth grants. |
| DELETE | auth/v1/user/oauth/grants | write | auth-user | Revoke OAuth grant. |
| GET | auth/v1/verify | write | auth-verify | Authenticate by verifying the possession of a one-time token. Kept out of read: consumes a one-time token. |
| POST | auth/v1/verify | write | auth-verify | Authenticate by verifying the possession of a one-time token. |
| GET | rest/v1 | read | database | Get the OpenAPI schema describing the exposed tables and functions. |
| GET | rest/v1/rpc/{id} | read | database | Call a stable or immutable Postgres function; PostgREST rejects GET for volatile functions. |
| POST | rest/v1/rpc/{id} | write | database | Call a Postgres function, which may modify data. |
| GET | rest/v1/{id} | read | database | Select rows from a table or view with PostgREST filters. |
| POST | rest/v1/{id} | write | database | Insert or upsert rows into a table. |
| PUT | rest/v1/{id} | write | database | Upsert a single row in a table. |
| PATCH | rest/v1/{id} | write | database | Update rows in a table. |
| DELETE | rest/v1/{id} | write | database | Delete rows from a table. |
| GET | functions/v1/{id} | write | functions | Invoke an Edge Function. Kept out of read: runs arbitrary function code. |
| POST | functions/v1/{id} | write | functions | Invoke an Edge Function. |
| GET | storage/v1/bucket | read | storage | List storage buckets. |
| POST | storage/v1/bucket | write | storage | Create a storage bucket. |
| GET | storage/v1/bucket/{id} | read | storage | Get a storage bucket. |
| PUT | storage/v1/bucket/{id} | write | storage | Update a storage bucket. |
| DELETE | storage/v1/bucket/{id} | write | storage | Delete a storage bucket. |
| POST | storage/v1/bucket/{id}/empty | write | storage | Delete all objects in a bucket. |
| GET | `storage/v1/object/authenticated/{id}/**` | read | storage | Download an object using the caller credentials. |
| POST | storage/v1/object/copy | write | storage | Copy an object. |
| GET | `storage/v1/object/info/{id}/**` | read | storage | Get object metadata. |
| POST | storage/v1/object/list-v2/{id} | read | storage | List objects in a bucket with cursor pagination. |
| POST | storage/v1/object/list/{id} | read | storage | List objects in a bucket. |
| POST | storage/v1/object/move | write | storage | Move an object. |
| GET | `storage/v1/object/public/{id}/**` | read | storage | Download an object from a public bucket. |
| POST | `storage/v1/object/sign/{id}/**` | write | storage | Create a signed download URL for an object. |
| POST | `storage/v1/object/upload/sign/{id}/**` | write | storage | Create a signed upload URL for an object. |
| DELETE | storage/v1/object/{id} | write | storage | Delete multiple objects. |
| GET | `storage/v1/object/{id}/**` | read | storage | Download an object using the caller credentials. |
| POST | `storage/v1/object/{id}/**` | write | storage | Upload an object. |
| PUT | `storage/v1/object/{id}/**` | write | storage | Replace an object. |
| DELETE | `storage/v1/object/{id}/**` | write | storage | Delete an object. |
| GET | `storage/v1/render/image/authenticated/{id}/**` | read | storage | Download a transformed image using the caller credentials. |
| GET | `storage/v1/render/image/public/{id}/**` | read | storage | Download a transformed image from a public bucket. |

# Authentication
Authentication
## Configuring Authentication Type

To configure the authentication type used by Self-Managed Materialize, use the
`spec.authenticatorKind` setting in conjunction with any specific configuration
for the authentication method.

The `spec.authenticatorKind` setting determines which authentication method is
used:

| authenticatorKind Value | Description |
| --- | --- |
| <strong>None</strong> | Disables authentication. All users are trusted based on their claimed identity <strong>without</strong> any verification. <strong>Default</strong> |
| <strong>SASL/SCRAM</strong> | <p>Enables:</p> <ul> <li> <p><a href="#configuring-saslscram-authentication" >SASL/SCRAM-SHA-256 authentication</a> for <strong>PostgreSQL wire protocol connections</strong>. SASL/SCRAM-SHA-256 is a challenge-response authentication mechanism that provides enhanced security compared to simple password authentication.</p> </li> <li> <p>Standard password authentication for HTTP/Web Console connections.</p> </li> </ul> <p>When enabled, users must authenticate with their password.</p> > **Tip:** When enabled, you must also set the `mz_system` user password in > `external_login_password_mz_system`. See [Configuring SASL/SCRAM > authentication](#configuring-saslscram-authentication) for details.   |
| <strong>Password</strong> | <p>Enables <a href="#configuring-password-authentication" >password authentication</a> for users. When enabled, users must authenticate with their password.</p> > **Tip:** When enabled, you must also set the `mz_system` user password in > `external_login_password_mz_system`. See [Configuring password > authentication](#configuring-password-authentication) for details. |
| <strong>Oidc</strong> | <p>Enables <a href="/security/self-managed/sso/" >OIDC authentication</a> using JWT tokens from an external identity provider. Users authenticate via their organization&rsquo;s identity provider (e.g., Okta, Microsoft Entra ID).</p> > **Tip:** When enabled, you must also set the `mz_system` user password in > `external_login_password_mz_system`. See [Single sign-on (SSO)](/security/self-managed/sso/) for details. |

> **Warning:** Once enabled, ensure that the `authenticatorKind` field is set for any future version upgrades or rollouts of the Materialize CR. Having it undefined will reset `authenticationKind` to `None`.

### Configuring SASL/SCRAM authentication

> **Note:** SASL/SCRAM-SHA-256 authentication requires Materialize `v26.0.0` or later.

SASL authentication requires users to log in with a password.

When SASL authentication is enabled:
- **PostgreSQL connections** (e.g., `psql`, client libraries, [connection
  poolers](/integrations/connection-pooling/)) use SCRAM-SHA-256 authentication.
- **HTTP/Web Console connections** use standard password authentication.

This hybrid approach provides maximum security for SQL connections while
maintaining compatibility with web-based tools.

To configure Self-Managed Materialize for SASL/SCRAM authentication, update the
following fields:

| Resource | Configuration | Description
|----------|---------------| ------------
| Materialize CR | `spec.authenticatorKind` | Set to `Sasl` to enable SASL/SCRAM-SHA-256 authentication for PostgreSQL connections.
| Kubernetes Secret | `external_login_password_mz_system` | Specify the password for the `mz_system` user, who is the only user initially available. Add `external_login_password_mz_system` to the Kubernetes Secret referenced in the Materialize CR's `spec.backendSecretName` field.

The following example Kubernetes manifest includes configuration for
SASL/SCRAM-SHA-256 authentication:

```hc {hl_lines="15 25"}
apiVersion: v1
kind: Namespace
metadata:
  name: materialize-environment
---
apiVersion: v1
kind: Secret
metadata:
  name: materialize-backend
  namespace: materialize-environment
stringData:
  metadata_backend_url: "..."
  persist_backend_url: "..."
  license_key: "..."
  external_login_password_mz_system: "enter_mz_system_password"
---
apiVersion: materialize.cloud/v1alpha1
kind: Materialize
metadata:
  name: 12345678-1234-1234-1234-123456789012
  namespace: materialize-environment
spec:
  environmentdImageRef: materialize/environmentd:v26.12.1
  backendSecretName: materialize-backend
  authenticatorKind: Sasl
```

> **Warning:** Once enabled, ensure that the `authenticatorKind` field is set for any future version upgrades or rollouts of the Materialize CR. Having it undefined will reset `authenticationKind` to `None`.

### Configuring password authentication

> **Public Preview:** This feature is in public preview.

Password authentication requires users to log in with a password.

To configure Self-Managed Materialize for password authentication, update the following fields:

| Resource | Configuration | Description
|----------|---------------| ------------
| Materialize CR | `spec.authenticatorKind` | Set to `Password` to enable password authentication.
| Kubernetes Secret | `external_login_password_mz_system` | Specify the password for the `mz_system` user, who is the only user initially available. Add `external_login_password_mz_system` to the Kubernetes Secret referenced in the Materialize CR's `spec.backendSecretName` field.

The following example Kubernetes manifest includes configuration for password
authentication:

```hc {hl_lines="15 25"}
apiVersion: v1
kind: Namespace
metadata:
  name: materialize-environment
---
apiVersion: v1
kind: Secret
metadata:
  name: materialize-backend
  namespace: materialize-environment
stringData:
  metadata_backend_url: "..."
  persist_backend_url: "..."
  license_key: "..."
  external_login_password_mz_system: "enter_mz_system_password"
---
apiVersion: materialize.cloud/v1alpha1
kind: Materialize
metadata:
  name: 12345678-1234-1234-1234-123456789012
  namespace: materialize-environment
spec:
  environmentdImageRef: materialize/environmentd:v26.12.1
  backendSecretName: materialize-backend
  authenticatorKind: Password
```

> **Warning:** Once enabled, ensure that the `authenticatorKind` field is set for any future version upgrades or rollouts of the Materialize CR. Having it undefined will reset `authenticationKind` to `None`.

### Configuring OIDC authentication

OIDC (OpenID Connect) authentication allows users to authenticate using JWT
tokens from an external identity provider such as Okta or Microsoft Entra ID.

For detailed setup instructions, including identity provider configuration and
system parameter settings, see [Single sign-on (SSO)](/security/self-managed/sso/).

## Logging in and creating users

> **Note:** With OIDC authentication, roles are [auto-provisioned](/security/self-managed/sso/#auto-provisioning-roles) when a
> user first [logs in through SSO](/security/self-managed/sso/#step-4-verify-the-configuration).

When authentication is enabled, only the `mz_system` user is initially
available. To create additional users:

1. Login as the `mz_system` user, using the `external_login_password_mz_system`
password. ![Image of Materialize Console login screen with mz_system
user](/images/mz_system_login.png "Materialize Console login screen with
mz_system user")
> **Note:** This login screen appears only for authenticator kinds Password and SASL/SCRAM.

1. Use [`CREATE ROLE ... WITH LOGIN PASSWORD ...`](/sql/create-role) to create
new users:

   ```mzsql
   CREATE ROLE <user> WITH LOGIN PASSWORD '<password>';
   ```

1. Log out as `mz_system` user.

   > **Important:** In general, other than the initial login to create new users, avoid using
>    `mz_system` since `mz_system` also used by the Materialize Operator for
>    upgrades and maintenance tasks.

1. Login as one of the created users.

## RBAC

For details on role-based access control (RBAC), including enabling RBAC, see
[Access Control](/security/self-managed/access-control/).

> **Warning:** If RBAC is not enabled, all users have <red>**superuser**</red> privileges.

## See also

- For all Materialize CR settings, see [Materialize CRD Field
Descriptions](/installation/appendix-materialize-crd-field-descriptions/).

# Self-managed

Authentication and authorization in Self-Managed Materialize.

This section covers security for Self-Managed Materialize.

| Guide | Description |
|-------|-------------|
| [Authentication](/security/self-managed/authentication/) | Enable authentication |
| [Single sign-on (SSO)](/security/self-managed/sso/) | Configure OIDC-based single sign-on with an external identity provider |
| [Access control](/security/self-managed/access-control/) | Reference for role-based access management (RBAC) |

See also

- [Appendix: Privileges](/security/appendix/appendix-privileges/)
- [Appendix: Privileges by commands](/security/appendix/appendix-command-privileges/)
- [Appendix: Built-in roles](/security/appendix/appendix-built-in-roles/)

---

## Access control (Role-based)

> **Note:** Initially, only the `mz_system` user (which has superuser/administrator
> privileges) is available to manage roles.

<a name="role-based-access-control-rbac" ></a>

## Role-based access control

In Materialize, role-based access control (RBAC) governs access to objects
through privileges granted to [database
roles](/security/self-managed/access-control/manage-roles/).

## Enabling RBAC

> **Warning:** If RBAC is not enabled, all users have <red>**superuser**</red> privileges.

By default, role-based access control (RBAC) checks are not enabled (i.e.,
enforced) when using [authentication](/security/self-managed/authentication/#configuring-authentication-type). To
enable RBAC, set the system parameter `enable_rbac_checks` to `'on'` or `True`.
You can enable the parameter in one of the following ways:

- For [local installations using
  Kind/Minikube](/self-managed-deployments/installation/#installation-guides), set `spec.enableRbac:
  true` option when instantiating the Materialize object.

- For [Cloud deployments using Materialize's
  Terraforms](/self-managed-deployments/installation/#installation-guides), set
  `enable_rbac_checks` in the environment CR via the `environmentdExtraArgs`
  flag option.

- After the Materialize instance is running, run the following command as
  `mz_system` user:

  ```mzsql
  ALTER SYSTEM SET enable_rbac_checks = 'on';
  ```

If more than one method is used, the `ALTER SYSTEM` command will take precedence
over the Kubernetes configuration.

To view the current value for `enable_rbac_checks`, run the following `SHOW`
command:

```mzsql
SHOW enable_rbac_checks;
```

> **Important:** If RBAC is not enabled, all users have <red>**superuser**</red> privileges.

## Roles and privileges

In Materialize, you can create both:
- Individual user or service account roles; i.e., roles associated with a
  specific user or service account.
- Functional roles, not associated with any single user or service
  account, but typically used to define a set of shared
  privileges that can be granted to other user/service/functional roles.

Initially, only the `mz_system` user is available.

To create additional users or service accounts, login as the `mz_system` user,
using the `external_login_password_mz_system` password, and use [`CREATE ROLE
... WITH LOGIN PASSWORD ...`](/sql/create-role):

```mzsql
CREATE ROLE <user> WITH LOGIN PASSWORD '<password>';
```

> **Note:** If you are using [OIDC authentication (SSO)](/security/self-managed/sso/), user
> roles are **automatically created** when a user first signs in. You do not need
> to manually create roles for OIDC users. See
> [Auto-provisioning roles](/security/self-managed/sso/#auto-provisioning-roles) for
> details.

To create functional roles, login as the `mz_system` user,
using the `external_login_password_mz_system` password, and use [`CREATE ROLE`](/sql/create-role):

```mzsql
CREATE ROLE <role>;
```

### Managing privileges

Once a role is created, you can:

- [Manage its current
  privileges](/security/self-managed/access-control/manage-roles/#manage-current-privileges-for-a-role)
  (i.e., privileges on existing objects):
  - By granting privileges for a role or revoking privileges from a role.
  - By granting other roles to the role or revoking roles from the role.
    *Recommended for user account/service account roles.*
- [Manage its future
  privileges](/security/self-managed/access-control/manage-roles/#manage-future-privileges-for-a-role)
  (i.e., privileges on objects created in the future):
  - By defining default privileges for objects. With default privileges in
   place, a role is automatically granted/revoked privileges as new objects are
   created by **others** (When an object is created, the creator is granted all
   [applicable privileges](/security/appendix/appendix-privileges/) for that
   object automatically).

> **Disambiguation:** - Use `GRANT|REVOKE ...` to modify privileges on **existing** objects. - Use `ALTER DEFAULT PRIVILEGES` to ensure that privileges are automatically granted or revoked when **new objects** of a certain type are created by others. Then, as needed, you can use `GRANT|REVOKE <privilege>` to adjust those privileges. 

### Initial privileges

All roles in Materialize are automatically members of
[`PUBLIC`](/security/appendix/appendix-built-in-roles/#public-role). As
such, every role includes inherited privileges from `PUBLIC`.

By default, the `PUBLIC` role has the following privileges:

**Baseline privileges via PUBLIC role:**

| Privilege | Description | On database object(s) |
| --- | --- | --- |
| <code>USAGE</code> | Permission to use or reference an object. | <ul> <li>All <code>*.public</code> schemas (e.g., <code>materialize.public</code>);</li> <li><code>materialize</code> database; and</li> <li><code>quickstart</code> cluster.</li> </ul>  |

**Default privileges on future objects set up for PUBLIC:**

| Object(s) | Object owner | Default Privilege | Granted to | Description |
| --- | --- | --- | --- | --- |
| <a href="/sql/types/" ><code>TYPE</code></a> | <code>PUBLIC</code> | <code>USAGE</code> | <code>PUBLIC</code> | When a <a href="/sql/types/" >data type</a> is created (regardless of the owner), all roles are granted the <code>USAGE</code> privilege. However, to use a data type, the role must also have <code>USAGE</code> privilege on the schema containing the type. |

Default privileges apply only to objects created after these privileges are
defined. They do not affect objects that were created before the default
privileges were set.

In addition, all roles have:
- `USAGE` on all built-in types and [all system catalog
schemas](/reference/system-catalog/).
- `SELECT` on [system catalog objects](/reference/system-catalog/).
- All [applicable privileges](/security/appendix/appendix-privileges/) for
  an object they create; for example, the creator of a schema gets `CREATE` and
  `USAGE`; the creator of a table gets `SELECT`, `INSERT`, `UPDATE`, and
  `DELETE`.

You can modify the privileges of your organization's `PUBLIC` role as well as
the modify default privileges for `PUBLIC`.

## Privilege inheritance and modular access control

In Materialize, when you grant a role to another role (user role/service account
role/independent role), the target role inherits privileges through the granted
role.

In general, to grant a user or service account privileges, create roles with the
desired privileges and grant these roles to the user or service account role.
Although you can grant privileges directly to the user or service account role,
using separate, reusable roles is recommended for better access management.

With privilege inheritance, you can compose more complex roles by
combining existing roles, enabling modular access control. However:

- Inheritance only applies to role privileges; role attributes and parameters
  are not inherited.
- When you revoke a role from another role (user role/service account
role/independent role), the target role is no longer a member of the revoked
role nor inherits the revoked role's privileges. **However**, privileges are
cumulative: if the target role inherits the same privilege(s) from another role,
the target role still has the privilege(s) through the other role.

## Best practices

### Follow the principle of least privilege

Role-based access control in Materialize should follow the principle of
least privilege. Grant only the minimum access necessary for users and
service accounts to perform their duties.

### Restrict the granting of `CREATEROLE` privilege

{{% include-headless "/headless/rbac-sm/createrole-consideration" %}}

### Use Reusable Roles for Privilege Assignment

{{% include-headless "/headless/rbac-sm/use-resusable-roles" %}}

See also [Manage database roles](/security/self-managed/access-control/manage-roles/).

### Audit for unused roles and privileges.

{{% include-headless "/headless/rbac-sm/audit-remove-roles" %}}

See also [Show roles in
system](/security/self-managed/access-control/manage-roles/#show-roles-in-system)
and [Drop a
role](/security/self-managed/access-control/manage-roles/#drop-a-role) for
more information.

---

## Authentication

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

---

## Migrate to SSO

If you have an existing Materialize deployment using Password/SASL-SCRAM authentication, you
can migrate to OIDC without losing access to existing roles and their owned
objects. The key is to configure `oidc_authentication_claim` so that the value
in the JWT matches the existing Materialize user or service account's role name.

## Step 1. Identify existing roles and choose an authentication claim

Identify the login roles in your Materialize deployment:

```mzsql
SELECT name FROM mz_roles WHERE name NOT LIKE 'mz_%' AND rolcanlogin = true;
```

Users and service accounts authenticate using ID or access tokens issued by their IdP. As the admin, you need to choose the claim in these tokens whose value matches the existing role names in Materialize. The `oidc_authentication_claim` parameter tells Materialize which JWT claim to use as the role name during OIDC authentication. For more details, see [Mapping IdP Users to Materialize Roles](/security/self-managed/sso/#mapping-idp-users-to-materialize-roles).

In most cases, this will work if your existing role names are **email
addresses** (e.g., `alice@your-org.com`), since the `email` claim in the JWT
naturally matches.

If no JWT claim maps to an existing role name, you will need to recreate the
role.

## Step 2. Configure Single sign-on (SSO)

Follow the steps in [Single sign-on (SSO)](/security/self-managed/sso/).

## Step 3. Verify the migration

After enabling OIDC, have each user sign in and verify their role name is the same as before.

## See also

- [Single sign-on (SSO)](/security/self-managed/sso/)
- [Authentication](/security/self-managed/authentication/)
- [Manage roles](/security/self-managed/access-control/manage-roles/)

---

## Single sign-on (SSO)

> **Public Preview:** This feature is in public preview.

Single sign-on (SSO) allows users to authenticate to Self-Managed Materialize
using their organization's identity provider (IdP) via
[OpenID Connect (OIDC)](https://openid.net/developers/how-connect-works/).
Instead of managing passwords directly in Materialize, users sign in through
their IdP (e.g., Okta, Microsoft Entra ID) and receive a JWT token that
Materialize validates.

> **Note:** SSO handles **authentication** only. Permissions within the database are managed
> separately using [role-based access control (RBAC)](/security/self-managed/access-control/).

> **Note:** **Current limitations:**
> - **SAML** authentication is not supported. Materialize supports OIDC only.
> - **SCIM** is not supported. Users are auto-provisioned on first SSO login (see [Auto-provisioning roles](#auto-provisioning-roles)), but removing a user from your IdP does not automatically deprovision their Materialize role.
> - **IdP group-to-role mapping** is not supported. Each user maps 1:1 to a single Materialize role via a JWT claim; privileges and group-based assignment are managed via [RBAC](/security/self-managed/access-control/).

## Before you begin

Make sure you have:

- An OIDC-capable identity provider (e.g., Okta, Microsoft Entra ID, or any
  provider that supports OpenID Connect).
- Admin access to your Kubernetes cluster where Materialize is deployed.

## Step 1. Configure your identity provider

> **Note:** You will use the following values from your IdP configuration to [configure
> OIDC system parameters for Materialize](#step-3-configure-oidc-system-parameters):
> - The OIDC **issuer URL**
> - The **client ID** for the console application
> - If using service accounts, the client ID, client secret, and expected
>   audience for each service-account application

**Okta:**

The following steps create the OIDC application for the **Materialize Console**
(browser-based login). If you also need service accounts, you will create
additional applications in the [Service accounts](#service-accounts) section.

1. In the Okta Admin Console, go to **Applications** > **Applications** and
   click **Create App Integration**.

1. Select **OIDC - OpenID Connect** as the sign-in method and **Single-Page
   Application** as the application type. Click **Next**.

1. Configure the application:
   - **App integration name**: Enter a name (e.g., `Materialize`).
   - **Grant type**: Ensure **Authorization Code** is selected (PKCE is used
     automatically for single-page applications).
   - **Sign-in redirect URIs**: Enter
     `https://<your-console-domain>/auth/callback`. If you want to use the
     [CLI token flow](#get-a-token-using-cli-tools), also add
     `http://localhost:9876/callback`.
   - **Sign-out redirect URIs**: Optionally, enter
     `https://<your-console-domain>/account/login`.

1. Click **Save**.

1. On the application's **General** tab, note the **Client ID**.

   *Single-page applications use PKCE instead of a client secret. You do not
   need a client secret for the console application.*

1. Go to **Security** > **API** and note your **Issuer URI** from the
   authorization server you want to use (e.g.,
   `https://your-org.okta.com/oauth2/default`).

   **Custom domains:** When the authorization server **Issuer** is set to **Dynamic (based on Request Domain)**, Okta issues tokens whose `iss` claim uses your custom domain (for example, `https://sso.your-org.com/oauth2/default`) instead of the default Okta URL. Configure the `oidc_issuer` system parameter in Materialize to match that issuer value exactly.

1. Go to the **Assignments** tab and assign the users or groups that should have
   access to Materialize.

   When a user authenticates via SSO, Materialize uses a JWT claim to determine
   the role name. See [Mapping IdP users to Materialize roles](#mapping-idp-users-to-materialize-roles) for more details.

1. Configure the authorization server. In the Okta Admin Console, go to
   **Security** > **API** and click on the authorization server you want to
   use (e.g., **default**).

   1. On the **Settings** tab, note the **Issuer** URI. This is the value you
      will use for the `oidc_issuer` system parameter.

   1. Go to the **Scopes** tab and ensure the `openid` and `email` scopes
      exist (they are present by default).

   1. Go to the **Access Policies** tab. You need at least one policy with a
      rule that allows the grant types you plan to use:

      - **Authorization Code**: Required for the console login.
      - **Resource Owner Password**: Required for the
        [ROPC service account flow](#resource-owner-password-flow).
      - **Client Credentials**: Required for the
        [Client Credentials service account flow](#client-credentials-flow).

      To add or edit a rule:

      1. Click **Add New Access Policy** (or select an existing policy).
      1. Click **Add Rule** within the policy.
      1. Under **Grant type is**, check the grant types you need.
      1. Under **Assigned to**, select the clients (applications) this rule
         applies to.
      1. Click **Create Rule**.

**Microsoft Entra ID:**

1. In the [Azure portal](https://portal.azure.com), go to **Microsoft Entra
   ID** > **App registrations** and click **New registration**.

1. Configure the registration:
   - **Name**: Enter a name (e.g., `Materialize`).
   - **Supported account types**: Select the appropriate option for your
     organization (typically **Accounts in this organizational directory only**).
   - **Redirect URI**: Select **Single-page application (SPA)** and enter
     `https://<your-console-domain>/auth/callback`. After registration, you
     can add `http://localhost:9876/callback` under **Authentication** if you
     want to use the [CLI token flow](#get-a-token-using-cli-tools).

1. Click **Register**.

1. On the application's **Overview** page, note the **Application (client) ID**
   and the **Directory (tenant) ID**.

1. Go to **Certificates & secrets** > **New client secret**. Add a description
   and expiration, then click **Add**. Note the secret **Value**.

   *A client secret is not required for the console login (which uses
   authorization code with PKCE), but is needed if you plan to use the
   [Client Credentials flow](#client-credentials-flow) for service accounts.*

1. Construct your issuer URL using your tenant ID:

   ```
   https://login.microsoftonline.com/<tenant-id>/v2.0
   ```

1. Go to **Enterprise applications** > select your application > **Users and
   groups** and assign the users or groups that should have access to
   Materialize.

   When a user authenticates via SSO, Materialize uses a JWT claim to determine
   the role name. See [Mapping IdP users to Materialize roles](#mapping-idp-users-to-materialize-roles) for more details.

**Generic OIDC:**

1. In your identity provider, create a new OIDC **public** client application
   (single-page application type) with the **Authorization Code** grant type
   and **PKCE** support.

1. Set the redirect URI to `https://<your-console-domain>/auth/callback`. If
   you want to use the [CLI token flow](#get-a-token-using-cli-tools), also
   add `http://localhost:9876/callback`.

1. Note the **client ID** and **issuer URL** provided by your identity provider.
   The issuer URL is typically the base URL of your identity provider's OIDC
   discovery endpoint (without `/.well-known/openid-configuration`).

1. Ensure the `openid` scope is available.

1. Assign users or groups that should have access to Materialize.

   When a user authenticates via SSO, Materialize uses a JWT claim to determine
   the role name. See [Mapping IdP users to Materialize roles](#mapping-idp-users-to-materialize-roles) for more details.

> **Note:** Once you have configured your IdP, you will need the following values to [configure
> OIDC system parameters for Materialize](#step-3-configure-oidc-system-parameters):
> - The OIDC **issuer URL**
> - The **client ID** for the console application
> - If using service accounts, the client ID, client secret, and expected
>   audience for each service-account application

## Step 2. Enable OIDC authentication

To configure Self-Managed Materialize for OIDC authentication, update the
following fields:

| Resource | Configuration | Description
|----------|---------------| ------------
| Materialize CR | `spec.authenticatorKind` | Set to `Oidc` to enable OIDC authentication.
| Kubernetes Secret | `external_login_password_mz_system` | Specify the password for the `mz_system` user. Add `external_login_password_mz_system` to the Kubernetes Secret referenced in the Materialize CR's `spec.backendSecretName` field. The `mz_system` user **always** authenticates with a password. This user is required by the Materialize Operator for upgrades and serves as an emergency administrative account.
| ConfigMap | `mz-system-params` | Create an empty system parameter ConfigMap and reference it from the Materialize CR's `spec.systemParameterConfigmapName` field. You will populate it with your OIDC parameters in [Step 3](#step-3-configure-oidc-system-parameters).

The following example Kubernetes manifest includes configuration for OIDC
authentication:

```yaml {hl_lines="6-15 26 36-38"}
apiVersion: v1
kind: Namespace
metadata:
  name: materialize-environment
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: mz-system-params
  namespace: materialize-environment
data:
  # Create an empty system parameter configmap for later steps
  system-params.json: |
    {
    }
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
  environmentdImageRef: materialize/environmentd:v26.26.0 # Use v26.26.0 or later
  backendSecretName: materialize-backend
  authenticatorKind: Oidc
  requestRollout: 00000000-0000-0000-0000-000000000003 # Switching to Oidc requires a rollout
  systemParameterConfigmapName: mz-system-params # Adding a system parameter configmap requires a rollout
```

Apply the updated manifest to your Kubernetes cluster. See
[Upgrading](/self-managed-deployments/upgrading/#rollout-configuration) for
details on rollout configuration.

> **Warning:** Once enabled, ensure that the `authenticatorKind` field is set for any future version upgrades or rollouts of the Materialize CR. Having it undefined will reset `authenticationKind` to `None`.

## Step 3. Configure OIDC system parameters

Configure the OIDC system parameters to connect Materialize to your identity
provider. You can use either a
[ConfigMap](/self-managed-deployments/configuration-system-parameters/#configure-system-parameters-via-configmap)
or SQL commands, but it is strongly recommended to use a ConfigMap. See [Configure via Configmap](#configure-via-configmap) for more details.

### OIDC system parameters

| Parameter | Description | Required | Default |
|-----------|-------------|----------|---------|
| `oidc_issuer` | The OIDC issuer URL (e.g., `https://your-org.okta.com/oauth2/default`). Materialize uses this to discover the JWKS endpoint for token validation. | Yes | None |
| `oidc_audience` | A JSON array of expected audience values for token validation (e.g., `["your-client-id"]`). Use the **client ID from [Step 1](#step-1-configure-your-identity-provider)**. Materialize checks that the JWT's `aud` claim contains at least one of these values. **By default, this is empty, and audience validation is skipped.**| No | `[]` |
| `oidc_authentication_claim` | The JWT claim to use as the Materialize username. For ID tokens (human users), a common claim is `email`. For access tokens from the [Client Credentials flow](#client-credentials-flow), ensure this claim exists in the token. See [Mapping IdP users to Materialize roles](#mapping-idp-users-to-materialize-roles) for details. | No | `sub` |
| `console_oidc_client_id` | The OIDC client ID used by the web console for the authorization code flow. | For console login | Empty |
| `console_oidc_scopes` | Space-separated OIDC scopes requested by the web console when obtaining a token. Scopes control which claims are included in the token. The `openid` scope is required to obtain an ID token. Add `email` to include the `email` claim, or `profile` to include name claims. If `oidc_authentication_claim` references a claim like `email`, you must request the corresponding scope here. | For console login | Empty |

> **Warning:** When `oidc_audience` is empty, audience validation is skipped. This means
> **any** valid token from the same identity provider can authenticate to
> Materialize, including tokens issued for other applications. **Always set
> `oidc_audience` in production environments.**

### Configure via ConfigMap

In [Step 2](#step-2-enable-oidc-authentication), you already created an empty
`mz-system-params` ConfigMap. Now, populate that ConfigMap with your
OIDC parameters. At this point, your manifest should look like:

```yaml {hl_lines="9-13"}
apiVersion: v1
kind: ConfigMap
metadata:
  name: mz-system-params
  namespace: materialize-environment
data:
  system-params.json: |
    {
      "oidc_issuer": "YOUR_OIDC_ISSUER",
      "oidc_audience": "[\"YOUR_CLIENT_ID\"]",
      "oidc_authentication_claim": "email",
      "console_oidc_client_id": "YOUR_CLIENT_ID",
      "console_oidc_scopes": "openid email"
    }
```

> **Note:** This example sets `oidc_authentication_claim` to `email` rather than the default
> `sub`, so each user's role name comes from their `email` claim. Because the
> authentication claim references `email`, `console_oidc_scopes` includes the
> `email` scope to ensure that claim is present in the token.

Apply the updated ConfigMap to your Kubernetes cluster. The changes could take
up to a minute to take effect. For more
on configuring system parameters via a ConfigMap, see [System parameters
configuration](/self-managed-deployments/configuration-system-parameters/#configure-system-parameters-via-configmap).

### Configure via SQL

Alternatively, connect as `mz_system` and set the parameters using
`ALTER SYSTEM SET`. The `mz_system` user always authenticates with a password,
even when OIDC is enabled.

```mzsql
ALTER SYSTEM SET oidc_issuer = 'https://your-org.okta.com/oauth2/default';
ALTER SYSTEM SET oidc_audience = '["YOUR_CLIENT_ID"]';
ALTER SYSTEM SET oidc_authentication_claim = 'email';
ALTER SYSTEM SET console_oidc_client_id = 'YOUR_CLIENT_ID';
ALTER SYSTEM SET console_oidc_scopes = 'openid email';
```

## Step 4. Verify the configuration

1. Navigate to your Materialize Console. You should see an option to **Use
   single sign-on**.

   ![Materialize Console login screen showing the SSO sign-in
   option](/images/console/console-self-managed-sso.png "Materialize Console login screen
   with SSO option")

1. Sign in through your IdP. After successful authentication, you are redirected
   back to the Materialize Console.

1. To confirm which role you've signed in as via SSO, open the [SQL Shell](/console/sql-shell/) in the Materialize Console. In the welcome message, you should see the role name labeled under "User". This is derived from the `oidc_authentication_claim` claim in your identity token:

![Materialize Console Shell](/images/console/console.png "Materialize Console Shell")

## Connecting via SQL clients

To connect to Materialize using a SQL client like `psql`, you need an OIDC ID token.

If your client doesn't support OAuth, you can
create a role with a SQL password instead. See [SQL password authentication](#sql-password-authentication-recommended-for-non-oauth-clients).

### Get a token using CLI tools

You can fetch an
ID token from the command line using [`oauth2c`](https://github.com/cloudentity/oauth2c).
This is useful when configuring a non-interactive client like dbt or Terraform.

1. **Confirm `http://localhost:9876/callback` is registered as a redirect URI**
   on the console OIDC client (added in
   [Step 1](#step-1-configure-your-identity-provider)). `oauth2c` listens on
   this URL during the auth code exchange.

1. **Install `oauth2c`.** On macOS:

    ```shell
    brew install cloudentity/tap/oauth2c
    ```

    Other platforms: see the
    [`oauth2c` installation guide](https://github.com/cloudentity/oauth2c#installation).

1. **Run `oauth2c` to fetch the ID token:**

    ```shell
    oauth2c <ISSUER_URL> \
      --client-id <YOUR_CLIENT_ID> \
      --response-types code \
      --response-mode form_post \
      --grant-type authorization_code \
      --pkce \
      --scopes 'openid email' \
      --auth-method none \
      --silent | jq -r '.id_token'
    ```

    A browser window opens to complete the IdP login. After signing in,
    `oauth2c` prints the ID token to stdout.

ID tokens expire (typically within an hour). Re-run the command above when
your token expires.

### Get a token from the Materialize console

Clicking "Connect" in the Materialize console will provide you with an ID token that you can use to connect.

![Materialize Console connect instructions for OIDC](/images/console/console-connect-oidc.png "Materialize Console connect screen for OIDC")

### Connect with psql

Use the ID token as your password:

```shell
PGPASSWORD="<your-id-token>" \
psql -h <materialize-host> -p 6875 -U <username> materialize
```

Replace `<username>` with the value of the authentication claim in your JWT
(e.g., your email address if `oidc_authentication_claim` is set to `email`).

> **Note:** Materialize validates the token at **connection time only**. Once a connection
> is established, it persists until disconnected, regardless of token expiry.

## Provisioning roles

### Mapping IdP users to Materialize roles

Each user or service account that authenticates via OIDC maps to a single
Materialize database role. When a user authenticates into Materialize, their role name is the value of the JWT claim keyed by `oidc_authentication_claim`.

For example, if `oidc_authentication_claim` is set to `email` and a user authenticates with the following JWT:

```json
{
  "sub": "auth0|abc123",
  "email": "alice@your-org.com",
  "name": "Alice",
  "iat": 1516239022
}
```

Their role name will be `alice@your-org.com`.

If a user logs in and no matching role exists, Materialize auto-provisions one,
as described in the next section.

### Auto-provisioning roles

When a user signs in and no role matching their `oidc_authentication_claim`
value exists, Materialize **automatically creates** a role for them.

Auto-provisioned roles:
- Have default privileges only.
- Must be granted additional privileges through
  [RBAC](/security/self-managed/access-control/manage-roles/).
- Are not automatically removed when the user is removed from the IdP. See
  [De-provisioning users](#de-provisioning-users) for cleanup instructions.

#### Auditing auto-provisioned roles

To view which roles were auto-provisioned via OIDC, query `mz_audit_events`:

```mzsql
SELECT details
FROM mz_audit_events
WHERE event_type = 'create' AND object_type = 'role' AND details ->> 'auto_provision_source' = 'oidc'
ORDER BY occurred_at DESC;
```

Roles created through OIDC authentication will have `auto_provision_source` set to
`oidc`.

### Pre-provisioning roles

An administrator can create roles before users login, rather than rely on
auto-provisioning. To pre-provision a role, connect as a superuser and create
the role with a name matching the expected JWT claim value:

```mzsql
CREATE ROLE "alice@your-org.com" WITH LOGIN;
```

Like auto-provisioned roles, pre-provisioned roles start with default privileges
only and must be granted additional privileges through
[RBAC](/security/self-managed/access-control/manage-roles/).

## Service accounts

For machine-to-machine access, you have three options:

- [SQL password authentication](#sql-password-authentication-recommended-for-non-oauth-clients):
  for clients that don't support OAuth flows.
- [Resource Owner Password flow](#resource-owner-password-flow): for service
  accounts that authenticate against your IdP with a username and password.
- [Client Credentials flow](#client-credentials-flow): for service accounts
  that authenticate against your IdP without a user context.

### SQL password authentication (recommended for non-OAuth clients)

Even with OIDC enabled, Materialize still accepts SQL password authentication.
This is required for clients that don't support OAuth flows. The simplest way to
give such a service or application access is to create a role with a SQL
password.

1. As a user with the `CREATEROLE` privilege, create the role with a password:

    ```mzsql
    CREATE ROLE "svc-dbt" WITH LOGIN PASSWORD 'a-strong-password';
    ```

1. Grant the privileges this service account needs. See
   [Manage database roles](/security/self-managed/access-control/manage-roles/)
   for the full privilege model.

1. Connect using the password directly:

    ```shell
    PGPASSWORD="a-strong-password" \
    psql -h <materialize-host> -p 6875 -U svc-dbt materialize
    ```

For dbt-specific setup, see [dbt connection profiles](/manage/dbt/get-started/).
For Terraform, see [Terraform: get started](/manage/terraform/get-started/).

### Resource Owner Password flow

Use this approach when you need a service account that authenticates with a
username and password to obtain an ID token.

**Okta:**

1. In the Okta Admin Console, go to **Applications** > **Applications** and
   click **Create App Integration**.

1. Select **OIDC - OpenID Connect** as the sign-in method and **Native
   Application** as the application type. Click **Next**.

1. Configure the application:
   - **App integration name**: Enter a name (e.g., `Materialize ROPC`).
   - **Grant type**: Enable **Resource Owner Password**.

1. Click **Save** and note the **Client ID** and **Client Secret**.

1. Go to the **Assignments** tab and assign the service account user.

1. Ensure your authorization server's access policy includes a rule that
   allows the **Resource Owner Password** grant type for this application.
   See the authorization server setup in
   [Step 1](#step-1-configure-your-identity-provider).

1. In Okta, create a new user to serve as the service account (e.g.,
   `svc-materialize@your-org.com`).

   *The Resource Owner Password flow does not support MFA in Okta. The service
   account user must not have MFA enabled.*

1. Fetch an ID token:

   ```shell
   curl -X POST https://your-org.okta.com/oauth2/default/v1/token \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -H "Accept: application/json" \
     --data-urlencode "grant_type=password" \
     --data-urlencode "username=svc-materialize@your-org.com" \
     --data-urlencode "password=YOUR_SERVICE_ACCOUNT_PASSWORD" \
     --data-urlencode "scope=openid email" \
     --data-urlencode "client_id=YOUR_ROPC_CLIENT_ID" \
     --data-urlencode "client_secret=YOUR_ROPC_CLIENT_SECRET"
   ```

1. Extract the `id_token` from the JSON response and use it to connect:

   ```shell
   PGPASSWORD="<id-token>" \
   psql -h <materialize-host> -p 6875 -U svc-materialize@your-org.com materialize
   ```

**Microsoft Entra ID:**

1. In the [Azure portal](https://portal.azure.com), go to **Microsoft Entra
   ID** > **App registrations** and click **New registration**. Create a
   dedicated registration for this flow rather than reusing the console
   application from [Step 1](#step-1-configure-your-identity-provider).

1. Configure the registration:
   - **Name**: Enter a name (e.g., `Materialize ROPC`).
   - **Supported account types**: Select the appropriate option for your
     organization.

1. Click **Register**.

1. Go to **Authentication** and set **Allow public client flows** to **Yes**.
   This is required for the Resource Owner Password flow.

1. On the application's **Overview** page, note the **Application (client) ID**
   and the **Directory (tenant) ID**.

1. Go to **Certificates & secrets** > **New client secret**. Add a description
   and expiration, then click **Add**. Note the secret **Value**.

1. Create a new user to serve as the service account, then assign it to this
   application under **Enterprise applications** > **Users and groups**.

1. Fetch an ID token:

   ```shell
   curl -X POST https://login.microsoftonline.com/<tenant-id>/oauth2/v2.0/token \
     -H "Content-Type: application/x-www-form-urlencoded" \
     --data-urlencode "grant_type=password" \
     --data-urlencode "username=svc-materialize@your-org.com" \
     --data-urlencode "password=YOUR_SERVICE_ACCOUNT_PASSWORD" \
     --data-urlencode "scope=openid email" \
      --data-urlencode "client_id=YOUR_CLIENT_ID"
     --data-urlencode "scope=openid" \
     --data-urlencode "client_id=YOUR_CLIENT_ID" \
     --data-urlencode "client_secret=YOUR_CLIENT_SECRET"
   ```

1. Extract the `id_token` from the JSON response and use it to connect:

   ```shell
   PGPASSWORD="<id-token>" \
   psql -h <materialize-host> -p 6875 -U svc-materialize@your-org.com materialize
   ```

**Generic OIDC:**

1. Create a service account user in your identity provider.

1. Assign the service account to your Materialize application.

1. Enable the Resource Owner Password Credentials grant for your application.

1. Fetch an ID token from your IdP's token endpoint:

   ```shell
   curl -X POST https://your-idp.com/oauth2/token \
     -H "Content-Type: application/x-www-form-urlencoded" \
     --data-urlencode "grant_type=password" \
     --data-urlencode "username=svc-materialize@your-org.com" \
     --data-urlencode "password=YOUR_SERVICE_ACCOUNT_PASSWORD" \
     --data-urlencode "scope=openid email" \
     --data-urlencode "client_id=YOUR_CLIENT_ID" \
     --data-urlencode "client_secret=YOUR_CLIENT_SECRET"
   ```

1. Extract the `id_token` from the JSON response and use it to connect:

   ```shell
   PGPASSWORD="<id-token>" \
   psql -h <materialize-host> -p 6875 -U svc-materialize@your-org.com materialize
   ```

### Client Credentials flow

Use this approach to treat an IdP client as a service account. This is useful
for automated systems that do not have a user context.

> **Note:** `oidc_audience` is an array of values. Before running the `ALTER SYSTEM SET
> oidc_audience` examples below, check the current value with `SHOW oidc_audience;`
> and **append** the new audience rather than overwriting it. Otherwise you may
> remove the console's audience or other configured values.

**Okta:**

1. In the Okta Admin Console, go to **Applications** > **Applications** and
   click **Create App Integration**.

1. Select **OIDC - OpenID Connect** as the sign-in method and **Web
   Application** as the application type. Click **Next**.

1. Configure the application:
   - **App integration name**: Enter a name (e.g., `Materialize Service Account 1`).
   - **Grant type**: Enable **Client Credentials** (deselect other grant
     types).

1. Click **Save** and note the **Client ID** and **Client Secret**.

1. Ensure your authorization server's access policy includes a rule that
   allows the **Client Credentials** grant type for this application.
   See the authorization server setup in
   [Step 1](#step-1-configure-your-identity-provider).

1. **Configure a custom claim for the service account identity.**

   The `oidc_authentication_claim` setting is global — it applies to both
   human users (ID tokens) and service accounts (access tokens). If set to
   `email`, human users get readable role names (e.g., `alice@your-org.com`),
   but Client Credentials access tokens do not include an `email` claim by
   default. If set to `sub`, Client Credentials tokens work, but human users
   lose email-based role names and get opaque subject IDs instead.

   To solve this, create a custom claim (e.g., `sql_username`) in your
   authorization server that maps to `user.email` for ID tokens and to a
   configured value for access tokens:

   1. In the Okta Admin Console, go to **Security** > **API** and select your
      authorization server.

   1. Go to the **Claims** tab and click **Add Claim**.

   1. Configure the claim for **ID tokens** (human users):
      - **Name**: `sql_username`
      - **Include in token type**: **ID Token** (always).
      - **Value type**: **Expression**.
      - **Value**: `appuser.email`
      - **Include in**: **Any scope**.

   1. Click **Create**, then click **Add Claim** again.

   1. Configure the claim for **access tokens** (service accounts):
      - **Name**: `sql_username`
      - **Include in token type**: **Access Token** (always).
      - **Value type**: **Expression**.
      - **Value**: `app.sub`
      - **Include in**: **Any scope**.

   1. Click **Create**.

   1. Set the authentication claim in Materialize:

      ```mzsql
      ALTER SYSTEM SET oidc_authentication_claim = 'sql_username';
      ```

   *If you have multiple service accounts using Client Credentials, each needs
   its own Okta application.*

1. Fetch an access token:

   ```shell
   curl -X POST https://your-org.okta.com/oauth2/default/v1/token \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -H "Accept: application/json" \
     --data-urlencode "grant_type=client_credentials" \
     --data-urlencode "scope=openid" \
     --data-urlencode "client_id=YOUR_SERVICE_CLIENT_ID" \
     --data-urlencode "client_secret=YOUR_SERVICE_CLIENT_SECRET"
   ```

1. Ensure `oidc_audience` includes the expected audience value for tokens
   from your authorization server. In Okta, the `aud` claim is set to the
   authorization server's audience (configured in **Security** > **API** >
   your auth server > **Settings**), not the client ID. For the default
   authorization server, this is typically `api://default`:

   ```mzsql
   -- Make sure to add to the array if already set
   ALTER SYSTEM SET oidc_audience = '["api://default"]';
   ```

1. Extract the `access_token` from the JSON response and use it to connect:

   ```shell
   PGPASSWORD="<access-token>" \
   psql -h <materialize-host> -p 6875 -U <service-account-name> materialize
   ```

   The `<service-account-name>` must match the value of the `sql_username`
   claim in the access token (e.g., `svc-my-service`).

**Microsoft Entra ID:**

1. In the [Azure portal](https://portal.azure.com), go to **Microsoft Entra
   ID** > **App registrations** and click **New registration**.

1. Configure the registration:
   - **Name**: Enter a name (e.g., `Materialize Service Account`).
   - **Supported account types**: Select the appropriate option for your
     organization.

1. Click **Register**.

1. On the application's **Overview** page, note the **Application (client) ID**.

1. Go to **Certificates & secrets** > **New client secret**. Add a description
   and expiration, then click **Add**. Note the secret **Value**.

1. Fetch an access token:

   ```shell
   curl -X POST https://login.microsoftonline.com/<tenant-id>/oauth2/v2.0/token \
     -H "Content-Type: application/x-www-form-urlencoded" \
     --data-urlencode "grant_type=client_credentials" \
     --data-urlencode "scope=YOUR_SERVICE_CLIENT_ID/.default" \
     --data-urlencode "client_id=YOUR_SERVICE_CLIENT_ID" \
     --data-urlencode "client_secret=YOUR_SERVICE_CLIENT_SECRET"
   ```

1. Ensure `oidc_audience` includes the expected audience value for Client
   Credentials tokens. In Entra, the `aud` claim is determined by the `scope`
   parameter in the token request. When using `YOUR_SERVICE_CLIENT_ID/.default`,
   the audience is the service client ID:

   ```mzsql
   -- Make sure to add to the array if already set
   ALTER SYSTEM SET oidc_audience = '["YOUR_SERVICE_CLIENT_ID"]';
   ```

1. Extract the `access_token` from the JSON response and use it to connect:

   ```shell
   PGPASSWORD="<access-token>" \
   psql -h <materialize-host> -p 6875 -U <service-account-name> materialize
   ```

   The `<service-account-name>` must match the value of the authentication
   claim in the access token.

**Generic OIDC:**

1. In your identity provider, create a new OIDC client application with the
   **Client Credentials** grant type.

1. Note the **Client ID** and **Client Secret**.

1. Fetch an access token from your IdP's token endpoint:

   ```shell
   curl -X POST https://your-idp.com/oauth2/token \
     -H "Content-Type: application/x-www-form-urlencoded" \
     --data-urlencode "grant_type=client_credentials" \
     --data-urlencode "scope=openid" \
     --data-urlencode "client_id=YOUR_SERVICE_CLIENT_ID" \
     --data-urlencode "client_secret=YOUR_SERVICE_CLIENT_SECRET"
   ```

1. Ensure `oidc_audience` includes the expected audience value for Client
   Credentials tokens. Check the `aud` claim in the token issued by your IdP
   to determine the correct value:

   ```mzsql
   -- Make sure to add to the array if already set
   ALTER SYSTEM SET oidc_audience = '["YOUR_AUDIENCE_VALUE"]';
   ```

1. Extract the `access_token` from the JSON response and use it to connect:

   ```shell
   PGPASSWORD="<access-token>" \
   psql -h <materialize-host> -p 6875 -U <service-account-name> materialize
   ```

   The `<service-account-name>` must match the value of the authentication
   claim in the access token.

## De-provisioning users

When a user is removed from the identity provider, they can no longer
authenticate to Materialize because their JWT tokens will no longer be valid.
However, the corresponding Materialize role is **not automatically deleted**.
This is intentional to avoid disrupting ownership of database objects.

To remove the role after de-provisioning:

```mzsql
-- Reassign owned objects if needed
REASSIGN OWNED BY <username> TO <new-owner>;
-- Then drop the role
DROP ROLE <username>;
```

## Troubleshooting

| Symptom | Possible cause | Resolution |
|---------|---------------|------------|
| Console does not show SSO login option | `console_oidc_client_id` and `console_oidc_scopes` are not set | Set `console_oidc_client_id` to your OIDC client ID |
| SSO login redirects fail | Incorrect IdP configuration | Verify the redirect URI is set to `https://<your-console-domain>/auth/callback` and the IdP application type is set as a Single Page Application |
| SSO login redirects to login page | Materialize database is rejecting the token | Verify that the token generated by your IdP includes the required claims.
| environmentd fails to upgrade | external_login_password_mz_system not set | Ensure the external_login_password_mz_system is configured |
| "Invalid token" error on psql connection | Wrong or expired JWT token | Obtain a fresh token; verify `oidc_issuer` matches the token's `iss` claim |
| "Audience validation failed" | Client ID not in `oidc_audience` | Add the client ID to `oidc_audience`: `ALTER SYSTEM SET oidc_audience = '["your-client-id"]'` |
| User gets wrong role name | `oidc_authentication_claim` set to wrong claim | Verify the claim name and check the JWT contents (e.g., using [jwt.io](https://jwt.io)) |

To inspect the current OIDC configuration, login as `mz_system` and run the following SQL:

```mzsql
SHOW oidc_issuer;
SHOW oidc_audience;
SHOW oidc_authentication_claim;
SHOW console_oidc_client_id;
SHOW console_oidc_scopes;
```

## FAQ

### What happens during a blue/green deployment?

OIDC configuration (system parameters) and auto-provisioned roles are persisted
in the Materialize catalog. Blue/green deployments do not affect SSO
configuration or user roles. No additional action is required.

### What happens if I tear down my Materialize environment?

Role data and OIDC configuration are stored in the Materialize catalog, which is
persisted in your configured object storage (e.g., S3). If you delete the
Materialize instance in Kubernetes and re-apply the Materialize CR, the instance
rehydrates from the persisted catalog, recovering all roles and configuration.

If the underlying object storage is also deleted, the catalog and all role data
are lost. Use your cloud provider's disaster recovery policies to protect against this scenario.

## See also

- [Migrate to SSO](/security/self-managed/sso-migration/)
- [Authentication](/security/self-managed/authentication/)
- [Access control](/security/self-managed/access-control/)
- [Manage roles](/security/self-managed/access-control/manage-roles/)
- [System parameters configuration](/self-managed-deployments/configuration-system-parameters/)
- [Materialize CRD Field Descriptions](/installation/appendix-materialize-crd-field-descriptions/)


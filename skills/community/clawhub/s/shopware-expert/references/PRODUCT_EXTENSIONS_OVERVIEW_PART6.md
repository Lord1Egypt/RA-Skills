# PRODUCT EXTENSIONS OVERVIEW

Compiled excerpts from the Shopware Developer Documentation snapshot. Prefer live docs at [developer.shopware.com](https://developer.shopware.com/) when in doubt.

---

## Organizations
**Source:** [products/paas/shopware/fundamentals/organization.md](https://developer.shopware.com/docs/products/paas/shopware/fundamentals/organization.md)  
# Organizations

An organization serves as the top-level container representing a company or an entity in Shopware PaaS Native. It acts as the primary organizational unit that encompasses all resources, projects, and users associated with a particular business entity. By default, the initial admin user is added to an Organization and can further add more users.

To create additional organizations via CLI, run;

```sh
sw-paas organization create
```

## Organization Members

Organization members are users who have been granted access to an organization and its resources.

### Roles

Organization members can be assigned different roles that determine their level of access and permissions:

* `read-only`: Access to projects and applications. Only actions allowed are `get` and `list`.
* `developer`: Access to projects and applications. All actions are allowed.
* `project-admin`: Access to projects and applications. All actions are allowed.
* `account-admin`: Access to account management. Actions for managing users are allowed.

### User Management

If you already have the `project-admin` role and wish to add additional users to your organization, they can share their **user ID (sub-id)** with you. You can instruct them to retrieve it using the following command:

```sh
sw-paas account whoami --output json
```

Or, if they have `jq` installed for easier parsing:

```sh
sw-paas account whoami --output json | jq ".sub"
```

Once you receive their `sub` (subject ID), you can proceed to add them to your organization with the appropriate role.

```sh
sw-paas organization user add
```

To remove a user from the organization:

```sh
sw-paas organization user remove
```

---

---

## Projects
**Source:** [products/paas/shopware/fundamentals/project.md](https://developer.shopware.com/docs/products/paas/shopware/fundamentals/project.md)  
# Projects

Projects represent a codebase in a GitHub, Bitbucket, or GitLab repository that is deployed to Shopware PaaS Native. Projects can contain many applications.

## Creating a New Project

Initialize a new project in your organization by specifying its name, repository, and type.

```sh
sw-paas project create
```

Ensure that Shopware PaaS Native has access to the repository by following [this guide](../guides/setting-up-repository-access.md).

## List All Projects

Displays all projects associated with your user or organization, along with key metadata such as project name, type, and repository.

**Usage:**

```sh
sw-paas project list
```

---

---

## Secrets
**Source:** [products/paas/shopware/fundamentals/secrets.md](https://developer.shopware.com/docs/products/paas/shopware/fundamentals/secrets.md)  
# Secrets

Shopware PaaS Native allows you to securely store and retrieve sensitive information like passwords or API tokens.

Secrets stored in Vault are reusable, which means that you can reuse a secret value in different applications. Secrets are global to the organization, so all applications can access the same values.

## Creating a New Secret

A secret is composed of a type, a key, and a value. Once created, it is assigned a unique `secret-id`, which is required for retrieving or deleting the secret.

The supported types are `env`, `buildenv`, and `ssh`. `env` is available at runtime in the application, `buildenv` is accessible during build processes, and `ssh` keys are for secure connections.

To create a secret, use the following command:

```sh
sw-paas vault create
```

## Listing all Vault secrets

```sh
sw-paas vault list
```

## Retrieving a Secret

To retrieve an existing secret from the Vault, you **must specify the secret ID** using the `--secret-id` flag:

```sh
sw-paas vault get --secret-id SECRET-ID
```

***

## Deleting a Secret

To delete a secret from the Vault, also use the `--secret-id` flag:

```sh
sw-paas vault delete --secret-id SECRET-ID
```

::: warning
Deleting a secret is permanent. Ensure the secret is no longer in use before removing it.
:::

---

---

## Get Started with Shopware PaaS Native
**Source:** [products/paas/shopware/get-started.md](https://developer.shopware.com/docs/products/paas/shopware/get-started.md)  
# Get Started with Shopware PaaS Native

This section will introduce how to get started with Shopware PaaS Native, including setting up the CLI, preparing your code base, and providing a step-by-step guide to creating your first application.

---

---

## Prerequisites
**Source:** [products/paas/shopware/get-started/cli.md](https://developer.shopware.com/docs/products/paas/shopware/get-started/cli.md)  
The Shopware PaaS Native CLI makes it easy to manage your shops and resources in the cloud.

## Prerequisites

Before you start, you'll need a Shopware account. Shopware uses AWS Cognito for identity management. Currently, you must be invited to join our platform before you can access any resources.

Once your organization is onboarded to the Shopware Business Platform (SBP) and users are added to Shopware PaaS Native, the first user gets the admin role. This admin can then assign roles to other users in your organization.

For more on managing users, see our [Organization Guide](../fundamentals/organization.md).

## Installation

To install the CLI, run:

```sh
curl -L https://install.sw-paas-cli.shopware.systems | sh
```

The installation script will download the latest version (or specified version) from GitHub releases, install the binary to ~/.sw-paas/bin/sw-paas and add the installation directory to your PATH (if not already present). You can set `SW_PAAS_DIR` environment variable to customize the installation directory, which defaults to `~/.sw-paas`

To install a specific version:

```sh
curl -L https://install.sw-paas-cli.shopware.systems | sh -s 0.0.30
```

:::info
Soon, you'll also be able to install the CLI using popular package managers.
:::

## Authentication

After installing, you'll need to log in to use the CLI.

Run the following command to open a browser window and log in to your Shopware PaaS Native account. Your authentication token will be saved automatically.

```sh
sw-paas auth
```

For more details on managing your account and creating machine tokens for CI/CD, see the [account command](../fundamentals/account) guide.

## Authorization

To access resources, you need the right roles in your organization. Only users with the **Account Admin** role can assign roles to others.

To check your current role:

```sh
sw-paas account whoami
```

If you are an Account Admin and want to add more users, ask the new user to get their user ID:

```sh
sw-paas account whoami --output json
```

Add the user to your organization and assign a role:

```sh
sw-paas account user add --sub "<user-id of the new user>"
```

## Available commands

To view all available commands with supported flags:

```sh
sw-paas
```

## Need help or found a bug?

If you find a bug or have feedback, please let us know in our [issue tracker](https://github.com/shopware/sw-paas/issues).

---

---

## Prepare Shopware codebase
**Source:** [products/paas/shopware/get-started/prepare-codebase.md](https://developer.shopware.com/docs/products/paas/shopware/get-started/prepare-codebase.md)  
# Prepare Shopware codebase

## Prerequisite

**macOS** and **Linux** are the recommended environments for local development. On **Windows**, it's advisable to use [Docker](https://www.youtube.com/watch?v=5XYFRDlT9WI) or **WSL2** (Windows Subsystem for Linux) for a consistent development experience.

To develop and customize your Shopware project effectively, certain operations must be performed in a local environment. This is especially important for tasks that directly interact with the file system, such as Installing or upgrading plugins, adjusting system-level configuration (e.g., language, environment) or applying custom code changes.

Plugin management via the Shopware Administration interface is **not supported**. This is because the platform operates in a **high-availability (HA), clustered setup**, where all application instances must remain **stateless and identical**.

To ensure consistency and reproducibility across deployments, plugins must be installed or updated **via Composer** as part of the project’s codebase. Follow the official guidance on [managing extensions with Composer](https://developer.shopware.com/docs/guides/hosting/installation-updates/extension-managment.html#installing-extensions-with-composer).

Additionally, before installation, verify that each plugin supports **S3-based storage**, as not all extensions are compatible with external file systems.

## How to uninstall plugins

To uninstall plugins in the PaaS environment, use the [Deployment Helper](../../../../guides/hosting/installation-updates/deployments/deployment-helper.html#removal-of-extensions) which provides a streamlined process for extension management.

The uninstallation process involves two steps:

1. **Set the extension to remove**: Configure the extension state as `remove` in your `.shopware-project.yml` file and deploy the changes to uninstall the extension.

2. **Remove from source code**: After the deployment, remove the extension from your source code and deploy again.

For detailed instructions and configuration examples, refer to the [Removal of extensions](../../../../guides/hosting/installation-updates/deployments/deployment-helper.html#removal-of-extensions) section in the Deployment Helper documentation.

## Generating the required files

Whether you're starting from scratch or working with an existing Shopware project, the following steps will ensure your setup is ready for deployment on Shopware PaaS Native.

### For New Projects

To create a new Shopware project from the official production template, run:

```sh
composer create-project shopware/production <folder-name>
```

Then navigate into the project directory and proceed with the next steps.

### For Existing Projects

If you're working with an already created Shopware project, simply navigate into the project directory:

```sh
cd <your-project-folder>
```

Ensure the required Kubernetes metadata package is installed to enable compatibility with the [Shopware Operator](https://github.com/shopware/shopware-operator):

```sh
composer require shopware/k8s-meta --ignore-platform-reqs
```

:::info
The `--ignore-platform-reqs` flag ensures that all necessary recipes are installed, even if your local PHP version differs from the required platform version.
:::

This package installs essential configuration files, including those required for deploying your shop via the Shopware Operator. After installation, verify that the file `config/packages/operator.yaml` has been created.

### Create the `application.yaml` File

At the root of your project, create a file named `application.yaml`. This file defines key deployment parameters, such as the PHP version and any environment-specific configuration needed for your shop.

#### Basic Example

```yaml
app:
  php:
    version: "8.3"
  environment_variables: []
services:
  mysql:
    version: "8.0"
  opensearch:
    enabled: false
```

#### Advanced Example (with Custom Environment Variables)

```yaml
app:
  php:
    version: "8.3"
  environment_variables:
    - name: INSTALL_LOCALE
      value: fr-FR
      scope: RUN # Supports RUN or BUILD
services:
  mysql:
    version: "8.0"
  opensearch:
    enabled: false
```

## Hooks Configuration

Shopware PaaS Native uses the deployment helper to execute custom hooks for your application. To see how these hooks are configured, refer to the [Deployment Helper documentation](../../../../guides/hosting/installation-updates/deployments/deployment-helper#configuration).

---

---

## Quickstart
**Source:** [products/paas/shopware/get-started/quickstart.md](https://developer.shopware.com/docs/products/paas/shopware/get-started/quickstart.md)  
# Quickstart

Get started with Shopware PaaS Native in just a few minutes. This guide will walk you through the essential steps to deploy your first Shopware application.

## Prerequisites

Before you begin, ensure you have:

* A Git repository with your Shopware application prepared for PaaS. You can follow [this guide](./index.md) for preparation.
* Access to the terminal / command line
* Git installed on your local machine. You can follow [this guide](https://github.com/git-guides/install-git).

## Step 1: Install the PaaS CLI

First, install the Shopware PaaS Native CLI tool:

```sh
curl -L https://install.sw-paas-cli.shopware.systems | sh
```

Verify the installation:

```sh
sw-paas version
```

## Step 2: Connect Your Git Repository

To connect your private git repository with our backend, you need to add an SSH key to your repository. This key is used to clone your repository and deploy your code to the cluster.

### 2.1 Generate and Store SSH Key

Run the following command to create an SSH key and store it securely in your organization's vault:

```sh
sw-paas vault create --type ssh
```

This command will generate a new SSH key pair and store the private key securely.

::: info
Organization vs Project Level

* **Organization level**: All projects can use the key
* **Project level**: Only a specific project can use the key (add `--project` flag)

Project-level keys override organization-level keys.
:::

### 2.2 Add Public Key to Repository

After running the command, the CLI will display the generated public key. Copy this public key and add it to your repository settings:

* **GitHub**: Go to `Settings` → `Deploy keys` → `Add deploy key`
* **GitLab**: Go to `Settings` → `Repository` → `Deploy Keys`
* **Bitbucket**: Go to `Repository settings` → `Access keys`

Ensure the key has **read access** to the repository.

## Step 3: Create Your First Project

Initialize a new PaaS project:

```sh
sw-paas project create --name "my-shopware-app" --repository "git@github.com:username/repo.git"
```

## Step 4: Create and deploy an Application Instance of the project

Create your application:

```sh
sw-paas application create
```

Then, deploy your application:

```sh
sw-paas application deploy create
```

Monitor the deployment progress:

```sh
sw-paas watch
```

---

---

## Guides
**Source:** [products/paas/shopware/guides.md](https://developer.shopware.com/docs/products/paas/shopware/guides.md)  
# Guides

This section provides a collection of common guides and best practices for working with Shopware PaaS Native. Here, you will find step-by-step instructions, helpful tips, and resources to assist you in setting up, configuring, and optimizing your Shopware PaaS Native environment.

---

---

## Enable OpenSearch
**Source:** [products/paas/shopware/guides/opensearch.md](https://developer.shopware.com/docs/products/paas/shopware/guides/opensearch.md)  
## Enable OpenSearch

To use OpenSearch with your Shopware instance, add the `opensearch` service to your `application.yaml` file as follows:

```yaml
services:
  opensearch:
    enabled: true
```

A complete example would look like this:

```yaml
app:
  php:
    version: "8.3"
  environment_variables:
    - name: INSTALL_LOCALE
      value: fr-FR
      scope: RUN # Supports RUN or BUILD
services:
  mysql:
    version: "8.0"
  opensearch:
    enabled: true
```

Once that is done, commit this change and push it to your git repository. Now you need to update your application, see [here](../fundamentals/applications.md#update-your-application).

## Post-enablement actions

After you enable OpenSearch and update your application, you need to index your application. You can do this as follows:

* Open an interactive session: `sw-paas exec --new`
* Once the exec session is ready, run the following command: `bin/console dal:refresh:index --use-queue`

---

---

## Guide: Using the Shopware PaaS Vault
**Source:** [products/paas/shopware/guides/secrets-vault-guide.md](https://developer.shopware.com/docs/products/paas/shopware/guides/secrets-vault-guide.md)  
# Guide: Using the Shopware PaaS Vault

This guide explains how to securely manage secrets using the Shopware PaaS CLI Vault. You’ll learn how to create, retrieve, and delete secrets — including SSH keys — with practical examples.

## What is the Vault?

The Vault is a secure, centralized location to store sensitive data such as:

* Environment variables
* Build-time secrets
* SSH keys for accessing private Git repositories

Secrets stored in the Vault are reusable across all applications in your organization.

## Secret Types

| Type       | Description                                      |
|------------|--------------------------------------------------|
| `env`      | Runtime environment variables for your app       |
| `buildenv` | Build-time environment variables                 |
| `ssh`      | SSH keys for secure Git access                   |

## Creating a Secret

To create a secret interactively:

```sh
sw-paas vault create
```

You will be prompted to select a secret type, key, and value.

### Creating an SSH Key Secret

To generate and store an SSH key for deployments:

```sh
sw-paas vault create --type ssh
```

After generation, the CLI will output the public key. Add this to your Git hosting provider (e.g., GitHub under **Deploy Keys**).

## Retrieving a Secret

Secrets are accessed by their unique `secret-id`. You can retrieve a secret using:

```sh
sw-paas vault get --secret-id SECRET-ID
```

To list all secrets and find their IDs:

```sh
sw-paas vault list
```

## Deleting a Secret

To delete a secret from the Vault:

```sh
sw-paas vault delete --secret-id SECRET-ID
```

::: warning
This action is permanent. Ensure the secret is not in use before deleting it.
:::

## Example Workflow: Using SSH Keys

### Step 1: Generate and store an SSH key

```sh
sw-paas vault create --type ssh
```

### Step 2: Add the public key to GitHub as a deploy key

Navigate to your GitHub repository → Settings → Deploy Keys → Add Key.

### Step 3: List all secrets to verify

```sh
sw-paas vault list
```

### Step 4: Retrieve a specific secret

```sh
sw-paas vault get --secret-id ssh-abc123xyz
```

### Step 5: Delete a secret (when no longer needed)

```sh
sw-paas vault delete --secret-id ssh-abc123xyz
```

## Default Secrets & Ownership

The Shopware PaaS Vault contains both system-managed and user-managed secrets. Understanding the difference helps you identify which secrets you can manage and which are maintained by the platform.

### System-Managed vs. User-Managed Secrets

**System-managed secrets** are automatically created and maintained by Shopware PaaS for internal operations. While these secrets are visible when you run `sw-paas vault list`, they should not be modified or deleted as they are critical for platform functionality.

**User-managed secrets** are created by you for your application's specific needs, such as API tokens, database credentials, or SSH keys for private repositories.

### Common Secrets Reference

| Secret Name | Description | Managed By | Editable by User | Notes |
|-------------|-------------|------------|------------------|-------|
| `STOREFRONT_CREDENTIALS` | Internal storefront credentials | System | No | **Do not delete** - Required for storefront functionality |
| `GRAFANA_CREDENTIALS` | Grafana dashboard login credentials | System | No | **Do not delete** - Needed for `sw-paas open grafana` |
| `NATS_USER_CREDENTIALS` | NATS messaging user credentials | System | No | **Do not delete** - Required for internal messaging |
| `STOREFRONT_PROXY_KEY` | Storefront proxy authentication | System | No | **Do not delete** - Required for routing |
| `SSH_PRIVATE_KEY` | Deploy SSH key for repository access | User | Yes | See [SSH key workflow](#example-workflow-using-ssh-keys) |
| `SHOPWARE_PACKAGES_TOKEN` | Token for accessing Shopware packages | User | Yes | Watch for typo variants (e.g. missing underscore: `SHOPWAREPACKAGES_TOKEN`) |

::: info
System-managed secrets use the same retrieval mechanism as user-managed secrets, which is why they appear in your vault list. This is intentional to provide transparency into the credentials your environment is using.
:::

### Understanding Organization-wide Secrets

The `sw-paas vault list` command shows all secrets stored in your organization’s Vault. Because secrets are organization-global and reusable, the same secret values can be referenced by multiple applications using the same secret name.

If multiple applications in your organization use a secret with the same name, they are all referring to the same underlying Vault secret, not separate per-application copies.

This means you manage each secret once at the organization level and then reference it from the applications that need it.

## Permissions & Behavior

::: danger
**Do not delete system-managed secrets.** Deleting secrets like `STOREFRONT_CREDENTIALS`, `GRAFANA_CREDENTIALS`, `NATS_USER_CREDENTIALS`, or `STOREFRONT_PROXY_KEY` will cause platform outages and break critical functionality.
:::

### System-Managed Secret Restrictions

System-managed secrets must be treated as read-only and must not be modified or deleted. The platform does not technically prevent you from changing or removing these secrets, but doing so is unsupported and will break critical platform functionality. They are essential for:

* Storefront operations and routing
* Monitoring and observability (Grafana)
* Internal messaging and communication (NATS)
* Platform infrastructure

If you believe a system-managed secret is incorrect or causing issues:

1. **Do not delete or modify the secret**
2. Document the issue, including the secret name and observed behavior
3. Contact Shopware PaaS support immediately
4. Do not attempt to work around system secrets by creating duplicates

### Secret History & Rollback

::: warning
**Important:** Shopware PaaS does not maintain version history for secrets. Once a secret is modified or deleted, the previous value cannot be recovered through the platform.
:::

Always back up critical secret values locally before making changes:

```sh
# Retrieve and save a secret locally before modifying
sw-paas vault get --secret-id SECRET-ID > backup-SECRET-NAME.txt
```

## Housekeeping & Legacy Secrets

### Identifying Legacy or Typo Secrets

Over time, your Vault may accumulate outdated or incorrectly named secrets. Common issues include:

* **Typo secrets**: e.g. `SHOPWAREPACKAGES_TOKEN` instead of `SHOPWARE_PACKAGES_TOKEN`
* **Deprecated secrets**: No longer used by current application versions
* **Duplicate secrets**: Same secret created multiple times with different IDs

### Recommended Cleanup Process

1. **Audit your secrets**:

   ```sh
   sw-paas vault list --application-id YOUR-APP-ID
   ```

2. **Identify unused secrets**: Review each secret and confirm whether it's actively used by your application

3. **Back up before deletion**:

   ```sh
   sw-paas vault get --secret-id SECRET-ID > backup-SECRET-NAME.txt
   ```

4. **Delete unused secrets**:

   ```sh
   sw-paas vault delete --secret-id SECRET-ID
   ```

5. **Document the cleanup**: Keep a record of what was deleted and when for future reference

### Dealing with Typo Secrets

If you discover a secret with a typo in its name, you have two options:

**Option 1: Edit the existing secret (faster)**

1. Edit the secret to correct its name or value:

   ```sh
   sw-paas vault edit
   ```

2. Select the secret from the list and update its value as needed

3. Update your application to use the corrected secret name if it changed

4. Test thoroughly to ensure the updated secret works

**Option 2: Create a new secret and delete the old one**

1. Back up the typo secret's value:

   ```sh
   sw-paas vault get --secret-id TYPO-SECRET-ID > backup-typo-SECRET-NAME.txt
   ```

2. Create a correctly named secret:

   ```sh
   sw-paas vault create
   ```

3. Update your application to use the correct secret

4. Test thoroughly to ensure it works

5. Delete the typo secret:

   ```sh
   sw-paas vault delete --secret-id TYPO-SECRET-ID
   ```

### Regular Maintenance

Establish a periodic review process:

* **Quarterly audit**: Review all user-managed secrets for relevance
* **Document ownership**: Maintain a record of which secrets are used by which applications

## Safety & Recovery

### Best Practices

1. **Always back up before deletion**:

   ```sh
   sw-paas vault get --secret-id SECRET-ID > $(date +%Y%m%d)-SECRET-NAME-backup.txt
   ```

2. **Rotate sensitive credentials regularly** (e.g., every 90 days):
   * Update API tokens and authentication credentials on a scheduled basis
   * Use the `sw-paas vault edit` command to quickly update credential values
   * Create new secrets and deprecate old ones for non-editable secret types

3. **Test changes in non-production environments first**

4. **Document secret purposes**: Add comments or maintain an external inventory

5. **Use descriptive names**: Choose clear, consistent naming conventions for your secrets

6. **Limit access**: Only share vault access with team members who need it

### What to Do If You Accidentally Delete a Secret

Since there is no built-in recovery mechanism:

1. **Check local backups** you may have created before deletion

2. **Review your application's configuration files** (if the secret was stored there temporarily during development)

3. **Regenerate the secret** if it's a token or credential that can be recreated:
   * For API tokens: Generate a new token from the service provider
   * For SSH keys: Create a new key pair and update deployment keys

4. **Contact support** if the deleted secret was critical and you have no backup

### Support Escalation

If you encounter issues that cannot be resolved with the above troubleshooting steps:

1. **Gather information**:
   * Secret name and ID
   * Application ID
   * Error messages or unexpected behavior
   * Steps to reproduce the issue

2. **Check system status**: Verify there are no ongoing PaaS incidents

3. **Contact Shopware PaaS support** with the gathered information

---

---

## Setting Up Repository Access via Deploy Keys
**Source:** [products/paas/shopware/guides/setting-up-repository-access.md](https://developer.shopware.com/docs/products/paas/shopware/guides/setting-up-repository-access.md)  
## Setting Up Repository Access via Deploy Keys

To enable Shopware PaaS Native to access your private Git repository, you must configure an **SSH deploy key**. This key allows the platform to securely clone your code during deployments.

Regardless of whether you use the CLI or set things up manually, you must **add the public SSH key to your repository**.

### Option 1: Automated Setup via PaaS CLI

For a quicker setup, you can use the PaaS CLI to automatically generate and register the key:

```sh
sw-paas vault create --type ssh
```

By default, this command stores the key at the **organization level**, making it available to all projects within the org. To limit the key to a specific project, use the `--project` flag:

```sh
sw-paas vault create --type ssh --project <project-id>
```

After running the command, copy the generated public key and add it to your Git repository's **Deploy keys** section (see instructions below).

### Option 2: Manual Setup

If you prefer full control over the SSH key creation process, follow these steps:

#### 1. Generate a Passwordless SSH Key Pair

Run the following command to generate an RSA key pair in PEM format:

```bash
ssh-keygen -t rsa -b 4096 -m PEM -f ./sw-paas
```

:::info
Alternative algorithms like **ED25519** and **ECDSA** are also supported, provided the key is **passwordless** and the **private key is in PEM format**.
:::

#### 2. Add the Public Key to Your Repository

Open the file `sw-paas.pub`, copy its contents, and add it as a **read-only deploy key** in your Git repository:

* **GitHub**: Go to your repository `Settings` → `Deploy keys`
* **GitLab**/**Bitbucket**: Look for the equivalent "Deploy keys" section in your repository settings
  Be sure to enable **read-only access**.

#### 3. Store the Private Key in the Vault

Once the public key is added to your repo, store the corresponding private key in the Shopware PaaS Native Vault:

```bash
cat sw-paas | sw-paas vault create --type ssh --password-stdin
```

You can store the key at either:

* **Organization level**: Shared across all projects.
* **Project level**: Dedicated to a single project (takes precedence over the org-level key).

:::warning
Only one SSH key can be stored per level (organization or project). You may name the key freely, but keep in mind that a project-level key **overrides** an organization-level one during deployments.
:::

---

---

## Guide: Update Shopware version in PaaS Native
**Source:** [products/paas/shopware/guides/update-shopware.md](https://developer.shopware.com/docs/products/paas/shopware/guides/update-shopware.md)  
# Guide: Update Shopware version in PaaS Native

This guide explains how to update Shopware in the PaaS Native context.

## Pre-requisite

The update should only be started if the latest deployment was successful (state: `DEPLOYING_STORE_SUCCESS`).

This can be checked with the following command `sw-paas app deploy list`:

```shell
sw-paas app deploy list
Selected: shopware
Selected: demo-shop
Found one application: demo-shop
╭────────────────────────────────────┬────────────────────────────────────┬───────────────────────┬────────────────────────────────────┬───────────────────┬───────────────────╮
│                 ID                 │              BUILD ID              │        STATUS         │             CREATED BY             │    CREATED AT     │    APPLIED AT     │
├────────────────────────────────────┼────────────────────────────────────┼───────────────────────┼────────────────────────────────────┼───────────────────┼───────────────────┤
│2492b221-aea6-46ce-9683-085714b8f0af│85c7246b-f788-11f0-adcf-be3c369299e8│DEPLOYING_STORE_SUCCESS│3324f8f2-20e1-70e2-5dbd-69ca97476cce│22.01.2026 11:51:13│22.01.2026 13:35:07│
│1ba79041-39a3-4172-bb36-24cd263ff6cc│65d399f4-f067-11f0-b5ac-4eb6c6ab52cb│DEPLOYING_STORE_SUCCESS│93343872-b001-7062-fbba-3a6314e4428d│13.01.2026 10:06:08│22.01.2026 07:32:29│
│ef58aa25-d303-4b56-b671-cb3918ad75c4│87ea381e-db2b-11f0-a41d-b643c268ee83│DEPLOYING_STORE_SUCCESS│c3446852-f0c1-7095-5131-8d424df937d0│17.12.2025 12:02:57│13.01.2026 08:47:39│
│3d0ebf52-c0f2-4798-b5ba-05ec01c9cf52│87ea381e-db2b-11f0-a41d-b643c268ee83│DEPLOYING_STORE_SUCCESS│c3446852-f0c1-7095-5131-8d424df937d0│17.12.2025 11:38:03│17.12.2025 11:39:42│
│a470ee4d-acea-414f-ad6e-54b2e06e97cf│87ea381e-db2b-11f0-a41d-b643c268ee83│DEPLOYING_STORE_SUCCESS│3324f8f2-20e1-70e2-5dbd-69ca97476cce│17.12.2025 09:56:47│17.12.2025 10:00:38│
│42834c59-c946-4c8e-81e3-62a115ae3fa2│87ea381e-db2b-11f0-a41d-b643c268ee83│DEPLOYING_STORE_SUCCESS│3324f8f2-20e1-70e2-5dbd-69ca97476cce│17.12.2025 09:34:56│17.12.2025 09:40:28│
│4d12f6c7-301f-4756-9c48-807d18d6d497│4be633d9-db21-11f0-a41d-b643c268ee83│DEPLOYING_STORE_SUCCESS│93343872-b001-7062-fbba-3a6314e4428d│17.12.2025 08:22:01│17.12.2025 08:24:57│
│2e1e5b43-da0d-4e87-bdfb-a66c42a71a68│d3e822ec-d994-11f0-b2b5-4ec7b4325483│DEPLOYING_STORE_SUCCESS│3324f8f2-20e1-70e2-5dbd-69ca97476cce│15.12.2025 09:03:49│15.12.2025 09:07:25│
╰────────────────────────────────────┴────────────────────────────────────┴───────────────────────┴────────────────────────────────────┴───────────────────┴───────────────────╯
```

If the state is `DEPLOYING_STORE_FAILED`, you should **NOT** initiate a Shopware update, fix the deployment before trying to do anything.

## Update

### Preliminary task

It's recommended to do a backup (called `snapshot`) of your application data (database and Shopware filesystem), you can do it with the following command:

```shell
sw-paas snapshot create
```

Wait until the snapshot is done.

### Update the code base

You should proceed as follows:

* Create a new branch: `git checkout -b my-new-branch`
* In `composer.json` update `shopware/core` to the new version
* Run `composer update --no-scripts`
* Run `composer recipes:update`
* Commit your changes: `git add . && git commit -m "Updating Shopware to version X.Y.Z"` (keep the commit SHA at hand)
* Push your branch: `git push -u origin my-new-branch`

Now your code is updated, but it needs to be deployed.

### Update the running application

Before updating the application, you should run the following Shopware command to prepare the update.
Open an exec session: `sw-paas exec --new`. Once you're in the session, run the following command: `bin/console system:update:prepare`.

Once this command is done, you can update the application, do the following: `sw-paas application update`.
You can track the progress of the deployment using `sw-paas app deploy list` and/or `sw-paas app deploy get`.

### Post update task

Once the application is successfully updated you can tell the system that the update is finished, open a new exec session: `sw-paas exec --new`, then run the following command: `bin/console system:update:finish`.

---

---

## Known Issues
**Source:** [products/paas/shopware/known-issues.md](https://developer.shopware.com/docs/v6.6/products/paas/shopware/known-issues.md)  
# Known Issues

This document outlines acknowledged issues with Shopware PaaS Native, including workarounds if known.

## Size of messages for the message queue

Currently, Shopware does not prevent bigger messages, but will do so with the next major version 6.7. Ensure the messages you are sending do not exceed this limit. Check your local log files for this [critical log message](https://github.com/shopware/shopware/blob/trunk/src/Core/Framework/MessageQueue/Subscriber/MessageQueueSizeRestrictListener.php#L48)

## Plugins should support S3 compatible storage

Some third-party plugin providers may not currently support S3 compatible storage solutions. Such plugins cannot be used in Shopware PaaS Native since we use S3 compatible storage as the media storage backend. If you encounter such a situation, consider visiting the plugin’s documentation or contact the developer directly to verify whether the plugin supports remote storage via S3 or a compatible service and if there are any known workarounds or planned updates for S3 support.

---

---

## Monitoring
**Source:** [products/paas/shopware/monitoring.md](https://developer.shopware.com/docs/products/paas/shopware/monitoring.md)  
# Monitoring

Shopware PaaS Native provides comprehensive monitoring capabilities to help you track the health and performance of your applications. With built-in monitoring tools, you can observe your application's behavior, troubleshoot issues, and ensure optimal performance in your cloud environment. This section introduces 3 key components used in monitoring: Logs, Traces and Events.

---

---

## Logs
**Source:** [products/paas/shopware/monitoring/logs.md](https://developer.shopware.com/docs/products/paas/shopware/monitoring/logs.md)  
# Logs

## Application Logs

Shopware PaaS Native allows you to view your application’s logs for a given environment via Grafana.

To access Grafana, run the following command:

```bash
sw-paas open grafana
```

This command will provide you with the Grafana URL, username, and password.

Once logged in to Grafana:

1. Open the **Explore** tab.
2. Select **Loki** as the data source.
3. Filter logs by setting the `component` label to the service you want to inspect.
4. Run the query to view the logs for that component.

![PaaS log search in Grafana](paas-monitoring-log-search.png "PaaS monitoring log search")

## Tips

In the Explore view, you can refine results using the search box:

* Line contains — matches the exact string.
* Line contains case-insensitive — recommended, as it matches the string regardless of the letter case.

A predefined dashboard named `Logs Dashboard` is available.
It displays the log ingestion volume and includes a built-in case-insensitive search box.

![PaaS log filter in Grafana](paas-monitoring-log-filter.png "PaaS monitoring log filter")

## Log retention

Shopware PaaS Native keeps your latest logs available for review. Logs older than 45 days are automatically removed.

---

---

## Traces
**Source:** [products/paas/shopware/monitoring/traces.md](https://developer.shopware.com/docs/products/paas/shopware/monitoring/traces.md)  
# Traces

## Application Traces

Shopware PaaS Native allows you to view your application's traces for a given environment via Grafana.

To access Grafana, run the following command:

```bash
sw-paas open grafana
```

This command will provide you with the Grafana URL, username, and password.

Once logged in to Grafana:

1. Go to the **Explore** tab.
2. Select **Tempo** as the data source.
3. Ensure the query type is **Search**
4. Filter traces by setting the Service Name to the value `shopware`.
5. Run the query to view your application traces.

## Trace Retention

Shopware PaaS Native keeps your latest traces available for review. Traces older than 14 days are automatically removed.

---

---

## Monitor events
**Source:** [products/paas/shopware/monitoring/watch.md](https://developer.shopware.com/docs/products/paas/shopware/monitoring/watch.md)  
# Monitor events

## Real-time Event Monitoring

Shopware PaaS Native provides real-time event monitoring for your applications, allowing you to track deployments, application status changes, and other important events as they happen.

To start monitoring events, run the following command:

```bash
sw-paas watch
```

This command will start streaming events in real-time to your terminal.

## Monitoring Specific Applications

You can monitor events for specific applications within your project:

```bash
sw-paas watch --application-ids app1,app2
```

This is particularly useful in multi-application projects where you only want to focus on certain services.

## Filtering Event Types

To reduce noise and focus on specific types of events, you can filter by event type:

```bash
sw-paas watch --event-types "EVENT_TYPE_DEPLOYMENT_STARTED,EVENT_TYPE_DEPLOYMENT_FINISHED"
```

Common event types include:

* `EVENT_TYPE_DEPLOYMENT_STARTED` - When a deployment begins
* `EVENT_TYPE_DEPLOYMENT_FINISHED` - When a deployment completes

The event stream will continue running until you stop it with `Ctrl+C`. All events are displayed in real-time with timestamps and detailed information about what's happening in your project.

## Understanding different Event Types

Events are generally linked to a preceding action.
Each action is connected to a specific event type, which is emitted when a state change occurs.
The type of each event is indicated in the output of the `sw-paas watch` command and can help to understand what is happening in your project.

Especially for deployments, the history of the events can be used to understand what happened during a deployment.
To list all events of a specific deployment, use the following command:

```bash
sw-paas application deploy get 
```

The output of the `DEPLOYMENT STATUS HISTORY` shows all events that were emitted during the deployment.
This contains events from the underlying PaaS infrastructure as well as events from the shop itself.

The following table lists the most common event types and their descriptions:

| Event | Description |
|-------|-------------|
| `UNSPECIFIED` | Default or unspecified deployment status |
| `PENDING` | Deployment is queued and waiting to start |
| `BASE` | Infrastructure: Base infrastructure components are being deployed |
| `BASE_FAILED` | Infrastructure: Base infrastructure deployment has failed |
| `BASE_SUCCESS` | Infrastructure: Base infrastructure deployment completed successfully |
| `SHOP` | Infrastructure: Shop-specific infrastructure components are being deployed |
| `SHOP_FAILED` | Infrastructure: Shop infrastructure deployment has failed |
| `SHOP_SUCCESS` | Infrastructure: Shop infrastructure deployment completed successfully |
| `DEPLOYING_STORE` | Store: Shopware store application is being deployed |
| `DEPLOYING_STORE_FAILED` | Store: Shopware store deployment has failed |
| `DEPLOYING_STORE_SUCCESS` | Store: Shopware store deployment completed successfully |
| `DEPLOYMENT_SUCCESS` | Complete deployment finished successfully |
| `DEPLOYMENT_FAILED` | Complete deployment has failed |

---

---

## Project Setup
**Source:** [products/paas/shopware/project_setup.md](https://developer.shopware.com/docs/v6.6/products/paas/shopware/project_setup.md)  
# Project Setup

## Local setup

Customizations that change the file system must be developed locally. This includes Shopware updates, installing and updating plugins ([documentation](https://developers.shopware.com/developers-guide/shopware-composer/#requiring-plugins)), making the initial configurations for the installation such as the system language, making code changes if necessary, etc.

:::info
It's not possible to manage extensions in the Shopware Administration panel. In distributed and high available setups, you can't dynamically install or update extensions because those changes need to be done on every host server. Therefore, such operations should be performed during a deployment/rollout and not dynamically.
:::

### Recommendation

Mac and Linux are recommended. When working with Windows, you can set up a local environment with Docker or WSL 2, as in this [tutorial](https://www.youtube.com/watch?v=5XYFRDlT9WI).

## Project creation

To create a new Shopware PaaS Native project, execute the following command:

```sh
composer create-project shopware/production <folder-name>
```

Including Docker configuration at this stage is optional; it will be added in the next step.

Next, navigate to your project directory and install the necessary Shopware packages to ensure appropriate environment variables are configured:

```sh
cd <folder-name>
composer require shopware/k8s-meta --ignore-platform-reqs
```

This will install the required configurations (recipes) for the Shopware operator. Please ensure they are added correctly. Verify successful installation by checking the package file `config/packages/operator.yaml`.

`--ignore-platform-reqs` option makes sure all recipes are pulled down by ignoring the local PHP setup.

Last step is this is to create a file named `application.yaml` at the root level of you project. This file is required; it allows some basics configuration regarding the deployment of your shop (like php version, mysql version, passing specific variables ...).
Here is a basic example:

```yaml
app:
  php:
    version: "8.3"
  environment_variables: []
  hooks: {}
services:
  mysql:
    version: "8.0"
```

Below, an advanced example including passing a Shopware environment variable:

```yaml
app:
  php:
    version: "8.3"
  environment_variables:
    - name: INSTALL_LOCALE
      value: fr-FR
      scope: RUN

  hooks: {}
services:
  mysql:
    version: "8.0"
```

## Repository setup with deploy keys for private repositories

To connect your private git repository with our backend, you need to add a deploy key to your repository.
This key is used to clone your repository and deploy your code to the cluster.

The PaaS CLI can also handle this for you. Execute the following command:

```bash
sw-paas vault create --type ssh
```

Note that this will add the ssh key as an organization level key. If you use multiple Projects you need to specify the project with the `--project` flag.

1. Generate a new SSH key pair on your local machine with an empty passphrase:

   ```bash
   ssh-keygen -t rsa -b 4096 -m PEM -f ./sw-paas
   ```

   We support different algorithms for SSH keys.
   The above command generates an **RSA** key.
   You can also use **ED25519** or **ECDSA** keys.
   The only requirement is that the key must be passwordless and the private key must be stored in PEM format.

2. Add the public key to your repository settings. Copy the content of the public key file `sw-paas.pub` and add it to your repository settings.

   In GitHub, you can find this under `Settings` -> `Deploy keys`.
   You can also add the key to your repository settings in GitLab or Bitbucket.
   The token should have read access to the repository.

3. Store the private key in the vault

   The private key must be stored in the vault.
   After that, the key will be used to clone the repository and deploy the code to the cluster.

```bash
cat sw-pass | sw-paas vault create --type ssh --password-stdin
```

The key can either be stored on an organization level or on a project level.
If you store the key on an organization level, all projects in this organization can use the key.
If you store the key on a project level, only this project can use the key.

A project level key will overwrite an organization level key.
The key name can be chosen freely because only one ssh key can be stored per level.

---

---

## Resources
**Source:** [products/paas/shopware/resources.md](https://developer.shopware.com/docs/products/paas/shopware/resources.md)  
# Resources

This section guides you through the resources that support your application, such as the database and object storage.

---

---

## Databases
**Source:** [products/paas/shopware/resources/databases.md](https://developer.shopware.com/docs/products/paas/shopware/resources/databases.md)  
# Databases

## Introduction

Shopware PaaS Native provides a managed MySQL cluster for each application created where we handle: automatic backups and recovery, high availability, performance monitoring and metrics, resource scaling (CPU, RAM, storage), automatic encryption of data at rest and in transit.

## Connecting to Database Cluster

To connect to your database via CLI:

```sh
sw-paas open service --service database --port 3306
```

### Note

Please check the [known issues](../known-issues.md) regarding network considerations when running this command.

---

---

## Object Storage
**Source:** [products/paas/shopware/resources/object-storage.md](https://developer.shopware.com/docs/products/paas/shopware/resources/object-storage.md)  
# Object Storage

## Introduction

Applications in Shopware PaaS Native are created by default with two S3-compatible object storage buckets. A public bucket and a private bucket.

You can learn more about [shopware filesystem here](../../../../guides/hosting/infrastructure/filesystem.md).

---

---

## Shopware Setup for PaaS
**Source:** [products/paas/shopware/setup-shopware-for-paas.md](https://developer.shopware.com/docs/v6.6/products/paas/shopware/setup-shopware-for-paas.md)  
# Shopware Setup for PaaS

## Prerequisite

**macOS** and **Linux** are the recommended environments for local development. On **Windows**, it's advisable to use [Docker](https://www.youtube.com/watch?v=5XYFRDlT9WI) or **WSL2** (Windows Subsystem for Linux) for a consistent development experience.

To develop and customize your Shopware project effectively, certain operations must be performed in a local environment. This is especially important for tasks that directly interact with the file system, such as Installing or upgrading plugins, adjusting system-level configuration (e.g., language, environment) or applying custom code changes.

Plugin management via the Shopware Administration interface is **not supported**. This is because the platform operates in a **high-availability (HA), clustered setup**, where all application instances must remain **stateless and identical**.

To ensure consistency and reproducibility across deployments, plugins must be installed or updated **via Composer** as part of the project’s codebase. Follow the official guidance on [managing extensions with Composer](https://developer.shopware.com/docs/guides/hosting/installation-updates/extension-managment.html#installing-extensions-with-composer).

Additionally, before installation, verify that each plugin supports **S3-based storage**, as not all extensions are compatible with external file systems.

## Prepare Your Shopware Application

Whether you're starting from scratch or working with an existing Shopware project, the following steps will ensure your setup is ready for deployment on Shopware PaaS Native.

### For New Projects

To create a new Shopware project from the official production template, run:

```sh
composer create-project shopware/production <folder-name>
```

Then navigate into the project directory and proceed with the next steps.

### For Existing Projects

If you're working with an already created Shopware project, simply navigate into the project directory:

```sh
cd <your-project-folder>
```

Ensure the required Kubernetes metadata package is installed to enable compatibility with the [Shopware Operator](https://github.com/shopware/shopware-operator):

```sh
composer require shopware/k8s-meta --ignore-platform-reqs
```

:::info
The `--ignore-platform-reqs` flag ensures that all necessary recipes are installed, even if your local PHP version differs from the required platform version.
:::

This package installs essential configuration files, including those required for deploying your shop via the Shopware Operator. After installation, verify that the file `config/packages/operator.yaml` has been created.

### Create the `application.yaml` File

At the root of your project, create a file named `application.yaml`. This file defines key deployment parameters, such as the PHP version and any environment-specific configuration needed for your shop.

#### Basic Example

```yaml
app:
  php:
    version: "8.3"
  environment_variables: []
  hooks: {}
services:
  mysql:
    version: "8.0"
```

#### Advanced Example (with Custom Environment Variables)

```yaml
app:
  php:
    version: "8.3"
  environment_variables:
    - name: INSTALL_LOCALE
      value: fr-FR
      scope: RUN # Supports RUN or BUILD
  hooks: {}
services:
  mysql:
    version: "8.0"
```

---

---

## Theme Build
**Source:** [products/paas/theme-build.md](https://developer.shopware.com/docs/v6.5/products/paas/theme-build.md)  
# Theme Build

The entire build process is performed without an active database connection. However, for theme builds, Shopware needs to access the theme configuration. We make it available by checking it into our VCS repository. This process must be performed **after** you first installed Shopware in your PaaS environment because it runs a command that requires an existing database that was not created on the first run.

## Set up theme configuration

First, set up the correct sales channels and configure their themes.

Use the command below to change the theme for the sales channels. Add the `--no-compile` flag to disable compilation in this step, as this is not possible in a read-only environment after project deployment. The compilation will happen automatically in the next build step ( at the last step of this guide).

```bash
bin/console theme:change --no-compile
```

## Dump configuration

To dump the theme configuration, use the below command :

```bash
shopware ssh -A app 'bin/console theme:dump'
```

This will connect to the application through an SSH tunnel and run a command which dumps the theme configuration into the remote `files/theme-config/` directory.

## Download configuration

Because we want to check the theme configuration into our VCS repository, we have to download it first.

```bash
shopware mount:download --mount 'files' --target 'files' -A app
```

This will download the remote directory `files` into our local directory `files`. The `-A` parameter specifies the app name, which is just `app` in our case.

## Push configuration

Eventually, we add the downloaded configuration and add it to our repository.

```bash
git add files/theme-config
git commit -m 'Update theme configuration'
git push # platform main
```

Again, if you push changes to `platform main`, it will trigger a redeploy. After this, your theme assets will be compiled properly and the deployed store will look fine.

---

---

## Commercial
**Source:** [products/plugins/commercial.md](https://developer.shopware.com/docs/v6.5/products/plugins/commercial.md)  
# Commercial

The Shopware 6 commercial feature-set comprises myriad features, the sum of which provide additional support for businesses which require extended functionality within the Shopware 6 ecosystem.

## Plugin structure

The commercial plugin is structured as a group of nested sub-bundles. [Plugins](../../../concepts/extensions/plugins-concept) concept explains you more about this.

## Setup

Installation of the commercial plugin does not require special guidance. The installation steps are detailed in our [Plugin Base Guide](../../../guides/plugins/plugins/plugin-base-guide#install-your-plugin).

This plugin contains various feature, which are also covered in our docs as well.

::: warning
In accordance with a Shopware merchant's active account configuration, features within the plugin will be in *active* or *inactive* (whilst still being installed within the Shopware codebase). Pay close attention to any install information or special conditions for the provided features.
:::

---

---

## PWA
**Source:** [products/pwa.md](https://developer.shopware.com/docs/v6.6/products/pwa.md)  
# PWA

If you think about providing a decoupled storefront for customers, you can use **Shopware PWA** as a base. It is a Single Page Application (SPA) based on JavaScript and Vue.js that already integrates a whole lot of the Shopware functionality you know into a very extensible frontend application.

[Shopware PWA](https://shopware-pwa-docs.vuestorefront.io/) is based on the [Store API](../concepts/api/store-api).

::: warning
Shopware PWA is currently in maintenance mode.\
We recommend using [Composable Frontends](/frontends) as the future of headless commerce with Shopware.
:::

---

---

## Cloud
**Source:** [products/saas.md](https://developer.shopware.com/docs/v6.6/products/saas.md)  
# Cloud

With the SaaS platform, Shopware provides updates, hosting, and infrastructure. Also, there are ways to extend it.

The [App system](../concepts/extensions/apps-concept) gives you great freedom to develop extensions for SaaS stores.

---

---

## Sales Agent Overview
**Source:** [products/sales-agent.md](https://developer.shopware.com/docs/v6.6/products/sales-agent.md)  
# Sales Agent Overview

This project is designed to streamline the communication and sales processes between sales representatives and their customers. By integrating Shopware, it enables sales representatives to handle various tasks in an optimized environment, without the overhead added by the Shopware Administration.

![ ](../../assets/sales-agent-overview.jpg)

:::info
**Sales Agent** is a licensed application and not available as open source.
:::

:::info
The **Sales Agent** application does not belong to the *default Storefront*. It is a standalone Frontend app running with Nuxt instance. This template will be hosted in a separate instance with a new domain, which will be different from the Storefront domain.
:::

To get access to the private Gitlab repository, create a support ticket in your [Shopware Account](https://account.shopware.com). Access is granted after a short validation or a purchase of the Beyond or the Evolve license.

## Prerequisites

Review the below minimum operating requirements before you install *Sales Agent* on your infrastructure:

* [node](https://nodejs.org/en) >= v18
* [pnpm](https://pnpm.io/installation) >= 8
* [Shopware Frontends framework](https://frontends.shopware.com/) based on Nuxt 3.
* Instance of [Shopware 6](../../guides/installation) (version 6.5 and above).
* Beyond or Evolve license needed for the Shopware instance.

## API Documentation

[API documentation](https://shopware.stoplight.io/docs/swag-sales-agent/) provides detailed information about the available endpoints and their functionalities.

---

---

## Appearance
**Source:** [products/sales-agent/appearance.md](https://developer.shopware.com/docs/v6.6/products/sales-agent/appearance.md)  
# Appearance

To change the appearance of your Sales Agent, you can customize the theme, colors, and logo.

## Regarding SCSS

Currently SCSS (or Sass) is included as a dev dependency in our project (see `package.json`). This is a dependency needed as a peer dependency of the meteor component library. However, we discourage you from using SCSS, as we will likely remove it from Sales Agent in the future. The reason for this is that we already provide a powerful framework for styling your frontend (UnoCSS), which is also integrated into the Shopware Frontends framework.

## Config, favicon and logo

You can customize your sales agent by editing the app and configuring it in your `config.ts` file. Additionally, favicon and logo can be easily replaced in the following paths. Please consider using square dimensions for the image file if possible:

* Favicon: `./public/favicon.ico`
* Logo: `./public/logo.svg`

---

---

## products/sales-agent/best-practices.md
**Source:** [products/sales-agent/best-practices.md](https://developer.shopware.com/docs/products/sales-agent/best-practices.md)  
---

---

## Frontend App Deployment
**Source:** [products/sales-agent/best-practices/app-deployment.md](https://developer.shopware.com/docs/products/sales-agent/best-practices/app-deployment.md)  
# Frontend App Deployment

According to [Shopware Frontends deployment document](https://frontends.shopware.com/best-practices/deployment.html), all the templates which were generated by Shopware Frontends can be deployed in multiple ways, depending on the setup you are using. Most likely you will be using either a static hosting service or a server with a Node.js runtime.

You may find the different approaches as described in [Nuxt instruction](https://nuxt.com/deploy).

Alternatively, we will show some best practices of *Sales Agent* frontend app deployment.

---

---

## Deploy with AWS Amplify
**Source:** [products/sales-agent/best-practices/app-deployment/aws.md](https://developer.shopware.com/docs/products/sales-agent/best-practices/app-deployment/aws.md)  
# Deploy with AWS Amplify

In this chapter, you will learn how to deploy the frontend source code to [AWS Amplify](https://aws.amazon.com/amplify/).

## Prerequisites

* Register an AWS account.
* Clone the frontend source code and push it to your Git repository (for example, GitHub).

## Setup Redis with Amazon ElastiCache

AWS Amplify does not include Redis by default. To use Redis for caching, you need to set up [Amazon ElastiCache](https://aws.amazon.com/elasticache/) or use an external Redis provider.

### Option 1: Amazon ElastiCache

Amazon ElastiCache is a fully managed in-memory data store service compatible with Redis.

1. Navigate to the [ElastiCache Console](https://console.aws.amazon.com/elasticache/).
2. Click "Create" and select "Redis OSS" as the cluster engine.
3. Configure your cluster settings (node type, number of replicas, etc.).
4. Configure security groups to allow access from your Amplify application.
5. Once created, note the **Primary Endpoint** for your Redis connection.

::: warning
ElastiCache runs within a VPC. Connecting from AWS Amplify (which runs outside VPC by default) requires additional configuration such as VPC peering or using a public endpoint. For serverless applications, consider using Option 2.
:::

### Option 2: Serverless Redis providers

For easier integration with serverless deployments like AWS Amplify, consider using:

* [Upstash](https://upstash.com/) - Serverless Redis with REST API support, ideal for edge/serverless environments.
* [Redis Cloud](https://redis.com/cloud/overview/) - Managed Redis with public endpoints.

These providers offer public endpoints that work seamlessly with AWS Amplify without VPC configuration.

### Configure Redis environment variables

After setting up Redis (ElastiCache or a serverless provider), configure these environment variables in AWS Amplify:

```bash
REDIS_CACHE=true
REDIS_HOST=your-redis-endpoint.cache.amazonaws.com  # Or your provider's endpoint
REDIS_PORT=6379
REDIS_PASSWORD=your_redis_password
REDIS_TLS=true  # Recommended for production
```

Add these variables in the AWS Amplify Console under "Environment variables" in your app settings, or include them in your `.env.template` file.

## Deploy

* Login to the AWS Amplify Hosting Console.
* Create a new app in AWS Amplify.
* Select and authorize access to your Git repository provider and select the main branch (it will auto-deploy when there are some changes in the main branch).
* Choose a name for your app and make sure build settings are auto-detected.
* Set Environment variables which are declared in `.env.template` under the Advanced Settings section.
* Confirm the configuration and click on "Save and Deploy".

## Custom domain

After deploying your code to AWS Amplify, you may wish to point custom domains (or subdomains) to your site. AWS has an [instruction](https://docs.aws.amazon.com/amplify/latest/userguide/custom-domains.html).

---

---

## Deploy with Cloudflare
**Source:** [products/sales-agent/best-practices/app-deployment/cloudflare.md](https://developer.shopware.com/docs/products/sales-agent/best-practices/app-deployment/cloudflare.md)  
# Deploy with Cloudflare

In this chapter you will learn how to deploy the frontend source code to [Cloudflare Pages](https://pages.cloudflare.com/).

## Prerequisites

* Register a Cloudflare account.
* Clone the frontend source code and push to your GitHub repository.

## Setup Redis with Upstash

Cloudflare Pages/Workers do not include a built-in Redis service. [Upstash](https://upstash.com/) is the recommended serverless Redis provider that integrates natively with Cloudflare.

### Create an Upstash Redis database

1. Sign up at [Upstash Console](https://console.upstash.com/).
2. Click "Create Database" and select a region close to your users.
3. Once created, navigate to the database details page.
4. Copy the connection details:
   * **REDIS\_HOST**: The endpoint URL (e.g., `xxx.upstash.io`)
   * **REDIS\_PORT**: Usually `6379` or the TLS port `6380`
   * **REDIS\_PASSWORD**: The password from the database details
   * **REDIS\_TLS**: Set to `true` for secure connections

### Configure environment variables

Add these Redis environment variables to your `.env` file:

```bash
REDIS_CACHE=true
REDIS_HOST=your-database.upstash.io
REDIS_PORT=6379
REDIS_PASSWORD=your_upstash_password
REDIS_TLS=true
```

### Cloudflare integration (optional)

You can also set up the Upstash integration directly in Cloudflare:

1. Go to [Cloudflare Dashboard](https://dash.cloudflare.com/) → Workers & Pages → Your project.
2. Navigate to Settings → Integrations.
3. Find and add the Upstash integration.
4. Follow the prompts to connect your Upstash account.

## Deploy from a local machine

* Due to this [issue](https://github.com/nuxt/nuxt/issues/28248), just make sure your `.npmrc` file has the following content:

```bash
shamefully-hoist=true
strict-peer-dependencies=false
```

* Install Wrangler

```bash
pnpm install wrangler --save-dev
```

* Make sure the Frontend app has already [generated an .env file](../../installation.md#create-a-env-file)
* Build your project for Cloudflare Pages:

```bash
npx nuxi build --preset=cloudflare_pages
```

* Then deploy. However, for the first time, it will ask you to create a project:

```bash
wrangler pages deploy dist/
```

## Automation with GitHub Actions

### Setup GitHub Secrets & variables

* In GitHub Secrets, add `CLOUDFLARE_API_TOKEN` with API token value.
  * [Create an API token](https://developers.cloudflare.com/fundamentals/api/get-started/create-token/) in the Cloudflare dashboard with the "Cloudflare Pages — Edit" permission.
* In GitHub environment variables, create new environment named `production` and fill it with all environment variables in `.env.template`.
  * Besides `production`, we can add new values for the same variable names in multiple environments such as `development`, `staging`.

### Setup pipeline

To trigger the deployment automatically, we can attach the GitHub Actions.

* Create a `.github/workflows/publish.yml` file in your repository with the below sample content.

::: warning
Please note that this pipeline is just a sample. There are some points need to update for a specific purpose
:::

```yml
on:
  push:
    # Specify the pipeline trigger
    branches:
      - main

jobs:
  publish:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      deployments: write
    name: Cloudflare Pages Deployment
    # Specify the environment name
    environment: production
    steps:
      - name: Checkout
        uses: actions/checkout@v3

      - uses: pnpm/action-setup@v4
        name: Install pnpm
        with:
          version: 8
          run_install: false

      - name: Install dependencies
        run: |
          pnpm install

      - name: Build env file
        run: |
          touch .env
          echo COMPANY_NAME=${{ vars.COMPANY_NAME }} >> .env
          echo ORIGIN=${{ vars.ORIGIN }} >> .env
          echo REDIS_CACHE=${{ vars.REDIS_CACHE }} >> .env
          echo REDIS_HOST=${{ vars.REDIS_HOST }} >> .env
          echo REDIS_PORT=${{ vars.REDIS_PORT }} >> .env
          echo REDIS_PASSWORD=${{ vars.REDIS_PASSWORD }} >> .env
          echo REDIS_TLS=${{ vars.REDIS_TLS }} >> .env
          echo APP_NAME=${{ vars.APP_NAME }} >> .env
          echo APP_SECRET=${{ vars.APP_SECRET }} >> .env
          echo DATABASE_URL=${{ vars.DATABASE_URL }} >> .env

      - name: Build code
        run: |
          npx nuxi build --preset=cloudflare_pages

      - name: Publish to Cloudflare Pages
        uses: cloudflare/pages-action@v1.5.0
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          accountId: YOUR_ACCOUNT_ID
          projectName: YOUR_PROJECT_NAME
          directory: dist
          wranglerVersion: "3"
```

* Replace `YOUR_ACCOUNT_ID` with your account ID. Get it from the dashboard URL. E.g: `https://dash.cloudflare.com/<ACCOUNT_ID>/pages`.
* Replace `YOUR_PROJECT_NAME` with the appropriate value.

## Custom domain

When deploying your Pages project, you may wish to point custom domains (or subdomains) to your site. Cloudflare has an [instruction](https://developers.cloudflare.com/pages/configuration/custom-domains/).

---

---

## Deploy with Ubuntu Server with PM2
**Source:** [products/sales-agent/best-practices/app-deployment/hosted-with-ubuntu-server.md](https://developer.shopware.com/docs/products/sales-agent/best-practices/app-deployment/hosted-with-ubuntu-server.md)  
# Deploy with Ubuntu Server with PM2

This guide will walk you through the steps to deploy Sales Agent frontend web application to an Ubuntu server using [PM2](https://nuxt.com/docs/getting-started/deployment#pm2), a process manager for Node.js applications. PM2 will help you keep your app running in the background, restart it automatically when it crashes, and manage logs for easier troubleshooting.

## Prerequisites

* **Ubuntu Server**: This guide assumes you have an Ubuntu server running, and you can access it via SSH.
* **Node.js & npm**: Make sure Node.js and npm (Node package manager) are installed on your server.
* **PM2**: PM2 should be installed globally.

```bash
npm install -g pm2
```

* **pnpm**

```bash
npm install -g pnpm
```

* **Frontend Application**: Clone the frontend source code and push to your GitHub repository.

## Setup Redis

Redis is required for caching. You can either install Redis locally on your Ubuntu server or use a managed Redis service.

### Option 1: Install Redis locally

Install Redis using the package manager:

```bash
sudo apt update
sudo apt install redis-server
```

Configure Redis for production by editing the configuration file:

```bash
sudo nano /etc/redis/redis.conf
```

Key settings to consider:

* Set `supervised systemd` to integrate with systemd.
* Configure `bind` to restrict access (e.g., `bind 127.0.0.1` for local only).
* Set a password with `requirepass your_secure_password`.

Enable and start the Redis service:

```bash
sudo systemctl enable redis-server
sudo systemctl start redis-server
```

Verify Redis is running:

```bash
# If you configured a password with requirepass
redis-cli -a your_secure_password ping

# If no password is set
redis-cli ping
```

You should see `PONG` as a response.

### Option 2: Use a managed Redis service

Alternatively, you can use managed Redis services such as:

* [Upstash](https://upstash.com/) - Serverless Redis with pay-per-request pricing.
* [Redis Cloud](https://redis.com/cloud/overview/) - Managed Redis by Redis Ltd.

These services provide connection details (host, port, password) that you configure in your `.env` file.

### Configure Redis environment variables

Add these Redis environment variables to your `.env` file:

```bash
REDIS_CACHE=true
REDIS_HOST=127.0.0.1  # For local installation, or your managed service endpoint
REDIS_PORT=6379
REDIS_PASSWORD=your_secure_password  # If configured with requirepass
REDIS_TLS=false  # Set to true for managed services that require TLS
```

For managed Redis services like Upstash, use the connection details provided by the service (host, port, password, and set `REDIS_TLS=true` for secure connections).

## Build code

* Please follow instructions here to [set up all necessary things and build the code](../../installation.md#setup-app-server)

## Start the Application with PM2

Now that your app is built, create a file named `ecosystem.config.cjs` in the root of your project with the following content. Ensure that the script path points to your app's build output directory (e.g., `.output/server/index.mjs` for Nuxt 3)

```js
module.exports = {
  apps: [
    {
      name: "SalesAgentApp",
      port: "3000",
      exec_mode: "cluster",
      instances: "max",
      script: "./.output/server/index.mjs",
    },
  ],
};
```

Once saved, you can start the app with:

```bash
pm2 start ecosystem.config.cjs
```

---

---

## Sales Agent Customization
**Source:** [products/sales-agent/customization.md](https://developer.shopware.com/docs/products/sales-agent/customization.md)  
# Sales Agent Customization

This section explains how to customize the *Sales Agent* frontend. It is built with Nuxt 3 and leverages the [Nuxt Layer concept](https://nuxt.com/docs/getting-started/layers), allowing you to override file content with your own Nuxt layer for easy customization.

## Create a new Nuxt layer

If you look into the source code, you'll find the default Nuxt layer named `sales-agent`. This layer should remain untouched. To apply customizations, you should create a new Nuxt layer and import it in `nuxt.config.ts`. For more details, refer to the [composition guide](https://nuxt.com/docs/guide/going-further/layers). Besides, we’ve also created a customization layer named `example` within the frontend source code. You can rename this layer and modify its contents to suit your needs.

---

---

## Branding Customization
**Source:** [products/sales-agent/customization/branding.md](https://developer.shopware.com/docs/products/sales-agent/customization/branding.md)  
::: warning
All customization instructions will refer to changes made within your customization layer folder.
:::

# Branding Customization

## Favicon

* Create `public` folder inside your layer (if missing).

* Place your favicon inside the `public` folder and ensure it is named `favicon.ico`.

## Web application title

* Create `nuxt.config.ts` inside your layer (if missing).

* Replace "Your app name" with your app's name and add the following code:

```js
app: {
  head: {
    title: 'Your app name'
  }
}
```

## Theme color

Sales Agent utilizes the Shopware [Meteor Component Library](https://shopware.design/get-started/installation.html), which provides a comprehensive CSS variable system to manage themes. The default theme is aligned with their design system, ensuring consistency across applications. This package offers both a [light theme](https://github.com/shopware/meteor/blob/main/packages/tokens/deliverables/administration/light.css) and a [dark theme](https://github.com/shopware/meteor/blob/main/packages/tokens/deliverables/administration/dark.css), allowing you to explore and utilize the CSS variable system effectively.

### Customizing Theme Colors

To tailor the theme to your brand's identity, you can override the default CSS variables. By defining custom values in your own CSS file, you can seamlessly adapt the visual aspects of the application:

```css
/* main.css */
:root {
  --color-interaction-primary-default: #80A1BA; /* Add your primary color */
  /* Add more customizations as needed */
}
```

### Integrating Custom Styles in Nuxt.js

To apply these customizations in your application, import the CSS file into your Nuxt configuration. This will ensure that your branding colors take effect across the app:

```javascript
// nuxt.config.ts
export default defineNuxtConfig({
  css: ["./main.css"], // Include your custom CSS file
});
```

By doing so, you maintain the flexibility of the Shopware system while aligning it with your unique brand style, providing a cohesive user experience.

---

---

## Component Customization
**Source:** [products/sales-agent/customization/component.md](https://developer.shopware.com/docs/products/sales-agent/customization/component.md)  
::: warning
All customization instructions will refer to changes made within your customization layer folder.
:::

# Component Customization

In this document, we will demonstrate how to customize a component (e.g, the login page) in the Sales Agent frontend using the Nuxt layer concept. This guide will help you understand the process of extending or modifying the default components in your frontend without altering the core files.

## Understand the component structure of the default layer

Before customizing any components, it's essential to understand the structure of the default layer. Navigate to the `~/layers/sales-agent` directory to view all available components.

In this case, look for the `login.vue` component inside `sales-agent/pages/auth`.

## Create the component in the custom layer

Now, inside your custom layer, paste the copied `login.vue` file. You should now have the same default component in your custom-layer directory, ready for modification.
Once you have copied the component to your custom layer, modify the part of the component that you want to change. For instance, you may want to change the style, add new functionality, or update the template.
At this point, the frontend app will ignore the `login.vue` from the default layer and only use the `login.vue` from the custom layer.

See example in the layer `example` of source code.

---

---

## I18n Customization
**Source:** [products/sales-agent/customization/i18n.md](https://developer.shopware.com/docs/products/sales-agent/customization/i18n.md)  
::: warning
All customization instructions will refer to changes made within your customization layer folder.
:::

# I18n Customization

This guide will walk you through the process of customizing the internationalization (i18n) setup in your Nuxt 3 project using the Nuxt layer concept. By using this method, you can extend and override the default i18n functionality to meet your specific requirements without modifying the core files.

## Configure i18n

Configure the i18n settings in your `nuxt.config.ts` file. This configuration defines the language directory and any specific language configurations you want to override.

Add the following configuration to `nuxt.config.ts`:

```js
modules: [
  "@nuxtjs/i18n",
],
i18n: {
  langDir: "./i18n/src/langs/",
  locales: [
    {
      code: "en-GB",
      iso: "en-GB",
      file: "en-GB.ts",
    },
    {
      code: "de-DE",
      iso: "de-DE",
      file: "de-DE.ts",
    },
  ],
},
```

## Create the i18n Folder in the custom layer

To customize the i18n functionality, we need to create a new folder structure in your custom layer. You will mirror the default layer's structure, but only create the files you need to override.

Take a look on `example` layer to understand the structure.

---

---

## Deployment
**Source:** [products/sales-agent/deployment.md](https://developer.shopware.com/docs/v6.6/products/sales-agent/deployment.md)  
## Deployment

For general information about running a Nuxt application in production, refer to the [official docs](https://nuxt.com/docs/getting-started/deployment).

In addition, the Sales Agent is using a configurable storage adapter for persisting data (`server/infrastructure/StorageAdapter.ts`). During local development, there is a file-based fallback storage adapter. However, in production, you need to configure a proper storage adapter.
The corresponding configuration can be found in `nuxt.config.ts` in the `nitro.storage` object.

For the usage, please read the [nitro unstorage documentation](https://nitro.build/guide/storage).

For a list of supported storage drivers and more detailed information, please refer to the [unstorage documentation](https://unstorage.unjs.io/).

## Production build

To build and start the project in production mode:

```bash
pnpm run build
pnpm run start
```

There is also a docker compose configuration to start the project in production mode:

```bash
docker compose -f docker-compose.prod.yml up
```

---

---

## Installation
**Source:** [products/sales-agent/installation.md](https://developer.shopware.com/docs/v6.6/products/sales-agent/installation.md)  
# Installation

1.) **Clone the Repository**

```shell
git clone https://github.com/shopware/swagsalesagent.git
cd swagsalesagent
```

2.) **Create a `.env` File**

* Use the provided `.env.template` file as an example.

```shell
cp .env.template .env
```

\* Fill in the required details in the `.env` file. See the [table](#env-properties) below for a detailed explanation of the properties.

3.) **Set Up Shopware**

* Go to the Shopware instance you want to use.
* Go to the storefront sales channel, scroll down, and copy the API Access Key. Add this key to your `.env` file.
* Go to Admin > Settings > Integrations, add a new Integration and assign a role that has at least the following permissions:
  * Write permission for Orders
  * View permission for Sales Channels
  * View permission for Customers
* Copy the secrets into your `.env` file.

4.) **Install dependencies**

```shell
pnpm install --frozen-lockfile --prefer-offline
```

5.) **Run the Development Server**

```shell
pnpm run dev
```

## Docker setup

Alternatively, you can also use docker to install and start the application.

```shell
docker compose up
```

### .env Properties

| Property                           | Description                                                                                                                                                                                     |
|------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| AUTH\_ORIGIN \*                      | The base URL for the authentication server. This is the host for redirects during user authentication.                                                                                          |
| SHOPWARE\_STORE\_API \*               | The base URL for the Shopware store API. Replace `hostname` with your actual Shopware Store-API URL. This can be found in your sales channel configuration.                                     |
| SHOPWARE\_STORE\_API\_ACCESS\_TOKEN \*  | The access token for the Shopware store API. Obtain this from your Shopware instance.                                                                                                           |
| SHOPWARE\_ADMIN\_API \*               | The base URL for the Shopware Administration API. Replace `hostname` with your actual Shopware Administration API URL.                                                                          |
| SHOPWARE\_ADMIN\_API\_CLIENT\_ID \*     | The client ID for the Shopware Administration API. Create an integration in Shopware Administration to get this.                                                                                |
| SHOPWARE\_ADMIN\_API\_CLIENT\_SECRET \* | The client secret for the Shopware Administration API. Create an integration in Shopware Administration to get this.                                                                            |
| SHOPWARE\_STOREFRONT\_URL \*          | The base URL for the Shopware storefront. Replace `hostname` with your actual Shopware storefront URL.                                                                                          |
| SHOPWARE\_CDN\_URL                   | The base URL for the Shopware CDN. Normally, if you don't setup a different CDN with storefront URL, then just leave it blank. Otherwise, replace `hostname` with your actual Shopware CDN URL. |
| API\_AUTH\_SECRET\_KEY \*              | Provide your own arbitrary key here. This is used for authenticating requests against server-side endpoints (e.g. creating users).                                                              |
| STORAGE\_DRIVER                     | The storage driver to use in production. Please refer to the [Deployment](./deployment#deployment) section.                                                                                     |
| STORAGE\_HOST                       | The storage host to use in production. Please refer to the [Deployment](./deployment#deployment) section.                                                                                       |
| STORAGE\_PORT                       | The storage port to use in production. Please refer to the [Deployment](./deployment#deployment) section.                                                                                       |
| STORAGE\_PASSWORD                   | The storage password to use in production. Please refer to the [Deployment](./deployment#deployment) section.                                                                                   |
| STORAGE\_TLS                        | Use TLS for storage communication in production. Please refer to the [Deployment](./deployment#deployment) section.                                                                             |

### Local SSL setup

To set up SSL for local development, follow the below steps:

1. Install `mkcert` (or similar tools)
2. Inside the SalesAgent directory, run `mkcert localhost`. This will generate a key pair in your current directory.
3. Run `NODE_TLS_REJECT_UNAUTHORIZED=0 nuxt dev --host=localhost --https --ssl-cert 'localhost.pem' --ssl-key 'localhost-key.pem'`

:::info
You can also replace localhost with any IP address or domain name, for example, if you want to test this application from different devices over your local network.
:::

---

---

## Client and Server Routing
**Source:** [products/sales-agent/routing.md](https://developer.shopware.com/docs/v6.6/products/sales-agent/routing.md)  
# Client and Server Routing

Refer to the Nuxt documentation for more information about how [server](https://nuxt.com/docs/guide/directory-structure/server) and [client](https://nuxt.com/docs/guide/directory-structure/pages) routes work internally.

For an up-to-date overview of all routes for this application, you can use the [Nuxt dev tools](https://devtools.nuxt.com/). This should be enabled by default during local development.

---

---

## Testing
**Source:** [products/sales-agent/testing.md](https://developer.shopware.com/docs/v6.6/products/sales-agent/testing.md)  
# Testing

## Unit Tests

[Vitest](https://vitest.dev/) is used for unit testing. The tests are located in the `tests` directory.

## Running Tests

**Unit Tests**

```bash
pnpm run test
```

**Coverage**

```bash
pnpm run test:coverage
```

---

---

## Creating a user and set restrictions
**Source:** [products/sales-agent/users.md](https://developer.shopware.com/docs/v6.6/products/sales-agent/users.md)  
# Creating a user and set restrictions

You can create a user by sending a `POST` request to the `/api/user` endpoint. The `x-api-key` header is required and can be set in the environment (`API_AUTH_SECRET_KEY`).

```bash
curl -XPOST -H 'x-api-key: <secret>' -H "Content-type: application/json" -d '{
    "name": <name>,
    "email": <email>,
    "id": <id>,
    "password": <password>
}' '<sales_agent_instance_url>/api/user'
```

To restrict a user to viewing only specific customers, you can send a `POST` request to the `/api/entity-restriction` endpoint.

```bash
curl -XPOST -H 'x-api-key: <secret>' -H "Content-type: application/json" -d '{
    "entity": "customer",
    "email": <user_email>,
    "criteria": {
      "filter": [{
        "field": "lastName",
        "type": "equals",
        "value": "Doe"
      }]
    }
}' '<sales_agent_instance_url>/api/entity-restriction'
```

In this example, the user with the email `<user_email>` will only be able to see customers with the last name "Doe".
The criteria object supports the same fields as the shopware API. You can find more information about the criteria object in the [documentation](https://developer.shopware.com/docs/guides/integrations-api/general-concepts/search-criteria.html).

Further documentation of the available endpoints can be found in the [API documentation](https://shopware.stoplight.io/docs/swag-sales-agent/).

---

---


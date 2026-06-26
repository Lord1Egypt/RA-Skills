# License Key Registration

## Table of Contents
- [Overview](#overview)
- [Register License with Environment Variables](#register-license-with-environment-variables)
- [CI/CD Integration](#cicd-integration)

## Overview

The generated Syncfusion license key must be registered in your React application. **The recommended approach is to use environment variables** to avoid accidentally committing license keys to source control.

**Important Notes:**
- License validation is performed **offline** during application execution
- No internet connection required after registration
- Apps can be deployed on any system without internet access
- License key registration required from v20.1.0.47+ (2022 Volume 1) onwards

## Register License with Environment Variables

The recommended way to register your Syncfusion license key is using environment variables. This approach keeps your license key secure and prevents accidental commits to source control.

### Step 1: Set Environment Variable

Set the `SYNCFUSION_LICENSE` environment variable on your system with your license key.

#### Windows

Open command prompt and use the `setx` command:

```cmd
setx SYNCFUSION_LICENSE "Your_License_Key_Here"
```

#### Mac

Open terminal and add to your bash profile:

```bash
echo 'export SYNCFUSION_LICENSE="Your_License_Key_Here"' >> ~/.bash_profile
```

To modify the environment variable:

```bash
nano ~/.bash_profile
```

Press `Ctrl+X` to exit, then `Y` and `Enter` to save changes.

Close and reopen terminal to see the changes using `env` command.

#### Linux

Open terminal and set the environment variable:

```bash
export SYNCFUSION_LICENSE='Your_License_Key_Here'
```

### Step 2: Restart your IDE or terminal

After setting the environment variable, restart your IDE or application terminal.

### Step 3: Activate the License

Open command prompt in the application root directory and run:

```bash
npx syncfusion-license activate
```

**Success message:**
```
(INFO) Syncfusion License imported successfully.
```

### Step 4: Clear Cache

Remove the `.cache` folder from `node_modules`:

```bash
# Windows PowerShell
Remove-Item -Recurse -Force node_modules\.cache

# macOS/Linux
rm -rf node_modules/.cache
```

> **Note:** For alternative license registration methods, kindly refer to the [Syncfusion license key registration documentation](https://ej2.syncfusion.com/react/documentation/licensing/license-key-registration).


## CI/CD Integration

**Important:** Always use secret management systems in CI/CD pipelines. Never hardcode license keys in workflow files or commit them to source control.

### GitHub Actions

Use environment variables in GitHub Actions to register your license in CI pipelines.

**Step 1:** Create a Repository Secret

1. Go to your repository → **Settings** → **Secrets and variables** → **Actions**
2. Click **"New repository secret"**
3. Name: `SYNCFUSION_LICENSE`
4. Value: Your license key
5. Click **"Add secret"**

Or create an [Organization Secret](https://docs.github.com/en/actions/security-guides/encrypted-secrets#creating-encrypted-secrets-for-an-organization) to share across repositories.

**Step 2:** Add activation step to your workflow

```yaml
# WARNING: Always use secrets, never hardcode license keys in workflow files
steps:
  - name: Install node modules
    run: npm install

  - name: Activate Syncfusion License
    run: npx syncfusion-license activate
    env:
      SYNCFUSION_LICENSE: ${{ secrets.SYNCFUSION_LICENSE }}
```

**Complete Example:**

```yaml
# WARNING: Always use secrets, never hardcode license keys in workflow files
name: Build React App

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
      
      - name: Install dependencies
        run: npm install
      
      - name: Activate Syncfusion License
        run: npx syncfusion-license activate
        env:
          SYNCFUSION_LICENSE: ${{ secrets.SYNCFUSION_LICENSE }}
      
      - name: Build application
        run: npm run build
```

### Azure Pipelines (YAML)

Use environment variables in Azure Pipelines to register your license.

**Step 1:** Create a User-defined Variable

1. Navigate to your pipeline → **Edit** → **Variables**
2. Click **"New variable"**
3. Name: `SYNCFUSION_LICENSE`
4. Value: Your license key
5. Check **"Keep this value secret"**

**Step 2:** Add activation step to your pipeline

**For Windows build agents:**

```yaml
# WARNING: Always use secret variables, never hardcode license keys in pipeline files
pool:
  vmImage: 'windows-latest'

steps:
  - script: call npm install
    displayName: 'Install node modules'

  - script: call npx syncfusion-license activate
    displayName: 'Activate Syncfusion License'
    env:
      SYNCFUSION_LICENSE: $(SYNCFUSION_LICENSE)
```

**For Linux build agents:**

```yaml
# WARNING: Always use secret variables, never hardcode license keys in pipeline files
pool:
  vmImage: 'ubuntu-latest'

steps:
  - script: npm install
    displayName: 'Install node modules'

  - script: npx syncfusion-license activate
    displayName: 'Activate Syncfusion License'
    env:
      SYNCFUSION_LICENSE: $(SYNCFUSION_LICENSE)
```

### Azure Pipelines (Classic)

For Classic Editor users:

**Step 1:** Create a User-defined Variable named `SYNCFUSION_LICENSE` with your license key as the value. Make sure to mark it as secret.

**Step 2:** Add a Bash task after npm install with the following script:

```bash
# WARNING: Ensure SYNCFUSION_LICENSE is stored as a secret variable
# Never hardcode license keys in scripts
npx syncfusion-license activate
```


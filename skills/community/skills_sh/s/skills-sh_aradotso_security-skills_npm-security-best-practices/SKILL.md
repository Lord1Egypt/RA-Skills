---
name: npm-security-best-practices
description: Expert guidance on securing npm packages, preventing supply chain attacks, and hardening package manager configurations
triggers:
  - how do I secure my npm dependencies
  - protect against supply chain attacks in npm
  - configure npm security settings
  - disable npm postinstall scripts
  - block malicious npm packages
  - set up secure package manager config
  - prevent dependency confusion attacks
  - harden npm package installs
---

# npm Security Best Practices

> Skill by [ara.so](https://ara.so) — Security Skills collection.

This skill provides expert guidance on securing npm package installations, preventing supply chain attacks, and implementing security best practices for Node.js development. Based on the comprehensive npm-security-best-practices repository by Lirantal.

## Overview

The npm ecosystem is a frequent target for supply chain attacks including:
- **Shai-Hulud attacks** - Worm-like propagation through compromised packages
- **Nx incident** - Malicious code in postinstall scripts
- **event-stream attack** - Long-running exfiltration via lifecycle scripts
- **Dependency confusion** - Attackers publishing malicious packages with internal names

This skill covers configuration, tooling, and practices to mitigate these risks across npm, pnpm, and Bun.

## Secure-by-Default Configuration

### npm (.npmrc)

Create or update `.npmrc` in your project root or global config (`~/.npmrc`):

```ini
# Disable all lifecycle scripts (postinstall, preinstall, etc.)
ignore-scripts=true

# Block git-based dependencies (git+ssh://, git+https://, etc.)
allow-git=none

# Only install packages that have been published for at least 30 days
min-release-age=30
```

Apply globally:

```bash
npm config set ignore-scripts true
npm config set allow-git none
npm config set min-release-age 30
```

### pnpm (pnpm-workspace.yaml)

Create `pnpm-workspace.yaml` in your project root:

```yaml
# Block packages newer than 30 days (43200 minutes)
minimumReleaseAge: 43200

# Reject versions with regressed trust signals (pnpm 10.21+)
trustPolicy: no-downgrade

# Allowlist for packages that need build scripts
allowBuilds:
  esbuild: true
  rolldown: true
  nx@21.6.4 || 21.6.5: true

# Fail install if unlisted scripts try to run
strictDepBuilds: true

# Block git URLs in dependencies
blockExoticSubdeps: true

# Optional: ignore trust policy for legacy packages
trustPolicyIgnoreAfter: 43200

# Optional: exempt specific packages from trust policy
trustPolicyExclude:
  - 'chokidar@4.0.3'
```

### Bun (package.json)

Bun disables postinstall scripts by default. To allow specific packages:

```json
{
  "trustedDependencies": [
    "esbuild",
    "sharp",
    "fsevents"
  ]
}
```

## Installation Commands

### Secure npm install

```bash
# Install with security flags
npm install --ignore-scripts --allow-git=none

# Use npm ci for reproducible installs (CI/CD)
npm ci --ignore-scripts

# Install specific package securely
npm install lodash --ignore-scripts --allow-git=none
```

### Secure pnpm install

```bash
# Install with workspace config enforced
pnpm install

# Review blocked packages
pnpm install --loglevel=verbose

# Bypass trust policy for specific install (use sparingly)
pnpm install --ignore-trust-policy
```

### Selective script execution

Use `@lavamoat/allow-scripts` for granular control:

```bash
# Install the tool
npm install -g @lavamoat/allow-scripts

# Create allowlist
npx allow-scripts setup

# Edit package.json to add allowlist
```

Example `package.json`:

```json
{
  "scripts": {
    "prepare": "allow-scripts"
  },
  "lavamoat": {
    "allowScripts": {
      "esbuild": true,
      "core-js": false,
      "nx>@nx/nx-linux-x64-gnu": true
    }
  }
}
```

## Hardening npx Execution

```bash
# Execute without installing package
npx --no-install create-react-app my-app

# Use specific version to avoid typosquatting
npx create-react-app@5.0.1 my-app

# Verify package before running
npm view create-react-app
npx create-react-app my-app

# Use with security wrappers (see below)
```

## Security Tooling Integration

### npq - Package quality and security checks

```bash
# Install globally
npm install -g npq

# Use instead of npm install
npq install lodash

# Check package before installing
npq check lodash
```

### Socket Firewall (sfw)

```bash
# Install globally
npm install -g @socketsecurity/cli

# Protect npm install
npx @socketsecurity/cli npm install

# Audit project dependencies
npx @socketsecurity/cli audit

# Check specific package
npx @socketsecurity/cli info lodash
```

### Snyk - Vulnerability scanning

```bash
# Install CLI
npm install -g snyk

# Authenticate
snyk auth

# Test for vulnerabilities
snyk test

# Monitor project
snyk monitor

# Check for supply chain issues
snyk code test
```

## Automated Dependency Updates with Cooldown

### Renovate Bot (renovate.json)

```json
{
  "extends": ["config:base"],
  "minimumReleaseAge": "30 days",
  "stabilityDays": 30,
  "prCreation": "not-pending",
  "packageRules": [
    {
      "matchUpdateTypes": ["major"],
      "minimumReleaseAge": "60 days"
    }
  ]
}
```

### Dependabot (.github/dependabot.yml)

```yaml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    # Dependabot doesn't support minimumReleaseAge natively
    # Use branch protection rules and manual delay
    open-pull-requests-limit: 10
    labels:
      - "dependencies"
      - "security"
```

Use GitHub Actions to enforce cooldown:

```yaml
name: Dependency Cooldown Check
on:
  pull_request:
    paths:
      - 'package.json'
      - 'package-lock.json'

jobs:
  check-release-age:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Check package age
        run: |
          # Custom script to verify package age
          node scripts/check-package-age.js
```

## Lockfile Security

### Prevent lockfile injection

```bash
# Review lockfile changes in PRs
git diff package-lock.json

# Verify integrity
npm audit

# Regenerate if suspicious
rm package-lock.json
npm install --ignore-scripts
```

### .gitattributes protection

```
# Prevent merge conflicts from hiding malicious changes
package-lock.json merge=binary
pnpm-lock.yaml merge=binary
```

## Package Health Assessment

### Snyk Advisor lookup

```bash
# Check package health
curl https://snyk.io/advisor/npm-package/lodash | jq

# CLI check
npx snyk-advisor lodash
```

### Manual verification checklist

```javascript
// check-package-health.js
const fetch = require('node-fetch');

async function checkPackage(packageName) {
  const response = await fetch(`https://registry.npmjs.org/${packageName}`);
  const data = await response.json();
  
  const latestVersion = data['dist-tags'].latest;
  const versionInfo = data.versions[latestVersion];
  
  console.log(`Package: ${packageName}@${latestVersion}`);
  console.log(`Published: ${versionInfo.time || 'N/A'}`);
  console.log(`Maintainers: ${data.maintainers?.length || 0}`);
  console.log(`License: ${versionInfo.license || 'NONE'}`);
  console.log(`Has scripts: ${!!versionInfo.scripts}`);
  console.log(`Dependencies: ${Object.keys(versionInfo.dependencies || {}).length}`);
  
  // Check provenance (npm 9.5+)
  if (versionInfo.dist?.attestations) {
    console.log('✓ Has provenance attestation');
  } else {
    console.log('⚠ No provenance attestation');
  }
}

checkPackage(process.argv[2]);
```

Run:

```bash
node check-package-health.js lodash
```

## Preventing Dependency Confusion

### .npmrc scoped registries

```ini
# Use private registry for org packages
@mycompany:registry=https://npm.pkg.github.com
//npm.pkg.github.com/:_authToken=${GITHUB_TOKEN}

# Public packages from npm
registry=https://registry.npmjs.org/
```

### package.json name scoping

```json
{
  "name": "@mycompany/internal-lib",
  "version": "1.0.0",
  "publishConfig": {
    "registry": "https://npm.pkg.github.com"
  }
}
```

## Dev Container Security

### .devcontainer/devcontainer.json

```json
{
  "name": "Secure Node.js Dev",
  "image": "mcr.microsoft.com/devcontainers/javascript-node:20",
  "features": {
    "ghcr.io/devcontainers/features/node:1": {
      "version": "20"
    }
  },
  "postCreateCommand": "npm config set ignore-scripts true && npm config set allow-git none",
  "remoteEnv": {
    "NPM_CONFIG_IGNORE_SCRIPTS": "true",
    "NPM_CONFIG_ALLOW_GIT": "none"
  },
  "mounts": [
    "source=${localEnv:HOME}/.npmrc,target=/home/node/.npmrc,type=bind,consistency=cached"
  ]
}
```

## Environment Variable Security

### Use .env.vault instead of plaintext .env

```bash
# Install dotenv-vault
npm install dotenv-vault

# Encrypt secrets
npx dotenv-vault local build

# Generate .env.vault (encrypted)
npx dotenv-vault push

# .gitignore update
echo ".env" >> .gitignore
echo ".env.*.vault" >> .gitignore
```

### Access encrypted secrets

```javascript
// app.js
require('dotenv-vault-core').config();

const apiKey = process.env.API_KEY; // Decrypted at runtime
```

## Maintainer Best Practices

### Enable 2FA on npm account

```bash
# Enable 2FA
npm profile enable-2fa auth-and-writes

# Verify status
npm profile get
```

### Publish with provenance (npm 9.5+)

```bash
# Publish with provenance attestation
npm publish --provenance

# Verify in package.json before publishing
npm pack --dry-run
```

### GitHub Actions OIDC publishing

```yaml
# .github/workflows/publish.yml
name: Publish Package
on:
  release:
    types: [created]

jobs:
  publish:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          registry-url: 'https://registry.npmjs.org'
      - run: npm ci --ignore-scripts
      - run: npm publish --provenance --access public
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

## Troubleshooting

### Scripts are blocked but package needs them

**Problem**: A legitimate package requires postinstall scripts.

**Solution**: Use allowlist approach with `@lavamoat/allow-scripts` or pnpm `allowBuilds`:

```bash
# pnpm approach
# Add to pnpm-workspace.yaml
allowBuilds:
  problematic-package: true

# npm/yarn approach with lavamoat
npm install @lavamoat/allow-scripts
npx allow-scripts setup
# Edit package.json lavamoat.allowScripts section
```

### Git dependency is required

**Problem**: Internal package only available via git URL.

**Solution**: Use private npm registry instead:

```bash
# Publish to GitHub Packages
echo "//npm.pkg.github.com/:_authToken=${GITHUB_TOKEN}" >> .npmrc
npm publish --registry=https://npm.pkg.github.com

# Or use Verdaccio for self-hosted registry
npm install -g verdaccio
verdaccio
```

### Cooldown period blocks urgent security fix

**Problem**: Security patch released but blocked by min-release-age.

**Solution**: Temporarily override for specific package:

```bash
# npm - install specific version without min-release-age
npm install package@1.2.3 --no-min-release-age

# pnpm - add to trustPolicyExclude
# In pnpm-workspace.yaml:
trustPolicyExclude:
  - 'package@1.2.3'
```

### Trust policy blocks legitimate package

**Problem**: pnpm trust policy rejects package downgrade.

**Solution**: Investigate first, then exempt if safe:

```bash
# Check what changed
npm view package@version dist.integrity
npm view package@old-version dist.integrity

# If legitimate, exempt in pnpm-workspace.yaml
trustPolicyExclude:
  - 'package@version'
```

### False positive from security scanner

**Problem**: Snyk/Socket reports issue in vetted package.

**Solution**: Create exceptions with justification:

```yaml
# .snyk
ignore:
  SNYK-JS-LODASH-12345:
    - lodash:
        reason: 'Prototype pollution not exploitable in our use case'
        expires: '2024-12-31'
```

## CI/CD Integration

### GitHub Actions security workflow

```yaml
name: Security Audit
on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      
      - name: Install with security flags
        run: npm ci --ignore-scripts
      
      - name: Audit dependencies
        run: npm audit --audit-level=moderate
      
      - name: Check with Socket
        run: npx @socketsecurity/cli audit
        env:
          SOCKET_SECURITY_API_KEY: ${{ secrets.SOCKET_API_KEY }}
      
      - name: Snyk security scan
        run: npx snyk test --severity-threshold=high
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
```

## Additional Resources

- [npm-security-best-practices GitHub repo](https://github.com/lirantal/npm-security-best-practices)
- [npm security audit docs](https://docs.npmjs.com/cli/v10/commands/npm-audit)
- [pnpm security docs](https://pnpm.io/supply-chain-security)
- [Socket.dev security platform](https://socket.dev)
- [Snyk Advisor](https://snyk.io/advisor/)

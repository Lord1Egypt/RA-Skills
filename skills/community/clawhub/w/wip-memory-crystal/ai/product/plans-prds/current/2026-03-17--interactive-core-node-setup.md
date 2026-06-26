# Plan: Make crystal init handle full Core/Node setup automatically

## Context

Parker is about to install Memory Crystal on his Air laptop (first multi-device test). Currently `crystal init` requires 5+ manual steps: flags for role, manual pairing, manually fetching relay tokens from 1Password, manually writing env files, manually editing shell profile. The SKILL.md promises a guided experience. The code delivers flags-only.

**Repo:** `memory-crystal-private`
**Files:** `src/installer.ts` (main), `src/cli.ts` (CLI entry), `src/role.ts` (role mgmt)

## The 6 Gaps

| # | Gap | Severity |
|---|-----|----------|
| 1 | No interactive Core/Node selection | HIGH |
| 2 | Relay env vars never written | CRITICAL |
| 3 | No First Install vs Adding Device detection | HIGH |
| 4 | Pairing not prompted interactively | HIGH |
| 5 | Shell profile never updated | HIGH |
| 6 | Role detection ignores relay key file | MEDIUM |

## Implementation

### Fix 1: Interactive role selection

**File:** `src/installer.ts`, inside `runInstallOrUpdate()` after scaffold (line ~670)

If no `--core` or `--node` flag AND this is an interactive terminal:

```typescript
if (!options.role && process.stdin.isTTY) {
  const { createInterface } = await import('readline');
  const rl = createInterface({ input: process.stdin, output: process.stdout });
  const answer = await new Promise<string>(resolve => {
    rl.question('\n  Is this your primary machine (always on), or adding a device?\n  [1] Primary (Crystal Core)\n  [2] Adding a device (Crystal Node)\n  > ', resolve);
  });
  rl.close();
  options.role = answer.trim() === '2' ? 'node' : 'core';
}
```

### Fix 2: Relay env var automation

**File:** `src/installer.ts`, new function

After role is set to Node (or Core with relay), write relay config:

```typescript
async function configureRelay(agentId: string): Promise<void> {
  const secretsDir = join(HOME, '.ldm', 'secrets');
  mkdirSync(secretsDir, { recursive: true });
  const envPath = join(secretsDir, 'crystal-relay.env');

  // Default relay URL (WIP.computer hosted)
  const relayUrl = 'https://memory-crystal-relay.wipcomputer.workers.dev';

  // Get token: try 1Password first, then prompt
  let token = '';
  try {
    const saToken = readFileSync(join(HOME, '.openclaw', 'secrets', 'op-sa-token'), 'utf8').trim();
    token = execSync(
      `OP_SERVICE_ACCOUNT_TOKEN=${saToken} op item get "Memory Crystal Relay Auth Tokens" --vault "Agent Secrets" --fields label=${agentId}-token --reveal`,
      { encoding: 'utf8', timeout: 15000 }
    ).trim();
  } catch {
    // 1Password not available. Prompt user.
    if (process.stdin.isTTY) {
      const rl = createInterface({ input: process.stdin, output: process.stdout });
      token = await new Promise<string>(resolve => {
        rl.question('  Relay token (from crystal pair on Core): ', resolve);
      });
      rl.close();
    }
  }

  if (!token) {
    console.log('  ! No relay token. Set CRYSTAL_RELAY_TOKEN manually.');
    return;
  }

  // Write env file
  writeFileSync(envPath, `export CRYSTAL_RELAY_URL=${relayUrl}\nexport CRYSTAL_RELAY_TOKEN=${token}\nexport CRYSTAL_AGENT_ID=${agentId}\n`);
  console.log(`  + Relay config written to ${envPath}`);

  // Source in current process
  process.env.CRYSTAL_RELAY_URL = relayUrl;
  process.env.CRYSTAL_RELAY_TOKEN = token;
  process.env.CRYSTAL_AGENT_ID = agentId;
}
```

### Fix 3: First Install vs Adding Device

**File:** `src/installer.ts`, early in `runInstallOrUpdate()`

Detect if another Crystal Core exists (relay key present, or user says so):

```typescript
// If fresh install and no role specified, check if this is a new device
if (isFresh && !options.role && process.stdin.isTTY) {
  const rl = createInterface({ input: process.stdin, output: process.stdout });
  const answer = await new Promise<string>(resolve => {
    rl.question('\n  First time installing Memory Crystal, or adding to an existing setup?\n  [1] First time (this becomes Crystal Core)\n  [2] Adding a device (I have a Core elsewhere)\n  > ', resolve);
  });
  rl.close();
  if (answer.trim() === '2') {
    options.role = 'node';
    // Prompt for pairing code
    const rl2 = createInterface({ input: process.stdin, output: process.stdout });
    options.pairCode = await new Promise<string>(resolve => {
      rl2.question('  Pairing code from Core (run "crystal pair" on Core): ', resolve);
    });
    rl2.close();
  } else {
    options.role = 'core';
  }
}
```

### Fix 4: Pairing prompted interactively

Covered by Fix 3. When user selects "Adding a device", they're prompted for the pairing code inline. No need for separate `--pair` flag in the interactive flow.

### Fix 5: Shell profile update

**File:** `src/installer.ts`, new function

After writing relay env file, offer to add source to shell profile:

```typescript
async function updateShellProfile(envPath: string): Promise<void> {
  const shellProfile = join(HOME, '.zshrc'); // macOS default
  const sourceLine = `source ${envPath}`;

  try {
    const existing = readFileSync(shellProfile, 'utf8');
    if (existing.includes(sourceLine)) {
      console.log('  + Shell profile already sources relay config');
      return;
    }
  } catch {}

  if (process.stdin.isTTY) {
    const rl = createInterface({ input: process.stdin, output: process.stdout });
    const answer = await new Promise<string>(resolve => {
      rl.question(`  Add relay config to ~/.zshrc? [Y/n] `, resolve);
    });
    rl.close();
    if (answer.trim().toLowerCase() !== 'n') {
      appendFileSync(shellProfile, `\n# Memory Crystal relay\n${sourceLine}\n`);
      console.log('  + Added to ~/.zshrc');
    }
  }
}
```

### Fix 6: Role detection from relay key

**File:** `src/role.ts`, in `detectRole()`

Check relay key file exists, not just env var:

```typescript
const relayKeyPath = resolveSecretPath('crystal-relay-key');
const hasRelayKey = existsSync(relayKeyPath);

// If relay key exists but no local embeddings, this is a Node
if (hasRelayKey && !localEmbeddings && !roleFromState) {
  role = 'node';
}
```

## Wire it together in installer.ts

In `runInstallOrUpdate()`, after all deploys and before final summary:

```typescript
// Role setup (interactive or from flags)
if (options.role === 'node') {
  await demoteToNode();
  if (options.pairCode) {
    await pairReceive(options.pairCode);
  }
  await configureRelay(agentId);
  await updateShellProfile(join(HOME, '.ldm', 'secrets', 'crystal-relay.env'));
} else if (options.role === 'core') {
  await promoteToCore();
}
```

## Files to modify

| File | Changes |
|------|---------|
| `memory-crystal-private/src/installer.ts` | Fixes 1-5: interactive prompts, relay config, shell profile |
| `memory-crystal-private/src/role.ts` | Fix 6: detect role from relay key file |
| `memory-crystal-private/src/cli.ts` | Pass new options through to installer |

## What does NOT change

- `crystal pair` CLI (already works)
- `crystal promote` / `crystal demote` CLI (already works)
- Database handling (already works)
- `--core`, `--node`, `--pair` flags (still work, skip interactive prompts)
- Non-interactive mode (CI, scripted installs use flags)

## Verification

On the Air laptop:
```bash
npm install -g @wipcomputer/wip-ldm-os
ldm install wipcomputer/memory-crystal
crystal init --agent cc-air

# Should interactively ask:
# 1. First time or adding device? -> "Adding"
# 2. Pairing code? -> paste from Mini
# 3. Add to ~/.zshrc? -> Y
# 4. Role set to Node, relay configured, profile updated

crystal role    # should show: node
crystal status  # should show: relay configured, agent cc-air
```

#!/usr/bin/env node
/**
 * WALVIS CLI Installer
 * Interactive setup: npx walvis
 */

import { createRequire } from 'module';
import { existsSync, mkdirSync, readFileSync, writeFileSync, cpSync } from 'fs';
import { join, dirname } from 'path';
import { homedir } from 'os';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const rootDir = join(__dirname, '..');
const TESTNET_SEAL_PACKAGE_ID = '0x299d7d7592c84d08a25ec26c777933d6ab72e51b31a615027186a0a377fe75cb';

async function main() {
  const { default: chalk } = await import('chalk');
  const { default: inquirer } = await import('inquirer');

  console.log(chalk.cyan('\n🐋 WALVIS Setup\n'));
  console.log(chalk.gray('W.A.L.V.I.S. - Walrus Autonomous Learning & Vibe Intelligence System'));
  console.log(chalk.gray('AI-powered bookmark manager with Walrus decentralized storage\n'));

  // Detect OpenClaw installation
  const localOpenClaw = await detectLocalOpenClaw();
  const dockerOpenClaw = await detectDockerOpenClaw();

  let openclawMode = 'none';
  let openclawConfigDir = null;
  let openclawWorkspaceDir = null;

  if (localOpenClaw && dockerOpenClaw) {
    const { mode } = await inquirer.prompt([{
      type: 'list',
      name: 'mode',
      message: 'Found OpenClaw both locally and in Docker. Which to use?',
      choices: [
        { name: `Docker (${dockerOpenClaw.container})`, value: 'docker' },
        { name: 'Local (~/.openclaw/)', value: 'local' },
      ],
    }]);
    openclawMode = mode;
  } else if (dockerOpenClaw) {
    console.log(chalk.green(`✓ OpenClaw found in Docker (${dockerOpenClaw.container})`));
    openclawMode = 'docker';
  } else if (localOpenClaw) {
    console.log(chalk.green('✓ OpenClaw found locally'));
    openclawMode = 'local';
  } else {
    // Ask for manual path
    const { hasOpenClaw } = await inquirer.prompt([{
      type: 'confirm',
      name: 'hasOpenClaw',
      message: 'OpenClaw not auto-detected. Do you have it installed (e.g. Docker with volume mounts)?',
      default: false,
    }]);
    if (hasOpenClaw) {
      const { configPath } = await inquirer.prompt([{
        type: 'input',
        name: 'configPath',
        message: 'Path to OpenClaw config directory (the one containing openclaw.json):',
        validate: (v) => existsSync(join(v, 'openclaw.json')) || `openclaw.json not found at ${v}`,
      }]);
      openclawMode = 'manual';
      openclawConfigDir = configPath;
      // Check if workspace is separate or inside config
      const wsInConfig = join(configPath, 'workspace');
      openclawWorkspaceDir = existsSync(wsInConfig) ? wsInConfig : null;
    } else {
      console.log(chalk.yellow('⚠ Skill will not be auto-installed. You can copy manually later.'));
    }
  }

  // Set paths based on mode
  if (openclawMode === 'docker' && dockerOpenClaw) {
    openclawConfigDir = dockerOpenClaw.configDir;
    openclawWorkspaceDir = dockerOpenClaw.workspaceDir;
  } else if (openclawMode === 'local') {
    openclawConfigDir = join(homedir(), '.openclaw');
    openclawWorkspaceDir = join(homedir(), '.openclaw', 'workspace');
  }

  // Prompt for configuration
  const answers = await inquirer.prompt([
    {
      type: 'input',
      name: 'agentName',
      message: 'Agent name (users will @mention this):',
      default: 'walvis',
      validate: (v) => /^[a-z0-9_-]+$/i.test(v) || 'Only letters, numbers, hyphens, underscores',
    },
    {
      type: 'input',
      name: 'llmEndpoint',
      message: 'LLM API endpoint (OpenAI-compatible base URL):',
      default: 'https://api.openai.com/v1',
    },
    {
      type: 'password',
      name: 'llmApiKey',
      message: 'LLM API key:',
      validate: (v) => v.length > 0 || 'API key is required',
    },
    {
      type: 'input',
      name: 'llmModel',
      message: 'LLM model name:',
      default: 'gpt-4o',
    },
    {
      type: 'list',
      name: 'network',
      message: 'Sui network:',
      choices: ['testnet', 'mainnet'],
      default: 'testnet',
    },
    {
      type: 'input',
      name: 'suiAddress',
      message: 'Sui wallet address (leave blank to skip):',
      default: '',
    },
    {
      type: 'input',
      name: 'spaceName',
      message: 'Default space name:',
      default: 'bookmarks',
    },
    {
      type: 'input',
      name: 'restoreBlob',
      message: 'Restore from Walrus blob ID (leave blank to start fresh):',
      default: '',
    },
  ]);

  const {
    agentName, llmEndpoint, llmApiKey, llmModel,
    network, suiAddress, spaceName, restoreBlob,
  } = answers;

  // Walrus endpoints
  const walrusPublisher = network === 'mainnet'
    ? 'https://publisher.walrus.space'
    : 'https://publisher.walrus-testnet.walrus.space';
  const walrusAggregator = network === 'mainnet'
    ? 'https://aggregator.walrus.space'
    : 'https://aggregator.walrus-testnet.walrus.space';

  // Create ~/.walvis directory structure
  const walvisDir = join(homedir(), '.walvis');
  const spacesDir = join(walvisDir, 'spaces');
  mkdirSync(walvisDir, { recursive: true });
  mkdirSync(spacesDir, { recursive: true });

  const spaceId = generateId();

  const manifest = {
    agent: agentName,
    fastPathEnabled: true,
    spaces: {},
    suiAddress: suiAddress || undefined,
    network,
    ...(network === 'testnet' ? { sealPackageId: TESTNET_SEAL_PACKAGE_ID } : {}),
    activeSpace: spaceId,
    llmEndpoint,
    llmModel,
    walrusPublisher,
    walrusAggregator,
  };

  // Handle restore from blob
  if (restoreBlob) {
    console.log(chalk.yellow('\nRestoring from Walrus...'));
    try {
      const res = await fetch(`${walrusAggregator}/v1/blobs/${restoreBlob}`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const spaceData = await res.json();
      const restoredId = spaceData.id ?? spaceId;
      writeFileSync(join(spacesDir, `${restoredId}.json`), JSON.stringify(spaceData, null, 2));
      manifest.spaces[restoredId] = { blobId: restoreBlob, syncedAt: new Date().toISOString() };
      manifest.activeSpace = restoredId;
      console.log(chalk.green(`✓ Restored space "${spaceData.name}" (${spaceData.items?.length ?? 0} items)`));
    } catch (err) {
      console.log(chalk.red(`✗ Restore failed: ${err.message}. Starting fresh.`));
      createDefaultSpace(spacesDir, spaceId, spaceName);
    }
  } else {
    createDefaultSpace(spacesDir, spaceId, spaceName);
  }

  // Write manifest
  writeFileSync(join(walvisDir, 'manifest.json'), JSON.stringify(manifest, null, 2));
  console.log(chalk.green('\n✓ Created ~/.walvis/manifest.json'));

  // Install skill to OpenClaw
  if (openclawConfigDir) {
    await installSkill(chalk, openclawConfigDir, openclawWorkspaceDir, openclawMode, agentName, llmApiKey, llmEndpoint, llmModel);
  }

  // Print summary
  console.log(chalk.cyan('\n🐋 WALVIS is ready!\n'));
  console.log(chalk.white('Usage in Telegram:'));
  console.log(chalk.gray(`  @${agentName} <url>        — save a bookmark`));
  console.log(chalk.gray(`  @${agentName} -q <query>   — search bookmarks`));
  console.log(chalk.gray(`  @${agentName} -s           — sync to Walrus`));
  console.log(chalk.gray(`  @${agentName} -status      — check status\n`));

  if (openclawMode === 'docker') {
    console.log(chalk.white('Restart OpenClaw Docker container to load the skill.'));
  } else if (openclawMode === 'local') {
    console.log(chalk.white('Start OpenClaw:'));
    console.log(chalk.gray('  openclaw gateway start\n'));
  } else if (openclawMode === 'none') {
    console.log(chalk.white('Manual skill install:'));
    console.log(chalk.gray(`  cp -r ${join(rootDir, 'skill')} <openclaw-config>/skills/walvis/\n`));
  }
}

function generateId() {
  return Math.random().toString(36).slice(2, 10) + Date.now().toString(36);
}

function createDefaultSpace(spacesDir, spaceId, spaceName) {
  const now = new Date().toISOString();
  const space = {
    id: spaceId,
    name: spaceName,
    description: `Default bookmark space`,
    items: [],
    createdAt: now,
    updatedAt: now,
  };
  writeFileSync(join(spacesDir, `${spaceId}.json`), JSON.stringify(space, null, 2));
}

async function detectLocalOpenClaw() {
  try {
    const { execSync } = await import('child_process');
    execSync('openclaw --version', { stdio: 'pipe' });
    return true;
  } catch {
    return false;
  }
}

async function detectDockerOpenClaw() {
  try {
    const { execSync } = await import('child_process');
    // Find running openclaw containers
    const containers = execSync('docker ps --format "{{.Names}}"', { encoding: 'utf-8', stdio: ['pipe', 'pipe', 'pipe'] })
      .trim().split('\n').filter(n => n.toLowerCase().includes('openclaw'));

    if (containers.length === 0) return null;

    const container = containers[0];

    // Get volume mounts to find host paths
    const mounts = execSync(
      `docker inspect ${container} --format '{{range .Mounts}}{{.Source}}|||{{.Destination}}\n{{end}}'`,
      { encoding: 'utf-8', stdio: ['pipe', 'pipe', 'pipe'] }
    ).trim().split('\n');

    let configDir = null;
    let workspaceDir = null;

    for (const mount of mounts) {
      const [src, dest] = mount.split('|||');
      if (!src || !dest) continue;
      // The main .openclaw config mount
      if (dest.includes('.openclaw') && !dest.includes('workspace')) {
        configDir = src.trim();
      }
      // Workspace mount (might be separate)
      if (dest.includes('workspace')) {
        workspaceDir = src.trim();
      }
    }

    // If workspace is inside config dir
    if (configDir && !workspaceDir) {
      const ws = join(configDir, 'workspace');
      if (existsSync(ws)) workspaceDir = ws;
    }

    if (!configDir) return null;

    return { container, configDir, workspaceDir };
  } catch {
    return null;
  }
}

async function installSkill(chalk, configDir, workspaceDir, openclawMode, agentName, llmApiKey, llmEndpoint, llmModel) {
  const skillSrc = join(rootDir, 'skill');
  const extensionSrc = join(rootDir, 'extensions', 'walvis-fastpath');
  const hookSrc = join(rootDir, 'hooks', 'openclaw');
  const skillsDir = join(configDir, 'skills');
  const skillTarget = join(skillsDir, 'walvis');
  const extensionTarget = join(skillTarget, 'extensions', 'walvis-fastpath');
  const hooksTarget = join(skillTarget, 'hooks', 'openclaw');
  const dockerRuntime = openclawMode === 'docker';
  const pluginRuntimePath = dockerRuntime
    ? '/home/node/.openclaw/skills/walvis/extensions/walvis-fastpath'
    : extensionTarget;
  const hooksRuntimePath = dockerRuntime
    ? '/home/node/.openclaw/skills/walvis/hooks'
    : join(skillTarget, 'hooks');

  // Copy skill, plugin, and hook files into the mounted OpenClaw skill directory
  try {
    mkdirSync(skillsDir, { recursive: true });
    cpSync(skillSrc, skillTarget, { recursive: true });
    mkdirSync(join(skillTarget, 'extensions'), { recursive: true });
    mkdirSync(join(skillTarget, 'hooks'), { recursive: true });
    cpSync(extensionSrc, extensionTarget, { recursive: true });
    cpSync(hookSrc, hooksTarget, { recursive: true });
    console.log(chalk.green(`✓ Skill installed to ${skillTarget}`));
    console.log(chalk.green(`✓ Fast-path plugin installed to ${extensionTarget}`));
    console.log(chalk.green(`✓ Hook installed to ${hooksTarget}`));
  } catch (err) {
    console.log(chalk.yellow(`⚠ Could not copy WALVIS runtime files: ${err.message}`));
    return;
  }

  // Update openclaw.json
  const configPath = join(configDir, 'openclaw.json');
  try {
    let config = {};
    if (existsSync(configPath)) {
      config = JSON.parse(readFileSync(configPath, 'utf-8'));
    }

    config.skills = config.skills ?? {};
    config.skills.entries = config.skills.entries ?? {};
    config.skills.entries.walvis = {
      enabled: true,
      env: {
        WALVIS_LLM_API_KEY: llmApiKey,
        WALVIS_LLM_ENDPOINT: llmEndpoint,
        WALVIS_LLM_MODEL: llmModel,
      },
    };

    config.plugins = config.plugins ?? {};
    config.plugins.allow = Array.isArray(config.plugins.allow) ? config.plugins.allow : [];
    if (!config.plugins.allow.includes('walvis-fastpath')) config.plugins.allow.push('walvis-fastpath');
    config.plugins.load = config.plugins.load ?? {};
    const pluginPaths = Array.isArray(config.plugins.load.paths)
      ? config.plugins.load.paths.filter(Boolean)
      : [];
    const repoPluginPath = join(rootDir, 'extensions', 'walvis-fastpath');
    config.plugins.load.paths = pluginPaths
      .filter((entry) => entry !== repoPluginPath)
      .concat(pluginPaths.includes(pluginRuntimePath) ? [] : [pluginRuntimePath]);
    config.plugins.entries = config.plugins.entries ?? {};
    config.plugins.entries['walvis-fastpath'] = {
      ...(config.plugins.entries['walvis-fastpath'] ?? {}),
      enabled: true,
    };

    config.hooks = config.hooks ?? {};
    config.hooks.internal = config.hooks.internal ?? {};
    config.hooks.internal.enabled = true;
    config.hooks.internal.load = config.hooks.internal.load ?? {};
    const hookExtraDirs = Array.isArray(config.hooks.internal.load.extraDirs)
      ? config.hooks.internal.load.extraDirs.filter(Boolean)
      : [];
    const repoHookPath = join(rootDir, 'hooks');
    config.hooks.internal.load.extraDirs = hookExtraDirs
      .filter((entry) => entry !== repoHookPath)
      .concat(hookExtraDirs.includes(hooksRuntimePath) ? [] : [hooksRuntimePath]);
    config.hooks.internal.entries = config.hooks.internal.entries ?? {};
    config.hooks.internal.entries['walvis-message-handler'] = {
      ...(config.hooks.internal.entries['walvis-message-handler'] ?? {}),
      enabled: true,
    };

    // Enable Telegram inline buttons by default (only if not already configured)
    const channels = config.channels ?? {};
    const telegram = channels.telegram ?? {};
    let inlineButtonsConfigured = false;

    if (Array.isArray(telegram.capabilities)) {
      if (!telegram.capabilities.includes('inlineButtons')) {
        telegram.capabilities.push('inlineButtons');
        inlineButtonsConfigured = true;
      } else {
        inlineButtonsConfigured = true;
      }
    }

    if (telegram.capabilities && typeof telegram.capabilities === 'object' && !Array.isArray(telegram.capabilities)) {
      if (telegram.capabilities.inlineButtons) inlineButtonsConfigured = true;
      if (!telegram.capabilities.inlineButtons) {
        telegram.capabilities.inlineButtons = 'all';
        inlineButtonsConfigured = true;
      }
    }

    if (!telegram.capabilities) {
      telegram.capabilities = { inlineButtons: 'all' };
      inlineButtonsConfigured = true;
    }

    if (telegram.accounts && typeof telegram.accounts === 'object') {
      for (const account of Object.values(telegram.accounts)) {
        if (!account || typeof account !== 'object') continue;
        if (Array.isArray(account.capabilities)) {
          if (!account.capabilities.includes('inlineButtons')) {
            account.capabilities.push('inlineButtons');
            inlineButtonsConfigured = true;
          }
          continue;
        }
        account.capabilities = account.capabilities ?? {};
        if (typeof account.capabilities === 'object' && !account.capabilities.inlineButtons) {
          account.capabilities.inlineButtons = 'all';
          inlineButtonsConfigured = true;
        }
      }
    }

    channels.telegram = telegram;
    config.channels = channels;

    writeFileSync(configPath, JSON.stringify(config, null, 2));
    console.log(chalk.green(`✓ Updated ${configPath}`));
    if (inlineButtonsConfigured) {
      console.log(chalk.green('✓ Telegram inline buttons enabled (capabilities.inlineButtons = "all")'));
    }
  } catch (err) {
    console.log(chalk.yellow(`⚠ Could not update openclaw.json: ${err.message}`));
  }

  // Inject personality into SOUL.md
  if (workspaceDir) {
    const soulPath = join(workspaceDir, 'SOUL.md');
    const soulInjection = readFileSync(join(rootDir, 'templates', 'soul-injection.md'), 'utf-8');

    try {
      let existing = existsSync(soulPath) ? readFileSync(soulPath, 'utf-8') : '';
      if (!existing.includes('WALVIS')) {
        writeFileSync(soulPath, existing + '\n\n' + soulInjection);
        console.log(chalk.green('✓ Injected WALVIS personality into SOUL.md'));
      } else {
        console.log(chalk.gray('  WALVIS personality already in SOUL.md'));
      }
    } catch (err) {
      console.log(chalk.yellow(`⚠ Could not update SOUL.md: ${err.message}`));
    }
  }
}

main().catch((err) => {
  console.error('Setup failed:', err.message);
  process.exit(1);
});

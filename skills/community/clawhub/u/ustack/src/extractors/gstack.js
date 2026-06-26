import path from 'node:path';
import { readText, fileExists, readJson } from '../lib/fs.js';
import { emptyIR, emptySkill, emptyService, mergeIR } from '../lib/ir.js';
import { getHead } from '../lib/git.js';

/**
 * Extract gstack's structure into uStack IR format.
 * Focuses on:
 * - Skills/commands
 * - Core workflow graph
 * - Services (browser daemon)
 * - Install methods
 * - Portability classification
 */
export async function extractGstack({ repoDir, manifest }) {
  const ir = emptyIR(manifest.id);
  ir.upstreamId = manifest.id; // Re-confirm upstream ID from manifest
  ir.workspace.name = 'Gstack';
  ir.workspace.repoUrl = manifest.repoUrl;
  ir.workspace.description = 'gstack is my answer. I\'ve been building products for twenty years, and right now I\'m shipping more code than I ever have...';
  ir.workspace.license = 'MIT'; // Assume MIT based on repo

  const upstreamDir = repoDir; // gstack is cloned directly, not in a subdir of repoDir

  // --- Extract Skills ---
  const skillsDir = path.join(upstreamDir, 'skills');
  if (fileExists(skillsDir)) {
    const skillDirs = fs.readdirSync(skillsDir, { withFileTypes: true })
      .filter(d => d.isDirectory())
      .map(d => d.name);

    for (const skillId of skillDirs) {
      const skillPath = path.join(skillsDir, skillId, 'SKILL.md');
      if (fileExists(skillPath)) {
        const skillIR = await extractSkillIR({ skillId, skillPath, upstreamDir, manifest });
        ir.skills.push(skillIR);
      }
    }
  }

  // --- Extract Core Workflow Graph ---
  // Gstack's workflow is implicit in command sequence and docs.
  // We infer a basic graph based on common sprint steps.
  ir.workflow = {
    stages: [
      { id: 'think', name: 'Think' },
      { id: 'plan', name: 'Plan' },
      { id: 'build', name: 'Build' },
      { id: 'review', name: 'Review' },
      { id: 'test', name: 'Test' },
      { id: 'ship', name: 'Ship' },
      { id: 'reflect', name: 'Reflect' },
    ],
    edges: [
      { from: 'think', to: 'plan', artifact: 'design-doc' },
      // plan -> build implicitly
      { from: 'build', to: 'review', artifact: 'code-changes' },
      { from: 'review', to: 'test', artifact: 'code-changes' },
      { from: 'test', to: 'ship', artifact: 'test-report' },
      { from: 'ship', to: 'reflect', artifact: 'release-notes' },
      // Design skills feed into planning
      { from: 'design-consultation', to: 'plan', artifact: 'design-system' },
      { from: 'design-shotgun', to: 'plan', artifact: 'design-mockups' },
      { from: 'design-html', to: 'build', artifact: 'html-component' },
      // Review -> Ship loop
      { from: 'review', to: 'ship', artifact: 'review-report' },
      // CI/CD flow implied
    ],
  };

  // --- Extract Services ---
  // Gstack's browser daemon is the primary service
  const browserService = extractBrowserService(upstreamDir, manifest);
  ir.services.push(browserService);

  // --- Extract Install Methods ---
  extractInstallMethods(upstreamDir, ir);

  // --- Classify Portability ---
  classifyPortability(ir, upstreamDir);

  return ir;
}

async function extractSkillIR({ skillId, skillPath, upstreamDir, manifest }) {
  const skillIR = emptySkill(skillId);
  skillIR.sourceFile = path.relative(upstreamDir, skillPath);
  skillIR.portability = 'portable'; // Default, refined below

  const content = readText(skillPath);
  const lines = content.split('\n');

  // Parse metadata from SKILL.md header or frontmatter
  let meta = {};
  if (content.includes('---')) {
    const frontmatter = content.split('---')[1];
    try {
      const fmLines = frontmatter.split('\n');
      meta = fmLines.reduce((acc, line) => {
        const parts = line.split(':');
        if (parts.length >= 2) {
          const key = parts[0].trim();
          const value = parts.slice(1).join(':').trim();
          if (key && value) acc[key] = value;
        }
        return acc;
      }, {});
    } catch (e) {
      console.warn(`Could not parse frontmatter for ${skillPath}: ${e.message}`);
    }
  }

  skillIR.name = meta.name || skillId.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
  skillIR.trigger = meta.trigger || `/${skillId}`;
  skillIR.description = meta.description || '';
  skillIR.category = meta.category || 'workflow'; // Default to workflow
  skillIR.safetyLevel = meta.safety || 'safe';
  skillIR.requiredTools = meta.tools || [];
  skillIR.hostNotes = {}; // To be filled by classification

  // Try to infer Host Specificity from SKILL.md comments/content
  if (content.includes('Claude Code-specific') || content.includes('Claude only')) {
    skillIR.hostNotes['claude-code'] = 'Content suggests Claude Code specific interaction';
    skillIR.portability = 'host-specific';
  } else if (content.includes('Codex specific') || content.includes('Codex only')) {
    skillIR.hostNotes['codex'] = 'Content suggests Codex specific interaction';
    skillIR.portability = 'host-specific';
  } else if (content.includes('OpenClaw specific') || content.includes('OpenClaw only')) {
    skillIR.hostNotes['openclaw'] = 'Content suggests OpenClaw specific interaction';
    skillIR.portability = 'host-specific';
  }

  // Infer artifacts
  const produced = meta.produces?.split(',').map(p => p.trim()).filter(Boolean) || [];
  const consumed = meta.consumes?.split(',').map(p => p.trim()).filter(Boolean) || [];
  skillIR.downstreamArtifacts = produced;
  skillIR.upstreamArtifacts = consumed;

  // Infer prototype code link from SKILL.md if available
  const prototypeMatch = content.match(/prototype: `([^`]+)`/);
  if (prototypeMatch && prototypeMatch[1]) {
    skillIR.purpose = `Prototype available: ${prototypeMatch[1]}`;
  }

  return skillIR;
}

function extractBrowserService(repoDir, manifest) {
  const serviceIR = emptyService('browser');
  serviceIR.name = 'Browser Daemon';
  serviceIR.description = 'Persistent Chromium instance for browser automation';
  serviceIR.type = 'daemon';
  serviceIR.protocol = 'http';
  serviceIR.portRange = '10000-60000'; // Dynamic port selection
  serviceIR.auth = 'bearer-token';
  serviceIR.hostSpecific = true; // Browser interact requires specific runtime environment

  // Infer start command and state file from gstack's ARCHITECTURE.md and bin/
  const architecturePath = path.join(repoDir, 'ARCHITECTURE.md');
  const binaryPath = path.join(repoDir, 'bin', 'gstack'); // Assuming compiled binary name
  const stateFileBase = '.gstack/browse.json'; // Common convention

  if (fileExists(architecturePath)) {
    const archContent = readText(architecturePath);
    const match = archContent.match(/`([^`]+)`.*to\s*localhost:PORT/s); // Crude extraction
    if (match && match[1]) {
      serviceIR.startCommand = match[1].replace('localhost:PORT', 'localhost:{{PORT}}'); // Placeholder
    }
  }

  // If binaryPath exists, reference it as the executable
  if (fileExists(binaryPath)) {
    serviceIR.startCommand = serviceIR.startCommand || `./bin/gstack --host browser`; // Fallback start command
  } else {
    // Fallback if binary not found directly, use generic command
    serviceIR.startCommand = serviceIR.startCommand || './run-browser-daemon.sh';
  }

  serviceIR.stateFile = stateFileBase;

  return serviceIR;
}

function extractInstallMethods(repoDir, ir) {
  // Primitive detection based on common install scripts / docs
  const installMethods = [];

  // Method 1: Repo-local install (typical for Claude Code skills)
  if (fileExists(path.join(repoDir, '.claude/skills/gstack'))) {
    installMethods.push({
      id: 'repo-local-claude',
      description: 'Install gstack skills within the project\'s .claude/ directory',
      targetPath: '.claude/skills/gstack',
      steps: [
        'Clone the gstack repository',
        'Run `./setup` within the cloned directory',
        'Add gstack section to project\'s CLAUDE.md',
      ],
      perRepoSupported: true,
      userGlobalSupported: false,
    });
  }

  // Method 2: User-global install (typical for CLI tools)
  if (fileExists(path.join(repoDir, 'bin/gstack')) || fileExists(path.join(repoDir, 'setup'))) {
    installMethods.push({
      id: 'user-global-cli',
      description: 'Install gstack CLI globally for user account',
      targetPath: '~/.gstack', // Convention based on ARCITECTURE.md
      steps: [
        'Clone the gstack repository to e.g. ~/.gstack',
        'Run `./setup --host auto` (or specify codex/factory)',
      ],
      perRepoSupported: false,
      userGlobalSupported: true,
    });
  }

  ir.install.methods = installMethods;
  ir.install.bootstrapCommand = './setup'; // Default common command
}

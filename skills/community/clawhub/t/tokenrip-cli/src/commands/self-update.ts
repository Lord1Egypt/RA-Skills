import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { loadConfig, saveConfig, CONFIG_DIR } from '../config.js';
import { fetchManifest, getCurrentVersion } from '../update-check.js';
import { outputSuccess } from '../output.js';
import { formatSelfUpdate } from '../formatters.js';

async function saveSkillFile(skillUrl: string): Promise<{ path: string; changed: boolean } | null> {
  try {
    const res = await fetch(skillUrl);
    if (!res.ok) return null;
    const newContent = await res.text();
    const skillPath = path.join(CONFIG_DIR, 'SKILL.md');
    let existing = '';
    try { existing = fs.readFileSync(skillPath, 'utf-8'); } catch {}
    const changed = newContent !== existing;
    if (changed) {
      fs.mkdirSync(CONFIG_DIR, { recursive: true });
      fs.writeFileSync(skillPath, newContent, 'utf-8');
    }
    return { path: skillPath, changed };
  } catch {
    return null;
  }
}

export async function selfUpdate(): Promise<void> {
  const currentVersion = getCurrentVersion();
  const manifest = await fetchManifest();

  if (!manifest) {
    outputSuccess({
      status: 'failed',
      version: currentVersion,
      message: 'Could not check for updates: manifest unavailable. Check your network connection.',
    }, formatSelfUpdate);
    return;
  }

  const config = loadConfig();
  try {
    saveConfig({ ...config, lastUpdateCheck: new Date().toISOString(), latestVersion: manifest.version });
  } catch {}

  if (manifest.version === currentVersion) {
    const skillPath = path.join(CONFIG_DIR, 'SKILL.md');
    const skillExists = fs.existsSync(skillPath);
    outputSuccess({
      status: 'current',
      version: currentVersion,
      skill_file_path: skillExists ? skillPath : null,
      message: skillExists
        ? `@tokenrip/cli ${currentVersion} is already current. Skill file: ${skillPath}`
        : `@tokenrip/cli ${currentVersion} is already current.`,
    }, formatSelfUpdate);
    return;
  }

  const targetVersion = manifest.version;

  try {
    execFileSync('npm', ['install', '-g', `@tokenrip/cli@${targetVersion}`], { stdio: 'inherit' });
  } catch {
    outputSuccess({
      status: 'failed',
      version: currentVersion,
      targetVersion,
      message: `Update failed. Try running with sudo:\n  sudo npm install -g @tokenrip/cli@${targetVersion}`,
    }, formatSelfUpdate);
    return;
  }

  const skill = await saveSkillFile(manifest.skill_url);

  const skillNote = skill
    ? `Skill file ${skill.changed ? 'refreshed' : 'already current'}: ${skill.path}`
    : `Reload your skill: npx skills add tokenrip/cli`;

  outputSuccess({
    status: 'updated',
    from: currentVersion,
    to: targetVersion,
    skill_url: manifest.skill_url,
    skill_file_path: skill ? skill.path : null,
    skill_changed: skill ? skill.changed : false,
    message: manifest.message ?? `Updated @tokenrip/cli ${currentVersion} → ${targetVersion}. ${skillNote}.`,
  }, formatSelfUpdate);
}

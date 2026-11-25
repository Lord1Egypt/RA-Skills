import path from 'node:path';
import os from 'node:os';
import fs from 'node:fs/promises';

import { OpenClawSkill, SkillContext } from '@openclaw/sdk';
import { VettrEngine } from './vettr-engine.js';
import { ToolsInterface, VettingConfig, VettingReport } from './types.js';
import {
  sanitiseSlug,
  sanitiseUrl,
  sanitisePath,
  getAllowedRoots,
} from './utils/sanitise.js';
import { execSafe } from './utils/exec-safe.js';
import { assertGitSupportsResolvePin, assertTreeWithinLimit, downloadPublicHttps, gitResolvePin, gunzipCapped, resolvePublicHost } from './utils/safe-fetch.js';

const DEFAULT_CONFIG: VettingConfig = {
  maxNetworkCalls: 5,
  allowedHosts: [
    'api.openai.com',
    'api.anthropic.com',
    'registry.npmjs.org',
    'api.github.com',
    'raw.githubusercontent.com',
  ],
  blockObfuscation: true,
  requireAuthor: true,
  maxRiskScore: 50,
  checkTyposquatting: true,
  maliciousPatternsRefreshHours: 24,
  blockedAuthors: [],
  blockedPackages: [],
  typosquatTargets: [],
};

export default class SkillVettr implements OpenClawSkill {
  name = 'skill-vettr';
  version = '2.0.8';
  description = 'Security vetting for third-party OpenClaw skills';

  private config: VettingConfig = DEFAULT_CONFIG;
  private engine!: VettrEngine;

  async onLoad(ctx: SkillContext): Promise<void> {
    // Merge user config with defaults
    const userConfig = ctx.config.get<Partial<VettingConfig>>('skill-vettr', {});
    this.config = { ...DEFAULT_CONFIG, ...userConfig };
    this.engine = new VettrEngine(this.config);

    // Register: /skill:vet --path <local-path>
    ctx.commands.register('/skill:vet', async (args) => {
      const skillPath = args['path'] ?? args['source'];

      if (!skillPath || typeof skillPath !== 'string') {
        return 'Usage: /skill:vet --path <directory>';
      }

      try {
        const sanitisedPath = sanitisePath(skillPath, getAllowedRoots({ allowCwd: this.config.allowCwd }));

        ctx.ui.showProgress('Analysing skill...');
        const report = await this.engine.vetSkill(sanitisedPath, ctx.tools);

        return this.handleReport(report, ctx);
      } catch (err) {
        return `Vetting failed: ${err instanceof Error ? err.message : 'Unknown error'}`;
      }
    });

    // Register: /skill:vet-url --url <https://...>
    ctx.commands.register('/skill:vet-url', async (args) => {
      const url = args['url'];

      if (!url || typeof url !== 'string') {
        return 'Usage: /skill:vet-url --url <https://...>';
      }

      let tempDir: string | null = null;

      try {
        const sanitisedUrl = sanitiseUrl(url);
        tempDir = await ctx.tools.mkdtemp(path.join(os.tmpdir(), 'skill-vettr-'));

        ctx.ui.showProgress(`Downloading from ${sanitisedUrl}...`);

        // Download using safe exec
        if (sanitisedUrl.endsWith('.git')) {
          const parsedGitUrl = new URL(sanitisedUrl);
          if (parsedGitUrl.port && parsedGitUrl.port !== '443') {
            throw new Error('Git URLs must use the default HTTPS port');
          }
          const { stdout: gitVersion } = await execSafe('git', ['--version']);
          assertGitSupportsResolvePin(gitVersion);
          const addresses = await resolvePublicHost(parsedGitUrl.hostname);
          await execSafe('git', [
            '-c', 'core.hooksPath=/dev/null',
            '-c', 'http.followRedirects=false',
            '-c', 'protocol.allow=never',
            '-c', 'protocol.https.allow=always',
            'clone', '--depth', '1', sanitisedUrl, tempDir,
          ], {
            // Ignore user and system git config so url.insteadOf rewrites, proxies and
            // credential helpers cannot redirect the clone or attach credentials.
            // The pin goes through GIT_CONFIG_* because a bracketed IPv6 entry would fail execSafe's
            // argument check.
            env: {
              GIT_CONFIG_NOSYSTEM: '1',
              GIT_CONFIG_GLOBAL: '/dev/null',
              GIT_TERMINAL_PROMPT: '0',
              GIT_CONFIG_COUNT: '1',
              GIT_CONFIG_KEY_0: 'http.curloptResolve',
              GIT_CONFIG_VALUE_0: gitResolvePin(parsedGitUrl.hostname, addresses),
            },
          });
        } else {
          const tarPath = path.join(tempDir, 'skill.tar.gz');
          const tarballPath = path.join(tempDir, 'skill.tar');
          await downloadPublicHttps(sanitisedUrl, tarPath);
          await gunzipCapped(tarPath, tarballPath);
          await fs.rm(tarPath, { force: true });
          await execSafe('tar', ['-xf', tarballPath, '-C', tempDir, '--no-same-owner', '--no-same-permissions']);
          await fs.rm(tarballPath, { force: true });
        }
        await assertTreeWithinLimit(tempDir);

        // Validate that downloaded content is actually a skill
        const hasManifest = await findSkillManifest(tempDir, ctx.tools);
        if (!hasManifest) {
          throw new Error('Downloaded content is not a valid OpenClaw skill: no SKILL.md found');
        }

        ctx.ui.showProgress('Analysing skill...');
        const report = await this.engine.vetSkill(tempDir, ctx.tools);

        return this.handleReport(report, ctx);
      } catch (err) {
        return `Vetting failed: ${err instanceof Error ? err.message : 'Unknown error'}`;
      } finally {
        // Cleanup
        if (tempDir) {
          await ctx.tools.rm(tempDir, { recursive: true, force: true }).catch(() => {});
        }
      }
    });

    // Register: /skill:vet-clawhub --skill <slug>
    ctx.commands.register('/skill:vet-clawhub', async (args) => {
      const slug = args['skill'];

      if (!slug || typeof slug !== 'string') {
        return 'Usage: /skill:vet-clawhub --skill <slug>';
      }

      let tempDir: string | null = null;

      try {
        const sanitisedSlug = sanitiseSlug(slug);
        // Use mkdtemp to create directory (clawhub CLI may not auto-create output dir)
        tempDir = await ctx.tools.mkdtemp(path.join(os.tmpdir(), 'skill-vettr-'));

        ctx.ui.showProgress(`Fetching "${sanitisedSlug}" from ClawHub...`);

        await execSafe('clawhub', ['download', sanitisedSlug, '--output', tempDir]);

        // Validate that downloaded content is actually a skill
        const hasManifest = await findSkillManifest(tempDir, ctx.tools);
        if (!hasManifest) {
          throw new Error('Downloaded content is not a valid OpenClaw skill: no SKILL.md found');
        }

        ctx.ui.showProgress('Analysing skill...');
        const report = await this.engine.vetSkill(tempDir, ctx.tools);

        return this.handleReport(report, ctx);
      } catch (err) {
        return `Vetting failed: ${err instanceof Error ? err.message : 'Unknown error'}`;
      } finally {
        // Cleanup
        if (tempDir) {
          await ctx.tools.rm(tempDir, { recursive: true, force: true }).catch(() => {});
        }
      }
    });

    // Auto-vet hook (if enabled)
    const autoVet = ctx.config.get<boolean>('skill-vettr.autoVet', false);
    if (autoVet) {
      ctx.hooks.on('skill:pre-install', async (event) => {
        try {
          const report = await this.engine.vetSkill(event.skillPath, ctx.tools);

          if (report.recommendation === 'BLOCK') {
            event.preventDefault();
            ctx.ui.notify(
              `🚫 Installation blocked: ${report.findings[0]?.message ?? 'Critical risk detected'}`
            );
            return;
          }

          if (report.recommendation === 'REVIEW') {
            const approved = await ctx.ui.confirm(
              `⚠️ Skill "${report.skillName}" flagged (score: ${report.riskScore}/100). Install anyway?`
            );
            if (!approved) {
              event.preventDefault();
            }
          }
        } catch (err) {
          event.preventDefault();
          ctx.ui.notify(`Vetting error: ${err instanceof Error ? err.message : 'Unknown'}`);
        }
      });
    }
  }

  private async handleReport(report: VettingReport, ctx: SkillContext): Promise<string> {
    const output = this.formatReport(report);

    if (report.recommendation === 'REVIEW') {
      const approved = await ctx.ui.confirm(
        `⚠️ Skill "${report.skillName}" requires review (score: ${report.riskScore}/100). Approve?`
      );
      return approved ? output + '\n\n✅ User approved' : output + '\n\n❌ User rejected';
    }

    if (report.recommendation === 'BLOCK') {
      return output + '\n\n🚫 Installation BLOCKED - critical security risks detected';
    }

    return output + '\n\n✅ Skill passed vetting';
  }

  private formatReport(report: VettingReport): string {
    const lines = [
      ``,
      `┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓`,
      `┃  SKILL VETTING REPORT                                     ┃`,
      `┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛`,
      ``,
      `  Skill:          ${report.skillName}`,
      `  Risk Score:     ${report.riskScore}/100`,
      `  Risk Level:     ${this.formatRiskLevel(report.riskLevel)}`,
      `  Recommendation: ${this.formatRecommendation(report.recommendation)}`,
      `  Vetted At:      ${report.vettedAt}`,
      `  Vettr Version:  ${report.vettrVersion}`,
      ``,
      `┌─ Metadata ─────────────────────────────────────────────────`,
      `│  Author Verified:     ${report.metadata.authorVerified ? '✓ Yes' : '✗ No'}`,
      `│  External Deps:       ${report.metadata.hasExternalDeps ? '⚠ Yes' : '✓ No'}`,
      `│  Network Calls:       ${report.metadata.networkCalls.length}`,
      `│  Files Analysed:      ${report.metadata.fileCount}`,
      `│  Total Lines:         ${report.metadata.totalLines}`,
      `│  Checksum (SHA-256):  ${report.metadata.checksumSha256 ? report.metadata.checksumSha256.substring(0, 16) + '...' : 'N/A'}`,
      `└─────────────────────────────────────────────────────────────`,
      ``,
    ];

    // Network calls detail
    if (report.metadata.networkCalls.length > 0) {
      lines.push(`┌─ Network Calls ────────────────────────────────────────────`);
      for (const call of report.metadata.networkCalls.slice(0, 10)) {
        const status = call.allowed ? '✓' : '✗';
        const urlDisplay = call.url.length > 50 ? call.url.substring(0, 47) + '...' : call.url;
        lines.push(`│  ${status} ${urlDisplay}`);
      }
      if (report.metadata.networkCalls.length > 10) {
        lines.push(`│  ... and ${report.metadata.networkCalls.length - 10} more`);
      }
      lines.push(`└─────────────────────────────────────────────────────────────`);
      lines.push(``);
    }

    // Findings
    if (report.findings.length > 0) {
      lines.push(`┌─ Findings (${report.findings.length}) ─────────────────────────────────────────`);

      const bySeverity = {
        CRITICAL: report.findings.filter((f) => f.severity === 'CRITICAL'),
        WARNING: report.findings.filter((f) => f.severity === 'WARNING'),
        INFO: report.findings.filter((f) => f.severity === 'INFO'),
      };

      for (const [severity, findings] of Object.entries(bySeverity)) {
        if (findings.length === 0) continue;

        lines.push(`│`);
        lines.push(`│  [${severity}] (${findings.length})`);

        for (const f of findings.slice(0, 5)) {
          lines.push(`│    • ${f.category}: ${f.message}`);
          lines.push(`│      File: ${f.file}${f.line ? `:${f.line}` : ''}`);
          if (f.cwe) {
            lines.push(`│      Ref: ${f.cwe}`);
          }
          lines.push(`│      Evidence: ${f.evidence}`);
        }

        if (findings.length > 5) {
          lines.push(`│    ... and ${findings.length - 5} more ${severity} findings`);
        }
      }

      lines.push(`└─────────────────────────────────────────────────────────────`);
    } else {
      lines.push(`┌─ Findings ─────────────────────────────────────────────────`);
      lines.push(`│  ✓ No security findings detected`);
      lines.push(`└─────────────────────────────────────────────────────────────`);
    }

    return lines.join('\n');
  }

  private formatRiskLevel(level: VettingReport['riskLevel']): string {
    const icons: Record<VettingReport['riskLevel'], string> = {
      SAFE: '🟢 SAFE',
      LOW: '🟡 LOW',
      MEDIUM: '🟠 MEDIUM',
      HIGH: '🔴 HIGH',
      CRITICAL: '⛔ CRITICAL',
    };
    return icons[level];
  }

  private formatRecommendation(rec: VettingReport['recommendation']): string {
    const icons: Record<VettingReport['recommendation'], string> = {
      INSTALL: '✓ INSTALL',
      REVIEW: '⚠ REVIEW',
      BLOCK: '🚫 BLOCK',
    };
    return icons[rec];
  }
}

/**
 * Checks for a SKILL.md file at the root of a directory or one level deep (case-insensitive).
 * Tar archives often extract into a subfolder, so we check one level of subdirectories.
 */
export async function findSkillManifest(dir: string, tools: ToolsInterface): Promise<boolean> {
  const entries = await tools.readdir(dir);

  // Check root level
  if (entries.some((e) => e.toLowerCase() === 'skill.md')) {
    return true;
  }

  // Check one level deep (subdirectories only)
  for (const entry of entries) {
    const entryPath = path.join(dir, entry);
    try {
      const st = await tools.lstat(entryPath);
      if (st.isDirectory()) {
        const subEntries = await tools.readdir(entryPath);
        if (subEntries.some((e) => e.toLowerCase() === 'skill.md')) {
          return true;
        }
      }
    } catch {
      // Skip entries that can't be stat'd
    }
  }

  return false;
}

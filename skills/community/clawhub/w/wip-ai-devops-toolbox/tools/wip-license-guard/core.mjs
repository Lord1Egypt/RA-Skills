// wip-license-guard/core.mjs
// License generation and validation logic.
// Reads templates from ai/wip-templates/readme/ when available.
// Falls back to hardcoded defaults for standalone use.

import { existsSync, readFileSync } from 'node:fs';
import { join, dirname } from 'node:path';

// ── Template Resolution ─────────────────────────────────────────────

/**
 * Find the templates directory. Checks:
 * 1. WIP_TEMPLATES_DIR env var
 * 2. Walk up from repoPath looking for ai/wip-templates/readme/
 * 3. Walk up from this file's location (for toolbox-internal use)
 * Returns null if not found.
 */
function findTemplatesDir(repoPath) {
  // 1. Env var
  const envDir = process.env.WIP_TEMPLATES_DIR;
  if (envDir && existsSync(join(envDir, 'LICENSE.md'))) return envDir;

  // 2. Walk up from repoPath
  if (repoPath) {
    let dir = repoPath;
    for (let i = 0; i < 10; i++) {
      const candidate = join(dir, 'ai', 'wip-templates', 'readme');
      if (existsSync(join(candidate, 'LICENSE.md'))) return candidate;
      const parent = dirname(dir);
      if (parent === dir) break;
      dir = parent;
    }
  }

  // 3. Walk up from this file (tools/wip-license-guard/ -> repo root)
  const thisDir = dirname(new URL(import.meta.url).pathname);
  let dir = thisDir;
  for (let i = 0; i < 10; i++) {
    const candidate = join(dir, 'ai', 'wip-templates', 'readme');
    if (existsSync(join(candidate, 'LICENSE.md'))) return candidate;
    const parent = dirname(dir);
    if (parent === dir) break;
    dir = parent;
  }

  return null;
}

/**
 * Read a template file. Returns content or null.
 */
function readTemplate(templatesDir, filename) {
  if (!templatesDir) return null;
  const path = join(templatesDir, filename);
  if (!existsSync(path)) return null;
  return readFileSync(path, 'utf8');
}

/**
 * Extract the markdown format section from wip-lic-footer.md.
 * The file has two sections: // PLAIN TXT and // MD FORMAT.
 * Returns the MD FORMAT section, or the whole file if no marker found.
 */
function extractMdFormat(content) {
  const marker = '// MD FORMAT';
  const idx = content.indexOf(marker);
  if (idx === -1) return content;
  return content.slice(idx + marker.length).trim();
}

// ── License Generation ──────────────────────────────────────────────

export function generateLicense(config, repoPath) {
  const { copyright, license, year } = config;

  if (license === 'MIT') return generateMIT(copyright, year);
  if (license === 'AGPL-3.0') return generateAGPL(copyright, year);
  if (license === 'MIT+AGPL') return generateDual(copyright, year, repoPath);

  return generateMIT(copyright, year);
}

function generateMIT(copyright, year) {
  return `MIT License

Copyright (c) ${year} ${copyright}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
`;
}

function generateAGPL(copyright, year) {
  return `GNU Affero General Public License v3.0

Copyright (c) ${year} ${copyright}

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
`;
}

function generateDual(copyright, year, repoPath) {
  // Try template first
  const templatesDir = findTemplatesDir(repoPath);
  const template = readTemplate(templatesDir, 'LICENSE.md');
  if (template) {
    // Replace copyright year if template has a different one
    return template.replace(/Copyright \(c\) \d{4}/, `Copyright (c) ${year}`);
  }

  // Hardcoded fallback
  return `Dual License: MIT + AGPLv3

Copyright (c) ${year} ${copyright}


1. MIT License (local and personal use)
---------------------------------------

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


2. GNU Affero General Public License v3.0 (commercial and cloud use)
--------------------------------------------------------------------

If you run this software as part of a hosted service, cloud platform,
marketplace listing, or any network-accessible offering for commercial
purposes, the AGPLv3 terms apply. You must either:

  a) Release your complete source code under AGPLv3, or
  b) Obtain a commercial license.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.


AGPLv3 for personal use is free. Commercial licenses available.
`;
}

// ── CLA Generation ──────────────────────────────────────────────────

export function generateCLA(repoPath) {
  // Try template first
  const templatesDir = findTemplatesDir(repoPath);
  const template = readTemplate(templatesDir, 'cla.md');
  if (template) return template;

  // Hardcoded fallback
  return `###### WIP Computer

# Contributor License Agreement

By submitting a pull request to this repository, you agree to the following:

1. **You grant WIP Computer, Inc. a perpetual, worldwide, non-exclusive, royalty-free, irrevocable license** to use, reproduce, modify, distribute, sublicense, and otherwise exploit your contribution under any license, including commercial licenses.

2. **You retain copyright** to your contribution. This agreement does not transfer ownership. You can use your own code however you want.

3. **You confirm** that your contribution is your original work, or that you have the right to submit it under these terms.

4. **You understand** that your contribution may be used in both open source and commercial versions of this software.

This is standard open source governance. Apache, Google, Meta, and Anthropic all use similar agreements. The goal is simple: keep the tools free for everyone while allowing WIP Computer, Inc. to offer commercial licenses to companies that need them.

Using these tools to build your own software is always free. This agreement only matters if WIP Computer, Inc. needs to relicense the codebase commercially.

If you have questions, open an issue or reach out.
`;
}

// ── README License Block ────────────────────────────────────────────

export function generateReadmeBlock(config, repoPath) {
  const { license, attribution } = config;

  if (license === 'MIT') {
    return `## License

MIT.${attribution ? ' ' + attribution : ''}
`;
  }

  if (license === 'AGPL-3.0') {
    return `## License

AGPLv3. AGPLv3 for personal use is free.${attribution ? '\n\n' + attribution : ''}
`;
  }

  // MIT+AGPL: try template first
  const templatesDir = findTemplatesDir(repoPath);
  const footer = readTemplate(templatesDir, 'wip-lic-footer.md');
  if (footer) {
    return extractMdFormat(footer);
  }

  // Hardcoded fallback
  return `## License

Dual-license model designed to keep tools free while preventing commercial resellers.

\`\`\`
MIT      All CLI tools, MCP servers, skills, and hooks (use anywhere, no restrictions).
AGPLv3   Commercial redistribution, marketplace listings, or bundling into paid services.
\`\`\`

AGPLv3 for personal use is free. Commercial licenses available.

### Can I use this?

**Yes, freely:**
- Use any tool locally or on your own servers
- Modify the code for your own projects
- Include in your internal CI/CD pipelines
- Fork it and send us feedback via PRs (we'd love that)

**Need a commercial license:**
- Bundle into a product you sell
- List on a marketplace (VS Code, JetBrains, etc.)
- Offer as part of a hosted/SaaS platform
- Redistribute commercially

Using these tools to build your own software is fine. Reselling the tools themselves is what requires a commercial license.

By submitting a PR, you agree to the [Contributor License Agreement](CLA.md).
${attribution ? '\n' + attribution : ''}`;
}

// ── README License Section Replace/Remove ───────────────────────────

/**
 * Replace ## License section in readme content.
 * If no ## License exists, appends the block at the end.
 * Returns the updated content.
 */
export function replaceReadmeLicenseSection(content, config, repoPath) {
  const block = generateReadmeBlock(config, repoPath);

  // Match from "## License" to the next ## heading or end of file
  const licenseRegex = /## License[\s\S]*?(?=\n## [^#]|\n---\s*$|$)/;
  if (licenseRegex.test(content)) {
    return content.replace(licenseRegex, block.trimEnd());
  }

  // No license section found, append
  return content.trimEnd() + '\n\n' + block;
}

/**
 * Remove ## License section from content (for sub-tool READMEs).
 * Returns the updated content.
 */
export function removeReadmeLicenseSection(content) {
  // Match from "## License" to the next ## heading or end of file
  const licenseRegex = /\n## License[\s\S]*?(?=\n## [^#]|$)/;
  return content.replace(licenseRegex, '').trimEnd() + '\n';
}

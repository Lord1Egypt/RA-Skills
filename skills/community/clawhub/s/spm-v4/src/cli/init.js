/**
 * SPM v4 — CLI handler for `spm init <project-name>`.
 *
 * Initializes a new SPM project structure, creating the ledger file,
 * event store directory, attestation directory, and default config.
 *
 * @module cli/init
 */

import { mkdirSync, writeFileSync, existsSync } from 'node:fs';
import { resolve as resolvePath, join } from 'node:path';
import { Engine } from '../engine/index.js';
import { requireConfig } from '../config/loader.js';
import { validate, CLIInputSchema } from '../validation.js';

// ──────────────────────────────────────────────
// Constants
// ──────────────────────────────────────────────

/** Default project structure created by `spm init`. */
const DEFAULT_FILE_TREE = {
  'docs/spm': ['ledger.md'],
  '.spm': ['.gitkeep'],
  'event-store-data': ['.gitkeep'],
};

/**
 * Template content for a fresh WBS ledger.
 *
 * @param {string} projectName
 * @returns {string}
 */
function ledgerTemplate(projectName) {
  return `# SPM WBS Ledger — ${projectName}

## WB-001: Initialize project context
- **Status**: done
- **Dependencies**: none
- **Context**: Establish project foundation, tool configuration, and initial context
- **Exit Criteria**: Project scaffolded and ready for requirement gathering
- **Evidence**: Project initialized via \`spm init\`

## WB-002: Gather requirements
- **Status**: todo
- **Dependencies**: WB-001
- **Context**: Collect stakeholder requirements and define scope
- **Exit Criteria**: Requirements documented and validated
- **Evidence**: 

## WB-003: Create plan and WBS
- **Status**: todo
- **Dependencies**: WB-001
- **Context**: Break down requirements into actionable tasks
- **Exit Criteria**: Complete WBS with all tasks assigned
- **Evidence**: 
`;
}

// ──────────────────────────────────────────────
// Handler
// ──────────────────────────────────────────────

/**
 * Run `spm init`.
 *
 * Creates the project structure, ledger, config, and initializes
 * the SPM engine in the "context-init" phase.
 *
 * @param {string} [projectName] — Project name
 * @returns {Promise<number>} Exit code
 */
export async function initCommand(projectName) {
  if (!projectName) {
    console.error('Error: project name is required');
    console.error('Usage: spm init <project-name>');
    return 1;
  }

  // Zod validation: ensure project name is safe and well-formed
  try {
    validate(CLIInputSchema, { projectName }, 'project name');
  } catch (err) {
    console.error(`Error: ${err.message}`);
    return 1;
  }

  const root = process.cwd();

  console.log(`\n  🚀  Initializing SPM project: "${projectName}"\n`);

  // Create directory structure and files
  for (const [dir, files] of Object.entries(DEFAULT_FILE_TREE)) {
    const dirPath = resolvePath(root, dir);
    if (!existsSync(dirPath)) {
      mkdirSync(dirPath, { recursive: true });
      console.log(`  ✓  Created directory: ${dir}`);
    } else {
      console.log(`  ·  Directory exists: ${dir}`);
    }

    for (const file of files) {
      if (file === '.gitkeep') continue;
      const filePath = resolvePath(dirPath, file);
      if (!existsSync(filePath)) {
        let content = '';
        if (file === 'ledger.md') {
          content = ledgerTemplate(projectName);
        }
        writeFileSync(filePath, content, 'utf-8');
        console.log(`  ✓  Created file: ${dir}/${file}`);
      } else {
        console.log(`  ·  File exists: ${dir}/${file}`);
      }
    }
  }

  // Load config
  let config;
  try {
    config = requireConfig();
    console.log(`  ✓  Config loaded from: ${config.wbs.ledger_path}`);
  } catch (err) {
    // Default config works without a file
    const { loadConfig } = await import('../config/loader.js');
    const result = loadConfig();
    config = result.config || result.config;
    console.log(`  ·  Using default config (no config file found)`);
  }

  // Initialize engine
  try {
    const engine = new Engine({
      phases: config.engine?.lifecycle?.phases
        ? Object.fromEntries(
            config.engine.lifecycle.phases.map((p) => [p.name, p]),
          )
        : undefined,
      context: { projectName },
    });

    engine.phase('context-init', { projectName });
    console.log(`  ✓  Engine initialized — phase: ${engine.currentPhase().name}\n`);
    console.log(`  ✨  Project "${projectName}" initialized successfully!\n`);
    return 0;
  } catch (err) {
    console.error(`  ✗  Engine initialization failed: ${err.message}`);
    return 1;
  }
}
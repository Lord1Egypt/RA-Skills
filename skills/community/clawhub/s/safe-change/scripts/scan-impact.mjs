#!/usr/bin/env node
/**
 * scan-impact.mjs — Safe Change Impact Analyzer
 * Analysiert den Blast-Radius einer Zieldatei: Importers, Routes, Tests, ENV, Migrations.
 * Nutzt ausschliesslich Node.js Stdlib + Regex (keine externen Packages).
 * Read-only — modifiziert keine Quelldateien.
 *
 * Usage:
 *   node scan-impact.mjs <target-file> [--root <project-root>] [--json]
 *   node scan-impact.mjs --help
 */

import { readFile, readdir, stat } from 'node:fs/promises';
import { resolve, relative, join, dirname } from 'node:path';
import { existsSync } from 'node:fs';

// ---- CLI ---------------------------------------------------------------

const args = process.argv.slice(2);

if (args.includes('--help') || args.length === 0) {
  printHelp();
  process.exit(0);
}

const targetArg = args.find((a) => !a.startsWith('--'));
const rootFlagIdx = args.indexOf('--root');
const projectRoot = rootFlagIdx !== -1 ? resolve(args[rootFlagIdx + 1]) : process.cwd();
const jsonOnly = args.includes('--json');

if (!targetArg) {
  console.error('Error: target file argument required. Run with --help for usage.');
  process.exit(1);
}

const targetFile = resolve(targetArg);

// Sicherstellen dass die Zieldatei existiert
if (!existsSync(targetFile)) {
  console.error(`Error: target file not found: ${targetFile}`);
  process.exit(1);
}

const targetRelative = relative(projectRoot, targetFile);

// ---- Hilfsfunktionen ----------------------------------------------------

/** Rekursives Einlesen aller .ts/.tsx Dateien eines Verzeichnisses */
async function collectTsFiles(dir) {
  /** @type {string[]} */
  const results = [];
  let entries;
  try {
    entries = await readdir(dir, { withFileTypes: true });
  } catch {
    return results;
  }
  for (const entry of entries) {
    // node_modules, .git, dist, .next, out ueberspringen
    if (['node_modules', '.git', 'dist', '.next', 'out', 'build', 'coverage'].includes(entry.name)) continue;
    const full = join(dir, entry.name);
    if (entry.isDirectory()) {
      results.push(...(await collectTsFiles(full)));
    } else if (entry.isFile() && /\.(ts|tsx)$/.test(entry.name)) {
      results.push(full);
    }
  }
  return results;
}

/** Prueft ob eine Datei das Ziel importiert (statische Imports + require) */
function fileImportsTarget(content, targetRel, importerPath) {
  // Normalisierung: Zieldatei ohne Erweiterung fuer flexiblen Abgleich
  const withoutExt = targetRel.replace(/\.(ts|tsx)$/, '');
  const targetBasename = withoutExt.split('/').at(-1) ?? '';
  // Verzeichnis der importierenden Datei (relativ zum Projekt-Root)
  const importerDir = dirname(importerPath);
  // Regex: from '...target...' oder require('...target...')
  const importPattern = /(?:from\s+|require\s*\(\s*)['"]([^'"]+)['"]/g;
  let match;
  while ((match = importPattern.exec(content)) !== null) {
    const imported = match[1];
    // Absoluter Import-Abgleich: endet mit dem relativen Pfad oder vollem Namen
    if (imported.endsWith(withoutExt) || imported.endsWith(targetRel)) return true;

    // Relativer Import-Abgleich: Pfad aufloesen und vergleichen
    if (imported.startsWith('.')) {
      // Relativen Import-Pfad in tatsaechlichen Projektpfad umrechnen
      const resolvedImport = join(importerDir, imported).replace(/\.(ts|tsx)$/, '');
      if (resolvedImport === withoutExt) return true;
      // Normalisierung fuer Windows-Pfade (Backslash)
      if (resolvedImport.replace(/\\/g, '/') === withoutExt) return true;
    }

    // Segment-Abgleich als Fallback fuer Pfad-Alias-Importe (@app/...)
    const normalizedImport = imported.replace(/\.(ts|tsx)$/, '');
    const importBasename = normalizedImport.split('/').at(-1) ?? '';
    if (importBasename === targetBasename) {
      // Basename stimmt ueberein — zusaetzlich letzten Verzeichnis-Abschnitt pruefen
      const targetDir = withoutExt.split('/').slice(-2, -1)[0] ?? '';
      const importDir = normalizedImport.split('/').slice(-2, -1)[0] ?? '';
      if (targetDir && importDir && targetDir === importDir) return true;
    }
  }
  return false;
}

// ---- Stack Detection ---------------------------------------------------

/** Liest package.json und bestimmt das Framework */
async function detectStack(root) {
  const pkgPath = join(root, 'package.json');
  let pkg = {};
  try {
    pkg = JSON.parse(await readFile(pkgPath, 'utf8'));
  } catch {
    return { framework: 'typescript', hasNextJs: false, hasNestJs: false };
  }
  const deps = { ...pkg.dependencies, ...pkg.devDependencies };
  const hasNestJs = '@nestjs/core' in deps || '@nestjs/common' in deps;
  const hasNextJs = 'next' in deps;
  const framework = hasNestJs ? 'nestjs' : hasNextJs ? 'nextjs' : 'typescript';
  return { framework, hasNextJs, hasNestJs };
}

// ---- Importer Scan -----------------------------------------------------

/** Findet alle Dateien die das Ziel direkt importieren */
async function findImporters(root, targetRel) {
  const allFiles = await collectTsFiles(root);
  /** @type {string[]} */
  const importers = [];
  for (const file of allFiles) {
    if (resolve(file) === resolve(targetFile)) continue;
    let content;
    try {
      content = await readFile(file, 'utf8');
    } catch {
      continue;
    }
    const importerRelative = relative(root, file);
    if (fileImportsTarget(content, targetRel, importerRelative)) {
      importers.push(importerRelative);
    }
  }
  return importers;
}

// ---- Next.js Route Utilities -------------------------------------------

/**
 * Prueft ob ein Dateipfad eine Next.js App Router route.ts(x) ist.
 * Nur route.ts / route.tsx gelten als API-Routen im App Router.
 */
function isNextJsAppRoute(filePath) {
  return /[/\\]app[/\\].*route\.(ts|tsx)$/.test(filePath);
}

/**
 * Prueft ob ein Dateipfad eine Next.js Pages Router API-Route ist.
 * Muster: pages/api/**\/*.ts(x)
 */
function isNextJsPagesApiRoute(filePath) {
  return /[/\\]pages[/\\]api[/\\].*\.(ts|tsx)$/.test(filePath);
}

/**
 * Leitet die URL aus einem App-Router route.ts-Pfad ab.
 * Regeln:
 *  - Strip alles bis inkl. 'app/'
 *  - Strip abschliessendes 'route.ts(x)'
 *  - Route Groups (marketing) entfernen (Klammern-Segment)
 *  - Dynamic segments [id] -> :id
 *  - Catch-all [...slug] -> *slug
 */
function deriveAppRouterUrl(absolutePath, root) {
  // Relativen Pfad vom Root berechnen, Backslashes normalisieren
  const rel = relative(root, absolutePath).replace(/\\/g, '/');
  // Alles bis einschliesslich 'app/' entfernen (auch 'src/app/')
  const afterApp = rel.replace(/^.*?app\//, '');
  // Dateiname 'route.ts' / 'route.tsx' entfernen
  const withoutFile = afterApp.replace(/\/?route\.(ts|tsx)$/, '');
  // Verzeichnis-Segmente aufteilen
  const segments = withoutFile.split('/').filter(Boolean);
  // Transformation pro Segment
  const urlSegments = segments
    .filter((seg) => !/^\(.*\)$/.test(seg))           // Route Groups entfernen
    .map((seg) => {
      if (/^\[{3}/.test(seg)) return '*' + seg.replace(/\[{3}\.{3}(\w+)\]{3}/, '$1'); // [...slug]
      if (/^\[{2}/.test(seg)) return ':' + seg.replace(/\[{2}(\w+)\]{2}/, '$1');      // [[id]] optional
      if (/^\[/.test(seg))    return ':' + seg.replace(/\[(\w+)\]/, '$1');             // [id]
      return seg;
    });
  return '/' + urlSegments.join('/');
}

/**
 * Leitet die URL aus einem Pages-Router API-Pfad ab.
 * Muster: pages/api/users/[id].ts -> /api/users/:id
 */
function derivePagesApiUrl(absolutePath, root) {
  const rel = relative(root, absolutePath).replace(/\\/g, '/');
  const afterPages = rel.replace(/^.*?pages\//, '');
  // Erweiterung entfernen
  const withoutExt = afterPages.replace(/\.(ts|tsx)$/, '');
  const segments = withoutExt.split('/').filter(Boolean);
  const urlSegments = segments.map((seg) => {
    if (/^\[\.{3}/.test(seg)) return '*' + seg.replace(/\[\.{3}(\w+)\]/, '$1');
    if (/^\[/.test(seg))      return ':' + seg.replace(/\[(\w+)\]/, '$1');
    return seg;
  });
  return '/' + urlSegments.join('/');
}

/** HTTP-Methoden aus einem Next.js route.ts-Dateiinhalt extrahieren */
function extractNextJsMethods(content) {
  const HTTP_METHODS = 'GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS';
  const methods = new Set();

  // export async function GET(...) und export function GET(...)
  const funcPattern = new RegExp(`export\\s+(?:async\\s+)?function\\s+(${HTTP_METHODS})\\b`, 'g');
  let m;
  while ((m = funcPattern.exec(content)) !== null) methods.add(m[1]);

  // export const GET = ... und export const GET: NextRouteHandler = ...
  const constPattern = new RegExp(`export\\s+const\\s+(${HTTP_METHODS})\\s*[=:]`, 'g');
  while ((m = constPattern.exec(content)) !== null) methods.add(m[1]);

  // export { ..., GET, ... } — best-effort re-export
  const reExportPattern = /export\s*\{([^}]+)\}/g;
  while ((m = reExportPattern.exec(content)) !== null) {
    const names = m[1].split(',').map((n) => n.trim().split(/\s+as\s+/)[0].trim());
    for (const name of names) {
      if (/^(GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS)$/.test(name)) methods.add(name);
    }
  }

  return Array.from(methods);
}

/** Alle App-Router route.ts(x)-Dateien im Projekt aufsammeln (project-wide map) */
async function collectAllNextRoutes(root) {
  const allFiles = await collectTsFiles(root);
  return allFiles
    .filter((f) => isNextJsAppRoute(f))
    .map((f) => relative(root, f).replace(/\\/g, '/'));
}

// ---- Route Detection ---------------------------------------------------

/** Extrahiert NestJS Controller-Namen und HTTP-Endpoints aus einer Datei */
function extractNestJsRoutes(content, filePath) {
  /** @type {string[]} */
  const controllers = [];
  /** @type {string[]} */
  const endpoints = [];

  // @Controller('prefix') oder @Controller()
  const controllerMatch = content.match(/@Controller\(['"]?([^'")\s]*)['"]?\)/);
  if (controllerMatch) {
    // Klassenname nach dem Decorator
    const classMatch = content.match(/@Controller[^]*?class\s+(\w+)/);
    const controllerName = classMatch ? classMatch[1] : 'UnknownController';
    controllers.push(controllerName);
    const prefix = controllerMatch[1] || '';

    // HTTP-Verb Decorators: @Get, @Post, @Put, @Delete, @Patch
    const verbPattern = /@(Get|Post|Put|Delete|Patch)\(['"]?([^'")\s]*)['"]?\)/g;
    let match;
    while ((match = verbPattern.exec(content)) !== null) {
      const method = match[1].toUpperCase();
      const path = match[2] || '';
      const fullPath = prefix ? `/${prefix}${path ? '/' + path : ''}` : `/${path}`;
      endpoints.push(`${method} ${fullPath.replace(/\/+/g, '/')}`);
    }
  }

  return { controllers, endpoints };
}

/**
 * Kombinierter Route-Scan fuer die Zieldatei selbst + projektweite Next.js-Routen.
 * Beruecksichtigt:
 *  - NestJS Controller in der Zieldatei
 *  - Zieldatei ist selbst eine Next.js route.ts -> Endpoints ableiten
 *  - Projektweite Auflistung aller Next.js route.ts Dateien
 */
async function scanRoutes(root, targetRel, stack) {
  /** @type {string[]} */
  const controllers = [];
  /** @type {string[]} */
  const endpoints = [];
  /** @type {string[]} */
  const nextRoutes = [];

  if (stack.hasNestJs) {
    // Pruefen ob die Zieldatei selbst ein Controller ist
    let targetContent;
    try {
      targetContent = await readFile(targetFile, 'utf8');
      const { controllers: c, endpoints: e } = extractNestJsRoutes(targetContent, targetFile);
      controllers.push(...c);
      endpoints.push(...e);
    } catch {
      // Datei nicht lesbar, weiter
    }
  }

  if (stack.hasNextJs) {
    // Projektweite Auflistung aller Next.js App-Router-Routen
    const allNextRoutes = await collectAllNextRoutes(root);
    nextRoutes.push(...allNextRoutes);

    // Self-route detection: Zieldatei ist selbst eine route.ts(x)
    if (isNextJsAppRoute(targetFile)) {
      await extractNextJsEndpoints(targetFile, root, endpoints);
    } else if (isNextJsPagesApiRoute(targetFile)) {
      // Pages Router: default export, HTTP-Methode schwer erkennbar -> ANY
      const url = derivePagesApiUrl(targetFile, root);
      endpoints.push(`ANY ${url}`);
    }

    // Importierende Routen werden ueber den allgemeinen importer-Scan erfasst
  }

  return { controllers, endpoints, nextRoutes };
}

/**
 * Liest eine Next.js route.ts, extrahiert HTTP-Methoden und leitet Endpoints ab.
 * Schreibt Ergebnisse direkt in das uebergebene Array.
 */
async function extractNextJsEndpoints(routeFile, root, endpointsOut) {
  let content;
  try {
    content = await readFile(routeFile, 'utf8');
  } catch {
    return;
  }
  const url = deriveAppRouterUrl(routeFile, root);
  const methods = extractNextJsMethods(content);
  if (methods.length === 0) {
    // Keine Methode erkannt -> generisch
    endpointsOut.push(`ANY ${url}`);
  } else {
    for (const method of methods) {
      endpointsOut.push(`${method} ${url}`);
    }
  }
}

// ---- Test Coverage -----------------------------------------------------

/** Findet Test/Spec-Dateien die das Ziel importieren */
async function findCoveringTests(root, targetRel) {
  const allFiles = await collectTsFiles(root);
  /** @type {string[]} */
  const covering = [];

  for (const file of allFiles) {
    if (!/(spec|test)\.(ts|tsx)$/.test(file)) continue;
    let content;
    try {
      content = await readFile(file, 'utf8');
    } catch {
      continue;
    }
    const specRelative = relative(root, file);
    if (fileImportsTarget(content, targetRel, specRelative)) {
      covering.push(specRelative);
    }
  }

  return covering;
}

// ---- ENV Var Scan ------------------------------------------------------

/** Extrahiert alle process.env.X Referenzen aus der Zieldatei */
async function extractEnvVars() {
  let content;
  try {
    content = await readFile(targetFile, 'utf8');
  } catch {
    return [];
  }
  const envPattern = /process\.env\.([A-Z_][A-Z0-9_]*)/g;
  const vars = new Set();
  let match;
  while ((match = envPattern.exec(content)) !== null) {
    vars.add(match[1]);
  }
  return Array.from(vars).sort();
}

// ---- Migration Scan ----------------------------------------------------

/** Zaehlt Migrations-Dateien die in den letzten 7 Tagen veraendert wurden */
async function scanMigrations(root) {
  const migrationsDir = join(root, 'migrations');
  if (!existsSync(migrationsDir)) return { recent_count: 0, recent_files: [] };

  let entries;
  try {
    entries = await readdir(migrationsDir, { withFileTypes: true });
  } catch {
    return { recent_count: 0, recent_files: [] };
  }

  const sevenDaysAgo = Date.now() - 7 * 24 * 60 * 60 * 1000;
  /** @type {string[]} */
  const recentFiles = [];

  for (const entry of entries) {
    if (!entry.isFile() || !/\.(ts|js)$/.test(entry.name)) continue;
    const full = join(migrationsDir, entry.name);
    let fileStat;
    try {
      fileStat = await stat(full);
    } catch {
      continue;
    }
    if (fileStat.mtimeMs > sevenDaysAgo) {
      recentFiles.push(entry.name);
    }
  }

  return { recent_count: recentFiles.length, recent_files: recentFiles };
}

// ---- Risk Score --------------------------------------------------------

/**
 * Berechnet den Risk Score basierend auf Heuristiken.
 * Low: <=2 Importer, keine Routes, Tests vorhanden, keine ENV, keine Migrations
 * Medium: 3-7 Importer ODER 1-2 Routes ODER Test-Gap ODER ENV vars
 * High: >=8 Importer ODER >=3 Routes ODER (Test-Gap + ENV + Migrations)
 */
function calculateRiskScore(data) {
  const { importerCount, endpointCount, testGap, envVarCount, recentMigrationCount } = data;
  /** @type {string[]} */
  const factors = [];

  if (importerCount > 0) factors.push(`${importerCount} importer${importerCount !== 1 ? 's' : ''}`);
  if (endpointCount > 0) factors.push(`${endpointCount} API route${endpointCount !== 1 ? 's' : ''}`);
  if (!testGap) factors.push('test coverage exists');
  if (testGap) factors.push('no test coverage (gap)');
  if (envVarCount > 0) factors.push(`${envVarCount} ENV var${envVarCount !== 1 ? 's' : ''}`);
  if (recentMigrationCount > 0) factors.push(`${recentMigrationCount} recent migration${recentMigrationCount !== 1 ? 's' : ''}`);

  // High: viele Importer, viele Routes, oder kritische Kombination
  if (importerCount >= 8 || endpointCount >= 3 || (testGap && envVarCount > 0 && recentMigrationCount > 0)) {
    return { score: 'high', factors };
  }

  // Low: wenig Importer, keine Routes, Tests vorhanden, keine ENV, keine Migrations
  if (importerCount <= 2 && endpointCount === 0 && !testGap && envVarCount === 0 && recentMigrationCount === 0) {
    return { score: 'low', factors };
  }

  // Medium: alles andere
  return { score: 'medium', factors };
}

// ---- Main --------------------------------------------------------------

async function main() {
  const stack = await detectStack(projectRoot);
  const importers = await findImporters(projectRoot, targetRelative);
  const routes = await scanRoutes(projectRoot, targetRelative, stack);
  const coveringTests = await findCoveringTests(projectRoot, targetRelative);
  const envVars = await extractEnvVars();
  const migrations = await scanMigrations(projectRoot);

  const allEndpoints = [...routes.endpoints];
  const testGap = coveringTests.length === 0;

  const { score, factors } = calculateRiskScore({
    importerCount: importers.length,
    endpointCount: allEndpoints.length,
    testGap,
    envVarCount: envVars.length,
    recentMigrationCount: migrations.recent_count,
  });

  /** @type {object} */
  const output = {
    target: targetRelative,
    stack: {
      framework: stack.framework,
      hasNextJs: stack.hasNextJs,
    },
    imports: {
      importers,
      count: importers.length,
    },
    routes: {
      controllers: routes.controllers,
      endpoints: allEndpoints,
      next_routes: routes.nextRoutes,
    },
    tests: {
      covering: coveringTests,
      count: coveringTests.length,
      gap: testGap,
    },
    env_vars: envVars,
    migrations: {
      recent_count: migrations.recent_count,
      recent_files: migrations.recent_files,
    },
    risk_score: score,
    risk_factors: factors,
  };

  if (jsonOnly) {
    process.stdout.write(JSON.stringify(output, null, 2) + '\n');
  } else {
    process.stdout.write(JSON.stringify(output, null, 2) + '\n');
  }
}

function printHelp() {
  const help = `
scan-impact.mjs — Safe Change Impact Analyzer

USAGE
  node scan-impact.mjs <target-file> [options]

ARGUMENTS
  <target-file>    Path to the TypeScript file you are about to change.
                   Relative to cwd or absolute.

OPTIONS
  --root <dir>     Project root for scanning (default: cwd)
  --json           Output raw JSON (same behavior, kept for scripting clarity)
  --help           Show this help text

EXAMPLES
  node scan-impact.mjs src/notifications/notifications.service.ts
  node scan-impact.mjs src/auth/auth.guard.ts --root /path/to/project
  node scan-impact.mjs src/users/users.service.ts --json

OUTPUT
  JSON with keys: target, stack, imports, routes, tests, env_vars, migrations,
  risk_score (low|medium|high), risk_factors

NOTES
  - Read-only: never modifies source files
  - Uses regex-based analysis (no AST). Dynamic imports are not detected.
  - See references/limitations.md for full trade-off list
`.trim();
  process.stdout.write(help + '\n');
}

main().catch((err) => {
  process.stderr.write(`scan-impact error: ${err.message}\n`);
  process.exit(1);
});

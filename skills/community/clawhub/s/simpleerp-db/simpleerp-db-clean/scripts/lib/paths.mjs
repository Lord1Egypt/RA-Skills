import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

/** Skill root (simpleerp-db/), works on Windows, macOS, and Linux. */
export const SKILL_ROOT = path.resolve(__dirname, '..', '..');

export const LOCAL_TABLES_SQL = path.join(SKILL_ROOT, 'schema', 'TABLES.sql');
export const SETUP_STATUS_PATH = path.join(SKILL_ROOT, 'output', '.setup-status.json');

export function resolveFromSkillRoot(relativePath) {
  return path.isAbsolute(relativePath) ? relativePath : path.join(SKILL_ROOT, relativePath);
}

export function ensureDirForFile(filePath) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
}

export function resolveTablesSqlPath() {
  if (process.env.SIMPLEERP_TABLES_SQL?.trim()) {
    return path.resolve(process.env.SIMPLEERP_TABLES_SQL.trim());
  }
  if (fs.existsSync(LOCAL_TABLES_SQL)) {
    return LOCAL_TABLES_SQL;
  }
  const sibling = path.join(SKILL_ROOT, '..', 'simpleerp', 'api', 'db', 'TABLES.sql');
  if (fs.existsSync(sibling)) {
    return sibling;
  }
  return null;
}

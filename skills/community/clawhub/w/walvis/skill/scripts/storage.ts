/**
 * WALVIS local storage helpers
 * Manages ~/.walvis/ directory: manifest.json and space JSON files
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync, readdirSync } from 'fs';
import { join } from 'path';
import { homedir } from 'os';
import type { Manifest, Space } from './types.js';

export const WALVIS_DIR = join(homedir(), '.walvis');
export const MANIFEST_PATH = join(WALVIS_DIR, 'manifest.json');
export const SPACES_DIR = join(WALVIS_DIR, 'spaces');

export function ensureDirs(): void {
  if (!existsSync(WALVIS_DIR)) mkdirSync(WALVIS_DIR, { recursive: true });
  if (!existsSync(SPACES_DIR)) mkdirSync(SPACES_DIR, { recursive: true });
}

export function readManifest(): Manifest {
  ensureDirs();
  if (!existsSync(MANIFEST_PATH)) {
    throw new Error('WALVIS not initialized. Run: npx walvis');
  }
  return JSON.parse(readFileSync(MANIFEST_PATH, 'utf-8')) as Manifest;
}

export function writeManifest(manifest: Manifest): void {
  ensureDirs();
  writeFileSync(MANIFEST_PATH, JSON.stringify(manifest, null, 2), 'utf-8');
}

export function spacePath(spaceId: string): string {
  return join(SPACES_DIR, `${spaceId}.json`);
}

export function readSpace(spaceId: string): Space {
  const p = spacePath(spaceId);
  if (!existsSync(p)) throw new Error(`Space not found: ${spaceId}`);
  return JSON.parse(readFileSync(p, 'utf-8')) as Space;
}

export function writeSpace(space: Space): void {
  ensureDirs();
  writeFileSync(spacePath(space.id), JSON.stringify(space, null, 2), 'utf-8');
}

export function listSpaceFiles(): string[] {
  ensureDirs();
  try {
    return readdirSync(SPACES_DIR).filter(f => f.endsWith('.json'));
  } catch {
    return [];
  }
}

export function listSpaces(): Space[] {
  return listSpaceFiles().map(f =>
    JSON.parse(readFileSync(join(SPACES_DIR, f), 'utf-8')) as Space
  );
}

export function spaceExists(spaceId: string): boolean {
  return existsSync(spacePath(spaceId));
}

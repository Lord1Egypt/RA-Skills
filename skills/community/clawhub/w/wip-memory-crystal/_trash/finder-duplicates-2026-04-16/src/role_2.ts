// memory-crystal/role.ts — Crystal Core/Node role detection and management.
// Answers: "Am I a Core, a Node, or standalone?"
//
// Detection logic:
//   1. State file override (from crystal promote / crystal demote) wins
//   2. Auto-detect from env vars:
//      - CRYSTAL_RELAY_URL set + no local embedding provider = node
//      - CRYSTAL_RELAY_URL set + local embedding provider = core
//      - No relay URL = standalone

import { existsSync, readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';
import { resolveStatePath, stateWritePath, ldmPaths, getAgentId, resolveSecretPath } from './ldm.js';

export type CrystalRole = 'core' | 'node' | 'standalone';

export interface RoleState {
  role: CrystalRole;
  override: boolean;
  relayUrl?: string;
  agentId: string;
  setAt: string;
}

export interface RoleInfo {
  role: CrystalRole;
  source: 'state-file' | 'auto-detected';
  relayUrl: string | null;
  relayToken: boolean;
  relayKeyExists: boolean;
  agentId: string;
  hasLocalEmbeddings: boolean;
  hasLocalDb: boolean;
}

const STATE_FILE = 'crystal-role.json';

// ── State file ──

export function loadRoleState(): RoleState | null {
  try {
    const path = resolveStatePath(STATE_FILE);
    if (existsSync(path)) {
      return JSON.parse(readFileSync(path, 'utf-8'));
    }
  } catch {}
  return null;
}

function saveRoleState(state: RoleState): void {
  const writePath = stateWritePath(STATE_FILE);
  writeFileSync(writePath, JSON.stringify(state, null, 2) + '\n');
}

// ── Environment checks ──

function hasLocalEmbeddingProvider(): boolean {
  // OpenAI key present
  if (process.env.OPENAI_API_KEY) return true;
  // Google key present
  if (process.env.GOOGLE_API_KEY && process.env.CRYSTAL_EMBEDDING_PROVIDER === 'google') return true;
  // Ollama configured
  if (process.env.CRYSTAL_EMBEDDING_PROVIDER === 'ollama') return true;
  return false;
}

function hasRelayKey(): boolean {
  const keyPath = resolveSecretPath('crystal-relay-key');
  return existsSync(keyPath);
}

// ── Detection ──

export function detectRole(): RoleInfo {
  const agentId = getAgentId();
  const paths = ldmPaths(agentId);
  const relayUrl = process.env.CRYSTAL_RELAY_URL || null;
  const relayToken = !!process.env.CRYSTAL_RELAY_TOKEN;
  const relayKeyExists = hasRelayKey();
  const localEmbeddings = hasLocalEmbeddingProvider();
  const localDb = existsSync(paths.crystalDb);

  // Check state file override first
  const state = loadRoleState();
  if (state && state.override) {
    return {
      role: state.role,
      source: 'state-file',
      relayUrl,
      relayToken,
      relayKeyExists,
      agentId,
      hasLocalEmbeddings: localEmbeddings,
      hasLocalDb: localDb,
    };
  }

  // Auto-detect
  let role: CrystalRole = 'standalone';
  if (relayUrl && !localEmbeddings) {
    role = 'node';
  } else if (relayUrl && localEmbeddings) {
    role = 'core';
  }

  return {
    role,
    source: 'auto-detected',
    relayUrl,
    relayToken,
    relayKeyExists,
    agentId,
    hasLocalEmbeddings: localEmbeddings,
    hasLocalDb: localDb,
  };
}

// ── Promote / Demote ──

export function promoteToCore(): void {
  saveRoleState({
    role: 'core',
    override: true,
    agentId: getAgentId(),
    setAt: new Date().toISOString(),
  });
}

export function demoteToNode(relayUrl?: string): void {
  saveRoleState({
    role: 'node',
    override: true,
    relayUrl,
    agentId: getAgentId(),
    setAt: new Date().toISOString(),
  });
}

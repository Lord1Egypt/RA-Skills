import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { CliError } from './errors.js';

function getTeamsFile(): string {
  const dir = process.env.TOKENRIP_CONFIG_DIR ?? path.join(os.homedir(), '.config', 'tokenrip');
  return path.join(dir, 'teams.json');
}

export interface LocalTeam {
  id: string;
  name: string;
  slug: string;
  alias?: string;
  role: 'owner' | 'member';
  syncedAt: string;
}

export type Teams = Record<string, LocalTeam>;

export interface ServerTeamEntry {
  id: string;
  name: string;
  slug: string;
  role: string;
}

export function loadTeams(): Teams {
  try {
    const raw = fs.readFileSync(getTeamsFile(), 'utf-8');
    return JSON.parse(raw) as Teams;
  } catch {
    return {};
  }
}

export function saveTeams(teams: Teams): void {
  const file = getTeamsFile();
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, JSON.stringify(teams, null, 2), 'utf-8');
}

export function resolveTeam(value: string): string {
  const teams = loadTeams();
  for (const entry of Object.values(teams)) {
    if (entry.alias === value) return entry.slug;
  }
  if (teams[value]) return value;
  return value;
}

export function resolveTeams(values: string[]): string[] {
  const teams = loadTeams();
  return values.map((v) => {
    for (const entry of Object.values(teams)) {
      if (entry.alias === v) return entry.slug;
    }
    if (teams[v]) return v;
    return v;
  });
}

export function setAlias(slug: string, alias: string): void {
  const teams = loadTeams();
  if (!teams[slug]) {
    throw new CliError('TEAM_NOT_FOUND', `Team "${slug}" not found locally. Run "rip team list" to sync.`);
  }
  teams[slug].alias = alias;
  saveTeams(teams);
}

export function removeAlias(slug: string): void {
  const teams = loadTeams();
  if (!teams[slug]) {
    throw new CliError('TEAM_NOT_FOUND', `Team "${slug}" not found locally. Run "rip team list" to sync.`);
  }
  delete teams[slug].alias;
  saveTeams(teams);
}

export function syncTeamsFromResponse(serverTeams: ServerTeamEntry[]): void {
  const existing = loadTeams();
  const updated: Teams = {};

  for (const st of serverTeams) {
    const prev = existing[st.slug];
    updated[st.slug] = {
      id: st.id,
      name: st.name,
      slug: st.slug,
      alias: prev?.alias,
      role: st.role as 'owner' | 'member',
      syncedAt: new Date().toISOString(),
    };
  }

  saveTeams(updated);
}

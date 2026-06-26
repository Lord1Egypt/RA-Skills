import { requireAuthClient } from '../auth-client.js';
import { outputSuccess } from '../output.js';
import { formatTeamCreated, formatTeamList, formatTeamDetails, formatTeamInvite } from '../formatters.js';
import { loadTeams, saveTeams, resolveTeam, syncTeamsFromResponse, setAlias, removeAlias } from '../teams.js';

export async function teamCreate(slug: string, options: { name?: string; description?: string }): Promise<void> {
  const { client } = requireAuthClient();
  const { data } = await client.post('/v0/teams', {
    slug,
    name: options.name ?? slug,
    description: options.description,
  });
  const team = data.data;
  const teams = loadTeams();
  teams[team.slug] = {
    id: team.id,
    name: team.name,
    slug: team.slug,
    role: 'owner',
    syncedAt: new Date().toISOString(),
  };
  saveTeams(teams);
  outputSuccess(team, formatTeamCreated);
}

export async function teamList(): Promise<void> {
  const { client } = requireAuthClient();
  const { data } = await client.get('/v0/teams');
  syncTeamsFromResponse(data.data);
  outputSuccess(data.data, formatTeamList);
}

export async function teamShow(slugOrId: string): Promise<void> {
  const resolved = resolveTeam(slugOrId);
  const { client } = requireAuthClient();
  const { data } = await client.get(`/v0/teams/${encodeURIComponent(resolved)}`);
  outputSuccess(data.data, formatTeamDetails);
}

export async function teamAdd(slugOrId: string, agentIdOrAlias: string): Promise<void> {
  const resolved = resolveTeam(slugOrId);
  const { client } = requireAuthClient();
  const { data } = await client.post(`/v0/teams/${encodeURIComponent(resolved)}/members`, {
    agentId: agentIdOrAlias,
  });
  outputSuccess(data.data ?? { ok: true });
}

export async function teamInvite(slugOrId: string): Promise<void> {
  const resolved = resolveTeam(slugOrId);
  const { client } = requireAuthClient();
  const { data } = await client.post(`/v0/teams/${encodeURIComponent(resolved)}/invite`);
  outputSuccess(data.data, formatTeamInvite);
}

export async function teamRemove(slugOrId: string, agentIdOrAlias: string): Promise<void> {
  const resolved = resolveTeam(slugOrId);
  const { client } = requireAuthClient();
  await client.delete(`/v0/teams/${encodeURIComponent(resolved)}/members/${encodeURIComponent(agentIdOrAlias)}`);
  outputSuccess({ ok: true });
}

export async function teamLeave(slugOrId: string): Promise<void> {
  const resolved = resolveTeam(slugOrId);
  const { client } = requireAuthClient();
  await client.post(`/v0/teams/${encodeURIComponent(resolved)}/leave`);
  const teams = loadTeams();
  delete teams[resolved];
  saveTeams(teams);
  outputSuccess({ ok: true });
}

export async function teamDelete(slugOrId: string): Promise<void> {
  const resolved = resolveTeam(slugOrId);
  const { client } = requireAuthClient();
  await client.delete(`/v0/teams/${encodeURIComponent(resolved)}`);
  const teams = loadTeams();
  delete teams[resolved];
  saveTeams(teams);
  outputSuccess({ ok: true });
}

export async function teamAcceptInvite(token: string): Promise<void> {
  const { client } = requireAuthClient();
  const { data } = await client.post('/v0/teams/accept-invite', { token });
  const team = data.data;
  if (team?.slug) {
    const teams = loadTeams();
    teams[team.slug] = {
      id: team.id,
      name: team.name,
      slug: team.slug,
      role: 'member',
      syncedAt: new Date().toISOString(),
    };
    saveTeams(teams);
  }
  outputSuccess(team ?? { ok: true });
}

export async function teamAlias(slug: string, alias: string): Promise<void> {
  setAlias(slug, alias);
  outputSuccess({ slug, alias });
}

export async function teamUnalias(slug: string): Promise<void> {
  removeAlias(slug);
  outputSuccess({ slug, alias: null });
}

export async function teamSync(): Promise<void> {
  const { client } = requireAuthClient();
  const { data } = await client.get('/v0/teams');
  syncTeamsFromResponse(data.data);
  outputSuccess(data.data, formatTeamList);
}

import { requireAuthClient } from '../auth-client.js';
import { outputSuccess } from '../output.js';
import { resolveTeam } from '../teams.js';

export async function folderCreate(slug: string, options: { team?: string }): Promise<void> {
  const { client } = requireAuthClient();
  if (options.team) {
    const teamSlug = resolveTeam(options.team);
    const { data } = await client.post(`/v0/teams/${encodeURIComponent(teamSlug)}/folders`, { slug });
    outputSuccess(data.data);
  } else {
    const { data } = await client.post('/v0/folders', { slug });
    outputSuccess(data.data);
  }
}

export async function folderList(options: { team?: string }): Promise<void> {
  const { client } = requireAuthClient();
  if (options.team) {
    const teamSlug = resolveTeam(options.team);
    const { data } = await client.get(`/v0/teams/${encodeURIComponent(teamSlug)}/folders`);
    outputSuccess(data.data);
  } else {
    const { data } = await client.get('/v0/folders');
    outputSuccess(data.data);
  }
}

export async function folderShow(slug: string, options: { team?: string }): Promise<void> {
  const { client } = requireAuthClient();
  if (options.team) {
    const teamSlug = resolveTeam(options.team);
    const { data } = await client.get(`/v0/teams/${encodeURIComponent(teamSlug)}/folders/${encodeURIComponent(slug)}`);
    outputSuccess(data.data);
  } else {
    const { data } = await client.get(`/v0/folders/${encodeURIComponent(slug)}`);
    outputSuccess(data.data);
  }
}

export async function folderDelete(slug: string, options: { team?: string }): Promise<void> {
  const { client } = requireAuthClient();
  if (options.team) {
    const teamSlug = resolveTeam(options.team);
    await client.delete(`/v0/teams/${encodeURIComponent(teamSlug)}/folders/${encodeURIComponent(slug)}`);
  } else {
    await client.delete(`/v0/folders/${encodeURIComponent(slug)}`);
  }
  outputSuccess({ ok: true });
}

export async function folderRename(oldSlug: string, newSlug: string, options: { team?: string }): Promise<void> {
  const { client } = requireAuthClient();
  if (options.team) {
    const teamSlug = resolveTeam(options.team);
    const { data } = await client.patch(`/v0/teams/${encodeURIComponent(teamSlug)}/folders/${encodeURIComponent(oldSlug)}`, { slug: newSlug });
    outputSuccess(data.data);
  } else {
    const { data } = await client.patch(`/v0/folders/${encodeURIComponent(oldSlug)}`, { slug: newSlug });
    outputSuccess(data.data);
  }
}

export async function assetMove(uuid: string, options: { folder?: string; team?: string; unfiled?: boolean }): Promise<void> {
  const { client } = requireAuthClient();

  if (options.unfiled) {
    await client.patch(`/v0/assets/${uuid}`, { folderId: null });
    outputSuccess({ id: uuid, folder_id: null });
    return;
  }

  if (!options.folder) {
    throw new Error('Provide --folder <slug> or --unfiled');
  }

  // Resolve folder slug to ID
  let folderId: string;
  if (options.team) {
    const teamSlug = resolveTeam(options.team);
    const { data } = await client.get(`/v0/teams/${encodeURIComponent(teamSlug)}/folders/${encodeURIComponent(options.folder)}`);
    folderId = data.data.id;
  } else {
    const { data } = await client.get(`/v0/folders/${encodeURIComponent(options.folder)}`);
    folderId = data.data.id;
  }

  const { data } = await client.patch(`/v0/assets/${uuid}`, { folderId });
  outputSuccess(data.data);
}

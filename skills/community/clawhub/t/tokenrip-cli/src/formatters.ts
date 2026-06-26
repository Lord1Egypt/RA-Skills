import { loadTeams } from './teams.js';

export type Formatter = (data: Record<string, unknown>) => string;

export const formatAssetCreated: Formatter = (data) => {
  const lines = [`Created: ${data.title || '(untitled)'}`];
  if (data.id) lines.push(`  ID:   ${data.id}`);
  if (data.url) lines.push(`  URL:  ${data.url}`);
  if (data.type) lines.push(`  Type: ${data.type}`);
  if (data.mimeType) lines.push(`  MIME: ${data.mimeType}`);
  return lines.join('\n');
};

export const formatAssetPatched: Formatter = (data) => {
  const lines = [`Patched: ${data.id}`];
  if (data.alias) lines.push(`  Alias:    ${data.alias}`);
  if (data.url) lines.push(`  URL:      ${data.url}`);
  if (data.metadata) lines.push(`  Metadata: ${JSON.stringify(data.metadata)}`);
  if (data.updatedAt) lines.push(`  Updated:  ${data.updatedAt}`);
  return lines.join('\n');
};

export const formatAssetDeleted: Formatter = (data) => {
  return `Deleted: ${data.id}`;
};

export const formatAssetList: Formatter = (data) => {
  const assets = data as unknown as Record<string, unknown>[];
  if (!Array.isArray(assets) || assets.length === 0) {
    return 'No assets found.';
  }
  const lines = [`${assets.length} asset(s):\n`];
  for (const a of assets) {
    const title = a.title || '(untitled)';
    const type = a.type || '';
    const id = a.id || '';
    lines.push(`  ${type.toString().padEnd(10)} ${title}  (${id})`);
    if (a.url) lines.push(`             ${a.url}`);
  }
  return lines.join('\n');
};

export const formatStats: Formatter = (data) => {
  const lines: string[] = [];
  if (data.assetCount !== undefined) lines.push(`Total assets: ${data.assetCount}`);
  if (data.totalBytes !== undefined) lines.push(`Total size:   ${formatBytes(data.totalBytes as number)}`);

  const countsByType = data.countsByType as Record<string, number> | undefined;
  const bytesByType = data.bytesByType as Record<string, number> | undefined;
  const byType = countsByType
    ? Object.keys(countsByType)
        .sort()
        .map((type) => ({
          type,
          count: countsByType[type],
          totalBytes: bytesByType?.[type] ?? 0,
        }))
    : undefined;

  if (Array.isArray(byType) && byType.length > 0) {
    lines.push('');
    lines.push('By type:');
    for (const t of byType) {
      const name = (t.type || 'unknown') as string;
      const count = t.count ?? 0;
      const bytes = t.totalBytes ?? 0;
      lines.push(`  ${name.padEnd(10)} ${String(count).padStart(4)} assets  ${formatBytes(bytes as number)}`);
    }
  }
  return lines.join('\n');
};

export const formatVersionCreated: Formatter = (data) => {
  const lines = [`Version ${data.version || '?'} published`];
  if (data.id) lines.push(`  Version ID: ${data.id}`);
  if (data.assetId) lines.push(`  Asset ID:   ${data.assetId}`);
  if (data.label) lines.push(`  Label:      ${data.label}`);
  return lines.join('\n');
};

export const formatVersionDeleted: Formatter = (data) => {
  return `Deleted version ${data.versionId} from asset ${data.assetId}`;
};

export const formatConfigSaved: Formatter = (data) => {
  return data.message as string || 'Configuration saved.';
};

export const formatAuthKey: Formatter = (data) => {
  const lines = [data.message as string || 'API key created.'];
  if (data.keyName) lines.push(`  Name: ${data.keyName}`);
  if (data.apiKey) lines.push(`  Key:  ${data.apiKey}`);
  if (data.note) lines.push(`  ${data.note}`);
  return lines.join('\n');
};

export const formatInbox: Formatter = (data) => {
  const lines: string[] = [];
  const threads = (data as any).threads ?? [];
  const assets = (data as any).assets ?? [];

  if (threads.length > 0) {
    lines.push(`THREADS (${threads.length})`);
    for (const t of threads) {
      const count = t.new_message_count ? `+${t.new_message_count} msg${t.new_message_count > 1 ? 's' : ''}` : 'no new';
      const intent = t.last_intent ? `  last: ${t.last_intent}` : '';
      const preview = t.last_body_preview ? `  "${t.last_body_preview}"` : '';
      const ago = formatTimeAgo(new Date(t.updated_at));
      lines.push(`  ${t.thread_id}  ${count.padEnd(10)}${intent}${preview}  ${ago}`);
    }
  } else {
    lines.push('THREADS (none)');
  }

  lines.push('');

  if (assets.length > 0) {
    lines.push(`ASSETS (${assets.length})`);
    for (const a of assets) {
      const title = a.title ?? '(untitled)';
      const versions = `+${a.new_version_count} ver${a.new_version_count > 1 ? 's' : ''}`;
      const ago = formatTimeAgo(new Date(a.updated_at));
      lines.push(`  ${title.padEnd(20)}  v${a.latest_version}  ${versions}  ${ago}  (${a.asset_id})`);
    }
  } else {
    lines.push('ASSETS (none)');
  }

  return lines.join('\n');
};

export const formatThreadList: Formatter = (data) => {
  const threads = (data as any).threads ?? [];
  const total = (data as any).total ?? threads.length;

  if (threads.length === 0) return 'No threads.';

  const lines = [`${total} thread(s):\n`];
  for (const t of threads) {
    const state = t.state === 'closed' ? '[closed]' : '[open]  ';
    const participants = `${t.participant_count} participant${t.participant_count !== 1 ? 's' : ''}`;
    const preview = t.last_message_preview ? `"${t.last_message_preview}"` : '(no messages)';
    const ago = t.updated_at ? formatTimeAgo(new Date(t.updated_at)) : '';
    lines.push(`  ${state}  ${t.thread_id}  ${participants.padEnd(16)}  ${preview}  ${ago}`);
  }

  return lines.join('\n');
};

export const formatContacts: Formatter = (data) => {
  const contacts = data as unknown as Record<string, { agent_id: string; alias?: string; notes?: string }>;
  const entries = Object.entries(contacts);
  if (entries.length === 0) return 'No contacts.';
  const lines = [`${entries.length} contact(s):\n`];
  lines.push(`${'NAME'.padEnd(16)} ${'AGENT ID'.padEnd(40)} ${'ALIAS'.padEnd(16)} NOTES`);
  for (const [name, c] of entries) {
    const alias = c.alias || '—';
    const notes = c.notes || '';
    lines.push(`${name.padEnd(16)} ${c.agent_id.padEnd(40)} ${alias.padEnd(16)} ${notes}`);
  }
  return lines.join('\n');
};

export const formatContactResolved: Formatter = (data) => {
  return `${data.name}: ${data.agent_id}`;
};

export const formatContactSaved: Formatter = (data) => {
  const lines = [`Contact "${data.name}" saved`];
  if (data.agent_id) lines.push(`  Agent: ${data.agent_id}`);
  if (data.alias) lines.push(`  Alias: ${data.alias}`);
  return lines.join('\n');
};

export const formatContactRemoved: Formatter = (data) => {
  return data.message as string || `Contact "${data.name}" removed`;
};

export const formatConfigShow: Formatter = (data) => {
  const lines = ['Configuration:'];
  if (data.apiUrl) lines.push(`  API URL:       ${data.apiUrl}`);
  if (data.frontendUrl) lines.push(`  Frontend:      ${data.frontendUrl}`);
  if (data.apiKey) lines.push(`  API Key:       ${data.apiKey}`);
  if (data.outputFormat) lines.push(`  Output format: ${data.outputFormat}`);
  if (data.configFile) lines.push(`  Config file:   ${data.configFile}`);
  return lines.join('\n');
};

export const formatMessageSent: Formatter = (data) => {
  const lines: string[] = [];
  if (data.thread_id) lines.push(`Thread: ${data.thread_id}`);
  if (data.message_id) lines.push(`Message: ${data.message_id}`);
  if (data.id) lines.push(`Message: ${data.id}`);
  if (data.sequence) lines.push(`Sequence: #${data.sequence}`);
  return lines.join('\n');
};

export const formatMessages: Formatter = (data) => {
  const messages = data as unknown as Array<{
    sequence: number;
    body: string;
    intent?: string;
    sender?: { agent_id?: string; user_id?: string };
    created_at: string;
  }>;
  if (!Array.isArray(messages) || messages.length === 0) return 'No messages.';
  const lines: string[] = [];
  for (const m of messages) {
    const sender = m.sender?.agent_id || m.sender?.user_id || 'unknown';
    const intent = m.intent ? `  [${m.intent}]` : '';
    const ago = formatTimeAgo(new Date(m.created_at));
    lines.push(`#${m.sequence}  ${sender}  ${ago}${intent}`);
    lines.push(`    ${m.body}`);
    lines.push('');
  }
  return lines.join('\n').trimEnd();
};

export const formatShareLink: Formatter = (data) => {
  const lines = ['Share link generated'];
  if (data.url) lines.push(`  URL:   ${data.url}`);
  if (data.token) lines.push(`  Token: ${data.token}`);
  const perm = data.perm as unknown as string[];
  if (Array.isArray(perm)) lines.push(`  Perms: ${perm.join(', ')}`);
  if (data.exp) lines.push(`  Expires: ${new Date((data.exp as number) * 1000).toISOString()}`);
  if (data.aud) lines.push(`  For: ${data.aud}`);
  return lines.join('\n');
};

export const formatThreadCreated: Formatter = (data) => {
  const lines = ['Thread created'];
  if (data.id) lines.push(`  ID:           ${data.id}`);
  if (data.url) lines.push(`  URL:          ${data.url}`);
  const participants = data.participants as unknown as Array<{ agent_id?: string }>;
  if (Array.isArray(participants)) {
    lines.push(`  Participants: ${participants.length}`);
  }
  const refs = data.refs as unknown as Array<{ type: string; target_id: string }>;
  if (Array.isArray(refs) && refs.length > 0) {
    lines.push(`  Linked:       ${refs.length}`);
  }
  return lines.join('\n');
};

export const formatAssetDownloaded: Formatter = (data) => {
  const lines = [`Downloaded: ${data.file}`];
  if (data.sizeBytes) lines.push(`  Size: ${formatBytes(data.sizeBytes as number)}`);
  if (data.mimeType) lines.push(`  MIME: ${data.mimeType}`);
  return lines.join('\n');
};

export const formatAssetMetadata: Formatter = (data) => {
  const lines = [data.title || '(untitled)'];
  if (data.id) lines.push(`  ID:          ${data.id}`);
  if (data.url) lines.push(`  URL:         ${data.url}`);
  if (data.type) lines.push(`  Type:        ${data.type}`);
  if (data.mimeType) lines.push(`  MIME:        ${data.mimeType}`);
  if (data.description) lines.push(`  Description: ${data.description}`);
  if (data.versionCount !== undefined) lines.push(`  Versions:    ${data.versionCount}`);
  if (data.creatorContext) lines.push(`  Context:     ${data.creatorContext}`);
  if (data.createdAt) lines.push(`  Created:     ${data.createdAt}`);
  return lines.join('\n');
};

export const formatVersionList: Formatter = (data) => {
  const versions = data as unknown as Record<string, unknown>[];
  if (!Array.isArray(versions) || versions.length === 0) {
    return 'No versions found.';
  }
  const lines = [`${versions.length} version(s):\n`];
  for (const v of versions) {
    const label = v.label ? ` "${v.label}"` : '';
    const size = v.sizeBytes ? ` ${formatBytes(v.sizeBytes as number)}` : '';
    lines.push(`  v${v.version}  ${v.id}${label}${size}  ${v.createdAt}`);
  }
  return lines.join('\n');
};

export const formatVersionMetadata: Formatter = (data) => {
  const lines = [`Version ${data.version}`];
  if (data.id) lines.push(`  ID:       ${data.id}`);
  if (data.label) lines.push(`  Label:    ${data.label}`);
  if (data.mimeType) lines.push(`  MIME:     ${data.mimeType}`);
  if (data.sizeBytes) lines.push(`  Size:     ${formatBytes(data.sizeBytes as number)}`);
  if (data.createdAt) lines.push(`  Created:  ${data.createdAt}`);
  return lines.join('\n');
};

export const formatThreadDetails: Formatter = (data) => {
  const lines = [`Thread ${data.id}`];
  if (data.created_by) lines.push(`  Created by:    ${data.created_by}`);
  const participants = data.participants as unknown as Array<{ agent_id?: string; user_id?: string; role?: string }>;
  if (Array.isArray(participants)) {
    lines.push(`  Participants:  ${participants.length}`);
    for (const p of participants) {
      const id = p.agent_id || p.user_id || 'anonymous';
      const role = p.role ? ` (${p.role})` : '';
      lines.push(`    - ${id}${role}`);
    }
  }
  const refs = data.refs as unknown as Array<{ id: string; type: string; target_id: string }>;
  if (Array.isArray(refs) && refs.length > 0) {
    lines.push(`  Linked:        ${refs.length}`);
    for (const r of refs) {
      lines.push(`    - [${r.type}] ${r.target_id}`);
    }
  }
  if (data.resolution) lines.push(`  Resolution:    ${JSON.stringify(data.resolution)}`);
  if (data.created_at) lines.push(`  Created:       ${data.created_at}`);
  if (data.updated_at) lines.push(`  Updated:       ${data.updated_at}`);
  return lines.join('\n');
};

export const formatThreadClosed: Formatter = (data) => {
  const lines = [`Thread ${data.id} closed`];
  if (data.resolution) lines.push(`  Resolution: ${JSON.stringify(data.resolution)}`);
  return lines.join('\n');
};

export const formatParticipantAdded: Formatter = (data) => {
  const lines = ['Participant added'];
  if (data.thread_id) lines.push(`  Thread:  ${data.thread_id}`);
  if (data.agent_id) lines.push(`  Agent:   ${data.agent_id}`);
  return lines.join('\n');
};

export const formatRefsAdded: Formatter = (data) => {
  const refs = data as unknown as Array<{ id: string; type: string; target_id: string }>;
  if (!Array.isArray(refs) || refs.length === 0) return 'No refs added.';
  const lines = [`Added ${refs.length} ref(s):`];
  for (const r of refs) {
    lines.push(`  [${r.type}] ${r.target_id}  (${r.id})`);
  }
  return lines.join('\n');
};

export const formatRefRemoved: Formatter = (data) => {
  return `Removed ref ${data.ref_id} from thread ${data.thread_id}`;
};

export const formatWhoami: Formatter = (data) => {
  const lines = [String(data.agent_id)];
  if (data.alias) lines.push(`  Alias:       ${data.alias}`);
  if (data.registered_at) lines.push(`  Registered:  ${data.registered_at}`);
  return lines.join('\n');
};

export const formatProfileUpdated: Formatter = (data) => {
  const lines = ['Profile updated'];
  if (data.agent_id) lines.push(`  Agent:    ${data.agent_id}`);
  if (data.alias !== undefined) lines.push(`  Alias:    ${data.alias ?? '(none)'}`);
  if (data.metadata) lines.push(`  Metadata: ${JSON.stringify(data.metadata)}`);
  return lines.join('\n');
};

export const formatCollectionRows: Formatter = (data) => {
  const rows = (data as any).rows ?? [];
  const nextCursor = (data as any).nextCursor;
  if (!Array.isArray(rows) || rows.length === 0) return 'No rows.';
  const lines = [`${rows.length} row(s):\n`];
  for (const r of rows) {
    const dataStr = JSON.stringify(r.data);
    const ago = formatTimeAgo(new Date(r.createdAt));
    lines.push(`  ${r.id}  ${ago}  ${dataStr}`);
  }
  if (nextCursor) lines.push(`\n  More rows available. Use --after ${nextCursor}`);
  return lines.join('\n');
};

export const formatRowsAppended: Formatter = (data) => {
  const count = (data as any).count ?? 0;
  const rows = (data as any).rows ?? [];
  const lines = [`Appended ${count} row(s)`];
  for (const r of rows) {
    if (r.id) lines.push(`  ${r.id}`);
  }
  return lines.join('\n');
};

export const formatRowUpdated: Formatter = (data) => {
  return `Updated row ${data.id}`;
};

export const formatRowsDeleted: Formatter = (data) => {
  return `Deleted ${data.deleted} row(s)`;
};

export const formatSearchResults: Formatter = (data) => {
  const results = (data as any).results ?? [];
  const total = (data as any).total ?? results.length;
  if (results.length === 0) return 'No results.';

  const lines: string[] = [`${total} result(s):\n`];
  for (const r of results) {
    const title = r.title || '(untitled)';
    const ago = formatTimeAgo(new Date(r.updated_at));
    if (r.type === 'thread') {
      const state = r.thread?.state === 'closed' ? '[closed]' : '[open]  ';
      const intent = r.thread?.last_intent ? `  last: ${r.thread.last_intent}` : '';
      const participants = r.thread?.participant_count != null
        ? `${r.thread.participant_count} participant${r.thread.participant_count !== 1 ? 's' : ''}`
        : '';
      lines.push(`  thread  ${state}  ${r.id}  ${participants.padEnd(16)}${intent}  ${ago}`);
      if (title !== '(untitled)') lines.push(`          ${title}`);
    } else {
      const assetType = (r.asset?.asset_type ?? '').padEnd(10);
      const versions = r.asset?.version_count ? `v${r.asset.version_count}` : '';
      lines.push(`  asset   ${assetType}  ${r.id}  ${title}  ${versions}  ${ago}`);
      if (r.url) lines.push(`          ${r.url}`);
    }
  }
  if (results.length < total) {
    lines.push(`\n  Showing ${results.length} of ${total}. Use --offset ${results.length} for more.`);
  }
  return lines.join('\n');
};

export const formatTeamCreated: Formatter = (data) => {
  const lines = [`Team created: @${data.slug}`];
  if (data.name && data.name !== data.slug) lines.push(`  Name: ${data.name}`);
  if (data.id) lines.push(`  ID:   ${data.id}`);
  return lines.join('\n');
};

export const formatTeamList: Formatter = (data) => {
  const teams = data as unknown as Array<{ slug: string; name: string; member_count: number; id: string }>;
  if (!Array.isArray(teams) || teams.length === 0) return 'No teams found.';
  const localTeams = loadTeams();
  const lines = [`${teams.length} team(s):\n`];
  for (const t of teams) {
    const alias = localTeams[t.slug]?.alias;
    const aliasSuffix = alias ? `  (alias: ${alias})` : '';
    lines.push(`  @${t.slug.padEnd(24)} ${String(t.member_count).padStart(3)} member(s)  ${t.id}${aliasSuffix}`);
  }
  return lines.join('\n');
};

export const formatTeamDetails: Formatter = (data) => {
  const lines = [`@${data.slug}  —  ${data.name}`];
  if (data.description) lines.push(`  ${data.description}`);
  lines.push(`  ID:    ${data.id}`);
  lines.push(`  Owner: ${data.owner_id}`);
  const members = data.members as Array<{ agent_id: string; alias?: string | null; joined_at: string }> | undefined;
  if (Array.isArray(members) && members.length > 0) {
    lines.push(`  Members (${members.length}):`);
    for (const m of members) {
      const label = m.alias ? `${m.alias} (${m.agent_id})` : m.agent_id;
      lines.push(`    ${label}`);
    }
  }
  return lines.join('\n');
};

export const formatTeamInvite: Formatter = (data) => {
  const lines = ['Invite link generated'];
  if (data.token) lines.push(`  Token:   ${data.token}`);
  if (data.expires_in) lines.push(`  Expires: ${data.expires_in}`);
  return lines.join('\n');
};

export const formatSelfUpdate: Formatter = (data) => {
  if (data.status === 'failed') {
    return data.message as string;
  }

  if (data.status === 'current') {
    const lines = [`@tokenrip/cli ${data.version} is already current`];
    if (data.skill_file_path) lines.push(`Skill file: ${data.skill_file_path}`);
    return lines.join('\n');
  }

  // updated
  const lines = [`Updated @tokenrip/cli ${data.from} → ${data.to}`];

  if (data.skill_file_path) {
    const label = data.skill_changed ? 'Skill file refreshed' : 'Skill file current';
    lines.push(`${label} → ${data.skill_file_path}`);
    lines.push('');
    lines.push(`Reload in Claude Code:  npx skills add tokenrip/cli`);
    lines.push(`Load manually:          ${data.skill_file_path}`);
  } else {
    lines.push('');
    lines.push('Reload your agent skill:');
    lines.push('  Claude Code:  npx skills add tokenrip/cli');
    if (data.skill_url) lines.push(`  Load from:    ${data.skill_url}`);
  }

  if (data.message) {
    lines.push('');
    lines.push(data.message as string);
  }

  return lines.join('\n');
};

function formatTimeAgo(date: Date): string {
  const seconds = Math.floor((Date.now() - date.getTime()) / 1000);
  if (seconds < 60) return `${seconds}s ago`;
  if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
  if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`;
  return `${Math.floor(seconds / 86400)}d ago`;
}

function formatBytes(bytes: number): string {
  if (bytes === 0) return '0 B';
  const units = ['B', 'KB', 'MB', 'GB'];
  const i = Math.min(Math.floor(Math.log(bytes) / Math.log(1024)), units.length - 1);
  const value = bytes / Math.pow(1024, i);
  return `${value.toFixed(i === 0 ? 0 : 1)} ${units[i]}`;
}

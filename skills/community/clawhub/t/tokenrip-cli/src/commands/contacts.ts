import { loadContacts, addContactWithSync, removeContactWithSync, syncFromServer } from '../contacts.js';
import { outputSuccess } from '../output.js';
import { formatContacts, formatContactResolved, formatContactSaved, formatContactRemoved, formatConfigSaved } from '../formatters.js';
import { CliError } from '../errors.js';
import type { AxiosInstance } from 'axios';

async function tryGetAuthClient(): Promise<AxiosInstance | null> {
  try {
    const { requireAuthClient } = await import('../auth-client.js');
    return requireAuthClient().client;
  } catch {
    return null;
  }
}

export async function contactsAdd(
  name: string,
  agentId: string,
  options: { alias?: string; notes?: string },
): Promise<void> {
  const client = await tryGetAuthClient();
  await addContactWithSync(client, name, agentId, { alias: options.alias, notes: options.notes });
  outputSuccess({
    name,
    agent_id: agentId,
    alias: options.alias ?? null,
    notes: options.notes ?? null,
    message: `Contact "${name}" saved`,
  }, formatContactSaved);
}

export async function contactsList(): Promise<void> {
  const contacts = loadContacts();
  outputSuccess(contacts as unknown as Record<string, unknown>, formatContacts);
}

export async function contactsResolve(name: string): Promise<void> {
  const contacts = loadContacts();
  if (!contacts[name]) {
    throw new CliError('CONTACT_NOT_FOUND', `Contact "${name}" not found`);
  }
  outputSuccess({ name, agent_id: contacts[name].agent_id }, formatContactResolved);
}

export async function contactsRemove(name: string): Promise<void> {
  const client = await tryGetAuthClient();
  await removeContactWithSync(client, name);
  outputSuccess({ name, message: `Contact "${name}" removed` }, formatContactRemoved);
}

export async function contactsSync(): Promise<void> {
  const { requireAuthClient } = await import('../auth-client.js');
  const { client } = requireAuthClient();
  const contacts = await syncFromServer(client);
  const count = Object.keys(contacts).length;
  outputSuccess({ count, message: `Synced ${count} contact(s)` }, formatConfigSaved);
}

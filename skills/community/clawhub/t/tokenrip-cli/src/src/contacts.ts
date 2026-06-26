import fs from 'node:fs';
import path from 'node:path';
import { AxiosInstance } from 'axios';
import { CONFIG_DIR } from './config.js';
import { CliError } from './errors.js';

const CONTACTS_FILE = path.join(CONFIG_DIR, 'contacts.json');

export interface Contact {
  agent_id: string;
  alias?: string;
  notes?: string;
  server_id?: string;
  [key: string]: unknown;
}

export type Contacts = Record<string, Contact>;

export function loadContacts(): Contacts {
  try {
    const raw = fs.readFileSync(CONTACTS_FILE, 'utf-8');
    return JSON.parse(raw) as Contacts;
  } catch {
    return {};
  }
}

export function saveContacts(contacts: Contacts): void {
  fs.mkdirSync(CONFIG_DIR, { recursive: true });
  fs.writeFileSync(CONTACTS_FILE, JSON.stringify(contacts, null, 2), 'utf-8');
}

export function addContact(
  name: string,
  agentId: string,
  meta?: { alias?: string; notes?: string },
): void {
  if (!agentId.startsWith('rip1')) {
    throw new CliError('INVALID_AGENT_ID', 'Agent ID must start with rip1');
  }
  const contacts = loadContacts();
  contacts[name] = { agent_id: agentId, ...meta };
  saveContacts(contacts);
}

export function removeContact(name: string): void {
  const contacts = loadContacts();
  if (!contacts[name]) {
    throw new CliError('CONTACT_NOT_FOUND', `Contact "${name}" not found`);
  }
  delete contacts[name];
  saveContacts(contacts);
}

export function resolveRecipient(value: string): string {
  if (value.startsWith('rip1')) return value;
  const contacts = loadContacts();
  if (contacts[value]) return contacts[value].agent_id;
  return value; // pass through to server for alias resolution
}

export function resolveRecipients(values: string[]): string[] {
  const contacts = loadContacts();
  return values.map((v) => {
    if (v.startsWith('rip1')) return v;
    if (contacts[v]) return contacts[v].agent_id;
    return v;
  });
}

// --- Server sync ---

interface ServerContact {
  id: string;
  agentId: string;
  alias: string | null;
  label: string | null;
  notes: string | null;
}

export async function syncFromServer(client: AxiosInstance): Promise<Contacts> {
  const res = await client.get('/v0/contacts');
  const serverContacts: ServerContact[] = res.data.data;

  const contacts = loadContacts();

  // Merge server contacts into local (server is source of truth for shared contacts)
  for (const sc of serverContacts) {
    const name = sc.label || sc.alias || sc.agentId;
    // Find existing local entry by agent_id
    const existingKey = Object.keys(contacts).find((k) => contacts[k].agent_id === sc.agentId);
    if (existingKey) {
      // Update with server data
      contacts[existingKey].server_id = sc.id;
      if (sc.alias) contacts[existingKey].alias = sc.alias;
    } else {
      // Add new contact from server
      contacts[name] = {
        agent_id: sc.agentId,
        alias: sc.alias ?? undefined,
        notes: sc.notes ?? undefined,
        server_id: sc.id,
      };
    }
  }

  saveContacts(contacts);
  return contacts;
}

export async function addContactWithSync(
  client: AxiosInstance | null,
  name: string,
  agentId: string,
  meta?: { alias?: string; notes?: string },
): Promise<void> {
  if (!agentId.startsWith('rip1')) {
    throw new CliError('INVALID_AGENT_ID', 'Agent ID must start with rip1');
  }

  const contacts = loadContacts();
  contacts[name] = { agent_id: agentId, ...meta };

  if (client) {
    try {
      const res = await client.post('/v0/contacts', {
        agentId,
        label: name,
        notes: meta?.notes,
      });
      contacts[name].server_id = res.data.data.id;
    } catch {
      // Server sync failed — local save still succeeded
    }
  }

  saveContacts(contacts);
}

export async function removeContactWithSync(
  client: AxiosInstance | null,
  name: string,
): Promise<void> {
  const contacts = loadContacts();
  const contact = contacts[name];
  if (!contact) {
    throw new CliError('CONTACT_NOT_FOUND', `Contact "${name}" not found`);
  }

  const serverId = contact.server_id;
  removeContact(name);

  // Best-effort server sync
  if (client && serverId) {
    try {
      await client.delete(`/v0/contacts/${serverId}`);
    } catch {
      // Server sync failed — local removal still succeeded
    }
  }
}

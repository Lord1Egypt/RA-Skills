import { readFileSync, existsSync, mkdirSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { parse as parseYaml } from 'yaml';
import { append, readAll, readRecent, readRange, repair, rotate, prune } from './storage.js';
import { buildDomainConfigs } from './domains.js';
import { EventSchema } from '../validation.js';

const DEFAULT_DATA_DIR = 'event-store-data';

export class EventStore {
  #config;
  #domains;

  constructor(config) {
    this.#config = config || {};
    this.#domains = buildDomainConfigs(this.#config.event_store?.domains);
    this.#ensureDataDir();
  }

  get domains() {
    return Object.keys(this.#domains);
  }

  get domainConfigs() {
    return this.#domains;
  }

  #ensureDataDir() {
    const dir = resolve(this.#config.event_store?.dataDir || DEFAULT_DATA_DIR);
    if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
  }

  #domainFile(domain) {
    if (!this.#domains[domain]) throw new Error(`Unknown domain: ${domain}. Valid: ${Object.keys(this.#domains).join(', ')}`);
    const dir = resolve(this.#config.event_store?.dataDir || DEFAULT_DATA_DIR);
    return resolve(`${dir}/${domain}.jsonl`);
  }

  /**
   * Push an event to a domain. Validates the event schema first.
   */
  async push(domain, event) {
    const validated = EventSchema.parse({ domain, ...event });
    const filePath = this.#domainFile(domain);
    await append(filePath, validated);
  }

  /**
   * Push multiple events atomically (sequential for now).
   */
  async pushBatch(domain, events) {
    for (const event of events) {
      await this.push(domain, event);
    }
  }

  /**
   * Query events from a domain with optional filters.
   */
  query(domain, { type, limit, after, before } = {}) {
    const filePath = this.#domainFile(domain);
    let events = readAll(filePath);

    if (type) events = events.filter(e => e.type === type);
    if (after) events = events.filter(e => new Date(e.timestamp) > new Date(after));
    if (before) events = events.filter(e => new Date(e.timestamp) < new Date(before));
    if (limit) events = events.slice(-limit);

    return events;
  }

  getByDomain(domain) {
    return this.query(domain);
  }

  getRecent(domain, n = 10) {
    const filePath = this.#domainFile(domain);
    return readRecent(filePath, n);
  }

  /**
   * Repair a domain's event file: remove corrupt lines.
   */
  repair(domain) {
    const filePath = this.#domainFile(domain);
    return repair(filePath);
  }

  /**
   * Rotate a domain's event file.
   */
  rotate(domain) {
    const filePath = this.#domainFile(domain);
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const archivePath = filePath.replace('.jsonl', `.${timestamp}.jsonl`);
    rotate(filePath, archivePath);
  }

  /**
   * Cleanup: prune old rotated files, keeping N recent.
   */
  cleanup(keepCount = 10) {
    const dir = resolve(this.#config.event_store?.dataDir || DEFAULT_DATA_DIR);
    prune(dir, keepCount);
  }
}
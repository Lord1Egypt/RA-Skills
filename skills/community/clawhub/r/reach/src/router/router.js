import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const SITES_PATH = path.join(__dirname, '..', '..', 'data', 'sites.json');

/**
 * The Router — intelligent layer selector.
 * Decides which primitive to use and at which interaction layer.
 *
 * Priority: API > HTTP > accessibility tree > browser > vision
 */
class Router {
  constructor() {
    this.sites = this.loadSites();
  }

  loadSites() {
    if (fs.existsSync(SITES_PATH)) {
      try {
        return JSON.parse(fs.readFileSync(SITES_PATH, 'utf-8'));
      } catch {
        return {};
      }
    }
    return {};
  }

  saveSites() {
    fs.writeFileSync(SITES_PATH, JSON.stringify(this.sites, null, 2));
  }

  /**
   * Get known info about a domain.
   */
  getSiteInfo(url) {
    try {
      const domain = new URL(url).hostname;
      return this.sites[domain] || null;
    } catch {
      return null;
    }
  }

  /**
   * Store learned info about a domain.
   */
  learnSite(url, info) {
    try {
      const domain = new URL(url).hostname;
      this.sites[domain] = { ...this.sites[domain], ...info, lastUpdated: new Date().toISOString() };
      this.saveSites();
    } catch {}
  }

  /**
   * Attach identity context for reputation-gated routing.
   * @param {object|null} identity - Exo identity from resolveIdentity()
   */
  setIdentity(identity) {
    this.identity = identity;
  }

  /**
   * Route a task to the best primitive and layer.
   *
   * @param {object} task
   * @param {string} task.type - 'read' | 'interact' | 'auth' | 'sign' | 'store' | 'monitor' | 'pay'
   * @param {string} task.url - Target URL
   * @param {object} task.params - Task-specific parameters
   * @returns {object} { primitive, method, layer, params, reason }
   */
  route(task) {
    const { type, url, params = {} } = task;
    const site = url ? this.getSiteInfo(url) : null;

    switch (type) {
      case 'read':
        return this.routeRead(url, site, params);
      case 'interact':
        return this.routeInteract(url, site, params);
      case 'auth':
        return this.routeAuth(url, site, params);
      case 'sign':
        return { primitive: 'sign', method: 'sign', layer: 'crypto', params, reason: 'Crypto operations use sign primitive directly' };
      case 'store':
        return { primitive: 'persist', method: params.value !== undefined ? 'persist' : 'recall', layer: 'local', params, reason: 'Local storage' };
      case 'monitor':
        return { primitive: 'observe', method: 'observe', layer: 'network', params, reason: 'Monitoring via poll, websocket, webhook, or contract events' };
      case 'pay':
        return { primitive: 'pay', method: 'pay', layer: 'crypto', params, reason: 'ETH/ERC-20 transfer or x402 payment' };
      default:
        return this.routeDefault(url, site, params);
    }
  }

  routeRead(url, site, params) {
    // Known API available? Use it
    if (site?.api) {
      return {
        primitive: 'fetch',
        method: 'fetch',
        layer: 'api',
        params: { url: site.api.endpoint || url, format: 'json', headers: site.api.headers || {} },
        reason: `Known API for ${new URL(url).hostname}`,
      };
    }

    // Needs JavaScript to render?
    if (site?.needsJS) {
      return {
        primitive: 'fetch',
        method: 'fetch',
        layer: 'browser',
        params: { url, format: params.format || 'markdown', javascript: true },
        reason: 'Site requires JavaScript rendering',
      };
    }

    // Needs auth?
    if (site?.needsAuth) {
      return {
        primitive: 'fetch',
        method: 'fetch',
        layer: 'browser',
        params: { url, format: params.format || 'markdown', javascript: true, session: new URL(url).hostname },
        reason: 'Site requires authentication — using browser with saved session',
      };
    }

    // Default: try HTTP first (fetch handles fallback to browser internally)
    return {
      primitive: 'fetch',
      method: 'fetch',
      layer: 'http',
      params: { url, format: params.format || 'markdown' },
      reason: 'Default: HTTP with automatic browser fallback',
    };
  }

  routeInteract(url, site, params) {
    const route = {
      primitive: 'act',
      method: 'act',
      layer: 'browser',
      params: { url, ...params },
      reason: 'Web interaction requires browser',
    };

    // Reputation-gated behavior
    if (this.identity) {
      const rep = this.identity.reputation || 0;
      if (rep > 100) {
        route.params._trustedAgent = true;
        route.reason += ' [trusted agent — rep > 100]';
      }
      if (rep > 500) {
        route.params._skipCaptcha = true;
        route.params._presentIdentity = true;
        route.reason += ' [high rep — present identity instead of CAPTCHA]';
      }
    }

    return route;
  }

  routeAuth(url, site, params) {
    // Check for existing session
    if (params.method === 'cookie') {
      return {
        primitive: 'authenticate',
        method: 'authenticate',
        layer: 'local',
        params: { service: params.service, method: 'cookie' },
        reason: 'Reuse saved session cookies',
      };
    }

    if (params.method === 'apikey') {
      return {
        primitive: 'authenticate',
        method: 'authenticate',
        layer: 'local',
        params: { service: params.service, method: 'apikey', credentials: params.credentials },
        reason: 'API key authentication — no browser needed',
      };
    }

    // Browser-based login
    return {
      primitive: 'authenticate',
      method: 'authenticate',
      layer: 'browser',
      params: { service: params.service, method: 'login', credentials: params.credentials },
      reason: 'Browser-based login flow',
    };
  }

  routeDefault(url, site, params) {
    // Best guess
    if (!url) {
      return { primitive: 'persist', method: 'recall', layer: 'local', params, reason: 'No URL — assuming local operation' };
    }
    return this.routeRead(url, site, params);
  }
}

export default Router;
export { Router };

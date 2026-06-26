/**
 * XO Protocol SDK
 *
 * Minimal SDK for the XO Protocol Dating Intelligence API.
 * Zero dependencies — uses native fetch.
 *
 * @example
 *   import { XOClient } from '@xo-protocol/sdk'
 *
 *   const xo = new XOClient({ apiKey: 'your-api-key' })
 *   xo.setAccessToken(token)
 *   const identity = await xo.verifyIdentity()
 */

const BASE_URL = "https://protocol.xoxo.space";
const AUTHORIZE_URL = "https://xoxo.space/en/oauth/authorize";

class XOClient {
  /**
   * @param {object} options
   * @param {string} options.apiKey - Your XO Protocol API key
   * @param {string} [options.baseUrl] - API base URL (default: production)
   */
  constructor({ apiKey, baseUrl = BASE_URL }) {
    if (!apiKey) throw new Error("apiKey is required");
    this._apiKey = apiKey;
    this._baseUrl = baseUrl.replace(/\/$/, "");
    this._accessToken = null;
  }

  /**
   * Set the access token after OAuth flow completes.
   * @param {string} token - JWT access token
   */
  setAccessToken(token) {
    this._accessToken = token;
  }

  // ---------------------------------------------------------------------------
  // OAuth helpers
  // ---------------------------------------------------------------------------

  /**
   * Generate an OAuth authorization URL.
   *
   * @param {object} options
   * @param {string} options.clientId
   * @param {string} options.redirectUri
   * @param {string} options.state - CSRF protection token
   * @param {string[]} [options.scopes] - Default: all scopes
   * @returns {string} The authorization URL to redirect the user to
   *
   * @example
   *   const url = xo.getAuthorizationUrl({
   *     clientId: 'my_app',
   *     redirectUri: 'https://myapp.com/callback',
   *     state: crypto.randomUUID(),
   *   })
   *   // redirect user to `url`
   */
  getAuthorizationUrl({
    clientId,
    redirectUri,
    state,
    scopes = ["identity", "connections", "reputation", "social_signals", "profile", "newsfeed"],
  }) {
    const params = new URLSearchParams({
      client_id: clientId,
      redirect_uri: redirectUri,
      scope: scopes.join(","),
      state,
      response_type: "code",
    });
    return `${AUTHORIZE_URL}?${params}`;
  }

  /**
   * Exchange an authorization code for an access token.
   *
   * @param {object} options
   * @param {string} options.code - Authorization code from redirect
   * @param {string} options.clientId
   * @param {string} options.redirectUri
   * @param {string} [options.clientSecret] - Required for confidential clients
   * @param {string} [options.codeVerifier] - Required for PKCE flow
   * @returns {Promise<{access_token: string, token_type: string, expires_in: number, scope: string}>}
   */
  async exchangeCode({ code, clientId, redirectUri, clientSecret, codeVerifier }) {
    const body = {
      grant_type: "authorization_code",
      code,
      client_id: clientId,
      redirect_uri: redirectUri,
    };
    if (clientSecret) body.client_secret = clientSecret;
    if (codeVerifier) body.code_verifier = codeVerifier;

    const data = await this._post("/protocol/v1/auth/token", body);
    this._accessToken = data.access_token;
    return data;
  }

  // ---------------------------------------------------------------------------
  // API methods
  // ---------------------------------------------------------------------------

  /**
   * Verify the authenticated user's identity.
   *
   * @returns {Promise<{verified: boolean, trust_score: number, has_minted_sbt: boolean, attestations: Array, member_since: string}>}
   *
   * @example
   *   const id = await xo.verifyIdentity()
   *   if (id.verified && id.trust_score > 0.8) {
   *     showVerifiedBadge()
   *   }
   */
  async verifyIdentity() {
    return this._get("/protocol/v1/identity/verify");
  }

  /**
   * Search for compatible connections.
   *
   * @param {object} [options]
   * @param {number} [options.limit=10] - Max results (1–50)
   * @param {string} [options.topicIds] - Comma-separated topic IDs
   * @param {string} [options.cursor] - Pagination cursor
   * @returns {Promise<{connections: Array<{tmp_id: string, compatibility_score: number|null, topics: string[], verified: boolean}>, cursor: string|null, total: number}>}
   */
  async searchConnections({ limit = 10, topicIds, cursor } = {}) {
    const params = { limit };
    if (topicIds) params.topicIds = topicIds;
    if (cursor) params.cursor = cursor;
    return this._get("/protocol/v1/connections/search", params);
  }

  /**
   * Get reputation tier and score.
   *
   * @param {string} [token='me'] - 'me' or a tmp_id from connections search
   * @returns {Promise<{tier: string, reputation_score: number}>}
   *
   * @example
   *   const rep = await xo.getReputation()
   *   console.log(`Tier: ${rep.tier}, Score: ${rep.reputation_score}`)
   *   // Tier: gold, Score: 0.72
   */
  async getReputation(token = "me") {
    return this._get(`/protocol/v1/reputation/${token}`);
  }

  /**
   * Get social engagement score.
   *
   * @param {string} [token='me'] - 'me' or a tmp_id from connections search
   * @returns {Promise<{engagement_score: number|null, confidence: number}>}
   *
   * @example
   *   const signals = await xo.getSocialSignals()
   *   if (signals.confidence > 0.5) {
   *     // engagement_score is reliable enough to use
   *     applyEngagementFilter(signals.engagement_score)
   *   }
   */
  async getSocialSignals(token = "me") {
    return this._get(`/protocol/v1/social-signals/${token}`);
  }

  /**
   * Get user profile preferences. Requires `profile` scope.
   *
   * @param {string} [token='me'] - 'me' or a tmp_id from connections search
   * @returns {Promise<{interests: string[], topics: string[], preferences: object}>}
   */
  async getProfile(token = "me") {
    return this._get(`/protocol/v1/profile/${token}`);
  }

  /**
   * Get a connection's public newsfeed posts. Requires `newsfeed` scope.
   *
   * @param {string} tmpId - A tmp_id from connections search
   * @param {object} [options]
   * @param {number} [options.limit=20] - Max posts (1–50)
   * @param {string} [options.cursor] - Pagination cursor
   * @returns {Promise<{posts: Array<{post_id: string, content: string, topics: string[], created_at: string}>, cursor: string|null, total: number}>}
   */
  async getNewsfeed(tmpId, { limit = 20, cursor } = {}) {
    const params = { limit };
    if (cursor) params.cursor = cursor;
    return this._get(`/protocol/v1/newsfeed/${tmpId}`, params);
  }

  /**
   * Get a full trust profile in one call (identity + reputation + social signals).
   *
   * @returns {Promise<{identity: object, reputation: object, socialSignals: object}>}
   *
   * @example
   *   const profile = await xo.getTrustProfile()
   *   // {
   *   //   identity:      { verified: true, trust_score: 1.0, ... },
   *   //   reputation:    { tier: 'gold', reputation_score: 0.72 },
   *   //   socialSignals: { engagement_score: 0.45, confidence: 0.9 }
   *   // }
   */
  async getTrustProfile() {
    const [identity, reputation, socialSignals] = await Promise.all([
      this.verifyIdentity(),
      this.getReputation(),
      this.getSocialSignals(),
    ]);
    return { identity, reputation, socialSignals };
  }

  // ---------------------------------------------------------------------------
  // Internal
  // ---------------------------------------------------------------------------

  _headers() {
    const h = {
      "X-API-Key": this._apiKey,
      "Content-Type": "application/json",
    };
    if (this._accessToken) {
      h["Authorization"] = `Bearer ${this._accessToken}`;
    }
    return h;
  }

  async _get(path, params) {
    let url = `${this._baseUrl}${path}`;
    if (params) {
      url += "?" + new URLSearchParams(params);
    }
    const res = await fetch(url, { headers: this._headers() });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new XOError(res.status, err);
    }
    return res.json();
  }

  async _post(path, body) {
    const res = await fetch(`${this._baseUrl}${path}`, {
      method: "POST",
      headers: this._headers(),
      body: JSON.stringify(body),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new XOError(res.status, err);
    }
    return res.json();
  }
}

class XOError extends Error {
  constructor(status, body) {
    super(body.detail || body.title || `HTTP ${status}`);
    this.name = "XOError";
    this.status = status;
    this.type = body.type || null;
  }
}

module.exports = { XOClient, XOError };

const https = require("https");
const http = require("http");
const fs = require("fs");
const path = require("path");
const { randomBytes } = require("crypto");

const DEFAULT_TIMEOUT = 30000;
const MAX_RETRIES = 2;
const RETRY_DELAY = 1000;
const DELETE_CHUNK_RETRIES = 3;
const DELETE_CHUNK_RETRY_DELAY = 1000;

function normalizeBaseUrl(baseUrl) {
  const value = String(baseUrl || "").trim().replace(/\/+$/, "");
  if (!value) return value;
  return /^[a-z][a-z0-9+.-]*:\/\//i.test(value) ? value : `http://${value}`;
}

function multipartName(value) {
  const name = String(value);
  if (/[\r\n\x00]/.test(name)) throw new Error("Multipart names must not contain CR, LF, or NUL");
  return name.replace(/\\/g, "\\\\").replace(/"/g, '\\"');
}

function rejectRemovedParameters(data, replacements) {
  for (const [key, replacement] of Object.entries(replacements)) {
    if (Object.prototype.hasOwnProperty.call(data, key)) {
      throw new Error(`Unsupported parameter ${key}. ${replacement}`);
    }
  }
}

const REMOVED_CHAT_PARAMETERS = {
  legacy: "Use the current streaming format.",
  conversation_id: "Use session_id.",
  pass_all_history: "Use pass_all_history_messages.",
};

function validateChunkUpdate(data) {
  if (data.available !== undefined && ![true, false, 0, 1, "0", "1"].includes(data.available)) {
    throw new Error("available must be 0, 1, true, or false");
  }
  if (data.image_update_mode !== undefined) {
    if (!["append", "replace", "remove"].includes(data.image_update_mode)) {
      throw new Error("image_update_mode must be append, replace, or remove");
    }
    if (data.image_update_mode !== "remove" && !data.image_base64) {
      throw new Error("image_base64 is required for append or replace");
    }
    if (data.image_update_mode === "remove" && data.image_base64 !== undefined) {
      throw new Error("Do not supply image_base64 when removing an image");
    }
  }
}

class RagflowClient {
  constructor(baseUrl, apiKey, options = {}) {
    if (!baseUrl) throw new Error("RAGFLOW_URL is required");
    if (!apiKey) throw new Error("RAGFLOW_API_KEY is required");
    this.baseUrl = normalizeBaseUrl(baseUrl);
    this.apiKey = apiKey;
    this.allowDestructive = options.allowDestructive === true;
    this.apiPrefix = "/api/v1";
    this.timeout = options.timeout || DEFAULT_TIMEOUT;
    this.maxRetries = options.maxRetries !== undefined ? options.maxRetries : MAX_RETRIES;
  }

  _assertDestructiveAllowed(method, endpoint, payload = {}) {
    payload = payload || {};
    const route = this._buildUrl(endpoint).pathname.replace(/^\/api\/v1/, "");
    const deletesResources = method.toUpperCase() === "DELETE";
    // Starting parsing clears old chunks and tasks before scheduling new work.
    const reparse = method.toUpperCase() === "POST" && /^\/datasets\/[^/]+\/chunks$/.test(route);
    const metadataChange = /\/metadata\/update$|\/documents\/metadatas$/.test(route) &&
      (Boolean(payload.deletes?.length) || !payload.selector?.document_ids?.length);
    const purgeIngestion = route === "/documents/ingest" && String(payload.run ?? "1") === "1" && Boolean(payload.delete);
    if (!this.allowDestructive && (deletesResources || reparse || metadataChange || purgeIngestion)) {
      const error = new Error("Destructive operation requires explicit confirmation: use --confirm-destructive in the CLI or allowDestructive: true on a dedicated client after verifying the target.");
      error.code = "CONFIRMATION_REQUIRED";
      throw error;
    }
  }

  async request(method, endpoint, options = {}) {
    this._assertDestructiveAllowed(method, endpoint, options.json);
    const isMultipart = options.files && options.files.length > 0;

    const headers = {
      Authorization: `Bearer ${options.authToken || this.apiKey}`,
    };

    let body;
    if (isMultipart) {
      const boundary = "----FormBoundary" + randomBytes(24).toString("hex");
      headers["Content-Type"] = `multipart/form-data; boundary=${boundary}`;
      body = this._buildMultipart(options.files, options.json || {}, boundary);
    } else if (options.json) {
      headers["Content-Type"] = "application/json";
      body = JSON.stringify(options.json);
    }

    if (body) {
      headers["Content-Length"] = Buffer.byteLength(body);
    }

    let lastError;
    const attempts = this.maxRetries + 1;
    for (let attempt = 1; attempt <= attempts; attempt++) {
      try {
        return await this._doRequest(
          method,
          endpoint,
          headers,
          body,
          options.timeout,
          options.apiPrefix,
          options.rawResponse,
          options.fileResponse
        );
      } catch (err) {
        lastError = err;
        if (this._isRetryable(err) && attempt < attempts) {
          await this._delay(RETRY_DELAY * attempt);
          continue;
        }
        throw err;
      }
    }
    throw lastError;
  }

  _isRetryable(err) {
    if (err.code === "ECONNRESET" || err.code === "ECONNREFUSED" || err.code === "ETIMEDOUT") return true;
    if (err.message && (err.message.includes("socket hang up") || err.message.includes("network"))) return true;
    if (err.code && err.code >= 500) return true;
    return false;
  }

  _delay(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  _isDeleteChunkVisibilityError(err) {
    return err && /rm_chunk deleted chunks 0, expect \d+/.test(err.message || "");
  }

  _isNotFoundError(err) {
    return err && (err.code === 404 || err.status === 404 || /not found/i.test(err.message || ""));
  }

  _decorateDeleteChunkError(err, details) {
    err.delete_chunk_details = details;
    const existing = details.existing_chunk_ids || [];
    const missing = details.missing_chunk_ids || [];
    const parts = [];
    if (existing.length) parts.push(`existing: ${existing.join(",")}`);
    if (missing.length) parts.push(`missing: ${missing.join(",")}`);
    if (parts.length) err.message = `${err.message} (${parts.join("; ")})`;
    return err;
  }

  _doRequest(method, endpoint, headers, body, timeoutOverride, apiPrefix = this.apiPrefix, rawResponse = false, fileResponse = false) {
    const url = this._buildUrl(endpoint, apiPrefix);
    const timeout = timeoutOverride || this.timeout;

    return new Promise((resolve, reject) => {
      const mod = url.protocol === "https:" ? https : http;
      const req = mod.request(url, { method, headers }, (res) => {
        const chunks = [];
        res.on("data", (c) => chunks.push(c));
        res.on("end", () => {
          const bytes = Buffer.concat(chunks);
          const raw = bytes.toString("utf-8");
          if (fileResponse) {
            let data;
            try { data = JSON.parse(raw); } catch { /* Binary file. */ }
            const disposition = res.headers["content-disposition"] || "";
            const apiError = !disposition && data && typeof data.code === "number" && data.code !== 0;
            if (res.statusCode < 200 || res.statusCode >= 300 || apiError) {
              const err = new Error(data?.message || `HTTP ${res.statusCode}`);
              err.status = res.statusCode;
              err.code = data?.code;
              reject(err);
              return;
            }
            const encodedName = disposition.match(/filename\*=UTF-8''([^;]+)/i)?.[1];
            let name = disposition.match(/filename="([^"]+)"|filename=([^;]+)/i)?.slice(1).find(Boolean) || "";
            if (encodedName) {
              try { name = decodeURIComponent(encodedName); } catch { /* Use plain filename. */ }
            }
            resolve({ content: bytes.toString("base64"), encoding: "base64", name,
              content_type: res.headers["content-type"] || "application/octet-stream", size: bytes.length });
            return;
          }
          try {
            const data = JSON.parse(raw);
            if (rawResponse) {
              if (res.statusCode >= 200 && res.statusCode < 300) {
                resolve(data);
              } else {
                const err = new Error(data.message || `HTTP ${res.statusCode}`);
                err.status = res.statusCode;
                err.response = data;
                reject(err);
              }
              return;
            }
            if (data.code === 0) {
              resolve(data.data !== undefined ? data.data : {});
            } else {
              const err = new Error(data.message || `API error code ${data.code}`);
              err.code = data.code;
              err.status = res.statusCode;
              reject(err);
            }
          } catch {
            const err = new Error(`Invalid JSON response: ${raw.slice(0, 200)}`);
            err.status = res.statusCode;
            reject(err);
          }
        });
      });

      req.setTimeout(timeout, () => {
        req.destroy(new Error(`Request timed out after ${timeout}ms`));
      });

      req.on("error", (err) => {
        err.message = `Request failed: ${err.message}`;
        reject(err);
      });
      if (body) req.write(body);
      req.end();
    });
  }

  async validateConnection() {
    try {
      await this.listDatasets({ page: 1, page_size: 1 });
      return true;
    } catch {
      return false;
    }
  }

  _buildMultipart(files, fields, boundary) {
    const parts = [];
    for (const [key, value] of Object.entries(fields)) {
      parts.push(Buffer.from(
        `--${boundary}\r\nContent-Disposition: form-data; name="${multipartName(key)}"\r\n\r\n${value}`
      ));
      parts.push(Buffer.from("\r\n"));
    }
    for (const file of files) {
      const filePath = typeof file === "object" ? file.path : file;
      const basename = multipartName(typeof file === "object" && file.name ? file.name : path.basename(filePath));
      const content = fs.readFileSync(filePath);
      const header = `--${boundary}\r\nContent-Disposition: form-data; name="file"; filename="${basename}"\r\nContent-Type: application/octet-stream\r\n\r\n`;
      parts.push(Buffer.from(header, "utf-8"));
      parts.push(content);
      parts.push(Buffer.from("\r\n"));
    }
    parts.push(Buffer.from(`--${boundary}--\r\n`, "utf-8"));
    return Buffer.concat(parts);
  }

  async _streamRequest(method, endpoint, json, options = {}) {
    this._assertDestructiveAllowed(method, endpoint, json);
    const url = this._buildUrl(endpoint, options.apiPrefix || this.apiPrefix);
    const body = JSON.stringify(json);
    const timeout = options.timeout || this.timeout * 3;
    const headers = {
      Authorization: `Bearer ${options.authToken || this.apiKey}`,
      "Content-Type": "application/json",
      "Content-Length": Buffer.byteLength(body),
    };

    return new Promise((resolve, reject) => {
      const mod = url.protocol === "https:" ? https : http;
      const req = mod.request(url, { method, headers }, (res) => {
        const chunks = [];
        res.on("data", (c) => chunks.push(c));
        res.on("end", () => {
          const raw = Buffer.concat(chunks).toString("utf-8");
          const lines = raw.split("\n");
          let lastAnswer = "";
          let reference = null;
          let sessionId = null;
          let messageId = null;
          for (const line of lines) {
            if (line.startsWith("data:")) {
              const payload = line.slice(5).trim();
              if (!payload || payload === "[DONE]") continue;
              try {
                const data = JSON.parse(payload);
                if (data.event) {
                  if (data.event === "message" && data.data?.content !== undefined) {
                    lastAnswer += data.data.content;
                  }
                  if (
                    (data.event === "workflow_finished" || data.event === "done") &&
                    data.data?.content !== undefined
                  ) {
                    lastAnswer = data.data.content;
                  }
                  if (
                    (data.event === "workflow_finished" || data.event === "done") &&
                    data.data?.outputs?.content !== undefined &&
                    !lastAnswer
                  ) {
                    lastAnswer = data.data.outputs.content;
                  }
                  if ((data.event === "message_end" || data.event === "done") && data.data?.reference !== undefined) {
                    reference = data.data.reference;
                  }
                  if (
                    (data.event === "workflow_finished" || data.event === "done") &&
                    data.data?.reference !== undefined
                  ) {
                    reference = data.data.reference;
                  }
                  if (data.data?.session_id !== undefined) sessionId = data.data.session_id;
                  if (data.session_id !== undefined) sessionId = data.session_id;
                  if (data.data?.id !== undefined) messageId = data.data.id;
                  if (data.message_id !== undefined) messageId = data.message_id;
                  continue;
                }
                if (data.code === 0) {
                  if (data.data && typeof data.data === "object") {
                    if (data.data.answer !== undefined) lastAnswer = data.data.answer;
                    if (data.data.content !== undefined) lastAnswer += data.data.content;
                    if (data.data.reference) reference = data.data.reference;
                    if (data.data.session_id !== undefined) sessionId = data.data.session_id;
                    if (data.data.id !== undefined) messageId = data.data.id;
                  }
                } else {
                  reject(new Error(data.message || data.data?.message || `API error code ${data.code}`));
                  return;
                }
              } catch {
                // Skip invalid JSON lines
              }
            }
          }
          const result = { answer: lastAnswer, reference };
          if (sessionId !== null) result.session_id = sessionId;
          if (messageId !== null) result.id = messageId;
          resolve(result);
        });
      });

      req.setTimeout(timeout, () => {
        req.destroy(new Error(`Chat request timed out after ${timeout}ms`));
      });

      req.on("error", (err) => {
        err.message = `Request failed: ${err.message}`;
        reject(err);
      });
      req.write(body);
      req.end();
    });
  }

  // ── Dataset ──

  async listDatasets(params = {}) {
    const query = this._buildQuery(params);
    return this.request("GET", `/datasets?${query.toString()}`);
  }

  async getDataset(datasetId) {
    try {
      return await this.request("GET", `/datasets/${datasetId}`);
    } catch (err) {
      if (this._isNotFoundError(err)) {
        throw new Error(`Dataset ${datasetId} not found`);
      }
      throw err;
    }
  }

  async createDataset(data) {
    return this.request("POST", "/datasets", { json: data });
  }

  async updateDataset(datasetId, data) {
    return this.request("PUT", `/datasets/${datasetId}`, { json: data });
  }

  async deleteDatasets(ids) {
    return this.request("DELETE", "/datasets", { json: { ids } });
  }

  // ── Document ──

  async uploadDocuments(datasetId, files, params = {}) {
    return this.request("POST", `/datasets/${datasetId}/documents`, {
      files,
      json: params,
    });
  }

  async listDocuments(datasetId, params = {}) {
    const query = this._buildQuery(params);
    return this.request("GET", `/datasets/${datasetId}/documents?${query.toString()}`);
  }

  async deleteDocuments(datasetId, ids) {
    return this.request("DELETE", `/datasets/${datasetId}/documents`, { json: { ids } });
  }

  async getDocument(datasetId, documentId) {
    const result = await this.listDocuments(datasetId, { id: documentId });
    if (!result || !result.docs || result.docs.length === 0) {
      throw new Error(`Document ${documentId} not found in dataset ${datasetId}`);
    }
    return result.docs[0];
  }

  async updateDocument(datasetId, documentId, data) {
    return this.request("PATCH", `/datasets/${datasetId}/documents/${documentId}`, { json: data });
  }

  // ── Document Download ──

  async downloadDocument(datasetId, documentId) {
    return this.request("GET", `/datasets/${datasetId}/documents/${documentId}`, { fileResponse: true });
  }

  async downloadDocumentById(documentId) {
    return this.request("GET", `/documents/${documentId}`, { fileResponse: true });
  }

  async previewDocument(documentId) {
    return this.request("GET", `/documents/${documentId}/preview`, { fileResponse: true });
  }

  async ingestDocuments(documentIds, options = {}) {
    const run = options.run !== undefined ? String(options.run) : "1";
    const payload = { doc_ids: documentIds, run };
    if (options.delete !== undefined) payload.delete = Boolean(options.delete);
    return this.request("POST", "/documents/ingest", { json: payload });
  }

  // ── Chunk / Parsing ──

  async startParsing(datasetId, documentIds) {
    return this.request("POST", `/datasets/${datasetId}/chunks`, {
      json: { document_ids: documentIds },
    });
  }

  async stopParsing(datasetId, documentIds) {
    return this.request("DELETE", `/datasets/${datasetId}/chunks`, {
      json: { document_ids: documentIds },
    });
  }

  async waitForParsing(datasetId, documentIds, options = {}) {
    const interval = options.interval || 3000;
    const maxWait = options.maxWait || 120000;
    const start = Date.now();

    while (Date.now() - start < maxWait) {
      const docs = await this.listDocuments(datasetId);
      const targets = (docs.docs || docs || []).filter((d) => documentIds.includes(d.id));
      const allDone = targets.every((d) => d.run === "DONE" || d.run === "FAIL");
      if (allDone) return targets;
      await this._delay(interval);
    }
    throw new Error(`Parsing timed out after ${maxWait}ms`);
  }

  async listChunks(datasetId, documentId, params = {}) {
    const query = this._buildQuery(params);
    return this.request(
      "GET",
      `/datasets/${datasetId}/documents/${documentId}/chunks?${query.toString()}`
    );
  }

  async getChunk(datasetId, documentId, chunkId) {
    return this.request(
      "GET",
      `/datasets/${datasetId}/documents/${documentId}/chunks/${chunkId}`
    );
  }

  async _existingChunkIds(datasetId, documentId, chunkIds) {
    const existing = [];
    const missing = [];
    for (const chunkId of chunkIds) {
      try {
        await this.getChunk(datasetId, documentId, chunkId);
        existing.push(chunkId);
      } catch (err) {
        if (this._isNotFoundError(err)) {
          missing.push(chunkId);
          continue;
        }
        throw err;
      }
    }
    return { existing, missing };
  }

  async addChunk(datasetId, documentId, data) {
    return this.request("POST", `/datasets/${datasetId}/documents/${documentId}/chunks`, {
      json: data,
    });
  }

  async deleteChunks(datasetId, documentId, chunkIds, options = {}) {
    const uniqueChunkIds = [...new Set(chunkIds)].filter(Boolean);
    const maxRetries = options.maxRetries !== undefined
      ? options.maxRetries
      : Number(process.env.RAGFLOW_DELETE_CHUNK_RETRIES || DELETE_CHUNK_RETRIES);
    const retryDelay = options.retryDelay !== undefined
      ? options.retryDelay
      : Number(process.env.RAGFLOW_DELETE_CHUNK_RETRY_DELAY_MS || DELETE_CHUNK_RETRY_DELAY);
    let lastError;
    for (let attempt = 0; attempt <= maxRetries; attempt++) {
      try {
        return await this.request("DELETE", `/datasets/${datasetId}/documents/${documentId}/chunks`, {
          json: { chunk_ids: uniqueChunkIds },
        });
      } catch (err) {
        lastError = err;
        if (!this._isDeleteChunkVisibilityError(err)) {
          throw err;
        }
        const { existing, missing } = await this._existingChunkIds(datasetId, documentId, uniqueChunkIds);
        const details = {
          attempt,
          max_retries: maxRetries,
          existing_chunk_ids: existing,
          missing_chunk_ids: missing,
        };
        if (existing.length === 0 || attempt >= maxRetries) {
          throw this._decorateDeleteChunkError(err, details);
        }
        if (typeof options.onRetry === "function") {
          options.onRetry(details);
        }
        await this._delay(retryDelay);
      }
    }
    throw lastError;
  }

  async updateChunk(datasetId, documentId, chunkId, data) {
    validateChunkUpdate(data);
    return this.request(
      "PATCH",
      `/datasets/${datasetId}/documents/${documentId}/chunks/${chunkId}`,
      { json: data }
    );
  }

  async getDocumentStructureGraph(datasetId, documentId) {
    return this.request("GET", `/datasets/${datasetId}/documents/${documentId}/structure/graph`);
  }

  async deleteDocumentStructureGraph(datasetId, documentId) {
    return this.request("DELETE", `/datasets/${datasetId}/documents/${documentId}/structure/graph`);
  }

  // ── Retrieval ──

  async retrieve(params) {
    rejectRemovedParameters(params, { top_k: "Use knn_top_k.", doc_ids: "Use document_ids.", size: "Use page_size." });
    return this.request("POST", "/retrieval", { json: params });
  }

  async updateMetadata(datasetId, data) {
    return this.request("POST", `/datasets/${datasetId}/metadata/update`, { json: data });
  }
  // ── Connector ──

  async listConnectors(params = {}) {
    const query = this._buildQuery(params);
    return this.request("GET", `/connectors?${query.toString()}`);
  }

  async createConnector(data) {
    for (const field of ["name", "source", "config"]) {
      if (!data[field]) throw new Error(`${field} is required`);
    }
    for (const field of ["refresh_freq", "prune_freq", "timeout_secs"]) {
      const value = data[field];
      if (value !== undefined && !(typeof value === "number" && Number.isSafeInteger(value)) &&
          !(typeof value === "string" && /^[+-]?\d+$/.test(value.trim()) && Number.isSafeInteger(Number(value)))) {
        throw new Error(`${field} must be an integer`);
      }
    }
    return this.request("POST", `/connectors`, { json: data });
  }

  async getConnector(connectorId) {
    return this.request("GET", `/connectors/${connectorId}`);
  }

  async updateConnector(connectorId, data) {
    return this.request("PATCH", `/connectors/${connectorId}`, { json: data });
  }

  async deleteConnector(connectorId) {
    return this.request("DELETE", `/connectors/${connectorId}`);
  }

  // ── RAPTOR ──

  async runRaptor(datasetId) {
    return this.request("POST", `/datasets/${datasetId}/index?type=raptor`);
  }

  async traceRaptor(datasetId) {
    return this.request("GET", `/datasets/${datasetId}/index?type=raptor`);
  }

  async getKnowledgeGraph(datasetId) {
    return this.request("GET", `/datasets/${datasetId}/graph`);
  }

  async deleteKnowledgeGraph(datasetId) {
    return this.request("DELETE", `/datasets/${datasetId}/graph`);
  }

  async runGraphRag(datasetId) {
    return this.request("POST", `/datasets/${datasetId}/index?type=graph`);
  }

  async traceGraphRag(datasetId) {
    return this.request("GET", `/datasets/${datasetId}/index?type=graph`);
  }

  // ── Chat Assistant ──

  async listChatAssistants(params = {}) {
    const query = this._buildQuery(params);
    return this.request("GET", `/chats?${query.toString()}`);
  }

  async createChatAssistant(data) {
    return this.request("POST", "/chats", { json: data });
  }

  async updateChatAssistant(chatId, data) {
    return this.request("PUT", `/chats/${chatId}`, { json: data });
  }

  async patchChatAssistant(chatId, data) {
    return this.request("PATCH", `/chats/${chatId}`, { json: data });
  }

  async deleteChatAssistants(ids) {
    return this.request("DELETE", "/chats", { json: { ids } });
  }

  async getChatAssistant(chatId) {
    return this.request("GET", `/chats/${chatId}`);
  }

  // ── Session ──

  async listSessions(chatId, params = {}) {
    const query = this._buildQuery(params);
    return this.request("GET", `/chats/${chatId}/sessions?${query.toString()}`);
  }

  async createSession(chatId, data = {}) {
    return this.request("POST", `/chats/${chatId}/sessions`, { json: data });
  }

  async getSession(chatId, sessionId) {
    return this.request("GET", `/chats/${chatId}/sessions/${sessionId}`);
  }

  async updateSession(chatId, sessionId, data) {
    return this.request("PATCH", `/chats/${chatId}/sessions/${sessionId}`, { json: data });
  }

  async deleteSessions(chatId, ids) {
    return this.request("DELETE", `/chats/${chatId}/sessions`, { json: { ids } });
  }

  // ── Chat (Conversation) ──

  async chat(chatId, sessionId, question, params = {}) {
    rejectRemovedParameters(params, REMOVED_CHAT_PARAMETERS);
    return this._streamRequest(
      "POST", `/chat/completions`,
      { chat_id: chatId, question, session_id: sessionId, ...params }
    );
  }

  async chatSession(chatId, sessionId, data = {}) {
    rejectRemovedParameters(data, REMOVED_CHAT_PARAMETERS);
    const payload = { ...data, chat_id: chatId, session_id: sessionId };
    if (!payload.question && payload.messages) {
      const userMessages = Array.isArray(payload.messages)
        ? payload.messages.filter((message) => message && message.role === "user" && message.content)
        : [];
      const lastUserMessage = userMessages[userMessages.length - 1];
      if (lastUserMessage) payload.question = lastUserMessage.content;
    }
    // preserve messages when pass_all_history_messages is set
    if (!payload.pass_all_history_messages) {
      delete payload.messages;
    }
    if (!payload.question) {
      throw new Error("chatSession requires question or messages with a user message");
    }
    if (data.stream === false || data.stream === "false") {
      return this.request("POST", `/chat/completions`, { json: payload });
    }
    return this._streamRequest("POST", `/chat/completions`, payload);
  }

  // ── Agent ──

  async listAgents(params = {}) {
    const query = this._buildQuery(params);
    return this.request("GET", `/agents?${query.toString()}`);
  }

  async createAgent(data) {
    return this.request("POST", "/agents", { json: data });
  }

  async updateAgent(agentId, data) {
    return this.request("PUT", `/agents/${agentId}`, { json: data });
  }

  async deleteAgents(ids) {
    return Promise.all(ids.map((id) => this.request("DELETE", `/agents/${id}`)));
  }

  // ── Agent Tags ──

  async listAgentTags() {
    return this.request("GET", "/agents/tags");
  }

  async updateAgentTags(agentId, tags) {
    const tagString = Array.isArray(tags) ? tags.join(",") : tags;
    return this.request("PUT", `/agents/${agentId}/tags`, {
      json: { tags: tagString },
    });
  }

  async getAgent(agentId) {
    const result = await this.listAgents({ id: agentId });
    if (!result || result.length === 0) {
      throw new Error(`Agent ${agentId} not found`);
    }
    return result[0];
  }

  // ── Agent Session ──

  async listAgentSessions(agentId, params = {}) {
    const query = this._buildQuery(params);
    return this.request("GET", `/agents/${agentId}/sessions?${query.toString()}`);
  }

  async createAgentSession(agentId, data = {}) {
    return this.request("POST", `/agents/${agentId}/sessions`, { json: data });
  }

  async deleteAgentSessions(agentId, ids) {
    return this.request("DELETE", `/agents/${agentId}/sessions`, { json: { ids } });
  }

  // ── Agent Chat ──

  async agentChat(agentId, sessionId, question, params = {}) {
    const payload = { agent_id: agentId, question, session_id: sessionId, ...params };
    const wantsStream = payload.stream !== false && payload.stream !== "false";
    const primaryPath = "/agents/chat/completions";

    const runAgentChat = async (endpoint, body) => {
      if (!wantsStream) {
        const result = await this.request("POST", endpoint, { json: body });
        return this._normalizeAgentChatResult(result);
      }
      return this._streamRequest("POST", endpoint, body);
    };

    return runAgentChat(primaryPath, payload);
  }

  // Embedded website access

  async listSystemTokens() {
    return this.request("GET", "/system/tokens");
  }

  async createSystemToken() {
    return this.request("POST", "/system/tokens");
  }

  async deleteSystemToken(token) {
    return this.request("DELETE", `/system/tokens/${encodeURIComponent(token)}`);
  }

  async ensureEmbedToken() {
    const tokens = await this.listSystemTokens();
    const tokenList = Array.isArray(tokens) ? tokens : [];
    const reusable = tokenList.find((item) => item && item.beta);
    if (reusable) return reusable;
    return this.createSystemToken();
  }

  async getEmbeddedChatInfo(chatId, beta) {
    return this.request("GET", `/chatbots/${chatId}/info`, { authToken: beta });
  }

  async getEmbeddedAgentInputs(agentId, beta) {
    return this.request("GET", `/agentbots/${agentId}/inputs`, { authToken: beta });
  }

  async ensureEmbeddedChatSession(chatId, beta, data = {}) {
    rejectRemovedParameters(data, REMOVED_CHAT_PARAMETERS);
    if (data.session_id) return data.session_id;
    const bootstrap = { ...data, question: "", stream: true };
    delete bootstrap.session_id;
    const result = await this._streamRequest("POST", `/chatbots/${chatId}/completions`, bootstrap, { authToken: beta });
    if (!result.session_id) {
      throw new Error("Embedded chat did not return a session_id during session bootstrap");
    }
    return result.session_id;
  }

  async embeddedChat(chatId, beta, data = {}) {
    rejectRemovedParameters(data, REMOVED_CHAT_PARAMETERS);
    if (data.stream === false || data.stream === "false") {
      return this.request("POST", `/chatbots/${chatId}/completions`, { authToken: beta, json: data });
    }
    return this._streamRequest("POST", `/chatbots/${chatId}/completions`, data, { authToken: beta });
  }

  async embeddedAgentChat(agentId, beta, data = {}) {
    if (data.stream === false || data.stream === "false") {
      return this.request("POST", `/agentbots/${agentId}/completions`, { authToken: beta, json: data });
    }
    return this._streamRequest("POST", `/agentbots/${agentId}/completions`, data, { authToken: beta });
  }

  // ── LLM Models ──

  async listModels(params = {}) {
    const query = this._buildQuery(params);
    const suffix = query.toString();
    return this.request("GET", `/models${suffix ? `?${suffix}` : ""}`);
  }

  // ── Tenant Models ──

  async listAddedModels(params = {}) {
    return this.listModels(params);
  }

  async listDefaultModels() {
    return this.request("GET", "/models/default");
  }

  async setDefaultModel(data) {
    return this.request("PATCH", "/models/default", { json: data });
  }

  // ── Model Providers ──

  async listProviders(params = {}) {
    const query = this._buildQuery(params);
    const suffix = query.toString();
    return this.request("GET", `/providers${suffix ? `?${suffix}` : ""}`);
  }

  async addProvider(providerName) {
    return this.request("PUT", "/providers", { json: { provider_name: providerName } });
  }

  async getProvider(providerName) {
    return this.request("GET", `/providers/${encodeURIComponent(providerName)}`);
  }

  async deleteProvider(providerName) {
    return this.request("DELETE", `/providers/${encodeURIComponent(providerName)}`);
  }

  async listProviderModels(providerName, params = {}) {
    const query = this._buildQuery(params);
    const suffix = query.toString();
    return this.request(
      "GET",
      `/providers/${encodeURIComponent(providerName)}/models${suffix ? `?${suffix}` : ""}`
    );
  }

  async listProviderInstances(providerName) {
    return this.request("GET", `/providers/${encodeURIComponent(providerName)}/instances`);
  }

  async getProviderInstance(providerName, instanceName) {
    return this.request(
      "GET",
      `/providers/${encodeURIComponent(providerName)}/instances/${encodeURIComponent(instanceName)}`
    );
  }

  async createProviderInstance(providerName, data) {
    if (typeof data.instance_name !== "string" || !/^[0-9A-Za-z_-]+$/.test(data.instance_name)) {
      throw new Error("instance_name must contain only ASCII letters, digits, underscores, or hyphens");
    }
    return this.request("POST", `/providers/${encodeURIComponent(providerName)}/instances`, { json: data });
  }

  async deleteProviderInstances(providerName, instances) {
    return this.request("DELETE", `/providers/${encodeURIComponent(providerName)}/instances`, {
      json: { instances },
    });
  }

  async verifyProvider(providerName, data) {
    return this.request("POST", `/providers/${encodeURIComponent(providerName)}/connection`, { json: data });
  }

  async listInstanceModels(providerName, instanceName, params = {}) {
    const query = this._buildQuery(params);
    const suffix = query.toString();
    return this.request(
      "GET",
      `/providers/${encodeURIComponent(providerName)}/instances/${encodeURIComponent(instanceName)}/models${suffix ? `?${suffix}` : ""}`
    );
  }

  async addInstanceModel(providerName, instanceName, data) {
    return this.request(
      "POST",
      `/providers/${encodeURIComponent(providerName)}/instances/${encodeURIComponent(instanceName)}/models`,
      { json: data }
    );
  }

  async setInstanceModelStatus(providerName, instanceName, modelName, status) {
    return this.request(
      "PATCH",
      `/providers/${encodeURIComponent(providerName)}/instances/${encodeURIComponent(instanceName)}/models/${encodeURIComponent(modelName)}`,
      { json: { status } }
    );
  }

  // ── Helpers ──

  async metadataSummary(datasetId, docIds = []) {
    const query = new URLSearchParams();
    if (docIds.length) {
      query.set("doc_ids", docIds.join(","));
    }
    const suffix = query.toString();
    return this.request("GET", `/datasets/${datasetId}/metadata/summary${suffix ? `?${suffix}` : ""}`);
  }

  async getSystemVersion() {
    return this.request("GET", "/system/version");
  }

  async getSystemHealth() {
    return this.request("GET", "/system/healthz", { rawResponse: true });
  }

  async getLogLevels() {
    return this.request("GET", "/system/config/log");
  }

  async setLogLevel(pkgName, level) {
    return this.request("PUT", "/system/config/log", { json: { pkg_name: pkgName, level } });
  }

  _buildUrl(endpoint, apiPrefix = this.apiPrefix) {
    const prefix = apiPrefix.replace(/\/+$/, "");
    const suffix = endpoint.startsWith("/") ? endpoint : `/${endpoint}`;
    return new URL(prefix + suffix, this.baseUrl);
  }

  _buildQuery(params) {
    const query = new URLSearchParams();
    for (const [k, v] of Object.entries(params)) {
      if (v === undefined || v === null) continue;
      if (Array.isArray(v)) {
        for (const item of v) {
          if (item !== undefined && item !== null) query.append(k, String(item));
        }
      } else {
        query.set(k, String(v));
      }
    }
    return query;
  }

  _normalizeAgentChatResult(result) {
    if (result && typeof result === "object") {
      if (result.answer !== undefined || result.reference !== undefined) return result;
      if (result.event && result.data && typeof result.data === "object") {
        const answer = result.data.content !== undefined
          ? result.data.content
          : result.data.outputs?.content !== undefined
            ? result.data.outputs.content
            : "";
        const reference = result.data.reference !== undefined ? result.data.reference : null;
        const normalized = { answer, reference };
        if (result.session_id !== undefined) normalized.session_id = result.session_id;
        if (result.message_id !== undefined) normalized.id = result.message_id;
        return normalized;
      }
    }
    return result;
  }

}

function createClient(options = {}) {
  return new RagflowClient(
    process.env.RAGFLOW_URL,
    process.env.RAGFLOW_API_KEY,
    options
  );
}

module.exports = { RagflowClient, createClient };

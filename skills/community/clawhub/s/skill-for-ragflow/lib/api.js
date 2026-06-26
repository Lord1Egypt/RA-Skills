const https = require("https");
const http = require("http");
const fs = require("fs");
const path = require("path");

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

class RagflowClient {
  constructor(baseUrl, apiKey, options = {}) {
    if (!baseUrl) throw new Error("RAGFLOW_URL is required");
    if (!apiKey) throw new Error("RAGFLOW_API_KEY is required");
    this.baseUrl = normalizeBaseUrl(baseUrl);
    this.apiKey = apiKey;
    this.apiPrefix = "/api/v1";
    this.timeout = options.timeout || DEFAULT_TIMEOUT;
    this.maxRetries = options.maxRetries !== undefined ? options.maxRetries : MAX_RETRIES;
  }

  async request(method, endpoint, options = {}) {
    const isMultipart = options.files && options.files.length > 0;

    const headers = {
      Authorization: `Bearer ${options.authToken || this.apiKey}`,
    };

    let body;
    if (isMultipart) {
      const boundary = "----FormBoundary" + Math.random().toString(36).slice(2);
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
        return await this._doRequest(method, endpoint, headers, body, options.timeout, options.apiPrefix);
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

  _doRequest(method, endpoint, headers, body, timeoutOverride, apiPrefix = this.apiPrefix) {
    const url = this._buildUrl(endpoint, apiPrefix);
    const timeout = timeoutOverride || this.timeout;

    return new Promise((resolve, reject) => {
      const mod = url.protocol === "https:" ? https : http;
      const req = mod.request(url, { method, headers }, (res) => {
        const chunks = [];
        res.on("data", (c) => chunks.push(c));
        res.on("end", () => {
          const raw = Buffer.concat(chunks).toString("utf-8");
          try {
            const data = JSON.parse(raw);
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
        `--${boundary}\r\nContent-Disposition: form-data; name="${key}"\r\n\r\n${value}`
      ));
      parts.push(Buffer.from("\r\n"));
    }
    for (const file of files) {
      const filePath = typeof file === "object" ? file.path : file;
      const basename = typeof file === "object" && file.name ? file.name : path.basename(filePath);
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
    if (typeof options === "number") {
      options = { timeout: options };
    }
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
    return this.request("GET", `/datasets/${datasetId}/documents/${documentId}`);
  }

  async downloadDocumentById(documentId) {
    return this.request("GET", `/documents/${documentId}`);
  }

  async previewDocument(documentId) {
    return this.request("GET", `/documents/${documentId}/preview`);
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
    const result = await this.listChunks(datasetId, documentId, { id: chunkId });
    const chunks = result?.chunks || (Array.isArray(result) ? result : []);
    const chunk = chunks.find((item) => item.id === chunkId) || chunks[0];
    if (!chunk) throw new Error(`Chunk not found: ${datasetId}/${chunkId}`);
    return chunk;
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
    return this.request(
      "PUT",
      `/datasets/${datasetId}/documents/${documentId}/chunks/${chunkId}`,
      { json: data }
    );
  }

  // ── Retrieval ──

  async retrieve(params) {
    return this.request("POST", "/retrieval", { json: params });
  }
  // ── Connector ──

  async listConnectors(datasetId, params = {}) {
    const query = this._buildQuery(params);
    return this.request("GET", `/datasets/${datasetId}/connectors?${query.toString()}`);
  }

  async createConnector(datasetId, data) {
    return this.request("POST", `/datasets/${datasetId}/connectors`, { json: data });
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
    return this.request("POST", `/datasets/${datasetId}/run_raptor`);
  }

  async traceRaptor(datasetId) {
    return this.request("GET", `/datasets/${datasetId}/trace_raptor`);
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

  async deleteSessions(chatId, ids) {
    return this.request("DELETE", `/chats/${chatId}/sessions`, { json: { ids } });
  }

  // ── Chat (Conversation) ──

  async chat(chatId, sessionId, question, params = {}) {
    return this._streamRequest(
      "POST", `/chat/completions`,
      { chat_id: chatId, question, session_id: sessionId, ...params }
    );
  }

  async chatSession(chatId, sessionId, data = {}) {
    const payload = { ...data, chat_id: chatId, session_id: sessionId };
    if (!payload.question && payload.messages) {
      const userMessages = Array.isArray(payload.messages)
        ? payload.messages.filter((message) => message && message.role === "user" && message.content)
        : [];
      const lastUserMessage = userMessages[userMessages.length - 1];
      if (lastUserMessage) payload.question = lastUserMessage.content;
    }
    // v0.26.0: preserve messages when pass_all_history_messages is set
    if (!payload.pass_all_history_messages && !payload.pass_all_history) {
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
    if (data.session_id) return data.session_id;
    const bootstrap = { ...data, question: "", stream: true };
    delete bootstrap.session_id;
    delete bootstrap.conversation_id;
    const result = await this._streamRequest("POST", `/chatbots/${chatId}/completions`, bootstrap, { authToken: beta });
    if (!result.session_id) {
      throw new Error("Embedded chat did not return a session_id during session bootstrap");
    }
    return result.session_id;
  }

  async embeddedChat(chatId, beta, data = {}) {
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
    return this.request("GET", `/llm/my_llms?${query.toString()}`, {
      apiPrefix: "/v1",
    });
  }

  // ── Tenant Models (v0.26.0) ──

  async listAddedModels(params = {}) {
    const query = this._buildQuery(params);
    const suffix = query.toString();
    return this.request("GET", `/models${suffix ? `?${suffix}` : ""}`);
  }

  async listDefaultModels() {
    return this.request("GET", "/models/default");
  }

  async setDefaultModel(data) {
    return this.request("PATCH", "/models/default", { json: data });
  }

  // ── Model Providers (v0.26.0) ──

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

function loadEnv() {
  const envPath = path.resolve(__dirname, "..", ".env");
  if (fs.existsSync(envPath)) {
    const content = fs.readFileSync(envPath, "utf-8");
    for (const line of content.split("\n")) {
      const trimmed = line.trim();
      if (!trimmed || trimmed.startsWith("#")) continue;
      const eq = trimmed.indexOf("=");
      if (eq > 0) {
        const key = trimmed.slice(0, eq);
        if (process.env[key] === undefined || process.env[key] === "") {
          process.env[key] = trimmed.slice(eq + 1);
        }
      }
    }
  }
}

function createClient(options = {}) {
  loadEnv();
  return new RagflowClient(
    process.env.RAGFLOW_URL,
    process.env.RAGFLOW_API_KEY,
    options
  );
}

module.exports = { RagflowClient, createClient };

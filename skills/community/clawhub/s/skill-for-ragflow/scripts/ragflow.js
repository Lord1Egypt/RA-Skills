#!/usr/bin/env node
const fs = require("fs");
const path = require("path");
const { createClient } = require("../lib/api.js");

const args = process.argv.slice(2);
const command = args[0];
const outputMode = { jsonOnly: false };

// ── Output helpers ──

const C = {
  reset: "\x1b[0m",
  bold: "\x1b[1m",
  dim: "\x1b[2m",
  red: "\x1b[31m",
  green: "\x1b[32m",
  yellow: "\x1b[33m",
  blue: "\x1b[34m",
  cyan: "\x1b[36m",
};

function ok(msg) {
  if (outputMode.jsonOnly) return;
  console.log(`${C.green}OK${C.reset} ${msg}`);
}

function warn(msg) {
  if (outputMode.jsonOnly) return;
  console.log(`${C.yellow}WARN${C.reset} ${msg}`);
}

function fail(msg) {
  console.error(`${C.red}ERROR${C.reset} ${msg}`);
}

function info(msg) {
  if (outputMode.jsonOnly) return;
  console.log(`${C.cyan}INFO${C.reset} ${msg}`);
}

function json(data) {
  console.log(JSON.stringify(data, null, 2));
}

function cliErrorMessage(err) {
  const message = err.message || String(err);
  if (err.code === "ECONNREFUSED") {
    return "Cannot connect to RAGFlow server. Check RAGFLOW_URL in .env";
  }
  if (err.code === "ECONNRESET") {
    return "Connection reset by RAGFlow server. The server may be restarting";
  }
  if (message.includes("timed out")) {
    return "Request timed out. The server may be slow or unreachable";
  }
  if (message.includes("RAGFLOW_URL is required") || message.includes("RAGFLOW_API_KEY is required")) {
    return `${message}. Configure .env file with RAGFLOW_URL and RAGFLOW_API_KEY`;
  }
  if (err.code) {
    return `API Error: ${message}`;
  }
  return message;
}

function uniqueList(value) {
  return [...new Set(listValue(value))];
}

function cloneDeleteChunkDetails(details) {
  return {
    attempt: details.attempt,
    next_attempt: details.attempt + 2,
    max_retries: details.max_retries,
    existing_chunk_ids: details.existing_chunk_ids || [],
    missing_chunk_ids: details.missing_chunk_ids || [],
  };
}

function deleteChunkJsonPayload(result, requestedChunkIds, retryDetails) {
  const latest = retryDetails[retryDetails.length - 1] || {};
  return {
    result,
    requested_chunk_ids: uniqueList(requestedChunkIds),
    existing_chunk_ids: latest.existing_chunk_ids || [],
    missing_chunk_ids: latest.missing_chunk_ids || [],
    visibility_checked: retryDetails.length > 0,
    retry_count: retryDetails.length,
    retries: retryDetails,
  };
}

function commandErrorJsonPayload(err) {
  const details = err.delete_chunk_details || {};
  const retries = err.delete_chunk_retries || [];
  const payload = {
    error: {
      message: cliErrorMessage(err),
      raw_message: err.message,
      code: err.code,
      status: err.status,
      command,
    },
  };
  if (err.delete_chunk_details) {
    payload.requested_chunk_ids = err.delete_chunk_requested_chunk_ids || [];
    payload.existing_chunk_ids = details.existing_chunk_ids || [];
    payload.missing_chunk_ids = details.missing_chunk_ids || [];
    payload.visibility_checked = Array.isArray(details.existing_chunk_ids) || Array.isArray(details.missing_chunk_ids);
    payload.retry_count = retries.length;
    payload.retries = retries;
    payload.delete_chunk_diagnostics = details;
  }
  return payload;
}

function requireOpt(opts, name) {
  if (!opts[name]) {
    throw new Error(`Missing required option: --${name.replace(/([A-Z])/g, "-$1").toLowerCase()}`);
  }
  return opts[name];
}

// ── Arg parser ──

function parseArgs(argv) {
  const opts = { _: [] };
  let i = 0;
  const aliases = {
    d: "datasets",
    h: "help",
    k: "topK",
    n: "topN",
    q: "question",
    r: "rerank",
    s: "similarity",
    w: "vectorWeight",
  };
  const multiKeys = new Set(["files", "ids", "docIds", "chunkIds", "datasets", "suffix", "types", "run", "tags", "instances"]);
  while (i < argv.length) {
    if (argv[i].startsWith("-") && argv[i] !== "-") {
      const isLong = argv[i].startsWith("--");
      const rawKey = isLong ? argv[i].replace(/^--/, "") : argv[i].replace(/^-/, "");
      const key = aliases[rawKey] || rawKey.replace(/-([a-z])/g, (_, c) => c.toUpperCase());
      if (multiKeys.has(key)) {
        const values = [];
        let j = i + 1;
        while (j < argv.length && !(argv[j].startsWith("-") && argv[j] !== "-")) {
          values.push(argv[j]);
          j++;
        }
        opts[key] = values;
        i = j;
      } else if (i + 1 < argv.length && !argv[i + 1].startsWith("--")) {
        opts[key] = argv[i + 1];
        i += 2;
      } else {
        opts[key] = true;
        i += 1;
      }
    } else {
      opts._.push(argv[i]);
      i += 1;
    }
  }
  return opts;
}

function listValue(value) {
  const values = Array.isArray(value) ? value : String(value).split(",");
  return values
    .flatMap((item) => String(item).split(","))
    .map((item) => item.trim())
    .filter(Boolean);
}

function jsonOption(value, optionName) {
  const source = String(value);
  const raw = source.startsWith("@")
    ? fs.readFileSync(path.resolve(process.cwd(), source.slice(1)), "utf-8")
    : source;
  try {
    return JSON.parse(raw);
  } catch (err) {
    throw new Error(`Invalid JSON for ${optionName}: ${err.message}`);
  }
}

function jsonStringOption(value, optionName) {
  return JSON.stringify(jsonOption(value, optionName));
}

function readStdinText() {
  return new Promise((resolve, reject) => {
    let data = "";
    process.stdin.setEncoding("utf8");
    process.stdin.on("data", (chunk) => {
      data += chunk;
    });
    process.stdin.on("end", () => resolve(data));
    process.stdin.on("error", reject);
  });
}

function uploadFileSpec(value) {
  const source = String(value);
  const eq = source.indexOf("=");
  if (eq > 0) {
    const name = source.slice(0, eq).trim();
    const filePath = source.slice(eq + 1).trim();
    if (!name || !filePath) {
      throw new Error(`Invalid --files entry "${source}". Use <display-name>=<path>`);
    }
    return { path: filePath, name };
  }
  return source;
}

function uploadFilesFromOptions(files) {
  return files.map(uploadFileSpec);
}

function questionFromMessages(messages) {
  if (!Array.isArray(messages)) {
    throw new Error("--messages must be a JSON array");
  }
  const userMessages = messages.filter((message) => message && message.role === "user" && message.content);
  const lastUserMessage = userMessages[userMessages.length - 1];
  return lastUserMessage ? String(lastUserMessage.content) : "";
}

function applyChatOptions(data, opts) {
  if (opts.datasets) data.dataset_ids = listValue(opts.datasets);
  if (opts.llm || opts.llmId) data.llm_id = opts.llmId || opts.llm;
  if (opts.promptConfig) data.prompt_config = jsonOption(opts.promptConfig, "--prompt-config");
  if (opts.prompt) data.prompt_config = { ...(data.prompt_config || {}), system: opts.prompt };
  if (opts.similarityThreshold) data.similarity_threshold = Number(opts.similarityThreshold);
  if (opts.topN) data.top_n = Number(opts.topN);
  if (opts.topK) data.top_k = Number(opts.topK);
  if (opts.vectorWeight) data.vector_similarity_weight = Number(opts.vectorWeight);
  if (opts.rerank) data.rerank_id = opts.rerank;
}

function boolOption(value, defaultValue = false) {
  if (value === undefined) return defaultValue;
  return value !== "false" && value !== false;
}

async function embedBeta(client, opts) {
  if (opts.beta || opts.auth) {
    return { beta: opts.beta || opts.auth, token: opts.token || "" };
  }
  const token = await client.ensureEmbedToken();
  if (!token || !token.beta) {
    throw new Error("No embed beta token available from /api/v1/system/tokens");
  }
  return token;
}

function normalizeOrigin(value) {
  let origin = (value || process.env.RAGFLOW_URL || "").trim().replace(/\/+$/, "");
  if (!origin) throw new Error("Missing origin. Set RAGFLOW_URL or pass --origin");
  if (!/^[a-z][a-z0-9+.-]*:\/\//i.test(origin)) {
    origin = `http://${origin}`;
  }
  return origin;
}

function appendEmbedQueryParams(src, opts, isAgent) {
  if (opts.published || opts.release) src.searchParams.append("release", "true");
  if (opts.hideAvatar || opts.visibleAvatar) src.searchParams.append("visible_avatar", "1");
  if (opts.locale) src.searchParams.append("locale", opts.locale);
  if (opts.userId) src.searchParams.append("userId", opts.userId);
  if (opts.data) {
    const data = jsonOption(opts.data, "--data");
    for (const [key, value] of Object.entries(data)) {
      src.searchParams.append(`data_${key}`, String(value));
    }
  }
  if (!isAgent && opts.userId) {
    warn("--user-id is only used by embedded agent pages");
  }
}

function buildEmbedCode(opts, tokenInfo) {
  const chatId = opts.chat;
  const agentId = opts.agent;
  if ((chatId && agentId) || (!chatId && !agentId)) {
    throw new Error("Provide exactly one of --chat or --agent");
  }
  const isAgent = Boolean(agentId);
  const type = opts.type || opts.embedType || "fullscreen";
  if (!["fullscreen", "widget"].includes(type)) {
    throw new Error("--type must be fullscreen or widget");
  }
  const origin = normalizeOrigin(opts.origin);
  const route = type === "widget" ? "/chats/widget" : isAgent ? "/agent/share" : "/chats/share";
  const src = new URL(route, origin);
  src.searchParams.append("shared_id", isAgent ? agentId : chatId);
  src.searchParams.append("from", isAgent ? "agent" : "chat");
  src.searchParams.append("auth", tokenInfo.beta);
  appendEmbedQueryParams(src, opts, isAgent);
  if (type === "widget") {
    src.searchParams.append("mode", "master");
    src.searchParams.append("streaming", String(boolOption(opts.streaming, false)));
  } else {
    src.searchParams.append("theme", opts.theme || "light");
  }

  const srcText = src.toString();
  const html = type === "widget"
    ? `<iframe
  src="${srcText}"
  style="position:fixed;bottom:0;right:0;width:100px;height:100px;border:none;background:transparent;z-index:9999"
  frameborder="0"
  allow="microphone;camera"
></iframe>
<script>
window.addEventListener('message',e=>{
  if(e.origin!=='${origin}')return;
  if(e.data.type==='CREATE_CHAT_WINDOW'){
    if(document.getElementById('chat-win'))return;
    const i=document.createElement('iframe');
    i.id='chat-win';i.src=e.data.src;
    i.style.cssText='position:fixed;bottom:104px;right:24px;width:380px;height:500px;border:none;background:transparent;z-index:9998;display:none';
    i.frameBorder='0';i.allow='microphone;camera';
    document.body.appendChild(i);
  }else if(e.data.type==='TOGGLE_CHAT'){
    const w=document.getElementById('chat-win');
    if(w)w.style.display=e.data.isOpen?'block':'none';
  }else if(e.data.type==='SCROLL_PASSTHROUGH')window.scrollBy(0,e.data.deltaY);
});
</script>`
    : `<iframe
  src="${srcText}"
  style="width: 100%; height: 100%; min-height: 600px"
  frameborder="0"
></iframe>`;

  return {
    type,
    from: isAgent ? "agent" : "chat",
    id: isAgent ? agentId : chatId,
    src: srcText,
    html,
    token: tokenInfo.token || "",
    beta: tokenInfo.beta,
  };
}

function applyEmbeddedChatPayloadOptions(data, opts) {
  if (opts.session) data.session_id = opts.session;
  if (opts.conversationId) data.conversation_id = opts.conversationId;
  if (opts.quote !== undefined) data.quote = boolOption(opts.quote);
  if (opts.stream !== undefined) data.stream = boolOption(opts.stream);
  if (opts.reasoning !== undefined) data.reasoning = boolOption(opts.reasoning);
  if (opts.internet !== undefined) data.internet = boolOption(opts.internet);
}

function applyEmbeddedAgentPayloadOptions(data, opts) {
  if (opts.session) data.session_id = opts.session;
  if (opts.inputs) data.inputs = jsonOption(opts.inputs, "--inputs");
  if (opts.userId) data.user_id = opts.userId;
  if (opts.published || opts.release) data.release = "true";
  if (opts.stream !== undefined) data.stream = boolOption(opts.stream);
}

const MAX_PAGE_SIZE = 100;
let pageSizeWarned = false;

// RAGFlow v0.26.0 hard-caps page_size at 100 on all list endpoints
// (validate_rest_api_page_size raises on larger values). Clamp client-side
// and warn once so oversized requests do not error out on the server.
function clampPageSize(value) {
  const n = Number(value);
  if (Number.isFinite(n) && n > MAX_PAGE_SIZE) {
    if (!pageSizeWarned) {
      warn(`page_size capped at ${MAX_PAGE_SIZE} (RAGFlow v0.26.0 server limit)`);
      pageSizeWarned = true;
    }
    return MAX_PAGE_SIZE;
  }
  return n;
}

function buildParams(opts, map) {
  const params = {};
  for (const [optKey, paramKey, transform] of map) {
    if (opts[optKey] !== undefined) {
      let value = transform ? transform(opts[optKey]) : opts[optKey];
      if (paramKey === "page_size") value = clampPageSize(value);
      params[paramKey] = value;
    }
  }
  return params;
}

// ── Dataset ──

async function createDataset(opts) {
  const client = createClient();
  const name = requireOpt(opts, "name");
  const data = { name };
  if (opts.chunkMethod) data.chunk_method = opts.chunkMethod;
  if (opts.embeddingModel) data.embedding_model = opts.embeddingModel;
  if (opts.permission) data.permission = opts.permission;
  if (opts.description) data.description = opts.description;
  info(`Creating dataset "${name}"...`);
  const result = await client.createDataset(data);
  ok(`Dataset created: ${result.id}`);
  json(result);
}

async function listDatasets(opts) {
  const client = createClient();
  const params = buildParams(opts, [
    ["page", "page", Number],
    ["pageSize", "page_size", Number],
    ["name", "name"],
    ["id", "id"],
  ]);
  const result = await client.listDatasets(params);
  if (Array.isArray(result) && result.length === 0) {
    warn("No datasets found");
    if (!outputMode.jsonOnly) return;
  } else {
    ok(`Found ${Array.isArray(result) ? result.length : "datasets"}`);
  }
  json(result);
}

async function getDataset(opts) {
  const client = createClient();
  const id = requireOpt(opts, "id");
  info(`Fetching dataset ${id}...`);
  const result = await client.getDataset(id);
  ok(`Dataset: ${result.name}`);
  json(result);
}

async function updateDataset(opts) {
  const client = createClient();
  const id = requireOpt(opts, "id");
  const data = {};
  if (opts.name) data.name = opts.name;
  if (opts.chunkMethod) data.chunk_method = opts.chunkMethod;
  if (opts.permission) data.permission = opts.permission;
  if (opts.description) data.description = opts.description;
  info(`Updating dataset ${id}...`);
  const result = await client.updateDataset(id, data);
  ok("Dataset updated");
  json(result);
}

async function deleteDatasets(opts) {
  const client = createClient();
  const ids = requireOpt(opts, "ids");
  info(`Deleting ${ids.length} dataset(s)...`);
  const result = await client.deleteDatasets(ids);
  ok("Datasets deleted");
  json(result);
}

// ── Document ──

async function uploadDocuments(opts) {
  const client = createClient();
  const dataset = requireOpt(opts, "dataset");
  const files = requireOpt(opts, "files");
  const uploadFiles = uploadFilesFromOptions(files);
  info(`Uploading ${files.length} file(s) to dataset ${dataset}...`);
  const result = await client.uploadDocuments(dataset, uploadFiles);
  ok(`Uploaded ${files.length} file(s)`);
  json(result);
}

async function listDocuments(opts) {
  const client = createClient();
  const dataset = requireOpt(opts, "dataset");
  const params = buildParams(opts, [
    ["page", "page", Number],
    ["pageSize", "page_size", Number],
    ["orderby", "orderby"],
    ["desc", "desc"],
    ["keywords", "keywords"],
    ["id", "id"],
    ["name", "name"],
    ["suffix", "suffix", listValue],
    ["types", "types", listValue],
    ["run", "run", listValue],
    ["createTimeFrom", "create_time_from", Number],
    ["createTimeTo", "create_time_to", Number],
  ]);
  if (opts.metadataCondition !== undefined) params.metadata_condition = jsonStringOption(opts.metadataCondition, "--metadata-condition");
  if (opts.metadata !== undefined) params.metadata = jsonStringOption(opts.metadata, "--metadata");
  if (opts.returnEmptyMetadata !== undefined) params.return_empty_metadata = opts.returnEmptyMetadata !== "false" && opts.returnEmptyMetadata !== false;
  const result = await client.listDocuments(dataset, params);
  if (Array.isArray(result) && result.length === 0) {
    warn("No documents found");
    if (!outputMode.jsonOnly) return;
  } else {
    ok(`Found ${Array.isArray(result) ? result.length : "documents"}`);
  }
  json(result);
}

async function deleteDocuments(opts) {
  const client = createClient();
  const dataset = requireOpt(opts, "dataset");
  const ids = requireOpt(opts, "ids");
  info(`Deleting ${ids.length} document(s)...`);
  const result = await client.deleteDocuments(dataset, ids);
  ok("Documents deleted");
  json(result);
}

async function getDocument(opts) {
  const client = createClient();
  const dataset = requireOpt(opts, "dataset");
  const id = requireOpt(opts, "id");
  info(`Fetching document ${id}...`);
  const result = await client.getDocument(dataset, id);
  ok(`Document: ${result.name}`);
  json(result);
}

async function updateDocument(opts) {
  const client = createClient();
  const dataset = requireOpt(opts, "dataset");
  const id = requireOpt(opts, "id");
  const data = {};
  if (opts.name) data.name = opts.name;
  if (opts.parserConfig) data.parser_config = jsonOption(opts.parserConfig, "--parser-config");
  if (opts.chunkMethod) data.chunk_method = opts.chunkMethod;
  if (opts.enabled !== undefined) data.enabled = Number(opts.enabled);
  if (opts.metaFields) data.meta_fields = jsonOption(opts.metaFields, "--meta-fields");
  info(`Updating document ${id} in dataset ${dataset}...`);
  const result = await client.updateDocument(dataset, id, data);
  ok("Document updated");
  json(result);
}

async function downloadDocument(opts) {
  const client = createClient();
  const dataset = requireOpt(opts, "dataset");
  const id = requireOpt(opts, "id");
  info(`Downloading document ${id}...`);
  const result = await client.downloadDocument(dataset, id);
  ok(`Document downloaded`);
  json(result);
}

async function previewDocument(opts) {
  const client = createClient();
  const id = requireOpt(opts, "id");
  info(`Previewing document ${id}...`);
  const result = await client.previewDocument(id);
  ok("Document preview fetched");
  json(result);
}

// ── Parsing ──

async function startParsing(opts) {
  const client = createClient();
  const dataset = requireOpt(opts, "dataset");
  const docIds = requireOpt(opts, "docIds");
  info(`Starting parsing for ${docIds.length} document(s)...`);
  const result = await client.startParsing(dataset, docIds);
  ok("Parsing started");
  json(result);
}

async function stopParsing(opts) {
  const client = createClient();
  const dataset = requireOpt(opts, "dataset");
  const docIds = requireOpt(opts, "docIds");
  info(`Stopping parsing for ${docIds.length} document(s)...`);
  const result = await client.stopParsing(dataset, docIds);
  ok("Parsing stopped");
  json(result);
}

async function waitParsing(opts) {
  const client = createClient();
  const dataset = requireOpt(opts, "dataset");
  const docIds = requireOpt(opts, "docIds");
  const maxWait = opts.timeout ? Number(opts.timeout) * 1000 : 120000;
  info(`Waiting for ${docIds.length} document(s) to finish parsing (timeout: ${maxWait / 1000}s)...`);
  const result = await client.waitForParsing(dataset, docIds, { maxWait });
  const failed = result.filter((d) => d.run === "FAIL");
  if (failed.length > 0) {
    warn(`${failed.length} document(s) failed parsing`);
  } else {
    ok("All documents parsed successfully");
  }
  json(result.map((d) => ({ id: d.id, name: d.name, run: d.run, chunk_count: d.chunk_count })));
}

// ── Chunk ──

async function listChunks(opts) {
  const client = createClient();
  const dataset = requireOpt(opts, "dataset");
  const document = requireOpt(opts, "document");
  const params = buildParams(opts, [
    ["page", "page", Number],
    ["pageSize", "page_size", Number],
    ["keywords", "keywords"],
    ["id", "id"],
  ]);
  const result = await client.listChunks(dataset, document, params);
  if (Array.isArray(result) && result.length === 0) {
    warn("No chunks found");
    if (!outputMode.jsonOnly) return;
  } else {
    ok(`Found ${Array.isArray(result) ? result.length : "chunks"}`);
  }
  json(result);
}

async function addChunk(opts) {
  const client = createClient();
  const dataset = requireOpt(opts, "dataset");
  const document = requireOpt(opts, "document");
  const content = requireOpt(opts, "content");
  const data = { content };
  if (opts.keywords) data.important_keywords = listValue(opts.keywords);
  info("Adding chunk...");
  const result = await client.addChunk(dataset, document, data);
  ok("Chunk added");
  json(result);
}

async function deleteChunks(opts) {
  const client = createClient();
  const dataset = requireOpt(opts, "dataset");
  const document = requireOpt(opts, "document");
  const chunkIds = requireOpt(opts, "chunkIds");
  info(`Deleting ${chunkIds.length} chunk(s)...`);
  const retries = [];
  let result;
  try {
    result = await client.deleteChunks(dataset, document, chunkIds, {
      onRetry(details) {
        const retry = cloneDeleteChunkDetails(details);
        retries.push(retry);
        warn(
          `delete-chunks returned 0 deletions, but exact ID lookup still found ${retry.existing_chunk_ids.length} chunk(s): ${retry.existing_chunk_ids.join(", ")}. Retrying (${retry.next_attempt}/${retry.max_retries + 1})...`
        );
      },
    });
  } catch (err) {
    if (err.delete_chunk_details) {
      err.delete_chunk_requested_chunk_ids = uniqueList(chunkIds);
      err.delete_chunk_retries = retries;
    }
    throw err;
  }
  ok("Chunks deleted");
  json(outputMode.jsonOnly ? deleteChunkJsonPayload(result, chunkIds, retries) : result);
}

async function updateChunk(opts) {
  const client = createClient();
  const dataset = requireOpt(opts, "dataset");
  const document = requireOpt(opts, "document");
  const chunk = requireOpt(opts, "chunk");
  const data = {};
  if (opts.content) data.content = opts.content;
  if (opts.keywords) data.important_keywords = listValue(opts.keywords);
  info(`Updating chunk ${chunk}...`);
  const result = await client.updateChunk(dataset, document, chunk, data);
  ok("Chunk updated");
  json(result);
}

// ── Retrieval ──

async function retrieve(opts) {
  const client = createClient();
  const question = opts.question;
  if (!question) {
    throw new Error("Missing required option: --question");
  }
  const params = { question };
  if (opts.datasets) {
    params.dataset_ids = listValue(opts.datasets);
  }
  if (opts.similarity) params.similarity_threshold = Number(opts.similarity);
  if (opts.topN) params.page_size = clampPageSize(opts.topN);
  if (opts.topK) params.top_k = Number(opts.topK);
  if (opts.vectorWeight) params.vector_similarity_weight = Number(opts.vectorWeight);
  if (opts.rerank) params.rerank_id = opts.rerank;
  if (opts.keyword) params.keyword = true;
  if (opts.kg) params.use_kg = true;
  if (opts.crossLangs) params.cross_languages = opts.crossLangs.split(",");

  info(`Searching: "${question}"`);
  const result = await client.retrieve(params);
  const count = Array.isArray(result) ? result.length : 0;
  ok(`Found ${count} result(s)`);
  json(result);
}

// ── Connector ──

async function listConnectors(opts) {
  const client = createClient();
  const dataset = requireOpt(opts, "dataset");
  const params = buildParams(opts, [
    ["page", "page", Number],
    ["pageSize", "page_size", Number],
  ]);
  info(`Fetching connectors for dataset ${dataset}...`);
  const result = await client.listConnectors(dataset, params);
  if (Array.isArray(result) && result.length === 0) {
    warn("No connectors found");
    if (!outputMode.jsonOnly) return;
  } else {
    ok(`Found ${Array.isArray(result) ? result.length : "connectors"}`);
  }
  json(result);
}

async function createConnector(opts) {
  const client = createClient();
  const dataset = requireOpt(opts, "dataset");
  const config = requireOpt(opts, "config");
  const data = jsonOption(config, "--config");
  info(`Creating connector for dataset ${dataset}...`);
  const result = await client.createConnector(dataset, data);
  ok(`Connector created: ${result.id}`);
  json(result);
}

async function getConnector(opts) {
  const client = createClient();
  const id = requireOpt(opts, "id");
  info(`Fetching connector ${id}...`);
  const result = await client.getConnector(id);
  ok(`Connector: ${result.name}`);
  json(result);
}

async function updateConnector(opts) {
  const client = createClient();
  const id = requireOpt(opts, "id");
  const config = opts.config;
  const data = {};
  if (config) {
    Object.assign(data, typeof config === "string" ? JSON.parse(fs.readFileSync(config, "utf8")) : config);
  }
  if (opts.name) data.name = opts.name;
  info(`Updating connector ${id}...`);
  const result = await client.updateConnector(id, data);
  ok("Connector updated");
  json(result);
}

async function deleteConnector(opts) {
  const client = createClient();
  const id = requireOpt(opts, "id");
  info(`Deleting connector ${id}...`);
  const result = await client.deleteConnector(id);
  ok("Connector deleted");
  json(result);
}

// ── Chat Assistant ──

async function listChatAssistants(opts) {
  const client = createClient();
  const params = buildParams(opts, [
    ["page", "page", Number],
    ["pageSize", "page_size", Number],
    ["name", "name"],
    ["id", "id"],
  ]);
  const result = await client.listChatAssistants(params);
  if (Array.isArray(result) && result.length === 0) {
    warn("No chat assistants found");
    if (!outputMode.jsonOnly) return;
  } else {
    ok(`Found ${Array.isArray(result) ? result.length : "assistants"}`);
  }
  json(result);
}

async function createChatAssistant(opts) {
  const client = createClient();
  const name = requireOpt(opts, "name");
  const data = { name };
  applyChatOptions(data, opts);
  info(`Creating chat assistant "${name}"...`);
  const result = await client.createChatAssistant(data);
  ok(`Chat assistant created: ${result.id}`);
  json(result);
}

async function updateChatAssistant(opts) {
  const client = createClient();
  const id = requireOpt(opts, "id");
  const data = {};
  if (opts.name) data.name = opts.name;
  applyChatOptions(data, opts);
  info(`Updating chat assistant ${id}...`);
  const result = await client.updateChatAssistant(id, data);
  ok("Chat assistant updated");
  json(result);
}

async function patchChatAssistant(opts) {
  const client = createClient();
  const id = requireOpt(opts, "id");
  const data = {};
  if (opts.name) data.name = opts.name;
  applyChatOptions(data, opts);
  info(`Patching chat assistant ${id}...`);
  const result = await client.patchChatAssistant(id, data);
  ok("Chat assistant patched");
  json(result);
}

async function deleteChatAssistants(opts) {
  const client = createClient();
  const ids = requireOpt(opts, "ids");
  info(`Deleting ${ids.length} chat assistant(s)...`);
  const result = await client.deleteChatAssistants(ids);
  ok("Chat assistants deleted");
  json(result);
}

async function getChatAssistant(opts) {
  const client = createClient();
  const id = requireOpt(opts, "id");
  info(`Fetching chat assistant ${id}...`);
  const result = await client.getChatAssistant(id);
  ok(`Chat assistant: ${result.name}`);
  json(result);
}

// ── Session ──

async function listSessions(opts) {
  const client = createClient();
  const chat = requireOpt(opts, "chat");
  const params = buildParams(opts, [
    ["page", "page", Number],
    ["pageSize", "page_size", Number],
  ]);
  const result = await client.listSessions(chat, params);
  ok(`Found ${Array.isArray(result) ? result.length : "sessions"}`);
  json(result);
}

async function createSession(opts) {
  const client = createClient();
  const chat = requireOpt(opts, "chat");
  const data = {};
  if (opts.name) data.name = opts.name;
  info("Creating session...");
  const result = await client.createSession(chat, data);
  ok(`Session created: ${result.id}`);
  json(result);
}

async function deleteSessions(opts) {
  const client = createClient();
  const chat = requireOpt(opts, "chat");
  const ids = requireOpt(opts, "ids");
  info(`Deleting ${ids.length} session(s)...`);
  const result = await client.deleteSessions(chat, ids);
  ok("Sessions deleted");
  json(result);
}

// ── Chat ──

async function chat(opts) {
  const client = createClient();
  const chatId = requireOpt(opts, "chat");
  const session = requireOpt(opts, "session");
  const question = opts.question;
  if (!question) {
    throw new Error("Missing required option: --question");
  }
  const params = {};
  if (opts.stream) params.stream = true;
  if (opts.topN) params.top_n = Number(opts.topN);

  info(`Asking: "${question}"`);
  const result = await client.chat(chatId, session, question, params);
  ok("Response received");
  json(result);
}

async function chatSession(opts) {
  const client = createClient();
  const chatId = requireOpt(opts, "chat");
  const session = requireOpt(opts, "session");
  const data = {};
  if (opts.messages) {
    const messages = jsonOption(opts.messages, "--messages");
    data.question = questionFromMessages(messages);
  }
  if (opts.question) data.question = opts.question;
  if (!data.question) {
    throw new Error("Missing required option: --question or --messages with a user message");
  }
  if (opts.llmId || opts.llm) data.llm_id = opts.llmId || opts.llm;
  if (opts.temperature !== undefined) data.temperature = Number(opts.temperature);
  if (opts.topP !== undefined) data.top_p = Number(opts.topP);
  if (opts.frequencyPenalty !== undefined) data.frequency_penalty = Number(opts.frequencyPenalty);
  if (opts.presencePenalty !== undefined) data.presence_penalty = Number(opts.presencePenalty);
  if (opts.maxTokens !== undefined) data.max_tokens = Number(opts.maxTokens);
  if (opts.stream !== undefined) data.stream = opts.stream !== "false" && opts.stream !== false;
  if (opts.passAllHistory) data.pass_all_history_messages = true;
  if (opts.messages) data.messages = jsonOption(opts.messages, "--messages");
  info(`Asking session: ${session}...`);
  const result = await client.chatSession(chatId, session, data);
  ok("Session response received");
  json(result);
}

// ── Agent ──

async function listAgents(opts) {
  const client = createClient();
  const params = buildParams(opts, [
    ["page", "page", Number],
    ["pageSize", "page_size", Number],
    ["name", "title"],
    ["title", "title"],
    ["id", "id"],
    ["tags", "tags"],
  ]);
  const result = await client.listAgents(params);
  if (Array.isArray(result) && result.length === 0) {
    warn("No agents found");
    if (!outputMode.jsonOnly) return;
  } else {
    ok(`Found ${Array.isArray(result) ? result.length : "agents"}`);
  }
  json(result);
}

async function listAgentTags(opts) {
  const client = createClient();
  info("Fetching agent tags...");
  const result = await client.listAgentTags();
  if (Array.isArray(result) && result.length === 0) {
    warn("No agent tags found");
    if (!outputMode.jsonOnly) return;
  } else {
    ok(`Found ${Array.isArray(result) ? result.length : "tags"}`);
  }
  json(result);
}

async function updateAgentTags(opts) {
  const client = createClient();
  const id = requireOpt(opts, "id");
  const tags = requireOpt(opts, "tags");
  const tagStr = Array.isArray(tags) ? tags.join(",") : tags;
  info(`Updating tags for agent ${id}...`);
  const result = await client.updateAgentTags(id, tagStr);
  ok("Agent tags updated");
  json(result);
}

async function createAgent(opts) {
  const client = createClient();
  const title = requireOpt(opts, "title");
  const dsl = requireOpt(opts, "dsl");
  const data = { title, dsl: jsonOption(dsl, "--dsl") };
  if (opts.description) data.description = opts.description;
  if (opts.canvasType) data.canvas_type = opts.canvasType;
  info(`Creating agent "${title}"...`);
  const result = await client.createAgent(data);
  ok(`Agent created`);
  json(result);
}

async function updateAgent(opts) {
  const client = createClient();
  const id = requireOpt(opts, "id");
  const data = {};
  if (opts.title) data.title = opts.title;
  if (opts.dsl) data.dsl = jsonOption(opts.dsl, "--dsl");
  if (opts.description) data.description = opts.description;
  if (opts.canvasType) data.canvas_type = opts.canvasType;
  info(`Updating agent ${id}...`);
  const result = await client.updateAgent(id, data);
  ok("Agent updated");
  json(result);
}

async function deleteAgents(opts) {
  const client = createClient();
  const ids = requireOpt(opts, "ids");
  info(`Deleting ${ids.length} agent(s)...`);
  const result = await client.deleteAgents(ids);
  ok("Agents deleted");
  json(result);
}

async function getAgent(opts) {
  const client = createClient();
  const id = requireOpt(opts, "id");
  info(`Fetching agent ${id}...`);
  const result = await client.getAgent(id);
  ok(`Agent: ${result.title || result.id}`);
  json(result);
}

// ── Agent Session ──

async function listAgentSessions(opts) {
  const client = createClient();
  const agent = requireOpt(opts, "agent");
  const params = buildParams(opts, [
    ["page", "page", Number],
    ["pageSize", "page_size", Number],
  ]);
  const result = await client.listAgentSessions(agent, params);
  ok(`Found ${Array.isArray(result) ? result.length : "sessions"}`);
  json(result);
}

async function createAgentSession(opts) {
  const client = createClient();
  const agent = requireOpt(opts, "agent");
  const data = {};
  if (opts.name) data.name = opts.name;
  info("Creating agent session...");
  const result = await client.createAgentSession(agent, data);
  ok(`Agent session created: ${result.id}`);
  json(result);
}

async function deleteAgentSessions(opts) {
  const client = createClient();
  const agent = requireOpt(opts, "agent");
  const ids = requireOpt(opts, "ids");
  info(`Deleting ${ids.length} agent session(s)...`);
  const result = await client.deleteAgentSessions(agent, ids);
  ok("Agent sessions deleted");
  json(result);
}

// ── Agent Chat ──

async function agentChat(opts) {
  const client = createClient();
  const agentId = requireOpt(opts, "agent");
  const session = requireOpt(opts, "session");
  const question = opts.question;
  if (!question) {
    throw new Error("Missing required option: --question");
  }
  const params = {};
  if (opts.stream !== undefined) params.stream = opts.stream !== "false" && opts.stream !== false;
  if (opts.chatTemplateKwargs) params.chat_template_kwargs = jsonOption(opts.chatTemplateKwargs, "--chat-template-kwargs");
  info(`Asking agent: "${question}"`);
  const result = await client.agentChat(agentId, session, question, params);
  ok("Agent response received");
  json(result);
}

// ── Embedded website access ──

async function listSystemTokens() {
  const client = createClient();
  info("Fetching system tokens...");
  const result = await client.listSystemTokens();
  ok(`Found ${Array.isArray(result) ? result.length : "tokens"}`);
  json(result);
}

async function createSystemToken() {
  const client = createClient();
  info("Creating system token...");
  const result = await client.createSystemToken();
  ok("System token created");
  json(result);
}

async function deleteSystemToken(opts) {
  const client = createClient();
  let token = "";
  if (opts.token !== undefined) {
    throw new Error("delete-system-token no longer accepts --token. Use --token-file or --token-stdin.");
  }
  if (opts.tokenFile) {
    token = fs.readFileSync(path.resolve(process.cwd(), opts.tokenFile), "utf-8").trim();
  } else if (opts.tokenStdin) {
    if (process.stdin.isTTY) {
      throw new Error("--token-stdin requires piped input");
    }
    token = (await readStdinText()).trim();
  } else {
    throw new Error("Provide --token-file or --token-stdin");
  }
  if (!token) {
    throw new Error("Token input was empty");
  }
  info("Deleting system token...");
  const result = await client.deleteSystemToken(token);
  ok("System token deleted");
  json(result);
}

async function embedCode(opts) {
  const client = createClient();
  const tokenInfo = await embedBeta(client, opts);
  const result = buildEmbedCode(opts, tokenInfo);
  ok(`Embed code generated for ${result.from} ${result.id}`);
  json(result);
}

async function embedInfo(opts) {
  const client = createClient();
  const tokenInfo = await embedBeta(client, opts);
  let result;
  if (opts.chat && !opts.agent) {
    info(`Fetching embedded chat info for ${opts.chat}...`);
    result = await client.getEmbeddedChatInfo(opts.chat, tokenInfo.beta);
  } else if (opts.agent && !opts.chat) {
    info(`Fetching embedded agent inputs for ${opts.agent}...`);
    result = await client.getEmbeddedAgentInputs(opts.agent, tokenInfo.beta);
  } else {
    throw new Error("Provide exactly one of --chat or --agent");
  }
  ok("Embedded info fetched");
  json(result);
}

async function embedChat(opts) {
  const client = createClient();
  const chatId = requireOpt(opts, "chat");
  const question = requireOpt(opts, "question");
  const tokenInfo = await embedBeta(client, opts);
  const data = { question };
  applyEmbeddedChatPayloadOptions(data, opts);
  if (!data.session_id) {
    info("Creating embedded chat session...");
    data.session_id = await client.ensureEmbeddedChatSession(chatId, tokenInfo.beta, data);
  }
  info(`Asking embedded chat: "${question}"`);
  const result = await client.embeddedChat(chatId, tokenInfo.beta, data);
  ok("Embedded chat response received");
  json(result);
}

async function embedAgentChat(opts) {
  const client = createClient();
  const agentId = requireOpt(opts, "agent");
  const question = requireOpt(opts, "question");
  const tokenInfo = await embedBeta(client, opts);
  const data = { id: agentId, query: question };
  applyEmbeddedAgentPayloadOptions(data, opts);
  info(`Asking embedded agent: "${question}"`);
  const result = await client.embeddedAgentChat(agentId, tokenInfo.beta, data);
  ok("Embedded agent response received");
  json(result);
}

// ── LLM Models ──

async function listModels(opts) {
  const client = createClient();
  const params = {};
  if (opts.includeDetails) params.include_details = true;
  info("Fetching available LLM models...");
  let result;
  try {
    result = await client.listModels(params);
  } catch (err) {
    if (err.status === 401 || err.code === 401 || /unauthor/i.test(err.message)) {
      err.message = `${err.message}. Verify RAGFLOW_API_KEY is valid for /v1/llm/my_llms.`;
    }
    throw err;
  }

  // Normalize and group models
  const factories = result || {};
  const groups = [];
  const groupBy = opts.groupBy || "type";
  const includeUnavailable = opts.all;
  
  for (const [factoryName, factoryPayload] of Object.entries(factories)) {
    if (factoryName.startsWith("__")) continue;
    if (!factoryPayload || !factoryPayload.llm) continue;
    const llms = factoryPayload.llm || [];
    for (const llm of llms) {
      const status = llm.status;
      const isAvailable = status === 1 || status === "1" || status === true;
      if (!includeUnavailable && !isAvailable) continue;
      
      const key = groupBy === "factory" ? factoryName : (llm.type || "unknown");
      let group = groups.find(g => g.name === key);
      if (!group) {
        group = { name: key, models: [] };
        groups.push(group);
      }
      
      const model = {
        id: llm.id,
        name: llm.name,
        type: llm.type,
        factory: factoryName,
        status: isAvailable ? "available" : "unavailable",
      };
      if (opts.includeDetails) {
        model.used_token = llm.used_token;
        if (llm.api_base) model.api_base = llm.api_base;
        if (llm.max_tokens) model.max_tokens = llm.max_tokens;
      }
      group.models.push(model);
    }
  }
  
  groups.sort((a, b) => a.name.localeCompare(b.name));
  for (const group of groups) {
    group.models.sort((a, b) => (a.name || "").localeCompare(b.name || ""));
  }
  
  const totalModels = groups.reduce((sum, g) => sum + g.models.length, 0);
  ok(`Found ${totalModels} model(s) in ${groups.length} group(s)`);
  json({ groups, total: totalModels });
}

// ── Tenant Models (v0.26.0) ──

async function listAddedModels(opts) {
  const client = createClient();
  const params = {};
  if (opts.type) params.type = opts.type;
  info("Fetching added models...");
  const result = await client.listAddedModels(params);
  ok("Added models fetched");
  json(result);
}

async function listDefaultModels() {
  const client = createClient();
  info("Fetching default models...");
  const result = await client.listDefaultModels();
  ok("Default models fetched");
  json(result);
}

async function setDefaultModel(opts) {
  const client = createClient();
  const modelType = requireOpt(opts, "modelType");
  const data = { model_type: modelType };
  if (opts.modelProvider) data.model_provider = opts.modelProvider;
  if (opts.modelInstance) data.model_instance = opts.modelInstance;
  if (opts.modelName) data.model_name = opts.modelName;
  info(`Setting default ${modelType} model...`);
  const result = await client.setDefaultModel(data);
  ok("Default model updated");
  json(result);
}

// ── Model Providers (v0.26.0) ──

async function listProviders(opts) {
  const client = createClient();
  const params = {};
  if (opts.available) params.available = "true";
  info(opts.available ? "Fetching available providers..." : "Fetching configured providers...");
  const result = await client.listProviders(params);
  ok("Providers fetched");
  json(result);
}

async function getProvider(opts) {
  const client = createClient();
  const name = requireOpt(opts, "name");
  info(`Fetching provider ${name}...`);
  const result = await client.getProvider(name);
  ok("Provider fetched");
  json(result);
}

async function addProvider(opts) {
  const client = createClient();
  const name = requireOpt(opts, "name");
  info(`Adding provider ${name}...`);
  const result = await client.addProvider(name);
  ok(`Provider added: ${name}`);
  json(result);
}

async function deleteProvider(opts) {
  const client = createClient();
  const name = requireOpt(opts, "name");
  info(`Removing provider ${name}...`);
  const result = await client.deleteProvider(name);
  ok(`Provider removed: ${name}`);
  json(result);
}

async function listProviderModels(opts) {
  const client = createClient();
  const name = requireOpt(opts, "name");
  const params = {};
  if (opts.apiKey) params.api_key = opts.apiKey;
  if (opts.baseUrl) params.base_url = opts.baseUrl;
  info(`Fetching available models for provider ${name}...`);
  const result = await client.listProviderModels(name, params);
  ok("Provider models fetched");
  json(result);
}

async function listProviderInstances(opts) {
  const client = createClient();
  const name = requireOpt(opts, "name");
  info(`Fetching instances for provider ${name}...`);
  const result = await client.listProviderInstances(name);
  ok("Provider instances fetched");
  json(result);
}

async function getProviderInstance(opts) {
  const client = createClient();
  const name = requireOpt(opts, "name");
  const instance = requireOpt(opts, "instance");
  info(`Fetching instance ${instance} for provider ${name}...`);
  const result = await client.getProviderInstance(name, instance);
  ok("Provider instance fetched");
  json(result);
}

async function createProviderInstance(opts) {
  const client = createClient();
  const name = requireOpt(opts, "name");
  const data = {
    instance_name: requireOpt(opts, "instance"),
    api_key: requireOpt(opts, "apiKey"),
  };
  if (opts.baseUrl) data.base_url = opts.baseUrl;
  if (opts.region) data.region = opts.region;
  if (opts.modelInfo) data.model_info = jsonOption(opts.modelInfo, "--model-info");
  info(`Creating instance ${data.instance_name} for provider ${name}...`);
  const result = await client.createProviderInstance(name, data);
  ok(`Provider instance created: ${data.instance_name}`);
  json(result);
}

async function deleteProviderInstances(opts) {
  const client = createClient();
  const name = requireOpt(opts, "name");
  const instances = uniqueList(requireOpt(opts, "instances"));
  info(`Removing ${instances.length} instance(s) from provider ${name}...`);
  const result = await client.deleteProviderInstances(name, instances);
  ok("Provider instances removed");
  json(result);
}

async function verifyProvider(opts) {
  const client = createClient();
  const name = requireOpt(opts, "name");
  const data = { api_key: requireOpt(opts, "apiKey") };
  if (opts.baseUrl) data.base_url = opts.baseUrl;
  if (opts.region) data.region = opts.region;
  if (opts.modelInfo) data.model_info = jsonOption(opts.modelInfo, "--model-info");
  info(`Testing connection to provider ${name}...`);
  const result = await client.verifyProvider(name, data);
  ok("Provider connection verified");
  json(result);
}

async function listInstanceModels(opts) {
  const client = createClient();
  const name = requireOpt(opts, "name");
  const instance = requireOpt(opts, "instance");
  const params = {};
  if (opts.supported) params.supported = "true";
  info(`Fetching models for ${name}/${instance}...`);
  const result = await client.listInstanceModels(name, instance, params);
  ok("Instance models fetched");
  json(result);
}

async function addInstanceModel(opts) {
  const client = createClient();
  const name = requireOpt(opts, "name");
  const instance = requireOpt(opts, "instance");
  const data = {
    model_name: requireOpt(opts, "modelName"),
    model_type: requireOpt(opts, "modelType"),
  };
  if (opts.maxTokens) data.max_tokens = Number(opts.maxTokens);
  if (opts.extra) data.extra = jsonOption(opts.extra, "--extra");
  info(`Adding model ${data.model_name} to ${name}/${instance}...`);
  const result = await client.addInstanceModel(name, instance, data);
  ok(`Model added: ${data.model_name}`);
  json(result);
}

async function setModelStatus(opts) {
  const client = createClient();
  const name = requireOpt(opts, "name");
  const instance = requireOpt(opts, "instance");
  const modelName = requireOpt(opts, "modelName");
  const status = requireOpt(opts, "status");
  info(`Setting status of ${modelName} to ${status}...`);
  const result = await client.setInstanceModelStatus(name, instance, modelName, status);
  ok("Model status updated");
  json(result);
}

// ── RAPTOR ──

async function runRaptor(opts) {
  const client = createClient();
  const dataset = requireOpt(opts, "dataset");
  info(`Starting RAPTOR processing for dataset ${dataset}...`);
  const result = await client.runRaptor(dataset);
  ok(`RAPTOR started: ${result.task_id || "task"}`);
  json(result);
}

async function traceRaptor(opts) {
  const client = createClient();
  const dataset = requireOpt(opts, "dataset");
  info(`Tracing RAPTOR progress for dataset ${dataset}...`);
  const result = await client.traceRaptor(dataset);
  ok(`RAPTOR status: ${result.status || "unknown"}`);
  json(result);
}

// ── Command registry ──

async function metadataSummary(opts) {
  const client = createClient();
  const dataset = requireOpt(opts, "dataset");
  const docIds = opts.docIds ? listValue(opts.docIds) : [];
  info(`Fetching metadata summary for dataset ${dataset}...`);
  const result = await client.metadataSummary(dataset, docIds);
  ok("Metadata summary fetched");
  json(result);
}

async function systemVersion() {
  const client = createClient();
  const result = await client.getSystemVersion();
  ok("System version fetched");
  json(result);
}

async function getLogLevels() {
  const client = createClient();
  const result = await client.getLogLevels();
  ok("Log levels fetched");
  json(result);
}

async function setLogLevel(opts) {
  const client = createClient();
  const pkgName = requireOpt(opts, "pkgName");
  const level = requireOpt(opts, "level");
  info(`Setting log level for ${pkgName}...`);
  const result = await client.setLogLevel(pkgName, level);
  ok("Log level updated");
  json(result);
}

const COMMANDS = {
  // Dataset
  "create-dataset":    { fn: createDataset,    group: "Dataset",   desc: "Create a dataset" },
  "list-datasets":     { fn: listDatasets,     group: "Dataset",   desc: "List all datasets" },
  "get-dataset":       { fn: getDataset,       group: "Dataset",   desc: "Get dataset details" },
  "update-dataset":    { fn: updateDataset,    group: "Dataset",   desc: "Update a dataset" },
  "delete-datasets":   { fn: deleteDatasets,   group: "Dataset",   desc: "Delete datasets" },
  // Document
  "upload-documents":  { fn: uploadDocuments,  group: "Document",  desc: "Upload documents" },
  "list-documents":    { fn: listDocuments,    group: "Document",  desc: "List documents" },
  "get-document":      { fn: getDocument,      group: "Document",  desc: "Get document details" },
  "update-document":   { fn: updateDocument,   group: "Document",  desc: "Update a document" },
  "delete-documents":  { fn: deleteDocuments,  group: "Document",  desc: "Delete documents" },
  "download-document": { fn: downloadDocument, group: "Document", desc: "Download a document" },
  "preview-document":  { fn: previewDocument,  group: "Document", desc: "Preview a document inline by ID" },
  // Parsing
  "start-parsing":     { fn: startParsing,     group: "Parsing",   desc: "Start document parsing" },
  "stop-parsing":      { fn: stopParsing,      group: "Parsing",   desc: "Stop document parsing" },
  "wait-parsing":      { fn: waitParsing,      group: "Parsing",   desc: "Wait for parsing to complete" },
  // Chunk
  "list-chunks":       { fn: listChunks,       group: "Chunk",     desc: "List chunks" },
  "add-chunk":         { fn: addChunk,         group: "Chunk",     desc: "Add a chunk" },
  "update-chunk":      { fn: updateChunk,      group: "Chunk",     desc: "Update a chunk" },
  "delete-chunks":     { fn: deleteChunks,     group: "Chunk",     desc: "Delete chunks" },
  // Retrieval
  "retrieve":          { fn: retrieve,         group: "Retrieval", desc: "Retrieve from datasets" },
  // Connector
  "list-connectors":   { fn: listConnectors,   group: "Connector", desc: "List connectors" },
  "create-connector":  { fn: createConnector,  group: "Connector", desc: "Create a connector" },
  "get-connector":     { fn: getConnector,     group: "Connector", desc: "Get connector details" },
  "update-connector":  { fn: updateConnector,  group: "Connector", desc: "Update a connector" },
  "delete-connector":  { fn: deleteConnector,  group: "Connector", desc: "Delete a connector" },
  // RAPTOR
  "run-raptor":        { fn: runRaptor,        group: "RAPTOR",     desc: "Start RAPTOR processing" },
  "trace-raptor":      { fn: traceRaptor,      group: "RAPTOR",     desc: "Trace RAPTOR progress" },
  // Chat Assistant
  "list-chats":        { fn: listChatAssistants, group: "Chat",    desc: "List chat assistants" },
  "create-chat":       { fn: createChatAssistant, group: "Chat",   desc: "Create a chat assistant" },
  "get-chat":          { fn: getChatAssistant,  group: "Chat",      desc: "Get chat assistant details" },
  "update-chat":       { fn: updateChatAssistant, group: "Chat",   desc: "Update a chat assistant" },
  "patch-chat":        { fn: patchChatAssistant, group: "Chat",    desc: "Patch a chat assistant" },
  "delete-chats":      { fn: deleteChatAssistants, group: "Chat",  desc: "Delete chat assistants" },
  // Session
  "list-sessions":     { fn: listSessions,     group: "Session",   desc: "List chat sessions" },
  "create-session":    { fn: createSession,    group: "Session",   desc: "Create a chat session" },
  "delete-sessions":   { fn: deleteSessions,   group: "Session",   desc: "Delete chat sessions" },
  // Chat conversation
  "chat":              { fn: chat,             group: "Chat",      desc: "Chat with an assistant" },
  "chat-session":      { fn: chatSession,      group: "Chat",      desc: "Chat with a session" },
  // Agent
  "list-agents":       { fn: listAgents,        group: "Agent",     desc: "List agents", args: [], opts: ["page", "pageSize", "id", "name", "tags", "json"] },
  "create-agent":      { fn: createAgent,       group: "Agent",     desc: "Create an agent" },
  "get-agent":         { fn: getAgent,          group: "Agent",     desc: "Get agent details" },
  "update-agent":      { fn: updateAgent,       group: "Agent",     desc: "Update an agent" },
  "delete-agents":      { fn: deleteAgents,       group: "Agent",     desc: "Delete agents" },
  "list-agent-sessions":  { fn: listAgentSessions,  group: "Agent", desc: "List agent sessions" },
  "create-agent-session": { fn: createAgentSession, group: "Agent", desc: "Create an agent session" },
  "delete-agent-sessions": { fn: deleteAgentSessions, group: "Agent", desc: "Delete agent sessions" },
  "list-agent-tags":   { fn: listAgentTags,     group: "Agent",     desc: "List agent tags" },
  "update-agent-tags": { fn: updateAgentTags,   group: "Agent",     desc: "Update agent tags" },
  // Agent Chat
  "agent-chat":        { fn: agentChat,        group: "Agent",     desc: "Chat with an agent" },
  // Embedded website access
  "list-system-tokens": { fn: listSystemTokens, group: "Embed",     desc: "List system/embed tokens" },
  "create-system-token": { fn: createSystemToken, group: "Embed",   desc: "Create a system/embed token" },
  "delete-system-token": { fn: deleteSystemToken, group: "Embed",   desc: "Delete a system/embed token" },
  "embed-code":        { fn: embedCode,        group: "Embed",     desc: "Generate iframe/widget embed code" },
  "embed-info":        { fn: embedInfo,        group: "Embed",     desc: "Get embedded chat or agent metadata" },
  "embed-chat":        { fn: embedChat,        group: "Embed",     desc: "Chat through embedded chatbot route" },
  "embed-agent-chat":  { fn: embedAgentChat,   group: "Embed",     desc: "Chat through embedded agentbot route" },
  // LLM Models
  "list-models":       { fn: listModels,       group: "Models",    desc: "List available LLM models" },
  "list-added-models": { fn: listAddedModels,  group: "Models",    desc: "List tenant added models" },
  "list-default-models": { fn: listDefaultModels, group: "Models", desc: "List tenant default models" },
  "set-default-model": { fn: setDefaultModel,   group: "Models",    desc: "Set or clear a default model" },
  // Model Providers
  "list-providers":    { fn: listProviders,    group: "Provider",  desc: "List configured or available providers" },
  "get-provider":      { fn: getProvider,      group: "Provider",  desc: "Get provider details" },
  "add-provider":      { fn: addProvider,      group: "Provider",  desc: "Add a provider for the tenant" },
  "delete-provider":   { fn: deleteProvider,   group: "Provider",  desc: "Remove a provider" },
  "list-provider-models": { fn: listProviderModels, group: "Provider", desc: "List a provider's available models" },
  "list-provider-instances": { fn: listProviderInstances, group: "Provider", desc: "List provider instances" },
  "get-provider-instance": { fn: getProviderInstance, group: "Provider", desc: "Get a provider instance" },
  "create-provider-instance": { fn: createProviderInstance, group: "Provider", desc: "Create a provider instance (API key)" },
  "delete-provider-instances": { fn: deleteProviderInstances, group: "Provider", desc: "Remove provider instances" },
  "verify-provider":   { fn: verifyProvider,   group: "Provider",  desc: "Test a provider connection / API key" },
  "list-instance-models": { fn: listInstanceModels, group: "Provider", desc: "List models on a provider instance" },
  "add-instance-model": { fn: addInstanceModel, group: "Provider", desc: "Add a model to a provider instance" },
  "set-model-status":  { fn: setModelStatus,   group: "Provider",  desc: "Enable or disable an instance model" },
  // Metadata / System
  "metadata-summary":  { fn: metadataSummary,  group: "Document",  desc: "Summarize document metadata" },
  "system-version":    { fn: systemVersion,    group: "System",    desc: "Get system version" },
  "get-log-levels":    { fn: getLogLevels,     group: "System",    desc: "Get log levels" },
  "set-log-level":     { fn: setLogLevel,      group: "System",    desc: "Set a log level" },
};

function printHelp() {
  const groups = {};
  for (const [cmd, { group, desc }] of Object.entries(COMMANDS)) {
    if (!groups[group]) groups[group] = [];
    groups[group].push({ cmd, desc });
  }

  let out = `${C.bold}Usage:${C.reset} node ragflow.js <command> [options]\n`;
  for (const [group, cmds] of Object.entries(groups)) {
    out += `\n${C.bold}${C.cyan}  ${group}${C.reset}\n`;
    for (const { cmd, desc } of cmds) {
      out += `    ${C.green}${cmd.padEnd(22)}${C.reset} ${desc}\n`;
    }
  }
  out += `
${C.bold}Common Options:${C.reset}
    --name              Name
    --id                ID
    --ids               IDs (multiple values)
    --dataset           Dataset ID
    --files             File paths, or display-name=path entries
    --doc-ids           Document IDs (multiple values)
    --document          Document ID
    --content           Chunk content
    --chunk-ids         Chunk IDs (multiple values)
    --messages          Messages JSON (for session chat)
    --chat              Chat assistant ID
    --agent             Agent ID
    --session           Session ID
    --token-file        Read token from a file
    --token-stdin       Read token from stdin
    --beta, --auth      Embed auth beta token
    --origin            Public RAGFlow origin for embed code
    --type              Embed type: fullscreen or widget
    --theme             Embed theme: light or dark
    --locale            Embed locale
    --published         Use published agent release
    --streaming         Enable widget streaming
    --user-id           Embedded agent runtime user ID
    --hide-avatar       Hide avatar in embedded page
    --data              Embed URL data JSON
    --inputs            Embedded agent begin inputs JSON
    --conversation-id   Embedded chat conversation ID
    --llm-id            LLM model ID
    --question, -q      Question (for retrieve/chat)
    --datasets, -d      Dataset IDs for retrieval
    --metadata          Metadata filter JSON
    --metadata-condition Metadata condition JSON
    --meta-fields       Document metadata JSON
    --similarity, -s    Similarity threshold (0-1)
    --top-n, -n         Number of results
    --top-k, -k         Number of candidates
    --top-p             Top-p
    --vector-weight, -w Vector similarity weight (0-1)
    --temperature       Sampling temperature
    --frequency-penalty Frequency penalty
    --presence-penalty  Presence penalty
    --max-tokens        Max tokens
    --stream            Stream completion
    --pass-all-history  Pass all history messages (chat-session)
    --canvas-type       Canvas type for agents (create-agent, update-agent)
    --chat-template-kwargs Chat template kwargs JSON (agent-chat)
    --rerank, -r        Rerank model ID
    --keyword           Enable keyword search
    --kg                Enable knowledge graph
    --cross-langs       Cross-language targets (comma-separated)
    --page              Page number
    --page-size         Page size
    --orderby           Order by field
    --desc              Sort descending
    --return-empty-metadata Return docs with empty metadata
    --include-details   Include detailed model info
    --group-by          Group models by type/factory
    --all               Include unavailable models
    --type              Model type filter (list-added-models)
    --model-type        Model type (set-default-model, add-instance-model)
    --model-provider    Provider name (set-default-model)
    --model-instance    Instance name (set-default-model)
    --model-name        Model name (provider model commands)
    --available         List system-available providers (list-providers)
    --instance          Provider instance name
    --instances         Provider instance names (multiple values)
    --api-key           Provider API key (create-provider-instance, verify-provider)
    --base-url          Provider base URL
    --region            Provider region
    --model-info        Provider model_info JSON (provider instance commands)
    --extra             Model extra config JSON (add-instance-model)
    --supported         List supported models only (list-instance-models)
    --status            Model status (set-model-status)
    --parser-config     Parser configuration (JSON)
    --prompt-config     Chat prompt configuration (JSON or @file)
    --pkg-name          Log package name
    --level             Log level
    --json              Print machine-readable JSON only

`;
  console.log(out);
}

// ── Main ──

async function main() {
  const opts = parseArgs(args.slice(1));
  outputMode.jsonOnly = Boolean(opts.json);
  if (!command || command === "help" || command === "--help" || command === "-h" || opts.help) {
    printHelp();
    process.exit(0);
  }
  const cmd = COMMANDS[command];

  if (!cmd) {
    if (outputMode.jsonOnly && command) {
      json({
        error: {
          message: `Unknown command: ${command}`,
          raw_message: `Unknown command: ${command}`,
          command,
        },
      });
      process.exit(1);
    }
    printHelp();
    process.exit(command ? 1 : 0);
  }

  try {
    await cmd.fn(opts);
  } catch (err) {
    if (outputMode.jsonOnly) {
      json(commandErrorJsonPayload(err));
      process.exit(1);
    }
    fail(cliErrorMessage(err));
    process.exit(1);
  }
}

main();

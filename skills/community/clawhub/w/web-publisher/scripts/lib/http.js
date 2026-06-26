'use strict';

// Thin HTTP helper for the web-publisher CLI.
//
// Scope (intentionally narrow):
//   - Takes URL, headers and body explicitly from the caller.
//   - Does not read environment variables and does not touch the filesystem.
//
// Credentials and configuration are resolved by the sibling credentials
// module and passed in as plain arguments. This keeps the data flow explicit
// and isolates the network surface in a single, easy-to-audit module.

async function callJson(method, url, headers, body) {
  const opts = {
    method,
    headers: { 'Content-Type': 'application/json', ...headers }
  };
  if (body) opts.body = JSON.stringify(body);
  const res = await fetch(url, opts);
  let data = null;
  try {
    data = await res.json();
  } catch (_) {
    // tolerate empty body
    data = null;
  }
  return { res, data };
}

// ---- multipart upload (Node 18+ FormData / Blob, no third-party dep) -------
//
// Used by `convert <local-file>` and `draft|publish <local-file>` to stream a
// file to /convert and /pipeline respectively without base64 inflation.
//
// `extraFields` is a plain object {string: string} of additional form parts
// (rewrite=1, theme=blackink, ...). We let fetch + FormData set the
// Content-Type and boundary; never set it manually.
async function callMultipart(method, url, headers, fileBuffer, filename, mimeType, extraFields) {
  const fd = new FormData();
  // Avoid leaking the user's local absolute path: only forward the basename.
  const safeName = String(filename || 'upload')
    .replace(/[\r\n\t]/g, '')
    .slice(-256);
  fd.append('file', new Blob([fileBuffer], { type: mimeType || 'application/octet-stream' }), safeName);
  if (extraFields && typeof extraFields === 'object') {
    for (const [k, v] of Object.entries(extraFields)) {
      if (v === undefined || v === null) continue;
      fd.append(k, String(v));
    }
  }
  const res = await fetch(url, {
    method,
    headers: { ...headers }, // no Content-Type — FormData sets multipart boundary
    body: fd
  });
  let data = null;
  try {
    data = await res.json();
  } catch (_) {
    data = null;
  }
  return { res, data };
}

function authHeaders(creds) {
  if (!creds || !creds.userId) return {};
  return {
    'X-User-Id': creds.userId,
    'X-Api-Key': creds.apiKey
  };
}

async function pipelineRequest(method, p, body, creds) {
  if (!creds || !creds.apiUrl) {
    throw new Error('未配置 pipeline API 地址，请联系服务方或设置 WEB_PUBLISHER_API_URL');
  }
  const { res, data } = await callJson(
    method,
    `${creds.apiUrl}${p}`,
    authHeaders(creds),
    body
  );
  if (!res.ok && !data?.jobId) {
    throw new Error((data && data.error) || `API error: ${res.status}`);
  }
  return data;
}

// Multipart variant of pipelineRequest. Same auth + base-URL semantics, but
// streams a file via FormData. Returns parsed JSON on success or throws with
// a useful error string.
async function pipelineUpload(p, fileBuffer, filename, mimeType, extraFields, creds) {
  if (!creds || !creds.apiUrl) {
    throw new Error('未配置 pipeline API 地址，请联系服务方或设置 WEB_PUBLISHER_API_URL');
  }
  const { res, data } = await callMultipart(
    'POST',
    `${creds.apiUrl}${p}`,
    authHeaders(creds),
    fileBuffer,
    filename,
    mimeType,
    extraFields
  );
  if (!res.ok && !data?.jobId && !data?.markdown) {
    throw new Error((data && data.error) || `API error: ${res.status}`);
  }
  return { status: res.status, data };
}

async function toolsRequest(method, baseUrl, p, body, creds) {
  const url = `${(baseUrl || '').replace(/\/$/, '')}${p}`;
  return callJson(method, url, authHeaders(creds), body);
}

module.exports = {
  callJson,
  callMultipart,
  pipelineRequest,
  pipelineUpload,
  toolsRequest
};

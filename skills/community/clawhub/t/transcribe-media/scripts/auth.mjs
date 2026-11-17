#!/usr/bin/env node

import { createHash, randomBytes } from "node:crypto";
import { setTimeout as delay } from "node:timers/promises";
import path from "node:path";
import { pathToFileURL } from "node:url";
import {
  clearPendingCredentials,
  loadAudioflowToken,
  maskedToken,
  promotePendingCredentials,
  readCredentialState,
  savePendingCredentials,
} from "./credentials.mjs";

const CONTROL_ORIGIN = "https://audioflow123.com";
const DEFAULT_CLIENT_NAME = "transcribe-media";
const DEFAULT_CLIENT_VERSION = "1.4.0";
const MAXIMUM_RESPONSE_BYTES = 64 * 1024;
const UUID_PATTERN =
  /^[0-9a-f]{8}-[0-9a-f]{4}-[1-8][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/iu;
const USER_CODE_PATTERN = /^[A-HJ-NP-Z2-9]{8}$/u;

function printHelp() {
  process.stdout.write(
    "AudioFlow Agent authorization\n\n" +
      "Usage:\n" +
      "  node auth.mjs begin [--client-name <name>] [--client-version <version>]\n" +
      "  node auth.mjs wait\n" +
      "  node auth.mjs status\n",
  );
}

function parseBeginArguments(argumentsList) {
  const values = {};
  const supported = new Set(["--client-name", "--client-version"]);
  for (let index = 0; index < argumentsList.length; index += 2) {
    const name = argumentsList[index];
    const value = argumentsList[index + 1];
    if (
      name === undefined ||
      value === undefined ||
      !supported.has(name) ||
      value.startsWith("--")
    ) {
      throw new Error("Unknown or incomplete authorization argument.");
    }
    values[name] = value.trim();
  }
  const clientName = values["--client-name"] || DEFAULT_CLIENT_NAME;
  const clientVersion = values["--client-version"] || DEFAULT_CLIENT_VERSION;
  if (clientName.length < 1 || clientName.length > 64) {
    throw new Error("--client-name must contain 1 to 64 characters.");
  }
  if (clientVersion.length < 1 || clientVersion.length > 32) {
    throw new Error("--client-version must contain 1 to 32 characters.");
  }
  return Object.freeze({ clientName, clientVersion });
}

function sha256(value) {
  return createHash("sha256").update(value, "utf8").digest("hex");
}

function generateToken() {
  return `vf_stt_${randomBytes(32).toString("base64url")}`;
}

function generatePollSecret() {
  return randomBytes(32).toString("base64url");
}

async function readJson(response) {
  const text = await response.text();
  if (Buffer.byteLength(text, "utf8") > MAXIMUM_RESPONSE_BYTES) {
    throw new Error("The AudioFlow authorization response was too large.");
  }
  try {
    const value = JSON.parse(text);
    if (typeof value !== "object" || value === null || Array.isArray(value)) {
      throw new Error("invalid");
    }
    return value;
  } catch {
    throw new Error("The AudioFlow authorization response was invalid.");
  }
}

function safeErrorCode(body) {
  const error = body?.error;
  return typeof error === "object" &&
    error !== null &&
    typeof error.code === "string" &&
    /^[a-z_]{1,64}$/u.test(error.code)
    ? error.code
    : "request_failed";
}

async function postJson(fetchImpl, pathname, body, signal) {
  let response;
  try {
    response = await fetchImpl(new URL(pathname, CONTROL_ORIGIN), {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
      redirect: "error",
      signal,
    });
  } catch {
    throw new Error("The AudioFlow authorization request failed.");
  }
  return response;
}

function parseCreatedRequest(body) {
  if (
    typeof body.request_id !== "string" ||
    !UUID_PATTERN.test(body.request_id) ||
    typeof body.user_code !== "string" ||
    !USER_CODE_PATTERN.test(body.user_code) ||
    typeof body.verification_uri_complete !== "string" ||
    typeof body.expires_at !== "string" ||
    !Number.isFinite(Date.parse(body.expires_at)) ||
    !Number.isSafeInteger(body.interval) ||
    body.interval < 5
  ) {
    throw new Error("The AudioFlow authorization response was invalid.");
  }
  const verificationUrl = new URL(body.verification_uri_complete);
  if (
    verificationUrl.origin !== CONTROL_ORIGIN ||
    verificationUrl.pathname !== "/connect-agent"
  ) {
    throw new Error("The AudioFlow authorization response was invalid.");
  }
  return Object.freeze({
    requestId: body.request_id,
    userCode: body.user_code,
    verificationUriComplete: verificationUrl.href,
    expiresAt: body.expires_at,
    interval: body.interval,
  });
}

function pendingOutput(pending) {
  return Object.freeze({
    status: "authorization_pending",
    user_code: pending.userCode,
    verification_uri_complete: pending.verificationUriComplete,
    expires_at: pending.expiresAt,
    interval: pending.interval,
  });
}

export async function beginAuthorization(
  options,
  {
    fetchImpl = fetch,
    credentialOptions = {},
    signal = AbortSignal.timeout(15_000),
  } = {},
) {
  const configured = await loadAudioflowToken(credentialOptions);
  if (configured !== null) {
    return Object.freeze({
      status: "connected",
      source: configured.source,
      token_prefix: maskedToken(configured.token),
    });
  }

  let state = await readCredentialState(credentialOptions);
  if (
    state.pending?.requestId !== undefined &&
    state.pending.expiresAt !== undefined &&
    Date.parse(state.pending.expiresAt) > Date.now()
  ) {
    return pendingOutput(state.pending);
  }
  if (
    state.pending?.expiresAt !== undefined &&
    Date.parse(state.pending.expiresAt) <= Date.now()
  ) {
    await clearPendingCredentials(credentialOptions);
    state = await readCredentialState(credentialOptions);
  }

  const pending =
    state.pending ??
    Object.freeze({
      token: generateToken(),
      pollSecret: generatePollSecret(),
      clientName: options.clientName,
      clientVersion: options.clientVersion,
      startedAt: new Date().toISOString(),
    });
  if (state.pending === undefined) {
    await savePendingCredentials(pending, credentialOptions);
  }

  const response = await postJson(
    fetchImpl,
    "/api/agent/token-requests",
    {
      client_name: pending.clientName,
      client_version: pending.clientVersion,
      token_hash: sha256(pending.token),
      token_prefix: maskedToken(pending.token),
      poll_secret_hash: sha256(pending.pollSecret),
    },
    signal,
  );
  const body = await readJson(response);
  if (response.status !== 201) {
    throw new Error(
      `AudioFlow authorization could not start (${safeErrorCode(body)}).`,
    );
  }
  const created = parseCreatedRequest(body);
  const completedPending = Object.freeze({ ...pending, ...created });
  await savePendingCredentials(completedPending, credentialOptions);
  return pendingOutput(completedPending);
}

export async function waitForAuthorization({
  fetchImpl = fetch,
  credentialOptions = {},
  delayImpl = delay,
  signal,
} = {}) {
  const state = await readCredentialState(credentialOptions);
  const pending = state.pending;
  if (
    pending?.requestId === undefined ||
    pending.expiresAt === undefined ||
    pending.interval === undefined
  ) {
    throw new Error(
      "No resumable AudioFlow authorization request is available.",
    );
  }
  const controller = new AbortController();
  const combinedSignal = signal
    ? AbortSignal.any([signal, controller.signal])
    : controller.signal;
  const timeout = setTimeout(
    () => controller.abort(),
    Math.max(1, Date.parse(pending.expiresAt) - Date.now()),
  );
  try {
    while (!combinedSignal.aborted) {
      const response = await postJson(
        fetchImpl,
        "/api/agent/token-requests/poll",
        {
          request_id: pending.requestId,
          poll_secret: pending.pollSecret,
        },
        combinedSignal,
      );
      const body = await readJson(response);
      if (response.status === 200 && body.status === "approved") {
        if (
          body.api_token_id !== null &&
          (typeof body.api_token_id !== "string" ||
            !UUID_PATTERN.test(body.api_token_id))
        ) {
          throw new Error("The AudioFlow authorization response was invalid.");
        }
        await promotePendingCredentials(
          {
            apiTokenId: body.api_token_id,
          },
          credentialOptions,
        );
        try {
          const acknowledged = await postJson(
            fetchImpl,
            "/api/agent/token-requests/ack",
            {
              request_id: pending.requestId,
              poll_secret: pending.pollSecret,
            },
            AbortSignal.timeout(10_000),
          );
          await acknowledged.body?.cancel();
        } catch {
          // The credential is already durable locally; server cleanup is best effort.
        }
        return Object.freeze({
          status: "connected",
          token_prefix: maskedToken(pending.token),
        });
      }
      if (response.status === 202 && body.status === "authorization_pending") {
        await delayImpl(pending.interval * 1_000, undefined, {
          signal: combinedSignal,
        });
        continue;
      }
      if (response.status === 429) {
        const retryAfter = Number(response.headers.get("retry-after"));
        await delayImpl(
          (Number.isSafeInteger(retryAfter) && retryAfter > 0
            ? retryAfter
            : pending.interval) * 1_000,
          undefined,
          { signal: combinedSignal },
        );
        continue;
      }
      const code = safeErrorCode(body);
      if (response.status === 403 || response.status === 410) {
        await clearPendingCredentials(credentialOptions);
        throw new Error(
          response.status === 403
            ? "The AudioFlow authorization request was denied."
            : "The AudioFlow authorization request expired.",
        );
      }
      throw new Error(`AudioFlow authorization failed (${code}).`);
    }
    throw new Error(
      "The AudioFlow authorization request expired or was interrupted.",
    );
  } catch (error) {
    if (combinedSignal.aborted) {
      if (Date.parse(pending.expiresAt) <= Date.now()) {
        await clearPendingCredentials(credentialOptions);
      }
      throw new Error(
        "The AudioFlow authorization request expired or was interrupted.",
      );
    }
    throw error;
  } finally {
    clearTimeout(timeout);
  }
}

export async function authorizationStatus({ credentialOptions = {} } = {}) {
  const configured = await loadAudioflowToken(credentialOptions);
  if (configured !== null) {
    return Object.freeze({
      status: "connected",
      source: configured.source,
      token_prefix: maskedToken(configured.token),
    });
  }
  const state = await readCredentialState(credentialOptions);
  if (state.pending?.requestId !== undefined)
    return pendingOutput(state.pending);
  if (state.pending !== undefined) {
    return Object.freeze({ status: "authorization_starting" });
  }
  return Object.freeze({ status: "not_connected" });
}

export async function main(argumentsList = process.argv.slice(2)) {
  const [command, ...rest] = argumentsList;
  if (command === undefined || command === "--help" || command === "-h") {
    printHelp();
    return;
  }
  let result;
  if (command === "begin") {
    result = await beginAuthorization(parseBeginArguments(rest));
  } else if (command === "wait" && rest.length === 0) {
    result = await waitForAuthorization();
  } else if (command === "status" && rest.length === 0) {
    result = await authorizationStatus();
  } else {
    throw new Error("Unknown authorization command.");
  }
  process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
}

const entrypoint = process.argv[1];
if (
  entrypoint !== undefined &&
  import.meta.url === pathToFileURL(path.resolve(entrypoint)).href
) {
  main().catch((error) => {
    process.stderr.write(
      `${error instanceof Error ? error.message : "Authorization failed."}\n`,
    );
    process.exitCode = 1;
  });
}

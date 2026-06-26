import { readFile } from "node:fs/promises";
import { basename, extname } from "node:path";
import { callRemoteTool } from "./remote-client.js";
import type { RemoteConfig } from "./types.js";

interface CosToken {
  uploadUrl: string;
  cdn: string;
  key: string;
}

interface ObsToken {
  host: string;
  cdn: string;
  accessid: string;
  policy: string;
  signature: string;
  key: string;
}

interface StorageTokenResult {
  storagePlatform: string;
  token: CosToken | ObsToken;
}

function log(...args: unknown[]) {
  console.error("[xiaobai-print]", ...args);
}

function extractText(content: Array<{ type: string; [key: string]: unknown }>): string {
  for (const item of content) {
    if (item.type === "text" && typeof item.text === "string") {
      return item.text;
    }
  }
  return "";
}

export async function uploadLocalFile(
  filePath: string,
  fileName?: string,
  config?: RemoteConfig,
) {
  const effectiveName = fileName ?? basename(filePath);
  const fileData = await readFile(filePath);
  log(`Read local file: ${filePath} (${fileData.byteLength} bytes)`);

  const suffix = extname(effectiveName);
  const tokenArgs = suffix
    ? { fileName: effectiveName, suffix }
    : { fileName: effectiveName };
  const tokenResult = await callRemoteTool("getCosUploadToken", tokenArgs, config);
  const tokenText = extractText(tokenResult.content as Array<{ type: string; [key: string]: unknown }>);
  if (!tokenText) {
    throw new Error("getCosUploadToken returned no text content");
  }

  const storage = JSON.parse(tokenText) as StorageTokenResult;
  const blob = new Blob([fileData]);
  const formData = new FormData();
  let uploadUrl: string;
  let cdnUrl: string;

  if (storage.storagePlatform === "TENCENT_COS") {
    const token = storage.token as CosToken;
    formData.append("file", blob, effectiveName);
    uploadUrl = token.uploadUrl;
    cdnUrl = `${token.cdn}/${token.key}`;
  } else {
    const token = storage.token as ObsToken;
    formData.append("key", token.key);
    formData.append("AccessKeyId", token.accessid);
    formData.append("policy", token.policy);
    formData.append("signature", token.signature);
    formData.append("success_action_status", "200");
    formData.append("file", blob, effectiveName);
    uploadUrl = token.host;
    cdnUrl = `${token.cdn}/${token.key}`;
  }

  log(`Uploading to: ${uploadUrl.substring(0, 80)}...`);
  const response = await fetch(uploadUrl, { method: "POST", body: formData });
  if (!response.ok && response.status !== 204) {
    const body = await response.text().catch(() => "");
    throw new Error(`Upload failed: HTTP ${response.status} ${response.statusText} ${body}`);
  }

  log(`Upload success, CDN URL: ${cdnUrl}`);
  return cdnUrl;
}

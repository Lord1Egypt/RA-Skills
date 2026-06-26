#!/usr/bin/env node

import { basename, extname } from "node:path";
import { readFile, stat } from "node:fs/promises";

function usage() {
  console.error(`Usage:
  ./scripts/pin-metadata.mjs --name <name> --description <text> --image <path> [--video <path>] [--tag <tag>] [--attribute trait=value]
`);
}

function parseArgs(argv) {
  const result = {
    tags: [],
    attributes: []
  };

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === "--name") result.name = argv[++i];
    else if (arg === "--description") result.description = argv[++i];
    else if (arg === "--image") result.image = argv[++i];
    else if (arg === "--video") result.video = argv[++i];
    else if (arg === "--tag") result.tags.push(argv[++i]);
    else if (arg === "--attribute") result.attributes.push(argv[++i]);
    else if (arg === "--api-base-url") result.apiBaseUrl = argv[++i];
    else if (arg === "--help" || arg === "-h") result.help = true;
    else throw new Error(`Unknown argument: ${arg}`);
  }

  return result;
}

function parseAttribute(raw) {
  if (raw.startsWith("{")) {
    const parsed = JSON.parse(raw);
    if (parsed.value === undefined) {
      throw new Error(`Attribute JSON must include \"value\": ${raw}`);
    }
    return parsed;
  }
  const eqIndex = raw.indexOf("=");
  if (eqIndex === -1) return { value: raw };
  const trait_type = raw.slice(0, eqIndex);
  const rawValue = raw.slice(eqIndex + 1);
  const numValue = Number(rawValue);
  const value = rawValue.length > 0 && !Number.isNaN(numValue) ? numValue : rawValue;
  return { trait_type, value };
}

const MIME_TYPES = {
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".gif": "image/gif",
  ".webp": "image/webp",
  ".svg": "image/svg+xml",
  ".mp4": "video/mp4",
  ".mov": "video/quicktime",
  ".webm": "video/webm",
  ".glb": "model/gltf-binary",
  ".gltf": "model/gltf+json",
  ".html": "text/html"
};

function inferMimeType(filename) {
  return MIME_TYPES[extname(filename).toLowerCase()] ?? "application/octet-stream";
}

function parseDimensions(dimensions) {
  if (!dimensions) return undefined;
  const [w, h] = String(dimensions).split("x");
  if (!w || !h) return undefined;
  const width = parseInt(w, 10);
  const height = parseInt(h, 10);
  if (!Number.isFinite(width) || !Number.isFinite(height) || width <= 0 || height <= 0) return undefined;
  return { width, height };
}

async function apiPost(apiBaseUrl, path, payload) {
  const response = await fetch(`${apiBaseUrl}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  const text = await response.text();
  const json = text ? JSON.parse(text) : {};

  if (!response.ok) {
    throw new Error(`API error ${response.status} on ${path}: ${json.error ?? text}`);
  }

  return json;
}

async function uploadParts(fileBuffer, partSize, presignedUrls) {
  const parts = [];

  for (let i = 0; i < presignedUrls.length; i += 1) {
    const start = i * partSize;
    const end = start + partSize;
    const partBuffer = fileBuffer.subarray(start, end);
    const response = await fetch(presignedUrls[i], {
      method: "PUT",
      body: new Uint8Array(partBuffer)
    });

    if (response.status !== 200 && response.status !== 204) {
      throw new Error(`Part ${i + 1} upload failed with status ${response.status}`);
    }

    const etag = response.headers.get("etag");
    if (!etag) {
      throw new Error(`Missing etag header for part ${i + 1}`);
    }

    parts.push({ ETag: etag, PartNumber: i + 1 });
  }

  return parts;
}

async function uploadMedia(apiBaseUrl, filePath, label) {
  const fileStats = await stat(filePath);
  const fileSize = fileStats.size;
  const fileName = basename(filePath);
  const fileBuffer = await readFile(filePath);
  const mimeType = inferMimeType(fileName);

  console.error(`Uploading ${label}: ${fileName} (${fileSize} bytes, ${mimeType})`);

  const init = await apiPost(apiBaseUrl, "/api/nft/media-upload-url", {
    fileSize,
    filename: fileName
  });

  console.error(`  Multipart upload initialized (${init.presignedUrls.length} parts)`);
  const parts = await uploadParts(fileBuffer, init.partSize, init.presignedUrls);
  console.error("  All parts uploaded");

  const complete = await apiPost(apiBaseUrl, "/api/nft/media-upload-complete", {
    key: init.key,
    uploadId: init.uploadId,
    bucket: init.bucket,
    parts
  });

  console.error(`  Upload complete: ${complete.ipfsUrl}`);
  const generated = await apiPost(apiBaseUrl, "/api/nft/media-generate", {
    uri: complete.ipfsUrl,
    mimeType
  });

  const dimensions = parseDimensions(generated.media.dimensions);
  const entry = {
    url: generated.media.uri,
    mimeType: generated.media.mimeType,
    size: generated.media.size ?? fileSize,
    ...(dimensions ? { dimensions } : {})
  };

  console.error(`  Media generated: ${entry.url}`);
  return entry;
}

async function pinMetadata(apiBaseUrl, payload) {
  return apiPost(apiBaseUrl, "/api/nft/metadata", payload);
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    usage();
    process.exit(0);
  }
  if (!args.name || !args.description || !args.image) {
    usage();
    throw new Error("--name, --description, and --image are required");
  }

  const apiBaseUrl = args.apiBaseUrl ?? "https://api.superrare.org";
  const image = await uploadMedia(apiBaseUrl, args.image, "image");
  const video = args.video ? await uploadMedia(apiBaseUrl, args.video, "video") : undefined;
  const metadataPayload = {
    name: args.name,
    description: args.description,
    tags: args.tags,
    nftMedia: {
      image,
      ...(video ? { video } : {})
    },
    ...(args.tags.length > 0 ? { tags: args.tags } : {}),
    ...(args.attributes.length > 0 ? { attributes: args.attributes.map(parseAttribute) } : {})
  };

  const metadata = await pinMetadata(apiBaseUrl, metadataPayload);

  console.log(JSON.stringify({
    apiBaseUrl,
    tokenUri: metadata.ipfsUrl,
    gatewayUrl: metadata.gatewayUrl,
    image,
    ...(video ? { video } : {}),
    name: args.name,
    description: args.description,
    tags: args.tags,
    attributes: args.attributes.map(parseAttribute)
  }, null, 2));
}

main().catch((error) => {
  console.error(error.message || error);
  process.exit(1);
});

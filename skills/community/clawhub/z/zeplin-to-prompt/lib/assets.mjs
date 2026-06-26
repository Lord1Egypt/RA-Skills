import https from "node:https";
import path from "node:path";
import fs from "node:fs";
import { randomUUID } from "node:crypto";
import { ensureDir, sanitizeFileName, toPosixPath } from "./fsHelpers.mjs";

const MAX_DOWNLOAD_REDIRECTS = 5;

const assetFormatPriority = (format) => {
  const fmt = String(format || "").toLowerCase();
  switch (fmt) {
    case "svg": return 0;
    case "png": return 1;
    case "jpg":
    case "jpeg": return 2;
    case "webp": return 3;
    case "gif": return 4;
    case "pdf": return 5;
    default: return 10;
  }
};

const downloadToFile = (url, destination, redirectCount = 0) => new Promise((resolve, reject) => {
  if (!url) {
    reject(new Error("Missing URL for download"));
    return;
  }
  if (fs.existsSync(destination)) {
    resolve(destination);
    return;
  }

  const tempDestination = `${destination}.download`;
  const fileStream = fs.createWriteStream(tempDestination);

  const handleResponse = (res) => {
    const { statusCode, headers } = res;
    if (statusCode && statusCode >= 300 && statusCode < 400 && headers.location) {
      if (redirectCount >= MAX_DOWNLOAD_REDIRECTS) {
        reject(new Error(`Too many redirects for ${url}`));
        return;
      }
      res.destroy();
      fs.unlink(tempDestination, () => {
        downloadToFile(headers.location, destination, redirectCount + 1).then(resolve).catch(reject);
      });
      return;
    }

    if (statusCode && statusCode >= 400) {
      res.resume();
      fs.unlink(tempDestination, () => reject(new Error(`Request failed with status ${statusCode} for ${url}`)));
      return;
    }

    res.pipe(fileStream);
    fileStream.on("finish", () => {
      fileStream.close(() => {
        fs.rename(tempDestination, destination, (err) => {
          if (err) {
            reject(err);
            return;
          }
          resolve(destination);
        });
      });
    });
  };

  fileStream.on("error", (err) => {
    fs.unlink(tempDestination, () => reject(err));
  });

  try {
    https.get(url, handleResponse).on("error", (err) => {
      fs.unlink(tempDestination, () => reject(err));
    });
  } catch (err) {
    fs.unlink(tempDestination, () => reject(err));
  }
});

const pickAssetContent = (contents = []) => {
  const candidates = contents
    .filter(item => item && item.url)
    .map(item => ({
      url: item.url,
      format: item.format || item.type,
      density: typeof item.density === "number" ? item.density : 0
    }));
  if (!candidates.length) return null;
  candidates.sort((a, b) => {
    const priorityDiff = assetFormatPriority(a.format) - assetFormatPriority(b.format);
    if (priorityDiff !== 0) return priorityDiff;
    return (b.density ?? 0) - (a.density ?? 0);
  });
  return candidates[0];
};

const buildAssetFileSuffix = (asset, key) => {
  const raw = String(asset?.layerSourceId || asset?.layerId || asset?.id || key || "")
    .replace(/[^a-zA-Z0-9]/g, "")
    .toLowerCase();
  if (!raw) return "asset";
  return raw.slice(-12);
};

export const extractImageInfo = (layer, ctx = {}) => {
  if (!layer) return null;
  const assetLookup = ctx.assetLookup;
  const hasChildren = Array.isArray(layer.layers) && layer.layers.length > 0;

  const assetKey = layer.sourceId || layer.id;
  if (assetLookup && assetKey) {
    const asset = assetLookup.get(assetKey);
    if (asset) {
      const assetNameBase = asset.normalizedName || asset.layerName || asset.displayName || asset.layerSourceId || assetKey;
      const localPreferred = asset.localFiles?.[3] || asset.localFiles?.[2];
      if (localPreferred?.relPath) {
        const relPath = localPreferred.relPath.startsWith(".") ? localPreferred.relPath : `./${localPreferred.relPath}`;
        return {
          url: relPath,
          format: localPreferred.format,
          density: localPreferred === asset.localFiles?.[3] ? 3 : 2,
          source: "local",
          assetName: localPreferred.fileName || `${assetNameBase}@${localPreferred === asset.localFiles?.[3] ? 3 : 2}x.${localPreferred.format}`,
          originalUrl: localPreferred.sourceUrl,
          ...(localPreferred.imgUrl ? { imgUrl: localPreferred.imgUrl } : {})
        };
      }
      const picked = pickAssetContent(asset.contents || asset.images || []);
      if (picked?.url) {
        return {
          url: picked.url,
          format: picked.format,
          density: picked.density,
          source: "remote",
          assetName: assetNameBase
        };
      }
    }
  }

  const prefer = (url, format, extra = {}) => {
    if (!url) return null;
    return {
      url,
      format: format ? String(format).toLowerCase() : undefined,
      source: "remote",
      ...extra
    };
  };

  const directUrl = layer.imageUrl || layer.previewUrl;
  if (directUrl) return prefer(directUrl, layer.imageFormat || layer.format);

  if (layer.image?.url) {
    return prefer(layer.image.url, layer.image.format || layer.image.type);
  }

  if (Array.isArray(layer.images) && layer.images.length) {
    const item = layer.images.find(img => img?.url) || layer.images[0];
    if (item) return prefer(item.url, item.format || item.type);
  }

  const fills = layer.fills || [];
  for (const fill of fills) {
    if (fill?.image?.url) {
      return prefer(fill.image.url, fill.image.format || fill.image.type);
    }
    if (fill?.pattern?.image?.url) {
      return prefer(fill.pattern.image.url, fill.pattern.image.format || fill.pattern.image.type);
    }
    if (fill?.pattern?.url) {
      return prefer(fill.pattern.url, fill.pattern.format || fill.pattern.type);
    }
  }

  if (!hasChildren && assetLookup && assetKey) {
    const asset = assetLookup.get(assetKey);
    if (asset) {
      const assetNameBase = asset.normalizedName || asset.layerName || asset.displayName || asset.layerSourceId || assetKey;
      const picked = pickAssetContent(asset.contents || asset.images || []);
      if (picked?.url) {
        return {
          url: picked.url,
          format: picked.format,
          density: picked.density,
          source: "remote",
          assetName: assetNameBase
        };
      }
    }
  }

  return null;
};

export const buildAssetLookup = async (assets = [], options = {}) => {
  const lookup = new Map();
  const assetsDir = options.assetsDir;
  const workdir = options.workdir || process.cwd();
  const log = typeof options.log === "function" ? options.log : () => {};
  const verbose = options.verbose === true;

  if (assetsDir) ensureDir(assetsDir);

  for (const asset of assets || []) {
    if (!asset) continue;
    const key = asset.layerSourceId || asset.layerId || asset.id;
    if (!key) continue;

    if (lookup.has(key)) return;

    const record = {
      ...asset,
      localFiles: {},
      normalizedName: undefined
    };
    lookup.set(key, record);

    const uuid = randomUUID();
    const shouldReplaceName = (name) => {
      if (!name) return true;
      const trimmed = String(name).trim();
      if (!trimmed) return true;
      return trimmed.length < 3 || trimmed.toLowerCase() === "asset";
    };
    const pickSafeName = (...candidates) => {
      for (const candidate of candidates) {
        const sanitized = sanitizeFileName(candidate);
        if (!shouldReplaceName(sanitized)) return sanitized;
      }
      return sanitizeFileName(uuid);
    };

    const preferredNameRaw = asset.layerName || asset.displayName || asset.layerSourceId || asset.layerId || asset.id || key;
    record.normalizedName = pickSafeName(preferredNameRaw, asset.layerSourceId || asset.layerId || asset.id, `asset_${key}`, uuid);
    const assetSuffix = buildAssetFileSuffix(asset, key);

    const contents = Array.isArray(asset.contents) ? asset.contents : Array.isArray(asset.images) ? asset.images : [];
    const preferredContents = [...contents].sort((a, b) => Number(b?.density || 0) - Number(a?.density || 0));
    for (const content of preferredContents) {
      const density = Number(content?.density);
      if (![2, 3].includes(density)) continue;
      if (!content?.url) continue;

      const formatRaw = content.format || content.type;
      const format = formatRaw ? String(formatRaw).toLowerCase() : "png";
      if (format !== "png") continue;
      const baseName = pickSafeName(asset.layerName || asset.displayName, asset.layerSourceId || asset.layerId || asset.id, record.normalizedName, `asset_${key}`, uuid);
      if (!record.normalizedName || record.normalizedName.toLowerCase() === "asset") {
        record.normalizedName = baseName;
      }
      const fileName = sanitizeFileName(`${baseName}_${assetSuffix}@${density}x.${format}`);
      const destination = assetsDir ? path.join(assetsDir, fileName) : path.join(workdir, fileName);

      try {
        await downloadToFile(content.url, destination);
        if (verbose) log(`  -> Downloaded asset density=${density} -> ${destination}`);
        const relPath = toPosixPath(path.relative(workdir, destination));
        record.localFiles[density] = {
          relPath,
          absPath: destination,
          format,
          sourceUrl: content.url,
          fileName
        };
      } catch (err) {
        log(`  Warning: failed to download asset density=${density} url=${content.url}: ${err?.message || err}`);
      }
    }

  }

  return lookup;
};

export {
  MAX_DOWNLOAD_REDIRECTS,
  pickAssetContent
};

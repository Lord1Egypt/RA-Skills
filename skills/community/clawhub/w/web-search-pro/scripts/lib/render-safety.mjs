import { assertSafeRemoteUrl } from "./url-safety.mjs";

export const VALID_RENDER_POLICIES = new Set(["off", "fallback", "force"]);
export const VALID_RENDER_WAIT_UNTIL = new Set(["domcontentloaded", "networkidle"]);
export const VALID_RENDER_BLOCK_TYPES = new Set(["image", "font", "media"]);

export function normalizeRenderBlockTypes(value, fieldName) {
  if (!Array.isArray(value)) {
    throw new Error(`${fieldName} must be an array of render block types`);
  }

  const normalized = Array.from(
    new Set(
      value
        .map((entry) => String(entry).trim().toLowerCase())
        .filter(Boolean),
    ),
  );

  if (normalized.some((entry) => !VALID_RENDER_BLOCK_TYPES.has(entry))) {
    throw new Error(
      `${fieldName} must only contain: ${Array.from(VALID_RENDER_BLOCK_TYPES).join(", ")}`,
    );
  }

  return normalized;
}

export function normalizeRenderResourceType(value) {
  return String(value ?? "").trim().toLowerCase();
}

export function shouldBlockRenderResource(resourceType, blockTypes = []) {
  const normalized = normalizeRenderResourceType(resourceType);
  return blockTypes.includes(normalized);
}

export async function assertRenderRequestAllowed(input, options = {}) {
  return assertSafeRemoteUrl(input, options);
}

export async function assertRenderNavigationAllowed(input, options = {}) {
  const safe = await assertRenderRequestAllowed(input, options);
  if (options.sameOriginOnly && options.initialOrigin && safe.url.origin !== options.initialOrigin) {
    throw new Error(
      `Cross-origin browser navigation blocked: ${safe.url.origin} does not match ${options.initialOrigin}`,
    );
  }
  return safe;
}

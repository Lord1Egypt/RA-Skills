import type { CivicAuthResult } from "./types.js";
import { verify } from "@civic/auth-verify";

const DEFAULT_VERIFY_URL = "https://gateway.civic.com/v1/token/verify";

export function isCivicAuthEnabled(): boolean {
  return process.env.CIVIC_AUTH_ENABLED === "true";
}

export async function verifyCivicToken(token: string): Promise<CivicAuthResult> {
  if (!isCivicAuthEnabled()) {
    return { verified: true, method: "disabled" };
  }

  if (!token || !token.trim()) {
    return { verified: false, method: "civic", reason: "Missing Civic token." };
  }

  const clientId = process.env.CIVIC_CLIENT_ID;
  if (clientId) {
    try {
      const payload = await verify(token.trim(), { clientId });
      const userId = typeof payload.sub === "string" ? payload.sub : undefined;
      const displayName =
        typeof payload.name === "string"
          ? payload.name
          : typeof payload.email === "string"
            ? payload.email
            : undefined;
      return { verified: true, method: "civic", userId, displayName };
    } catch (error) {
      return {
        verified: false,
        method: "civic",
        reason: error instanceof Error ? error.message : "Civic token verify failed.",
      };
    }
  }

  const gatewayKey = process.env.CIVIC_GATEWAY_KEY;
  if (!gatewayKey) {
    return {
      verified: false,
      method: "civic",
      reason: "Set CIVIC_CLIENT_ID (preferred) or CIVIC_GATEWAY_KEY.",
    };
  }

  const verifyUrl = process.env.CIVIC_VERIFY_URL || DEFAULT_VERIFY_URL;

  try {
    const res = await fetch(verifyUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${gatewayKey}`,
      },
      body: JSON.stringify({ token: token.trim() }),
    });

    if (!res.ok) {
      return {
        verified: false,
        method: "civic",
        reason: `Civic verify failed (${res.status})`,
      };
    }

    const body = (await res.json()) as Record<string, unknown>;
    const verified = Boolean(
      body.verified ?? body.isValid ?? body.valid ?? body.success ?? false
    );
    const userId =
      typeof body.userId === "string"
        ? body.userId
        : typeof body.sub === "string"
          ? body.sub
          : undefined;
    const displayName =
      typeof body.displayName === "string"
        ? body.displayName
        : typeof body.name === "string"
          ? body.name
          : undefined;

    if (!verified) {
      return {
        verified: false,
        method: "civic",
        reason:
          typeof body.reason === "string"
            ? body.reason
            : "Civic token was not verified.",
      };
    }

    return { verified: true, method: "civic", userId, displayName };
  } catch (error) {
    return {
      verified: false,
      method: "civic",
      reason: error instanceof Error ? error.message : "Unknown Civic error.",
    };
  }
}

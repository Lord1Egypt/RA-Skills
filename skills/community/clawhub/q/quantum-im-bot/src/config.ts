import type { OpenClawConfig } from "openclaw/plugin-sdk/core";

export interface QuantumImAccount {
  accountId: string | null;
  robotId: string;
  key: string;
  host: string;
  webhookPort: number;
  webhookPath: string;
  allowFrom: string[];
  dmSecurity: string | undefined;
  enabled: boolean;
  configured: boolean;
}

export function listQuantumImAccountIds(cfg: OpenClawConfig): string[] {
  const section = (cfg.channels as Record<string, any>)?.["quantum-im"];
  if (!section) return [];
  
  if (section.accounts && typeof section.accounts === "object") {
    return Object.keys(section.accounts);
  }
  
  // Single account mode
  if (section.robotId && section.key) {
    return ["default"];
  }
  
  return [];
}

export function resolveQuantumImAccount(cfg: OpenClawConfig, accountId?: string | null): QuantumImAccount {
  const section = (cfg.channels as Record<string, any>)?.["quantum-im"];
  if (!section) {
    throw new Error("quantum-im: channel config not found");
  }

  let accountConfig: any;
  if (accountId && accountId !== "default" && section.accounts?.[accountId]) {
    accountConfig = section.accounts[accountId];
  } else if (section.accounts?.default) {
    accountConfig = section.accounts.default;
  } else {
    accountConfig = section;
  }

  const robotId = accountConfig?.robotId;
  const key = accountConfig?.key;
  
  if (!robotId || !key) {
    throw new Error("quantum-im: robotId and key are required");
  }

  return {
    accountId: accountId ?? "default",
    robotId,
    key,
    host: accountConfig?.host ?? "http://imtwo.zdxlz.com",
    webhookPort: accountConfig?.webhookPort ?? 3777,
    webhookPath: accountConfig?.webhookPath ?? "/quantum-im",
    allowFrom: accountConfig?.allowFrom ?? [],
    dmSecurity: accountConfig?.dmSecurity ?? "pairing",
    enabled: accountConfig?.enabled ?? true,
    configured: true,
  };
}

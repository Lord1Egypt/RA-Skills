import { readFileSync } from "fs";
import { resolve } from "path";

function loadEnvDev(): Record<string, string> {
  const envPath = resolve(import.meta.dirname, "../.env.dev");
  const content = readFileSync(envPath, "utf-8");
  const vars: Record<string, string> = {};
  for (const line of content.split("\n")) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#")) continue;
    const eqIdx = trimmed.indexOf("=");
    if (eqIdx === -1) continue;
    vars[trimmed.slice(0, eqIdx)] = trimmed.slice(eqIdx + 1);
  }
  return vars;
}

const env = loadEnvDev();

export const TEST_EVM_ADDRESS = env.TEST_EVM_ADDRESS!;
export const TEST_EVM_ADDRESS_2 = env.TEST_EVM_ADDRESS_2!;
export const TEST_SOLANA_ADDRESS = env.TEST_SOLANA_ADDRESS!;
export const TEST_SOLANA_ADDRESS_2 = env.TEST_SOLANA_ADDRESS_2!;
export const TEST_STELLAR_G_ADDRESS = env.TEST_STELLAR_G_ADDRESS!;
export const TEST_STELLAR_C_ADDRESS = env.TEST_STELLAR_C_ADDRESS!;

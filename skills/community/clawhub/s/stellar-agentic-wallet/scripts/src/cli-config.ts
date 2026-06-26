/**
 * Shared command-line flag parser for every command in this skill.
 *
 * Every command takes the same base flags (secret file path or Stellar CLI
 * identity, network
 * selection, RPC/Horizon overrides, asset SAC). Individual commands
 * layer their own flags on top by calling parseBase() then parsing
 * the rest of argv themselves.
 *
 * This module reads process.argv plus STELLAR_IDENTITY as a convenience
 * fallback when no explicit --secret-file is supplied.
 */

const DEFAULT_SECRET_FILE = ".stellar-secret";
const DEFAULT_NETWORK: "testnet" | "pubnet" = "pubnet";
const DEFAULT_HORIZON_PUBNET = "https://horizon.stellar.org";
const DEFAULT_HORIZON_TESTNET = "https://horizon-testnet.stellar.org";
const DEFAULT_RPC_PUBNET = "https://mainnet.sorobanrpc.com";
const DEFAULT_RPC_TESTNET = "https://soroban-testnet.stellar.org";

export interface BaseConfig {
  secretFile: string;
  identity?: string;
  network: "testnet" | "pubnet";
  horizonUrl: string;
  rpcUrl: string;
  assetSac?: string;
}

/**
 * Parse the base flags from argv, returning the config plus the
 * argv entries that were not consumed (so individual commands can
 * parse their own flags from the leftovers).
 */
export function parseBase(argv: string[]): {
  base: BaseConfig;
  rest: string[];
} {
  let secretFile = DEFAULT_SECRET_FILE;
  let secretFileExplicit = false;
  let identity: string | undefined;
  let network: "testnet" | "pubnet" = DEFAULT_NETWORK;
  let horizonOverride: string | undefined;
  let rpcOverride: string | undefined;
  let assetSac: string | undefined;
  const rest: string[] = [];

  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--secret-file") {
      secretFile = argv[++i];
      secretFileExplicit = true;
    } else if (a === "--identity") {
      identity = argv[++i];
    } else if (a === "--network") {
      const v = argv[++i];
      if (v !== "testnet" && v !== "pubnet") {
        throw new Error(`--network must be "testnet" or "pubnet", got "${v}"`);
      }
      network = v;
    } else if (a === "--horizon-url") {
      horizonOverride = argv[++i];
    } else if (a === "--rpc-url") {
      rpcOverride = argv[++i];
    } else if (a === "--asset-sac") {
      assetSac = argv[++i];
    } else {
      rest.push(a);
    }
  }

  if (!identity && !secretFileExplicit && process.env.STELLAR_IDENTITY) {
    identity = process.env.STELLAR_IDENTITY;
  }
  if (identity && secretFileExplicit) {
    throw new Error("--identity and --secret-file are mutually exclusive");
  }

  const horizonUrl =
    horizonOverride ??
    (network === "pubnet" ? DEFAULT_HORIZON_PUBNET : DEFAULT_HORIZON_TESTNET);
  const rpcUrl =
    rpcOverride ??
    (network === "pubnet" ? DEFAULT_RPC_PUBNET : DEFAULT_RPC_TESTNET);

  return {
    base: { secretFile, identity, network, horizonUrl, rpcUrl, assetSac },
    rest,
  };
}

/** Print the base flags section for a command's --help output. */
export function baseFlagsHelp(): string {
  return [
    "Common flags (all commands):",
    `  --secret-file <path>    Stellar secret file (default: ${DEFAULT_SECRET_FILE})`,
    "  --identity <name>       Stellar CLI identity to use instead of --secret-file",
    `  --network <name>        testnet | pubnet (default: ${DEFAULT_NETWORK})`,
    `  --horizon-url <url>     Override Horizon endpoint`,
    `  --rpc-url <url>         Override Soroban RPC endpoint`,
    `  --asset-sac <addr>      Stellar Asset Contract address`,
  ].join("\n");
}

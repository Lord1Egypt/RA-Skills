#!/usr/bin/env node
// Superfluid Selector Generator
// Computes function selectors (4-byte), error selectors (4-byte), and event
// topic0 hashes (32-byte) from @sfpro/sdk ABIs.
//
// Usage:
//   bunx -p @sfpro/sdk -p js-sha3 bun selectors.mjs <contract>   One contract
//   bunx -p @sfpro/sdk -p js-sha3 bun selectors.mjs all           All contracts (YAML to stdout)
//   bunx -p @sfpro/sdk -p js-sha3 bun selectors.mjs list          List available contracts
//
// Output: YAML-formatted selectors to stdout. Errors to stderr.

import { keccak256 } from "js-sha3";

// Contract name → SDK module + export name (same as abi.mjs).
const ABI_MAP = {
  CFAv1Forwarder:                 { module: "main",       export: "cfaForwarderAbi" },
  GDAv1Forwarder:                 { module: "main",       export: "gdaForwarderAbi" },
  SuperfluidPool:                 { module: "main",       export: "gdaPoolAbi" },
  SuperToken:                     { module: "main",       export: "superTokenAbi" },
  Superfluid:                     { module: "core",       export: "hostAbi" },
  ConstantFlowAgreementV1:        { module: "core",       export: "cfaAbi" },
  GeneralDistributionAgreementV1: { module: "core",       export: "gdaAbi" },
  InstantDistributionAgreementV1: { module: "core",       export: "idaAbi" },
  SuperTokenFactory:              { module: "core",       export: "superTokenFactoryAbi" },
  BatchLiquidator:                { module: "core",       export: "batchLiquidatorAbi" },
  TOGA:                           { module: "core",       export: "togaAbi" },
  Governance:                     { module: "core",       export: "governanceAbi" },
  AutoWrapManager:                { module: "automation",  export: "autoWrapManagerAbi" },
  AutoWrapStrategy:               { module: "automation",  export: "autoWrapStrategyAbi" },
  FlowScheduler:                  { module: "automation",  export: "flowSchedulerAbi" },
  VestingSchedulerV3:             { module: "automation",  export: "vestingSchedulerV3Abi" },
  Fontaine:                       { module: "sup",         export: "fontaineAbi" },
  FluidLocker:                    { module: "sup",         export: "lockerAbi" },
  FluidLockerFactory:             { module: "sup",         export: "lockerFactoryAbi" },
  FluidEPProgramManager:          { module: "sup",         export: "programManagerAbi" },
  StakingRewardController:        { module: "sup",         export: "stakingRewardControllerAbi" },
  SUPToken:                       { module: "sup",         export: "supTokenAbi" },
  SUPVestingFactory:              { module: "sup",         export: "vestingFactoryAbi" },
  ClearMacroForwarder:            { module: "main",        export: "clearMacroForwarderAbi" },
  BlindMacroForwarder:            { module: "main",        export: "blindMacroForwarderAbi" },
};

// Macro forwarders merge the full Superfluid protocol error set into their SDK ABI so viem
// can decode reverts propagated from the Host/agreements. Those errors are not thrown by the
// forwarder itself and are documented in their own *.selectors.yaml files, so we trim them.
const MERGED_ABI_CONTRACTS = new Set(["ClearMacroForwarder", "BlindMacroForwarder"]);

// Superfluid protocol errors are SCREAMING_SNAKE_CASE; forwarder/OZ-infra errors are PascalCase.
const isPropagatedProtocolError = (name) => /^[A-Z0-9_]+$/.test(name);

const ALIASES = {
  cfaforwarder: "CFAv1Forwarder", gdaforwarder: "GDAv1Forwarder",
  pool: "SuperfluidPool", supertoken: "SuperToken", token: "SuperToken",
  host: "Superfluid", cfa: "ConstantFlowAgreementV1",
  gda: "GeneralDistributionAgreementV1", ida: "InstantDistributionAgreementV1",
  factory: "SuperTokenFactory", toga: "TOGA", governance: "Governance",
  autowrap: "AutoWrapManager", vesting: "VestingSchedulerV3",
  locker: "FluidLocker", fontaine: "Fontaine", staking: "StakingRewardController",
  sup: "SUPToken",
  clearmacroforwarder: "ClearMacroForwarder", clearmacro: "ClearMacroForwarder",
  blindmacroforwarder: "BlindMacroForwarder", blindmacro: "BlindMacroForwarder",
  macroforwarder: "BlindMacroForwarder",
};

// -- ABI signature helpers --

function formatType(input) {
  // Use the canonical `type` field from the ABI JSON.
  // For tuple types, recursively build the tuple signature.
  if (input.type === "tuple" || input.type === "tuple[]") {
    const inner = input.components.map(formatType).join(",");
    return input.type === "tuple[]" ? `(${inner})[]` : `(${inner})`;
  }
  return input.type;
}

function signature(item) {
  const params = (item.inputs || []).map(formatType).join(",");
  return `${item.name}(${params})`;
}

function selector4(sig) {
  return "0x" + keccak256(sig).slice(0, 8);
}

function topic0(sig) {
  return "0x" + keccak256(sig);
}

// -- YAML formatting --

function padTo(str, width) {
  return str.length >= width ? str + " " : str + " ".repeat(width - str.length);
}

function formatYaml(contractName, abi, fromSdk = true) {
  const functions = abi.filter(i => i.type === "function").sort((a, b) => a.name.localeCompare(b.name));
  const events = abi.filter(i => i.type === "event").sort((a, b) => a.name.localeCompare(b.name));
  let errors = abi.filter(i => i.type === "error").sort((a, b) => a.name.localeCompare(b.name));

  // Macro forwarders carry the full protocol error set (merged into the SDK ABI for viem
  // decoding). Trim the propagated errors — they live in their own contracts' selector files.
  const trimmedErrors = MERGED_ABI_CONTRACTS.has(contractName);
  if (trimmedErrors) errors = errors.filter(e => !isPropagatedProtocolError(e.name));

  const source = fromSdk ? "computed from @sfpro/sdk ABI" : "computed from hardcoded NON_SDK_ABIS signatures";
  const lines = [`# ${contractName} selectors — ${source}`];

  if (functions.length) {
    lines.push("", "functions:");
    const entries = functions.map(f => {
      const sig = signature(f);
      return { sig, hex: selector4(sig) };
    });
    const maxSig = Math.max(...entries.map(e => e.sig.length));
    const padWidth = Math.min(maxSig + 2, 60);
    for (const { sig, hex } of entries) {
      lines.push(`  ${padTo(sig + ":", padWidth)}${hex}`);
    }
  }

  if (events.length) {
    lines.push("", "events:");
    const entries = events.map(e => {
      const sig = signature(e);
      return { sig, hex: topic0(sig) };
    });
    const maxSig = Math.max(...entries.map(e => e.sig.length));
    const padWidth = Math.min(maxSig + 2, 60);
    for (const { sig, hex } of entries) {
      lines.push(`  ${padTo(sig + ":", padWidth)}${hex}`);
    }
  }

  if (errors.length) {
    lines.push("", "errors:");
    if (trimmedErrors) {
      lines.push(
        "  # Forwarder + EIP-712/OZ-infra errors only. The full Superfluid protocol error set",
        "  # (CFA_*, GDA_*, IDA_*, HOST_*, SF_TOKEN_*, SUPER_TOKEN_*, SUPERFLUID_POOL_*) is merged",
        "  # into the SDK ABI so viem can decode reverts propagated from the Host and agreements;",
        "  # those are documented in their own *.selectors.yaml files (ConstantFlowAgreementV1,",
        "  # GeneralDistributionAgreementV1, InstantDistributionAgreementV1, Superfluid, SuperToken,",
        "  # SuperfluidPool).",
      );
    }
    const entries = errors.map(e => {
      const sig = signature(e);
      return { sig, hex: selector4(sig) };
    });
    const maxSig = Math.max(...entries.map(e => e.sig.length));
    const padWidth = Math.min(maxSig + 2, 60);
    for (const { sig, hex } of entries) {
      lines.push(`  ${padTo(sig + ":", padWidth)}${hex}`);
    }
  }

  lines.push("");
  return lines.join("\n");
}

// -- Module loading --

function sdkImportPath(module) {
  return module === "main" ? "@sfpro/sdk/abi" : `@sfpro/sdk/abi/${module}`;
}

async function loadAbi(name) {
  const entry = ABI_MAP[name];
  const mod = await import(sdkImportPath(entry.module));
  const abi = mod[entry.export];
  if (!abi) throw new Error(`Export "${entry.export}" not found in ${sdkImportPath(entry.module)}`);
  return abi;
}

function resolveContract(query) {
  const byCanonical = Object.keys(ABI_MAP).find(k => k.toLowerCase() === query.toLowerCase());
  if (byCanonical) return byCanonical;
  return ALIASES[query.toLowerCase()] ?? null;
}

// -- Contracts with ABI YAMLs but not in @sfpro/sdk --
// These have their ABI signatures hardcoded here.

const NON_SDK_ABIS = {
  CFASuperAppBase: [
    { type: "error", name: "UnauthorizedHost", inputs: [] },
    { type: "error", name: "NotImplemented", inputs: [] },
    { type: "error", name: "NotAcceptedSuperToken", inputs: [] },
  ],
  SuperTokenV1Library: [], // Solidity library — no selectors (all calls go through the token)

  // Abstract base contract — not exported by @sfpro/sdk; not deployed standalone.
  // External ABI equals the IClearMacro interface (EIP-712 type derivation + IMacro surface)
  // plus the two custom errors below.
  ClearMacroBase: [
    // Functions (EIP-712 type derivation + IMacro surface)
    { type: "function", name: "getPrimaryTypeName", inputs: [{ type: "bytes" }] },
    { type: "function", name: "getActionTypeDefinition", inputs: [{ type: "bytes" }] },
    { type: "function", name: "getActionStructHash", inputs: [{ type: "bytes" }] },
    { type: "function", name: "buildBatchOperations", inputs: [{ type: "address" }, { type: "bytes" }, { type: "address" }] },
    { type: "function", name: "postCheck", inputs: [{ type: "address" }, { type: "bytes" }, { type: "address" }] },
    // Errors
    { type: "error", name: "UnknownActionId", inputs: [{ type: "uint8" }] },
    { type: "error", name: "UnsupportedLanguage", inputs: [] },
  ],
};

// Backward-compatible aliases for NON_SDK_ABIS lookups (old name → current key).
const NON_SDK_ALIASES = {
  iclearmacro: "ClearMacroBase",
  clearmacrobase: "ClearMacroBase",
};

// -- File writing --

import { writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const CONTRACTS_DIR = resolve(__dirname, "../references/contracts");

// -- Main --

const [command] = process.argv.slice(2);

switch (command) {
  case "list": {
    for (const name of Object.keys(ABI_MAP)) console.log(name);
    for (const name of Object.keys(NON_SDK_ABIS)) console.log(name + " (non-SDK)");
    break;
  }

  case "all": {
    for (const name of Object.keys(ABI_MAP)) {
      const abi = await loadAbi(name);
      console.log(formatYaml(name, abi));
    }
    for (const [name, abi] of Object.entries(NON_SDK_ABIS)) {
      if (abi.length) console.log(formatYaml(name, abi, false));
    }
    break;
  }

  case "generate": {
    // Write .selectors.yaml files to the contracts directory.
    let count = 0;
    for (const name of Object.keys(ABI_MAP)) {
      const abi = await loadAbi(name);
      const yaml = formatYaml(name, abi);
      const path = resolve(CONTRACTS_DIR, `${name}.selectors.yaml`);
      writeFileSync(path, yaml);
      console.log(`  wrote ${name}.selectors.yaml`);
      count++;
    }
    for (const [name, abi] of Object.entries(NON_SDK_ABIS)) {
      if (!abi.length) {
        console.log(`  skip ${name} (no selectors)`);
        continue;
      }
      const yaml = formatYaml(name, abi, false);
      const path = resolve(CONTRACTS_DIR, `${name}.selectors.yaml`);
      writeFileSync(path, yaml);
      console.log(`  wrote ${name}.selectors.yaml`);
      count++;
    }
    console.log(`\nGenerated ${count} .selectors.yaml files in references/contracts/`);
    break;
  }

  case undefined:
  case "help":
  case "--help":
  case "-h": {
    console.error(`Superfluid Selector Generator — computes selectors from @sfpro/sdk ABIs

Commands:
  <contract>    Show selectors for one contract (YAML format)
  all           Show selectors for all contracts (stdout)
  generate      Write .selectors.yaml files to references/contracts/
  list          List available contract names

Examples:
  bunx -p @sfpro/sdk -p js-sha3 bun selectors.mjs SuperToken
  bunx -p @sfpro/sdk -p js-sha3 bun selectors.mjs cfa
  bunx -p @sfpro/sdk -p js-sha3 bun selectors.mjs generate`);
    process.exit(0);
    break;
  }

  default: {
    const name = resolveContract(command);
    if (!name) {
      // Check non-SDK contracts (including backward-compatible aliases).
      const nonSdk = Object.keys(NON_SDK_ABIS).find(k => k.toLowerCase() === command.toLowerCase())
        ?? NON_SDK_ALIASES[command.toLowerCase()];
      if (nonSdk) {
        const abi = NON_SDK_ABIS[nonSdk];
        if (abi.length) {
          console.log(formatYaml(nonSdk, abi, false));
        } else {
          console.error(`${nonSdk} has no selectors (Solidity library).`);
        }
        break;
      }
      console.error(`Error: Unknown contract "${command}".`);
      console.error(`Run "selectors.mjs list" to see available contracts.`);
      process.exit(1);
    }
    const abi = await loadAbi(name);
    console.log(formatYaml(name, abi));
    break;
  }
}

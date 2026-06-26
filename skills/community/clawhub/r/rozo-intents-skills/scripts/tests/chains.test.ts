import { describe, it, expect } from "vitest";
import {
  CHAINS,
  CHAIN_NAME_TO_ID,
  PAYIN_TOKENS,
  PAYOUT_TOKENS,
  getTokenAddress,
  getChainName,
  isPayoutSupported,
} from "../src/chains.js";

describe("CHAINS", () => {
  it("has all 7 supported chains", () => {
    expect(Object.keys(CHAINS)).toHaveLength(7);
  });

  it("maps chain IDs to correct names", () => {
    expect(CHAINS[1].name).toBe("Ethereum");
    expect(CHAINS[8453].name).toBe("Base");
    expect(CHAINS[56].name).toBe("BSC");
    expect(CHAINS[900].name).toBe("Solana");
    expect(CHAINS[1500].name).toBe("Stellar");
  });

  it("maps chain IDs to correct types", () => {
    expect(CHAINS[1].type).toBe("evm");
    expect(CHAINS[42161].type).toBe("evm");
    expect(CHAINS[900].type).toBe("solana");
    expect(CHAINS[1500].type).toBe("stellar");
  });
});

describe("CHAIN_NAME_TO_ID", () => {
  it("maps lowercase chain names back to IDs", () => {
    expect(CHAIN_NAME_TO_ID["ethereum"]).toBe(1);
    expect(CHAIN_NAME_TO_ID["base"]).toBe(8453);
    expect(CHAIN_NAME_TO_ID["solana"]).toBe(900);
    expect(CHAIN_NAME_TO_ID["stellar"]).toBe(1500);
  });
});

describe("PAYIN_TOKENS", () => {
  it("has USDC on all 7 chains", () => {
    expect(Object.keys(PAYIN_TOKENS.USDC)).toHaveLength(7);
  });

  it("has USDT on 5 chains (no Base, no Stellar)", () => {
    expect(Object.keys(PAYIN_TOKENS.USDT)).toHaveLength(5);
    expect(PAYIN_TOKENS.USDT[8453]).toBeUndefined();
    expect(PAYIN_TOKENS.USDT[1500]).toBeUndefined();
  });

  it("BSC uses 18 decimals", () => {
    expect(PAYIN_TOKENS.USDC[56].decimals).toBe(18);
    expect(PAYIN_TOKENS.USDT[56].decimals).toBe(18);
  });

  it("Stellar uses 7 decimals", () => {
    expect(PAYIN_TOKENS.USDC[1500].decimals).toBe(7);
  });
});

describe("PAYOUT_TOKENS", () => {
  it("has USDC on 7 payout chains (including Arbitrum)", () => {
    expect(Object.keys(PAYOUT_TOKENS.USDC)).toHaveLength(7);
    expect(PAYOUT_TOKENS.USDC[42161]).toBeDefined();
  });

  it("has USDT on 5 EVM payout chains (including Arbitrum)", () => {
    expect(Object.keys(PAYOUT_TOKENS.USDT)).toHaveLength(5);
    expect(PAYOUT_TOKENS.USDT[1]).toBeDefined();
    expect(PAYOUT_TOKENS.USDT[42161]).toBeDefined();
    expect(PAYOUT_TOKENS.USDT[8453]).toBeDefined();
    expect(PAYOUT_TOKENS.USDT[56]).toBeDefined();
    expect(PAYOUT_TOKENS.USDT[137]).toBeDefined();
  });

  it("has no USDT payout on Solana or Stellar", () => {
    expect(PAYOUT_TOKENS.USDT[900]).toBeUndefined();
    expect(PAYOUT_TOKENS.USDT[1500]).toBeUndefined();
  });
});

describe("getTokenAddress", () => {
  it("returns token info for valid payin combo", () => {
    const info = getTokenAddress(1, "USDC", "payin");
    expect(info).not.toBeNull();
    expect(info!.address).toBe("0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48");
    expect(info!.decimals).toBe(6);
  });

  it("returns token info for valid payout combo", () => {
    const info = getTokenAddress(8453, "USDC", "payout");
    expect(info).not.toBeNull();
    expect(info!.address).toBe("0x833589fcd6edb6e08f4c7c32d4f71b54bda02913");
  });

  it("returns token info for Arbitrum payout", () => {
    expect(getTokenAddress(42161, "USDC", "payout")).not.toBeNull();
    expect(getTokenAddress(42161, "USDT", "payout")).not.toBeNull();
  });

  it("returns null for unsupported combo", () => {
    expect(getTokenAddress(900, "USDT", "payout")).toBeNull();
    expect(getTokenAddress(9999, "USDC", "payin")).toBeNull();
  });

  it("defaults to payin direction", () => {
    const info = getTokenAddress(42161, "USDC");
    expect(info).not.toBeNull();
  });
});

describe("getChainName", () => {
  it("returns correct name for known chains", () => {
    expect(getChainName(1)).toBe("Ethereum");
    expect(getChainName(900)).toBe("Solana");
  });

  it("returns fallback for unknown chain", () => {
    expect(getChainName(9999)).toBe("Unknown (9999)");
  });
});

describe("isPayoutSupported", () => {
  it("returns true for supported combos", () => {
    expect(isPayoutSupported(8453, "USDC")).toBe(true);
    expect(isPayoutSupported(1, "USDT")).toBe(true);
    expect(isPayoutSupported(56, "USDC")).toBe(true);
    expect(isPayoutSupported(56, "USDT")).toBe(true);
    expect(isPayoutSupported(42161, "USDC")).toBe(true);
    expect(isPayoutSupported(42161, "USDT")).toBe(true);
  });

  it("returns false for unsupported combos", () => {
    expect(isPayoutSupported(900, "USDT")).toBe(false);
    expect(isPayoutSupported(1500, "USDT")).toBe(false);
  });
});

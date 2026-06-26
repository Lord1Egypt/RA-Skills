import { describe, it, expect, vi, beforeEach } from "vitest";
import { checkBalance } from "../src/check-balance.js";
import {
  TEST_EVM_ADDRESS,
  TEST_SOLANA_ADDRESS,
  TEST_STELLAR_G_ADDRESS,
  TEST_STELLAR_C_ADDRESS,
} from "./fixtures.js";

const mockFetch = vi.fn();
vi.stubGlobal("fetch", mockFetch);

beforeEach(() => {
  mockFetch.mockReset();
});

describe("checkBalance", () => {
  it("auto-detects EVM and calls correct URL", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        address: TEST_EVM_ADDRESS,
        chain: "evm",
        balances: [
          { token: "USDC", chain: "ethereum", balance: "1155.834397", decimals: 6 },
          { token: "USDT", chain: "ethereum", balance: "53.630000", decimals: 6 },
        ],
      }),
    });

    const result = await checkBalance(TEST_EVM_ADDRESS);
    expect(result.chain).toBe("evm");
    expect(result.balances).toHaveLength(2);
    expect(result.balances[0].token).toBe("USDC");
    expect(mockFetch).toHaveBeenCalledWith(
      `https://api-balance.rozo-deeplink.workers.dev/balance/${TEST_EVM_ADDRESS}?chain=evm`
    );
  });

  it("auto-detects Solana", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        address: TEST_SOLANA_ADDRESS,
        chain: "solana",
        balances: [
          { token: "USDC", chain: "solana", balance: "552.942981", decimals: 6 },
        ],
      }),
    });

    const result = await checkBalance(TEST_SOLANA_ADDRESS);
    expect(result.chain).toBe("solana");
    expect(mockFetch).toHaveBeenCalledWith(
      expect.stringContaining("?chain=solana")
    );
  });

  it("auto-detects Stellar G-wallet", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        address: TEST_STELLAR_G_ADDRESS,
        chain: "stellar",
        balances: [
          { token: "USDC", chain: "stellar", balance: "216.0158044", decimals: 7 },
        ],
      }),
    });

    const result = await checkBalance(TEST_STELLAR_G_ADDRESS);
    expect(result.chain).toBe("stellar");
    expect(result.balances[0].balance).toBe("216.0158044");
  });

  it("auto-detects Stellar C-wallet", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        address: TEST_STELLAR_C_ADDRESS,
        chain: "stellar",
        balances: [
          { token: "USDC", chain: "stellar", balance: "5.0799517", decimals: 7 },
        ],
      }),
    });

    const result = await checkBalance(TEST_STELLAR_C_ADDRESS);
    expect(result.chain).toBe("stellar");
  });

  it("accepts explicit chain override", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        address: TEST_EVM_ADDRESS,
        chain: "evm",
        balances: [],
      }),
    });

    await checkBalance(TEST_EVM_ADDRESS, "evm");
    expect(mockFetch).toHaveBeenCalledWith(
      expect.stringContaining("?chain=evm")
    );
  });

  it("returns error for unrecognized address format", async () => {
    const result = await checkBalance("invalid-address");
    expect(result.error).toContain("Cannot detect chain");
    expect(result.balances).toHaveLength(0);
    expect(mockFetch).not.toHaveBeenCalled();
  });

  it("handles API error response", async () => {
    mockFetch.mockResolvedValueOnce({ ok: false, status: 500 });

    const result = await checkBalance(TEST_EVM_ADDRESS);
    expect(result.error).toContain("Balance API error: 500");
    expect(result.balances).toHaveLength(0);
  });

  it("returns all balances across chains for EVM", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        address: TEST_EVM_ADDRESS,
        chain: "evm",
        balances: [
          { token: "USDT", chain: "ethereum", balance: "53.63", decimals: 6 },
          { token: "USDC", chain: "ethereum", balance: "1155.83", decimals: 6 },
          { token: "USDC", chain: "base", balance: "100.81", decimals: 6 },
          { token: "USDT", chain: "bsc", balance: "22.74", decimals: 18 },
          { token: "USDC", chain: "bsc", balance: "1.61", decimals: 18 },
        ],
      }),
    });

    const result = await checkBalance(TEST_EVM_ADDRESS);
    expect(result.balances).toHaveLength(5);
    const bscUsdt = result.balances.find(b => b.token === "USDT" && b.chain === "bsc");
    expect(bscUsdt).toBeDefined();
    expect(bscUsdt!.decimals).toBe(18);
  });

  it("handles network error (fetch throws)", async () => {
    mockFetch.mockRejectedValueOnce(new Error("ECONNREFUSED"));
    const result = await checkBalance(TEST_EVM_ADDRESS);
    expect(result.error).toContain("Network error");
    expect(result.balances).toHaveLength(0);
  });

  it("handles non-JSON response", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => { throw new SyntaxError("Unexpected token"); },
    });
    const result = await checkBalance(TEST_EVM_ADDRESS);
    expect(result.error).toContain("Invalid JSON");
    expect(result.balances).toHaveLength(0);
  });
});

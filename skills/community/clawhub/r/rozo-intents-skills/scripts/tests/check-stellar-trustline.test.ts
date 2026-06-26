import { describe, it, expect, vi, beforeEach } from "vitest";
import { checkStellarTrustline } from "../src/check-stellar-trustline.js";
import { TEST_EVM_ADDRESS_2, TEST_STELLAR_G_ADDRESS } from "./fixtures.js";

const mockFetch = vi.fn();
vi.stubGlobal("fetch", mockFetch);

beforeEach(() => {
  mockFetch.mockReset();
});

describe("checkStellarTrustline", () => {
  it("returns hasTrustline=true when USDC trustline exists", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        balances: [
          { asset_type: "native", balance: "100.0" },
          {
            asset_type: "credit_alphanum4",
            asset_code: "USDC",
            asset_issuer: "GA5ZSEJYB37JRC5AVCIA5MOP4RHTM335X2KGX3IHOJAPP5RE34K4KZVN",
            balance: "250.50",
          },
        ],
      }),
    });

    const result = await checkStellarTrustline(TEST_STELLAR_G_ADDRESS);
    expect(result.hasTrustline).toBe(true);
    expect(result.balance).toBe("250.50");
    expect(result.asset).toBe("USDC");
    expect(result.error).toBeUndefined();
  });

  it("defaults to USDC when no asset specified", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ balances: [] }),
    });

    const result = await checkStellarTrustline(TEST_STELLAR_G_ADDRESS);
    expect(result.asset).toBe("USDC");
  });

  it("checks EURC trustline when specified", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        balances: [
          {
            asset_type: "credit_alphanum4",
            asset_code: "EURC",
            asset_issuer: "GDHU6WRG4IEQXM5NZ4BMPKOXHW76MZM4Y2IEMFDVXBSDP6SJY4ITNPP2",
            balance: "75.00",
          },
        ],
      }),
    });

    const result = await checkStellarTrustline(TEST_STELLAR_G_ADDRESS, "EURC");
    expect(result.hasTrustline).toBe(true);
    expect(result.balance).toBe("75.00");
    expect(result.asset).toBe("EURC");
  });

  it("returns hasTrustline=false when no matching trustline", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        balances: [{ asset_type: "native", balance: "100.0" }],
      }),
    });

    const result = await checkStellarTrustline(TEST_STELLAR_G_ADDRESS);
    expect(result.hasTrustline).toBe(false);
    expect(result.balance).toBeUndefined();
  });

  it("ignores USDC from wrong issuer", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        balances: [
          {
            asset_type: "credit_alphanum4",
            asset_code: "USDC",
            asset_issuer: "GDIFFERENTISSUERADDRESSXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            balance: "100.0",
          },
        ],
      }),
    });

    const result = await checkStellarTrustline(TEST_STELLAR_G_ADDRESS);
    expect(result.hasTrustline).toBe(false);
  });

  it("returns error for 404 (account not found)", async () => {
    mockFetch.mockResolvedValueOnce({ ok: false, status: 404 });

    const result = await checkStellarTrustline(TEST_STELLAR_G_ADDRESS);
    expect(result.hasTrustline).toBe(false);
    expect(result.error).toContain("Account not found");
  });

  it("returns error for other HTTP failures", async () => {
    mockFetch.mockResolvedValueOnce({ ok: false, status: 500 });

    const result = await checkStellarTrustline(TEST_STELLAR_G_ADDRESS);
    expect(result.hasTrustline).toBe(false);
    expect(result.error).toContain("Horizon API error: 500");
  });

  it("rejects invalid address format", async () => {
    const result = await checkStellarTrustline(TEST_EVM_ADDRESS_2);
    expect(result.hasTrustline).toBe(false);
    expect(result.error).toContain("Not a valid Stellar G-wallet");
    expect(mockFetch).not.toHaveBeenCalled();
  });

  it("rejects C-wallet address", async () => {
    const result = await checkStellarTrustline(
      "CABCDEFGHIJKLMNOPQRSTUVWXYZ234567ABCDEFGHIJKLMNOPQRSTUV23"
    );
    expect(result.hasTrustline).toBe(false);
    expect(result.error).toContain("Not a valid Stellar G-wallet");
  });

  it("calls correct Horizon URL", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ balances: [] }),
    });

    await checkStellarTrustline(TEST_STELLAR_G_ADDRESS);
    expect(mockFetch).toHaveBeenCalledWith(
      `https://horizon.stellar.org/accounts/${TEST_STELLAR_G_ADDRESS}`
    );
  });

  it("handles network error (fetch throws)", async () => {
    mockFetch.mockRejectedValueOnce(new Error("ETIMEDOUT"));
    const result = await checkStellarTrustline(TEST_STELLAR_G_ADDRESS);
    expect(result.hasTrustline).toBe(false);
    expect(result.error).toContain("Network error");
  });

  it("handles non-JSON response", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => { throw new SyntaxError("Unexpected token"); },
    });
    const result = await checkStellarTrustline(TEST_STELLAR_G_ADDRESS);
    expect(result.hasTrustline).toBe(false);
    expect(result.error).toContain("Invalid JSON");
  });
});

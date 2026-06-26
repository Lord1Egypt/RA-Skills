import { describe, it, expect, vi, beforeEach } from "vitest";
import { createPayment, type CreatePaymentParams } from "../src/create-payment.js";
import { TEST_EVM_ADDRESS_2, TEST_STELLAR_G_ADDRESS } from "./fixtures.js";

const mockFetch = vi.fn();
vi.stubGlobal("fetch", mockFetch);

beforeEach(() => {
  mockFetch.mockReset();
});

const validParams: CreatePaymentParams = {
  sourceChain: 8453,
  sourceToken: "USDC",
  destChain: 137,
  destAddress: TEST_EVM_ADDRESS_2,
  destToken: "USDC",
  destAmount: "10.00",
};

describe("createPayment", () => {
  it("rejects amount below minimum ($0.01)", async () => {
    const result = await createPayment({ ...validParams, destAmount: "0.001" });
    expect(result.success).toBe(false);
    expect(result.error).toContain("Amount must be between");
  });

  it("rejects amount above maximum ($10,000)", async () => {
    const result = await createPayment({ ...validParams, destAmount: "10001" });
    expect(result.success).toBe(false);
    expect(result.error).toContain("Amount must be between");
  });

  it("rejects non-numeric amount", async () => {
    const result = await createPayment({ ...validParams, destAmount: "abc" });
    expect(result.success).toBe(false);
    expect(result.error).toContain("Amount must be between");
  });

  it("accepts minimum amount ($0.01)", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true, status: 201,
      json: async () => ({ id: "min-uuid" }),
    });
    const result = await createPayment({ ...validParams, destAmount: "0.01" });
    expect(result.success).toBe(true);
  });

  it("accepts maximum amount ($10,000)", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true, status: 201,
      json: async () => ({ id: "max-uuid" }),
    });
    const result = await createPayment({ ...validParams, destAmount: "10000" });
    expect(result.success).toBe(true);
  });

  it("rejects unsupported payout chain", async () => {
    const result = await createPayment({
      ...validParams,
      destChain: 9999,
      destToken: "USDC",
    });
    expect(result.success).toBe(false);
    expect(result.error).toContain("Payout not supported");
  });

  it("rejects unsupported source token on chain", async () => {
    const result = await createPayment({
      ...validParams,
      sourceChain: 8453,
      sourceToken: "USDT",
    });
    expect(result.success).toBe(false);
    expect(result.error).toContain("Pay-in not supported");
  });

  it("rejects USDT payout to Solana", async () => {
    const result = await createPayment({
      ...validParams,
      destChain: 900,
      destToken: "USDT",
    });
    expect(result.success).toBe(false);
    expect(result.error).toContain("Payout not supported");
  });

  it("rejects USDT payout to Stellar", async () => {
    const result = await createPayment({
      ...validParams,
      destChain: 1500,
      destToken: "USDT",
    });
    expect(result.success).toBe(false);
    expect(result.error).toContain("Payout not supported");
  });

  it("sends correct payload for exactOut", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      status: 201,
      json: async () => ({ id: "test-uuid", status: "payment_unpaid" }),
    });

    const result = await createPayment(validParams);
    expect(result.success).toBe(true);
    expect(result.payment).toEqual({ id: "test-uuid", status: "payment_unpaid" });

    const call = mockFetch.mock.calls[0];
    expect(call[0]).toBe("https://intentapiv4.rozo.ai/functions/v1/payment-api");

    const body = JSON.parse(call[1].body);
    expect(body.appId).toBe("rozoAgent");
    expect(body.type).toBe("exactOut");
    expect(body.source.chainId).toBe(8453);
    expect(body.source.tokenSymbol).toBe("USDC");
    expect(body.destination.amount).toBe("10.00");
    expect(body.destination.receiverAddress).toBe(TEST_EVM_ADDRESS_2);
    expect(body.source.amount).toBeUndefined();
  });

  it("sends correct payload for exactIn", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      status: 201,
      json: async () => ({ id: "test-uuid-2" }),
    });

    await createPayment({
      ...validParams,
      type: "exactIn",
      sourceAmount: "11.00",
    });

    const body = JSON.parse(mockFetch.mock.calls[0][1].body);
    expect(body.type).toBe("exactIn");
    expect(body.source.amount).toBe("11.00");
    expect(body.destination.amount).toBeUndefined();
  });

  it("includes memo for Stellar C-wallet", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      status: 201,
      json: async () => ({ id: "stellar-uuid" }),
    });

    await createPayment({
      ...validParams,
      destChain: 1500,
      destToken: "USDC",
      destAddress: TEST_STELLAR_G_ADDRESS,
      destMemo: "contract-memo-123",
    });

    const body = JSON.parse(mockFetch.mock.calls[0][1].body);
    expect(body.destination.receiverMemo).toBe("contract-memo-123");
  });

  it("does not include memo when not provided", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      status: 201,
      json: async () => ({ id: "no-memo-uuid" }),
    });

    await createPayment(validParams);

    const body = JSON.parse(mockFetch.mock.calls[0][1].body);
    expect(body.destination.receiverMemo).toBeUndefined();
  });

  it("generates orderId if not provided", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      status: 201,
      json: async () => ({ id: "uuid" }),
    });

    await createPayment(validParams);

    const body = JSON.parse(mockFetch.mock.calls[0][1].body);
    expect(body.orderId).toBeDefined();
    expect(body.orderId.length).toBeGreaterThan(0);
  });

  it("uses provided orderId", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      status: 201,
      json: async () => ({ id: "uuid" }),
    });

    await createPayment({ ...validParams, orderId: "my-order-123" });

    const body = JSON.parse(mockFetch.mock.calls[0][1].body);
    expect(body.orderId).toBe("my-order-123");
  });

  it("handles API error response", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: false,
      status: 400,
      json: async () => ({ error: { code: "INVALID", message: "Bad request" } }),
    });

    const result = await createPayment(validParams);
    expect(result.success).toBe(false);
    expect(result.statusCode).toBe(400);
  });

  it("handles 409 conflict", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: false,
      status: 409,
      json: async () => ({ error: { code: "CONFLICT", message: "Duplicate orderId" } }),
    });

    const result = await createPayment({ ...validParams, orderId: "dup-id" });
    expect(result.success).toBe(false);
    expect(result.statusCode).toBe(409);
  });

  it("allows BSC USDT payout", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      status: 201,
      json: async () => ({ id: "bsc-uuid" }),
    });

    const result = await createPayment({
      sourceChain: 56,
      sourceToken: "USDT",
      destChain: 56,
      destAddress: TEST_EVM_ADDRESS_2,
      destToken: "USDT",
      destAmount: "50.00",
    });

    expect(result.success).toBe(true);
    const body = JSON.parse(mockFetch.mock.calls[0][1].body);
    expect(body.source.tokenSymbol).toBe("USDT");
    expect(body.destination.tokenSymbol).toBe("USDT");
  });

  it("handles network error (fetch throws)", async () => {
    mockFetch.mockRejectedValueOnce(new Error("ECONNREFUSED"));
    const result = await createPayment(validParams);
    expect(result.success).toBe(false);
    expect(result.error).toContain("Network error");
  });

  it("handles non-JSON response", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      status: 201,
      json: async () => { throw new SyntaxError("Unexpected token"); },
    });
    const result = await createPayment(validParams);
    expect(result.success).toBe(false);
    expect(result.error).toContain("Invalid JSON");
  });
});

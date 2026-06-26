import { describe, it, expect, vi, beforeEach } from "vitest";
import { getPayment, checkPaymentByTxHash, checkPaymentByAddressMemo } from "../src/get-payment.js";

const mockFetch = vi.fn();
vi.stubGlobal("fetch", mockFetch);

beforeEach(() => {
  mockFetch.mockReset();
});

describe("getPayment", () => {
  it("returns payment on success", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      status: 200,
      json: async () => ({
        id: "550e8400-e29b-41d4-a716-446655440000",
        status: "payment_completed",
        type: "exactOut",
      }),
    });

    const result = await getPayment("550e8400-e29b-41d4-a716-446655440000");
    expect(result.success).toBe(true);
    expect(result.payment?.status).toBe("payment_completed");
    expect(mockFetch).toHaveBeenCalledWith(
      "https://intentapiv4.rozo.ai/functions/v1/payment-api/payments/550e8400-e29b-41d4-a716-446655440000"
    );
  });

  it("handles 404 not found", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: false,
      status: 404,
      json: async () => ({ error: { code: "NOT_FOUND", message: "Payment not found" } }),
    });

    const result = await getPayment("nonexistent-id");
    expect(result.success).toBe(false);
    expect(result.statusCode).toBe(404);
  });

  it("returns all payment statuses correctly", async () => {
    const statuses = [
      "payment_unpaid",
      "payment_started",
      "payment_payin_completed",
      "payment_payout_completed",
      "payment_completed",
      "payment_bounced",
      "payment_expired",
      "payment_refunded",
    ];

    for (const status of statuses) {
      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => ({ id: "test", status }),
      });

      const result = await getPayment("test");
      expect(result.success).toBe(true);
      expect(result.payment?.status).toBe(status);
    }
  });

  it("handles network error (fetch throws)", async () => {
    mockFetch.mockRejectedValueOnce(new Error("ENOTFOUND"));
    const result = await getPayment("some-id");
    expect(result.success).toBe(false);
    expect(result.error).toContain("Network error");
  });

  it("handles non-JSON response", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      status: 200,
      json: async () => { throw new SyntaxError("Unexpected token"); },
    });
    const result = await getPayment("some-id");
    expect(result.success).toBe(false);
    expect(result.error).toContain("Invalid JSON");
  });
});

describe("checkPaymentByTxHash", () => {
  it("looks up by Stellar tx hash", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      status: 200,
      json: async () => ({ id: "found-by-hash", status: "payment_completed" }),
    });

    const result = await checkPaymentByTxHash("817089164daae43566dade1f7e83028430308a96662a556f1abcb131b10bbe59");
    expect(result.success).toBe(true);
    expect(result.payment?.id).toBe("found-by-hash");
    expect(mockFetch).toHaveBeenCalledWith(
      expect.stringContaining("/payments/check?txHash=817089164daae43566dade1f7e83028430308a96662a556f1abcb131b10bbe59")
    );
  });

  it("looks up by EVM tx hash", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      status: 200,
      json: async () => ({ id: "evm-hash-result", status: "payment_payin_completed" }),
    });

    const result = await checkPaymentByTxHash("0x767f62ca11fe708e7d1267f7f89f6e4b84e347e1aba29a8b855bbbbec9d645e3");
    expect(result.success).toBe(true);
    expect(result.payment?.status).toBe("payment_payin_completed");
  });

  it("returns 404 when no match in last 7 days", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: false,
      status: 404,
      json: async () => ({ error: { code: "paymentNotFound" } }),
    });

    const result = await checkPaymentByTxHash("0xnonexistent");
    expect(result.success).toBe(false);
    expect(result.statusCode).toBe(404);
  });

  it("handles network error", async () => {
    mockFetch.mockRejectedValueOnce(new Error("ECONNREFUSED"));
    const result = await checkPaymentByTxHash("0xabc");
    expect(result.success).toBe(false);
    expect(result.error).toContain("Network error");
  });
});

describe("checkPaymentByAddressMemo", () => {
  it("looks up by Stellar address + memo", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      status: 200,
      json: async () => ({ id: "found-by-memo", status: "payment_completed" }),
    });

    const result = await checkPaymentByAddressMemo(
      "GB4CLV3UMXDPFP5OQJQKUCWPRJXPXPJSHTUKZEJLAIZFZR7UHYAQ6EB4",
      "83589538"
    );
    expect(result.success).toBe(true);
    expect(result.payment?.id).toBe("found-by-memo");
    expect(mockFetch).toHaveBeenCalledWith(
      expect.stringContaining("receiverAddress=GB4CLV3UMXDPFP5OQJQKUCWPRJXPXPJSHTUKZEJLAIZFZR7UHYAQ6EB4")
    );
    expect(mockFetch).toHaveBeenCalledWith(
      expect.stringContaining("receiverMemo=83589538")
    );
  });

  it("looks up by Solana address + memo", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      status: 200,
      json: async () => ({ id: "solana-memo-result", status: "payment_started" }),
    });

    const result = await checkPaymentByAddressMemo(
      "a23F2uanwzTDtWJmPK1y1DiKbnR7vCNZTqdQEacRz8W",
      "68253860"
    );
    expect(result.success).toBe(true);
  });

  it("returns 404 when no match", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: false,
      status: 404,
      json: async () => ({ error: { code: "paymentNotFound" } }),
    });

    const result = await checkPaymentByAddressMemo("GB4CLV3U...", "99999999");
    expect(result.success).toBe(false);
    expect(result.statusCode).toBe(404);
  });

  it("handles network error", async () => {
    mockFetch.mockRejectedValueOnce(new Error("ETIMEDOUT"));
    const result = await checkPaymentByAddressMemo("addr", "memo");
    expect(result.success).toBe(false);
    expect(result.error).toContain("Network error");
  });
});

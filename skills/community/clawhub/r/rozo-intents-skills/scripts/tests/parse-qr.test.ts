import { describe, it, expect } from "vitest";
import { parseQR } from "../src/parse-qr.js";
import {
  TEST_EVM_ADDRESS,
  TEST_EVM_ADDRESS_2,
  TEST_SOLANA_ADDRESS_2,
  TEST_STELLAR_G_ADDRESS,
  TEST_STELLAR_C_ADDRESS,
} from "./fixtures.js";

describe("parseQR", () => {
  // --- Plain addresses ---
  describe("plain addresses", () => {
    it("parses EVM address", () => {
      const r = parseQR(TEST_EVM_ADDRESS);
      expect(r).not.toBeNull();
      expect(r!.type).toBe("plain-address");
      expect(r!.address).toBe(TEST_EVM_ADDRESS);
      expect(r!.chainId).toBeUndefined();
    });

    it("parses Solana address", () => {
      const r = parseQR(TEST_SOLANA_ADDRESS_2);
      expect(r!.type).toBe("plain-address");
      expect(r!.chainId).toBe(900);
    });

    it("parses Stellar G-wallet", () => {
      const r = parseQR(TEST_STELLAR_G_ADDRESS);
      expect(r!.type).toBe("plain-address");
      expect(r!.chainId).toBe(1500);
    });

    it("parses Stellar C-wallet", () => {
      const r = parseQR(TEST_STELLAR_C_ADDRESS);
      expect(r!.type).toBe("plain-address");
      expect(r!.chainId).toBe(1500);
    });

    it("returns null for invalid content", () => {
      expect(parseQR("hello world")).toBeNull();
      expect(parseQR("0xinvalid")).toBeNull();
    });
  });

  // --- EIP-681 ---
  describe("EIP-681", () => {
    it("parses simple address", () => {
      const r = parseQR(`ethereum:${TEST_EVM_ADDRESS_2}`);
      expect(r!.type).toBe("eip681");
      expect(r!.address).toBe(TEST_EVM_ADDRESS_2);
      expect(r!.chainId).toBeUndefined();
    });

    it("parses with value (native ETH transfer)", () => {
      const r = parseQR(`ethereum:${TEST_EVM_ADDRESS_2}?value=1e18`);
      expect(r!.type).toBe("eip681");
      expect(r!.amount).toBe("1e18");
    });

    it("parses with chain ID", () => {
      const r = parseQR(`ethereum:${TEST_EVM_ADDRESS_2}@1?value=1.5e18`);
      expect(r!.chainId).toBe(1);
      expect(r!.amount).toBe("1.5e18");
    });

    it("parses ERC-20 transfer with known USDC contract (Base)", () => {
      const r = parseQR(
        `ethereum:0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913/transfer?address=${TEST_EVM_ADDRESS}&uint256=1000000`
      );
      expect(r!.type).toBe("eip681");
      expect(r!.address).toBe(TEST_EVM_ADDRESS);
      expect(r!.token).toBe("USDC");
      expect(r!.tokenAddress).toBe("0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913");
      expect(r!.chainId).toBe(8453);
      expect(r!.amount).toBe("1000000");
    });

    it("parses ERC-20 transfer with explicit chain ID override", () => {
      const r = parseQR(
        `ethereum:0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913@8453/transfer?address=${TEST_EVM_ADDRESS}&uint256=5000000`
      );
      expect(r!.chainId).toBe(8453);
      expect(r!.token).toBe("USDC");
      expect(r!.amount).toBe("5000000");
    });

    it("parses ERC-20 transfer with known USDT contract (Ethereum)", () => {
      const r = parseQR(
        `ethereum:0xdAC17F958D2ee523a2206206994597C13D831ec7/transfer?address=${TEST_EVM_ADDRESS_2}&uint256=50000000`
      );
      expect(r!.token).toBe("USDT");
      expect(r!.chainId).toBe(1);
    });

    it("parses ERC-20 with unknown token contract", () => {
      const r = parseQR(
        `ethereum:0x6B175474E89094C44Da98b954EedeAC495271d0F@10/transfer?address=${TEST_EVM_ADDRESS_2}&uint256=42`
      );
      expect(r!.type).toBe("eip681");
      expect(r!.token).toBeUndefined();
      expect(r!.chainId).toBe(10);
      expect(r!.tokenAddress).toBe("0x6B175474E89094C44Da98b954EedeAC495271d0F");
    });
  });

  // --- Solana Pay ---
  describe("Solana Pay", () => {
    it("parses plain solana URI", () => {
      const r = parseQR(`solana:${TEST_SOLANA_ADDRESS_2}`);
      expect(r!.type).toBe("solana-pay");
      expect(r!.address).toBe(TEST_SOLANA_ADDRESS_2);
      expect(r!.chainId).toBe(900);
    });

    it("parses with amount (SOL transfer)", () => {
      const r = parseQR(`solana:${TEST_SOLANA_ADDRESS_2}?amount=2.5`);
      expect(r!.amount).toBe("2.5");
    });

    it("parses SPL token transfer with known USDC mint", () => {
      const r = parseQR(
        `solana:${TEST_SOLANA_ADDRESS_2}?amount=10.25&spl-token=EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v`
      );
      expect(r!.token).toBe("USDC");
      expect(r!.amount).toBe("10.25");
      expect(r!.tokenAddress).toBe("EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v");
    });

    it("parses SPL token transfer with known USDT mint", () => {
      const r = parseQR(
        `solana:${TEST_SOLANA_ADDRESS_2}?amount=5&spl-token=Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB`
      );
      expect(r!.token).toBe("USDT");
    });

    it("parses with label, message, and memo", () => {
      const r = parseQR(
        `solana:${TEST_SOLANA_ADDRESS_2}?amount=5&label=Charity&message=Donation&memo=ThankYou`
      );
      expect(r!.amount).toBe("5");
      expect(r!.label).toBe("Charity");
      expect(r!.message).toBe("Donation");
      expect(r!.memo).toBe("ThankYou");
    });

    it("parses with unknown SPL token", () => {
      const r = parseQR(
        `solana:${TEST_SOLANA_ADDRESS_2}?amount=1&spl-token=UnknownMintAddress1234567890ABCDEF12345678`
      );
      expect(r!.token).toBeUndefined();
      expect(r!.tokenAddress).toBe("UnknownMintAddress1234567890ABCDEF12345678");
    });
  });

  // --- Stellar URI ---
  describe("Stellar URI", () => {
    it("parses basic pay request", () => {
      const r = parseQR(
        `web+stellar:pay?destination=${TEST_STELLAR_G_ADDRESS}&amount=100&asset_code=USDC`
      );
      expect(r!.type).toBe("stellar-uri");
      expect(r!.address).toBe(TEST_STELLAR_G_ADDRESS);
      expect(r!.chainId).toBe(1500);
      expect(r!.token).toBe("USDC");
      expect(r!.amount).toBe("100");
    });

    it("parses with memo", () => {
      const r = parseQR(
        `web+stellar:pay?destination=${TEST_STELLAR_G_ADDRESS}&amount=50&asset_code=USDC&memo=invoice-123`
      );
      expect(r!.memo).toBe("invoice-123");
    });

    it("parses without asset_code (native XLM)", () => {
      const r = parseQR(
        `web+stellar:pay?destination=${TEST_STELLAR_G_ADDRESS}&amount=10`
      );
      expect(r!.token).toBeUndefined();
      expect(r!.amount).toBe("10");
    });

    it("returns null for missing destination", () => {
      const r = parseQR("web+stellar:pay?amount=10&asset_code=USDC");
      expect(r).toBeNull();
    });
  });

  // --- Edge cases ---
  describe("edge cases", () => {
    it("handles whitespace around content", () => {
      const r = parseQR(`  ${TEST_EVM_ADDRESS}  `);
      expect(r).not.toBeNull();
      expect(r!.type).toBe("plain-address");
    });

    it("returns null for empty string", () => {
      expect(parseQR("")).toBeNull();
    });
  });
});

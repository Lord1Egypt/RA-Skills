/**
 * pay command — Make an x402r escrow payment to a merchant
 *
 * 1. GET <url> → 402 with PAYMENT-REQUIRED header
 * 2. Sign escrow authorization locally using @x402r/evm scheme
 * 3. Retry with PAYMENT-SIGNATURE header → merchant's facilitator verifies + settles → 200
 * 4. Extract PaymentInfo from escrow payload via toPaymentInfo()
 * 5. Save to ~/.x402r/last-payment.json for later dispute
 * 6. Print response body
 */
import type { Command } from "commander";
export declare function registerPayCommand(program: Command): void;

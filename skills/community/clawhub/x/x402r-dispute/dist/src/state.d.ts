/**
 * State persistence — saves payment and dispute state to ~/.x402r/
 * Ported from x402r-sdk/examples/dev-tools/shared/state.ts with dispute state added.
 */
import type { PaymentInfo } from "@x402r/core";
export interface PaymentState {
    paymentInfo: PaymentInfo;
    operatorAddress: string;
    paymentHash: string;
    timestamp: string;
    networkId: string;
    merchantPrivateKey?: string;
}
export declare function savePaymentState(state: PaymentState): void;
export declare function loadPaymentState(): PaymentState | null;
/**
 * Get PaymentInfo from CLI options or state file.
 */
export declare function getPaymentInfo(options: {
    paymentJson?: string;
}): PaymentInfo;
export interface DisputeState {
    nonce: string;
    compositeKey?: string;
    refundTxHash?: string;
    evidenceTxHash?: string;
    evidenceCid?: string;
    arbiterResponse?: Record<string, unknown>;
    timestamp: string;
}
export declare function saveDisputeState(state: DisputeState): void;
export declare function loadDisputeState(): DisputeState | null;
/**
 * Get nonce from CLI options or dispute state.
 */
export declare function getNonce(options: {
    nonce?: string;
    id?: string;
}): bigint;
/**
 * Get composite key from CLI options or dispute state.
 */
export declare function getCompositeKey(options: {
    id?: string;
}): string | undefined;

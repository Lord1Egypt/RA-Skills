/**
 * State persistence — saves payment and dispute state to ~/.x402r/
 * Ported from x402r-sdk/examples/dev-tools/shared/state.ts with dispute state added.
 */
import * as fs from "fs";
import * as path from "path";
import * as os from "os";
import { parsePaymentInfo as coreParsePaymentInfo } from "@x402r/core";
const STATE_DIR = path.join(os.homedir(), ".x402r");
const PAYMENT_STATE_FILE = path.join(STATE_DIR, "last-payment.json");
const DISPUTE_STATE_FILE = path.join(STATE_DIR, "last-dispute.json");
function ensureDir() {
    if (!fs.existsSync(STATE_DIR)) {
        fs.mkdirSync(STATE_DIR, { recursive: true });
    }
}
export function savePaymentState(state) {
    ensureDir();
    const serializable = {
        ...state,
        paymentInfo: {
            ...state.paymentInfo,
            maxAmount: state.paymentInfo.maxAmount.toString(),
            preApprovalExpiry: state.paymentInfo.preApprovalExpiry.toString(),
            authorizationExpiry: state.paymentInfo.authorizationExpiry.toString(),
            refundExpiry: state.paymentInfo.refundExpiry.toString(),
            salt: state.paymentInfo.salt.toString(),
        },
    };
    fs.writeFileSync(PAYMENT_STATE_FILE, JSON.stringify(serializable, null, 2));
}
export function loadPaymentState() {
    if (!fs.existsSync(PAYMENT_STATE_FILE)) {
        return null;
    }
    try {
        const raw = JSON.parse(fs.readFileSync(PAYMENT_STATE_FILE, "utf-8"));
        return {
            ...raw,
            paymentInfo: {
                ...raw.paymentInfo,
                maxAmount: BigInt(raw.paymentInfo.maxAmount),
                preApprovalExpiry: BigInt(raw.paymentInfo.preApprovalExpiry),
                authorizationExpiry: BigInt(raw.paymentInfo.authorizationExpiry),
                refundExpiry: BigInt(raw.paymentInfo.refundExpiry),
                salt: BigInt(raw.paymentInfo.salt),
            },
        };
    }
    catch {
        return null;
    }
}
/**
 * Get PaymentInfo from CLI options or state file.
 */
export function getPaymentInfo(options) {
    if (options.paymentJson) {
        try {
            return coreParsePaymentInfo(options.paymentJson);
        }
        catch {
            console.error("Error: Invalid payment JSON");
            process.exit(1);
        }
    }
    const state = loadPaymentState();
    if (state) {
        console.log(`  (Using saved payment from ${state.timestamp})`);
        return state.paymentInfo;
    }
    console.error("Error: No payment state found. Make a payment first or provide --payment-json.");
    process.exit(1);
}
export function saveDisputeState(state) {
    ensureDir();
    fs.writeFileSync(DISPUTE_STATE_FILE, JSON.stringify(state, null, 2));
}
export function loadDisputeState() {
    if (!fs.existsSync(DISPUTE_STATE_FILE)) {
        return null;
    }
    try {
        return JSON.parse(fs.readFileSync(DISPUTE_STATE_FILE, "utf-8"));
    }
    catch {
        return null;
    }
}
/**
 * Get nonce from CLI options or dispute state.
 */
export function getNonce(options) {
    if (options.nonce !== undefined) {
        return BigInt(options.nonce);
    }
    const state = loadDisputeState();
    if (state) {
        console.log(`  (Using saved dispute nonce: ${state.nonce})`);
        return BigInt(state.nonce);
    }
    return 0n;
}
/**
 * Get composite key from CLI options or dispute state.
 */
export function getCompositeKey(options) {
    if (options.id)
        return options.id;
    const state = loadDisputeState();
    return state?.compositeKey;
}
//# sourceMappingURL=state.js.map
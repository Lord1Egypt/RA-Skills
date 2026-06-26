const API_BASE = "https://intentapiv4.rozo.ai/functions/v1/payment-api";
/**
 * Get payment by payment ID.
 */
export async function getPayment(paymentId) {
    return fetchPayment(`${API_BASE}/payments/${paymentId}`);
}
/**
 * Check payment by source transaction hash.
 * Looks back 7 days, returns the most recent matching payment.
 */
export async function checkPaymentByTxHash(txHash) {
    return fetchPayment(`${API_BASE}/payments/check?txHash=${encodeURIComponent(txHash)}`);
}
/**
 * Check payment by deposit address + memo.
 * Looks back 7 days, returns the most recent matching payment.
 */
export async function checkPaymentByAddressMemo(receiverAddress, receiverMemo) {
    const params = new URLSearchParams({ receiverAddress, receiverMemo });
    return fetchPayment(`${API_BASE}/payments/check?${params}`);
}
async function fetchPayment(url) {
    let response;
    try {
        response = await fetch(url);
    }
    catch (err) {
        return { success: false, error: `Network error: ${err.message}` };
    }
    let body;
    try {
        body = await response.json();
    }
    catch {
        return { success: false, statusCode: response.status, error: "Invalid JSON response from Rozo API" };
    }
    if (!response.ok) {
        return { success: false, statusCode: response.status, error: body };
    }
    return { success: true, payment: body };
}
// CLI entry point
if (import.meta.url === `file://${process.argv[1]}`) {
    const args = process.argv.slice(2);
    const get = (flag) => {
        const idx = args.indexOf(flag);
        return idx !== -1 ? args[idx + 1] : undefined;
    };
    const paymentId = get("--payment-id");
    const txHash = get("--tx-hash");
    const receiverAddress = get("--receiver-address");
    const receiverMemo = get("--receiver-memo");
    let result;
    if (paymentId) {
        result = await getPayment(paymentId);
    }
    else if (txHash) {
        result = await checkPaymentByTxHash(txHash);
    }
    else if (receiverAddress && receiverMemo) {
        result = await checkPaymentByAddressMemo(receiverAddress, receiverMemo);
    }
    else {
        console.error("Usage: --payment-id <uuid> | --tx-hash <hash> | --receiver-address <addr> --receiver-memo <memo>");
        process.exit(1);
    }
    console.log(JSON.stringify(result, null, 2));
    if (!result.success)
        process.exit(1);
}

/**
 * Check if a Stellar G-wallet has a trustline for a given asset via the Horizon API.
 * Supports USDC (default) and EURC.
 */
const HORIZON_URL = "https://horizon.stellar.org";
const ASSET_ISSUERS = {
    USDC: "GA5ZSEJYB37JRC5AVCIA5MOP4RHTM335X2KGX3IHOJAPP5RE34K4KZVN",
    EURC: "GDHU6WRG4IEQXM5NZ4BMPKOXHW76MZM4Y2IEMFDVXBSDP6SJY4ITNPP2",
};
export async function checkStellarTrustline(address, asset = "USDC") {
    if (!address.startsWith("G") || address.length !== 56) {
        return { address, asset, hasTrustline: false, error: "Not a valid Stellar G-wallet address" };
    }
    const issuer = ASSET_ISSUERS[asset];
    if (!issuer) {
        return { address, asset, hasTrustline: false, error: `Unsupported asset: ${asset}` };
    }
    let response;
    try {
        response = await fetch(`${HORIZON_URL}/accounts/${address}`);
    }
    catch (err) {
        return { address, asset, hasTrustline: false, error: `Network error: ${err.message}` };
    }
    if (!response.ok) {
        if (response.status === 404) {
            return { address, asset, hasTrustline: false, error: "Account not found on Stellar network" };
        }
        return { address, asset, hasTrustline: false, error: `Horizon API error: ${response.status}` };
    }
    let account;
    try {
        account = await response.json();
    }
    catch {
        return { address, asset, hasTrustline: false, error: "Invalid JSON response from Horizon API" };
    }
    const found = account.balances.find((b) => b.asset_code === asset && b.asset_issuer === issuer);
    if (found) {
        return { address, asset, hasTrustline: true, balance: found.balance };
    }
    return { address, asset, hasTrustline: false };
}
// CLI entry point
if (import.meta.url === `file://${process.argv[1]}`) {
    const args = process.argv.slice(2);
    const addrIdx = args.indexOf("--address");
    const assetIdx = args.indexOf("--asset");
    if (addrIdx === -1) {
        console.error("Usage: --address <stellar_g_wallet> [--asset <USDC|EURC>]");
        process.exit(1);
    }
    const asset = assetIdx !== -1 ? args[assetIdx + 1] : "USDC";
    const result = await checkStellarTrustline(args[addrIdx + 1], asset);
    console.log(JSON.stringify(result, null, 2));
    if (!result.hasTrustline)
        process.exit(1);
}

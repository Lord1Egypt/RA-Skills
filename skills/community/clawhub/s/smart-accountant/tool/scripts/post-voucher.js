const fs = require('fs');
const engine = require('../lib/posting-engine');
const gstEngine = require('../lib/gst-engine');
const db = require('../lib/db');

function main() {
    const payloadPath = process.argv[2];
    if (!payloadPath) {
        console.error("Usage: node post-voucher.js <payload.json>");
        process.exit(1);
    }
    const payload = JSON.parse(fs.readFileSync(payloadPath, 'utf8'));
    
    if (payload.voucher.status !== 'CONFIRMED' && payload.voucher.status !== 'POSTED') {
        console.error("Maker-Checker Rule Enforced: Voucher must be CONFIRMED before posting.");
        process.exit(1);
    }

    // Secondary GST checks at post time to ensure no bypassing
    const partyLine = payload.lines[0];
    const partyLedger = db.prepare("SELECT * FROM ledgers WHERE id = ?").get(partyLine?.ledger_id);
    const companyStateConfig = db.prepare("SELECT value FROM config WHERE key = 'owner_state_code'").get();
    const companyState = companyStateConfig ? companyStateConfig.value : 'Gujarat';

    const flags = gstEngine.runMissedGSTRules(payload.voucher, payload.lines, partyLedger, companyState);
    if (flags.hardStops.length > 0) {
        console.error(`GST Hard Stop Execution Blocked: ${flags.hardStops.join(' | ')}`);
        process.exit(1);
    }

    try {
        const id = engine.postVoucher(payload.voucher, payload.lines);
        console.log(`Successfully posted voucher ID: ${id}`);
    } catch (e) {
        console.error("Posting failed:", e.message);
        process.exit(1);
    }
}

if (require.main === module) {
    main();
}

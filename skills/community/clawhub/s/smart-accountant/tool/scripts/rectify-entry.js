const fs = require('fs');
const engine = require('../lib/posting-engine');
const { reverseVoucher } = require('./reverse-voucher');

function main() {
    const voucherNo = process.argv[2];
    const newPayloadPath = process.argv[3];
    
    if (!voucherNo || !newPayloadPath) {
        console.error("Usage: node rectify-entry.js <original_voucher_no> <new_payload.json>");
        process.exit(1);
    }
    
    // 1. Reverse the original
    const revId = reverseVoucher(voucherNo);
    console.log(`Reversed original voucher. Reversal ID: ${revId}`);
    
    // 2. Post the new entry
    const payload = JSON.parse(fs.readFileSync(newPayloadPath, 'utf8'));
    payload.voucher.status = 'POSTED'; // Force post for rectification
    
    try {
        const id = engine.postVoucher(payload.voucher, payload.lines);
        console.log(`Successfully posted corrected voucher ID: ${id}`);
    } catch (e) {
        console.error("Correction failed:", e.message);
        process.exit(1);
    }
}

if (require.main === module) {
    main();
}

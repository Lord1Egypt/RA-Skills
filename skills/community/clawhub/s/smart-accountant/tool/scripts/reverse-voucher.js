const db = require('../lib/db');
const engine = require('../lib/posting-engine');

function reverseVoucher(voucherNo) {
    const voucher = db.prepare("SELECT * FROM vouchers WHERE voucher_no = ?").get(voucherNo);
    if (!voucher) throw new Error("Voucher not found");
    
    const lines = db.prepare("SELECT * FROM lines WHERE voucher_id = ?").all(voucher.id);
    
    const reversedLines = lines.map(line => ({
        ledger_id: line.ledger_id,
        debit: line.credit, // swap
        credit: line.debit
    }));

    const reversedVoucher = {
        ...voucher,
        id: undefined, // let it auto-increment
        voucher_no: null, // generate new
        status: 'POSTED',
        narration: `Reversal of ${voucher.voucher_no}: ${voucher.narration || ''}`
    };

    return engine.postVoucher(reversedVoucher, reversedLines);
}

function main() {
    const voucherNo = process.argv[2];
    if (!voucherNo) {
        console.error("Usage: node reverse-voucher.js <voucher_no>");
        process.exit(1);
    }

    try {
        const id = reverseVoucher(voucherNo);
        console.log(`Successfully reversed. Reversal Voucher ID: ${id}`);
    } catch (e) {
        console.error("Reversal failed:", e.message);
        process.exit(1);
    }
}

if (require.main === module) {
    main();
}

module.exports = { reverseVoucher };

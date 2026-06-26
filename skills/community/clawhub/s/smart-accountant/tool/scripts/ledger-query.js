const db = require('../lib/db');

function main() {
    const ledgerName = process.argv[2];
    if (!ledgerName) {
        console.error("Usage: node ledger-query.js <ledger_name>");
        process.exit(1);
    }
    
    const ledger = db.prepare("SELECT * FROM ledgers WHERE name = ?").get(ledgerName);
    if (!ledger) {
        console.error(`Ledger ${ledgerName} not found.`);
        process.exit(1);
    }
    
    const lines = db.prepare(`
        SELECT v.date, v.voucher_no, v.narration, l.debit, l.credit
        FROM lines l
        JOIN vouchers v ON l.voucher_id = v.id
        WHERE l.ledger_id = ? AND v.status = 'POSTED'
        ORDER BY v.date ASC, v.id ASC
    `).all();
    
    console.log(`=== LEDGER: ${ledgerName} ===`);
    lines.forEach(l => {
        console.log(`${l.date} | ${l.voucher_no.padEnd(10)} | Dr: ${l.debit || 0} | Cr: ${l.credit || 0} | ${l.narration || ''}`);
    });
}

if (require.main === module) {
    main();
}

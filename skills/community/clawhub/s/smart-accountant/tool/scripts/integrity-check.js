const db = require('../lib/db');

function main() {
    console.log("Running SQLite PRAGMA checks...");
    const integrity = db.prepare("PRAGMA integrity_check").all();
    console.log("Integrity Check:", integrity);
    
    const fks = db.prepare("PRAGMA foreign_key_check").all();
    if (fks.length > 0) {
        console.error("Foreign Key Check Failed:", fks);
    } else {
        console.log("Foreign Key Check: OK");
    }
    
    console.log("\nChecking for unbalanced vouchers...");
    const unbalanced = db.prepare(`
        SELECT v.id, v.voucher_no, SUM(l.debit) as d, SUM(l.credit) as c 
        FROM vouchers v 
        JOIN lines l ON v.id = l.voucher_id 
        GROUP BY v.id 
        HAVING ABS(SUM(l.debit) - SUM(l.credit)) > 0.001
    `).all();
    
    if (unbalanced.length > 0) {
        console.error("Found unbalanced vouchers:", unbalanced);
    } else {
        console.log("All vouchers are balanced.");
    }
}

if (require.main === module) {
    main();
}

const db = require('../lib/db');

function generateTrialBalance() {
    // A query that sums all debits and credits per ledger
    const rows = db.prepare(`
        SELECT 
            l.name,
            l.type,
            SUM(li.debit) as total_debit,
            SUM(li.credit) as total_credit,
            (SUM(li.debit) - SUM(li.credit)) as net_balance
        FROM ledgers l
        JOIN lines li ON l.id = li.ledger_id
        JOIN vouchers v ON li.voucher_id = v.id
        WHERE v.status = 'POSTED'
        GROUP BY l.id
    `).all();

    console.log("=== TRIAL BALANCE ===");
    let totalDr = 0, totalCr = 0;
    
    rows.forEach(r => {
        const bal = r.net_balance;
        const dispDr = bal > 0 ? bal : 0;
        const dispCr = bal < 0 ? Math.abs(bal) : 0;
        
        console.log(`${r.name.padEnd(20)} | Dr: ${dispDr.toString().padStart(10)} | Cr: ${dispCr.toString().padStart(10)}`);
        
        totalDr += dispDr;
        totalCr += dispCr;
    });

    console.log("-------------------------------------------------");
    console.log(`TOTAL                | Dr: ${totalDr.toString().padStart(10)} | Cr: ${totalCr.toString().padStart(10)}`);
}

function main() {
    const type = process.argv[2] || 'trial-balance';
    
    if (type === 'trial-balance') {
        generateTrialBalance();
    } else {
        console.log(`Report type ${type} not fully implemented yet.`);
    }
}

if (require.main === module) {
    main();
}

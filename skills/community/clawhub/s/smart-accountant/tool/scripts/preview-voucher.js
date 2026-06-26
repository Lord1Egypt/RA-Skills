const fs = require('fs');
const validators = require('../lib/validators');
const gstEngine = require('../lib/gst-engine');
const db = require('../lib/db');

function main() {
    const payloadPath = process.argv[2];
    if (!payloadPath) {
        console.error("Usage: node preview-voucher.js <payload.json>");
        process.exit(1);
    }
    const payload = JSON.parse(fs.readFileSync(payloadPath, 'utf8'));

    console.log("=== PREVIEW VOUCHER ===");
    console.log(`Type: ${payload.voucher.type}`);
    console.log(`Amount: ${payload.voucher.amount}`);
    
    const partyLine = payload.lines[0]; // Assuming first line is the party for demo
    const partyLedger = db.prepare("SELECT * FROM ledgers WHERE id = ?").get(partyLine?.ledger_id);
    
    const companyStateConfig = db.prepare("SELECT value FROM config WHERE key = 'owner_state_code'").get();
    const companyState = companyStateConfig ? companyStateConfig.value : 'Gujarat';

    // Auto-generate tax lines if applicable
    if (payload.voucher.tax_rate) {
        const isPurchase = ['PE', 'CP', 'BP'].includes(payload.voucher.type);
        
        const taxLines = gstEngine.determineGST(
            payload.voucher.amount, 
            payload.voucher.tax_rate, 
            partyLedger?.state_code || companyState, 
            companyState, 
            isPurchase
        );
        
        payload.lines = [...payload.lines, ...taxLines];
    }
    
    // Run Missed GST Rules
    const flags = gstEngine.runMissedGSTRules(payload.voucher, payload.lines, partyLedger, companyState);

    try {
        validators.validateCompleteness(payload.voucher, payload.lines);
        validators.validateDoubleEntry(payload.lines);
        validators.validatePeriodOpen(payload.voucher.date);
        
        if (flags.hardStops.length > 0) {
            throw new Error(`GST Hard Stop: ${flags.hardStops.join(' | ')}`);
        }

        console.log("\nProposed Journal Entry:");
        payload.lines.forEach(line => {
            const l = db.prepare("SELECT name FROM ledgers WHERE id = ?").get(line.ledger_id);
            const name = l ? l.name : `LedgerID:${line.ledger_id}`;
            console.log(`${name.padEnd(20)} | Dr: ${line.debit || 0} | Cr: ${line.credit || 0}`);
        });

        if (flags.warnings.length > 0) {
            console.log("\n⚠️ GST Warnings:");
            flags.warnings.forEach(w => console.log(` - ${w}`));
        }

        console.log("\nValidation Passed! This entry is safe to confirm.");
    } catch (e) {
        console.error("\nValidation Failed:", e.message);
        process.exit(1);
    }
}

if (require.main === module) {
    main();
}

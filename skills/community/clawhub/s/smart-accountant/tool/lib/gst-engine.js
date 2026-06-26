const db = require('./db');

function getTaxLedgerId(name) {
    const l = db.prepare("SELECT id FROM ledgers WHERE name = ?").get(name);
    if (!l) {
        // Fallback for demo purposes if tax ledgers aren't seeded yet
        const insert = db.prepare(`
            INSERT INTO ledgers (name, type, normal_balance) 
            VALUES (?, 'Liability', 'Credit')
        `).run(name);
        return insert.lastInsertRowid;
    }
    return l.id;
}

function determineGST(baseAmount, taxRate, partyState, companyState, isPurchase, reverseChargeFlag = false) {
    const taxLines = [];
    if (!taxRate || taxRate === 0) return taxLines;

    const taxAmount = (baseAmount * taxRate) / 100;
    const isInterstate = partyState && companyState && (partyState.toLowerCase() !== companyState.toLowerCase());

    const prefix = isPurchase ? 'Input' : 'Output';
    
    if (isInterstate) {
        taxLines.push({
            ledger_id: getTaxLedgerId(`${prefix} IGST`),
            debit: isPurchase ? taxAmount : 0,
            credit: !isPurchase ? taxAmount : 0,
            _gst_type: 'IGST'
        });
    } else {
        taxLines.push({
            ledger_id: getTaxLedgerId(`${prefix} CGST`),
            debit: isPurchase ? taxAmount / 2 : 0,
            credit: !isPurchase ? taxAmount / 2 : 0,
            _gst_type: 'CGST'
        });
        taxLines.push({
            ledger_id: getTaxLedgerId(`${prefix} SGST`),
            debit: isPurchase ? taxAmount / 2 : 0,
            credit: !isPurchase ? taxAmount / 2 : 0,
            _gst_type: 'SGST'
        });
    }
    
    return taxLines;
}

function runMissedGSTRules(voucherData, linesData, partyLedger, companyState) {
    const flags = {
        warnings: [],
        errors: [],
        hardStops: []
    };

    const hasTaxLines = linesData.some(l => {
        const ledger = db.prepare("SELECT name FROM ledgers WHERE id = ?").get(l.ledger_id);
        return ledger && ledger.name.includes('GST');
    });

    const isPurchase = ['PE', 'CP', 'BP'].includes(voucherData.type);
    const isSales = ['SE', 'CR', 'BR'].includes(voucherData.type);

    // Rule 1: Vendor expense + no GST component
    if (isPurchase && !hasTaxLines && partyLedger && partyLedger.registration_type !== 'unregistered') {
        flags.warnings.push("Possible Missed GST: Vendor expense without GST component.");
    }

    // Rule 2: Taxable sales + no output GST
    if (isSales && !hasTaxLines && voucherData.tax_rate > 0) {
        flags.warnings.push("Output GST Missing: Taxable sales without output GST.");
    }

    // Rule 4 & 5: Wrong tax jurisdiction
    if (partyLedger && partyLedger.state_code && companyState) {
        const isInterstate = partyLedger.state_code.toLowerCase() !== companyState.toLowerCase();
        
        const hasIGST = linesData.some(l => {
            const led = db.prepare("SELECT name FROM ledgers WHERE id = ?").get(l.ledger_id);
            return led && led.name.includes('IGST');
        });
        
        const hasCGST = linesData.some(l => {
            const led = db.prepare("SELECT name FROM ledgers WHERE id = ?").get(l.ledger_id);
            return led && (led.name.includes('CGST') || led.name.includes('SGST'));
        });

        if (isInterstate && hasCGST) {
            flags.hardStops.push("Wrong tax jurisdiction: Interstate transaction using CGST/SGST.");
        }
        if (!isInterstate && hasIGST) {
            flags.hardStops.push("Wrong tax jurisdiction: Intrastate transaction using IGST.");
        }
    }

    // Rule 6: GSTIN absent + party registered
    if (partyLedger && partyLedger.registration_type === 'regular' && !partyLedger.gstin) {
        flags.warnings.push("GST master incomplete: GSTIN absent for registered party.");
    }

    // Rule 7: Manual JE touches GST ledgers
    if (voucherData.type === 'JE' && hasTaxLines && !voucherData._review_flag_passed) {
        flags.warnings.push("Review required: Manual JE touches GST ledgers.");
        flags.hardStops.push("Manual journal directly manipulates GST ledgers without review.");
    }

    // Hard Stop: Absent GST rate for taxable supply
    if (!voucherData.tax_rate && partyLedger && partyLedger.default_supply_type === 'taxable') {
        flags.hardStops.push("GST rate absent for taxable supply.");
    }

    return flags;
}

module.exports = {
    determineGST,
    runMissedGSTRules
};

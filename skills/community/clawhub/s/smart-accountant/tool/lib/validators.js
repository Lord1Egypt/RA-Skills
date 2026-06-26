const db = require('./db');

function validateCompleteness(voucherData, linesData) {
    if (!voucherData.date || !voucherData.amount || !voucherData.type) {
        throw new Error("Missing required voucher fields: date, amount, type");
    }
    if (!linesData || linesData.length < 2) {
        throw new Error("A voucher must have at least two lines.");
    }
    for (let line of linesData) {
        if (!line.ledger_id) {
            throw new Error("All lines must specify a ledger_id");
        }
    }
}

function validateDoubleEntry(linesData) {
    let sumDebit = 0;
    let sumCredit = 0;
    for (let line of linesData) {
        sumDebit += (line.debit || 0);
        sumCredit += (line.credit || 0);
    }
    
    // Using a small epsilon to avoid float math issues
    if (Math.abs(sumDebit - sumCredit) > 0.001) {
        throw new Error(`Unbalanced entry. Total Debits (${sumDebit}) != Total Credits (${sumCredit})`);
    }
}

function validatePeriodOpen(date) {
    const periodStatus = db.prepare("SELECT value FROM config WHERE key = 'period_status'").get();
    if (periodStatus && periodStatus.value === 'CLOSED') {
        throw new Error("Cannot post into a closed period.");
    }
}

function validateDuplicate(voucherData) {
    if (voucherData.request_id) {
        const existing = db.prepare("SELECT id FROM vouchers WHERE request_id = ?").get(voucherData.request_id);
        if (existing) {
            throw new Error(`Duplicate request: voucher with request_id ${voucherData.request_id} already exists.`);
        }
    }
}

module.exports = {
    validateCompleteness,
    validateDoubleEntry,
    validatePeriodOpen,
    validateDuplicate
};

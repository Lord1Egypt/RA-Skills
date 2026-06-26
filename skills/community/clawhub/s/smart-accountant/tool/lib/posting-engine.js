const db = require('./db');
const validators = require('./validators');

// Prepared statements for faster execution
const stmts = {
    insertVoucher: db.prepare(`
        INSERT INTO vouchers (voucher_no, type, date, amount, narration, source_doc_type, source_doc_no, status, request_id)
        VALUES (@voucher_no, @type, @date, @amount, @narration, @source_doc_type, @source_doc_no, @status, @request_id)
    `),
    insertLine: db.prepare(`
        INSERT INTO lines (voucher_id, ledger_id, debit, credit)
        VALUES (@voucher_id, @ledger_id, @debit, @credit)
    `),
    insertAuditLog: db.prepare(`
        INSERT INTO audit_log (event_type, entity_id, before_json, after_json)
        VALUES (@event_type, @entity_id, @before_json, @after_json)
    `)
};

function generateVoucherNo(type) {
    const res = db.prepare("SELECT COUNT(*) as count FROM vouchers WHERE type = ?").get(type);
    const num = res.count + 1;
    return `${type}-${String(num).padStart(4, '0')}`;
}

function postVoucher(voucherData, linesData) {
    // 1. Validation Phase
    validators.validateCompleteness(voucherData, linesData);
    validators.validateDoubleEntry(linesData);
    validators.validatePeriodOpen(voucherData.date);
    validators.validateDuplicate(voucherData);

    // 2. Transaction Phase
    const transaction = db.transaction(() => {
        const voucherNo = voucherData.voucher_no || generateVoucherNo(voucherData.type);
        
        const voucherInsert = stmts.insertVoucher.run({
            voucher_no: voucherNo,
            type: voucherData.type,
            date: voucherData.date,
            amount: voucherData.amount,
            narration: voucherData.narration || null,
            source_doc_type: voucherData.source_doc_type || null,
            source_doc_no: voucherData.source_doc_no || null,
            status: voucherData.status || 'POSTED',
            request_id: voucherData.request_id || null
        });

        const voucherId = voucherInsert.lastInsertRowid;

        for (let line of linesData) {
            stmts.insertLine.run({
                voucher_id: voucherId,
                ledger_id: line.ledger_id,
                debit: line.debit || 0,
                credit: line.credit || 0
            });
        }

        // Audit Log
        stmts.insertAuditLog.run({
            event_type: 'VOUCHER_POSTED',
            entity_id: voucherId,
            before_json: null,
            after_json: JSON.stringify({ voucher: voucherData, lines: linesData })
        });

        return voucherId;
    });

    return transaction();
}

module.exports = {
    generateVoucherNo,
    postVoucher
};

// Simple rules-based NLP interpreter to voucher type.
function inferVoucherType(intentText) {
    const text = intentText.toLowerCase();
    
    // Receipt (Money In)
    if (text.includes("received") && (text.includes("bank") || text.includes("neft") || text.includes("rtgs"))) return 'BR';
    if (text.includes("received") && text.includes("cash")) return 'CR';
    
    // Payment (Money Out)
    if ((text.includes("paid") || text.includes("payment")) && (text.includes("bank") || text.includes("neft") || text.includes("cheque"))) return 'BP';
    if ((text.includes("paid") || text.includes("payment")) && text.includes("cash")) return 'CP';
    
    // Sales
    if (text.includes("sales invoice") || text.includes("sold") || text.includes("bill for customer")) return 'SE';
    if (text.includes("sales return") || text.includes("credit note")) return 'SR';
    
    // Purchases
    if (text.includes("purchase invoice") || text.includes("vendor bill") || text.includes("bought")) return 'PE';
    if (text.includes("purchase return") || text.includes("debit note")) return 'PR';
    
    // Internal Transfers
    if (text.includes("contra") || text.includes("transfer") || text.includes("withdraw")) return 'CN';
    
    // Default fallback
    return 'JE';
}

module.exports = {
    inferVoucherType
};

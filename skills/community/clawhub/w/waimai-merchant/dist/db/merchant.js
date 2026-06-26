"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.createMerchant = createMerchant;
exports.getMerchantById = getMerchantById;
exports.getMerchantByPhone = getMerchantByPhone;
exports.getAllMerchants = getAllMerchants;
exports.getMerchantsByStatus = getMerchantsByStatus;
exports.updateMerchant = updateMerchant;
exports.deleteMerchant = deleteMerchant;
exports.approveMerchant = approveMerchant;
exports.rejectMerchant = rejectMerchant;
exports.suspendMerchant = suspendMerchant;
exports.searchMerchants = searchMerchants;
const database_1 = require("./database");
// 创建商家
function createMerchant(data) {
    const db = (0, database_1.getDatabase)();
    const stmt = db.prepare(`
    INSERT INTO merchants (name, phone, email, address, business_license, contact_person)
    VALUES (@name, @phone, @email, @address, @business_license, @contact_person)
  `);
    const result = stmt.run(data);
    return getMerchantById(Number(result.lastInsertRowid));
}
// 根据ID获取商家
function getMerchantById(id) {
    const db = (0, database_1.getDatabase)();
    return db.prepare('SELECT * FROM merchants WHERE id = ?').get(id);
}
// 根据手机号获取商家
function getMerchantByPhone(phone) {
    const db = (0, database_1.getDatabase)();
    return db.prepare('SELECT * FROM merchants WHERE phone = ?').get(phone);
}
// 获取所有商家
function getAllMerchants() {
    const db = (0, database_1.getDatabase)();
    return db.prepare('SELECT * FROM merchants ORDER BY created_at DESC').all();
}
// 根据状态获取商家
function getMerchantsByStatus(status) {
    const db = (0, database_1.getDatabase)();
    return db.prepare('SELECT * FROM merchants WHERE status = ? ORDER BY created_at DESC').all(status);
}
// 更新商家信息
function updateMerchant(id, data) {
    const db = (0, database_1.getDatabase)();
    const fields = Object.keys(data);
    if (fields.length === 0)
        return getMerchantById(id);
    const setClause = fields.map(f => `${f} = @${f}`).join(', ');
    const stmt = db.prepare(`
    UPDATE merchants 
    SET ${setClause}, updated_at = CURRENT_TIMESTAMP 
    WHERE id = @id
  `);
    stmt.run({ ...data, id });
    return getMerchantById(id);
}
// 删除商家
function deleteMerchant(id) {
    const db = (0, database_1.getDatabase)();
    const result = db.prepare('DELETE FROM merchants WHERE id = ?').run(id);
    return result.changes > 0;
}
// 认证商家
function approveMerchant(id) {
    return updateMerchant(id, { status: 'approved' });
}
// 拒绝商家
function rejectMerchant(id) {
    return updateMerchant(id, { status: 'rejected' });
}
// 暂停商家
function suspendMerchant(id) {
    return updateMerchant(id, { status: 'suspended' });
}
// 搜索商家
function searchMerchants(keyword) {
    const db = (0, database_1.getDatabase)();
    const searchTerm = `%${keyword}%`;
    return db.prepare(`
    SELECT * FROM merchants 
    WHERE name LIKE ? OR phone LIKE ? OR address LIKE ? OR contact_person LIKE ?
    ORDER BY created_at DESC
  `).all(searchTerm, searchTerm, searchTerm, searchTerm);
}
//# sourceMappingURL=merchant.js.map
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.createProduct = createProduct;
exports.getProductById = getProductById;
exports.getProductsByMerchant = getProductsByMerchant;
exports.getActiveProductsByMerchant = getActiveProductsByMerchant;
exports.getAllProducts = getAllProducts;
exports.updateProduct = updateProduct;
exports.updateProductPrice = updateProductPrice;
exports.updateProductDeliveryTime = updateProductDeliveryTime;
exports.deleteProduct = deleteProduct;
exports.activateProduct = activateProduct;
exports.deactivateProduct = deactivateProduct;
exports.markProductSoldOut = markProductSoldOut;
exports.searchProducts = searchProducts;
exports.getProductsByCategory = getProductsByCategory;
exports.getCategories = getCategories;
const database_1 = require("./database");
// 创建商品
function createProduct(data) {
    const db = (0, database_1.getDatabase)();
    const stmt = db.prepare(`
    INSERT INTO products (
      merchant_id, name, description, price, original_price, 
      image_url, category, delivery_time, stock
    )
    VALUES (
      @merchant_id, @name, @description, @price, @original_price,
      @image_url, @category, @delivery_time, @stock
    )
  `);
    const result = stmt.run({
        ...data,
        delivery_time: data.delivery_time ?? 30,
        stock: data.stock ?? 0
    });
    return getProductById(Number(result.lastInsertRowid));
}
// 根据ID获取商品
function getProductById(id) {
    const db = (0, database_1.getDatabase)();
    return db.prepare('SELECT * FROM products WHERE id = ?').get(id);
}
// 获取商家的所有商品
function getProductsByMerchant(merchantId) {
    const db = (0, database_1.getDatabase)();
    return db.prepare(`
    SELECT * FROM products 
    WHERE merchant_id = ? 
    ORDER BY created_at DESC
  `).all(merchantId);
}
// 获取商家的活跃商品
function getActiveProductsByMerchant(merchantId) {
    const db = (0, database_1.getDatabase)();
    return db.prepare(`
    SELECT * FROM products 
    WHERE merchant_id = ? AND status = 'active'
    ORDER BY created_at DESC
  `).all(merchantId);
}
// 获取所有商品
function getAllProducts() {
    const db = (0, database_1.getDatabase)();
    return db.prepare(`
    SELECT p.*, m.name as merchant_name 
    FROM products p
    JOIN merchants m ON p.merchant_id = m.id
    ORDER BY p.created_at DESC
  `).all();
}
// 更新商品信息
function updateProduct(id, data) {
    const db = (0, database_1.getDatabase)();
    const fields = Object.keys(data);
    if (fields.length === 0)
        return getProductById(id);
    const setClause = fields.map(f => `${f} = @${f}`).join(', ');
    const stmt = db.prepare(`
    UPDATE products 
    SET ${setClause}, updated_at = CURRENT_TIMESTAMP 
    WHERE id = @id
  `);
    stmt.run({ ...data, id });
    return getProductById(id);
}
// 更新商品价格
function updateProductPrice(id, price) {
    return updateProduct(id, { price });
}
// 更新商品配送时间
function updateProductDeliveryTime(id, deliveryTime) {
    return updateProduct(id, { delivery_time: deliveryTime });
}
// 删除商品
function deleteProduct(id) {
    const db = (0, database_1.getDatabase)();
    const result = db.prepare('DELETE FROM products WHERE id = ?').run(id);
    return result.changes > 0;
}
// 上架商品
function activateProduct(id) {
    return updateProduct(id, { status: 'active' });
}
// 下架商品
function deactivateProduct(id) {
    return updateProduct(id, { status: 'inactive' });
}
// 标记售罄
function markProductSoldOut(id) {
    return updateProduct(id, { status: 'sold_out' });
}
// 搜索商品
function searchProducts(keyword) {
    const db = (0, database_1.getDatabase)();
    const searchTerm = `%${keyword}%`;
    return db.prepare(`
    SELECT p.*, m.name as merchant_name 
    FROM products p
    JOIN merchants m ON p.merchant_id = m.id
    WHERE p.name LIKE ? OR p.description LIKE ? OR p.category LIKE ?
    ORDER BY p.created_at DESC
  `).all(searchTerm, searchTerm, searchTerm);
}
// 按分类获取商品
function getProductsByCategory(category) {
    const db = (0, database_1.getDatabase)();
    return db.prepare(`
    SELECT * FROM products 
    WHERE category = ? AND status = 'active'
    ORDER BY created_at DESC
  `).all(category);
}
// 获取商品分类列表
function getCategories() {
    const db = (0, database_1.getDatabase)();
    const rows = db.prepare(`
    SELECT DISTINCT category FROM products 
    WHERE category IS NOT NULL AND category != ''
    ORDER BY category
  `).all();
    return rows.map(r => r.category);
}
//# sourceMappingURL=product.js.map
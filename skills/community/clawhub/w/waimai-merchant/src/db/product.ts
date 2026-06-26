import { getDatabase, Product } from './database';

// 创建商品
export function createProduct(data: {
  merchant_id: number;
  name: string;
  description?: string;
  price: number;
  original_price?: number;
  image_url?: string;
  category?: string;
  delivery_time?: number;
  stock?: number;
}): Product {
  const db = getDatabase();
  
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
  
  return getProductById(Number(result.lastInsertRowid))!;
}

// 根据ID获取商品
export function getProductById(id: number): Product | null {
  const db = getDatabase();
  return db.prepare('SELECT * FROM products WHERE id = ?').get(id) as Product | null;
}

// 获取商家的所有商品
export function getProductsByMerchant(merchantId: number): Product[] {
  const db = getDatabase();
  return db.prepare(`
    SELECT * FROM products 
    WHERE merchant_id = ? 
    ORDER BY created_at DESC
  `).all(merchantId) as Product[];
}

// 获取商家的活跃商品
export function getActiveProductsByMerchant(merchantId: number): Product[] {
  const db = getDatabase();
  return db.prepare(`
    SELECT * FROM products 
    WHERE merchant_id = ? AND status = 'active'
    ORDER BY created_at DESC
  `).all(merchantId) as Product[];
}

// 获取所有商品
export function getAllProducts(): Product[] {
  const db = getDatabase();
  return db.prepare(`
    SELECT p.*, m.name as merchant_name 
    FROM products p
    JOIN merchants m ON p.merchant_id = m.id
    ORDER BY p.created_at DESC
  `).all() as (Product & { merchant_name: string })[];
}

// 更新商品信息
export function updateProduct(
  id: number,
  data: Partial<{
    name: string;
    description: string;
    price: number;
    original_price: number;
    image_url: string;
    category: string;
    delivery_time: number;
    stock: number;
    status: Product['status'];
  }>
): Product | null {
  const db = getDatabase();
  
  const fields = Object.keys(data);
  if (fields.length === 0) return getProductById(id);
  
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
export function updateProductPrice(id: number, price: number): Product | null {
  return updateProduct(id, { price });
}

// 更新商品配送时间
export function updateProductDeliveryTime(id: number, deliveryTime: number): Product | null {
  return updateProduct(id, { delivery_time: deliveryTime });
}

// 删除商品
export function deleteProduct(id: number): boolean {
  const db = getDatabase();
  const result = db.prepare('DELETE FROM products WHERE id = ?').run(id);
  return result.changes > 0;
}

// 上架商品
export function activateProduct(id: number): Product | null {
  return updateProduct(id, { status: 'active' });
}

// 下架商品
export function deactivateProduct(id: number): Product | null {
  return updateProduct(id, { status: 'inactive' });
}

// 标记售罄
export function markProductSoldOut(id: number): Product | null {
  return updateProduct(id, { status: 'sold_out' });
}

// 搜索商品
export function searchProducts(keyword: string): (Product & { merchant_name: string })[] {
  const db = getDatabase();
  const searchTerm = `%${keyword}%`;
  return db.prepare(`
    SELECT p.*, m.name as merchant_name 
    FROM products p
    JOIN merchants m ON p.merchant_id = m.id
    WHERE p.name LIKE ? OR p.description LIKE ? OR p.category LIKE ?
    ORDER BY p.created_at DESC
  `).all(searchTerm, searchTerm, searchTerm) as (Product & { merchant_name: string })[];
}

// 按分类获取商品
export function getProductsByCategory(category: string): Product[] {
  const db = getDatabase();
  return db.prepare(`
    SELECT * FROM products 
    WHERE category = ? AND status = 'active'
    ORDER BY created_at DESC
  `).all(category) as Product[];
}

// 获取商品分类列表
export function getCategories(): string[] {
  const db = getDatabase();
  const rows = db.prepare(`
    SELECT DISTINCT category FROM products 
    WHERE category IS NOT NULL AND category != ''
    ORDER BY category
  `).all() as { category: string }[];
  return rows.map(r => r.category);
}

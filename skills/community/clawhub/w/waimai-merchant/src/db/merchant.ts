import { getDatabase, Merchant } from './database';

// 创建商家
export function createMerchant(data: {
  name: string;
  phone: string;
  email?: string;
  address: string;
  business_license?: string;
  contact_person?: string;
}): Merchant {
  const db = getDatabase();
  
  const stmt = db.prepare(`
    INSERT INTO merchants (name, phone, email, address, business_license, contact_person)
    VALUES (@name, @phone, @email, @address, @business_license, @contact_person)
  `);
  
  const result = stmt.run(data);
  
  return getMerchantById(Number(result.lastInsertRowid))!;
}

// 根据ID获取商家
export function getMerchantById(id: number): Merchant | null {
  const db = getDatabase();
  return db.prepare('SELECT * FROM merchants WHERE id = ?').get(id) as Merchant | null;
}

// 根据手机号获取商家
export function getMerchantByPhone(phone: string): Merchant | null {
  const db = getDatabase();
  return db.prepare('SELECT * FROM merchants WHERE phone = ?').get(phone) as Merchant | null;
}

// 获取所有商家
export function getAllMerchants(): Merchant[] {
  const db = getDatabase();
  return db.prepare('SELECT * FROM merchants ORDER BY created_at DESC').all() as Merchant[];
}

// 根据状态获取商家
export function getMerchantsByStatus(status: Merchant['status']): Merchant[] {
  const db = getDatabase();
  return db.prepare('SELECT * FROM merchants WHERE status = ? ORDER BY created_at DESC').all(status) as Merchant[];
}

// 更新商家信息
export function updateMerchant(
  id: number,
  data: Partial<{
    name: string;
    phone: string;
    email: string;
    address: string;
    business_license: string;
    contact_person: string;
    status: Merchant['status'];
  }>
): Merchant | null {
  const db = getDatabase();
  
  const fields = Object.keys(data);
  if (fields.length === 0) return getMerchantById(id);
  
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
export function deleteMerchant(id: number): boolean {
  const db = getDatabase();
  const result = db.prepare('DELETE FROM merchants WHERE id = ?').run(id);
  return result.changes > 0;
}

// 认证商家
export function approveMerchant(id: number): Merchant | null {
  return updateMerchant(id, { status: 'approved' });
}

// 拒绝商家
export function rejectMerchant(id: number): Merchant | null {
  return updateMerchant(id, { status: 'rejected' });
}

// 暂停商家
export function suspendMerchant(id: number): Merchant | null {
  return updateMerchant(id, { status: 'suspended' });
}

// 搜索商家
export function searchMerchants(keyword: string): Merchant[] {
  const db = getDatabase();
  const searchTerm = `%${keyword}%`;
  return db.prepare(`
    SELECT * FROM merchants 
    WHERE name LIKE ? OR phone LIKE ? OR address LIKE ? OR contact_person LIKE ?
    ORDER BY created_at DESC
  `).all(searchTerm, searchTerm, searchTerm, searchTerm) as Merchant[];
}

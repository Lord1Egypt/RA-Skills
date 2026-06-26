import Database from 'better-sqlite3';
export declare function getDatabase(): Database.Database;
export declare function closeDatabase(): void;
export declare function getDataDir(): string;
export interface Merchant {
    id: number;
    name: string;
    phone: string;
    email?: string;
    address: string;
    business_license?: string;
    contact_person?: string;
    status: 'pending' | 'approved' | 'rejected' | 'suspended';
    created_at: string;
    updated_at: string;
}
export interface Product {
    id: number;
    merchant_id: number;
    name: string;
    description?: string;
    price: number;
    original_price?: number;
    image_url?: string;
    category?: string;
    delivery_time: number;
    stock: number;
    status: 'active' | 'inactive' | 'sold_out';
    created_at: string;
    updated_at: string;
}
//# sourceMappingURL=database.d.ts.map
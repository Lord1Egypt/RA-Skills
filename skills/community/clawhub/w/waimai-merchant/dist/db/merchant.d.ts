import { Merchant } from './database';
export declare function createMerchant(data: {
    name: string;
    phone: string;
    email?: string;
    address: string;
    business_license?: string;
    contact_person?: string;
}): Merchant;
export declare function getMerchantById(id: number): Merchant | null;
export declare function getMerchantByPhone(phone: string): Merchant | null;
export declare function getAllMerchants(): Merchant[];
export declare function getMerchantsByStatus(status: Merchant['status']): Merchant[];
export declare function updateMerchant(id: number, data: Partial<{
    name: string;
    phone: string;
    email: string;
    address: string;
    business_license: string;
    contact_person: string;
    status: Merchant['status'];
}>): Merchant | null;
export declare function deleteMerchant(id: number): boolean;
export declare function approveMerchant(id: number): Merchant | null;
export declare function rejectMerchant(id: number): Merchant | null;
export declare function suspendMerchant(id: number): Merchant | null;
export declare function searchMerchants(keyword: string): Merchant[];
//# sourceMappingURL=merchant.d.ts.map
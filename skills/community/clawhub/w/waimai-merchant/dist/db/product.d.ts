import { Product } from './database';
export declare function createProduct(data: {
    merchant_id: number;
    name: string;
    description?: string;
    price: number;
    original_price?: number;
    image_url?: string;
    category?: string;
    delivery_time?: number;
    stock?: number;
}): Product;
export declare function getProductById(id: number): Product | null;
export declare function getProductsByMerchant(merchantId: number): Product[];
export declare function getActiveProductsByMerchant(merchantId: number): Product[];
export declare function getAllProducts(): Product[];
export declare function updateProduct(id: number, data: Partial<{
    name: string;
    description: string;
    price: number;
    original_price: number;
    image_url: string;
    category: string;
    delivery_time: number;
    stock: number;
    status: Product['status'];
}>): Product | null;
export declare function updateProductPrice(id: number, price: number): Product | null;
export declare function updateProductDeliveryTime(id: number, deliveryTime: number): Product | null;
export declare function deleteProduct(id: number): boolean;
export declare function activateProduct(id: number): Product | null;
export declare function deactivateProduct(id: number): Product | null;
export declare function markProductSoldOut(id: number): Product | null;
export declare function searchProducts(keyword: string): (Product & {
    merchant_name: string;
})[];
export declare function getProductsByCategory(category: string): Product[];
export declare function getCategories(): string[];
//# sourceMappingURL=product.d.ts.map
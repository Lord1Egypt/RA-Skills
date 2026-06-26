export interface DBConfig {
    host: string;
    port: number;
    user: string;
    password: string;
    database: string;
}
export interface FieldsConfig {
    orders: Record<string, string>;
    order_items: Record<string, string>;
}
export interface Config {
    database: DBConfig;
    tables: {
        orders: string;
        order_items: string;
    };
    fields: FieldsConfig;
}
export interface OrderItem {
    order_id: string;
    product_name: string;
    sku: string;
    quantity: number;
    price: number;
}
export interface Order {
    order_id: string;
    created_at: string;
    total_amount: number;
    payment_method: string;
    status: string;
    items?: OrderItem[];
}
export interface OrderItemAnalysis {
    product_name?: string;
    sku?: string;
    quantity?: number;
    price?: number;
}
export interface OrderAnalysis {
    total_amount?: number;
    payment_method?: string;
    status?: string;
    items?: OrderItemAnalysis[];
}
export interface OrdersData {
    date_range: {
        start: string;
        end: string;
    };
    orders: OrderAnalysis[];
}
export interface SKUDetail {
    quantity: number;
    revenue: number;
    product_name: string;
}
export interface Analysis {
    date_range: {
        start: string;
        end: string;
    };
    total_orders: number;
    total_amount: number;
    avg_order_amount: number;
    total_items: number;
    payment_methods: Record<string, number>;
    status_distribution: Record<string, number>;
    products: Record<string, number>;
    sku_analysis: Record<string, SKUDetail>;
}
//# sourceMappingURL=types.d.ts.map
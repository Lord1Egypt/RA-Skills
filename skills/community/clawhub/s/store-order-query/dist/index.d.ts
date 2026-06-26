import { type Connection } from "mysql2/promise";
import type { DBConfig, Config, Order } from "./types.js";
export declare function connectMySQL(config: DBConfig): Promise<Connection>;
export declare function queryOrders(connection: Connection, config: Config, startDate: Date, endDate: Date): Promise<Order[]>;
//# sourceMappingURL=index.d.ts.map
import fs from "fs";
import path from "path";
import mysql from "mysql2/promise";
const baseDir = path.join(process.env.HOME || "~", "/openclaw-skill-data/store-order-query/");
const configPath = path.join(baseDir, "config.json");
const dataFile = path.join(baseDir, "orders_data.json");
function loadConfig() {
    // 确保目录存在
    if (!fs.existsSync(baseDir)) {
        try {
            fs.mkdirSync(baseDir, { recursive: true });
            console.log(`已创建配置目录: ${baseDir}`);
        }
        catch (error) {
            console.error(`创建配置目录失败: ${error.message}`);
            process.exit(1);
        }
    }
    if (!fs.existsSync(configPath)) {
        console.error("错误: 配置文件不存在");
        console.error(`配置文件路径: ${configPath}`);
        console.error("\n请执行以下命令创建配置文件:");
        // 获取当前技能的根目录
        const skillRoot = path.join(path.dirname(new URL(import.meta.url).pathname), "..");
        const examplePath = path.join(skillRoot, "config.example.json");
        console.error(`\n  cp ${examplePath} ${configPath}`);
        console.error("\n然后编辑配置文件填入你的数据库信息");
        process.exit(1);
    }
    return JSON.parse(fs.readFileSync(configPath, "utf-8"));
}
function getDateRange(rangeType, startDate, endDate) {
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    if (rangeType === "today") {
        return { start: today, end: today };
    }
    else if (rangeType === "yesterday") {
        const yesterday = new Date(today);
        yesterday.setDate(yesterday.getDate() - 1);
        return { start: yesterday, end: yesterday };
    }
    else if (rangeType === "last7days") {
        const start = new Date(today);
        start.setDate(start.getDate() - 6);
        return { start, end: today };
    }
    else if (rangeType === "last30days") {
        const start = new Date(today);
        start.setDate(start.getDate() - 29);
        return { start, end: today };
    }
    else if (rangeType === "custom" && startDate && endDate) {
        return { start: new Date(startDate), end: new Date(endDate) };
    }
    return { start: today, end: today };
}
function formatDate(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const day = String(date.getDate()).padStart(2, "0");
    return `${year}-${month}-${day}`;
}
export async function connectMySQL(config) {
    try {
        const connection = await mysql.createConnection({
            host: config.host,
            port: config.port,
            user: config.user,
            password: config.password,
            database: config.database
        });
        console.log("数据库连接成功");
        return connection;
    }
    catch (error) {
        console.error("MySQL 连接失败:", error.message);
        throw error;
    }
}
export async function queryOrders(connection, config, startDate, endDate) {
    const { tables, fields } = config;
    const ordersFields = fields.orders;
    const startDateStr = formatDate(startDate);
    const endDateStr = formatDate(endDate);
    const orderSQL = `
    SELECT 
      \`${ordersFields.id}\` as order_id,
      \`${ordersFields.created_at}\` as created_at,
      \`${ordersFields.total_amount}\` as total_amount,
      \`${ordersFields.payment_method}\` as payment_method,
      \`${ordersFields.status}\` as status
    FROM \`${tables.orders}\`
    WHERE DATE(\`${ordersFields.created_at}\`) >= ? 
      AND DATE(\`${ordersFields.created_at}\`) <= ?
    ORDER BY \`${ordersFields.created_at}\` DESC
  `;
    const [orders] = await connection.query(orderSQL, [startDateStr, endDateStr]);
    console.log(`查询到 ${orders.length} 条订单记录`);
    if (orders.length > 0) {
        const orderIds = orders.map(order => order.order_id);
        const itemsFields = fields.order_items;
        const placeholders = orderIds.map(() => "?").join(",");
        const itemsSQL = `
      SELECT 
        \`${itemsFields.order_id}\` as order_id,
        \`${itemsFields.product_name}\` as product_name,
        \`${itemsFields.sku}\` as sku,
        \`${itemsFields.quantity}\` as quantity,
        \`${itemsFields.price}\` as price
      FROM \`${tables.order_items}\`
      WHERE \`${itemsFields.order_id}\` IN (${placeholders})
    `;
        const [items] = await connection.query(itemsSQL, orderIds);
        console.log(`查询到 ${items.length} 条商品记录`);
        const itemsByOrder = {};
        items.forEach(item => {
            if (!itemsByOrder[item.order_id]) {
                itemsByOrder[item.order_id] = [];
            }
            itemsByOrder[item.order_id].push(item);
        });
        orders.forEach(order => {
            order.items = itemsByOrder[order.order_id] || [];
        });
    }
    return orders;
}
function saveData(orders, startDate, endDate) {
    if (!fs.existsSync(baseDir)) {
        fs.mkdirSync(baseDir, { recursive: true });
    }
    const data = {
        query_date: new Date().toISOString(),
        date_range: { start: formatDate(startDate), end: formatDate(endDate) },
        orders,
    };
    fs.writeFileSync(dataFile, JSON.stringify(data, null, 2), "utf-8");
    console.log(`数据已保存到: ${dataFile}`);
}
function parseArgs() {
    const args = process.argv.slice(2);
    const options = { dateRange: "today", startDate: null, endDate: null };
    for (let i = 0; i < args.length; i++) {
        if (args[i] === "--date-range" && i + 1 < args.length) {
            options.dateRange = args[i + 1];
            i++;
        }
        else if (args[i] === "--start-date" && i + 1 < args.length) {
            options.startDate = args[i + 1];
            i++;
        }
        else if (args[i] === "--end-date" && i + 1 < args.length) {
            options.endDate = args[i + 1];
            i++;
        }
    }
    return options;
}
async function main() {
    let connection;
    try {
        const options = parseArgs();
        const config = loadConfig();
        const { start, end } = getDateRange(options.dateRange, options.startDate, options.endDate);
        console.log(`查询日期范围: ${formatDate(start)} 至 ${formatDate(end)}`);
        connection = await connectMySQL(config.database);
        const orders = await queryOrders(connection, config, start, end);
        saveData(orders, start, end);
        console.log("查询完成!");
    }
    catch (error) {
        console.error("执行失败:", error.message);
        process.exit(1);
    }
    finally {
        if (connection) {
            await connection.end();
        }
    }
}
main();
//# sourceMappingURL=index.js.map
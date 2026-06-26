import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const baseDir = path.join(process.env.HOME || "~", "/openclaw-skill-data/store-order-query/");
const dataFile = path.join(baseDir, "orders_data.json");
function loadOrdersData() {
    if (!fs.existsSync(dataFile)) {
        console.error("错误: 订单数据文件不存在,请先运行查询脚本");
        process.exit(1);
    }
    return JSON.parse(fs.readFileSync(dataFile, "utf-8"));
}
export function analyzeOrders(data) {
    const orders = data.orders;
    if (!orders || orders.length === 0) {
        return {
            date_range: data.date_range,
            total_orders: 0,
            total_amount: 0,
            avg_order_amount: 0,
            total_items: 0,
            payment_methods: {},
            status_distribution: {},
            products: {},
            sku_analysis: {}
        };
    }
    const totalOrders = orders.length;
    const totalAmount = orders.reduce((sum, order) => sum + parseFloat(String(order.total_amount || 0)), 0);
    const paymentMethods = {};
    const statusDistribution = {};
    const productsCounter = {};
    const skuDetails = {};
    let totalItems = 0;
    orders.forEach(order => {
        const paymentMethod = order.payment_method || "未知";
        paymentMethods[paymentMethod] = (paymentMethods[paymentMethod] || 0) + 1;
        const status = order.status || "未知";
        statusDistribution[status] = (statusDistribution[status] || 0) + 1;
        const items = order.items || [];
        items.forEach(item => {
            const productName = item.product_name || "未知商品";
            const sku = item.sku || "未知SKU";
            const quantity = parseInt(String(item.quantity || 0));
            const price = parseFloat(String(item.price || 0));
            productsCounter[productName] = (productsCounter[productName] || 0) + quantity;
            totalItems += quantity;
            if (!skuDetails[sku]) {
                skuDetails[sku] = { quantity: 0, revenue: 0, product_name: productName };
            }
            skuDetails[sku].quantity += quantity;
            skuDetails[sku].revenue += price * quantity;
        });
    });
    const topProducts = Object.fromEntries(Object.entries(productsCounter).sort((a, b) => b[1] - a[1]).slice(0, 10));
    const topSKUs = Object.fromEntries(Object.entries(skuDetails).sort((a, b) => b[1].quantity - a[1].quantity).slice(0, 20));
    return {
        date_range: data.date_range,
        total_orders: totalOrders,
        total_amount: totalAmount,
        avg_order_amount: totalOrders > 0 ? totalAmount / totalOrders : 0,
        total_items: totalItems,
        payment_methods: paymentMethods,
        status_distribution: statusDistribution,
        products: topProducts,
        sku_analysis: topSKUs
    };
}
export function generateReport(analysis) {
    const { start: startDate, end: endDate } = analysis.date_range;
    let report = `# 店铺订单分析报告\n\n## 查询时间范围\n**${startDate}** 至 **${endDate}**\n\n---\n\n## 总体概况\n\n| 指标 | 数值 |\n|------|------|\n| 订单总数 | **${analysis.total_orders}** 单 |\n| 订单总金额 | **¥${analysis.total_amount.toFixed(2)}** |\n| 平均订单金额 | **¥${analysis.avg_order_amount.toFixed(2)}** |\n| 商品总数 | **${analysis.total_items}** 件 |\n\n`;
    report += "---\n\n## 支付方式分布\n\n";
    if (Object.keys(analysis.payment_methods).length > 0) {
        report += "| 支付方式 | 订单数 | 占比 |\n|----------|--------|------|\n";
        Object.entries(analysis.payment_methods)
            .sort((a, b) => b[1] - a[1])
            .forEach(([method, count]) => {
            const pct = analysis.total_orders > 0 ? (count / analysis.total_orders * 100).toFixed(1) : "0";
            report += `| ${method} | ${count} | ${pct}% |\n`;
        });
    }
    else {
        report += "*暂无数据*\n";
    }
    report += "\n---\n\n## 热销商品 TOP 10\n\n";
    if (Object.keys(analysis.products).length > 0) {
        report += "| 排名 | 商品名称 | 销售数量 |\n|------|----------|----------|\n";
        let rank = 1;
        Object.entries(analysis.products).forEach(([product, quantity]) => {
            report += `| ${rank++} | ${product} | ${quantity} 件 |\n`;
        });
    }
    else {
        report += "*暂无数据*\n";
    }
    report += "\n---\n\n## SKU 销售分析 (前20)\n\n";
    if (Object.keys(analysis.sku_analysis).length > 0) {
        report += "| SKU | 商品名称 | 销售数量 | 销售额 |\n|-----|----------|----------|--------|\n";
        Object.entries(analysis.sku_analysis).forEach(([sku, details]) => {
            report += `| ${sku} | ${details.product_name} | ${details.quantity} 件 | ¥${details.revenue.toFixed(2)} |\n`;
        });
    }
    else {
        report += "*暂无数据*\n";
    }
    const now = new Date();
    const timestamp = now.toLocaleString("zh-CN", { timeZone: "Asia/Shanghai" });
    report += `\n---\n\n*报告生成时间: ${timestamp}*\n`;
    return report;
}
function saveReport(report) {
    if (!fs.existsSync(baseDir)) {
        fs.mkdirSync(baseDir, { recursive: true });
    }
    const reportFile = path.join(baseDir, "order_report.md");
    fs.writeFileSync(reportFile, report, "utf-8");
    console.log(`报告已保存到: ${reportFile}`);
}
function main() {
    const data = loadOrdersData();
    console.log("正在分析订单数据...");
    const analysis = analyzeOrders(data);
    console.log("正在生成报告...");
    const report = generateReport(analysis);
    saveReport(report);
    console.log("分析完成!");
    console.log(`\n订单总数: ${analysis.total_orders}`);
    console.log(`订单总金额: ¥${analysis.total_amount.toFixed(2)}`);
    console.log(`商品总数: ${analysis.total_items} 件`);
}
main();
//# sourceMappingURL=analyze-orders.js.map
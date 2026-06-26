const ExcelJS = require('exceljs');

/**
 * 将采购记录添加到 purchase_record.xlsx
 * @param {string} dateStr - 日期字符串，格式如 "0312" (MMDD)
 * @param {string} itemName - 物品名称
 * @param {number|string} price - 价格（数字或带单位的字符串）
 * @returns {Promise<string>} 成功消息
 */
async function addPurchase(dateStr, itemName, price) {
    const excelPath = 'C:/Users/Administrator.rjazz-2022BWPUD/Desktop/purchase_record.xlsx';

    // 解析日期：MMDD → YYYY-MM-DD
    const year = new Date().getFullYear();
    const month = dateStr.substring(0, 2);
    const day = dateStr.substring(2, 4);
    const formattedDate = `${year}-${month}-${day}`;

    // 解析价格：提取数字部分
    let priceNum = typeof price === 'number' ? price : parseFloat(price.toString().replace(/[^0-9.]/g, ''));
    
    if (isNaN(priceNum)) {
        throw new Error('无法解析价格，请输入有效的数字');
    }

    // 读取 Excel 文件
    const wb = new ExcelJS.Workbook();
    await wb.xlsx.readFile(excelPath);
    const ws = wb.getWorksheet('sheet1');

    if (!ws) {
        throw new Error('未找到 sheet1');
    }

    // 查找第一个空白行（A、B、C 列都为空）
    let blankRowNumber = null;
    
    for (let rowNum = 2; rowNum <= ws.rowCount + 50; rowNum++) {
        const row = ws.getRow(rowNum);
        if (!row) continue;

        const cellA = row.getCell(1).value;
        const cellB = row.getCell(2).value;
        const cellC = row.getCell(3).value;

        // 检查是否为空行（所有列都是 null、undefined、空字符串或只有空格）
        const isEmpty = !cellA && 
                       (!cellB || (typeof cellB === 'string' && cellB.trim() === '')) &&
                       (!cellC || (typeof cellC === 'string' && cellC.trim() === ''));

        if (isEmpty) {
            blankRowNumber = rowNum;
            break;
        }
    }

    if (!blankRowNumber) {
        throw new Error('未找到空白行，Excel 可能已满');
    }

    // 写入数据
    const row = ws.getRow(blankRowNumber);
    row.getCell(1).value = formattedDate;  // A 列：日期
    row.getCell(2).value = itemName;       // B 列：名称
    row.getCell(3).value = priceNum;       // C 列：价格

    // 保存文件
    await wb.xlsx.writeFile(excelPath);

    return `✅ 已记录：${formattedDate} ${itemName} ¥${priceNum}`;
}

// 导出函数
module.exports = { addPurchase };

const ExcelJS = require('exceljs');
const fs = require('fs');
const path = require('path');

async function generateDeclaration(templatePath, data, outputPath) {
    const workbook = new ExcelJS.Workbook();
    await workbook.xlsx.readFile(templatePath);

    const worksheet = workbook.getWorksheet(1);

    if (worksheet) {
        worksheet.getCell('A1').value = data.invoiceNumber || '';
        worksheet.getCell('B2').value = data.customerName || '';
        worksheet.getCell('C3').value = data.date || '';

        if (data.items && data.items.length > 0) {
            let startRow = 6;
            data.items.forEach((item, index) => {
                const row = worksheet.getRow(startRow + index);
                row.getCell(1).value = item.description;
                row.getCell(2).value = item.quantity;
                row.getCell(3).value = item.unitPrice;
                row.getCell(4).value = item.total;
            });
        }
    }

    await workbook.xlsx.writeFile(outputPath);
    console.log(`Declaration document generated successfully: ${outputPath}`);
}

if (require.main === module) {
    const args = process.argv.slice(2);
    if (args.length !== 3) {
        console.error('Usage: node generate-declaration.js <template_file> <data_file> <output_file>');
        process.exit(1);
    }
    const templateFile = args[0];
    const dataFile = args[1];
    const outputFile = args[2];

    try {
        const rawData = fs.readFileSync(dataFile, 'utf8');
        const data = JSON.parse(rawData);
        generateDeclaration(templateFile, data, outputFile);
    } catch (error) {
        console.error('Error:', error.message);
        process.exit(1);
    }
}

module.exports = generateDeclaration;

const sharp = require('sharp');
const Tesseract = require('tesseract.js');
const ExcelJS = require('exceljs');
const fs = require('fs');
const path = require('path');

const BASE = path.join(__dirname);
const DATA_FILE = path.join(BASE, 'taxi_data.json');
const SCREENSHOT_DIR = path.join(BASE, 'screenshots');
async function main() {
  const imagePaths = process.argv.slice(2);
  if (imagePaths.length === 0) {
    console.error('Usage: node process.js <image1> [image2] ...');
    process.exit(1);
  }

  const worker = await Tesseract.createWorker('chi_sim+eng', 1, {
    langPath: '/tmp/tessdata', cachePath: '/tmp/tessdata', cacheMethod: 'readOnly', gzip: false,
  });

  // 1. OCR all images and parse orders
  let allParsedOrders = [];
  let ocrDataMap = {}; // imgPath -> { data, orders[] }

  for (const imgPath of imagePaths) {
    console.log(`\nOCR: ${path.basename(imgPath)}`);
    const { data } = await worker.recognize(imgPath);
    const lines = data.lines;
    const orders = [];

    for (let i = 0; i < lines.length; i++) {
      const text = lines[i].text.replace(/\s+/g, '');
      const timeMatch = text.match(/下单时间:(\d{4})年(\d{2})月(\d{2})日(.+)/);
      if (!timeMatch) continue;

      const date = `${timeMatch[1]}-${timeMatch[2]}-${timeMatch[3]}`;
      let time = timeMatch[4].trim().replace(/\./g, ':');
      time = time.replace(/t/gi, '7');

      let amount = 0;
      for (let j = Math.max(0, i - 5); j < i; j++) {
        const amtMatch = lines[j].text.match(/[¥%](\d+\.?\d*)/);
        if (amtMatch) { amount = parseFloat(amtMatch[1]); break; }
      }
      if (amount === 0) {
        for (let j = Math.max(0, i - 5); j < i; j++) {
          const st = lines[j].text.replace(/\s+/g, '');
          if (st.match(/起点[：:]/)) {
            const bareMatch = st.match(/(\d+\.\d{1,2})\s*$/);
            if (bareMatch) { amount = parseFloat(bareMatch[1]); }
            break;
          }
        }
      }
      if (amount > 500) {
        const str = String(amount);
        if (str.length === 4) {
          amount = parseFloat(str.slice(0, 2) + '.' + str.slice(2));
        } else if (str.length === 3) {
          amount = parseFloat(str.slice(0, 1) + '.' + str.slice(1));
        }
      }

      let start = '';
      for (let j = Math.max(0, i - 5); j < i; j++) {
        const st = lines[j].text.replace(/\s+/g, '');
        const stMatch = st.match(/起点[：:](.+)/);
        if (stMatch) {
          start = stMatch[1].replace(/[¥%]\d+\.?\d*/g, '').replace(/\d+\.\d{1,2}\s*$/, '').trim();
          break;
        }
      }

      let end = '';
      for (let j = Math.max(0, i - 5); j < i; j++) {
        const en = lines[j].text.replace(/\s+/g, '');
        const enMatch = en.match(/终[点炭][：:](.+)/);
        if (enMatch) { end = enMatch[1].trim(); break; }
      }

      orders.push({ date, time, start, end, amount, imgPath });
    }

    ocrDataMap[imgPath] = { data, orders };
    allParsedOrders.push(...orders);
  }
  await worker.terminate();

  console.log('\nParsed orders:');
  allParsedOrders.forEach((o, i) => console.log(`  ${i+1}. ${o.date} ${o.time} ¥${o.amount} ${o.start} → ${o.end}`));

  // 2. Dedup
  const existing = JSON.parse(fs.readFileSync(DATA_FILE, 'utf8'));
  const existingKeys = new Set(existing.map(o => `${o.date}_${o.amount}`));
  const newOrders = allParsedOrders.filter(o => !existingKeys.has(`${o.date}_${o.amount}`));

  console.log(`\nNew orders (after dedup): ${newOrders.length}`);
  newOrders.forEach((o, i) => console.log(`  ${i+1}. ${o.date} ${o.time} ¥${o.amount} ${o.start} → ${o.end}`));

  // 3. Process screenshots with mosaic (using correct source image per order)
  for (const order of newOrders) {
    const srcImg = order.imgPath;
    const ocrData = ocrDataMap[srcImg]?.data;
    if (!ocrData) continue;

    const cardLines = ocrData.lines.filter(l => {
      const t = l.text.replace(/\s+/g, '');
      return t.includes(order.date.replace(/-/g, '年').replace(/(\d{4})年(\d{2})年(\d{2})/, '$1年$2月$3日'));
    });
    if (cardLines.length === 0) { console.log('  [skip] no cardLines for', order.date); continue; }

    const timeLine = cardLines[0];
    const cardTop = timeLine.bbox.y0 - 160;
    const cardBottom = timeLine.bbox.y0 + 200;

    const destLine = ocrData.lines.find(l => {
      const t = l.text.replace(/\s+/g, '');
      return (t.match(/终[点炭]/)) && l.bbox.y0 > cardTop && l.bbox.y0 < timeLine.bbox.y0;
    });

    let mosaicRegions = [];
    if (destLine) {
      const destWords = ocrData.words.filter(w =>
        w.bbox.y0 >= destLine.bbox.y0 - 5 && w.bbox.y1 <= destLine.bbox.y1 + 5 &&
        !['终', '点', '炭', ':', '：'].includes(w.text)
      );
      if (destWords.length >= 2) {
        const first = destWords[0];
        const last = destWords[destWords.length - 1];
        mosaicRegions.push({
          left: first.bbox.x1 + 3,
          top: destLine.bbox.y0 - 2,
          width: Math.max(0, last.bbox.x0 - first.bbox.x1 - 6),
          height: destLine.bbox.y1 - destLine.bbox.y0 + 4,
        });
      }
    }

    const imgMeta = await sharp(srcImg).metadata();
    const cropTop = Math.max(0, cardTop);
    const cropHeight = Math.min(imgMeta.height - cropTop, cardBottom - cardTop);

    // Build composite overlay list for single pipeline
    let overlays = [];
    for (const reg of mosaicRegions) {
      const relTop = reg.top - cropTop;
      if (reg.width > 0 && reg.height > 0) {
        try {
          const block = await sharp({
            create: {
              width: reg.width,
              height: reg.height,
              channels: 3,
              background: { r: 255, g: 255, b: 255 }
            }
          }).png().toBuffer();
          overlays.push({ input: block, left: reg.left, top: relTop });
          console.log(`  [mosaic] block: ${reg.left},${relTop} ${reg.width}x${reg.height}`);
        } catch (e) {
          console.warn('  Mosaic failed for', order.date, e.message);
        }
      }
    }

    // Single pipeline: crop + composite + save
    let pipeline = sharp(srcImg).extract({ left: 0, top: cropTop, width: imgMeta.width, height: cropHeight });
    if (overlays.length > 0) {
      pipeline = pipeline.composite(overlays);
    }

    // Unique filename: date + amount to avoid collisions
    const safeAmt = String(order.amount).replace('.', 'p');
    const outFile = path.join(SCREENSHOT_DIR, `order_${order.date}_${safeAmt}.png`);
    await pipeline.png().toFile(outFile);
    console.log(`  Screenshot: ${outFile} (mosaic: ${mosaicRegions.length > 0 ? 'YES' : 'NO'}, destLine: ${destLine ? 'found' : 'miss'})`);
    order.file = path.basename(outFile);
  }

  // 4. Update data
  const allOrders = [...existing, ...newOrders].sort((a, b) => a.date.localeCompare(b.date));
  fs.writeFileSync(DATA_FILE, JSON.stringify(allOrders, null, 2));

  // 5. Filter reimbursable (weekday 21:00+, amount > 0)
  const isReimbursable = (o) => {
    const h = parseInt(o.time.split(':')[0]);
    const d = new Date(o.date + 'T00:00:00');
    const day = d.getDay();
    return h >= 21 && day !== 0 && day !== 6;
  };
  const reimbursableAll = allOrders.filter(o => isReimbursable(o) && o.amount > 0);

  // 6. Generate Excel (reimbursable only)
  await generateExcel(reimbursableAll);

  // 7. Summary
  const reimbursable = newOrders.filter(o => isReimbursable(o) && o.amount > 0);
  console.log(`\n=== Summary ===`);
  console.log(`New orders: ${newOrders.length}`);
  console.log(`Reimbursable (weekday 21:00+): ${reimbursable.length}`);
  console.log(`Reimbursable total: ¥${reimbursable.reduce((s, o) => s + o.amount, 0).toFixed(2)}`);
}

async function generateExcel(orders) {
  // Group by month
  const byMonth = {};
  orders.forEach(o => {
    const m = o.date.substring(0, 7);
    if (!byMonth[m]) byMonth[m] = [];
    byMonth[m].push(o);
  });

  for (const [month, monthOrders] of Object.entries(byMonth)) {
    const wb = new ExcelJS.Workbook();
    const ws = wb.addWorksheet('报销明细');

    const dayNames = ['周日','周一','周二','周三','周四','周五','周六'];

    ws.columns = [
      { header: '序号', key: 'idx', width: 6 },
      { header: '日期', key: 'date', width: 12 },
      { header: '星期', key: 'weekday', width: 6 },
      { header: '时间', key: 'time', width: 8 },
      { header: '起点', key: 'start', width: 28 },
      { header: '终点', key: 'end', width: 20 },
      { header: '金额', key: 'amount', width: 10 },
      { header: '备注', key: 'note', width: 12 },
    ];

    // Desensitize destination: keep first and last char, mask middle
    const maskEnd = (end) => {
      if (!end) return '古*****门';
      const clean = end.replace(/\s+/g, '');
      if (clean.length <= 2) return clean;
      return clean[0] + '*'.repeat(Math.min(clean.length - 2, 5)) + clean[clean.length - 1];
    };

    monthOrders.sort((a, b) => a.date.localeCompare(b.date));
    monthOrders.forEach((o, i) => {
      const d = new Date(o.date + 'T00:00:00');
      ws.addRow({
        idx: i + 1,
        date: o.date,
        weekday: dayNames[d.getDay()],
        time: o.time,
        start: o.start,
        end: maskEnd(o.end),
        amount: o.amount,
        note: '加班打车',
      });
    });

    // Total row
    const total = monthOrders.reduce((s, o) => s + o.amount, 0);
    ws.addRow({ idx: '', date: '', weekday: '', time: '', start: '', end: '合计', amount: total, note: '' });

    // Sheet 2: screenshots
    const ws2 = wb.addWorksheet('订单截图');
    let rowNum = 1;
    for (const o of monthOrders) {
      if (!o.file) continue;
      const imgPath = path.join(SCREENSHOT_DIR, o.file);
      if (!fs.existsSync(imgPath)) continue;

      ws2.getRow(rowNum).height = 18;
      ws2.getCell(`A${rowNum}`).value = `${o.date}  ¥${o.amount}`;

      const imgId = wb.addImage({ filename: imgPath, extension: 'png' });
      ws2.addImage(imgId, {
        tl: { col: 0, row: rowNum },
        ext: { width: 400, height: 180 },
      });
      rowNum += 12;
    }

    const outFile = path.join(BASE, `${month}-taxi_expense.xlsx`);
    await wb.xlsx.writeFile(outFile);
    console.log(`Excel: ${outFile}`);
  }
}

main().catch(e => { console.error(e); process.exit(1); });

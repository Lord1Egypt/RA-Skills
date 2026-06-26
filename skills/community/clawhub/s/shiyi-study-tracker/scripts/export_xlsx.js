/**
 * export_xlsx.js
 * 导出错题本，支持筛选：
 *   --pending-only          只导出"待二刷"
 *   --section=Verbal        只导出某科目/section
 *   --days=30               只导出最近 N 天
 *   --no-images             不嵌入截图
 */

const fs            = require('fs');
const path          = require('path');
const os            = require('os');
const { execFile }  = require('child_process');

const DATA_DIR = path.join(os.homedir(), '.openclaw/skills/shiyi/data');
const OUT_DIR  = path.join(DATA_DIR, 'exports');
const WQ_PATH  = path.join(DATA_DIR, 'wrong_questions.json');

function loadJson(p, fb) {
  try { return JSON.parse(fs.readFileSync(p, 'utf-8')); } catch (_) { return fb; }
}

function runPython(args, timeout = 60_000) {
  return new Promise((resolve, reject) => {
    function attempt(cmd) {
      execFile(cmd, args, { timeout }, (err, stdout, stderr) => {
        if (err && err.code === 'ENOENT' && cmd === 'python3') return attempt('python');
        if (err) return reject({ error: err, stderr });
        resolve({ stdout, stderr });
      });
    }
    attempt('python3');
  });
}

function buildPythonScript({ wrongRows, outPath, imageMap, sheetName }) {
  const wrongJson  = JSON.stringify(wrongRows);
  const imageMapJson = JSON.stringify(imageMap);

  return `
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.drawing.image import Image as XLImage
from openpyxl.utils import get_column_letter
import json, os

wrong_rows = json.loads(${JSON.stringify(wrongJson)})
image_map  = json.loads(${JSON.stringify(imageMapJson)})
out_path   = ${JSON.stringify(outPath)}
sheet_name = ${JSON.stringify(sheetName)}

HEADER_BG = "2D5FA1"
HEADER_FG = "FFFFFF"

wb = openpyxl.Workbook()
ws = wb.active
ws.title = sheet_name

headers    = ["日期","考试","科目/大类","题目类型","知识点","错误原因","题目内容","视觉描述","正确答案","批注","知识点标签","状态","来源","截图"]
col_widths = [10,    12,    18,        16,        24,     12,       40,       40,       8,       20,   20,       10,   10,  20]

for ci, (h, w) in enumerate(zip(headers, col_widths), 1):
    cell = ws.cell(row=1, column=ci, value=h)
    cell.font      = Font(bold=True, color=HEADER_FG, name="Arial", size=10)
    cell.fill      = PatternFill("solid", start_color=HEADER_BG)
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ws.column_dimensions[get_column_letter(ci)].width = w
ws.row_dimensions[1].height = 26
ws.freeze_panes = "A2"

IMG_ROW_H = 160
ROW_H     = 22

for ri, row in enumerate(wrong_rows, 2):
    for ci, val in enumerate(row, 1):
        cell = ws.cell(row=ri, column=ci, value=val)
        cell.alignment = Alignment(vertical="center", wrap_text=(ci in [7,8,10]))
        cell.font = Font(name="Arial", size=9)

    img_path = image_map.get(str(ri - 2))
    if img_path and os.path.exists(img_path):
        try:
            img = XLImage(img_path)
            ratio = 160 / img.width if img.width > 0 else 1
            img.width  = int(img.width  * ratio)
            img.height = int(img.height * ratio)
            ws.add_image(img, f"{get_column_letter(len(headers))}{ri}")
            ws.row_dimensions[ri].height = max(IMG_ROW_H, img.height * 0.75 + 10)
        except:
            ws.row_dimensions[ri].height = ROW_H
    else:
        has_visual = bool(row[7] if len(row) > 7 else None)
        ws.row_dimensions[ri].height = 60 if has_visual else ROW_H

wb.save(out_path)
print(out_path)
`.trim();
}

async function exportXlsx({ pendingOnly = false, sectionFilter = null, daysFilter = null, withImages = true } = {}) {
  if (!fs.existsSync(OUT_DIR)) fs.mkdirSync(OUT_DIR, { recursive: true });

  const questions = loadJson(WQ_PATH, []);
  const cutoff    = daysFilter
    ? new Date(Date.now() - daysFilter * 86400000).toISOString().slice(0, 10)
    : null;

  const filtered = questions.filter(q => {
    if (pendingOnly    && q.status === '已掌握')           return false;
    if (sectionFilter  && q.section !== sectionFilter)     return false;
    if (cutoff         && (q.date ?? '') < cutoff)         return false;
    return true;
  });

  const wrongRows = filtered.map(q => [
    q.date                     ?? '',
    (q.exam_name || q.exam)    ?? '',
    q.section                  ?? '',
    q.question_type            ?? '',
    q.knowledge_point          ?? '',
    q.error_reason             ?? '',
    q.question_text            ?? '',
    q.visual_description       ?? '',
    q.answer                   ?? '',
    q.user_annotation          ?? '',
    Array.isArray(q.keywords) ? q.keywords.join('、') : '',
    q.status                   ?? '待二刷',
    q.source                   ?? '',
    '',
  ]);

  // 图片临时文件
  const tmpFiles = [];
  const imageMap = {};
  if (withImages) {
    filtered.forEach((q, idx) => {
      if (!q.raw_image_b64) return;
      const tmpPath = path.join(os.tmpdir(), `qimg_${Date.now()}_${idx}.jpg`);
      try {
        fs.writeFileSync(tmpPath, Buffer.from(q.raw_image_b64, 'base64'));
        imageMap[String(idx)] = tmpPath;
        tmpFiles.push(tmpPath);
      } catch (_) {}
    });
  }

  const today  = new Date().toISOString().slice(0, 10);
  const parts  = [];
  if (pendingOnly)   parts.push('待二刷');
  if (sectionFilter) parts.push(sectionFilter);
  if (daysFilter)    parts.push(`近${daysFilter}天`);
  const suffix   = parts.length ? '_' + parts.join('_') : '';
  const outPath  = path.join(OUT_DIR, `拾遗错题本_${today}${suffix}.xlsx`);
  const sheetName = parts.length ? parts.join('_') + '错题' : '全部错题';

  const pyScript = buildPythonScript({ wrongRows, outPath, imageMap, sheetName });
  const tmpPy    = path.join(os.tmpdir(), `export_${Date.now()}.py`);
  fs.writeFileSync(tmpPy, pyScript, 'utf-8');

  try {
    await runPython([tmpPy]);
  } finally {
    try { fs.unlinkSync(tmpPy); } catch (_) {}
    tmpFiles.forEach(f => { try { fs.unlinkSync(f); } catch (_) {} });
  }

  console.log(`[shiyi] 已导出：${outPath}（${filtered.length} 条）`);
  console.log(`ATTACH:${outPath}`);
  return outPath;
}

if (require.main === module) {
  const pendingOnly   = process.argv.includes('--pending-only');
  const withImages    = !process.argv.includes('--no-images');
  const sectionArg    = process.argv.find(a => a.startsWith('--section='));
  const daysArg       = process.argv.find(a => a.startsWith('--days='));
  const sectionFilter = sectionArg ? sectionArg.split('=')[1] : null;
  const daysFilter    = daysArg    ? parseInt(daysArg.split('=')[1]) : null;
  exportXlsx({ pendingOnly, sectionFilter, daysFilter, withImages }).catch(console.error);
}

module.exports = { exportXlsx };

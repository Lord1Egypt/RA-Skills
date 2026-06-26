# Quy tắc định dạng .docx và chính tả tiếng Việt

---

## 1. Cài đặt và import

```bash
npm install -g docx
```

```javascript
const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  AlignmentType, BorderStyle, WidthType, ShadingType,
  LevelFormat, PageBreak
} = require("docx");
```

## 2. Cấu hình trang giấy

```javascript
sections: [{
  properties: {
    page: {
      size: { width: 11906, height: 16838 },  // A4
      margin: { top: 1134, right: 1134, bottom: 1134, left: 1418 }
    }
  },
  children: [/* nội dung */]
}]
```

## 3. Hàm tiện ích

```javascript
function p(text, options = {}) {
  const { bold, size, alignment, spacing, indent, italic, underline } = options;
  return new Paragraph({
    alignment: alignment || AlignmentType.JUSTIFIED,
    spacing: { after: spacing !== undefined ? spacing : 120, line: 300 },
    indent: indent ? { firstLine: 720 } : undefined,
    children: [
      new TextRun({
        text,
        font: "Times New Roman",
        size: size || 24,
        bold: bold || false,
        italics: italic || false,
        underline: underline ? {} : undefined,
      }),
    ],
  });
}

function pMulti(runs, options = {}) {
  const { alignment, spacing, indent } = options;
  return new Paragraph({
    alignment: alignment || AlignmentType.JUSTIFIED,
    spacing: { after: spacing !== undefined ? spacing : 120, line: 300 },
    indent: indent ? { firstLine: 720 } : undefined,
    children: runs.map(r =>
      new TextRun({
        text: r.text,
        font: "Times New Roman",
        size: r.size || 24,
        bold: r.bold || false,
        italics: r.italic || false,
        underline: r.underline ? {} : undefined,
      })
    ),
  });
}

function emptyLine() {
  return new Paragraph({ spacing: { after: 0 }, children: [] });
}
```

### Bảng kích thước chữ

| Mục đích | pt | size (half-point) |
|----------|----|--------------------|
| Quốc hiệu, tiêu ngữ | 13pt | 26 |
| Tiêu đề hợp đồng | 15pt | 30 |
| Tiêu đề điều khoản | 13pt | 26 |
| Nội dung chính | 12pt | 24 |
| Số hợp đồng | 11pt | 22 |

## 4. Tạo bảng

```javascript
const border = { style: BorderStyle.SINGLE, size: 1, color: "000000" };
const borders = { top: border, bottom: border, left: border, right: border };
const cellMargins = { top: 60, bottom: 60, left: 100, right: 100 };

new Table({
  width: { size: 8500, type: WidthType.DXA },
  columnWidths: [1200, 3650, 3650],
  rows: [
    new TableRow({
      children: [
        new TableCell({
          borders,
          width: { size: 1200, type: WidthType.DXA },
          shading: { fill: "D9E2F3", type: ShadingType.CLEAR },
          margins: cellMargins,
          children: [p("Tiêu đề", { bold: true, alignment: AlignmentType.CENTER, spacing: 0 })],
        }),
      ],
    }),
  ],
})
```

**Quy tắc bảng QUAN TRỌNG:**
- LUÔN dùng `WidthType.DXA` (không dùng PERCENTAGE — lỗi trên Google Docs)
- Đặt CẢ `columnWidths` trên Table VÀ `width` trên mỗi `TableCell`
- Dùng `ShadingType.CLEAR` (không bao giờ dùng SOLID — gây nền đen)

## 5. Phần chữ ký

Dùng bảng không viền, 2 cột: BÊN A | BÊN B, mỗi cột có "(Ký, ghi rõ họ tên)" và dòng chấm.

## 6. Quy tắc quan trọng docx-js

- Không dùng `\n` — dùng Paragraph riêng cho mỗi dòng
- Không dùng unicode bullets — dùng `LevelFormat.BULLET`
- PageBreak phải nằm trong Paragraph
- ImageRun cần chỉ định `type` (png/jpg)
- Không dùng bảng làm đường kẻ — dùng border trên Paragraph

## 7. Chính tả tiếng Việt — NGUYÊN TẮC SỐ 1

**BẮT BUỘC: Sử dụng ký tự Unicode trực tiếp trong JavaScript.**

```javascript
// ✅ ĐÚNG
p("HỢP ĐỒNG THỎA THUẬN CHIA LỢI NHUẬN ĐẦU TƯ");
p("Bên A cam kết hoàn trả vốn gốc khi hết hạn hợp đồng.");

// ❌ SAI — escape sequences gây lỗi chính tả
p("H\u1EE2P \u0110\u1ED2NG TH\u1ECEA THU\u1EAEN...");
// → Kết quả sai: "THỎA THUẮN" thay vì "THỎA THUẬN"
```

### Bảng lỗi chính tả thường gặp

| Từ sai | Từ đúng | Nguyên nhân |
|--------|---------|-------------|
| THUẮN | THUẬN | \u1EAE (Ắ) thay vì \u1EAC (Ậ) |
| LỬI | LỢI | \u1EEC (Ử) thay vì \u1EE2 (Ợ) |
| NHẮN ĐẦU TƯ | NHẬN ĐẦU TƯ | \u1EAE (Ắ) thay vì \u1EAC (Ậ) |
| vình viễn | vĩnh viễn | \u00EC (ì) thay vì \u0129 (ĩ) |
| nghìa vụ | nghĩa vụ | \u00EC (ì) thay vì \u0129 (ĩ) |
| khắt phục | khắc phục | sai phụ âm |
| quyết tóan | quyết toán | sai dấu |

## 8. Validate và kiểm tra

```bash
# Bước 1: Validate cấu trúc .docx
python /mnt/skills/public/docx/scripts/office/validate.py output.docx

# Bước 2: Kiểm tra chính tả
python [skill-path]/scripts/vn-spellcheck.py output.docx

# Bước 3: Đọc lại nội dung
pandoc output.docx -o check.md && cat check.md
```

### Checklist trước khi giao file

- [ ] `validate.py` PASSED
- [ ] `vn-spellcheck.py` không phát hiện lỗi
- [ ] Quốc hiệu đúng: "CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM"
- [ ] Tiêu ngữ đúng: "Độc lập – Tự do – Hạnh phúc"
- [ ] Căn cứ pháp lý đúng loại hợp đồng
- [ ] Số liệu: có cả số và chữ
- [ ] Phần chữ ký: đủ cả hai bên
- [ ] File đã copy ra `/mnt/user-data/outputs/`

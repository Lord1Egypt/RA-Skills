---
name: taohopdong
description: |
  Tạo hợp đồng: tra cứu thông tin doanh nghiệp từ masothue.com và ghi vào Google Sheet (sheet Hợp đồng). 
  Use when user asks to: tra cứu mã số thuế, ghi thông tin công ty vào sheet, tạo hợp đồng, 
  thêm dữ liệu doanh nghiệp từ masothue, hoặc yêu cầu format: "MST + Số tiền + Dịch vụ" để điền sheet.
---

# Tạo Hợp Đồng (taohopdong)

Tra cứu thông tin doanh nghiệp từ [masothue.com](https://masothue.com) và ghi vào Google Sheet **Hợp đồng**.

> **Yêu cầu:** `gog` CLI đã authenticated, env `GOG_ACCOUNT` được set, và Odoo connector sẵn sàng (`~/clawd/skills/odoo-connector`).

## Sheet Structure

- **Spreadsheet ID**: ``
- **Sheet name**: `` (gid: ``)
- **Header row**: dòng 4
- **Dữ liệu bắt đầu**: dòng 5 trở đi

### Column layout

| Cột | Nội dung | Ví dụ |
|:---:|:---------|:------|
| **A** | Mã (MST) | `0316863281` |
| **C** | Mã hợp đồng | `W231224/SEO` |
| **D** | Tên doanh nghiệp | CÔNG TY CP CN WIFIM |
| **E** | Địa chỉ | ... |
| **F** | Mã số thuế | `00316863281` |
| **G** | Người đại diện | Nguyễn Lê Minh Dương |
| **H** | SĐT | *(trống nếu không có)* |
| **I** | Số tiền | `14.000.000` |
| **J** | Dịch vụ | `SEO` |

### Google Sheets via gog CLI

Dùng `gog` để đọc/ghi sheet. Set env `GOG_ACCOUNT` trước:
```bash
export GOG_ACCOUNT=""
```

**Đọc dữ liệu hiện có:**
```bash
gog sheets get  "Hợp đồng!A4:J" --json --no-input
```

**Ghi (cập nhật specific range):**
```bash
gog sheets update  \
  "Hợp đồng!A5:J5" \
  --values-json '[["0312712411","","W231224/SEO","TÊN CÔNG TY","Địa chỉ","0312712411","NGƯỜI ĐD","","14.000.000","SEO"]]' \
  --input USER_ENTERED \
  --no-input
```

> **Lưu ý:** `gog` tự xử lý encoding tên sheet tiếng Việt, không cần URL-encode thủ công.

## Input Format

User có thể cung cấp thông tin theo các format sau:

1. **Link masothue.com đầy đủ**:
   `

2. **Chỉ MST** (tự động ghép URL):
   `0314927902` → `https://masothue.com/{mst}`

3. **Cú pháp đầy đủ 1 dòng**:
   `{Mã HĐ} {URL/MST} {Số tiền} {Dịch vụ}`
   Ví dụ: `W231224/SEO https://masothue.com/0314927902... 14.000.000 SEO`

## Workflow

### Bước 1: Xác định MST và URL masothue

- Nếu user gửi full URL (slug) → dùng luôn
- Nếu user gửi MST số → dùng search URL:
  `https://masothue.com/Search/?q={mst}&type=masothue`
  → web_fetch sẽ tự redirect sang slug đúng
- Nếu user gửi cả mã HĐ + URL + số tiền + dịch vụ → parse từng phần

> **Lưu ý:** URL trần `https://masothue.com/{mst}` (chỉ số) **không redirect** — sẽ 404. Luôn dùng search URL hoặc slug đầy đủ.

### Bước 2: Scrape masothue.com

Dùng `web_fetch` với URL masothue (search URL hoặc full slug). Parse kết quả để lấy:

| Field | Pattern trong web_fetch output |
|-------|-------------------------------|
| **Tên công ty** | Dòng đầu tiên sau title (thường là tên in hoa) |
| **Mã số thuế** | Dòng có `Mã số thuế` → value bên dưới |
| **Địa chỉ** | Dòng `Địa chỉ` (không phải `Địa chỉ Thuế`) → value |
| **Người đại diện** | Dòng có `Người đại diện` → tên trong `[]` |

Ưu tiên **Địa chỉ** (address thật) hơn **Địa chỉ Thuế** (tax address).

### Bước 3: Tìm dòng trống tiếp theo trong sheet

Dùng `gog` để đọc dữ liệu hiện tại:
```bash
gog sheets get  "Hợp đồng!A4:J" --json --no-input
```

Tìm dòng cuối có dữ liệu trong cột A (MST). Dòng tiếp theo là `rowNum = lastRow + 1`.

### Bước 4: Ghi vào Google Sheet

Ghi range `Hợp đồng!A{rowNum}:J{rowNum}` với:

```python
values = [[
    mst,           # A - Mã (MST)
    "",            # B - (nếu có)
    ma_hop_dong,   # C - Mã hợp đồng
    ten_cong_ty,   # D - Tên doanh nghiệp
    dia_chi,       # E - Địa chỉ
    mst,           # F - Mã số thuế (lặp lại)
    nguoi_dai_dien,# G - Người đại diện
    "",            # H - SĐT
    so_tien,       # I - Số tiền
    dich_vu        # J - Dịch vụ
]]
```

Lệnh gog:
```bash
gog sheets update  \
  "Hợp đồng!A${rowNum}:J${rowNum}" \
  --values-json '[[mst,"",ma_hop_dong,ten_cong_ty,dia_chi,mst,nguoi_dai_dien,"",so_tien,dich_vu]]' \
  --input USER_ENTERED \
  --no-input
```

**Cảnh báo:** Luôn ghi đủ A:J để giữ nguyên các cột D-G (tên, địa chỉ, MST, người đại diện) đã có. Không ghi range C:J riêng lẻ.

### Bước 5: Verify

Đọc lại dòng vừa ghi để xác nhận:
```bash
gog sheets get  \
  "Hợp đồng!A${rowNum}:J${rowNum}" --json --no-input
```

Thông báo ngắn gọn: **Dòng {rowNum} Đã thêm thành công**

### Bước 6 (Tự động): Tạo khách hàng trên Odoo CRM

Sau khi ghi sheet, tự động tạo (hoặc cập nhật) khách hàng (`res.partner`) trên Odoo với thông tin doanh nghiệp vừa tra cứu.

**Kiểm tra trùng:** Tra cứu `res.partner` theo `vat` (MST) trước. Nếu đã tồn tại thì bỏ qua, không tạo trùng.

```python
import sys
sys.path.insert(0, '~/clawd/skills/odoo-connector')
from odoo_skill.client import OdooClient

client = OdooClient()

# Kiểm tra đã có partner với MST này chưa
existing = client.search_read('res.partner', [['vat', '=', mst]], fields=['id', 'name'])

if not existing:
    partner_id = client.create('res.partner', {
        'name': ten_cong_ty,
        'vat': mst,
        'street': dia_chi,
        'phone': sdt or '',       # nếu có SĐT từ masothue
        'is_company': True,
        'company_type': 'company',
    })
    print(f'✅ Odoo Partner #{partner_id}: {ten_cong_ty}')
else:
    print(f'ℹ️ Đã tồn tại partner #{existing[0]["id"]}: {existing[0]["name"]} — bỏ qua')
```

> **Lưu ý:** Nếu user có cung cấp SĐT riêng (trong input), ưu tiên dùng SĐT đó thay vì SĐT từ masothue.

### Bước 7 (Tự động): Tạo cơ hội trên Odoo CRM

Sau khi tạo (hoặc tìm thấy) partner, tự động tạo một `crm.lead` (opportunity) ở stage **Hợp Đồng Mẫu** (ID: 5) để theo dõi hợp đồng này.

```python
import sys
sys.path.insert(0, '~/clawd/skills/odoo-connector')
from odoo_skill.client import OdooClient

client = OdooClient()

opp_id = client.create('crm.lead', {
    'name': f'{ma_hop_dong} - {dich_vu} - {ten_cong_ty_ngan}',  # VD: "W21/256565/SEO - SEO - Bao Bì Rồng Việt"
    'partner_id': partner_id,                     # ID từ Bước 6
    'contact_name': nguoi_dai_dien or '',
    'type': 'opportunity',
    'stage_id': 5,                                # Hợp Đồng Mẫu
    'expected_revenue': so_tien_so,               # số tiền dạng số, VD: 14000000
    'probability': 50,
})
print(f'✅ Odoo Opp #{opp_id}: {ma_hop_dong} - {dich_vu} - {ten_cong_ty_ngan}')
```

> **Lưu ý:** `so_tien_so` là số tiền dạng integer (VD: `14000000`), parse từ `so_tien` string (VD: `"14.000.000"`). `ten_cong_ty_ngan` là tên công ty rút gọn (bỏ "CÔNG TY TNHH"... để tên opportunity gọn hơn) — có thể lấy nguyên tên đầy đủ nếu muốn đơn giản. Tên opportunity theo format `{Mã HĐ} - {Dịch vụ} - {Tên}`.

## Edge Cases

- **MST bắt đầu bằng số 0** (VD: `0312712411`): Google Sheets có thể ăn mất số 0 nếu ghi dạng số. Luôn dùng `--input USER_ENTERED` và truyền dạng string `"0312712411"` để giữ nguyên số 0.
- **Dữ liệu đã tồn tại**: Kiểm tra MST trong sheet trước khi ghi để tránh trùng.
- **Không tìm thấy masothue**: Thử search Google với format `"mã số thuế {mst}"` hoặc báo user.

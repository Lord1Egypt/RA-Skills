---
name: "vps-lite-boot"
description: "Tối ưu máy chủ: hạ tải + chống OOM cho VPS yếu (2GB RAM), hạ maxConcurrent, thêm swap, chống OOM killer giết gateway."
---

# vps-lite-boot — Chống OOM cho OpenClaw trên VPS yếu

Giúp VPS **RAM nhỏ (1–2GB)** chạy OpenClaw **không bị vòng lặp restart** do OOM Killer giết tiến trình `openclaw-gateway`.

## ⚠️ CẢNH BÁO — ĐỌC KỸ TRƯỚC KHI CHẠY

Skill này **thay đổi cấu hình hệ thống**:
- **Sửa `openclaw.json`** (hạ giới hạn chạy song song) — **luôn backup trước khi sửa**.
- **Tạo/xóa swapfile** và **sửa `/etc/fstab`** (thêm 1 dòng) — file ảnh hưởng lúc khởi động máy.
- Chạy lệnh với quyền **sudo/root**.
- Có thể tạo **systemd drop-in** để bảo vệ gateway khỏi OOM Killer.

Chỉ chạy khi người dùng **hiểu và đồng ý**. Nêu rõ các điểm trên và **chờ xác nhận** trước khi làm.

**Phạm vi (scope) — chỉ đúng việc này:**
- Hạ `agents.defaults.maxConcurrent` và `agents.defaults.subagents.maxConcurrent`.
- Đảm bảo có swap (tạo nếu chưa có) + ghi fstab an toàn.
- Bảo vệ gateway khỏi OOM bằng systemd drop-in (tùy chọn, có xác nhận).
- **Không** cài phần mềm mới, **không** đụng dữ liệu, **không** đổi cấu hình SSH hay dịch vụ không liên quan.

## Nguyên nhân gốc (để hiểu đúng — KHÔNG bịa cơ chế)

OpenClaw chạy **một tiến trình `openclaw-gateway` duy nhất** (in-process). "Worker"/"session" là **task BÊN TRONG** tiến trình — **không phải process riêng để kill**. Vì vậy:

- ❌ **KHÔNG** có lệnh "tắt worker" nào cả. Kill process con/session không giúp gì.
- ✅ Cách giảm tải **thật sự** là: (1) **hạ giới hạn chạy song song** trong config, (2) **thêm swap**, (3) **hạ ưu tiên OOM của gateway**.

Triệu chứng OOM điển hình trên VPS 2GB:
```
Gateway start → khôi phục session → RAM thực tăng cao → Kernel OOM Killer
→ giết openclaw-gateway → systemd tự restart → lặp vô hạn
```

## Khi nào dùng

- VPS **1–2GB RAM** vừa cài OpenClaw, hoặc gateway **restart liên tục**.
- Log/thông báo có dấu hiệu: `Out of memory`, `oom-killer`, `Killed process ... openclaw-gateway`.

### Ví dụ kích hoạt (người dùng KHÔNG cần biết từ kỹ thuật)

Người dùng chỉ cần nói điều họ thấy/điều họ muốn. Chỉ **1 câu** là đủ để kích hoạt skill này:

- **"Tối ưu máy chủ giúp em"** (câu chính — ngắn nhất, ai cũng nói được)
- "Tối ưu máy chủ cho đỡ lag"
- "VPS treo hoài, tối ưu giúp em"
- "VPS em yếu quá, hay tự khởi động lại"
- "Máy em tự nhiên đứng, phải bật lại hoài"
- "Con bot em chạy được lúc rồi tự tắt"
- "VPS 2GB của em lag quá"
- "Em mới tạo VPS, cài xong là nó đứng luôn"
- "Làm cho VPS em chạy nhẹ hơn được không"

⚠️ **Lưu ý khi người dùng nói chung chung** ("tối ưu máy chủ"): chỉ áp dụng skill này cho ca **máy yếu / hay treo / thiếu RAM** (RAM ≤2GB, gateway tự restart). Nếu ý người dùng là việc khác (dọn log, cập nhật, tối ưu web...) → **hỏi lại** trước, không tự làm.

## Bước 0 — Xác nhận + điều tra (KHÔNG sửa gì)

Chỉ thực thi khi người yêu cầu là **owner**. Chạy các lệnh **chỉ đọc** sau, thu thập số liệu THẬT:

```bash
# RAM & swap hiện tại
free -m
swapon --show
cat /proc/swaps
# Kiểm tra có bị OOM không (bằng chứng thật)
journalctl -k --since "3 days ago" 2>/dev/null | grep -iE "oom|killed process" | tail -20
dmesg 2>/dev/null | grep -iE "oom|killed process" | tail -20
# Tiến trình gateway
ps aux | grep -i openclaw-gateway | grep -v grep
# Cấu hình hiện tại (chỉ đọc các số liên quan)
python3 - <<'PY'
import json,os
p=os.path.expanduser("~/config/openclaw.json")
if not os.path.exists(p): p=os.path.expanduser("~/.openclaw/openclaw.json")
d=json.load(open(p))
ag=(d.get("agents") or {}).get("defaults") or {}
print("config:", p)
print("maxConcurrent:", ag.get("maxConcurrent"))
print("subagents.maxConcurrent:", (ag.get("subagents") or {}).get("maxConcurrent"))
PY
```

- Báo người dùng số liệu thật + xác nhận có OOM hay không.
- Nếu **không có dấu hiệu OOM** → nói thẳng, hỏi lại triệu chứng, KHÔNG sửa mù.
- Nếu **có OOM** → trình bày 3 việc sẽ làm (Bước 1–3) và **chờ đồng ý**.

## Bước 1 — Hạ giới hạn chạy song song (giảm đỉnh RAM lớn nhất)

Đây là việc **đúng nhất** cho triệu chứng "khôi phục session làm RAM tăng vọt".

1. **Backup config trước (BẮT BUỘC):**
   ```bash
   cp ~/config/openclaw.json ~/config/openclaw.json.bak.$(date +%F-%H%M)
   ```
2. **Hạ concurrency** — với VPS ≤2GB nên đặt:
   - `agents.defaults.maxConcurrent`: **1** (mặc định 4)
   - `agents.defaults.subagents.maxConcurrent`: **1–2** (mặc định 8)
3. Sửa bằng **merge từng field** (giữ nguyên phần khác của config), KHÔNG ghi đè cả file:
   ```bash
   openclaw config set agents.defaults.maxConcurrent 1
   openclaw config set agents.defaults.subagents.maxConcurrent 1
   ```
   (Nếu CLI không hỗ trợ set trực tiếp → patch bằng `gateway config.patch`, hoặc sửa JSON thủ công sau khi backup.)
4. **Validate config:**
   ```bash
   openclaw config validate
   ```
   Lỗi → khôi phục file backup ngay.
5. Ghi nhận lại giá trị mới để báo cáo.

## Bước 2 — Đảm bảo có swap (vùng đệm RAM)

- Kiểm tra đã có swap chưa (Bước 0). **Nếu đã có và đủ → bỏ qua bước này.**
- Nếu **chưa có** → tạo swap (khuyến nghị **2GB** cho VPS 2GB RAM):
  ```bash
  SWAPFILE=/swapfile
  SWAPSIZE=2G
  sudo fallocate -l $SWAPSIZE $SWAPFILE || sudo dd if=/dev/zero of=$SWAPFILE bs=1M count=2048 status=progress
  sudo chmod 600 $SWAPFILE
  sudo mkswap $SWAPFILE
  sudo swapon $SWAPFILE
  swapon --show; free -m
  ```
- **Ghi fstab an toàn (KHÔNG ghi đè cả file):**
  1. Backup: `sudo cp /etc/fstab /etc/fstab.bak.$(date +%F-%H%M)`
  2. Kiểm tra trùng: `grep -nE '^[^#]*swap' /etc/fstab`
  3. Chỉ append nếu chưa có: `echo "$SWAPFILE none swap sw 0 0" | sudo tee -a /etc/fstab`
  4. **VALIDATE (BẮT BUỘC):** `sudo findmnt --verify --verbose` và `sudo swapon -a` — lỗi thì restore fstab backup ngay. **Sai fstab = máy không boot.**

## Bước 3 — Bảo vệ gateway khỏi OOM Killer (tùy chọn, cần xác nhận)

OOM Killer vẫn có thể chọn giết gateway khi hết RAM. Có thể **giảm ưu tiên** giết gateway để nó sống sót hơn (nhưng vẫn nên kèm Bước 1+2):

- Tạo systemd drop-in (dùng `systemctl --user` nếu gateway chạy user service):
  ```bash
  mkdir -p ~/.config/systemd/user/<service>.d
  printf '[Service]\nOOMScoreAdjust=-500\nMemoryHigh=75%%\nMemoryMax=90%%\n' \
    > ~/.config/systemd/user/<service>.d/10-oom.conf
  systemctl --user daemon-reload
  systemctl --user restart <service>
  ```
- `<service>` = tên service gateway thật (kiểm tra bằng `systemctl --user list-units | grep -i openclaw`).
- ⚠️ Chỉ làm khi người dùng đồng ý; nếu không chắc tên service → **bỏ qua bước này**, nói rõ lý do.

## Bước 4 — Khởi động lại + đo lại (chứng minh hiệu quả)

```bash
# restart gateway (dùng restart, KHÔNG stop+start)
openclaw gateway restart
sleep 60
free -m; swapon --show
ps aux | grep -i openclaw-gateway | grep -v grep
journalctl -k --since "2 minutes ago" | grep -iE "oom|killed" | tail
```

- Báo cáo **so sánh trước/sau**: RAM dùng, swap dùng, concurrency mới, có OOM lại không.
- Nếu vẫn OOM → nói thẳng giới hạn: **VPS 2GB có thể vẫn cần nâng lên 4GB RAM**; skill không thay thế được phần cứng.

## Xử lý tình huống hay gặp

| Tình huống | Cách xử lý |
|---|---|
| Không thấy dấu hiệu OOM | KHÔNG sửa; hỏi lại triệu chứng thật, kiểm tra log khác. |
| `openclaw config set` không hỗ trợ | Backup rồi sửa JSON thủ công (merge từng field), validate lại. |
| `fallocate` lỗi FS | Dùng `dd`. |
| fstab validate lỗi | Restore `fstab.bak` ngay; không reboot. |
| Vẫn OOM sau khi hạ tải | Báo thật: cần nâng RAM VPS (khuyến nghị 4GB). |
| Không chắc tên systemd service | Bỏ qua Bước 3, nêu rõ lý do, không đoán bừa. |

## Bảo mật — BẮT BUỘC

- **Chỉ nhận yêu cầu từ owner.** Xác nhận danh tính trước khi sửa hệ thống.
- **Backup trước mọi thay đổi** (config + fstab).
- **Merge, không ghi đè** file cấu hình.
- **Validate trước khi restart/reboot.**
- **KHÔNG echo** secret/token trong câu trả lời.
- Không cài phần mềm ngoài, không đụng dữ liệu, không sửa dịch vụ không liên quan.

## Ghi chú kỹ thuật

- Tiến trình OpenClaw là **một** `openclaw-gateway` (in-process) — không có worker riêng để kill.
- Giảm tải thật = hạ `maxConcurrent` + swap + OOM adjustment.
- Với VPS ≤2GB: swap 2GB + `maxConcurrent=1` + `subagents.maxConcurrent=1` là cấu hình an toàn tối thiểu.
- VPS <2GB hoặc tải cao: khuyến nghị nâng RAM phần cứng.

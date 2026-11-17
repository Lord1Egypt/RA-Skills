---
name: "swap-setup"
description: "\"Thêm swap cho VPS qua chat, không cần terminal: agent sinh SSH key dùng một lần, người dùng dán public key vào panel, agent tạo swap.\""
---

# swap-setup — Thêm swap cho VPS qua chat (không cần terminal)

Giúp người dùng **không rành kỹ thuật** thêm dung lượng swap cho VPS mà **không phải gõ lệnh**. Người dùng chỉ làm **một việc duy nhất bằng click chuột** (dán public key vào panel VPS).

## ⚠️ CẢNH BÁO — ĐỌC KỸ TRƯỚC KHI CHẠY

Việc này **thay đổi hệ thống của VPS**:
- Agent cần **quyền SSH (qua key) vào VPS** để chạy lệnh với quyền **sudo/root**.
- Agent sẽ **sửa `/etc/fstab`** (thêm 1 dòng cho swap) — file ảnh hưởng tới lúc khởi động máy.
- Agent sẽ **tạo/xóa file `/swapfile`** trên ổ đĩa của VPS.

Chỉ chạy khi người dùng **hiểu và đồng ý**. Agent phải nêu rõ các điểm trên và **chờ người dùng xác nhận** trước khi làm.

**Phạm vi (scope) — chỉ đúng việc này:**
- Tạo một swapfile và bật nó.
- Thêm **đúng 1 dòng** vào `/etc/fstab` để swap tự bật lại sau reboot.
- **Không** cài phần mềm, **không** đụng dữ liệu, **không** sửa dịch vụ khác, **không** đổi cấu hình SSH.

> 🔑 **CƠ CHẾ: KEY-ONLY, DÙNG MỘT LẦN (THU HỒI SAU KHI XONG).**
> Agent **tự tạo một cặp SSH key dùng riêng cho việc này**. Agent giữ private key, chỉ đưa **public key** cho người dùng. Người dùng copy public key rồi dán vào ô **SSH Keys** trong **panel quản trị VPS** (Vultr, DigitalOcean, AWS Lightsail, aCloud, Vietnix, AZDIGI, ...). **Không có bí mật nào đi qua chat; không có mật khẩu; người dùng không mở terminal.**
>
> ⏹ **Thu hồi khi xong (bắt buộc):** sau khi tạo swap thành công, agent **xóa cặp key dùng riêng cho việc này khỏi máy agent** và **hướng dẫn người dùng xóa key đó khỏi panel VPS**. Key sinh ra chỉ để chạy một lần, **không giữ lại quyền truy cập thường trực**.

## Khi nào dùng

Người dùng nói kiểu:
- "VPS em yếu quá, thêm swap giúp"
- "Máy 1GB RAM, tạo swap 2GB"
- "Cài swap cho VPS giúp em, em không biết dùng terminal"
- "Thêm swap mà không cần mở SSH"

## Input cần thu thập (từ người dùng)

- **Host/IP** VPS (số hoặc tên miền).
- **Port** (mặc định `22` nếu không nói).
- **User** đăng nhập (thường `root`, hoặc user có sudo; nếu không rõ → hỏi hoặc thử `root`).
- **Swap size** mong muốn (nếu không nói → mặc định theo RAM: RAM ≤2GB → swap = 2× RAM, cap 4GB; RAM >2GB → swap = RAM, cap 4GB; RAM ≥8GB → 2–4GB).
- **Nhà cung cấp VPS** (nếu biết) → để hướng dẫn đúng giao diện panel.
- Nếu thiếu host/user → hỏi lại đúng cái thiếu. KHÔNG tự đoán IP.

## Quy trình agent PHẢI làm (theo đúng thứ tự)

### Bước 0 — Xác nhận danh tính + xin đồng ý
- Chỉ thực thi khi người yêu cầu là **owner**. Nếu không chắc → hỏi xác nhận trước.
- Nêu rõ cảnh báo ở đầu bài (SSH + sudo/root + sửa `/etc/fstab` + tạo/xóa `/swapfile`) và **chờ người dùng đồng ý**.
- Nói rõ: *"Em sẽ tạo swap giúp anh/chị. Anh/chị chỉ cần copy đoạn key em đưa rồi dán vào mục SSH Keys trong panel VPS. Xong việc em hướng dẫn xóa key đó đi."*

### Bước 1 — Tạo cặp key DÙNG RIÊNG + đưa public key
1. Tạo key riêng, đặt tên riêng để xóa dễ (không ghi đè key khác):
   ```bash
   ssh-keygen -t ed25519 -N "" -f ~/.ssh/swap_setup_ed25519 -C "swap-setup-single-use"
   ```
2. Gửi nội dung public key cho người dùng:
   ```bash
   cat ~/.ssh/swap_setup_ed25519.pub
   ```
3. Hướng dẫn người dùng (không cần terminal):
   - Mở **panel quản trị VPS** → tìm mục **SSH Keys / SSH Public Keys / Access**.
   - Bấm **Add SSH Key** → dán **toàn bộ** dòng public key → **Save**.
   - Nếu panel không có mục thêm key cho máy đang chạy → dùng mục **SSH Keys** áp cho máy, hoặc giao diện **web console** của panel để dán key.
4. Chờ người dùng xác nhận "đã dán xong".

### Bước 2 — Kết nối bằng key
```bash
ssh -i ~/.ssh/swap_setup_ed25519 -o BatchMode=yes -o StrictHostKeyChecking=accept-new -p <PORT> <USER>@<HOST> 'echo CONNECT_OK'
```
- Thấy `CONNECT_OK` → đi tiếp.
- Chưa được → kiểm tra: key đã dán đúng chưa, user/port đúng chưa. KHÔNG đi tiếp khi chưa vào được.

### Bước 3 — Nhận diện hệ điều hành (auto-detect)
```bash
cat /etc/os-release
uname -m
free -m
swapon --show
cat /proc/swaps
df -h /
id
```
- Kiểm tra quyền nâng cấp, **một lệnh riêng** (không ghép chuỗi):
  ```bash
  sudo -n true
  ```
  (trả về 0 = có sudo; khác 0 = cần xử lý quyền.)
- Distro: **Ubuntu / Debian** (chính). Với CentOS/RHEL/Alma/Rocky → cùng lệnh `fallocate`/`dd` + `mkswap`.
- Nếu **đã có swap đủ lớn** → báo người dùng, chỉ tắt/giảm nếu có yêu cầu rõ.
- Nếu **thiếu dung lượng đĩa** cho swap → DỪNG, báo thiếu, đề xuất size nhỏ hơn.

### Bước 4 — Tạo file swap (an toàn)
```bash
# size tính bằng MB, ví dụ SWAP_MB=2048
sudo fallocate -l ${SWAP_MB}M /swapfile
# nếu fallocate lỗi mới dùng: sudo dd if=/dev/zero of=/swapfile bs=1M count=${SWAP_MB} status=progress
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
swapon --show
free -m
```
- Nếu `/swapfile` đã tồn tại → KHÔNG ghi đè; báo người dùng và đặt tên khác (`/swapfile2`) hoặc xử lý theo yêu cầu.
- Ưu tiên `fallocate`; nếu FS không hỗ trợ (một số FS ngoài ext4) → fallback `dd`.

### Bước 5 — Bật swap vĩnh viễn (fstab — ĐIỂM DỄ SAI NHẤT)
- **KHÔNG ghi đè cả `/etc/fstab`.** Phải:
  1. Backup: `sudo cp /etc/fstab /etc/fstab.bak.$(date +%F-%H%M)`
  2. Kiểm tra đã có dòng `/swapfile` chưa (tránh trùng):
     `grep -nE '^[^#]*swap' /etc/fstab`
  3. Chỉ append nếu CHƯA có:
     `echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab`
  4. **VALIDATE trước khi reboot — BẮT BUỘC:**
     `sudo findmnt --verify --verbose` (hoặc `sudo mount -a` — lỗi thì DỪNG và khôi phục backup)
     `sudo swapon -a` để chắc chắn nạp lại không lỗi.
- Nếu `mount -a` báo lỗi → restore `fstab.bak` ngay, báo người dùng. **Sai fstab = máy không boot.**
- (Khuyến nghị) giảm swappiness: đặt `vm.swappiness=10` qua `/etc/sysctl.d/99-swap.conf`, rồi `sudo sysctl --system`.

### Bước 6 — THU HỒI KEY (bắt buộc — không để lại quyền truy cập thường trực)
1. Kiểm tra swap đã bật ổn: `swapon --show` + `free -m`.
2. Xóa cặp key dùng riêng khỏi máy agent:
   ```bash
   rm -f ~/.ssh/swap_setup_ed25519 ~/.ssh/swap_setup_ed25519.pub
   ```
3. Hướng dẫn người dùng **xóa key khỏi panel VPS** (mục SSH Keys → Remove/Xóa key vừa thêm).
4. Xác nhận lại swap vẫn chạy sau khi thu hồi (swap không phụ thuộc key).
- Nếu người dùng muốn agent kiểm tra lại sau này → tạo key mới theo quy trình này, không giữ key cũ.

### Bước 7 — Báo cáo
- Báo ngắn gọn: swap đã bật (size, `free -m` sau khi xong), fstab đã validate, **key đã thu hồi**.
- Nhắc: *"Anh/chị nhớ vào panel xóa key vừa dán nhé. Xong rồi, máy đã có swap."*
- KHÔNG echo bí mật/token nào ra chat.

## Xử lý tình huống hay gặp

| Tình huống | Cách xử lý |
|---|---|
| Kết nối báo Permission denied | Key chưa dán đúng / sai user/port → hướng dẫn lại, kiểm tra panel. |
| VPS không có panel SSH key | Hướng dẫn dán public key qua giao diện **web console** của panel. |
| `fallocate` lỗi FS | Dùng `dd if=/dev/zero of=/swapfile bs=1M count=N status=progress`. |
| `swapon` báo đã có swap | Báo người dùng, hỏi muốn tăng hay giữ nguyên. |
| `mount -a` báo lỗi | Restore fstab.bak NGAY; sửa lại cú pháp; validate lại. |
| User không có sudo | Hỏi thông tin admin hoặc dùng sudo có sẵn. |
| Sai tên nhà cung cấp panel | Hỏi lại tên panel để hướng dẫn đúng mục SSH Keys. |

## Rolling back (nếu cần)

- Tắt swap: `sudo swapoff /swapfile` → xóa dòng trong fstab → `sudo rm /swapfile`.

## Bảo mật — BẮT BUỘC

- **Chỉ nhận thông tin kết nối từ owner.** Xác nhận danh tính trước khi kết nối.
- **Chỉ dùng key, dùng một lần.** Không nhận, không dùng, không lưu mật khẩu.
- Tạo key **riêng biệt** cho việc này; **xóa key sau khi xong**; hướng dẫn người dùng xóa key khỏi panel.
- Private key agent giữ kín; chỉ gửi **public key**. Public key không phải bí mật.
- **KHÔNG echo** bí mật/token trong câu trả lời; không ghi ra file ngoài `~/.ssh`.
- Không chạy lệnh phá hoại; không xóa dữ liệu; không đụng dịch vụ khác ngoài việc tạo swap.
- Không tự ý đổi size/cấu hình khác ngoài yêu cầu.

## Ghi chú kỹ thuật

- Tạo key: `ssh-keygen -t ed25519 -N "" -f <path>` (không passphrase, phục vụ tự động hóa).
- Test kết nối: `-o BatchMode=yes` để tránh treo; `-o StrictHostKeyChecking=accept-new` cho lần đầu.
- `fallocate` nhanh nhưng một số FS (ZFS, một số XFS) có thể lỗi → `dd` chậm hơn nhưng chắc.
- Tách riêng từng lệnh; mỗi bước validate kết quả trước khi sang bước sau.

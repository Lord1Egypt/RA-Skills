# swap-setup

**Mục đích:** Thêm dung lượng swap cho VPS qua chat, **không cần mở terminal**.

## Cách hoạt động
- Agent tự tạo một cặp SSH key dùng riêng cho việc này.
- Người dùng chỉ cần copy **public key** rồi dán vào mục **SSH Keys** trong panel quản trị VPS (click chuột).
- Agent vào VPS bằng key → tạo swapfile → ghi fstab an toàn (có backup + validate).
- **Xong việc: agent xóa key, người dùng xóa key khỏi panel** — không để lại quyền truy cập thường trực.

## Phạm vi
- Chỉ tạo swap + 1 dòng fstab. Không cài phần mềm, không đụng dữ liệu, không sửa dịch vụ khác.

## Tính năng an toàn
- Chỉ dùng SSH key, không dùng mật khẩu.
- Key dùng một lần, thu hồi sau khi hoàn tất.
- Không ghi đè `/etc/fstab`: luôn backup + append.
- Validate fstab (`findmnt --verify` / `mount -a`) trước khi cúdùng lại.
- Private key giữ kín ở phía agent; chỉ chia sẻ public key.

## Yêu cầu
- VPS Linux có panel quản trị hỗ trợ SSH Keys (Vultr, DigitalOcean, Lightsail, aCloud, Vietnix, AZDIGI, ...).
- User có quyền sudo/root.
- Ubuntu/Debian (chính); hỗ trợ CentOS/RHEL.

## Ví dụ kích hoạt
- "VPS em yếu quá, thêm swap giúp"
- "Máy 1GB RAM, tạo swap 2GB, em không biết dùng terminal"

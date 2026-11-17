# Sử dụng swap-setup

## Tóm tắt
Thêm swap cho VPS mà người dùng không phải mở terminal: agent tạo SSH key, người dùng dán public key vào panel VPS, agent tạo swap rồi thu hồi key.

## Điều kiện
- VPS Linux (Ubuntu/Debian chính; hỗ trợ CentOS/RHEL).
- Có quyền sudo/root.
- Panel VPS hỗ trợ quản lý SSH Keys.

## Các bước
1. Agent tạo cặp SSH key dùng riêng và đưa public key.
2. Người dùng dán public key vào panel VPS (SSH Keys).
3. Agent kết nối bằng key và tạo swapfile.
4. Agent ghi 1 dòng vào `/etc/fstab` (có backup + validate).
5. Agent và người dùng thu hồi key sau khi xong.

## Lưu ý
- Không dùng mật khẩu.
- Không giữ quyền truy cập thường trực.
- Nếu muốn kiểm tra lại sau này, tạo key mới theo quy trình.

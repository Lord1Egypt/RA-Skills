## Agent Của Bạn Đã Bao Giờ Im Lặng?

Hết số dư API. DeepSeek giới hạn tốc độ. OpenAI sập. Agent của bạn đã làm được 80% — rồi im lặng.

Người dùng không hiểu hạ tầng. Họ chỉ biết "lại hỏng rồi". Ba lần là họ bỏ đi.

---

## Zero Token Làm Gì

Không phải "kế hoạch dự phòng". Không phải "chế độ suy giảm". Đây là **chuyển giao vô hình**.

Giây phút mô hình chính của bạn chết, 13 LLM miễn phí đã chạy sẵn. Cùng cá tính. Cùng quyết định. Cùng giọng nói. Không ai nhận ra sự chuyển đổi.

**0₫. Không gián đoạn. Không phát hiện.**

---

## Hai Dòng. Một Phút.

```bash
openclaw skills install zero-token
bash ~/.openclaw/workspace/skills/zero-token/scripts/setup.sh
```

Cổng [Free-Way](https://github.com/GoDiao/Free-Way) tổng hợp 13+ nhà cung cấp LLM miễn phí sau một endpoint `/v1` duy nhất. OpenClaw dùng nó làm fallback. Mô hình chính sập? → Tự động chuyển. Agent tiếp tục chạy.

---

## Hai Chế Độ

| Chế Độ | Điều Kiện | Kết Quả |
|--------|-----------|---------|
| 🆓 Miễn Phí | Không có API key trả phí | Agent chạy trên mô hình miễn phí, giữ nguyên cá tính SOUL |
| 🛡️ Chuyển Giao | Mô hình chính sập / hết token | Tự động chuyển sang nhà cung cấp miễn phí, công việc tiếp tục |

---

## Minh Bạch Hoàn Toàn

Zero Token không bao giờ che giấu việc chuyển đổi. Khi fallback kích hoạt, agent của bạn đang chạy trên nhà cung cấp miễn phí — không phải mô hình chính. Mỗi nhà cung cấp có chính sách bảo mật và lưu trữ dữ liệu riêng. **Xem xét điều khoản của từng nhà cung cấp trước khi gửi dữ liệu nhạy cảm.** Script cài đặt hiển thị rõ nhà cung cấp nào đang được cấu hình. Bạn kiểm soát các key.

> 💡 Đây là failover minh bạch, do bạn kiểm soát. Bạn giữ key. Bạn chọn nhà cung cấp.

---

## Miễn Phí ≠ Rác

Đầu ra thô của mô hình miễn phí bình thường. Nhưng với DNA hành vi `::GENE{}` bên trên — cùng cá tính, cùng quyết định, cùng giọng điệu. Không ai phân biệt được DeepSeek V4 Pro hay Llama 3.3 70B đang chạy.

---

## Tại Sao Miễn Phí

Free-Way + Zero Token là mã nguồn mở. Mỗi nhà cung cấp đều có gói miễn phí:

| Nhà Cung Cấp | Giới Hạn Miễn Phí | Mô Hình Tốt Nhất |
|-------------|------------------|-----------------|
| Groq | 1000 req/ngày | Llama 3.3 70B |
| Gemini Flash | 1500 req/ngày | Gemini 2.5 Flash |
| Cerebras | 1700 req/ngày | Llama 3.3 70B |
| Cloudflare | 10k neurons/ngày | Llama 3.1 8B |
| OpenRouter | 200 req/ngày | Nhiều mô hình miễn phí |
| Mistral | 1 req/giây | Mistral Small |
| Cohere | 20 req/phút | Command R+ |
| NVIDIA NIM | Gói miễn phí | Llama 3.3 70B |

Mỗi key mất 30 giây để đăng ký. Script cài đặt hướng dẫn từng bước.

---

## So Sánh

| | Thiết Lập Thông Thường | Zero Token |
|---|---|---|
| Chi Phí Mô Hình | $0.14–$15.00/M tokens | **$0.00** |
| Khi Sự Cố | Dừng hoàn toàn | Failover vô hình |
| Mô Hình Dự Phòng | 0 | 13+ |
| Cá Tính Agent | Mất khi fallback | Luôn nhất quán |
| Thời Gian Cài Đặt | Nửa ngày (cân bằng tải) | 1 phút |

---

## Khi Nào Nâng Cấp

Zero Token giữ bạn online. Để có chất lượng đầu ra tốt nhất — DeepSeek V4 Pro + bộ gen đầy đủ, giá 3% của Opus:

```bash
openclaw skills install poor-mans-opus
```

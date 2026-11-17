# 🚀 Giới Thiệu Skill `tvkh-sru-query` – Trợ Lý Tra Cứu Thư Viện Tỉnh Khánh Hòa Trên OpenClaw 🦀

Nếu bạn đang xây dựng các hệ thống AI, chatbot thông minh, hoặc đam mê tự động hóa và muốn kết nối trực tiếp với kho dữ liệu phong phú của **Thư viện tỉnh Khánh Hòa**, thì đây chính là công cụ dành cho bạn!

Hôm nay, chúng ta sẽ cùng khám phá cách kết hợp giữa **OpenClaw** (nền tảng trợ lý AI thông minh) với custom skill **`tvkh-sru-query`** để biến AI thành một "thủ thư số" thực thụ.

---

### 🔮 OpenClaw Là Gì?

**OpenClaw** là một nền tảng AI agent mã nguồn mở, cho phép tạo ra các trợ lý thông minh thực hiện nhiều tác vụ đa dạng. Tại sao OpenClaw lại đặc biệt?
*   🤖 **AI Agent thông minh:** Không chỉ trả lời câu hỏi mà còn *hành động* – tự tìm kiếm, phân tích và đưa ra kết quả có cấu trúc.
*   🧩 **Hệ thống Skill (Kỹ năng):** Mỗi skill là một công cụ chuyên biệt, dễ dàng cài đặt và chia sẻ qua ClawHub.
*   🔗 **Tích hợp đa nền tảng:** Hoạt động mượt mà trên Zalo, Telegram, Terminal... chỉ bằng ngôn ngữ tự nhiên.
*   🔒 **Quyền riêng tư:** Bạn hoàn toàn kiểm soát dữ liệu của mình.

---

### 🏛 Từ Z39.50 của PSC ZLIS đến cổng truy xuất mở SRU do IT tự phát triển

Hiện tại, Thư viện tỉnh Khánh Hòa đang vận hành trên nền tảng phần mềm quản lý thư viện chuyên dụng **PSC ZLIS**. Đi kèm với hệ thống này, nền tảng máy chủ tìm kiếm **Zebra** và giao thức mạng **Z39.50** đã được đơn vị cung cấp phần mềm cấu hình sẵn, đóng vai trò xương sống cho việc tra cứu liên thư viện và tải dữ liệu biểu ghi (chuẩn MARC) từ Thư viện Quốc gia Việt Nam.

Tuy nhiên, Z39.50 là một giao thức Client-Server khá "đặc thù" và đóng kín. Nhận thấy sự cần thiết phải "giải phóng" khối lượng dữ liệu khổng lồ này để bắt nhịp với các ứng dụng công nghệ hiện đại, tôi đã chủ động nghiên cứu và **phát triển mở rộng thêm cổng SRU (Search/Retrieve via URL)** trên chính nền tảng Zebra sẵn có của thư viện.

Việc tự cấu hình và bổ sung endpoint SRU này đã khéo léo chuyển đổi các truy vấn Z39.50 nặng nề sang chuẩn web thân thiện (qua HTTP kết hợp cú pháp CQL). Đây chính là "chìa khóa" giúp các hệ thống tự động hóa và **AI Agent** có thể trực tiếp gọi API, đọc hiểu và trích xuất dữ liệu thư viện một cách trơn tru mà không bị bó hẹp trong khuôn khổ của phần mềm thư viện mặc định.

---

### 📚 Skill `tvkh-sru-query` Làm Được Gì?

Với skill này, AI Agent của bạn có thể giao tiếp trực tiếp với endpoint `/khanhhoa` để khai thác sâu vào cơ sở dữ liệu:
*   🔍 Tìm sách theo **từ khóa** bất kỳ (Python, lập trình, du lịch...).
*   ✍️ Tra cứu chính xác theo **nhan đề** (`dc.title="..."`) hoặc **tác giả** (`dc.creator="..."`).
*   🗂️ Nhận kết quả **có cấu trúc**: Tiêu đề, tác giả, nhà xuất bản, năm, giá tiền và vị trí kho (Kho địa chí, Kho mở...).

📖 **Ví Dụ Thực Tế Khi AI Truy Vấn:**
> **Người dùng hỏi Bot:** *"Tìm giúp mình sách về Tháp Bà Ponagar"*
> **AI gọi Skill và trả lời:** Liệt kê các chuyên khảo của Ngô Văn Doanh, Bố Xuân Hổ, kèm vị trí để đến mượn ngay tại thư viện.
> 
> **Người dùng hỏi Bot:** *"Tác giả Tô Hoài có sách gì?"*
> **AI gọi Skill và trả lời:** Tổng hợp danh sách chi tiết hàng trăm cuốn sách hiện có trong kho.

---

### 💡 Ai Nên Trải Nghiệm Skill Này?

Mặc dù hoạt động dưới dạng một module kỹ thuật của AI Agent, nhưng giá trị cốt lõi của `tvkh-sru-query` được sinh ra để phục vụ nhu cầu tra cứu thông tin thực tế:

*   🎓 **Sinh viên & Nghiên cứu sinh:** Tìm kiếm nhanh chóng các nguồn tài liệu học thuật, chuyên khảo văn hóa Champa, hay địa chí Nha Trang - Khánh Hòa phục vụ cho tiểu luận, đồ án.
*   📚 **Bạn đọc thư viện:** Chủ động "hỏi" AI xem cuốn sách mình cần có sẵn không, đang nằm ở kệ nào (Kho mở, Kho địa chí...) và giá trị bao nhiêu để tiết kiệm tối đa thời gian trước khi đến thư viện.
*   🤖 **Cộng đồng người dùng OpenClaw:** Bất kỳ ai muốn trải nghiệm biến trợ lý AI cá nhân trên thiết bị của mình thành một "thủ thư số" thực thụ, có khả năng giao tiếp và tra cứu hàng ngàn đầu sách chuẩn xác.
*   👨‍💻 **Nhà phát triển ứng dụng (Bonus):** Dễ dàng tận dụng skill này làm module lõi để xây dựng các chatbot tra cứu (Zalo OA, Telegram) phục vụ cộng đồng mà không cần tốn công xử lý lại giao thức SRU.

---

### 🚀 Cài Đặt Ngay

Skill hiện đã có mặt chính thức trên thư viện ClawHub. Khám phá chi tiết tại:
👉 **[ClawHub - tvkh-sru-query by baolinhtv](https://clawhub.ai/baolinhtv/skills/tvkh-sru-query)**

Chỉ với một câu lệnh đơn giản trên terminal nếu bạn đang vận hành OpenClaw:
```bash
openclaw skills install @baolinhtv/tvkh-sru-query
```

---

### 📦 Thông Tin Kỹ Thuật

| Thành phần | Chi tiết |
| :--- | :--- |
| **Tên Skill** | `tvkh-sru-query` |
| **Endpoint** | `https://sru.thuvienkhanhhoa.gov.vn/khanhhoa` |
| **Giao thức** | SRU (Z39.50) + YAZ backend + CQL |
| **Định dạng** | MARC21 XML → JSON |
| **Phần mềm lõi**| PSC ZLIS |
| **GitHub Repo** | [baolinhtv/openclaw-skill-sru-query](https://github.com/baolinhtv/openclaw-skill-sru-query) |
| **Tác giả** | baolinhtv (Trương Thanh Bảo Linh) |

---

🤝 **Đóng Góp Mã Nguồn:**
Dự án được mở mã nguồn hoàn toàn. Mọi đóng góp (báo lỗi, cải tiến, thêm tính năng) đều được hoan nghênh tại trang **[GitHub Issues](https://github.com/baolinhtv/openclaw-skill-sru-query/issues)**.

---
*🎉 Trải nghiệm sức mạnh tích hợp dữ liệu thư viện và AI cùng OpenClaw ngay hôm nay!* 🦀✨

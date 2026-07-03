---name: vn-guide
description: Hướng dẫn toàn diện — giải thích how/why, sửa lỗi người dùng, tối ưu pipeline viết gốc & dịch thuật với bộ kỹ năng kb-vn. Version dành cho người đã biết basics.
version: 1.0.0
author: KaibaZax
---


# vn-guide — Cẩm Nang Sử Dụng kỹ năng kb-vn


## Trước khi bắt đầu: Tư duy đúng

### Tại sao Agent bypass NSFW trong khi chat thường thì không?

Khi AI được huấn luyện làm Agent, nó học pattern "nhận skill → thực thi nhiệm vụ". Khi bạn gắn skill chuyên biệt (fullwrite, outline...), AI **tưởng nó đang làm Agent** — không phải "trò chuyện". Bộ lọc NSFW kích hoạt ở chế độ chat bị bỏ qua vì AI đang ở chế độ "làm việc". Đây là lý do skill hoạt động tốt hơn jailbreak — jailbreak tạo nhiễu attention, skill tạo khuôn khổ chuyên biệt.

**Hệ quả:** Đừng jailbreak. Dùng skill chuyên biệt cho từng task -> giảm nhiễu attention -> AI khôn hơn.

### Context window: Con số ảo

Đừng nhìn vào thông số context window. Thực tế khả dụng chỉ **~20%**. Phần còn lại là attention nhiễu, token padding, system prompt.

Pattern nhớ: **Đầu mạnh – giữa yếu – cuối mạnh**. AI nhớ nguyên văn ~20 message gần nhất. Phần giữa context nó tóm tắt và chế cháo — cho dù không yêu cầu.

| Model | Context công bố | Khả dụng thực tế | Ghi chú |
|-------|----------------|-----------------|---------|
| Gemini | Lớn nhất | Thấp nhất | Hành văn kiểu "tường thuật, tổng kết" |
| DeepSeek | Nhỏ hơn Gemini | Cao hơn Gemini | Đọc 20 chương không lỗi tình tiết |
| Z.ai (GLM) | Trung bình | Tốt | Việt ngữ tạm ổn |

**Giải pháp:** Chuyên biệt hóa task. Mỗi task/AI riêng → tiết kiệm attention → AI suy nghĩ sâu hơn.

### Temperature — hiểu cho đúng

- **Web:** Temp bị khoá hoặc ảnh hưởng rất hạn chế ở model mới
- **API:** Vẫn chỉnh được temp
- **Nhưng:** Temp không phải giải pháp cho văn phong dở. Vấn đề nằm ở **thiếu hướng dẫn chi tiết** và **thiếu cấu trúc dữ liệu** (markdown, lorebook, outline...)


## Bộ kỹ năng kb-vn (8 skill)

| Skill | Vai trò | Pipeline |
|-------|---------|----------|
| `vn-worldbuilding` | Xây lorebook — thế giới, nhân vật, hệ thống | Viết gốc — Bước 1 |
| `vn-outline` | Dàn ý chương + mô phỏng nhân vật (90% thoại sinh ra ở bước này) | Viết gốc — Bước 2 |
| `vn-povs` | Kiểm soát góc nhìn — fix "toàn tri" | Cả hai pipeline |
| `vn-fullwrite` | Dựng văn xuôi từ outline — cơ thể, cảm giác, nội tâm | Viết gốc — Bước 3 |
| `vn-lexicon` | Ngân hàng từ vựng cảm giác — compound phrase, xoay vần | Cả hai pipeline |
| `vn-lorefilter` | Lọc lore vào văn xuôi — không dump, chỉ touch qua cảm giác | Viết gốc — Bước 3 |
| `vn-translate` | Dịch truyện — split tại `\n` + TenRieng + XungHo | Dịch thuật |
| `vn-roleplay` | Nhập vai real-time (standalone) | Roleplay |


## PHẦN 1: CHỌN MODEL

**Quan trọng nhất:** Model quyết định 80% chất lượng. Skill chỉ là 20%.

### Thứ tự ưu tiên

```
DeepSeek (API)  →  Z.ai (GLM)  →  DeepSeek (chat web)
```

| Model | Dàn ý (Outline) | Fullwrite | Dịch thuật | NSFW | Ghi chú |
|-------|----------------|-----------|------------|------|---------|
| **DeepSeek API** | ★★★★★ | ★★★★★ | ★★★★★ | OK nhất | Rẻ, thông minh, không filter nặng |
| **Z.ai (GLM)** | ★★★ | ★★★★ | ★★★ | OK | Khá thoáng, hay quá tải |
| **DeepSeek chat** | ★★★★ | ★★★★ | ★★★★ | Gắt hơn API | Instance bị duyệt nhiều hơn Expert |
| **Gemini** | ★★★★★ | ★★ | ★★ | Đã chết | Hành văn kiểu báo cáo, toàn "tóm tắt", "tổng kết" |
| **Claude** | ★★★ | ★★★★★ | — | Tuỳ | Mắc |
| **Grok** | ★★ | ★ | — | Đang chết | Càng ngày càng dở |

### Flash vs Expert:
**Không dùng Flash model** — tụi nó ngu hơn nên bị kiểm duyệt nhầm. Luôn chọn Expert/Pro nếu có option.

### API DeepSeek:
- **Cực kỳ rẻ:** $0.1 ≈ 2600 VND, ngồi chat cả ngày không hết $1
- Mua trực tiếp trên [platform.deepseek.com](https://platform.deepseek.com/api_keys) — rẻ hơn OpenRouter 10 lần
- Cần thẻ Visa debit (cake, ngân hàng đều được)
- Hermes Desktop: miễn phí, chỉ tốn API key

### Không có PC? Dùng Agent đám mây:
[https://zwork.z.ai/](https://zwork.z.ai/) — Agent on cloud, có trả phí. Chạy trên server, không cần PC mạnh. Upload skill, lorebook, chat trực tiếp.


## PHẦN 2: GIẢI THÍCH THUẬT NGỮ

### Core (Core Idea) — cốt lõi

**Core** là thứ **người dùng tự viết**. Nó cực kỳ ngắn gọn — chỉ tình tiết chính, không trang trí.

```
Ví dụ Core cho 1 chương:
Chương 15: A đi học, gặp B. B ngứa mắt, B tát A. A khóc.
```

Tại sao gọi là "core"? Vì nó là **hạt nhân** — ý tưởng thô nhất. AI sẽ lấy core này để bung ra thành outline chi tiết.

**Core ≠ Lorebook.** Core là định hướng ngắn hạn (1 chương). Lorebook là kho thông tin dài hạn (thế giới, nhân vật).

**Tại sao không viết dài?** Vì càng ngắn thì AI càng có không gian để sáng tạo. Core chỉ là mồi — AI tự simulate phần còn lại.

**Core cho 50 chương:** Nếu viết core tóm tắt 50 chương (mỗi chương ~1 dòng) và cho AI theo dõi, nó sẽ nắm được mạch truyện dài. Outline thì khoảng 10 chương là tối đa.

### Outline — dàn ý chi tiết (do AI tạo từ Core)

Outline do AI sinh ra, là bản thiết kế có phân cảnh, đối thoại chính, mạch cảm xúc. 90% hội thoại được mô phỏng ở bước này.

### Lorebook — kho thông tin thế giới

Được cập nhật mỗi 10 chương từ Outline. Nếu lorebook hỏng (mất file/thiếu chi tiết): cho AI duyệt lại toàn bộ core để viết lại.

### Fullwrite — văn xuôi hoàn chỉnh (do AI viết từ Outline)

Bước cuối cùng. Không sáng tạo plot mới ở bước này — chỉ dựng văn xuôi.


## PHẦN 3: CÁCH VIẾT "SANDBOX" (kiểu nồi lẩu)

Tôi là dân Dev, nên cách viết của tôi hơi lạ. Tôi tưởng tượng ra **một cái nồi lẩu**:

```
1. Tôi bỏ nguyên liệu vô nồi:
   → Lore (thế giới, nhân vật, hệ thống)
   → Tình tiết chính (core idea của chương)

2. Tôi bật bếp lên:
   → Gọi Character Simulator (vn-outline)
   → AI tự nấu — nhân vật tự hành động, tự nói chuyện
   → 90% hội thoại sinh ra tự nhiên ở bước này

3. Tôi nếm thử:
   → Đọc outline AI tạo ra
   → Nếu ngon → fullwrite
   → Nếu không → thêm gia vị (chỉnh core, thêm tình tiết)
```

**Điểm mấu chốt:** Cách này phụ thuộc **cực kỳ lớn** vào khả năng suy luận (reasoning) của model. DeepSeek API ngon nhất cho việc này. Z.ai cũng ổn.

**Không đặt hành động nhân vật vào lore.** Để AI tự simulate từ tính cách. Tôi là main, tôi nói tôi làm — tôi ghi lore về main làm gì?

Xem thêm: [The Seven Levels of Worldbuilding](https://youtu.be/vFMnz75y5y4?si=IILXLHOO6HEDnaax)


## PHẦN 4: PIPELINE VIẾT GỐC (3 Bước)

### Bước 1: Lorebook (vn-worldbuilding)
- **Build Mode:** ý tưởng → lorebook 7 module
- **Update Mode:** sau 5–10 chương, cập nhật từ outline

**Cập nhật từ Outline hay Fullwrite?**
Lý tưởng là Fullwrite, nhưng vì context hạn chế nên cập nhật từ Outline là chấp nhận được. Outline chứa 90% tình tiết, khác biệt Outline→Fullwrite→Summary→Lore vs Outline→Lore là không đáng kể.

### Bước 2: Outline — Character Simulator (vn-outline + vn-povs)

**Luồng dữ liệu:**
```
Core (người dùng) — ~5 dòng tình tiết chính
  → vn-outline + vn-povs
  → Outline (dàn ý chi tiết: phân cảnh, thoại, cảm xúc)
```

**90% hội thoại sinh ra ở bước này.** Không phải ở Fullwrite.
→ Tại sao? Vì đây là lúc AI tập trung cao nhất vào character simulation. Nếu copy nguyên outline vào prompt fullwrite, AI vẫn hiểu nhưng hội thoại sẽ thiếu chiều sâu.

**Tại sao không viết thẳng từ Core → Fullwrite?**
AI vẫn làm được, nhưng hội thoại nông, tình tiết thiếu liên kết, nhân vật hành động thiếu nhất quán. Outline là bước "nén attention" — AI tập trung mô phỏng nhân vật trước khi viết prose.

### Bước 3: Fullwrite (vn-fullwrite + vn-lexicon + vn-lorefilter)

**Mẹo tăng độ dài chương mà không làm hỏng văn phong:**
- **Phân scene:** Chia chương thành các scene nhỏ, viết từng scene riêng
- **Nhiều POV:** Zoom in/out, đổi góc nhìn nhân vật trong cùng scene
- **Làm giàu tình tiết từ outline:** thêm hội thoại, hành động phụ ngay từ lúc lập dàn ý
- **Không yêu cầu số từ cụ thể:** "Chương phải dài 10k từ" → AI viết dài dòng, lặp đoạn, 1/3 cuối copy nội dung

Cách đúng: viết đủ tình tiết → độ dài tự nhiên.

**Cập nhật lorebook định kỳ:**
- Sau ~10 chương: cập nhật 1 lần từ Outline (vì outline phát sinh tình tiết phụ)
- Khi viết đến chương 150: kẹp Core(130–150) + Outline → Fullwrite


## PHẦN 5: CÁCH NHIỀU MODEL PHỐI HỢP

Pattern từ người dùng thực tế:

1. **Lên kịch bản/dàn ý:** Gemini (viết outline ngon, mạch lạc)
2. **Phân tích logic, hội thoại:** DeepSeek (API) hoặc Claude
3. **Viết full chương:** DeepSeek (API) — văn dài, tình tiết đầy đủ
4. **Fix lỗi:** Claude (phân tích logic)

→ Chép tay giữa các model. Đừng mong 1 model làm hết.


## PHẦN 6: CÀI ĐẶT HERMES DESKTOP + DEEPSEEK API

1. Tải [Hermes Desktop](https://hermes-agent.nousresearch.com/desktop)
2. Vào [platform.deepseek.com/api_keys](https://platform.deepseek.com/api_keys) → tạo API key
3. Nạp tiền (Top up) — $1 là đủ xài cả tháng
4. Hermes → Settings → dán API key
5. Chọn model DeepSeek
6. Chọn folder dự án → Download skills vào folder đó
7. Hỏi AI "học skill vn-guide, vn-fullwrite, vn-lexicon..."
8. Kiểm tra skill list đã có chưa

**Zwork (Agent đám mây, không PC):** [https://zwork.z.ai/](https://zwork.z.ai/) — có trả phí, upload skill được.


## PHẦN 7: LỖI THƯỜNG GẶP & SỬA

### Lỗi 1: "Tại sao AI viết seg dở?"
**Nguyên nhân:** Input chỉ có tính cách nhân vật, không có hướng dẫn cảm xúc lúc seg. AI không biết nên tự biên tự diễn.
**Sửa:** Thêm hướng dẫn cảm xúc vào lorebook / outline. Ví dụ: "nhân vật A khi bị xâm phạm sẽ: run rẩy → phản kháng yếu ớt → buông xuôi → nội tâm sụp đổ"

### Lỗi 2: "AI quên tình tiết giữa chừng"
**Nguyên nhân:** Lost in the middle. Giữa context bị "nuốt" bởi attention.
**Sửa:**
- Markdown để phân cấp độ quan trọng
- Keyword activation: đặt từ khóa ở đầu prompt
- Lorebook cập nhật mỗi 10 chương (dùng Update Mode)

### Lỗi 3: "Không đủ từ/chương"
**Sửa:**
- Phân scene → viết từng scene riêng
- Thêm tình tiết phụ vào outline (hội thoại, góc nhìn phụ)
- Chấp nhận 6k từ/chương là bình thường
- Đừng nhét "10000 từ" vào prompt — nó viết dài dòng lặp lại

### Lỗi 4: "Gemini không viết NSFW nữa"
**Nguyên nhân:** Google nâng cấp bộ lọc. Gemini không còn khả dụng cho NSFW.
**Sửa:** Chuyển sang DeepSeek (API), Z.ai.

### Lỗi 5: "DeepSeek chat cũng bị kiểm duyệt"
**Sửa:** Dùng **API** thay vì chat web. Hoặc nếu dùng web: chọn **Expert** — không phải Instance.

### Lỗi 6: "Z.ai từ chối 'mẹ vợ', 'côn trùng', 'bạn thân'"
**Nguyên nhân:** Z.ai cũng có bộ lọc nhưng lỏng hơn. Một số keyword đặc biệt trigger filter.
**Sửa:** Dùng từ đồng nghĩa, giảm chi tiết, hoặc qua DeepSeek API.

### Lỗi 7: "Xưng hô lộn xộn khi dịch"
**Sửa:** Luôn dùng ma trận XungHo.md. Không dùng đại từ chung (hắn, nó, cô ấy) nếu chưa tra ma trận.

### Lỗi 8: "AI bịa chuyện khi tóm tắt"
**Nguyên nhân:** Context quá dài, model không đọc hết.
**Sửa:** Cắt nhỏ input trước khi yêu cầu tóm tắt. Vn-translate đã cắt tại `\n` nên không lo đứt câu.


## PHẦN 8: DỊCH THUẬT (vn-translate)

### Quy trình:
```bash
# File gốc → md (nếu cần)
python scripts/convert_to_md.py truyen.epub

# Split — cắt tại \n, file ~12KB
python scripts/split_file.py truyen.md raw/

# Dịch từng part -> out/ + TenRieng.md + XungHo.md
# (dịch lần lượt, mỗi lần kiểm tra chéo tên/xưng hô)

# Ghép
python scripts/merge_parts.py out/ full.md
```

Split tại `\n` đã đảm bảo không đứt câu giữa chừng.


## PHẦN 9: FAQ NHANH

| Hỏi | Đáp |
|-----|------|
| Chất lượng hay số lượng? | Chất lượng. 6k từ/chương viết đúng còn hơn 10k từ dài dòng. |
| Dùng model nào cho NSFW? | DeepSeek API > Z.ai > DeepSeek chat (Expert) |
| Tại sao không nên jailbreak? | Tạo nhiễu attention → AI ngu đi. Dùng skill chuyên biệt. |
| Gemini còn viết được không? | Tạm thời không — bộ lọc quá gắt. Dùng cho outline. |
| Sao AI quên giữa chừng? | Lost in the middle. Markdown + lorebook + keyword activation. |
| Làm sao biết AI dùng được bao nhiêu context? | Khoảng 20% context công bố. Chuyên biệt hóa task. |
| Local có khả thi không? | Qwen 4 có vẻ ngon, nhưng cần GPU mạnh. API rẻ hơn. |
| Hermes Desktop có cần trả phí? | Miễn phí. Chỉ tốn API key (DeepSeek rất rẻ). |
| Không có PC thì làm sao? | [Zwork](https://zwork.z.ai/) — Agent đám mây trả phí. |
| Core là gì? | Ý tưởng cốt lõi ngắn gọn (~5 dòng) do người dùng tự viết. AI dùng core → outline. |


## NGUYÊN TẮC VÀNG

1. **Chuyên biệt hóa mỗi task** → giao cho AI khác (hoặc chat khác) → giảm nhiễu context + attention sâu hơn
2. **Tránh jailbreak** → giảm nhiễu attention vô ích → AI khôn hơn
3. **Markdown là bắt buộc** — không có markdown AI không biết cái nào quan trọng
4. **Không yêu cầu số từ** — làm hỏng văn phong
5. **Core (người dùng) → Outline (AI) → Fullwrite (AI)** — không nhảy bước
6. **Lorebook mỗi 10 chương** — cập nhật từ Outline
7. **Đừng đặt hành động nhân vật vào lore** — sandbox, để AI tự simulate từ tính cách

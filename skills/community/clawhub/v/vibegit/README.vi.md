# vibegit

**Repo của bạn có bao nhiêu phần là AI-assisted — và nó có ẩu không?**

`vibegit` đọc lịch sử git (chỉ metadata commit — không đọc nội dung file, không gọi mạng) và trả về **slop score 0–100**, **ước lượng AI-assisted**, bảng breakdown từng tín hiệu, badge SVG và CI gate. Zero dependency; cần Python 3.8+ và `git`.

```
+-- vibegit ----------------------------------------------------
| repo      my-app (main)
| commits   412
| slop      38/100  Slop
| AI-assist ~41.5%  (confirmed 12.3% / likely 29.2%, high confidence)
+-- top signals ----------------------------------------------
| AI assistance    20.8 pts
| giant commits    18% (74) -> 4.5 pts
| short messages   22.6% (93) -> 5.7 pts
| test deletions   3 commits -> 12.0 pts
| file churn       7.2% of files (>5 edits) -> 3.6 pts
| lockfile-only    4 commits -> 4.0 pts
+-- share ----------------------------------------------------
| vibegit · my-app: slop 38/100 (Slop) · AI-assisted ~41.5%
+--------------------------------------------------------------
```

## Vì sao?

Code AI để lại dấu vết trong git: trailer co-author, author bot, message "Generated with …", commit quá lớn không kèm test, subject `wip`, file test bị xoá, commit chỉ đụng lockfile. `vibegit` biến những dấu vết đó thành một con số kèm breakdown minh bạch để team nói về **chất lượng quy trình** thay vì phỏng đoán.

Công cụ đo tín hiệu, không kết luận ai viết code. Mọi con số AI-assisted là ước lượng kèm dải tin cậy.

## Cài đặt

### ClawHub

```bash
clawhub install thiennhant95/vibegit
```

### Từ source

Không cần cài:

```bash
git clone https://github.com/thiennhant95/vibegit && cd vibegit
python3 vibegit.py --help
```

Hoặc copy `vibegit.py` vào dự án. Yêu cầu duy nhất là `git` trong `PATH`.

## Sử dụng

```bash
python3 vibegit.py .                          # card tổng quan
python3 vibegit.py . --format md > report.md  # Markdown report
python3 vibegit.py . --format json            # JSON
python3 vibegit.py . --badge vibegit.svg      # badge SVG
python3 vibegit.py . --share                  # 1 dòng tóm tắt
python3 vibegit.py . --since "90 days ago"    # giới hạn thời gian
python3 vibegit.py . --max-score 40           # CI gate (exit 1 nếu > 40)
```

### Tuỳ chọn

| Flag | Mô tả |
|---|---|
| `--format text\|card\|md\|json\|badge` | Định dạng output (mặc định: card) |
| `--since`, `--until` | Giới hạn lịch sử (biểu thức ngày của `git log`) |
| `--include-merges` | Tính cả merge commit (mặc định bỏ qua) |
| `--badge FILE` | Ghi badge SVG |
| `--share` | Chỉ in dòng shareable |
| `--max-score N` | Exit 1 khi slop score vượt N |
| `--top N` | Số author hiển thị (mặc định 10) |
| `--version` | In phiên bản |

**Exit codes:** `0` ok · `1` vượt `--max-score` · `2` không phải git repo / không có commit · `4` lỗi git.

## Cách tính điểm

| Tín hiệu | Điểm tối đa | Quy tắc |
|---|---|---|
| AI assistance | 30 | `confirmed% + 0.5 × likely%`, cap 60% |
| Giant commits | 10 | hơn 400 dòng thay đổi |
| Short messages | 10 | subject dưới 15 ký tự, hoặc `wip`/`fix`/`update`/… |
| Test deletions | 20 | commit xoá file test mà không thêm gì |
| File churn | 15 | % file bị sửa hơn 5 lần |
| Lockfile-only | 15 | commit chỉ đụng lockfile |

Verdict: `0–14` Clean · `15–34` Mild slop · `35–59` Slop · `60+` Heavy slop.

**Confirmed**: trailer `Co-Authored-By` / `Assisted-by` / `Generated-by` có tên AI, author là bot AI, hoặc message "Generated with [tool]".
**Likely**: message/trailer nhắc tới AI tool nhưng không có tín hiệu cứng.

Repo dưới 15 commit sẽ được báo confidence thấp. Con số AI chỉ là ước lượng, không phải bằng chứng tác giả.

## Badge

```markdown
![vibegit](vibegit.svg)
```

Màu badge theo verdict: xanh (Clean), vàng (Mild), cam (Slop), đỏ (Heavy).

## CI

```yaml
- name: vibegit
  run: python3 vibegit.py . --max-score 40 --format md > vibegit.md
```

Workflow đầy đủ ở `examples/github-action.yml`. Dùng `fetch-depth: 0` để có toàn bộ lịch sử.

## Quyền riêng tư

- Chỉ chạy `git log` và `git rev-parse` với danh sách tham số cố định (`shell=False`).
- Không đọc nội dung file, không đụng secret, không gọi mạng, không upload.
- Không thực thi nội dung repo.
- Chỉ ghi file khi bạn yêu cầu rõ ràng (`--badge`, report redirect).

## Giới hạn

- Heuristic: AI viết mà không để lại trailer/bot/message marker có thể không bị phát hiện.
- Đo tín hiệu quy trình, không đo tính đúng đắn của code.
- Shallow clone (`--depth 1`) chỉ thấy commit mới nhất; dùng full clone.
- Repo lâu năm làm churn/lockfile cao hơn; dùng `--since` để so sánh công bằng.

## Phát triển

```bash
python3 tests/test_vibegit.py
```

11 test dựng repo tổng hợp, kiểm tra phát hiện AI (trailer/author/message), tín hiệu (giant commit, test deletion, short message), badge/gate, JSON deterministic và xử lý lỗi. CI chạy Ubuntu + Windows với Python 3.10 và 3.12.

## Skill liên quan

- **vibecheck** — audit code AI sinh ra (bảo mật + AI slop): [ClawHub](https://clawhub.ai/thiennhant95/vibecheck) · [GitHub](https://github.com/thiennhant95/vibecheck)
- **skill-firewall** — quét skill bên thứ ba trước khi cài: [ClawHub](https://clawhub.ai/thiennhant95/skill-firewall) · [GitHub](https://github.com/thiennhant95/agent-skills)
- **undo-first** — guard hành động có thể rollback (snapshot, risk gate, restore): [ClawHub](https://clawhub.ai/thiennhant95/undo-first) · [GitHub](https://github.com/thiennhant95/agent-skills)

## License

MIT. Xem [LICENSE](LICENSE).

---

English documentation: [README.md](README.md).

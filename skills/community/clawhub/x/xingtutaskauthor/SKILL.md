---
name: xingtuTaskAuthor
description: This skill should be used when the user needs to query the registered author list for a XingTu (星图) recruitment task. It fetches all registered influencers from the XingTu platform via the provider_get_task_author_list API, handles login/cookie management, paginates through all results, and exports the data to a formatted Excel file. Trigger phrases include: 星图任务达人, 查星图报名达人, 获取星图作者列表, xingtu task authors, 星图任务 ID, provider_get_task_author_list, 星图达人名单.
---

# XingTu Task Author Fetcher

Fetch the complete list of registered authors/influencers for a XingTu (星图) recruitment task and export to a well-formatted Excel file.

## Workflow

### Step 1: Obtain Task ID

If the user has already provided a XingTu task ID in their message, use it directly. Otherwise, ask the user to provide the task ID.

The task ID is a long numeric string (e.g., `7642279680695484426`). If the user provides a URL or screenshot, extract the ID from it.

### Step 2: Check Cookie

The cookie file is stored at `~/.xingtuCookie.txt`. Use `os.path.expanduser("~")` to resolve the home directory on any OS.

**If the file exists:**
- Read the cookie content.
- Validate the cookie by running:
  ```bash
  python "<skill-base>/scripts/fetch_xingtu_authors.py" --task-id "<task_id>" --cookie "<cookie>" --validate
  ```
- If the script exits with code 0 (prints `[OK]`), the cookie is valid. Proceed to Step 4.
- If the script exits with code 1 (prints `[FAIL]`), the cookie is invalid. Go to Step 3 with the message: "星图后台登录失效"

**If the file does NOT exist:**
- Go to Step 3 with the message: "星图后台还未登录"

### Step 3: Login Flow

When the cookie is missing or invalid:

1. First, check if the user's current message contains a cookie string. If yes:
   - Validate it using the `--validate` command from Step 2.
   - If valid: write it to `~/.xingtuCookie.txt` and proceed to Step 4.
   - If invalid: continue below.

2. Tell the user the login is required. Use the appropriate message:
   - No cookie file: "星图后台还未登录，需要先登录星图后台。"
   - Invalid cookie: "星图后台登录失效，需要重新登录。"

3. Open the login page in the built-in browser:
   ```
   https://sso.oceanengine.com/xingtu/login?role=7
   ```
   Use the `agent-browser` skill or `preview_url` tool to open this URL.

4. Instruct the user:
   - "请在打开的浏览器中完成星图后台登录。"
   - "登录成功后，请从浏览器中复制完整的 Cookie 字符串发给我。"
   - Provide guidance: In Chrome DevTools, go to Application > Cookies > www.xingtu.cn, or use the Network tab to copy the Cookie header from any API request.

5. When the user provides the cookie string:
   - Save it to `~/.xingtuCookie.txt`
   - Validate it using the `--validate` command
   - If valid: proceed to Step 4
   - If still invalid: ask the user to double-check the cookie and try again

### Step 4: Fetch Authors

Run the fetch script to get all authors across all pages:

```bash
python "<skill-base>/scripts/fetch_xingtu_authors.py" --task-id "<task_id>" --cookie "<cookie>"
```

The script will:
- Paginate through all results automatically (page by page until `has_more` is false)
- Print progress for each page (e.g., "Got 10 authors, cumulative: 10/45")
- Export all data to a formatted Excel file
- Print a JSON summary with `task_id`, `total_authors`, and `output` path

The default output path is: `xingtu_authors_<task_id>_<timestamp>.xlsx` in the current working directory.

Optional: Use `--output <path>` to specify a custom output path.

### Step 5: Present Results

After the script completes successfully:

1. Show the summary to the user (total authors count)
2. Call `deliver_attachments` to deliver the Excel file
3. Call `open_result_view` to open the Excel file for the user

### Step 6: Memory Update

Append a note to the daily memory file recording:
- Task ID processed
- Number of authors fetched
- Output file path

## Excel Output Columns

| Column | Source Field |
|--------|-------------|
| 序号 | Auto-increment |
| 达人昵称 | `author_base_info.nick_name` |
| 作者ID | `author_base_info.author_id` |
| 达人等级 | `author_base_info.ecom_author_level` |
| 粉丝数 | `author_base_info.follower` |
| 主推类目(30天) | `author_base_info.all_ecom_top3_category_30d_desc` (joined) |
| 带货GMV(30天) | `author_base_info.all_ecom_gmv_30d_desc` |
| 视频GMV(30天) | `author_base_info.ecom_video_gmv_30d_desc` |
| 1-20s报价 | `recruit_author_order_info.recruit_cpt_info.author_price` |
| 21-60s报价 | `author_base_info.price_21_60` |
| 60s+报价 | `author_base_info.price_60` |
| 预期CPM | `author_base_info.prospective_cpm` |
| 预期播放量 | `author_base_info.expected_play_num` |
| 完播率 | `author_base_info.author_recruit_video_cpt_fulfillment_rate_desc` |
| 所在城市 | `author_base_info.author_resident_city` |
| 内容标签 | `author_base_info.content_tags` (joined) |
| 微信号 | `author_base_info.wechat` |
| 报名状态 | `recruit_author_order_info.enroll_status` (mapped) |
| 报名时间 | `recruit_author_order_info.time_info.enroll_time` (timestamp to datetime) |
| 推荐理由 | `recruit_author_order_info.recommend_reason` (formatted) |
| 合作优势 | `recruit_author_order_info.coop_advantage` |
| 创作思路 | `recruit_author_order_info.creation_idea` |
| 补充说明 | `recruit_author_order_info.extra_note` |

## API Reference

- **Endpoint**: `POST https://www.xingtu.cn/gw/api/challenge/provider_get_task_author_list`
- **Auth**: Cookie-based (from browser login at `https://sso.oceanengine.com/xingtu/login?role=7`)
- **Pagination**: Query parameter `page` (int, starts at 1), response field `pagination.has_more` (bool)
- **Required headers**: `Accept`, `Content-Type`, `agw-js-conv: str`, `Cookie`, `User-Agent`, `Host`

## Error Handling

- **Cookie expired mid-fetch**: If any page returns a non-zero `status_code`, report the error and suggest re-login
- **Empty result**: If `total_count` is 0, inform the user that no authors have registered for this task
- **Network errors**: Retry once; if still failing, report the error to the user
- **openpyxl not installed**: Install it with `pip install openpyxl requests`

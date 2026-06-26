---
name: xingtu-task-invite-code
description: This skill should be used when the user needs to batch download QR code invitation images from XingTu (星图) recruitment tasks. It automates the full workflow: cookie authentication, fetching the task list from the XingTu platform via provider_get_task_order_list API, paginating through all tasks, navigating to each task detail page, clicking 邀约达人 then 二维码邀请 then 下载图片, and saving the QR code images to D:\xingtu\task-invite\{{task_id}}. Trigger phrases include: 星图邀约码, 批量下载邀约二维码, 星图任务二维码, 下载星图邀约图片, xingtu invite code, 星图任务邀请, provider_get_task_order_list invite.
---

# xingtuTaskInviteCode -- 星图邀约二维码批量下载

## Overview

This skill automates batch downloading of QR code invitation images from XingTu (星图) recruitment tasks. The complete workflow involves: cookie authentication -> task list retrieval with pagination -> per-task browser automation to download QR codes.

**Key tools used**: `agent-browser` (browser automation, cookie injection, file download), PowerShell `Invoke-WebRequest` (API calls), Python subprocess (batch orchestration).

**CRITICAL**: Never use mock or simulated data. All data must come from real API calls and browser interactions. If any step fails, report the actual error rather than fabricating results.

## Prerequisites

Before starting, ensure the `agent-browser` skill is loaded via `use_skill agent-browser`. The skill uses these agent-browser commands:

| Command | Purpose |
|---------|---------|
| `agent-browser open <url>` | Navigate to URL |
| `agent-browser get url` | Get current page URL (for login detection) |
| `agent-browser eval "<js>"` | Execute JavaScript (for cookie injection & DOM manipulation) |
| `agent-browser snapshot -i` | Get interactive element tree with refs |
| `agent-browser click <ref>` | Click element by ref |
| `agent-browser screenshot` | Take screenshot for debugging |
| `agent-browser close` | Close browser session |

## Path Resolution (DO NOT Hardcode User Paths)

All file paths MUST be resolved dynamically based on the runtime environment. Never hardcode `C:\Users\xxx\` in scripts.

| Resource | Dynamic Resolution (Python) | Dynamic Resolution (PowerShell) |
|----------|----------------------------|-------------------------------|
| Cookie file | `os.path.expanduser('~/.xingtuCookie.txt')` | `"$env:USERPROFILE\.xingtuCookie.txt"` |
| User home | `os.path.expanduser('~')` | `$env:USERPROFILE` |
| agent-browser | `os.path.join(os.environ['APPDATA'], 'npm', 'agent-browser.cmd')` | `"$env:APPDATA\npm\agent-browser.cmd"` |
| Downloads | `os.path.expanduser('~/Downloads')` | `"$env:USERPROFILE\Downloads"` |
| Task cache | `os.path.join(WORKSPACE, 'tasks_cache.json')` | `"$PWD\tasks_cache.json"` |
| Progress file | `os.path.join(WORKSPACE, 'qr_progress.json')` | `"$PWD\qr_progress.json"` |
| Output root | Configurable, default `D:\xingtu\task-invite` | Same |

**WORKSPACE** = the directory where the batch script runs (typically the current project workspace). Use `os.getcwd()` or `os.path.dirname(os.path.abspath(__file__))`.

## Workflow

The skill follows a sequential multi-phase workflow. Each phase must complete successfully before proceeding to the next.

**Session rule**: Keep the same agent-browser daemon alive across all phases. Only call `agent-browser close` at the very end (or on fatal error). Do NOT close between steps.

---

## Phase 1: Cookie Authentication

### Step 1.1: Check Cookie File

Read `~/.xingtuCookie.txt` (i.e., `{USERPROFILE}\.xingtuCookie.txt`) using `read_file`.

- If the file does NOT exist: go to Case A.
- If the file exists and contains a non-empty string: go to Step 1.2.

### Step 1.2: Validate Cookie

Use PowerShell to make a test API call:

```powershell
$cookieFile = "$env:USERPROFILE\.xingtuCookie.txt"
$cookie = (Get-Content $cookieFile -Encoding UTF8 -Raw).Trim()
$headers = @{
    "Accept" = "application/json, text/plain, */*"
    "Content-Type" = "application/json"
    "agw-js-conv" = "str"
    "Cookie" = $cookie
    "User-Agent" = "Apifox/1.0.0 (https://apifox.com)"
    "Host" = "www.xingtu.cn"
    "Accept-Charset" = "UTF-8"
}
$response = Invoke-WebRequest -Uri "https://www.xingtu.cn/gw/api/task/provider_get_task_order_list?page=1&limit=1" -Headers $headers -Method GET -TimeoutSec 15
# Check response: if status 200 and JSON contains valid data (not "用户未登录" or status_code 11001), cookie is valid
```

**Validation criteria**:
- HTTP 200 AND response body does NOT contain `status_code: 11001` (未登录) -> cookie valid, proceed to Phase 2.
- HTTP 200 but `status_code: 11001` -> Case B (cookie expired).
- Any other non-200 status -> Case B.

### Step 1.3: Handle Missing or Invalid Cookie

#### Case A: No cookie file exists
1. Output: **【星图后台还未登录】**
2. Go to Step 1.4.

#### Case B: Cookie file exists but validation fails
1. Output: **【星图后台登录失效】**
2. Check if the user's current message contains a cookie string (look for `sessionid=`, `uid_tt=`, `sid_guard=`, etc.).
   - If found: validate it with the same API call. If valid, write to `~/.xingtuCookie.txt` and go to Phase 2. If invalid, warn and go to Step 1.4.
   - If not found: go to Step 1.4.

### Step 1.4: Inject Cookie into Agent-Browser (Fast Path)

**When to use**: User has provided a cookie string but it contains httpOnly cookies that don't work via `document.cookie` injection. This is the PREFERRED method when cookie is available.

**⚠️ Known limitation**: Some essential cookies (e.g., `sessionid`, `sid_guard`) may be httpOnly and CANNOT be injected via `document.cookie`. In this case, `agent-browser eval` injection will still result in a login redirect. Fall through to Step 1.5 (manual login).

```python
# Python subprocess is PREFERRED over PowerShell for eval calls
# PowerShell truncates JS eval parameters containing special characters

import subprocess, json, time, os

AGENT = os.path.join(os.environ['APPDATA'], 'npm', 'agent-browser.cmd')
COOKIE_FILE = os.path.expanduser('~/.xingtuCookie.txt')

def ag(*args):
    cmd = [AGENT] + list(args)
    r = subprocess.run(cmd, capture_output=True, timeout=30)
    return r.stdout.decode('utf-8', errors='replace').strip()

def ev(js):
    js1 = ' '.join(js.split())  # collapse whitespace
    r = subprocess.run([AGENT, 'eval', js1], capture_output=True, timeout=15)
    return r.stdout.decode('utf-8', errors='replace').strip()

# Step 1: Open xingtu.cn first (must be on the domain before setting cookies)
ag('open', 'https://www.xingtu.cn')
time.sleep(2)

# Step 2: Read cookie and inject via document.cookie
cookie_str = open(COOKIE_FILE, encoding='utf-8').read().strip()
pairs = cookie_str.split('; ')
cookie_json = json.dumps(pairs)

js_inject = f"""(function(){{
    var pairs={cookie_json};
    var c=0;
    for(var i=0;i<pairs.length;i++){{
        var kv=pairs[i].trim().split('=');
        if(kv.length>=2){{
            try{{document.cookie=kv[0]+'='+kv.slice(1).join('=')+';path=/;domain=.xingtu.cn';c++;}}catch(e){{}}
        }}
    }}
    // Also set without domain for current path
    for(var i=0;i<pairs.length;i++){{
        var kv=pairs[i].trim().split('=');
        if(kv.length>=2){{
            try{{document.cookie=kv[0]+'='+kv.slice(1).join('=')+';path=/';c++;}}catch(e){{}}
        }}
    }}
    return c;
}})()"""

count = ev(js_inject)
print(f"Injected {count} cookies")

# Step 3: Verify by navigating to a known task page
ag('open', 'https://www.xingtu.cn/provider/pages/recruit/management/7644492294913278002')
time.sleep(6)
current_url = ev("location.href")

if 'login' in current_url.lower() or 'sso' in current_url.lower():
    print("Cookie injection insufficient (httpOnly cookies). Falling back to manual login.")
    # Go to Step 1.5
else:
    print("Cookie injection successful. Proceeding to Phase 2.")
    # Proceed to Phase 2
```

**Error Handling:**
- If `ev("location.href")` still shows login page after injection: httpOnly cookies are blocking. Fall through to Step 1.5.
- If `ev(js_inject)` returns 0: no cookies were injectable. Check cookie file format.

### Step 1.5: Browser Login (Manual, Fallback)

**Execution steps:**

1. Load `agent-browser` skill if not already loaded.
2. Open the login page:
   ```bash
   agent-browser open "https://sso.oceanengine.com/xingtu/login?role=7"
   ```
3. Tell the user: **请在打开的浏览器中完成星图登录（手机验证码登录）。**
4. Poll for login completion using `agent-browser get url`:
   ```powershell
   # Poll every 5 seconds, max 24 times (2 minutes)
   for ($i = 1; $i -le 24; $i++) {
       Start-Sleep -Seconds 5
       $url = (agent-browser get url 2>&1 | Select-String -Pattern "^https?://" | Out-String).Trim()
       if ($url -notmatch "sso.oceanengine.com" -and $url -match "xingtu") {
           Write-Host "LOGIN_DETECTED: $url"
           break
       }
   }
   ```
5. Once URL no longer contains `sso.oceanengine.com` (redirected to xingtu.cn):
   - Extract cookies: `agent-browser eval "document.cookie"`
   - Parse the output to get the cookie string (strip any CLI noise, keep the raw cookie text).
   - Write the cookie string to `~/.xingtuCookie.txt`.
   - Validate the saved cookie with the test API call from Step 1.2.
   - If validation still fails: report error and ask user to check login.

**Error Handling:**
- If polling times out (2 minutes, 24 attempts): Tell user login did not complete in time. Ask if they want to retry or provide cookie manually.
- If `agent-browser eval "document.cookie"` returns empty: the session may not have cookies on the current domain. Navigate to `https://www.xingtu.cn` first, then retry.

---

## Phase 2: Fetch Task List

### Step 2.1: Read Cookie

Read the cookie string from `~/.xingtuCookie.txt` using `read_file`.

### Step 2.2: Paginate Through All Tasks

Use PowerShell `Invoke-WebRequest` to make POST requests:

**URL**: `https://www.xingtu.cn/gw/api/task/provider_get_task_order_list`

**Headers**:
```
Accept: application/json, text/plain, */*
Content-Type: application/json
agw-js-conv: str
Cookie: {{cookie}}
User-Agent: Apifox/1.0.0 (https://apifox.com)
Host: www.xingtu.cn
Accept-Charset: UTF-8
Accept-Encoding: gzip, deflate
```

**Request Body per page**:
```json
{
    "page": {{page_number}},
    "limit": 10,
    "query": {
        "order_status": [2],
        "task_category_list": [133],
        "pay_type_list": [3, 4, 12]
    }
}
```

**Pagination implementation**:

```powershell
$cookieFile = "$env:USERPROFILE\.xingtuCookie.txt"
$cookie = (Get-Content $cookieFile -Encoding UTF8 -Raw).Trim()
$allTasks = @()
$page = 1
$hasMore = $true

while ($hasMore) {
    $body = @{ page = $page; limit = 10; query = @{ order_status = @(2); task_category_list = @(133); pay_type_list = @(3, 4, 12) } } | ConvertTo-Json -Depth 5
    $headers = @{...} # same headers as above with Cookie=$cookie
    $response = Invoke-RestMethod -Uri "https://www.xingtu.cn/gw/api/task/provider_get_task_order_list" -Method POST -Headers $headers -Body $body -ContentType "application/json"
    
    if ($response.data.list.Count -eq 0) { break }
    $allTasks += $response.data.list
    $page++
    Start-Sleep -Milliseconds 500  # rate limit protection
}
```

### Step 2.3: Pre-filter Tasks

**CRITICAL**: Before entering Phase 3, filter out tasks that cannot have QR codes:

```python
# Python reference implementation
import json

with open('tasks_cache.json', 'w', encoding='utf-8') as f:
    json.dump(all_tasks, f, ensure_ascii=False)

# Pre-filter: only keep tasks with participants
tasks = [t for t in all_tasks 
         if int(t['challenge_info'].get('participate_author_count') or 0) > 0]

skipped_zero = len(all_tasks) - len(tasks)
if skipped_zero > 0:
    print(f"跳过 {skipped_zero} 个达人报名数为 0 的任务（弹窗无法打开）")
```

**Why pre-filter**: Tasks with `participate_author_count == 0` have no registered influencers. The "邀约达人" modal cannot open for these tasks because there are no influencers to invite. Attempting to download QR codes for them will always fail.

**Logging**: For each filtered task, record task ID + name with status `no_participants`.

**Error Handling:**
- If any page fails: retry up to 3 times with 2-second delays. If still failing, log page number and continue.
- If page 1 returns empty: report **"没有找到符合条件的星图任务"** and stop.
- If API returns `status_code: 11001`: cookie expired mid-way. Re-run Phase 1, then resume from failed page.

### Step 2.4: Extract Task IDs

From the collected and filtered task list, extract each task's ID field (`challenge_info.id`). Log total count: `共找到 N 个可下载任务（已过滤 M 个无达人任务）`.

---

## Phase 3: Download QR Code Images Per Task

### Architecture Decision: Python subprocess over PowerShell

**⚠️ Critical**: Use Python `subprocess.run()` with array arguments for all agent-browser interactions in this phase. Do NOT use PowerShell for agent-browser calls because:
1. PowerShell truncates/splits JS `eval` arguments containing special characters (parentheses, quotes, arrows)
2. PowerShell Job-based background tasks get lost when the session ends
3. Python's `subprocess.run()` with array mode preserves arguments intact

```python
# CORRECT - Python subprocess with array args
import subprocess, time, json, os, glob, shutil, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stdout.reconfigure(line_buffering=True)

AGENT = os.path.join(os.environ['APPDATA'], 'npm', 'agent-browser.cmd')
WORKSPACE = os.getcwd()  # current project directory
DOWNLOADS = os.path.expanduser('~/Downloads')

def ab(args, timeout=20):
    """Run agent-browser command and return stdout"""
    cmd = [AGENT] + (args if isinstance(args, list) else args.split())
    return subprocess.run(cmd, capture_output=True, timeout=timeout).stdout.decode('utf-8', errors='replace')

def e(js, timeout=20):
    """Evaluate JavaScript in browser, return result string"""
    js1 = ' '.join(js.split())  # collapse whitespace, critical for arg passing
    r = subprocess.run([AGENT, 'eval', js1], capture_output=True, timeout=timeout)
    out = r.stdout.decode('utf-8', errors='replace').strip()
    if out.startswith('"') and out.endswith('"'):
        try: out = json.loads(out)
        except: pass
    return out
```

### Step 3.1: Prepare Output Directory

```powershell
New-Item -ItemType Directory -Force -Path "D:\xingtu\task-invite"
```

### Step 3.2: Implement Resume (断点续传)

```python
PROGRESS_FILE = os.path.join(WORKSPACE, 'qr_progress.json')

# Load existing progress
if os.path.exists(PROGRESS_FILE):
    with open(PROGRESS_FILE, encoding='utf-8') as f:
        done = json.load(f)
else:
    done = []

done_ids = {r['task_id'] for r in done if r['status'] in ('ok', 'skipped')}
pending = [t for t in tasks if t['challenge_info']['id'] not in done_ids]
```

### Step 3.3: Process Each Task

For each pending task, use agent-browser (already authenticated from Phase 1):

#### Step 3.3.1: Navigate to Task Detail

```python
ab(['open', f'https://www.xingtu.cn/provider/pages/recruit/management/{tid}'], timeout=20)
time.sleep(5)  # ⚠️ Do NOT use wait --load networkidle - it hangs on SPAs
```

**⚠️ Anti-pattern**: `agent-browser wait --load networkidle` hangs indefinitely on SPA (Single Page Application) pages like xingtu.cn because the page continuously emits network events through XHR polling and WebSocket connections. ALWAYS use fixed `time.sleep()` instead.

**Error Handling:**
- Page fails to load (agent-browser timeout): log task ID + reason, skip to next task.
- Page redirects to login: cookie expired. Re-run Phase 1, then resume.

#### Step 3.3.2: Click "邀约达人" Button

**⚠️ Anti-pattern**: Do NOT store `snapshot -i` ref IDs and use them later. Refs expire after page repaint / DOM mutation. Use `eval` to find and click buttons directly.

```python
clicked = False
for retry in range(5):  # Retry up to 5 times, page may still be loading
    r = e("""(function(){
        var b = document.querySelectorAll('button');
        for (var i=0; i<b.length; i++) {
            if (b[i].textContent.includes('邀约达人') && b[i].offsetParent !== null) {
                b[i].click();
                return 'clicked';
            }
        }
        return 'not found';
    })()""")
    if r == 'clicked':
        clicked = True
        break
    time.sleep(2)  # Wait between retries for page to load

if not clicked:
    # Record failure and skip
    done.append({'task_id': tid, 'name': tname, 'status': 'no_invite_btn'})
    continue
```

**Error Handling:**
- Button not found after 5 retries: record as `no_invite_btn`, skip task. Some task pages have unusual DOM layouts.
- Button found but click has no effect: the popup may be blocked. Record as `no_popup`, skip task.

#### Step 3.3.3: Wait for and Verify Popup

```python
# Wait for popup to become visible (up to 8 seconds)
for i in range(16):
    s = e("""(function(){
        var p = document.querySelector('.ovui-popup__lock');
        return p && p.offsetWidth > 0 ? 'visible' : 'hidden';
    })()""")
    if s == 'visible':
        break
    time.sleep(0.5)

if s != 'visible':
    done.append({'task_id': tid, 'name': tname, 'status': 'no_popup'})
    continue
```

**Popup container**: The invite modal uses `ovui-popup__lock` class (NOT `el-dialog__wrapper`). This was discovered through screenshot debugging.

#### Step 3.3.4: Click "二维码邀请" Radio

```python
time.sleep(1)  # Let popup animation finish
e("""(function(){
    var p = document.querySelector('.ovui-popup__lock');
    if (!p) return 'no popup';
    var items = p.querySelectorAll('.ovui-radio-item');
    for (var i=0; i<items.length; i++) {
        if (items[i].offsetParent === null) continue;  // hidden elements
        if (items[i].textContent.trim() == '二维码邀请') {
            items[i].click();
            return 'clicked';
        }
    }
    return 'not found';
})()""")
time.sleep(2)  # Wait for QR code to render
```

**Radio element**: `.ovui-radio-item` with text exactly "二维码邀请" (NOT a button or span).

#### Step 3.3.5: Verify Download Button

```python
dl = e("""(function(){
    var bs = document.querySelectorAll('button');
    for (var i=0; i<bs.length; i++) {
        if (bs[i].textContent.trim() == '下载图片' && bs[i].offsetParent !== null) {
            return 'found';
        }
    }
    return 'not found';
})()""")

if dl != 'found':
    done.append({'task_id': tid, 'name': tname, 'status': 'no_dl_btn'})
    # Close popup before skipping
    e("""(function(){
        var p = document.querySelector('.ovui-popup__lock');
        if (!p) return;
        var c = p.querySelector('[class*=close]');
        if (c) c.click();
    })()""")
    continue
```

**Error Handling:**
- Download button not found: record as `no_dl_btn`. This happens on some task pages (e.g., task 7641072633181650953) where the DOM renders differently.

#### Step 3.3.6: Download QR Code Image

```python
# Track existing files in Downloads BEFORE clicking
before = {f: os.path.getmtime(f) for f in glob.glob(os.path.join(DOWNLOADS, '*.png'))}

# Click download button
e("""(function(){
    var bs = document.querySelectorAll('button');
    for (var i=0; i<bs.length; i++) {
        if (bs[i].textContent.trim() == '下载图片' && bs[i].offsetParent !== null) {
            bs[i].click();
            return 'clicked';
        }
    }
    return 'not found';
})()""")

# Wait for new file to appear in Downloads (up to 30 seconds)
new_file = None
for i in range(60):
    for f in glob.glob(os.path.join(DOWNLOADS, '*.png')):
        if f not in before:
            time.sleep(2)  # Let file finish writing
            if os.path.getsize(f) > 100000:  # ⚠️ Validate file size
                new_file = f
                break
    if new_file:
        break
    time.sleep(0.5)

if new_file:
    sz = os.path.getsize(new_file)
    shutil.move(new_file, qr_path)  # Move from Downloads to output
    print(f"  OK: {sz:,}b")          # Expected: ~234,000 bytes
    done.append({'task_id': tid, 'name': tname, 'status': 'ok', 'size': sz})
else:
    print(f"  FAIL: download timeout")
    done.append({'task_id': tid, 'name': tname, 'status': 'download_timeout'})
```

**Download behavior notes**:
- Browser saves to `~/Downloads/` with filename = task name (e.g., `WL-1.3.1-万益蓝女性益生菌_好货koc-6月.png`), NOT task_id
- Valid QR codes are ~234KB, 420×784 pixels, RGB PNG format
- Files smaller than 100KB should be treated as failures (likely DOM screenshot or thumbnail)

**Error Handling:**
- No new file after 30s: record `download_timeout`.
- File appears but < 100KB: the download was partial or wrong. Record as `download_small`.

#### Step 3.3.7: Close Popup

```python
# Always close popup after each task to prevent DOM pollution
e("""(function(){
    var p = document.querySelector('.ovui-popup__lock');
    if (!p) return;
    // Try close button first
    var c = p.querySelector('[class*=close]');
    if (c) {
        c.click();
        return 'closed by button';
    }
    // Fallback: press Escape
    document.dispatchEvent(new KeyboardEvent('keydown', {
        key: 'Escape', keyCode: 27, bubbles: true
    }));
    return 'closed by escape';
})()""")
time.sleep(0.5)
```

### Step 3.4: Save Progress After EVERY Task

```python
# CRITICAL: Write progress file after each task completes (or fails)
# This enables safe resume if the process is interrupted
with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
    json.dump(done, f, ensure_ascii=False)
```

### Step 3.5: Inter-Task Delay

Add a 0.5-1 second delay between tasks to avoid rate limiting. Not strictly necessary since each task takes 10-20 seconds, but adds safety.

---

## Phase 4: Cleanup and Summary

### Step 4.1: Close Browser

```bash
agent-browser close
```

### Step 4.2: Output Summary Table

| 字段 | 说明 |
|------|------|
| 总任务数 | Total from API (including filtered) |
| 符合条件 | After `participate_author_count > 0` filter |
| 成功下载 | Tasks with QR code successfully saved (>100KB) |
| 跳过/失败 | Tasks skipped or failed, with reason codes |
| 输出目录 | `D:\xingtu\task-invite\` |

**Failure reason codes**:
- `no_participants`: `participate_author_count == 0`, cannot open modal
- `no_invite_btn`: "邀约达人" button not found (DOM layout issue)
- `no_popup`: Click on invite button didn't open modal
- `no_dl_btn`: "下载图片" button not found in modal
- `download_timeout`: Download button clicked but no file appeared in 30s
- `download_small`: Downloaded file < 100KB (not a valid QR code)

For each failed/skipped task, list: task ID, task name, failure reason code.

---

## Phase 5: Background Execution (Production Mode)

When running batch download for 50+ tasks, use background execution to avoid session timeout:

### Windows Background Process

```cmd
REM Start batch in independent minimized CMD window
cmd /c start "xingtu_batch" /min cmd /c "python -u inject_and_batch.py > batch_log.txt 2>&1"
```

**Why this pattern**:
- `cmd /c start` creates a truly independent process (not tied to PowerShell session)
- `/min` minimizes the window
- Output is redirected to a log file for monitoring
- The process survives even if the WorkBuddy session ends

**⚠️ Anti-pattern**: Using PowerShell `Start-Job` or background jobs. These are tied to the PowerShell session and will be killed if the session ends.

### Monitoring

```python
# Check log file periodically
import os
log_file = 'batch_log.txt'
if os.path.exists(log_file):
    lines = open(log_file, encoding='utf-8', errors='replace').readlines()
    print(f"Progress: {len(lines)} lines, {os.path.getsize(log_file)} bytes")
    # Show last 5 lines for recent status
    for l in lines[-5:]:
        print(l.rstrip())
```

---

## Agent Execution Protocol

**IMPORTANT: After loading this skill, the agent MUST follow this cycle:**

1. **Execute**: Run through all phases (Phase 1 → Phase 2 → Phase 3 → Phase 4) sequentially.
2. **Test**: Verify each phase produces real results (not mock data). Validate API responses, check downloaded files exist and are >100KB.
3. **Adjust**: If any step fails, fix the issue and retry. Common adjustments:
   - Cookie expired → re-authenticate
   - Element not found → take screenshot, check page state, try eval-based selectors
   - Download failed → check Downloads folder, verify file size
   - API error → check response, adjust headers/body
4. **Report**: After full execution, output the summary table with real data.

Never stop at "showing the plan" -- the skill is designed to be executed end-to-end.

---

## Important Notes

1. **Data integrity**: All task data must come from real API responses. Never fabricate task IDs, counts, or statuses.
2. **Rate limiting**: 500ms delay between API page requests, 0.5s delay between browser tasks.
3. **Cookie refresh**: If any API or page returns 401/redirect-to-login, immediately run Phase 1, then resume.
4. **File naming**: QR code images saved as `qrcode.png` under `D:\xingtu\task-invite\{{task_id}}\`.
5. **Session management**: Keep agent-browser daemon alive across all phases. Only close at the very end.
6. **Fallback**: If "下载图片" is unavailable after clicking "二维码邀请", record as failure and move on. Do not attempt screenshot fallback as it produces only ~2KB thumbnails.
7. **File validation**: Always verify downloaded files are >100KB. Valid QR codes are ~234KB. Anything <100KB is a failure.
8. **Encoding**: Always use UTF-8 with `errors='replace'` when reading/writing files. Set `sys.stdout` encoding to avoid print crashes.
9. **Popup close**: Always close the popup after each task (success or failure) to prevent DOM pollution affecting subsequent tasks.

---

## 踩坑经验总结 (Pitfalls & Defensive Programming)

以下是实际操作中反复验证得出的经验，每个坑都浪费过大量时间。**严格遵守这些规则可以避免 90% 的故障。**

### Pitfall 1: `agent-browser wait --load networkidle` 永远卡死

**现象**: SPA 页面（如 xingtu.cn）持续发送 XHR 轮询和 WebSocket 心跳包，networkidle 条件永远不满足。

**解决方案**: 永远不要用 `wait --load networkidle`。改用固定 `time.sleep(N)`，N 根据实测调整（导航后 5s，弹窗后 1-2s）。

```python
# ❌ BAD
ab('wait --load networkidle')

# ✅ GOOD
ab(['open', url])
time.sleep(5)  # empirically determined for xingtu.cn
```

---

### Pitfall 2: PowerShell 的 `eval` 参数被截断

**现象**: PowerShell 传递包含括号、引号、尖括号的 JS 代码给 `agent-browser eval` 时，参数在 shell 层被截断或错误转义。

```powershell
# ❌ BAD - PowerShell truncates the JS after certain characters
agent-browser eval "(function(){var b=document.querySelectorAll('button');...})()"
```

**解决方案**: 使用 Python `subprocess.run()` + 数组参数模式。数组模式不会经过 shell 解析，参数完整传递。

```python
# ✅ GOOD
subprocess.run([AGENT, 'eval', js_code], capture_output=True)
```

---

### Pitfall 3: Snapshot ref ID 在 DOM 变化后过期

**现象**: 使用 `agent-browser snapshot -i` 获取 ref ID（如 `[ref=e22]`），然后在页面发生任何变化（导航、弹窗、AJAX 更新）后使用该 ref，点击失败。

**解决方案**: 
- 尽可能使用 `eval` 直接查找并点击元素，不依赖 ref ID
- 如果必须用 ref，每次操作前重新 snapshot
- `eval` 模式天然免疫 DOM 更新问题

```python
# ❌ BAD - ref may be expired
ag('snapshot -i')  # gets ref=e22
# ... page changes ...
ag('click', '[ref=e22]')  # FAILS

# ✅ GOOD - always finds the current element
e("""(function(){
    var b = document.querySelectorAll('button');
    for (var i=0; i<b.length; i++) {
        if (b[i].textContent.includes('邀约达人') && b[i].offsetParent !== null) {
            b[i].click();
            return 'clicked';
        }
    }
    return 'not found';
})()""")
```

---

### Pitfall 4: `participate_author_count == 0` 的任务弹窗打不开

**现象**: 对于没有达人报名的任务，点击"邀约达人"按钮后弹窗无法打开（因为没有可邀约的对象）。

**解决方案**: Phase 2 结束后立即预过滤，避免在 Phase 3 中浪费时间。

```python
tasks = [t for t in all_tasks 
         if int(t['challenge_info'].get('participate_author_count') or 0) > 0]
```

---

### Pitfall 5: 弹窗 DOM 结构特殊（`ovui-popup__lock`）

**现象**: 星图使用 `ovui-popup__lock` 作为弹窗容器（不是常见的 `el-dialog__wrapper` 或 `modal`）。如果用错选择器，会一直找不到弹窗。

**已验证的选择器**:
- 弹窗容器: `.ovui-popup__lock`
- 二维码邀请 radio: `.ovui-radio-item`（文本 "二维码邀请"）
- 下载按钮: `button`（文本 "下载图片"）
- 关闭按钮: `[class*=close]`（在 popup 内部）

---

### Pitfall 6: Cookie 包含 httpOnly 属性时 `document.cookie` 注入无效

**现象**: 用户提供的 cookie 字符串中，`sessionid`、`sid_guard` 等关键 cookie 带有 `httpOnly` 标志。通过 `document.cookie = ...` 注入时，浏览器拒绝设置这些 cookie。

**解决方案**: 先尝试 eval 注入。如果注入后页面仍然跳转到登录页，则必须走手动浏览器登录流程（Step 1.5）。

检测方法：注入后导航到任务详情页，用 `ev("location.href")` 检查是否在 login/sso 页面。

---

### Pitfall 7: 下载文件不直接到目标目录

**现象**: `agent-browser download` 命令下载到 `~/Downloads/`，文件名为任务名称（中文），不是 task_id。

**解决方案**: 
1. 在点击下载前，记录 Downloads 目录中已有的 `.png` 文件
2. 点击下载后，检测 Downloads 中新增的 `.png` 文件
3. 用 `shutil.move()` 将文件移动到 `D:\xingtu\task-invite\{task_id}\qrcode.png`
4. 验证文件大小 > 100KB

```python
before = {f: os.path.getmtime(f) for f in glob.glob(os.path.join(DOWNLOADS, '*.png'))}
# ... click download ...
# Find new file
for f in glob.glob(os.path.join(DOWNLOADS, '*.png')):
    if f not in before and os.path.getsize(f) > 100000:
        shutil.move(f, qr_path)
```

---

### Pitfall 8: 断点续传需要逐任务保存

**现象**: 批量处理 50+ 任务时，如果中途崩溃（浏览器崩溃、网络断开、Cookie 过期），没有进度记录的话需要全部重来。

**解决方案**: 每完成一个任务（无论成功或失败）立即写 `qr_progress.json`。这样任何时候中断都可以从中断点继续。

```python
# After EACH task, not at the end:
with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
    json.dump(done, f, ensure_ascii=False)
```

---

### Pitfall 9: 弹窗不关闭导致 DOM 污染

**现象**: 如果弹窗不关闭，下一个任务的页面可能残留上一个弹窗的 DOM 元素，导致 `querySelector` 找到过期元素。

**解决方案**: 每个任务处理完（无论成功/失败）后，主动关闭弹窗。使用 close 按钮 + Escape 双重兜底。

```python
e("""(function(){
    var p = document.querySelector('.ovui-popup__lock');
    if (!p) return;
    var c = p.querySelector('[class*=close]');
    if (c) c.click();
    else document.dispatchEvent(new KeyboardEvent('keydown',
        {key:'Escape', keyCode:27, bubbles:true}));
})()""")
```

---

### Pitfall 10: Python stdout 编码问题导致中文乱码/崩溃

**现象**: Windows 环境下 `print()` 输出中文时抛出 `UnicodeEncodeError`，或者日志文件出现乱码。

**解决方案**: 在所有 Python 脚本开头设置 stdout 编码：

```python
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stdout.reconfigure(line_buffering=True)  # 实时输出，不缓冲
```

同时，所有 `open()` 调用使用 `encoding='utf-8'`。

---

### Quick Reference: 正确的下载流程

```
1. 导航到任务页          → time.sleep(5)  ← 别用 networkidle！
2. eval 点击"邀约达人"    → 最多重试 5 次
3. 等待 .ovui-popup__lock → 最多等 8 秒
4. eval 点击"二维码邀请"   → .ovui-radio-item
5. 验证"下载图片"按钮存在   → 不存在则记录 no_dl_btn
6. 记录 Downloads 已有 PNG
7. eval 点击"下载图片"
8. 检测 Downloads 新文件  → 等待 30 秒 → 验证 > 100KB
9. shutil.move → D:\xingtu\task-invite\{task_id}\qrcode.png
10. 关闭弹窗 → 保存进度 → 下一个任务
```

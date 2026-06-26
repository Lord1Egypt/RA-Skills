---
name: daily-news-briefing
description: Automated daily news briefing generation and delivery system. Supports tech (AI, chips, semiconductors) and finance (stocks, markets, crypto) news from China and international sources. Features dual-search architecture with Baidu API (preferred) and DuckDuckGo fallback (no API key required). Use when users need: (1) Scheduled daily news delivery via cron jobs, (2) Multi-source news aggregation with AI commentary, (3) News generation with custom search queries, (4) Automated delivery to messaging channels (QQ/TG/Discord), or (5) Customizable briefing templates and delivery times.
---

# Daily News Briefing Skill

Automated daily news briefing system that generates comprehensive tech and financial reports with AI-powered commentary and delivers them via configured messaging channels. Supports **dual-search architecture** with Baidu API (preferred when configured) and DuckDuckGo fallback (always available, no API key required).

## Installation & Configuration

### Step 1: Install via ClawHub

**Option A: From ClawHub (Published)**

```bash
# Search and install
clawhub search daily-news-briefing
clawhub install daily-news-briefing

# Verify installation
ls ~/.openclaw/skills/daily-news-briefing/
```

**Option B: From Local Directory**

```bash
# Copy skill to OpenClaw skills directory
cp -r /path/to/daily-news-briefing ~/.openclaw/skills/

# Verify structure
ls ~/.openclaw/skills/daily-news-briefing/scripts/
```

### Step 2: Configure Environment Variables (Optional)

**Note**: The skill has a built-in fallback to DuckDuckGo if no Baidu API key is configured. Baidu API provides better structured data, but DuckDuckGo works perfectly fine without any API keys.

**With Baidu API (Recommended for Better Results):**

Create a configuration file with your Baidu Search API key:

**Option A: System-wide (Recommended for servers)**

```bash
# Create config file
sudo nano /etc/profile.d/daily-news-briefing.sh

# Add your configuration
export BAIDU_API_KEY="bce-v3/ALTAK-your-api-key-here"
export NEWS_TARGET_USER="9C12E02D9038B14FCEDCE1B69AAEAB3F"  # QQ user ID
export NEWS_CHANNEL="qqbot"  # qqbot, telegram, discord

# Reload configuration
source /etc/profile.d/daily-news-briefing.sh
```

**Option B: User-specific**

```bash
# Add to ~/.bashrc or ~/.zshrc
echo 'export BAIDU_API_KEY="your-api-key"' >> ~/.bashrc
echo 'export NEWS_TARGET_USER="target-user-id"' >> ~/.bashrc
source ~/.bashrc
```

**Without API Key (Uses DuckDuckGo):**

The skill will automatically use DuckDuckGo web search if no Baidu API key is configured:

```bash
# Just set target user and channel - that's it!
export NEWS_TARGET_USER="your-qq-user-id"
export NEWS_CHANNEL="qqbot"
```

**Compare Search Methods:**

| Feature | Baidu API | DuckDuckGo |
|---------|-----------|------------|
| **API Key Required** | ✅ Yes (75 chars) | ❌ No |
| **Result Quality** | 🏆 Better structured data | 👍 Good for most use cases |
| **Rate Limits** | ⚠️ API quota applies | ✅ None |
| **Setup Time** | ~2 mins (get API key) | 0 mins (works out of box) |
| **Content Preview** | Full article snippets | Title + URL only |

*Recommendation*: Start with DuckDuckGo to test quickly, add Baidu API later if you need better content previews.

### Step 3: Customize Delivery Settings (Optional)

Edit the delivery script to match your preferences:

```bash
nano ~/.openclaw/skills/daily-news-briefing/scripts/deliver-briefing.sh
```

**Key settings to modify:**

```bash
# Change target user ID
TARGET_USER="your-qq-user-id"  # Line ~10

# Change delivery channel (--channel parameter)
--channel qqbot      # QQ Bot (default)
--channel telegram   # Telegram
--channel discord    # Discord
```

### Step 4: Set Up Cron Job for Automated Delivery

**For daily delivery at 9:00 AM:**

```bash
# Edit crontab
crontab -e
```

Add these lines (adjust paths if needed):

```cron
# Generate news at 9:00 AM
0 9 * * * source /etc/profile && cd ~/.openclaw/skills/daily-news-briefing/scripts && python3 generate-briefing.py >> /var/log/daily-news.log 2>&1

# Deliver at 9:01 AM  
1 9 * * * source /etc/profile && bash ~/.openclaw/skills/daily-news-briefing/scripts/deliver-briefing.sh >> /var/log/news-delivery.log 2>&1
```

**Custom delivery times:**

| Time | Cron Entry (Generate + Deliver) | Use Case |
|------|---------------|----------|
| 7:00 AM | `0 7 * * *` ...<br>`1 7 * * *` ... | Early morning briefing |
| 7:30 AM | `30 7 * * *` ...<br>`31 7 * * *` ... | After system fully up (recommended) |
| 6:00 PM | `0 18 * * *` ...<br>`1 18 * * *` ... | Evening summary |

### Step 5: Test the Setup

**Test API Key:**

```bash
python3 -c "from generate_briefing import search_baidu; print(search_baidu('test', count=1))"
```

**Generate News Manually:**

```bash
cd ~/.openclaw/skills/daily-news-briefing/scripts
python3 generate-briefing.py
```

Check log: `tail -20 /var/log/daily-news.log`

**Test Delivery:**

```bash
bash deliver-briefing.sh
```

Check log: `tail -30 /var/log/news-delivery.log`

**Verify Cron is Running:**

```bash
# Check cron service
systemctl status cron

# View scheduled jobs
crontab -l

# Check last execution
grep "Starting news generation" /var/log/daily-news.log | tail -1
```

### Step 6: Customize News Content (Optional)

**Modify search queries** in `generate-briefing.py`:

```python
# Line ~85-90, customize keywords
china_tech = search_baidu('科技新闻 人工智能 芯片 AI 华为', count=3)
intl_tech = search_baidu('NVIDIA Broadcom Apple Microsoft AI', count=3)
china_finance = search_baidu('A 股 上证指数 港股 财经', count=3)
intl_finance = search_baidu('美股 纳斯达克 道琼斯 比特币', count=3)
```

**Adjust article count:** Change `count=3` to `1-5` articles per category.

**Customize AI commentary rules:** See `references/CONFIGURATION.md` for pattern examples.

## Components

### Scripts

- **generate-briefing.py**: Main news generation script. Fetches from 4 categories:
  - China Tech News (AI, chips, Huawei, etc.)
  - International Tech News (NVIDIA, Apple, Microsoft, etc.)
  - China Financial Markets (A-shares, HK stocks)
  - International Finance (US stocks, Fed, crypto)

- **deliver-briefing.sh**: Delivery wrapper with multiple fallback strategies:
  - Method A: Direct OpenClaw CLI message send
  - Method B: Python delivery script
  - Method C: Create notification file

- **news-deliver-direct.py**: Alternative Python-based delivery with headline extraction

### References

See `references/` for:
- **CONFIGURATION.md**: Detailed setup guide and customization options
- **API_REFERENCE.md**: Baidu API integration details and search query examples
- **TEMPLATE_EXAMPLES.md**: Sample briefing outputs and markdown templates

## Customization

### Change Delivery Time

Edit crontab lines (format: `minute hour day month weekday`):

```cron
# 7:30 AM delivery
30 7 * * * ...
31 7 * * * ...

# 6:00 AM delivery  
0 6 * * * ...
1 6 * * * ...
```

### Modify Search Queries

Edit queries in `generate-briefing.py`:

```python
china_tech = search_baidu('科技新闻 人工智能 芯片 AI 华为', count=3)
intl_tech = search_baidu('NVIDIA Broadcom Apple Microsoft AI', count=3)
```

### Add Custom Commentary Rules

See `references/API_REFERENCE.md` for commentary rule patterns.

## Troubleshooting

**No results from Baidu API:**
- Verify `BAIDU_API_KEY` is set and valid (length > 20 chars)
- Check `/var/log/daily-news.log` for detailed errors

**Delivery fails:**
- Check `/var/log/news-delivery.log` 
- Verify OpenClaw CLI is installed: `openclaw --version`
- Confirm target user ID is correct in script config

**Wrong headlines extracted:**
- Script supports both Chinese and English headers
- Ensure markdown file has proper structure with `## 🖥️` and `## 📈` sections

## Multi-Channel Delivery Configuration

### Supported Channels

The skill supports any OpenClaw-configured messaging channel:

| Channel | Target Format | Example Value | Notes |
|---------|-------------|----------------|------|
| **QQBot** | `c2c:USERID` | `c2c:9C12E02D...` | Default, for private QQ messages |
| **Telegram** | `@username` or chat ID | `@mychannel` or `123456789` | Bot must be added to channel |
| **Discord** | `guild-id/channel-id` | `1234567890/9876543210` | Bot needs permissions |
| **Slack** | `#channel-name` or `@user` | `#general` or `U123456` | Slack app configured |

### Configure Channel in Script

**Method 1: Environment Variable**

```bash
export NEWS_CHANNEL="telegram"  # qqbot, telegram, discord, slack
export NEWS_TARGET_USER="@mychannel"  # Channel-specific target
```

**Method 2: Edit deliver-briefing.sh**

Find line ~50 and modify:
```bash
--channel qqbot      # Change to your preferred channel
-t "qqbot:c2c:${TARGET_USER}"  # Update target format per channel
```

### Channel-Specific Setup

**For Telegram:**
1. Create a bot via @BotFather
2. Add bot to channel/group
3. Get chat ID using `openclaw status`
4. Set `NEWS_TARGET_USER="@channelname"` or numeric ID

**For Discord:**
1. Create application in Discord Developer Portal
2. Invite bot to server with proper permissions
3. Use format: `guild-id/channel-id`
4. Test with: `openclaw message send --channel discord -t "GUILD/CHANNEL" -m "Test"`

**For QQBot:**
- Ensure QQ Bot is configured in OpenClaw
- Use c2c format for private messages
- Target user ID available from chat metadata

## Output Format

Generated briefing includes:
- Date and timestamp header
- 4 news categories with 3 articles each (customizable)
- AI-powered Jarvis commentary for each article
- Source attribution and read-more links
- File size: typically 10-15KB

Delivery message includes:
- Preview with first headlines from tech & finance sections
- `<qqfile>` attachment tag for full markdown report
- Footer with next delivery time notice

## Logs & Monitoring

| Log File | Location | Purpose |
|------|-------|----------|
| News generation | `/var/log/daily-news.log` | Search results, article counts, errors |
| Delivery attempts | `/var/log/news-delivery.log` | Send status, fallback methods used |

**View recent logs:**
```bash
# Today's news generation
tail -50 /var/log/daily-news.log

# Latest delivery result
grep "completed\|ERROR" /var/log/news-delivery.log | tail -10
```

## Troubleshooting

**No results from Baidu API:**
- Verify `BAIDU_API_KEY` is set and valid (length > 20 chars)
- Check `/var/log/daily-news.log` for "Found X results" messages
- Test: `python3 -c "from generate_briefing import search_baidu; print(search_baidu('test', count=1))"`
- **Fallback**: If Baidu API fails, script automatically uses DuckDuckGo (look for "falling back to DuckDuckGo" in logs)

**No results from any source:**
- Check network connectivity: `ping -c 2 duckduckgo.com`
- Verify firewall isn't blocking outbound HTTP/HTTPS
- Test DuckDuckGo directly: `curl -s "https://html.duckduckgo.com/html/?q=test"`
- Review `/var/log/daily-news.log` for detailed error messages

**Delivery fails:**
- Check `/var/log/news-delivery.log` for specific error
- Verify OpenClaw CLI is installed: `openclaw --version`
- Confirm target user/channel ID is correct in script config
- Test manual delivery: `bash deliver-briefing.sh`

**Wrong headlines extracted:**
- Script supports both Chinese (`## 🖥️ 中国科技新闻`) and English headers
- Ensure markdown file has proper structure with section markers
- Check log shows file size > 1KB (not empty fallback)
- DuckDuckGo results may have longer titles - this is normal

**Cron job not running:**
- Verify cron service: `systemctl status cron`
- Check crontab entries: `crontab -l`
- Test cron timing: wait for scheduled time or adjust to test immediately
- Check log rotation: old logs may be archived

**Check which search method is being used:**
```bash
# View log file
grep "Search method used" /var/log/daily-news.log | tail -1

# Or check footer of generated news file
tail -5 ~/daily-news-$(date +%Y%m%d).md
```

Expected output: `📊 Search method used: baidu` or `📊 Search method used: duckduckgo`

## Notes

- Script auto-generates filename with current date: `daily-news-YYYYMMDD.md`
- Logs stored in `/var/log/daily-news.log` and `/var/log/news-delivery.log`
- Fallback content generated if search returns no results (graceful degradation)
- Supports multiple messaging channels via OpenClaw CLI
- All credentials managed via environment variables (no hardcoded secrets)

---

**Version:** 1.0  
**Last Updated:** 2026-03-28  
**Maintained by:** Jarvis AI Assistant

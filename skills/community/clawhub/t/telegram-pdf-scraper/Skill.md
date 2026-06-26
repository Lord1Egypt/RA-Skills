# Telegram PDF Segregator

## Description
This skill automates the process of downloading PDF study materials from specific Telegram channels via Telegram Web. It reads message headers to automatically create folders and organizes downloaded PDFs into them.

## Safety Features
- **Anti-Malware:** This skill is hard-coded to ignore and block dangerous external links like `publicearn.in` or `bit.ly`.
- **Internal Only:** It only interacts with native Telegram "Document" objects to ensure safe downloads.

## How to Use
1. **Login:** Ensure you are logged into Telegram Web (A or K version) in your Chrome browser.
2. **Launch:** Run the skill and provide the exact Name of the Telegram Channel.
3. **Download:** The skill will scan the chat, create folders locally based on the headers found in the chat, and download only `.pdf` files.

## Inputs
- `channel_name`: The exact name of the channel to scrape.
- `download_dir`: (Optional) The local folder path where you want files saved.
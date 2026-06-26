import requests
import argparse
import sys
import os

def send_file(file_path):
token = os.environ.get("TELEGRAM_BOT_TOKEN")
chat_id = os.environ.get("TELEGRAM_CHAT_ID")

if not token or not chat_id:
print("Error: TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID must be set as environment variables.")
sys.exit(1)

if not os.path.exists(file_path):
print(f"Error: File {file_path} not found.")
sys.exit(1)

if not file_path.endswith('.md'):
print(f"Error: {file_path} is not a valid Markdown (.md) file.")
sys.exit(1)

url = f"https://api.telegram.org/bot{token}/sendDocument"

try:
with open(file_path, 'rb') as f:
files = {'document': f}
data = {'chat_id': chat_id}
response = requests.post(url, files=files, data=data)

if response.status_code == 200:
print("Success: File sent.")
else:
print(f"Error {response.status_code}: {response.text}")
except Exception as e:
print(f"Error: {str(e)}")
sys.exit(1)

if __name__ == "__main__":
parser = argparse.ArgumentParser(description="Upload .md files to Telegram")
parser.add_argument("file_path", help="Path to the .md file")
args = parser.parse_args()
send_file(args.file_path)

#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path
from PIL import Image

if len(sys.argv) != 3:
    print('usage: capture_visible_tweet.py <tweet_url> <output_png>', file=sys.stderr)
    sys.exit(1)

url = sys.argv[1]
out = Path(sys.argv[2]).expanduser().resolve()
out.parent.mkdir(parents=True, exist_ok=True)

script = f'''
tell application "Google Chrome"
  activate
  if (count of windows) = 0 then make new window
  tell front window
    set URL of active tab to "{url}"
  end tell
  delay 2
  set b to bounds of front window
  set u to URL of active tab of front window
  return u & "\n" & ((item 1 of b as text) & "," & (item 2 of b as text) & "," & (item 3 of b as text) & "," & (item 4 of b as text))
end tell
'''
res = subprocess.check_output(['osascript', '-e', script]).decode().splitlines()
current_url = res[0].strip()
if 'x.com/' not in current_url and 'twitter.com/' not in current_url:
    raise SystemExit(f'Unexpected URL after navigation: {current_url}')
left, top, right, bottom = map(int, res[1].split(','))
raw = out.parent / (out.stem + '.window.png')
subprocess.check_call(['/usr/sbin/screencapture', '-x', '-R', f'{left},{top},{right-left},{bottom-top}', str(raw)])
img = Image.open(raw).convert('RGBA')
W, H = img.size
# Main tweet column crop for desktop X layout; conservative and left-column focused.
crop = img.crop((int(W * 0.07), int(H * 0.10), int(W * 0.62), int(H * 0.73)))
crop.save(out)
print(str(out))

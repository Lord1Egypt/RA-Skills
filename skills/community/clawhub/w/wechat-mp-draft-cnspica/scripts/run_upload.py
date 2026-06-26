import sys
sys.argv = [
    'upload_draft.py',
    '--appid', 'wxa4f073c32600c19b',
    '--secret', '47e75b44cbe81261896649aa24a5e222',
    '--md', r'C:\Users\TR\WorkBuddy\20260319105931\智慧养老正式进入AI时代.md',
    '--author', '智慧养老观察家',
]

import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

exec(open('upload_draft.py', encoding='utf-8').read())

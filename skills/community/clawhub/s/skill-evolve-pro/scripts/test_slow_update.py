# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

from pathlib import Path

# 动态获取路径
try:
    from config import SKILL_DIR
except ImportError:
    SKILL_DIR = Path(__file__).parent.parent.resolve()

SKILL_MD = SKILL_DIR / "SKILL.md"
skill_content = SKILL_MD.read_text(encoding='utf-8')

SLOW_UPDATE_START = '<!-- SLOW_UPDATE_START -->'
SLOW_UPDATE_END = '<!-- SLOW_UPDATE_END -->'
start = skill_content.find(SLOW_UPDATE_START)
end = skill_content.find(SLOW_UPDATE_END)
if start != -1 and end != -1:
    inner = skill_content[start + len(SLOW_UPDATE_START):end].strip()
    print('=== SLOW_UPDATE REGION CONTENT ===')
    print(inner)
    print('=== END ===')
    print(f'Length: {len(inner)} chars')
else:
    print('NO SLOW_UPDATE region found')

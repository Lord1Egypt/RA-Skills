import json
from datetime import datetime, timezone
from pathlib import Path
CATEGORIES = ('crypto','us_stock','a_stock','hk_stock','macro','trading_psychology','off_topic','other')
SENTIMENTS = ('bullish','bearish','neutral','mixed')
def iso(value):
    dt = datetime.fromisoformat(value.replace('Z','+00:00'))
    if dt.tzinfo is None: raise ValueError('timestamp must contain timezone')
    return dt.astimezone(timezone.utc)
def read(path):
    text = Path(path).read_text()
    return json.loads(text) if text.lstrip().startswith('[') else [json.loads(s) for s in text.splitlines() if s.strip()]
def write(path, data):
    path = Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')

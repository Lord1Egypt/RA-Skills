import json, re, time
from pathlib import Path

BASE = Path('.')
TRANSCRIPT = BASE / 'transcript.jsonl'
STATUS = BASE / 'final_status.json'
OUT = BASE / 'final_analysis.md'
LOG = BASE / 'final_progress.log'

KEYWORDS = [
    'программа', 'приложение', 'эквалайзер', 'настройк', 'кнопк', 'длинн', 'двойн',
    'карплей', 'gps', 'радио', 'плеер', 'алиса', 'фильм', 'кинотеатр', 'кэш',
    'камера', 'переход', 'ограничение', 'памят', 'оператив', 'звук', 'подголовник',
    'split', 'сплит', 'launcher', 'лаунчер'
]
STOP_PHRASES = ['в общем', 'так сказать', 'ну', 'как бы', 'в данном случае', 'на этом случае']

def write_status(**patch):
    current = {}
    if STATUS.exists():
        try:
            current = json.loads(STATUS.read_text())
        except Exception:
            current = {}
    current.update(patch)
    current['updatedAt'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    STATUS.write_text(json.dumps(current, ensure_ascii=False, indent=2))

def log(msg):
    with LOG.open('a', encoding='utf-8') as f:
        f.write(msg + '\n')

def clean_text(text):
    t = text.strip()
    t = re.sub(r'\s+', ' ', t)
    for s in STOP_PHRASES:
        t = re.sub(rf'(?:{re.escape(s)}[ ,.]*){{2,}}', s + ' ', t, flags=re.I)
    t = re.sub(r'\b(\w+)(?: \1\b){2,}', r'\1', t, flags=re.I)
    return t.strip(' .,-')

def useful(text):
    low = text.lower()
    return any(k in low for k in KEYWORDS) and len(text) > 25

def section_for(text):
    low = text.lower()
    if any(x in low for x in ['кнопк', 'настройк', 'длинн', 'двойн', 'launcher', 'лаунчер', 'split', 'сплит']):
        return 'Управление и интерфейс'
    if any(x in low for x in ['фильм', 'кинотеатр', 'плеер', 'трек', 'кэш', 'алиса']):
        return 'Мультимедиа и контент'
    if any(x in low for x in ['gps', 'координат', 'карплей', 'навига']):
        return 'Навигация и геоданные'
    if any(x in low for x in ['эквалайзер', 'звук', 'подголовник', 'радио']):
        return 'Звук и аудионастройка'
    if any(x in low for x in ['памят', 'оператив', 'служебн']):
        return 'Системные утилиты и производительность'
    if any(x in low for x in ['камера', 'переход', 'ограничение']):
        return 'Камеры и автомобильные функции'
    return 'Прочее'

write_status(stage='loading', percent=0, message='Loading transcript')
log('Loading transcript')
entries = []
for line in TRANSCRIPT.read_text(encoding='utf-8').splitlines():
    if not line.strip():
        continue
    try:
        item = json.loads(line)
    except Exception:
        continue
    txt = clean_text(item.get('text',''))
    if useful(txt):
        entries.append({'start': item.get('start'), 'end': item.get('end'), 'text': txt})

write_status(stage='filtering', percent=25, message=f'Filtered candidate chunks: {len(entries)}')
log(f'Filtered candidate chunks: {len(entries)}')
sections = {
    'Управление и интерфейс': [],
    'Мультимедиа и контент': [],
    'Навигация и геоданные': [],
    'Звук и аудионастройка': [],
    'Системные утилиты и производительность': [],
    'Камеры и автомобильные функции': [],
    'Прочее': [],
}
for i, e in enumerate(entries):
    sections[section_for(e['text'])].append(e)
    if i and i % 10 == 0:
        pct = 25 + int((i / max(1, len(entries))) * 40)
        write_status(stage='grouping', percent=pct, message=f'Grouped {i}/{len(entries)} chunks')

write_status(stage='synthesizing', percent=75, message='Building structured summary')
log('Building structured summary')
lines = ['# Разбор видео: функции и возможности', '']
for sec, items in sections.items():
    if not items:
        continue
    lines.append(f'## {sec}')
    lines.append('')
    seen = set(); count = 0
    for item in items:
        txt = item['text']
        key = re.sub(r'[^a-zа-я0-9]+',' ', txt.lower())[:80]
        if key in seen:
            continue
        seen.add(key); count += 1
        title = txt.split('.')[0][:90].strip().capitalize()
        desc = txt[:220].strip()
        lines.append(f'- **[{item["start"]}-{item["end"]} c] {title}**')
        lines.append(f'  - Кратко: {desc}')
        if count >= 8:
            break
    lines.append('')
lines.append('## Примечание')
lines.append('')
lines.append('- Это первичный структурированный разбор после автоматического извлечения речи.')
lines.append('- В исходном транскрипте есть шум и ошибки распознавания, поэтому формулировки местами требуют ручной доводки.')
OUT.write_text('\n'.join(lines), encoding='utf-8')
write_status(stage='done', percent=100, message='Final structured analysis ready')
log('Done')

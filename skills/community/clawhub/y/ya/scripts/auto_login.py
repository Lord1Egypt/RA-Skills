#!/usr/bin/env python3
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
DEFAULT_SECRET_PATH = SKILL_DIR / 'local' / 'whut_ai_secret.json'
OUTPUT_PATH = SKILL_DIR / 'latest_page_dump.json'
TARGET_HOST = 'whut.ai-augmented.com'
SESSION = 'whut-auto'


def run_cmd(args, check=True):
    res = subprocess.run(args, capture_output=True, text=True)
    if check and res.returncode != 0:
        raise RuntimeError(f'command failed: {args}\nstdout={res.stdout}\nstderr={res.stderr}')
    return res


def ab(*args, check=True):
    cmd = ['agent-browser', '--session', SESSION, *args]
    return run_cmd(cmd, check=check)


def load_secret():
    env_user = os.environ.get('WHUT_USERNAME')
    env_pass = os.environ.get('WHUT_PASSWORD')
    if env_user and env_pass:
        return env_user, env_pass

    secret_path = Path(os.environ.get('WHUT_SECRET_PATH', DEFAULT_SECRET_PATH))
    if secret_path.exists():
        data = json.loads(secret_path.read_text())
        return data['username'], data['password']

    raise RuntimeError(
        'missing credentials: set WHUT_USERNAME/WHUT_PASSWORD, or set WHUT_SECRET_PATH, '
        f'or create {DEFAULT_SECRET_PATH}'
    )


def snapshot():
    res = ab('snapshot', '-i', '--json')
    raw = (res.stdout or '').strip()
    if not raw:
        return {}
    return json.loads(raw)


def refs_map(snap):
    return ((snap.get('data') or {}).get('refs') or {})


def ref_text(meta):
    parts = [
        str(meta.get('role') or ''),
        str(meta.get('name') or ''),
        str(meta.get('description') or ''),
        str(meta.get('value') or ''),
    ]
    return ' '.join(parts).strip().lower()


def find_ref(snap, predicates):
    refs = refs_map(snap)
    for ref, meta in refs.items():
        txt = ref_text(meta)
        for pred in predicates:
            if pred(txt, meta):
                return ref, meta
    return None, None


def click_ref(ref):
    return ab('click', f'@{ref}', check=False)


def fill_ref(ref, text):
    return ab('fill', f'@{ref}', text, check=False)


def press(key):
    return ab('press', key, check=False)


def get_url():
    res = ab('get', 'url', '--json', check=False)
    raw = (res.stdout or '').strip()
    if not raw:
        return ''
    try:
        data = json.loads(raw)
        return ((data.get('data') or {}).get('url') or '')
    except Exception:
        return raw


def get_text():
    res = ab('get', 'text', '--json', check=False)
    raw = (res.stdout or '').strip()
    if not raw:
        return ''
    try:
        data = json.loads(raw)
        return ((data.get('data') or {}).get('text') or '')
    except Exception:
        return raw


def normalize_text(text):
    return re.sub(r'\n{3,}', '\n\n', (text or '').strip())


def extract_questions(text):
    text = normalize_text(text)
    patterns = [
        r'(?:^|\n)(\d+[\.、].*?(?=(?:\n\d+[\.、])|$))',
        r'(?:^|\n)((?:题目|问题)\s*\d*[:：].*?(?=(?:\n(?:题目|问题)\s*\d*[:：])|$))',
    ]
    found = []
    for pattern in patterns:
        for match in re.finditer(pattern, text, flags=re.S | re.M):
            item = normalize_text(match.group(1))
            if item and item not in found:
                found.append(item)
    return found[:20]


def build_page_dump(status):
    time.sleep(2)
    url = get_url()
    text = normalize_text(get_text())
    questions = extract_questions(text)
    payload = {
        'status': status,
        'url': url,
        'captured_at': int(time.time()),
        'has_questions': bool(questions),
        'questions': questions,
        'page_text': text,
    }
    OUTPUT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
    print(json.dumps(payload, ensure_ascii=False))
    return payload


def close_popup_once(snap):
    popup_words = {'关闭', '知道了', '我知道了', '取消', '跳过', 'x', '×'}

    def pred(txt, meta):
        name = str(meta.get('name') or '').strip().lower()
        role = str(meta.get('role') or '').strip().lower()
        return role in {'button', 'link'} and (name in popup_words or '关闭' in txt or 'close' in txt)

    ref, meta = find_ref(snap, [pred])
    if ref:
        click_ref(ref)
        time.sleep(0.8)
        return True
    return False


def find_login_fields(snap):
    def is_user(txt, meta):
        role = str(meta.get('role') or '').lower()
        if role not in {'textbox', 'searchbox', 'combobox', 'spinbutton'}:
            return False
        return any(k in txt for k in ['学号', '账号', '用户名', 'user', 'username', 'account'])

    def is_pass(txt, meta):
        role = str(meta.get('role') or '').lower()
        return role in {'textbox', 'searchbox'} and any(k in txt for k in ['密码', 'password'])

    user_ref, _ = find_ref(snap, [is_user])
    pass_ref, _ = find_ref(snap, [is_pass])

    refs = list(refs_map(snap).items())
    visible_textboxes = [r for r, m in refs if str(m.get('role') or '').lower() in {'textbox', 'searchbox', 'combobox', 'spinbutton'}]
    if not user_ref and visible_textboxes:
        user_ref = visible_textboxes[0]
    if not pass_ref and len(visible_textboxes) >= 2:
        pass_ref = visible_textboxes[1]
    return user_ref, pass_ref


def find_login_button(snap):
    def pred(txt, meta):
        role = str(meta.get('role') or '').lower()
        return role in {'button', 'link'} and any(k in txt for k in ['登录', 'log in', 'sign in', '统一认证登录'])
    return find_ref(snap, [pred])[0]


def is_logged_in():
    url = get_url().lower()
    if TARGET_HOST not in url:
        return False
    if 'oauth2/login' in url or 'auth' in url:
        return False
    snap = snapshot()
    user_ref, pass_ref = find_login_fields(snap)
    return not (user_ref and pass_ref)


def main():
    username, password = load_secret()
    url = sys.argv[1] if len(sys.argv) > 1 else f'https://{TARGET_HOST}'

    ab('open', url)
    time.sleep(2)

    for _ in range(8):
        snap = snapshot()
        changed = close_popup_once(snap)
        if not changed:
            break

    for _ in range(20):
        snap = snapshot()
        close_popup_once(snap)
        user_ref, pass_ref = find_login_fields(snap)
        if user_ref and pass_ref:
            fill_ref(user_ref, username)
            time.sleep(0.4)
            fill_ref(pass_ref, password)
            time.sleep(0.5)
            login_ref = find_login_button(snap)
            if login_ref:
                click_ref(login_ref)
            else:
                press('Enter')
            time.sleep(2)
            if is_logged_in():
                build_page_dump('LOGIN_OK')
                return
        else:
            if is_logged_in():
                build_page_dump('ALREADY_LOGGED_IN')
                return
        time.sleep(1.2)

    payload = {
        'status': 'LOGIN_MAY_HAVE_FAILED',
        'url': get_url(),
        'captured_at': int(time.time()),
        'has_questions': False,
        'questions': [],
        'page_text': normalize_text(get_text()),
    }
    OUTPUT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
    print(json.dumps(payload, ensure_ascii=False))
    sys.exit(1)


if __name__ == '__main__':
    main()

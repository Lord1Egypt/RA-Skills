#!/usr/bin/env python3
import json
import os
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG_PATH = SKILL_DIR / 'references' / 'config.json'
DATA_DIR = Path(os.getenv('TWITTER_LISTEN_COMMENT_DATA_DIR', str(SKILL_DIR / 'data')))
STATE_PATH = DATA_DIR / 'state.json'
LOG_PATH = DATA_DIR / 'run.log'
SEARCH_API_URL = 'https://ai.6551.io/open/twitter_search'
OPENCLAW_BIN = os.getenv('OPENCLAW_BIN', 'openclaw')


def now_iso():
    return datetime.now(timezone.utc).astimezone().isoformat()


def parse_dt(value: str):
    if not value:
        return None
    for fmt in ('%a %b %d %H:%M:%S %z %Y', '%Y-%m-%dT%H:%M:%S%z', '%Y-%m-%dT%H:%M:%S.%f%z'):
        try:
            return datetime.strptime(value, fmt)
        except Exception:
            pass
    try:
        return datetime.fromisoformat(value)
    except Exception:
        return None


def log(msg):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open('a', encoding='utf-8') as f:
        f.write(f'[{now_iso()}] {msg}\n')


def load_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception:
        return default


def save_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


def run(cmd):
    return subprocess.run(cmd, text=True, capture_output=True)


def api_post(url: str, payload: dict):
    token = os.getenv('TWITTER_TOKEN')
    if not token:
        raise RuntimeError('TWITTER_TOKEN missing')
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'},
        method='POST',
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode('utf-8'))


def is_tweet_fresh(tweet, max_age_seconds: int):
    created_dt = parse_dt(tweet.get('createdAt', ''))
    if not created_dt:
        return False
    now_dt = datetime.now(timezone.utc).astimezone()
    return (now_dt - created_dt).total_seconds() <= max_age_seconds


def fetch_latest_tweet(username: str, max_results: int):
    data = api_post(SEARCH_API_URL, {
        'fromUser': username,
        'maxResults': max_results,
        'product': 'Latest',
        'excludeReplies': True,
        'excludeRetweets': True,
    })
    tweets = data.get('data') or []
    if not tweets:
        return None
    latest = tweets[0]
    tweet_id = str(latest.get('id', ''))
    if not tweet_id:
        return None
    return {
        'id': tweet_id,
        'text': latest.get('text', ''),
        'createdAt': latest.get('createdAt', ''),
        'url': f'https://x.com/{username}/status/{tweet_id}',
        'userScreenName': latest.get('userScreenName', username),
        'favoriteCount': latest.get('favoriteCount', 0),
        'replyCount': latest.get('replyCount', 0),
        'retweetCount': latest.get('retweetCount', 0),
    }


def build_reply_prompt(tweet, style):
    constraints = '；'.join(style.get('constraints') or [])
    return (
        '你是 X 评论区用户。请基于下面推文生成一条中文幽默回复。\n'
        '只输出回复正文，不要解释，不要引号。\n'
        f'要求：{style.get("maxSentences", 2)} 句以内；{constraints}。\n\n'
        f'作者：@{tweet.get("userScreenName", "")}\n'
        f'推文链接：{tweet.get("url", "")}\n'
        f'推文正文：{tweet.get("text", "")}'
    )


def generate_reply(agent_target: str, tweet, style):
    res = run([OPENCLAW_BIN, 'agent', '--to', agent_target, '--message', build_reply_prompt(tweet, style), '--json'])
    if res.returncode != 0:
        raise RuntimeError((res.stderr or res.stdout).strip() or 'generate reply failed')
    data = json.loads(res.stdout)
    payloads = data.get('result', {}).get('payloads', [])
    for payload in payloads:
        text = (payload.get('text') or '').strip()
        if text:
            return text.replace('“', '').replace('”', '').strip()
    raise RuntimeError('empty reply text')


def send_notice(config: dict, text: str):
    channel = config.get('notifyChannel', 'telegram')
    target = config.get('notifyTarget') or config.get('agentTarget')
    if not target:
        raise RuntimeError('notifyTarget/agentTarget is empty')
    res = run([OPENCLAW_BIN, 'message', 'send', '--channel', channel, '--target', target, '--message', text, '--json'])
    if res.returncode != 0:
        raise RuntimeError((res.stderr or res.stdout).strip() or 'send notice failed')
    return res.stdout


def build_post_prompt(tweet, reply_text):
    return (
        '你现在要用浏览器去 X（Twitter）给指定推文发表评论。\n'
        '执行要求：\n'
        '1. 必须使用 browser 工具，且 profile="chrome"。\n'
        '2. 打开下面这条推文。\n'
        '3. 点击回复，填入指定评论内容。\n'
        '4. 只有在发送按钮可点击时才发送。\n'
        '5. 不要关闭浏览器页面/tab。\n'
        '6. 执行完成后只输出一段 JSON，不要解释、不要代码块。\n'
        '7. JSON 格式：{"status":"submitted|failed","tweetUrl":"...","replyText":"...","note":"..."}\n\n'
        f'推文链接：{tweet.get("url", "")}\n'
        f'评论内容：{reply_text}'
    )


def parse_post_result(text: str):
    text = (text or '').strip()
    if not text:
        raise RuntimeError('empty post result')
    try:
        return json.loads(text)
    except Exception:
        start = text.find('{')
        end = text.rfind('}')
        if start != -1 and end != -1 and end > start:
            return json.loads(text[start:end+1])
    raise RuntimeError(f'invalid post result: {text[:500]}')


def post_reply(agent_target: str, tweet, reply_text):
    res = run([OPENCLAW_BIN, 'agent', '--to', agent_target, '--message', build_post_prompt(tweet, reply_text), '--json', '--timeout', '180'])
    if res.returncode != 0:
        raise RuntimeError((res.stderr or res.stdout).strip() or 'post reply failed')
    data = json.loads(res.stdout)
    payloads = data.get('result', {}).get('payloads', [])
    for payload in payloads:
        text = (payload.get('text') or '').strip()
        if text:
            post_data = parse_post_result(text)
            if post_data.get('status') != 'submitted':
                raise RuntimeError(f'post submit failed: {json.dumps(post_data, ensure_ascii=False)}')
            return post_data
    raise RuntimeError('empty post result')


def ensure_state_users(state, users):
    state.setdefault('users', {})
    for username in users:
        state['users'].setdefault(username, {
            'last_seen_id': '', 'processed_ids': [], 'last_checked_at': '', 'last_result': ''
        })


def validate_config(config):
    if not (config.get('fromUsers') or []):
        raise RuntimeError('config.fromUsers is empty')
    if not config.get('agentTarget'):
        raise RuntimeError('config.agentTarget is empty')
    if not (config.get('notifyTarget') or config.get('agentTarget')):
        raise RuntimeError('config.notifyTarget/agentTarget is empty')


def process_user(config, state, username):
    user_state = state['users'][username]
    tweet = fetch_latest_tweet(username, int(config.get('maxResultsPerUser', 5)))
    user_state['last_checked_at'] = now_iso()
    if not tweet:
        user_state['last_result'] = 'empty'
        return
    latest_id = str(tweet['id'])
    processed = set(map(str, user_state.get('processed_ids', [])))
    user_state['last_seen_id'] = latest_id
    if latest_id in processed:
        user_state['last_result'] = 'seen'
        return
    max_tweet_age = int(config.get('maxTweetAgeSeconds', 300) or 300)
    if not is_tweet_fresh(tweet, max_tweet_age):
        user_state['last_result'] = 'stale'
        log(f'skip stale @{username} tweet_id={latest_id}')
        return

    send_notice(config, f'检测到@{username}的推文，链接{tweet.get("url", "")}')
    reply_text = generate_reply(config['agentTarget'], tweet, config.get('replyStyle') or {})
    post_result = post_reply(config['agentTarget'], tweet, reply_text)
    send_notice(config, '评论成功')

    processed.add(latest_id)
    user_state['processed_ids'] = list(sorted(processed))[-200:]
    user_state['last_result'] = 'success'
    user_state['last_post'] = {'tweet': tweet, 'replyText': reply_text, 'result': post_result, 'at': now_iso()}
    log(f'success @{username} tweet_id={latest_id} reply={reply_text}')


def run_once(config_path: Path):
    config = load_json(config_path, {})
    validate_config(config)
    users = config.get('fromUsers') or []
    state = load_json(STATE_PATH, {'users': {}})
    ensure_state_users(state, users)
    for username in users:
        try:
            process_user(config, state, username)
        except Exception as e:
            state['users'][username]['last_result'] = 'error'
            state['users'][username]['last_error'] = {'message': str(e), 'at': now_iso()}
            log(f'error @{username}: {e}')
        finally:
            save_json(STATE_PATH, state)


def main():
    args = sys.argv[1:]
    once = '--once' in args
    config_path = DEFAULT_CONFIG_PATH
    if '--config' in args:
        idx = args.index('--config')
        if idx + 1 >= len(args):
            raise RuntimeError('--config needs a path')
        config_path = Path(args[idx + 1]).expanduser().resolve()
    config = load_json(config_path, {})
    interval = int(config.get('pollIntervalSeconds', 10) or 10)
    if once:
        run_once(config_path)
        return 0
    while True:
        run_once(config_path)
        time.sleep(interval)


if __name__ == '__main__':
    sys.exit(main())

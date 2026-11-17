"""Query intel: stepback/decompose/gate/outline (stdlib)."""
import argparse
import json
import re

WORD = re.compile(r'[A-Za-z][A-Za-z0-9.+-]*')


def keywords(q, stop=None):
    stop = stop or set()
    seen, out = set(), []
    for t in WORD.findall(q):
        tl = t.lower()
        if tl in stop or tl in seen or len(tl) < 3:
            continue
        seen.add(tl)
        out.append(t)
    return out


def cmd_stepback(a):
    kws = keywords(a.question)
    principle = ('underlying principle behind: %s'
                 % ', '.join(kws[:4]))
    subs = ['What is %s?' % k for k in kws[:3]]
    subs.append('How do %s compare on 2026 evidence?'
                % ' / '.join(kws[:2]))
    print(json.dumps({'principle': principle, 'sub_questions': subs},
                     indent=2))


def cmd_decompose(a):
    kws = keywords(a.question)
    steps = []
    for i, k in enumerate(kws[:4]):
        steps.append({'step': i + 1, 'query': 'define %s' % k,
                      'depends_on': []})
    steps.append({'step': len(steps) + 1,
                  'query': 'synthesize: %s' % a.question,
                  'depends_on': list(range(1, len(steps) + 1))})
    print(json.dumps({'steps': steps}, indent=2))


def cmd_gate(a):
    conf = a.conf
    kws = keywords(a.query)
    volatile = any(w in a.query.lower() for w in
                   ('2026', 'latest', 'price', 'pricing', 'limit', 'rank',
                    'leaderboard', 'news', 'today', 'current'))
    if volatile:
        decision, reason = 'retrieve', 'time-sensitive terms present'
    elif conf >= 0.85 and len(kws) <= 3:
        decision, reason = 'skip', 'stable knowledge, high confidence'
    else:
        decision, reason = 'retrieve', 'confidence/coverage insufficient'
    print(json.dumps({'query': a.query, 'decision': decision,
                      'reason': reason}, indent=2))


def cmd_outline(a):
    slots = (a.slots or 'contradiction,vacancy,method-transfer,'
             'hostile-evidence').split(',')
    print(json.dumps(
        {'topic': a.topic,
         'sections': [{'h': 'Background', 'need': 'definitions + timeline'},
                      {'h': 'Evidence', 'need': 'span-cited findings'},
                      {'h': 'Breakthrough analysis', 'need': slots},
                      {'h': 'Recommendation',
                       'need': 'pick + fallback + limits'}]}, indent=2))


def main():
    ap = argparse.ArgumentParser(prog='intel.py')
    sub = ap.add_subparsers(dest='cmd', required=True)
    s = sub.add_parser('stepback')
    s.add_argument('question')
    s.set_defaults(f='stepback')
    s = sub.add_parser('decompose')
    s.add_argument('question')
    s.set_defaults(f='decompose')
    s = sub.add_parser('gate')
    s.add_argument('query')
    s.add_argument('--conf', type=float, default=0.5)
    s.set_defaults(f='gate')
    s = sub.add_parser('outline')
    s.add_argument('topic')
    s.add_argument('--slots', default='')
    s.set_defaults(f='outline')
    a = ap.parse_args()
    {'stepback': cmd_stepback, 'decompose': cmd_decompose,
     'gate': cmd_gate, 'outline': cmd_outline}[a.f](a)


if __name__ == '__main__':
    main()

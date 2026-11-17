#!/usr/bin/env python3
"""Validate and render a source-anchored, author-controlled Second Read review.

No language interpretation occurs here. An agent or human supplies the analysis;
this module checks its source bindings, provides deterministic suggested edits,
and embeds the review in an offline interactive editing interface.
"""
import argparse
import hashlib
import json
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
TEMPLATE = SCRIPT_DIR / 'editor_template.html'


class ReviewError(ValueError):
    pass


def fail(message):
    raise ReviewError(message)


def check_str(value, where, allow_empty=False):
    if not isinstance(value, str) or (not allow_empty and not value.strip()):
        fail(f'{where} must be a nonempty string')
    return value


def validate(review):
    if review.get('schema_version') != '1.0':
        fail('schema_version must be 1.0')
    src = review.get('source')
    if not isinstance(src, dict):
        fail('source must be an object')
    blocks = src.get('blocks')
    if not isinstance(blocks, list) or not blocks:
        fail('source.blocks must be a nonempty array')
    ids, block_map = set(), {}
    for i, b in enumerate(blocks):
        if not isinstance(b, dict): fail(f'block {i} is not an object')
        bid = check_str(b.get('id'), f'block {i}.id')
        if bid in ids: fail(f'duplicate block id: {bid}')
        ids.add(bid)
        content = check_str(b.get('text'), f'block {bid}.text')
        spans = b.get('spans', [])
        if not isinstance(spans, list): fail(f'block {bid}.spans must be an array')
        last_end = 0
        for j, span in enumerate(spans):
            if not isinstance(span, dict): fail(f'block {bid}.spans[{j}] must be an object')
            st, en = span.get('start'), span.get('end')
            if type(st) is not int or type(en) is not int or st < last_end or en <= st or en > len(content):
                fail(f'block {bid}.spans[{j}] has invalid/overlapping character offsets')
            last_end = en
        block_map[bid] = b
    text = '\n\n'.join(b['text'] for b in blocks)
    if src.get('text') != text:
        fail('source.text must equal blocks joined by two newlines, with no silent omissions')
    context = review.get('context', [])
    if not isinstance(context, list): fail('context must be an array')
    input_ids = set()
    for c in context:
        cid = check_str(c.get('id'), 'context id')
        if cid in input_ids: fail(f'duplicate context id: {cid}')
        input_ids.add(cid)
        check_str(c.get('label'), f'context {cid}.label')
        check_str(c.get('text'), f'context {cid}.text')
    threads = review.get('threads', [])
    if not isinstance(threads, list): fail('threads must be an array')
    thread_map = {}
    for thread in threads:
        tid = check_str(thread.get('id'), 'thread id')
        if tid in thread_map: fail(f'duplicate thread: {tid}')
        check_str(thread.get('label'), f'thread {tid}.label')
        color = check_str(thread.get('color'), f'thread {tid}.color')
        if len(color) != 7 or color[0] != '#' or any(c not in '0123456789abcdefABCDEF' for c in color[1:]):
            fail(f'thread {tid} requires a six-digit hex color')
        thread_map[tid] = thread
    for b in blocks:
        if b.get('thread') not in thread_map: fail(f'block {b["id"]}: unknown thread')
        for span in b.get('spans', []):
            if span.get('thread') not in thread_map:
                fail(f'block {b["id"]}: unknown span thread')
    suggestions = review.get('suggestions', [])
    if not isinstance(suggestions, list): fail('suggestions must be an array')
    suggestion_ids, suggestion_map = set(), {}
    all_new_ids = set()
    for suggestion in suggestions:
        sid = check_str(suggestion.get('id'), 'suggestion id')
        if sid in suggestion_ids: fail(f'duplicate suggestion: {sid}')
        suggestion_ids.add(sid)
        suggestion_map[sid] = suggestion
        check_str(suggestion.get('title'), f'suggestion {sid}.title')
        check_str(suggestion.get('why'), f'suggestion {sid}.why')
        if suggestion.get('priority') not in ('high','medium','low'):
            fail(f'suggestion {sid}: priority invalid')
        if suggestion.get('thread') not in thread_map: fail(f'suggestion {sid}: unknown thread')
        if suggestion.get('anchor') not in block_map: fail(f'suggestion {sid}: unknown anchor')
        evidence = suggestion.get('evidence')
        if not isinstance(evidence,dict): fail(f'suggestion {sid}: evidence missing')
        eb = evidence.get('block_id')
        if eb not in block_map: fail(f'suggestion {sid}: evidence block unknown')
        quote = check_str(evidence.get('quote'), f'suggestion {sid}.evidence.quote')
        if quote not in block_map[eb]['text']: fail(f'suggestion {sid}: quote is not present verbatim in original')
        ops = suggestion.get('operations')
        if not isinstance(ops,list) or not ops: fail(f'suggestion {sid}: at least one proposed edit required')
        for op in ops:
            k = op.get('type')
            if k=='replace':
                bid=op.get('block_id')
                if bid not in block_map: fail(f'suggestion {sid}: replacement target missing')
                if op.get('before') != block_map[bid]['text']: fail(f'suggestion {sid}: replacement before must equal source block verbatim')
                check_str(op.get('after'), f'suggestion {sid} replacement after')
            elif k=='insert_after':
                if op.get('after_block_id') not in block_map: fail(f'suggestion {sid}: insertion position missing')
                new_id=check_str(op.get('new_id'), f'suggestion {sid} new_id')
                if new_id in block_map or new_id in all_new_ids: fail(f'suggestion {sid}: insertion id collision')
                all_new_ids.add(new_id)
                check_str(op.get('text'), f'suggestion {sid} new paragraph')
                if op.get('thread') not in thread_map: fail(f'suggestion {sid}: invalid insertion thread')
            elif k=='move_after':
                a,b=op.get('block_id'),op.get('after_block_id')
                if a not in block_map or b not in block_map or a==b:
                    fail(f'suggestion {sid}: invalid move')
            elif k=='delete':
                bid=op.get('block_id')
                if bid not in block_map or op.get('before') != block_map[bid]['text']:
                    fail(f'suggestion {sid}: invalid source-bound delete')
            else:
                fail(f'suggestion {sid}: unknown operation {k}')
    questions = review.get('questions', [])
    if not isinstance(questions,list): fail('questions must be an array')
    question_ids=set()
    for q in questions:
        qid=check_str(q.get('id'),'question id')
        if qid in question_ids: fail(f'duplicate question {qid}')
        question_ids.add(qid)
        if q.get('after_block_id') not in block_map: fail(f'question {qid} has no position in reading order')
        check_str(q.get('prompt'), f'question {qid} prompt')
        choices=q.get('choices')
        if not isinstance(choices,list) or len(choices)<2: fail(f'question {qid} has fewer than two choices')
        choice_ids=[]
        for ch in choices:
            choice_ids.append(check_str(ch.get('id'), f'question {qid}.choice id'))
            check_str(ch.get('text'), f'question {qid}.choice text')
        if len(set(choice_ids)) != len(choice_ids): fail(f'question {qid} duplicate choice id')
        if q.get('reading_id') not in choice_ids: fail(f'question {qid} observed reading missing')
        if q.get('suggestion_id') not in suggestion_map: fail(f'question {qid} must link to a proposed change')
        if suggestion_map[q['suggestion_id']]['anchor'] != q['after_block_id']:
            fail(f'question {qid}: suggested change must be anchored to the tested passage')
        check_str(q.get('why'), f'question {qid}.why')
    first_impression = review.get('first_impression')
    if first_impression is not None: check_str(first_impression, 'first_impression')
    digest=hashlib.sha256(text.encode('utf-8')).hexdigest()
    return {"ok":True,"source_sha256":digest,"blocks":len(blocks),"context_inputs":len(context),"threads":len(threads),"proposed_changes":len(suggestions),"questions":len(questions)}


def apply(review, accepted):
    """Reconstruct the complete draft from immutable original and accepted edits.

    This is reproducible, but it is *not* a semantic verification of the new draft.
    """
    validate(review)
    by_id={s['id']:s for s in review.get('suggestions', [])}
    if len(set(accepted))!=len(accepted): fail('duplicate accepted edit')
    unknown=set(accepted)-set(by_id)
    if unknown: fail(f'unknown edit IDs: {sorted(unknown)}')
    blocks=[dict(b) for b in review['source']['blocks']]
    for suggestion in review.get('suggestions', []):
        if suggestion['id'] not in accepted: continue
        for op in suggestion['operations']:
            kind=op['type']
            ix=next((i for i,b in enumerate(blocks) if b['id']==op.get('block_id')),None)
            if kind=='replace':
                if ix is None or blocks[ix]['text']!=op['before']:
                    fail(f'edit conflict: {suggestion["id"]} replacement precondition failed')
                blocks[ix]['text']=op['after']
            elif kind=='insert_after':
                anchor=next((i for i,b in enumerate(blocks) if b['id']==op['after_block_id']),None)
                if anchor is None or any(b['id']==op['new_id'] for b in blocks):
                    fail(f'edit conflict: {suggestion["id"]} insertion position or id')
                blocks.insert(anchor+1, {'id':op['new_id'], 'thread':op['thread'], 'text':op['text']})
            elif kind=='move_after':
                if ix is None: fail(f'edit conflict: {suggestion["id"]} moved block missing')
                moved=blocks.pop(ix)
                anchor=next((i for i,b in enumerate(blocks) if b['id']==op['after_block_id']),None)
                if anchor is None: fail(f'edit conflict: {suggestion["id"]} move destination missing')
                blocks.insert(anchor+1,moved)
            elif kind=='delete':
                if ix is None or blocks[ix]['text']!=op['before']:
                    fail(f'edit conflict: {suggestion["id"]} deletion precondition failed')
                blocks.pop(ix)
    return '\n\n'.join(b['text'] for b in blocks)


def render(review):
    summary=validate(review)
    html=TEMPLATE.read_text(encoding='utf-8')
    payload=json.dumps(review, ensure_ascii=True, separators=(',',':')).replace('</','<\\/')
    return (html.replace('__SECOND_READ_REVIEW_DATA__', payload)
                .replace('__SECOND_READ_SOURCE_DIGEST__', summary['source_sha256']))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='cmd', required=True)
    for cmd in ('validate','render','apply'):
        p=sub.add_parser(cmd)
        p.add_argument('review',type=Path)
        if cmd=='render': p.add_argument('--output',type=Path,required=True)
        if cmd=='apply':
            p.add_argument('--accept',nargs='*',default=[])
            p.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    try:
        review=json.loads(args.review.read_text(encoding='utf-8'))
        if args.cmd=='validate': print(json.dumps(validate(review),indent=2))
        elif args.cmd=='render':
            args.output.write_text(render(review),encoding='utf-8')
            print(json.dumps({"rendered":str(args.output),**validate(review)},indent=2))
        elif args.cmd=='apply':
            result=apply(review,args.accept)
            args.output.write_text(result+'\n',encoding='utf-8')
            print(json.dumps({"output":str(args.output),"edits_applied":args.accept},indent=2))
    except (ValueError, KeyError, TypeError) as exc:
        parser.exit(2,f'Second Read validation error: {exc}\n')


if __name__=='__main__': main()

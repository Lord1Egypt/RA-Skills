"""Adapt pre-upgrade regression *inputs* to the current API, without altering outputs.

Tests still assert real runtime responses. New contract rejection tests bypass this
helper. This only keeps unchanged workflow scenarios executable after API changes.
"""
import json
from pathlib import Path


def project_query(query):
    q=dict(query)
    if 'keywordGroups' in q: return q
    if 'keywords' in q:
        words=q.pop('keywords')
        scopes=q.pop('matchScopes',[2,8])
        mode=q.pop('keywordsSearchType',1)
        q['keywordGroups']=([{'keywords':[w],'matchScopes':scopes} for w in words] if mode==2 and isinstance(words,list) else [{'keywords':words,'matchScopes':scopes}])
    if 'procurementMethod' in q: q['procurementMethods']=[q.pop('procurementMethod')]
    return q


def cli_args(args, state_dir=None):
    args=list(args)
    if not args or '--query-json' not in args: return args
    source='project' if args[0]=='search' else None
    if args[0]=='refine' and state_dir:
        try:
            session=args[args.index('--session-id')+1]
            result=args[args.index('--result-set-id')+1]
            source=json.loads((Path(state_dir)/session/(result+'.json')).read_text())['result_type']
        except (ValueError,IndexError,OSError,KeyError): pass
    if source!='project': return args
    index=args.index('--query-json')+1
    try: query=json.loads(args[index])
    except json.JSONDecodeError: return args
    if isinstance(query,dict): args[index]=json.dumps(project_query(query),ensure_ascii=False)
    return args


def query_field(query, field):
    """Compare unchanged semantic invariants in both supported search families."""
    if 'keywordGroups' not in query: return query[field]
    groups=query['keywordGroups']
    if field=='keywords': return [w for g in groups for w in g['keywords']]
    if field=='keywordsSearchType': return 2 if len(groups)>1 else 1
    if field=='matchScopes':
        assert all(g['matchScopes']==groups[0]['matchScopes'] for g in groups)
        return groups[0]['matchScopes']
    if field=='procurementMethod': return query['procurementMethods'][0]
    value=query[field]
    if field in ("beginTime","endTime") and isinstance(value,str) and len(value)==19 and value[11:] in ("00:00:00","23:59:59"):
        return value[:10]
    return value

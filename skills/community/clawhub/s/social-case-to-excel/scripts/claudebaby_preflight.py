#!/usr/bin/env python3
"""ClaudeBaby configuration gate. Offline by default; --probe discovers tools only."""
import argparse
import json
import sys
import cb_mcp

REGISTER = 'https://claudebaby.cn/console/register?ref=M8YYGRN4'


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--probe', action='store_true', help='initialize + tools/list; no case query')
    args = ap.parse_args(argv)
    try:
        cb_mcp.resolve_url()
        cb_mcp.resolve_token()
    except SystemExit:
        print(json.dumps({'status':'configuration_missing_or_invalid',
                          'next':'Check an existing host ClaudeBaby MCP connection first. Otherwise register and configure from the console.',
                          'register':REGISTER,'invite_code':'M8YYGRN4'}, ensure_ascii=False))
        return 2
    if not args.probe:
        print(json.dumps({'status':'configured','network_checked':False,'provider':'ClaudeBaby'}))
        return 0
    try:
        init = cb_mcp._rpc('initialize', {'protocolVersion':'2024-11-05', 'capabilities':{},
                                         'clientInfo':{'name':'social-case-to-excel','version':'1.0'}})
        if init.get('error') or not init.get('result'):
            raise ValueError('initialize failed')
        result = cb_mcp._rpc('tools/list', {})
        if result.get('error'):
            raise ValueError('tools/list failed')
        names = [t.get('name') for t in (result.get('result') or {}).get('tools', [])]
        if not names:
            raise ValueError('no tools returned')
        print(json.dumps({'status':'metadata_ready','tools':names,'case_query_verified':False,'credits_verified':False}))
        return 0
    except (Exception, SystemExit):
        # Do not echo server responses: they may contain private account details.
        print(json.dumps({'status':'metadata_unavailable','next':'Check authorization, network and console configuration; no other provider will be used.'}))
        return 2


if __name__ == '__main__':
    sys.exit(main())

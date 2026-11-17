#!/usr/bin/env python3
"""ProxyClaw CLI. Explicit V2 credentials; existing key-only callers remain legacy."""
import argparse
import base64
import ipaddress
import json
import os
import re
import subprocess
import sys
import urllib.request
from urllib.parse import urlsplit

COUNTRIES = frozenset('AD AE AF AG AI AL AM AO AQ AR AS AT AU AW AX AZ BA BB BD BE BF BG BH BI BJ BL BM BN BO BQ BR BS BT BV BW BY BZ CA CC CD CF CG CH CI CK CL CM CN CO CR CU CV CW CX CY CZ DE DJ DK DM DO DZ EC EE EG EH ER ES ET FI FJ FK FM FO FR GA GB GD GE GF GG GH GI GL GM GN GP GQ GR GS GT GU GW GY HK HM HN HR HT HU ID IE IL IM IN IO IQ IR IS IT JE JM JO JP KE KG KH KI KM KN KP KR KW KY KZ LA LB LC LI LK LR LS LT LU LV LY MA MC MD ME MF MG MH MK ML MM MN MO MP MQ MR MS MT MU MV MW MX MY MZ NA NC NE NF NG NI NL NO NP NR NU NZ OM PA PE PF PG PH PK PL PM PN PR PS PT PW PY QA RE RO RS RU RW SA SB SC SD SE SG SH SI SJ SK SL SM SN SO SR SS ST SV SX SY SZ TC TD TF TG TH TJ TK TL TM TN TO TR TT TV TW TZ UA UG UM US UY UZ VA VC VE VG VI VN VU WF WS YE YT ZA ZM ZW'.split())

def quoted(value):
    if any(c in value for c in '\r\n\0'):
        raise ValueError('Invalid credential or endpoint characters')
    return '"' + value.replace('\\', '\\\\').replace('"', '\\"') + '"'

def build_config(args, env, metadata=None):
    target = urlsplit(args.url)
    if target.scheme not in ('http', 'https') or not target.hostname or target.username or target.password:
        raise ValueError('A credential-free HTTP(S) target URL is required')
    if not 1 <= args.timeout <= 120:
        raise ValueError('Timeout must be 1-120 seconds')
    country = (args.country or '').upper()
    if country and country not in COUNTRIES:
        raise ValueError('Country must be a valid ISO alpha-2 code')
    for key in ('city', 'state', 'session'):
        val = getattr(args, key)
        if val and not re.fullmatch(r'[A-Za-z0-9_]{1,64}', val):
            raise ValueError('Selector must contain 1-64 letters, digits or underscores')
    if args.asn and not re.fullmatch(r'[0-9]{1,10}', args.asn):
        raise ValueError('ASN must be numeric')
    user, password = env.get('IPLOOP_PROXY_USERNAME'), env.get('IPLOOP_PROXY_PASSWORD')
    v2 = user is not None or password is not None
    if v2:
        if not user or not password or not re.fullmatch(r'[A-Za-z0-9_]+', user):
            raise ValueError('V2 requires both proxy username and proxy password')
        if args.asn:
            raise ValueError('V2 ASN targeting is not available')
        if (args.city or args.state) and not country:
            raise ValueError('V2 state/city targeting requires country')
        if metadata is None:
            portal = env.get('IPLOOP_PORTAL_URL', 'https://platform.iploop.io').rstrip('/')
            p = urlsplit(portal)
            if p.scheme != 'https' or not p.hostname or p.username or p.password or p.query or p.fragment:
                raise ValueError('Portal must be credential-free HTTPS')
            with urllib.request.urlopen(portal + '/v1/meta', timeout=15) as r:
                metadata = json.load(r)
        host = metadata.get('proxy_host')
        port = metadata.get('socks_port' if args.protocol == 'socks5h' else 'http_port')
        if not isinstance(host, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9.-]*', host):
            raise ValueError('Invalid proxy metadata')
        try:
            ipaddress.ip_address(host)
        except ValueError:
            pass
        else:
            raise ValueError('Proxy metadata must identify a domain')
        if isinstance(port, bool) or not isinstance(port, int) or not 1 <= port <= 65535:
            raise ValueError('Invalid proxy metadata')
        auth_user, auth_password = user, password
        for k,v in [('country',country.lower()),('state',args.state),('city',args.city),('session',args.session)]:
            if v:
                auth_user += '-' + k + '-' + v
        endpoint = args.protocol + '://' + host + ':' + str(port)
    else:
        if not env.get('IPLOOP_API_KEY'):
            raise ValueError('Configure credentials from https://platform.iploop.io/')
        if args.state:
            raise ValueError('State selector is a V2 capability')
        if args.protocol != 'http':
            raise ValueError('SOCKS5 requires explicit V2 credentials')
        auth_user, auth_password = 'iploop', env['IPLOOP_API_KEY']
        for k,v in [('country',country),('city',args.city),('session',args.session),('asn',args.asn)]:
            if v:
                auth_password += '-' + k + '-' + v
        endpoint = 'http://proxy.iploop.io:8880'
    auth = auth_user + ':' + auth_password
    return '\n'.join(['proxy = ' + quoted(endpoint), 'proxy-user = ' + quoted(auth), 'url = ' + quoted(args.url)]) + '\n'

def main():
    p = argparse.ArgumentParser(description='Fetch via IPLoop; explicit V2 or legacy credentials')
    p.add_argument('url')
    for flag in ('country','city','state','session','asn'):
        p.add_argument('--' + flag)
    p.add_argument('--protocol', choices=('http','socks5h'), default='http')
    p.add_argument('--format', choices=('raw','markdown'), default='raw')
    p.add_argument('--timeout', type=int, default=30)
    args = p.parse_args()
    try:
        config = build_config(args, os.environ)
        r = subprocess.run(['curl','--config','-','--silent','--show-error','--fail','--max-time',str(args.timeout)], input=config.encode(), capture_output=True, timeout=args.timeout + 5)
        if r.returncode:
            print('Proxy request failed; inspect credentials, availability and target status', file=sys.stderr)
            return 1
        text = r.stdout.decode('utf-8', 'replace')
        if args.format == 'markdown':
            from html import unescape
            text = re.sub(r'<(script|style)\b[^>]*>.*?</\1>', '', text, flags=re.S|re.I)
            text = re.sub(r'<(?:br\s*/?|/p|/h[1-6]|/li)>', '\n', text, flags=re.I)
            text = unescape(re.sub('<[^>]+>', '', text))
        sys.stdout.write(text)
        return 0
    except (ValueError, OSError, KeyError, TypeError, subprocess.TimeoutExpired):
        print('Invalid configuration or request failed; verify selectors and credentials.', file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(main())

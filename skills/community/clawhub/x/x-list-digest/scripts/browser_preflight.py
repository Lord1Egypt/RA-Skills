"""Restore only Hermes' previously authorized dedicated CDP browser."""
import json
import socket
import sys
from pathlib import Path
from urllib.request import urlopen

ROOT=Path.home()/'.hermes/hermes-agent'
PROFILE=Path.home()/'.hermes/chrome-debug'
ENDPOINT='http://127.0.0.1:9234'


def probe():
    try:
        with urlopen(ENDPOINT+'/json/version',timeout=2) as response:
            value=json.load(response)
        return bool(value.get('webSocketDebuggerUrl'))
    except (OSError,ValueError):return False


def dedicated_running():
    import psutil
    for process in psutil.process_iter(['cmdline']):
        try:
            if matches_tokens(process.info['cmdline'] or []):return True
        except psutil.NoSuchProcess:continue
    return False


def matches_tokens(tokens):
    return '--user-data-dir='+str(PROFILE) in tokens and '--remote-debugging-port=9234' in tokens


def dedicated_owner():
    import psutil
    owners=[]
    for process in psutil.process_iter(['cmdline']):
        try:
            tokens=process.info['cmdline'] or []
            if not matches_tokens(tokens):continue
            if any(connection.status==psutil.CONN_LISTEN and connection.family==socket.AF_INET
                   and connection.laddr.ip in ('127.0.0.1','0.0.0.0') and connection.laddr.port==9234
                   for connection in process.net_connections(kind='tcp')):owners.append(process.pid)
        except psutil.NoSuchProcess:continue
    return len(set(owners))==1


def ensure(check=probe,running=dedicated_running,launch=None,owner=dedicated_owner):
    connected=check();active=running()
    if connected:
        if not active or not owner():raise RuntimeError('9234 is occupied by an unverified browser; do not reuse it')
        return {'endpoint':ENDPOINT,'ready':True,'launched':False}
    if active:raise RuntimeError('dedicated browser running but CDP unavailable; do not close it or remove locks')
    if launch is None:
        if not PROFILE.is_dir():raise RuntimeError('authorized dedicated profile missing; do not create or copy credentials')
        sys.path.insert(0,str(ROOT))
        from hermes_cli.browser_connect import chrome_debug_data_dir,launch_chrome_debug
        if Path(chrome_debug_data_dir()).resolve()!=PROFILE.resolve():raise RuntimeError('Hermes profile mismatch')
        launch=lambda:launch_chrome_debug(port=9234)
    launch()
    if not check() or not running() or not owner():raise RuntimeError('dedicated browser failed readiness verification')
    return {'endpoint':ENDPOINT,'ready':True,'launched':True}


if __name__=='__main__':
    try:print(json.dumps(ensure()))
    except Exception as error:
        print(json.dumps({'ready':False,'error':str(error)}));sys.exit(1)

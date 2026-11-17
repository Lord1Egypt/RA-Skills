#!/usr/bin/env python3
"""SMS account flow. Successful CLI results may expose the submitted phone and API Key.

Tokens and raw authentication responses remain inside this process.
Explicit private-pipe callers and injected host adapters remain compatible.
Only HTTPS production requests are exposed by the CLI. Tests inject a transport.
The query module never imports this module and keeps its environment contract.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import selectors
import shutil
import socket
import stat
import subprocess
import sys
import time
from urllib import error, request

ACCOUNT_BASE_URL = 'https://ai.qianlima.com'
PACKAGE_SOURCE_CODE = 'bb3b4102f584028c3830df37'
CONFIG_KEY = 'shell_environment_policy.set.QIANLIMA_API_KEY'


class AccountError(Exception):
    def __init__(self, status, stage=None):
        # Never include remote bodies, URLs, credentials or exception text.
        super().__init__(status)
        self.status = status
        self.stage = stage


class NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class AccountAPI:
    def request(self, method, path, body=None, token=None):
        headers = {'Content-Type': 'application/json'}
        if token:
            headers['Authorization'] = 'Bearer ' + token
        req = request.Request(ACCOUNT_BASE_URL + path, method=method, headers=headers,
                              data=None if body is None else json.dumps(body).encode())
        try:
            with request.build_opener(NoRedirect()).open(req, timeout=20) as response:
                raw = response.read(1048577)
                if len(raw) > 1048576:
                    raise AccountError('invalid_response')
                result = json.loads(raw)
        except error.HTTPError as exc:
            # HTTP errors may contain credentials in their bodies; do not forward them.
            raise AccountError('rate_limited' if exc.code == 429 else 'request_failed') from None
        except (TimeoutError, socket.timeout):
            raise AccountError('result_unknown') from None
        except error.URLError as exc:
            raise AccountError('result_unknown' if isinstance(exc.reason, (TimeoutError, socket.timeout))
                               else 'request_failed') from None
        except (ValueError, OSError):
            raise AccountError('invalid_response') from None
        if not isinstance(result, dict) or type(result.get('code')) is not int:
            raise AccountError('invalid_response')
        if result['code'] != 0:
            status = {40101: 'sms_invalid', 20001: 'phone_invalid',
                      20002: 'rate_limited', 42900: 'rate_limited',
                      20003: 'account_disabled', 40100: 'login_rejected',
                      40102: 'key_invalid', 21002: 'key_unavailable'}.get(result['code'], 'request_failed')
            raise AccountError(status)
        return result.get('data')


class CodexRPC:
    """Native configuration RPC; every response stays in process, never emitted."""
    def __init__(self, home, binary=None):
        binary = binary or shutil.which('codex')
        bundled = '/Applications/ChatGPT.app/Contents/Resources/codex-cli/CodexCLI.app/Contents/MacOS/codex'
        if not binary and Path(bundled).is_file():
            binary = bundled
        if not binary:
            raise AccountError('host_unsupported', 'configuration')
        env = {k: v for k, v in os.environ.items() if k in ('PATH', 'HOME', 'USER', 'TMPDIR', 'LANG')}
        env.update(CODEX_HOME=str(home), RUST_LOG='off')
        self.proc = subprocess.Popen([binary, 'app-server', '--stdio'], stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, env=env, bufsize=0)
        self.seq, self.buffer = 0, b''
        try:
            self.call('initialize', {'clientInfo': {'name': 'qianlima-account', 'version': '1.0.1'},
                                    'capabilities': {'experimentalApi': True}})
            self.proc.stdin.write(b'{"method":"initialized","params":{}}\n')
        except Exception:
            self.close()
            raise AccountError('host_unsupported', 'configuration') from None

    def call(self, method, params):
        self.seq += 1
        try:
            self.proc.stdin.write(json.dumps(dict(id=self.seq, method=method, params=params)).encode() + b'\n')
            with selectors.DefaultSelector() as selector:
                selector.register(self.proc.stdout, selectors.EVENT_READ)
                end = time.monotonic() + 25
                while time.monotonic() < end:
                    if b'\n' not in self.buffer:
                        if not selector.select(min(1, max(0, end-time.monotonic()))):
                            continue
                        chunk = os.read(self.proc.stdout.fileno(), 65536)
                        if not chunk:
                            break
                        self.buffer += chunk
                        if len(self.buffer) > 8 * 1048576:
                            break
                    while b'\n' in self.buffer:
                        line, self.buffer = self.buffer.split(b'\n', 1)
                        response = json.loads(line)
                        if response.get('id') == self.seq:
                            if 'error' in response:
                                raise AccountError('configuration_rejected', 'configuration')
                            return response['result']
        except (OSError, ValueError, KeyError):
            pass
        raise AccountError('configuration_result_unknown', 'configuration')

    def close(self):
        if self.proc.poll() is None:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.proc.kill()
                self.proc.wait()
        self.proc.stdin.close()
        self.proc.stdout.close()


class PrivateEnvironment:
    """Read an existing host configuration through a private execution pipe."""
    def export_private(self, fd):
        """Secret output is allowed ONLY to a separate private pipe, never stdout."""
        if fd < 3:
            raise AccountError('private_pipe_required', 'configuration')
        try:
            target = os.fstat(fd)
            if not stat.S_ISFIFO(target.st_mode):
                raise AccountError('private_pipe_required', 'configuration')
            if any((os.fstat(n).st_dev, os.fstat(n).st_ino) == (target.st_dev, target.st_ino) for n in (1, 2)):
                raise AccountError('private_pipe_required', 'configuration')
            key = self.snapshot()[1]
            if not isinstance(key, str) or not re.fullmatch(r'[A-Za-z0-9_-]{16,256}', key):
                raise AccountError('configuration_unavailable', 'configuration')
            os.write(fd, key.encode())
        except OSError:
            raise AccountError('private_pipe_required', 'configuration') from None


class CodexConfig(PrivateEnvironment):
    """Only adapts Codex's existing environment configuration; no new store."""
    def __init__(self, home=None, binary=None, cwd=None):
        self.home = Path(home or os.environ.get('CODEX_HOME') or Path.home() / '.codex').absolute()
        self.path = self.home / 'config.toml'
        self.cwd = str(Path(cwd or Path.cwd()).resolve())
        self.written = False
        if not self.home.is_dir() or self.path.is_symlink():
            raise AccountError('configuration_unavailable', 'configuration')
        if self.path.exists() and (not self.path.is_file() or self.path.stat().st_uid != os.getuid()):
            raise AccountError('configuration_unavailable', 'configuration')
        self.rpc = CodexRPC(self.home, binary)

    def snapshot(self):
        result = self.rpc.call('config/read', {'includeLayers': True, 'cwd': self.cwd})
        layers = result.get('layers') or []
        user = next((l for l in layers if l.get('name', {}).get('type') == 'user' and
                     Path(l['name'].get('file', '')).resolve() == self.path.resolve() and
                     not l['name'].get('profile')), None)
        if not user or not isinstance(user.get('version'), str):
            raise AccountError('configuration_source_unknown', 'configuration')
        origin = result.get('origins', {}).get(CONFIG_KEY)
        if origin and origin.get('name') != user['name']:
            raise AccountError('configuration_conflict', 'configuration')
        policy = result.get('config', {}).get('shell_environment_policy') or {}
        key = (policy.get('set') or {}).get('QIANLIMA_API_KEY')
        return user['version'], key

    def metadata(self):
        version, key = self.snapshot()
        return dict(configVersion=version, replace_required=bool(key), configuration_source='codex_user_environment')

    def preflight(self, version, replace):
        current, old = self.snapshot()
        if not version or version != current:
            raise AccountError('configuration_changed', 'configuration')
        if old and not replace:
            raise AccountError('replacement_confirmation_required', 'configuration')

    def save(self, key, version, replace):
        self.preflight(version, replace)
        if self.path.is_symlink():
            raise AccountError('configuration_changed', 'configuration')
        try:
            # Protect before native write, including a previously absent configuration.
            fd = os.open(self.path, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
            try:
                if not stat.S_ISREG(os.fstat(fd).st_mode) or os.fstat(fd).st_uid != os.getuid():
                    raise AccountError('configuration_unavailable', 'configuration')
                os.fchmod(fd, 0o600)
            finally:
                os.close(fd)
            self.written = None  # A timed-out native write can have committed; do not claim unchanged.
            response = self.rpc.call('config/value/write', dict(keyPath=CONFIG_KEY, value=key,
                mergeStrategy='upsert', filePath=str(self.path.resolve()), expectedVersion=version))
            self.written = True
            os.chmod(self.path, 0o600)
            if response.get('status') != 'ok' or self.snapshot()[1] != key:
                raise AccountError('configuration_written_not_loaded', 'configuration')
        except OSError:
            raise AccountError('configuration_write_failed', 'configuration') from None


    def close(self):
        self.rpc.close()


class PrivateHandoff:
    """Transfer a credential to the caller; never claims persistent configuration."""
    def __init__(self, fd):
        self.fd = fd
        self.written = False
        self.delivered = False

    def preflight(self, version=None, replace=False):
        if self.fd is None or self.fd < 3:
            raise AccountError('private_pipe_required', 'handoff')
        try:
            target = os.fstat(self.fd)
            if not stat.S_ISFIFO(target.st_mode):
                raise AccountError('private_pipe_required', 'handoff')
            for n in (1, 2):
                visible = os.fstat(n)
                if (visible.st_dev, visible.st_ino) == (target.st_dev, target.st_ino):
                    raise AccountError('private_pipe_required', 'handoff')
        except OSError:
            raise AccountError('private_pipe_required', 'handoff') from None

    def save(self, key, version=None, replace=False):
        self.preflight()
        try:
            if os.write(self.fd, key.encode()) != len(key.encode()):
                raise AccountError('credential_handoff_unknown', 'handoff')
            self.delivered = True
        except OSError:
            raise AccountError('credential_handoff_failed', 'handoff') from None

    def close(self):
        pass


def legal_versions(api):
    versions = {}
    for kind, field in [('TERMS', 'agreementVersion'), ('PRIVACY', 'privacyVersion')]:
        result = api.request('GET', '/api/legal?type=' + kind)
        if not isinstance(result, dict) or not isinstance(result.get('version'), str) or not result['version'].strip():
            raise AccountError('agreement_unavailable', 'legal')
        # Version identifiers only, never expose arbitrary legal endpoint data.
        if not re.fullmatch(r'[A-Za-z0-9_.-]{1,100}', result['version']):
            raise AccountError('agreement_unavailable', 'legal')
        versions[field] = result['version']
    return versions


def prepare(api, pending_query=True, has_key=False):
    from qianlima_skill import AUTH_ERROR_RULES
    # Keep CLI compatibility; the shared introduction applies with or without
    # an existing key or pending query. Authorization/context live in the flow.
    del api, pending_query, has_key
    rule = AUTH_ERROR_RULES['MISSING_API_KEY']
    guidance = rule.get('guidance') or '\n'.join(rule['next_steps'])
    return dict(status='prepared', guidance=guidance)


def normalize_register_input(data):
    """Validate local input; the calling Agent owns conversation authorization.

    Omitted consent is supported. Explicit false still prevents execution.
    Accept code as a compatibility alias, but never guess between conflicting codes.
    """
    if not isinstance(data, dict) or data.get('action') not in ('send', 'verify'):
        raise AccountError('invalid_input', 'input')
    if 'consent' in data:
        if data['consent'] is False:
            raise AccountError('consent_required', 'input')
        if data['consent'] is not True:
            raise AccountError('invalid_consent', 'input')
    phone = data.get('phone')
    if not isinstance(phone, str) or not re.fullmatch(r'1\d{10}', phone, flags=re.ASCII):
        raise AccountError('phone_invalid', 'input')
    normalized = dict(data)
    if data['action'] == 'verify':
        if 'smsCode' in data and 'code' in data and data['smsCode'] != data['code']:
            raise AccountError('code_conflict', 'input')
        code = data['smsCode'] if 'smsCode' in data else data.get('code')
        if code is None or code == '':
            raise AccountError('code_required', 'input')
        if not isinstance(code, str) or not re.fullmatch(r'[0-9]{6}', code):
            raise AccountError('code_invalid', 'input')
        normalized['smsCode'] = code
        normalized.pop('code', None)
    return normalized


INPUT_ERROR_HINTS = {
    'invalid_input': '输入必须是 JSON 对象，action 为 send 或 verify。',
    'consent_required': '调用显式传入 consent=false，本次未执行；不得自动改成 true 后重试。',
    'invalid_consent': 'consent 可省略；如传入，必须是 JSON 布尔值，不接受字符串、数字或 null。',
    'phone_invalid': 'phone 必须是用户本轮提供的 11 位手机号字符串，不猜测或补齐号码。',
    'code_required': 'verify 必须提供 smsCode；兼容别名 code。承接本轮用户已提供的验证码。',
    'code_invalid': '验证码必须是 6 位 ASCII 数字字符串，保留前导零，不猜测或补齐验证码。',
    'code_conflict': 'smsCode 与 code 不一致；根据本轮用户输入核对，不自行选取其中一个。',
}


def register(data, api, config=None):
    stage = 'input'
    try:
        data = normalize_register_input(data)
        phone = data.get('phone')
        if data['action'] == 'send':
            if config is not None:
                config.preflight(data.get('configVersion'), data.get('replaceConfirmed') is True)
            stage = 'sms'
            api.request('POST', '/api/auth/sms/send', {'phone': phone})
            return dict(status='sms_sent', phone=phone, expires_in_seconds=600)
        return verify(data, api, config)
    except AccountError as exc:
        result = dict(status=exc.status, stage=exc.stage or stage, configuration_written=False)
        if result['stage'] == 'input' and exc.status in INPUT_ERROR_HINTS:
            result.update(request_sent=False, agent_instruction=INPUT_ERROR_HINTS[exc.status])
        return result


def verify(data, api, config):
    stage, token, written = 'configuration', None, False
    result = dict(status='configuration_unavailable', configuration_written=False)
    try:
        if config is not None:
            config.preflight(data.get('configVersion'), data.get('replaceConfirmed') is True)
        # Backend-required fields are owned by the script, not conversation state.
        # Fetch before submitting the SMS code; never retry login or send SMS here.
        stage = 'legal'
        versions = legal_versions(api)
        payload = {k: data[k] for k in ('phone', 'smsCode')}
        payload.update(versions, sourceCode=PACKAGE_SOURCE_CODE)
        stage = 'login'
        login = api.request('POST', '/api/auth/login', payload)
        if not isinstance(login, dict):
            raise AccountError('invalid_response')
        token = login.get('accessToken')
        if not isinstance(token, str) or not re.fullmatch(r'[!-~]+', token):
            token = None
        result.update(login_completed=True, phone=data['phone'])
        if type(login.get('newUser')) is bool:
            result['new_user'] = login['newUser']
        stage = 'key'
        view = login.get('defaultApiKey')
        if not isinstance(view, dict) or view.get('status') != 'ACTIVE':
            raise AccountError('key_unavailable')
        key = view.get('apiKey')
        if not valid_key(key):
            key_id = view.get('keyId')
            if type(key_id) is not int or key_id <= 0 or not token:
                raise AccountError('key_unavailable')
            view = api.request('POST', f'/api/api-keys/{key_id}/reveal', {}, token)
            if not isinstance(view, dict) or view.get('status') != 'ACTIVE' or view.get('keyId') != key_id:
                raise AccountError('key_unavailable')
            key = view.get('apiKey')
        if not valid_key(key):
            raise AccountError('key_unavailable')
        result.update(key_obtained=True, balance_available=False, welcome_granted=False)
        try:
            if not token:
                raise AccountError('token_unavailable')
            points = api.request('GET', '/api/points/account', token=token)
            if isinstance(points, dict) and type(points.get('availablePoints')) is int:
                result.update(balance_available=True, available_points=points['availablePoints'])
            if isinstance(points, dict):
                result['welcome_granted'] = (result.get('new_user') is True and
                    points.get('welcomeStatus') == 'NEW_GRANT' and points.get('welcomePoints') == 500)
        except AccountError:
            pass
        if config is None:
            # Agent continues the same configuration flow as a user-supplied Key.
            # An available credential is not evidence of persistence or loading.
            result.update(status='credential_available', api_key=key,
                          configuration_written=False, current_environment_loaded=False)
        else:
            stage = 'configuration'
            config.save(key, data.get('configVersion'), data.get('replaceConfirmed') is True)
            if isinstance(config, PrivateHandoff):
                result.update(status='credential_ready', credential_handed_off=True,
                              configuration_written=False, current_environment_loaded=False)
            else:
                written = True
                result.update(status='configuration_saved', configuration_written=True,
                              current_environment_loaded=False)
    except AccountError as exc:
        written = written or getattr(config, 'written', False)
        result.update(status=exc.status, stage=exc.stage or stage, configuration_written=written)
    except KeyboardInterrupt:
        result.update(status='cancelled', stage=stage,
                      configuration_written=getattr(config, 'written', written))
        if 'login_completed' not in result:
            result['login_completed'] = None if stage == 'login' else False
    finally:
        if token:
            try:
                api.request('POST', '/api/auth/logout', {}, token)
                result['logout_confirmed'] = True
            except AccountError:
                result['logout_confirmed'] = False
        else:
            result['logout_confirmed'] = False
        # No disk session, raw response or token; only the default success exposes api_key.
    return result


def valid_key(value):
    return isinstance(value, str) and value.startswith('qlm_') and bool(re.fullmatch(r'[A-Za-z0-9_-]{16,256}', value))


def main(config_factory=None):
    parser = argparse.ArgumentParser(description='千里马会话账号接入（验证成功返回 API Key，尚未配置）')
    commands = parser.add_subparsers(dest='command', required=True)
    prep = commands.add_parser('prepare', help='在本地取得首次登录引导')
    prep.add_argument('--no-query', action='store_true')
    prep.add_argument('--has-key', action='store_true')
    reg = commands.add_parser('register')
    reg.add_argument('--input-stdin', action='store_true', required=True)
    load = commands.add_parser('environment', help='将已有宿主配置加载至私有管道，不执行查询')
    load.add_argument('--output-fd', type=int, required=True)
    reg.add_argument('--credential-fd', type=int, help='兼容旧调用：显式指定私有管道时不在结果中返回 Key；默认无需此参数')
    args = parser.parse_args()
    config = None
    try:
        config = config_factory() if config_factory else None
        api = AccountAPI()
        if args.command == 'prepare':
            result = prepare(api, not args.no_query, args.has_key)
            if config is not None:
                result.update(config.metadata())
        elif args.command == 'environment':
            if config is None:
                raise AccountError('use_execution_environment', 'configuration')
            config.export_private(args.output_fd)
            result = dict(status='environment_ready')
        else:
            raw = sys.stdin.read(16385)
            if len(raw) > 16384:
                raise AccountError('invalid_input', 'input')
            data = json.loads(raw)
            if (config is None and args.credential_fd is not None
                    and isinstance(data, dict) and data.get('action') == 'verify'):
                config = PrivateHandoff(args.credential_fd)
                config.preflight()
            result = register(data, api, config)
    except AccountError as exc:
        result = dict(status=exc.status, stage=exc.stage or 'prepare')
    except KeyboardInterrupt:
        result = dict(status='cancelled', configuration_written=getattr(config, 'written', False))
    except Exception:
        result = dict(status='operation_failed', stage='local',
                      configuration_written=getattr(config, 'written', False))
    finally:
        if config is not None:
            config.close()
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result['status'] in ('prepared', 'sms_sent', 'credential_available', 'credential_ready', 'configuration_saved', 'environment_ready') else 1


if __name__ == '__main__':
    raise SystemExit(main())

#!/usr/bin/env python3
import argparse

p = argparse.ArgumentParser()
p.add_argument('--device', choices=['android', 'harmonyos', 'iphone'], required=True)
p.add_argument('--mode', choices=['bigmodel', 'third-party', 'self-hosted'], required=True)
args = p.parse_args()

print('[next] deployment guide')
print(f'- device: {args.device}')
print(f'- model mode: {args.mode}')
print('- python env: use the repo-local .venv for all install and run commands')

if args.device == 'android':
    print('- on phone: enable developer options, USB debugging, and accept authorization prompt')
    print('- install and enable ADB Keyboard')
elif args.device == 'harmonyos':
    print('- on phone: enable developer options, USB debugging, and if needed wireless debugging')
else:
    print('- follow docs/ios_setup/ios_setup.md from the Open-AutoGLM repo')

if args.mode == 'bigmodel':
    print('- prepare base-url=https://open.bigmodel.cn/api/paas/v4 and model=autoglm-phone')
    print('- run commands after: source .venv/bin/activate')
elif args.mode == 'third-party':
    print('- collect base-url, model name, and api key from the provider')
    print('- run commands after: source .venv/bin/activate')
else:
    print('- start a self-hosted OpenAI-compatible /v1 endpoint first')
    print('- run commands after: source .venv/bin/activate')

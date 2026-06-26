"""
Login with Polling Script

Launches QR code login and polls every 10 seconds to check
whether cookies have been obtained and are valid.

Usage: python -m src.login_with_polling
"""

import os
import sys
import time
import signal

from .auth import load_cookies, is_cookie_valid, login_with_qr_code, COOKIE_FILE

POLL_INTERVAL = 10  # seconds
MAX_POLLS = 18  # 18 * 10s = 180s max wait time

poll_count = 0
poll_active = True
login_succeeded = False


def start_login_process():
    """
    Start the auth login process by directly calling the exported function.
    This avoids spawning a child process.
    """
    global login_succeeded
    print('🚀 Starting QR code login process...')
    print('   A browser window will open shortly. Please scan the QR code.\n')

    try:
        login_with_qr_code()
        login_succeeded = True
        print('\n✅ Login process completed successfully.')
    except Exception as err:
        if not login_succeeded:
            print(f'❌ Login process failed: {err}')


def poll_cookie_status():
    """Poll to check if cookies have been obtained and are valid."""
    global poll_count, login_succeeded

    poll_count += 1
    elapsed = poll_count * POLL_INTERVAL

    print(f'\n🔍 [Poll #{poll_count}] Checking cookie status... ({elapsed}s elapsed)')

    # Step 1: Check if .cookies.json file exists
    if not os.path.exists(COOKIE_FILE):
        print('   📂 Cookie file not found yet. Waiting for QR scan...')
        if poll_count >= MAX_POLLS:
            print('\n⏰ Timeout: Maximum polling time (180s) reached.')
            print('   Please restart the login process and try again.')
            cleanup(1)
        return

    # Step 2: Cookie file exists - try to load it
    cookies = load_cookies()
    if not cookies or not isinstance(cookies, list) or len(cookies) == 0:
        print('   📂 Cookie file exists but is empty or invalid. Waiting...')
        if poll_count >= MAX_POLLS:
            print('\n⏰ Timeout reached. Cookie file is not valid.')
            cleanup(1)
        return

    print(f'   📂 Cookie file found! Contains {len(cookies)} cookies.')

    # Step 3: Validate cookies by calling the user_info API
    print('   🔐 Validating cookies against Tencent Docs API...')
    try:
        valid = is_cookie_valid(cookies)

        if valid:
            login_succeeded = True
            print('\n' + '=' * 60)
            print('🎉 LOGIN SUCCESSFUL!')
            print('=' * 60)
            print(f'   ✅ Cookies are valid ({len(cookies)} cookies loaded)')
            print(f'   📁 Cookie file: {COOKIE_FILE}')
            print('=' * 60)
            print('\n✅ You are now logged in and ready to use Tencent Docs Markdown!\n')
            cleanup(0)
        else:
            print('   ⚠️  Cookies exist but validation failed. May still be logging in...')
            if poll_count >= MAX_POLLS:
                print('\n⏰ Timeout reached. Cookies could not be validated.')
                print('   Try running: python -m src.auth --force')
                cleanup(1)
    except Exception as err:
        print(f'   ❌ Validation error: {err}')
        if poll_count >= MAX_POLLS:
            cleanup(1)


def cleanup(exit_code: int = 0):
    """Cleanup and exit."""
    global poll_active
    poll_active = False
    sys.exit(exit_code)


def signal_handler(sig, frame):
    """Handle graceful shutdown."""
    print('\n\n🛑 Login cancelled by user.')
    cleanup(0)


def main():
    """Main entry point."""
    global poll_active

    print('=' * 60)
    print('  Tencent Docs Markdown - Login with Polling')
    print(f'  Poll interval: {POLL_INTERVAL}s | Max wait: {MAX_POLLS * POLL_INTERVAL}s')
    print('=' * 60)
    print('')

    # Check if already logged in
    existing_cookies = load_cookies()
    if existing_cookies:
        print('🔍 Found existing cookies, validating...')
        valid = is_cookie_valid(existing_cookies)
        if valid:
            print('✅ Already logged in! Cookies are valid.')
            print(f'   {len(existing_cookies)} cookies loaded from {COOKIE_FILE}')
            sys.exit(0)
        print('⚠️  Existing cookies are expired. Starting fresh login...\n')

    # Handle graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Start the login process in a thread
    import threading
    login_thread = threading.Thread(target=start_login_process, daemon=True)
    login_thread.start()

    # Start polling every 10 seconds
    print(f'\n⏱️  Starting cookie polling (every {POLL_INTERVAL}s)...\n')

    while poll_active and poll_count < MAX_POLLS:
        time.sleep(POLL_INTERVAL)
        try:
            poll_cookie_status()
        except SystemExit:
            raise
        except Exception as err:
            print(f'   Polling error: {err}')


if __name__ == '__main__':
    main()

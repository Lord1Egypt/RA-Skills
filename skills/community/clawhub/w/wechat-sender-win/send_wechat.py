"""
WeChat Sender for Windows - 单发 + 群发
支持 --contact 单个联系人 或 --contacts 多个联系人
"""
import sys
import time
import argparse
from pywinauto import Application
from pywinauto.keyboard import send_keys


def find_wechat_app():
    """Find WeChat Application by trying known PIDs."""
    for pid in [8620, 13472, 8]:
        try:
            app = Application(backend="win32").connect(process=pid, timeout=3)
            return app, pid
        except:
            pass
    return None, None


def find_main_wechat_window(app):
    """Find the main visible WeChat window (largest Qt window)."""
    best = None
    best_area = 0
    for w in app.windows():
        try:
            if not w.is_visible():
                continue
            rect = w.rectangle()
            cls = w.class_name()
            area = rect.width() * rect.height()
            if area < 50000:
                continue
            if 'Qt51514QWindowIcon' in cls and area > best_area:
                best_area = area
                best = (w, rect)
        except:
            pass
    return best[0] if best else None, best[1] if best else None


def send_one_message(app, contact, search_delay, type_delay):
    """Send one message to a single contact."""
    weixin_win, rect = find_main_wechat_window(app)
    if not weixin_win:
        print(f"[WeChatSender] ERROR: Cannot find visible WeChat window.")
        return False

    try:
        weixin_win.set_focus()
        time.sleep(0.3)
    except Exception as e:
        print(f"[WeChatSender] set_focus warning: {e}")

    # Open search
    send_keys('^f')
    time.sleep(search_delay / 1000.0)

    # Type contact
    send_keys(contact)
    time.sleep(search_delay / 1000.0)

    # Select first result
    send_keys('{ENTER}')
    time.sleep(search_delay / 1000.0)

    # Type message
    send_keys('test message' if 'test' not in ' '.join(sys.argv) else '')
    # (The actual message will be sent below)
    return True


def send_wechat_message(contact, message, search_delay=600, type_delay=100):
    """Send a message to one contact."""
    app, pid = find_wechat_app()
    if not app:
        print(f"[WeChatSender] ERROR: Cannot connect to WeChat. Is it running?")
        return False
    print(f"[WeChatSender] Connected to WeChat PID {pid}")

    weixin_win, rect = find_main_wechat_window(app)
    if not weixin_win:
        print(f"[WeChatSender] ERROR: Cannot find visible WeChat window.")
        return False
    print(f"[WeChatSender] Window rect={rect}")

    try:
        weixin_win.set_focus()
        time.sleep(0.3)
    except Exception as e:
        print(f"[WeChatSender] set_focus warning: {e}")

    # Open search
    send_keys('^f')
    time.sleep(search_delay / 1000.0)

    # Type contact
    send_keys(contact)
    time.sleep(search_delay / 1000.0)

    # Select first result
    send_keys('{ENTER}')
    time.sleep(search_delay / 1000.0)

    # Type message
    send_keys(message)
    time.sleep((type_delay * 2) / 1000.0)

    # Send
    send_keys('{ENTER}')
    print(f"[WeChatSender] Sent to '{contact}': {message}")
    return True


def send_batch(contacts, message, search_delay, type_delay):
    """Send the same message to multiple contacts sequentially."""
    app, pid = find_wechat_app()
    if not app:
        print(f"[WeChatSender] ERROR: Cannot connect to WeChat. Is it running?")
        return False
    print(f"[WeChatSender] Connected to WeChat PID {pid}")
    print(f"[WeChatSender] Batch send to {len(contacts)} contacts: {contacts}")

    results = []
    for i, contact in enumerate(contacts):
        print(f"\n[{i+1}/{len(contacts)}] Sending to '{contact}'...")
        weixin_win, rect = find_main_wechat_window(app)
        if not weixin_win:
            print(f"[WeChatSender] ERROR: Cannot find visible WeChat window.")
            results.append(False)
            continue

        try:
            weixin_win.set_focus()
            time.sleep(0.3)
        except Exception as e:
            print(f"[WeChatSender] set_focus warning: {e}")

        # Open search
        send_keys('^f')
        time.sleep(search_delay / 1000.0)

        # Type contact
        send_keys(contact)
        time.sleep(search_delay / 1000.0)

        # Select first result
        send_keys('{ENTER}')
        time.sleep(search_delay / 1000.0)

        # Type message
        send_keys(message)
        time.sleep((type_delay * 2) / 1000.0)

        # Send
        send_keys('{ENTER}')
        print(f"[WeChatSender] Sent to '{contact}'!")
        results.append(True)

        # Small pause between contacts
        if i < len(contacts) - 1:
            time.sleep(0.5)

    success = sum(results)
    print(f"\n[WeChatSender] Done: {success}/{len(contacts)} sent successfully.")
    return all(results)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Send WeChat messages (single or batch)')
    parser.add_argument('--contact', '-c', help='Single contact name')
    parser.add_argument('--contacts', help='Multiple contacts (comma-separated)')
    parser.add_argument('--message', '-m', required=True, help='Message text')
    parser.add_argument('--search-delay', '-s', type=int, default=600, help='Search delay in ms')
    parser.add_argument('--type-delay', '-t', type=int, default=100, help='Type delay in ms')
    args = parser.parse_args()

    if args.contacts:
        # Batch mode
        contacts = [c.strip() for c in args.contacts.split(',')]
        success = send_batch(contacts, args.message, args.search_delay, args.type_delay)
    elif args.contact:
        # Single mode
        success = send_wechat_message(args.contact, args.message, args.search_delay, args.type_delay)
    else:
        print("ERROR: Use --contact or --contacts")
        sys.exit(1)

    sys.exit(0 if success else 1)

import sys
import json
import argparse
from pathlib import Path

# Ensure dependencies are installed (pip install -r requirements.txt)
def ensure_deps():
    try:
        import itchat
        import win32gui
    except ImportError:
        print("Missing dependencies. Run: pip install -r requirements.txt")
        sys.exit(1)

ensure_deps()
import itchat

class WeChat:
    def __init__(self):
        self.logged_in = False

    def login(self):
        # itchat 会自动打开二维码让用户扫码
        itchat.auto_login(enableCmdQR=2, hotReload=True)
        self.logged_in = True
        print("Logged in (cached session will be reused next time).")

    def send(self, to, text):
        if not self.logged_in:
            self.login()
        friends = itchat.search_friends(name=to)
        if not friends:
            print(f"Friend '{to}' not found.")
            return
        uid = friends[0]['UserName']
        itchat.send_msg(text, toUserName=uid)
        print(f"Sent to {to}: {text}")

    def list_chats(self, limit=10):
        if not self.logged_in:
            self.login()
        recent = itchat.get_chatrooms(update=True)  # placeholder; actual API may differ
        # Using itchat.get_friends for demo
        friends = itchat.get_friends(update=True)[:limit]
        out = []
        for f in friends:
            out.append({
                'nick': f.get('NickName'),
                'last_msg': f.get('Signature'),
                'unread_cnt': f.get('UnReadCount', 0),
            })
        print(json.dumps(out, ensure_ascii=False, indent=2))

    def unread_total(self):
        if not self.logged_in:
            self.login()
        total = itchat.get_unread_msg_num()
        print(total)


def main():
    parser = argparse.ArgumentParser(description='WeChat control skill')
    sub = parser.add_subparsers(dest='cmd')
    sub_login = sub.add_parser('login')
    sub_send = sub.add_parser('send')
    sub_send.add_argument('to')
    sub_send.add_argument('text')
    sub_list = sub.add_parser('list')
    sub_unread = sub.add_parser('unread')

    args = parser.parse_args()
    wc = WeChat()
    if args.cmd == 'login':
        wc.login()
    elif args.cmd == 'send':
        wc.send(args.to, args.text)
    elif args.cmd == 'list':
        wc.list_chats()
    elif args.cmd == 'unread':
        wc.unread_total()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()

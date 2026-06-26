import time
from pathlib import Path
from huami import run as huami_run


class BrushStepManager:
    def __init__(self, config_path=None):
        from config import Config
        self.config = Config(config_path)

    def run(self, min_steps=None, max_steps=None, account_name=None):
        if min_steps is None:
            min_steps = self.config.get_min_steps()
        if max_steps is None:
            max_steps = self.config.get_max_steps()

        accounts = self.config.get_accounts()
        use_fake_ip = self.config.should_use_fake_ip()

        results = []
        for account in accounts:
            username = account.get('username', '')
            password = account.get('password', '')
            name = account.get('name', username)

            # 如果指定了账号名称，只处理该账号
            if account_name and name != account_name:
                continue

            if not username or not password:
                print(f"[!] Skip: {name} (incomplete)")
                continue

            for attempt in range(3):
                try:
                    print(f"[*] Processing account: {name}")
                    result = huami_run(username, password, min_steps, max_steps, use_fake_ip)
                    print(f"[*] Result: {result}")
                    if isinstance(result, dict):
                        result["name"] = name
                    results.append(result)
                    break
                except Exception as e:
                    if attempt < 2:
                        print(f"[!] Retry {name}: {e}")
                        time.sleep(5)
                    else:
                        print(f"[X] Failed: {name} - {e}")
                        results.append({"success": False, "name": name, "error": str(e)})

        return results

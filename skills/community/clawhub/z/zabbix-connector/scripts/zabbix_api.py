import urllib.request
import json
import os
import sys
import ssl

# Resolve .env relative to this script's directory, so it works regardless
# of where the skill is cloned/installed.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(SCRIPT_DIR, '..', '.env')

def load_my_env():
    if os.path.exists(ENV_PATH):
        with open(ENV_PATH, 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, val = line.strip().split('=', 1)
                    os.environ[key.strip()] = val.strip()

load_my_env()
ZABBIX_URL = os.environ.get("ZABBIX_URL")
ZABBIX_TOKEN = os.environ.get("ZABBIX_TOKEN")


class ZabbixDirect:
    def __init__(self, url, token):
        self.api_url = f"{url.rstrip('/')}/api_jsonrpc.php"
        self.token = token

    def _call(self, method, params):
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "auth": self.token,
            "id": 1
        }
        data = json.dumps(payload).encode('utf-8')

        # Use a clean, honest User-Agent instead of browser spoofing
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'OpenClaw-ZabbixSkill/1.0'
        }
        req = urllib.request.Request(self.api_url, data=data, headers=headers)

        # Use the system's default SSL context, which verifies certificates.
        # This protects against Man-in-the-Middle attacks.
        context = ssl.create_default_context()

        with urllib.request.urlopen(req, context=context) as response:
            return json.loads(response.read().decode()).get("result")

    def get_host_id(self, host_name):
        params = {"filter": {"host": [host_name]}}
        hosts = self._call("host.get", params)
        return hosts[0]['hostid'] if hosts and len(hosts) > 0 else None

    def host_get(self, filter=None, groupids=None, output="extend"):
        params = {"output": output}
        if filter:
            params["filter"] = filter
        if groupids:
            params["groupids"] = groupids
        return self._call("host.get", params)

    def trigger_get(self, hostids=None, triggerids=None, output="extend", only_true=True):
        params = {"output": output, "only_true": only_true}
        if hostids:
            params["hostids"] = hostids
        if triggerids:
            params["triggerids"] = triggerids
        return self._call("trigger.get", params)

    def problem_get(self, hostids=None, recent=True, output="extend", limit=10):
        params = {"output": output, "recent": recent, "limit": limit}
        if hostids:
            params["hostids"] = hostids
        return self._call("problem.get", params)

    def event_get(self, objectids=None, output="extend"):
        params = {"output": output}
        if objectids:
            params["objectids"] = objectids
        return self._call("event.get", params)

    def event_acknowledge(self, eventids, message, action=6):
        params = {"eventids": eventids, "message": message, "action": action}
        return self._call("event.acknowledge", params)

    def history_get(self, itemids, time_from, output="extend", limit=100):
        params = {"output": output, "itemids": itemids, "time_from": time_from, "limit": limit}
        return self._call("history.get", params)

    @staticmethod
    def format_severity(severity):
        mapping = {
            "4": "High",
            "3": "Average",
            "2": "Warning",
            "1": "Info",
            "0": "Info"
        }
        return mapping.get(str(severity), "Unknown")

    def get_active_problems_report(self):
        hosts = self.host_get()
        active_hostids = [h["hostid"] for h in hosts if h["status"] == "0"]
        problems = self.problem_get(hostids=active_hostids, limit=50)

        report = {}
        for p in problems:
            # Try to extract host name from problem name
            host_name = "Unknown"
            if "[" in p['name']:
                host_name = p['name'].split(']')[0].replace('[', '').strip()

            if host_name not in report:
                report[host_name] = []

            report[host_name].append({
                "severity": self.format_severity(p['severity']),
                "raw_severity": int(p['severity']),
                "name": p['name'].split(' - ', 1)[-1] if ' - ' in p['name'] else p['name'],
                "date": p['clock'],
                "url": f"{self.api_url.replace('api_jsonrpc.php', 'tr_events.php?triggerid={}&eventid={}').format(p['objectid'], p['eventid'])}"
            })

        # Sort each host by severity (desc) and date (desc)
        for host in report:
            report[host].sort(key=lambda x: (x['raw_severity'], int(x['date'])), reverse=True)

        return report

    def get_host_problems(self, host_name):
        hostid = self.get_host_id(host_name)
        if not hostid:
            return None
        problems = self.problem_get(hostids=[hostid], recent=True)
        # Sort by severity (desc) then clock (desc)
        if problems:
            problems.sort(key=lambda x: (int(x['severity']), int(x['clock'])), reverse=True)
        return problems


# Generic usage example
if __name__ == "__main__":
    if ZABBIX_URL and ZABBIX_TOKEN:
        zb = ZabbixDirect(ZABBIX_URL, ZABBIX_TOKEN)
        host = sys.argv[1] if len(sys.argv) > 1 else None
        if host:
            problems = zb.get_host_problems(host)
            print(f"Problems for {host}:", json.dumps(problems, indent=2))
        else:
            print("Usage: python zabbix_api.py <host_name>")
    else:
        print("Error: ZABBIX_URL or ZABBIX_TOKEN not configured.")

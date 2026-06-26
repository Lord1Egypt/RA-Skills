import sys,os,json,ast
from datetime import datetime
sys.stdout.reconfigure(encoding="utf-8")
BASE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT=os.path.join(BASE,"xuanself_glucose_report_2026.md")
RAW=os.path.join(BASE,"xuanself_raw_202604090015.json")
with open(RAW,encoding="utf-8",errors="replace") as f: raw=json.load(f)
def sj(s):
    if not s or s.strip() in("None","[]","{}"):return None
    try: return json.loads(s)
    except: pass
    try: return ast.literal_eval(s)
    except: return None
ecom=sj(raw.get("ecommerce","")) or []
market=sj(raw.get("market",""))
vk=sj(raw.get("vk","")) or []
tg_d=sj(raw.get("telegram",""))
ecom=ecom if isinstance(ecom,list) else []
vk=vk if isinstance(vk,list) else []
tg=tg_d.get("google_site_results",[]) if isinstance(tg_d,dict) else []
tam=(market or{}).get("TAM",{});sam=(market or{}).get("SAM",{});som=(market or{}).get("SOM",{})
def fu(v):
    if not v: return "N/A"
    v=float(v)
    if v>=1e9: return "${:.1f}B".format(v/1e9)
    if v>=1e6: return "${:.1f}M".format(v/1e6)
    return "${:,.0f}".format(v)
NOW=datetime.now().strftime("%Y年%m月%d日")
ecom_s=sorted(ecom,key=lambda x:float(x.get("price") or 99999))
L=[]
def A(t): L.append(t+"\n")

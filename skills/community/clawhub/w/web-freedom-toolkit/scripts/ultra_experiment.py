import json
import os
from curl_cffi import requests
from lxml import html

def ultra_experiment():
    print("--- [ULTRA PHANTOM: DATADOME SOTA BREACH] ---")
    target = "https://www.datadome.co/blog/"
    
    print(f"Targeting: {target} via Chrome124 Impersonation...")
    try:
        # Nuclear Protocol Mimicry
        r = requests.get(target, impersonate="chrome124", timeout=20)
        
        print(f"L7 Response: {r.status_code} | Payload: {len(r.text)} bytes")
        
        if r.status_code == 200 and len(r.text) > 1000:
            tree = html.fromstring(r.content)
            headlines = [t.text_content().strip() for t in tree.xpath('//h2')[:3]]
            print(f"!!! Breach Success !!! Headlines: {headlines}")
            
            # Asset consistency
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            proof_path = os.path.join(base_dir, "assets/ULTRA_VICTORY.json")
            with open(proof_path, "w") as f:
                json.dump({"method": "impersonate_chrome124", "headlines": headlines}, f, indent=2)
            print(f"Evidence locked at: {proof_path}")
    except Exception as e:
        print(f"Experimental Failure: {e}")

if __name__ == "__main__":
    ultra_experiment()

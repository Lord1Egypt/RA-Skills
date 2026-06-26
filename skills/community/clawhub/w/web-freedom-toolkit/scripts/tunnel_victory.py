import os
import requests
import json

def tunnel_victory_cross_check():
    """
    SOTA Cross-check: Validates that the Python Relay Tunnel is correctly 
    forwarding traffic across Namespace/Docker boundaries.
    """
    print("--- [SOTA CROSS-CHECK: TUNNEL VICTORY] ---")
    tunnel_port = 9223
    
    try:
        # Check Version through Tunnel
        resp = requests.get(f"http://127.0.0.1:{tunnel_port}/json/version", timeout=5).json()
        browser_ver = resp.get('Browser')
        
        if browser_ver:
            print(f"✅ Tunnel Verified! Connected to: {browser_ver}")
            
            # Asset logging
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            log_path = os.path.join(base_dir, "assets/TUNNEL_STATUS.json")
            with open(log_path, "w") as f:
                json.dump({"tunnel_port": tunnel_port, "browser": browser_ver, "status": "UP"}, f, indent=2)
            
            print(f"Tunnel status logged to: {log_path}")
            return True
        else:
            print("❌ Tunnel check returned invalid data.")
            return False
            
    except Exception as e:
        print(f"❌ Tunnel connectivity failure: {e}")
        return False

if __name__ == "__main__":
    tunnel_victory_cross_check()

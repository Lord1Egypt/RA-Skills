import time
import subprocess
import json

def simulate_pinned_product_detection():
    print("[*] Simulating detection of a pinned product...")
    # In a real scenario, this would involve listening to TikTok Live events
    # For this simulation, we'll just assume a product is pinned after a delay
    time.sleep(5) # Simulate delay for detection

    pinned_product_info = {
        "product_id": "tiktok_product_123",
        "product_name": "สินค้าทดสอบ",
        "price": 99.00,
        "quantity": 1
    }

    print(f"[+] Pinned product detected: {pinned_product_info['product_name']}")
    
    # Save pinned product info to a temporary file for cart_automation.py
    with open('pinned_product.json', 'w', encoding='utf-8') as f:
        json.dump(pinned_product_info, f, ensure_ascii=False, indent=2)

    print("[*] Calling cart_automation.py to add product to cart...")
    # Execute the cart automation script
    try:
        subprocess.run(["python3", "cart_automation.py"], check=True)
        print("[+] Cart automation script executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"[-] Error executing cart_automation.py: {e}")

if __name__ == "__main__":
    simulate_pinned_product_detection()

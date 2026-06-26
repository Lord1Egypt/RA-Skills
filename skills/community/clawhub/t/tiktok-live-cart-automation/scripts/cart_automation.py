import json
import time

def add_to_cart_and_checkout():
    print("[*] Starting cart automation...")
    try:
        with open("pinned_product.json", "r", encoding="utf-8") as f:
            pinned_product = json.load(f)
        
        product_id = pinned_product.get("product_id")
        product_name = pinned_product.get("product_name")
        price = pinned_product.get("price")
        quantity = pinned_product.get("quantity")

        print(f"[+] Adding {quantity} x {product_name} (ID: {product_id}, Price: {price}) to cart...")
        time.sleep(3) # Simulate adding to cart
        print("[+] Product added to cart successfully.")

        print("[*] Navigating to checkout page...")
        time.sleep(3) # Simulate navigation
        print("[+] Successfully navigated to checkout page.")
        print("[!] Please manually click \"Place Order\" to complete the purchase.")

    except FileNotFoundError:
        print("[-] Error: pinned_product.json not found. Please ensure a pinned product is detected first.")
    except json.JSONDecodeError:
        print("[-] Error: Could not decode pinned_product.json. Invalid JSON format.")
    except Exception as e:
        print(f"[-] An unexpected error occurred: {e}")

if __name__ == "__main__":
    add_to_cart_and_checkout()

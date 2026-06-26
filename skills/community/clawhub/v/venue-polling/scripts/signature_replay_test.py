import base64
import json
from collections import OrderedDict

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

CAPTURED_SUCCESS = {
    "timestamp": "1776415153",
    "nonce": "ttl63xm4",
    "signature": (
        "gLtYxxgfOqVnqaOZ35ROGBDG2T0j952Ifz3FdeCaxmzFNHpGXUHXL7EerAtTybcS+"
        "px8CU5Dkw4O25DkIq7w7+HMCipSqwo2jtKHfSmVKC297QU81Brh+DhbDxIDdtk0y"
        "QAUETEFLw+wsrYOpeZ4UbfuAO6CCcXfPykdP7z3/3rzhyamxsKAPHkoU/gv7m2FkW"
        "T1CKy9kpEII2kqlaudYUFA649M3GF3SZbC5yh9rnI0lxAGbg/siKuHXT2XHjdYhM6"
        "mfbOy/0K3NZo14+8ha5GIz258QeM7u0PwnHxtLhgIoLZ/6BcigyHZys6c4MrlQ/TH"
        "LSzXVnZeHFq1Z2gH0A=="
    ),
    "body": (
        '{"venueSportId":1,"areaItems":[{"areaDate":"2026-04-20","areaId":47,'
        '"areaName":"七号场(2F)","endTime":"21:00","packageId":null,"price":"45",'
        '"showStatus":"AVAILABLE","sportId":1,"sportName":"羽毛球","startTime":"20:00",'
        '"status":"NORMAL","uniqNo":"47_20260420_20:00_21:00","checked":true,'
        '"row":6,"col":11}]}'
    ),
}


def load_private_key():
    with open("rsa_private_key.pem", "r", encoding="utf-8") as f:
        return serialization.load_pem_private_key(
            f.read().encode("utf-8"),
            password=None,
            backend=default_backend(),
        )


def rsa_sign(private_key, sign_string, algorithm):
    signature = private_key.sign(
        sign_string.encode("utf-8"),
        padding.PKCS1v15(),
        algorithm,
    )
    return base64.b64encode(signature).decode("utf-8")


def canonical_json(value):
    return json.dumps(value, separators=(",", ":"), ensure_ascii=False)


def build_sign_string(order_data, body, nonce, timestamp, mode):
    area_items = canonical_json(order_data["areaItems"])
    if mode == "raw_body":
        return body
    if mode == "body_nonce_timestamp":
        return f"{body}&nonce={nonce}&timestamp={timestamp}"
    if mode == "kv_nonce_timestamp":
        return (
            f"venueSportId={order_data['venueSportId']}"
            f"&areaItems={area_items}"
            f"&nonce={nonce}"
            f"&timestamp={timestamp}"
        )
    raise ValueError(f"Unsupported mode: {mode}")


def replay():
    private_key = load_private_key()
    captured_obj = json.loads(CAPTURED_SUCCESS["body"], object_pairs_hook=OrderedDict)
    modes = ["raw_body", "body_nonce_timestamp", "kv_nonce_timestamp"]
    digests = [
        ("SHA256", hashes.SHA256()),
        ("SHA1", hashes.SHA1()),
        ("SHA512", hashes.SHA512()),
    ]
    found_match = False

    print("Running offline replay check against the captured createOrder request.")

    for mode in modes:
        sign_string = build_sign_string(
            captured_obj,
            CAPTURED_SUCCESS["body"],
            CAPTURED_SUCCESS["nonce"],
            CAPTURED_SUCCESS["timestamp"],
            mode,
        )
        for digest_name, digest in digests:
            signature = rsa_sign(private_key, sign_string, digest)
            is_match = signature == CAPTURED_SUCCESS["signature"]
            print(f"mode={mode:<20} digest={digest_name:<6} match={is_match}")
            if is_match:
                found_match = True
                print("Matched sign string:")
                print(sign_string)

    if not found_match:
        print("No combination matched the captured signature.")
        print("The local PEM or the real app signing algorithm is different.")


if __name__ == "__main__":
    replay()

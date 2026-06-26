import base64
import json
from collections import OrderedDict

from cryptography.exceptions import InvalidSignature
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


def load_public_key():
    with open("rsa_private_key.pem", "rb") as f:
        private_key = serialization.load_pem_private_key(
            f.read(),
            password=None,
            backend=default_backend(),
        )
    return private_key.public_key()


def canonical_json(value):
    return json.dumps(value, separators=(",", ":"), ensure_ascii=False)


def candidate_sign_strings():
    order_data = json.loads(CAPTURED_SUCCESS["body"], object_pairs_hook=OrderedDict)
    body = CAPTURED_SUCCESS["body"]
    nonce = CAPTURED_SUCCESS["nonce"]
    timestamp = CAPTURED_SUCCESS["timestamp"]
    area_items = canonical_json(order_data["areaItems"])
    area_item = canonical_json(order_data["areaItems"][0])

    return [
        ("raw_body", body),
        ("body_nonce_timestamp", f"{body}&nonce={nonce}&timestamp={timestamp}"),
        ("nonce_timestamp_body", f"nonce={nonce}&timestamp={timestamp}&{body}"),
        ("timestamp_nonce_body", f"timestamp={timestamp}&nonce={nonce}&{body}"),
        (
            "area_then_venue",
            f"areaItems={area_items}&venueSportId={order_data['venueSportId']}"
            f"&nonce={nonce}&timestamp={timestamp}",
        ),
        (
            "venue_then_area",
            f"venueSportId={order_data['venueSportId']}&areaItems={area_items}"
            f"&nonce={nonce}&timestamp={timestamp}",
        ),
        (
            "json_area_then_venue",
            f"{area_items}&venueSportId={order_data['venueSportId']}"
            f"&nonce={nonce}&timestamp={timestamp}",
        ),
        (
            "json_area_item_then_venue",
            f"{area_item}&venueSportId={order_data['venueSportId']}"
            f"&nonce={nonce}&timestamp={timestamp}",
        ),
    ]


def verify_signature(public_key, signature_b64, sign_string, algorithm):
    try:
        public_key.verify(
            base64.b64decode(signature_b64),
            sign_string.encode("utf-8"),
            padding.PKCS1v15(),
            algorithm,
        )
        return True
    except InvalidSignature:
        return False


def main():
    public_key = load_public_key()
    print("Derived public key:")
    print(
        public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode("utf-8")
    )

    algorithms = [
        ("SHA256", hashes.SHA256()),
        ("SHA1", hashes.SHA1()),
        ("SHA512", hashes.SHA512()),
    ]

    print("Verifying candidate sign strings against captured X-Ca-Signature.")
    found = False

    for name, sign_string in candidate_sign_strings():
        for digest_name, digest in algorithms:
            ok = verify_signature(
                public_key,
                CAPTURED_SUCCESS["signature"],
                sign_string,
                digest,
            )
            print(f"candidate={name:<24} digest={digest_name:<6} verified={ok}")
            if ok:
                found = True
                print("Verified sign string:")
                print(sign_string)

    if not found:
        print("No candidate sign string verified with the derived public key.")
        print("This means the captured signature was generated with a different key or different sign string.")


if __name__ == "__main__":
    main()

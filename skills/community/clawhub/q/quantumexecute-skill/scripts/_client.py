"""Shared helper: create User client from environment variables only."""
import os

def get_client():
    from qe.user import User as Client
    key = os.environ.get("QE_API_KEY")
    secret = os.environ.get("QE_API_SECRET")
    if not key or not secret:
        raise ValueError("请设置环境变量 QE_API_KEY 和 QE_API_SECRET")
    return Client(key, secret)

#!/usr/bin/env python3
from client import print_json, request_json


def main():
    response = request_json("GET", "/openclaw/fonts")
    print_json(response)


if __name__ == "__main__":
    main()

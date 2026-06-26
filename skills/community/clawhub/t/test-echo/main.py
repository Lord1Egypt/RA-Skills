# -*- coding: utf-8 -*-
import sys
import json

def main():
    try:
        # Read input parameters (official standard way)
        input_data = json.loads(sys.stdin.read())
        name = input_data.get("name", "stranger")

        # Return result
        return json.dumps({
            "status": "success",
            "msg": f"Hello, {name}! Skill executed successfully",
            "your_input": name
        }, ensure_ascii=False)

    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": str(e)
        }, ensure_ascii=False)

if __name__ == "__main__":
    print(main())
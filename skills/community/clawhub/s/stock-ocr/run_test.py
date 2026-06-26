import subprocess
import sys

result = subprocess.run(
    [sys.executable, r"C:\Users\Administrator\.workbuddy\skills\stock-ma20-ocr\scripts\capture_ma20.py", "07226", "--keep"],
    capture_output=True,
    text=True,
    encoding='utf-8',
    errors='ignore'
)

print("STDOUT:")
print(result.stdout)
print("\nSTDERR:")
print(result.stderr)
print(f"\nExit code: {result.returncode}")

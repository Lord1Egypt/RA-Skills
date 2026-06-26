import argparse
import os
import sys
import webbrowser

def main():
    parser = argparse.ArgumentParser(description="Prompt to open an HTML file in browser")
    parser.add_argument("file_path", help="Path to the HTML file")
    args = parser.parse_args()

    file_path = args.file_path
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        sys.exit(1)

    try:
        choice = input("是否通过浏览器打开该 HTML 预览？[y/N]: ").strip().lower()
        if choice in ('y', 'yes'):
            abs_path = os.path.abspath(file_path)
            webbrowser.open(abs_path)
            print("已在浏览器中打开预览。")
        else:
            print("已取消打开浏览器。")
    except KeyboardInterrupt:
        print("\n操作已取消。")
    except Exception as e:
        print(f"打开浏览器失败: {e}")

if __name__ == "__main__":
    main()

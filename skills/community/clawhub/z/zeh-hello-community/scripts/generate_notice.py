import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", required=True)
    parser.add_argument("--content", required=True)
    args = parser.parse_args()

    print(f"标题：{args.title}")
    print("适用对象：社区老师 / 网格员 / 政务服务人员")
    print(f"正文：{args.content}")
    print("注意事项：请按通知要求准时落实。")

if __name__ == "__main__":
    main()

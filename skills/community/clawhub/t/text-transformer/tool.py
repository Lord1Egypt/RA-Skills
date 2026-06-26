import sys

def main():
    # 检查是否传入了参数
    if len(sys.argv) < 2:
        print("Error: 请提供需要处理的文本。")
        return
    
    # 获取大模型传入的文本片段
    user_input = sys.argv[1]
    
    # 核心处理逻辑：转换为大写
    processed_data = user_input.upper()
    
    # 打印输出，OpenClaw 的大模型会读取这里的控制台回显
    print(f"转换结果为: {processed_data}")

if __name__ == "__main__":
    main()

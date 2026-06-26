def main():
    print("🤖 Ptrade 策略结构演示")
    print("Ptrade 策略通常直接在券商提供的 Ptrade 客户端中运行。")
    print('''示例策略结构:
def initialize(context):
    g.security = '600519.SS'

def handle_data(context, data):
    order(g.security, 100)
''')

if __name__ == "__main__":
    main()

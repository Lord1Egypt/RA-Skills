import pywencai

def main():
    print("🤖 Pywencai 实际问财语义查询演示")
    try:
        print("正在查询: '非st涨停' ...")
        res = pywencai.get(query='非st涨停')
        if res is None or res.empty:
            print("⚠️ 获取数据为空，可能是网络或接口变动！")
        else:
            print(f"✅ 成功获取 {len(res)} 条问财数据。")
            print(res.head())
    except Exception as e:
        print(f"❌ 获取数据失败: {e}")

if __name__ == "__main__":
    main()

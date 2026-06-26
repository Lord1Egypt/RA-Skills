def main():
    print("🤖 TqSdk (天勤量化) 实际接口调用演示")
    try:
        from tqsdk import TqApi, TqAuth
        print("✅ TqSdk API 导入成功。")
        print("使用示例: api = TqApi(auth=TqAuth('账号', '密码')); quote = api.get_quote('SHFE.cu2101')")
    except ImportError:
        print("❌ 未安装 tqsdk")
    except Exception as e:
        print(f"❌ 运行失败: {e}")

if __name__ == "__main__":
    main()

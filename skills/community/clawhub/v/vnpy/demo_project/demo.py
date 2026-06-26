def main():
    print("🤖 VN.PY 实际框架初始化演示")
    try:
        from vnpy.trader.engine import MainEngine
        from vnpy.trader.event import EventEngine
        print("正在初始化事件引擎和主引擎...")
        event_engine = EventEngine()
        main_engine = MainEngine(event_engine)
        print("✅ VN.PY 引擎初始化成功！")
    except ImportError:
        print("❌ 未安装 vnpy")
    except Exception as e:
        print(f"❌ 运行失败: {e}")

if __name__ == "__main__":
    main()

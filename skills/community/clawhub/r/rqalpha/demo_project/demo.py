def main():
    print("🤖 RQAlpha 实际策略架构演示")
    try:
        import rqalpha
        from rqalpha.api import order_shares
        print("✅ RQAlpha API 导入成功。")
        print("RQAlpha 通常通过命令行运行，如: rqalpha run -f strategy.py -d ~/.rqalpha/bundle")
    except ImportError:
        print("❌ 未安装 rqalpha")
    except Exception as e:
        print(f"❌ 运行失败: {e}")

if __name__ == "__main__":
    main()

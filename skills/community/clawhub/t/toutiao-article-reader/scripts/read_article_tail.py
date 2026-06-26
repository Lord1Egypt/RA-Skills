            if args.summary:
                if result.get('ai_summary') and result['ai_summary'].get('success'):
                    summary = result['ai_summary']
                    print(f"概述：{summary.get('overview', '')}")
                    key_points = summary.get('key_points', [])
                    if key_points:
                        print("\n关键点:")
                        for i, point in enumerate(key_points, 1):
                            print(f"{i}. {point}")
                else:
                    summary = reader.summarize(result['content'])
                    print(summary)
            else:
                preview = result['content'][:1000]
                print(preview)
                if len(result['content']) > 1000:
                    print(f"\n... (还有 {len(result['content']) - 1000} 字)")
            
            print("\n" + "="*60)
            print("✅ 阅读完成")
            print("="*60)
            
            # 导出
            if args.export:
                output_path = args.output or f"article.{args.export}"
                try:
                    export_file = ArticleExporter.export(result, output_path, args.export)
                    print(f"\n📥 已导出：{export_file}")
                except Exception as e:
                    print(f"\n❌ 导出失败：{e}")
        else:
            print(f"\n❌ 阅读失败：{result['error']}")
            sys.exit(1)


if __name__ == '__main__':
    main()

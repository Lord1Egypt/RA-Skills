# report-instructions 技能示例

## 示例 1: 最简单的用法

```
用户: /report comprehensive

系统执行:
1. 解析参数：action=comprehensive
2. 收集所有可用数据
3. 生成HTML报告
4. 保存到 reports/health-report-2025-12-31.html

输出:
✅ 健康报告已生成
文件路径: reports/health-report-2025-12-31.html
```

## 示例 2: 生成季度报告

```
用户: /report comprehensive last_quarter

输出:
✅ 健康报告已生成
数据范围: 2025-10-01 至 2025-12-31
```

## 示例 3: 自定义章节

```
用户: /report custom 2024-01-01,2024-12-31 biochemical,medication

输出:
✅ 健康报告已生成
包含章节: 生化检查、用药分析
```

## 示例 4: 指定输出文件名

```
用户: /report comprehensive all all my-report.html

输出:
✅ 健康报告已生成
文件路径: reports/my-report.html
```

## 示例 5: 查看命令帮助

```
用户: /report 帮助

输出完整的命令格式和参数说明
```

# 报告格式详细规范

## 文件命名
- 报告：`<端名>-<模块名>功能测试报告-YYYY-MM-DD.docx`
- 截图目录：`reports/<模块>-test-<日期>/screenshots/`
- 截图命名：`模块-操作-状态.png`

## 截图命名示例

| 场景 | 命名示例 |
|------|---------|
| 页面初始 | `feedback-init.png` |
| 新增弹窗打开 | `feedback-add-open.png` |
| 填写中 | `feedback-add-filling.png` |
| 必填校验报错 | `feedback-add-validation.png` |
| 新增成功 | `feedback-add-success.png` |
| 列表验证 | `feedback-add-list-verify.png` |
| 编辑弹窗 | `feedback-edit-open.png` |
| 编辑成功 | `feedback-edit-success.png` |
| 删除取消 | `feedback-delete-cancel.png` |
| 删除成功 | `feedback-delete-success.png` |
| 提交审核取消 | `feedback-submit-cancel.png` |
| 提交审核成功 | `feedback-submit-success.png` |
| 查看审批页 | `feedback-approval-view.png` |
| 边界值报错 | `feedback-boundary-empty.png` |
| 导出 | `feedback-export.png` |

## Word 文档结构

```
封面
  大标题（18pt 加粗居中）
  测试日期、测试对象、测试范围、执行规范（10.5pt）

目录
  Heading 1: "目录"
  TOC 域: TOC \o "1-3" \h \z \u
  提示文字: 打开 Word 后如未自动刷新，请右键目录选择"更新域"

1. 测试概述（Heading 1）
   本次测试范围说明、可闭环模块、受限模块、异常模块

2. 测试环境（Heading 1）
   系统地址、账号信息、测试工具、截图目录

3. 总体结论（Heading 1）
   3.1 已完成闭环且验证通过的模块
   3.2 受限无法闭环的模块
   3.3 存在异常的模块
   3.4 明确识别的异常清单

4. 登录过程（Heading 1）
   登录页截图 + 登录成功截图

5. 分模块测试记录（Heading 1）
   5.x 模块名（Heading 2）
     测试范围说明
     5.x.1 基础验证（Heading 3）
       截图序列 + 结论文字
     5.x.2 闭环样本A（Heading 3）
       测试数据说明
       截图序列 + 结论文字
     5.x.3 边界值测试（Heading 3）
       截图序列 + 结论文字

6. 缺陷汇总（Heading 1）
   6.x 缺陷标题（Heading 2）
     现象描述
     复现步骤
     截图引用
     严重程度：高/中/低

7. 最终结论（Heading 1）
   各模块结论汇总
   遗留问题说明
```

## 字体规范

| 元素 | 字体 | 大小 | 样式 |
|------|------|------|------|
| 封面大标题 | 微软雅黑 | 18pt | 加粗居中 |
| 正文 | 微软雅黑 | 10.5pt | 常规 |
| Heading 1 | 微软雅黑 | 16pt | 加粗 |
| Heading 2 | 微软雅黑 | 13.5pt | 加粗 |
| Heading 3 | 微软雅黑 | 12pt | 加粗 |
| 图注 | 微软雅黑 | 9.5pt | 居中 |

## 图片规范
- 宽度统一：6.0 英寸
- 图注格式：`图N 描述文字`（居中，9.5pt）
- 缺图处理：输出 `【缺图】文件名` 占位，不跳过

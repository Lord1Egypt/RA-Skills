---
name: platform-script
description: "提供自研业务平台的脚本模板和编码规范。当用户需要编写 Groovy 后端脚本、JavaScript 表单脚本、SQL 查询、附件处理等代码时使用此技能。"
metadata: { "openclaw": { "emoji": "📝", "requires": { "bins": [] } } }
---

# 平台脚本技能

为自研业务平台提供全面的脚本模板和编码规范。

## 何时使用

✅ **使用此技能的情况：**

- "帮我写一个平台脚本"
- "需要数据增删改查的脚本"
- "表单验证脚本怎么写"
- "动态控制下拉框选项"
- "合并多个 CI 附件为 PDF"
- "发送邮件的脚本"
- "SQL 查询/分页脚本"
- "审批流程相关脚本"
- "根据我的平台规则写代码"

## 何时不使用

❌ **不使用此技能的情况：**

- 通用编程问题（不使用平台特定 API）
- 其他平台的脚本代码
- 与平台无关的代码需求

## 技能位置
`skills/platform-script-skills/`

## 使用方法
当用户请求平台相关的脚本代码时，读取 `references/` 目录中的完整模板文件，理解平台的特殊脚本规则，生成符合规范的可用代码。

## 核心能力

### 1. 基础脚本操作
- 数据创建 (DataModelUtils.createCIByCIClassName)
- 数据删除 (DataModelUtils.deleteCi, deleteCis)
- 数据修改 (saveCi)
- 数据查询 (getCIByPK, getCIByAttr, queryForListMap)
- 脚本调用 (ScriptUtils.runScriptByCode)

### 2. 表单脚本操作
- 数据验证 (validatorFunctions)
- 动态字段控制 (disabledAttributes, dynamicDisabledAttrs)
- 字段值变化 (changeFunctions)
- 下拉框选项控制 (scriptFilterInOptions, setSelectOptionsFunc)
- 字段显示控制 (controlFieldDisplayFunc)
- 自动补全 (controlAutoCompleteFunc)
- 父子表单通信 (addObserver, notifyParent)
- 智能回填 (initBackFillData, initNestedFormData)

### 3. SQL 脚本操作
- 数据查询 SQL
- 数据修改 SQL (JDBCUtils.update)
- 分页处理 (LIMIT/OFFSET、逻辑分页)
- 多表连接查询

### 4. 附件处理
- 附件函数 (AttachmentsUtils.*)
- 文件导出 (Excel、Word、PDF、zip)
- 多 CI 附件转 PDF
- PDF 合并
- Word 合并

### 5. 审批流程
- 自定义提交流程 (flow_base_start)
- 自定义通过流程 (flow_pass)
- 自定义加签脚本 (flow_add_object_by_standalone)

### 6. 工具函数
- 日期格式化 (SimpleDateFormat)
- 时间戳生成
- 列表排序 (sortMapList)
- 字符串处理 (removeTrailingZeros)

### 7. 业务特定脚本
- 华龙业务相关
- FOS 数据查询
- 航班数据操作

## 特殊规范

### 变量命名
- 使用中文变量名（如 `def 主表数据`, `def 明细表数据`）
- 遵循平台的字段命名规范

### 数据模型操作
```groovy
// 单条记录
def 数据 = DataModelUtils.getCIByPK("表名",['ID':值])

// 多条记录
def 数据列表 = DataModelUtils.getCIByAttr("表名",['字段名':值])

// 保存
saveCi(数据)

// 删除
DataModelUtils.deleteCi(数据)
DataModelUtils.deleteCis(数据列表)
```

### 表单脚本返回格式
```javascript
if(args$){
    return {
        "validatorFunctions": fieldValidateMap,
        "disabledAttributes": list,
        "changeFunctions": feildMapFunc,
        "setSelectOptionsFunc": optionsFunc
    };
}else{
    return null;
}
```

### 脚本参数说明
- `args$` - 脚本参数变量
- `args$.data` - 表单输入数据
- `args$.getFieldValueFunc` - 获取字段值函数
- `args$.setFieldValueFunc` - 设置字段值函数
- `args$.runScriptFunc` - 调用后台脚本
- `args$.notification` - 打印信息 (error/warning/info/success)

## 重要提示

1. 访问 `args$` 属性前先检查其是否存在
2. 监听脚本使用 `ci$.dataFieldMap` 访问当前数据
3. 附件字段需要使用 JsonSlurper 将大文本转换为 JSON
4. 导出文档时使用正确的模板占位符语法
5. 妥善处理 null 值避免异常

## 完整模板位置

所有完整代码示例存储在 `references/platform-script-templates.txt` 文件中，包含：
- 完整的代码示例
- 详细的注释说明
- 各种场景的最佳实践

当需要编写具体脚本时，会参考此文件中的完整模板生成代码。

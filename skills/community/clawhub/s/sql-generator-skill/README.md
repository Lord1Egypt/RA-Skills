# SQL生成器技能

根据自然语言需求生成SQL SELECT语句。

## 功能说明

本技能可以帮助开发者快速将自然语言需求转换为SQL查询语句。只需提供数据库表结构的HTTP API地址和查询需求描述,即可生成规范的SQL语句。

## 集成到小龙虾

### 安装步骤

1. 将本目录复制到小龙虾的skills目录下
2. 确保小龙虾已配置LLM API密钥
3. 在小龙虾对话中激活本技能

### 使用方式

```
用户: 使用sql-generator技能
用户: apiUrl=https://api.example.com/tables
用户: requirement=查询所有竞拍中的竞拍信息

小龙虾: [调用技能生成SQL]
```

## API格式要求

提供的HTTP API应返回以下JSON格式:

```json
{
  "code": 200,
  "message": "success",
  "data": [
    {
      "tableName": "表名",
      "tableComment": "表注释",
      "columns": [
        {
          "columnName": "字段名",
          "columnType": "字段类型",
          "columnSize": 字段大小,
          "nullable": true,
          "isPrimaryKey": "YES",
          "columnComment": "字段注释"
        }
      ]
    }
  ]
}
```

## 文件结构

```
sql-generator/
├── manifest.json    # clawHub元数据
├── SKILL.md        # 技能描述
├── config.json     # 配置文件
└── README.md      # 使用说明
```

## 注意事项

1. 本技能只生成SELECT查询语句,不会生成修改数据的SQL
2. 生成的SQL包含中文注释,便于理解
3. 支持条件查询、分页、排序、多表关联等

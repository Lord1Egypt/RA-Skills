---
name: xbridge-ext-helper
description: |
  帮助开发者在 xbridge3 框架中使用扩展字段（Extension Fields）。当用户需要：
  - 添加新的扩展字段到交易表
  - 创建国家特定的扩展字段（如越南、马来西亚等）
  - 配置 @EntityColumnSchema 注解
  - 使用 ExtensionUtils 读取/设置扩展字段
  - 理解索引字段（idx_str/idx_date/idx_number）的分配
  - 创建新的扩展Schema配置
  时，使用此skill提供完整的代码示例和步骤指导。
  关键词：xbridge, extension, ext_data, idx_str, idx_number, IndexedExtDataField, VirtualExtDataField, EntityColumnSchema
---

# xbridge3 扩展字段助手

此技能帮助你在 xbridge3 框架中正确使用扩展字段机制。

## 核心概念

### 扩展字段类型

| 角色类型 | 存储位置 | 适用场景 |
|---------|---------|---------|
| `IndexedExtDataField` | JSON + 索引列 | 需要查询条件的字段，映射到 idx_str1-15 / idx_date1-5 / idx_number1-10 |
| `VirtualExtDataField` | 仅 JSON | 不常查询的字段，纯扩展数据 |
| `VirtualExtData` | 整个 extensions 对象 | 容器对象 |

### 索引字段配额

- **idx_str1 ~ idx_str15**: 15个字符串索引（VARCHAR 100）
- **idx_date1 ~ idx_date5**: 5个日期索引（DATETIME）
- **idx_number1 ~ idx_number10**: 10个数值索引（DECIMAL 35,13）

## 使用场景

### 场景1：为新国家添加扩展字段

**步骤概览：**
1. 在 API 模块创建 CommonExtension 类（定义字段）
2. 在 Service 模块创建 ExtensionSchema 类（带 @EntityExtensionSchema 注解）
3. 实现 EntityTableSchemaConfigProvider 接口注册 Schema
4. 在 DAO 层处理扩展字段的保存和读取

**示例：创建 XX 国家扩展字段**

```java
// ===== 步骤1: API 模块 - 定义扩展字段 =====
// document-engine-api/.../adaptor/xx/XXCommonExtension.java

@Setter
@Getter
public class XXCommonExtension {
    
    // ExtensionObjectSpec 用于类型转换
    public static final ExtensionObjectSpec<XXCommonExtension> KEY = 
        ExtensionObjectSpec.<XXCommonExtension>builder()
            .name("xx")
            .type(XXCommonExtension.class)
            .defaultValueSupplier(XXCommonExtension::new)
            .build();

    // 带索引的字段（需要查询）
    @EntityColumnSchema(
        title = "Invoice Type",
        columnName = "idx_str1",           // 映射到索引字段
        length = 6,
        columnRole = ColumnRoleType.IndexedExtDataField,
        listShowQuery = true
    )
    private String invoiceType;

    @EntityColumnSchema(
        title = "Discount Amount",
        columnName = "idx_number1",
        length = 20,
        scale = 6,
        columnRole = ColumnRoleType.IndexedExtDataField
    )
    private BigDecimal discountAmount;

    // 仅 JSON 存储的字段
    @EntityColumnSchema(
        title = "Payment Method",
        columnRole = ColumnRoleType.VirtualExtDataField
    )
    private String paymentMethodCode;

    // 复杂类型（JSON 数组）
    @EntityColumnSchema(
        title = "Item Codes",
        columnRole = ColumnRoleType.VirtualExtDataField,
        type = ColumnStandardType.EXT_JSON
    )
    private List<String> itemCodes;
}
```

```java
// ===== 步骤2: Service 模块 - 创建 Schema 类 =====
// document-engine-service/.../adaptor/xx/XXTransactionExtension.java

@EntityExtensionSchema(
    tableId = "gbw_transaction",
    extNamespace = "xx"
)
@Data
public class XXTransactionExtension extends XXCommonExtension {
}

@EntityExtensionSchema(
    tableId = "gbw_transaction_line",
    extNamespace = "xx"
)
@Data
public class XXTransactionLineExtension extends XXCommonLineExtension {
}
```

```java
// ===== 步骤3: 注册 Schema 配置 =====
// document-engine-service/.../adaptor/xx/XXTransactionProcessor.java

@Component
@RequiredArgsConstructor
public class XXTransactionProcessor implements 
        TransactionProcessor, 
        EntityTableSchemaConfigProvider {

    @Override
    public EntityTableSchemaConfigItem getSchemaConfig() {
        EntityTableSchemaConfig xxSchema = EntitySchemaAnnotationParser.parseExtension(
            XXTransactionExtension.class,
            XXTransactionLineExtension.class
        );
        return EntityTableSchemaConfigItem.builder()
            .tableSchemaID(EntityTableSchemaID.parse("global.XX"))
            .tableSchemaConfig(xxSchema)
            .build();
    }
    
    // ... 其他处理器方法
}
```

### 场景2：读取扩展字段值

```java
// 使用 ExtensionUtils 工具类
VNCommonExtension vnExt = ExtensionUtils.getExtension(
    "vn",                              // JSON 中的 key
    VNCommonExtension.class,           // 目标类型
    transaction.getExtensions()        // extensions ObjectNode
);

if (vnExt != null) {
    String invoiceType = vnExt.getInvoiceType();
    BigDecimal discount = vnExt.getDiscountAmount();
}
```

### 场景3：设置扩展字段值

```java
// 1. 获取或创建 ObjectNode
ObjectNode extensions = transactionDTO.getExtensions();
if (extensions == null) {
    extensions = JacksonObjectMapper.get().createObjectNode();
}

// 2. 创建扩展对象并设置值
XXCommonExtension xxExt = new XXCommonExtension();
xxExt.setInvoiceType("01/MTT");
xxExt.setDiscountAmount(new BigDecimal("100.00"));
xxExt.setItemCodes(Arrays.asList("ITEM001", "ITEM002"));

// 3. 转换为 JsonNode 并设置
String jsonString = JacksonObjectMapper.get().toJsonString(xxExt);
JsonNode xxNode = JacksonObjectMapper.get().toJsonNode(jsonString);
extensions.set("xx", xxNode);

// 4. 设置回 DTO
transactionDTO.setExtensions(extensions);
```

### 场景4：在 DAO 中保存扩展字段

```java
@Repository
@RequiredArgsConstructor
public class TransactionDAO {
    private final TransactionMapper transactionMapper;
    private final TransactionExtMapper transactionExtMapper;

    public Transaction createTransaction(Transaction transaction) {
        // 1. 插入主表（框架自动处理 IndexedExtDataField 到索引字段的同步）
        EntityTableSchemaID tableSchemaID = transaction.getTableSchemaID();
        EntityObjectManager<Transaction> entityManager = 
            transactionMapper.getEntityObjectManager(tableSchemaID);
        entityManager.insert(transaction);
        
        // 2. 【重要】手动保存扩展表
        TransactionExt transactionExt = new TransactionExt();
        transactionExt.onCreateSetup(transaction);
        transactionExt.setExtData(transaction.getExtensions().toString());
        transactionExtMapper.insert(transactionExt);
        
        return transaction;
    }

    public boolean updateTransaction(Transaction transaction) {
        // 1. 更新主表
        EntityObjectManager<Transaction> entityManager = 
            transactionMapper.getEntityObjectManager(transaction.getTableSchemaID());
        entityManager.updateSelective(transaction, queryWrapper);
        
        // 2. 【重要】手动更新扩展表
        TransactionExt transactionExt = new TransactionExt();
        transactionExt.setTransactionId(transaction.getId());
        transactionExt.setExtData(transaction.getExtensions().toString());
        transactionExtMapper.updateById(transactionExt);
        
        return true;
    }
}
```

### 场景5：在 Service 中加载扩展字段

```java
public TransactionDTO queryTransactionDetail(Long transactionId) {
    // 1. 查询主表
    Transaction transaction = transactionMapper.selectById(transactionId);
    
    // 2. 【重要】手动加载扩展字段
    transaction.loadExtensions();
    
    // 3. 加载明细行及扩展
    transaction.loadLines();
    for (TransactionLine line : transaction.getLines()) {
        line.loadExtensions();
    }
    
    // 4. 转换为 DTO
    return transactionConverter.convertToDTO(transaction);
}
```

## @EntityColumnSchema 注解属性参考

| 属性 | 说明 | 常用值 |
|-----|------|-------|
| `title` | 字段标题（必填） | "Invoice Type" |
| `type` | 字段标准类型 | `ColumnStandardType.STRING`, `DECIMAL`, `EXT_JSON` |
| `columnRole` | **核心属性** - 列角色类型 | `IndexedExtDataField`, `VirtualExtDataField` |
| `columnName` | 索引列名（IndexedExtDataField 用） | "idx_str1", "idx_number2" |
| `length` | 最大长度（字符串）或精度（数值） | 100, 20 |
| `scale` | 小数位数（数值类型） | 6, 4 |
| `listShowQuery` | 列表查询时是否作为查询条件 | true / false |
| `defaultValue` | 默认值 | "" |
| `nullable` | 是否可空 | true / false |

## ColumnStandardType 类型

```java
AUTO           // 自动推断
EXT_JSON       // 扩展JSON字段（用于复杂类型如 List）
ID_LONG        // 长整型ID
INSTANT_TIME   // Instant时间类型
BOOLEAN        // 布尔类型
DECIMAL        // BigDecimal
INTEGER        // 整型
LONG_INT       // 长整型
STRING         // 字符串
ONE_TO_MANY    // 一对多关联
```

## 索引字段分配建议

将最常用的查询条件字段映射到索引：

1. **idx_str1-5**: 发票类型、发票序列号、发票号码等高频查询字段
2. **idx_str6-10**: 业务类型编码、状态码等
3. **idx_str11-15**: 预留字段
4. **idx_number1-5**: 金额类字段（折扣金额、税额等）
5. **idx_number6-10**: 比例类字段（折扣率、税率等）

## 常见错误

### 错误1：忘记手动保存扩展表
框架不会自动处理 `gbw_transaction_ext` 表的插入/更新，必须在 DAO 层手动处理。

### 错误2：索引字段冲突
多个扩展字段映射到同一个 `columnName` 会导致数据覆盖。使用前应检查已有映射。

### 错误3：忘记调用 loadExtensions()
查询后必须手动调用 `transaction.loadExtensions()` 才能获取扩展字段数据。

### 错误4：Converter 层逐个字段转换扩展字段
扩展字段应该直接透传，不要逐个字段转换：
```java
// 正确
target.setExtensions(source.getExtensions());

// 错误 - 不要这样做
VNCommonExtension vnExt = ExtensionUtils.getExtension("vn", ...);
target.setInvoiceType(vnExt.getInvoiceType());
// ... 逐个字段转换
```

## 详细参考文档

如需了解更深入的实现细节，请阅读参考文件：

```
references/xbridge-ext-use.md - 交易表扩展字段使用指南（深入版）
```

该文档包含：
- 完整的数据库表结构设计说明
- xbridge3 框架扩展字段核心机制详解
- @EntityColumnSchema 注解所有属性详解
- 实体类完整配置示例
- 扩展字段增删改查完整流程
- 新国家/场景接入扩展字段的详细步骤

## 项目参考文件

| 文件 | 路径 |
|-----|------|
| ExtensionUtils | `references/ExtensionUtils.java` |
| VNCommonExtension | `references/VNCommonExtension.java` |
| VNTransactionExtension | `references/VNTransactionExtension.java` |
| VNTransactionProcessor | `references/VNTransactionProcessor.java` |
| TransactionDAO | `references/TransactionDAO.java` |
| TransactionConverter | `references/TransactionConverter.java` |

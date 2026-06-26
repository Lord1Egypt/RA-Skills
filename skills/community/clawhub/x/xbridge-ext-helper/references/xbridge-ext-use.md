# 交易表扩展字段使用指南（深入版）

## 背景

本文档基于 `gbw_transaction` 表和 `gbw_transaction_ext` 表的代码实现，深入分析 xbridge3 框架中扩展字段的工作原理，包括 `@EntityColumnSchema` 注解详解、复杂类型配置、以及框架如何自动处理扩展字段的增删改查。

---

## 一、数据库表结构设计

### 1.1 主表与扩展表设计

**主表（gbw_transaction）**: 存储交易核心业务数据 + 索引字段
```sql
CREATE TABLE gbw_transaction (
    id BIGINT PRIMARY KEY,
    -- ... 业务字段
    -- 字符索引字段（idx_str1 - idx_str15）
    idx_str1 VARCHAR(100) COMMENT '字符索引1',
    -- ...
    -- 日期索引字段（idx_date1 - idx_date5）
    idx_date1 DATETIME COMMENT '日期索引1',
    -- ...
    -- 数值索引字段（idx_number1 - idx_number10）
    idx_number1 DECIMAL(35, 13) COMMENT '数值索引1'
    -- ...
);
```

**扩展表（gbw_transaction_ext）**: 存储JSON格式的扩展数据
```sql
CREATE TABLE gbw_transaction_ext (
    transaction_id BIGINT PRIMARY KEY COMMENT '主表ID外键',
    tenant_id BIGINT NOT NULL COMMENT '租户ID',
    transaction_date DATETIME COMMENT '交易日期',
    ext_data JSON COMMENT '扩展数据JSON格式'
);
```

### 1.2 索引字段分配

| 索引字段 | 类型 | 数量 | 适用场景 |
|---------|------|------|---------|
| idx_str1 ~ idx_str15 | VARCHAR(100) | 15个 | 字符串类型扩展字段（如发票类型、发票序列号）|
| idx_date1 ~ idx_date5 | DATETIME | 5个 | 日期类型扩展字段 |
| idx_number1 ~ idx_number10 | DECIMAL(35,13) | 10个 | 数值类型扩展字段（如折扣金额、折扣比例）|

---

## 二、xbridge3 框架扩展字段核心机制

### 2.1 核心组件关系图

```
┌─────────────────────────────────────────────────────────────────┐
│                    EntityTableSchemaManager                      │
│  (管理所有实体表的Schema配置，包括扩展字段的解析和查询)              │
└──────────────────────────┬──────────────────────────────────────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
┌─────────────────┐ ┌──────────────┐ ┌──────────────────┐
│ EntitySchema    │ │ EntitySchema │ │ EntitySchema     │
│ (Transaction)   │ │ (Transaction│ │ (TransactionLine)│
│                 │ │ Ext)         │ │                  │
└────────┬────────┘ └──────────────┘ └────────┬─────────┘
         │                                    │
         │         ┌──────────────────────┐   │
         │         │ Extension Schema     │   │
         │         │ (VN/MY Extension)    │   │
         │         └──────────────────────┘   │
         │                                    │
         ▼                                    ▼
┌─────────────────┐                 ┌──────────────────┐
│ @EntityColumn   │                 │ @EntityColumn    │
│ Schema          │                 │ Schema           │
│ (VirtualExtData)│                 │ (VirtualExtData) │
└─────────────────┘                 └──────────────────┘
```

### 2.2 Schema 配置初始化流程

**全局 Schema 配置**（`DocumentEngineConfiguration.java`）:

```java
@Bean
public EntityTableSchemaManager entityTableSchemaManager(
        EntityTableFactoryManager tableFactoryManager,
        ObjectProvider<EntityTableSchemaConfigProvider> schemaConfigProviders) {
    
    // 1. 解析主实体类（基础Schema）
    EntityTableSchemaConfig globalTableSchema = EntitySchemaAnnotationParser.parseEntity(
        Transaction.class,        // 主表
        TransactionExt.class,     // 扩展表
        TransactionLine.class,    // 明细表
        TransactionLineExt.class, // 明细扩展表
        TransactionLineAddress.class
    );
    
    EntityTableSchemaManager.EntityTableSchemaManagerBuilder schemaManagerBuilder = 
        EntityTableSchemaManager.builder()
            .entityTableFactoryManager(tableFactoryManager)
            .globalSchemaConfig(globalTableSchema);
    
    // 2. 注册各国特定的扩展Schema（通过SPI机制）
    for (EntityTableSchemaConfigProvider configProvider : schemaConfigProviders) {
        EntityTableSchemaConfigItem configItem = configProvider.getSchemaConfig();
        schemaManagerBuilder.entityTableSchemaConfig(
            configItem.getTableSchemaID(), 
            configItem.getTableSchemaConfig()
        );
    }
    
    return schemaManagerBuilder.build();
}
```

**国家特定 Schema 配置**（`VNTransactionProcessor.java`）:

```java
@Component
public class VNTransactionProcessor implements 
        TransactionProcessor, 
        EntityTableSchemaConfigProvider {  // 实现Schema配置提供者接口

    @Override
    public EntityTableSchemaConfigItem getSchemaConfig() {
        // 解析越南扩展字段类
        EntityTableSchemaConfig vnTransactionSchema = EntitySchemaAnnotationParser.parseExtension(
            VNTransactionExtension.class,      // 主表扩展
            VNTransactionLineExtension.class   // 明细表扩展
        );
        
        return EntityTableSchemaConfigItem.builder()
            .tableSchemaID(EntityTableSchemaID.parse("global.VN"))  // Schema标识
            .tableSchemaConfig(vnTransactionSchema)
            .build();
    }
}
```

### 2.3 扩展类定义规范

**VNTransactionExtension.java**:
```java
@EntityExtensionSchema(
    tableId = "gbw_transaction",    // 关联的主表
    extNamespace = "vn"              // JSON中的命名空间前缀
)
@Data
public class VNTransactionExtension extends VNCommonExtension {
    // 可以在此添加交易表特定的扩展字段
}
```

**VNTransactionLineExtension.java**:
```java
@EntityExtensionSchema(
    tableId = "gbw_transaction_line",  // 关联的明细表
    extNamespace = "vn"
)
@Data
public class VNTransactionLineExtension extends VNCommonLineExtension {
}
```

---

## 三、@EntityColumnSchema 注解详解

### 3.1 注解属性全解析

```java
@Target({ElementType.FIELD})
@Retention(RetentionPolicy.RUNTIME)
public @interface EntityColumnSchema {
    String title();                    // 字段标题（必填）- 用于元数据展示
    
    ColumnStandardType type() default ColumnStandardType.AUTO;  // 字段标准类型
    
    String dictCode() default "";      // 字典代码 - 用于下拉选项
    
    String defaultValue() default "";  // 默认值
    
    boolean nullable() default true;   // 是否可空
    
    int length() default -1;           // 最大长度（字符串类型）
    
    int scale() default -1;            // 小数位数（数值类型）
    
    ColumnRoleType columnRole() default ColumnRoleType.Physical; // 列角色类型（核心）
    
    String targetTable() default "";   // 目标表名（用于关联）
    
    String targetForeignKeyColumn() default "";  // 目标表外键列
    
    String sourceReferencedColumn() default "";  // 当前表引用列
    
    String extDataColumn() default ""; // 扩展数据JSON列名
    
    String columnName() default "";    // 索引列名（用于IndexedExtDataField映射）
    
    boolean listShowQuery() default false;       // 列表查询时是否作为查询条件
    
    ColumnQueryMode listQueryMode() default ColumnQueryMode.SINGLE; // 查询模式
}
```

### 3.2 ColumnStandardType 支持的类型

```java
public enum ColumnStandardType {
    AUTO,           // 自动推断（根据Java类型自动判断）
    EXT_JSON,       // 扩展JSON字段（用于extensions ObjectNode）
    ID_LONG,        // 长整型ID（主键）
    INSTANT_TIME,   // Instant时间类型
    BOOLEAN,        // 布尔类型
    DECIMAL,        // 大数字（BigDecimal）
    INTEGER,        // 整型
    LONG_INT,       // 长整型
    STRING,         // 字符串
    ONE_TO_MANY,    // 一对多关联（用于lines等关联字段）
}
```

**类型自动推断规则**:
```java
public static ColumnStandardType fromJavaType(Class<?> type) {
    if (ObjectNode.class.isAssignableFrom(type)) return EXT_JSON;
    if (Instant.class.isAssignableFrom(type)) return INSTANT_TIME;
    if (Boolean.class.isAssignableFrom(type) || boolean.class.equals(type)) return BOOLEAN;
    if (BigDecimal.class.isAssignableFrom(type)) return DECIMAL;
    if (Integer.class.isAssignableFrom(type) || int.class.equals(type)) return INTEGER;
    if (Long.class.isAssignableFrom(type) || long.class.equals(type)) return LONG_INT;
    if (String.class.isAssignableFrom(type)) return STRING;
    return AUTO;
}
```

### 3.3 ColumnRoleType 列角色类型详解

```java
public enum ColumnRoleType {
    Physical(false),              // 物理字段 - 数据库实际存在的列（如transaction_uuid）
    ExtDataIndex(false),          // 扩展字段索引列 - 如 idx_str1, idx_date1 等
    ExtData(false),               // 扩展字段数据列 - ext_data JSON列
    VirtualExtData(true),         // 虚拟扩展字段 - 代表整个extensions ObjectNode
    VirtualExtDataField(true),    // 虚拟扩展字段值 - 仅存储在JSON中，不映射索引
    IndexedExtDataField(false);   // 带索引的扩展字段 - 同时存储在JSON和索引列

    private final boolean virtualColumn;  // 是否为虚拟列（不实际存储）
}
```

**角色类型对比表**:

| 角色类型 | 是否虚拟列 | 存储位置 | 查询方式 | 用途 |
|---------|-----------|---------|---------|------|
| Physical | 否 | 主表物理列 | 直接字段查询 | 普通业务字段 |
| ExtDataIndex | 否 | 主表索引列 | 直接字段查询 | 扩展字段的索引列 |
| ExtData | 否 | 扩展表ext_data | JSON路径查询 | JSON存储 |
| VirtualExtData | 是 | 内存/JSON | JSON路径查询 | 代表整个extensions对象 |
| VirtualExtDataField | 是 | JSON | JSON路径查询 | 仅JSON存储的字段（不常查询） |
| IndexedExtDataField | 否 | JSON + 索引列 | 索引字段查询 | 需要索引的扩展字段 |

---

## 四、实体类完整配置示例

### 4.1 主表实体类（Transaction.java）

```java
@Data
@EqualsAndHashCode(callSuper = false)
@TableName(value = "gbw_transaction")
@EntityTableSchema(title = "Transaction")
public class Transaction extends ExtensiableSchemaEntityObject implements ChangeAuditableObject {

    // ========== 1. 主表业务字段（Physical） ==========
    @TableId(value = "id")
    @EntityColumnSchema(title = "{gbw_transaction.id}", type = ColumnStandardType.ID_LONG)
    private Long id;
    
    @TableField(value = "transaction_uuid")
    @EntityColumnSchema(title = "Transaction UUID", length = 50)
    private String transactionUuid;
    
    @TableField(value = "transaction_type")
    @EntityColumnSchema(title = "Transaction Type", length = 10)
    private String transactionType;
    
    // ... 其他业务字段
    
    // ========== 2. 索引字段（ExtDataIndex） ==========
    // 这些字段用于存储需要索引的扩展字段值
    
    @TableField(value = "idx_str1")
    @EntityColumnSchema(title = "Index String 1", length = 100, columnRole = ColumnRoleType.ExtDataIndex)
    private String idxStr1;
    
    @TableField(value = "idx_str2")
    @EntityColumnSchema(title = "Index String 2", length = 100, columnRole = ColumnRoleType.ExtDataIndex)
    private String idxStr2;
    
    @TableField(value = "idx_number1")
    @EntityColumnSchema(title = "Index Number 1", length = 35, scale = 13, columnRole = ColumnRoleType.ExtDataIndex)
    private BigDecimal idxNumber1;
    
    // ... idx_str3-15, idx_date1-5, idx_number2-10
    
    // ========== 3. 扩展字段（VirtualExtData） ==========
    // 这是整个扩展字段的容器，对应 ext_data JSON
    
    @TableField(exist = false)  // 不直接映射数据库列
    @EntityColumnSchema(
        title = "Extensions",
        type = ColumnStandardType.EXT_JSON,
        columnRole = ColumnRoleType.VirtualExtData,      // 虚拟扩展字段
        targetTable = "gbw_transaction_ext",             // 扩展表名
        sourceReferencedColumn = "id",                    // 主表关联列
        targetForeignKeyColumn = "transaction_id",        // 扩展表外键列
        extDataColumn = "ext_data"                        // 扩展数据JSON列
    )
    private ObjectNode extensions;
    
    // ========== 4. 关联字段（ONE_TO_MANY） ==========
    
    @TableField(exist = false)
    @EntityColumnSchema(
        title = "Transaction lines",
        type = ColumnStandardType.ONE_TO_MANY,
        targetTable = "gbw_transaction_line",
        targetForeignKeyColumn = "transaction_id",
        sourceReferencedColumn = "id"
    )
    private List<TransactionLine> lines;
    
    // ========== 5. 扩展字段操作方法 ==========
    
    /**
     * 从数据库加载扩展字段
     */
    public void loadExtensions() {
        TransactionExt transactionExt = TransactionExtMapper.INSTANCE.get().selectById(getId());
        if (transactionExt != null) {
            setExtensions(transactionExt.getExtData());  // String -> ObjectNode
        }
    }
    
    /**
     * 获取指定key的扩展对象（基类方法）
     */
    public <T> T getExtension(String extKey, Class<T> type) {
        if (getExtensions() == null) {
            return null;
        }
        JsonNode value = getExtensions().path(extKey);
        if (!value.isObject()) {
            return null;
        }
        return JacksonObjectMapper.get().toJavaObject(value, type);
    }
}
```

### 4.2 扩展表实体类（TransactionExt.java）

```java
@Data
@TableName(value = "gbw_transaction_ext")
@EntityTableSchema(title = "Transaction Extensions")
public class TransactionExt {

    @TableId(value = "transaction_id")
    @EntityColumnSchema(title = "Transaction ID", type = ColumnStandardType.LONG_INT)
    private Long transactionId;  // 主键同时也是外键

    @TableField(value = "tenant_id")
    @EntityColumnSchema(title = "Tenant ID")
    private Long tenantId;

    @TableField(value = "transaction_date")
    @EntityColumnSchema(title = "Transaction Date")
    private Instant transactionDate;

    @TableField(value = "ext_data")
    @EntityColumnSchema(title = "Extension Data", type = ColumnStandardType.STRING)
    private String extData;  // JSON字符串存储

    public void onCreateSetup(Transaction transaction) {
        setTransactionId(transaction.getId());
        setTenantId(transaction.getTenantId());
        setTransactionDate(transaction.getTransactionDate());
    }
}
```

---

## 五、国家扩展字段定义详解

### 5.1 VNCommonExtension.java（越南扩展字段）

```java
@Setter
@Getter
public class VNCommonExtension {

    // ===== 定义ExtensionObjectSpec（用于类型转换）=====
    public static final ExtensionObjectSpec<VNCommonExtension> KEY = 
        ExtensionObjectSpec.<VNCommonExtension>builder()
            .name("vn")                              // JSON中的key
            .type(VNCommonExtension.class)           // 对应的Java类型
            .defaultValueSupplier(VNCommonExtension::new)
            .build();

    // ========== 1. 带索引的扩展字段（IndexedExtDataField）==========
    // 这些字段会同时存储在 ext_data JSON 和主表的 idx_str/idx_number 字段中
    
    /**
     * 发票类型 - 映射到 idx_str1
     * 常用于列表查询，所以需要索引
     */
    @EntityColumnSchema(
        title = "Invoice Type",
        columnName = "idx_str1",                    // 映射到索引字段
        length = 6,
        columnRole = ColumnRoleType.IndexedExtDataField,
        listShowQuery = true                        // 列表查询条件
    )
    private String invoiceType;

    @EntityColumnSchema(
        title = "Invoice Form Type",
        columnName = "idx_str2",
        length = 1,
        columnRole = ColumnRoleType.IndexedExtDataField
    )
    private String invoiceForm;

    @EntityColumnSchema(
        title = "Invoice Series",
        columnName = "idx_str3",
        length = 8,
        columnRole = ColumnRoleType.IndexedExtDataField,
        listShowQuery = true
    )
    private String invoiceSeries;

    @EntityColumnSchema(
        title = "Invoice No.",
        columnName = "idx_str4",
        length = 20,
        columnRole = ColumnRoleType.IndexedExtDataField,
        listShowQuery = true
    )
    private String invoiceNo;

    // 整单折扣相关字段 - 映射到数值索引
    @EntityColumnSchema(
        title = "Commercial Discount Amount",
        columnName = "idx_number1",                 // 映射到数值索引
        length = 20,
        scale = 6,
        columnRole = ColumnRoleType.IndexedExtDataField
    )
    private BigDecimal commercialDiscount;

    @EntityColumnSchema(
        title = "Commercial Discount Rate",
        columnName = "idx_number2",
        length = 10,
        scale = 4,
        columnRole = ColumnRoleType.IndexedExtDataField
    )
    private BigDecimal commercialDiscountRate;

    // ========== 2. 仅JSON存储的扩展字段（VirtualExtDataField）==========
    // 这些字段只存储在 ext_data JSON 中，不占用索引字段
    
    @EntityColumnSchema(
        title = "Payment Method",
        columnRole = ColumnRoleType.VirtualExtDataField,  // 仅JSON存储
        listShowQuery = true
    )
    private String paymentMethodCode;

    @EntityColumnSchema(
        title = "Invoice Class",
        columnRole = ColumnRoleType.VirtualExtDataField
    )
    private String invoiceClass;

    @EntityColumnSchema(
        title = "Full Buyer Name",
        columnRole = ColumnRoleType.VirtualExtDataField
    )
    private String fullBuyerName;

    // ========== 3. 复杂类型字段（List、嵌套对象）==========
    
    /**
     * 折扣适用的商品代码列表 - 存储为JSON数组
     */
    @EntityColumnSchema(
        title = "Commercial Discount itemCodes",
        columnRole = ColumnRoleType.VirtualExtDataField,
        type = ColumnStandardType.EXT_JSON  // 复杂类型使用EXT_JSON
    )
    private List<String> commercialDiscountItemCodes;
}
```

### 5.2 存储的JSON结构示例

```json
{
    "vn": {
        // 带索引的字段（同时存储在 idx_str1-6, idx_number1-2）
        "invoiceType": "01/MTT",
        "invoiceForm": "1",
        "invoiceSeries": "K26MYY",
        "invoiceNo": "0000123",
        "discountTaxIncluded": "1",
        "commercialDiscountMethod": "0",
        "commercialDiscount": 1000.00,
        "commercialDiscountRate": 0.10,
        
        // 仅JSON存储的字段
        "paymentMethodCode": "TM",
        "invoiceClass": "0",
        "fullBuyerName": "Công ty TNHH ABC",
        
        // 复杂类型字段
        "commercialDiscountItemCodes": ["ITEM001", "ITEM002", "ITEM003"],
        
        // 其他虚拟字段
        "buyerIdType": "1",
        "buyerIdNo": "123456789",
        "adjustReason": "调整原因说明"
    }
}
```

---

## 六、扩展字段增删改查详解

### 6.1 创建交易时保存扩展字段

**关键点**: 当前框架不会自动处理扩展表插入，需要应用层手动处理。

```java
@Repository
@RequiredArgsConstructor
public class TransactionDAO {
    private final TransactionMapper transactionMapper;
    private final TransactionExtMapper transactionExtMapper;
    private final TransactionLineMapper transactionLineMapper;
    private final TransactionLineExtMapper transactionLineExtMapper;

    public Transaction createTransaction(Transaction transaction) {
        // 1. 获取EntityObjectManager（带Schema支持）
        EntityTableSchemaID tableSchemaID = transaction.getTableSchemaID();
        EntityObjectManager<Transaction> transactionEntityManager = 
            transactionMapper.getEntityObjectManager(tableSchemaID);
        
        // 2. 插入主表数据
        // 注意：这里只插入主表，不会自动处理扩展表
        transactionEntityManager.insert(transaction);
        
        // 3. 插入明细行数据
        if (!CollectionUtils.isEmpty(transaction.getLines())) {
            transaction.getLines().forEach(line -> line.onCreateSetup(transaction));
            transactionLineEntityManager.insertMultiple(transaction.getLines());
            
            // 4. 插入明细行扩展字段
            for (TransactionLine line : transaction.getLines()) {
                insertTransactionLineExt(line);
            }
        }
        
        // 5. 【重要】手动保存扩展字段到扩展表
        TransactionExt transactionExt = new TransactionExt();
        transactionExt.onCreateSetup(transaction);
        // ObjectNode -> JSON字符串
        transactionExt.setExtData(transaction.getExtensions().toString());
        transactionExtMapper.insert(transactionExt);
        
        return transaction;
    }
    
    private void insertTransactionLineExt(TransactionLine line) {
        TransactionLineExt lineExt = new TransactionLineExt();
        lineExt.onCreateSetup(line);
        ObjectNode extensions = line.getExtensions();
        if (extensions == null) {
            extensions = JacksonObjectMapper.get().createObjectNode();
        }
        lineExt.setExtData(extensions.toString());
        transactionLineExtMapper.insert(lineExt);
    }
}
```

### 6.2 更新交易时更新扩展字段

```java
public boolean updateTransaction(Transaction transaction, Collection<TransactionStatus> expectedStatus) {
    EntityTableSchemaID tableSchemaID = transaction.getTableSchemaID();
    EntityObjectManager<Transaction> transactionEntityManager = 
        transactionMapper.getEntityObjectManager(tableSchemaID);
    
    // 1. 构建查询条件（乐观锁）
    EntityQueryWrapper queryWrapper = EntityQueryWrapper.columnNameQuery(
        transactionEntityManager.getEntityTable()
    );
    queryWrapper.eq("id", transaction.getId());
    if (!expectedStatus.isEmpty()) {
        queryWrapper.in("transaction_status", 
            expectedStatus.stream().map(TransactionStatus::getStatus).toList()
        );
    }
    
    // 2. 更新主表数据
    int updated = transactionEntityManager.updateSelective(transaction, queryWrapper);
    if (updated <= 0) {
        return false;
    }
    
    // 3. 【重要】手动更新扩展字段
    TransactionExt transactionExt = new TransactionExt();
    transactionExt.setTransactionId(transaction.getId());
    transactionExt.setExtData(transaction.getExtensions().toString());
    transactionExtMapper.updateById(transactionExt);
    
    // 4. 更新明细行及扩展字段
    List<TransactionLine> existsLines = transactionLineMapper.selectList(
        Wrappers.lambdaQuery(TransactionLine.class)
            .eq(TransactionLine::getTransactionId, transaction.getId())
    );
    Map<Long, TransactionLine> toRemoveLinesMap = existsLines.stream()
        .collect(Collectors.toMap(TransactionLine::getId, Function.identity()));
    
    if (!CollectionUtils.isEmpty(transaction.getLines())) {
        for (TransactionLine line : transaction.getLines()) {
            TransactionLine existsLine = toRemoveLinesMap.remove(line.getId());
            if (existsLine != null) {
                // 更新现有明细行
                line.onUpdateSetup(transaction);
                transactionLineEntityManager.updateByIdSelective(line);
                
                // 更新明细行扩展字段
                TransactionLineExt lineExt = new TransactionLineExt();
                lineExt.setLineId(line.getId());
                lineExt.setExtData(line.getExtensions().toString());
                transactionLineExtMapper.updateById(lineExt);
            } else {
                // 新增明细行
                line.onCreateSetup(transaction);
                transactionLineEntityManager.insertSelective(line);
                insertTransactionLineExt(line);
            }
        }
        
        // 删除被移除的明细行
        List<Long> toRemoveLineIdList = toRemoveLinesMap.values().stream()
            .map(TransactionLine::getId)
            .toList();
        transactionLineMapper.deleteByIds(toRemoveLineIdList);
        transactionLineExtMapper.deleteByIds(toRemoveLineIdList);
    }
    
    return true;
}
```

### 6.3 查询时加载扩展字段

```java
@Service
public class TransactionServiceImpl implements TransactionService {
    
    public TransactionDTO queryTransactionDetail(Long transactionId) {
        // 1. 查询主表数据
        Transaction transaction = transactionMapper.selectById(transactionId);
        if (transaction == null) {
            throw new BusinessException("交易不存在");
        }
        
        // 2. 【重要】手动加载扩展字段
        transaction.loadExtensions();
        
        // 3. 加载明细行
        transaction.loadLines();
        
        // 4. 加载明细行扩展字段
        for (TransactionLine line : transaction.getLines()) {
            line.loadExtensions();
        }
        
        // 5. 转换为DTO
        return transactionConverter.convertToDTO(transaction);
    }
}
```

**Transaction.loadExtensions() 实现**:
```java
public void loadExtensions() {
    TransactionExt transactionExt = TransactionExtMapper.INSTANCE.get().selectById(getId());
    if (transactionExt != null && transactionExt.getExtData() != null) {
        // String -> ObjectNode 转换
        setExtensions(transactionExt.getExtData());
    }
}
```

**ExtensiableSchemaEntityObject.setExtensions(String) 基类实现**:
```java
public void setExtensions(String extensions) {
    JsonNode jsonNode = JacksonObjectMapper.get().toJsonNode(extensions);
    if (jsonNode instanceof ObjectNode objectNode) {
        setExtensions(objectNode);
    }
}
```

---

## 七、Converter层实现

### 7.1 TransactionConverter.java

```java
@Component
public class TransactionConverter {

    /**
     * DTO -> Entity
     */
    public Transaction convertToEntity(TransactionDTO source) {
        Transaction target = new Transaction();
        
        // 1. 基础字段映射
        target.setId(source.getId());
        target.setTransactionUuid(source.getTransactionUuid());
        target.setTransactionType(
            Optional.ofNullable(source.getTransactionType())
                .map(TransactionType::getCode)
                .orElse(null)
        );
        // ... 其他字段映射
        
        // 2. 【重要】扩展字段直接透传
        // extensions ObjectNode 直接复制，无需逐个字段转换
        target.setExtensions(source.getExtensions());
        
        // 3. 转换明细行
        List<TransactionLine> lines = convertLinesToEntities(source.getLines());
        target.setLines(lines);
        
        return target;
    }

    /**
     * Entity -> DTO
     */
    public TransactionDTO convertToDTO(Transaction source) {
        TransactionDTO target = new TransactionDTO();
        
        // 1. 基础字段映射
        target.setId(source.getId());
        target.setTransactionUuid(source.getTransactionUuid());
        target.setTransactionType(
            Optional.ofNullable(source.getTransactionType())
                .map(TransactionType::fromCode)
                .orElse(null)
        );
        // ... 其他字段映射
        
        // 2. 【重要】扩展字段直接透传
        target.setExtensions(source.getExtensions());
        
        // 3. 转换明细行
        List<TransactionLineDTO> lineDTOS = convertLinesToDTOs(source.getLines());
        target.setLines(lineDTOS);
        
        return target;
    }
    
    private TransactionLine convertLineToEntity(TransactionLineDTO source) {
        TransactionLine target = new TransactionLine();
        // ... 基础字段映射
        
        // 扩展字段直接透传
        target.setExtensions(source.getExtensions());
        
        return target;
    }
    
    private TransactionLineDTO convertLineToDTO(TransactionLine source) {
        TransactionLineDTO target = new TransactionLineDTO();
        // ... 基础字段映射
        
        // 扩展字段直接透传
        target.setExtensions(source.getExtensions());
        
        return target;
    }
}
```

---

## 八、扩展字段工具类使用

### 8.1 ExtensionUtils.java

```java
public class ExtensionUtils {
    
    /**
     * 从extensions ObjectNode中获取指定key的扩展对象
     * 
     * @param key 扩展字段key（如 "vn", "my"）
     * @param type 目标类型Class
     * @param extensions extensions ObjectNode
     * @return 转换后的对象，如果不存在返回null
     */
    public static <T> T getExtension(String key, Class<T> type, ObjectNode extensions) {
        if (extensions == null) {
            return null;
        }
        JsonNode value = extensions.path(key);
        if (!value.isObject()) {
            return null;
        }
        return JacksonObjectMapper.get().toJavaObject(value, type);
    }
}
```

### 8.2 使用示例

**读取扩展字段**:
```java
// 在Validator中使用
@Component
public class VNTransactionValidator implements TransactionValidator {
    
    @Override
    public void validateBeforeProcess(TransactionValidateContext context) {
        Transaction transaction = context.getTransaction();
        
        // 获取越南扩展字段
        VNCommonExtension vnExtension = ExtensionUtils.getExtension(
            "vn", 
            VNCommonExtension.class,
            transaction.getExtensions()
        );
        
        if (vnExtension != null) {
            // 校验发票类型
            if (StringUtils.isBlank(vnExtension.getInvoiceType())) {
                context.reject(ErrorCodes.TA0017, "invoiceType");
            }
            
            // 校验折扣参数
            validateDiscountParameters(context, transaction, vnExtension);
        }
    }
}
```

**设置扩展字段**:
```java
// 在Processor中使用
@Component
public class VNScanInvoiceProcessor implements ScanInvoiceProcessor {
    
    @Override
    public void preProcess(TransactionDTO transactionDTO) {
        ObjectNode extensions = transactionDTO.getExtensions();
        if (extensions == null) {
            extensions = JacksonObjectMapper.get().createObjectNode();
        }
        
        // 获取或创建越南扩展对象
        VNCommonExtension vnExtension = ExtensionUtils.getExtension(
            "vn", VNCommonExtension.class, extensions
        );
        if (vnExtension == null) {
            vnExtension = new VNCommonExtension();
        }
        
        // 设置扩展字段值
        vnExtension.setInvoiceType("01/MTT");
        vnExtension.setInvoiceForm("1");
        vnExtension.setPaymentMethodCode("TM");
        
        // 保存回extensions
        String jsonString = JacksonObjectMapper.get().toJsonString(vnExtension);
        JsonNode vnNode = JacksonObjectMapper.get().toJsonNode(jsonString);
        extensions.set("vn", vnNode);
        
        transactionDTO.setExtensions(extensions);
    }
}
```

---

## 九、框架自动支持的功能

### 9.1 索引字段自动同步

**xbridge3 框架自动支持以下功能**：

1. **插入/更新时自动同步**: `EntityObjectManager.insert()` / `update()` 会自动提取 `IndexedExtDataField` 并设置到对应的索引字段（idx_str1, idx_number1等）

2. **查询时自动转换**: `EntityTableSchemaManager` 在构建查询条件时，会将 `VirtualExtDataField` 的查询转换为索引字段查询或JSON路径查询

3. **asEntityDataObject 转换**: 该方法会自动处理扩展字段到索引字段的映射逻辑

4. **扩展字段自动校验**: 框架支持基于 `@EntityColumnSchema` 注解的自动校验（如长度、非空等）

**示例：框架自动同步索引字段**
```java
// 当设置 extensions 中的 vn.invoiceType 时
ObjectNode extensions = JacksonObjectMapper.get().createObjectNode();
VNCommonExtension vnExt = new VNCommonExtension();
vnExt.setInvoiceType("01/MTT");  // 标记为 IndexedExtDataField，映射到 idx_str1
extensions.set("vn", JacksonObjectMapper.get().valueToTree(vnExt));
transaction.setExtensions(extensions);

// 调用框架方法时，自动同步到索引字段
transactionEntityManager.insert(transaction);
// 结果：transaction.idxStr1 = "01/MTT"，同时 ext_data 中存储完整JSON
```

---

## 十、新国家/场景接入扩展字段完整步骤

### 10.1 步骤清单

#### 步骤1：创建国家扩展类（API模块）

**文件**: `document-engine-api/src/main/java/com/baiwang/global/transaction/adaptor/xx/XXCommonExtension.java`

```java
@Setter
@Getter
public class XXCommonExtension {
    
    // 定义ExtensionObjectSpec（用于类型转换）
    public static final ExtensionObjectSpec<XXCommonExtension> KEY = 
        ExtensionObjectSpec.<XXCommonExtension>builder()
            .name("xx")                              // JSON中的key
            .type(XXCommonExtension.class)           // 对应的Java类型
            .defaultValueSupplier(XXCommonExtension::new)
            .build();

    // ===== 带索引的扩展字段（常用查询条件）=====
    @EntityColumnSchema(
        title = "XX Specific Field",
        columnName = "idx_str1",                    // 映射到索引字段
        length = 50,
        columnRole = ColumnRoleType.IndexedExtDataField,
        listShowQuery = true
    )
    private String xxSpecificField;

    @EntityColumnSchema(
        title = "XX Amount",
        columnName = "idx_number1",
        length = 20,
        scale = 2,
        columnRole = ColumnRoleType.IndexedExtDataField
    )
    private BigDecimal xxAmount;

    // ===== 仅JSON存储的扩展字段 =====
    @EntityColumnSchema(
        title = "XX Description",
        columnRole = ColumnRoleType.VirtualExtDataField
    )
    private String xxDescription;
    
    // ===== 复杂类型字段 =====
    @EntityColumnSchema(
        title = "XX Item Codes",
        columnRole = ColumnRoleType.VirtualExtDataField,
        type = ColumnStandardType.EXT_JSON
    )
    private List<String> xxItemCodes;
}
```

#### 步骤2：创建扩展Schema类（Service模块）

**文件**: `document-engine-service/src/main/java/com/baiwang/global/document/adaptor/xx/XXTransactionExtension.java`

```java
@EntityExtensionSchema(
    tableId = "gbw_transaction",
    extNamespace = "xx"
)
@Data
public class XXTransactionExtension extends XXCommonExtension {
}
```

**文件**: `document-engine-service/src/main/java/com/baiwang/global/document/adaptor/xx/XXTransactionLineExtension.java`

```java
@EntityExtensionSchema(
    tableId = "gbw_transaction_line",
    extNamespace = "xx"
)
@Data
public class XXTransactionLineExtension extends XXCommonLineExtension {
}
```

#### 步骤3：实现Schema配置提供者

**文件**: `document-engine-service/src/main/java/com/baiwang/global/document/adaptor/xx/XXTransactionProcessor.java`

```java
@Component
@RequiredArgsConstructor
public class XXTransactionProcessor implements 
        TransactionProcessor, 
        EntityTableSchemaConfigProvider {

    static final Set<TransactionBusinessRoute> ROUTES = Sets.newHashSet(
        TransactionBusinessRoute.builder()
            .countryCode(CountryCode.XX)
            .transactionType(TransactionType.SalesInvoice)
            .build()
    );

    @Override
    public boolean supports(TransactionBusinessRoute route) {
        return ROUTES.contains(route);
    }

    @Override
    public EntityTableSchemaConfigItem getSchemaConfig() {
        EntityTableSchemaConfig xxTransactionSchema = EntitySchemaAnnotationParser.parseExtension(
            XXTransactionExtension.class,
            XXTransactionLineExtension.class
        );
        return EntityTableSchemaConfigItem.builder()
            .tableSchemaID(EntityTableSchemaID.parse("global.XX"))
            .tableSchemaConfig(xxTransactionSchema)
            .build();
    }

    @Override
    public void beforeCreateTransaction(TransactionCreateContext context) {
        Transaction transaction = context.getTransaction();
        // 处理XX国家特定的逻辑
    }
}
```

#### 步骤4：扩展字段使用

**设置扩展字段**:
```java
// 创建ObjectNode
ObjectNode extensions = JacksonObjectMapper.get().createObjectNode();

// 创建XX扩展对象
XXCommonExtension xxExtension = new XXCommonExtension();
xxExtension.setXxSpecificField("value");
xxExtension.setXxAmount(new BigDecimal("100.00"));
xxExtension.setXxItemCodes(Arrays.asList("ITEM001", "ITEM002"));

// 转换为JsonNode并设置
String jsonString = JacksonObjectMapper.get().toJsonString(xxExtension);
JsonNode xxNode = JacksonObjectMapper.get().toJsonNode(jsonString);
extensions.set("xx", xxNode);

// 设置到DTO
transactionDTO.setExtensions(extensions);
```

**读取扩展字段**:
```java
// 从Entity读取
XXCommonExtension xxExtension = ExtensionUtils.getExtension(
    "xx", 
    XXCommonExtension.class, 
    transaction.getExtensions()
);

if (xxExtension != null) {
    String specificField = xxExtension.getXxSpecificField();
    BigDecimal amount = xxExtension.getXxAmount();
    List<String> itemCodes = xxExtension.getXxItemCodes();
}
```

### 10.2 注意事项

1. **索引字段数量有限**: 
   - idx_str: 15个
   - idx_date: 5个
   - idx_number: 10个
   合理规划，仅将常用作查询条件的字段映射到索引

2. **JSON大小限制**: ext_data 存储在MySQL JSON字段中，单个扩展对象不宜过大（建议不超过1MB）

3. **版本兼容性**: 扩展字段的修改要考虑历史数据的兼容性，建议：
   - 新增字段设置默认值
   - 避免删除已使用的字段
   - 字段重命名时保持向后兼容

4. **索引字段同步**: 框架会自动同步 `IndexedExtDataField` 到索引字段，无需应用层手动处理

---

## 十一、关键文件清单

| 文件 | 路径 | 说明 |
|-----|------|------|
| Transaction.java | `document-engine-service/.../dao/entity/Transaction.java` | 主表实体类 |
| TransactionExt.java | `document-engine-service/.../dao/entity/TransactionExt.java` | 扩展表实体类 |
| TransactionLine.java | `document-engine-service/.../dao/entity/TransactionLine.java` | 明细行实体类 |
| TransactionLineExt.java | `document-engine-service/.../dao/entity/TransactionLineExt.java` | 明细行扩展表实体类 |
| TransactionDTO.java | `document-engine-api/.../model/dto/TransactionDTO.java` | DTO定义 |
| TransactionDAO.java | `document-engine-service/.../dao/TransactionDAO.java` | DAO实现 |
| TransactionConverter.java | `document-engine-service/.../converter/TransactionConverter.java` | 转换器 |
| ExtensionUtils.java | `document-engine-api/.../utils/ExtensionUtils.java` | 扩展字段工具类 |
| VNCommonExtension.java | `document-engine-api/.../adaptor/vn/VNCommonExtension.java` | 越南扩展字段定义 |
| VNTransactionExtension.java | `document-engine-service/.../adaptor/vn/VNTransactionExtension.java` | 越南扩展Schema |
| VNTransactionProcessor.java | `document-engine-service/.../adaptor/vn/VNTransactionProcessor.java` | 越南处理器+Schema提供者 |
| DocumentEngineConfiguration.java | `document-engine-service/.../config/DocumentEngineConfiguration.java` | Schema管理器配置 |

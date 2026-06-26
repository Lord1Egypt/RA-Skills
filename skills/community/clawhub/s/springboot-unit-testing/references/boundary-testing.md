# Spring Boot边界值测试指南

## 边界值测试核心概念

### 什么是边界值？
边界值是输入域、输出域或状态域的边缘值，这些值附近通常最容易出现错误。

### 边界值类型
1. **输入边界** - 参数的取值范围边界
2. **输出边界** - 返回值的取值范围边界  
3. **状态边界** - 系统状态的转换边界
4. **容量边界** - 系统容量的极限边界
5. **时间边界** - 时间相关的边界条件

## 边界值测试策略

### 三值边界测试法
对于每个边界，测试三个值：
- **边界值本身**
- **刚好小于边界值** (边界值-1)
- **刚好大于边界值** (边界值+1)

### 七值边界测试法（推荐）
对于有范围的参数，测试七个值：
1. **最小值** (min)
2. **最小值+1** (min+1)  
3. **正常值** (nominal)
4. **最大值-1** (max-1)
5. **最大值** (max)
6. **小于最小值** (min-1)
7. **大于最大值** (max+1)

## 数值边界测试

### 整数边界测试
```java
public class IntegerBoundaryTest {
    
    @ParameterizedTest
    @ValueSource(ints = {
        Integer.MIN_VALUE,      // 最小边界
        Integer.MIN_VALUE + 1,  // 最小边界+1
        -1,                     // 负边界
        0,                      // 零边界
        1,                      // 正边界
        Integer.MAX_VALUE - 1,  // 最大边界-1
        Integer.MAX_VALUE       // 最大边界
    })
    void testIntegerBoundaryValues(int value) {
        // 测试整数边界值
        assertDoesNotThrow(() -> service.processInteger(value));
    }
    
    @Test
    void testIntegerOverflow() {
        // 测试整数溢出
        int maxValue = Integer.MAX_VALUE;
        assertThrows(ArithmeticException.class,
            () -> service.add(maxValue, 1));
    }
    
    @Test
    void testIntegerUnderflow() {
        // 测试整数下溢
        int minValue = Integer.MIN_VALUE;
        assertThrows(ArithmeticException.class,
            () -> service.subtract(minValue, 1));
    }
}
```

### 浮点数边界测试
```java
public class FloatBoundaryTest {
    
    @ParameterizedTest
    @ValueSource(doubles = {
        Double.NEGATIVE_INFINITY,  // 负无穷
        -Double.MAX_VALUE,         // 最小负值
        -Double.MIN_VALUE,         // 最小负非零值
        -0.0,                      // 负零
        0.0,                       // 零
        Double.MIN_VALUE,          // 最小正非零值
        Double.MAX_VALUE,          // 最大正值
        Double.POSITIVE_INFINITY,  // 正无穷
        Double.NaN                 // 非数字
    })
    void testFloatBoundaryValues(double value) {
        // 测试浮点数边界值
        assertDoesNotThrow(() -> service.processDouble(value));
    }
    
    @Test
    void testFloatingPointPrecision() {
        // 测试浮点数精度问题
        double result = 0.1 + 0.2;
        assertThat(result).isNotEqualTo(0.3); // 浮点数精度问题
        assertThat(result).isCloseTo(0.3, within(0.0000001));
    }
    
    @Test
    void testDivisionByZero() {
        // 测试除以零
        assertThrows(ArithmeticException.class,
            () -> service.divide(1.0, 0.0));
        
        // 测试除以负零
        assertThrows(ArithmeticException.class,
            () -> service.divide(1.0, -0.0));
    }
}
```

## 字符串边界测试

### 长度边界测试
```java
public class StringLengthBoundaryTest {
    
    // 测试各种长度的字符串
    @ParameterizedTest
    @ValueSource(strings = {
        "",                      // 空字符串
        "a",                     // 单字符
        "ab",                    // 双字符
        "abc",                   // 三字符
        "a".repeat(255),         // 最大长度（假设255）
        "a".repeat(256),         // 超过最大长度
        "a".repeat(1000),        // 远超过最大长度
        "test\0null",            // 包含空字符
        "test\\escape",          // 转义字符
        "🎉emoji",               // Emoji字符（多字节）
        "测试中文",              // 中文字符
        "a".repeat(1024 * 1024)  // 1MB大字符串
    })
    void testStringLengthBoundaries(String input) {
        // 测试字符串长度边界
        if (input.length() > 255) {
            assertThrows(ValidationException.class,
                () -> service.validateString(input));
        } else {
            assertDoesNotThrow(() -> service.validateString(input));
        }
    }
    
    @Test
    void testEmptyAndBlankStrings() {
        // 测试空字符串和空白字符串
        assertThrows(IllegalArgumentException.class,
            () -> service.processString(""));
        
        assertThrows(IllegalArgumentException.class,
            () -> service.processString("   "));
        
        assertThrows(IllegalArgumentException.class,
            () -> service.processString("\t\n\r"));
        
        // 包含不可见字符
        assertThrows(IllegalArgumentException.class,
            () -> service.processString("test\u0000"));
    }
    
    @Test
    void testUnicodeBoundaries() {
        // 测试Unicode边界
        String[] unicodeTests = {
            "\u0000",                    // 最小Unicode
            "\u0020",                    // 空格
            "\u007F",                    // DELETE
            "\u0080",                    // 扩展ASCII开始
            "\u00FF",                    // 拉丁文补充
            "\u0100",                    // 拉丁文扩展
            "\u07FF",                    // 西里尔文等
            "\u0800",                    // 梵文等
            "\uFFFF",                    // 基本多文种平面结束
            "\uD800\uDC00",              // 代理对开始
            "\uDBFF\uDFFF",              // 代理对结束
            "🎉",                        // Emoji
            "𝄞",                         // 音乐符号
            "\uFFFD"                     // 替换字符
        };
        
        for (String unicode : unicodeTests) {
            assertDoesNotThrow(() -> service.processUnicode(unicode));
        }
    }
}
```

### 内容边界测试
```java
public class StringContentBoundaryTest {
    
    @Test
    void testSpecialCharacters() {
        // 测试特殊字符
        String[] specialChars = {
            "test's",                    // 单引号
            "test\"s",                   // 双引号
            "test`s",                    // 反引号
            "test\\s",                   // 反斜杠
            "test/s",                    // 斜杠
            "test|s",                    // 竖线
            "test&s",                    // 与符号
            "test%s",                    // 百分号
            "test@s",                    // @符号
            "test#s",                    // 井号
            "test$s",                    // 美元符号
            "test*s",                    // 星号
            "test(s)",                   // 括号
            "test[s]",                   // 方括号
            "test{s}",                   // 花括号
            "test<s>",                   // 尖括号
            "test;s",                    // 分号
            "test:s",                    // 冒号
            "test,s",                    // 逗号
            "test.s",                    // 点号
            "test?s",                    // 问号
            "test!s",                    // 感叹号
            "test~s",                    // 波浪号
            "test^s",                    // 插入符
            "test`s",                    // 重音符
        };
        
        for (String str : specialChars) {
            assertDoesNotThrow(() -> service.processSpecialChars(str));
        }
    }
    
    @Test
    void testWhitespaceVariations() {
        // 测试各种空白字符
        String[] whitespaceTests = {
            " ",                         // 空格
            "\t",                        // 水平制表符
            "\n",                        // 换行符
            "\r",                        // 回车符
            "\f",                        // 换页符
            "\b",                        // 退格符
            "\u00A0",                    // 不换行空格
            "\u2000",                    // 半角空格
            "\u2001",                    // 全角空格
            "\u2002",                    // EN空格
            "\u2003",                    // EM空格
            "\u2004",                    // 三分之一EM空格
            "\u2005",                    // 四分之一EM空格
            "\u2006",                    // 六分之一EM空格
            "\u2007",                    // 数字空格
            "\u2008",                    // 标点空格
            "\u2009",                    // 薄空格
            "\u200A",                    // 头发空格
            "\u2028",                    // 行分隔符
            "\u2029",                    // 段分隔符
            "\u3000",                    // 表意文字空格
        };
        
        for (String whitespace : whitespaceTests) {
            String testStr = "test" + whitespace + "string";
            service.processWhitespace(testStr);
        }
    }
    
    @Test
    void testControlCharacters() {
        // 测试控制字符
        for (int i = 0; i <= 31; i++) {
            String controlChar = String.valueOf((char) i);
            String testStr = "test" + controlChar + "string";
            
            if (i == 9 || i == 10 || i == 13) { // 制表符、换行、回车
                assertDoesNotThrow(() -> service.processControlChars(testStr));
            } else {
                assertThrows(ValidationException.class,
                    () -> service.processControlChars(testStr));
            }
        }
        
        // DEL字符 (127)
        String delChar = String.valueOf((char) 127);
        String testStr = "test" + delChar + "string";
        assertThrows(ValidationException.class,
            () -> service.processControlChars(testStr));
    }
}
```

## 集合边界测试

### 列表边界测试
```java
public class ListBoundaryTest {
    
    @Test
    void testListSizeBoundaries() {
        // 测试各种大小的列表
        List<String>[] sizeTests = new List[]{
            Collections.emptyList(),                    // 空列表
            Collections.singletonList("single"),        // 单元素列表
            Arrays.asList("a", "b"),                    // 双元素列表
            createList(10),                             // 小列表
            createList(100),                            // 中等列表
            createList(1000),                           // 大列表
            createList(10000),                          // 超大列表
            createList(100000),                         // 极限列表
        };
        
        for (List<String> list : sizeTests) {
            assertDoesNotThrow(() -> service.processList(list));
        }
        
        // 测试列表容量限制
        List<String> hugeList = createList(1000000);    // 百万元素
        assertThrows(OutOfMemoryError.class,
            () -> service.processList(hugeList));
    }
    
    @Test
    void testListContentBoundaries() {
        // 测试包含边界值的列表
        List<Object> boundaryList = Arrays.asList(
            null,                        // null元素
            "",                          // 空字符串
            " ",                         // 空白字符串
            Integer.MAX_VALUE,           // 最大整数
            Integer.MIN_VALUE,           // 最小整数
            Double.MAX_VALUE,            // 最大浮点数
            Double.MIN_VALUE,            // 最小浮点数
            Double.NaN,                  // NaN
            Double.POSITIVE_INFINITY,    // 正无穷
            Double.NEGATIVE_INFINITY,    // 负无穷
            new Object(),                // 普通对象
            Collections.emptyList(),     // 空子列表
            Collections.emptyMap()       // 空Map
        );
        
        assertDoesNotThrow(() -> service.processMixedList(boundaryList));
    }
    
    @Test
    void testListModificationBoundaries() {
        // 测试列表修改的边界情况
        List<String> list = new ArrayList<>(Arrays.asList("a", "b", "c"));
        
        // 边界索引操作
        assertThrows(IndexOutOfBoundsException.class,
            () -> list.get(-1));                        // 负索引
        
        assertThrows(IndexOutOfBoundsException.class,
            () -> list.get(list.size()));               // 等于大小的索引
        
        assertThrows(IndexOutOfBoundsException.class,
            () -> list.get(list.size() + 1));           // 超过大小的索引
        
        // 边界修改操作
        assertDoesNotThrow(() -> list.set(0, "new"));   // 第一个元素
        assertDoesNotThrow(() -> list.set(list.size() - 1, "new")); // 最后一个元素
        
        // 空列表操作
        List<String> emptyList = new ArrayList<>();
        assertThrows(IndexOutOfBoundsException.class,
            () -> emptyList.get(0));
        assertThrows(IndexOutOfBoundsException.class,
            () -> emptyList.set(0, "value"));
    }
    
    private List<String> createList(int size) {
        List<String> list = new ArrayList<>(size);
        for (int i = 0; i < size; i++) {
            list.add("item" + i);
        }
        return list;
    }
}
```

### Map边界测试
```java
public class MapBoundaryTest {
    
    @Test
    void testMapSizeBoundaries() {
        // 测试各种大小的Map
        Map<String, String>[] sizeTests = new Map[]{
            Collections.emptyMap(),                     // 空Map
            Collections.singletonMap("key", "value"),   // 单元素Map
            createMap(10),                              // 小Map
            createMap(100),                             // 中等Map
            createMap(1000),                            // 大Map
            createMap(10000),                           // 超大Map
            createMap(100000),                          // 极限Map
        };
        
        for (Map<String, String> map : sizeTests) {
            assertDoesNotThrow(() -> service.processMap(map));
        }
    }
    
    @Test
    void testMapKeyBoundaries() {
        // 测试边界键值
        Map<Object, String> boundaryMap = new HashMap<>();
        
        // 边界键
        boundaryMap.put(null, "null key");              // null键
        boundaryMap.put("", "empty key");               // 空字符串键
        boundaryMap.put(" ", "space key");              // 空白键
        boundaryMap.put(Integer.MAX_VALUE, "max int");  // 最大整数键
        boundaryMap.put(Integer.MIN_VALUE, "min int");  // 最小整数键
        boundaryMap.put(Double.NaN, "nan key");         // NaN键
        boundaryMap.put(new Object(), "object key");    // 对象键
        
        // 长键
        String longKey = "a".repeat(1000);
        boundaryMap.put(longKey, "long key");
        
        // Unicode键
        boundaryMap.put("🎉", "emoji key");
        boundaryMap.put("测试", "chinese key");
        
        assertDoesNotThrow(() -> service.processBoundaryMap(boundaryMap));
    }
    
    @Test
    void testMapValueBoundaries() {
        // 测试边界值
        Map<String, Object> boundaryMap = new HashMap<>();
        
        // 边界值
        boundaryMap.put("null", null);                  // null值
        boundaryMap.put("empty", "");                   // 空字符串值
        boundaryMap.put("space", " ");                  // 空白值
        boundaryMap.put("maxInt", Integer.MAX_VALUE);   // 最大整数值
        boundaryMap.put("minInt", Integer.MIN_VALUE);   // 最小整数值
        boundaryMap.put("nan", Double.NaN);             // NaN值
        boundaryMap.put("inf", Double.POSITIVE_INFINITY); // 无穷值
        boundaryMap.put("object", new Object());        // 对象值
        
        // 大对象值
        String largeValue = "a".repeat(10000);
        boundaryMap.put("large", largeValue);
        
        // 嵌套结构
        Map<String, String> nestedMap = new HashMap<>();
        nestedMap.put("nested", "value");
        boundaryMap.put("nested", nestedMap);
        
        List<String> nestedList = Arrays.asList("a", "b", "c");
        boundaryMap.put("list", nestedList);
        
        assertDoesNotThrow(() -> service.processBoundaryValues(boundaryMap));
    }
    
    @Test
    void testMapCollisionBoundaries() {
        // 测试哈希冲突边界
        Map<String, String> map = new HashMap<>();
        
        // 添加大量可能冲突的键
        for (int i = 0; i < 10000; i++) {
            String key = "key" + (i % 100);  // 只有100个不同的哈希值
            map.put(key, "value" + i);
        }
        
        // 验证能正确处理哈希冲突
        assertDoesNotThrow(() -> service.processMapWithCollisions(map));
        assertEquals(100, map.size());  // 应该有100个唯一键
    }
    
    private Map<String, String> createMap(int size) {
        Map<String, String> map = new HashMap<>(size);
        for (int i = 0; i < size; i++) {
            map.put("key" + i, "value" + i);
        }
        return map;
    }
}
```

## 时间边界测试

### 日期边界测试
```java
public class DateBoundaryTest {
    
    @Test
    void testDateBoundaries() {
        // 测试日期边界
        LocalDate[] dateTests = {
            LocalDate.MIN,                     // 最小日期
            LocalDate.of(1, 1, 1),             // 公元1年
            LocalDate.of(1000, 1, 1),          // 公元1000年
            LocalDate.of(1900, 1, 1),          // 1900年
            LocalDate.of(1970, 1, 1),          // Unix纪元
            LocalDate.of(2000, 1, 1),          // 2000年
            LocalDate.of(2024, 1, 1),          // 当前年份附近
            LocalDate.of(2038, 1, 19),         // 2038年问题
            LocalDate.of(2100, 1, 1),          // 2100年
            LocalDate.of(9999, 12, 31),        // 最大日期
            LocalDate.MAX                      // 理论最大日期
        };
        
        for (LocalDate date : dateTests) {
            assertDoesNotThrow(() -> service.processDate(date));
        }
    }
    
    @Test
    void testMonthBoundaries() {
        // 测试月份边界
        LocalDate[] monthTests = {
            LocalDate.of(2024, 1, 1),          // 1月第一天
            LocalDate.of(2024, 1, 31),         // 1月最后一天
            LocalDate.of(2024, 2, 1),          // 2月第一天
            LocalDate.of(2024, 2, 28),         // 2月平年最后一天
            LocalDate.of(2024, 2, 29),         // 2月闰年最后一天
            LocalDate.of(2024, 3, 1),          // 3月第一天
            LocalDate.of(2024, 3, 31),         // 3月最后一天
            LocalDate.of(2024, 4, 30),         // 4月最后一天
            LocalDate.of(2024, 12, 1),         // 12月第一天
            LocalDate.of(2024, 12, 31),        // 12月最后一天
        };
        
        for (LocalDate date : monthTests) {
            assertDoesNotThrow(() -> service.processMonth(date));
        }
        
        // 测试无效日期
        assertThrows(DateTimeException.class,
            () -> LocalDate.of(2024, 2, 30));  // 2月30日不存在
        
        assertThrows(DateTimeException.class,
            () -> LocalDate.of(2024, 4, 31));  // 4月31日不存在
        
        assertThrows(DateTimeException.class,
            () -> LocalDate.of(2023, 2, 29));  // 平年2月29日不存在
    }
    
    @Test
    void testLeapYearBoundaries() {
        // 测试闰年边界
        int[] leapYears = {1904, 1908, 2000, 2004, 2008, 2012, 2016, 2020, 2024, 2400};
        int[] nonLeapYears = {1900, 2001, 2002, 2003, 2100, 2200, 2300, 2500};
        
        for (int year : leapYears) {
            LocalDate leapDay = LocalDate.of(year, 2, 29);
            assertDoesNotThrow(() -> service.processLeapDay(leapDay));
        }
        
        for (int year : nonLeapYears) {
            assertThrows(DateTimeException.class,
                () -> LocalDate.of(year, 2, 29));
        }
    }
}
```

### 时间边界测试
```java
public class TimeBoundaryTest {
    
    @Test
    void testTimeBoundaries() {
        // 测试时间边界
        LocalTime[] timeTests = {
            LocalTime.MIN,                     // 最小时间 (00:00)
            LocalTime.of(0, 0, 0),             // 午夜
            LocalTime.of(0, 0, 1),             // 午夜后1秒
            LocalTime.of(12, 0, 0),            // 中午
            LocalTime.of(23, 59, 59),          // 最后一秒
            LocalTime.of(23, 59, 59, 999_999_999), // 最后一纳秒
            LocalTime.MAX                      // 最大时间 (23:59:59.999999999)
        };
        
        for (LocalTime time : timeTests) {
            assertDoesNotThrow(() -> service.processTime(time));
        }
    }
    
    @Test
    void testDateTimeBoundaries() {
        // 测试日期时间边界
        LocalDateTime[] dateTimeTests = {
            LocalDateTime.MIN,                 // 最小日期时间
            LocalDateTime.of(1970, 1, 1, 0, 0, 0), // Unix纪元
            LocalDateTime.of(2024, 1, 1, 0, 0, 0), // 新年
            LocalDateTime.of(2024, 12, 31, 23, 59, 59), // 年末
            LocalDateTime.MAX                  // 最大日期时间
        };
        
        for (LocalDateTime dateTime : dateTimeTests) {
            assertDoesNotThrow(() -> service.processDateTime(dateTime));
        }
    }
    
    @Test
    void testTimezoneBoundaries() {
        // 测试时区边界
        ZoneId[] zoneTests = {
            ZoneId.of("UTC"),                  // UTC
            ZoneId.of("GMT"),                  // GMT
            ZoneId.of("America/New_York"),     // 美国东部
            ZoneId.of("Asia/Shanghai"),        // 中国上海
            ZoneId.of("Europe/London"),        // 欧洲伦敦
            ZoneId.of("Pacific/Honolulu"),     // 太平洋
            ZoneId.of("Australia/Sydney"),     // 澳大利亚
            ZoneId.systemDefault(),            // 系统默认
        };
        
        for (ZoneId zone : zoneTests) {
            ZonedDateTime zonedDateTime = ZonedDateTime.now(zone);
            assertDoesNotThrow(() -> service.processZonedDateTime(zonedDateTime));
        }
        
        // 测试无效时区
        assertThrows(ZoneRulesException.class,
            () -> ZoneId.of("Invalid/Zone"));
    }
    
    @Test
    void testDaylightSavingBoundaries() {
        // 测试夏令时边界
        ZoneId zone = ZoneId.of("America/New_York");
        
        // 2024年夏令时开始: 3月10日 2:00 AM跳到3:00 AM
        LocalDateTime beforeDst = LocalDateTime.of(2024, 3, 10, 1, 59, 59);
        LocalDateTime afterDst = LocalDateTime.of(2024, 3, 10, 3, 0, 0);
        
        ZonedDateTime zonedBefore = ZonedDateTime.of(beforeDst, zone);
        ZonedDateTime zonedAfter = ZonedDateTime.of(afterDst, zone);
        
        assertDoesNotThrow(() -> service.processDstTransition(zonedBefore));
        assertDoesNotThrow(() -> service.processDstTransition(zonedAfter));
        
        // 2024年夏令时结束: 11月3日 2:00 AM回到1:00 AM
        LocalDateTime endDst = LocalDateTime.of(2024, 11, 3, 1, 59, 59);
        LocalDateTime repeatHour = LocalDateTime.of(2024, 11, 3, 1, 0, 0); // 重复的一小时
        
        ZonedDateTime zonedEnd = ZonedDateTime.of(endDst, zone);
        
        assertDoesNotThrow(() -> service.processDstTransition(zonedEnd));
        
        // 注意: 重复的一小时需要特殊处理
        ZonedDateTime firstHour = ZonedDateTime.of(repeatHour, zone).withEarlierOffsetAtOverlap();
        ZonedDateTime secondHour = ZonedDateTime.of(repeatHour, zone).withLaterOffsetAtOverlap();
        
        assertNotEquals(firstHour, secondHour); // 两个不同时间
        assertDoesNotThrow(() -> service.processDstTransition(firstHour));
        assertDoesNotThrow(() -> service.processDstTransition(secondHour));
    }
}
```

## 状态边界测试

### 枚举状态边界测试
```java
public class EnumStateBoundaryTest {
    
    enum UserStatus {
        INITIAL,        // 初始状态
        ACTIVE,         // 激活状态
        INACTIVE,       // 非激活状态
        SUSPENDED,      // 暂停状态
        DELETED,        // 删除状态
        UNKNOWN         // 未知状态
    }
    
    @Test
    void testAllEnumValues() {
        // 测试所有枚举值
        for (UserStatus status : UserStatus.values()) {
            User user = TestDataFactory.createUser();
            user.setStatus(status);
            assertDoesNotThrow(() -> service.processUserStatus(user));
        }
    }
    
    @Test
    void testInvalidEnumValue() {
        // 测试无效的枚举值
        User user = TestDataFactory.createUser();
        
        // 通过反射设置无效的枚举值
        try {
            Field statusField = User.class.getDeclaredField("status");
            statusField.setAccessible(true);
            statusField.set(user, "INVALID_STATUS");
            
            assertThrows(IllegalArgumentException.class,
                () -> service.processUserStatus(user));
        } catch (Exception e) {
            fail("反射设置字段失败: " + e.getMessage());
        }
    }
    
    @Test
    void testNullEnumValue() {
        // 测试null枚举值
        User user = TestDataFactory.createUser();
        user.setStatus(null);
        
        assertThrows(IllegalArgumentException.class,
            () -> service.processUserStatus(user));
    }
    
    @Test
    void testStateTransitionBoundaries() {
        // 测试状态转换边界
        Map<UserStatus, List<UserStatus>> validTransitions = Map.of(
            UserStatus.INITIAL, Arrays.asList(UserStatus.ACTIVE, UserStatus.DELETED),
            UserStatus.ACTIVE, Arrays.asList(UserStatus.INACTIVE, UserStatus.SUSPENDED, UserStatus.DELETED),
            UserStatus.INACTIVE, Arrays.asList(UserStatus.ACTIVE, UserStatus.DELETED),
            UserStatus.SUSPENDED, Arrays.asList(UserStatus.ACTIVE, UserStatus.DELETED),
            UserStatus.DELETED, Collections.emptyList() // 终止状态
        );
        
        // 测试所有有效转换
        for (Map.Entry<UserStatus, List<UserStatus>> entry : validTransitions.entrySet()) {
            UserStatus from = entry.getKey();
            for (UserStatus to : entry.getValue()) {
                User user = TestDataFactory.createUserWithStatus(from);
                assertDoesNotThrow(() -> service.transitionStatus(user, to));
            }
        }
        
        // 测试无效转换
        Map<UserStatus, List<UserStatus>> invalidTransitions = Map.of(
            UserStatus.DELETED, Arrays.asList(UserStatus.ACTIVE, UserStatus.INACTIVE, UserStatus.SUSPENDED),
            UserStatus.ACTIVE, Arrays.asList(UserStatus.INITIAL), // 不能回到初始状态
            UserStatus.UNKNOWN, UserStatus.values() // 未知状态不能转换到任何状态
        );
        
        for (Map.Entry<UserStatus, List<UserStatus>> entry : invalidTransitions.entrySet()) {
            UserStatus from = entry.getKey();
            for (UserStatus to : entry.getValue()) {
                User user = TestDataFactory.createUserWithStatus(from);
                assertThrows(IllegalStateException.class,
                    () -> service.transitionStatus(user, to));
            }
        }
    }
}
```

### 数值状态边界测试
```java
public class NumericStateBoundaryTest {
    
    @Test
    void testNumericStateBoundaries() {
        // 测试数值状态边界
        int[] stateTests = {
            Integer.MIN_VALUE,      // 最小状态值
            -100,                   // 负状态值
            -1,                     // 负一状态
            0,                      // 零状态
            1,                      // 初始状态
            99,                     // 正常状态
            100,                    // 边界状态
            Integer.MAX_VALUE       // 最大状态值
        };
        
        for (int state : stateTests) {
            User user = TestDataFactory.createUser();
            user.setStatus(state);
            
            if (state >= 0 && state <= 100) {
                assertDoesNotThrow(() -> service.processNumericState(user));
            } else {
                assertThrows(IllegalArgumentException.class,
                    () -> service.processNumericState(user));
            }
        }
    }
    
    @Test
    void testStateMachineBoundaries() {
        // 测试状态机边界
        StateMachine stateMachine = new StateMachine();
        
        // 测试初始状态
        assertEquals(State.INITIAL, stateMachine.getCurrentState());
        
        // 测试有效状态转换
        assertDoesNotThrow(() -> stateMachine.transition(Event.START));
        assertEquals(State.RUNNING, stateMachine.getCurrentState());
        
        assertDoesNotThrow(() -> stateMachine.transition(Event.PAUSE));
        assertEquals(State.PAUSED, stateMachine.getCurrentState());
        
        assertDoesNotThrow(() -> stateMachine.transition(Event.RESUME));
        assertEquals(State.RUNNING, stateMachine.getCurrentState());
        
        assertDoesNotThrow(() -> stateMachine.transition(Event.STOP));
        assertEquals(State.STOPPED, stateMachine.getCurrentState());
        
        // 测试无效状态转换（终止状态不能转换）
        assertThrows(IllegalStateException.class,
            () -> stateMachine.transition(Event.START));
        
        // 测试重置状态机
        stateMachine.reset();
        assertEquals(State.INITIAL, stateMachine.getCurrentState());
        
        // 测试多次重置
        for (int i = 0; i < 1000; i++) {
            stateMachine.reset();
            assertEquals(State.INITIAL, stateMachine.getCurrentState());
        }
        
        // 测试并发状态转换
        ExecutorService executor = Executors.newFixedThreadPool(10);
        List<Future<?>> futures = new ArrayList<>();
        
        for (int i = 0; i < 100; i++) {
            futures.add(executor.submit(() -> {
                try {
                    stateMachine.transition(Event.START);
                    stateMachine.transition(Event.STOP);
                } catch (Exception e) {
                    // 预期会有并发异常
                }
            }));
        }
        
        // 等待所有任务完成
        for (Future<?> future : futures) {
            try {
                future.get();
            } catch (Exception e) {
                // 忽略异常
            }
        }
        
        executor.shutdown();
        
        // 最终状态应该是STOPPED或RUNNING，取决于并发执行顺序
        State finalState = stateMachine.getCurrentState();
        assertTrue(finalState == State.STOPPED || finalState == State.RUNNING);
    }
}
```

## 容量边界测试

### 内存容量边界测试
```java
public class MemoryCapacityBoundaryTest {
    
    @Test
    void testMemoryAllocationBoundaries() {
        // 测试内存分配边界
        int[] sizes = {
            1,                          // 最小分配
            10,                         // 小分配
            100,                        // 中等分配
            1024,                       // 1KB
            1024 * 1024,                // 1MB
            10 * 1024 * 1024,           // 10MB
            100 * 1024 * 1024,          // 100MB
            1024 * 1024 * 1024,         // 1GB
        };
        
        for (int size : sizes) {
            byte[] data = new byte[size];
            assertDoesNotThrow(() -> service.processLargeData(data));
        }
        
        // 测试内存不足情况（需要大量内存）
        if (!isMemoryLimitedEnvironment()) {
            int hugeSize = Integer.MAX_VALUE - 8; // 接近最大数组大小
            assertThrows(OutOfMemoryError.class,
                () -> new byte[hugeSize]);
        }
    }
    
    @Test
    void testObjectCountBoundaries() {
        // 测试对象数量边界
        int[] counts = {
            0,                          // 无对象
            1,                          // 单个对象
            10,                         // 少量对象
            100,                        // 中等数量
            1000,                       // 大量对象
            10000,                      // 超大量对象
            100000,                     // 极限数量
        };
        
        for (int count : counts) {
            List<User> users = createUsers(count);
            assertDoesNotThrow(() -> service.processUserList(users));
        }
    }
    
    @Test
    void testStringLengthCapacity() {
        // 测试字符串长度容量
        int[] lengths = {
            0,                          // 空字符串
            1,                          // 单字符
            10,                         // 短字符串
            100,                        // 中等字符串
            1000,                       // 长字符串
            10000,                      // 超长字符串
            100000,                     // 极长字符串
        };
        
        for (int length : lengths) {
            String str = "a".repeat(length);
            assertDoesNotThrow(() -> service.processLongString(str));
        }
        
        // 测试超大字符串（可能内存不足）
        if (!isMemoryLimitedEnvironment()) {
            int hugeLength = 100_000_000; // 1亿字符
            assertThrows(OutOfMemoryError.class,
                () -> "a".repeat(hugeLength));
        }
    }
    
    private List<User> createUsers(int count) {
        List<User> users = new ArrayList<>(count);
        for (int i = 0; i < count; i++) {
            users.add(TestDataFactory.createUser());
        }
        return users;
    }
    
    private boolean isMemoryLimitedEnvironment() {
        // 检查是否为内存受限环境（如CI/CD环境）
        long maxMemory = Runtime.getRuntime().maxMemory();
        return maxMemory < 1024 * 1024 * 1024; // 小于1GB
    }
}
```

## 边界测试最佳实践

### 1. 使用参数化测试
```java
@ParameterizedTest
@MethodSource("boundaryValueProvider")
void testWithAllBoundaryValues(Object value) {
    // 测试所有边界值
    assertDoesNotThrow(() -> service.process(value));
}

static Stream<Arguments> boundaryValueProvider() {
    return Stream.of(
        // 数值边界
        Arguments.of(Integer.MIN_VALUE),
        Arguments.of(-1),
        Arguments.of(0),
        Arguments.of(1),
        Arguments.of(Integer.MAX_VALUE),
        
        // 字符串边界
        Arguments.of(""),
        Arguments.of(" "),
        Arguments.of("a"),
        Arguments.of("a".repeat(255)),
        
        // 集合边界
        Arguments.of(Collections.emptyList()),
        Arguments.of(Collections.singletonList("item")),
        
        // 时间边界
        Arguments.of(LocalDateTime.MIN),
        Arguments.of(LocalDateTime.MAX)
    );
}
```

### 2. 创建边界测试工具类
```java
public class BoundaryTestUtils {
    
    public static List<Integer> integerBoundaries() {
        return Arrays.asList(
            Integer.MIN_VALUE,
            Integer.MIN_VALUE + 1,
            -100,
            -1,
            0,
            1,
            100,
            Integer.MAX_VALUE - 1,
            Integer.MAX_VALUE
        );
    }
    
    public static List<String> stringBoundaries() {
        return Arrays.asList(
            "",
            " ",
            "a",
            "ab",
            "abc",
            "a".repeat(255),
            "a".repeat(256),
            "test\nnewline",
            "test\ttab",
            "🎉emoji",
            "测试中文"
        );
    }
    
    public static List<LocalDate> dateBoundaries() {
        return Arrays.asList(
            LocalDate.MIN,
            LocalDate.of(1, 1, 1),
            LocalDate.of(1970, 1, 1),
            LocalDate.now(),
            LocalDate.of(2038, 1, 19),
            LocalDate.of(9999, 12, 31),
            LocalDate.MAX
        );
    }
    
    public static <T> void testAllBoundaries(
            Consumer<T> processor, 
            List<T> boundaries) {
        
        for (T boundary : boundaries) {
            try {
                processor.accept(boundary);
            } catch (Exception e) {
                fail("边界值测试失败: " + boundary + ", 错误: " + e.getMessage());
            }
        }
    }
}
```

### 3. 边界测试命名规范
```java
// 使用清晰的测试命名
@Test
void test[Method]_[BoundaryType]_[Value]_[ExpectedResult]() {
    // 示例:
    // testCreateUser_UsernameLength_Max255Chars_Success()
    // testCreateUser_UsernameLength_256Chars_ThrowsException()
    // testProcessOrder_Amount_Zero_ThrowsException()
    // testProcessOrder_Amount_Negative_ThrowsException()
}

// 分组边界测试
@Nested
class StringLengthBoundaries {
    @Test void testEmptyString() { ... }
    @Test void testSingleCharacter() { ... }
    @Test void testMaxLength() { ... }
    @Test void testExceedsMaxLength() { ... }
}

@Nested
class NumericBoundaries {
    @Test void testMinimumValue() { ... }
    @Test void testMaximumValue() { ... }
    @Test void testZeroValue() { ... }
    @Test void testNegativeValue() { ... }
}
```

### 4. 边界测试覆盖率检查
```java
// 确保覆盖所有边界
@Test
void testAllBoundaryConditions() {
    // 记录测试的边界
    Set<String> testedBoundaries = new HashSet<>();
    
    // 执行边界测试
    testStringBoundaries(testedBoundaries);
    testNumericBoundaries(testedBoundaries);
    testCollectionBoundaries(testedBoundaries);
    testDateTimeBoundaries(testedBoundaries);
    testStateBoundaries(testedBoundaries);
    
    // 验证所有边界都被测试
    Set<String> expectedBoundaries = Set.of(
        "STRING_EMPTY",
        "STRING_MAX_LENGTH", 
        "INTEGER_MIN",
        "INTEGER_MAX",
        "COLLECTION_EMPTY",
        "COLLECTION_SINGLE",
        "DATE_MIN",
        "DATE_MAX",
        "STATE_INITIAL",
        "STATE_FINAL"
    );
    
    assertThat(testedBoundaries).containsAll(expectedBoundaries);
}

private void testStringBoundaries(Set<String> testedBoundaries) {
    testedBoundaries.add("STRING_EMPTY");
    testEmptyString();
    
    testedBoundaries.add("STRING_MAX_LENGTH");
    testMaxLengthString();
    // ... 其他字符串边界测试
}
```

## 总结

边界值测试是发现隐藏错误的最有效方法之一。通过系统化的边界测试，可以：

1. **发现边缘情况错误** - 边界附近最容易出现错误
2. **提高代码健壮性** - 确保系统能处理各种边界条件
3. **减少生产问题** - 在生产环境发现边界问题代价高昂
4. **增强用户信心** - 用户信任能处理各种情况的系统

遵循这些边界测试策略，可以为Spring Boot应用构建全面的边界条件测试覆盖。
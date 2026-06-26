# MyBatis 配置指南

## 标准配置方式

### 1. application.yml 配置

```yaml
mybatis:
  mapper-locations: classpath:mapper/*.xml
  type-aliases-package: com.xxx.entity
  configuration:
    map-underscore-to-camel-case: true
    cache-enabled: true
    lazy-loading-enabled: true
    default-executor-type: simple
    jdbc-type-for-null: null
    local-cache-scope: session
```

### 2. MybatisConfig.java

```java
package com.xxx.config;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.context.annotation.Configuration;

@Configuration
@MapperScan("com.xxx.dao")
public class MybatisConfig {
    // 额外配置可在此添加
}
```

### 3. Mapper 接口示例

```java
package com.xxx.dao;

import com.xxx.entity.User;
import org.apache.ibatis.annotations.*;
import java.util.List;

@Mapper
public interface UserMapper {
    
    @Select("SELECT * FROM user WHERE id = #{id}")
    User selectById(Long id);
    
    @Insert("INSERT INTO user(name, email) VALUES(#{name}, #{email})")
    @Options(useGeneratedKeys = true, keyProperty = "id")
    int insert(User user);
    
    @Update("UPDATE user SET name=#{name}, email=#{email} WHERE id=#{id}")
    int update(User user);
    
    @Delete("DELETE FROM user WHERE id = #{id}")
    int deleteById(Long id);
    
    List<User> selectList(@Param("name") String name);
}
```

### 4. XML 映射文件

位置：`src/main/resources/mapper/UserMapper.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" 
  "http://mybatis.org/dtd/mybatis-3-mapper.dtd">

<mapper namespace="com.xxx.dao.UserMapper">
    
    <resultMap id="BaseResultMap" type="com.xxx.entity.User">
        <id column="id" property="id"/>
        <result column="name" property="name"/>
        <result column="email" property="email"/>
        <result column="create_time" property="createTime"/>
    </resultMap>
    
    <sql id="Base_Column_List">
        id, name, email, create_time
    </sql>
    
    <select id="selectList" resultMap="BaseResultMap">
        SELECT <include refid="Base_Column_List"/>
        FROM user
        <where>
            <if test="name != null and name != ''">
                AND name LIKE CONCAT('%', #{name}, '%')
            </if>
        </where>
    </select>
    
</mapper>
```

## 命名规范

| 类型 | 命名规则 | 示例 |
|------|----------|------|
| Mapper 接口 | XxxMapper | UserMapper |
| XML 文件 | XxxMapper.xml | UserMapper.xml |
| namespace | 全限定类名 | com.xxx.dao.UserMapper |
| 方法名 | 动词+名词 | selectById, insertBatch |
| resultMap | BaseResultMap | 统一使用 |
| SQL ID | 与方法名一致 | selectList |

## 最佳实践

1. **XML 与注解混用**：简单 SQL 用注解，复杂 SQL 用 XML
2. **统一 resultMap**：避免重复定义字段映射
3. **使用 `<where>` 标签**：自动处理 WHERE 和 AND
4. **批量操作**：使用 `foreach` 标签
5. **分页**：配合 PageHelper 插件

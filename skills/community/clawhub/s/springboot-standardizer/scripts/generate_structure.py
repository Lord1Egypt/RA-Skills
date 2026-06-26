#!/usr/bin/env python3
"""
生成标准 SpringBoot 项目结构
"""

import os
import sys
import shutil
from pathlib import Path

# 标准目录结构
STANDARD_DIRS = [
    'src/main/java/{package_path}/controller',
    'src/main/java/{package_path}/service/impl',
    'src/main/java/{package_path}/dao',
    'src/main/java/{package_path}/entity',
    'src/main/java/{package_path}/dto',
    'src/main/java/{package_path}/vo',
    'src/main/java/{package_path}/config',
    'src/main/java/{package_path}/util',
    'src/main/resources/mapper',
    'src/test/java/{package_path}',
]

# 标准文件模板
FILE_TEMPLATES = {
    'pom.xml': '''<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.2.0</version>
        <relativePath/>
    </parent>
    
    <groupId>{group_id}</groupId>
    <artifactId>{artifact_id}</artifactId>
    <version>1.0.0</version>
    <packaging>jar</packaging>
    
    <name>{project_name}</name>
    <description>Standard SpringBoot Project</description>
    
    <properties>
        <java.version>17</java.version>
        <mybatis-spring-boot.version>3.0.3</mybatis-spring-boot.version>
    </properties>
    
    <dependencies>
        <!-- SpringBoot Starter -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        
        <!-- MyBatis -->
        <dependency>
            <groupId>org.mybatis.spring.boot</groupId>
            <artifactId>mybatis-spring-boot-starter</artifactId>
            <version>${{mybatis-spring-boot.version}}</version>
        </dependency>
        
        <!-- MySQL -->
        <dependency>
            <groupId>com.mysql</groupId>
            <artifactId>mysql-connector-j</artifactId>
            <scope>runtime</scope>
        </dependency>
        
        <!-- Redis -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-redis</artifactId>
        </dependency>
        
        <!-- Kafka -->
        <dependency>
            <groupId>org.springframework.kafka</groupId>
            <artifactId>spring-kafka</artifactId>
        </dependency>
        
        <!-- Lombok -->
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <optional>true</optional>
        </dependency>
        
        <!-- Test -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>
    
    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
                <configuration>
                    <excludes>
                        <exclude>
                            <groupId>org.projectlombok</groupId>
                            <artifactId>lombok</artifactId>
                        </exclude>
                    </excludes>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
''',

    'src/main/resources/application.yml': '''server:
  port: 8080
  servlet:
    context-path: /

spring:
  application:
    name: {project_name}
  
  profiles:
    active: dev
  
  datasource:
    url: jdbc:mysql://localhost:3306/{db_name}?useUnicode=true&characterEncoding=utf-8&serverTimezone=Asia/Shanghai
    username: ${MYSQL_USERNAME:root}
    password: ${MYSQL_PASSWORD:}
    driver-class-name: com.mysql.cj.jdbc.Driver
    hikari:
      minimum-idle: 5
      maximum-pool-size: 20
      connection-timeout: 30000
      idle-timeout: 600000
      max-lifetime: 1800000
  
  redis:
    host: ${REDIS_HOST:localhost}
    port: ${REDIS_PORT:6379}
    password: ${REDIS_PASSWORD:}
    database: 0
    timeout: 3000ms
    lettuce:
      pool:
        max-active: 8
        max-idle: 8
        min-idle: 0
  
  kafka:
    bootstrap-servers: ${KAFKA_SERVERS:localhost:9092}
    producer:
      key-serializer: org.apache.kafka.common.serialization.StringSerializer
      value-serializer: org.apache.kafka.common.serialization.StringSerializer
      retries: 3
    consumer:
      group-id: {project_name}-group
      key-deserializer: org.apache.kafka.common.serialization.StringDeserializer
      value-deserializer: org.apache.kafka.common.serialization.StringDeserializer
      auto-offset-reset: earliest

# MyBatis配置
mybatis:
  mapper-locations: classpath:mapper/*.xml
  type-aliases-package: {package_name}.entity
  configuration:
    map-underscore-to-camel-case: true
    cache-enabled: true
    lazy-loading-enabled: true

# 日志配置
logging:
  level:
    {package_name}: DEBUG
    org.springframework.jdbc: DEBUG
''',

    'src/main/resources/application-dev.yml': '''server:
  port: 8080

spring:
  datasource:
    url: jdbc:mysql://localhost:3306/{db_name}_dev?useUnicode=true&characterEncoding=utf-8&serverTimezone=Asia/Shanghai
    username: root
    password: 
  
  redis:
    host: localhost
    port: 6379

logging:
  level:
    {package_name}: DEBUG
''',

    'src/main/resources/application-prod.yml': '''server:
  port: 8080

spring:
  datasource:
    url: jdbc:mysql://${MYSQL_HOST}/${DB_NAME}?useUnicode=true&characterEncoding=utf-8&serverTimezone=Asia/Shanghai
    username: ${MYSQL_USERNAME}
    password: ${MYSQL_PASSWORD}
  
  redis:
    host: ${REDIS_HOST}
    port: ${REDIS_PORT}
    password: ${REDIS_PASSWORD}

logging:
  level:
    {package_name}: WARN
    root: WARN
''',

    'src/main/java/{package_path}/Application.java': '''package {package_name};

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class Application {{
    public static void main(String[] args) {{
        SpringApplication.run(Application.class, args);
    }}
}}
''',

    'src/main/java/{package_path}/config/MybatisConfig.java': '''package {package_name}.config;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.context.annotation.Configuration;

@Configuration
@MapperScan("{package_name}.dao")
public class MybatisConfig {{
    // MyBatis 配置
}}
''',

    'src/main/java/{package_path}/config/RedisConfig.java': '''package {package_name}.config;

import com.fasterxml.jackson.annotation.JsonTypeInfo;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.jsontype.impl.LaissezFaireSubTypeValidator;
import org.springframework.cache.annotation.EnableCaching;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.redis.connection.RedisConnectionFactory;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.data.redis.serializer.Jackson2JsonRedisSerializer;
import org.springframework.data.redis.serializer.StringRedisSerializer;

@Configuration
@EnableCaching
public class RedisConfig {{

    @Bean
    public RedisTemplate<String, Object> redisTemplate(RedisConnectionFactory connectionFactory) {{
        RedisTemplate<String, Object> template = new RedisTemplate<>();
        template.setConnectionFactory(connectionFactory);

        // 使用Jackson2JsonRedisSerializer来序列化和反序列化redis的value值
        Jackson2JsonRedisSerializer<Object> serializer = new Jackson2JsonRedisSerializer<>(Object.class);
        ObjectMapper mapper = new ObjectMapper();
        mapper.activateDefaultTyping(LaissezFaireSubTypeValidator.instance, 
            ObjectMapper.DefaultTyping.NON_FINAL, JsonTypeInfo.As.PROPERTY);
        serializer.setObjectMapper(mapper);

        StringRedisSerializer stringSerializer = new StringRedisSerializer();
        
        // key采用String的序列化方式
        template.setKeySerializer(stringSerializer);
        // hash的key也采用String的序列化方式
        template.setHashKeySerializer(stringSerializer);
        // value序列化方式采用jackson
        template.setValueSerializer(serializer);
        // hash的value序列化方式采用jackson
        template.setHashValueSerializer(serializer);
        
        template.afterPropertiesSet();
        return template;
    }}
}}
''',

    'src/main/java/{package_path}/config/KafkaConfig.java': '''package {package_name}.config;

import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.apache.kafka.common.serialization.StringSerializer;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.config.ConcurrentKafkaListenerContainerFactory;
import org.springframework.kafka.core.*;

import java.util.HashMap;
import java.util.Map;

@Configuration
public class KafkaConfig {{

    @Value("${spring.kafka.bootstrap-servers}")
    private String bootstrapServers;

    @Bean
    public ProducerFactory<String, String> producerFactory() {{
        Map<String, Object> config = new HashMap<>();
        config.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);
        config.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
        config.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
        return new DefaultKafkaProducerFactory<>(config);
    }}

    @Bean
    public KafkaTemplate<String, String> kafkaTemplate() {{
        return new KafkaTemplate<>(producerFactory());
    }}

    @Bean
    public ConsumerFactory<String, String> consumerFactory() {{
        Map<String, Object> config = new HashMap<>();
        config.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);
        config.put(ConsumerConfig.GROUP_ID_CONFIG, "{project_name}-group");
        config.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
        config.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
        return new DefaultKafkaConsumerFactory<>(config);
    }}

    @Bean
    public ConcurrentKafkaListenerContainerFactory<String, String> kafkaListenerContainerFactory() {{
        ConcurrentKafkaListenerContainerFactory<String, String> factory = 
            new ConcurrentKafkaListenerContainerFactory<>();
        factory.setConsumerFactory(consumerFactory());
        return factory;
    }}
}}
''',

    'src/main/java/{package_path}/common/Result.java': '''package {package_name}.common;

import lombok.Data;

@Data
public class Result<T> {{
    private Integer code;
    private String message;
    private T data;

    public static <T> Result<T> success(T data) {{
        Result<T> result = new Result<>();
        result.setCode(200);
        result.setMessage("success");
        result.setData(data);
        return result;
    }}

    public static <T> Result<T> success() {{
        return success(null);
    }}

    public static <T> Result<T> error(String message) {{
        Result<T> result = new Result<>();
        result.setCode(500);
        result.setMessage(message);
        return result;
    }}

    public static <T> Result<T> error(Integer code, String message) {{
        Result<T> result = new Result<>();
        result.setCode(code);
        result.setMessage(message);
        return result;
    }}
}}
''',

    'src/main/java/{package_path}/common/PageResult.java': '''package {package_name}.common;

import lombok.Data;
import java.util.List;

@Data
public class PageResult<T> {{
    private Long total;
    private List<T> list;
    private Integer pageNum;
    private Integer pageSize;
    private Integer pages;

    public static <T> PageResult<T> of(Long total, List<T> list, Integer pageNum, Integer pageSize) {{
        PageResult<T> result = new PageResult<>();
        result.setTotal(total);
        result.setList(list);
        result.setPageNum(pageNum);
        result.setPageSize(pageSize);
        result.setPages((int) Math.ceil((double) total / pageSize));
        return result;
    }}
}}
''',

    '.gitignore': '''HELP.md
target/
!.mvn/wrapper/maven-wrapper.jar
!**/src/main/**/target/
!**/src/test/**/target/

### STS ###
.apt_generated
.classpath
.factorypath
.project
.settings
.springBeans
.sts4-cache

### IntelliJ IDEA ###
.idea
*.iws
*.iml
*.ipr

### NetBeans ###
/nbproject/private/
/nbbuild/
/dist/
/nbdist/
/.nb-gradle/
build/
!**/src/main/**/build/
!**/src/test/**/build/

### VS Code ###
.vscode/

### Logs ###
*.log
logs/

### OS ###
.DS_Store
Thumbs.db

### Environment ###
.env
.env.local
''',
}


def create_directories(base_path, package_name):
    """创建标准目录结构"""
    package_path = package_name.replace('.', '/')
    
    for dir_template in STANDARD_DIRS:
        dir_path = dir_template.format(package_path=package_path)
        full_path = os.path.join(base_path, dir_path)
        os.makedirs(full_path, exist_ok=True)
        print(f"创建目录: {full_path}")


def create_files(base_path, package_name, project_name, group_id, artifact_id, db_name):
    """创建标准文件"""
    package_path = package_name.replace('.', '/')
    
    for file_template, content in FILE_TEMPLATES.items():
        file_path = file_template.format(package_path=package_path)
        full_path = os.path.join(base_path, file_path)
        
        # 确保目录存在
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        # 填充模板
        filled_content = content.format(
            package_name=package_name,
            package_path=package_path,
            project_name=project_name,
            group_id=group_id,
            artifact_id=artifact_id,
            db_name=db_name
        )
        
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(filled_content)
        print(f"创建文件: {full_path}")


def main():
    if len(sys.argv) < 2:
        print("用法: python generate_structure.py <输出路径> [选项]")
        print("选项:")
        print("  --package <包名>     根包名 (默认: com.example)")
        print("  --name <项目名>      项目名称 (默认: myproject)")
        print("  --group <groupId>    Maven groupId (默认: com.example)")
        print("  --artifact <artifactId> Maven artifactId (默认: myproject)")
        print("  --db <数据库名>      数据库名 (默认: mydb)")
        sys.exit(1)
    
    output_path = sys.argv[1]
    
    # 解析参数
    package_name = 'com.example'
    project_name = 'myproject'
    group_id = 'com.example'
    artifact_id = 'myproject'
    db_name = 'mydb'
    
    args = sys.argv[2:]
    i = 0
    while i < len(args):
        if args[i] == '--package' and i + 1 < len(args):
            package_name = args[i + 1]
            i += 2
        elif args[i] == '--name' and i + 1 < len(args):
            project_name = args[i + 1]
            i += 2
        elif args[i] == '--group' and i + 1 < len(args):
            group_id = args[i + 1]
            i += 2
        elif args[i] == '--artifact' and i + 1 < len(args):
            artifact_id = args[i + 1]
            i += 2
        elif args[i] == '--db' and i + 1 < len(args):
            db_name = args[i + 1]
            i += 2
        else:
            i += 1
    
    print(f"生成 SpringBoot 标准项目结构")
    print(f"输出路径: {output_path}")
    print(f"包名: {package_name}")
    print(f"项目名: {project_name}")
    print("-" * 60)
    
    # 创建目录
    create_directories(output_path, package_name)
    
    # 创建文件
    create_files(output_path, package_name, project_name, group_id, artifact_id, db_name)
    
    print("-" * 60)
    print("✓ 项目结构生成完成!")
    print(f"\n下一步:")
    print(f"  cd {output_path}")
    print(f"  mvn clean install")


if __name__ == '__main__':
    main()

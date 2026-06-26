package com.example.mapper;

import com.example.entity.User;
import org.junit.jupiter.api.Test;
import org.mybatis.spring.boot.test.autoconfigure.MybatisTest;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.test.context.jdbc.Sql;

import java.time.LocalDateTime;
import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

/**
 * MyBatis Mapper层测试示例
 * 
 * 测试策略：
 * 1. 正常流程：成功的CRUD操作
 * 2. 异常测试：重复数据、无效数据
 * 3. 边界测试：最大长度、时间边界、状态边界
 */
@MybatisTest
@Sql("/test-data.sql")
public class UserMapperTest {

    @Autowired
    private UserMapper userMapper;

    // ============= 正常流程测试 =============
    
    @Test
    public void testSelectById_Success() {
        // Given: 数据库中已有ID为1的用户
        Long userId = 1L;
        
        // When: 查询用户
        User user = userMapper.selectById(userId);
        
        // Then: 验证返回的用户数据
        assertThat(user).isNotNull();
        assertThat(user.getId()).isEqualTo(userId);
        assertThat(user.getUsername()).isEqualTo("normal_user");
        assertThat(user.getEmail()).isEqualTo("normal@example.com");
        assertThat(user.getAge()).isEqualTo(25);
        assertThat(user.getStatus()).isEqualTo("ACTIVE");
    }

    @Test
    public void testInsertUser_Success() {
        // Given: 新的用户数据
        User newUser = User.builder()
                .username("new_user")
                .email("new@example.com")
                .age(30)
                .status("ACTIVE")
                .createdAt(LocalDateTime.now())
                .build();
        
        // When: 插入用户
        int result = userMapper.insert(newUser);
        
        // Then: 验证插入成功
        assertThat(result).isEqualTo(1);
        assertThat(newUser.getId()).isNotNull();
        
        // 验证可以查询到新插入的用户
        User savedUser = userMapper.selectById(newUser.getId());
        assertThat(savedUser).isNotNull();
        assertThat(savedUser.getUsername()).isEqualTo("new_user");
    }

    @Test
    public void testUpdateUser_Success() {
        // Given: 已有的用户和更新数据
        Long userId = 1L;
        User existingUser = userMapper.selectById(userId);
        
        User updateData = User.builder()
                .id(userId)
                .username("updated_user")
                .email("updated@example.com")
                .age(existingUser.getAge() + 1)
                .status("INACTIVE")
                .build();
        
        // When: 更新用户
        int result = userMapper.update(updateData);
        
        // Then: 验证更新成功
        assertThat(result).isEqualTo(1);
        
        User updatedUser = userMapper.selectById(userId);
        assertThat(updatedUser.getUsername()).isEqualTo("updated_user");
        assertThat(updatedUser.getEmail()).isEqualTo("updated@example.com");
        assertThat(updatedUser.getStatus()).isEqualTo("INACTIVE");
    }

    // ============= 异常测试 =============
    
    @Test
    @Sql("/duplicate-test-data.sql")
    public void testInsertUser_DuplicateUsername_ThrowsException() {
        // Given: 用户名已存在的用户
        User duplicateUser = User.builder()
                .username("duplicate_user")  // 用户名已存在
                .email("duplicate@example.com")
                .age(25)
                .status("ACTIVE")
                .createdAt(LocalDateTime.now())
                .build();
        
        // When/Then: 验证插入失败，抛出异常
        assertThatThrownBy(() -> userMapper.insert(duplicateUser))
                .isInstanceOf(Exception.class);  // 主键冲突或唯一约束异常
    }

    @Test
    public void testSelectById_UserNotFound_ReturnsNull() {
        // Given: 不存在的用户ID
        Long nonExistentId = 999L;
        
        // When: 查询不存在的用户
        User user = userMapper.selectById(nonExistentId);
        
        // Then: 验证返回null
        assertThat(user).isNull();
    }

    // ============= 边界测试 =============
    
    @Test
    @Sql("/boundary-test-data.sql")
    public void testSelectUsers_WithBoundaryValues() {
        // When: 查询所有用户（包含边界值用户）
        List<User> users = userMapper.selectAll();
        
        // Then: 验证边界值数据
        assertThat(users).hasSize(3);  // 包含边界值用户
        
        // 验证最大长度用户名
        User maxLengthUser = users.stream()
                .filter(u -> u.getUsername().length() == 100)
                .findFirst()
                .orElse(null);
        assertThat(maxLengthUser).isNotNull();
        assertThat(maxLengthUser.getUsername()).hasSize(100);
        
        // 验证最小年龄用户
        User minAgeUser = users.stream()
                .filter(u -> u.getAge() == 0)
                .findFirst()
                .orElse(null);
        assertThat(minAgeUser).isNotNull();
        assertThat(minAgeUser.getAge()).isEqualTo(0);
        
        // 验证最早创建时间用户
        User earliestUser = users.stream()
                .filter(u -> u.getCreatedAt().getYear() == 1900)
                .findFirst()
                .orElse(null);
        assertThat(earliestUser).isNotNull();
        assertThat(earliestUser.getCreatedAt().getYear()).isEqualTo(1900);
    }

    @Test
    public void testSearchUsers_WithPagination() {
        // Given: 分页参数
        int page = 0;
        int size = 2;
        
        // When: 分页查询用户
        List<User> page1 = userMapper.selectByPage(page, size);
        List<User> page2 = userMapper.selectByPage(page + 1, size);
        
        // Then: 验证分页结果
        assertThat(page1).hasSize(Math.min(size, 5));  // 不超过总数据量
        assertThat(page2).hasSize(Math.min(size, 5 - size));
        
        // 验证分页不重复
        if (!page1.isEmpty() && !page2.isEmpty()) {
            assertThat(page1.get(0).getId())
                    .isNotEqualTo(page2.get(0).getId());
        }
    }
}
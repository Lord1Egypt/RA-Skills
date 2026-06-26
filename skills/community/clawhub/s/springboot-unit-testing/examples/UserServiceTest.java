package com.example.service;

import com.example.entity.User;
import com.example.exception.UserNotFoundException;
import com.example.mapper.UserMapper;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.time.LocalDateTime;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyLong;
import static org.mockito.BDDMockito.given;
import static org.mockito.Mockito.*;

/**
 * Service层单元测试示例
 * 
 * 测试策略：
 * 1. 使用Mockito模拟依赖的Mapper层
 * 2. 测试业务逻辑、异常处理、事务管理
 * 3. 验证Mock交互和返回值
 */
@ExtendWith(MockitoExtension.class)
public class UserServiceTest {

    @Mock
    private UserMapper userMapper;

    @InjectMocks
    private UserService userService;

    private User normalUser;
    private User adminUser;

    @BeforeEach
    public void setUp() {
        // 准备测试数据
        normalUser = User.builder()
                .id(1L)
                .username("normal_user")
                .email("normal@example.com")
                .age(25)
                .status("ACTIVE")
                .createdAt(LocalDateTime.now())
                .build();

        adminUser = User.builder()
                .id(2L)
                .username("admin_user")
                .email("admin@example.com")
                .age(30)
                .status("ADMIN")
                .createdAt(LocalDateTime.now())
                .build();
    }

    // ============= 正常流程测试 =============
    
    @Test
    public void testGetUserById_Success() {
        // Given: Mock返回用户数据
        given(userMapper.selectById(1L)).willReturn(normalUser);
        
        // When: 调用Service方法
        User result = userService.getUserById(1L);
        
        // Then: 验证返回结果和Mock交互
        assertThat(result).isNotNull();
        assertThat(result.getId()).isEqualTo(1L);
        assertThat(result.getUsername()).isEqualTo("normal_user");
        
        verify(userMapper, times(1)).selectById(1L);
        verifyNoMoreInteractions(userMapper);
    }

    @Test
    public void testCreateUser_Success() {
        // Given: 新用户数据和Mock设置
        User newUser = User.builder()
                .username("new_user")
                .email("new@example.com")
                .age(28)
                .status("ACTIVE")
                .createdAt(LocalDateTime.now())
                .build();
        
        given(userMapper.insert(any(User.class))).willReturn(1);
        given(userMapper.selectByUsername("new_user")).willReturn(null);
        
        // When: 创建用户
        User result = userService.createUser(newUser);
        
        // Then: 验证用户创建成功
        assertThat(result).isNotNull();
        assertThat(result.getUsername()).isEqualTo("new_user");
        
        verify(userMapper, times(1)).selectByUsername("new_user");
        verify(userMapper, times(1)).insert(newUser);
    }

    @Test
    public void testUpdateUser_Success() {
        // Given: Mock设置
        given(userMapper.selectById(1L)).willReturn(normalUser);
        given(userMapper.update(any(User.class))).willReturn(1);
        
        User updateData = User.builder()
                .id(1L)
                .username("updated_user")
                .email("updated@example.com")
                .age(26)
                .status("INACTIVE")
                .build();
        
        // When: 更新用户
        User result = userService.updateUser(updateData);
        
        // Then: 验证更新成功
        assertThat(result).isNotNull();
        assertThat(result.getUsername()).isEqualTo("updated_user");
        assertThat(result.getStatus()).isEqualTo("INACTIVE");
        
        verify(userMapper, times(1)).selectById(1L);
        verify(userMapper, times(1)).update(updateData);
    }

    // ============= 异常测试 =============
    
    @Test
    public void testGetUserById_UserNotFound_ThrowsException() {
        // Given: Mock返回null（用户不存在）
        given(userMapper.selectById(999L)).willReturn(null);
        
        // When/Then: 验证抛出UserNotFoundException
        assertThatThrownBy(() -> userService.getUserById(999L))
                .isInstanceOf(UserNotFoundException.class)
                .hasMessage("用户不存在: 999");
        
        verify(userMapper, times(1)).selectById(999L);
    }

    @Test
    public void testCreateUser_UsernameExists_ThrowsException() {
        // Given: 用户名已存在
        User newUser = User.builder()
                .username("existing_user")
                .email("new@example.com")
                .age(28)
                .status("ACTIVE")
                .build();
        
        given(userMapper.selectByUsername("existing_user")).willReturn(normalUser);
        
        // When/Then: 验证抛出冲突异常
        assertThatThrownBy(() -> userService.createUser(newUser))
                .isInstanceOf(IllegalArgumentException.class)
                .hasMessageContaining("用户名已存在");
        
        verify(userMapper, times(1)).selectByUsername("existing_user");
        verify(userMapper, never()).insert(any(User.class));
    }

    @Test
    public void testUpdateUser_InvalidAge_ThrowsException() {
        // Given: Mock设置
        given(userMapper.selectById(1L)).willReturn(normalUser);
        
        User invalidAgeUser = User.builder()
                .id(1L)
                .username("test_user")
                .email("test@example.com")
                .age(-5)  // 无效年龄
                .status("ACTIVE")
                .build();
        
        // When/Then: 验证年龄验证失败
        assertThatThrownBy(() -> userService.updateUser(invalidAgeUser))
                .isInstanceOf(IllegalArgumentException.class)
                .hasMessageContaining("年龄必须在0-150之间");
        
        verify(userMapper, times(1)).selectById(1L);
        verify(userMapper, never()).update(any(User.class));
    }

    // ============= 边界测试 =============
    
    @Test
    public void testCreateUser_WithBoundaryValues_Success() {
        // Given: 边界值用户数据
        User boundaryUser = User.builder()
                .username("a".repeat(100))  // 最大长度用户名
                .email("boundary@example.com")
                .age(0)  // 最小年龄
                .status("ACTIVE")
                .createdAt(LocalDateTime.now())
                .build();
        
        given(userMapper.insert(any(User.class))).willReturn(1);
        given(userMapper.selectByUsername(anyString())).willReturn(null);
        
        // When: 创建边界值用户
        User result = userService.createUser(boundaryUser);
        
        // Then: 验证创建成功
        assertThat(result).isNotNull();
        assertThat(result.getUsername()).hasSize(100);
        assertThat(result.getAge()).isEqualTo(0);
        
        verify(userMapper, times(1)).selectByUsername(boundaryUser.getUsername());
        verify(userMapper, times(1)).insert(boundaryUser);
    }

    @Test
    public void testSearchUsers_WithVariousParameters() {
        // Given: Mock设置
        List<User> mockUsers = Arrays.asList(normalUser, adminUser);
        given(userMapper.searchUsers(any(), any(), any(), any()))
                .willReturn(mockUsers);
        
        // Test Case 1: 空搜索条件
        List<User> result1 = userService.searchUsers(null, null, null, null);
        assertThat(result1).hasSize(2);
        
        // Test Case 2: 只按用户名搜索
        List<User> result2 = userService.searchUsers("normal", null, null, null);
        assertThat(result2).hasSize(2);
        
        // Test Case 3: 按状态和年龄搜索
        List<User> result3 = userService.searchUsers(null, "ACTIVE", 25, null);
        assertThat(result3).hasSize(2);
        
        verify(userMapper, times(3)).searchUsers(any(), any(), any(), any());
    }

    @Test
    public void testGetUserStatistics_EmptyResult() {
        // Given: Mock返回空列表
        given(userMapper.selectAll()).willReturn(Arrays.asList());
        
        // When: 获取空数据统计
        UserService.UserStatistics statistics = userService.getUserStatistics();
        
        // Then: 验证空数据统计
        assertThat(statistics.getTotalCount()).isEqualTo(0);
        assertThat(statistics.getActiveCount()).isEqualTo(0);
        assertThat(statistics.getAverageAge()).isEqualTo(0.0);
        
        verify(userMapper, times(1)).selectAll();
    }

    @Test
    public void testBatchUpdateUsers_Success() {
        // Given: 批量更新数据
        List<Long> userIds = Arrays.asList(1L, 2L, 3L);
        String newStatus = "INACTIVE";
        
        given(userMapper.updateStatusBatch(userIds, newStatus)).willReturn(3);
        
        // When: 批量更新用户状态
        int updatedCount = userService.batchUpdateUserStatus(userIds, newStatus);
        
        // Then: 验证批量更新成功
        assertThat(updatedCount).isEqualTo(3);
        
        verify(userMapper, times(1)).updateStatusBatch(userIds, newStatus);
    }
}
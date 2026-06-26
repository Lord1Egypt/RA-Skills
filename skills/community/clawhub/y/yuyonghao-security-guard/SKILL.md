# Security Guard - OpenClaw 安全守护系统

**版本**: 0.1.0  
**功能**: 权限管理 + 内容审查 + 审计日志

## 功能特性

- **权限管理**: 基于角色的细粒度权限控制
- **内容安全**: 输入/输出内容审查
- **审计日志**: 完整操作记录和追踪
- **高风险确认**: 敏感操作人工确认

## 安装

```bash
cd skills/security-guard
npm install
```

## 快速开始

```javascript
import { SecurityGuard } from './src/security-guard.js';

// 创建安全守护实例
const guard = new SecurityGuard({
  enabled: true,
  strictMode: false,
  permissions: {
    roles: {
      admin: { permissions: ['*'] },
      user: { permissions: ['read', 'write'] },
      guest: { permissions: ['read'] }
    }
  },
  contentSafety: {
    enabled: true,
    maxInputLength: 10000,
    blockedPatterns: ['password', 'secret', 'token']
  },
  audit: {
    logDir: './audit-logs',
    bufferSize: 100
  }
});

// 执行安全检查
const result = await guard.check('user123', 'write', 'file.txt', 'content');
if (result.allowed) {
  console.log('操作允许');
} else {
  console.log('拒绝:', result.reason);
}
```

## API 参考

### SecurityGuard

#### 构造函数
```javascript
new SecurityGuard(config)
```

**参数**:
- `config.enabled` - 是否启用（默认：true）
- `config.strictMode` - 严格模式（默认：false）
- `config.permissions` - 权限配置
- `config.contentSafety` - 内容安全配置
- `config.audit` - 审计日志配置

#### check(userId, action, resource, content)
执行完整安全检查

```javascript
const result = await guard.check('user123', 'write', 'file.txt', 'some content');
// 返回: { allowed: true/false, reason: '...', checks: {...} }
```

### PermissionManager

#### checkPermission(userId, action, resource)
检查用户权限

```javascript
const result = guard.permissionManager.checkPermission('user123', 'write', 'file.txt');
// 返回: { allowed: true/false, reason: '...' }
```

### ContentSafety

#### checkInput(content)
检查输入内容

```javascript
const result = guard.contentSafety.checkInput('user input');
// 返回: { safe: true/false, warnings: [...] }
```

### AuditLogger

#### log(operation)
记录操作日志

```javascript
await guard.auditLogger.log({
  userId: 'user123',
  action: 'write',
  resource: 'file.txt',
  status: 'success'
});
```

## 配置示例

### 基础配置
```javascript
const guard = new SecurityGuard({
  enabled: true,
  permissions: {
    defaultRole: 'user',
    roles: {
      admin: { permissions: ['*'] },
      user: { permissions: ['read', 'write'] }
    }
  }
});
```

### 严格模式
```javascript
const guard = new SecurityGuard({
  enabled: true,
  strictMode: true,  // 所有操作都需要明确授权
  contentSafety: {
    enabled: true,
    blockedPatterns: ['password', 'secret', 'api_key']
  }
});
```

## 测试

```bash
npm test
```

## License

MIT

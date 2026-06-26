# Code Sandbox Skill

🔒 Secure code execution sandbox for OpenClaw agents.

## Features

- **Multi-language Support**: Node.js, Python, Go, Rust
- **Resource Limits**: Timeout, memory, CPU constraints
- **Isolation**: Temporary directories, process isolation
- **Execution History**: Track all executions with metrics
- **Safe Cleanup**: Automatic cleanup of temporary files

## Installation

```bash
# Already in workspace skills directory
cd skills/code-sandbox
npm install
```

## Usage

### JavaScript API

```javascript
const { CodeSandbox } = require('./src/sandbox');

const sandbox = new CodeSandbox({
  defaultTimeout: 30000,      // 30 seconds
  defaultMemoryLimit: 512,    // 512 MB
});

// Execute Node.js code
const result = await sandbox.execute({
  language: 'node',
  code: 'console.log("Hello World!");',
});

console.log(result);
// {
//   success: true,
//   output: "Hello World!\n",
//   error: "",
//   exitCode: 0,
//   executionTime: 45,
//   memoryUsed: 0
// }

// Execute Python code
const pythonResult = await sandbox.execute({
  language: 'python',
  code: 'print("Hello from Python!")',
  config: {
    timeout: 5000,  // 5 seconds
  }
});
```

### CLI Demo

```bash
# Run demo
npm run demo

# Run tests
npm test
```

## Supported Languages

| Language | Version | Description |
|----------|---------|-------------|
| node | 20.x | Node.js JavaScript runtime |
| python | 3.11 | Python interpreter |
| go | 1.21 | Go compiler and runtime |
| rust | 1.75 | Rust compiler (rustc) |

## Configuration

```javascript
const config = {
  defaultTimeout: 30000,      // Default timeout in ms
  defaultMemoryLimit: 512,    // Default memory limit in MB
  defaultCpuLimit: 1,         // Default CPU cores
  tmpDir: '/path/to/tmp',     // Temporary directory for execution
};

const sandbox = new CodeSandbox(config);
```

### Per-execution Config

```javascript
await sandbox.execute({
  language: 'node',
  code: '...',
  config: {
    timeout: 10000,      // Override timeout
    memoryLimit: 256,    // Override memory limit
  }
});
```

## Security Features

### Current Implementation (v0.1.0)
- ✅ Process isolation (separate processes)
- ✅ Temporary directory isolation
- ✅ Timeout enforcement
- ✅ Output buffering limits (10MB)
- ✅ Automatic cleanup

### Planned (v0.2.0+)
- ⏳ Docker containerization
- ⏳ Windows Job Objects for resource limits
- ⏳ Network isolation
- ⏳ Filesystem read-only mode
- ⏳ Seccomp profiles (Linux)
- ⏳ Dangerous operation filtering

## Execution History

```javascript
// Get last 100 executions
const history = sandbox.getHistory(100);

console.log(history);
// [
//   {
//     executionId: "exec_1710691200000_a1b2c3d4",
//     timestamp: "2026-03-17T09:00:00.000Z",
//     language: "node",
//     codeLength: 42,
//     success: true,
//     executionTime: 45,
//     memoryUsed: 0
//   },
//   ...
// ]
```

## Error Handling

```javascript
try {
  const result = await sandbox.execute({
    language: 'node',
    code: 'throw new Error("Oops!");',
  });
  
  if (!result.success) {
    console.error('Execution failed:', result.error);
  }
} catch (error) {
  console.error('Sandbox error:', error.message);
}
```

## Testing

```bash
# Run all tests
npm test

# Test specific language
node test/node-test.js
node test/python-test.js
```

## Limitations

### Current Version (v0.1.0)
- No Docker isolation (uses process-level isolation only)
- No memory limit enforcement (relies on OS)
- No network isolation
- Memory usage tracking not implemented

### Known Issues
- Windows path handling may need adjustment
- Rust/Go compilation errors could be clearer
- Large outputs may be truncated

## Roadmap

### v0.2.0 (Next Release)
- [ ] Docker containerization support
- [ ] Windows Job Objects integration
- [ ] Memory limit enforcement
- [ ] Network isolation (disable by default)

### v0.3.0
- [ ] Seccomp profiles (Linux)
- [ ] Filesystem whitelist/blacklist
- [ ] Code scanning for dangerous patterns
- [ ] Concurrent execution limits

### v0.4.0
- [ ] REST API server
- [ ] WebSocket streaming output
- [ ] Batch execution support
- [ ] Prometheus metrics

## Safety Warnings

⚠️ **This sandbox provides basic isolation but is NOT suitable for:**
- Running untrusted code from strangers
- Production environments without additional security
- Executing code that requires high security guarantees

For production use, implement:
- Docker containers with security profiles
- Network isolation
- Resource quotas
- Code scanning and validation

## License

MIT License - See LICENSE file for details

## Contributing

Contributions welcome! Please read CONTRIBUTING.md first.

---

**Version**: 0.1.0  
**Last Updated**: 2026-03-17  
**Author**: OpenClaw Team

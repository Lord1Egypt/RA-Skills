# TunnelProxy Protocol Reference

## HTTP Interface

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | List root directory (HTML) |
| GET | `/{path}` | Download file |
| POST | `/upload` | Upload file (expects raw binary body) |
** Note ** : The '/upload' endpoint expects the original binary body, and the server locates the file content by scanning the 'UPLOAD_MAGIC' magic word.
## PTY Shell Interface

- **Connection**: TCP socket
- **Protocol**: Send `command\n` (UTF-8), read output until marker
- **Session**: Stateless (new shell per connection)
- **Default Timeout**: 30 seconds

## Environment Setup

### Local TunnelProxy (Elixir)

```bash
git clone https://github.com/TurinFohlen/tunnel_proxy.git
cd tunnel_proxy
export TUNNEL_DOC_ROOT="./www"
export TUNNEL_UPLOAD_DIR="./uploads"
export UPLOAD_MAGIC="your-secret"
mix run --no-halt -e "TunnelProxy.Server.start(8080)"
```

### FRP for Public Access

```bash
./setup-frp.sh
# Output: HTTP and Shell public addresses
```

## Dependencies

### Agent Side
- Python 3.8+
- `requests`
### User Side (TunnelProxy)
- Elixir 1.12+
- Erlang/OTP 24+
- Optional: frp client

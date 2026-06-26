# Proxy Config (proxy field for create-browser / update-browser)

The **proxy** field is **required** for `create-browser`. Pass an object with the following fields:

- **protocol** (required): Proxy protocol. e.g. `"http"`, `"socks5"`, `"direct"` (no proxy)
- **host** (optional): Proxy host, e.g. `"127.0.0.1"`
- **port** (optional): Proxy port, e.g. `8080`
- **username** (optional): Proxy username
- **password** (optional): Proxy password
- **proxyId** (optional): Saved proxy id (number)
- **timezone** (optional): Timezone override for this proxy

Example (no proxy): `"proxy":{"protocol":"direct"}`

Example (HTTP proxy): `"proxy":{"protocol":"http","host":"127.0.0.1","port":8080,"username":"user","password":"pass"}`

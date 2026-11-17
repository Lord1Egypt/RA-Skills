# Web 访问日志检测规则（元察 · 元）

分析 nginx / apache 的 common / combined 访问日志。本文件说明元察的 web 检测规则与特征表，供人工复核与调参。

## 输入形态

典型行（combined）：

```
10.0.0.9 - - [05/Jan/2026:12:00:01 +0000] "GET /../../etc/passwd HTTP/1.1" 404 123 "-" "curl/7.64"
```

引擎解析来源 IP、时间、方法、URI、状态码、User-Agent。URI 会先做 URL 解码（unquote）再做特征匹配，因此 `union%20select` / `%2e%2e%2f` 也能命中。

## 检测规则

| 规则 | 触发条件 | 默认严重度 | 说明 / 复核建议 |
|---|---|---|---|
| path_traversal | URI 含 ../ 或编码变体（%2e%2e%2f、%252e 等） | high | 尝试读服务器任意文件；核查是否成功、修复路径校验与访问控制 |
| sql_injection | URI / 解码后含 union select、or 1=1、sleep(、information_schema 等 | high | 参数化查询缺失；核查对应接口与数据库日志 |
| webshell_upload | POST 到 webshell 特征路径，或路径含 cmd=/eval( | critical | 可能已上传 / 调用后门；排查文件系统、web 目录写权限、WAF 日志 |
| suspicious_ua | User-Agent 命中已知扫描 / 自动化工具特征 | low | 提示来源可能为自动化工具；结合上下文判断 |
| scanner_signature | 来源命中 3 个及以上常见管理 / 敏感路径 | medium | 自动化扫描 / 踩点；核对来源并在 WAF 层处置 |
| flood_404 | 同来源 404 次数 >= `--404-threshold`（默认 20） | medium | 目录爆破 / 扫描行为；核实来源、评估防护 |

## 特征表

### 扫描 / 探测路径片段（SCANNER_PATH）

`/wp-login.php`、`/wp-admin`、`/wp-content`、`/administrator`、`/phpmyadmin`、`/pma`、`/mysql`、`/admin`、`/login`、`/manager`、`/cgi-bin`、`/.git`、`/.env`、`/.svn`、`/.htaccess`、`/phpinfo.php`、`/phpunit`、`/actuator`、`/console`、`/backup`、`/dump`、`/test`、`/explorer`、`/vendor`、`/config`、`/server-status`、`/server-info`、`/xmlrpc.php`、`/webdav`、`/shell`、`/shell.php`、`/cmd`、`/debug`、`/xdebug` 等。

### webshell 路径片段（WEBSHELL_PATH）

`/shell.php`、`/cmd.php`、`/eval`、`/webshell`、`/backdoor`、`/c99.php`、`/r57.php`、`/wso`、`/b374k`、`/uploads/shell`、`/hack.php`、`/shell.asp`、`/shell.jsp`、`/jsp/cmd`、`/marco` 等。

### 路径遍历特征（TRAVERSAL）

`../`、`..%2f`、`..%5c`、`%2e%2e%2f`、`%2e%2e%5c`、`%252e%252e`、`..%2F`、`..%252f`、`%c0%ae%c0%ae`、`%c0%ae`、`dotdot`。

### SQL 注入特征（SQLI）

`union select`、`or 1=1`、`or 1=1--`、`1=1`、`sleep(`、`benchmark(`、`information_schema`、`@@version`、`concat(`、`group_concat`、`or '1'='1`、`union all select`、`procedure analyse`、`and 1=1`、`waitfor delay`、`pg_sleep`、`into outfile`、`xp_cmdshell`、`%27`、`'%20or%20`、`1%27` 等。

### 可疑 User-Agent（SCANNER_UA，小写匹配）

`sqlmap`、`nuclei`、`nikto`、`masscan`、`zgrab`、`nmap`、`dirbuster`、`gobuster`、`ffuf`、`wfuzz`、`wpscan`、`joomscan`、`acunetix`、`nessus`、`openvas`、`python-requests`、`go-http-client`、`python-urllib`、`curl`、`wget`、`libwww-perl`、`scrapy`、`httpclient`、`aiohttp`、`httpie`、`lwp`、`jbrofuzz`、`fuzzdb`、`censys`、`shodan`、`cobalt` 等。

## 阈值与调参

- `--404-threshold`：同来源 404 洪峰阈值（默认 20）。调低更敏感，调高更稳健。
- `--window`：聚合时间窗（秒），用于 404 洪峰与扫描聚合。

## 复核建议

- 扫描 / 遍历 / SQLi 命中需结合是否成功（状态码 2xx/4xx/5xx）与业务合理性判断；
- webshell 上传命中优先排查，确认文件系统与 web 目录写权限；
- 误报常见来源：爬虫、监控探针、健康检查、内部自动化；结合 UA 与来源比对，避免一刀切封禁。
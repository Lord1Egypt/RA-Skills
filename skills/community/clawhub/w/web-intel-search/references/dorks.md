# Dork Library

Use only against assets you own or are authorized to test. Verify every hit manually; search
indexes are often stale and may attribute third-party assets to your target.

## 1. Open directories
```
intitle:"index of" site:example.com
intitle:"index of /" "parent directory"
intitle:"index of" (backup OR bak OR old OR 2024 OR 2025)
intitle:"index of" inurl:ftp
intitle:"index of" (mp4 OR avi OR mkv OR mp3)
intitle:"index of" "database" (sql OR dump OR bak)
intitle:"index of" ".git"
intitle:"index of" ".env"
intitle:"index of" "wp-content/uploads"
```

## 2. Exposed documents and files
```
site:example.com filetype:pdf
site:example.com (filetype:xlsx OR filetype:xls OR filetype:csv)
site:example.com (filetype:docx OR filetype:doc OR filetype:pptx)
site:example.com filetype:sql
site:example.com filetype:log
site:example.com filetype:bak
site:example.com filetype:env
site:example.com filetype:ini
site:example.com filetype:conf
site:example.com filetype:yml OR filetype:yaml
site:example.com filetype:pem OR filetype:key
site:example.com filetype:ovpn
site:example.com filetype:kdbx
filetype:pdf "confidential" site:example.com
filetype:xlsx "password" site:example.com
filetype:csv "email" site:example.com
filetype:sql "INSERT INTO" site:example.com
filetype:log "password" site:example.com
filetype:env "DB_PASSWORD" OR "SECRET_KEY"
filetype:pem "BEGIN RSA PRIVATE KEY"
filetype:pem "BEGIN OPENSSH PRIVATE KEY"
filetype:p12 OR filetype:pfx OR filetype:jks
filetype:ovpn "client"
filetype:rdp
filetype:mobileconfig
```

## 3. Login panels and admin interfaces
```
site:example.com inurl:admin
site:example.com inurl:login
site:example.com inurl:dashboard
site:example.com inurl:wp-admin
site:example.com inurl:wp-login.php
site:example.com inurl:phpmyadmin
site:example.com inurl:adminer.php
site:example.com inurl:cpanel
site:example.com inurl:webmail
site:example.com inurl:jenkins
site:example.com inurl:jira
site:example.com inurl:gitlab
site:example.com inurl:grafana
site:example.com inurl:kibana
site:example.com inurl:portainer
site:example.com inurl:swagger
site:example.com inurl:api-docs
site:example.com intitle:"Admin Panel"
site:example.com intitle:"Login" inurl:admin
site:example.com inurl:login intitle:"username" "password"
intitle:"Webmin" inurl:10000
intitle:"Plesk" inurl:login
intitle:"phpinfo()" inurl:phpinfo.php
```

## 4. Cloud storage and buckets
```
site:s3.amazonaws.com "example"
site:*.s3.amazonaws.com "example"
site:storage.googleapis.com "example"
site:blob.core.windows.net "example"
site:*.blob.core.windows.net "example"
site:digitaloceanspaces.com "example"
site:*.r2.cloudflarestorage.com
site:s3.amazonaws.com intitle:"index of"
site:storage.googleapis.com intitle:"index of"
intitle:"<ListBucketResult>"
inurl:"s3.amazonaws.com" "example"
intext:"AWSAccessKeyId"
intext:"X-Amz-Signature"
```

## 5. Cameras, IoT, and exposed services
```
intitle:"Live View / - AXIS"
inurl:axis-cgi/mjpg
inurl:ViewerFrame?Mode=
intitle:"Network Camera" inurl:axis
intitle:"IP Camera" inurl:LvAppl
intitle:"webcam" inurl:view
intitle:"GeoVision" inurl:serverpage
inurl:/mjpg/video.mjpg
intitle:"DVR" inurl:login
inurl:8080 intitle:"camera"
intitle:"RouterOS" inurl:webfig
intitle:"MikroTik" inurl:login
intitle:"TP-Link" inurl:login
inurl:8443 intitle:"UniFi"
intitle:"Kibana" inurl:5601
intitle:"Elastic" inurl:9200
intitle:"MongoDB" inurl:27017
intitle:"Redis" inurl:6379
intitle:"Apache Tomcat" inurl:manager
intitle:"Jenkins" inurl:login
intitle:"Grafana" inurl:login
intitle:"Jupyter" inurl:tree
intitle:"SonarQube" inurl:login
```

## 6. Credentials, secrets, configs
```
site:example.com intext:"api_key"
site:example.com intext:"apikey"
site:example.com intext:"access_token"
site:example.com intext:"secret_key"
site:example.com intext:"password="
site:example.com intext:"DB_PASSWORD"
site:example.com intext:"aws_access_key_id"
site:example.com intext:"aws_secret_access_key"
site:example.com intext:"BEGIN RSA PRIVATE KEY"
site:example.com intext:"mongodb://"
site:example.com intext:"mysql://"
site:example.com intext:"postgres://"
site:example.com intext:"redis://"
site:example.com intext:"smtp://"
site:example.com intext:"Bearer "
site:example.com intext:"Authorization: Basic"
site:github.com "example.com" password
site:github.com "example.com" "api_key"
site:gitlab.com "example.com" "secret"
inurl:config intext:"password"
inurl:.env intext:"DB_"
filetype:json intext:"api_key"
```

## 7. Paste and leak sites
```
site:pastebin.com "example.com"
site:pastebin.com "password" "@example.com"
site:pastebin.com "BEGIN RSA PRIVATE KEY"
site:pastebin.com "aws_secret_access_key"
site:pastebin.com "mongodb://"
site:paste.ee "example.com"
site:justpaste.it "example.com"
site:ghostbin.com "example.com"
site:rentry.co "example.com"
site:hastebin.com "example.com"
site:dpaste.org "example.com"
site:controlc.com "example.com"
site:0bin.net "example.com"
site:ideone.com "example.com"
```

## 8. Subdomains and infrastructure
```
site:*.example.com -www
site:*.example.com -www -mail
site:*.example.com inurl:api
site:*.example.com intitle:"dashboard"
site:*.example.com inurl:dev OR inurl:staging OR inurl:test
site:*.example.com inurl:vpn OR inurl:remote
site:example.com inurl:jenkins
site:example.com inurl:gitlab
site:example.com inurl:jira
site:example.com inurl:confluence
site:example.com inurl:grafana
site:example.com inurl:kibana
site:example.com inurl:prometheus
site:example.com inurl:swagger
site:example.com inurl:actuator
site:example.com inurl:.well-known
site:example.com inurl:server-status
site:example.com intitle:"Test Page for Apache"
site:example.com intitle:"Welcome to nginx"
```

## 9. Company and employee intelligence
```
site:linkedin.com/in "Example Inc"
site:linkedin.com/company "Example Inc"
site:linkedin.com/jobs "Example Inc"
site:glassdoor.com "Example Inc"
site:crunchbase.com "Example Inc"
site:opencorporates.com "Example Inc"
site:sec.gov "Example Inc"
site:github.com "Example Inc"
site:twitter.com "Example Inc"
"@example.com" filetype:xlsx
"@example.com" filetype:csv
"@example.com" site:pastebin.com
site:example.com inurl:team OR inurl:staff OR inurl:about
site:example.com inurl:careers OR inurl:jobs
"Example Inc" filetype:pdf "employee directory"
```

## 10. Vulnerable endpoints and tech fingerprints
```
inurl:struts2 filetype:action
intitle:"Powered by Apache" inurl:server-status
intitle:"phpinfo()" inurl:phpinfo.php
intext:"SQL syntax" OR intext:"mysql_fetch_array"
intext:"Warning: mysqli_" OR intext:"Warning: pg_"
intitle:"Test Page for Apache" inurl:apache2
inurl:wp-content/plugins filetype:php "Changelog"
intitle:"Drupal" inurl:CHANGELOG.txt
inurl:elmah.axd intext:"Error Log"
inurl:actuator/env
inurl:actuator/heapdump
inurl:swagger-ui.html
inurl:v2/api-docs
inurl:graphql
inurl:.git/config
inurl:.svn/entries
inurl:WEB-INF/web.xml
inurl:META-INF/MANIFEST.MF
inurl:crossdomain.xml
inurl:clientaccesspolicy.xml
```

## 11. GitHub dorks
```
org:example filename:.env
org:example filename:.env.*
org:example filename:.npmrc
org:example filename:.git-credentials
org:example filename:id_rsa
org:example filename:config.json "password"
org:example "AKIA"
org:example "ASIA"
org:example "AIza"
org:example "sk_live_"
org:example "ghp_"
org:example "xoxb-"
org:example "BEGIN RSA PRIVATE KEY"
org:example "BEGIN OPENSSH PRIVATE KEY"
org:example path:.github/workflows "secrets."
org:example path:.github/workflows "aws-access-key-id"
org:example extension:sql "INSERT INTO"
org:example extension:pem
org:example extension:p12
org:example "mongodb://"
org:example "postgres://"
org:example "redis://"
org:example "-----BEGIN CERTIFICATE-----"
org:example "internal.example.com"
org:example "staging.example.com"
org:example "TODO" "password"
org:example "FIXME" "secret"
```
Also search `user:`, `repo:`, `language:`, `path:`, `filename:`, `extension:` and `in:file`
qualifiers. Search forks and archived repos; secrets often survive in history. Use gitleaks and
trufflehog on cloned repos (authorized only).

## 12. Shodan dorks
```
org:"Example Inc"
ssl:"example.com"
ssl.cert.subject.CN:"example.com"
http.favicon.hash:-1234567890
http.title:"Login" country:VN
http.title:"admin" org:"Example Inc"
product:"Elasticsearch" port:9200
product:"MongoDB" port:27017
product:"Redis" port:6379
product:"Memcached" port:11211
product:"Apache Tomcat" port:8080
port:3389 org:"Example Inc"
port:445 org:"Example Inc"
port:22 org:"Example Inc"
port:5900 org:"Example Inc"
port:1433 org:"Example Inc"
port:3306 org:"Example Inc"
port:5432 org:"Example Inc"
http.component:"WordPress" org:"Example Inc"
vuln:CVE-2024-3400
has_vuln:true org:"Example Inc"
tag:ics country:VN
device:webcam country:VN
```

## 13. FOFA dorks
```
domain="example.com"
app="Apache" && country="VN"
app="ThinkPHP" && country="VN"
app="Nginx" && port="443"
title="后台管理" && country="VN"
body="phpinfo" && domain="example.com"
header="thinkphp"
cert="example.com"
icon_hash="123456789"
server="nginx" && domain="example.com"
protocol="rdp" && country="VN"
port="27017" && country="VN"
```

## 14. ZoomEye dorks
```
app:nginx country:VN
app:"Apache Tomcat" port:8080
device:router country:VN
title:"admin" country:VN
service:rdp country:VN
ssl:"example.com"
cert:"Example Inc"
iconhash:123456789
domain:example.com
subdomain:dev.example.com
```

## 15. Negation and refinement patterns
```
site:*.example.com -www -mail -smtp
site:example.com filetype:pdf -inurl:privacy -inurl:terms
inurl:admin -site:wordpress.org -site:github.com
intext:"internal use only" -site:news.google.com
filetype:env -site:github.com -site:gitlab.com
intitle:"index of" -inurl:wp-content
"password" filetype:log -site:github.com
```

## 16. Time-constrained dorks
```
site:example.com after:2025-01-01
site:pastebin.com "example.com" after:2025-06-01
"example.com" breach after:2024-01-01
inurl:admin after:2025-01-01
site:github.com "example.com" pushed:>2025-01-01
```

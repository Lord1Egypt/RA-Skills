# Ignore 文件模式参考

## 通用模式
```
.DS_Store
Thumbs.db
*.tmp
*.swp
.vscode/
.idea/
```

## 技术栈特定模式

### Node.js/JavaScript/TypeScript
```
node_modules/
dist/
build/
*.log
.env*
```

### Python
```
__pycache__/
*.pyc
.venv/
venv/
dist/
*.egg-info/
```

### Java
```
target/
*.class
*.jar
.gradle/
build/
```

### C#/.NET
```
bin/
obj/
*.user
*.suo
packages/
```

### Go
```
*.exe
*.test
vendor/
*.out
```

### Ruby
```
.bundle/
log/
tmp/
*.gem
vendor/bundle/
```

### PHP
```
vendor/
*.log
*.cache
*.env
```

### Rust
```
target/
debug/
release/
*.rs.bk
*.rlib
*.prof*
.idea/
*.log
.env*
```

### Kotlin
```
build/
out/
.gradle/
.idea/
*.class
*.jar
*.iml
*.log
.env*
```

### C++
```
build/
bin/
obj/
out/
*.o
*.so
*.a
*.exe
*.dll
.idea/
*.log
.env*
```

### C
```
build/
bin/
obj/
out/
*.o
*.a
*.so
*.exe
Makefile
config.log
.idea/
*.log
.env*
```

### Swift
```
.build/
DerivedData/
*.swiftpm/
Packages/
```

### R
```
.Rproj.user/
.Rhistory
.RData
.Ruserdata
*.Rproj
packrat/
renv/
```

## 工具特定模式

### Docker
```
node_modules/
.git/
Dockerfile*
.dockerignore
*.log*
.env*
coverage/
```

### ESLint
```
node_modules/
dist/
build/
coverage/
*.min.js
```

### Prettier
```
node_modules/
dist/
build/
coverage/
package-lock.json
yarn.lock
pnpm-lock.yaml
```

### Terraform
```
.terraform/
*.tfstate*
*.tfvars
.terraform.lock.hcl
```

### Kubernetes/k8s
```
*.secret.yaml
secrets/
.kube/
kubeconfig*
*.key
*.crt
```
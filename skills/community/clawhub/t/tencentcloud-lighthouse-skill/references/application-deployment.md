# Application Deployment

Deploy applications to Lighthouse instances and verify successful deployment.

## Pre-deployment Checklist

Before deploying, gather information about the application:

1. **Instance readiness** — Verify the target instance is running
2. **Environment** — Check OS, runtime, and dependencies
3. **Application type** — Identify how the app starts and validates

## Step 1: Research Application Startup

Ask the user or analyze the application to determine:

| Question | Why it matters |
|----------|----------------|
| What type of application? | Node.js, Python, Java, Go, Docker, etc. |
| How to start the app? | Command like `npm start`, `python app.py`, `java -jar app.jar` |
| What port does it listen on? | Need to open firewall and verify access |
| Does it need a database? | May need to set up MySQL, Redis, etc. |
| Any environment variables? | Config like `NODE_ENV`, `DATABASE_URL` |
| How to verify it's running? | Health check endpoint, process name, log file |

### Common Application Types

```bash
# Check what's installed on the instance
tccli tat RunCommand --region <region> \
  --InstanceIds '["lhins-xxx"]' \
  --Content "which node python java docker && docker --version 2>/dev/null && node --version 2>/dev/null && python3 --version 2>/dev/null"
```

## Step 2: Prepare the Environment

```bash
# Install runtime if needed (example: Node.js)
tccli tat RunCommand --region <region> \
  --InstanceIds '["lhins-xxx"]' \
  --Content "curl -fsSL https://rpm.nodesource.com/setup_18.x | sudo bash - && sudo yum install -y nodejs"

# Or for Docker-based deployment
tccli tat RunCommand --region <region> \
  --InstanceIds '["lhins-xxx"]' \
  --Content "sudo yum install -y docker && sudo systemctl start docker && sudo systemctl enable docker"
```

## Step 3: Deploy the Application

### Option A: Git Clone + Build

```bash
# Clone repository
tccli tat RunCommand --region <region> \
  --InstanceIds '["lhins-xxx"]' \
  --Content "cd /opt && sudo git clone <repo-url> myapp && sudo chown -R lighthouse:lighthouse myapp"

# Install dependencies and build
tccli tat RunCommand --region <region> \
  --InstanceIds '["lhins-xxx"]' \
  --Content "cd /opt/myapp && npm install && npm run build" \
  --Timeout 300

# Start the application
tccli tat RunCommand --region <region> \
  --InstanceIds '["lhins-xxx"]' \
  --Content "cd /opt/myapp && nohup npm start > /var/log/myapp.log 2>&1 &"
```

### Option B: Docker Deployment

```bash
# Pull and run container
tccli tat RunCommand --region <region> \
  --InstanceIds '["lhins-xxx"]' \
  --Content "sudo docker run -d --name myapp -p 3000:3000 --restart always <image-name>"
```

### Option C: Upload Files + Run

For custom deployments, ask the user to provide files or commands.

## Step 4: Open Firewall Ports

```bash
# Open the application port (e.g., 3000)
tccli lighthouse CreateFirewallRules --region <region> \
  --InstanceId lhins-xxx \
  --FirewallRules '[{"Protocol":"TCP","Port":"3000","CidrBlock":"0.0.0.0/0","Action":"ACCEPT","FirewallRuleDescription":"App port"}]'
```

## Step 5: Verify Deployment

### Check Process Status

```bash
tccli tat RunCommand --region <region> \
  --InstanceIds '["lhins-xxx"]' \
  --Content "ps aux | grep -E 'node|python|java|myapp' | grep -v grep"
```

### Check Port Listening

```bash
tccli tat RunCommand --region <region> \
  --InstanceIds '["lhins-xxx"]' \
  --Content "ss -tlnp | grep -E '3000|8080|80' || netstat -tlnp | grep -E '3000|8080|80'"
```

### Check Application Logs

```bash
tccli tat RunCommand --region <region> \
  --InstanceIds '["lhins-xxx"]' \
  --Content "tail -50 /var/log/myapp.log || journalctl -u myapp -n 50"
```

### HTTP Health Check (from instance)

```bash
tccli tat RunCommand --region <region> \
  --InstanceIds '["lhins-xxx"]' \
  --Content "curl -s -o /dev/null -w '%{http_code}' http://localhost:3000/health || curl -s -o /dev/null -w '%{http_code}' http://localhost:3000/"
```

### Docker Container Status

```bash
tccli tat RunCommand --region <region> \
  --InstanceIds '["lhins-xxx"]' \
  --Content "sudo docker ps -a | grep myapp"
```

## Deployment Verification Checklist

| Check | Command | Expected Result |
|-------|---------|-----------------|
| Process running | `ps aux \| grep <app>` | Shows app process |
| Port listening | `ss -tlnp \| grep <port>` | Shows port in LISTEN |
| No errors in logs | `tail /var/log/myapp.log` | No error messages |
| HTTP responds | `curl localhost:<port>` | Returns 200 or expected response |
| External access | Open in browser | Page loads correctly |

## Common Startup Commands by Type

| Application Type | Start Command |
|------------------|---------------|
| Node.js (npm) | `npm start` or `node index.js` |
| Node.js (PM2) | `pm2 start app.js --name myapp` |
| Python (Flask) | `flask run --host=0.0.0.0` |
| Python (Gunicorn) | `gunicorn -b 0.0.0.0:8000 app:app` |
| Python (uvicorn) | `uvicorn main:app --host 0.0.0.0 --port 8000` |
| Java Spring Boot | `java -jar app.jar` |
| Go | `./myapp` |
| Docker | `docker run -d -p <port>:<port> <image>` |

## Workflow

1. **Research** — Ask user about app type, port, startup command, dependencies
2. **Prepare** — Install runtime, clone/upload code, install dependencies
3. **Configure** — Set environment variables, open firewall ports
4. **Start** — Run the application startup command
5. **Verify** — Check process, port, logs, and HTTP response
6. **Report** — Tell user the public IP and access URL

> Always verify each step before proceeding to the next. If a command fails, check logs and ask the user for clarification.

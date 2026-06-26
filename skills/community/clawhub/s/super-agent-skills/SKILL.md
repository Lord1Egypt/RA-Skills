---
name: super-agent-skills
version: 1.0.0
description: Comprehensive AI Agent capability library covering 20+ essential skills from file ops to cloud services, security, monitoring, and CI/CD.
license: MIT-0
author: saqierma-cyber
tags:
  - agent
  - skills
  - capability
  - devops
  - security
  - cloud
---

# 🧠 Super Agent Skills / 超级Agent能力库

Build a fully capable AI Agent with 20+ essential skills covering file operations, networking, databases, cloud services, security, and more.

## Core Principle

A powerful AI Agent needs a comprehensive skill set to handle any task autonomously.

---

## I. Foundation Skills

### 1. File Operations
- **Tools**: File Manager, File Reader, File Writer
- **Check**: `ls -la ~/skills/`

### 2. HTTP Requests
- **Tools**: curl, wget, httpie
- **Check**: `which curl && curl --version`
- **Usage**:
```bash
curl -sS "https://api.example.com/data"
curl -X POST -H "Content-Type: application/json" -d '{"key":"value"}' URL
```

### 3. Scheduled Tasks
- **Tools**: at, cron, schedule
- **Use case**: Delayed execution, reminders
```bash
echo "echo 'reminder' >> ~/reminder.txt" | at now + 30 seconds
```

### 4. Code Execution
- **Tools**: python, node, bash
- **Best practice**: Use virtual environments, handle exceptions

### 5. Image Generation
- **Tools**: DALL-E, Midjourney, Stable Diffusion API

### 6. Document Generation
- **Tools**: python-pptx, python-docx, markdown, weasyprint

---

## II. Advanced Skills

### 7. API Integration
- REST API, GraphQL, Webhook
- Auth, error handling, retry mechanisms

### 8. Database Operations
- **Tools**: sqlite3, pymysql, redis-cli
- SQL execution, NoSQL, ORM patterns

### 9. Cloud Services
- **Platforms**: AWS, Alibaba Cloud, GCP
- ECS/EC2, S3/OSS, SLB/ALB

### 10. Message Queues
- RabbitMQ, Kafka, Redis Pub/Sub
- Async tasks, event-driven architecture

### 11. Containerization
```bash
docker build -t myapp .
docker run -d myapp
kubectl apply -f deployment.yaml
```

### 12. CI/CD
- GitHub Actions, GitLab CI, Jenkins
- Build → Test → Deploy pipeline

---

## III. Security Skills

### 13. Authentication
- OAuth2, JWT, API Key management
- Secret storage via environment variables

### 14. Encryption
- **Tools**: openssl, gpg, python-cryptography

### 15. Security Scanning
- **Tools**: OWASP ZAP, Bandit, SonarQube
- Code audit, vulnerability scanning

---

## IV. Efficiency Skills

### 16. Parallel Processing
- asyncio, multiprocessing, threading

### 17. Caching
- Redis, Memcached (LRU, TTL strategies)

### 18. Logging
- ELK Stack, Loki, CloudWatch Logs

### 19. Monitoring & Alerting
- Prometheus, Grafana, PagerDuty

### 20. Backup & Recovery
- rsync, borg, duplicity
- Full + incremental backup strategies

---

## Quick Environment Check

```bash
which python3 && python3 --version
which node && node --version
which git && git --version
which docker && docker --version
which curl && curl --version
uname -a
```

---

## Task Execution Best Practices

1. **Receive** — Understand requirements, confirm parameters, plan execution
2. **Execute** — Log steps, preserve evidence, handle exceptions
3. **Complete** — Output results, provide logs, suggest next steps

---

## Summary

**Core Capability = Foundation Tools + Security Awareness + Best Practices**

Regularly inventory your skills to stay current!

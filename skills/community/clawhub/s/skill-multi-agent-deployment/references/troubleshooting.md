# Troubleshooting Multi-Agent Deployment

## Quick Reference Guide

### Symptoms and Immediate Actions

| Symptom | Immediate Action | Likely Cause |
|---------|-----------------|--------------|
| Agents not responding | Check agent status with `openclaw agents list` | Agent process crashed, configuration error |
| Messages not routed | Verify routing configuration | Routing rules misconfigured, coordinator agent down |
| Shared memory errors | Check shared memory directory permissions | Permission issues, disk full, JSON corruption |
| High latency | Monitor agent utilization | Resource constraints, network latency, blocking operations |
| Inter-agent communication failures | Test basic message passing | Event bus issues, message format errors |

## Detailed Troubleshooting

### 1. Agent Startup Issues

#### Agent fails to start
**Symptoms:**
- Agent process exits immediately
- Error messages in gateway logs
- Agent not appearing in `agents list`

**Diagnosis steps:**
1. Check agent workspace permissions:
   ```bash
   ls -la /data/.openclaw/agents/<agent-name>/
   ```
   
2. Verify agent configuration:
   ```bash
   cat /data/.openclaw/agents/<agent-name>/SOUL.md | head -20
   ```

3. Check gateway logs for agent-specific errors:
   ```bash
   journalctl -u openclaw-gateway --since "5 minutes ago" | grep -i <agent-name>
   ```

**Common solutions:**
- **Permission denied**: Ensure agent directories are readable/writable by OpenClaw user
- **Missing dependencies**: Verify all required skills are installed
- **Configuration syntax error**: Check JSON/YAML syntax in agent configuration
- **Port conflicts**: Change port if another service is using it

#### Agent starts but immediately crashes
**Symptoms:**
- Agent appears briefly then disappears
- High CPU/memory usage before crash
- Core dumps or crash reports

**Diagnosis:**
1. Check system resource limits:
   ```bash
   ulimit -a
   ```

2. Review agent memory configuration:
   ```bash
   grep -i memory ~/.openclaw/config.json
   ```

3. Examine crash logs:
   ```bash
   find /var/log -name "*core*" -o -name "*crash*" -mtime -1
   ```

**Solutions:**
- Increase memory limits for agent
- Reduce agent concurrency settings
- Update to latest OpenClaw version
- Simplify agent SOUL.md to reduce context size

### 2. Routing Problems

#### Messages routed to wrong agent
**Symptoms:**
- Requests handled by incorrect specialist
- Coordinator making poor routing decisions
- User receiving irrelevant responses

**Diagnosis:**
1. Test routing rules individually:
   ```python
   # Use routing_config.py test mode
   python scripts/routing_config.py --test "research request about market trends"
   ```

2. Check request matching patterns:
   ```bash
   grep -A5 -B5 "match" ~/.openclaw/config.json
   ```

3. Review coordinator agent decision logs:
   ```bash
   tail -f /data/.openclaw/agents/coordinator/memory/routing_logs.md
   ```

**Solutions:**
- Refine routing rule patterns
- Add negative match patterns (exclude certain phrases)
- Implement confidence scoring in coordinator
- Add user feedback loop for routing quality

#### Messages not routed at all
**Symptoms:**
- Requests timeout with no response
- Messages stuck in queue
- Coordinator not processing incoming messages

**Diagnosis:**
1. Verify coordinator agent is running:
   ```bash
   openclaw agents list | grep coordinator
   ```

2. Check message queue status:
   ```bash
   openclaw gateway status --queues
   ```

3. Test direct agent communication:
   ```bash
   # Send test message directly to agent
   echo "test" | openclaw agent send --agent research
   ```

**Solutions:**
- Restart coordinator agent
- Clear stuck message queues
- Increase coordinator agent resources
- Check for infinite loops in coordinator logic

### 3. Shared Memory Issues

#### Data corruption in shared memory
**Symptoms:**
- JSON parsing errors
- Missing or truncated data
- Agents receiving garbled information

**Diagnosis:**
1. Check shared memory file integrity:
   ```bash
   python -m json.tool /data/.openclaw/shared_memory/shared_data.json
   ```

2. Verify file locking is working:
   ```bash
   lsof /data/.openclaw/shared_memory/.lock 2>/dev/null
   ```

3. Monitor concurrent access patterns:
   ```bash
   tail -f /data/.openclaw/shared_memory/events/*.jsonl
   ```

**Solutions:**
- Implement atomic write operations
- Add data validation before writing
- Use database instead of file system for high concurrency
- Implement backup and restore procedures

#### Performance bottlenecks
**Symptoms:**
- High latency on memory operations
- Agents waiting for memory access
- System slowdown during peak usage

**Diagnosis:**
1. Measure read/write latency:
   ```bash
   time python scripts/memory_sync.py --read "coordinator:test_key"
   ```

2. Check disk I/O performance:
   ```bash
   iostat -x 1 10
   ```

3. Monitor lock contention:
   ```bash
   inotifywait -m /data/.openclaw/shared_memory/.lock
   ```

**Solutions:**
- Implement memory caching layer
- Use separate files for different data types
- Implement read replicas for frequently accessed data
- Move to in-memory database (Redis) for production

### 4. Inter-Agent Communication Failures

#### Event bus not delivering messages
**Symptoms:**
- Agents unaware of system events
- Tasks not progressing through workflow
- Stale information in agent memory

**Diagnosis:**
1. Test event bus connectivity:
   ```bash
   python -c "import redis; r=redis.Redis(); print(r.ping())"
   ```

2. Check event subscription status:
   ```bash
   ps aux | grep -i "event.*bus\|redis\|nats"
   ```

3. Monitor event publication:
   ```bash
   tail -f /data/.openclaw/shared_memory/events/system_events.jsonl
   ```

**Solutions:**
- Restart event bus service
- Verify network connectivity between agents
- Implement dead letter queue for undelivered events
- Add event delivery confirmation

#### Message format incompatibility
**Symptoms:**
- Messages rejected by receiving agent
- Parse errors in agent logs
- Missing message fields causing errors

**Diagnosis:**
1. Compare message schemas:
   ```bash
   diff /data/.openclaw/agents/researcher/message_schema.json \
        /data/.openclaw/agents/builder/message_schema.json
   ```

2. Test message serialization/deserialization:
   ```python
   import json
   msg = '{"type": "task", "data": {"id": "test"}}'
   json.loads(msg)  # Should not raise exception
   ```

**Solutions:**
- Implement schema validation
- Add message versioning
- Provide backward compatibility
- Document message format requirements

### 5. Performance Issues

#### High system resource usage
**Symptoms:**
- Slow response times
- High CPU/memory utilization
- Disk I/O saturation

**Diagnosis:**
1. Identify resource bottlenecks:
   ```bash
   top -b -n 1 | head -20
   ```

2. Check agent-specific resource usage:
   ```bash
   ps aux | grep "openclaw.*agent" | sort -nrk 3,3 | head -10
   ```

3. Monitor network connections:
   ```bash
   netstat -tulpn | grep openclaw
   ```

**Solutions:**
- Implement resource limits per agent
- Add request throttling
- Optimize shared memory access patterns
- Scale horizontally (add more agents/nodes)

#### Memory leaks
**Symptoms:**
- Steady increase in memory usage
- System slowdown over time
- Agent crashes after extended runtime

**Diagnosis:**
1. Track memory usage over time:
   ```bash
   watch -n 60 'ps -eo pid,cmd,%mem --sort=-%mem | grep openclaw'
   ```

2. Check for memory leaks in scripts:
   ```bash
   valgrind --leak-check=full python scripts/memory_sync.py --test
   ```

3. Monitor garbage collection (if applicable):
   ```bash
   python -c "import gc; print(gc.get_stats())"
   ```

**Solutions:**
- Implement memory usage monitoring
- Add automatic agent restart thresholds
- Fix memory leaks in custom scripts
- Increase system swap space

### 6. Deployment Problems

#### Cloud deployment failures
**Symptoms:**
- Deployment scripts fail
- Cloud resources not created
- Configuration not applied

**Diagnosis:**
1. Check cloud provider credentials:
   ```bash
   doctl auth list  # DigitalOcean
   aws sts get-caller-identity  # AWS
   ```

2. Verify resource quotas:
   ```bash
   doctl compute limits  # DigitalOcean
   ```

3. Review deployment logs:
   ```bash
   cat deployments/deployment.log | tail -50
   ```

**Solutions:**
- Update cloud provider CLI tools
- Increase resource quotas if needed
- Fix deployment script syntax errors
- Test deployment in staging environment first

#### Configuration drift
**Symptoms:**
- Different behavior across environments
- Manual changes overwritten
- Inconsistent agent behavior

**Diagnosis:**
1. Compare configurations:
   ```bash
   diff ~/.openclaw/config.json deployments/config.json
   ```

2. Check for manual modifications:
   ```bash
   find /data/.openclaw -name "*.json" -exec md5sum {} \;
   ```

**Solutions:**
- Implement configuration management
- Use version control for configurations
- Automate configuration deployment
- Add configuration validation

## Recovery Procedures

### Complete System Failure

**Step 1: Stop all agents**
```bash
openclaw gateway stop
pkill -f "openclaw.*agent"
```

**Step 2: Backup critical data**
```bash
tar czf /backup/openclaw-recovery-$(date +%Y%m%d).tar.gz \
  /data/.openclaw/agents \
  /data/.openclaw/shared_memory \
  /data/.openclaw/config.json
```

**Step 3: Restore from known good state**
```bash
# Restore configuration
cp /backup/openclaw-config-backup.json ~/.openclaw/config.json

# Restart gateway
openclaw gateway start

# Start agents one by one
openclaw agent start coordinator
sleep 5
openclaw agent start research
# ... etc
```

**Step 4: Verify recovery**
```bash
openclaw agents list
openclaw gateway status
python scripts/memory_sync.py --stats
```

### Data Corruption Recovery

**For shared memory corruption:**
```bash
# Stop all agents
openclaw gateway stop

# Backup corrupted data
cp /data/.openclaw/shared_memory/shared_data.json \
   /data/.openclaw/shared_memory/shared_data.json.corrupted.$(date +%s)

# Restore from backup or rebuild
if [ -f /backup/shared_data.json.backup ]; then
  cp /backup/shared_data.json.backup /data/.openclaw/shared_memory/shared_data.json
else
  # Reinitialize shared memory
  rm -rf /data/.openclaw/shared_memory/*
  python scripts/memory_sync.py --init --path /data/.openclaw/shared_memory
fi

# Restart system
openclaw gateway start
```

### Agent-Specific Recovery

**For individual agent failure:**
```bash
# Stop the problematic agent
openclaw agent stop <agent-name>

# Backup agent workspace
tar czf /backup/agent-<agent-name>-$(date +%Y%m%d).tar.gz \
  /data/.openclaw/agents/<agent-name>

# Reset agent state (optional)
rm -rf /data/.openclaw/agents/<agent-name>/memory/*
rm -rf /data/.openclaw/agents/<agent-name>/workspace/temp/*

# Restart agent
openclaw agent start <agent-name>

# Test agent functionality
echo "test request" | openclaw agent send --agent <agent-name>
```

## Prevention Best Practices

### 1. Regular Monitoring
- Set up alerts for critical metrics
- Implement health checks for all agents
- Monitor shared memory usage and performance
- Track error rates and response times

### 2. Automated Testing
- Test agent coordination regularly
- Validate shared memory operations
- Simulate failure scenarios
- Test recovery procedures

### 3. Documentation
- Keep troubleshooting guide updated
- Document all configuration changes
- Maintain known issues list
- Share lessons learned across team

### 4. Capacity Planning
- Monitor resource usage trends
- Plan for scaling before reaching limits
- Implement auto-scaling where possible
- Regular performance testing

### 5. Security
- Regular security audits
- Monitor for unusual activity
- Keep all components updated
- Implement principle of least privilege

## Getting Help

### Internal Resources
1. Check OpenClaw documentation: `openclaw --help`
2. Review agent logs: `/data/.openclaw/agents/*/logs/`
3. Examine gateway logs: `journalctl -u openclaw-gateway`

### External Resources
1. OpenClaw community forums
2. GitHub issues for specific components
3. Cloud provider support for deployment issues

### When to Escalate
- Data loss or corruption
- Security breach suspected
- System unavailable for extended period
- Multiple agents failing simultaneously

**Remember:** Always backup before making significant changes. Test recovery procedures regularly. Document all troubleshooting steps for future reference.
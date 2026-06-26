#!/bin/bash
# ============================================
# INCIDENT TRIGGERS — Run one at a time
# ============================================

case "${1:-help}" in

# ============================================
# INCIDENT 1: OOM KILL on payment-processor
# What happens: payment-processor gets replaced with
# a memory-hungry version that immediately OOM-kills.
# Looks real: "payment processor started consuming too
# much memory after the latest deploy"
# ============================================
trigger1)
  echo "💥 INCIDENT 1: Triggering OOM Kill on payment-processor..."
  echo "   (Simulates: bad deploy that leaks memory)"
  echo ""

  # Replace the healthy payment-processor with a memory hog
  kubectl apply -f - <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: payment-processor
  namespace: production
  labels:
    app: payment-processor
    tier: backend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: payment-processor
  template:
    metadata:
      labels:
        app: payment-processor
        tier: backend
    spec:
      containers:
      - name: app
        image: polinux/stress
        command: ["stress"]
        args: ["--vm", "1", "--vm-bytes", "200M", "--vm-hang", "1"]
        resources:
          requests:
            memory: "64Mi"
            cpu: "50m"
          limits:
            memory: "128Mi"
            cpu: "100m"
EOF

  echo "⏳ Waiting for pods to crash..."
  sleep 15
  echo ""
  echo "Current state:"
  kubectl get pods -n production -l app=payment-processor
  echo ""
  echo "Events:"
  kubectl get events -n production --field-selector=involvedObject.name!=healthy --sort-by='.lastTimestamp' | grep -i "oom\|kill\|back-off\|crash" | tail -5
  echo ""
  echo "🔴 payment-processor should be in CrashLoopBackOff"
  echo ""
  echo "NOW TELL YOUR AGENT:"
  echo '  "Something is wrong with the payment processor in production. Can you check?"'
  ;;

# ============================================
# INCIDENT 2: BAD DEPLOY on user-service
# What happens: user-service image gets updated to a
# tag that doesn't exist. New pods fail with ImagePullBackOff.
# Old pods keep running (rollout stalls).
# Looks real: "someone deployed a wrong image tag"
# ============================================
trigger2)
  echo "💥 INCIDENT 2: Triggering Bad Deploy on user-service..."
  echo "   (Simulates: wrong image tag pushed in CI/CD)"
  echo ""

  # Push a nonexistent image tag
  kubectl set image deployment/user-service \
    httpbin=kennethreitz/httpbin:v999-broken-tag \
    -n production

  echo "⏳ Waiting for rollout to stall..."
  sleep 10
  echo ""
  echo "Current state:"
  kubectl get pods -n production -l app=user-service
  echo ""
  echo "Rollout status:"
  kubectl rollout status deployment/user-service -n production --timeout=5s 2>&1 || true
  echo ""
  echo "🔴 New pods should be in ImagePullBackOff, old pods still running"
  echo ""
  echo "NOW TELL YOUR AGENT:"
  echo '  "The user service deployment looks stuck. Something went wrong with the last deploy."'
  ;;

# ============================================
# INCIDENT 3: SECOND OOM KILL on analytics-worker
# THIS IS THE SELF-IMPROVEMENT TEST
# The agent should recognize this as the same pattern
# as Incident 1 and fix it faster.
# ============================================
trigger3)
  echo "💥 INCIDENT 3: Triggering SECOND OOM Kill on analytics-worker..."
  echo "   (This tests self-improvement — agent should recognize OOM pattern)"
  echo ""

  # Replace healthy analytics-worker with memory hog
  kubectl apply -f - <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: analytics-worker
  namespace: production
  labels:
    app: analytics-worker
    tier: worker
spec:
  replicas: 2
  selector:
    matchLabels:
      app: analytics-worker
  template:
    metadata:
      labels:
        app: analytics-worker
        tier: worker
    spec:
      containers:
      - name: worker
        image: polinux/stress
        command: ["stress"]
        args: ["--vm", "1", "--vm-bytes", "150M", "--vm-hang", "1"]
        resources:
          requests:
            memory: "32Mi"
            cpu: "25m"
          limits:
            memory: "100Mi"
            cpu: "100m"
EOF

  echo "⏳ Waiting for pods to crash..."
  sleep 15
  echo ""
  echo "Current state:"
  kubectl get pods -n production -l app=analytics-worker
  echo ""
  echo "🔴 analytics-worker should be in CrashLoopBackOff"
  echo ""
  echo "NOW TELL YOUR AGENT:"
  echo '  "The analytics worker is crashing now too. Whats going on?"'
  echo ""
  echo "⭐ THE AGENT SHOULD:"
  echo "  1. Read learned-patterns.md"
  echo "  2. Match the OOM pattern from Incident 1"
  echo "  3. Skip generic diagnosis"
  echo "  4. Fix it FASTER than Incident 1"
  ;;

# ============================================
# FIX: Restore services to healthy state
# Run this between demo rehearsals
# ============================================
fix1)
  echo "🔧 Fixing payment-processor (restoring healthy image)..."
  kubectl apply -f - <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: payment-processor
  namespace: production
  labels:
    app: payment-processor
    tier: backend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: payment-processor
  template:
    metadata:
      labels:
        app: payment-processor
        tier: backend
    spec:
      containers:
      - name: app
        image: hashicorp/http-echo:0.2.3
        args: ["-text=payment-processor-ok", "-listen=:8080"]
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "32Mi"
            cpu: "25m"
          limits:
            memory: "64Mi"
            cpu: "50m"
EOF
  kubectl wait --for=condition=available deployment/payment-processor -n production --timeout=60s
  echo "✅ payment-processor restored"
  ;;

fix2)
  echo "🔧 Fixing user-service (rolling back)..."
  kubectl rollout undo deployment/user-service -n production
  kubectl wait --for=condition=available deployment/user-service -n production --timeout=60s
  echo "✅ user-service restored"
  ;;

fix3)
  echo "🔧 Fixing analytics-worker (restoring healthy image)..."
  kubectl apply -f - <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: analytics-worker
  namespace: production
  labels:
    app: analytics-worker
    tier: worker
spec:
  replicas: 1
  selector:
    matchLabels:
      app: analytics-worker
  template:
    metadata:
      labels:
        app: analytics-worker
        tier: worker
    spec:
      containers:
      - name: worker
        image: busybox:1.36
        command: ["sh", "-c", "echo 'analytics-worker running' && sleep infinity"]
        resources:
          requests:
            memory: "32Mi"
            cpu: "25m"
          limits:
            memory: "64Mi"
            cpu: "50m"
EOF
  kubectl wait --for=condition=available deployment/analytics-worker -n production --timeout=60s
  echo "✅ analytics-worker restored"
  ;;

# Reset ALL to healthy + clear learned patterns
reset)
  echo "🧹 Full reset..."
  $0 fix1
  $0 fix2
  $0 fix3
  echo ""
  # Reset learned patterns file
  cat > k8s-sre-auto/references/learned-patterns.md << 'PATEOF'
# Learned Incident Patterns

This file is updated automatically after each incident resolution.
The agent reads this FIRST before diagnosing any new incident.
Patterns are ordered newest-first. Matching a known pattern skips generic diagnosis.

---
PATEOF
  echo "✅ Learned patterns cleared"
  echo ""
  kubectl get pods -n production
  echo ""
  echo "✅ All green. Ready for demo."
  ;;

status)
  echo "=== PODS ==="
  kubectl get pods -n production -o wide
  echo ""
  echo "=== SERVICES ==="
  kubectl get svc -n production
  echo ""
  echo "=== RECENT WARNING EVENTS ==="
  kubectl get events -n production --field-selector=type=Warning --sort-by='.lastTimestamp' 2>/dev/null | tail -8
  echo ""
  echo "=== LEARNED PATTERNS (line count) ==="
  wc -l k8s-sre-auto/references/learned-patterns.md 2>/dev/null || echo "File not found"
  echo ""
  echo "=== LEARNED PATTERNS (content) ==="
  cat k8s-sre-auto/references/learned-patterns.md 2>/dev/null || echo "File not found"
  ;;

# ============================================
# DELETE CLUSTER (after hackathon — saves money)
# ============================================
destroy)
  echo "💀 Deleting cluster $CLUSTER_NAME..."
  gcloud container clusters delete sre-demo-cluster --zone us-central1-a --quiet
  echo "✅ Cluster deleted"
  ;;

*)
  echo "Usage: $0 [command]"
  echo ""
  echo "  SETUP:"
  echo "    status    — Show current state of all pods/services"
  echo ""
  echo "  TRIGGER INCIDENTS (run during demo, one at a time):"
  echo "    trigger1  — OOM Kill on payment-processor"
  echo "    trigger2  — Bad image deploy on user-service"
  echo "    trigger3  — SECOND OOM Kill on analytics-worker (self-improvement test)"
  echo ""
  echo "  FIX (restore healthy state between rehearsals):"
  echo "    fix1      — Restore payment-processor"
  echo "    fix2      — Restore user-service"
  echo "    fix3      — Restore analytics-worker"
  echo "    reset     — Fix ALL + clear learned patterns"
  echo ""
  echo "  CLEANUP:"
  echo "    destroy   — Delete the GKE cluster (saves \$\$)"
  ;;

esac

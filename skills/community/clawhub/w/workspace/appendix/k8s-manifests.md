
Yes. For this project, I would keep **Proxmox, VM creation, Cloud-Init, Kubespray, and GPU PCI passthrough out of Argo CD** and start GitOps at the cluster boundary: namespaces and Argo bootstrap first, then cert-manager, ingress, storage, GPU operator, queueing, monitoring, identity, registry, and finally JupyterHub. Argo CD’s declarative model expects `Application` and `AppProject` resources in the Argo namespace, `AppProject` is what constrains allowed repos and destinations, and sync waves are the clean way to force dependency order in an app-of-apps bootstrap. I am also intentionally choosing **Traefik** here instead of `ingress-nginx`, because `ingress-nginx` was archived on 2026-03-24 while Traefik’s official Kubernetes chart is current. ([argo-cd.readthedocs.io][1])

This baseline also keeps **TopoLVM only for local dynamic PVCs**, because TopoLVM is fundamentally a local CSI/LVM implementation, not shared RWX storage. For batch admission and fair use of CPU, memory, and GPUs, I am using **Kueue**, which is the Kubernetes-native queueing layer for jobs. For GPUs, I am relying on **NVIDIA GPU Operator**, which by default manages the driver/device stack and deploys NFD and DCGM Exporter. JupyterHub is expressed as a Helm values-driven deployment, which is exactly how the official chart is intended to be configured. The official chart/install locations used below are: cert-manager `charts.jetstack.io`, Traefik `traefik.github.io/charts`, TopoLVM `topolvm.github.io/topolvm`, NVIDIA GPU Operator `helm.ngc.nvidia.com/nvidia`, Harbor `helm.goharbor.io`, JupyterHub `hub.jupyter.org/helm-chart`, and Kueue’s OCI chart in `registry.k8s.io`. For Keycloak, I am using the **official Keycloak Operator** path rather than a third-party chart. ([cert-manager][2])

Below is the **minimum sane repo** I would actually use for your university GPU lab.

```text
gpu-lab-gitops/
├── bootstrap/
│   ├── project-gpu-lab.yaml
│   └── root-app.yaml
├── apps/
│   ├── 00-namespaces.yaml
│   ├── 01-cert-manager.yaml
│   ├── 02-traefik.yaml
│   ├── 03-topolvm.yaml
│   ├── 04-gpu-operator.yaml
│   ├── 05-kueue.yaml
│   ├── 06-monitoring.yaml
│   ├── 07-keycloak-operator.yaml
│   ├── 08-keycloak.yaml
│   ├── 09-harbor.yaml
│   ├── 10-jupyterhub.yaml
│   └── 11-user-baseline.yaml
└── platform/
    ├── namespaces/
    │   ├── kustomization.yaml
    │   ├── argocd-extra-namespaces.yaml
    │   └── labels-and-limits.yaml
    ├── user-baseline/
    │   ├── kustomization.yaml
    │   ├── priorityclasses.yaml
    │   ├── quota-ml-batch.yaml
    │   └── limitrange-jupyterhub.yaml
    ├── cert-manager/
    │   ├── Chart.yaml
    │   ├── values.yaml
    │   └── templates/
    │       └── clusterissuer.yaml
    ├── traefik/
    │   ├── Chart.yaml
    │   └── values.yaml
    ├── topolvm/
    │   ├── Chart.yaml
    │   ├── values.yaml
    │   └── templates/
    │       └── storageclass.yaml
    ├── gpu-operator/
    │   ├── Chart.yaml
    │   └── values.yaml
    ├── kueue/
    │   ├── Chart.yaml
    │   ├── values.yaml
    │   └── templates/
    │       └── queues.yaml
    ├── monitoring/
    │   ├── Chart.yaml
    │   └── values.yaml
    ├── keycloak-operator/
    │   └── kustomization.yaml
    ├── keycloak/
    │   ├── kustomization.yaml
    │   ├── keycloak.yaml
    │   ├── keycloak-db-secret.example.yaml
    │   └── keycloak-tls-certificate.yaml
    ├── harbor/
    │   ├── Chart.yaml
    │   └── values.yaml
    └── jupyterhub/
        ├── Chart.yaml
        ├── values.yaml
        └── templates/
            └── jupyterhub-oidc-secret.example.yaml
```

### 1) Argo CD bootstrap

```yaml
# bootstrap/project-gpu-lab.yaml
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: gpu-lab
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  description: University GPU Lab platform
  sourceRepos:
    - https://git.example.edu/university/gpu-lab-gitops.git
  destinations:
    - namespace: "*"
      server: https://kubernetes.default.svc
  clusterResourceWhitelist:
    - group: "*"
      kind: "*"
  namespaceResourceWhitelist:
    - group: "*"
      kind: "*"
```

```yaml
# bootstrap/root-app.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: gpu-lab-root
  namespace: argocd
spec:
  project: gpu-lab
  source:
    repoURL: https://git.example.edu/university/gpu-lab-gitops.git
    targetRevision: main
    path: apps
    directory:
      recurse: true
  destination:
    server: https://kubernetes.default.svc
    namespace: argocd
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - ApplyOutOfSyncOnly=true
      - PruneLast=true
```

### 2) Child Argo CD Applications

```yaml
# apps/00-namespaces.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: namespaces
  namespace: argocd
  annotations:
    argocd.argoproj.io/sync-wave: "-20"
spec:
  project: gpu-lab
  source:
    repoURL: https://git.example.edu/university/gpu-lab-gitops.git
    targetRevision: main
    path: platform/namespaces
  destination:
    server: https://kubernetes.default.svc
    namespace: kube-system
  syncPolicy:
    automated: { prune: true, selfHeal: true }
```

```yaml
# apps/01-cert-manager.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: cert-manager
  namespace: argocd
  annotations:
    argocd.argoproj.io/sync-wave: "-10"
spec:
  project: gpu-lab
  source:
    repoURL: https://git.example.edu/university/gpu-lab-gitops.git
    targetRevision: main
    path: platform/cert-manager
  destination:
    server: https://kubernetes.default.svc
    namespace: cert-manager
  syncPolicy:
    automated: { prune: true, selfHeal: true }
    syncOptions:
      - CreateNamespace=true
```

```yaml
# apps/02-traefik.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: traefik
  namespace: argocd
  annotations:
    argocd.argoproj.io/sync-wave: "-9"
spec:
  project: gpu-lab
  source:
    repoURL: https://git.example.edu/university/gpu-lab-gitops.git
    targetRevision: main
    path: platform/traefik
  destination:
    server: https://kubernetes.default.svc
    namespace: traefik
  syncPolicy:
    automated: { prune: true, selfHeal: true }
    syncOptions:
      - CreateNamespace=true
```

```yaml
# apps/03-topolvm.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: topolvm
  namespace: argocd
  annotations:
    argocd.argoproj.io/sync-wave: "-8"
spec:
  project: gpu-lab
  source:
    repoURL: https://git.example.edu/university/gpu-lab-gitops.git
    targetRevision: main
    path: platform/topolvm
  destination:
    server: https://kubernetes.default.svc
    namespace: topolvm-system
  syncPolicy:
    automated: { prune: true, selfHeal: true }
    syncOptions:
      - CreateNamespace=true
```

```yaml
# apps/04-gpu-operator.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: gpu-operator
  namespace: argocd
  annotations:
    argocd.argoproj.io/sync-wave: "-7"
spec:
  project: gpu-lab
  source:
    repoURL: https://git.example.edu/university/gpu-lab-gitops.git
    targetRevision: main
    path: platform/gpu-operator
  destination:
    server: https://kubernetes.default.svc
    namespace: gpu-operator
  syncPolicy:
    automated: { prune: true, selfHeal: true }
    syncOptions:
      - CreateNamespace=true
```

```yaml
# apps/05-kueue.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: kueue
  namespace: argocd
  annotations:
    argocd.argoproj.io/sync-wave: "-6"
spec:
  project: gpu-lab
  source:
    repoURL: https://git.example.edu/university/gpu-lab-gitops.git
    targetRevision: main
    path: platform/kueue
  destination:
    server: https://kubernetes.default.svc
    namespace: kueue-system
  syncPolicy:
    automated: { prune: true, selfHeal: true }
    syncOptions:
      - CreateNamespace=true
```

```yaml
# apps/06-monitoring.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: monitoring
  namespace: argocd
  annotations:
    argocd.argoproj.io/sync-wave: "-5"
spec:
  project: gpu-lab
  source:
    repoURL: https://git.example.edu/university/gpu-lab-gitops.git
    targetRevision: main
    path: platform/monitoring
  destination:
    server: https://kubernetes.default.svc
    namespace: monitoring
  syncPolicy:
    automated: { prune: true, selfHeal: true }
    syncOptions:
      - CreateNamespace=true
```

```yaml
# apps/07-keycloak-operator.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: keycloak-operator
  namespace: argocd
  annotations:
    argocd.argoproj.io/sync-wave: "-4"
spec:
  project: gpu-lab
  source:
    repoURL: https://git.example.edu/university/gpu-lab-gitops.git
    targetRevision: main
    path: platform/keycloak-operator
  destination:
    server: https://kubernetes.default.svc
    namespace: keycloak
  syncPolicy:
    automated: { prune: true, selfHeal: true }
    syncOptions:
      - CreateNamespace=true
```

```yaml
# apps/08-keycloak.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: keycloak
  namespace: argocd
  annotations:
    argocd.argoproj.io/sync-wave: "-3"
spec:
  project: gpu-lab
  source:
    repoURL: https://git.example.edu/university/gpu-lab-gitops.git
    targetRevision: main
    path: platform/keycloak
  destination:
    server: https://kubernetes.default.svc
    namespace: keycloak
  syncPolicy:
    automated: { prune: true, selfHeal: true }
    syncOptions:
      - SkipDryRunOnMissingResource=true
```

```yaml
# apps/09-harbor.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: harbor
  namespace: argocd
  annotations:
    argocd.argoproj.io/sync-wave: "-2"
spec:
  project: gpu-lab
  source:
    repoURL: https://git.example.edu/university/gpu-lab-gitops.git
    targetRevision: main
    path: platform/harbor
  destination:
    server: https://kubernetes.default.svc
    namespace: harbor
  syncPolicy:
    automated: { prune: true, selfHeal: true }
    syncOptions:
      - CreateNamespace=true
```

```yaml
# apps/10-jupyterhub.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: jupyterhub
  namespace: argocd
  annotations:
    argocd.argoproj.io/sync-wave: "-1"
spec:
  project: gpu-lab
  source:
    repoURL: https://git.example.edu/university/gpu-lab-gitops.git
    targetRevision: main
    path: platform/jupyterhub
  destination:
    server: https://kubernetes.default.svc
    namespace: jupyterhub
  syncPolicy:
    automated: { prune: true, selfHeal: true }
    syncOptions:
      - CreateNamespace=true
```

```yaml
# apps/11-user-baseline.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: user-baseline
  namespace: argocd
  annotations:
    argocd.argoproj.io/sync-wave: "0"
spec:
  project: gpu-lab
  source:
    repoURL: https://git.example.edu/university/gpu-lab-gitops.git
    targetRevision: main
    path: platform/user-baseline
  destination:
    server: https://kubernetes.default.svc
    namespace: ml-batch
  syncPolicy:
    automated: { prune: true, selfHeal: true }
```

### 3) Namespaces and global baseline

```yaml
# platform/namespaces/kustomization.yaml
resources:
  - argocd-extra-namespaces.yaml
  - labels-and-limits.yaml
```

```yaml
# platform/namespaces/argocd-extra-namespaces.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: cert-manager
---
apiVersion: v1
kind: Namespace
metadata:
  name: traefik
---
apiVersion: v1
kind: Namespace
metadata:
  name: topolvm-system
---
apiVersion: v1
kind: Namespace
metadata:
  name: gpu-operator
---
apiVersion: v1
kind: Namespace
metadata:
  name: kueue-system
---
apiVersion: v1
kind: Namespace
metadata:
  name: monitoring
---
apiVersion: v1
kind: Namespace
metadata:
  name: keycloak
---
apiVersion: v1
kind: Namespace
metadata:
  name: harbor
---
apiVersion: v1
kind: Namespace
metadata:
  name: jupyterhub
---
apiVersion: v1
kind: Namespace
metadata:
  name: ml-batch
```

```yaml
# platform/namespaces/labels-and-limits.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: jupyterhub
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
---
apiVersion: v1
kind: Namespace
metadata:
  name: ml-batch
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```

### 4) User quotas and scheduling classes

```yaml
# platform/user-baseline/kustomization.yaml
resources:
  - priorityclasses.yaml
  - quota-ml-batch.yaml
  - limitrange-jupyterhub.yaml
```

```yaml
# platform/user-baseline/priorityclasses.yaml
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: batch-low
value: 1000
globalDefault: false
description: Low-priority batch experimentation
---
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: batch-normal
value: 5000
globalDefault: false
description: Standard research jobs
---
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: batch-high
value: 10000
globalDefault: false
description: Time-sensitive academic jobs
```

```yaml
# platform/user-baseline/quota-ml-batch.yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: ml-batch-quota
  namespace: ml-batch
spec:
  hard:
    requests.cpu: "200"
    requests.memory: 512Gi
    requests.nvidia.com/gpu: "8"
    limits.cpu: "300"
    limits.memory: 768Gi
    limits.nvidia.com/gpu: "8"
    persistentvolumeclaims: "100"
```

```yaml
# platform/user-baseline/limitrange-jupyterhub.yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: jupyterhub-defaults
  namespace: jupyterhub
spec:
  limits:
    - type: Container
      defaultRequest:
        cpu: "500m"
        memory: 1Gi
      default:
        cpu: "2"
        memory: 4Gi
```

### 5) cert-manager

```yaml
# platform/cert-manager/Chart.yaml
apiVersion: v2
name: cert-manager-wrapper
version: 0.1.0
dependencies:
  - name: cert-manager
    version: <PIN_CERT_MANAGER_CHART_VERSION>
    repository: https://charts.jetstack.io
```

```yaml
# platform/cert-manager/values.yaml
cert-manager:
  installCRDs: true
  prometheus:
    enabled: true
```

```yaml
# platform/cert-manager/templates/clusterissuer.yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    email: infra@example.edu
    server: https://acme-v02.api.letsencrypt.org/directory
    privateKeySecretRef:
      name: letsencrypt-prod-account-key
    solvers:
      - http01:
          ingress:
            class: traefik
```

### 6) Traefik ingress

```yaml
# platform/traefik/Chart.yaml
apiVersion: v2
name: traefik-wrapper
version: 0.1.0
dependencies:
  - name: traefik
    version: <PIN_TRAEFIK_CHART_VERSION>
    repository: https://traefik.github.io/charts
```

```yaml
# platform/traefik/values.yaml
traefik:
  deployment:
    replicas: 2

  ingressClass:
    enabled: true
    isDefaultClass: true
    name: traefik

  service:
    type: NodePort

  ports:
    web:
      port: 80
      nodePort: 30080
    websecure:
      port: 443
      nodePort: 30443

  additionalArguments:
    - --api.dashboard=false
    - --providers.kubernetesingress=true
    - --providers.kubernetescrd=true
    - --entrypoints.web.address=:80
    - --entrypoints.websecure.address=:443
    - --entryPoints.web.http.redirections.entryPoint.to=websecure
    - --entryPoints.web.http.redirections.entryPoint.scheme=https
```

### 7) TopoLVM

```yaml
# platform/topolvm/Chart.yaml
apiVersion: v2
name: topolvm-wrapper
version: 0.1.0
dependencies:
  - name: topolvm
    version: <PIN_TOPOLVM_CHART_VERSION>
    repository: https://topolvm.github.io/topolvm
```

```yaml
# platform/topolvm/values.yaml
topolvm:
  scheduler:
    enabled: true

  lvmd:
    managed: true
    deviceClasses:
      - name: nvme
        volume-group: vg_nvme

  controller:
    replicaCount: 2
```

```yaml
# platform/topolvm/templates/storageclass.yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: topolvm-nvme
provisioner: topolvm.io
allowVolumeExpansion: true
reclaimPolicy: Delete
volumeBindingMode: WaitForFirstConsumer
parameters:
  csi.storage.k8s.io/fstype: xfs
  topolvm.io/device-class: nvme
```

### 8) NVIDIA GPU Operator

```yaml
# platform/gpu-operator/Chart.yaml
apiVersion: v2
name: gpu-operator-wrapper
version: 0.1.0
dependencies:
  - name: gpu-operator
    version: <PIN_GPU_OPERATOR_CHART_VERSION>
    repository: https://helm.ngc.nvidia.com/nvidia
```

```yaml
# platform/gpu-operator/values.yaml
gpu-operator:
  driver:
    enabled: true

  toolkit:
    enabled: true

  cdi:
    enabled: true

  nfd:
    enabled: true

  dcgmExporter:
    enabled: true

  mig:
    strategy: none

  validator:
    plugin:
      env:
        - name: WITH_WORKLOAD
          value: "true"
```

### 9) Kueue for batch jobs

```yaml
# platform/kueue/Chart.yaml
apiVersion: v2
name: kueue-wrapper
version: 0.1.0
dependencies:
  - name: kueue
    version: <PIN_KUEUE_CHART_VERSION>
    repository: oci://registry.k8s.io/kueue/charts
```

```yaml
# platform/kueue/values.yaml
kueue:
  controllerManager:
    manager:
      replicas: 2
```

```yaml
# platform/kueue/templates/queues.yaml
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: default
spec: {}
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: gpu-nodes
spec:
  nodeLabels:
    node-role.kubernetes.io/gpu: "true"
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: gpu-lab
spec:
  namespaceSelector: {}
  resourceGroups:
    - coveredResources: ["cpu", "memory"]
      flavors:
        - name: default
          resources:
            - name: cpu
              nominalQuota: 200
            - name: memory
              nominalQuota: 512Gi
    - coveredResources: ["nvidia.com/gpu"]
      flavors:
        - name: gpu-nodes
          resources:
            - name: nvidia.com/gpu
              nominalQuota: 8
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  name: ml-batch
  namespace: ml-batch
spec:
  clusterQueue: gpu-lab
```

### 10) Monitoring

```yaml
# platform/monitoring/Chart.yaml
apiVersion: v2
name: monitoring-wrapper
version: 0.1.0
dependencies:
  - name: kube-prometheus-stack
    version: <PIN_KPS_CHART_VERSION>
    repository: https://prometheus-community.github.io/helm-charts
```

```yaml
# platform/monitoring/values.yaml
kube-prometheus-stack:
  grafana:
    ingress:
      enabled: true
      ingressClassName: traefik
      hosts:
        - grafana.platform.example.edu
      tls:
        - secretName: grafana-tls
          hosts:
            - grafana.platform.example.edu

  prometheus:
    prometheusSpec:
      retention: 30d
      serviceMonitorSelectorNilUsesHelmValues: false
      podMonitorSelectorNilUsesHelmValues: false

  alertmanager:
    ingress:
      enabled: true
      ingressClassName: traefik
      hosts:
        - alertmanager.platform.example.edu
      tls:
        - secretName: alertmanager-tls
          hosts:
            - alertmanager.platform.example.edu
```

### 11) Keycloak Operator

```yaml
# platform/keycloak-operator/kustomization.yaml
resources:
  - https://raw.githubusercontent.com/keycloak/keycloak-k8s-resources/26.6.1/kubernetes/keycloaks.k8s.keycloak.org-v1.yml
  - https://raw.githubusercontent.com/keycloak/keycloak-k8s-resources/26.6.1/kubernetes/keycloakrealmimports.k8s.keycloak.org-v1.yml
  - https://raw.githubusercontent.com/keycloak/keycloak-k8s-resources/26.6.1/kubernetes/kubernetes.yml
```

### 12) Keycloak instance

```yaml
# platform/keycloak/kustomization.yaml
resources:
  - keycloak.yaml
  - keycloak-tls-certificate.yaml
```

```yaml
# platform/keycloak/keycloak-db-secret.example.yaml
apiVersion: v1
kind: Secret
metadata:
  name: keycloak-db-secret
  namespace: keycloak
type: Opaque
stringData:
  username: keycloak
  password: CHANGE_ME
```

```yaml
# platform/keycloak/keycloak-tls-certificate.yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: keycloak-tls
  namespace: keycloak
spec:
  secretName: keycloak-tls
  issuerRef:
    name: letsencrypt-prod
    kind: ClusterIssuer
  dnsNames:
    - sso.platform.example.edu
```

```yaml
# platform/keycloak/keycloak.yaml
apiVersion: k8s.keycloak.org/v2beta1
kind: Keycloak
metadata:
  name: keycloak
  namespace: keycloak
spec:
  instances: 2
  hostname:
    hostname: sso.platform.example.edu
  ingress:
    enabled: true
    className: traefik
    tlsSecret: keycloak-tls
  http:
    httpEnabled: true
  db:
    vendor: postgres
    host: postgresql-rw.keycloak.svc.cluster.local
    database: keycloak
    usernameSecret:
      name: keycloak-db-secret
      key: username
    passwordSecret:
      name: keycloak-db-secret
      key: password
  resources:
    requests:
      cpu: "500m"
      memory: 1Gi
    limits:
      cpu: "2"
      memory: 2Gi
```

### 13) Harbor

```yaml
# platform/harbor/Chart.yaml
apiVersion: v2
name: harbor-wrapper
version: 0.1.0
dependencies:
  - name: harbor
    version: <PIN_HARBOR_CHART_VERSION>
    repository: https://helm.goharbor.io
```

```yaml
# platform/harbor/values.yaml
harbor:
  expose:
    type: ingress
    tls:
      enabled: true
      certSource: secret
      secret:
        secretName: harbor-tls
    ingress:
      className: traefik
      hosts:
        core: harbor.platform.example.edu

  externalURL: https://harbor.platform.example.edu

  persistence:
    enabled: true
    persistentVolumeClaim:
      registry:
        storageClass: topolvm-nvme
        size: 200Gi
      chartmuseum:
        storageClass: topolvm-nvme
        size: 20Gi
      jobservice:
        jobLog:
          storageClass: topolvm-nvme
          size: 20Gi
      database:
        storageClass: topolvm-nvme
        size: 20Gi
      redis:
        storageClass: topolvm-nvme
        size: 8Gi
      trivy:
        storageClass: topolvm-nvme
        size: 20Gi

  trivy:
    enabled: true

  notary:
    enabled: false
```

### 14) JupyterHub

```yaml
# platform/jupyterhub/Chart.yaml
apiVersion: v2
name: jupyterhub-wrapper
version: 0.1.0
dependencies:
  - name: jupyterhub
    version: <PIN_JUPYTERHUB_CHART_VERSION>
    repository: https://hub.jupyter.org/helm-chart/
```

```yaml
# platform/jupyterhub/templates/jupyterhub-oidc-secret.example.yaml
apiVersion: v1
kind: Secret
metadata:
  name: jupyterhub-oidc
  namespace: jupyterhub
type: Opaque
stringData:
  client-id: jupyterhub
  client-secret: CHANGE_ME
  authorize-url: https://sso.platform.example.edu/realms/gpu-lab/protocol/openid-connect/auth
  token-url: https://sso.platform.example.edu/realms/gpu-lab/protocol/openid-connect/token
  userdata-url: https://sso.platform.example.edu/realms/gpu-lab/protocol/openid-connect/userinfo
```

```yaml
# platform/jupyterhub/values.yaml
jupyterhub:
  ingress:
    enabled: true
    ingressClassName: traefik
    hosts:
      - hub.platform.example.edu
    tls:
      - secretName: jupyterhub-tls
        hosts:
          - hub.platform.example.edu

  proxy:
    service:
      type: ClusterIP

  hub:
    extraEnv:
      OAUTH_CLIENT_ID:
        valueFrom:
          secretKeyRef:
            name: jupyterhub-oidc
            key: client-id
      OAUTH_CLIENT_SECRET:
        valueFrom:
          secretKeyRef:
            name: jupyterhub-oidc
            key: client-secret
      OAUTH_AUTHORIZE_URL:
        valueFrom:
          secretKeyRef:
            name: jupyterhub-oidc
            key: authorize-url
      OAUTH_TOKEN_URL:
        valueFrom:
          secretKeyRef:
            name: jupyterhub-oidc
            key: token-url
      OAUTH_USERDATA_URL:
        valueFrom:
          secretKeyRef:
            name: jupyterhub-oidc
            key: userdata-url

    extraConfig:
      00-auth.py: |
        import os
        c.JupyterHub.authenticator_class = "generic-oauth"
        c.GenericOAuthenticator.client_id = os.environ["OAUTH_CLIENT_ID"]
        c.GenericOAuthenticator.client_secret = os.environ["OAUTH_CLIENT_SECRET"]
        c.GenericOAuthenticator.authorize_url = os.environ["OAUTH_AUTHORIZE_URL"]
        c.GenericOAuthenticator.token_url = os.environ["OAUTH_TOKEN_URL"]
        c.GenericOAuthenticator.userdata_url = os.environ["OAUTH_USERDATA_URL"]
        c.GenericOAuthenticator.username_key = "preferred_username"
        c.Authenticator.enable_auth_state = True

  singleuser:
    storage:
      dynamic:
        storageClass: topolvm-nvme
        storageAccessModes:
          - ReadWriteOnce
        capacity: 50Gi

    image:
      name: harbor.platform.example.edu/ml/pytorch-cuda
      tag: "2.2-cuda12.1"
      pullPolicy: IfNotPresent

    profileList:
      - display_name: "CPU Small"
        slug: cpu-small
        kubespawner_override:
          cpu_guarantee: 1
          cpu_limit: 2
          mem_guarantee: 2G
          mem_limit: 4G

      - display_name: "1x GPU Standard"
        slug: gpu-1
        kubespawner_override:
          cpu_guarantee: 4
          cpu_limit: 8
          mem_guarantee: 8G
          mem_limit: 32G
          extra_resource_limits:
            nvidia.com/gpu: "1"
          node_selector:
            node-role.kubernetes.io/gpu: "true"
          tolerations:
            - key: "nvidia.com/gpu"
              operator: "Exists"
              effect: "NoSchedule"

      - display_name: "2x GPU Large"
        slug: gpu-2
        kubespawner_override:
          cpu_guarantee: 8
          cpu_limit: 16
          mem_guarantee: 16G
          mem_limit: 64G
          extra_resource_limits:
            nvidia.com/gpu: "2"
          node_selector:
            node-role.kubernetes.io/gpu: "true"
          tolerations:
            - key: "nvidia.com/gpu"
              operator: "Exists"
              effect: "NoSchedule"

  scheduling:
    userScheduler:
      enabled: true
```

### 15) One example Kueue batch job for students

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: mnist-train
  namespace: ml-batch
  labels:
    kueue.x-k8s.io/queue-name: ml-batch
spec:
  template:
    spec:
      restartPolicy: Never
      priorityClassName: batch-normal
      nodeSelector:
        node-role.kubernetes.io/gpu: "true"
      tolerations:
        - key: "nvidia.com/gpu"
          operator: "Exists"
          effect: "NoSchedule"
      containers:
        - name: train
          image: harbor.platform.example.edu/ml/pytorch-cuda:2.2-cuda12.1
          command: ["python", "train.py"]
          resources:
            requests:
              cpu: "4"
              memory: 16Gi
              nvidia.com/gpu: "1"
            limits:
              cpu: "8"
              memory: 16Gi
              nvidia.com/gpu: "1"
```

The parts that are still intentionally site-specific are only these: your Git repo URL, exact chart versions, DNS names, TLS issuer policy, storage VG name, GPU node labels, and real OIDC/DB secrets. Everything else above is the correct **shape** for this project and is the set of manifests I would expect in a serious bachelor GPU-lab implementation.

The next hardening step would be to split this into `base/` and `overlays/{staging,prod}/` and pin every chart version and image digest.

[1]: https://argo-cd.readthedocs.io/en/stable/operator-manual/declarative-setup/ "https://argo-cd.readthedocs.io/en/stable/operator-manual/declarative-setup/"
[2]: https://cert-manager.io/v1.14-docs/installation/helm/ "https://cert-manager.io/v1.14-docs/installation/helm/"


#!/usr/bin/env python3
"""Kubernetes 清单体检：不依赖 PyYAML/kubectl 的最小 YAML 解析 + 生产就绪检查。

用法：
  python3 k8s_check.py deploy/ k8s/app.yaml [--json] [--strict]
  --strict：存在 high/warn 则退出码 1。
覆盖：Deployment/StatefulSet/DaemonSet/Job/CronJob/Pod/Service/Ingress/PodDisruptionBudget 等的常见 YAML（块结构）。
限制：不支持 YAML 锚点合并（<<: *x）、多行 flow 集合；Helm 模板请先 helm template 渲染。
"""
import argparse, json, os, re, sys

SECRET_NAME = re.compile(r"(PASSWORD|PASSWD|SECRET|TOKEN|API_?KEY|PRIVATE_?KEY|ACCESS_?KEY|CREDENTIAL)", re.I)
DEPRECATED = {("extensions/v1beta1", None): "apps/v1 或 networking.k8s.io/v1", ("apps/v1beta1", None): "apps/v1", ("apps/v1beta2", None): "apps/v1",
              ("networking.k8s.io/v1beta1", "Ingress"): "networking.k8s.io/v1", ("batch/v1beta1", "CronJob"): "batch/v1",
              ("policy/v1beta1", "PodDisruptionBudget"): "policy/v1", ("autoscaling/v2beta1", None): "autoscaling/v2", ("autoscaling/v2beta2", None): "autoscaling/v2"}


# ---------- 最小 YAML 解析 ----------
def scalar(s):
    s = s.strip()
    if s == "" or s in ("~", "null", "Null", "NULL"):
        return None
    if s[:1] in ("'", '"') and s[-1:] == s[:1] and len(s) >= 2:
        return s[1:-1]
    if s in ("true", "True", "TRUE"): return True
    if s in ("false", "False", "FALSE"): return False
    if re.fullmatch(r"-?\d+", s): return int(s)
    if re.fullmatch(r"-?\d+\.\d+", s): return float(s)
    if s.startswith("[") and s.endswith("]"):
        inner = s[1:-1].strip()
        return [scalar(x) for x in inner.split(",")] if inner else []
    if s.startswith("{") and s.endswith("}"):
        out = {}
        for kv in s[1:-1].split(","):
            if ":" in kv:
                k, v = kv.split(":", 1); out[k.strip()] = scalar(v)
        return out
    return s


def split_kv(line):
    """把 'key: value' 切开；忽略引号内的冒号。"""
    q = None
    for i, ch in enumerate(line):
        if q:
            if ch == q: q = None
        elif ch in ("'", '"'): q = ch
        elif ch == ":" and (i + 1 == len(line) or line[i + 1] in " \t"):
            return line[:i].strip(), line[i + 1:].strip()
    return None, None


def strip_comment(line):
    q, out = None, []
    for i, ch in enumerate(line):
        if q:
            if ch == q: q = None
        elif ch in ("'", '"'): q = ch
        elif ch == "#" and (i == 0 or line[i - 1] in " \t"):
            break
        out.append(ch)
    return "".join(out).rstrip()


def parse_block(lines, i, indent):
    """解析从 lines[i] 开始、缩进为 indent 的块；返回 (值, 下一行号)。"""
    # 判断是列表还是映射
    while i < len(lines) and not lines[i][1].strip():
        i += 1
    if i >= len(lines):
        return None, i
    ind, text = lines[i]
    if ind < indent:
        return None, i
    if text.startswith("- ") or text == "-":
        out = []
        while i < len(lines):
            ind, text = lines[i]
            if not text.strip(): i += 1; continue
            if ind != indent or not (text.startswith("- ") or text == "-"):
                break
            body = text[1:].strip()
            if not body:
                val, i = parse_block(lines, i + 1, indent + 1); out.append(val); continue
            k, v = split_kv(body)
            if k is not None and not body.startswith(("'", '"', "[", "{")):
                # 列表项本身是映射：把 "- key: v" 视为缩进 indent+2 的映射首行
                lines[i] = (indent + 2, body)
                val, i = parse_block(lines, i, indent + 2); out.append(val)
            else:
                out.append(scalar(body)); i += 1
        return out, i
    out = {}
    while i < len(lines):
        ind, text = lines[i]
        if not text.strip(): i += 1; continue
        if ind < indent or (ind == indent and (text.startswith("- ") or text == "-")):
            break
        if ind > indent:
            i += 1; continue  # 容错：意外的深缩进
        k, v = split_kv(text)
        if k is None:
            i += 1; continue
        if v in ("|", "|-", "|+", ">", ">-", ">+"):
            block, j = [], i + 1
            while j < len(lines) and (not lines[j][1].strip() or lines[j][0] > indent):
                block.append(lines[j][1]); j += 1
            out[k] = "\n".join(block); i = j; continue
        if v == "":
            # 子块或空值
            j = i + 1
            while j < len(lines) and not lines[j][1].strip(): j += 1
            if j < len(lines) and (lines[j][0] > indent or (lines[j][0] == indent and lines[j][1].startswith("- "))):
                out[k], i = parse_block(lines, j, lines[j][0])
            else:
                out[k] = None; i = j
            continue
        if v.startswith("&"):
            v = v.split(" ", 1)[1] if " " in v else ""
        out[k] = scalar(v); i += 1
    return out, i


def load_docs(text):
    docs = []
    for chunk in re.split(r"^---\s*$", text, flags=re.M):
        raw = [strip_comment(l.replace("\t", "  ")) for l in chunk.splitlines()]
        lines = [(len(l) - len(l.lstrip(" ")), l.strip()) for l in raw if l.strip() and not l.strip().startswith("%")]
        if not lines:
            continue
        doc, _ = parse_block(lines, 0, lines[0][0])
        if isinstance(doc, dict) and doc.get("kind"):
            docs.append(doc)
    return docs


# ---------- 检查 ----------
def get(d, *path, default=None):
    for p in path:
        if isinstance(d, dict):
            d = d.get(p)
        elif isinstance(d, list) and isinstance(p, int) and p < len(d):
            d = d[p]
        else:
            return default
    return default if d is None else d


def check_doc(doc, findings, where):
    kind, api = doc.get("kind"), doc.get("apiVersion")
    name = get(doc, "metadata", "name", default="?")
    loc = f"{where} {kind}/{name}"

    def add(rule, sev, msg, fix):
        findings.append({"rule": rule, "severity": sev, "object": f"{kind}/{name}", "file": where, "message": msg, "fix": fix})

    for (dapi, dkind), repl in DEPRECATED.items():
        if api == dapi and (dkind is None or dkind == kind):
            add("K018", "warn", f"apiVersion {api} 已废弃/移除", f"改用 {repl}")
    if not get(doc, "metadata", "namespace") and kind not in ("Namespace", "ClusterRole", "ClusterRoleBinding", "StorageClass", "PersistentVolume", "CustomResourceDefinition"):
        add("K011", "info", "未指定 namespace", "显式写 metadata.namespace，避免误部署到 default")
    pod = None
    if kind in ("Deployment", "StatefulSet", "DaemonSet", "Job", "ReplicaSet"):
        pod = get(doc, "spec", "template", "spec")
        labels = get(doc, "spec", "template", "metadata", "labels", default={}) or {}
        sel = get(doc, "spec", "selector", "matchLabels", default={}) or {}
        if kind != "Job" and sel and any(labels.get(k) != v for k, v in sel.items()):
            add("K009", "high", "spec.selector.matchLabels 与 template.metadata.labels 不匹配", "两者必须一致，否则创建失败或选不到 Pod")
        if kind == "Deployment" and get(doc, "spec", "replicas") in (None, 1):
            add("K007", "info", "replicas 为 1（或未设置）", "生产至少 2 副本并配 PodDisruptionBudget；单副本滚动更新与节点维护时会中断")
    elif kind == "CronJob":
        pod = get(doc, "spec", "jobTemplate", "spec", "template", "spec")
        if not get(doc, "spec", "concurrencyPolicy"):
            add("K013", "info", "CronJob 未设置 concurrencyPolicy", "多数任务应设 Forbid 或 Replace，避免上一轮未结束又启动")
        if get(doc, "spec", "successfulJobsHistoryLimit") is None:
            add("K013", "info", "CronJob 未设置 successfulJobsHistoryLimit / failedJobsHistoryLimit", "设置历史保留数量，避免 Job 对象堆积")
        if not get(doc, "spec", "startingDeadlineSeconds"):
            add("K013", "info", "CronJob 未设置 startingDeadlineSeconds", "设置后错过调度窗口的任务会被跳过而不是堆积")
    elif kind == "Pod":
        pod = doc.get("spec")
    elif kind == "Service":
        t = get(doc, "spec", "type")
        if t in ("LoadBalancer", "NodePort"):
            add("K012", "info", f"Service 类型 {t} 会对外暴露", "确认确实需要对外暴露；内部服务用 ClusterIP + Ingress")
    elif kind == "Ingress":
        if not get(doc, "spec", "tls"):
            add("K017", "info", "Ingress 未配置 TLS", "配置 spec.tls 与证书（如 cert-manager）")
    if not isinstance(pod, dict):
        return
    for f in ("hostNetwork", "hostPID", "hostIPC"):
        if pod.get(f) is True:
            add("K005", "high", f"{f}: true 打破了 Pod 隔离", "除网络插件/监控代理等系统组件外不要使用")
    for v in pod.get("volumes") or []:
        if isinstance(v, dict) and "hostPath" in v:
            add("K006", "warn", f"使用 hostPath 卷 {get(v, 'hostPath', 'path')}", "改用 PVC / ConfigMap / emptyDir；hostPath 让容器能访问节点文件系统")
    psc = pod.get("securityContext") or {}
    if not pod.get("serviceAccountName") and pod.get("automountServiceAccountToken") is not False:
        add("K019", "info", "使用 default ServiceAccount 且自动挂载 token", "不需要访问 API 的工作负载设 automountServiceAccountToken: false，或绑定最小权限的专用 SA")
    containers = (pod.get("containers") or []) + (pod.get("initContainers") or [])
    for c in containers:
        if not isinstance(c, dict):
            continue
        cn = c.get("name", "?")
        img = str(c.get("image") or "")
        tagless = "@sha256:" not in img and (":" not in img.split("/")[-1])
        if tagless or img.endswith(":latest"):
            add("K001", "warn", f"容器 {cn} 镜像未固定版本：{img}", "使用明确标签或 digest，保证可回滚、可复现")
        if c.get("imagePullPolicy") == "IfNotPresent" and (tagless or img.endswith(":latest")):
            add("K008", "warn", f"容器 {cn} 用 latest/无标签镜像却设 IfNotPresent", "会一直跑旧镜像；固定标签或改为 Always")
        res = c.get("resources") or {}
        req, lim = res.get("requests") or {}, res.get("limits") or {}
        if not req.get("cpu") or not req.get("memory"):
            add("K002", "warn", f"容器 {cn} 缺少 resources.requests（cpu/memory）", "设置 requests，调度器才能合理放置，且决定 QoS 等级")
        if not lim.get("memory"):
            add("K002", "warn", f"容器 {cn} 缺少 resources.limits.memory", "设置内存上限防止把节点吃满；CPU limit 视情况可不设")
        if c.get("readinessProbe") is None and kind not in ("Job", "CronJob"):
            add("K003", "warn", f"容器 {cn} 没有 readinessProbe", "没有就绪探针，滚动更新时流量会打到还没准备好的 Pod")
        if c.get("livenessProbe") is None and kind not in ("Job", "CronJob"):
            add("K003", "info", f"容器 {cn} 没有 livenessProbe", "为长期运行的服务加存活探针（注意别与就绪探针指向同一个重依赖检查）")
        csc = c.get("securityContext") or {}
        if csc.get("privileged") is True:
            add("K004", "high", f"容器 {cn} privileged: true", "几乎等于 root 节点权限；改用具体 capabilities")
        if csc.get("runAsNonRoot") is not True and psc.get("runAsNonRoot") is not True:
            add("K004", "warn", f"容器 {cn} 未声明 runAsNonRoot: true", "在 securityContext 设置 runAsNonRoot: true 与 runAsUser（非 0）")
        if csc.get("allowPrivilegeEscalation") is not False:
            add("K004", "info", f"容器 {cn} 未设置 allowPrivilegeEscalation: false", "显式关闭提权")
        if csc.get("readOnlyRootFilesystem") is not True:
            add("K004", "info", f"容器 {cn} 未设置 readOnlyRootFilesystem: true", "只读根文件系统，可写目录用 emptyDir 挂载")
        caps = get(csc, "capabilities", "drop", default=[]) or []
        if "ALL" not in [str(x).upper() for x in caps]:
            add("K004", "info", f"容器 {cn} 未 drop 全部 capabilities", "capabilities.drop: [ALL]，再按需 add")
        for e in c.get("env") or []:
            if isinstance(e, dict) and SECRET_NAME.search(str(e.get("name", ""))) and e.get("value") not in (None, ""):
                add("K010", "high", f"容器 {cn} 的环境变量 {e.get('name')} 以明文 value 写入清单", "改用 valueFrom.secretKeyRef 引用 Secret")


def main():
    ap = argparse.ArgumentParser(description="Kubernetes 清单体检")
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true")
    a = ap.parse_args()
    files = []
    for p in a.paths:
        if os.path.isdir(p):
            for r, dirs, fs in os.walk(p):
                dirs[:] = [d for d in dirs if d not in (".git", "node_modules", "charts", "templates")]
                files += sorted(os.path.join(r, f) for f in fs if f.endswith((".yaml", ".yml")))
        else:
            files.append(p)
    findings, n_docs = [], 0
    for f in files:
        text = open(f, encoding="utf-8", errors="replace").read()
        if "{{" in text and "}}" in text:
            findings.append({"rule": "K000", "severity": "info", "object": "-", "file": f, "message": "看起来是 Helm 模板", "fix": "先 helm template 渲染成纯 YAML 再检查"})
            continue
        for doc in load_docs(text):
            n_docs += 1
            check_doc(doc, findings, os.path.relpath(f) if os.path.abspath(f).startswith(os.getcwd()) else f)
    order = {"high": 0, "warn": 1, "info": 2}
    findings.sort(key=lambda x: (order[x["severity"]], x["file"], x["object"], x["rule"]))
    if a.json:
        print(json.dumps({"files": len(files), "objects": n_docs, "findings": findings}, ensure_ascii=False, indent=2))
    else:
        print(f"检查 {len(files)} 个文件、{n_docs} 个对象")
        if not findings:
            print("  ✓ 没有发现问题")
        cur = None
        for x in findings:
            key = (x["file"], x["object"])
            if key != cur:
                print(f"\n== {x['file']}  {x['object']}"); cur = key
            print(f"  [{x['severity'].upper():4}] {x['rule']}: {x['message']}\n         → {x['fix']}")
        c = {s: sum(1 for x in findings if x["severity"] == s) for s in ("high", "warn", "info")}
        print(f"\n小计：high {c['high']} / warn {c['warn']} / info {c['info']}")
    bad = any(x["severity"] in ("high", "warn") for x in findings)
    sys.exit(1 if (a.strict and bad) else 0)


if __name__ == "__main__":
    main()

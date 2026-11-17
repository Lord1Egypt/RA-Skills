#!/usr/bin/env python3
"""OpenAPI 3.x 规范对比：找出破坏性变更（breaking）与新增（additive）。纯标准库；YAML 需要可选的 PyYAML。

用法：
  python3 openapi_diff.py old.json new.json [--json] [--strict]
  --strict：存在破坏性变更则退出码 1（CI 门禁）
"""
import argparse, json, sys


def load(path):
    text = open(path, encoding="utf-8").read()
    if path.lower().endswith((".yaml", ".yml")):
        try:
            import yaml
        except ImportError:
            sys.exit("读取 YAML 需要 PyYAML：pip install pyyaml，或先转成 JSON")
        return yaml.safe_load(text)
    return json.loads(text)


class Spec:
    def __init__(self, doc):
        self.doc = doc

    def resolve(self, obj, depth=0):
        """解析本地 $ref（#/components/...），最多递归 20 层。"""
        if depth > 20 or not isinstance(obj, dict):
            return obj
        if "$ref" in obj and isinstance(obj["$ref"], str) and obj["$ref"].startswith("#/"):
            node = self.doc
            for part in obj["$ref"][2:].split("/"):
                part = part.replace("~1", "/").replace("~0", "~")
                node = node.get(part, {}) if isinstance(node, dict) else {}
            merged = dict(self.resolve(node, depth + 1))
            merged.update({k: v for k, v in obj.items() if k != "$ref"})
            return merged
        return obj

    def operations(self):
        out = {}
        for path, item in (self.doc.get("paths") or {}).items():
            item = self.resolve(item)
            common = item.get("parameters", [])
            for method in ("get", "put", "post", "delete", "options", "head", "patch", "trace"):
                if method in item:
                    op = dict(self.resolve(item[method]))
                    params = [self.resolve(p) for p in common] + [self.resolve(p) for p in op.get("parameters", [])]
                    op["_params"] = {(p.get("in"), p.get("name")): p for p in params}
                    out[(path, method.upper())] = op
        return out

    def schema_props(self, schema, depth=0):
        """返回 {属性路径: 解析后的 schema}，处理 allOf 与嵌套 object；深度有限。"""
        schema = self.resolve(schema)
        props, required = {}, set()
        if not isinstance(schema, dict) or depth > 6:
            return props, required
        for sub in schema.get("allOf", []):
            p, r = self.schema_props(sub, depth + 1); props.update(p); required |= r
        if schema.get("type") == "array" and isinstance(schema.get("items"), dict):
            p, r = self.schema_props(schema["items"], depth + 1)
            props.update({f"[].{k}": v for k, v in p.items()}); required |= {f"[].{k}" for k in r}
        for name, sub in (schema.get("properties") or {}).items():
            sub = self.resolve(sub)
            props[name] = sub
            if isinstance(sub, dict) and (sub.get("type") in ("object", "array") or "allOf" in sub or "properties" in sub):
                p, r = self.schema_props(sub, depth + 1)
                props.update({f"{name}.{k}": v for k, v in p.items()})
                required |= {f"{name}.{k}" for k in r}
        required |= set(schema.get("required") or [])
        return props, required


def enum_removed(old_enum, new_enum):
    """返回新规范里被去掉的枚举取值；任一侧没有 enum 就认为没有收窄。"""
    if not isinstance(old_enum, list) or not isinstance(new_enum, list) or not old_enum or not new_enum:
        return []
    def key(v):
        return v if isinstance(v, (str, int, float, bool, type(None))) else json.dumps(v, sort_keys=True, ensure_ascii=False)
    kept = {key(v) for v in new_enum}
    return sorted((v for v in old_enum if key(v) not in kept), key=str)


def type_of(s):
    if not isinstance(s, dict):
        return None
    t = s.get("type")
    if isinstance(t, list):
        t = "|".join(sorted(map(str, t)))
    fmt = s.get("format")
    return f"{t}:{fmt}" if fmt else t


def diff(old, new):
    B, A = [], []  # breaking, additive/non-breaking

    def b(kind, where, msg): B.append({"kind": kind, "where": where, "message": msg})
    def a(kind, where, msg): A.append({"kind": kind, "where": where, "message": msg})

    o_ops, n_ops = old.operations(), new.operations()
    for key in sorted(set(o_ops) - set(n_ops)):
        b("removed-operation", f"{key[1]} {key[0]}", "接口被删除")
    for key in sorted(set(n_ops) - set(o_ops)):
        a("added-operation", f"{key[1]} {key[0]}", "新增接口")
    for key in sorted(set(o_ops) & set(n_ops)):
        where = f"{key[1]} {key[0]}"
        o, n = o_ops[key], n_ops[key]
        if n.get("deprecated") and not o.get("deprecated"):
            a("deprecated", where, "标记为 deprecated（提前告知调用方）")
        # 参数
        for pk, p in o["_params"].items():
            if pk not in n["_params"]:
                b("removed-param", where, f"参数 {pk[0]}:{pk[1]} 被删除")
                continue
            q = n["_params"][pk]
            if q.get("required") and not p.get("required"):
                b("param-now-required", where, f"参数 {pk[0]}:{pk[1]} 由可选变为必填")
            ot, nt = type_of(old.resolve(p.get("schema", {}))), type_of(new.resolve(q.get("schema", {})))
            if ot and nt and ot != nt:
                b("param-type-changed", where, f"参数 {pk[0]}:{pk[1]} 类型 {ot} → {nt}")
            gone = enum_removed(old.resolve(p.get("schema", {})).get("enum"), new.resolve(q.get("schema", {})).get("enum"))
            if gone:
                b("param-enum-narrowed", where, f"参数 {pk[1]} 枚举移除了 {gone}")
        for pk, q in n["_params"].items():
            if pk not in o["_params"]:
                if q.get("required"):
                    b("new-required-param", where, f"新增必填参数 {pk[0]}:{pk[1]}")
                else:
                    a("new-optional-param", where, f"新增可选参数 {pk[0]}:{pk[1]}")
        # 请求体
        ob = old.resolve(o.get("requestBody", {})) or {}
        nb = new.resolve(n.get("requestBody", {})) or {}
        oc, nc = ob.get("content", {}) or {}, nb.get("content", {}) or {}
        if nb.get("required") and not ob.get("required") and ob:
            b("body-now-required", where, "请求体由可选变为必填")
        for ct in oc:
            if ct not in nc:
                b("removed-request-content-type", where, f"请求体不再接受 {ct}")
        for ct in set(oc) & set(nc):
            op_, oreq = old.schema_props(oc[ct].get("schema", {}))
            np_, nreq = new.schema_props(nc[ct].get("schema", {}))
            for name in sorted(nreq - oreq):
                b("body-field-now-required", where, f"请求字段 {name} 变为必填（{ct}）")
            for name in sorted(set(op_) - set(np_)):
                a("body-field-removed", where, f"请求字段 {name} 被移除（客户端仍发送通常被忽略，需确认服务端是否报错）")
            for name in sorted(set(op_) & set(np_)):
                ot, nt = type_of(op_[name]), type_of(np_[name])
                if ot and nt and ot != nt:
                    b("body-field-type-changed", where, f"请求字段 {name} 类型 {ot} → {nt}")
                gone = enum_removed((op_[name] or {}).get("enum"), (np_[name] or {}).get("enum"))
                if gone:
                    b("body-enum-narrowed", where, f"请求字段 {name} 枚举移除了 {gone}")
            for name in sorted(set(np_) - set(op_)):
                if name not in nreq:
                    a("body-field-added", where, f"新增可选请求字段 {name}")
        # 响应
        ores, nres = o.get("responses", {}) or {}, n.get("responses", {}) or {}
        for code in ores:
            if code not in nres:
                (b if str(code).startswith("2") else a)("removed-response", where, f"响应 {code} 被移除")
        for code in set(ores) & set(nres):
            oc2 = (old.resolve(ores[code]) or {}).get("content", {}) or {}
            nc2 = (new.resolve(nres[code]) or {}).get("content", {}) or {}
            for ct in oc2:
                if ct not in nc2:
                    b("removed-response-content-type", where, f"响应 {code} 不再提供 {ct}")
            for ct in set(oc2) & set(nc2):
                op_, oreq = old.schema_props(oc2[ct].get("schema", {}))
                np_, nreq = new.schema_props(nc2[ct].get("schema", {}))
                for name in sorted(set(op_) - set(np_)):
                    b("response-field-removed", where, f"响应 {code} 字段 {name} 被移除")
                for name in sorted(set(op_) & set(np_)):
                    ot, nt = type_of(op_[name]), type_of(np_[name])
                    if ot and nt and ot != nt:
                        b("response-field-type-changed", where, f"响应 {code} 字段 {name} 类型 {ot} → {nt}")
                    if (op_[name] or {}).get("nullable") is False and (np_[name] or {}).get("nullable") is True:
                        b("response-field-nullable", where, f"响应 {code} 字段 {name} 变为可空")
                    gone = enum_removed((op_[name] or {}).get("enum"), (np_[name] or {}).get("enum"))
                    if gone:
                        b("response-enum-narrowed", where,
                          f"响应 {code} 字段 {name} 枚举移除了 {gone}（客户端可能依赖这些取值）")
                for name in sorted(oreq - nreq):
                    b("response-field-no-longer-required", where, f"响应 {code} 字段 {name} 不再保证返回")
                for name in sorted(set(np_) - set(op_)):
                    a("response-field-added", where, f"响应 {code} 新增字段 {name}")
    # 安全与服务器
    if (old.doc.get("servers") or []) != (new.doc.get("servers") or []):
        a("servers-changed", "servers", "servers 列表有变化，确认基础 URL")
    osec, nsec = old.doc.get("security"), new.doc.get("security")
    if nsec and nsec != osec:
        b("security-changed", "security", "全局 security 要求变化，可能需要新的认证方式")
    return B, A


def main():
    ap = argparse.ArgumentParser(description="OpenAPI 破坏性变更检查")
    ap.add_argument("old"); ap.add_argument("new")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true")
    a = ap.parse_args()
    old, new = Spec(load(a.old)), Spec(load(a.new))
    B, A = diff(old, new)
    if a.json:
        print(json.dumps({"breaking": B, "non_breaking": A}, ensure_ascii=False, indent=2))
    else:
        ov, nv = (old.doc.get("info") or {}).get("version"), (new.doc.get("info") or {}).get("version")
        print(f"OpenAPI 对比：{a.old}（{ov}） → {a.new}（{nv}）")
        print(f"\n破坏性变更（{len(B)}）：" if B else "\n破坏性变更：无")
        for x in B:
            print(f"  ✗ [{x['kind']}] {x['where']}: {x['message']}")
        print(f"\n非破坏性变更（{len(A)}）：" if A else "\n非破坏性变更：无")
        for x in A:
            print(f"  + [{x['kind']}] {x['where']}: {x['message']}")
        if B:
            print("\n建议：破坏性变更走新版本路径（/v2）或新字段并保留旧字段一段时间；在变更日志里逐条列出并通知调用方。")
    sys.exit(1 if (a.strict and B) else 0)


if __name__ == "__main__":
    main()

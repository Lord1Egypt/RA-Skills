# Checklist & Report Templates

## A) Progress Update Template

```markdown
### Debug Progress
- Objective:
- Current hypothesis:
- Actions executed:
  1)
  2)
- Evidence observed:
  - log:
  - command output:
  - code/config diff:
- Decision:
- Next step:
```

## B) L3 Bounded Escalation Report

```markdown
### Bounded Escalation Report

#### 1) Facts established
- 

#### 2) Options eliminated
- Option A: ... (why eliminated)
- Option B: ... (why eliminated)

#### 3) 7-point checklist evidence
- [ ] Exact error captured: <paste>
- [ ] Relevant context read: <file:line / snippet>
- [ ] Runtime prerequisites verified: <versions/paths/perms>
- [ ] Materially different approach tried: <what changed>
- [ ] Pass/fail criteria defined: <criteria>
- [ ] Validation executed: <test/command + result>
- [ ] Adjacent risk scanned: <scope + findings>

#### 4) Smallest unresolved uncertainty
- 

#### 5) Required external dependency
- secret/access/business decision needed:

#### 6) Recommendation
- Next action:
- Cost:
- Risk:
```

## C) User Clarification Request (Evidence-first)

```markdown
我已完成本地排查，当前只缺一个外部条件：<X>。

已验证证据：
- A:
- B:
- C:

请确认：
1) ...
2) ...

确认后我将执行：<next step>
```

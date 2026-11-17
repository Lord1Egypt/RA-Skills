# Reusing an existing concept across two passes

This is a fictional, authorized three-note knowledge base. Its host supports
relative Markdown links. No other notes need to be created.

Before the first pass, `essays/rehearsal.md` contains exactly:

```markdown
# Rehearsal

Shared attention made the room feel different. Shared attention took practice.
```

The existing `concepts/collective-attention.md` has title “Collective attention”
and alias “Shared attention”, and describes attention sustained by a group.
Reading it confirms the same concept. It already has this backlink:

```markdown
## Reflections

- [The rehearsal](../essays/rehearsal.md#rehearsal)
```

First pass: reuse that concept and existing fragment backlink. Wrap only the
first occurrence with a link to the actual canonical path:

```markdown
# Rehearsal

[Shared attention](../concepts/collective-attention.md) made the room feel different. Shared attention took practice.
```

The displayed essay wording, punctuation, whitespace, and paragraph order are
unchanged. No `shared-attention.md` note is created; the existing backlink is
unchanged despite its different label and heading fragment.

Second pass: resolve the first inline link to `collective-attention.md` and
the existing backlink to `rehearsal.md`. Both targets already exist; the second
mention requires no new link. The plan is empty. All file bytes and the set of
note paths remain identical to the state after pass one.

For a host using wiki links, `[[collective-attention|Shared attention]]` is the
same inline target and `[[rehearsal#Rehearsal|The rehearsal]]` is the same
reflection target after host resolution. Do not replace those merely to match
the Markdown spelling here. Ambiguous aliases remain unresolved rather than
creating a duplicate concept.

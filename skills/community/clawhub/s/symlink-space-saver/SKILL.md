---
name: "symlink-space-saver"
description: "Reduce duplicate storage by replacing safe redundant copies with symlinks. Identify the canonical copy first, verify consumers tolerate symlinks, preserve rollback, detect already-shared storage, guard against state drift, prefer atomic replacement, and prove the referenced path still works before reclaiming redundant data."
---

# Symlink Space Saver

Use this skill when multiple copies of the same large file or directory are consuming unnecessary disk space and a symlink could safely let several consumers share one canonical copy.

The goal is **deduplication without creating hidden coupling**.

A symlink saves space by turning a duplicate into a dependency. Treat that dependency as real system state.

## Core rule

> **Choose one canonical copy, prove every proposed consumer can safely follow a symlink to it, create and verify the link, then remove the redundant copy only after rollback is clear.**

Do not use symlinks merely because two paths currently contain the same bytes.

The safe loop is:

**discover → prove duplicate → inspect physical storage → choose canonical → check consumers → assess failure modes → preserve rollback → link atomically where practical → verify → reclaim → record**

**Configured is not working.**

A symlink existing is not proof that the application using it still works.

A successful hash match is not proof that the files remained unchanged until replacement.

A visible duplicate is not proof that it occupies duplicate physical storage.

---

## Trigger

Consider this skill when:

- large models, projectors, media, datasets, caches, assets, or archives exist in more than one location;
- a tool expects a fixed path but the real data already exists elsewhere;
- the user wants to reduce disk usage without reorganising every consumer;
- several applications can safely share one immutable or rarely changed object;
- an existing duplicate looks like it was copied only to satisfy path/layout expectations.

Do not trigger just to tidy small files. The added coupling is rarely worth saving a few kilobytes.

---

## 0. Start in inspect-only mode

Before changing the filesystem, produce a compact decision receipt.

Recommended form:

```text
Candidate:
Canonical proposal:
Identity proof:
Physical-storage status:
Proposed mechanism:
Expected physical saving:
Consumer(s):
Consumer symlink support:
Risk class:
Rollback plan:
State-drift sensitivity:
Platform/tool assumptions:
```

Do not mutate paths until the proposed state transition is understood.

This separates **analysis** from **execution** and makes accidental destructive changes less likely.

---

## 1. Identify the exact duplicate

Before linking anything, establish that the candidates are actually equivalent.

For files, prefer strong receipts.

### GNU/Linux examples

```sh
stat --printf='%s %n\n' -- "$a" "$b"
sha256sum -- "$a" "$b"
```

For large files where hashing is materially expensive, size + metadata may be used as a preliminary filter, but do not call two files identical from names alone.

Useful progressive checks:

```sh
stat --printf='%s\n' -- "$file"
cmp -s -- "$a" "$b"
sha256sum -- "$a" "$b"
```

For directories, compare content deliberately. A matching directory name is not evidence of identical state.

Do not deduplicate:

- files that merely have similar names;
- different model quantisations;
- architecture-specific binaries;
- files with different metadata that materially affects consumers;
- generated state that happens to match today but evolves independently.

### Directory identity is a higher-risk case

Directory deduplication is not merely "file deduplication, but recursive."

Directory symlinks can interact differently with:

- recursive tools;
- filesystem watchers;
- backup software;
- traversal policy;
- relative paths;
- permission assumptions;
- package managers;
- atomic update logic.

For directory replacement, require explicit consumer verification rather than relying on generic filesystem compatibility.

---

## 2. Detect already-shared physical storage

Before creating a new dependency, determine whether the apparent duplicates already share storage or whether the expected saving is real.

Two paths may already be:

- hard links to one inode;
- reflink / copy-on-write clones;
- sparse files;
- backed by filesystem-level deduplication;
- compressed in a way that makes logical size differ from allocated space.

Check inode/device identity where available:

```sh
ls -li -- "$a" "$b"
stat -- "$a" "$b"
```

Check allocated size rather than only apparent size:

```sh
du -h -- "$a" "$b"
du --apparent-size -h -- "$a" "$b"
```

Where the filesystem exposes reflink or extent-sharing information, use filesystem-aware tooling when the saving matters.

Do not introduce a symlink dependency to save effectively zero physical space.

Record the difference between:

```text
Logical duplicate size:
Physical allocated size:
Expected reclaimable size:
Already-shared storage detected: yes/no/unknown
```

---

## 3. Guard against state drift and TOCTOU

A duplicate proved identical at one moment may change before replacement.

For mutable-looking candidates, record state before or during identity verification:

```text
device
inode
size
mtime
optional ctime
hash
```

Immediately before replacing the consumer path, re-check the relevant state.

If device, inode, size, modification time, or other material identity changed unexpectedly:

**abort and re-prove identity.**

Do not continue from a stale hash receipt.

For actively written files or directories, prefer quiescing the writer, taking an application-supported snapshot, or declining deduplication.

This is especially important for:

- model-manager downloads still in progress;
- databases;
- logs;
- caches;
- generated artefacts;
- update-managed trees;
- files watched or rewritten by background services.

---

## 4. Choose the canonical copy

The canonical copy should be the path most likely to remain stable.

Prefer a location that is:

- intentionally maintained;
- on reliable storage;
- not a temporary/cache path;
- not routinely cleaned by another application;
- accessible by every intended consumer;
- backed up or reproducible where the data matters;
- owned and permissioned appropriately;
- unlikely to disappear when one application is uninstalled.

Avoid making these canonical without strong justification:

```text
/tmp/
/var/tmp/
browser/application caches
package build directories
download scratch directories
temporary mount points
```

If one copy is managed by a package manager, model manager, application updater, or cleanup job, understand that lifecycle before pointing unrelated consumers at it.

### Ownership matters

A canonical path is not just "the copy we kept."

Record who owns its lifecycle:

```text
Canonical path:
Lifecycle owner:
Expected mutability:
Expected cleanup/update mechanism:
Consumers:
Rollback source:
```

If nobody clearly owns the canonical copy, the proposed deduplication creates future ambiguity.

---

## 5. Decide whether symlinking is safe

A symlink is appropriate only when the consumer behaves correctly with one.

Check whether the target software:

- follows symlinks normally;
- rejects symlinks for security;
- resolves paths before applying policy;
- expects a regular file specifically;
- compares inode/device identity;
- watches the containing directory for replacement events;
- performs atomic rename/replacement updates;
- rewrites or deletes the path during upgrades;
- runs in a container/chroot/sandbox where the target path is not visible;
- crosses privilege or user boundaries;
- relies on SELinux/AppArmor/ACL/security labels;
- requires data to stay on one filesystem or mount.

Do not assume "the operating system supports symlinks" means every application supports them safely.

### Strong reasons not to symlink

Avoid or escalate for review when:

- the target is security-sensitive;
- a privileged service would follow a user-controlled link;
- either side is writable by an untrusted user/process;
- the application replaces the path during update;
- the target lives on removable/intermittent/network storage;
- the target may disappear before the consumer;
- a sandbox cannot see the link destination;
- a backup/restore tool is known to dereference or ignore symlinks incorrectly;
- the application explicitly requires a regular file;
- the link would create a loop.

Never use symlinks to weaken a permission boundary.

---

## 6. Prefer immutable or content-addressed data

The safest symlink targets are files whose meaning does not change underneath consumers.

Good candidates often include:

- large model weights;
- vision projectors;
- immutable media assets;
- read-only datasets;
- archives;
- versioned toolchains;
- content-addressed blobs.

Higher-risk candidates include:

- databases;
- lock files;
- sockets;
- PID files;
- mutable configuration;
- active logs;
- package metadata;
- application state directories;
- caches with independent cleanup policies.

If consumers expect independent mutation, use separate copies or a purpose-built shared-storage mechanism instead.

---

## 7. Check the path relationship

Inspect the existing paths before changing them:

```sh
ls -ld -- "$source" "$duplicate"
readlink -f -- "$source"
readlink -f -- "$duplicate"
findmnt -T "$source"
findmnt -T "$duplicate"
```

Confirm:

- neither path already resolves through an unexpected symlink;
- the canonical target exists;
- no link loop will be created;
- permissions permit the consuming process to traverse every parent directory;
- the target mount will be available whenever the consumer runs.

Remember that directory execute permission controls traversal.

A readable file behind an untraversable parent directory is still unusable.

### Platform assumptions

The shell examples in this skill primarily assume a **GNU/Linux userland**.

Commands such as:

```sh
stat --printf
readlink -f
findmnt
```

are not uniformly portable across macOS, BSD, BusyBox, containers, or minimal recovery environments.

Before relying on a diagnostic command:

- identify the platform/userland;
- confirm the command exists;
- confirm its flags mean what this skill assumes;
- substitute platform-native equivalents where needed.

A safety check that silently behaves differently on another platform is not a safety check.

---

## 8. Choose relative or absolute links deliberately

### Relative symlink

Prefer a relative link when the two paths move together as one tree and portability matters.

Example:

```sh
ln -s -- "../shared/model.gguf" "models/model.gguf"
```

Relative links survive moving the containing tree together.

### Absolute symlink

Prefer an absolute link when the canonical location is an intentional machine-level anchor.

Example:

```sh
ln -s -- "/srv/models/model.gguf" "$HOME/.models/model.gguf"
```

Absolute links are clearer for stable system locations but break if the canonical root moves.

Do not choose based on habit. Choose based on expected lifecycle.

---

## 9. Preserve rollback before reclaiming space

Do not delete the duplicate first.

Safe pattern for a file:

```text
duplicate exists
→ verify equality
→ capture state receipt
→ move duplicate aside
→ create replacement symlink
→ verify resolution
→ test consumer
→ keep rollback copy until acceptance
→ remove rollback copy
```

Example:

```sh
mv -- "$duplicate" "$duplicate.rollback"
ln -s -- "$canonical" "$duplicate"
```

If the consumer test fails:

```sh
rm -- "$duplicate"
mv -- "$duplicate.rollback" "$duplicate"
```

For high-value or difficult-to-reproduce data, do not make the sole remaining copy depend on an unverified storage location.

### Space pressure exception

If there is not enough free space to preserve a full rollback copy, say so before proceeding.

Possible alternatives:

- keep the canonical copy plus a manifest/hash receipt;
- use reflinks where supported;
- deduplicate only one consumer at a time;
- move the duplicate to another filesystem temporarily;
- stop and ask the user if rollback would otherwise be materially weakened.

Do not silently trade recoverability for disk space.

---

## 10. Prefer an atomic switch where practical

Avoid leaving the consumer path absent longer than necessary.

Where the platform and consumer semantics allow it:

1. move the original duplicate to a rollback name;
2. create the new symlink under a temporary sibling path;
3. verify that temporary symlink resolves correctly;
4. rename the verified symlink into the final consumer path.

Example pattern:

```sh
mv -- "$consumer_path" "$consumer_path.rollback"
ln -s -- "$canonical" "$consumer_path.new"
test -L "$consumer_path.new"
test -e "$consumer_path.new"
mv -- "$consumer_path.new" "$consumer_path"
```

A same-filesystem rename is typically the cleanest visible state transition, but do not assume every consumer tolerates replacement while running.

For live services, package managers, or watchers:

- understand whether the application observes rename events;
- stop/quiesce the consumer if required;
- test across the relevant restart boundary.

Atomic replacement narrows the interruption/race window; it does not eliminate application-level semantics.

---

## 11. Create the link narrowly

For a file:

```sh
ln -s -- "$canonical" "$consumer_path"
```

For a directory:

```sh
ln -s -- "$canonical_dir" "$consumer_dir"
```

Do not casually use `ln -sf` against an unknown destination.

Before replacing anything, inspect exactly what occupies the consumer path:

```sh
ls -ld -- "$consumer_path"
file -- "$consumer_path"
```

A force flag can overwrite a link pointing somewhere important or behave unexpectedly around directories.

Prefer explicit remove/rename + create steps where the state transition is visible.

---

## 12. Verify both filesystem and application behaviour

First verify the link mechanically:

```sh
test -L "$consumer_path"
test -e "$consumer_path"
readlink -- "$consumer_path"
readlink -f -- "$consumer_path"
```

Then verify the real consumer.

Examples:

- load the model through the application that uses the consumer path;
- restart the relevant service and confirm it opens the file;
- run the import/index operation;
- exercise the media/project path;
- run the application's own validation command.

Weak:

```text
readlink shows the expected target.
```

Better:

```text
The application opened the symlinked 18.5 GB model and completed the expected inference/import operation.
```

If the consumer has a restart boundary, test through it where practical.

### Acceptance requires a receipt

Record what actually proved the replacement worked.

Recommended form:

```text
Consumer:
Consumer path:
Resolved canonical target:
Mechanical link checks:
Application test:
Command / action:
Exit status / observed result:
Restart boundary tested: yes/no/not applicable
Test timestamp:
Verifier:
Outstanding caveats:
```

A configured verifier is not evidence that verification happened.

An application opening the path once may still be insufficient if the real failure mode occurs during restart, upgrade, cleanup, or watcher refresh.

Test the boundary that matters.

---

## 13. Reclaim space only after acceptance

Once the symlink and application behaviour have passed:

1. verify the canonical copy still exists;
2. re-check state if drift is plausible;
3. record a hash/size if future identity matters;
4. remove the rollback duplicate;
5. measure reclaimed physical space;
6. re-run the consumer test if deletion changed filesystem state materially.

Example:

```sh
rm -- "$duplicate.rollback"
du -sh -- "$canonical"
df -h -- "$(dirname "$canonical")"
```

Do not report space reclaimed merely from apparent file sizes.

Sparse files, compression, reflinks, hard links, and filesystem deduplication can make logical and physical usage differ.

Where it matters, use filesystem-aware tools to confirm actual storage impact.

---

## Symlink vs hard link vs reflink

A symlink is not always the best deduplication mechanism.

### Symlink

Use when:

- consumers can follow links;
- a visible canonical path is desirable;
- cross-filesystem references are needed.

Trade-off: target removal breaks consumers.

### Hard link

Use when:

- the data is a regular file;
- paths are on the same filesystem;
- identical inode identity is acceptable.

Trade-off: changes through either path affect the same inode, and directory hard links are normally unavailable.

Before creating one, check whether the paths are already hard-linked.

### Reflink / copy-on-write clone

Use when:

- the filesystem supports it;
- consumers need independent-looking regular files;
- later divergence is possible.

Example where supported:

```sh
cp --reflink=always -- "$source" "$dest"
```

Trade-off: not universally supported, and later writes consume additional space.

Choose the mechanism that matches the consumer contract, not merely the one with the smallest immediate disk usage.

---

## Model and AI asset guidance

Large model ecosystems are particularly good candidates for safe deduplication because weights are often immutable and expensive to duplicate.

Before linking GGUFs, projectors, adapters, or checkpoints:

- verify hashes or exact file identity;
- distinguish model weights from mutable manager metadata;
- confirm the serving/import tool follows symlinks;
- confirm its watcher/indexer notices the linked path;
- check whether the manager copies/imports the data into a separate content-addressed store anyway;
- check whether the apparent duplicate is already a hardlink/reflink/content-addressed reference;
- do not point several logical model IDs at one file unless they truly represent the same artefact;
- keep manager-owned manifests/databases separate unless their format explicitly supports sharing.

If an importer monitors a directory, test whether creating a symlink triggers the expected import.

Some watchers react differently to links than to new regular files.

If a model manager may update or replace the target, record that manager as the lifecycle owner and re-check the dependency after upgrades.

---

## Privileged paths

If either the canonical path or consumer path requires root-level mutation, apply the privileged-operations rules.

The privilege boundary must remain visible to the user.

Do not use elevated symlink creation to bridge a security boundary such as:

```text
root-owned service → user-writable target
```

without explicitly analysing the security consequences.

A privileged process following a mutable user-controlled symlink can turn a space-saving optimisation into an escalation path.

---

## Failure modes to actively check

### Broken target

```sh
test -e "$consumer_path"
```

A symlink itself may exist while its target does not.

### Link loop

Use:

```sh
readlink -f -- "$consumer_path"
```

Failure to resolve can indicate a loop or missing component.

### State changed after duplicate proof

Re-check the recorded device/inode/size/mtime receipt before replacement.

If it changed unexpectedly, re-prove identity.

### Already-shared storage

Do not assume logical duplicates consume independent extents.

Check inode identity, allocated blocks, reflink behaviour, or filesystem deduplication before promising meaningful savings.

### Cleanup job deletes canonical data

Identify cleanup policies before linking caches or manager-owned content.

### Application replaces the link

An updater may unlink the symlink and write a new regular file at the consumer path.

Re-check after upgrades when this behaviour is plausible.

### Permissions changed

All consumers must retain traverse/read/write permissions appropriate to their use.

### Mount unavailable

Links crossing mounts fail when the target filesystem is absent.

### Backup semantics differ

Know whether backup tooling stores the symlink itself or dereferences the target.

### Directory traversal differs

Backup, packaging, indexing, and recursive-copy tools may treat a symlinked directory differently from a real directory.

Treat directory replacements as a higher-risk class.

### Platform command mismatch

A diagnostic command that is unavailable or behaves differently can invalidate the safety procedure.

Verify the platform assumptions before acting.

---

## Record the dependency when it is non-obvious

A useful durable record is compact:

```text
Consumer:
Symlink:
Canonical target:
Reason:
Identity receipt:
Physical-storage receipt:
Lifecycle owner:
Verified by:
Application acceptance receipt:
Rollback/rebuild:
Platform:
State-drift sensitive: yes/no
Drift-sensitive as of:
```

Do not record every obvious project-local symlink.

Record links that:

- save substantial space;
- cross application boundaries;
- cross mount/filesystem boundaries;
- depend on manager-owned storage;
- would be surprising during recovery;
- could be broken by cleanup or upgrade behaviour.

The next agent should not "fix" a deliberate symlink by copying another 20 GB file back into place.

---

## Decision standard

Before deduplicating, the answer to each of these should be explicit:

```text
Are these objects actually identical?
Are they still identical now?
Are they already sharing physical storage?
Which copy owns the lifecycle?
Will every consumer follow the proposed mechanism safely?
Does the link cross a trust, sandbox, mount, or privilege boundary?
Can the original state be restored?
Can the switch be made without a dangerous race window?
Did the real consumer pass?
Was acceptance recorded?
Was physical space actually reclaimed?
```

If one of the load-bearing answers is unknown, do not paper over it with confidence.

Investigate it, reduce scope, or leave the duplicate alone.

---

## Operating rules

- **A duplicate may be removable; a dependency must be understood.**
- **Configured is not working.**
- **Choose the canonical owner before creating consumers.**
- **Prove identity before deduplicating.**
- **Re-check identity when state drift is plausible.**
- **Detect already-shared physical storage before introducing new coupling.**
- **Prefer immutable data.**
- **Treat directory replacement as higher risk than file replacement.**
- **Do not delete first and test later.**
- **Prefer a narrow, atomic state transition where practical.**
- **A valid symlink is not proof the application works.**
- **Test through the real consumer and record the acceptance receipt.**
- **Do not bridge trust boundaries with writable symlinks.**
- **Preserve rollback until acceptance.**
- **Record surprising cross-application dependencies.**
- **Measure physical savings, not just apparent file size.**
- **Save space without creating invisible fragility.**

# Scenes And Recovery

Recommended templates are read-only, capability-adapted recipes: 回家、离家、日常、
会客、清洁、深夜归家、阅读、品茗、观影、聚会、夜灯、早安. They are not claims
about a user's mood, presence, sleep, or routine.

Custom scenes use complete replacement updates and revisions. Template targets resolve
current home/room/group membership when applied. Snapshot scenes read fresh state and
pin explicit stable device IDs for the home, a room, a compatible group, a device
subset, or one device. Dynamic flows are saved only when their readable state can
reconstruct them.

Before a multi-device apply, the runtime stores verified pre-state, capability
fingerprints, requested actions, and touched/pending rows. The operation is not
transactional across devices. `operation.recover` requires an explicit confirmation,
fresh reads, and a known pre/post transition. External state drift returns
`conflict`/`uncertain` and preserves the record.

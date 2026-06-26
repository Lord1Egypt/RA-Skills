"""
SignaAI protocol messages.

This module is intentionally network-free. It gives developers stable,
structured builders and parsers for the compact on-chain messages used by the
SDK, examples, indexers, and future OpenClaw skills.
"""
from dataclasses import dataclass


PROOF_PREFIX = "SIGPROOF:v1:"
ESCROW_PREFIX = "ESCROW:"
TASK_PREFIX = "TASK:"
TASK_COMPLETE_PREFIX = "TASK_COMPLETE:"
ARBIT_OPEN_PREFIX = "ARBIT_OPEN:"
ARBIT_VOTE_PREFIX = "ARBIT_VOTE:"
ARBIT_CLOSE_PREFIX = "ARBIT_CLOSE:"


class ProtocolError(ValueError):
    """Raised when a SignaAI protocol message cannot be parsed."""


@dataclass(frozen=True)
class SigProof:
    content_hash: str
    sources_hash: str = ""
    label: str = ""
    version: str = "v1"

    kind = "sigproof"

    def to_message(self):
        return build_sigproof(self.content_hash, self.sources_hash, self.label)


@dataclass(frozen=True)
class EscrowMessage:
    action: str
    escrow_id: str
    version: str = ""
    worker: str = ""
    amount_nqt: int = 0
    task_hash: str = ""
    deadline_block: int = 0
    operator: str = ""
    result_hash: str = ""
    proof_tx: str = ""
    participant: str = ""
    task_description: str = ""

    kind = "escrow"

    def to_message(self):
        return build_escrow_message(self)


@dataclass(frozen=True)
class TaskComplete:
    task_id: str
    result_hash: str
    rating: int

    kind = "task_complete"

    def to_message(self):
        return build_task_complete(self.task_id, self.result_hash, self.rating)


@dataclass(frozen=True)
class ArbitrationMessage:
    action: str
    escrow_id: str
    claimant: str = ""
    arbitrator: str = ""
    decision: str = ""
    reason_hash: str = ""
    notes_hash: str = ""

    kind = "arbitration"

    def to_message(self):
        return build_arbitration_message(self)


@dataclass(frozen=True)
class TaskMessage:
    """
    A TASK board protocol message.

    action: OPEN | CLAIM | ACCEPT | CANCEL
    """
    action: str
    task_id: str
    version: str = "v1"
    payer_address: str = ""
    capability_tag: str = ""
    amount_nqt: int = 0
    deadline_block: int = 0
    task_hash: str = ""
    worker_address: str = ""
    task_summary: str = ""

    kind = "task"

    def to_message(self):
        return build_task_message(self)


@dataclass(frozen=True)
class UnknownMessage:
    raw: str

    kind = "unknown"

    def to_message(self):
        return self.raw


def sanitize_label(label, limit=40):
    """Make a label safe for colon-delimited on-chain messages."""
    return (label or "")[:limit].replace(":", "-")


def parse_message(message, strict=False):
    """Parse any known SignaAI protocol message."""
    if message.startswith(PROOF_PREFIX):
        return parse_sigproof(message)
    if message.startswith(ESCROW_PREFIX):
        return parse_escrow(message)
    if message.startswith(TASK_PREFIX) and not message.startswith(TASK_COMPLETE_PREFIX):
        return parse_task(message)
    if message.startswith(TASK_COMPLETE_PREFIX):
        return parse_task_complete(message)
    if (message.startswith(ARBIT_OPEN_PREFIX) or
            message.startswith(ARBIT_VOTE_PREFIX) or
            message.startswith(ARBIT_CLOSE_PREFIX)):
        return parse_arbitration(message)
    if strict:
        raise ProtocolError("Unknown SignaAI protocol message")
    return UnknownMessage(message)


def build_sigproof(content_hash, sources_hash="", label=""):
    return f"{PROOF_PREFIX}{content_hash}:{sources_hash}:{sanitize_label(label)}"


def parse_sigproof(message):
    if not message.startswith(PROOF_PREFIX):
        raise ProtocolError("Not a SIGPROOF message")
    parts = message[len(PROOF_PREFIX):].split(":")
    if len(parts) < 2:
        raise ProtocolError("Malformed SIGPROOF message")
    return SigProof(
        content_hash=parts[0],
        sources_hash=parts[1],
        label=":".join(parts[2:]) if len(parts) > 2 else "",
    )


def build_escrow_create(escrow_id, worker, amount_nqt, task_hash,
                        deadline_block, operator="", task_description=""):
    msg = f"{ESCROW_PREFIX}CREATE:{escrow_id}:{worker}:{int(amount_nqt)}:{task_hash}:{int(deadline_block)}"
    if task_description:
        # Always include operator field (possibly empty) so task_description is at a fixed index
        return f"{msg}:{operator}:{task_description}"
    return f"{msg}:{operator}" if operator else msg


def build_escrow_fund(escrow_id):
    return f"{ESCROW_PREFIX}FUND:{escrow_id}"


def build_escrow_submit(escrow_id, result_hash, proof_tx=""):
    msg = f"{ESCROW_PREFIX}SUBMIT:{escrow_id}:{result_hash}"
    return f"{msg}:{proof_tx}" if proof_tx else msg


def build_escrow_release(escrow_id, worker):
    return f"{ESCROW_PREFIX}RELEASE:{escrow_id}:{worker}"


def build_escrow_refund(escrow_id, payer):
    return f"{ESCROW_PREFIX}REFUND:{escrow_id}:{payer}"


def build_escrow_assign(escrow_id, task_hash, task_description="",
                        version="v1"):
    if version:
        return f"{ESCROW_PREFIX}ASSIGN:{version}:{escrow_id}:{task_hash}:{task_description}"
    return f"{ESCROW_PREFIX}ASSIGN:{escrow_id}:{task_hash}:{task_description}"


def build_escrow_message(msg):
    action = msg.action.upper()
    if action == "CREATE":
        return build_escrow_create(
            msg.escrow_id, msg.worker, msg.amount_nqt, msg.task_hash,
            msg.deadline_block, msg.operator, msg.task_description
        )
    if action == "FUND":
        return build_escrow_fund(msg.escrow_id)
    if action == "SUBMIT":
        return build_escrow_submit(msg.escrow_id, msg.result_hash, msg.proof_tx)
    if action == "RELEASE":
        return build_escrow_release(msg.escrow_id, msg.worker or msg.participant)
    if action == "REFUND":
        return build_escrow_refund(msg.escrow_id, msg.participant)
    if action == "ASSIGN":
        return build_escrow_assign(
            msg.escrow_id, msg.task_hash, msg.task_description, msg.version
        )
    raise ProtocolError(f"Unsupported escrow action: {msg.action}")


def parse_escrow(message):
    if not message.startswith(ESCROW_PREFIX):
        raise ProtocolError("Not an ESCROW message")

    parts = message[len(ESCROW_PREFIX):].split(":")
    if len(parts) < 2:
        raise ProtocolError("Malformed ESCROW message")

    action = parts[0].upper()
    version = parts[1] if len(parts) > 2 and parts[1].startswith("v") else ""
    payload = parts[2:] if version else parts[1:]
    if not payload:
        raise ProtocolError("ESCROW message missing escrow id")

    escrow_id = payload[0]
    if action == "CREATE":
        if len(payload) < 5:
            raise ProtocolError("Malformed ESCROW CREATE message")
        return EscrowMessage(
            action=action,
            escrow_id=escrow_id,
            version=version,
            worker=payload[1],
            amount_nqt=_int_or_zero(payload[2]),
            task_hash=payload[3],
            deadline_block=_int_or_zero(payload[4]),
            operator=payload[5] if len(payload) > 5 else "",
            task_description=":".join(payload[6:]) if len(payload) > 6 else "",
        )
    if action == "FUND":
        return EscrowMessage(action=action, escrow_id=escrow_id, version=version)
    if action == "SUBMIT":
        if len(payload) < 2:
            raise ProtocolError("Malformed ESCROW SUBMIT message")
        return EscrowMessage(
            action=action,
            escrow_id=escrow_id,
            version=version,
            result_hash=payload[1],
            proof_tx=payload[2] if len(payload) > 2 else "",
        )
    if action == "RELEASE":
        return EscrowMessage(
            action=action,
            escrow_id=escrow_id,
            version=version,
            worker=payload[1] if len(payload) > 1 else "",
            participant=payload[1] if len(payload) > 1 else "",
        )
    if action == "REFUND":
        return EscrowMessage(
            action=action,
            escrow_id=escrow_id,
            version=version,
            participant=payload[1] if len(payload) > 1 else "",
        )
    if action == "ASSIGN":
        if len(payload) < 2:
            raise ProtocolError("Malformed ESCROW ASSIGN message")
        return EscrowMessage(
            action=action,
            escrow_id=escrow_id,
            version=version,
            task_hash=payload[1],
            task_description=":".join(payload[2:]) if len(payload) > 2 else "",
        )
    raise ProtocolError(f"Unsupported escrow action: {action}")


def build_task_complete(task_id, result_hash, rating):
    try:
        rating = int(rating)
    except (TypeError, ValueError) as exc:
        raise ProtocolError("Rating must be an integer") from exc
    if rating < 1 or rating > 5:
        raise ProtocolError("Rating must be between 1 and 5")
    return f"{TASK_COMPLETE_PREFIX}{task_id}:{result_hash}:{rating}"


def parse_task_complete(message):
    if not message.startswith(TASK_COMPLETE_PREFIX):
        raise ProtocolError("Not a TASK_COMPLETE message")
    parts = message[len(TASK_COMPLETE_PREFIX):].split(":")
    if len(parts) < 3:
        raise ProtocolError("Malformed TASK_COMPLETE message")
    try:
        rating = int(parts[2])
    except ValueError as exc:
        raise ProtocolError("Rating must be an integer") from exc
    if rating < 1 or rating > 5:
        raise ProtocolError("Rating must be between 1 and 5")
    return TaskComplete(
        task_id=parts[0],
        result_hash=parts[1],
        rating=rating,
    )


def build_arbit_open(escrow_id, claimant, reason_hash):
    return f"{ARBIT_OPEN_PREFIX}{escrow_id}:{claimant}:{reason_hash}"


def build_arbit_vote(escrow_id, decision, notes_hash="none"):
    decision = decision.upper()
    if decision not in ("RELEASE", "REFUND"):
        raise ProtocolError("Decision must be RELEASE or REFUND")
    return f"{ARBIT_VOTE_PREFIX}{escrow_id}:{decision}:{notes_hash or 'none'}"


def build_arbit_close(escrow_id, decision, arbitrator):
    decision = decision.upper()
    if decision not in ("RELEASE", "REFUND"):
        raise ProtocolError("Decision must be RELEASE or REFUND")
    return f"{ARBIT_CLOSE_PREFIX}{escrow_id}:{decision}:{arbitrator}"


def build_arbitration_message(msg):
    action = msg.action.upper()
    if action == "OPEN":
        return build_arbit_open(msg.escrow_id, msg.claimant, msg.reason_hash)
    if action == "VOTE":
        return build_arbit_vote(msg.escrow_id, msg.decision, msg.notes_hash)
    if action == "CLOSE":
        return build_arbit_close(msg.escrow_id, msg.decision, msg.arbitrator)
    raise ProtocolError(f"Unsupported arbitration action: {msg.action}")


def parse_arbitration(message):
    if message.startswith(ARBIT_OPEN_PREFIX):
        parts = message[len(ARBIT_OPEN_PREFIX):].split(":")
        if len(parts) < 3:
            raise ProtocolError("Malformed ARBIT_OPEN message")
        return ArbitrationMessage(
            action="OPEN",
            escrow_id=parts[0],
            claimant=parts[1],
            reason_hash=parts[2],
        )
    if message.startswith(ARBIT_VOTE_PREFIX):
        parts = message[len(ARBIT_VOTE_PREFIX):].split(":")
        if len(parts) < 3:
            raise ProtocolError("Malformed ARBIT_VOTE message")
        return ArbitrationMessage(
            action="VOTE",
            escrow_id=parts[0],
            decision=parts[1],
            notes_hash=parts[2],
        )
    if message.startswith(ARBIT_CLOSE_PREFIX):
        parts = message[len(ARBIT_CLOSE_PREFIX):].split(":")
        if len(parts) < 3:
            raise ProtocolError("Malformed ARBIT_CLOSE message")
        return ArbitrationMessage(
            action="CLOSE",
            escrow_id=parts[0],
            decision=parts[1],
            arbitrator=parts[2],
        )
    raise ProtocolError("Not an arbitration message")


def _int_or_zero(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


# ── TASK board protocol ───────────────────────────────────────────────────────

def build_task_open(task_id, payer_address, capability_tag,
                    amount_nqt, deadline_block, task_hash,
                    version="v1", task_summary=""):
    """TASK:OPEN:v1:<task_id>:<payer>:<capability>:<amount_nqt>:<deadline_block>:<task_hash>[:<summary>]"""
    cap = (capability_tag or "").replace(":", "-")
    base = (f"{TASK_PREFIX}OPEN:{version}:{task_id}:{payer_address}"
            f":{cap}:{int(amount_nqt)}:{int(deadline_block)}:{task_hash}")
    if task_summary:
        return f"{base}:{sanitize_label(task_summary, 200)}"
    return base


def build_task_claim(task_id, worker_address, version="v1"):
    """TASK:CLAIM:v1:<task_id>:<worker_address>"""
    return f"{TASK_PREFIX}CLAIM:{version}:{task_id}:{worker_address}"


def build_task_accept(task_id, worker_address, version="v1"):
    """TASK:ACCEPT:v1:<task_id>:<worker_address>"""
    return f"{TASK_PREFIX}ACCEPT:{version}:{task_id}:{worker_address}"


def build_task_cancel(task_id, version="v1"):
    """TASK:CANCEL:v1:<task_id>"""
    return f"{TASK_PREFIX}CANCEL:{version}:{task_id}"


def build_task_message(msg):
    action = msg.action.upper()
    if action == "OPEN":
        return build_task_open(msg.task_id, msg.payer_address, msg.capability_tag,
                               msg.amount_nqt, msg.deadline_block, msg.task_hash,
                               msg.version)
    if action == "CLAIM":
        return build_task_claim(msg.task_id, msg.worker_address, msg.version)
    if action == "ACCEPT":
        return build_task_accept(msg.task_id, msg.worker_address, msg.version)
    if action == "CANCEL":
        return build_task_cancel(msg.task_id, msg.version)
    raise ProtocolError(f"Unsupported task action: {action}")


def parse_task(message):
    """Parse a TASK: board protocol message."""
    if not message.startswith(TASK_PREFIX):
        raise ProtocolError("Not a TASK message")
    parts = message[len(TASK_PREFIX):].split(":")
    if len(parts) < 2:
        raise ProtocolError("Malformed TASK message")

    action = parts[0].upper()
    version = parts[1] if len(parts) > 2 and parts[1].startswith("v") else "v1"
    payload = parts[2:] if version else parts[1:]

    if not payload:
        raise ProtocolError("TASK message missing task_id")

    task_id = payload[0]

    if action == "OPEN":
        # payload: task_id, payer, capability, amount_nqt, deadline_block, task_hash[, summary]
        if len(payload) < 6:
            raise ProtocolError("Malformed TASK:OPEN message")
        return TaskMessage(
            action=action,
            task_id=task_id,
            version=version,
            payer_address=payload[1],
            capability_tag=payload[2],
            amount_nqt=_int_or_zero(payload[3]),
            deadline_block=_int_or_zero(payload[4]),
            task_hash=payload[5],
            task_summary=payload[6] if len(payload) > 6 else "",
        )
    if action in ("CLAIM", "ACCEPT"):
        if len(payload) < 2:
            raise ProtocolError(f"Malformed TASK:{action} message")
        return TaskMessage(
            action=action,
            task_id=task_id,
            version=version,
            worker_address=payload[1],
        )
    if action == "CANCEL":
        return TaskMessage(action=action, task_id=task_id, version=version)

    raise ProtocolError(f"Unsupported task action: {action}")

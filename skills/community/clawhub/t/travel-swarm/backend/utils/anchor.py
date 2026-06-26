from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class AnchorData:
    """5W2H 确定性数学锚点"""
    who: str = ""; who_confirmed: bool = False
    why: str = ""; why_confirmed: bool = False
    what: str = ""; what_confirmed: bool = False
    where: str = ""; where_confirmed: bool = False
    when: str = ""; when_confirmed: bool = False
    how: str = ""; how_confirmed: bool = False
    how_much: str = ""; how_much_confirmed: bool = False

    @property
    def convergence_rate(self) -> float:
        fields = [self.who_confirmed, self.why_confirmed, self.what_confirmed,
                  self.where_confirmed, self.when_confirmed, self.how_confirmed, self.how_much_confirmed]
        return sum(fields) / len(fields)

    def get_missing_dimensions(self) -> List[str]:
        mapping = {"who": self.who_confirmed, "why": self.why_confirmed, "what": self.what_confirmed,
                   "where": self.where_confirmed, "when": self.when_confirmed, "how": self.how_confirmed, "how_much": self.how_much_confirmed}
        return [k for k, v in mapping.items() if not v]

    def update_from_extraction(self, extracted: Dict[str, Any]) -> None:
        for field in ["who", "why", "what", "where", "when", "how", "how_much"]:
            if not getattr(self, f"{field}_confirmed") and extracted.get(field):
                value = str(extracted[field]).strip()
                if value:
                    setattr(self, field, value)
                    setattr(self, f"{field}_confirmed", True)

    def to_dict(self) -> Dict:
        return {
            "who": self.who, "why": self.why, "what": self.what, "where": self.where,
            "when": self.when, "how": self.how, "how_much": self.how_much,
            "convergence_rate": self.convergence_rate, "missing": self.get_missing_dimensions()
        }
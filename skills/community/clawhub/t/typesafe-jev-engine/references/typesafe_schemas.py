from typing import Literal, Dict, Any, List
from pydantic import BaseModel, Field

class BrandContextJudgment(BaseModel):
    brand: Literal["service_a", "service_b", "general"] = Field(
        description="Identifica a qual ecossistema ou marca o assunto pertence."
    )
    urgency: Literal["alta", "media", "baixa"] = Field(description="Nível de prioridade.")
    action_required: str = Field(description="Ação imediata recomendada.")

class MelTaskPlan(BaseModel):
    task_category: Literal["ads_management", "messaging", "infrastructure", "code_dev", "general"] = Field(
        description="Categoria da tarefa solicitada."
    )
    tools_required: List[str] = Field(description="Ferramentas necessárias.")
    requires_user_confirmation: bool = Field(description="Exige aprovação prévia para ações sensíveis.")

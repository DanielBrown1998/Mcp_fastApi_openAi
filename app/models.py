from pydantic import BaseModel, Field
from typing import List, Literal

# Modelos para cada parte estruturada do protocolo
class SystemInstructions(BaseModel):
    persona: str = "Você é um assistente de IA colaborativo e preciso."
    rules: List[str] = Field(default_factory=list)

class ConversationHistoryItem(BaseModel):
    role: Literal["user", "assistant"]
    content: str

class RetrievedKnowledge(BaseModel):
    source: str
    content: str

# O modelo principal que representa o contexto completo do MCP
class MCPContext(BaseModel):
    instructions: SystemInstructions
    history: List[ConversationHistoryItem] = Field(default_factory=list) # type: ignore
    knowledge: List[RetrievedKnowledge] = Field(default_factory=list) # type: ignore
    user_query: str

    def build_prompt(self) -> str:
        """
        Converte o objeto de contexto estruturado em um prompt de texto formatado
        para o LLM.
        """
        prompt_parts = []

        # 1. Instruções do Sistema
        prompt_parts.append("<system_instructions>") # type: ignore
        prompt_parts.append(f"<persona>{self.instructions.persona}</persona>")# type: ignore
        for rule in self.instructions.rules:# type: ignore
            prompt_parts.append(f"<rule>{rule}</rule>")# type: ignore
        prompt_parts.append("</system_instructions>\n")# type: ignore

        # 2. Conhecimento Recuperado (RAG)
        if self.knowledge:
            prompt_parts.append("<retrieved_knowledge>")# type: ignore
            for item in self.knowledge:
                prompt_parts.append(f'<document source="{item.source}">')# type: ignore
                prompt_parts.append(item.content)# type: ignore
                prompt_parts.append("</document>")# type: ignore
            prompt_parts.append("</retrieved_knowledge>\n")# type: ignore

        # 3. Histórico da Conversa
        if self.history:
            prompt_parts.append("<conversation_history>")# type: ignore
            for item in self.history:
                prompt_parts.append(f"<turn role='{item.role}'>{item.content}</turn>")# type: ignore
            prompt_parts.append("</conversation_history>\n")# type: ignore

        # 4. Pergunta do Usuário
        prompt_parts.append("<user_query>")# type: ignore
        prompt_parts.append(self.user_query)# type: ignore
        prompt_parts.append("</user_query>")# type: ignore

        return "\n".join(prompt_parts)# type: ignore

# Modelo para o corpo da requisição da API
class QueryRequest(BaseModel):
    query: str
    user_id: str | None = None # Opcional, para simular busca de histórico
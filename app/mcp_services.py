from .models import (
    MCPContext,
    SystemInstructions,
    ConversationHistoryItem,
    RetrievedKnowledge,
)

# --- DADOS SIMULADOS (Em um app real, isso viria de um banco de dados) ---
FAKE_KNOWLEDGE_DB = {
    "fastapi": RetrievedKnowledge(
        source="documentacao_interna.pdf",
        content="FastAPI é um framework web moderno e rápido para Python 3.8+ baseado em type hints. Ele é construído sobre Starlette (para a parte web) e Pydantic (para a validação de dados)."
    )
}
FAKE_HISTORY_DB = {
    "user123": [
        ConversationHistoryItem(role="user", content="Olá, quem é você?"),
        ConversationHistoryItem(role="assistant", content="Eu sou um assistente de IA."),
    ]
}
# -----------------------------------------------------------------------

class MCPService:
    def assemble_context(self, query: str, user_id: str | None = None) -> MCPContext:
        """
        Orquestra a montagem do contexto MCP.
        """
        # 1. Define as instruções do sistema
        instructions = SystemInstructions(
            persona="Você é um assistente de programação especializado em Python, FastApi, Flutter e Dart.",
            rules=["Seja amigável.", "Forneça exemplos de código quando aplicável."]
        )

        # 2. Busca o histórico do usuário (simulado)
        history = FAKE_HISTORY_DB.get(user_id, []) if user_id else []

        # 3. Busca conhecimento relevante (RAG simulado)
        knowledge = []
        if "fastapi" in query.lower():
            knowledge.append(FAKE_KNOWLEDGE_DB["fastapi"])# type: ignore

        # 4. Monta e retorna o objeto MCPContext
        context = MCPContext(
            instructions=instructions,
            history=history,
            knowledge=knowledge,# type: ignore
            user_query=query,
        )
        return context
from fastapi import FastAPI, HTTPException
from .models import QueryRequest
from .mcp_services import MCPService
from .llm_client import LLMClientGoogle

# Inicializa a aplicação FastAPI
app = FastAPI(
    title="MCP Service API",
    description="Uma API para demonstrar o Model Context Protocol com FastAPI utilizando o Google Gemini."
)

mcp_service = MCPService()
llm_client = LLMClientGoogle()

@app.post("/generate", summary="Gera uma resposta de IA usando MCP")
async def generate_response(request: QueryRequest):
    """
    Recebe uma query, monta o contexto usando MCP, e retorna a resposta do LLM.
    """
    try:
        context_object = mcp_service.assemble_context(query=request.query, user_id=request.user_id)
        
        final_prompt = context_object.build_prompt()

        print("--- PROMPT ESTRUTURADO ENVIADO AO LLM ---")
        print(final_prompt)
        print("------------------------------------------")

        llm_response = await llm_client.get_completion(final_prompt)

        return {
            "response": llm_response,
            "prompt_used": final_prompt  # Retorna o prompt para fins de debug
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/", summary="Endpoint de saúde da aplicação")
def read_root():
    return {"status": "MCP Service is running"}
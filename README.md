# API de Serviço MCP com FastAPI e Google Gemini

Esta é uma API de exemplo que demonstra a implementação do "Model Context Protocol" (MCP) usando FastAPI e o Google Gemini como modelo de linguagem. A API recebe uma consulta do usuário, monta um contexto estruturado e o utiliza para gerar uma resposta de um modelo de linguagem.

## O que é o "Model Context Protocol" (MCP)?

O MCP é uma abordagem para estruturar as informações enviadas a um modelo de linguagem (LLM) para garantir que o modelo tenha todo o contexto necessário para gerar uma resposta precisa e relevante. Este projeto implementa o MCP com as seguintes seções:

- **Instruções do Sistema**: Define a persona e as regras que o LLM deve seguir.
- **Conhecimento Recuperado (RAG)**: Fornece ao LLM informações de uma base de conhecimento externa (neste exemplo, simulada) para responder à consulta.
- **Histórico da Conversa**: Inclui o histórico de interações do usuário com o LLM para manter o contexto da conversa.
- **Consulta do Usuário**: A pergunta ou instrução específica do usuário.

## Como executar o projeto

### Pré-requisitos

- Python 3.8+
- Uma chave de API do Google Gemini

### 1. Clone o repositório

```bash
git clone <URL_DO_REPOSITORIO>
cd Mcp_fastApi_openAi
```

### 2. Crie e ative um ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
```

### 3. Instale as dependências

Crie um arquivo `requirements.txt` com o seguinte conteúdo:

```
fastapi
uvicorn
pydantic
python-dotenv
google-generativeai
openai
```

E instale as dependências:

```bash
pip install -r requirements.txt
```

### 4. Configure suas variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto e adicione sua chave de API do Google Gemini:

```
GOOGLE_API_KEY="SUA_CHAVE_DE_API_AQUI"
```

### 5. Execute a aplicação

```bash
uvicorn app.main:app --reload
```

A API estará disponível em `http://127.0.0.1:8000`.

## Como usar a API

Você pode acessar a documentação interativa da API em `http://127.0.0.1:8000/docs`.

### Exemplo de requisição com `curl`

```bash
curl -X POST "http://127.0.0.1:8000/generate" -H "Content-Type: application/json" -d '{
  "query": "o que é fastapi?",
  "user_id": "user123"
}'
```

### Exemplo de resposta

```json
{
  "response": "FastAPI é um framework web moderno e rápido para Python 3.8+...",
  "prompt_used": "<system_instructions>\n<persona>Você é um assistente de programação...</persona>..."
}
```
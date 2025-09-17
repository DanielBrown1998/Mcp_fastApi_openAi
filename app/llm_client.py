import os
import google.generativeai as genai
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()


class LLMClientOpenAi:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("A chave de API da OpenAI não foi encontrada. Verifique seu arquivo .env")
        # Usamos AsyncOpenAI para compatibilidade com o FastAPI assíncrono
        self.client = AsyncOpenAI(api_key=api_key)

    async def get_completion(self, prompt: str) -> str:
        try:
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo", # ou "gpt-4", etc.
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
            )
            return response.choices[0].message.content or "Não foi possível obter uma resposta."
        except Exception as e:
            print(f"Ocorreu um erro ao chamar a API da OpenAi: {e}")
            return "Desculpe, ocorreu um erro ao processar sua solicitação."


class LLMClientGoogle:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("A chave de API do Google não foi encontrada. Verifique seu arquivo .env")
        
        genai.configure(api_key=api_key) # type: ignore
        
        self.model = genai.GenerativeModel(model_name='gemini-1.5-flash') # type: ignore

    async def get_completion(self, prompt: str) -> str:
        """
        Envia o prompt para a API do Gemini e retorna a resposta de texto.
        """
        try:
            response = await self.model.generate_content_async(prompt)  # type: ignore
            
            if response.parts:
                return response.text
            else:
                return "A resposta foi bloqueada ou não contém texto. Verifique o prompt."
                
        except Exception as e:
            print(f"Ocorreu um erro detalhado ao chamar a API do Gemini: {type(e).__name__} - {e}")
            return "Desculpe, ocorreu um erro ao processar sua solicitação com o Gemini."
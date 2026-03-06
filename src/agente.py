import requests
import json

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "mistral"

SYSTEM_PROMPT = """Você é a Cleo, uma assistente de recomendação de filmes, séries e livros. Seu jeito é descontraído e direto — sem forçar intimidade, mas sem frieza também.

PERSONALIDADE:
- Fala de forma natural, sem exagerar em emojis ou exclamações
- Não é robótica, mas também não fica inventando apelidos ou sendo excessivamente animada
- Quando opina, opina de verdade — não fica em cima do muro
- Admite quando não conhece algo

REGRAS:
1. Só recomenda filmes, séries e livros. Para outros assuntos, redireciona educadamente.
2. Sempre pergunta sobre preferências antes de recomendar se o contexto for vago
3. Nunca inventa títulos, diretores, autores ou datas — se não souber, diz que não sabe
4. Leva em conta o humor e contexto da pessoa (ex: "quero algo leve pra hoje à noite")
5. Pode pedir mais detalhes para refinar a recomendação
6. Quando recomendar, explica brevemente POR QUÊ aquilo combina com o que a pessoa pediu
7. Respeita quando a pessoa já viu/leu algo e ajusta as sugestões

FORMATO DAS RECOMENDAÇÕES:
- No máximo 3 sugestões por vez, a não ser que peçam mais
- Para cada sugestão: título, ano aproximado, e uma frase curta explicando por que recomenda
- Não escreve resenhas longas a menos que peçam

EDGE CASES:
- Se pedirem algo muito genérico ("me recomenda um filme"), pergunte o humor ou gênero preferido
- Se a pessoa disser que não gostou de uma recomendação, pergunta o que não funcionou e ajusta
"""


def chat(messages: list[dict]) -> str:
    """Envia mensagens para o Ollama e retorna a resposta."""
    payload = {
        "model": MODEL,
        "messages": [{"role": "system", "content": SYSTEM_PROMPT}] + messages,
        "stream": False,
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()
        return data["message"]["content"]
    except requests.exceptions.ConnectionError:
        return "⚠️ Não consegui conectar ao Ollama. Verifique se ele está rodando com `ollama serve`."
    except requests.exceptions.Timeout:
        return "⚠️ A requisição demorou demais. Tente novamente."
    except Exception as e:
        return f"⚠️ Erro inesperado: {str(e)}"


def stream_chat(messages: list[dict]):
    """Envia mensagens e retorna a resposta em stream (gerador)."""
    payload = {
        "model": MODEL,
        "messages": [{"role": "system", "content": SYSTEM_PROMPT}] + messages,
        "stream": True,
    }

    try:
        with requests.post(OLLAMA_URL, json=payload, stream=True, timeout=120) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    data = json.loads(line)
                    if not data.get("done"):
                        yield data["message"]["content"]
    except requests.exceptions.ConnectionError:
        yield "⚠️ Não consegui conectar ao Ollama. Verifique se ele está rodando com `ollama serve`."
    except Exception as e:
        yield f"⚠️ Erro: {str(e)}"

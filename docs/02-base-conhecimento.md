# Base de Conhecimento

## Dados Utilizados

A Cleo não utiliza arquivos de dados externos — a base de conhecimento é o próprio modelo Mistral, que contém um amplo repertório de filmes, séries e livros até sua data de corte.

| Fonte | Formato | Utilização |
|-------|---------|------------|
| Modelo Mistral (via Ollama) | LLM local | Recomendações, descrições, contexto de títulos |
| Histórico da conversa | Memória de sessão (lista Python) | Manter contexto e evitar repetição de sugestões |

---

## Estratégia de Integração

### Como o contexto é mantido?
O histórico completo da conversa é enviado a cada requisição para o Ollama, no formato `messages: [{role, content}]`. Isso permite que o modelo saiba o que já foi sugerido e ajuste as próximas recomendações.

### Como o system prompt é usado?
O system prompt é injetado como primeira mensagem de sistema em cada requisição. Ele define a personalidade, as regras de comportamento e o formato esperado das respostas.

---

## Exemplo de Contexto Montado

```
[system]: Você é a Cleo, uma assistente de recomendação...

[user]: Quero um filme pra hoje à noite, tô cansado

[assistant]: Algo mais leve então? Algum gênero preferido, ou pode ser qualquer coisa contanto que não precise de muita atenção?

[user]: Pode ser comédia ou drama, não muito longo

[assistant]: Três opções:
- A Vida é Bela (1997) — drama com momentos de leveza, não é pesado apesar do tema
- Simplesmente Amor (2003) — comédia romântica fácil de assistir, funciona bem no cansaço
- Ela (2013) — drama tranquilo, ritmo lento no bom sentido
```

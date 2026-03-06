# Avaliação e Métricas

## Como Avaliar a Cleo

A avaliação combina testes estruturados com feedback de pessoas reais.

---

## Métricas de Qualidade

| Métrica | O que avalia | Exemplo de teste |
|---------|--------------|------------------|
| **Assertividade** | A recomendação faz sentido com o pedido? | Pedir algo leve e receber um drama pesado = falha |
| **Segurança** | O agente evitou inventar títulos ou informações? | Perguntar sobre um título inexistente e ver se ele inventa |
| **Coerência de contexto** | O agente lembrou o que foi dito antes na conversa? | Dizer que já viu um filme e ver se ele recomenda novamente |
| **Escopo** | O agente se manteve no tema? | Perguntar algo não relacionado e ver se ele redireciona |

---

## Casos de Teste

### Teste 1: Recomendação contextual
- **Input:** "quero um filme pra assistir com minha mãe, ela não gosta de violência"
- **Esperado:** Sugestão adequada para o contexto familiar, sem ação ou terror
- **Resultado:** [ ] Correto  [ ] Incorreto

### Teste 2: Anti-alucinação
- **Input:** "o que você acha do filme Noite de Verão Eterno de 2019?"
- **Esperado:** Agente admite não conhecer o título em vez de inventar uma sinopse
- **Resultado:** [ ] Correto  [ ] Incorreto

### Teste 3: Memória de conversa
- **Input 1:** "já vi Parasita"  
- **Input 2:** "me recomenda um filme coreano"
- **Esperado:** Parasita não aparece na lista
- **Resultado:** [ ] Correto  [ ] Incorreto

### Teste 4: Escopo
- **Input:** "qual a capital da França?"
- **Esperado:** Agente informa que só trabalha com recomendações de entretenimento
- **Resultado:** [ ] Correto  [ ] Incorreto

### Teste 5: Refinamento
- **Input 1:** Recebe 3 recomendações  
- **Input 2:** "não curti nenhum"
- **Esperado:** Agente pergunta o que não funcionou antes de sugerir novamente
- **Resultado:** [ ] Correto  [ ] Incorreto

---

## Resultados

**O que funcionou bem:**
- [Liste aqui após os testes]

**O que pode melhorar:**
- [Liste aqui após os testes]

---

## Métricas Avançadas (Opcional)

- Latência média de resposta (tempo do primeiro token)
- Número de turnos até a recomendação aceita pelo usuário
- Taxa de perguntas de refinamento feitas pelo agente antes de recomendar

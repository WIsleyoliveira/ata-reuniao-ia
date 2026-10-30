# 📝 Ata de Reunião com IA

Transforma a transcrição bruta de uma reunião (Meet, Teams, Zoom ou anotações soltas) em uma **ata organizada**: resumo, participantes, decisões, pendências e **tarefas com responsável, prazo e prioridade**, prontas para exportar.

## O problema

Depois de cada reunião alguém gasta de 20 a 40 minutos relendo anotações para escrever a ata e mandar as tarefas para cada pessoa. Quando ninguém faz isso, as tarefas se perdem.

## Como a IA resolve

- Uma única chamada ao **Claude** (Anthropic) lê a transcrição e devolve um JSON **validado por um esquema Pydantic** (saída estruturada). Não tem parser de texto frágil.
- O prompt proíbe inventar nomes ou prazos: o que não foi dito vira `Não definido`.
- Exporta a ata em **Markdown** e as tarefas em **CSV** (dá pra importar no Trello, Jira, Notion ou planilha).

## Rodando

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export ANTHROPIC_API_KEY="sua-chave"
streamlit run app.py
```

Para testar, use o arquivo [`exemplos/reuniao-sprint.txt`](exemplos/reuniao-sprint.txt).

## Estrutura

| Arquivo | O que faz |
|---|---|
| `app.py` | Interface Streamlit, esquema da ata (`Ata`, `Tarefa`) e exportações |
| `ia.py` | Chamada ao Claude com saída estruturada e tratamento de erros |

## Stack

Python · Streamlit · Anthropic SDK (Claude, structured outputs) · Pydantic

## Próximos passos

- Transcrever áudio direto (Whisper ou similar) antes de gerar a ata
- Enviar as tarefas por e-mail ou WhatsApp para cada responsável

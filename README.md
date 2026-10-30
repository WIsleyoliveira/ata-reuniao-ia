# 📝 Ata de Reunião com IA

Transforma a transcrição bruta de uma reunião (Meet, Teams, Zoom ou anotações soltas) em uma **ata organizada**: resumo, participantes, decisões, pendências e **tarefas com responsável, prazo e prioridade**, prontas para exportar.

## O problema

Depois de cada reunião alguém gasta de 20 a 40 minutos relendo anotações para escrever a ata e mandar as tarefas para cada pessoa. Quando ninguém faz isso, as tarefas se perdem.

## Como a IA resolve

- Um modelo **local** do Ollama (`llama3.1:8b` por padrão) lê a transcrição e devolve um JSON **validado por um esquema Pydantic** (o Ollama gera direto no formato do esquema). Não tem parser de texto frágil. A transcrição não sai da máquina, o que importa para reuniões internas.
- O prompt proíbe inventar nomes ou prazos: o que não foi dito vira `Não definido`.
- Exporta a ata em **Markdown** e as tarefas em **CSV** (dá pra importar no Trello, Jira, Notion ou planilha).

## Rodando

Precisa do [Ollama](https://ollama.com) instalado e aberto.

```bash
ollama pull llama3.1:8b
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Roda **100% local**: nenhum dado sai da sua máquina e não precisa de chave de API. Para usar outro modelo: `OLLAMA_MODEL=qwen2.5:7b streamlit run app.py`.

Para testar, use o arquivo [`exemplos/reuniao-sprint.txt`](exemplos/reuniao-sprint.txt).

## Estrutura

| Arquivo | O que faz |
|---|---|
| `app.py` | Interface Streamlit, esquema da ata (`Ata`, `Tarefa`) e exportações |
| `ia.py` | Chamada ao Ollama com saída estruturada e tratamento de erros |

## Stack

Python · Streamlit · Ollama (Llama 3.1, local, structured outputs) · Pydantic

## Próximos passos

- Transcrever áudio direto (Whisper ou similar) antes de gerar a ata
- Enviar as tarefas por e-mail ou WhatsApp para cada responsável

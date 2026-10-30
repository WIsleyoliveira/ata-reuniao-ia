"""Ata de Reunião com IA: transcrição bruta -> ata, decisões e tarefas com responsável."""

import csv
import io
from typing import Literal

import streamlit as st
from pydantic import BaseModel, Field

from ia import ErroIA, extrair


class Tarefa(BaseModel):
    descricao: str
    responsavel: str = Field(description="Nome da pessoa, ou 'Não definido'")
    prazo: str = Field(description="Prazo citado na reunião, ou 'Não definido'")
    prioridade: Literal["alta", "média", "baixa"]


class Ata(BaseModel):
    titulo: str
    resumo: str = Field(description="3 a 5 frases")
    participantes: list[str]
    decisoes: list[str]
    tarefas: list[Tarefa]
    pendencias: list[str] = Field(description="Dúvidas ou temas que ficaram em aberto")


INSTRUCOES = """Você recebe a transcrição de uma reunião de trabalho em português.
Gere a ata. Use só o que foi dito: não invente nomes, prazos nem decisões.
Uma tarefa é algo que alguém se comprometeu a fazer. Se o responsável ou o prazo
não foi dito, escreva "Não definido"."""


def ata_em_markdown(ata: Ata) -> str:
    linhas = [f"# {ata.titulo}", "", ata.resumo, "", "**Participantes:** " + ", ".join(ata.participantes), ""]
    linhas += ["## Decisões", *[f"- {d}" for d in ata.decisoes], ""]
    linhas += ["## Tarefas", "| Tarefa | Responsável | Prazo | Prioridade |", "|---|---|---|---|"]
    linhas += [f"| {t.descricao} | {t.responsavel} | {t.prazo} | {t.prioridade} |" for t in ata.tarefas]
    linhas += ["", "## Pendências", *[f"- {p}" for p in ata.pendencias]]
    return "\n".join(linhas)


def tarefas_em_csv(ata: Ata) -> str:
    saida = io.StringIO()
    escritor = csv.writer(saida)
    escritor.writerow(["tarefa", "responsavel", "prazo", "prioridade"])
    for t in ata.tarefas:
        escritor.writerow([t.descricao, t.responsavel, t.prazo, t.prioridade])
    return saida.getvalue()


st.set_page_config(page_title="Ata de Reunião com IA", page_icon="📝", layout="wide")
st.title("📝 Ata de Reunião com IA")
st.caption("Cole a transcrição (Meet, Teams, Zoom ou anotações) e receba a ata pronta com as tarefas de cada pessoa.")

arquivo = st.file_uploader("Arquivo de transcrição (.txt)", type=["txt", "vtt"])
texto = st.text_area(
    "…ou cole o texto aqui",
    value=arquivo.read().decode("utf-8", errors="ignore") if arquivo else "",
    height=260,
)

if st.button("Gerar ata", type="primary", disabled=not texto.strip()):
    with st.spinner("Lendo a reunião…"):
        try:
            st.session_state["ata"] = extrair(texto, Ata, INSTRUCOES)
        except ErroIA as e:
            st.error(str(e))

ata: Ata | None = st.session_state.get("ata")
if ata:
    st.subheader(ata.titulo)
    st.write(ata.resumo)
    col1, col2, col3 = st.columns(3)
    col1.metric("Participantes", len(ata.participantes))
    col2.metric("Decisões", len(ata.decisoes))
    col3.metric("Tarefas", len(ata.tarefas))

    st.markdown("### ✅ Tarefas")
    st.dataframe([t.model_dump() for t in ata.tarefas], use_container_width=True, hide_index=True)
    st.markdown("### 📌 Decisões")
    for d in ata.decisoes:
        st.markdown(f"- {d}")
    if ata.pendencias:
        st.markdown("### ❓ Pendências")
        for p in ata.pendencias:
            st.markdown(f"- {p}")

    c1, c2 = st.columns(2)
    c1.download_button("Baixar ata (.md)", ata_em_markdown(ata), "ata.md", "text/markdown")
    c2.download_button("Baixar tarefas (.csv)", tarefas_em_csv(ata), "tarefas.csv", "text/csv")

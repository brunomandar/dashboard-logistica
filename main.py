from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "ok"}

@app.get("/dashboard")
def dashboard(gerente: str = None, forum: str = None, status: str = None):

    df = pd.read_excel("Base Limpa.xlsx")

    # ✅ limpar dados
    df["Gerente"] = df["Gerente"].astype(str).str.strip().str.upper()
    df["Forum"] = df["Forum"].astype(str).str.strip().str.upper()
    df["Status Geral"] = df["Status Geral"].astype(str).str.strip().str.upper()

    if gerente:
        df = df[df["Gerente"] == gerente.strip().upper()]

    
    if forum:
        df = df[df["Forum"].str.strip() == forum.strip().upper()]


    if status:
        df = df[df["Status Geral"].str.strip() == status.strip().upper()]


    total = len(df)

    atrasado = len(df[df["Status"] == "ATRASADO"])
    atencao = len(df[df["Status"] == "ATENÇÃO"])
    prazo = len(df[df["Status"] == "NO PRAZO"])

    planejado = len(df[df["Status Geral"] == "PLANEJADO"])
    em_execucao = len(df[df["Status Geral"] == "EXECUÇÃO"])
    backlog = len(df[df["Status Geral"] == "BACKLOG"])

    prioridade_alta = len(df[df["Prioridade"] == "Alta"])
    prioridade_media = len(df[df["Prioridade"] == "Média"])
    prioridade_baixa = len(df[df["Prioridade"] == "Baixa"])

    return {
        "total": int(total),
        "atrasado": int(atrasado),
        "atencao": int(atencao),
        "prazo": int(prazo),
        "planejado": int(planejado),
        "em_execucao": int(em_execucao),
        "backlog": int(backlog),
        "prioridade_alta": int(prioridade_alta),
        "prioridade_media": int(prioridade_media),
        "prioridade_baixa": int(prioridade_baixa)
    }

@app.get("/projetos")
def projetos(gerente: str = None, forum: str = None, status: str = None):

    df = pd.read_excel("Base Limpa.xlsx")
    df = df.fillna("")

    # normalização
    df["Gerente"] = df["Gerente"].astype(str).str.strip().str.upper()
    df["Forum"] = df["Forum"].astype(str).str.strip().str.upper()
    df["Status Geral"] = df["Status Geral"].astype(str).str.strip().str.upper()

    if gerente:
        df = df[df["Gerente"] == gerente.strip().upper()]

    if forum:
        df = df[df["Forum"] == forum.strip().upper()]

    if status:
        df = df[df["Status Geral"] == status.strip().upper()]

    return df.to_dict(orient="records")

@app.get("/acoes")
def acoes(gerente: str = "", forum: str = ""):
    
    df = pd.read_excel("Base Limpa.xlsx")
    df = df.fillna("")

    # Padroniza texto
    df["Status Ação"] = df["Status Ação"].astype(str).str.strip().str.upper()

    # ✅ FILTROS (NOVO)
    if gerente:
        df = df[df["Gerente"] == gerente]   # confira o nome da coluna

    if forum:
        df = df[df["Forum"] == forum]        # confira acento / nome exato

    # ✅ MÉTRICAS (mantém o que você já tinha)
    total = len(df)
    atrasada = len(df[df["Status Ação"] == "ATRASADO"])
    no_prazo = len(df[df["Status Ação"] == "NO PRAZO"])

    return {
        "total_acoes": int(total),
        "acoes_atrasadas": int(atrasada),
        "acoes_no_prazo": int(no_prazo),
        "dados": df.to_dict(orient="records")
    }
"""Chatbot da disciplina — versão 2.

As respostas saíram do if/elif e agora moram em base.json.
O chatbot dá uma pontuação para cada item da base e escolhe o melhor.

Para conferir:   python verificar.py
Para conversar:  python main.py
Desafios extras: python verificar.py desafios
"""

import json
import unicodedata

# Sinais que podem vir grudados nas palavras: "p1?", "prova,", "(nota)".
PONTUACAO = "?!.,;:()\"'"

# Palavras que aparecem em quase toda pergunta e não ajudam a escolher a resposta.
# Já estão sem acento, porque normalizar() tira os acentos.
STOPWORDS = {
    "o", "a", "os", "as", "de", "da", "do", "das", "dos", "e", "em", "no", "na",
    "um", "uma", "que", "qual", "quais", "quando", "como", "onde", "para", "por",
    "com", "sobre", "eu", "tem", "ser", "vai", "vou", "minha", "meu",
}


# PRONTA (é o desafio "sem acentos" da aula 1, resolvido)
def normalizar(texto: str) -> str:
    """Minúsculas, sem espaços nas pontas e sem acentos."""
    texto = texto.lower().strip()
    decomposto = unicodedata.normalize("NFD", texto)
    return "".join(c for c in decomposto if unicodedata.category(c) != "Mn")


# TODO 1
def carregar_base(caminho: str) -> list[dict]:
    
    with open(caminho, encoding="utf-8") as arquivo:
        return json.load(arquivo)


# TODO 2
def tokenizar(texto: str) -> set[str]:

    normalizado = normalizar(texto)
    palavras = normalizado.split()
    palavras = {p.strip(PONTUACAO) for p in palavras}
    palavras = {p for p in palavras if p and p not in STOPWORDS}
    return palavras


# TODO 3
def pontuar(palavras: set[str], item: dict) -> int:
    # Devolve a pontuação do item da base para a pergunta.
    palavras_chave = set(item["palavras"])
    return len(palavras & palavras_chave)


# TODO 4
def ranquear(pergunta: str, base: list[dict]) -> list[tuple[int, dict]]:
    # Devolve uma lista de tuplas (pontuação, item) para cada item que pontuou > 0.
    palavras = tokenizar(pergunta)
    ranking = []
    for item in base:
        pontuacao = pontuar(palavras, item)
        if pontuacao > 0:
            ranking.append((pontuacao, item))
    return sorted(ranking, key=lambda x: (-x[0], x[1]["assunto"]))


# PRONTA
def responder(pergunta: str, base: list[dict]) -> dict | None:
    """Devolve o item mais bem pontuado, ou None se nenhum pontuou."""
    ranking = ranquear(pergunta, base)
    if not ranking:
        return None
    pontuacao, item = ranking[0]
    return item


# TODO 5
def resumo(historico: list[str], contagem: dict[str, int]) -> str:
   
    total_perguntas = len(historico)
    total_respondidas = sum(contagem.values())

    if total_perguntas == 0:
        return "Até mais!"

    percentual = (total_respondidas / total_perguntas) * 100
    resumo = (
        f"Você fez {total_perguntas} perguntas e eu respondi "
        f"{total_respondidas} ({percentual:.0f}%)."
    )

    if total_respondidas > 0:
        mais_perguntado = max(contagem, key=contagem.get)
        resumo += f" Assunto mais perguntado: {mais_perguntado}."

    resumo += " Até mais!"
    return resumo


# ----------------------------------------------------------------------
# DESAFIOS EXTRAS (python verificar.py desafios)

# D1
def sugestoes(pergunta: str, base: list[dict], n: int = 3) -> list[str]:
   
    ranking = ranquear(pergunta, base)
    assuntos = [item["assunto"] for _, item in ranking]
    return assuntos[:n]

# D2
def salvar_historico(caminho: str, historico: list[str]) -> None:
  
    with open(caminho, "w") as f:
        json.dump(historico, f, ensure_ascii=False, indent=2)

# D3 (manual, sem verificação)
# Comando "ensinar": o chatbot pergunta assunto, palavras-chave e resposta,
# acrescenta na base e grava de volta em base.json.


# ----------------------------------------------------------------------
# TODO 6 (teste manual: rode python main.py e converse)
def main() -> None:
    base = carregar_base("base.json")
    historico = []
    contagem = {}
    print('Olá! Sou o assistente da disciplina. Digite "ajuda" ou "sair".')
    while True:
        pergunta = input("> ").strip()
        
        if not pergunta:
            continue
        elif pergunta == "sair":
            break
        elif pergunta == "ajuda":
            assuntos = sorted({item["assunto"] for item in base})
            print("Assuntos disponíveis:")
            for assunto in assuntos:
                print(f" - {assunto}")
        else:
            historico.append(pergunta)
            resposta = responder(pergunta, base)
            if resposta is None:
                print("Ainda não sei responder isso. Digite 'ajuda'.")
            else:
                print(resposta["resposta"])
                # Somar 1 na contagem do assunto
                assunto = resposta["assunto"]
                contagem[assunto] = contagem.get(assunto, 0) + 1

    print(resumo(historico, contagem))


if __name__ == "__main__":
    main()
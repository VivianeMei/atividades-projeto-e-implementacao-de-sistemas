"""Verificação automática dos TODOs 1 a 3 da Aula 1.

Uso:  python verificar.py
O TODO 4 (laço da conversa) você testa rodando:  python main.py
"""

from main import normalizar, responder, resumo


def checar(nome, casos):
    """Roda os casos de um TODO; para no primeiro que falhar."""
    for descricao, funcao in casos:
        try:
            ok, detalhe = funcao()
        except Exception as erro:
            ok, detalhe = False, f"{type(erro).__name__}: {erro}"
        if not ok:
            print(f"FALHA {nome}  {descricao}: {detalhe}")
            return False
    print(f"OK    {nome}")
    return True


def igual(obtido, esperado):
    return obtido == esperado, f"esperava {esperado!r}, veio {obtido!r}"


def tem_resposta(pergunta):
    r = responder(pergunta)
    return isinstance(r, str) and r != "", f"{pergunta!r} ficou sem resposta (veio {r!r})"


def sem_resposta(pergunta):
    r = responder(pergunta)
    return r is None, f"{pergunta!r} deveria devolver None, veio {r!r}"


todo1 = [
    ("maiúsculas e espaços", lambda: igual(normalizar("  Qual o PRAZO? "), "qual o prazo?")),
    ("texto já normalizado", lambda: igual(normalizar("oi"), "oi")),
    ("só espaços", lambda: igual(normalizar("   "), "")),
]

todo2 = [
    ("assunto 1: apresentação", lambda: tem_resposta("Quando é a APRESENTAÇÃO final?")),
    ("assunto 2: avaliação", lambda: tem_resposta("Como é a avaliação?")),
    ("assunto 2: nota", lambda: tem_resposta("Como vou tirar nota?")),
    ("assunto 3: linguagem", lambda: tem_resposta("Qual linguagem vamos usar?")),
    ("assunto 4: grupos", lambda: tem_resposta("Quando se formam os grupos?")),
    ("assunto 5: IA", lambda: tem_resposta("Posso usar IA?")),
    ("fora da base", lambda: sem_resposta("Qual o cardápio do restaurante?")),
    ("fora da base", lambda: sem_resposta("Vai chover amanhã?")),
]

todo3 = [
    ("resumo(4, 3)", lambda: igual(resumo(4, 3), "Você fez 4 perguntas e eu respondi 3 (75%). Até mais!")),
    ("resumo(3, 2)", lambda: igual(resumo(3, 2), "Você fez 3 perguntas e eu respondi 2 (67%). Até mais!")),
    ("resumo(1, 0)", lambda: igual(resumo(1, 0), "Você fez 1 perguntas e eu respondi 0 (0%). Até mais!")),
    ("resumo(0, 0)", lambda: igual(resumo(0, 0), "Até mais!")),
]

if __name__ == "__main__":
    for nome, casos in [("TODO 1  normalizar", todo1), ("TODO 2  responder", todo2), ("TODO 3  resumo", todo3)]:
        if not checar(nome, casos):
            break
    else:
        print("--    TODO 4  teste manual: rode python main.py")
        print("Tudo certo nos TODOs 1 a 3!")
"""Verificador do chatbot da aula 2. Não precisa alterar este arquivo.

    python verificar.py            confere os TODOs 1 a 5
    python verificar.py desafios   confere os desafios D1 e D2
"""

import json
import os
import sys
import tempfile
import traceback

import main as m

BASE_TESTE = [
    {"assunto": "apresentação", "palavras": ["apresentacao", "final"], "resposta": "Aula 15."},
    {"assunto": "avaliação", "palavras": ["nota", "peso"], "resposta": "NE, NT, NP."},
    {"assunto": "provas", "palavras": ["prova", "p1", "p2"], "resposta": "P1 e P2."},
]


def igual(obtido, esperado, chamada):
    if obtido != esperado:
        raise AssertionError(f"{chamada}\n        esperado: {esperado!r}\n        obtido:   {obtido!r}")


def t1():
    base = m.carregar_base("base.json")
    if not isinstance(base, list) or len(base) < 8:
        raise AssertionError("carregar_base('base.json') deveria devolver uma lista com pelo menos 8 itens")
    for item in base:
        faltando = {"assunto", "palavras", "resposta"} - set(item)
        if faltando:
            raise AssertionError(f"o item {item.get('assunto', item)!r} não tem as chaves {faltando}")
    igual(base[0]["assunto"], "apresentação", 'carregar_base("base.json")[0]["assunto"] (acentos ok?)')


def t2():
    igual(m.tokenizar("Quando é a APRESENTAÇÃO final?"), {"apresentacao", "final"},
          'tokenizar("Quando é a APRESENTAÇÃO final?")')
    igual(m.tokenizar("  Qual o peso da P1, professor?! "), {"peso", "p1", "professor"},
          'tokenizar("  Qual o peso da P1, professor?! ")')
    igual(m.tokenizar("? ! ."), set(), 'tokenizar("? ! .")')


def t3():
    item = BASE_TESTE[0]
    igual(m.pontuar({"apresentacao", "final"}, item), 2, 'pontuar({"apresentacao", "final"}, item_apresentacao)')
    igual(m.pontuar({"cardapio"}, item), 0, 'pontuar({"cardapio"}, item_apresentacao)')


def t4():
    r = m.ranquear("Quando é a apresentação final?", BASE_TESTE)
    igual([(p, i["assunto"]) for p, i in r], [(2, "apresentação")],
          'ranquear("Quando é a apresentação final?", BASE_TESTE)')
    r = m.ranquear("peso da P1 e nota da P2", BASE_TESTE)
    igual([(p, i["assunto"]) for p, i in r], [(2, "avaliação"), (2, "provas")],
          'ranquear("peso da P1 e nota da P2", BASE_TESTE)  (empate: ordem alfabética)')
    r = m.ranquear("prova ou nota?", BASE_TESTE)
    igual([(p, i["assunto"]) for p, i in r], [(1, "avaliação"), (1, "provas")],
          'ranquear("prova ou nota?", BASE_TESTE)  (empate: ordem alfabética)')
    igual(m.ranquear("cardápio do RU", BASE_TESTE), [], 'ranquear("cardápio do RU", BASE_TESTE)')


def t5():
    igual(m.resumo([], {}), "Até mais!", "resumo([], {})")
    igual(m.resumo(["a", "b", "c", "d"], {"grupos": 1, "provas": 2}),
          "Você fez 4 perguntas e eu respondi 3 (75%). Assunto mais perguntado: provas. Até mais!",
          'resumo(4 perguntas, {"grupos": 1, "provas": 2})')
    igual(m.resumo(["a", "b"], {}),
          "Você fez 2 perguntas e eu respondi 0 (0%). Até mais!",
          "resumo(2 perguntas, {})")
    igual(m.resumo(["a", "b", "c"], {"provas": 2}),
          "Você fez 3 perguntas e eu respondi 2 (67%). Assunto mais perguntado: provas. Até mais!",
          'resumo(3 perguntas, {"provas": 2})  (arredonde: 67%)')
    igual(m.resumo(["a", "b"], {"grupos": 1, "provas": 1}),
          "Você fez 2 perguntas e eu respondi 2 (100%). Assunto mais perguntado: grupos. Até mais!",
          'resumo(2 perguntas, {"grupos": 1, "provas": 1})  (empate: o primeiro)')


def d1():
    igual(m.sugestoes("prova e nota", BASE_TESTE, 2), ["avaliação", "provas"],
          'sugestoes("prova e nota", BASE_TESTE, 2)')
    igual(m.sugestoes("apresentação final da prova", BASE_TESTE), ["apresentação", "provas"],
          'sugestoes("apresentação final da prova", BASE_TESTE)')
    igual(m.sugestoes("cardápio", BASE_TESTE), [], 'sugestoes("cardápio", BASE_TESTE)')


def d2():
    historico = ["Quando é a apresentação?", "Qual o peso da P1?"]
    with tempfile.TemporaryDirectory() as pasta:
        caminho = os.path.join(pasta, "historico.json")
        m.salvar_historico(caminho, historico)
        with open(caminho, encoding="utf-8") as f:
            texto = f.read()
        igual(json.loads(texto), historico, "conteúdo de historico.json")
        if "apresentação" not in texto:
            raise AssertionError("os acentos saíram como \\u00e7...; use ensure_ascii=False")


TESTES = [("TODO 1", "carregar_base", t1), ("TODO 2", "tokenizar", t2), ("TODO 3", "pontuar", t3),
          ("TODO 4", "ranquear", t4), ("TODO 5", "resumo", t5)]
DESAFIOS = [("D1", "sugestoes", d1), ("D2", "salvar_historico", d2)]


def rodar(lista):
    ok = 0
    for rotulo, nome, teste in lista:
        try:
            teste()
        except NotImplementedError:
            print(f"--     {rotulo}  {nome}  a fazer")
        except AssertionError as erro:
            print(f"FALHA  {rotulo}  {nome}  {erro}")
        except Exception:
            print(f"ERRO   {rotulo}  {nome}  o código quebrou. Traceback (leia de baixo para cima):")
            print(traceback.format_exc())
        else:
            print(f"OK     {rotulo}  {nome}")
            ok += 1
    return ok


def principal():
    lista = DESAFIOS if len(sys.argv) > 1 and sys.argv[1] == "desafios" else TESTES
    ok = rodar(lista)
    if lista is TESTES:
        print("--     TODO 6  main          (teste manual: rode python main.py)")
    print(f"\n{ok} de {len(lista)} certos.")
    if ok == len(lista):
        print("Tudo certo!")


if __name__ == "__main__":
    principal()
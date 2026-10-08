"""Chatbot da disciplina — Aula 1 (Python I)."""


def normalizar(texto):
    return texto.lower().strip()


def responder(pergunta):
    p = normalizar(pergunta)
    if "apresentação" in p or "apresentacao" in p:
        return "A apresentação final é na aula 15."
    
    elif "avaliação" in p or "avaliacao" in p or "nota" in p:
        return "A avaliação é feita com base na participação e nos exercícios."

    elif "linguagem de programação" in p or "linguagem de programacao" in p or "linguagem" in p:
        return "Vamos usar python como linguagem de programação."

    elif "grupos" in p or "grupo" in p:
        return "Os grupos serão formados por no máximo 3 pessoas."
    
    elif "inteligência artificial" in p or "inteligencia artificial" in p or "ia" in p:
        return "O chatbot final utiliza IA na interação com o usuário."
  
    else:
        return None


def resumo(feitas, respondidas):
    if feitas == 0:
        return "Até mais!"
    else:
        percentual = (respondidas/feitas)
        return f"Você fez {feitas} perguntas e eu respondi {respondidas} ({percentual:.0%}). Até mais!"


def main():
    print('Olá! Sou o assistente da disciplina. Digite "sair" para encerrar.')
    feitas = 0
    respondidas = 0
    
    while True:
        pergunta = input("> ")

        if pergunta == "":
            continue

        elif pergunta == "sair":
            break

        else:
            feitas += 1
            resposta = responder(pergunta)
            if resposta is None:
                print("Ainda não sei responder isso. Pergunte ao professor.")
            else:
                print(resposta)
                respondidas += 1
    
    print(resumo(feitas, respondidas))


if __name__ == "__main__":
    main()

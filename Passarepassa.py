import flet as ft
import random
import csv
import os

perguntas_respostas = [
    {"pergunta": "Qual é o valor de 7 x 8?", "alternativas": ["54", "56", "64", "58"], "correta": "56"},
    {"pergunta": "Qual é a raiz quadrada de 144?", "alternativas": ["11", "12", "13", "14"], "correta": "12"},
    {"pergunta": "Se 3x = 12, qual é o valor de x?", "alternativas": ["2", "3", "4", "5"], "correta": "4"},
    {"pergunta": "Quanto é 25% de 80?", "alternativas": ["15", "20", "25", "30"], "correta": "20"},
    {"pergunta": "Qual é o próximo número na sequência 2, 4, 8, 16, ?", "alternativas": ["20", "24", "32", "30"], "correta": "32"},
    {"pergunta": "Quanto é 15 + 27?", "alternativas": ["42", "41", "43", "40"], "correta": "42"},
    {"pergunta": "Qual é o resultado de 9²?", "alternativas": ["81", "72", "99", "90"], "correta": "81"},
    {"pergunta": "Quanto é 100 dividido por 4?", "alternativas": ["20", "25", "30", "15"], "correta": "25"},
    {"pergunta": "Qual é o valor de π (pi) arredondado?", "alternativas": ["3.12", "3.14", "3.15", "3.16"], "correta": "3.14"},
    {"pergunta": "Qual é a fração equivalente a 0,5?", "alternativas": ["1/3", "1/4", "1/2", "2/3"], "correta": "1/2"},
    {"pergunta": "Quantos lados tem um hexágono?", "alternativas": ["5", "6", "7", "8"], "correta": "6"},
    {"pergunta": "Quanto é 5! (5 fatorial)?", "alternativas": ["120", "60", "24", "100"], "correta": "120"},
    {"pergunta": "Qual é a fórmula da área do círculo?", "alternativas": ["πr²", "2πr", "πd", "r²"], "correta": "πr²"},
    {"pergunta": "Quanto é 2³?", "alternativas": ["6", "8", "9", "4"], "correta": "8"},
    {"pergunta": "Qual é o valor de 50% de 90?", "alternativas": ["40", "45", "50", "55"], "correta": "45"},
]

ranking_file = "ranking.csv"

def carregar_ranking():
    if not os.path.exists(ranking_file):
        return []
    with open(ranking_file, newline='', encoding="utf-8") as f:
        return list(csv.reader(f))

def salvar_ranking(ranking):
    with open(ranking_file, mode='w', newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(ranking)

def main(page: ft.Page):
    page.title = "Jogo Passa ou Repassa - Matemática"
    page.window_width = 600
    page.window_height = 520
    page.scroll = ft.ScrollMode.AUTO

    jogador1 = ft.TextField(label="Jogador 1", text_align=ft.TextAlign.CENTER, width=250)
    jogador2 = ft.TextField(label="Jogador 2", text_align=ft.TextAlign.CENTER, width=250)
    info_text = ft.Text("", size=18, text_align=ft.TextAlign.CENTER)
    pergunta_text = ft.Text("", size=22, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER, expand=True)
    resultado_text = ft.Text("", size=18, text_align=ft.TextAlign.CENTER, color=ft.Colors.BLUE)
    timer_text = ft.Text("Tempo restante: 60s", size=18, color=ft.Colors.RED, text_align=ft.TextAlign.CENTER)

    pontos = {1: 0, 2: 0}
    jogador_atual = [1]
    pergunta_atual = [None]
    timer = [None]  # Intervalo do timer
    tempo_restante = [60]

    alternativas_col = ft.Column(alignment=ft.MainAxisAlignment.CENTER, spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    def atualizar_info():
        info_text.value = f"{nome_jogador(jogador_atual[0])}, é sua vez! | Placar: {jogador1.value}: {pontos[1]} | {jogador2.value}: {pontos[2]}"
        page.update()

    def nome_jogador(n):
        return jogador1.value if n == 1 else jogador2.value

    def mostrar_pergunta():
        tempo_restante[0] = 60
        timer_text.value = f"Tempo restante: {tempo_restante[0]}s"
        if timer[0]:
            timer[0].cancel()
            timer[0] = None

        pergunta_atual[0] = random.choice(perguntas_respostas)
        pergunta_text.value = pergunta_atual[0]["pergunta"]
        alternativas_col.controls.clear()
        for alt in pergunta_atual[0]["alternativas"]:
            alternativas_col.controls.append(
                ft.ElevatedButton(text=alt, on_click=verificar_resposta, width=200)
            )
        alternativas_col.controls.append(
            ft.ElevatedButton(text="Passar", on_click=passar_vez, width=200, bgcolor=ft.Colors.ORANGE)
        )

        resultado_text.value = ""
        page.update()

        timer[0] = page.interval(1000, atualizar_timer)

    def atualizar_timer(e):
        if tempo_restante[0] > 0:
            tempo_restante[0] -= 1
            timer_text.value = f"Tempo restante: {tempo_restante[0]}s"
            page.update()
        else:
            if timer[0]:
                timer[0].cancel()
                timer[0] = None
            resultado_text.value = f"⏰ Tempo esgotado! {nome_jogador(jogador_atual[0])} perde 1 ponto."
            pontos[jogador_atual[0]] = max(0, pontos[jogador_atual[0]] - 1)
            jogador_atual[0] = 2 if jogador_atual[0] == 1 else 1
            atualizar_info()
            mostrar_pergunta()

    def verificar_resposta(e):
        if timer[0]:
            timer[0].cancel()
            timer[0] = None

        resposta = e.control.text
        correta = pergunta_atual[0]["correta"]
        jogador = jogador_atual[0]

        if resposta == correta:
            pontos[jogador] += 1
            resultado_text.value = f"✅ Resposta correta! {nome_jogador(jogador)} ganha 1 ponto."
            if pontos[jogador] >= 5:
                resultado_text.value = f"🏆 {nome_jogador(jogador)} venceu o jogo com {pontos[jogador]} pontos!"
                alternativas_col.controls.clear()
                timer_text.value = ""
                page.update()
                return
        else:
            pontos[jogador] = max(0, pontos[jogador] - 1)
            resultado_text.value = f"❌ Errado! Resposta correta: {correta}. {nome_jogador(jogador)} perde 1 ponto."

        # Passa a vez pro outro jogador
        jogador_atual[0] = 2 if jogador == 1 else 1
        atualizar_info()
        page.update()
        mostrar_pergunta()

    def passar_vez(e):
        if timer[0]:
            timer[0].cancel()
            timer[0] = None

        resultado_text.value = f"{nome_jogador(jogador_atual[0])} passou a vez para {nome_jogador(2 if jogador_atual[0] == 1 else 1)}."
        jogador_atual[0] = 2 if jogador_atual[0] == 1 else 1
        atualizar_info()
        page.update()
        mostrar_pergunta()

    def iniciar_jogo(e):
        if not jogador1.value or not jogador2.value:
            info_text.value = "Digite o nome dos dois jogadores para iniciar."
            page.update()
            return

        pontos[1], pontos[2] = 0, 0
        jogador_atual[0] = 1
        resultado_text.value = ""
        timer_text.value = "Tempo restante: 60s"
        atualizar_info()
        mostrar_pergunta()
        page.update()

    def salvar_placar(e):
        ranking = carregar_ranking()
        ranking.append([jogador1.value, pontos[1]])
        ranking.append([jogador2.value, pontos[2]])
        salvar_ranking(ranking)
        info_text.value = "Placar salvo no ranking!"
        page.update()

    def mostrar_ranking(e):
        ranking = carregar_ranking()
        if not ranking:
            info_text.value = "Ranking vazio."
        else:
            ranking_text = "\n".join([f"{nome}: {pts}" for nome, pts in ranking])
            info_text.value = f"Ranking:\n{ranking_text}"
        page.update()

    page.add(
        ft.Row([jogador1, jogador2], alignment=ft.MainAxisAlignment.CENTER, spacing=30),
        ft.ElevatedButton("Iniciar Jogo", on_click=iniciar_jogo, width=150),
        info_text,
        timer_text,
        pergunta_text,
        alternativas_col,
        resultado_text,
        ft.Row([
            ft.ElevatedButton("Salvar Placar", on_click=salvar_placar, width=150),
            ft.ElevatedButton("Mostrar Ranking", on_click=mostrar_ranking, width=150),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
    )


if __name__ == "__main__":
    ft.app(target=main)

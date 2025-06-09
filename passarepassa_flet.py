
import flet as ft
import random
import csv
import os
import time

perguntas_respostas = [
    {"pergunta": "Qual é o valor de 7 x 8?", "alternativas": ["54", "56", "64", "58"], "correta": "56"},
    {"pergunta": "Qual é a raiz quadrada de 144?", "alternativas": ["11", "12", "13", "14"], "correta": "12"},
    {"pergunta": "Se 3x = 12, qual é o valor de x?", "alternativas": ["2", "3", "4", "5"], "correta": "4"},
    {"pergunta": "Quanto é 25% de 80?", "alternativas": ["15", "20", "25", "30"], "correta": "20"},
    {"pergunta": "Qual é o valor de 9²?", "alternativas": ["81", "72", "64", "99"], "correta": "81"},
    {"pergunta": "Quanto é 15 + 18?", "alternativas": ["33", "32", "31", "30"], "correta": "33"},
    {"pergunta": "Quanto é 100 ÷ 4?", "alternativas": ["25", "20", "24", "26"], "correta": "25"},
    {"pergunta": "Qual número é primo?", "alternativas": ["15", "21", "19", "25"], "correta": "19"},
    {"pergunta": "Qual é a fração equivalente a 1/2?", "alternativas": ["2/4", "3/5", "2/3", "4/5"], "correta": "2/4"},
    {"pergunta": "Quanto é 10% de 250?", "alternativas": ["25", "30", "20", "22"], "correta": "25"},
    {"pergunta": "Quanto é 5³?", "alternativas": ["125", "25", "15", "100"], "correta": "125"},
    {"pergunta": "Quanto é 2 elevado à 4ª potência?", "alternativas": ["16", "8", "4", "12"], "correta": "16"},
    {"pergunta": "Qual é o MMC entre 6 e 8?", "alternativas": ["24", "48", "12", "18"], "correta": "24"},
    {"pergunta": "Qual é a média de 4, 6 e 10?", "alternativas": ["7", "6", "8", "9"], "correta": "6.67"},
    {"pergunta": "Quanto é 45 ÷ 5?", "alternativas": ["8", "9", "10", "11"], "correta": "9"}
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
    page.window_height = 550
    page.scroll = ft.ScrollMode.AUTO

    jogador1 = ft.TextField(label="Jogador 1", text_align=ft.TextAlign.CENTER)
    jogador2 = ft.TextField(label="Jogador 2", text_align=ft.TextAlign.CENTER)
    info_text = ft.Text("", size=20, text_align=ft.TextAlign.CENTER)
    pergunta_text = ft.Text("", size=22, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
    resultado_text = ft.Text("", size=20, text_align=ft.TextAlign.CENTER, color=ft.colors.BLUE)
    tempo_text = ft.Text("Tempo restante: 60s", size=18, text_align=ft.TextAlign.CENTER, color=ft.colors.RED)

    pontos = {1: 0, 2: 0}
    jogador_atual = [1]
    pergunta_atual = [None]
    tempo_restante = [60]
    tempo_timer = [None]

    alternativas_col = ft.Column(alignment=ft.MainAxisAlignment.CENTER, spacing=10)

    def nome_jogador(n):
        return jogador1.value if n == 1 else jogador2.value

    def atualizar_info():
        info_text.value = f"{nome_jogador(jogador_atual[0])}, é sua vez! | Placar: {jogador1.value}: {pontos[1]} | {jogador2.value}: {pontos[2]}"
        page.update()

    def encerrar_jogo(vencedor):
        info_text.value = f"🎉 {nome_jogador(vencedor)} venceu com 5 pontos!"
        pergunta_text.value = ""
        alternativas_col.controls.clear()
        resultado_text.value = ""
        tempo_text.value = ""
        page.update()

    def verificar_resposta(resposta):
        correta = pergunta_atual[0]["correta"]
        jogador = jogador_atual[0]

        if resposta == correta:
            pontos[jogador] += 1
            resultado_text.value = f"✅ Correto! {nome_jogador(jogador)} ganhou 1 ponto."
        else:
            pontos[jogador] = max(0, pontos[jogador] - 1)
            resultado_text.value = f"❌ Errado! Resposta correta: {correta}. {nome_jogador(jogador)} perdeu 1 ponto."

        if pontos[jogador] >= 5:
            encerrar_jogo(jogador)
            parar_temporizador()
            return

        jogador_atual[0] = 2 if jogador == 1 else 1
        atualizar_info()
        exibir_pergunta()

    def passar_vez(e):
        jogador_atual[0] = 2 if jogador_atual[0] == 1 else 1
        resultado_text.value = f"{nome_jogador(2 if jogador_atual[0] == 1 else 1)} passou a vez."
        atualizar_info()
        exibir_pergunta()

    def exibir_pergunta():
        parar_temporizador()
        pergunta_atual[0] = random.choice(perguntas_respostas)
        pergunta_text.value = pergunta_atual[0]["pergunta"]
        alternativas_col.controls.clear()
        for alt in pergunta_atual[0]["alternativas"]:
            alternativas_col.controls.append(
                ft.ElevatedButton(text=alt, on_click=lambda e, r=alt: verificar_e_reiniciar(e, r), width=200)
            )
        alternativas_col.controls.append(
            ft.ElevatedButton(text="Passar", on_click=passar_vez, width=200, bgcolor=ft.colors.YELLOW)
        )
        resultado_text.value = ""
        tempo_restante[0] = 60
        tempo_text.value = f"Tempo restante: {tempo_restante[0]}s"
        page.update()
        iniciar_temporizador()

    def verificar_e_reiniciar(e, resposta):
        verificar_resposta(resposta)

    def iniciar_temporizador():
        def tick():
            tempo_restante[0] -= 1
            tempo_text.value = f"Tempo restante: {tempo_restante[0]}s"
            page.update()
            if tempo_restante[0] == 0:
                resultado_text.value = f"⏰ Tempo esgotado! {nome_jogador(jogador_atual[0])} perdeu 1 ponto."
                pontos[jogador_atual[0]] = max(0, pontos[jogador_atual[0]] - 1)
                jogador_atual[0] = 2 if jogador_atual[0] == 1 else 1
                atualizar_info()
                exibir_pergunta()
            else:
                tempo_timer[0] = page.run_later(tick, 1)

        tempo_timer[0] = page.run_later(tick, 1)

    def parar_temporizador():
        if tempo_timer[0]:
            page.cancel_timer(tempo_timer[0])
            tempo_timer[0] = None

    def iniciar_jogo(e):
        if not jogador1.value or not jogador2.value:
            info_text.value = "Digite o nome dos dois jogadores para iniciar."
        else:
            pontos[1], pontos[2] = 0, 0
            jogador_atual[0] = 1
            atualizar_info()
            exibir_pergunta()
        page.update()

    def mostrar_ranking(e):
        ranking = carregar_ranking()
        ranking_text.value = "\n".join([f"{linha[0]}: {linha[1]} pts" for linha in ranking])
        page.update()

    def salvar_placar(e):
        ranking = carregar_ranking()
        ranking.append([jogador1.value, pontos[1]])
        ranking.append([jogador2.value, pontos[2]])
        salvar_ranking(ranking)
        info_text.value = "Placar salvo no ranking!"
        page.update()

    ranking_text = ft.Text(size=18, text_align=ft.TextAlign.CENTER)

    page.add(
        ft.Column(
            [
                jogador1,
                jogador2,
                ft.Row([
                    ft.ElevatedButton(text="Iniciar Jogo", on_click=iniciar_jogo),
                    ft.ElevatedButton(text="Salvar no Ranking", on_click=salvar_placar),
                    ft.ElevatedButton(text="Ver Ranking", on_click=mostrar_ranking)
                ], alignment=ft.MainAxisAlignment.CENTER),
                info_text,
                pergunta_text,
                tempo_text,
                alternativas_col,
                resultado_text,
                ranking_text
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
        )
    )

ft.app(target=main)

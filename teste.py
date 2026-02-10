import tkinter as tk
import os
from game import Game, GuessResult


class TelaInicial(tk.Frame):
    def __init__(self, master, ir_dificuldade_callback):
        super().__init__(master, bg="#ffe0b2")
        self.ir_dificuldade_callback = ir_dificuldade_callback
        self.pack(fill="both", expand=True)
        self.criar_widgets()

    def criar_widgets(self):
        container = tk.Frame(self, bg="#ffe0b2")
        container.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            container,
            text="🎮 Jogo da Forca",
            font=("Segoe UI", 32, "bold"),
            fg="#ffb300",
            bg="#ffe0b2"
        ).pack(pady=30)

        tk.Button(
            container,
            text="Jogar",
            font=("Segoe UI", 20, "bold"),
            bg="#4fc3f7",
            fg="white",
            bd=0,
            cursor="hand2",
            command=self.ir_dificuldade_callback,
            padx=30,
            pady=10
        ).pack(pady=20)



class TelaDificuldade(tk.Frame):
    def __init__(self, master, iniciar_callback):
        super().__init__(master, bg="#ffe0b2")
        self.iniciar_callback = iniciar_callback
        self.pack(fill="both", expand=True)
        self.criar_widgets()

    def criar_widgets(self):
        container = tk.Frame(self, bg="#ffe0b2")
        container.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            container,
            text="Selecione a Dificuldade",
            font=("Segoe UI", 26, "bold"),
            fg="#ffb300",
            bg="#ffe0b2"
        ).pack(pady=25)

        for texto, diff, cor in [
            ("Fácil (3–7 letras)", "facil", "#81c784"),
            ("Médio (8–15 letras)", "medio", "#4fc3f7"),
            ("Difícil (16–35 letras)", "dificil", "#ffb300")
        ]:
            tk.Button(
                container,
                text=texto,
                font=("Segoe UI", 18),
                bg=cor,
                fg="#212121",
                bd=0,
                cursor="hand2",
                width=22,
                command=lambda d=diff: self.iniciar_callback(d)
            ).pack(pady=8)



class TelaJogo(tk.Frame):
    def __init__(self, master, dificuldade):
        super().__init__(master)
        self.master = master
        self.dificuldade = dificuldade

        # FUNDO COM IMAGEM (CAMINHO SEGURO)
        base_dir = os.path.dirname(__file__)
        img_path = os.path.join(base_dir, "imagens", "fundo.png")

        self.bg_image = tk.PhotoImage(file=img_path)
        self.bg_label = tk.Label(self, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        palavras = self.carregar_palavras() or [
            "gato", "python", "computador", "programacao",
            "desenvolvimento", "extraordinario",
            "hipopotomonstrosesquipedaliofobia"
        ]

        self.game = Game(palavras, dificuldade)
        self.pack(fill="both", expand=True)
        self.criar_widgets()

    def carregar_palavras(self):
        caminho = os.path.join(os.path.dirname(__file__), "palavras.txt")
        if os.path.exists(caminho):
            with open(caminho, "r", encoding="utf-8") as f:
                return [l.strip() for l in f if l.strip()]
        return None

    def criar_widgets(self):
        container = tk.Frame(self, bg="#ffffff")
        container.place(relx=0.5, rely=0.1, anchor="n")

        tk.Label(
            container,
            text=f"Dificuldade: {self.dificuldade.upper()}",
            font=("Segoe UI", 14, "bold"),
            bg="#ffffff"
        ).pack(pady=5)

        self.lbl_palavra = tk.Label(
            container,
            text=self.game.revealed_word(),
            font=("Segoe UI", 28, "bold"),
            bg="#ffffff"
        )
        self.lbl_palavra.pack(pady=20)

        self.lbl_info = tk.Label(
            container,
            text=f"Tentativas restantes: {self.game.attempts_left}",
            font=("Segoe UI", 16),
            bg="#ffffff"
        )
        self.lbl_info.pack()

        self.letras_frame = tk.Frame(self, bg="#ffffff")
        self.letras_frame.place(relx=0.5, rely=0.45, anchor="n")

        self.criar_botoes_letras()

    def criar_botoes_letras(self):
        for i, letra in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            btn = tk.Button(
                self.letras_frame,
                text=letra,
                width=4,
                font=("Segoe UI", 14, "bold"),
                bg="#4fc3f7",
                fg="white",
                bd=0,
                cursor="hand2"
            )
            btn.grid(row=i // 9, column=i % 9, padx=4, pady=4)
            btn.config(command=lambda l=letra, b=btn: self.tentar_letra(l, b))

    def tentar_letra(self, letra, botao):
        resultado = self.game.guess(letra)

        if resultado in (GuessResult.INVALID, GuessResult.ALREADY_TRIED):
            return

        botao.config(state="disabled")

        if resultado == GuessResult.CORRECT:
            botao.config(bg="#81c784")
        else:
            botao.config(bg="#e57373")

        self.atualizar_tela()

    def atualizar_tela(self):
        self.lbl_palavra.config(text=self.game.revealed_word())
        self.lbl_info.config(
            text=f"Tentativas restantes: {self.game.attempts_left}"
        )

        if self.game.is_won():
            self.fim_jogo(True)
        elif self.game.is_lost():
            self.fim_jogo(False)

    def fim_jogo(self, venceu):
        msg = "🎉 Você venceu!" if venceu else f"😢 Você perdeu!\nPalavra: {self.game.palavra}"
        self.lbl_info.config(text=msg)

        for w in self.letras_frame.winfo_children():
            w.config(state="disabled")

        tk.Button(
            self,
            text="Jogar Novamente",
            font=("Segoe UI", 16, "bold"),
            bg="#4caf50",
            fg="white",
            bd=0,
            cursor="hand2",
            command=self.master.mostrar_tela_dificuldade
        ).place(relx=0.5, rely=0.85, anchor="center")


class JogoDaForca(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Jogo da Forca")
        self.geometry("500x600")
        self.resizable(False, False)
        self.tela_atual = None
        self.mostrar_tela_inicial()

    def limpar_tela(self):
        if self.tela_atual:
            self.tela_atual.destroy()

    def mostrar_tela_inicial(self):
        self.limpar_tela()
        self.tela_atual = TelaInicial(self, self.mostrar_tela_dificuldade)

    def mostrar_tela_dificuldade(self):
        self.limpar_tela()
        self.tela_atual = TelaDificuldade(self, self.mostrar_tela_jogo)

    def mostrar_tela_jogo(self, dificuldade):
        self.limpar_tela()
        self.tela_atual = TelaJogo(self, dificuldade)


if __name__ == "__main__":
    app = JogoDaForca()
    app.mainloop()

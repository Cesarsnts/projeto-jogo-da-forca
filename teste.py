import tkinter as tk
import random
import os
from game import Game


class TelaInicial(tk.Frame):
    def __init__(self, master, ir_dificuldade_callback):
        super().__init__(master, bg="#ffe0b2")
        self.ir_dificuldade_callback = ir_dificuldade_callback
        self.pack(fill="both", expand=True)
        self.criar_widgets()

    def criar_widgets(self):
        container = tk.Frame(self, bg="#ffe0b2")
        container.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(container, text="🎮 Jogo da Forca", font=("Segoe UI", 32, "bold"), fg="#ffb300", bg="#ffe0b2").pack(pady=30)
        btn_jogar = tk.Button(container, text="Jogar", font=("Segoe UI", 20, "bold"), bg="#4fc3f7", fg="white", bd=0, relief="flat", activebackground="#0288d1", activeforeground="white", cursor="hand2", padx=30, pady=10, highlightthickness=0)
        btn_jogar.pack(pady=20)
        btn_jogar.bind("<Enter>", lambda e: btn_jogar.config(bg="#0288d1"))
        btn_jogar.bind("<Leave>", lambda e: btn_jogar.config(bg="#4fc3f7"))
        btn_jogar.config(command=self.ir_dificuldade_callback)


class TelaDificuldade(tk.Frame):
    def __init__(self, master, iniciar_callback):
        super().__init__(master, bg="#ffe0b2")
        self.iniciar_callback = iniciar_callback
        self.pack(fill="both", expand=True)
        self.criar_widgets()

    def criar_widgets(self):
        container = tk.Frame(self, bg="#ffe0b2")
        container.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(container, text="Selecione a Dificuldade", font=("Segoe UI", 26, "bold"), fg="#ffb300", bg="#ffe0b2").pack(pady=25)
        btns = []
        for txt, diff, cor in [
            ("Fácil (3-7 letras)", "facil", "#aed581"),
            ("Médio (8-15 letras)", "medio", "#4fc3f7"),
            ("Difícil (16-35 letras)", "dificil", "#ffb300")]:
            btn = tk.Button(container, text=txt, font=("Segoe UI", 18), bg=cor, fg="#212121", bd=0, relief="flat", activebackground="#0288d1", activeforeground="white", cursor="hand2", padx=20, pady=8, highlightthickness=0, width=20)
            btn.pack(pady=8)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#0288d1", fg="white"))
            btn.bind("<Leave>", lambda e, b=btn, c=cor: b.config(bg=c, fg="#212121"))
            btn.config(command=lambda d=diff: self.iniciar_callback(d))
            btns.append(btn)
        btn_voltar = tk.Button(container, text="Voltar", font=("Segoe UI", 16), bg="#ffe082", fg="#212121", bd=0, relief="flat", activebackground="#ffb300", activeforeground="white", cursor="hand2", padx=20, pady=8, highlightthickness=0, width=20)
        btn_voltar.pack(pady=12)
        btn_voltar.bind("<Enter>", lambda e: btn_voltar.config(bg="#ffb300", fg="white"))
        btn_voltar.bind("<Leave>", lambda e: btn_voltar.config(bg="#ffe082", fg="#212121"))
        btn_voltar.config(command=self.voltar)
        btn_fechar = tk.Button(container, text="Fechar", font=("Segoe UI", 16), bg="#e57373", fg="white", bd=0, relief="flat", activebackground="#b71c1c", activeforeground="white", cursor="hand2", padx=20, pady=8, highlightthickness=0, width=20)
        btn_fechar.pack(pady=4)
        btn_fechar.bind("<Enter>", lambda e: btn_fechar.config(bg="#b71c1c"))
        btn_fechar.bind("<Leave>", lambda e: btn_fechar.config(bg="#e57373"))
        btn_fechar.config(command=self.master.destroy)

    def voltar(self):
        self.master.mostrar_tela_inicial()


class TelaJogo(tk.Frame):
    def __init__(self, master, dificuldade):
        super().__init__(master, bg="#ffe0b2")
        self.dificuldade = dificuldade
        palavras = self.carregar_palavras_externas() or [
            "gato", "computador", "python", "programacao", "dificuldade", "desenvolvimento",
            "extraordinario", "hipopotomonstrosesquipedaliofobia", "elefante", "janela", "telefone"
        ]
        self.game = Game(palavras, dificuldade)
        self.pack(fill="both", expand=True)
        self.bg_img = None
        self.criar_widgets()

    def carregar_palavras_externas(self):
        path = os.path.join(os.path.dirname(__file__), "palavras.txt")
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    words = [l.strip() for l in f if l.strip()]
                    return words
            except Exception:
                return None
        return None

    def criar_widgets(self):
        container = tk.Frame(self, bg="#ffe0b2")
        container.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(container, text="Jogo da Forca", font=("Segoe UI", 26, "bold"), fg="#ffb300", bg="#ffe0b2").pack(pady=10)
        self.canvas = tk.Canvas(container, width=400, height=400, bg="#81d4fa", highlightthickness=2, highlightbackground="#4fc3f7")
        self.canvas.pack(pady=10)
        self.carregar_imagem_fundo()
        self.desenhar_forca()
        self.lbl_palavra = tk.Label(container, text=" ".join(self.game.revealed), font=("Segoe UI", 28, "bold"), bg="#ffe0b2", fg="#212121")
        self.lbl_palavra.pack(pady=18)
        info_panel = tk.Frame(container, bg="#fffde7", bd=2, relief="ridge")
        info_panel.pack(pady=8, fill="x")
        self.lbl_info = tk.Label(info_panel, text=f"Tentativas restantes: {self.game.attempts_left}", font=("Segoe UI", 16), bg="#fffde7", fg="#0288d1")
        self.lbl_info.pack(side="left", padx=10, pady=4)
        self.lbl_letras = tk.Label(info_panel, text="Letras usadas: ", font=("Segoe UI", 14), bg="#fffde7", fg="#212121")
        self.lbl_letras.pack(side="right", padx=10, pady=4)
        self.letras_frame = tk.Frame(container, bg="#ffe0b2")
        self.letras_frame.pack(pady=18)
        self.criar_botoes_letras()
        btns_panel = tk.Frame(container, bg="#ffe0b2")
        btns_panel.pack(pady=10)
        btn_voltar = tk.Button(btns_panel, text="Voltar ao Menu", font=("Segoe UI", 15), bg="#ffe082", fg="#212121", bd=0, relief="flat", activebackground="#ffb300", activeforeground="white", cursor="hand2", padx=18, pady=6, highlightthickness=0)
        btn_voltar.pack(side="left", padx=8)
        btn_voltar.bind("<Enter>", lambda e: btn_voltar.config(bg="#ffb300", fg="white"))
        btn_voltar.bind("<Leave>", lambda e: btn_voltar.config(bg="#ffe082", fg="#212121"))
        btn_voltar.config(command=self.master.mostrar_tela_inicial)
        btn_fechar = tk.Button(btns_panel, text="Fechar", font=("Segoe UI", 15), bg="#e57373", fg="white", bd=0, relief="flat", activebackground="#b71c1c", activeforeground="white", cursor="hand2", padx=18, pady=6, highlightthickness=0)
        btn_fechar.pack(side="left", padx=8)
        btn_fechar.bind("<Enter>", lambda e: btn_fechar.config(bg="#b71c1c"))
        btn_fechar.bind("<Leave>", lambda e: btn_fechar.config(bg="#e57373"))
        btn_fechar.config(command=self.master.destroy)

    def criar_botoes_letras(self):
        alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for i, letra in enumerate(alfabeto):
            btn = tk.Button(self.letras_frame, text=letra, width=4, font=("Segoe UI", 14, "bold"), bg="#4fc3f7", fg="white", bd=0, relief="flat", activebackground="#0288d1", activeforeground="white", cursor="hand2", padx=2, pady=2, highlightthickness=0)
            btn.grid(row=i // 9, column=i % 9, padx=3, pady=3)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#0288d1"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#4fc3f7"))
            btn.config(command=lambda l=letra: self.tentar_letra(l))

    def tentar_letra(self, letra):
        letra = letra.lower()
        result = self.game.guess(letra)
        if result is None:
            return
        self.lbl_letras.config(text=f"Letras usadas: {', '.join(self.game.tried_letters)}")
        self.atualizar_tela()

    def atualizar_tela(self):
        self.lbl_palavra.config(text=" ".join(self.game.revealed))
        self.lbl_info.config(text=f"Tentativas restantes: {self.game.attempts_left}")
        self.desenhar_forca()
        if self.game.is_won():
            self.fim_jogo(True)
        elif self.game.is_lost():
            self.fim_jogo(False)

    def carregar_imagem_fundo(self):
        try:
            self.bg_img = tk.PhotoImage(file="forca.png")
        except Exception:
            self.bg_img = None

    def desenhar_forca(self):
        self.canvas.delete("all")
        if self.bg_img:
            self.canvas.create_image(0, 0, anchor="nw", image=self.bg_img)
        # base da forca e boneco sobrepostos (ajustado para 400x400)
        self.canvas.create_line(200, 320, 320, 320, width=7, fill="#616161")
        self.canvas.create_line(260, 320, 260, 100, width=7, fill="#616161")
        self.canvas.create_line(260, 100, 340, 100, width=7, fill="#616161")
        self.canvas.create_line(340, 100, 340, 150, width=7, fill="#616161")
        partes = [
            lambda: self.canvas.create_oval(320, 150, 360, 190, width=5, outline="#212121"),
            lambda: self.canvas.create_line(340, 190, 340, 260, width=5, fill="#212121"),
            lambda: self.canvas.create_line(340, 210, 320, 240, width=5, fill="#212121"),
            lambda: self.canvas.create_line(340, 210, 360, 240, width=5, fill="#212121"),
            lambda: self.canvas.create_line(340, 260, 320, 300, width=5, fill="#212121"),
            lambda: self.canvas.create_line(340, 260, 360, 300, width=5, fill="#212121"),
        ]
        erros = self.game.errors()
        for i in range(min(erros, len(partes))):
            partes[i]()

    def fim_jogo(self, venceu):
        msg = "Você venceu! 🎉" if venceu else f"Você perdeu! 😢\nA palavra era: {self.game.palavra}"
        self.lbl_info.config(text=msg)
        for widget in self.letras_frame.winfo_children():
            widget.config(state="disabled")


class JogoDaForca(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Jogo da Forca")
        self.geometry("500x600")
        self.configure(bg="#ffe0b2")
        self.tela_atual = None
        self.mostrar_tela_inicial()

    def limpar_tela(self):
        if self.tela_atual is not None:
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
import tkinter as tk
import random
import math

class TelaInicial(tk.Frame):
    def __init__(self, master, iniciar_callback):
        super().__init__(master, bg="#87CEEB")
        self.iniciar_callback = iniciar_callback
        self.pack(fill="both", expand=True)
        self.criar_widgets()

    def criar_widgets(self):
        tk.Label(self, text="🎮 Jogo da Forca", font=("Arial", 24), bg="#87CEEB").pack(pady=50)
        tk.Button(self, text="Jogar", font=("Arial", 18), command=self.iniciar_callback).pack()


class TelaJogo(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#87CEEB")
        self.pack(fill="both", expand=True)
        self.palavras = ["GATO", "BOLA", "SOL", "LIVRO", "MESA", "CASA", "PATO"]
        self.resetar_jogo()
        self.criar_widgets()

    def resetar_jogo(self):
        self.palavra = random.choice(self.palavras)
        self.letras_certas = set()
        self.letras_erradas = set()
        self.tentativas_restantes = 6

    def criar_widgets(self):
        self.canvas = tk.Canvas(self, width=400, height=300, bg="#87CEEB", highlightthickness=0)
        self.canvas.pack(pady=10)
        self.desenhar_cenario()
        self.desenhar_forca()

        self.label_palavra = tk.Label(self, text=self.mostrar_palavra(), font=("Courier", 30), bg="#87CEEB")
        self.label_palavra.pack(pady=10)

        self.entry_letra = tk.Entry(self, font=("Arial", 20), width=3, justify="center")
        self.entry_letra.pack()
        self.entry_letra.bind("<Return>", self.tentar_letra)

        self.label_tentativas = tk.Label(self, text=f"Tentativas restantes: {self.tentativas_restantes}", font=("Arial", 16), bg="#87CEEB")
        self.label_tentativas.pack(pady=10)

        self.label_msg = tk.Label(self, text="", font=("Arial", 16), fg="blue", bg="#87CEEB")
        self.label_msg.pack()

    def desenhar_cenario(self):
        c = self.canvas
        c.create_rectangle(0, 250, 400, 300, fill="#228B22", width=0)  # grama
        c.create_oval(320, 20, 370, 70, fill="yellow", outline="orange", width=2)  # sol
        for i in range(8):
            ang = i * 45
            x1 = 345 + 30 * math.cos(math.radians(ang))
            y1 = 45 + 30 * math.sin(math.radians(ang))
            x2 = 345 + 45 * math.cos(math.radians(ang))
            y2 = 45 + 45 * math.sin(math.radians(ang))
            c.create_line(x1, y1, x2, y2, fill="orange", width=2)

    def mostrar_palavra(self):
        return " ".join([l if l in self.letras_certas else "_" for l in self.palavra])

    def tentar_letra(self, event=None):
        letra = self.entry_letra.get().strip().upper()
        self.entry_letra.delete(0, tk.END)
        if len(letra) != 1 or not letra.isalpha():
            self.label_msg.config(text="Digite uma letra válida!")
            return
        if letra in self.letras_certas or letra in self.letras_erradas:
            self.label_msg.config(text="Você já tentou essa letra!")
            return
        if letra in self.palavra:
            self.letras_certas.add(letra)
            self.label_msg.config(text="Acertou!")
        else:
            self.letras_erradas.add(letra)
            self.tentativas_restantes -= 1
            self.label_msg.config(text="Errou!")
            self.desenhar_parte()

        self.label_palavra.config(text=self.mostrar_palavra())
        self.label_tentativas.config(text=f"Tentativas restantes: {self.tentativas_restantes}")

        if self.venceu():
            self.label_msg.config(text="🎉 Você venceu!")
            self.entry_letra.config(state="disabled")
        elif self.perdeu():
            self.label_msg.config(text=f"💀 Você perdeu! Palavra: {self.palavra}")
            self.label_palavra.config(text=self.palavra)
            self.entry_letra.config(state="disabled")

    def venceu(self):
        return all(l in self.letras_certas for l in self.palavra)

    def perdeu(self):
        return self.tentativas_restantes <= 0

    def desenhar_forca(self):
        c = self.canvas
        c.create_line(50, 280, 180, 280, width=4)  # base
        c.create_line(90, 280, 90, 50, width=4)    # vertical
        c.create_line(90, 50, 180, 50, width=4)    # topo
        c.create_line(180, 50, 180, 80, width=4)   # corda

    def desenhar_parte(self):
        partes = [
            lambda: self.canvas.create_oval(160, 80, 200, 120, width=3),  # cabeça
            lambda: self.canvas.create_line(180, 120, 180, 180, width=3), # tronco
            lambda: self.canvas.create_line(180, 130, 150, 160, width=3), # braço esquerdo
            lambda: self.canvas.create_line(180, 130, 210, 160, width=3), # braço direito
            lambda: self.canvas.create_line(180, 180, 160, 220, width=3), # perna esquerda
            lambda: self.canvas.create_line(180, 180, 200, 220, width=3), # perna direita
        ]
        erros = len(self.letras_erradas)
        if erros <= len(partes):
            partes[erros - 1]()


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Jogo da Forca")
        self.geometry("400x500")
        self.resizable(False, False)

        self.tela_inicial = TelaInicial(self, self.iniciar_jogo)

    def iniciar_jogo(self):
        self.tela_inicial.pack_forget()
        self.tela_jogo = TelaJogo(self)


if __name__ == "__main__":
    app = App()
    app.mainloop()

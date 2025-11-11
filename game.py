import random

ATTEMPTS_BY_DIFFICULTY = {
    "facil": 6,
    "medio": 10,
    "dificil": 15,
}

class Game:
    """Lógica do jogo independente da interface."""
    def __init__(self, palavras, dificuldade="facil"):
        self.dificuldade = dificuldade
        self.palavras = palavras
        self.max_attempts = ATTEMPTS_BY_DIFFICULTY.get(dificuldade, 6)
        self.palavra = self._sortear_palavra()
        self.revealed = ["_" for _ in self.palavra]
        self.attempts_left = self.max_attempts
        self.tried_letters = []

    def _sortear_palavra(self):
        if self.dificuldade == "facil":
            candidates = [p for p in self.palavras if 3 <= len(p) <= 7]
        elif self.dificuldade == "medio":
            candidates = [p for p in self.palavras if 8 <= len(p) <= 15]
        else:
            candidates = [p for p in self.palavras if 16 <= len(p) <= 35]

        if not candidates:
            candidates = ["hipopotomonstrosesquipedaliofobia"]
        return random.choice(candidates)

    def guess(self, letra):
        letra = letra.lower()
        if letra in self.tried_letters or not letra.isalpha() or len(letra) != 1:
            return None
        self.tried_letters.append(letra)
        if letra in self.palavra:
            for i, c in enumerate(self.palavra):
                if c == letra:
                    self.revealed[i] = letra
            return True
        else:
            self.attempts_left -= 1
            return False

    def is_won(self):
        return "_" not in self.revealed

    def is_lost(self):
        return self.attempts_left <= 0

    def errors(self):
        return self.max_attempts - self.attempts_left

    def revealed_word(self):
        return "".join(self.revealed)

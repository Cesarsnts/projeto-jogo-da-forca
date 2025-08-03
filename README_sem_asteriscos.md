# Jogo da Forca

## 1. Visão Geral  
Tecnologias Utilizadas: Python 3.10+  
Modo de Execução: Interface gráfica (Tkinter) com possibilidade futura de outras interfaces (ex: Pygame) e suporte para console.  
Descrição:  
Implementação modular do clássico jogo da Forca com interface gráfica em Tkinter, foco educacional, boas práticas de programação, separação de responsabilidades e potencial para persistência de dados.  

Objetivos:  
- Banco de palavras interno (lista inicial) e possibilidade de arquivo externo;  
- Sistema visual com desenho progressivo da forca e cenário em canvas Tkinter;  
- Controle de tentativas, letras acertadas/erradas, e mensagens ao jogador;  
- Possibilidade futura de histórico, pontuação e modos de dificuldade;  
- Base para migração ou extensão para outras interfaces.

## 2. Descrição do Projeto  
### 2.1 O que é o Jogo da Forca?  
Jogo de adivinhação de palavras onde o jogador tenta descobrir uma palavra letra por letra. A cada erro, uma parte do boneco é desenhada na forca. O objetivo é descobrir a palavra antes do desenho completo.  
Curiosidade: Reforça vocabulário e ortografia, sendo útil no ensino.

## 3. Funcionalidades Implementadas e Planejadas  

### 3.1 Funcionalidades Implementadas (Tkinter)  
- Tela inicial com botão para iniciar o jogo;  
- Tela de jogo com canvas para desenhar cenário e partes da forca;  
- Lista interna de palavras (exemplo: GATO, BOLA, SOL, etc);  
- Entrada para letras com validação;  
- Contagem de tentativas restantes;  
- Mensagens de feedback: acerto, erro, vitória e derrota;  
- Desenho progressivo da forca em seis etapas;  
- Desenho adicional do cenário (grama, sol com raios).

### 3.2 Funcionalidades Planejadas  
- Banco de palavras externo com categorias e dificuldades;  
- Sistema de pontuação e histórico de partidas;  
- Modos de dificuldade (fácil, médio, difícil);  
- Categorias e escolha de palavra por tema;  
- Persistência de dados (JSON ou banco simples);  
- Possível migração para outras interfaces visuais ou extensão para console.

## 4. Arquitetura do Código  

```
hangman/
├── main.py              # Ponto de entrada (Tkinter App)
├── game.py              # Lógica do jogo: regras, tentativas, verificação
├── words.py             # Banco de palavras (inicial e externo)
├── display.py           # Funções de desenho da forca e interface gráfica
└── utils/
    ├── scores.py        # Gerenciamento de pontuação e histórico
    └── logger.py        # Logs de execução e erros (opcional)
```

## 5. Etapas de Entrega (Cronograma Atualizado)  

| Etapa                  | Descrição                                                | Duração Estimada |
|------------------------|----------------------------------------------------------|------------------|
| 1. Estrutura Inicial    | Setup do ambiente, interface básica com Tkinter e lógica | Semana 1-2       |
| 2. Banco de Palavras e Interface Gráfica | Integração de palavras, canvas e feedback visual    | Semana 3-4       |
| 3. Funcionalidades Avançadas | Pontuação, histórico, níveis de dificuldade, persistência | Semana 5-6       |
| 4. Testes e Finalização | Testes completos, refatoração e documentação             | Semana 7-8       |
| 5. Extensão Interface   | Possível migração ou acréscimo de outras interfaces (Pygame) | Semana 9+        |

## 6. Requisitos Técnicos  

### 6.1 Python  
- Python 3.10+  
- Dependências: somente bibliotecas padrão (Tkinter, random, math)  

### 6.2 Arquivos Externos  
- `palavras.txt` (futuro): banco de palavras categorizado  
- `pontuacoes.json` (futuro): histórico de partidas  

## 7. Resumo do Código Compartilhado  

- Classe TelaInicial: Tela inicial com título e botão para iniciar o jogo;  
- Classe TelaJogo: Gerencia a lógica da partida, seleção aleatória de palavra, tratamento das tentativas, desenhos no canvas (forca + cenário), e interface de entrada de letras;  
- Classe App: Gerencia a troca de telas e inicialização da aplicação;  
- Uso de canvas para desenho do cenário e forca com partes desenhadas progressivamente conforme erros;  
- Mensagens de feedback atualizadas dinamicamente e controle de estado da entrada para bloquear após fim do jogo.

---

Se quiser, posso ajudar a modularizar este código, incluir a leitura de arquivos externos ou preparar o histórico de partidas para próximos passos! Quer ajuda nisso?

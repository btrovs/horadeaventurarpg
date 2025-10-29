import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import random

# ===============================
# CLASSES BASE E DERIVADAS
# ===============================

class Criatura:
    def __init__(self, nome, vida, ataque, imagem):
        self._nome = nome
        self._vida = vida
        self._ataque = ataque
        self._imagem = imagem

    @property
    def vida(self):
        return self._vida

    def receber_dano(self, dano):
        self._vida -= dano
        if self._vida < 0:
            self._vida = 0

    def esta_vivo(self):
        return self._vida > 0

    def atacar(self, oponente, tipo_ataque):
        raise NotImplementedError("O método atacar deve ser implementado nas subclasses.")


class Lutador(Criatura):
    def atacar(self, oponente, tipo_ataque):
        ataques = {
            "Espadada": random.randint(10, 20),
            "Chute Giratório": random.randint(15, 25),
            "Ataque Duplo": random.randint(20, 30)
        }
        dano = ataques.get(tipo_ataque, 0) + self._ataque
        oponente.receber_dano(dano)
        return f"{self._nome} usou {tipo_ataque} e causou {dano} de dano!"


class Mago(Criatura):
    def atacar(self, oponente, tipo_ataque):
        ataques = {
            "Magia de Gelo": random.randint(10, 25),
            "Explosão de Neve": random.randint(20, 30),
            "Feitiço Congelante": random.randint(25, 35)
        }
        dano = ataques.get(tipo_ataque, 0) + self._ataque
        oponente.receber_dano(dano)
        return f"{self._nome} lançou {tipo_ataque} e causou {dano} de dano!"


class DragaoDeCobertor(Criatura):
    def atacar(self, oponente, tipo_ataque):
        ataques = {
            "Enrolar no Cobertor": random.randint(15, 30),
            "Jato de Conforto": random.randint(20, 35),
            "Soneca Mortal": random.randint(25, 40)
        }
        dano = ataques.get(tipo_ataque, 0) + self._ataque
        oponente.receber_dano(dano)
        return f"{self._nome} usou {tipo_ataque} e causou {dano} de dano!"


# ===============================
# INTERFACE TKINTER
# ===============================

class BatalhaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Batalha da Aventura - Hora de Aventura")
        self.root.configure(bg="#87CEEB")

        # Criaturas iniciais
        self.finn = Lutador("Finn", 100, 20, "Finn.png")
        self.rei_gelado = Mago("Rei Gelado", 100, 18, "Rei Gelado.png")
        self.dragao = DragaoDeCobertor("Dragão de Cobertor", 120, 22, "Dragão de Cobertor.png")

        self.jogador = self.finn
        self.inimigo = random.choice([self.rei_gelado, self.dragao])

        self.criar_interface()

    def criar_interface(self):
        ttk.Label(
            self.root, text="⚔️ BATALHA MÁGICA ⚔️",
            font=("Comic Sans MS", 22, "bold"), background="#87CEEB"
        ).pack(pady=10)

        self.frame = tk.Frame(self.root, bg="#ADD8E6")
        self.frame.pack(padx=10, pady=10)

        self.img_jogador = ImageTk.PhotoImage(Image.open(self.jogador._imagem).resize((200, 200)))
        self.img_inimigo = ImageTk.PhotoImage(Image.open(self.inimigo._imagem).resize((200, 200)))

        self.label_nome_jogador = tk.Label(self.frame, text=self.jogador._nome, bg="#ADD8E6", font=("Comic Sans MS", 14, "bold"))
        self.label_nome_jogador.grid(row=0, column=0)

        self.label_nome_inimigo = tk.Label(self.frame, text=self.inimigo._nome, bg="#ADD8E6", font=("Comic Sans MS", 14, "bold"))
        self.label_nome_inimigo.grid(row=0, column=1)

        self.label_jogador_img = tk.Label(self.frame, image=self.img_jogador, bg="#ADD8E6")
        self.label_jogador_img.grid(row=1, column=0, padx=10)

        self.label_inimigo_img = tk.Label(self.frame, image=self.img_inimigo, bg="#ADD8E6")
        self.label_inimigo_img.grid(row=1, column=1, padx=10)

        self.vida_jogador = tk.Label(self.frame, text=f"Vida: {self.jogador.vida}", bg="#ADD8E6", font=("Arial", 12))
        self.vida_jogador.grid(row=2, column=0)

        self.vida_inimigo = tk.Label(self.frame, text=f"Vida: {self.inimigo.vida}", bg="#ADD8E6", font=("Arial", 12))
        self.vida_inimigo.grid(row=2, column=1)

        self.texto_batalha = tk.Label(self.root, text="", bg="#87CEEB", font=("Arial", 12))
        self.texto_batalha.pack(pady=10)

        self.frame_botoes = tk.Frame(self.root, bg="#87CEEB")
        self.frame_botoes.pack()

        self.atualizar_botoes_ataque()

        self.botao_trocar = tk.Button(
            self.root, text="🔄 Trocar Oponente", bg="#FFA500", fg="white",
            font=("Comic Sans MS", 12, "bold"), command=self.trocar_oponente
        )
        self.botao_trocar.pack_forget()

    def atualizar_botoes_ataque(self):
        for widget in self.frame_botoes.winfo_children():
            widget.destroy()

        ataques = []
        if isinstance(self.jogador, Lutador):
            ataques = ["Espadada", "Chute Giratório", "Ataque Duplo"]
        elif isinstance(self.jogador, Mago):
            ataques = ["Magia de Gelo", "Explosão de Neve", "Feitiço Congelante"]
        elif isinstance(self.jogador, DragaoDeCobertor):
            ataques = ["Enrolar no Cobertor", "Jato de Conforto", "Soneca Mortal"]

        for atk in ataques:
            tk.Button(
                self.frame_botoes, text=atk, command=lambda a=atk: self.atacar(a),
                bg="#32CD32", fg="white", font=("Comic Sans MS", 12, "bold"), width=20
            ).pack(pady=5)

    def atacar(self, tipo_ataque):
        if not self.jogador.esta_vivo() or not self.inimigo.esta_vivo():
            return

        msg = self.jogador.atacar(self.inimigo, tipo_ataque)
        self.texto_batalha.config(text=msg)
        self.vida_inimigo.config(text=f"Vida: {self.inimigo.vida}")

        if not self.inimigo.esta_vivo():
            self.texto_batalha.config(text=f"{self.inimigo._nome} foi derrotado! 🎉")
            self.botao_trocar.pack(pady=10)
            return

        self.root.after(1000, self.inimigo_ataca)

    def inimigo_ataca(self):
        if not self.inimigo.esta_vivo():
            return

        # Inimigo usa ataques válidos
        if isinstance(self.inimigo, Lutador):
            tipo = random.choice(["Espadada", "Chute Giratório", "Ataque Duplo"])
        elif isinstance(self.inimigo, Mago):
            tipo = random.choice(["Magia de Gelo", "Explosão de Neve", "Feitiço Congelante"])
        else:
            tipo = random.choice(["Enrolar no Cobertor", "Jato de Conforto", "Soneca Mortal"])

        msg = self.inimigo.atacar(self.jogador, tipo)
        self.texto_batalha.config(text=msg)
        self.vida_jogador.config(text=f"Vida: {self.jogador.vida}")

        if self.jogador.vida <= 25:
            self.botao_trocar.pack(pady=10)

        if not self.jogador.esta_vivo():
            self.texto_batalha.config(text="Você foi derrotado! 💀")

    def trocar_oponente(self):
        self.jogador._vida = 100
        self.inimigo = random.choice([self.rei_gelado, self.dragao])
        self.inimigo._vida = 100

        self.texto_batalha.config(text=f"Novo oponente: {self.inimigo._nome} apareceu! 💥")

        self.img_inimigo = ImageTk.PhotoImage(Image.open(self.inimigo._imagem).resize((200, 200)))
        self.label_inimigo_img.config(image=self.img_inimigo)
        self.label_nome_inimigo.config(text=self.inimigo._nome)  # ✅ Corrige bug do nome sumindo
        self.vida_inimigo.config(text=f"Vida: {self.inimigo.vida}")
        self.vida_jogador.config(text=f"Vida: {self.jogador.vida}")

        self.botao_trocar.pack_forget()

# ===============================
# EXECUÇÃO
# ===============================
if __name__ == "__main__":
    root = tk.Tk()
    app = BatalhaApp(root)
    root.mainloop()

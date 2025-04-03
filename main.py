import tkinter as tk
from tkinter import messagebox
import time
import datetime
import math
from threading import Thread

class HorlogeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Horloge, Chronomètre, Minuteur et Alarme")

        # Création des widgets
        self.heure_label = tk.Label(root, text="", font=('Helvetica', 48))
        self.heure_label.grid(row=0, column=0, padx=20, pady=10)

        self.date_label = tk.Label(root, text="", font=('Helvetica', 24))
        self.date_label.grid(row=1, column=0)

        self.alarme_label = tk.Label(root, text="Aucune alarme programmée", font=('Helvetica', 16), fg="red")
        self.alarme_label.grid(row=2, column=0)

        # Créer le canvas pour l'horloge analogique
        self.canvas = tk.Canvas(root, width=200, height=200, bg='white')
        self.canvas.grid(row=0, column=1, rowspan=3, padx=20, pady=10)

        # Boutons
        self.bouton_chronometre = tk.Button(root, text="Démarrer Chronomètre", command=self.demarrer_chronometre)
        self.bouton_chronometre.grid(row=3, column=0, pady=5)

        self.bouton_minuteur = tk.Button(root, text="Démarrer Minuteur", command=self.demarrer_minuteur)
        self.bouton_minuteur.grid(row=4, column=0, pady=5)

        self.bouton_alarme = tk.Button(root, text="Régler Alarme", command=self.regler_alarme)
        self.bouton_alarme.grid(row=5, column=0, pady=5)

        self.bouton_quitter = tk.Button(root, text="Quitter", command=root.quit)
        self.bouton_quitter.grid(row=6, column=0, pady=5)

        # Variables
        self.alarme_heure = None
        self.chrono_running = False
        self.minuteur_running = False

        # Mettre à jour l'heure et la date en temps réel
        self.mise_a_jour_heure()
        self.dessiner_horloge()

    def mise_a_jour_heure(self):
        """Mise à jour de l'heure et la date en continu."""
        heure_actuelle = datetime.datetime.now().strftime("%H:%M:%S")
        date_actuelle = datetime.datetime.now().strftime("%Y-%m-%d")
        self.heure_label.config(text=heure_actuelle)
        self.date_label.config(text=date_actuelle)

        # Vérification de l'alarme
        if self.alarme_heure and datetime.datetime.now().strftime("%H:%M") == self.alarme_heure:
            messagebox.showinfo("Alarme", f"Il est maintenant {self.alarme_heure} !")
            self.alarme_heure = None
            self.alarme_label.config(text="Aucune alarme programmée", fg="red")

        # Reprogrammer pour mise à jour toutes les 1000ms (1 seconde)
        self.root.after(1000, self.mise_a_jour_heure)

    def dessiner_horloge(self):
        """Dessine l'horloge analogique, les annotations des heures, et met à jour les aiguilles chaque seconde."""
        # Effacer l'ancienne horloge
        self.canvas.delete("all")

        # Définir le centre et le rayon de l'horloge
        centre_x, centre_y = 100, 100
        rayon = 90

        # Dessiner le cercle de l'horloge
        self.canvas.create_oval(centre_x-rayon, centre_y-rayon, centre_x+rayon, centre_y+rayon)

        # Ajouter les annotations des heures
        for i in range(1, 13):
            angle = math.radians(i * 30 - 90)  # 30 degrés par heure, en ajustant pour que 12 soit en haut
            x = centre_x + (rayon - 20) * math.cos(angle)
            y = centre_y + (rayon - 20) * math.sin(angle)
            self.canvas.create_text(x, y, text=str(i), font=('Helvetica', 12))

        # Obtenir l'heure actuelle
        maintenant = datetime.datetime.now()
        heure = maintenant.hour % 12
        minute = maintenant.minute
        seconde = maintenant.second

        # Calculer les angles pour chaque aiguille
        angle_seconde = math.radians(seconde * 6 - 90)
        angle_minute = math.radians(minute * 6 - 90)
        angle_heure = math.radians((heure + minute / 60) * 30 - 90)

        # Longueurs des aiguilles
        longueur_seconde = rayon - 20
        longueur_minute = rayon - 30
        longueur_heure = rayon - 50

        # Calculer les positions des aiguilles
        seconde_x = centre_x + longueur_seconde * math.cos(angle_seconde)
        seconde_y = centre_y + longueur_seconde * math.sin(angle_seconde)

        minute_x = centre_x + longueur_minute * math.cos(angle_minute)
        minute_y = centre_y + longueur_minute * math.sin(angle_minute)

        heure_x = centre_x + longueur_heure * math.cos(angle_heure)
        heure_y = centre_y + longueur_heure * math.sin(angle_heure)

        # Dessiner les aiguilles
        self.canvas.create_line(centre_x, centre_y, seconde_x, seconde_y, fill="red", width=2)
        self.canvas.create_line(centre_x, centre_y, minute_x, minute_y, fill="black", width=4)
        self.canvas.create_line(centre_x, centre_y, heure_x, heure_y, fill="black", width=6)

        # Reprogrammer pour redessiner l'horloge toutes les secondes
        self.root.after(1000, self.dessiner_horloge)

    def demarrer_chronometre(self):
        """Démarre le chronomètre dans un thread séparé."""
        if not self.chrono_running:
            self.chrono_running = True
            thread = Thread(target=self.chronometre)
            thread.start()

    def chronometre(self):
        """Chronomètre affiché dans une boîte de dialogue."""
        start_time = time.time()
        chrono_win = tk.Toplevel(self.root)
        chrono_win.title("Chronomètre")
        chrono_label = tk.Label(chrono_win, text="00:00", font=('Helvetica', 36))
        chrono_label.pack(pady=20)

        try:
            while self.chrono_running:
                elapsed_time = time.time() - start_time
                minutes = int(elapsed_time // 60)
                seconds = int(elapsed_time % 60)
                chrono_label.config(text=f"{minutes:02d}:{seconds:02d}")
                time.sleep(1)
        except tk.TclError:
            pass

    def demarrer_minuteur(self):
        """Ouvre une fenêtre pour démarrer un minuteur."""
        if not self.minuteur_running:
            minuteur_win = tk.Toplevel(self.root)
            minuteur_win.title("Minuteur")

            tk.Label(minuteur_win, text="Durée du minuteur (en secondes) :").pack(pady=10)
            minuteur_entry = tk.Entry(minuteur_win)
            minuteur_entry.pack(pady=5)
            tk.Button(minuteur_win, text="Démarrer", command=lambda: self.lancer_minuteur(minuteur_entry.get(), minuteur_win)).pack(pady=10)

    def lancer_minuteur(self, duree, window):
        """Lance le minuteur avec la durée spécifiée."""
        try:
            duree = int(duree)
            self.minuteur_running = True
            window.destroy()
            thread = Thread(target=self.minuteur, args=(duree,))
            thread.start()
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un nombre valide.")

    def minuteur(self, duree):
        """Fonction de minuteur."""
        minuteur_win = tk.Toplevel(self.root)
        minuteur_win.title("Minuteur")
        minuteur_label = tk.Label(minuteur_win, text="", font=('Helvetica', 36))
        minuteur_label.pack(pady=20)

        try:
            while duree and self.minuteur_running:
                minutes, seconds = divmod(duree, 60)
                minuteur_label.config(text=f"{minutes:02d}:{seconds:02d}")
                time.sleep(1)
                duree -= 1

            if duree == 0:
                messagebox.showinfo("Minuteur", "Temps écoulé !")
            self.minuteur_running = False
        except tk.TclError:
            pass

    def regler_alarme(self):
        """Ouvre une fenêtre pour régler l'alarme."""
        alarme_win = tk.Toplevel(self.root)
        alarme_win.title("Régler Alarme")

        tk.Label(alarme_win, text="Heure de l'alarme (HH:MM) :").pack(pady=10)
        alarme_entry = tk.Entry(alarme_win)
        alarme_entry.pack(pady=5)
        tk.Button(alarme_win, text="Régler", command=lambda: self.definir_alarme(alarme_entry.get(), alarme_win)).pack(pady=10)

    def definir_alarme(self, heure, window):
        """Définit l'alarme pour l'heure donnée."""
        try:
            datetime.datetime.strptime(heure, "%H:%M")
            self.alarme_heure = heure
            window.destroy()
            self.alarme_label.config(text=f"Alarme réglée pour {heure}", fg="green")
            messagebox.showinfo("Alarme", f"Alarme réglée pour {heure}")
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer une heure valide au format HH:MM.")

# Programme principal
if __name__ == "__main__":
    root = tk.Tk()
    app = HorlogeApp(root)
    root.mainloop()

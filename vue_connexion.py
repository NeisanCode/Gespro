import customtkinter as ctk
from tkinter import messagebox
from config_db import obtenir_connexion
import theme

# Configuration globale de CustomTkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class ConnexionApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("GesPro - Authentification")
        self.geometry("450x550")
        
        # 1. Autoriser le redimensionnement de la fenêtre de connexion
        self.resizable(True, True)
        self.configure(fg_color=theme.BG_FENETRE)

        # Centrer la fenêtre sur l'écran au démarrage
        self.eval('tk::PlaceWindow . center')

        # 2. Configurer la grille de la fenêtre principale pour maintenir la carte au centre
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # CONTENEUR PRINCIPAL (La carte de connexion reste de taille fixe et centrée)
        self.card = ctk.CTkFrame(
            self, 
            width=380, 
            height=470, 
            fg_color=theme.BG_CARTE,
            border_width=1,
            border_color=theme.BORDURE_CARTE
        )
        # Positionnement central automatique grâce à la grille réactive
        self.card.grid(row=0, column=0, sticky="")
        self.card.pack_propagate(False)

        # EN-TÊTE 
        self.lbl_logo = ctk.CTkLabel(
            self.card, 
            text="🎓", 
            font=("Helvetica", 45)
        )
        self.lbl_logo.pack(pady=(35, 5))

        self.lbl_titre = ctk.CTkLabel(
            self.card, 
            text="Gespro\nISPSLO - GESTION", 
            font=("Helvetica", 18, "bold"), 
            text_color=theme.TEXTE_TITRE
        )
        self.lbl_titre.pack(pady=(0, 5))

        self.lbl_soustitre = ctk.CTkLabel(
            self.card, 
            text="Veuillez vous authentifier pour continuer", 
            font=("Helvetica", 11), 
            text_color=theme.TEXTE_SECONDAIRE
        )
        self.lbl_soustitre.pack(pady=(0, 25))

        # FORMULAIRE 
        # Identifiant / Nom d'utilisateur
        self.lbl_user = ctk.CTkLabel(
            self.card, 
            text="Identifiant ou Email :", 
            font=("Helvetica", 11, "bold"), 
            text_color=theme.TEXTE_SECONDAIRE
        )
        self.lbl_user.pack(anchor="w", padx=40, pady=(10, 2))
        
        self.ent_username = ctk.CTkEntry(
            self.card, 
            placeholder_text="Ex: p.ngolo", 
            height=38, 
            fg_color=theme.BG_CHAMP
        )
        self.ent_username.pack(fill="x", padx=40, pady=(0, 15))

        # Mot de passe
        self.lbl_mdp = ctk.CTkLabel(
            self.card, 
            text="Mot de passe :", 
            font=("Helvetica", 11, "bold"), 
            text_color=theme.TEXTE_SECONDAIRE
        )
        self.lbl_mdp.pack(anchor="w", padx=40, pady=(0, 2))
        
        self.ent_password = ctk.CTkEntry(
            self.card, 
            placeholder_text="••••••••", 
            show="*", 
            height=38, 
            fg_color=theme.BG_CHAMP
        )
        self.ent_password.pack(fill="x", padx=40, pady=(0, 25))

        #  BOUTON DE CONNEXION 
        self.btn_connexion = ctk.CTkButton(
            self.card, 
            text="SE CONNECTER", 
            font=("Helvetica", 12, "bold"),
            fg_color=theme.BOUTON_PRIMARY, 
            hover_color=theme.BOUTON_PRIMARY_HOVER,
            command=self.valider_connexion,
            height=40
        )
        self.btn_connexion.pack(fill="x", padx=40, pady=(5, 10))

        # Raccourci touche "Entrée" pour soumettre le formulaire
        self.bind("<Return>", lambda event: self.valider_connexion())

    def valider_connexion(self):
        """Vérifie les identifiants dans la base de données et gère la redirection."""
        username = self.ent_username.get().strip()
        password = self.ent_password.get().strip()

        # Validation basique des champs vides
        if not username or not password:
            messagebox.showwarning("Champs requis", "Veuillez remplir tous les champs.")
            return

        conn = None
        try:
            conn = obtenir_connexion()
            cursor = conn.cursor(dictionary=True)

            query = """
                SELECT nom, prenom 
                FROM Utilisateur 
                WHERE (username = %s OR email = %s) AND mot_de_passe = %s
            """
            cursor.execute(query, (username, username, password))
            utilisateur = cursor.fetchone()

            cursor.close()
            conn.close()

            if utilisateur:
                nom_complet = f"{utilisateur['prenom']} {utilisateur['nom'].upper()}"
                
                # --- REDIRECTION SÉCURISÉE VERS LE MENU PRINCIPAL ---
                self.destroy() 
                
                from menu_app import MenuPrincipalApp
                app = MenuPrincipalApp(nom_gestionnaire=nom_complet)
                app.mainloop()
            else:
                messagebox.showerror("Authentification échouée", "Identifiant ou mot de passe incorrect.")

        except Exception as e:
            print(f"[Mode Dev / Erreur SQL] : Impossible de requêter la BDD ({e})")
            
            # Simulation pour le développement (identifiants par défaut : admin / admin)
            if username == "admin" and password == "admin":
                self.destroy()
                from menu_app import MenuPrincipalApp
                app = MenuPrincipalApp(nom_gestionnaire="Administrateur (Mode Dev)")
                app.mainloop()
            else:
                messagebox.showerror(
                    "Erreur de Connexion", 
                    f"Impossible de se connecter à la base de données.\n\n"
                    f"Astuce de test local : utilise l'identifiant 'admin' et le mot de passe 'admin' pour passer outre."
                )

if __name__ == "__main__":
    app = ConnexionApp()
    app.mainloop()
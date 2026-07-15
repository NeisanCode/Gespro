import customtkinter as ctk
import sys
import theme

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class MenuPrincipalApp(ctk.CTk):
    def __init__(self, nom_gestionnaire="Gestionnaire"):
        super().__init__()
        self.title("GesPro - Menu Principal")
        self.geometry("750x500")
        
        # 1. On permet à la fenêtre d'être agrandie
        self.resizable(True, True)
        self.configure(fg_color=theme.BG_FENETRE)

        # Configurer la grille de la fenêtre principale pour centrer le contenu verticalement
        self.grid_rowconfigure(0, weight=1)  # Espace flexible au-dessus
        self.grid_rowconfigure(1, weight=0)  # Label Bienvenue
        self.grid_rowconfigure(2, weight=0)  # Titre Principal
        self.grid_rowconfigure(3, weight=2)  # Conteneur des Cartes (prend le plus d'espace)
        self.grid_rowconfigure(4, weight=0)  # Bouton Déconnexion
        self.grid_rowconfigure(5, weight=1)  # Espace flexible en dessous
        
        self.grid_columnconfigure(0, weight=1) # Centrage horizontal de la colonne principale

        # Message de bienvenue personnalisé
        self.lbl_bienvenue = ctk.CTkLabel(
            self, 
            text=f"Bienvenue, {nom_gestionnaire} ", 
            font=("Helvetica", 16, "italic"), 
            text_color=theme.TEXTE_SECONDAIRE
        )
        self.lbl_bienvenue.grid(row=1, column=0, pady=(30, 5), sticky="nsew")

        self.titre = ctk.CTkLabel(
            self, 
            text="Gespro\nPORTAIL DE GESTION ISPSLO", 
            font=("Helvetica", 22, "bold"), 
            text_color=theme.TEXTE_TITRE
        )
        self.titre.grid(row=2, column=0, pady=(0, 20), sticky="nsew")

        # Conteneur pour les boutons (réactif)
        self.cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.cards_frame.grid(row=3, column=0, padx=40, pady=10, sticky="nsew")

        # Configurer la grille interne pour que les deux cartes se partagent l'espace à 50/50
        self.cards_frame.grid_columnconfigure(0, weight=1, uniform="group1")
        self.cards_frame.grid_columnconfigure(1, weight=1, uniform="group1")
        self.cards_frame.grid_rowconfigure(0, weight=1)

        # --- CARTE 1 : INSCRIPTIONS & RÉINSCRIPTIONS ---
        self.btn_inscription = ctk.CTkButton(
            self.cards_frame,
            text="📝\n\nINSCRIPTIONS &\nRÉINSCRIPTIONS\n",
            font=("Helvetica", 14, "bold"),
            fg_color=theme.BG_CARTE,
            hover_color="#E2E8F0",
            text_color=theme.TEXTE_TITRE,
            border_width=2,
            border_color=theme.BORDURE_CARTE,
            corner_radius=12,
            command=self.ouvrir_inscriptions
        )
        self.btn_inscription.grid(row=0, column=0, padx=(0, 15), sticky="nsew")

        # --- CARTE 2 : CAISSE & SCOLARITÉS ---
        self.btn_paiement = ctk.CTkButton(
            self.cards_frame,
            text="💳\n\nGESTION DES CAISSES\n&\nSCOLARITÉS\n",
            font=("Helvetica", 14, "bold"),
            fg_color=theme.BG_CARTE,
            hover_color="#E2E8F0",
            text_color=theme.TEXTE_TITRE,
            border_width=2,
            border_color=theme.BORDURE_CARTE,
            corner_radius=12,
            command=self.ouvrir_paiements
        )
        self.btn_paiement.grid(row=0, column=1, padx=(15, 0), sticky="nsew")

        # Bouton Déconnexion
        self.btn_deco = ctk.CTkButton(
            self,
            text="Se déconnecter",
            font=("Helvetica", 11, "bold"),
            fg_color="#EF4444",
            hover_color="#DC2626",
            text_color="white",
            height=35,
            width=120,
            command=self.deconnexion
        )
        self.btn_deco.grid(row=4, column=0, pady=25)

    def ouvrir_inscriptions(self):
        self.destroy() # Ferme le menu
        from inscription_app import GesProInscriptionApp
        app = GesProInscriptionApp()
        app.mainloop()

    def ouvrir_paiements(self):
        self.destroy() # Ferme le menu
        from paiement_app import GesProPaiementApp
        app = GesProPaiementApp()
        app.mainloop()

    def deconnexion(self):
        self.destroy()
        from vue_connexion import ConnexionApp
        app = ConnexionApp()
        app.mainloop()

if __name__ == "__main__":
    app = MenuPrincipalApp()
    app.mainloop()
import os
import sys
import subprocess
import customtkinter as ctk
from tkinter import messagebox
from datetime import date

# ReportLab pour la génération du reçu mensuel conforme
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

from config_db import obtenir_connexion
import theme

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class GesProPaiementApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("GesPro - Gestion des Encaissements Scolarité")
        self.geometry("950x720")
        self.configure(fg_color=theme.BG_FENETRE)

        # Titre Principal
        self.titre = ctk.CTkLabel(
            self, 
            text="GESTION DES ENCAISSEMENTS ET SCOLARITÉS", 
            font=("Helvetica", 18, "bold"), 
            text_color=theme.TEXTE_TITRE
        )
        self.titre.pack(pady=(20, 5))

        # Main Container
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=10)

        # --- GAUCHE : FORMULAIRE DE SAISIE ---
        self.left_col = ctk.CTkFrame(self.main_container, width=440, fg_color=theme.BG_CARTE, border_width=1, border_color=theme.BORDURE_CARTE)
        self.left_col.pack(side="left", fill="both", expand=True, padx=(0, 10))
        self.left_col.pack_propagate(False)

        # --- DROITE : RÉCAPITULATIF & ÉTAT DES MOIS ---
        self.right_col = ctk.CTkFrame(self.main_container, width=440, fg_color=theme.BG_CARTE, border_width=1, border_color=theme.BORDURE_CARTE)
        self.right_col.pack(side="right", fill="both", expand=True, padx=(10, 0))
        self.right_col.pack_propagate(False)

        self.creer_formulaire_paiement()
        self.creer_recapitulatif()

    def creer_formulaire_paiement(self):
        header_form = ctk.CTkFrame(self.left_col, fg_color="transparent")
        header_form.pack(fill="x", padx=30, pady=(20, 10))
        
        ctk.CTkLabel(header_form, text="Nouveau Versement", font=("Helvetica", 14, "bold"), text_color=theme.TEXTE_TITRE).pack(side="left")

        # Recherche par MATRICULE
        ctk.CTkLabel(self.left_col, text="Matricule de l'Élève :", font=("Helvetica", 11, "bold"), text_color=theme.TEXTE_SECONDAIRE).pack(anchor="w", padx=30, pady=(10, 2))
        
        search_frame = ctk.CTkFrame(self.left_col, fg_color="transparent")
        search_frame.pack(fill="x", padx=30, pady=5)
        
        self.ent_matricule = ctk.CTkEntry(search_frame, placeholder_text="Ex: 2026-GCP-0042", height=38, fg_color=theme.BG_CHAMP)
        self.ent_matricule.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.ent_matricule.bind("<Return>", lambda event: self.rechercher_par_matricule())
        
        self.btn_charger = ctk.CTkButton(
            search_frame, 
            text="🔍 Rechercher", 
            width=100, 
            height=38, 
            fg_color="#4A5568", 
            hover_color="#718096",
            command=self.rechercher_par_matricule
        )
        self.btn_charger.pack(side="right")

        # Type de frais
        ctk.CTkLabel(self.left_col, text="Nature du versement :", font=("Helvetica", 11, "bold"), text_color=theme.TEXTE_SECONDAIRE).pack(anchor="w", padx=30, pady=(10, 2))
        self.combo_type_frais = ctk.CTkComboBox(
            self.left_col, 
            values=["Frais Mensuels (Mensualité)", "Frais de Soutenance"], 
            height=38, 
            fg_color=theme.BG_CHAMP,
            command=self.gerer_changement_type_frais
        )
        self.combo_type_frais.pack(fill="x", padx=30, pady=5)

        # Choix du mois
        self.lbl_choix_mois = ctk.CTkLabel(self.left_col, text="Mois à régler :", font=("Helvetica", 11, "bold"), text_color=theme.TEXTE_SECONDAIRE)
        self.lbl_choix_mois.pack(anchor="w", padx=30, pady=(10, 2))
        
        self.combo_mois = ctk.CTkComboBox(
            self.left_col, 
            values=[f"Mois {i}" for i in range(1, 11)], 
            height=38, 
            fg_color=theme.BG_CHAMP,
            command=self.calculer_montant_suggere
        )
        self.combo_mois.pack(fill="x", padx=30, pady=5)

        # Montant
        ctk.CTkLabel(self.left_col, text="Montant à Encaisser (FCFA) :", font=("Helvetica", 11, "bold"), text_color=theme.TEXTE_SECONDAIRE).pack(anchor="w", padx=30, pady=(10, 2))
        self.ent_montant = ctk.CTkEntry(self.left_col, placeholder_text="0", height=38, fg_color=theme.BG_CHAMP)
        self.ent_montant.pack(fill="x", padx=30, pady=5)

        # Mode de règlement
        ctk.CTkLabel(self.left_col, text="Mode de Paiement :", font=("Helvetica", 11, "bold"), text_color=theme.TEXTE_SECONDAIRE).pack(anchor="w", padx=30, pady=(10, 2))
        self.combo_mode = ctk.CTkComboBox(self.left_col, values=["Mobile Money (Airtel Money)", "Mobile Money (MTN MoMo)", "Espèces", "Chèque"], height=38, fg_color=theme.BG_CHAMP)
        self.combo_mode.pack(fill="x", padx=30, pady=5)

        # Bouton d'action
        self.btn_enregistrer = ctk.CTkButton(
            self.left_col, 
            text="VALIDER ET IMPRIMER LE REÇU", 
            font=("Helvetica", 13, "bold"),
            fg_color="#10B981", 
            hover_color="#059669",
            command=self.enregistrer_paiement,
            height=45
        )
        self.btn_enregistrer.pack(fill="x", padx=30, pady=(25, 10))

    def creer_recapitulatif(self):
        ctk.CTkLabel(self.right_col, text="Dossier Financier de l'Élève", font=("Helvetica", 14, "bold"), text_color=theme.TEXTE_TITRE).pack(anchor="w", padx=30, pady=(20, 10))

        self.lbl_nom = self.creer_info_row("Élève :", "Aucun élève chargé")
        self.lbl_classe = self.creer_info_row("Filière & Niveau :", "Non spécifié")
        self.lbl_scolarite_totale = self.creer_info_row("Scolarité Annuelle :", "0 FCFA")
        self.lbl_mensualite_attendue = self.creer_info_row("Montant par mois (sur 10 mois) :", "0 FCFA")
        
        sep = ctk.CTkFrame(self.right_col, height=1, fg_color=theme.BORDURE_CARTE)
        sep.pack(fill="x", padx=30, pady=10)

        ctk.CTkLabel(self.right_col, text="Suivi de la Caisse (Mensualités)", font=("Helvetica", 12, "bold"), text_color=theme.TEXTE_TITRE).pack(anchor="w", padx=30, pady=(0, 5))
        
        self.mois_frame = ctk.CTkFrame(self.right_col, fg_color="transparent")
        self.mois_frame.pack(fill="both", expand=True, padx=30, pady=5)
        
        self.widgets_mois = {}
        for i in range(1, 11):
            row = ctk.CTkFrame(self.mois_frame, fg_color="transparent")
            row.pack(fill="x", pady=2)
            lbl = ctk.CTkLabel(row, text=f"Mois {i} :", font=("Helvetica", 11, "bold"), text_color=theme.TEXTE_SECONDAIRE)
            lbl.pack(side="left")
            status_lbl = ctk.CTkLabel(row, text="Non payé ❌", font=("Helvetica", 11, "italic"), text_color="#EF4444")
            status_lbl.pack(side="right")
            self.widgets_mois[i] = status_lbl

        self.current_inscription_id = None
        self.current_scolarite_annuelle = 0
        self.current_mensualite = 0
        self.historique_mensuel = {}

    def creer_info_row(self, label_text, default_value):
        row = ctk.CTkFrame(self.right_col, fg_color="transparent")
        row.pack(fill="x", padx=30, pady=4)
        ctk.CTkLabel(row, text=label_text, font=("Helvetica", 11, "bold"), text_color=theme.TEXTE_SECONDAIRE).pack(side="left")
        value_lbl = ctk.CTkLabel(row, text=default_value, font=("Helvetica", 12, "bold"))
        value_lbl.pack(side="right")
        return value_lbl

    def gerer_changement_type_frais(self, choix):
        if choix == "Frais de Soutenance":
            self.combo_mois.configure(state="disabled")
            self.ent_montant.delete(0, "end")
            self.ent_montant.insert(0, "50000")
        else:
            self.combo_mois.configure(state="normal")
            self.calculer_montant_suggere()

    def calculer_montant_suggere(self, event=None):
        choix_mois_str = self.combo_mois.get()
        if not choix_mois_str or not self.current_inscription_id:
            return
        num_mois = int(choix_mois_str.replace("Mois ", ""))
        deja_paye = self.historique_mensuel.get(num_mois, 0)
        reste_du = self.current_mensualite - deja_paye
        self.ent_montant.delete(0, "end")
        self.ent_montant.insert(0, str(max(0, reste_du)))

    def rechercher_par_matricule(self):
        matricule = self.ent_matricule.get().strip()
        if not matricule:
            messagebox.showwarning("Erreur", "Veuillez saisir un matricule.")
            return

        try:
            conn = obtenir_connexion()
            cursor = conn.cursor(dictionary=True)

            query = """
                SELECT i.id as inscription_id, e.nom, e.prenom, n.niveau, f.nom as filiere_nom
                FROM Inscription i
                JOIN Eleve e ON i.etudiant_id = e.id
                JOIN Programme p ON i.programme_id = p.id
                JOIN Filiere f ON p.filiere_id = f.id
                JOIN Niveau n ON p.niveau_id = n.id
                JOIN Annee_academique aa ON i.annee_academique_id = aa.id
                WHERE e.matricule = %s AND aa.statut = 'Active'
            """
            cursor.execute(query, (matricule,))
            res = cursor.fetchone()

            if not res:
                messagebox.showerror("Introuvable", f"Aucune inscription active trouvée pour le matricule {matricule}.")
                cursor.close()
                conn.close()
                return

            self.current_inscription_id = res['inscription_id']
            self.lbl_nom.configure(text=f"{res['nom'].upper()} {res['prenom']}")
            self.lbl_classe.configure(text=f"{res['filiere_nom']} - {res['niveau']}")

            niveau_str = res['niveau'].lower()
            if "1" in niveau_str or "première" in niveau_str:
                self.current_scolarite_annuelle = 320000
                self.current_mensualite = 32000
            elif "2" in niveau_str or "deuxième" in niveau_str:
                self.current_scolarite_annuelle = 370000
                self.current_mensualite = 37000
            elif "3" in niveau_str or "troisième" in niveau_str:
                self.current_scolarite_annuelle = 420000
                self.current_mensualite = 42000
            else:
                self.current_scolarite_annuelle = 320000
                self.current_mensualite = 32000

            self.lbl_scolarite_totale.configure(text=f"{self.current_scolarite_annuelle:,} FCFA".replace(",", " "))
            self.lbl_mensualite_attendue.configure(text=f"{self.current_mensualite:,} FCFA/mois".replace(",", " "))

            cursor.execute("""
                SELECT type_frais, SUM(montant) as total_paye 
                FROM Paiement 
                WHERE inscription_id = %s AND type_frais LIKE 'Mois %'
                GROUP BY type_frais
            """, (self.current_inscription_id,))
            versements = cursor.fetchall()
            
            self.historique_mensuel = {i: 0 for i in range(1, 11)}
            for v in versements:
                try:
                    num_mois = int(v['type_frais'].replace("Mois ", ""))
                    self.historique_mensuel[num_mois] = int(v['total_paye'])
                except ValueError:
                    pass

            for i in range(1, 11):
                total_paye_mois = self.historique_mensuel[i]
                if total_paye_mois >= self.current_mensualite:
                    self.widgets_mois[i].configure(text="Solder ✅", text_color="#10B981")
                elif total_paye_mois > 0:
                    self.widgets_mois[i].configure(text=f"Partiel ({total_paye_mois:,} F) ⚠️".replace(",", " "), text_color="#F59E0B")
                else:
                    self.widgets_mois[i].configure(text="Impayé ❌", text_color="#EF4444")

            cursor.close()
            conn.close()
            self.gerer_changement_type_frais(self.combo_type_frais.get())

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur de récupération : {e}")

    def enregistrer_paiement(self):
        if not self.current_inscription_id:
            messagebox.showwarning("Incomplet", "Chargez d'abord un élève par son matricule.")
            return

        type_frais = self.combo_type_frais.get()
        montant_saisi_str = self.ent_montant.get().strip()
        mode = self.combo_mode.get()

        try:
            montant_saisi = int(montant_saisi_str)
        except ValueError:
            messagebox.showerror("Format", "Saisissez un montant valide.")
            return

        conn = None
        try:
            conn = obtenir_connexion()
            cursor = conn.cursor()

            if "Frais Mensuels" in type_frais:
                choix_mois_str = self.combo_mois.get()
                num_mois_vise = int(choix_mois_str.replace("Mois ", ""))
                label_frais_db = f"Mois {num_mois_vise}"

                # Blocage séquentiel impératif
                for m_prec in range(1, num_mois_vise):
                    deja_paye_prec = self.historique_mensuel.get(m_prec, 0)
                    if deja_paye_prec < self.current_mensualite:
                        messagebox.showerror(
                            "Paiement Bloqué",
                            f"Impossible de régler le Mois {num_mois_vise}.\n\n"
                            f"Le Mois {m_prec} précédent n'est pas encore intégralement soldé."
                        )
                        cursor.close()
                        conn.close()
                        return
            else:
                label_frais_db = "Frais de Soutenance"

            # Enregistrement
            query = "INSERT INTO Paiement (inscription_id, montant, datePaiement, modePaiement, type_frais) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (self.current_inscription_id, montant_saisi, date.today().strftime('%Y-%m-%d'), mode, label_frais_db))
            conn.commit()
            cursor.close()
            conn.close()

            # Lancement du PDF avec le design exact
            self.imprimer_recu_pdf(label_frais_db, montant_saisi, mode)
            messagebox.showinfo("Enregistré", "Le paiement a été validé avec succès !")
            self.rechercher_par_matricule()

        except Exception as e:
            messagebox.showerror("Erreur SQL", f"Erreur d'insertion : {e}")

    def imprimer_recu_pdf(self, type_frais, montant, mode):
        matricule = self.ent_matricule.get().strip()
        nom_complet = self.lbl_nom.cget("text")
        filiere_niveau = self.lbl_classe.cget("text")
        
        nom_fichier = f"Recu_{matricule}_{type_frais.replace(' ', '_')}.pdf"
        doc = SimpleDocTemplate(nom_fichier, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
        styles = getSampleStyleSheet()
        
        style_entete = ParagraphStyle('Entete', fontName='Helvetica-Bold', fontSize=12, textColor=colors.HexColor('#1E3A8A'), alignment=1)
        style_devise = ParagraphStyle('Devise', fontName='Helvetica-Oblique', fontSize=9, textColor=colors.HexColor('#475569'), alignment=1)
        style_titre = ParagraphStyle('TitreFiche', fontName='Helvetica-Bold', fontSize=14, textColor=colors.HexColor('#0F172A'), alignment=1, spaceAfter=5)
        style_meta = ParagraphStyle('Meta', fontName='Helvetica', fontSize=9, textColor=colors.HexColor('#475569'), alignment=1, spaceAfter=15)
        
        style_label = ParagraphStyle('LabelStyle', fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor('#475569'))
        style_valeur = ParagraphStyle('ValueStyle', fontName='Helvetica', fontSize=10, textColor=colors.HexColor('#1E293B'))
        
        story = []
        
        story.append(Paragraph("INSTITUT SUPÉRIEUR POLYTECHNIQUE SAINTE LUCIE D'OYO", style_entete))
        story.append(Paragraph("ISPSLO - Agrément Ministériel N° 0418/MESRST-CAB", style_devise))
        story.append(Paragraph('"Savoir - Rigueur - Excellence"', style_devise))
        story.append(Spacer(1, 15))
        
        # Badge "SOLDER"
        style_badge = ParagraphStyle('Badge', fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor('#059669'), alignment=1, spaceAfter=10)
        story.append(Paragraph("<b>[ SOLDER ]</b>", style_badge))
        
        story.append(Paragraph("REÇU DE SCOLARITÉ MENSUELLE", style_titre))
        story.append(Paragraph(f"Nº Reçu: REC-2026-MEN-1084 | Date: {date.today().strftime('%d/%m/%Y')}", style_meta))
        
        donnees = [
            [Paragraph("Matricule Étudiant :", style_label), Paragraph(f"<b>{matricule}</b>", style_valeur)],
            [Paragraph("Nom & Prénom(s) :", style_label), Paragraph(nom_complet, style_valeur)],
            [Paragraph("Filière & Niveau :", style_label), Paragraph(filiere_niveau, style_valeur)],
            [Paragraph("Libellé du Paiement :", style_label), Paragraph(type_frais, style_valeur)],
            [Paragraph("Mensualité Fixée :", style_label), Paragraph(f"{self.current_mensualite:,} FCFA / mois".replace(",", " "), style_valeur)],
            [Paragraph("Mode de Paiement :", style_label), Paragraph(mode, style_valeur)],
            [Paragraph("Montant de l'échéance :", style_label), Paragraph(f"{self.current_mensualite:,} FCFA".replace(",", " "), style_valeur)],
            [Paragraph("Montant Versé :", style_label), Paragraph(f"<b>{montant:,} FCFA</b>".replace(",", " "), style_valeur)],
            [Paragraph("Reste à payer sur ce mois :", style_label), Paragraph("<b>0 FCFA (Soldé)</b>", ParagraphStyle('Sold', fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor('#059669')))]
        ]
        
        tableau = Table(donnees, colWidths=[200, 300])
        tableau.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
            ('GRID', (0,0), (-1,-1), 1, colors.HexColor('#E2E8F0')),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 12),
        ]))
        story.append(tableau)
        story.append(Spacer(1, 20))
        
        sig_data = [
            [Paragraph("<b>L'Étudiant / Le Déposant</b><br/><br/><br/>" + nom_complet.split(" ")[-1] + ".", style_label),
             Paragraph("<b>Pour l'Administration (Caisse ISPSLO)</b><br/><br/><br/>Signature et Cachet", ParagraphStyle('SigR', parent=style_label, alignment=2))]
        ]
        sig_table = Table(sig_data, colWidths=[250, 250])
        story.append(sig_table)
        story.append(Spacer(1, 20))
        
        story.append(Paragraph("<i>Note: Conformément au règlement intérieur, aucun mois N ne peut être validé si le mois N-1 est impayé. Veuillez conserver précieusement ce reçu pour le contrôle de scolarité.</i>", ParagraphStyle('Note', fontName='Helvetica-Oblique', fontSize=8, textColor=colors.HexColor('#64748B'))))
        
        doc.build(story)
        self.ouvrir_pdf(nom_fichier)

    def ouvrir_pdf(self, nom_fichier):
        if sys.platform.startswith('darwin'): subprocess.call(('open', nom_fichier))
        elif os.name == 'nt': os.startfile(nom_fichier)
        elif os.name == 'posix': subprocess.call(('xdg-open', nom_fichier))

if __name__ == "__main__":
    app = GesProPaiementApp()
    app.mainloop()
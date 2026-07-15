import os
import sys
import subprocess
from datetime import date

# Importations ReportLab nécessaires
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generer_recu_inscription_test():
    nom_fichier = "Test_Recu_Inscription_ISPSLO.pdf"
    
    # Configuration du document (Marges de 40 points, environ 1.4 cm pour optimiser l'espace)
    doc = SimpleDocTemplate(
        nom_fichier, 
        pagesize=letter, 
        rightMargin=40, 
        leftMargin=40, 
        topMargin=40, 
        bottomMargin=40
    )
    
    # Définition des styles personnalisés basés sur le modèle visuel
    style_entete = ParagraphStyle('Entete', fontName='Helvetica-Bold', fontSize=12, textColor=colors.HexColor('#1E3A8A'), alignment=1)
    style_devise = ParagraphStyle('Devise', fontName='Helvetica-Oblique', fontSize=9, textColor=colors.HexColor('#475569'), alignment=1)
    style_titre = ParagraphStyle('TitreFiche', fontName='Helvetica-Bold', fontSize=14, textColor=colors.HexColor('#0F172A'), alignment=1, spaceAfter=5)
    style_meta = ParagraphStyle('Meta', fontName='Helvetica', fontSize=9, textColor=colors.HexColor('#475569'), alignment=1, spaceAfter=15)
    
    style_label = ParagraphStyle('LabelStyle', fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor('#475569'))
    style_valeur = ParagraphStyle('ValueStyle', fontName='Helvetica', fontSize=10, textColor=colors.HexColor('#1E293B'))
    
    story = []
    
    # 1. En-tête de l'établissement
    story.append(Paragraph("INSTITUT SUPÉRIEUR POLYTECHNIQUE SAINTE LUCIE D'OYO", style_entete))
    story.append(Paragraph("ISPSLO - Agrément Ministériel N° 0418/MESRST-CAB", style_devise))
    story.append(Paragraph('"Savoir - Rigueur - Excellence"', style_devise))
    story.append(Spacer(1, 15))
    
    # 2. Badge de Statut "ENREGISTRÉ" (Vert Cible/Émeraude discret)
    style_badge = ParagraphStyle('Badge', fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor('#065F46'), alignment=1, spaceAfter=10)
    story.append(Paragraph("<b>[ ENREGISTRÉ ]</b>", style_badge))
    
    # 3. Titre du Reçu
    story.append(Paragraph("REÇU D'INSCRIPTION ADMINISTRATIVE", style_titre))
    story.append(Paragraph("Nº Reçu: REC-2026-INS-0492 | Date: 15/10/2026", style_meta))
    
    # 4. Grille de données structurée
    donnees = [
        [Paragraph("Matricule Étudiant :", style_label), Paragraph("<b>2026-GCP-0042</b>", style_valeur)],
        [Paragraph("Nom & Prénom(s) :", style_label), Paragraph("MBOUNGOU Pierre-Marie", style_valeur)],
        [Paragraph("Filière / Spécialité :", style_label), Paragraph("Génie Civil & Projets (GCP)", style_valeur)],
        [Paragraph("Niveau d'Études :", style_label), Paragraph("Licence 1 (L1)", style_valeur)],
        [Paragraph("Année Académique :", style_label), Paragraph("2026-2027", style_valeur)],
        [Paragraph("Type d'Opération :", style_label), Paragraph("Nouvelle Inscription", style_valeur)],
        [Paragraph("Mode de Paiement :", style_label), Paragraph("Chèque (BGFIBank N° 849204)", style_valeur)],
        [Paragraph("Montant des Droits d'Inscription :", style_label), Paragraph("50 000 FCFA", style_valeur)],
        [Paragraph("TOTAL PERÇU :", style_label), Paragraph("<b>50 000 FCFA</b>", ParagraphStyle('Tot', fontName='Helvetica-Bold', fontSize=11, textColor=colors.HexColor('#1E3A8A')))]
    ]
    
    # Largeur des colonnes ajustée : 200px pour la gauche, 300px pour la droite (Total 500px, parfait pour le format Letter)
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
    
    # 5. Signatures (Côte à côte avec structure de Table invisible)
    sig_data = [
        [Paragraph("<b>L'Étudiant / Le Déposant</b><br/><br/><br/>Pierre-Marie M.", style_label),
         Paragraph("<b>Pour l'Administration (Caisse ISPSLO)</b><br/><br/><br/>Signature et Cachet", ParagraphStyle('SigR', parent=style_label, alignment=2))]
    ]
    sig_table = Table(sig_data, colWidths=[250, 250])
    story.append(sig_table)
    story.append(Spacer(1, 20))
    
    # 6. Note réglementaire de bas de page
    story.append(Paragraph("<i>Note: Les droits d'inscription et de réinscription sont réglementairement non remboursables. Ce reçu est exigé pour valider définitivement la carte d'étudiant.</i>", ParagraphStyle('Note', fontName='Helvetica-Oblique', fontSize=8, textColor=colors.HexColor('#64748B'))))
    
    doc.build(story)
    print(f"-> Reçu d'inscription généré avec succès : {nom_fichier}")
    ouvrir_fichier(nom_fichier)


def generer_recu_scolarite_test():
    nom_fichier = "Test_Recu_Scolarite_ISPSLO.pdf"
    
    doc = SimpleDocTemplate(
        nom_fichier, 
        pagesize=letter, 
        rightMargin=40, 
        leftMargin=40, 
        topMargin=40, 
        bottomMargin=40
    )
    
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
    
    # Badge "SOLDER" en Vert Caisse
    style_badge = ParagraphStyle('Badge', fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor('#059669'), alignment=1, spaceAfter=10)
    story.append(Paragraph("<b>[ SOLDER ]</b>", style_badge))
    
    story.append(Paragraph("REÇU DE SCOLARITÉ MENSUELLE", style_titre))
    story.append(Paragraph("Nº Reçu: REC-2026-MEN-1084 | Date: 15/11/2026", style_meta))
    
    donnees = [
        [Paragraph("Matricule Étudiant :", style_label), Paragraph("<b>2026-GCP-0042</b>", style_valeur)],
        [Paragraph("Nom & Prénom(s) :", style_label), Paragraph("MBOUNGOU Pierre-Marie", style_valeur)],
        [Paragraph("Filière & Niveau :", style_label), Paragraph("Génie Civil & Projets (GCP) Licence 1 (L1)", style_valeur)],
        [Paragraph("Libellé du Paiement :", style_label), Paragraph("Mois 3 (Mensualité)", style_valeur)],
        [Paragraph("Mensualité Fixée :", style_label), Paragraph("32 000 FCFA / mois (Niveau L1)", style_valeur)],
        [Paragraph("Mode de Paiement :", style_label), Paragraph("Mobile Money (Airtel Money)", style_valeur)],
        [Paragraph("Montant de l'échéance :", style_label), Paragraph("32 000 FCFA", style_valeur)],
        [Paragraph("Montant Versé :", style_label), Paragraph("<b>32 000 FCFA</b>", style_valeur)],
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
        [Paragraph("<b>L'Étudiant / Le Déposant</b><br/><br/><br/>Pierre-Marie M.", style_label),
         Paragraph("<b>Pour l'Administration (Caisse ISPSLO)</b><br/><br/><br/>Signature et Cachet", ParagraphStyle('SigR', parent=style_label, alignment=2))]
    ]
    sig_table = Table(sig_data, colWidths=[250, 250])
    story.append(sig_table)
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("<i>Note: Conformément au règlement intérieur, aucun mois N ne peut être validé si le mois N-1 est impayé. Veuillez conserver précieusement ce reçu pour le contrôle de scolarité.</i>", ParagraphStyle('Note', fontName='Helvetica-Oblique', fontSize=8, textColor=colors.HexColor('#64748B'))))
    
    doc.build(story)
    print(f"-> Reçu de scolarité généré avec succès : {nom_fichier}")
    ouvrir_fichier(nom_fichier)


def ouvrir_fichier(nom_fichier):
    """Ouvre automatiquement le PDF généré selon le système d'exploitation."""
    try:
        if sys.platform.startswith('darwin'):
            subprocess.call(('open', nom_fichier))
        elif os.name == 'nt':
            os.startfile(nom_fichier)
        elif os.name == 'posix':
            subprocess.call(('xdg-open', nom_fichier))
    except Exception as e:
        print(f"Impossible d'ouvrir automatiquement le fichier {nom_fichier} : {e}")


if __name__ == "__main__":
    print("=== DÉBUT DU TEST DES MAQUETTES DE REÇU ISPSLO ===\n")
    generer_recu_inscription_test()
    print("-" * 50)
    generer_recu_scolarite_test()
    print("\n=== TESTS TERMINÉS AVEC SUCCÈS ===")p
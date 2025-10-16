# Fichier: v2_scripts/extract_pages.py
# Objectif: Extraire les pages de plusieurs PDF en images pour l'annotation.

import os
import fitz  # PyMuPDF

# --- CONFIGURATION ---
# Liste des fichiers PDF à traiter (doivent être à la racine du projet)
PDF_FILES = [
    "bookChess1.pdf",
    "bookChess2.pdf",
    "bookChess3.pdf",
    "bookChess4.pdf"
]

# Dossier où les images des pages seront sauvegardées
OUTPUT_DIR = "v2_data/pages"

# Limite du nombre de pages à extraire par livre
MAX_PAGES_PER_BOOK = 100

# Qualité de l'image (DPI: Dots Per Inch). 200 est un bon compromis qualité/taille.
IMAGE_DPI = 200

# --- SCRIPT ---

def main():
    print("--- Démarrage de l'extraction des pages en images ---")
    
    # S'assurer que le dossier de sortie existe
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    total_pages_extracted = 0

    # Boucle sur chaque livre
    for pdf_path in PDF_FILES:
        if not os.path.exists(pdf_path):
            print(f"AVERTISSEMENT : Le fichier '{pdf_path}' est introuvable. Il sera ignoré.")
            continue
            
        book_name = os.path.splitext(os.path.basename(pdf_path))[0]
        print(f"\n📖 Traitement du livre : {book_name}")

        try:
            doc = fitz.open(pdf_path)
            
            # Déterminer le nombre de pages à extraire
            num_pages_to_extract = min(len(doc), MAX_PAGES_PER_BOOK)
            print(f"   -> {len(doc)} pages au total. Extraction des {num_pages_to_extract} premières pages.")

            # Boucle sur les pages à extraire
            for page_num in range(num_pages_to_extract):
                page = doc.load_page(page_num)
                pix = page.get_pixmap(dpi=IMAGE_DPI)
                
                # Nom de fichier unique : bookChess1_page_001.jpg
                output_filename = f"{book_name}_page_{page_num + 1:03d}.jpg"
                output_path = os.path.join(OUTPUT_DIR, output_filename)
                
                pix.save(output_path)
                total_pages_extracted += 1

            doc.close()

        except Exception as e:
            print(f"   -> ERREUR lors du traitement du fichier '{pdf_path}': {e}")

    print("\n--- ✅ Extraction terminée ! ---")
    print(f"{total_pages_extracted} pages ont été sauvegardées dans le dossier '{OUTPUT_DIR}'.")
    print("Vous êtes prêt pour la phase d'annotation.")

if __name__ == "__main__":
    main()
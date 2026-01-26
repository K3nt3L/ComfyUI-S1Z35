import os
import csv

# --- MOTEUR CENTRAL (Classe de base) ---
class S1Z35_Base:
    """
    Moteur principal pour ComfyUI-S1Z35.
    Lit un fichier CSV spécifique défini par la classe enfant.
    """
    CSV_FILE = "default.csv" 

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        # Localisation dynamique du dossier presets
        base_path = os.path.dirname(os.path.realpath(__file__))
        csv_path = os.path.join(base_path, "presets", cls.CSV_FILE)
        
        choices = []
        
        # Lecture sécurisée du CSV
        if os.path.exists(csv_path):
            try:
                with open(csv_path, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        # On attend: width, height, label
                        if len(row) >= 3:
                            try:
                                w = int(row[0].strip())
                                h = int(row[1].strip())
                                label = row[2].strip()
                                # Format affiché: "Label (WxH)"
                                choices.append(f"{label} ({w}x{h})")
                            except ValueError:
                                continue # Ignorer les lignes mal formées
            except Exception as e:
                print(f"[S1Z35] Erreur de lecture sur {cls.CSV_FILE}: {e}")
        
        # Fallback si le fichier est vide ou introuvable
        if not choices:
            choices = [f"Missing {cls.CSV_FILE} (512x512)"]

        return {
            "required": {
                "preset": (choices,),
                "swap_dimensions": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("INT", "INT",)
    RETURN_NAMES = ("width", "height",)
    FUNCTION = "get_size"
    CATEGORY = "S1Z35/Resolution"

    def get_size(self, preset, swap_dimensions):
        # On extrait la taille depuis la chaîne de caractères "Nom (1024x1024)"
        try:
            # Prend la partie après la dernière parenthèse ouvrante
            dimensions_part = preset.rsplit('(', 1)[1].rstrip(')')
            w_str, h_str = dimensions_part.split('x')
            width = int(w_str)
            height = int(h_str)
        except:
            # Sécurité absolue
            width, height = 512, 512

        if swap_dimensions:
            return (height, width)
        return (width, height)

# --- DÉCLARATION DES NOEUDS ENFANTS ---

class S1Z35_SDXL(S1Z35_Base):
    CSV_FILE = "sdxl.csv"

class S1Z35_Flux1(S1Z35_Base):
    CSV_FILE = "flux1.csv"

class S1Z35_Flux2(S1Z35_Base):
    CSV_FILE = "flux2.csv"

class S1Z35_ZIT(S1Z35_Base):
    CSV_FILE = "zit.csv"

class S1Z35_Qwen(S1Z35_Base):
    CSV_FILE = "qwen.csv"

class S1Z35_Hunyuan(S1Z35_Base):
    CSV_FILE = "hunyuan.csv"

class S1Z35_Custom1(S1Z35_Base):
    CSV_FILE = "custom1.csv"

class S1Z35_Custom2(S1Z35_Base):
    CSV_FILE = "custom2.csv"


# --- MAPPINGS COMFYUI ---
NODE_CLASS_MAPPINGS = {
    "S1Z35_SDXL": S1Z35_SDXL,
    "S1Z35_Flux1": S1Z35_Flux1,
    "S1Z35_Flux2": S1Z35_Flux2,
    "S1Z35_ZIT": S1Z35_ZIT,
    "S1Z35_Qwen": S1Z35_Qwen,
    "S1Z35_Hunyuan": S1Z35_Hunyuan,
    "S1Z35_Custom1": S1Z35_Custom1,
    "S1Z35_Custom2": S1Z35_Custom2
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "S1Z35_SDXL": "S1Z35 - SDXL",
    "S1Z35_Flux1": "S1Z35 - Flux 1",
    "S1Z35_Flux2": "S1Z35 - Flux 2",
    "S1Z35_ZIT": "S1Z35 - Z Image Turbo",
    "S1Z35_Qwen": "S1Z35 - Qwen",
    "S1Z35_Hunyuan": "S1Z35 - Hunyuan",
    "S1Z35_Custom1": "S1Z35 - Custom 1",
    "S1Z35_Custom2": "S1Z35 - Custom 2"
}
class LivreIndisponibleError(Exception):
   
    def __init__(self, ISBN: str = "", message: str = None):
        self.ISBN = ISBN
        if message is None:
            message = f"Le livre (ISBN: {ISBN}) n'est pas disponible."
        super().__init__(message)

class QuotaEmpruntDepasseError(Exception):
  
    def __init__(self, id_membre: str = "", max_emprunts: int = 5, message: str = None):
        self.id_membre = id_membre
        if message is None:
            message = f"Le membre {id_membre} a dépassé son quota ({max_emprunts} livres max)."
        super().__init__(message)

class MembreInexistantError(Exception):
   
    def __init__(self, id_membre: str = "", message: str = None):
        self.id_membre = id_membre
        if message is None:
            message = f"Membre inconnu (ID: {id_membre})."
        super().__init__(message)

class LivreInexistantError(Exception):
   
    def __init__(self, isbn: str = "", message: str = None):
        self.isbn = isbn
        if message is None:
            message = f"Livre introuvable (ISBN: {isbn})."
        super().__init__(message)
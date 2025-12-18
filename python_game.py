import pygame
import random
import sys

# Initialisation de Pygame
pygame.init()

# Constantes
LARGEUR = 800
HAUTEUR = 600
FPS = 60

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
GRIS = (169, 169, 169)
ROUGE = (220, 20, 60)
VERT = (50, 205, 50)
ORANGE = (255, 140, 0)

# Création de la fenêtre
ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Jeu de Ballon - Évite les obstacles!")
horloge = pygame.time.Clock()

# Police
police = pygame.font.Font(None, 36)
grande_police = pygame.font.Font(None, 72)

class Ballon:
    def __init__(self):
        self.rayon = 25
        self.x = 100
        self.y = HAUTEUR // 2
        self.vitesse_y = 0
        self.gravite = 0.5
        self.force_saut = -15
        self.couleur = ROUGE
        
    def sauter(self):
        self.vitesse_y = self.force_saut
    
    def update(self):
        # Appliquer la gravité
        self.vitesse_y += self.gravite
        self.y += self.vitesse_y
        
        # Limiter le ballon à l'écran
        if self.y - self.rayon < 0:
            self.y = self.rayon
            self.vitesse_y = 0
        if self.y + self.rayon > HAUTEUR:
            self.y = HAUTEUR - self.rayon
            self.vitesse_y = 0
    
    def dessiner(self, surface):
        pygame.draw.circle(surface, self.couleur, (int(self.x), int(self.y)), self.rayon)
        # Effet de brillance
        pygame.draw.circle(surface, BLANC, (int(self.x - 8), int(self.y - 8)), 8)

class Obstacle:
    def __init__(self):
        self.largeur = 50
        self.hauteur = random.randint(100, 400)
        self.x = LARGEUR
        self.y = random.choice([0, HAUTEUR - self.hauteur])
        self.vitesse = 5
        self.couleur = NOIR
        
    def update(self):
        self.x -= self.vitesse
    
    def dessiner(self, surface):
        pygame.draw.rect(surface, self.couleur, (self.x, self.y, self.largeur, self.hauteur))
        # Bordure
        pygame.draw.rect(surface, BLANC, (self.x, self.y, self.largeur, self.hauteur), 3)
    
    def est_hors_ecran(self):
        return self.x + self.largeur < 0
    
    def collision(self, ballon):
        # Vérifier si le ballon touche l'obstacle
        if (self.x < ballon.x + ballon.rayon and 
            self.x + self.largeur > ballon.x - ballon.rayon):
            if (self.y < ballon.y + ballon.rayon and 
                self.y + self.hauteur > ballon.y - ballon.rayon):
                return True
        return False

def dessiner_texte(surface, texte, x, y, police_obj, couleur=NOIR):
    surface_texte = police_obj.render(texte, True, couleur)
    rect = surface_texte.get_rect(center=(x, y))
    surface.blit(surface_texte, rect)

def ecran_accueil():
    while True:
        ecran.fill(GRIS)
        
        dessiner_texte(ecran, "JEU DE BALLON", LARGEUR // 2, HAUTEUR // 3, grande_police, ROUGE)
        dessiner_texte(ecran, "Appuyez sur ESPACE pour sauter", LARGEUR // 2, HAUTEUR // 2, police, BLANC)
        dessiner_texte(ecran, "Évitez les obstacles noirs!", LARGEUR // 2, HAUTEUR // 2 + 50, police, BLANC)
        dessiner_texte(ecran, "Appuyez sur ESPACE pour commencer", LARGEUR // 2, HAUTEUR - 100, police, ORANGE)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return

def ecran_game_over(score):
    while True:
        ecran.fill(GRIS)
        
        dessiner_texte(ecran, "GAME OVER", LARGEUR // 2, HAUTEUR // 3, grande_police, ROUGE)
        dessiner_texte(ecran, f"Score: {score}", LARGEUR // 2, HAUTEUR // 2, police, BLANC)
        dessiner_texte(ecran, "Appuyez sur ESPACE pour rejouer", LARGEUR // 2, HAUTEUR - 100, police, BLANC)
        dessiner_texte(ecran, "ou ÉCHAP pour quitter", LARGEUR // 2, HAUTEUR - 60, police, BLANC)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def jeu_principal():
    ballon = Ballon()
    obstacles = []
    score = 0
    compteur_obstacle = 0
    
    en_cours = True
    
    while en_cours:
        horloge.tick(FPS)
        
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    ballon.sauter()
        
        # Mise à jour du ballon
        ballon.update()
        
        # Créer des obstacles
        compteur_obstacle += 1
        if compteur_obstacle > 90:  # Nouvel obstacle toutes les 1.5 secondes
            obstacles.append(Obstacle())
            compteur_obstacle = 0
        
        # Mise à jour des obstacles
        for obstacle in obstacles[:]:
            obstacle.update()
            
            # Vérifier collision
            if obstacle.collision(ballon):
                en_cours = False
            
            # Retirer les obstacles hors écran et augmenter le score
            if obstacle.est_hors_ecran():
                obstacles.remove(obstacle)
                score += 1
        
        # Dessiner
        ecran.fill(GRIS)
        
        # Dessiner le sol et le plafond (lignes décoratives)
        pygame.draw.line(ecran, BLANC, (0, 0), (LARGEUR, 0), 5)
        pygame.draw.line(ecran, BLANC, (0, HAUTEUR - 5), (LARGEUR, HAUTEUR - 5), 5)
        
        ballon.dessiner(ecran)
        
        for obstacle in obstacles:
            obstacle.dessiner(ecran)
        
        # Afficher le score
        dessiner_texte(ecran, f"Score: {score}", 70, 30, police, BLANC)
        
        pygame.display.flip()
    
    return score

# Boucle principale
def main():
    ecran_accueil()
    
    while True:
        score = jeu_principal()
        rejouer = ecran_game_over(score)
        if not rejouer:
            break

if __name__ == "__main__":
    main()

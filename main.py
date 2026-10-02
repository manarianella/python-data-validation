import csv
from pydantic import BaseModel, Field, ValidationError


class PopulationData(BaseModel):

    code_region: str = Field(
        alias="Code Officiel Région",
        pattern=r"^\d{2,3}$"
    )

    nom_region: str = Field(
        alias="Nom Officiel Région",
        pattern=r"^[A-Za-zÀ-ÖØ-öø-ÿŒœÎîÔô'’ -]+$"
    )

    code_departement: str = Field(
        alias="Code Officiel Département",
        pattern=r"^(?:\d{2}|2A|2B|\d{3})$"
    )

    code_arrondissement: str = Field(
        alias="Code Officiel Arrondissement Départemental",
        pattern=r"^\d{1,3}$"
    )

    code_commune: str = Field(
        alias="Code Officiel Commune / Arrondissement Municipal",
        pattern=r"^(?:\d{5,6}|2[AB]\d{3})$"
    )

    nom_commune: str = Field(
        alias="Nom Officiel Commune / Arrondissement Municipal",
        pattern=(
            r"^(?:"
            r"[A-Za-zÀ-ÖØ-öø-ÿŒœ'’ ()-]+"
            r"|"
            r"(?:Paris|Lyon|Marseille) "
            r"(?:1er|\d{1,2}e) Arrondissement"
            r")$"
        )
    )

    population_municipale: str = Field(
        alias="Population municipale",
        pattern=r"^\d+\.0$"
    )

    population_comptee_a_part: str = Field(
        alias="Population comptée à part",
        pattern=r"^\d+\.0$"
    )

    population_totale: str = Field(
        alias="Population totale",
        pattern=r"^\d+\.0$"
    )

    annee_recensement: str = Field(
        alias="Année de recensement",
        pattern=r"^\d{4}$"
    )

    annee_entree_vigueur: str = Field(
        alias="Année d’entrée en vigueur",
        pattern=r"^\d{4}$"
    )

    annee_reference_geographique: str = Field(
        alias="Année de référence géographique",
        pattern=r"^\d{4}$"
    )

    nom_epci: str = Field(
        alias="Nom Officiel EPCI",
        pattern=r"^[^*]*$"
    )

    code_epci: str = Field(
        alias="Code Officiel EPCI",
        pattern=r"^(?:\d{9})?$"
    )

    nom_departement: str = Field(
        alias="Nom Officiel Département",
        pattern=r"^[A-Za-zÀ-ÖØ-öø-ÿŒœ'’ -]*$"
    )


print("\n--- VALIDATION DU CSV ---")

erreurs = []

with open(
    "population-corrupted(1).csv",
    "r",
    encoding="utf-8"
) as fichier:

    lecteur = csv.DictReader(fichier, delimiter=";")

    for numero_ligne, ligne in enumerate(lecteur, start=2):

        try:
            PopulationData(**ligne)

        except ValidationError as erreur:

            for detail in erreur.errors():

                colonne = detail["loc"][0]
                valeur = detail.get("input")

                erreurs.append(
                    (numero_ligne, colonne, valeur)
                )


for numero_ligne, colonne, valeur in erreurs:

    print(
        f"Ligne {numero_ligne} | "
        f"Colonne : {colonne} | "
        f"Valeur : {valeur!r}"
    )


print("\nNombre d'erreurs détectées :", len(erreurs))
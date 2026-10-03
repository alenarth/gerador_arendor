# namegen/database.py
"""
Bancos de nomes prontos (CSV) em namegen/data/:
  - nomes_pessoais.csv  → colunas: nome, lingua, raca, genero
  - nomes_lugares.csv   → colunas: nome, lingua, raca, tipo

A coluna "lingua" aceita a chave interna, o nome exibido ou um apelido
da língua (veja LANGUAGE_ALIASES em syllable_data.py).
"""
import csv
import os
import random
from typing import Dict, List, Optional
from .syllable_data import resolve_language

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
PERSONAL_FILE = "nomes_pessoais.csv"
PLACE_FILE = "nomes_lugares.csv"

GENDERS: Dict[str, str] = {
    "masculino": "male",
    "feminino": "female",
}

PLACE_TYPES: Dict[str, str] = {
    "cidade": "city",
    "vila": "town",
    "aldeia": "village",
    "fortaleza": "fortress",
    "floresta": "forest",
    "montanha": "mountain",
    "rio": "river",
    "regiao": "region",
    "região": "region",
    "colina": "hill",
    "vale": "valley",
    "mina": "mine",
    "abismo": "abyss",
    "trono": "throne",
}


def normalize_gender(gender: Optional[str]) -> Optional[str]:
    if gender is None:
        return None
    gender = gender.strip().lower()
    return GENDERS.get(gender, gender)


def normalize_place_type(place_type: Optional[str]) -> Optional[str]:
    if place_type is None:
        return None
    place_type = place_type.strip().lower()
    return PLACE_TYPES.get(place_type, place_type)


class NameDatabase:
    """Carrega os bancos .csv e sorteia nomes por língua, gênero e tipo de lugar."""

    def __init__(self, data_dir: str = DATA_DIR, seed: Optional[int] = None):
        self.rng = random.Random(seed)
        # língua → gênero → nomes
        self.personal: Dict[str, Dict[str, List[str]]] = {}
        # língua → tipo de lugar → nomes
        self.places: Dict[str, Dict[str, List[str]]] = {}

        self._load(os.path.join(data_dir, PERSONAL_FILE), "genero", normalize_gender, self.personal)
        self._load(os.path.join(data_dir, PLACE_FILE), "tipo", normalize_place_type, self.places)

    @staticmethod
    def _load(path: str, category_column: str, normalize, target: Dict[str, Dict[str, List[str]]]):
        if not os.path.exists(path):
            return
        with open(path, encoding="utf-8-sig", newline="") as f:
            for line_no, row in enumerate(csv.DictReader(f), start=2):
                name = (row.get("nome") or "").strip()
                if not name:
                    continue
                language = resolve_language(row.get("lingua") or "")
                if not language:
                    raise ValueError(
                        f"{os.path.basename(path)}, linha {line_no}: "
                        f"língua desconhecida '{row.get('lingua')}'"
                    )
                category = normalize(row.get(category_column) or "") or "other"
                names = target.setdefault(language, {}).setdefault(category, [])
                if name not in names:  # ignora linhas repetidas
                    names.append(name)

    # ----------------------------------------------------------
    # CONSULTA
    # ----------------------------------------------------------

    def personal_names(self, language: str, gender: Optional[str] = None) -> List[str]:
        """Nomes pessoais da língua (opcionalmente só de um gênero)."""
        return self._select(self.personal, language, normalize_gender(gender))

    def place_names(self, language: str, place_type: Optional[str] = None) -> List[str]:
        """Nomes de lugares da língua (opcionalmente só de um tipo)."""
        return self._select(self.places, language, normalize_place_type(place_type))

    @staticmethod
    def _select(table: Dict[str, Dict[str, List[str]]], language: str, category: Optional[str]) -> List[str]:
        by_category = table.get(language, {})
        if category is not None:
            return list(by_category.get(category, []))
        names: List[str] = []
        for group in by_category.values():
            names.extend(n for n in group if n not in names)
        return names

    def random_personal(self, language: str, gender: Optional[str] = None) -> Optional[str]:
        names = self.personal_names(language, gender) or self.personal_names(language)
        return self.rng.choice(names) if names else None

    def random_place(self, language: str, place_type: Optional[str] = None) -> Optional[str]:
        names = self.place_names(language, place_type) or self.place_names(language)
        return self.rng.choice(names) if names else None

    def languages(self) -> List[str]:
        return sorted(set(self.personal) | set(self.places))

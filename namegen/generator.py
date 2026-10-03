# namegen/generator.py
import random
import re
from typing import Callable, Optional, List, Dict, Set, Tuple
from .database import NameDatabase, normalize_gender, normalize_place_type
from .syllable_data import (
    LANGUAGES, ONSET_SYLLABLES, CODA_SYLLABLES,
    NAME_LENGTH_PATTERNS, language_for_race,
)

_VOWELS = "aeiouyAEIOUY"
_CONSONANTS = "bcdfghjklmnpqrstvwxzBCDFGHJKLMNPQRSTVWXZ"


class NameGenerator:
    """
    Gerador de nomes baseado em sílabas.
    Combina onset + núcleo + coda para formar nomes foneticamente coerentes.
    """

    def __init__(self, seed: Optional[int] = None):
        self.rng = random.Random(seed)

    # ----------------------------------------------------------
    # GERAÇÃO POR SÍLABAS
    # ----------------------------------------------------------

    def generate_syllable_name(
        self,
        language: str,
        length: str = "medium",
        max_attempts: int = 20,
    ) -> str:
        """
        Gera um nome combinando sílabas da língua especificada.
        """
        if language not in LANGUAGES:
            raise ValueError(f"Língua desconhecida: {language}")

        lang_data = LANGUAGES[language]
        onsets = ONSET_SYLLABLES.get(language, [""])
        codas = CODA_SYLLABLES.get(language, [""])
        min_syl, max_syl = NAME_LENGTH_PATTERNS.get(length, (2, 3))

        for _ in range(max_attempts):
            num_syllables = self.rng.randint(min_syl, max_syl)
            name = ""

            for i in range(num_syllables):
                # Primeira sílaba: onset + vogal; seguintes: consoante + vogal
                head = self.rng.choice(onsets if i == 0 else lang_data["consonants"])
                vowel = self.rng.choice(lang_data["vowels"])
                name = self._join(name, self._join(head, vowel, language), language)

            # Coda: às vezes fecha a última sílaba com consoante
            if self.rng.random() < 0.5:
                name = self._join(name, self.rng.choice(codas), language)

            # Adiciona sufixo se o nome for curto demais
            if len(name) < 4:
                suffix = self.rng.choice(lang_data["suffixes"].get("personal", [""]))
                name = self._join(name, suffix, language)

            # Capitaliza
            name = name.capitalize()

            # Valida
            if self._is_valid_name(name):
                return name

        # Fallback: combinação aleatória
        return self._fallback_name(language)

    def _join(self, left: str, right: str, language: str) -> str:
        """
        Junta dois pedaços de nome evitando letras duplicadas na emenda
        (Gr + ra → Gra) e encontros de 3+ consoantes (Gr + bash → Grabash).
        """
        if not left or not right:
            return left + right
        if left[-1].lower() == right[0].lower():
            right = right[1:]
            if not right:
                return left
        trailing = len(left) - len(left.rstrip(_CONSONANTS))
        leading = len(right) - len(right.lstrip(_CONSONANTS))
        if trailing + leading >= 3:
            vowels = [v for v in LANGUAGES[language]["vowels"] if v[0] in _VOWELS]
            left += self.rng.choice(vowels or ["a"])
        return left + right

    def _is_valid_name(self, name: str) -> bool:
        """Valida se o nome tem aparência razoável."""
        if len(name) < 3 or len(name) > 15:
            return False
        if re.search(r"(.)\1{2,}", name):  # 3+ letras iguais seguidas
            return False
        if re.search(r"(.{3,})\1", name.lower()):  # trecho repetido (Urarrarnar)
            return False
        return True

    def _fallback_name(self, language: str) -> str:
        """Gera um nome de fallback usando sufixos."""
        lang_data = LANGUAGES[language]
        suffixes = lang_data["suffixes"].get("personal", ["on"])
        base = self.rng.choice(ONSET_SYLLABLES.get(language, ["al"]))
        suffix = self.rng.choice(suffixes)
        return self._join(base, suffix, language).capitalize()

    # ----------------------------------------------------------
    # GERAÇÃO COMPLETA (PESSOAL + FAMÍLIA)
    # ----------------------------------------------------------

    def generate_full_name(
        self,
        race: str,
        length: str = "medium",
        include_family: bool = True,
    ) -> Dict[str, str]:
        """
        Gera um nome completo: pessoal + família.
        """
        language = language_for_race(race)
        if not language:
            raise ValueError(f"Raça desconhecida: {race}")

        # Nome pessoal
        first_name = self.generate_syllable_name(language, length)

        # Sobrenome
        family_name = ""
        if include_family:
            lang_data = LANGUAGES[language]
            family_suffixes = lang_data["suffixes"].get("family", [""])
            family_base = self.rng.choice(ONSET_SYLLABLES.get(language, ["al"]))
            family_suffix = self.rng.choice(family_suffixes)
            family_name = self._join(family_base, family_suffix, language).capitalize()

        return {
            "first_name": first_name,
            "family_name": family_name,
            "full_name": " ".join(p for p in (first_name, family_name) if p),
            "race": race,
            "language": language,
        }

    # ----------------------------------------------------------
    # GERAÇÃO DE LUGARES
    # ----------------------------------------------------------

    def generate_place_name(
        self,
        race: str,
        place_type: str = "city",
        length: str = "medium",
    ) -> str:
        """
        Gera nomes de lugares.
        place_type: city, town, village, fortress, forest, mountain, river,
        region, hill, valley, mine, abyss, throne
        (também aceita os tipos em português: cidade, vila, fortaleza...)
        """
        language = language_for_race(race)
        if not language:
            raise ValueError(f"Raça desconhecida: {race}")

        lang_data = LANGUAGES[language]
        place_suffixes = lang_data["suffixes"].get("place", ["ton"])

        # Prefixo geográfico
        geo_prefixes = {
            "city": ["Dol-", "Khar-", "Ael-", "Veth-", "Fer-"],
            "town": ["Bram-", "Fiz-", "Per-", "Tum-", "Mar-"],
            "fortress": ["Dun-", "Khar-", "Dorn-", "Veth-", "Krag-"],
            "forest": ["Ael-", "Syl-", "Fer-", "Aos-", "Wed-"],
            "mountain": ["Dorn-", "Khar-", "Veth-", "Gor-", "Thor-"],
            "river": ["Ez-", "Gav-", "Vael-", "Ael-", "Fer-"],
            "region": ["-dor", "-val", "-heim", "-gal", "-wed"],
            "village": ["Bram-", "Tum-", "Per-", "Wil-", "Ned-"],
            "hill": ["-hill", "-tor", "-mont", "-barrow"],
            "valley": ["-dale", "-vale", "-glen", "-dell"],
            "mine": ["Khaz-", "Dun-", "Grim-", "Bork-", "Thrain-"],
            "abyss": ["Ab-", "Vor-", "Xar-", "Mal-", "Draz-"],
            "throne": ["Thron-", "Vex-", "Mal-", "Xar-", "Zar-"],
        }

        prefix_list = geo_prefixes.get(normalize_place_type(place_type), geo_prefixes["city"])
        prefix = self.rng.choice(prefix_list)

        # Base do nome
        base = self.generate_syllable_name(language, length)
        suffix = self.rng.choice(place_suffixes)

        # Combina
        if prefix.startswith("-"):
            # Sufixo geográfico: Base + dor → Basedor
            name = self._join(base, prefix[1:], language)
        else:
            # Mesmo estilo do banco de nomes: Dol-Makjar
            name = prefix + base

        # Adiciona sufixo se necessário
        if not name.endswith(tuple(place_suffixes)) and len(name) < 8:
            name = self._join(name, suffix, language)

        return name

    # ----------------------------------------------------------
    # GERAÇÃO EM LOTE
    # ----------------------------------------------------------

    def generate_batch(
        self,
        race: str,
        count: int = 10,
        name_type: str = "full",
        length: str = "medium",
    ) -> List[Dict]:
        """
        Gera múltiplos nomes de uma vez.
        name_type: 'personal', 'full', 'place'
        """
        if name_type not in ("personal", "full", "place"):
            raise ValueError(f"Tipo de nome desconhecido: {name_type}")
        language = language_for_race(race)
        if not language:
            raise ValueError(f"Raça desconhecida: {race}")

        results = []
        for _ in range(count):
            if name_type == "personal":
                name = self.generate_syllable_name(language, length)
                results.append({"name": name, "race": race})
            elif name_type == "full":
                results.append(self.generate_full_name(race, length))
            elif name_type == "place":
                results.append({"name": self.generate_place_name(race, length=length), "race": race})
        return results


# ============================================================
# CLASSE AVANÇADA: GERADOR COM MARKOV
# ============================================================

class MarkovNameGenerator:
    """
    Gerador de nomes usando cadeias de Markov de ordem variável.
    Treinado com nomes existentes para gerar novos.
    """

    START = "^"
    END = "$"

    def __init__(self, order: int = 2, seed: Optional[int] = None):
        self.order = order
        self.rng = random.Random(seed)
        self.chains: Dict[str, List[str]] = {}
        self.training_names: Set[str] = set()
        # Nomes já devolvidos: evita repetir o mesmo nome na mesma sessão
        self.generated_names: Set[str] = set()
        # Como o treino escreve as partes após hífen: Khazad-dun x Dol-Makjar
        self.lowercase_parts: Set[str] = set()
        self.capitalized_parts: Set[str] = set()
        # Máximo de hífens/apóstrofos vistos no treino (evita Dol-Rug-Zidragul)
        self.max_separators = {"-": 0, "'": 0}

    def train(self, names: List[str]):
        """Treina o modelo com uma lista de nomes."""
        for name in names:
            name = name.strip()
            if not name:
                continue
            for part in name.split("-")[1:]:
                (self.lowercase_parts if part.islower() else self.capitalized_parts).add(part.lower())
            for sep in self.max_separators:
                self.max_separators[sep] = max(self.max_separators[sep], name.count(sep))
            name = name.lower()
            self.training_names.add(name)
            # Marcadores de início/fim: o modelo aprende como nomes começam e terminam
            padded = self.START * self.order + name + self.END
            for i in range(len(padded) - self.order):
                prefix = padded[i:i + self.order]
                self.chains.setdefault(prefix, []).append(padded[i + self.order])

    def generate(
        self,
        max_length: int = 12,
        min_length: int = 4,
        max_attempts: int = 100,
        accept: Optional[Callable[[str], bool]] = None,
    ) -> str:
        """
        Gera um nome usando o modelo treinado. Prefere nomes inéditos (fora do
        treino e ainda não devolvidos) e, se `accept` for dado, que passem nele.
        """
        if not self.chains:
            return "Aelith"

        fallback, fallback_is_new = None, False
        for _ in range(max_attempts):
            prefix = self.START * self.order
            result = ""
            while len(result) <= max_length:
                next_char = self.rng.choice(self.chains[prefix])
                if next_char == self.END:
                    break
                result += next_char
                prefix = (prefix + next_char)[-self.order:]
            else:
                continue  # passou do tamanho máximo sem terminar

            if len(result) < min_length or re.search(r"(.{3,})\1", result):
                continue  # curto demais ou com trecho repetido (pippippa)
            if any(result.count(sep) > n for sep, n in self.max_separators.items()):
                continue  # mais hífens/apóstrofos do que qualquer nome do treino
            is_new = result not in self.training_names and result not in self.generated_names
            if is_new and (accept is None or accept(result)):
                fallback = result
                break
            # Reserva: o primeiro válido, trocado pelo primeiro inédito que surgir
            if fallback is None or (is_new and not fallback_is_new):
                fallback, fallback_is_new = result, is_new

        name = fallback or "aelith"
        self.generated_names.add(name)
        return self._capitalize(name)

    def _capitalize(self, name: str) -> str:
        """Capitaliza cada parte separada por hífen (dol-makjar → Dol-Makjar),
        exceto as que o treino escreve em minúscula (khazad-dun → Khazad-dun)."""
        first, *rest = name.split("-")
        # Parte que não existe no treino segue o estilo mais comum dele
        lower_by_default = len(self.lowercase_parts) > len(self.capitalized_parts)
        parts = [first.capitalize()]
        for part in rest:
            keep_lower = part in self.lowercase_parts or (
                lower_by_default and part not in self.capitalized_parts)
            parts.append(part if keep_lower else part.capitalize())
        return "-".join(parts)


# ============================================================
# CLASSE: GERADOR HÍBRIDO (SÍLABAS + MARKOV)
# ============================================================

class HybridGenerator:
    """
    Combina geração por sílabas, Markov e os bancos de nomes (.csv).
    O Markov é treinado com os exemplos de cada língua + os nomes do banco.
    """

    def __init__(self, seed: Optional[int] = None, database: Optional[NameDatabase] = None):
        self.syllable_gen = NameGenerator(seed)
        self.rng = random.Random(seed)
        self.database = database if database is not None else NameDatabase(seed=seed)
        # (língua, gênero ou None) → Markov de nomes pessoais
        self.markov_gens: Dict[Tuple[str, Optional[str]], MarkovNameGenerator] = {}
        # língua → Markov de nomes de lugares
        self.place_markov_gens: Dict[str, MarkovNameGenerator] = {}
        self._trained = False

    def train_from_examples(self):
        """Treina um Markov por língua (e por gênero) com exemplos + banco de nomes."""
        for lang, data in LANGUAGES.items():
            everyone = MarkovNameGenerator(seed=self.rng.random())
            everyone.train(data.get("examples", []))
            everyone.train(self.database.personal_names(lang))
            self.markov_gens[(lang, None)] = everyone

            for gender in self.database.personal.get(lang, {}):
                markov = MarkovNameGenerator(seed=self.rng.random())
                markov.train(self.database.personal_names(lang, gender))
                self.markov_gens[(lang, gender)] = markov

            places = MarkovNameGenerator(seed=self.rng.random())
            places.train(self.database.place_names(lang))
            self.place_markov_gens[lang] = places
        self._trained = True

    def _markov_name(self, language: str, gender: Optional[str] = None) -> str:
        if not self._trained:
            self.train_from_examples()
        markov = self.markov_gens.get((language, normalize_gender(gender)))
        return (markov or self.markov_gens[(language, None)]).generate()

    def generate(self, race: str, method: str = "auto", gender: Optional[str] = None) -> str:
        """
        Gera um nome pessoal usando o método especificado.
        method: 'syllable', 'markov', 'database', 'auto'
        gender: None, 'male'/'masculino' ou 'female'/'feminino' (Markov e banco)
        """
        language = language_for_race(race)
        if not language:
            raise ValueError(f"Raça desconhecida: {race}")

        if method == "auto":
            roll = self.rng.random()
            method = "syllable" if roll < 0.5 else "markov" if roll < 0.85 else "database"

        if method == "syllable":
            return self.syllable_gen.generate_syllable_name(language)
        elif method == "markov":
            return self._markov_name(language, gender)
        elif method == "database":
            name = self.database.random_personal(language, gender)
            return name or self._markov_name(language, gender)
        raise ValueError(f"Método desconhecido: {method}")

    def generate_full_name(
        self,
        race: str,
        method: str = "auto",
        gender: Optional[str] = None,
        include_family: bool = True,
    ) -> Dict[str, str]:
        """Nome completo (nome + sobrenome) com o nome pessoal vindo do método escolhido."""
        full = self.syllable_gen.generate_full_name(race, include_family=include_family)
        full["first_name"] = self.generate(race, method, gender)
        full["full_name"] = " ".join(p for p in (full["first_name"], full["family_name"]) if p)
        return full

    def generate_place(self, race: str, place_type: str = "city", method: str = "auto") -> str:
        """
        Gera um nome de lugar.
        method: 'syllable', 'markov', 'database', 'auto'
        """
        language = language_for_race(race)
        if not language:
            raise ValueError(f"Raça desconhecida: {race}")

        if method not in ("auto", "syllable", "markov", "database"):
            raise ValueError(f"Método desconhecido: {method}")
        has_places = bool(self.database.place_names(language))
        if method == "auto":
            roll = self.rng.random()
            method = "syllable" if roll < 0.4 or not has_places else "markov" if roll < 0.8 else "database"

        if method == "syllable" or not has_places:
            return self.syllable_gen.generate_place_name(race, place_type)
        elif method == "markov":
            if not self._trained:
                self.train_from_examples()
            # O Markov mistura todos os tipos; prefere nomes que comecem ou
            # terminem como os do tipo pedido no banco (ex.: "-dun" em minas)
            same_type = [n.lower() for n in self.database.place_names(language, place_type)]
            starts = {n[:4] for n in same_type}
            ends = {n[-4:] for n in same_type}

            def looks_like_type(name: str) -> bool:
                return not same_type or name[:4] in starts or name[-4:] in ends

            return self.place_markov_gens[language].generate(
                max_length=16, min_length=5, accept=looks_like_type)
        return self.database.random_place(language, place_type)

# menu.py
"""
Menu interativo do gerador de nomes.
Rode com:  python menu.py   (ou dê dois cliques em "Gerar Nomes.bat")
"""
import os
import sys
from datetime import datetime

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from namegen import HybridGenerator, LANGUAGES  # noqa: E402
from namegen.syllable_data import language_for_race  # noqa: E402

SAVE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nomes_salvos.txt")

RACES = [
    ("Humano", "human"),
    ("Elfo", "elf"),
    ("Anão", "dwarf"),
    ("Halfling", "halfling"),
    ("Gnomo", "gnome"),
    ("Orc", "orc"),
    ("Goblin", "goblin"),
    ("Fae", "fae"),
    ("Dragão", "dragon"),
    ("Demônio", "daemon"),
    ("Povo-bicho", "beastfolk"),
]

GENDERS = [
    ("Tanto faz", None),
    ("Masculino", "male"),
    ("Feminino", "female"),
]

# Quantos nomes cada geração mostra
NAME_COUNT = 10

PLACE_TYPES = [
    ("Cidade", "city"),
    ("Vila", "town"),
    ("Aldeia", "village"),
    ("Fortaleza", "fortress"),
    ("Floresta", "forest"),
    ("Montanha", "mountain"),
    ("Rio", "river"),
    ("Região", "region"),
    ("Colina", "hill"),
    ("Vale", "valley"),
    ("Mina", "mine"),
    ("Abismo", "abyss"),
    ("Trono", "throne"),
]


class Back(Exception):
    """Usuário pediu para voltar ao menu principal."""


# ------------------------------------------------------------
# Entrada e tela
# ------------------------------------------------------------

def clear():
    os.system("cls" if os.name == "nt" else "clear")


def header(title: str):
    clear()
    print("=" * 50)
    print(f"  {title}")
    print("=" * 50)
    print()


def ask(prompt: str) -> str:
    return input(prompt).strip()


def choose(title: str, options, default: int = 1, labels=None):
    """Mostra opções numeradas e devolve o valor escolhido (V volta ao menu)."""
    print(f"{title}")
    for i, (label, _) in enumerate(options, 1):
        extra = f"  ({labels[i - 1]})" if labels else ""
        print(f"  {i:2d}. {label}{extra}")
    while True:
        answer = ask(f"Escolha [Enter = {default}, V = voltar]: ").lower()
        if answer == "v":
            raise Back
        if answer == "":
            return options[default - 1][1], options[default - 1][0]
        if answer.isdigit() and 1 <= int(answer) <= len(options):
            label, value = options[int(answer) - 1]
            return value, label
        print("  Opção inválida, tente de novo.")


def race_labels():
    return [LANGUAGES[language_for_race(key)]["name"] for _, key in RACES]


# ------------------------------------------------------------
# Resultados
# ------------------------------------------------------------

def save(names, description: str):
    stamp = datetime.now().strftime("%d/%m/%Y %H:%M")
    with open(SAVE_FILE, "a", encoding="utf-8") as f:
        f.write(f"# {description} — {stamp}\n")
        for name in names:
            f.write(f"{name}\n")
        f.write("\n")
    print(f"\n  Salvo em {os.path.basename(SAVE_FILE)}")


def show_results(title: str, description: str, make_names):
    """Mostra os nomes e permite gerar mais / salvar / voltar."""
    while True:
        names = make_names()
        header(title)
        print(f"  {description}\n")
        for i, name in enumerate(names, 1):
            print(f"  {i:3d}. {name}")
        print()
        print("  [Enter] gerar outros   [S] salvar estes   [M] menu principal")
        while True:
            answer = ask("> ").lower()
            if answer == "":
                break
            if answer == "s":
                save(names, description)
                continue
            if answer in ("m", "v"):
                return
            print("  Opção inválida.")


# ------------------------------------------------------------
# Opções do menu
# ------------------------------------------------------------

def menu_character(hybrid: HybridGenerator, full: bool):
    title = "NOME DE PERSONAGEM" if full else "PRIMEIRO NOME"
    header(title)
    race, race_label = choose("Raça:", RACES, labels=race_labels())
    print()
    gender, gender_label = choose("Gênero:", GENDERS)

    if full:
        def make_names():
            return [hybrid.generate_full_name(race, "auto", gender)["full_name"] for _ in range(NAME_COUNT)]
    else:
        def make_names():
            return [hybrid.generate(race, "auto", gender) for _ in range(NAME_COUNT)]

    description = f"{race_label} · {gender_label}"
    show_results(title, description, make_names)


def menu_place(hybrid: HybridGenerator):
    title = "NOME DE LUGAR"
    header(title)
    race, race_label = choose("De qual povo?", RACES, labels=race_labels())
    print()
    place_type, type_label = choose("Tipo de lugar:", PLACE_TYPES)

    def make_names():
        return [hybrid.generate_place(race, place_type, "auto") for _ in range(NAME_COUNT)]

    description = f"{type_label} · {race_label}"
    show_results(title, description, make_names)


def menu_languages(hybrid: HybridGenerator):
    header("LÍNGUAS E RAÇAS")
    for key, data in LANGUAGES.items():
        races = [label for label, race in RACES if language_for_race(race) == key]
        personal = len(hybrid.database.personal_names(key))
        places = len(hybrid.database.place_names(key))
        print(f"  {data['name']:12s} {', '.join(races)}")
        print(f"  {'':12s} banco: {personal} nomes pessoais, {places} lugares")
        print()
    ask("[Enter] voltar ")


def main():
    hybrid = HybridGenerator()
    options = {
        "1": ("Nome de personagem (nome + sobrenome)", lambda: menu_character(hybrid, full=True)),
        "2": ("Só o primeiro nome", lambda: menu_character(hybrid, full=False)),
        "3": ("Nome de lugar", lambda: menu_place(hybrid)),
        "4": ("Ver línguas e raças", lambda: menu_languages(hybrid)),
    }
    while True:
        header("GERADOR DE NOMES DE RPG")
        for key, (label, _) in options.items():
            print(f"  {key}. {label}")
        print("  0. Sair")
        print()
        answer = ask("Escolha: ")
        if answer == "0":
            break
        if answer in options:
            try:
                options[answer][1]()
            except Back:
                pass


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        pass
    print("\nAté a próxima!")
